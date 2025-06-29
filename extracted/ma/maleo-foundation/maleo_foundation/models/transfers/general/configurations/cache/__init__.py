from __future__ import annotations
from pydantic import BaseModel, Field
from .redis import RedisCacheConfigurations

SKIP_CACHE_FUNC = lambda x: x is None

class CacheConfigurations(BaseModel):
    redis:RedisCacheConfigurations = Field(..., description="Redis cache's configurations")