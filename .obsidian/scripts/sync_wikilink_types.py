#!/usr/bin/env python3
import os
import re
import yaml

VALID_KEYS = {
    "supersedes", "contradicts", "supports", "causes", "influenced_by",
    "parent_of", "child_of", "sibling_of", "updates", "evolution_of",
    "prerequisite_for", "implements", "refines", "extends", "part_of",
    "instance_of", "related_to", "blocks", "prevents", "replaces",
    "derives_from", "uses", "defines", "illustrates"
}

# Regex to extract wikilinks: [[Target|Alias]] or [[Target]]
WIKILINK_RE = re.compile(r'\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]')
TYPE_RE = re.compile(r'(?:^|\s)@([a-zA-Z0-9_-]+)')

def clean_code_blocks(text):
    # Remove fenced code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # Remove inline code
    text = re.sub(r'`.*?`', '', text)
    return text

def parse_markdown_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    frontmatter = {}
    body = content
    has_frontmatter = False

    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            has_frontmatter = True
            fm_text = parts[1]
            body = parts[2]
            try:
                frontmatter = yaml.safe_load(fm_text) or {}
            except Exception as e:
                print(f"Error parsing YAML in {filepath}: {e}")
                return

    clean_body = clean_code_blocks(body)

    extracted = {k: [] for k in VALID_KEYS}
    for match in WIKILINK_RE.finditer(clean_body):
        target = match.group(1).strip()
        alias = match.group(2)
        if alias:
            for type_match in TYPE_RE.finditer(alias):
                rel_type = type_match.group(1)
                if rel_type in VALID_KEYS:
                    link_repr = f"[[{target}]]"
                    if link_repr not in extracted[rel_type]:
                        extracted[rel_type].append(link_repr)

    for k in VALID_KEYS:
        if k in frontmatter:
            del frontmatter[k]

    for k, v in extracted.items():
        if v:
            frontmatter[k] = v

    if frontmatter:
        fm_dump = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
        new_content = f"---\n{fm_dump}---\n{body.lstrip() if body.startswith(chr(10)) else body}"
    else:
        new_content = body.lstrip() if not has_frontmatter else f"---\n---\n{body.lstrip()}"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

def sync_vault(vault_dir):
    for root, dirs, files in os.walk(vault_dir):
        if '.git' in root or '.obsidian' in root:
            continue
        for file in files:
            if file.endswith('.md'):
                parse_markdown_file(os.path.join(root, file))

if __name__ == '__main__':
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    print(f"Syncing wikilink types for vault: {root_dir}")
    sync_vault(root_dir)
    print("Synchronization complete!")
