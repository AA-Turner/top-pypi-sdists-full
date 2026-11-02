from pydantic import Field
from typing import Optional
from .content_media import ChattyContentUploadable

class ChattyContentSticker(ChattyContentUploadable):
    # sha256 stays Optional (inherited): Meta supplies it on incoming stickers, but an
    # outbound sticker picked from the media library has no reliable hash to send —
    # promoted (received→library) assets store None and list previews omit the field.
    # Nothing on the send path ever reads it, so requiring it here only produced 422s.
    animated: Optional[bool] = Field(default=None, description="Whether the sticker is animated — known for incoming Meta stickers, unset otherwise")

    def get_body_or_caption(self) -> str:
        return f"Sticker: {self.url}"
