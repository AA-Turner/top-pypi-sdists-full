from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from ....utils.types.message_types import MessageType, MessageSubtype
from ....utils.types.message_status_types import Status

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
    referral: Optional[Dict] = Field(default=None)
    context: Optional[Dict] = Field(default=None)
    subtype: Optional[str] = Field(default="")