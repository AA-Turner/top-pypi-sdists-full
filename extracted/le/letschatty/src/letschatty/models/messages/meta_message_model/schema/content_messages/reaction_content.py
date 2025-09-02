
from pydantic import BaseModel

class MetaReactionContent(BaseModel):
    emoji: str
    message_id: str
