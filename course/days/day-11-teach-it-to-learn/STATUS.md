# Day 11 Status — 2026-03-29

## What's Deployed

| Component | Path (inside container) | Status |
|-----------|------------------------|--------|
| `ingest_paper.py` | `~/.openclaw/workspace/scripts/ingest_paper.py` | Working |
| `fetch_arxiv.py` | `~/.openclaw/workspace/scripts/fetch_arxiv.py` | Broken (rate-limited) |
| `weekly_synthesis.py` | `~/.openclaw/workspace/scripts/weekly_synthesis.py` | Working |
| `knowledge-search` skill | `~/.openclaw/workspace/skills/knowledge-search/` | Working |
| `learning-proposal` skill | `~/.openclaw/workspace/skills/learning-proposal/` | Working |
| ChromaDB | `~/.openclaw/chromadb/` | 134 chunks, 4 papers (with duplicates) |

## Known Issues

### 1. Duplicate papers in ChromaDB

Three papers were ingested twice — once via local PDF path (`file:///...`) and once via arXiv URL (`https://...`). The duplicate detection in `ingest_paper.py` matches on `source_url`, but the same paper gets different URLs depending on how it was ingested.

**Fix:** Normalize all source URLs to a canonical form (`https://arxiv.org/abs/{id}`) before checking for duplicates. Then purge the 73 duplicate chunks.

### 2. Titles are arXiv IDs, not paper names

`ingest_paper.py` tries to extract the title from the first `# ` heading in the Docling markdown output. For arXiv papers, this often fails and falls back to the filename (e.g., "2310.11511").

**Fix:** For arXiv papers, fetch the title from the arXiv API metadata before ingesting. For non-arXiv sources, improve the markdown title extraction heuristic.

### 3. fetch_arxiv.py is rate-limited

The arXiv search API (`export.arxiv.org/api/query`) blocks our VPS IP after a few requests. This makes it unreliable as a cron job.

**Fix:** Replace with a multi-source `research-fetcher` skill (see Day 12 plan below).

### 4. No multi-source support

The current fetcher only knows about arXiv. The goal is to also pull from Hugging Face, Semantic Scholar, AI blogs, and RSS feeds.

**Fix:** Build a `research-fetcher` skill with pluggable source modules (Day 12).

## ChromaDB Contents

```
 24 chunks | 2005.11401 | https://arxiv.org/abs/2005.11401    ← RAG (Lewis et al.)
 37 chunks | 2312.10997 | https://arxiv.org/pdf/2312.10997    ← Self-RAG
 37 chunks | 2312.10997 | file:///...2312.10997.pdf            ← DUPLICATE
 36 chunks | 2310.11511 | https://arxiv.org/pdf/2310.11511    ← Chain-of-Note
 36 chunks | 2310.11511 | file:///...2310.11511.pdf            ← DUPLICATE
 27 chunks | 2402.10200 | file:///...2402.10200.pdf            ← Agentic RAG survey
```

Total: 197 chunks (134 unique after dedup)

## Day 12 Plan: Research Fetcher

Build a general-purpose `research-fetcher` skill that replaces `fetch_arxiv.py` with a multi-source, extensible architecture.

### Architecture

```
~/.openclaw/workspace/skills/research-fetcher/
  ├── SKILL.md              ← "Fetch latest research from all configured sources"
  ├── fetcher.py            ← Orchestrator: loops sources, deduplicates, ingests
  └── sources/
      ├── arxiv_rss.py      ← arXiv RSS feed (no API, no rate limit)
      ├── huggingface.py    ← Hugging Face daily papers + blog
      ├── semantic.py       ← Semantic Scholar API (100 req/sec free)
      └── rss.py            ← Generic RSS (AI blogs, newsletters)
```

### How it works

1. Each source module exports a `fetch_new(since: datetime) -> list[Paper]` function
2. `Paper` = `{title, url, pdf_url, source_name, published_date}`
3. `fetcher.py` loops through enabled sources, collects papers, deduplicates by canonical URL, calls `ingest_paper.py` for each
4. SAI triggers via cron: "Run the research-fetcher skill"
5. Adding a new source = adding one Python file to `sources/`

### Source details

| Source | Method | Rate limit | What it provides |
|--------|--------|-----------|------------------|
| **arXiv RSS** | `arxiv.org/rss/cs.AI` | 1 req per poll | ~50 new papers/day, titles + abs URLs |
| **Hugging Face** | `huggingface.co/api/daily_papers` | Generous | Daily curated AI papers |
| **Semantic Scholar** | `api.semanticscholar.org` | 100/sec free | Search across all academic papers |
| **Generic RSS** | Any RSS feed URL | Per-feed | AI blogs, newsletters, etc. |

### Fixes included in Day 12

- Canonical URL normalization (fixes duplicate issue)
- Title extraction from API metadata (fixes title issue)
- Configurable source list (user enables/disables sources)
- Proper User-Agent headers to avoid blocks

### Security

- Fetcher runs in isolated cron session (no identity file access)
- Only writes to ChromaDB and `~/openclaw-ingestion/papers/`
- Cannot modify agent config
- New source modules go to `skill-drafts/` first, require manual review
