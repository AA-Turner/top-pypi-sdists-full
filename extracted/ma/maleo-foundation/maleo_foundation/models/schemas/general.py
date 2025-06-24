from __future__ import annotations
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from uuid import UUID
from maleo_foundation.enums import BaseEnums
from maleo_foundation.types import BaseTypes

class BaseGeneralSchemas:
    class DateFilter(BaseModel):
        name: str = Field(..., description="Column name.")
        from_date: BaseTypes.OptionalDatetime = Field(None, description="From date.")
        to_date: BaseTypes.OptionalDatetime = Field(None, description="To date.")

    class SortColumn(BaseModel):
        name: str = Field(..., description="Column name.")
        order: BaseEnums.SortOrder = Field(..., description="Sort order.")

    class SimplePagination(BaseModel):
        page: int = Field(1, ge=1, description="Page number, must be >= 1.")
        limit: int = Field(10, ge=1, le=100, description="Page size, must be 1 <= limit <= 100.")

    #* ----- ----- ----- Data ----- ----- ----- *#
    class Identifiers(BaseModel):
        id: int = Field(..., ge=1, description="Data's ID, must be >= 1.")
        uuid: UUID = Field(..., description="Data's UUID.")

    class EssentialTimestamps(BaseModel):
        created_at: datetime = Field(..., description="Data's created_at timestamp")
        updated_at: datetime = Field(..., description="Data's updated_at timestamp")

    class StatusTimestamps(BaseModel):
        deleted_at: BaseTypes.OptionalDatetime = Field(..., description="Data's deleted_at timestamp")
        restored_at: BaseTypes.OptionalDatetime = Field(..., description="Data's restored_at timestamp")
        deactivated_at: BaseTypes.OptionalDatetime = Field(..., description="Data's deactivated_at timestamp")
        activated_at: datetime = Field(..., description="Data's activated_at timestamp")

    class Timestamps(
        StatusTimestamps,
        EssentialTimestamps
    ): pass

    class Status(BaseModel):
        status: BaseEnums.StatusType = Field(..., description="Data's status")

    class IsDefault(BaseModel):
        is_default: BaseTypes.OptionalBoolean = Field(None, description="Whether data is default")

    class IsRoot(BaseModel):
        is_root: BaseTypes.OptionalBoolean = Field(None, description="Whether data is root")

    class IsParent(BaseModel):
        is_parent: BaseTypes.OptionalBoolean = Field(None, description="Whether data is parent")

    class IsChild(BaseModel):
        is_child: BaseTypes.OptionalBoolean = Field(None, description="Whether data is child")

    class IsLeaf(BaseModel):
        is_leaf: BaseTypes.OptionalBoolean = Field(None, description="Whether data is leaf")

    class Order(BaseModel):
        order: BaseTypes.OptionalInteger = Field(..., description="Data's order")

    class Code(BaseModel):
        code: str = Field(..., description="Data's code")

    class Key(BaseModel):
        key: str = Field(..., description="Data's key")

    class Name(BaseModel):
        name: str = Field(..., description="Data's name")

    class Secret(BaseModel):
        secret: UUID = Field(..., description="Data's secret")

    #* ----- ----- ----- RSA Key ----- ----- ----- *#
    class PrivateKey(BaseModel):
        private_key: str = Field(..., description="Private key in str format.")

    class PublicKey(BaseModel):
        public_key: str = Field(..., description="Public key in str format.")

    class KeyPair(PublicKey, PrivateKey): pass

    class RSAKeys(BaseModel):
        password: str = Field(..., description="Key's password")
        private: str = Field(..., description="Private key")
        public: str = Field(..., description="Public key")

    class AccessedAt(BaseModel):
        accessed_at: datetime = Field(datetime.now(tz=timezone.utc), description="Accessed at")

    class AccessedBy(BaseModel):
        accessed_by: int = Field(0, ge=0, description="Accessed by")