"""A company's WhatsApp account: one phone number with a stable Chatty id.

The account is what a chat belongs to. Its Meta ids (`phone_number_id`, `waba_id`,
`portfolio_id`) are mutable attributes: reconnecting the account with a new number or moving
the number to another WABA updates the account and never touches its chats.
"""
from datetime import datetime
from enum import StrEnum
from typing import Any, Dict, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, SecretStr

from ..utils.types.identifier import StrObjectId
from .time import utc_now


class WhatsAppAccountStatus(StrEnum):
    #: Created by the connect flow before Meta registration finished. Never sends.
    PENDING = "pending"
    CONNECTED = "connected"
    #: Kept for reading its chats. Never sends.
    DISCONNECTED = "disconnected"


class WhatsAppAccount(BaseModel):
    id: StrObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    company_id: StrObjectId
    name: str = Field(description="Shown to agents (e.g. «Ventas»). Set by the user when connecting.")
    is_default: bool = Field(default=False, description="Picked when a request does not say which account to use")
    status: WhatsAppAccountStatus = WhatsAppAccountStatus.PENDING
    phone_number_id: str = Field(description="Meta id of the CURRENT number")
    display_phone_number: str
    waba_id: str = Field(description="Meta id of the current WABA")
    portfolio_id: Optional[str] = Field(default=None, description="Meta id of the current business portfolio")
    token: SecretStr = Field(description="Business token granted for this account's connection")
    is_coexistence: bool = False
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    connected_at: Optional[datetime] = None
    disconnected_at: Optional[datetime] = None

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    @property
    def can_send(self) -> bool:
        return self.status == WhatsAppAccountStatus.CONNECTED

    def to_document(self) -> Dict[str, Any]:
        document = self.model_dump(by_alias=True, exclude={"token"})
        document["token"] = self.token.get_secret_value()
        return document

    @classmethod
    def from_document(cls, document: Dict[str, Any]) -> "WhatsAppAccount":
        return cls(**{**document, "_id": str(document["_id"])})
