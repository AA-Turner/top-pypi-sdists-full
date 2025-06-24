from pydantic import BaseModel, Field
from typing import Union
from maleo_foundation.types import BaseTypes
from maleo_foundation.enums import BaseEnums

class RedisCacheNamespaces(BaseModel):
    base: str = Field(..., description="Base's redis namespace")

    def create(
        self,
        *ext: str,
        type: BaseEnums.CacheType,
        base_override: BaseTypes.OptionalString = None
    ) -> str:
        return ":".join([self.base if base_override is None else base_override, type, *ext])

class RedisCacheConfigurations(BaseModel):
    ttl: Union[int, float] = Field(BaseEnums.CacheTTL.TTL_5MN, description="Default TTL")
    namespaces: RedisCacheNamespaces = Field(..., description="Redis cache's namepsaces")
    host: str = Field(..., description="Redis instance's host")
    port: int = Field(6379, description="Redis instance's port")
    db: int = Field(0, description="Redis instance's db")
    password: BaseTypes.OptionalString = Field(None, description="AUTH password")
    decode_responses: bool = Field(False, description="Whether to decode responses")
    health_check_interval: int = Field(30, description="Health check interval")