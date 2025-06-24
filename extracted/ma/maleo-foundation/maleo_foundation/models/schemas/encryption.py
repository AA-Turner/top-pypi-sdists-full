from pydantic import BaseModel, Field
from maleo_foundation.types import BaseTypes

class MaleoFoundationEncryptionSchemas:
    class Key(BaseModel):
        key: str = Field(..., description="Key")

    class Password(BaseModel):
        password: BaseTypes.OptionalString = Field(None, min_length=32, max_length=1024, description="password")

    class InitializationVector(BaseModel):
        initialization_vector: str = Field(..., description="Initialization vector")

    class Plaintext(BaseModel):
        plaintext: str = Field(..., description="Plaintext")

    class Ciphertext(BaseModel):
        ciphertext: str = Field(..., description="Ciphertext")