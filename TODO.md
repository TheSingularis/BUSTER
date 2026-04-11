# TODO

Core first, polish later.

---

## Name

**BUSTER** - Bot for Uptime, Status & Troublesome Event Reporting

---

## Phase 1 - Core bot (get it running)

- [x] Scaffold project structure (`bot.py`, `config.py`, `cogs/`, `services/`)
- [x] Create Discord application and bot user, note token
- [x] Load Discord config from `.env` with validation (fail loudly on missing required keys)
- [x] Connect to Discord, verify bot comes online in server
- [ ] Register slash commands globally (or server-scoped for faster dev iteration)

### Bot configured

---

## Phase 2 - Service plugin system

- [x] Write `BaseService` abstract class in `services/base.py`
  - [x] Fields: `type`, `name`, `url`, `api_key`
  - [x] Abstract method: `async def check() -> ServiceStatus`
  - [x] Helper: `async def get(path)` - wraps aiohttp, measures response time, handles timeouts
- [x] Write `ServiceStatus` dataclass: `{ up: bool, response_ms: int | None, detail: str | None }`
- [x] Write service registry in `base.py`: `register(cls)` + `REGISTRY: dict[str, type[BaseService]]`
- [x] Auto-import all `services/*.py` files at startup so each file self-registers
- [x] Write `services.yml` schema and loader in `config.py`
  - [x] Validate each entry has a `type` that exists in the registry
  - [x] Fail loudly with a clear message if a type is unknown
- [x] Implement `JellyfinService`
  - [x] Hit `/health` for liveness
  - [ ] Hit `/Sessions` for active stream count (no user/title data)
  - [x] Self-register: `register(JellyfinService)` at bottom of file
- [x] Implement `AudiobookshelfService`
  - [x] Hit `/healthcheck` for liveness
  - [x] Self-register at bottom of file
- [x] Test both checkers with a standalone script before wiring into the bot
- [x] Graceful timeout handling - treat no response within N seconds as down

### Service Structure Built

---

## Phase 3 - Persistent status panel

- [x] On startup: search `#server-status` for an existing BUSTER pinned message (match by post ID)
- [x] If not found: post a new embed and pin it; save message ID to `state.json`
- [x] If found: load message ID from `state.json` and resume editing it
- [x] Build embed renderer - given a list of `ServiceStatus` results, produce a `discord.Embed`:
  - [x] Title: `🟢 BUSTER - Service Status` (color reflects worst state across all services)
  - [x] One line per service: name, status indicator (✅ / ⚠️ / ❌), response time
  - [ ] Footer: active stream count, overall uptime string, last-updated timestamp
- [ ] Attach a persistent `discord.ui.View` with two buttons:
  - [ ] `🔄 Refresh` - triggers immediate out-of-cycle poll, updates embed
  - [ ] `🚨 Report Issue` - opens a modal for the user to type a message; DMs owner with context
- [x] Polling loop using `discord.ext.tasks` - runs every `POLL_INTERVAL_SECONDS`
- [x] Edit the pinned message in place on each poll (never delete + repost)
- [ ] Handle embed edit rate limits gracefully (skip cycle if rejected, log it)

---

## Phase 4 - Alerts

- [ ] Track previous service state in memory (dict keyed by service name)
- [ ] Alert fires only on state transition: up→down or down→up
- [ ] On down: post in `#alerts` + DM owner with service name, timestamp, response detail
- [ ] On recovery: follow-up in `#alerts` + DM owner with downtime duration
- [ ] Cooldown: suppress repeat alerts for same service within `ALERT_COOLDOWN_SECONDS`
- [ ] Test cooldown logic manually by toggling a service off/on quickly

---

## Phase 5 - Slash commands

- [ ] `/status` - poll all services on demand, return ephemeral embed with current state
- [ ] `/ping <service>` - check one named service right now, return result
  - [ ] Autocomplete on `<service>` parameter from loaded service names
  - [ ] Handle unknown service name gracefully
- [ ] `/report` - accepts optional free-text; DMs owner with:
  - [ ] Who reported (display name, not user ID)
  - [ ] Their message
  - [ ] Current service states at time of report
  - [ ] Active stream count

---

## Phase 6 - Deployment

- [ ] Write `.env.example` with all keys documented and placeholder values
- [ ] Write `services.yml.example` with Jellyfin + Audiobookshelf as templates
- [ ] Write `requirements.txt` (pin major versions)
- [ ] Write `homelab-buster.service` systemd unit
  - [ ] `Restart=always`, `RestartSec=10`
  - [ ] `User=` set to a non-root user
  - [ ] `WorkingDirectory=` and `ExecStart=` point to venv Python
- [ ] Test clean install on a fresh host from scratch (follow your own README)
- [ ] Verify the bot survives a host reboot and reconnects cleanly
- [ ] Verify the pinned panel is restored correctly after a restart (state.json roundtrip)
- [ ] Verify alerts fire when the media server is unreachable from the bot host

---

## Phase 7 - Polish (before going public)

- [ ] Add logging to file with rotation (`logging.handlers.RotatingFileHandler`)
- [ ] `config.py` validation errors give clear human-readable messages
- [ ] Confirm adding a new service is genuinely a one-file + one-yml-entry job - test it
- [ ] Confirm no secrets in git history (`git log --all --full-diff -p`)
- [ ] Add `.gitignore` (`.env`, `__pycache__`, `*.pyc`, `state.json`)
- [ ] Add GitHub Actions CI: lint with `ruff`, type check with `mypy`
- [ ] Write a brief `CONTRIBUTING.md` if you want PRs

---

## Backlog / future ideas

**Web UI (config + status)**
- [ ] Add FastAPI running in the same async process as the bot
- [ ] `/` - read-only status page (same data as the Discord panel, no auth needed)
- [ ] `/admin` - edit `services.yml` in the browser; LAN-only, no public exposure
- [ ] `/reload` endpoint - hot-reload `services.yml` without restarting the bot
- [ ] Keep web UI LAN-only; do not expose to the internet without auth

**Monitoring improvements**
- [ ] Persistent state (SQLite) so downtime history survives bot restarts
- [ ] `/history` command - last N up/down events per service
- [ ] Configurable per-service poll intervals in `services.yml`
- [ ] Generic HTTP check type (`type: http`, any URL + expected status code) - no code needed for simple services
- [ ] Uptime percentage in the embed (7-day rolling)

**Integrations**
- [ ] Sonarr / Radarr / Prowlarr health checks
- [ ] Unraid-specific: array status, disk usage (via Unraid API or community plugin)
- [ ] Optional Ntfy / Pushover webhook as a secondary alert channel alongside Discord DMs

**Distribution**
- [ ] Docker image + `compose.yml` for users who prefer containers over systemd
