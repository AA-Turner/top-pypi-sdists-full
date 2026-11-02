from .content_media import ChattyContentMedia
from pydantic import Field
from typing import Optional

class ChattyContentAudio(ChattyContentMedia):
    transcription: Optional[str] = Field(default=None, description="The transcript of the audio")
    transcription_status: Optional[str] = Field(
        default=None,
        description=(
            "Why the audio has no transcription, when it doesn't. Today the only value is "
            "'sin_creditos' (the company had no AI credits left to pay for it). Open string on "
            "purpose: an unknown future value must never break reading an old chat. Cleared "
            "when a transcription arrives."
        ),
    )
