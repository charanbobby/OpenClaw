# Day 11: Set Up the Human-Gated Improvement Loop

Configure a weekly synthesis task that reads the ChromaDB knowledge base, generates a Learning Report, and sends a Telegram summary with proposed changes. Nothing is modified without explicit human approval.

Before you start:

- confirm the `knowledge-search` skill is installed and working
- confirm ChromaDB has at least one paper ingested
- confirm Telegram delivery is configured
- if any prerequisite is missing, stop and report it

---

## 1. Create the Synthesis Script

Write a script at `~/.openclaw/workspace/scripts/weekly_synthesis.py` that:

- queries ChromaDB for all papers ingested in the past 7 days
- groups chunks by paper, extracts key findings and recurring themes
- generates a Learning Report markdown file saved to `~/openclaw-reports/YYYY-MM-DD-weekly.md`
- the report contains: summary of papers ingested, top insights (max 5), and proposed actions

The script must be **read-only**:

- it reads from ChromaDB — never writes, updates, or deletes
- it reads MEMORY.md to check what's already known — never writes to it
- it writes only to `~/openclaw-reports/` — a directory with no agent config files
- it never touches SOUL.md, USER.md, or AGENTS.md

Before writing the script, show the user what you plan to create and wait for confirmation.

---

## 2. Create the Proposal Skill

Write a skill at `~/.openclaw/workspace/skills/learning-proposal/SKILL.md` that:

- triggers when the weekly synthesis report is ready, or when the user asks "what did you learn this week?"
- reads the latest report from `~/openclaw-reports/`
- sends a Telegram summary in this exact format:

```
Weekly Learning Report ready.

[N] insights found:
1. "[insight]" — [evidence count] papers
2. "[insight]" — [evidence count] papers

Proposed actions:
- [action description for each insight]
- "No action" for insights already reflected in config

Full report: ~/openclaw-reports/YYYY-MM-DD-weekly.md

Reply "approve all", "approve 1,3", or "skip".
```

---

## 3. Configure the Approval Gate

This is the critical security layer. The proposal skill must enforce these rules with no exceptions:

**On "skip":**
- do nothing
- confirm to the user that no changes were made
- log the skip in the report file

**On "approve all" or "approve [numbers]":**
- for each approved insight, generate the exact diff that would be applied to MEMORY.md
- send each diff to Telegram one at a time in this format:

```
Change 1 of N:
Section: [which section of MEMORY.md]
Add: "[exact text to add]"

Apply this change? [yes/no]
```

- wait for "yes" before applying each individual change
- if "no", skip that change and move to the next
- before writing, save a backup: `cp MEMORY.md MEMORY.md.bak`
- after all approved changes are applied, run `openclaw security audit` and report the result
- if the audit fails, automatically restore from `.bak` and report the failure

**Forbidden actions (hardcoded, not configurable):**
- never modify SOUL.md, USER.md, or AGENTS.md
- never install a skill automatically
- never delete or overwrite existing MEMORY.md content — only append
- never apply a change without showing the diff first and receiving "yes"
- never batch multiple changes into a single write — one at a time only
- never proceed if `openclaw security audit` fails after a change

---

## 4. Skill Draft Gate (for Future Use)

If the synthesis identifies a pattern that could become a new skill:

- write the draft to `~/.openclaw/workspace/skill-drafts/[skill-name]/SKILL.md`
- notify the user via Telegram: "Skill draft ready: [name]. Review at [path]. Run `clawvet scan [path]` before installing."
- do not install the draft
- do not move it to the skills directory
- do not add it to any skill registry
- the user must manually review, scan, and install

---

## 5. Test the Full Loop

Run a test cycle:

1. Generate a Learning Report from the current knowledge base
2. Send the Telegram proposal message
3. Have the user reply "approve 1" (or whichever insight exists)
4. Show the diff for that insight
5. Wait for "yes"
6. Apply the change and run the security audit
7. Then test "skip" and confirm zero changes

Show the user the results of each step.

---

## 6. Final Report

Report PASS or FAIL for:

- synthesis script generates a report in `~/openclaw-reports/`
- synthesis script is read-only (does not write to agent config)
- Telegram proposal message matches the required format
- "skip" results in zero file changes
- "approve" shows a diff before writing
- each diff requires individual "yes" confirmation
- `.bak` file is created before any write
- `openclaw security audit` runs after changes
- audit failure triggers automatic rollback
- skill drafts go to `skill-drafts/` only, never auto-installed

Stop when the report is complete.
