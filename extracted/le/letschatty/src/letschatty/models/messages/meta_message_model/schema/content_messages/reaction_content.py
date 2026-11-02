
from pydantic import BaseModel

class MetaReactionContent(BaseModel):
    # emoji is optional — Meta omits the field entirely when a user REMOVES a
    # reaction (or sends empty string). Default to empty string so existing
    # consumers (chat_getter.py, get_caption_or_body_or_preview.py) that
    # branch on `if emoji:` correctly render "removed reaction" messaging.
    emoji: str = ""
    message_id: str
