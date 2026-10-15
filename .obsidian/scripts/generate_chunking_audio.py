#!/usr/bin/env python3
"""
Generate Continuous Japanese Chunking Immersion Audio for Obsidian Notes (Day 01 - Day 99+).
Powered by Microsoft Edge Neural TTS (edge-tts) & ffmpeg.
"""

import os
import re
import sys
import shutil
import asyncio
import argparse
import subprocess
from pathlib import Path

VOICE_DEFAULT = "ja-JP-NanamiNeural"

def num_to_japanese_kanji(n: int) -> str:
    """Convert integer (1..99) to Japanese kanji reading for TTS announcement."""
    digits = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八", 9: "九"}
    if n <= 0:
        return str(n)
    if n < 10:
        return digits[n]
    if n == 10:
        return "十"
    if n < 20:
        return "十" + digits[n - 10]
    if n < 100:
        tens, rem = divmod(n, 10)
        return digits[tens] + "十" + (digits[rem] if rem else "")
    return str(n)

def clean_japanese_text(raw_text: str) -> str:
    """Clean markdown/html tags, ruby tags, and Chinese explanations from Japanese sentences."""
    text = re.sub(r"<rt>.*?</rt>", "", raw_text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"^\s*\d+\.\s*", "", text)
    text = re.sub(r"^\s*\[[^\]]+\]\s*", "", text)
    text = re.sub(r"\s*[—–-].*$", "", text)
    text = re.sub(r"\s*（.*?）.*$", "", text)
    text = re.sub(r"\s*\(.*?\).*$", "", text)
    text = re.sub(r"\s*/\s*", "、", text)
    text = text.strip()
    return text

def extract_markdown_table_rows(table_block: str):
    """Extract (col1, col2) rows from a Markdown table, skipping the header and separator lines."""
    lines = [line.strip() for line in table_block.split("\n") if line.strip().startswith("|")]
    data_rows = []
    seen_separator = False
    for line in lines:
        if re.match(r"^\|\s*:?-+\s*\|", line):
            seen_separator = True
            continue
        if not seen_separator:
            continue
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) >= 2:
            c1 = clean_japanese_text(parts[0])
            c2 = clean_japanese_text(parts[1])
            if c1 and c2:
                data_rows.append((c1, c2))
    return data_rows

def parse_day_card(filepath: Path):
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
                if clean_s:
                    sentences.append(clean_s)
        
        p_name_clean = clean_japanese_text(p_name)
        patterns.append({
            "id": p_id,
            "name": p_name_clean,
            "sentences": sentences
        })
    
    drills = {"base": "", "substitutions": [], "transformations": []}
    
    base_match = re.search(r"\* \*\*Base Sentence\*\*：(.*?)\n", content)
    if base_match:
        drills["base"] = clean_japanese_text(base_match.group(1))
    
    sub_table = re.search(r"### 1️⃣ Substitution Drill.*?\n(.*?)(?=\n###|\n##|\Z)", content, re.DOTALL)
    if sub_table:
        drills["substitutions"] = extract_markdown_table_rows(sub_table.group(1))
    
    trans_table = re.search(r"### 2️⃣ Transformation Drill.*?\n(.*?)(?=\n###|\n##|\Z)", content, re.DOTALL)
    if trans_table:
        drills["transformations"] = extract_markdown_table_rows(trans_table.group(1))
                        
    return {
        "day_num": day_num,
        "day_title": day_title,
        "patterns": patterns,
        "drills": drills
    }

def get_silence_file(cache_dir: Path, duration: float) -> Path:
    silence_file = cache_dir / f"silence_{str(duration).replace('.', '_')}.mp3"
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

async def generate_speech_clip(text: str, output_path: Path, voice: str, sem: asyncio.Semaphore):
    import edge_tts
    if not output_path.exists():
        async with sem:
            communicate = edge_tts.Communicate(text=text, voice=voice)
            await communicate.save(str(output_path))

async def build_continuous_track(data: dict, output_mp3: Path, cache_dir: Path, voice: str = VOICE_DEFAULT):
    cache_dir.mkdir(parents=True, exist_ok=True)
    playlist = []
    speech_tasks = []
    
    seq = 0
    def add_speech(text: str, pause_after: float = 1.5):
        nonlocal seq
        seq += 1
        clip_path = cache_dir / f"clip_{seq:03d}.mp3"
        speech_tasks.append((text, clip_path))
        playlist.append(clip_path)
        if pause_after > 0:
            playlist.append(get_silence_file(cache_dir, pause_after))

    day_str = num_to_japanese_kanji(data['day_num'])
    add_speech(f"デイ{day_str}、語塊トレーニング。", pause_after=1.8)
    
    p_num_kanji = ["一", "二", "三", "四"]
    for idx, pattern in enumerate(data["patterns"]):
        p_num = p_num_kanji[idx] if idx < len(p_num_kanji) else str(idx + 1)
        p_title = f"パターン{p_num}、{pattern['name']}。"
        add_speech(p_title, pause_after=1.6)
        
        for s in pattern["sentences"]:
            add_speech(s, pause_after=1.5)
            
        playlist.append(get_silence_file(cache_dir, 1.2))
        
    drills = data["drills"]
    if drills["base"] or drills["substitutions"] or drills["transformations"]:
        add_speech("スピードドリル、意群代入練習。", pause_after=1.5)
        if drills["base"]:
            add_speech(f"基本文、{drills['base']}", pause_after=1.8)
            
        for prompt, resp in drills["substitutions"]:
            add_speech(prompt, pause_after=1.8)
            add_speech(resp, pause_after=1.5)
            
        if drills["transformations"]:
            add_speech("語体変換と、文末アンカー練習。", pause_after=1.5)
            for orig, trans in drills["transformations"]:
                add_speech(orig, pause_after=1.8)
                add_speech(trans, pause_after=1.5)
                
    add_speech(f"お疲れ様でした。デイ{day_str}のトレーニングは終了です。", pause_after=0.5)

    sem = asyncio.Semaphore(6)
    tasks = [generate_speech_clip(t, p, voice, sem) for t, p in speech_tasks]
    await asyncio.gather(*tasks)

    concat_list = cache_dir / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for p in playlist:
            f.write(f"file '{p.resolve()}'\n")
            
    output_mp3.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c:a", "libmp3lame", "-b:a", "128k",
        str(output_mp3)
    ]
    subprocess.run(cmd, check=True)
    print(f"Generated continuous audio track: {output_mp3}")

def update_note_with_audio_embed(note_path: Path, mp3_filename: str):
    content = note_path.read_text(encoding="utf-8")
    embed_line = f"![[{mp3_filename}]]"
    
    if embed_line in content:
        print(f"Note {note_path.name} already contains {mp3_filename}.")
        return
        
    callout_block = f"""
> [!audio] 🎧 本日磨耳朵・影子跟讀沉浸音軌 (Nanami 語音・連續朗讀與間隔操練)
> {embed_line}
"""
    
    pattern = r"(> \[!abstract\][^\n]*\n(?:> [^\n]*\n)+)"
    if re.search(pattern, content):
        new_content = re.sub(pattern, r"\1" + callout_block, content, count=1)
    else:
        new_content = re.sub(r"(# [^\n]+\n)", r"\1" + callout_block + "\n", content, count=1)
        
    note_path.write_text(new_content, encoding="utf-8")
    print(f"Updated note {note_path.name} with audio callout embed.")

async def main():
    parser = argparse.ArgumentParser(description="Generate Chunking Audio for Obsidian Vault")
    parser.add_argument("--day", type=int, default=None, help="Specific day number (e.g. 16)")
    parser.add_argument("--start", type=int, default=None, help="Start day number (e.g. 16)")
    parser.add_argument("--end", type=int, default=None, help="End day number (e.g. 33)")
    parser.add_argument("--all", action="store_true", help="Generate for all available Day_XX_Chunking_Training.md files")
    parser.add_argument("--force", action="store_true", help="Overwrite existing mp3 files instead of skipping them")
    parser.add_argument("--voice", type=str, default=VOICE_DEFAULT, help="Edge TTS voice name")
    parser.add_argument("--vault-root", type=str, default=".", help="Root of Obsidian vault")
    args = parser.parse_args()

    vault_root = Path(args.vault_root).resolve()
    chunking_dir = vault_root / "HML_Wiki" / "concepts" / "24_Chunking_語塊與聽力自動化"
    if not chunking_dir.exists():
        alt1 = vault_root / "concepts" / "24_Chunking_語塊與聽力自動化"
        alt2 = vault_root
        if alt1.exists():
            chunking_dir = alt1
        elif (alt2 / "Chunking_Training_Index.md").exists():
            chunking_dir = alt2
        else:
            print(f"Error: Chunking dir not found: {chunking_dir}")
            sys.exit(1)
            
    audio_dir = chunking_dir / "audio"
    
    available_days = sorted([
        int(m.group(1))
        for p in chunking_dir.glob("Day_*_Chunking_Training.md")
        if (m := re.match(r"Day_(\d+)_Chunking_Training\.md", p.name))
    ])
    
    if args.day is not None:
        days_to_process = [args.day]
    elif args.start is not None or args.end is not None:
        s = args.start or 1
        e = args.end or (max(available_days) if available_days else 33)
        days_to_process = [d for d in available_days if s <= d <= e]
    elif args.all:
        days_to_process = available_days
    else:
        days_to_process = [
            d for d in available_days
            if not (audio_dir / f"Day_{d:02d}_Chunking_Immersion.mp3").exists()
        ]
        if not days_to_process:
            days_to_process = available_days
            
    for day in days_to_process:
        card_name = f"Day_{day:02d}_Chunking_Training.md"
        card_path = chunking_dir / card_name
        if not card_path.exists():
            print(f"Warning: {card_path} not found, skipping.")
            continue
            
        mp3_name = f"Day_{day:02d}_Chunking_Immersion.mp3"
        output_mp3 = audio_dir / mp3_name
        if output_mp3.exists() and not args.force and args.day is None:
            print(f"Skipping {mp3_name} (already exists; use --force to regenerate).")
            update_note_with_audio_embed(card_path, mp3_name)
            continue
            
        print(f"\n==========================================")
        print(f"Processing {card_name}...")
        print(f"==========================================")
        data = parse_day_card(card_path)
        
        cache_dir = Path("/tmp") / "chunking_audio_cache" / f"day_{day:02d}"
        if cache_dir.exists():
            shutil.rmtree(cache_dir)
            
        await build_continuous_track(data, output_mp3, cache_dir, voice=args.voice)
        update_note_with_audio_embed(card_path, mp3_name)

if __name__ == "__main__":
    asyncio.run(main())
