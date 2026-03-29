# Day 11: Teach It to Learn

---

**What you'll learn today:**
- What Retrieval-Augmented Generation (RAG) is and why it matters for a personal AI assistant
- How document ingestion pipelines work: fetch, parse, chunk, embed, store
- What vector databases are and why ChromaDB is a good starting point
- How a self-improving agent loop works, and why it needs strict security gates
- Why human-in-the-loop approval is non-negotiable for any agent that modifies itself

**What you'll build today:** By the end of today, your Claw can ingest AI research papers, store them in a searchable vector database, and surface relevant knowledge when you ask questions. It cannot modify itself without your explicit approval at every step.

---

## The Problem: Your Claw Forgets Everything It Reads

By Day 10, your Claw can read emails, research the web, write drafts, and coordinate with sub-agents. But every conversation starts fresh. If you asked it to summarize an arXiv paper last Tuesday, that knowledge is gone by Wednesday.

MEMORY.md helps. It stores curated facts that reload every turn. But MEMORY.md is a hand-maintained file. It cannot hold 50 research papers. It was designed for personal context, not a knowledge library.

RAG solves this. Instead of cramming everything into the conversation window, you build a separate knowledge base that your Claw can search on demand. When you ask "what's new in AI agents this week?", it queries the knowledge base, retrieves the most relevant chunks, and weaves them into its answer.

---

## RAG: The Core Idea

RAG stands for Retrieval-Augmented Generation. The name describes exactly what happens:

1. **Retrieval** — search a knowledge base for chunks of text relevant to the current question
2. **Augmented** — inject those chunks into the conversation context alongside the question
3. **Generation** — the language model answers using both the question and the retrieved context

Without RAG, the model can only use what fits in its context window. With RAG, it can draw on a library of any size. The trade-off: retrieval quality matters. Bad chunking or weak embeddings mean the model retrieves irrelevant text and gives worse answers than it would with no retrieval at all.

---

## The Ingestion Pipeline

Before your Claw can retrieve anything, documents need to be processed into a searchable format. This is the ingestion pipeline:

```
Source (arXiv, RSS, PDF, URL)
    ↓
Fetch — download the raw content
    ↓
Parse — extract clean text (Docling handles PDFs, tables, figures)
    ↓
Chunk — split text into overlapping segments (~500 tokens each)
    ↓
Embed — convert each chunk into a vector (a list of numbers)
    ↓
Store — save vectors + metadata in ChromaDB
```

**Fetching** is the simplest step. For arXiv, there is a free API that returns metadata and PDF links for any search query. RSS feeds from AI blogs work the same way. You already know how to set up periodic tasks from Day 4 — the fetch step runs on a schedule you configure through the OpenClaw UI.

**Parsing** is where Docling comes in. Raw PDFs are not plain text. They contain layout information, figures, tables, and formatting that a naive text extractor will mangle. Docling is a document processing library that extracts clean, structured text from PDFs, DOCX, and HTML. It handles academic papers well because it understands multi-column layouts and citation blocks.

**Chunking** splits the parsed text into segments small enough to embed. Overlapping chunks (where each chunk shares some text with its neighbors) preserve context at chunk boundaries. A chunk size of ~500 tokens with ~50 token overlap is a common starting point.

**Embedding** converts each chunk into a vector — a list of numbers that captures the meaning of the text. Similar chunks end up with similar vectors, which is what makes semantic search possible. You can use OpenAI's embedding API, or run a local model like `all-MiniLM-L6-v2` through Ollama for zero cloud dependency.

**Storing** saves the vectors and their associated text into ChromaDB, a lightweight vector database that runs as a single process and stores data on disk. No external server required. It fits comfortably on your Hetzner VPS.

---

## Searching the Knowledge Base

Once documents are ingested, your Claw searches using **hybrid retrieval**:

- **Semantic search** — finds chunks whose meaning is similar to the query, even if the exact words differ
- **Keyword search (BM25)** — finds chunks that contain the exact terms in the query

Combining both catches cases that either alone would miss. A query like "attention mechanism alternatives" finds papers about "linear attention" (semantic match) and papers that literally say "attention mechanism" (keyword match).

ChromaDB handles the semantic side. BM25 runs alongside it as a simple index. The results are merged and ranked before being passed to the language model.

---

## The Self-Improvement Loop (With Guard Rails)

This is the ambitious part, and the part that requires the most caution. The idea: your Claw periodically reviews its knowledge base, extracts patterns, and proposes updates to its own behavior.

**This is powerful and dangerous.** An agent that modifies itself without oversight can drift, hallucinate improvements, or break its own configuration. Every self-modification must go through explicit human approval.

### The Security-First Self-Improvement Architecture

```
┌─────────────────────────────────────────────────┐
│  LAYER 1: INGEST (automated, read-only)         │
│  Cron fetches papers → parse → embed → store    │
│  No write access to agent config                 │
│  No approval needed — it's just adding to the    │
│  knowledge base                                  │
└──────────────────┬──────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────┐
│  LAYER 2: SYNTHESIZE (automated, read-only)     │
│  Weekly: agent reads knowledge base              │
│  Generates a "Learning Report" markdown file     │
│  Proposes changes but writes NOTHING to config   │
│  Report saved to ~/openclaw-reports/ for review  │
└──────────────────┬──────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────┐
│  LAYER 3: PROPOSE (human-gated)                 │
│  Agent sends you the Learning Report via         │
│  Telegram with a summary:                        │
│  "I found 3 insights this week. Here they are.  │
│   Should I update MEMORY.md? [Yes/No]"           │
│  NOTHING changes without your explicit "Yes"     │
└──────────────────┬──────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────┐
│  LAYER 4: APPLY (human-approved, audited)       │
│  Only after "Yes": agent applies ONE change      │
│  at a time, shows you the diff BEFORE writing    │
│  You approve each diff individually              │
│  After apply: openclaw security audit runs       │
│  Rollback: previous version saved as .bak        │
└──────────────────┬──────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────┐
│  LAYER 5: SKILL CREATION (highest gate)         │
│  Agent may propose a new skill based on patterns │
│  Skill is written to a DRAFT folder, never       │
│  installed automatically                         │
│  You must: read it, approve it, run clawvet,     │
│  then manually install                           │
│  No auto-install. No exceptions.                 │
└─────────────────────────────────────────────────┘
```

### Why Five Layers?

Each layer has a higher trust requirement:

| Layer | What Changes | Who Approves | Reversible? |
|-------|-------------|-------------|-------------|
| 1. Ingest | Knowledge base only | Nobody (read-only to agent) | Delete vectors |
| 2. Synthesize | Nothing — generates a report | Nobody (read-only) | Delete report |
| 3. Propose | Nothing — sends you a message | You read it | Ignore it |
| 4. Apply | MEMORY.md or config files | You approve each diff | .bak file |
| 5. Skill Creation | New skill in DRAFT folder | You review + clawvet + manual install | Delete draft |

The key principle: **the agent never modifies itself without you seeing exactly what will change and saying "yes."** Layers 1 and 2 are fully automated because they only add to the knowledge base or generate reports — they never touch the agent's configuration. Layers 3-5 require progressively more explicit approval.

---

## What You'll Learn About AI By Building This

This is not just a tool. Building this pipeline teaches you core AI engineering concepts:

| Concept | Where You Learn It |
|---------|-------------------|
| **Embeddings** | When you choose an embedding model and see how similar texts cluster |
| **Vector databases** | When you set up ChromaDB and run similarity queries |
| **Chunking strategies** | When you tune chunk size and see retrieval quality change |
| **Hybrid search** | When you combine semantic + keyword and see better results |
| **RAG architecture** | The full pipeline from fetch to answer |
| **Agent safety** | The 5-layer approval model and why autonomous self-modification is risky |
| **Prompt engineering** | Writing the synthesis and proposal prompts |

---

## Security Notes

- The ingestion cron runs in an **isolated session** with no access to identity files or conversation history
- ChromaDB stores vectors on disk at `~/.openclaw/chromadb/` — back it up with your regular VPS backups
- The synthesis agent runs **read-only** — it can query ChromaDB and read MEMORY.md but cannot write to either
- Skill drafts are written to `~/.openclaw/workspace/skill-drafts/`, a directory the agent cannot install from
- All proposed changes generate a diff that you see **before** any write happens
- `clawvet scan` must pass on any proposed skill before you install it manually
- If the agent ever writes to config without approval, that is a bug — report it and roll back from `.bak`

---

## Ready to Build?

Today's build has four phases. You'll set up the vector database, create the ingestion pipeline, build the search skill, and configure the human-gated improvement loop. The cron scheduling happens through the OpenClaw UI as you've been doing.

Head to [build.md](./build.md) when you're ready.
