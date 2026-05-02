from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class ChattyContentContact(BaseModel):
    full_name: str = Field(description="Meta Formatted name")
    phone_number: str = Field(description="Meta waid", alias="phone_number")
    name_details: Optional[Dict[str, Any]] = Field(default=None)
    phones: Optional[List[Dict[str, Any]]] = Field(default=None)
    addresses: Optional[List[Dict[str, Any]]] = Field(default=None)
    birthday: Optional[str] = Field(default=None)
    emails: Optional[List[Dict[str, Any]]] = Field(default=None)
    org: Optional[Dict[str, Any]] = Field(default=None)
    urls: Optional[List[Dict[str, Any]]] = Field(default=None)

    def model_dump(self) -> Dict[str, Any]:
        data = super().model_dump(exclude_none=True)
        return data

class ChattyContentContacts(BaseModel):
    contacts: List[ChattyContentContact]

    def get_body_or_caption(self) -> str:
        return f"El usuario envió un contacto"
