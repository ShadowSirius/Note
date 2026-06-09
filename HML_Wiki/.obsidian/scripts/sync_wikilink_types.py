#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

# Configured relationship keys as defined by obsidian-wikilink-types plugin defaults
VALID_KEYS = {
    "supersedes", "contradicts", "supports", "causes", "influenced_by",
    "parent_of", "child_of", "sibling_of", "updates", "evolution_of",
    "prerequisite_for", "implements", "refines", "extends", "part_of",
    "instance_of", "related_to", "blocks", "prevents", "replaces",
    "derives_from", "uses", "defines", "illustrates"
}

def split_frontmatter(content):
    """Split note content into frontmatter block and body text."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[1], parts[2]
    return "", content

def strip_code(body):
    """Remove code blocks and inline code from markdown body."""
    # Strip fenced code blocks (``` or ~~~)
    body = re.sub(r'```[\s\S]*?```', '', body)
    body = re.sub(r'~~~[\s\S]*?~~~', '', body)
    # Strip inline code (`...`)
    body = re.sub(r'`[^`\n]+`', '', body)
    return body

def parse_relationships(body):
    """Parse typed wikilinks [[Target|Alias @type]] from body."""
    wikilink_re = re.compile(r'\[\[([^\]|]+)\|([^\]]+)\]\]')
    at_type_re = re.compile(r'(?:^|\s)@([\w-]+)')
    
    relationships = {}
    for target, alias in wikilink_re.findall(body):
        target = target.strip()
        types = at_type_re.findall(alias)
        for t in types:
            t = t.lower()
            if t in VALID_KEYS:
                if t not in relationships:
                    relationships[t] = []
                formatted_target = f"[[{target}]]"
                if formatted_target not in relationships[t]:
                    relationships[t].append(formatted_target)
    return relationships

def update_frontmatter_text(fm_text, relationships):
    """Update frontmatter text by replacing relationship keys while preserving others."""
    lines = fm_text.splitlines()
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        key_match = re.match(r'^([\w-]+)\s*:', line)
        if key_match:
            key = key_match.group(1).lower()
            if key in VALID_KEYS:
                # Skip the key line and all associated list items or indented values
                i += 1
                while i < len(lines) and (lines[i].strip().startswith("-") or re.match(r'^\s+', lines[i]) or not lines[i].strip()):
                    i += 1
                continue
        new_lines.append(line)
        i += 1
    
    # Append the updated relationships
    for key in sorted(relationships.keys()):
        targets = relationships[key]
        if targets:
            # Ensure proper spacing and format
            new_lines.append(f"{key}:")
            for t in targets:
                new_lines.append(f'  - "{t}"')
                
    # Clean up empty lines
    joined = "\n".join(new_lines).strip()
    return joined

def process_file(file_path):
    """Synchronize typed relationships in a single file to its frontmatter."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False, {}

    fm_text, body = split_frontmatter(content)
    clean_body = strip_code(body)
    relationships = parse_relationships(clean_body)
    new_fm_text = update_frontmatter_text(fm_text, relationships)
    
    if new_fm_text:
        new_content = f"---\n{new_fm_text}\n---\n" + body.lstrip("\r\n")
    else:
        if fm_text.strip():
            new_content = body.lstrip("\r\n")
        else:
            new_content = content
            
    if new_content != content:
        try:
            with open(file_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(new_content)
            return True, relationships
        except Exception as e:
            print(f"Error writing to {file_path}: {e}")
            return False, {}
    return False, {}

def sync_vault(vault_dir):
    """Recursively search and sync markdown files in the vault."""
    vault_path = Path(vault_dir).resolve()
    print(f"Scanning vault: {vault_path}")
    
    synced_count = 0
    total_count = 0
    
    for root, dirs, files in os.walk(vault_path):
        # Ignore hidden directories like .obsidian
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.md'):
                total_count += 1
                file_path = Path(root) / file
                changed, relationships = process_file(file_path)
                if changed:
                    synced_count += 1
                    rel_desc = ", ".join(f"{k} -> {len(v)} links" for k, v in relationships.items())
                    print(f"Synced: {file_path.relative_to(vault_path)} ({rel_desc})")
                    
    print(f"Sync complete. Checked {total_count} files, updated {synced_count} files.")

if __name__ == "__main__":
    # Vault directory defaults to the parent directory of .obsidian/scripts
    script_dir = Path(__file__).resolve().parent
    default_vault = script_dir.parent.parent
    
    target_vault = sys.argv[1] if len(sys.argv) > 1 else default_vault
    sync_vault(target_vault)
