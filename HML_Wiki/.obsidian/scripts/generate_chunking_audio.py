#!/usr/bin/env python3
"""
Generate Continuous Japanese Chunking & Daily Vocabulary Immersion Audio for Obsidian Notes.
Powered by Microsoft Edge Neural TTS (edge-tts) & ffmpeg.
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

def to_kanji_number(n: int) -> str:
    """Convert an integer (1-99) into Japanese kanji numerals for TTS."""
    kanji_digits = ["", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
    if n <= 0:
        return str(n)
    if n < 10:
        return kanji_digits[n]
    if n == 10:
        return "十"
    if n < 20:
        return "十" + kanji_digits[n % 10]
    tens = n // 10
    ones = n % 10
    return kanji_digits[tens] + "十" + (kanji_digits[ones] if ones > 0 else "")

def clean_japanese_text(raw_text: str) -> str:
    """Clean markdown/html tags, ruby tags, and Chinese explanations from Japanese sentences for Chunking cards."""
    # Remove ruby readings <rt>...</rt>
    text = re.sub(r"<rt>.*?</rt>", "", raw_text)
    # Remove all HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Remove markdown formatting
    text = text.replace("*", "").replace("_", "")
    # Remove leading numbering and style markers, e.g. "1. [丁寧] ", "[常體・縮約]"
    text = re.sub(r"^\s*\d+\.\s*", "", text)
    text = re.sub(r"^\s*\[[^\]]+\]\s*", "", text)
    # Remove Chinese explanation after dash or brackets
    text = re.sub(r"\s*[—–-].*$", "", text)
    text = re.sub(r"\s*（.*?）.*$", "", text)
    text = re.sub(r"\s*\(.*?\).*$", "", text)
    # Replace chunk separators "/" with natural Japanese comma for natural prosody pause
    text = re.sub(r"\s*/\s*", "、", text)
    # Clean whitespace
    text = text.strip()
    return text

def clean_vocab_text(text: str) -> str:
    """Clean furigana readings and Chinese explanations for Vocabulary cards."""
    # Remove ruby readings <rt>...</rt>
    text = re.sub(r"<rt>.*?</rt>", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    # Remove leading markdown quotes or list markers
    text = re.sub(r"^[>\s*]*", "", text)
    # Remove speaker tags like A:, B:, **A**:, A（媽媽 / 室友）:
    text = re.sub(r"^\*?\*?[A-ZＡ-Ｚ]\*?\*?(?:（[^）]+）|\([^)]+\))?[:：]\s*", "", text)
    # Remove kana furigana in parentheses, e.g. 7時（じ）, 起（お）きて, 目覚（めざ）まし時計（どけい）
    text = re.sub(r"[（\(][ぁ-んァ-ヶー\s・]+[）\)]", "", text)
    # Remove markdown bold/italic
    text = text.replace("*", "").replace("_", "")
    # If the entire line is a parenthesized stage direction or Chinese explanation, return empty
    stripped = text.strip()
    if re.match(r"^[（\(].*?[）\)]$", stripped):
        return ""
    # Remove trailing Chinese explanations in parentheses
    text = re.sub(r"[（\(][^）\)]*[\u4e00-\u9fff]+[^）\)]*[）\)]\s*$", "", text)
    # Replace chunk separators "/" with natural Japanese comma
    text = re.sub(r"\s*/\s*", "、", text)
    return text.strip()

def parse_chunking_card(filepath: Path) -> dict:
    """Parse a chunking daily markdown file into structured audio sections."""
    content = filepath.read_text(encoding="utf-8")
    
    # Extract Title / Day
    title_match = re.search(r"^title:\s*['\"]?(?:Day\s*(\d+)[:：]\s*)?(.*?)['\"]?$", content, re.MULTILINE)
    day_num = int(title_match.group(1)) if title_match and title_match.group(1) else 1
    day_title = title_match.group(2).strip() if title_match else ""
    
    # Extract Patterns
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
    
    # Extract FSI Drills
    drills = {"base": "", "substitutions": [], "transformations": []}
    
    base_match = re.search(r"\* \*\*Base Sentence\*\*：(.*?)\n", content)
    if base_match:
        drills["base"] = clean_japanese_text(base_match.group(1))
    
    # Substitution Drill Table
    sub_table = re.search(r"### 1️⃣ Substitution Drill.*?\n(.*?)(?=\n###|\n##|\Z)", content, re.DOTALL)
    if sub_table:
        for line in sub_table.group(1).split("\n"):
            line = line.strip()
            if line.startswith("|") and not line.startswith("| 提示語塊") and not line.startswith("|:--") and not line.startswith("|---"):
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 2:
                    prompt = clean_japanese_text(parts[0])
                    response = clean_japanese_text(parts[1])
                    if prompt and response:
                        drills["substitutions"].append((prompt, response))
    
    # Transformation Drill Table
    trans_table = re.search(r"### 2️⃣ Transformation Drill.*?\n(.*?)(?=\n###|\n##|\Z)", content, re.DOTALL)
    if trans_table:
        for line in trans_table.group(1).split("\n"):
            line = line.strip()
            if line.startswith("|") and not line.startswith("| 原始語塊") and not line.startswith("|:--") and not line.startswith("|---"):
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 2:
                    orig = clean_japanese_text(parts[0])
                    trans = clean_japanese_text(parts[1])
                    if orig and trans:
                        drills["transformations"].append((orig, trans))
                        
    return {
        "day_num": day_num,
        "day_title": day_title,
        "patterns": patterns,
        "drills": drills
    }

def parse_vocabulary_card(filepath: Path) -> dict:
    """Parse a daily vocabulary markdown file (Folder 23) into dialogue and vocabulary sections."""
    content = filepath.read_text(encoding="utf-8")
    
    # Extract Day number
    day_match = re.search(r"^day:\s*(\d+)", content, re.MULTILINE)
    day_num = int(day_match.group(1)) if day_match else 1
    
    title_match = re.search(r"^title:\s*['\"]?(?:Day\s*\d+\s*(?:\([^)]+\))?\s*)?(.*?)['\"]?$", content, re.MULTILINE)
    day_title = title_match.group(1).strip() if title_match else ""
    
    # Special Handling for Day 33 (Weekly Review)
    if day_num == 33:
        recall_sentences = []
        diff_items = []
        practical_sentences = []
        for line in content.splitlines():
            if "解答：" in line:
                ans = clean_vocab_text(line.split("解答：")[-1])
                if ans:
                    recall_sentences.append(ans)
            elif line.strip().startswith("* **") and "：" in line:
                m = re.match(r"\s*\*\s*\*\*(.*?)\*\*(?:[（\(].*?[）\)])?[:：]\s*(.*)", line)
                if m:
                    w = clean_vocab_text(m.group(1))
                    ex = clean_vocab_text(m.group(2))
                    # Only include if example contains Japanese characters
                    if w and ex and re.search(r"[\u3040-\u30ff]", ex):
                        diff_items.append((w, ex))
            elif re.match(r"^\s*\d+\.\s*\*\*", line):
                # Section IV practical sentences often start with 1. **【...】**
                pass
            elif line.strip().startswith("* ") and not line.strip().startswith("* **"):
                # Potential practical sentence bullet
                ex = clean_vocab_text(line)
                if ex and re.search(r"[\u3040-\u30ff]", ex) and len(ex) > 10:
                    practical_sentences.append(ex)
                    
        return {
            "day_num": day_num,
            "day_title": day_title,
            "is_review_33": True,
            "recall_sentences": recall_sentences,
            "diff_items": diff_items,
            "practical_sentences": practical_sentences,
            "dialogues": [],
            "vocab_items": []
        }

    # Special Handling for Day 34 (Weekly Compound Review)
    if day_num == 34:
        dialogues = []
        vocab_items = []
        for line in content.splitlines():
            if re.search(r"^[>\s*]*\*\*?[A-ZＡ-Ｚ]\*\*?(?:（[^）]+）|\([^)]+\))?[:：]", line):
                cl = clean_vocab_text(line)
                if cl:
                    dialogues.append(cl)
            m = re.match(r"^\s*\d+\.\s*\*\*(.*?)\*\*(?:[（\(].*?[）\)])?[:：]\s*(.*?)(?:[（\(][^）\)]*[\u4e00-\u9fff]+.*|$)", line)
            if m:
                w = clean_vocab_text(m.group(1))
                c = clean_vocab_text(m.group(2))
                if w and c:
                    vocab_items.append((w, c))
        return {
            "day_num": day_num,
            "day_title": day_title,
            "is_review_34": True,
            "dialogues": dialogues,
            "vocab_items": vocab_items
        }

    # Regular Days (1-32, 35-38)
    dialogues = []
    vocab_items = []
    in_dialogue_section = False
    
    for line in content.splitlines():
        if line.startswith("## 第一部分") or "生活實戰對話" in line or "生活微對話" in line:
            in_dialogue_section = True
            continue
        elif line.startswith("## 第二部分") or line.startswith("## 二、"):
            in_dialogue_section = False
        
        if in_dialogue_section:
            if re.search(r"^[>\s*]*\*\*?[A-ZＡ-Ｚ]\*\*?(?:（[^）]+）|\([^)]+\))?[:：]", line):
                cl = clean_vocab_text(line)
                if cl:
                    dialogues.append(cl)
        
        # Parse Vocabulary Table
        if line.startswith("|") and not line.startswith("| 編號") and not line.startswith("|:--") and not line.startswith("|---"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 4 and parts[0].isdigit():
                w_match = re.search(r"\*\*(.*?)\*\*", parts[1])
                w_raw = w_match.group(1) if w_match else parts[1]
                w = clean_vocab_text(w_raw)
                
                c_match = re.search(r"\*\*(.*?)\*\*", parts[3])
                c_raw = c_match.group(1) if c_match else parts[3]
                c = clean_vocab_text(c_raw)
                if w and c:
                    vocab_items.append((w, c))

    return {
        "day_num": day_num,
        "day_title": day_title,
        "dialogues": dialogues,
        "vocab_items": vocab_items
    }

def get_silence_file(cache_dir: Path, duration: float) -> Path:
    """Generate or retrieve a silence mp3 of given duration."""
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
                print(f"Failed to synthesize clip '{text[:20]}...': {e}", file=sys.stderr)
                raise
            await asyncio.sleep(1.0 * (attempt + 1))

async def build_continuous_track(data: dict, output_mp3: Path, cache_dir: Path, voice: str = VOICE_DEFAULT):
    """Build the continuous audio track for a Day's chunking card (Folder 24)."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    playlist = []
    speech_tasks = []
    
    day_num = data["day_num"]
    day_str = to_kanji_number(day_num)
    
    seq = 0
    def add_speech(text: str, pause_after: float = 1.5):
        nonlocal seq
        seq += 1
        clip_path = cache_dir / f"clip_{seq:04d}.mp3"
        speech_tasks.append((text, clip_path))
        playlist.append(clip_path)
        if pause_after > 0:
            playlist.append(get_silence_file(cache_dir, pause_after))

    # 1. Intro
    add_speech(f"デイ{day_str}、語塊トレーニング。", pause_after=1.8)
    
    # 2. Patterns
    p_num_kanji = ["一", "二", "三", "四", "五", "六"]
    for idx, pattern in enumerate(data["patterns"]):
        p_num = p_num_kanji[idx] if idx < len(p_num_kanji) else str(idx + 1)
        p_title = f"パターン{p_num}、{pattern['name']}。"
        add_speech(p_title, pause_after=1.6)
        
        for s in pattern["sentences"]:
            add_speech(s, pause_after=1.5)
            
        playlist.append(get_silence_file(cache_dir, 1.2))
        
    # 3. Speed Drill
    drills = data["drills"]
    if drills["base"] or drills["substitutions"] or drills["transformations"]:
        add_speech("スピードドリル、意群代入練習。", pause_after=1.5)
        if drills["base"]:
            add_speech(f"基本文、{drills['base']}", pause_after=1.8)
            
        for prompt, resp in drills["substitutions"]:
            add_speech(prompt, pause_after=1.8)  # Pause for user reflection
            add_speech(resp, pause_after=1.5)
            
        if drills["transformations"]:
            add_speech("語体変換と、文末アンカー練習。", pause_after=1.5)
            for orig, trans in drills["transformations"]:
                add_speech(orig, pause_after=1.8)  # Pause for user transformation
                add_speech(trans, pause_after=1.5)
                
    # 4. Outro
    add_speech(f"お疲れ様でした。デイ{day_str}のトレーニングは終了です。", pause_after=0.5)

    # 5. Concurrently synthesize all speech clips
    sem = asyncio.Semaphore(10)
    tasks = [generate_speech_clip(t, p, voice, sem) for t, p in speech_tasks]
    await asyncio.gather(*tasks)

    # 6. Concatenate all files using ffmpeg concat demuxer
    concat_list = cache_dir / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for p in playlist:
            f.write(f"file '{p.resolve().as_posix()}'\n")
            
    output_mp3.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c:a", "libmp3lame", "-b:a", "128k",
        str(output_mp3)
    ]
    subprocess.run(cmd, check=True)
    print(f"[Chunking] Generated: {output_mp3.name}")

async def build_vocabulary_track(data: dict, output_mp3: Path, cache_dir: Path, voice: str = VOICE_DEFAULT):
    """Build the continuous audio track for a Day's daily vocabulary card (Folder 23)."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    playlist = []
    speech_tasks = []
    
    day_num = data["day_num"]
    day_str = to_kanji_number(day_num)
    
    seq = 0
    def add_speech(text: str, pause_after: float = 1.5):
        nonlocal seq
        seq += 1
        clip_path = cache_dir / f"clip_{seq:04d}.mp3"
        speech_tasks.append((text, clip_path))
        playlist.append(clip_path)
        if pause_after > 0:
            playlist.append(get_silence_file(cache_dir, pause_after))

    # Special Case: Day 33 (Review Day)
    if data.get("is_review_33"):
        add_speech(f"デイ{day_str}、生活単語総復習トレーニング。", pause_after=1.8)
        
        # Section 1: Recall Sentences
        if data["recall_sentences"]:
            add_speech("セクション一、反向提取練習。", pause_after=1.6)
            for ans in data["recall_sentences"]:
                add_speech(ans, pause_after=1.8)
            playlist.append(get_silence_file(cache_dir, 1.2))
            
        # Section 2: Differentiations
        if data["diff_items"]:
            add_speech("セクション二、重要語塊と例文。", pause_after=1.6)
            for word, ex in data["diff_items"]:
                add_speech(word, pause_after=0.8)
                add_speech(ex, pause_after=1.4)
            playlist.append(get_silence_file(cache_dir, 1.2))
            
        # Section 3: Practical Sentences
        if data["practical_sentences"]:
            add_speech("セクション三、総合実用例文。", pause_after=1.6)
            for sent in data["practical_sentences"]:
                add_speech(sent, pause_after=1.8)
                
        add_speech(f"お疲れ様でした。デイ{day_str}の総復習は終了です。", pause_after=0.5)

    # Special Case: Day 34 (Compound Dialogue & 100 Review Words)
    elif data.get("is_review_34"):
        add_speech(f"デイ{day_str}、複合会話と単語総復習トレーニング。", pause_after=1.8)
        
        # Section 1: Dialogues
        if data["dialogues"]:
            add_speech("セクション一、生活実戦会話劇。", pause_after=1.6)
            for d in data["dialogues"]:
                add_speech(d, pause_after=1.4)
            playlist.append(get_silence_file(cache_dir, 1.5))
            
        # Section 2: 100 Words Review
        if data["vocab_items"]:
            add_speech("セクション二、百単語総復習。", pause_after=1.6)
            for word, chunk in data["vocab_items"]:
                add_speech(word, pause_after=0.8)
                add_speech(chunk, pause_after=1.3)
                
        add_speech(f"お疲れ様でした。デイ{day_str}の複合トレーニングは終了です。", pause_after=0.5)

    # Standard Days (1-32, 35-38)
    else:
        add_speech(f"デイ{day_str}、生活単語と会話トレーニング。", pause_after=1.8)
        
        # Section 1: Micro-dialogue
        if data["dialogues"]:
            add_speech("セクション一、生活会話。", pause_after=1.6)
            for d in data["dialogues"]:
                add_speech(d, pause_after=1.4)
            playlist.append(get_silence_file(cache_dir, 1.5))
            
        # Section 2: Vocabulary & Chunks
        if data["vocab_items"]:
            add_speech("セクション二、単語と語塊。", pause_after=1.6)
            for word, chunk in data["vocab_items"]:
                add_speech(word, pause_after=0.8)
                add_speech(chunk, pause_after=1.4)
                
        add_speech(f"お疲れ様でした。デイ{day_str}のトレーニングは終了です。", pause_after=0.5)

    # Concurrently synthesize all speech clips
    sem = asyncio.Semaphore(10)
    tasks = [generate_speech_clip(t, p, voice, sem) for t, p in speech_tasks]
    await asyncio.gather(*tasks)

    # Concatenate all files using ffmpeg concat demuxer
    concat_list = cache_dir / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for p in playlist:
            f.write(f"file '{p.resolve().as_posix()}'\n")
            
    output_mp3.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c:a", "libmp3lame", "-b:a", "128k",
        str(output_mp3)
    ]
    subprocess.run(cmd, check=True)
    print(f"[Vocabulary] Generated: {output_mp3.name}")

def update_note_callout(note_path: Path, mp3_filename: str):
    """
    Ensure the note embeds the audio player with the clean, concise header:
    > [!audio] 🎧 {mp3_filename}
    > ![[{mp3_filename}]]
    """
    content = note_path.read_text(encoding="utf-8")
    embed_target = f"![[{mp3_filename}]]"
    new_callout = f"> [!audio] 🎧 {mp3_filename}\n> {embed_target}"

    # 1. If an audio callout block already exists with ANY header or title, replace it
    pattern_existing = r"> \[!audio\][^\n]*\n> !\[\[" + re.escape(mp3_filename) + r"\]\]"
    if re.search(pattern_existing, content):
        new_content = re.sub(pattern_existing, new_callout, content, count=1)
        if new_content != content:
            note_path.write_text(new_content, encoding="utf-8")
            print(f"[Callout Updated] {note_path.name} -> 🎧 {mp3_filename}")
        return

    # 2. If embed line exists without standard callout, replace surrounding line
    if embed_target in content:
        pattern_solo = r"(?:> \[!audio\][^\n]*\n)?(?:\s*>?\s*)?" + re.escape(embed_target)
        new_content = re.sub(pattern_solo, new_callout, content, count=1)
        note_path.write_text(new_content, encoding="utf-8")
        print(f"[Callout Replaced] {note_path.name} -> 🎧 {mp3_filename}")
        return

    # 3. Otherwise, insert below abstract block or after the first heading
    abstract_pattern = r"(> \[!abstract\][^\n]*\n(?:> [^\n]*\n)+)"
    if re.search(abstract_pattern, content):
        new_content = re.sub(abstract_pattern, rf"\1\n{new_callout}\n", content, count=1)
    else:
        new_content = re.sub(r"(# [^\n]+\n)", rf"\1\n{new_callout}\n\n", content, count=1)

    note_path.write_text(new_content, encoding="utf-8")
    print(f"[Callout Inserted] {note_path.name} -> 🎧 {mp3_filename}")

def update_all_vault_callout_titles(vault_root: Path):
    """Scan both Chunking and Daily Vocabulary directories and normalize all audio callouts."""
    chunking_dir = vault_root / "HML_Wiki" / "concepts" / "24_Chunking_語塊與聽力自動化"
    vocab_dir = vault_root / "HML_Wiki" / "concepts" / "23_Daily_Vocabulary_生活單字與對話"
    
    count = 0
    # Process Chunking notes
    if chunking_dir.exists():
        for note_file in sorted(chunking_dir.glob("Day_*_Chunking_Training.md")):
            m = re.search(r"Day_(\d+)_Chunking_Training\.md", note_file.name)
            if m:
                day_num = int(m.group(1))
                mp3_name = f"Day_{day_num:02d}_Chunking_Immersion.mp3"
                update_note_callout(note_file, mp3_name)
                count += 1
                
    # Process Daily Vocabulary notes
    if vocab_dir.exists():
        for note_file in sorted(vocab_dir.glob("Day*.md")):
            m = re.search(r"Day(\d+)_", note_file.name)
            if m:
                day_num = int(m.group(1))
                mp3_name = f"Day_{day_num:02d}_Vocabulary_Immersion.mp3"
                update_note_callout(note_file, mp3_name)
                count += 1
                
    print(f"Callout title normalization complete across {count} notes.")

async def process_chunking(vault_root: Path, days: list = None, force: bool = False, voice: str = VOICE_DEFAULT):
    """Generate audio files and update callouts for Chunking (Folder 24)."""
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
        
        # Always ensure note callout is updated to short format
        update_note_callout(note_file, mp3_name)
        
        # Check if generation is needed
        if output_mp3.exists() and output_mp3.stat().st_size > 0 and not force:
            print(f"[Chunking] Day {day_num:02d} audio already exists: {output_mp3.name}, skipping.")
            continue
            
        print(f"\n[Chunking] Generating Day {day_num:02d} ({note_file.name})...")
        data = parse_chunking_card(note_file)
        cache_dir = base_tmp / f"day_{day_num:02d}"
        if cache_dir.exists():
            shutil.rmtree(cache_dir, ignore_errors=True)
            
        await build_continuous_track(data, output_mp3, cache_dir, voice=voice)
        shutil.rmtree(cache_dir, ignore_errors=True)

async def process_vocabulary(vault_root: Path, days: list = None, force: bool = False, voice: str = VOICE_DEFAULT):
    """Generate audio files and update callouts for Daily Vocabulary (Folder 23)."""
    vocab_dir = vault_root / "HML_Wiki" / "concepts" / "23_Daily_Vocabulary_生活單字與對話"
    audio_dir = vocab_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    all_notes = sorted(vocab_dir.glob("Day*.md"))
    base_tmp = Path(tempfile.gettempdir()) / "obsidian_vocab_cache"
    
    for note_file in all_notes:
        m = re.search(r"Day(\d+)_", note_file.name)
        if not m:
            continue
        day_num = int(m.group(1))
        if days is not None and day_num not in days:
            continue
            
        mp3_name = f"Day_{day_num:02d}_Vocabulary_Immersion.mp3"
        output_mp3 = audio_dir / mp3_name
        
        # Always ensure note callout is updated to short format
        update_note_callout(note_file, mp3_name)
        
        # Check if generation is needed
        if output_mp3.exists() and output_mp3.stat().st_size > 0 and not force:
            print(f"[Vocabulary] Day {day_num:02d} audio already exists: {output_mp3.name}, skipping.")
            continue
            
        print(f"\n[Vocabulary] Generating Day {day_num:02d} ({note_file.name})...")
        data = parse_vocabulary_card(note_file)
        cache_dir = base_tmp / f"day_{day_num:02d}"
        if cache_dir.exists():
            shutil.rmtree(cache_dir, ignore_errors=True)
            
        await build_vocabulary_track(data, output_mp3, cache_dir, voice=voice)
        shutil.rmtree(cache_dir, ignore_errors=True)

async def main():
    parser = argparse.ArgumentParser(description="Generate Audio Immersion for Chunking (24) & Vocabulary (23)")
    parser.add_argument("--target", choices=["all", "chunking", "vocab", "24", "23"], default="all",
                        help="Target module to process (default: all)")
    parser.add_argument("--day", type=int, default=None, help="Specific Day number to process")
    parser.add_argument("--force", action="store_true", help="Force regenerate audio even if file exists")
    parser.add_argument("--update-titles-only", action="store_true", help="Only update markdown callouts without generating audio")
    parser.add_argument("--voice", type=str, default=VOICE_DEFAULT, help="Edge TTS voice name")
    parser.add_argument("--vault-root", type=str, default=".", help="Root of Obsidian vault")
    args = parser.parse_args()

    vault_root = Path(args.vault_root).resolve()
    
    # 1. Update markdown titles only if requested
    if args.update_titles_only:
        update_all_vault_callout_titles(vault_root)
        return

    days_filter = [args.day] if args.day is not None else None

    # 2. Process Chunking (Folder 24)
    if args.target in ["all", "chunking", "24"]:
        print("\n=======================================================")
        print(">>> Processing Chunking (Folder 24)...")
        print("=======================================================")
        await process_chunking(vault_root, days=days_filter, force=args.force, voice=args.voice)

    # 3. Process Daily Vocabulary (Folder 23)
    if args.target in ["all", "vocab", "23"]:
        print("\n=======================================================")
        print(">>> Processing Daily Vocabulary (Folder 23)...")
        print("=======================================================")
        await process_vocabulary(vault_root, days=days_filter, force=args.force, voice=args.voice)

    # 4. Final sweep of all callouts
    update_all_vault_callout_titles(vault_root)
    print("\nAll tasks completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())
