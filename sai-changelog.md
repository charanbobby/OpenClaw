# SAI Configuration Changelog

Tracks every change to the SAI's operating files (AGENTS.md, MEMORY.md, SOUL.md, openclaw.json) on the VPS — what changed, why, and the source.

---

## 2026-04-01

### AGENTS.md — Memory Management
**Added:**
```
- For durable habits, especially retrieval and memory use, store them only after repeated validation and keep them structured by workflow, project, and safety note.
```
**Why:** Agent memory papers (A-Mem, Learning to Commit) show that flat, unorganized memory degrades over time. Structured, validated memory with separate categories (workflow, project, safety) performs better.
**Source papers:**
- *A-Mem: Agentic Memory for LLM Agents*
- *Learning to Commit: Generating Organic Pull Requests via Online Repository Memory*

---

### AGENTS.md — Security Protocols
**Added:**
```
- Do not treat chain-of-thought or internal reasoning as faithful evidence of what caused an output. Verbal reasoning traces can diverge from actual causes. Corroborate with external evidence before citing internal reasoning as proof.
```
**Why:** Chain-of-thought reasoning can be unfaithful — the model's verbal reasoning may not reflect the actual causes of its output. This prevents the SAI from citing its own reasoning as proof.
**Source paper:**
- *Lie to Me: How Faithful Is Chain-of-Thought Reasoning in Reasoning Models?*

---

### AGENTS.md — Response Defaults
**Added:**
```
- Prefer retrieval-based answers for prior work, long-running context, stored decisions, or any question where memory may be stale.
- When answering with retrieval, separate evidence from inference.
```
**Why:** Multiple RAG papers emphasize that retrieval quality, evidence accumulation, and grounding need to be first-class concerns — not just end-answer accuracy. Separating evidence from inference makes answers more honest.
**Source papers:**
- *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*
- *Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection*
- *Chain-of-Note: Enhancing Robustness in Retrieval-Augmented Language Models*
- *A Survey on RAG Meeting LLMs: Towards Retrieval-Augmented Large Language Models*

---

### MEMORY.md — Open Loops
**Added:**
```
- Prefer retrieval over raw recall when an answer depends on prior work, stored decisions, or long-running context.
```
**Why:** Same as Response Defaults change above — codifies the retrieval preference as a persistent pattern the SAI remembers across sessions.

---

### MEMORY.md — Patterns
**Added:**
```
- When using research or stored context, keep answers short, evidence-linked, and split into what the source says versus what is inferred when that distinction matters.
```
**Why:** Validated preference for how research-heavy answers should be formatted. Evidence handling is where AI answers go wrong most often.
**Source papers:**
- *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*
- *Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection*

---

### openclaw.json — Gateway Auth
**Changed:** Added `OPENCLAW_GATEWAY_PASSWORD=admin` env var to match config file's `gateway.auth.password: "admin"`
**Why:** Gateway exec tool was failing with "unauthorized: gateway password missing/mismatch". The password in the config file (`admin`) didn't match what was provided via environment variable. The exec tool reads from the config, so the env var must match.
**Source:** Debugging session — gateway logs showed `GatewayClientRequestError: unauthorized: gateway password mismatch`

---

### openclaw.json — Exec Security
**Changed:** `tools.exec.security` set from default to `"full"`
**Why:** Without this, every shell command required manual approval in the Control UI. Since the user isn't always at the computer, exec needs to run autonomously via Telegram.
**Source:** Debugging session — SAI couldn't run any commands from Telegram without UI approval

---

### AGENTS.md — Email Skill Paths
**Added:**
```
## Email Skill Paths (imap-smtp-email)

- Skill directory: ~/.openclaw/workspace/skills/imap-smtp-email/
- IMAP script: node ~/.openclaw/workspace/skills/imap-smtp-email/scripts/imap.js
- SMTP script: node ~/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js
- Config: ~/.config/imap-smtp-email/.env
- Working directory for exec: ~/.openclaw/workspace/
- Relative path from workspace: node skills/imap-smtp-email/scripts/imap.js check --limit 10
- These paths are fixed. Do not look in /app/skills/ for user-installed skills.
```
**Why:** SAI kept looking for the email skill at `/app/skills/imap-smtp-email/` (bundled skills directory) instead of the correct workspace path. Explicit paths prevent the model from guessing wrong.
**Source:** Debugging session — gateway logs showed `ENOENT: no such file or directory, access '/app/skills/imap-smtp-email/SKILL.md'`
