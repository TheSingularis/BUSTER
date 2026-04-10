# 🟢 BUSTER — Bot for Uptime, Status & Troublesome Event Reporting

> A lightweight Discord bot that monitors self-hosted services and keeps your friends in the loop — without exposing what anyone's watching.

Built to run on a separate machine and monitor your homelab from the outside.

> **⚠️ Status: Early development.** The project scaffold is in place and the bot connects to Discord. Service integrations, the status panel, alerts, and slash commands are not yet implemented.

---

## Planned Features

- **Persistent status panel** — a single pinned embed in `#server-status` that edits itself in place on every poll cycle, with interactive buttons for on-demand refresh and issue reporting
- **Plugin-style service registry** — drop a new file into `services/` and add entries to `.env`; zero changes to core bot code
- **Alert DMs** — when a service goes down or recovers, the bot DMs the owner directly (your phone gets the ping via Discord notifications)
- **Cooldown logic** — flapping services don't spam you; alerts fire on state *transitions*, not every poll
- **Friend-facing slash commands** — `/status`, `/ping <service>`, and `/report` let friends self-serve or flag issues
- **Privacy-first** — active session *count* only; no titles, no usernames, nothing identifying
- **No write access** — the bot is read-only; it cannot restart, modify, or control any service

---

## Planned Status Panel

```
🟢 BUSTER — Service Status
Last updated: 2 minutes ago

Jellyfin          ✅  142ms
Audiobookshelf    ✅   89ms

Active streams: 2
All services up for: 4d 12h

[ 🔄 Refresh ]  [ 🚨 Report Issue ]
```

---

## Planned Services

| Service        | What will be checked                                        |
| -------------- | ----------------------------------------------------------- |
| Jellyfin       | Health endpoint, response time, active stream count         |
| Audiobookshelf | Health endpoint, response time                              |
| *(extensible)* | Any HTTP service — add a file in `services/` and an env var |

---

## Current Project Structure

```
buster/
├── bot.py                  # Entry point — connects to Discord, loads cogs (stubs)
├── config.py               # Loads and validates required env vars from .env
├── services/
│   ├── base.py             # (stub) BaseService abstract class + registry
│   ├── jellyfin.py         # (stub) Jellyfin service check
│   └── audiobookshelf.py   # (stub) Audiobookshelf service check
├── cogs/
│   ├── status.py           # (stub) Persistent embed, polling loop, button handlers
│   ├── alerts.py           # (stub) Down/recovery DM logic + cooldown
│   └── commands.py         # (stub) Slash command definitions
├── services.yml            # (empty) Service configuration — not yet loaded
├── compose.yml             # Docker Compose — primary way to run the bot
├── Dockerfile              # Python 3.11-slim image
├── .env.example            # Copy to .env and fill in your values
└── requirements.txt        # Pinned dependencies
```

---

## Setup

### Requirements

- Docker and Docker Compose
- A Discord bot token ([Discord developer portal](https://discord.com/developers/applications))
- Your services reachable from the host running the bot

### Configuration

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

```env
# Discord
DISCORD_TOKEN=your_bot_token_here
DISCORD_GUILD_ID=your_server_id
STATUS_CHANNEL_ID=channel_id_for_the_pinned_embed
ALERT_CHANNEL_ID=channel_id_for_alert_messages
OWNER_DISCORD_ID=your_discord_user_id

# Services
JELLYFIN_URL=http://192.168.1.x:8096
JELLYFIN_API_KEY=your_jellyfin_api_key

AUDIOBOOKSHELF_URL=http://192.168.1.x:13378
AUDIOBOOKSHELF_API_KEY=your_abs_api_key

# Polling
POLL_INTERVAL_SECONDS=60
ALERT_COOLDOWN_SECONDS=300
```

### Running with Docker Compose

```bash
docker compose up --build
```

To run in the background:

```bash
docker compose up --build -d
```

Check logs:

```bash
docker compose logs -f
```

Stop the bot:

```bash
docker compose down
```

---

## Privacy

- No usernames or media titles are ever stored or displayed
- Active session counts are the only usage data shown
- No data is sent anywhere except your own Discord server
- The bot has no write access to any service

---

## License

MIT
