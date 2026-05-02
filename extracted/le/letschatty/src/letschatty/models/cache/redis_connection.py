"""RedisConnection — singleton wrapper around the async Redis client"""

from ..base_models.singleton import SingletonMeta
from typing import Optional
import os

import redis.asyncio as aioredis


class RedisConnection(metaclass=SingletonMeta):
    def __init__(
        self,
        url: Optional[str] = None,
        password: Optional[str] = None,
        max_connections: Optional[int] = None,
    ):
        self.url = url or os.getenv("REDIS_URL") or "redis://localhost:6379"
        self.password = password or os.getenv("REDIS_PASSWORD")

        pool_kwargs: dict = {"decode_responses": True}
        if self.password:
            pool_kwargs["password"] = self.password
        if max_connections is not None:
            pool_kwargs["max_connections"] = max_connections

        self.client: aioredis.Redis = aioredis.from_url(self.url, **pool_kwargs)

    async def ping(self) -> bool:
        try:
            return await self.client.ping()
        except Exception:
            return False

    async def close(self) -> None:
        await self.client.aclose()
