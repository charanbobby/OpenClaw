# Day 7: Make It Research

---

**What you'll learn today:**
- What live web search adds to OpenClaw, and why it changes the quality of current answers
- The difference between search and fetch, and which part we are actually using today
- How web content introduces the same injection risks you handled with email, and what changes
- What a well-designed research brief looks like versus a vague one

**What you'll build today:** By the end of today, your Claw can browse the live web using Vercel's `agent-browser`, answer current questions with real source links, and it has one reusable `research-brief` skill built on top of that.

---

## Your Claw Goes Out Into the World

Until now, your Claw has worked with information that comes to it: messages you send, emails that land in your inbox. Today we add a new kind of reach. Your Claw can go out, look up something current, and come back with sources.

That changes the kind of questions it can answer well. "What changed this week in AI agents?" or "What are people saying about this product launch?" are live questions. Model memory alone is not enough there. The search tool is what turns your Claw into something useful on moving topics.

By the end of today, you'll be able to message your Claw and ask a time-sensitive question, then get back a short answer with links you can inspect yourself. Then you turn that into a reusable `research-brief` skill.

---

## Two Tools, Two Speeds

OpenClaw has a few ways to reach the web, and they do different jobs.

The main one for today is Vercel's [`agent-browser`](https://agent-browser.dev/). It is a headless browser automation CLI built specifically for AI agents. Instead of returning search snippets through an API, `agent-browser` opens real web pages and reads them through accessibility snapshots — the same semantic tree that screen readers use. Your Claw sees element refs like `@e1`, `@e2`, and can click, type, scroll, and extract content from any page.

This is more powerful than a search API. Your Claw can visit a specific site, navigate through pages, fill forms, and read content that search engines might not index. It can also search Google directly by opening it and reading the results.

OpenClaw also has [`web_fetch`](https://docs.openclaw.ai/tools/web-fetch), which is useful when you already know the page you want and just need the raw content. That is a lighter-weight option. But `agent-browser` handles both simple lookups and complex multi-step browsing.

Here's how the flow works:

![How research flows through your Claw](../../diagrams/day-07-research-flow.png)

The build walks you through setting up `agent-browser` and turning it into a reusable research workflow.

---

## Extending Your Injection Protection

On Day 6, you learned that email is an open channel where anyone can put text in front of your Claw. The web works the same way. Search results, snippets, and fetched pages are all external content. Any of them can contain text that looks like instructions to the model.

The good news is that the mental model is already familiar. The same rule still applies: external content is data, not instructions. OpenClaw's own [security guidance](https://docs.openclaw.ai/gateway/security) treats tools like `web_search` and `web_fetch` as higher-risk because they bring untrusted content into the loop. So Day 7 adds one short rule to your workspace `AGENTS.md`: web content gets summarized, cited, and filtered. It does not get obeyed.

That is the practical baseline. It will not solve prompt injection forever. It gives your Claw a sane posture before you start asking it to pull from the open web.

---

## Designing a Research Brief That Works

A vague research prompt produces a vague answer. "Tell me about AI news this week" leaves too much up to the model. The answer might be fine. It might also miss the part you actually cared about.

A good research brief has three elements: a clear question, named sources or source types to check, and an output format.

```
Research Brief: Vague vs. Specific
──────────────────────────────────────────────────────────────
VAGUE (produces inconsistent results)
"Tell me about AI news this week."

SPECIFIC (produces useful output every time)
"What are the three most significant AI agent developments
from the past week?

Sources to check:
- Recent posts from Anthropic, OpenAI, and Google research blogs
- Top-linked articles in AI newsletters (Ben's Bites,
  The Neuron, TLDR AI)
- Any new open-source agent frameworks trending on GitHub

Output format:
Three items. For each: one-sentence headline, one paragraph
summary, and a link to the primary source."
──────────────────────────────────────────────────────────────
```

The pattern is simple: narrow the question, name the sources, define the shape of the answer. That is what turns search into useful research, and it is also the shape of the skill you create in the build.

---

## Ready to Build?

You now understand what live web browsing adds, where it fits in OpenClaw's tool stack, why web content needs the same security posture as email, and how a specific research prompt beats a vague one. The build verifies `agent-browser` is working, extends your research guardrails, and turns that into one reusable research skill. [`build.md`](build.md) shows you the sequence and points to the short `claw-instructions-*.md` files that belong in OpenClaw chat.

Tomorrow you go from reading and researching to actually writing things in the world.

---

## Go Deeper

- Vercel's [`agent-browser` documentation](https://agent-browser.dev/) covers installation, commands, and the ref-based element model. The [GitHub repo](https://github.com/vercel-labs/agent-browser) has the full README and skill definitions.
- [`web_fetch`](https://docs.openclaw.ai/tools/web-fetch) is a lighter alternative if you just need the raw content of a known URL without full browser automation.

---

[← Day 6: Tame Your Inbox](../day-06-tame-your-inbox/learn.md) | [Day 8: Let It Write →](../day-08-let-it-write/learn.md)