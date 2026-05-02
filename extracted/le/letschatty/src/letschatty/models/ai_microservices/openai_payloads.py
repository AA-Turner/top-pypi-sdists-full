from typing import Optional
from pydantic import BaseModel

class OpenaiPayload(BaseModel):
    model: str
    system_message: str
    user_message: str
    schema: dict

class N8nPayload(BaseModel):
    callback_url: str
    event_type: str
    openai_payload: OpenaiPayload
    callback_data: dict
    calendar_data: Optional[dict] = None