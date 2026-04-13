import logging
from services.base import BaseService, ServiceStatus, register

class JellyfinService(BaseService):
    type = "jellyfin"

    async def check(self) -> ServiceStatus:
        status, response_ms, _ = await self.get("/health")
        detail = await self.get_streams()
        return ServiceStatus(
            up=status == 200,
            response_ms=response_ms,
            detail=detail if status == 200 else f"Unexpected status code: {status}"
        )

    async def get_streams(self) -> str | None:
        if not self.api_key:
            logging.getLogger(__name__).warning("No API key configured for Jellyfin service; skipping stream check.")
            return None

        status, _, sessions = await self.get("/Sessions", headers={"X-Emby-Token": self.api_key})
        if status != 200:
            return f"Unexpected status code: {status}"

        stream_count = sum(1 for s in sessions if s.get("NowPlayingItem") and not s.get("PlayState", {}).get("IsPaused", False))
        return f"{stream_count} stream{'s' if stream_count > 1 else ''} active" if stream_count > 0 else None

register(JellyfinService)
