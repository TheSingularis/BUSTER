# BUSTER — Bot for Uptime, Status & Troublesome Event Reporting

> A lightweight Discord bot that monitors self-hosted services and keeps your friends in the loop — without exposing what anyone's watching.

Built to watch an Unraid server (or any homelab) from the outside.

---

## Features

- **Pinned status embed** — a single message in `#server-status` that auto-refreshes, showing each service as up, degraded, or down with response times
- **Alert DMs** — when a service goes down or recovers, the bot DMs the owner directly (your phone gets the ping via Discord notifications)
- **Cooldown logic** — flapping services don't spam you; alerts fire on state *transitions*, not every poll
- **Friend-facing slash commands** — `/status`, `/ping <service>`, and `/report` let friends self-serve or flag issues
- **Privacy-first** — active session *count* only; no titles, no usernames, nothing identifying
- **No write access** — the bot is read-only; it cannot restart, modify, or control any service

---

## Supported Services

| Service        | What's checked                                      |
| -------------- | --------------------------------------------------- |
| Jellyfin       | Health endpoint, response time, active stream count |
| Audiobookshelf | Health endpoint, response time                      |
| *(extensible)* | Any HTTP service with a health endpoint             |

---

## How It Works

```
sentinel (systemd service)
├── polls each service every 60s
├── edits a pinned embed in #server-status
├── DMs the owner on state transitions
└── responds to slash commands
```

The bot runs outside your Unraid server so it can report on your server even if the server itself is the thing that went down.

---

## Slash Commands

| Command           | Who    | What it does                                             |
| ----------------- | ------ | -------------------------------------------------------- |
| `/status`         | Anyone | On-demand summary of all services                        |
| `/ping <service>` | Anyone | Check one service right now                              |
| `/report`         | Anyone | Flag something feels broken — DMs the owner with context |

---

## Setup

### Requirements

- Python 3.11+
- A Discord bot token ([guide](https://discord.com/developers/docs/getting-started))
- Your services reachable from your host machine (local network or via domain/VPN)

### Installation

```bash
git clone https://github.com/yourusername/sentinel
cd sentinel
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

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

### Running as a systemd service

Copy the included unit file and enable it:

```bash
sudo cp homelab-buster.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now homelab-buster
```

Check status:

```bash
sudo systemctl status homelab-buster
journalctl -u homelab-buster -f
```

---

## Project Structure

```
buster/
├── bot.py                      # Entry point
├── config.py                   # Loads and validates .env
├── services/
│   ├── base.py                 # Abstract service checker
│   ├── jellyfin.py             # Jellyfin health + session count
│   └── audiobookshelf.py       # Audiobookshelf health
├── cogs/
│   ├── status.py               # Pinned embed + polling loop
│   ├── alerts.py               # Down/recovery DM logic
│   └── commands.py             # Slash command definitions
├── .env.example
├── requirements.txt
└── homelab-buster.service      # systemd unit file
```

---

## Adding a Service

Create a new file in `services/` that extends `BaseService`:

```python
from services.base import BaseService, ServiceStatus

class MyService(BaseService):
    name = "My Service"

    async def check(self) -> ServiceStatus:
        # hit your health endpoint here
        ...
```

Then register it in `config.py`. That's it.

---

## Privacy

- No usernames or media titles are ever stored or displayed
- Active session counts are the only usage data shown
- No data is sent anywhere except your own Discord server
- The bot has no write access to any service

---

## License

MIT
