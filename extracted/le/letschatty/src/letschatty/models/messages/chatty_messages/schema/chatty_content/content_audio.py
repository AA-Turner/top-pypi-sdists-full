from .content_media import ChattyContentMedia
from pydantic import Field
from typing import Optional

class ChattyContentAudio(ChattyContentMedia):
    transcription: Optional[str] = Field(default=None, description="The transcript of the audio")