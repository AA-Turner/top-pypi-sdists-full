from __future__ import annotations
from pydantic import BaseModel, Field
from maleo_foundation.enums import BaseEnums
from maleo_foundation.types import BaseTypes

class BaseKeySchemas:
    class KeySize(BaseModel):
        key_size: int = Field(2048, ge=2048, le=16384, description="Key's size")

    class Password(BaseModel):
        password: BaseTypes.OptionalString = Field(None, min_length=32, max_length=1024, description="password")

    class Key(BaseModel):
        type: BaseEnums.KeyType = Field(..., description="Key's type")
        value: str = Field(..., description="Key's value")