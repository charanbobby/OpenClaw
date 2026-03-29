#!/usr/bin/env python3
"""Round-robin research fetcher.

Cycles through sources, deduplicates, downloads PDFs, and ingests into ChromaDB.
"""
import importlib
import importlib.util
import os
import sys
import time
from pathlib import Path

SOURCES_DIR = Path(__file__).resolve().parent / "sources"
INGEST_SCRIPT = Path.home() / ".openclaw" / "workspace" / "scripts" / "ingest_paper.py"
PAPERS_DIR = Path.home() / "openclaw-ingestion" / "papers"
PDF_DELAY = 10  # seconds between PDF downloads

# Import ingest function
sys.path.insert(0, str(INGEST_SCRIPT.parent))
from ingest_paper import ingest, canonical_url, get_collection


def load_sources():
    """Dynamically load all source modules from sources/ directory."""
    sources = []
    for f in sorted(SOURCES_DIR.glob("*.py")):
        if f.name.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location(f.stem, str(f))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, "fetch_new"):
            sources.append((f.stem, mod))
    return sources


def already_have(collection, arxiv_id):
    """Check if paper is already in ChromaDB."""
    canon = "https://arxiv.org/abs/" + arxiv_id
    try:
        results = collection.get(where={"source_url": canon}, limit=1)
        return bool(results and results.get("ids"))
    except Exception:
        return False


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-per-source", type=int, default=2,
                        help="Max papers to fetch per source (default: 2)")
    parser.add_argument("--max-total", type=int, default=5,
                        help="Max total papers to ingest (default: 5)")
    parser.add_argument("--dry-run", action="store_true",
                        help="List papers without downloading or ingesting")
    parser.add_argument("--smart", action="store_true",
                        help="Use smart queries derived from AGENTS.md and MEMORY.md")
    parser.add_argument("--queries", nargs="+",
                        help="Custom search queries (overrides defaults)")
    args = parser.parse_args()

    # Apply smart or custom queries to Semantic Scholar source
    if args.smart or args.queries:
        if args.smart:
            sys.path.insert(0, str(SOURCES_DIR))
            from smart_queries import generate_queries
            queries = generate_queries(max_queries=5)
            print("Smart queries from AGENTS.md + MEMORY.md:")
            for i, q in enumerate(queries, 1):
                print("  " + str(i) + ". " + q)
            print()
        else:
            queries = args.queries
            print("Custom queries: " + str(queries))
            print()

        # Set queries on semantic_scholar source if loaded
        try:
            spec = importlib.util.spec_from_file_location(
                "semantic_scholar", str(SOURCES_DIR / "semantic_scholar.py"))
            ss_mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(ss_mod)
            ss_mod.set_queries(queries)
        except Exception as e:
            print("Warning: could not set smart queries on semantic_scholar: " + str(e))

    sources = load_sources()
    if not sources:
        print("No sources found in sources/ directory.")
        return 1

    collection = get_collection()
    source_names = [name for name, _ in sources]
    print("Sources loaded: " + str(source_names))
    print("ChromaDB collection size: " + str(collection.count()) + " chunks")
    print()

    # Round-robin: take max_per_source from each, up to max_total
    candidates = []
    for name, mod in sources:
        try:
            papers = mod.fetch_new(max_papers=args.max_per_source)
            new_count = 0
            for p in papers:
                aid = p.get("arxiv_id", "")
                if aid and not already_have(collection, aid):
                    p["fetched_from"] = name
                    candidates.append(p)
                    new_count += 1
            print("  [" + name + "] fetched " + str(len(papers)) + ", " + str(new_count) + " new")
        except Exception as e:
            print("  [" + name + "] ERROR: " + str(e))
            continue

    # Deduplicate by arxiv_id
    seen = set()
    unique = []
    for p in candidates:
        aid = p.get("arxiv_id", "")
        if aid not in seen:
            seen.add(aid)
            unique.append(p)

    to_ingest = unique[:args.max_total]

    if not to_ingest:
        print("\nNo new papers to ingest.")
        return 0

    print("\nPapers to ingest: " + str(len(to_ingest)))
    for p in to_ingest:
        src = p.get("fetched_from", "?")
        ttl = p.get("title", "?")[:70]
        lnk = p.get("url", "?")
        print("  [" + src + "] " + ttl + " | " + lnk)

    if args.dry_run:
        print("\n(dry run - nothing downloaded or ingested)")
        return 0

    # Download and ingest with delays
    ingested = 0
    for i, p in enumerate(to_ingest):
        ttl = p.get("title", "?")[:60]
        print("\nIngesting " + str(i + 1) + "/" + str(len(to_ingest)) + ": " + ttl + "...")
        try:
            result = ingest(p.get("url", ""), title_hint=p.get("title", ""))
            if result["status"] == "ingested":
                print("  OK: " + str(result["chunk_count"]) + " chunks, total: " + str(result["collection_total"]))
                ingested += 1
            elif result["status"] == "duplicate":
                print("  Skipped (duplicate)")
        except Exception as e:
            print("  FAILED: " + str(e))
        if i < len(to_ingest) - 1:
            print("  Waiting " + str(PDF_DELAY) + "s...")
            time.sleep(PDF_DELAY)

    print("\nDone. Ingested " + str(ingested) + " new papers.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
