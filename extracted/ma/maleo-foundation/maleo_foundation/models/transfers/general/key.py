from __future__ import annotations
from pydantic import BaseModel, Field
from maleo_foundation.enums import BaseEnums
from maleo_foundation.models.schemas.key import BaseKeySchemas

class MaleoFoundationKeyGeneralTransfers:
    class PrivateKey(BaseKeySchemas.Key):
        type: BaseEnums.KeyType = Field(BaseEnums.KeyType.PRIVATE, description="Private key's type")

    class PublicKey(BaseKeySchemas.Key):
        type: BaseEnums.KeyType = Field(BaseEnums.KeyType.PUBLIC, description="Public key's type")

    class KeyPair(BaseModel):
        private: MaleoFoundationKeyGeneralTransfers.PrivateKey = Field(..., description="Private key's data")
        public: MaleoFoundationKeyGeneralTransfers.PublicKey = Field(..., description="Public key's data")