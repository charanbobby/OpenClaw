#!/usr/bin/env python3
"""ChromaDB knowledge base maintenance.

Manages paper lifecycle with tier system:
  - hot:    last 30 days, full search priority
  - warm:   30-90 days, still searchable
  - cold:   90+ days, never referenced — auto-deleted
  - pinned: led to an approved change — never deleted

Usage:
  python3 db_maintenance.py status          # Show tier breakdown
  python3 db_maintenance.py pin <arxiv_id>  # Pin a paper permanently
  python3 db_maintenance.py prune           # Delete cold-tier papers
  python3 db_maintenance.py prune --dry-run # Show what would be deleted
"""
import argparse
import datetime as dt
import json
from collections import defaultdict
from pathlib import Path

import chromadb

CHROMA_DIR = Path.home() / ".openclaw" / "chromadb"
COLLECTION_NAME = "papers"
PINNED_FILE = Path.home() / ".openclaw" / "chromadb" / "pinned_papers.json"

HOT_DAYS = 30
WARM_DAYS = 90


def get_collection():
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(COLLECTION_NAME)


def load_pinned():
    """Load set of pinned arxiv IDs."""
    if PINNED_FILE.exists():
        try:
            return set(json.loads(PINNED_FILE.read_text()))
        except Exception:
            return set()
    return set()


def save_pinned(pinned):
    """Save pinned arxiv IDs."""
    PINNED_FILE.parent.mkdir(parents=True, exist_ok=True)
    PINNED_FILE.write_text(json.dumps(sorted(pinned), indent=2))


def get_tier(ingest_date_str, source_url, pinned_ids):
    """Determine tier for a paper."""
    import re
    match = re.search(r"(\d{4}\.\d{4,5})", source_url)
    arxiv_id = match.group(1) if match else ""

    if arxiv_id in pinned_ids:
        return "pinned"

    try:
        parsed = dt.datetime.fromisoformat(ingest_date_str.replace("Z", "+00:00"))
        age_days = (dt.datetime.now(dt.timezone.utc) - parsed).days
    except Exception:
        age_days = 999

    if age_days <= HOT_DAYS:
        return "hot"
    elif age_days <= WARM_DAYS:
        return "warm"
    else:
        return "cold"


def cmd_status(args):
    """Show tier breakdown."""
    col = get_collection()
    data = col.get(include=["metadatas"])
    pinned = load_pinned()

    papers = defaultdict(lambda: {"title": "", "chunks": 0, "tier": "", "date": ""})
    for m in data["metadatas"]:
        src = m.get("source_url", "")
        papers[src]["title"] = m.get("title", "?")
        papers[src]["chunks"] += 1
        papers[src]["date"] = m.get("ingest_date", "")
        papers[src]["tier"] = get_tier(m.get("ingest_date", ""), src, pinned)

    tier_counts = defaultdict(int)
    tier_chunks = defaultdict(int)

    print("Papers by tier:")
    print()
    for tier_name in ["pinned", "hot", "warm", "cold"]:
        tier_papers = [(s, p) for s, p in papers.items() if p["tier"] == tier_name]
        if not tier_papers:
            continue
        print("  [" + tier_name.upper() + "]")
        for src, p in sorted(tier_papers, key=lambda x: x[1]["date"], reverse=True):
            print("    " + str(p["chunks"]) + " chunks | " + p["title"][:55] + " | " + p["date"][:10])
            tier_counts[tier_name] += 1
            tier_chunks[tier_name] += p["chunks"]
        print()

    print("Summary:")
    total_papers = 0
    total_chunks = 0
    for tier_name in ["pinned", "hot", "warm", "cold"]:
        if tier_counts[tier_name]:
            print("  " + tier_name + ": " + str(tier_counts[tier_name]) + " papers, " + str(tier_chunks[tier_name]) + " chunks")
            total_papers += tier_counts[tier_name]
            total_chunks += tier_chunks[tier_name]
    print("  total: " + str(total_papers) + " papers, " + str(total_chunks) + " chunks")


def cmd_pin(args):
    """Pin a paper so it's never deleted."""
    pinned = load_pinned()
    arxiv_id = args.arxiv_id.strip()
    pinned.add(arxiv_id)
    save_pinned(pinned)
    print("Pinned: " + arxiv_id)
    print("Total pinned: " + str(len(pinned)))


def cmd_prune(args):
    """Delete cold-tier papers."""
    col = get_collection()
    data = col.get(include=["metadatas"])
    pinned = load_pinned()

    cold_ids = []
    cold_papers = set()
    for cid, m in zip(data["ids"], data["metadatas"]):
        src = m.get("source_url", "")
        tier = get_tier(m.get("ingest_date", ""), src, pinned)
        if tier == "cold":
            cold_ids.append(cid)
            cold_papers.add(m.get("title", "?"))

    if not cold_ids:
        print("No cold-tier papers to prune.")
        return

    print("Cold-tier papers to prune:")
    for title in sorted(cold_papers):
        print("  - " + title)
    print("Total: " + str(len(cold_ids)) + " chunks from " + str(len(cold_papers)) + " papers")

    if args.dry_run:
        print("\n(dry run - nothing deleted)")
        return

    col.delete(ids=cold_ids)
    print("\nDeleted " + str(len(cold_ids)) + " chunks.")
    print("New collection size: " + str(col.count()) + " chunks")


def main():
    parser = argparse.ArgumentParser(description="ChromaDB knowledge base maintenance")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="Show tier breakdown")

    pin_p = sub.add_parser("pin", help="Pin a paper permanently")
    pin_p.add_argument("arxiv_id", help="arXiv ID to pin (e.g. 2005.11401)")

    prune_p = sub.add_parser("prune", help="Delete cold-tier papers")
    prune_p.add_argument("--dry-run", action="store_true", help="Show what would be deleted")

    args = parser.parse_args()

    if args.command == "status":
        cmd_status(args)
    elif args.command == "pin":
        cmd_pin(args)
    elif args.command == "prune":
        cmd_prune(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
