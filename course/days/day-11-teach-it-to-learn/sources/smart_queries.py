"""Smart query generator — reads AGENTS.md and MEMORY.md to derive search topics.

Extracts themes from the agent's current config and knowledge gaps
to generate targeted research queries.
"""
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw" / "workspace"
AGENTS_PATH = WORKSPACE / "AGENTS.md"
MEMORY_PATH = WORKSPACE / "MEMORY.md"

# Topics we always want to learn about
BASE_TOPICS = [
    "retrieval augmented generation improvements",
    "LLM self-improvement techniques",
    "AI agent architecture",
]

# Map keywords found in AGENTS.md to research queries
KEYWORD_TO_QUERY = {
    "retrieval": "improving retrieval quality for RAG systems",
    "critique": "LLM self-critique and self-reflection methods",
    "evidence": "grounding LLM responses in evidence",
    "approval": "human-in-the-loop AI safety",
    "memory": "long-term memory for AI agents",
    "email": "AI email processing and summarization",
    "delegation": "multi-agent delegation and coordination",
    "tool use": "LLM tool use and function calling",
    "reasoning": "chain of thought reasoning in language models",
    "embedding": "text embedding models for semantic search",
    "chunking": "document chunking strategies for RAG",
    "hallucination": "reducing hallucination in language models",
    "prompt engineering": "automated prompt optimization",
    "reinforcement learning": "reinforcement learning from human feedback",
    "fine-tuning": "parameter efficient fine-tuning methods",
}


def read_file(path):
    """Read file content or return empty string."""
    try:
        return path.read_text(encoding="utf-8", errors="ignore").lower()
    except Exception:
        return ""


def generate_queries(max_queries=5):
    """Generate search queries based on current agent config."""
    agents_text = read_file(AGENTS_PATH)
    memory_text = read_file(MEMORY_PATH)
    combined = agents_text + " " + memory_text

    # Find which keywords appear in the agent's config
    matched = []
    for keyword, query in KEYWORD_TO_QUERY.items():
        if keyword in combined:
            matched.append(query)

    # Combine: matched queries first (most relevant), then base topics
    all_queries = matched + [q for q in BASE_TOPICS if q not in matched]

    # Deduplicate and limit
    seen = set()
    unique = []
    for q in all_queries:
        if q not in seen:
            seen.add(q)
            unique.append(q)

    return unique[:max_queries]


if __name__ == "__main__":
    queries = generate_queries()
    print("Smart queries generated from AGENTS.md + MEMORY.md:")
    for i, q in enumerate(queries, 1):
        print("  " + str(i) + ". " + q)
