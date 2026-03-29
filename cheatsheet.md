# OpenClaw + Agent Browser Cheat Sheet

Copy-paste these commands from your phone. Designed for quick Telegram use.

---

## OpenClaw Skills (Telegram Triggers)

### Quick Note
Save a thought instantly. Auto-categorizes as idea/task/follow-up/reminder.
```
note: call dentist Monday
note: idea for newsletter about AI agents
note: follow up with Amir about the proposal
note: reminder to renew domain before April
```

### Document Summary
Summarize any text or link.
```
Summarize this text: [paste text here]
Use document-summary on this link: https://example.com/article
```

### Email Triage
Scan your inbox. Sorts into Urgent/Important/FYI/Skip.
```
Check my inbox
Triage my email
Show me urgent emails from the last 24 hours
```

### Research Brief
Quick web research on any topic using `agent-browser`.
```
Research brief on Canadian immigration policy changes 2026
Research brief on best practices for Hetzner VPS security
```

### Follow-Up Email
Draft and send follow-up emails. Always asks for approval first.
```
Send a follow-up to john@example.com about the project timeline
Send a follow-up to sarah@company.com about the meeting notes
```

### Writer Agent (Delegation)
Long-form writing: essays, newsletters, explainers. Drafts only, never sends.
```
Ask the writer to draft a newsletter about [topic]
Delegate to writer: write an explainer on [topic] for [audience]
```

### Daily Reflection (Cron)
Arrives automatically at your scheduled time via Telegram. To manage:
```
Show me my active cron jobs
Update my reflection time to 8:00 AM
Disable the daily reflection
```

### Morning Email Summary (Cron)
Auto-delivers urgent emails + open loops each morning. To manage:
```
Show me my morning summary cron job
Change morning summary to 7:30 AM
Run the morning summary now
```

---

## OpenClaw System Commands

```
/new              Start a fresh session (do this after adding skills)
/start            Pair with Telegram bot (first time only)
openclaw gateway restart    Restart after config changes
```

---

## Agent Browser Commands

Installed globally. Use from any terminal or AI agent.

### Navigation
```bash
agent-browser open https://example.com
agent-browser open https://google.com
agent-browser close
```

### See the Page (AI-friendly)
```bash
agent-browser snapshot          # Accessibility tree with @e1, @e2 refs
agent-browser screenshot page.png
agent-browser screenshot --full page.png   # Full page
agent-browser get title
agent-browser get url
```

### Click & Type
```bash
agent-browser click @e2
agent-browser dblclick @e3
agent-browser fill @e4 "search query"
agent-browser type @e5 "hello world"
agent-browser press Enter
agent-browser press Tab
```

### Find by Meaning (Semantic)
```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "test@example.com"
agent-browser find testid "login-btn" click
```

### Forms
```bash
agent-browser select @e6 "Option A"
agent-browser check @e7
agent-browser uncheck @e8
agent-browser upload @e9 /path/to/file.pdf
```

### Read Content
```bash
agent-browser get text @e3
agent-browser get html @e4
agent-browser get value @e5
agent-browser get attr @e6 href
```

### Wait for Things
```bash
agent-browser wait @e3                    # Wait for element
agent-browser wait 2000                   # Wait 2 seconds
agent-browser wait --text "Welcome"       # Wait for text
agent-browser wait --url "**/dashboard"   # Wait for URL
```

### Tabs & Windows
```bash
agent-browser tab                # List tabs
agent-browser tab new https://example.com
agent-browser tab 2              # Switch to tab 2
agent-browser tab close
agent-browser window new
```

### Viewport & Device
```bash
agent-browser set viewport 1920 1080
agent-browser set device "iPhone 15"
agent-browser set media dark
agent-browser set offline on
```

### Cookies & Storage
```bash
agent-browser cookies
agent-browser cookies set token abc123
agent-browser storage local
agent-browser storage local set key value
```

### Network
```bash
agent-browser network requests
agent-browser network route "*.ads.com" --abort
agent-browser network har start
agent-browser network har stop output.har
```

### Batch Mode (Multiple Commands)
```bash
echo '[["open","https://google.com"],["snapshot"],["close"]]' | agent-browser batch --json
```

### Run JavaScript
```bash
agent-browser eval "document.title"
agent-browser eval "window.scrollTo(0, document.body.scrollHeight)"
```

---

## Server Commands (Hetzner VPS)

### SSH In
```powershell
ssh -i "$env:USERPROFILE\.ssh\id_hetzner" sri@46.62.255.66
```

### Services Running on sshub.dev
| Service           | URL                        | Port  |
|-------------------|----------------------------|-------|
| Trilium Notes     | notes.sshub.dev            | 8080  |
| Uptime Kuma       | status.sshub.dev           | 3001  |
| Glances           | monitor.sshub.dev          | 61208 |
| Nginx Proxy Mgr   | npm.sshub.dev              | 8081  |
| MaplePulse        | maplepulse.sshub.dev       | —     |
| OpenClaw (SAI)    | claw.sshub.dev             | 18789 |

### Common Server Tasks
```bash
# Check running containers
docker ps

# Restart a container
docker restart <container-name>

# View logs
docker logs <container-name> --tail 50

# System status
htop
df -h
free -m
```

---

## Typical AI Agent Workflow

Tell any AI model to do this:
```
1. agent-browser open https://target-site.com
2. agent-browser snapshot
3. [AI reads the accessibility tree, picks element refs]
4. agent-browser fill @e4 "search term"
5. agent-browser press Enter
6. agent-browser snapshot
7. [AI reads results]
8. agent-browser close
```

---

## Quick Reference

| What                  | Command                                      |
|-----------------------|----------------------------------------------|
| Save a note           | `note: [your thought]`                       |
| Summarize something   | `Summarize this text: [text]`                |
| Check inbox           | `Check my inbox` or `Triage my email`        |
| Research a topic      | `Research brief on [topic]`                  |
| Send follow-up        | `Send a follow-up to [email] about [topic]`  |
| Write long-form       | `Ask the writer to draft [topic]`            |
| Browse a site (AI)    | `agent-browser open [url]`                   |
| See page as AI        | `agent-browser snapshot`                     |
| Click element         | `agent-browser click @e2`                    |
| SSH to server         | `ssh -i ~/.ssh/id_hetzner sri@46.62.255.66`  |
| Fresh OpenClaw session| `/new`                                       |
