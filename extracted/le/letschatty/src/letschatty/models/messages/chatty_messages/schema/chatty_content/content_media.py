from pydantic import BaseModel, Field, field_validator, HttpUrl
from typing import Optional
class ChattyContentMedia(BaseModel):
    id: Optional[str] = Field(description="Unique identifier for the image. Also known as media_id", default="")
    url: str = Field(description="URL of the media from S3")
    caption: str = Field(default="", description="Caption of the media that goes as a text below the media")
    mime_type: str
    sha256: Optional[str] = Field(default=None, description="SHA256 hash of the media")
    
    @field_validator("url", mode="before")
    def validate_url(cls, v):
        if not v:
            raise ValueError("URL is required")
        HttpUrl(v)
        return v
    
    def get_body_or_caption(self) -> str:
        return self.caption

