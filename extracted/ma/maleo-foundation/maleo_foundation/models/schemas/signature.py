from pydantic import BaseModel, Field
from maleo_foundation.types import BaseTypes

class MaleoFoundationSignatureSchemas:
    class Key(BaseModel):
        key: str = Field(..., description="Key")

    class Password(BaseModel):
        password: BaseTypes.OptionalString = Field(None, min_length=32, max_length=1024, description="password")

    class Message(BaseModel):
        message: str = Field(..., description="Message")

    class Signature(BaseModel):
        signature: str = Field(..., description="Signature")

    class IsValid(BaseModel):
        is_valid: bool = Field(..., description="Is valid signature")