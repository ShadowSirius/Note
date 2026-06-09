---
author: Karpathy
tags:
  - compiler
  - llm
contradicts:
  - "[[RAG System]]"
supersedes:
  - "[[RAG System]]"
uses:
  - "[[Obsidian Web Clipper]]"
---
# LLM Compiler

The LLM Compiler is a modern design pattern for managing personal knowledge base scale indexing.

## Details
- We use the [[Obsidian Web Clipper|clipper @uses]] to ingest raw web pages.
- The LLM Compiler [[RAG System|completely @supersedes and @contradicts traditional RAG systems]] at personal scale.

## Code Example (Should be Ignored)
```markdown
This fake link [[Vector Database|is inside a code block @supports]] and should not be parsed.
```

An inline code block like `[[Vector Database|inline @supports]]` should also be ignored.
