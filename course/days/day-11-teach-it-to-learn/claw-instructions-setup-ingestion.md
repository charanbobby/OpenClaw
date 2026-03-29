# Day 11: Set Up the Ingestion Pipeline

Set up a RAG ingestion pipeline that fetches an AI research paper, parses it, chunks the text, embeds it, and stores it in ChromaDB.

Before you start:

- confirm ChromaDB, Docling, and sentence-transformers are installed (`python3 -c "import chromadb; import docling; from sentence_transformers import SentenceTransformer"`)
- confirm `~/.openclaw/chromadb/` and `~/openclaw-ingestion/papers/` exist
- if any prerequisite is missing, stop and report it

---

## 1. Create the Ingestion Script

Write a Python script at `~/.openclaw/workspace/scripts/ingest_paper.py` that:

- accepts an arXiv URL or PDF path as input
- downloads the PDF to `~/openclaw-ingestion/papers/`
- uses Docling `DocumentConverter` to extract clean markdown text
- chunks the text into ~500 token segments with ~50 token overlap
- embeds each chunk using `all-MiniLM-L6-v2` via sentence-transformers
- stores vectors + metadata (title, source URL, chunk index, ingest date) in a ChromaDB persistent collection called `papers` at `~/.openclaw/chromadb/`
- skips papers already in the collection (match by source URL)
- prints a summary: paper title, number of chunks created, collection total

Before writing the script, show the user what you plan to create and wait for confirmation.

---

## 2. Create the Fetch Script

Write a second script at `~/.openclaw/workspace/scripts/fetch_arxiv.py` that:

- queries the arXiv API for recent papers matching configurable search terms (default: `"AI agents" OR "retrieval augmented generation" OR "LLM reasoning"`)
- fetches the 5 most recent papers not already in the collection
- calls `ingest_paper.py` for each
- prints a summary of what was fetched and ingested
- exits cleanly if no new papers are found

---

## 3. Test End to End

Run the ingestion pipeline on a single paper to verify:

- use `https://arxiv.org/abs/2005.11401` (the RAG paper by Lewis et al.)
- show the user: paper title, chunk count, a sample of the first 3 chunks (first 100 characters each)
- confirm the paper is queryable: run a test similarity search for "retrieval augmented generation" and show the top result

---

## 4. Final Report

Report PASS or FAIL for:

- Docling successfully parsed the test PDF
- chunks were created and stored in ChromaDB
- similarity search returns relevant results
- duplicate detection works (re-running does not create duplicates)
- scripts are saved at the reported paths

Do not configure any scheduled tasks. The user will set up the cron schedule through the UI.

Stop when the report is complete.
