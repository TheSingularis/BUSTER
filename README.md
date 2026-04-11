# 🟢 BUSTER — Bot for Uptime, Status & Troublesome Event Reporting

> A lightweight Discord bot that monitors self-hosted services and keeps your friends in the loop — without exposing what anyone's watching.

Built to run on a separate machine and monitor your homelab from the outside.

---

## Features

**Implemented**
- Plugin-style service registry — drop a new file into `services/`, add an entry to `services.yml`, zero changes to core bot code
- Jellyfin and Audiobookshelf health checks with response time tracking
- Config validation — bot refuses to start with a clear error if required values are missing

**Planned**
- **Persistent status panel** — a single pinned embed in `#server-status` that edits itself in place on every poll cycle, with interactive buttons for on-demand refresh and issue reporting
- **Alert DMs** — when a service goes down or recovers, the bot DMs the owner directly
- **Cooldown logic** — flapping services don't spam you; alerts fire on state *transitions*, not every poll
- **Friend-facing slash commands** — `/status`, `/ping <service>`, and `/report`
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

## Supported Services

| Service        | What's checked                                                           |
| -------------- | ------------------------------------------------------------------------ |
| Jellyfin       | Health endpoint, response time, active stream count                      |
| Audiobookshelf | Health endpoint, response time                                           |
| *(extensible)* | Any HTTP service — add a file in `services/`, register in `services.yml` |

---

## Project Structure

```
buster/
├── bot.py                      # Entry point
├── config.py                   # Loads .env and services.yml, validates both
├── services/
│   ├── base.py                 # BaseService abstract class + registry
│   ├── jellyfin.py             # Jellyfin health check
│   └── audiobookshelf.py       # Audiobookshelf health check
├── cogs/
│   ├── status.py               # (planned) Persistent embed, polling loop, button handlers
│   ├── alerts.py               # (planned) Down/recovery DM logic + cooldown
│   └── commands.py             # (planned) Slash command definitions
├── services.yml                # Service configuration — edit this to add services
├── .env.example
├── requirements.txt
└── homelab-buster.service      # systemd unit file
```

---

## Setup

### Requirements

- A Linux host to run the bot on (separate from your media server)
- Python 3.11+
- A Discord bot token ([Discord developer guide](https://discord.com/developers/docs/getting-started))
- Your services reachable from the host (local network, domain, or VPN)

### Installation

```bash
git clone https://github.com/yourusername/buster
cd buster
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and fill in your Discord credentials:

```bash
cp .env.example .env
```

```env
DISCORD_TOKEN=your_bot_token_here
DISCORD_GUILD_ID=your_server_id
STATUS_CHANNEL_ID=channel_id_for_the_pinned_panel
ALERT_CHANNEL_ID=channel_id_for_alert_messages
OWNER_DISCORD_ID=your_discord_user_id
POLL_INTERVAL_SECONDS=60
ALERT_COOLDOWN_SECONDS=300
```

Then configure your services in `services.yml`:

```yaml
services:
  - name: Jellyfin
    type: jellyfin
    url: http://192.168.1.x:8096
    api_key: your_jellyfin_api_key

  - name: Audiobookshelf
    type: audiobookshelf
    url: http://192.168.1.x:13378
    api_key: your_abs_api_key
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

## Adding a Service

**Step 1** — create `services/myservice.py`:

```python
from services.base import BaseService, ServiceStatus, register

class MyService(BaseService):
    type = "myservice"
    name = "My Service"

    async def check(self) -> ServiceStatus:
        status, response_ms = await self.get("/health")
        return ServiceStatus(
            up=status == 200,
            response_ms=response_ms,
            detail=None if status == 200 else f"Unexpected status code: {status}"
        )

register(MyService)
```

**Step 2** — add an entry to `services.yml`:

```yaml
  - name: My Service
    type: myservice
    url: http://192.168.1.x:1234
    api_key: optional
```

That's it. No changes to the bot core.

---

## Privacy

- No usernames or media titles are ever stored or displayed
- Active session counts are the only usage data shown
- No data is sent anywhere except your own Discord server
- The bot has no write access to any service

---

## License

MIT
