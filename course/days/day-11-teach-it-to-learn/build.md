# Day 11 Build: Teach It to Learn

This is the user-facing guide for Day 11. Today you give your Claw a knowledge base it can search, an ingestion pipeline for AI research papers, and a human-gated self-improvement loop where nothing changes without your approval.

The cron scheduling for periodic fetches happens through the OpenClaw UI, the same way you set up scheduled tasks in Day 4.

---

## What You Need Before Starting

- Days 1-10 complete: OpenClaw installed, identity files created, Telegram connected, skills working
- Access to your Claw through the web chat
- Telegram on your phone (for approval notifications)
- SSH access to your VPS for installing dependencies
- Your Anthropic API key (already configured from Day 1)

---

## How To Run Day 11

Work through these phases in order. Each phase builds on the previous one.

1. **Phase 1: Install the Vector Database** — SSH setup for dependencies
2. **Phase 2: Build the Ingestion Pipeline** — [`claw-instructions-setup-ingestion.md`](./claw-instructions-setup-ingestion.md)
3. **Phase 3: Create the Search Skill** — [`claw-instructions-create-knowledge-search.md`](./claw-instructions-create-knowledge-search.md)
4. **Phase 4: Configure the Human-Gated Improvement Loop** — [`claw-instructions-setup-improvement-loop.md`](./claw-instructions-setup-improvement-loop.md)

---

## Phase 1: Install the Vector Database

SSH into your VPS and install the dependencies your Claw will need:

```bash
ssh sri@sshub.dev
```

```bash
# Install ChromaDB and Docling
pip install chromadb docling sentence-transformers

# Create the data directories
mkdir -p ~/.openclaw/chromadb
mkdir -p ~/.openclaw/workspace/skill-drafts
mkdir -p ~/openclaw-reports
mkdir -p ~/openclaw-ingestion/papers
```

Verify the install:

```bash
python3 -c "import chromadb; print('ChromaDB', chromadb.__version__)"
python3 -c "from docling.document_converter import DocumentConverter; print('Docling OK')"
python3 -c "from sentence_transformers import SentenceTransformer; print('Embeddings OK')"
```

All three should print without errors. If your VPS runs low on memory during the sentence-transformers download, see Troubleshooting below.

---

## Phase 2: Build the Ingestion Pipeline

Copy and paste the following into the OpenClaw web chat:

> Read `https://raw.githubusercontent.com/charanbobby/OpenClaw/master/course/days/day-11-teach-it-to-learn/claw-instructions-setup-ingestion.md` and follow every step. Set up an arXiv ingestion pipeline that fetches AI research papers, parses them with Docling, chunks the text, embeds it, and stores it in ChromaDB. Do not configure any scheduled tasks — I will do that through the UI. Stop when the pipeline can process a single paper end to end.

Alternatively, if you have the course files on your VPS, paste the contents of [`claw-instructions-setup-ingestion.md`](./claw-instructions-setup-ingestion.md) directly into the chat.

After the agent confirms the pipeline works, test it:

> Ingest this paper: https://arxiv.org/abs/2005.11401 (the original RAG paper by Lewis et al.). Show me how many chunks were created and a sample of the first 3 chunks.

You should see the paper split into chunks and stored in ChromaDB. This is a good test because you're building a RAG system by ingesting the paper that introduced RAG.

### Setting Up the Fetch Schedule

Open the OpenClaw UI and create a new scheduled task (the same way you did in Day 4):

- **Task:** Fetch latest arXiv papers on AI agents, RAG, and LLM reasoning
- **Schedule:** Every 6 hours (or whatever frequency you prefer)
- **Action:** Run the ingestion pipeline on new papers
- **Session type:** Isolated (no access to identity files)

The cron runs in an isolated session — it can only write to ChromaDB and the papers directory. It cannot read or write MEMORY.md, SOUL.md, or any identity files.

---

## Phase 3: Create the Search Skill

Copy and paste the following into the web chat:

> Read `https://raw.githubusercontent.com/charanbobby/OpenClaw/master/course/days/day-11-teach-it-to-learn/claw-instructions-create-knowledge-search.md` and follow every step. Create a skill called `knowledge-search` that queries the ChromaDB knowledge base using hybrid search (semantic + keyword). The skill should return relevant chunks with source citations. Stop when the skill responds correctly to a test query.

Alternatively, paste the contents of [`claw-instructions-create-knowledge-search.md`](./claw-instructions-create-knowledge-search.md) directly into the chat.

Test it:

> Search my knowledge base for: "How does RAG improve factual accuracy?"

The Claw should retrieve chunks from the Lewis et al. paper you ingested in Phase 2 and cite the source.

### Verify the Skill

```
openclaw doctor
openclaw security audit
clawvet scan ~/.openclaw/workspace/skills/knowledge-search/
```

All checks must pass before proceeding.

---

## Phase 4: Configure the Human-Gated Improvement Loop

This is the security-critical phase. Read this section fully before pasting anything into chat.

### What This Phase Does

You are giving your Claw the ability to:
1. Read its own knowledge base (already possible from Phase 3)
2. Generate a weekly "Learning Report" summarizing what it found
3. Propose changes to MEMORY.md based on those findings
4. **Wait for your explicit approval before changing anything**

### What This Phase Does NOT Do

- It does not let the Claw modify MEMORY.md automatically
- It does not let the Claw install skills automatically
- It does not let the Claw change SOUL.md, USER.md, or AGENTS.md at all
- It does not let the Claw run any proposed changes without your per-diff approval

### Setup

Copy and paste the following into the web chat:

> Read `https://raw.githubusercontent.com/charanbobby/OpenClaw/master/course/days/day-11-teach-it-to-learn/claw-instructions-setup-improvement-loop.md` and follow every step. Configure a weekly synthesis task that reads the ChromaDB knowledge base, generates a Learning Report, and sends me a Telegram summary with proposed changes. No changes to any config file without my explicit approval. Stop when you've explained the full approval flow.

Alternatively, paste the contents of [`claw-instructions-setup-improvement-loop.md`](./claw-instructions-setup-improvement-loop.md) directly into the chat.

### The Approval Flow

When the weekly synthesis runs, you'll get a Telegram message like:

```
Weekly Learning Report ready.

3 insights found:
1. "Chain-of-thought prompting improves reasoning by 40% on GSM8K" — 5 papers confirm this
2. "Tool-use agents perform better with explicit planning steps" — 3 papers
3. "RAG retrieval quality degrades with chunk sizes over 1000 tokens" — suggests reviewing our chunking config

Proposed actions:
- Update MEMORY.md: add insight #1 to Patterns section
- Update MEMORY.md: add insight #3 as a config note
- No action for #2 (already reflected in AGENTS.md)

Full report: ~/openclaw-reports/2026-03-29-weekly.md

Reply "approve all", "approve 1,3", or "skip" to this message.
```

- **"approve all"** — the Claw shows you the exact diff for each change, one at a time. You confirm each.
- **"approve 1,3"** — only the specified insights are applied, with per-diff confirmation.
- **"skip"** — nothing changes. The report is saved for future reference.

### Setting Up the Weekly Schedule

Open the OpenClaw UI and create a new scheduled task:

- **Task:** Run the Learning Report synthesis
- **Schedule:** Weekly (e.g., every Sunday at 9am)
- **Action:** Query ChromaDB for papers ingested this week, generate report, send Telegram summary
- **Session type:** Isolated (read-only access to ChromaDB, no write access to config)

---

## Security Checklist

Before considering Day 11 complete, verify all of these:

- [ ] ChromaDB is running and storing vectors at `~/.openclaw/chromadb/`
- [ ] The ingestion pipeline can process a PDF end to end
- [ ] The `knowledge-search` skill returns relevant results with citations
- [ ] The ingestion cron runs in an isolated session (no identity file access)
- [ ] The synthesis cron runs read-only (can query ChromaDB, cannot write config)
- [ ] The Telegram approval flow works — you received a test message
- [ ] Saying "skip" results in zero changes to any file
- [ ] Saying "approve" shows you the diff before writing
- [ ] Previous versions are saved as `.bak` files after any approved change
- [ ] `openclaw doctor` passes
- [ ] `openclaw security audit` shows no critical failures
- [ ] `clawvet scan` passes on the knowledge-search skill

---

## What Should Be True After Day 11

- [ ] Your Claw has a searchable knowledge base of AI research papers
- [ ] New papers are ingested automatically on a schedule you configured
- [ ] You can ask questions and get answers grounded in real research with citations
- [ ] Your Claw proposes self-improvements weekly, but changes nothing without your approval
- [ ] Every proposed change shows an exact diff before you confirm
- [ ] Skill drafts go to a draft folder and require manual install after clawvet scan
- [ ] You understand RAG: embeddings, chunking, vector search, and hybrid retrieval

---

## Quick Win

Ask your Claw:

> What are the most cited techniques for improving RAG retrieval quality, based on papers in my knowledge base?

If it gives you a grounded answer with paper citations, Day 11 is working.

---

## Troubleshooting

### ChromaDB won't install — out of memory
Your VPS may need a swap file. Run:
```bash
sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile
```
Then retry the install.

### Docling fails on a specific PDF
Not all PDFs parse cleanly. Try:
```bash
python3 -c "from docling.document_converter import DocumentConverter; dc = DocumentConverter(); result = dc.convert('path/to/paper.pdf'); print(result.document.export_to_markdown()[:500])"
```
If it fails, the PDF may have unusual formatting. Skip it and try another paper.

### Embedding model download is slow
The `all-MiniLM-L6-v2` model is ~80MB. If the download stalls, check your VPS internet speed with `curl -o /dev/null -w '%{speed_download}' https://speed.hetzner.de/100MB.bin`. If it's under 1MB/s, try downloading during off-peak hours.

### The Claw modified a config file without approval
This is a bug in the improvement loop configuration. Immediately:
1. Check for `.bak` files and restore: `cp ~/.openclaw/workspace/MEMORY.md.bak ~/.openclaw/workspace/MEMORY.md`
2. Run `openclaw security audit --deep`
3. Review the claw-instructions for the improvement loop — the write constraint may need tightening
4. Report the issue so the instructions can be fixed

### The weekly report is empty
The synthesis task may not have found papers ingested in the past week. Check:
```bash
python3 -c "import chromadb; c = chromadb.PersistentClient('~/.openclaw/chromadb'); print(c.get_collection('papers').count())"
```
If the count is 0, the ingestion cron may not be running. Check your scheduled tasks in the UI.

---

## Day 11 Verification Check

Add this to the Day 10 verification sweep if you extend it:

```markdown
## Day 11: Teach It to Learn

**Check:** ChromaDB collection `papers` exists with at least one document, `knowledge-search` skill is installed, improvement loop requires per-diff approval
**Pass:** knowledge-search returns cited results, "skip" produces zero config changes, "approve" shows diff before writing
**Fail:** empty knowledge base, missing skill, or any config change without explicit approval
```
