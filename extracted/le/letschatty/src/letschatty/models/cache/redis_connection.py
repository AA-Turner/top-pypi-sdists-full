"""RedisConnection — singleton wrapper around the async Redis client"""

from ..base_models.singleton import SingletonMeta
from typing import Optional
import os

import redis.asyncio as aioredis

# CHAT-277: a Redis GET/SET with no client-side timeout can block a request
# forever if the server stalls (connection contention, a slow blocking
# command, a network blip). Observed in production: a single GET on
# `GET /company_workspace/{company_id}/messaging-settings` blocked for 12.6s
# (and an outlier for 17.2s) with no socket timeout to bound it. 3 seconds is
# a conservative default for an in-VPC ElastiCache call — comfortably above
# normal latency, but well below what a caller upstream (API Gateway, ALB)
# would tolerate before it gives up anyway.
DEFAULT_REDIS_SOCKET_TIMEOUT = 3.0
DEFAULT_REDIS_SOCKET_CONNECT_TIMEOUT = 3.0


class RedisConnection(metaclass=SingletonMeta):
    def __init__(
        self,
        url: Optional[str] = None,
        password: Optional[str] = None,
        max_connections: Optional[int] = None,
        socket_timeout: Optional[float] = None,
        socket_connect_timeout: Optional[float] = None,
    ):
        self.url = url or os.getenv("REDIS_URL") or "redis://localhost:6379"
        self.password = password or os.getenv("REDIS_PASSWORD")
        self.socket_timeout = (
            socket_timeout
            if socket_timeout is not None
            else _float_env("REDIS_SOCKET_TIMEOUT", DEFAULT_REDIS_SOCKET_TIMEOUT)
        )
        self.socket_connect_timeout = (
            socket_connect_timeout
            if socket_connect_timeout is not None
            else _float_env("REDIS_SOCKET_CONNECT_TIMEOUT", DEFAULT_REDIS_SOCKET_CONNECT_TIMEOUT)
        )

        pool_kwargs: dict = {
            "decode_responses": True,
            "socket_timeout": self.socket_timeout,
            "socket_connect_timeout": self.socket_connect_timeout,
        }
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


def _float_env(name: str, default: float) -> float:
    """Read a float env var, falling back to `default` if unset or unparseable."""
    raw = os.getenv(name)
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        return default
