from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from ....utils.types.message_types import MessageType, MessageSubtype
from ....utils.types.message_status_types import Status
from ...meta_message_model.schema.values.value_statuses import ErrorDetail
from ...meta_message_model.schema.values.motivos_de_no_entrega import NoEntrega

class Content(BaseModel):
    pass

class ChattyMessageJson(BaseModel):
    """This is the database message model"""
    id: str
    created_at: datetime
    updated_at: datetime
    type: MessageType
    status: Status
    is_incoming_message: bool
    content: Dict[str, Any] 
    sent_by: Optional[str] = Field(default=None)
    revoked: bool = Field(default=False)
    played_at: Optional[datetime] = Field(default=None)  # voice notes only; see Message.played_at
    error_details: Optional[ErrorDetail] = Field(default=None)  # see Message.error_details
    no_entrega: Optional[NoEntrega] = Field(default=None)  # see Message.no_entrega
    starred: bool = Field(default=False)  # see Message.starred / mark_as_starred
    referral: Optional[Dict] = Field(default=None)
    context: Optional[Dict] = Field(default=None)
    subtype: Optional[str] = Field(default="")