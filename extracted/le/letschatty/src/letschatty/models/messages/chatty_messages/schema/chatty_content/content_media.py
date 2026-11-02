from pydantic import BaseModel, Field, field_validator, HttpUrl
from typing import Optional
from urllib.parse import quote

class ChattyContentUploadable(BaseModel):
    """Content backed by a file that gets uploaded to Meta's Cloud API as media.
    The narrow contract WhatsAppPayloadFactory.upload_media_to_whatsapp_api actually
    needs (url + mime_type, plus sha256 for dedup) — split out from ChattyContentMedia
    so a type that doesn't want caption/id/media_asset_id (e.g. ChattyContentSticker)
    can still be genuinely substitutable wherever "uploadable media" is expected,
    instead of being isinstance-invisible to it."""
    url: str = Field(description="URL of the media from S3")
    mime_type: str
    sha256: Optional[str] = Field(default=None, description="SHA256 hash of the media")

    @field_validator("url", mode="before")
    def validate_url(cls, v):
        if not v:
            raise ValueError("URL is required")
        encoded = quote(str(v), safe=":/?&=%#")
        HttpUrl(encoded)
        return encoded

class ChattyContentMedia(ChattyContentUploadable):
    id: Optional[str] = Field(description="Unique identifier for the image. Also known as media_id", default="")
    caption: str = Field(default="", description="Caption of the media that goes as a text below the media")
    media_asset_id: Optional[str] = Field(default=None, description="Library asset this media was composed from. Usage attribution only — never read to render; the url field stays the render source")

    def get_body_or_caption(self) -> str:
        return self.caption
