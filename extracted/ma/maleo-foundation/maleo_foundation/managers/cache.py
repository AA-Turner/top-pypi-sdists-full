from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field
from redis.asyncio.client import Redis

class CacheManagers(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    redis:Redis = Field(..., description="Redis client")