from services.base import BaseService, ServiceStatus, register

class JellyfinService(BaseService):
    type = "jellyfin"

    async def check(self) -> ServiceStatus:
        status, response_ms = await self.get("/health")
        return ServiceStatus(
            up=status == 200,
            response_ms=response_ms,
            detail=None if status == 200 else f"Unexpected status code: {status}"
        )

register(JellyfinService)
