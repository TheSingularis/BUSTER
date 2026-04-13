from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Any

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

    async def get(self, path: str, headers: dict | None = None) -> tuple[int, int, Any]:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

        headers = headers or {}

        start = time.monotonic()
        async with self.session.get(f"{self.url}{path}", headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
            elapsed_ms = int((time.monotonic() - start) * 1000)
            try:
                data = await response.json(content_type=None)
            except (ValueError, aiohttp.ContentTypeError):
                data = None
            return (response.status, elapsed_ms, data)

REGISTRY: dict[str, type[BaseService]] = {}

def register(cls: type[BaseService]) -> None:
    REGISTRY[cls.type] = cls
