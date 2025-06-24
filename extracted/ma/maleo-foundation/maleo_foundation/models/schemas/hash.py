from __future__ import annotations
from pydantic import BaseModel, Field

class MaleoFoundationHashSchemas:
    class Key(BaseModel):
        key: str = Field(..., description="Key")

    class Message(BaseModel):
        message: str = Field(..., description="Message")

    class Hash(BaseModel):
        hash: str = Field(..., description="Hash")

    class IsValid(BaseModel):
        is_valid: bool = Field(..., description="Is valid hash")