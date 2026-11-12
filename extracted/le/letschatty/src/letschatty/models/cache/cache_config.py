from pydantic import BaseModel, Field


class CacheConfig(BaseModel):
    cache_ttl: int = Field(default=60 * 60 * 24, description="TTL in seconds for individual items")
    preview_cache_ttl: int = Field(default=60 * 60 * 24, description="TTL in seconds for preview lists")

    @classmethod
    def default(cls) -> 'CacheConfig':
        return cls()
