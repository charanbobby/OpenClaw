# OpenClaw Mastery — 10-Day Course

**Course:** [OpenClaw Mastery for Everyone](https://github.com/aishwaryanr/awesome-generative-ai-guide/tree/main/free_courses/openclaw_mastery_for_everyone)
**Infrastructure:** Hetzner VPS — `sshub.dev` (46.62.255.66), user: `sri`
**Started:** 2026-03-28

---

## Course Overview

| Day | Focus | Status |
|-----|-------|--------|
| 1 | Installation & Security | ✅ Complete |
| 2 | Personalization (identity, personality, rules, memory) | ✅ Complete |
| 3 | Channel Integration (Telegram) | ✅ Complete |
| 4 | Proactive Automation (scheduled tasks) | ✅ Complete |
| 5 | Skills (ClawHub + custom skills) | ✅ Complete |
| 6 | Email Management (Gmail triage) | ✅ Complete |
| 7 | Research (web search, browser automation) | ✅ Complete |
| 8 | Communication (email sending, approval gates) | ✅ Complete |
| 9 | Multi-Agent Systems (specialist agents) | ✅ Complete (delegation blocked by auth setup, writer works directly) |
| 10 | Verification & Next Steps | ✅ Complete |

Each day has two files in the course repo under `days/day-XX-*/`:
- `learn.md` — theory & concepts
- `build.md` — hands-on implementation

---

## Pre-requisites

- [x] Hetzner VPS with Docker & Nginx already set up
- [ ] **Upgrade server specs** (current tier too low for OpenClaw)
- [ ] LLM API key (OpenAI, Anthropic, or Google)

---

## Day 0: Server Preparation (Pre-Course)

### Step 1: Upgrade Hetzner Server

The current server may not have enough resources for OpenClaw. Recommended minimum:
- **4 vCPUs**
- **8 GB RAM**
- **80 GB SSD**

**How to upgrade on Hetzner Cloud Console:**
1. Log in to [Hetzner Cloud Console](https://console.hetzner.cloud/)
2. Select your server
3. Go to **Rescale** (or Power off → Resize)
4. Choose a plan with adequate specs (e.g., **CX31** or **CX41**)
5. Confirm and power the server back on
6. Verify with: `ssh -i ~/.ssh/id_hetzner sri@46.62.255.66` then `free -h && nproc`

### Step 2: Verify Existing Services Still Work

After upgrade, confirm all services are running:
```bash
docker ps
sudo systemctl status nginx
```

Check:
- https://notes.sshub.dev
- https://status.sshub.dev
- https://monitor.sshub.dev

---

## Day 1: Install & Secure OpenClaw

### Learn (Theory)
Three eras of AI tools:
1. **2023 — Conversational AI:** Context lost between sessions
2. **2024-2025 — Agent Tools:** Multi-step workflows, but session-bound
3. **2025+ — Continuous Assistants:** OpenClaw — background processes + messaging access

Key security principles:
- Start read-only, grant permissions progressively
- Implement approval gates before autonomous actions
- Inspect skills before installation

### Build (Hands-on)
The course uses Hostinger's one-click template. Since we're on Hetzner, we'll install OpenClaw manually via Docker.

**Steps (to be executed on Day 1):**
1. SSH into server
2. Install OpenClaw via Docker
3. Configure API key
4. Run security audit
5. Set system name
6. Verify: chat responsiveness, security audit passing, gateway on localhost

**Completion checklist:**
- [x] Chat responds in web UI (https://claw.sshub.dev)
- [x] Security audit passes (remaining warnings are expected for reverse proxy setup)
- [x] Gateway bound to 127.0.0.1 via Docker port mapping, behind Nginx+SSL
- [x] Auth mode: trusted-proxy (appropriate for Nginx reverse proxy)
- [ ] Credential file permissions (700) — to verify
- [x] Heartbeat disabled (set to 0m)
- [x] No stored channel credentials
- [x] Web search disabled (not enabled in config)
- [ ] System named — **do this now in the chat**

---

## Notes

- Course recommends Hostinger VPS — we adapt all instructions for our Hetzner setup
- Update `d:\Python Applications\Hetzner Cloud Setup\sshub_project_guide.md` as we add OpenClaw
- DNS: will need `claw.sshub.dev` or similar subdomain
