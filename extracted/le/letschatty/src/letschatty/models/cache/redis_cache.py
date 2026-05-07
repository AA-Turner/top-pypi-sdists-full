"""RedisCache — concrete CacheProtocol implementation backed by Redis"""

from typing import Optional, List
from .redis_connection import RedisConnection


class RedisCache:
    """Implements CacheProtocol using the package-managed RedisConnection singleton."""

    def __init__(self, connection: RedisConnection):
        self._redis = connection.client

    async def get(self, key: str) -> Optional[str]:
        return await self._redis.get(key)

    async def set(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        await self._redis.set(key, value, ex=ttl)

    async def delete(self, key: str) -> None:
        await self._redis.delete(key)

    async def delete_many(self, keys: List[str]) -> None:
        if keys:
            await self._redis.delete(*keys)

    async def get_many(self, keys: List[str]) -> List[Optional[str]]:
        if not keys:
            return []
        return await self._redis.mget(keys)

    async def flush_all(self) -> None:
        await self._redis.flushdb()
