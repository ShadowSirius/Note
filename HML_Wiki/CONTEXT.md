# System Context: HML Wiki (LLM Compiler Vault)

This file serves as a context manifest for AI agents (including LLM compilers and assistants) to quickly onboard, understand the vault structure, and perform operations with optimal token efficiency.

## 🎯 System Overview
Inspired by Andrej Karpathy's LLM Compiler concept, this Obsidian vault is a personal knowledge base where raw source documents are ingested, compiled, and semantically interlinked using typed wikilinks.

---

## 📂 Vault Directory Structure

- **`/raw`**: Staging directory for raw files (web clips, imported PDFs, raw drafts).
  - *Agent Action*: Read raw files here, compile them into structured notes, and move/archive them when compiled.
- **`/concepts`**: Core semantic wiki containing clean, focused concept notes.
  - *Agent Action*: Write new concepts and establish link connections here.
- **`/derived`**: Secondary outputs generated from the wiki (e.g. Marp slide decks, matplotlib charts, Q&A summaries).
  - *Agent Action*: Store generated assets and filed-back Q&A outputs here.
- **`/index.md`**: Main navigation entrypoint and high-level vault summary.

---

## 🛠️ Semantic Relationship Protocol (`obsidian-wikilink-types`)

We use typed wikilinks to construct a machine-readable knowledge graph.

### 1. Linking Format
- Format: `[[TargetNote|Display text @relationship_type]]`
- Examples:
  - `[[Obsidian Web Clipper|clipper @uses]]`
  - `[[RAG System|completely @supersedes and @contradicts traditional RAG]]`

### 2. Synchronization Script
A synchronization script is located at:
[sync_wikilink_types.py](file:///C:/Data/Note/HML_Wiki/.obsidian/scripts/sync_wikilink_types.py)
- *Command to run*: `python .obsidian/scripts/sync_wikilink_types.py` from the vault root.
- *Function*: Automatically parses note bodies, extracts relationships, and synchronizes them to note YAML frontmatter, e.g.:
  ```yaml
  ---
  uses:
    - "[[Obsidian Web Clipper]]"
  supersedes:
    - "[[RAG System]]"
  contradicts:
    - "[[RAG System]]"
  ---
  ```

### 3. Valid Relationship Keys (24 types)
Use *only* the following lowercase relationship keys inside link aliases:
- `supersedes`, `contradicts`, `supports`, `causes`, `influenced_by`
- `parent_of`, `child_of`, `sibling_of`, `updates`, `evolution_of`
- `prerequisite_for`, `implements`, `refines`, `extends`, `part_of`
- `instance_of`, `related_to`, `blocks`, `prevents`, `replaces`
- `derives_from`, `uses`, `defines`, `illustrates`

---

## 🤖 AI Agent Guidelines (Token Saver)

When asked to update, compile, or query this vault, follow these rules:
1. **Always consult this [CONTEXT.md](file:///C:/Data/Note/HML_Wiki/CONTEXT.md) first** to ground your knowledge of the system.
2. **Compile Flow**:
   - Ingest raw texts from `/raw`.
   - Write structured notes to `/concepts` using H1 headers (`# Note Title`).
   - Create semantic connections using the `[[TargetNote|alias @type]]` syntax.
   - Run `python .obsidian/scripts/sync_wikilink_types.py` to compile the frontmatter graph.
3. **Graph Consistency**: Ensure backlinks are balanced and logical (e.g., if A `supersedes` B, B is outdated; if A is a `child_of` B, B is a `parent_of` A).
4. **Code Fences**: Do not parse or extract typed links inside inline code or fenced code blocks.
