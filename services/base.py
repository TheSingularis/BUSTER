from dataclasses import dataclass
from abc import ABC, abstractmethod

import time
import aiohttp

@dataclass
class ServiceStatus:
    up: bool
    response_ms: int | None = None
    detail: str | None = None

class BaseService(ABC):
    type: str
    name: str
    url: str
    api_key: str | None = None

    def __init__(self):
        self.session: aiohttp.ClientSession | None = None

    @abstractmethod
    async def check(self) -> ServiceStatus:
        ...

    async def get(self, path: str) -> tuple[int, int]:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

        headers = {}
        if self.api_key:
            headers["X-Api-Key"] = self.api_key

        start = time.monotonic()
        async with self.session.get(f"{self.url}/{path}", headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
            elapsed_ms = int((time.monotonic() - start) * 1000)
            return (response.status, elapsed_ms)

REGISTRY: dict[str, type[BaseService]] = {}

def register(cls: type[BaseService]) -> None:
    REGISTRY[cls.type] = cls
