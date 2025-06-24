from __future__ import annotations
from pydantic import BaseModel, Field
from maleo_foundation.types import BaseTypes

class MaleoFoundationTokenSchemas:
    class Key(BaseModel):
        key: str = Field(..., description="Key")

    class Password(BaseModel):
        password: BaseTypes.OptionalString = Field(None, min_length=32, max_length=1024, description="password")

    class Token(BaseModel):
        token: str = Field(..., description="Token")

    class ExpIn(BaseModel):
        exp_in: int = Field(15, ge=1, description="Expires in (integer, minutes)")