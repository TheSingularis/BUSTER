import os

import importlib
import pkgutil
import yaml  # type: ignore

from dotenv import load_dotenv
import services

from services.base import REGISTRY, BaseService

# Load environment variables from .env file
load_dotenv()

# Raises an error if a required environment variable is missing


def require(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value


# Bot configuration constants loaded from environment variables
DISCORD_TOKEN = require("DISCORD_TOKEN")
DISCORD_GUILD_ID = int(require("DISCORD_GUILD_ID"))
STATUS_CHANNEL_ID = int(require("STATUS_CHANNEL_ID"))
ALERT_CHANNEL_ID = int(require("ALERT_CHANNEL_ID"))
OWNER_DISCORD_ID = int(require("OWNER_DISCORD_ID"))
# How often to poll services (default: 60s)
POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", "60"))
# Min time between repeat alerts (default: 300s)
ALERT_COOLDOWN_SECONDS = int(os.getenv("ALERT_COOLDOWN_SECONDS", "300"))

# Whether or not to show error details in Discord Embed
SHOW_ERROR_DETAIL = bool(int(os.getenv("SHOW_ERROR_DETAIL", "0")))

# Dynamically loads and instantiates all services defined in services.yml


def load_services() -> list[BaseService]:
    service_entries = []

    # Auto-import all modules in the services dir to trigger registration
    for _, name, _ in pkgutil.iter_modules(services.__path__):
        importlib.import_module(f"services.{name}")

    # Read and parse the services configuration file
    with open("services.yml", "r", encoding="utf-8") as f:
        services_config = yaml.safe_load(f)["services"]
        for entry in services_config:
            if entry["type"] not in REGISTRY:
                raise RuntimeError(f"Unknown service type: {entry['type']}")

            # Instantiate the service class and apply config values from the YAML entry
            service_class = REGISTRY[entry["type"]]
            service_instance = service_class()
            service_instance.name = entry.get("name")
            service_instance.url = entry.get("url")
            service_instance.api_key = entry.get("api_key")
            service_entries.append(service_instance)

    return service_entries


# Load all configured services at startup
SERVICES = load_services()
