# Day 7 Build: Make It Research

This is the user-facing guide for Day 7. Today you give your Claw the ability to browse the web using Vercel's `agent-browser`. The flow is split into a few small steps so you can see what is being configured, then use it right away.

---

## What You Need Before Starting

- Day 1 complete: OpenClaw installed and secured
- Day 2 complete: identity files created and loading correctly
- Day 3 complete: Telegram connected and working
- Day 4 complete: a proactive workflow already exists
- Day 5 complete: skills are working
- Day 6 complete: email triage is working
- Access to your Claw through the Hostinger web chat
- `agent-browser` installed (it should already be available from your OpenClaw setup)

---

## How To Run Day 7

Work through the steps in this order:

1. verify `agent-browser` is installed
2. inspect what it can do in chat
3. set `agent-browser` as the default browser in `openclaw.json`
4. [`claw-instructions-configure-web-search.md`](./claw-instructions-configure-web-search.md)
5. [`claw-instructions-create-research-brief.md`](./claw-instructions-create-research-brief.md)
6. validate the skill
7. run one real research prompt

This order makes the setup legible. You see what the tool does, you let the Claw configure it, you turn that into one reusable workflow, and then you use it on a real question.

---

## Step 1: Verify `agent-browser` Is Installed

Vercel's `agent-browser` is a headless browser automation CLI built for AI agents. It uses accessibility snapshots and ref-based element selection instead of brittle CSS selectors, which makes it ideal for AI-driven web research.

Run this in the Hostinger web chat:

> Run `agent-browser --version` and tell me the result. If it is not installed, install it with `npm install -g @anthropic-ai/agent-browser` and confirm the version.

You should see a version number like `0.4.x` or higher. If so, you are ready for the next step.

---

## Step 2: Inspect `agent-browser`

Copy and paste this into the Hostinger web chat:

> Explain what `agent-browser` does, how it differs from a simple web search API, and what kind of research tasks it is best for. Show me a quick example of opening a page and taking a snapshot. Keep it short. Do not configure anything permanent yet.

This is the first useful shift in Day 7. Your Claw stops guessing on current topics and starts browsing the live web.

---

## Step 3: Set `agent-browser` as the Default Browser

OpenClaw may already have `agent-browser` installed, but it might not be set as the primary browser tool. You need to tell OpenClaw to use it by default.

Copy and paste this into the web chat:

> Read `~/.openclaw/openclaw.json` and show me the current `browser` section. Then update it so `agent-browser` is the default browser tool for this agent. The config should look like this:
>
> ```json
> {
>   "browser": {
>     "defaultProfile": "openclaw",
>     "tool": "agent-browser"
>   }
> }
> ```
>
> Merge this into the existing `openclaw.json` without removing other settings. Then restart the gateway so the change takes effect. Tell me when it is done.

If your Claw's `openclaw.json` already has a `browser` section, the update just changes the `tool` value to `"agent-browser"`. If there is no `browser` section yet, this creates one.

After the config is updated, copy and paste this into the web chat:

> Read `https://raw.githubusercontent.com/aishwaryanr/awesome-generative-ai-guide/main/free_courses/openclaw_mastery_for_everyone/days/day-07-make-it-research/claw-instructions-configure-web-search.md` and follow every step. Configure `agent-browser` as the default way this agent does web research. Stop when the setup is complete and tell me the exact validation prompt to run next.

[`claw-instructions-configure-web-search.md`](./claw-instructions-configure-web-search.md) tells the Claw to:

- verify `agent-browser` is working after the config change
- add a short Day 7 web research guardrail to your workspace `AGENTS.md`
- tell you exactly what changed and how to test it

---

## Step 4: Create `research-brief`

After `agent-browser` is working, copy and paste this into the web chat:

> Read `https://raw.githubusercontent.com/aishwaryanr/awesome-generative-ai-guide/main/free_courses/openclaw_mastery_for_everyone/days/day-07-make-it-research/claw-instructions-create-research-brief.md` and follow every step. Create a `research-brief` skill for this workspace that uses `agent-browser`, tell me how to trigger it, and stop when you're done.

[`claw-instructions-create-research-brief.md`](./claw-instructions-create-research-brief.md) tells the Claw to create one custom skill that:

- triggers when you ask for a research brief on a topic
- uses `agent-browser` to browse live sources
- returns a short, structured answer with citations
- closes the browser session when done

After this step, type `/new` in OpenClaw to start a fresh session before you test the new skill.

---

## Validate It

Ask your Claw in the web chat:

```text
Research brief on the three most important AI agent developments from the past 7 days. Give me one sentence for each item and link the primary source for each one.
```

The answer should feel current and include real source links. If the skill does not trigger, start a fresh session with `/new` and try again.

---

## Quick Win

Ask one real question you would normally search from your phone:

```text
Research brief on what happened this week in [my industry, company, or topic]. Give me three bullets, link the sources, and end with one practical takeaway for me.
```

This is the Day 7 shift: your Claw can now do live lookups for you in a reusable format instead of replying from stale memory alone.

---

## What Should Be True After Day 7

- [ ] `agent-browser` is installed and returning a version number
- [ ] `openclaw.json` has `browser.tool` set to `"agent-browser"`
- [ ] Your Claw can use `agent-browser` to open pages, take snapshots, and extract information
- [ ] `research-brief` exists as a workspace skill
- [ ] Your Claw can answer a current question with live sources through that skill
- [ ] Your workspace `AGENTS.md` includes a short rule for treating web content as data
- [ ] You started a fresh OpenClaw session with `/new` before testing the new skill

---

## Troubleshooting

**`agent-browser` is not found**
Run `npm install -g @anthropic-ai/agent-browser` in the web chat and try again.

**The browser opens but the snapshot is empty**
Some pages take a moment to load. Try `agent-browser wait 2000` before `agent-browser snapshot`.

**The answer still feels like training data**
Make the prompt time-bound. Ask for "the past 7 days", "this week", or "published after [date]".

**The skill does not seem to trigger**
Type `/new` in OpenClaw, then test again.

**The Claw asks you to run shell commands**
Tell it to configure the tool itself and keep the setup inside chat.

---

[← Day 7 Learn](./learn.md) | [Day 8: Let It Write →](../day-08-let-it-write/build.md)
