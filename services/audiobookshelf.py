import time
import logging
from services.base import BaseService, ServiceStatus, register

class AudioBookShelfService(BaseService):
    type = "audiobookshelf"

    async def check(self) -> ServiceStatus:
        status, response_ms, _ = await self.get("/healthcheck")
        detail = await self.get_streams()
        return ServiceStatus(
            up=status == 200,
            response_ms=response_ms,
            detail=detail if status == 200 else f"Unexpected status code: {status}"
        )

    async def get_streams(self) -> str | None:
        if not self.api_key:
            logging.getLogger(__name__).warning("No API key configured for AudioBookShelf service; skipping stream check.")
            return None

        status, _, sessions = await self.get("/api/users/online", headers={"Authorization": f"Bearer {self.api_key}"})
        if status != 200:
            return f"Unexpected status code: {status}"

        STALE_SESSION_SECONDS = 300 # "Active" sessions that havent updated in 5 minutes are filtered out of "Active" stream count

        now_ms = time.time() * 1000
        stream_count = sum(1 for s in sessions.get("openSessions", []) if now_ms - s.get("updatedAt", 0) < STALE_SESSION_SECONDS * 1000)
        return f"{stream_count} stream{'s' if stream_count > 1 else ''} active" if stream_count > 0 else None

register(AudioBookShelfService)
