from services.base import BaseService, ServiceStatus, register

class AudioBookShelfService(BaseService):
    type = "audiobookshelf"

    async def check(self) -> ServiceStatus:
        status, response_ms, _ = await self.get("/healthcheck")
        return ServiceStatus(
            up=status == 200,
            response_ms=response_ms,
            detail=None if status == 200 else f"Unexpected status code: {status}"
        )

register(AudioBookShelfService)
