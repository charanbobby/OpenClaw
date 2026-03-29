"""Semantic Scholar source — free API, 100 req/sec.

Supports custom queries via set_queries() or uses defaults.
"""
import json
from urllib.request import Request, urlopen
from urllib.parse import quote

API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
USER_AGENT = "OpenClaw-Research-Bot/1.0 (sai@sshub.dev)"
DEFAULT_QUERIES = ["RAG retrieval augmented generation", "LLM agents", "AI reasoning"]

_custom_queries = None


def set_queries(queries):
    """Override default queries with custom ones."""
    global _custom_queries
    _custom_queries = queries


def fetch_new(since=None, max_papers=5):
    """Fetch recent papers from Semantic Scholar."""
    queries = _custom_queries if _custom_queries else DEFAULT_QUERIES
    papers = []
    seen_ids = set()

    for query in queries:
        if len(papers) >= max_papers:
            break
        try:
            url = API_URL + "?query=" + quote(query) + "&limit=5&fields=title,externalIds,url&year=2024-2026"
            req = Request(url, headers={"User-Agent": USER_AGENT})
            resp = urlopen(req, timeout=30)
            data = json.loads(resp.read().decode("utf-8"))

            for item in data.get("data", []):
                if len(papers) >= max_papers:
                    break
                title = item.get("title", "Unknown")
                ext_ids = item.get("externalIds") or {}
                arxiv_id = ext_ids.get("ArXiv")
                if not arxiv_id or arxiv_id in seen_ids:
                    continue
                seen_ids.add(arxiv_id)

                papers.append({
                    "title": title,
                    "url": "https://arxiv.org/abs/" + arxiv_id,
                    "pdf_url": "https://arxiv.org/pdf/" + arxiv_id,
                    "source_name": "semantic_scholar",
                    "arxiv_id": arxiv_id,
                })
        except Exception as e:
            print("Semantic Scholar error (" + query + "): " + str(e))
            continue

    return papers


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        set_queries(sys.argv[1:])
    results = fetch_new(max_papers=5)
    for p in results:
        print("  " + p.get("title", "?")[:80] + " | " + p.get("url", "?"))
    print("Total: " + str(len(results)))
