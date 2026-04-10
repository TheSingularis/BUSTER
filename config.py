import os
from dotenv import load_dotenv

load_dotenv()

# Make sure all required values are in the .env of the bot
def require(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value

DISCORD_TOKEN = require("DISCORD_TOKEN")
DISCORD_GUILD_ID = int(require("DISCORD_GUILD_ID"))
STATUS_CHANNEL_ID = int(require("STATUS_CHANNEL_ID"))
ALERT_CHANNEL_ID = int(require("ALERT_CHANNEL_ID"))
OWNER_DISCORD_ID = int(require("OWNER_DISCORD_ID"))
POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", "60"))
ALERT_COOLDOWN_SECONDS = int(os.getenv("ALERT_COOLDOWN_SECONDS", "300"))
