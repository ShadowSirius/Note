#!/usr/bin/env python3
"""
Generate Continuous Japanese Chunking, Daily Dialogue, & Vocabulary Immersion Audio for Obsidian Notes.
Powered by Microsoft Edge Neural TTS (edge-tts) & ffmpeg.
Directly reads Japanese sentences/words without unnecessary titles, section names, or outros.
"""

import os
import re
import sys
import shutil
import asyncio
import tempfile
import argparse
import subprocess
from pathlib import Path

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

VOICE_DEFAULT = "ja-JP-NanamiNeural"

def clean_japanese_text(raw_text: str) -> str:
    """Clean markdown/html tags, ruby tags, and Chinese explanations from Japanese sentences for Chunking cards."""
    text = re.sub(r"<rt>.*?</rt>", "", raw_text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("*", "").replace("_", "")
    text = re.sub(r"^\s*\d+\.\s*", "", text)
    text = re.sub(r"^\s*\[[^\]]+\]\s*", "", text)
    text = re.sub(r"\s*[—–-].*$", "", text)
    text = re.sub(r"\s*（.*?）.*$", "", text)
    text = re.sub(r"\s*\(.*?\).*$", "", text)
    text = re.sub(r"\s*/\s*", "、", text)
    return text.strip()

def clean_dialogue_line(text: str) -> str:
    """Clean dialogue text for pure spoken immersion."""
    text = re.sub(r"<rt>.*?</rt>", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"^[>\s*]*", "", text)
    # Remove speaker prefixes: A:, **A**:, 美容師:, 旅客（打電話到櫃台）:, etc.
    text = re.sub(r"^\*?\*?[^\s:：]{1,15}(?:（[^）]+）|\([^)]+\))?\*?\*?[:：]\s*", "", text)
    # Remove kana furigana in parentheses, e.g. 7時（じ）, 起（お）きて, 目覚（めざ）まし時計（どけい）
    text = re.sub(r"[（\(][ぁ-んァ-ヶー\s・]+[）\)]", "", text)
    text = text.replace("*", "").replace("_", "")
    stripped = text.strip()
    if re.match(r"^[（\(].*?[）\)]$", stripped):
        return ""
    text = re.sub(r"[（\(][^）\)]*[\u4e00-\u9fff]+[^）\)]*[）\)]\s*$", "", text)
    text = re.sub(r"\s*/\s*", "、", text)
    return text.strip()

def clean_vocab_line(text: str) -> str:
    """Clean vocabulary text for pure spoken immersion."""
    text = re.sub(r"<rt>.*?</rt>", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"^[>\s*]*", "", text)
    text = re.sub(r"[（\(][ぁ-んァ-ヶー\s・]+[）\)]", "", text)
    text = text.replace("*", "").replace("_", "")
    text = re.sub(r"[（\(][^）\)]*[\u4e00-\u9fff]+[^）\)]*[）\)]\s*$", "", text)
    text = re.sub(r"\s*/\s*", "、", text)
    return text.strip()

def get_silence_file(cache_dir: Path, duration: float) -> Path:
    """Generate or retrieve a silence mp3 of given duration."""
    dur_str = str(duration).replace(".", "_")
    silence_file = cache_dir / f"silence_{dur_str}.mp3"
    if not silence_file.exists():
        cmd = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
            "-t", str(duration),
            "-q:a", "9", "-acodec", "libmp3lame",
            str(silence_file)
        ]
        subprocess.run(cmd, check=True)
    return silence_file

async def generate_speech_clip(text: str, output_path: Path, voice: str, sem: asyncio.Semaphore, max_retries: int = 3):
    """Generate a single speech mp3 using edge-tts with semaphore concurrency and retry logic."""
    import edge_tts
    if output_path.exists() and output_path.stat().st_size > 0:
        return
    for attempt in range(max_retries):
        try:
            async with sem:
                communicate = edge_tts.Communicate(text=text, voice=voice)
                await communicate.save(str(output_path))
            return
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Failed clip: {text[:20]} -> {e}", file=sys.stderr)
                raise
            await asyncio.sleep(1.0 * (attempt + 1))

async def synthesize_track(playlist_spec, output_mp3, cache_dir, voice=VOICE_DEFAULT):
    """Synthesize audio track from a list of (text, pause_after_seconds) tuples directly."""
    if not playlist_spec:
        return
    cache_dir.mkdir(parents=True, exist_ok=True)
    playlist = []
    speech_tasks = []
    seq = 0
    for text, pause_after in playlist_spec:
        seq += 1
        clip = cache_dir / f"clip_{seq:04d}.mp3"
        speech_tasks.append((text, clip))
        playlist.append(clip)
        if pause_after > 0:
            playlist.append(get_silence_file(cache_dir, pause_after))
            
    sem = asyncio.Semaphore(10)
    tasks = [generate_speech_clip(t, p, voice, sem) for t, p in speech_tasks]
    await asyncio.gather(*tasks)
    
    concat_list = cache_dir / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for p in playlist:
            f.write(f"file '{p.resolve().as_posix()}'\n")
            
    output_mp3.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c:a", "libmp3lame", "-b:a", "48k", "-ac", "1", "-ar", "24000",
        str(output_mp3)
    ]
    subprocess.run(cmd, check=True)
    shutil.rmtree(cache_dir, ignore_errors=True)

def extract_table_rows(table_markdown: str):
    """Extract (prompt, response) pairs from markdown table, strictly skipping headers and validating Japanese."""
    lines = [l.strip() for l in table_markdown.splitlines() if l.strip().startswith("|")]
    data = []
    seen_sep = False
    for line in lines:
        if re.match(r"^\|\s*:?-+\s*\|", line):
            seen_sep = True
            continue
        if not seen_sep:
            continue
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) >= 2:
            p1 = clean_japanese_text(parts[0])
            p2 = clean_japanese_text(parts[1])
            if p1 and p2 and re.search(r"[\u3040-\u30ff]", p1) and re.search(r"[\u3040-\u30ff]", p2):
                data.append((p1, p2))
    return data

def parse_chunking_card(filepath: Path) -> dict:
    """Parse a chunking daily markdown file into structured audio sections."""
    content = filepath.read_text(encoding="utf-8")
    
    title_match = re.search(r"^title:\s*['\"]?(?:Day\s*(\d+)[:：]\s*)?(.*?)['\"]?$", content, re.MULTILINE)
    day_num = int(title_match.group(1)) if title_match and title_match.group(1) else 1
    day_title = title_match.group(2).strip() if title_match else ""
    
    patterns = []
    pattern_blocks = re.findall(
        r"###\s*<span[^>]*>(Pattern\s*\d+)</span>[：:]\s*(.*?)\n(.*?)(?=\n###|\n##|\Z)",
        content,
        re.DOTALL
    )
    for p_id, p_name, p_body in pattern_blocks:
        sentences = []
        for line in p_body.strip().split("\n"):
            line = line.strip()
            if re.match(r"^\d+\.\s*\[", line):
                clean_s = clean_japanese_text(line)
                if clean_s and re.search(r"[\u3040-\u30ff]", clean_s):
                    sentences.append(clean_s)
        patterns.append({
            "id": p_id,
            "sentences": sentences
        })
    
    drills = {"base": "", "substitutions": [], "transformations": []}
    base_match = re.search(r"\* \*\*Base Sentence\*\*：(.*?)\n", content)
    if base_match:
        b_clean = clean_japanese_text(base_match.group(1))
        if b_clean and re.search(r"[\u3040-\u30ff]", b_clean):
            drills["base"] = b_clean
    
    sub_table = re.search(r"### 1️⃣ Substitution Drill.*?\n(.*?)(?=\n###|\n##|\Z)", content, re.DOTALL)
    if sub_table:
        drills["substitutions"] = extract_table_rows(sub_table.group(1))
    
    trans_table = re.search(r"### 2️⃣ Transformation Drill.*?\n(.*?)(?=\n###|\n##|\Z)", content, re.DOTALL)
    if trans_table:
        drills["transformations"] = extract_table_rows(trans_table.group(1))
                        
    return {
        "day_num": day_num,
        "day_title": day_title,
        "patterns": patterns,
        "drills": drills
    }

async def build_chunking_track(data: dict, output_mp3: Path, cache_dir: Path, voice: str = VOICE_DEFAULT):
    """Build the continuous audio track for a Day's chunking card (Folder 24) with pure sentence immersion."""
    playlist_spec = []
    # 1. Pure pattern sentences
    for pattern in data["patterns"]:
        for s in pattern["sentences"]:
            playlist_spec.append((s, 1.4))
            
    # 2. Pure drill practice
    drills = data["drills"]
    if drills["base"]:
        playlist_spec.append((drills["base"], 1.6))
    for prompt, resp in drills["substitutions"]:
        playlist_spec.append((prompt, 1.6))
        playlist_spec.append((resp, 1.4))
    for orig, trans in drills["transformations"]:
        playlist_spec.append((orig, 1.6))
        playlist_spec.append((trans, 1.4))
        
    await synthesize_track(playlist_spec, output_mp3, cache_dir, voice=voice)
    print(f"[Chunking] Generated: {output_mp3.name}")

def parse_vocabulary_card(file_path: Path):
    """Parse Daily Vocabulary markdown into dialogue and vocabulary lists."""
    content = file_path.read_text("utf-8")
    m = re.search(r"Day(\d+)_", file_path.name)
    day_num = int(m.group(1)) if m else 1
    
    dialogues = []
    vocab_items = []
    
    if day_num == 33:
        recall_sentences = []
        diff_items = []
        practical_sentences = []
        for line in content.splitlines():
            if "解答：" in line or "解答:" in line:
                ans = line.split("解答：")[-1].split("解答:")[-1]
                cl = clean_vocab_line(ans)
                if cl:
                    recall_sentences.append(cl)
            elif line.strip().startswith("* **") and ("：" in line or ":" in line):
                m_diff = re.match(r"\s*\*\s*\*\*(.*?)\*\*(?:[（\(].*?[）\)])?[:：]\s*(.*)", line)
                if m_diff:
                    w = clean_vocab_line(m_diff.group(1))
                    ex = clean_vocab_line(m_diff.group(2))
                    if w != "解答" and w and ex and re.search(r"[\u3040-\u30ff]", ex):
                        diff_items.append((w, ex))
            elif line.strip().startswith("* ") and not line.strip().startswith("* **"):
                ex = clean_vocab_line(line)
                if ex and re.search(r"[\u3040-\u30ff]", ex) and len(ex) > 10:
                    practical_sentences.append(ex)
        return {
            "day_num": day_num,
            "dialogues": [],
            "vocab_items": [],
            "is_day_33": True,
            "recall": recall_sentences,
            "diff": diff_items,
            "practical": practical_sentences
        }

    if day_num == 34:
        in_dia = False
        for line in content.splitlines():
            if line.startswith("## 一、"):
                in_dia = True
                continue
            elif line.startswith("## 二、"):
                in_dia = False
            if in_dia:
                cl = clean_dialogue_line(line)
                if cl and re.search(r"[\u3040-\u30ff]", cl):
                    dialogues.append(cl)
            else:
                m_v = re.match(r"^\s*\d+\.\s*\*\*(.*?)\*\*(?:[（\(].*?[）\)])?[:：]\s*(.*?)(?:[（\(][^）\)]*[\u4e00-\u9fff]+.*|$)", line)
                if m_v:
                    w = clean_vocab_line(m_v.group(1))
                    c = clean_vocab_line(m_v.group(2))
                    if w and c:
                        vocab_items.append((w, c))
        return {
            "day_num": day_num,
            "dialogues": dialogues,
            "vocab_items": vocab_items,
            "is_day_33": False
        }

    in_dia = False
    for line in content.splitlines():
        if line.startswith("## 第一部分"):
            in_dia = True
            continue
        elif line.startswith("## 第二部分"):
            in_dia = False
            
        if in_dia:
            cl = clean_dialogue_line(line)
            if cl and re.search(r"[\u3040-\u30ff]", cl):
                dialogues.append(cl)
        else:
            if line.startswith("|") and not line.startswith("| 編號") and not line.startswith("|:--") and not line.startswith("|---"):
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 4 and parts[0].isdigit():
                    w_match = re.search(r"\*\*(.*?)\*\*", parts[1])
                    w = clean_vocab_line(w_match.group(1) if w_match else parts[1])
                    c_match = re.search(r"\*\*(.*?)\*\*", parts[3])
                    c = clean_vocab_line(c_match.group(1) if c_match else parts[3])
                    if w and c:
                        vocab_items.append((w, c))
                        
    return {
        "day_num": day_num,
        "dialogues": dialogues,
        "vocab_items": vocab_items,
        "is_day_33": False
    }

def update_note_callout(note_path: Path, mp3_filename: str):
    """Ensure standard Chunking note embeds audio player."""
    content = note_path.read_text(encoding="utf-8")
    embed_target = f"![[{mp3_filename}]]"
    new_callout = f"> [!audio] 🎧 {mp3_filename}\n> {embed_target}"

    pattern_existing = r"> \[!audio\][^\n]*\n> !\[\[" + re.escape(mp3_filename) + r"\]\]"
    if re.search(pattern_existing, content):
        new_content = re.sub(pattern_existing, new_callout, content, count=1)
        if new_content != content:
            note_path.write_text(new_content, encoding="utf-8")
        return

    if embed_target in content:
        pattern_solo = r"(?:> \[!audio\][^\n]*\n)?(?:\s*>?\s*)?" + re.escape(embed_target)
        new_content = re.sub(pattern_solo, new_callout, content, count=1)
        note_path.write_text(new_content, encoding="utf-8")
        return

    abstract_pattern = r"(> \[!abstract\][^\n]*\n(?:> [^\n]*\n)+)"
    if re.search(abstract_pattern, content):
        new_content = re.sub(abstract_pattern, rf"\1\n{new_callout}\n", content, count=1)
    else:
        new_content = re.sub(r"(# [^\n]+\n)", rf"\1\n{new_callout}\n\n", content, count=1)

    note_path.write_text(new_content, encoding="utf-8")

def update_vocabulary_note_markdown(file_path: Path):
    """Ensure Daily Vocabulary note embeds Dialogue audio at Part 1 and Vocabulary audio at Part 2."""
    content = file_path.read_text("utf-8")
    m = re.search(r"Day(\d+)_", file_path.name)
    if not m:
        return
    day_num = int(m.group(1))
    vocab_mp3 = f"Day_{day_num:02d}_Vocabulary_Immersion.mp3"
    dialogue_mp3 = f"Day_{day_num:02d}_Dialogue_Immersion.mp3"
    
    vocab_callout = f"> [!audio] 🎧 {vocab_mp3}\n> ![[{vocab_mp3}]]"
    dialogue_callout = f"> [!audio] 🎧 {dialogue_mp3}\n> ![[{dialogue_mp3}]]"
    
    content = re.sub(r">\s*\[!audio\][^\n]*\n>\s*!\[\[[^\]]+\]\]\n*", "", content)
    content = re.sub(r"!\[\[Day_\d+_(?:Vocabulary|Dialogue)_Immersion\.mp3\]\]\n*", "", content)
    
    if day_num == 33:
        content = re.sub(r"(## 一、[^\n]*\n+)", rf"\1{vocab_callout}\n\n", content, count=1)
    elif day_num == 34:
        content = re.sub(r"(## 一、[^\n]*\n+)", rf"\1{dialogue_callout}\n\n", content, count=1)
        content = re.sub(r"(## 二、[^\n]*\n+)", rf"\1{vocab_callout}\n\n", content, count=1)
    else:
        content = re.sub(r"(## 第一部分[^\n]*\n+)", rf"\1{dialogue_callout}\n\n", content, count=1)
        content = re.sub(r"(## 第二部分[^\n]*\n+)", rf"\1{vocab_callout}\n\n", content, count=1)
        
    file_path.write_text(content, encoding="utf-8")

def update_all_vault_callout_titles(vault_root: Path):
    """Scan both Chunking and Daily Vocabulary directories and normalize all audio callouts."""
    chunking_dir = vault_root / "HML_Wiki" / "concepts" / "24_Chunking_語塊與聽力自動化"
    vocab_dir = vault_root / "HML_Wiki" / "concepts" / "23_Daily_Vocabulary_生活單字與對話"
    
    count = 0
    if chunking_dir.exists():
        for note_file in sorted(chunking_dir.glob("Day_*_Chunking_Training.md")):
            m = re.search(r"Day_(\d+)_Chunking_Training\.md", note_file.name)
            if m:
                day_num = int(m.group(1))
                mp3_name = f"Day_{day_num:02d}_Chunking_Immersion.mp3"
                update_note_callout(note_file, mp3_name)
                count += 1
                
    if vocab_dir.exists():
        for note_file in sorted(vocab_dir.glob("Day*.md")):
            update_vocabulary_note_markdown(note_file)
            count += 1
                
    print(f"Callout normalization complete across {count} notes.")

async def process_chunking(vault_root: Path, days: list = None, force: bool = False, voice: str = VOICE_DEFAULT):
    chunking_dir = vault_root / "HML_Wiki" / "concepts" / "24_Chunking_語塊與聽力自動化"
    audio_dir = chunking_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    all_notes = sorted(chunking_dir.glob("Day_*_Chunking_Training.md"))
    base_tmp = Path(tempfile.gettempdir()) / "obsidian_chunking_cache"
    
    for note_file in all_notes:
        m = re.search(r"Day_(\d+)_Chunking_Training\.md", note_file.name)
        if not m:
            continue
        day_num = int(m.group(1))
        if days is not None and day_num not in days:
            continue
            
        mp3_name = f"Day_{day_num:02d}_Chunking_Immersion.mp3"
        output_mp3 = audio_dir / mp3_name
        update_note_callout(note_file, mp3_name)
        
        if output_mp3.exists() and output_mp3.stat().st_size > 0 and not force:
            continue
            
        print(f"[Chunking] Generating Day {day_num:02d} ({note_file.name})...")
        data = parse_chunking_card(note_file)
        cache_dir = base_tmp / f"day_{day_num:02d}"
        await build_chunking_track(data, output_mp3, cache_dir, voice=voice)

async def process_vocabulary(vault_root: Path, days: list = None, force: bool = False, voice: str = VOICE_DEFAULT):
    vocab_dir = vault_root / "HML_Wiki" / "concepts" / "23_Daily_Vocabulary_生活單字與對話"
    audio_dir = vocab_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    all_notes = sorted(vocab_dir.glob("Day*.md"))
    cache_base = Path(tempfile.gettempdir()) / "obsidian_vocab_audio"
    
    for note_path in all_notes:
        m = re.search(r"Day(\d+)_", note_path.name)
        if not m:
            continue
        day_num = int(m.group(1))
        if days is not None and day_num not in days:
            continue
            
        data = parse_vocabulary_card(note_path)
        
        # Dialogue Track
        if data["dialogues"]:
            dia_mp3 = audio_dir / f"Day_{day_num:02d}_Dialogue_Immersion.mp3"
            if not dia_mp3.exists() or dia_mp3.stat().st_size == 0 or force:
                dia_spec = [(d, 1.3) for d in data["dialogues"]]
                await synthesize_track(dia_spec, dia_mp3, cache_base / f"d{day_num:02d}_dia", voice=voice)
                print(f"[Dialogue] Generated: {dia_mp3.name}")
                
        # Vocabulary Track
        voc_mp3 = audio_dir / f"Day_{day_num:02d}_Vocabulary_Immersion.mp3"
        if not voc_mp3.exists() or voc_mp3.stat().st_size == 0 or force:
            voc_spec = []
            if data.get("is_day_33"):
                for s in data["recall"]:
                    voc_spec.append((s, 1.5))
                for w, ex in data["diff"]:
                    voc_spec.append((w, 0.7))
                    voc_spec.append((ex, 1.4))
                for p in data["practical"]:
                    voc_spec.append((p, 1.5))
            else:
                for w, c in data["vocab_items"]:
                    voc_spec.append((w, 0.7))
                    voc_spec.append((c, 1.3))
            if voc_spec:
                await synthesize_track(voc_spec, voc_mp3, cache_base / f"d{day_num:02d}_voc", voice=voice)
                print(f"[Vocabulary] Generated: {voc_mp3.name}")
                
        update_vocabulary_note_markdown(note_path)

async def main():
    parser = argparse.ArgumentParser(description="Generate Audio Immersion for Chunking (24) & Vocabulary (23)")
    parser.add_argument("--target", choices=["all", "chunking", "vocab", "24", "23"], default="all")
    parser.add_argument("--day", type=int, default=None)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--update-titles-only", action="store_true")
    parser.add_argument("--voice", type=str, default=VOICE_DEFAULT)
    parser.add_argument("--vault-root", type=str, default=".")
    args = parser.parse_args()

    vault_root = Path(args.vault_root).resolve()
    if args.update_titles_only:
        update_all_vault_callout_titles(vault_root)
        return

    days_filter = [args.day] if args.day is not None else None

    if args.target in ["all", "chunking", "24"]:
        await process_chunking(vault_root, days=days_filter, force=args.force, voice=args.voice)

    if args.target in ["all", "vocab", "23"]:
        await process_vocabulary(vault_root, days=days_filter, force=args.force, voice=args.voice)

    update_all_vault_callout_titles(vault_root)
    print("Completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())
