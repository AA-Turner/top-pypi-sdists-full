from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, List, Optional

class ChattyContentContact(BaseModel):
    full_name: str = Field(description="Meta Formatted name")
    # The contact's WhatsApp id. WhatsApp lets a user share a card with no number on
    # WhatsApp (a phone without wa_id, only an email/URL, or no phones at all), so it
    # can be missing: requiring it made Meta's webhook a ValidationError and the
    # customer's message was dropped (CHAT-344). The numbers still travel in `phones`.
    # A missing number is stored as "" (never None, never omitted): letschatty <= 0.6.34
    # requires a string here, and one unreadable message makes its whole bucket unreadable.
    phone_number: str = Field(default="", description="Meta waid; \"\" when the contact has no number on WhatsApp", alias="phone_number")
    name_details: Optional[Dict[str, Any]] = Field(default=None)
    phones: Optional[List[Dict[str, Any]]] = Field(default=None)
    addresses: Optional[List[Dict[str, Any]]] = Field(default=None)
    birthday: Optional[str] = Field(default=None)
    emails: Optional[List[Dict[str, Any]]] = Field(default=None)
    org: Optional[Dict[str, Any]] = Field(default=None)
    urls: Optional[List[Dict[str, Any]]] = Field(default=None)

    @field_validator("phone_number", mode="before")
    @classmethod
    def _missing_number_is_empty(cls, value: Any) -> Any:
        return "" if value is None else value

    def model_dump(self) -> Dict[str, Any]:
        data = super().model_dump(exclude_none=True)
        return data

class ChattyContentContacts(BaseModel):
    contacts: List[ChattyContentContact]

    def get_body_or_caption(self) -> str:
        return f"El usuario envió un contacto"
