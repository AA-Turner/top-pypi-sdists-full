from __future__ import annotations
from pydantic import BaseModel, Field
from redis.asyncio.client import Redis

class CacheManagers(BaseModel):
    redis:Redis = Field(..., description="Redis client")

    class Config:
        arbitrary_types_allowed=True