# TODO

Roughly ordered — core first, polish later.

---

## Name

**BUSTER** — Bot for Uptime, Status & Troublesome Event Reporting



---

## Phase 1 — Core bot (get it running)

- [ ] Scaffold project structure (`bot.py`, `config.py`, `cogs/`, `services/`)
- [ ] Create Discord application and bot user, note token
- [ ] Load config from `.env` with validation (fail loudly on missing required keys)
- [ ] Connect to Discord, verify bot comes online in guild
- [ ] Register slash commands globally (or guild-scoped for faster iteration during dev)

---

## Phase 2 — Service health checking

- [ ] Write `BaseService` abstract class with `name`, `check()`, and `ServiceStatus` return type
- [ ] `ServiceStatus` dataclass: `{ up: bool, response_ms: int | None, detail: str | None }`
- [ ] Implement `JellyfinService`
  - [ ] Hit `/System/Info` for liveness
  - [ ] Hit `/Sessions` for active stream count (no user/title data)
  - [ ] Handle auth via API key header
- [ ] Implement `AudiobookshelfService`
  - [ ] Hit `/api/ping` or equivalent for liveness
  - [ ] Handle auth via API key header
- [ ] Test both checkers independently (simple script, not the full bot)
- [ ] Graceful timeout handling — treat no response within N seconds as down

---

## Phase 3 — Status embed

- [ ] Find or create a pinned message in `#server-status` on startup (store message ID in state)
- [ ] Build embed: one field per service, green/yellow/red indicator, response time, last-updated timestamp
- [ ] Show total active stream count across all services (no per-user breakdown)
- [ ] Polling loop using `discord.ext.tasks` — runs every `POLL_INTERVAL_SECONDS`
- [ ] Edit the pinned message in place on each poll (never delete + repost)
- [ ] Handle embed rate limits gracefully (don't crash if an edit is rejected)

---

## Phase 4 — Alerts

- [ ] Track previous service state in memory (simple dict is fine for v1)
- [ ] Alert fires only on state *transition*: up→down or down→up
- [ ] On down: post in `#alerts` + DM the owner with service name, timestamp, response detail
- [ ] On recovery: follow-up message in `#alerts` + DM the owner with downtime duration
- [ ] Cooldown: suppress repeat alerts for the same service within `ALERT_COOLDOWN_SECONDS`
- [ ] Test cooldown logic manually by toggling a service off and on quickly

---

## Phase 5 — Slash commands

- [ ] `/status` — call all service checkers, return ephemeral embed with current state
- [ ] `/ping <service>` — check one named service on demand, return result
- [ ] `/report` — accepts optional free-text from the user; DMs owner with:
  - Who reported (username, not user ID)
  - Their message
  - Current service states at time of report
  - Active stream count
- [ ] Autocomplete on `<service>` parameter for `/ping`
- [ ] Handle unknown service name gracefully in `/ping`

---

## Phase 6 — Deployment

- [ ] Write `.env.example` with all keys documented and placeholder values
- [ ] Write `requirements.txt` (pin major versions)
- [ ] Write `homelab-buster.service` systemd unit
  - [ ] `Restart=always`, `RestartSec=10`
  - [ ] `User=` set to a non-root user
  - [ ] `WorkingDirectory=` and `ExecStart=` point to venv Python
- [ ] Test clean install on the Pi from scratch (follow your own README)
- [ ] Verify the bot survives a Pi reboot and reconnects cleanly
- [ ] Verify alerts fire when Unraid is unreachable from the Pi

---

## Phase 7 — Polish (before going public)

- [ ] Add logging to file with rotation (`logging.handlers.RotatingFileHandler`)
- [ ] `config.py` validation errors give clear human-readable messages
- [ ] `BaseService` makes adding a new service a one-file job — document it in README
- [ ] Confirm no secrets in git history (check with `git log --all --full-diff -p`)
- [ ] Add `.gitignore` (`.env`, `__pycache__`, `*.pyc`, `state.json` if used)
- [ ] Add GitHub Actions CI: lint with `ruff`, type check with `mypy` (optional but nice for a public repo)
- [ ] Write a brief CONTRIBUTING.md if you want PRs

---

## Backlog / future ideas

- [ ] Persistent state (SQLite) so downtime history survives bot restarts
- [ ] `/history` command — show last N up/down events per service
- [ ] Configurable per-service poll intervals (some services warrant more frequent checks)
- [ ] Support for generic HTTP health checks (any URL + expected status code) so adding services requires no code
- [ ] Uptime percentage display in the embed (7-day rolling)
- [ ] Optional webhook support as an alternative alert channel (Ntfy, Pushover, etc.)
- [ ] Docker image + `compose.yml` for users who prefer that over systemd
- [ ] Sonarr / Radarr / Prowlarr health checks
- [ ] Unraid-specific: disk usage, array status (requires Unraid API or Community Apps plugin)
