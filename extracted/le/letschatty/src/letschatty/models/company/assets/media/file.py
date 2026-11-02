from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl
from enum import StrEnum
import mimetypes
import urllib.parse

class MediaType(StrEnum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    STICKER = "sticker"
    GIF = "gif"
    ALL = "all"

class MediaFile(BaseModel):
    key: str
    type: MediaType
    name: str = Field(..., description="File name")
    url: HttpUrl
    is_starred: bool = Field(default=False)
    last_modified: datetime
    size: int = Field(ge=0, description="File size in bytes")
    mime_type: str
    thumbnail_url: Optional[HttpUrl] = None

    def model_dump(self, *args, **kwargs) -> Dict[str, Any]:
        data = super().model_dump(*args, **kwargs)
        data["last_modified"] = data["last_modified"].isoformat()
        data["key"] = urllib.parse.quote(data["key"], safe="")
        return data

    @classmethod
    def from_s3_object(cls, s3_object: Dict[str, Any]) -> 'MediaFile':
        key = s3_object['Key']
        name = key.split('/')[-1]
        mime_type = mimetypes.guess_type(name)[0] or 'application/octet-stream'
        if s3_object.get('ContentLength', None) is None:
            size = s3_object.get('Size', 0)
        else:
            size = s3_object['ContentLength']
        return cls(
            key=key,
            type=cls._get_media_type(mime_type),
            name=name,
            url=s3_object['Url'],
            last_modified=s3_object['LastModified'],
            size=size,
            mime_type=mime_type,
            is_starred=s3_object['Tags'].get('starred') == 'true' if s3_object['Tags'] else False
        )

    @staticmethod
    def _get_media_type(mime_type: str) -> MediaType:
        # WhatsApp only ever uses image/webp for the sticker message type — a
        # regular "image" message can't be webp — so classify it as STICKER
        # before the generic image bucket. Getting this wrong silently applies
        # the wrong size cap (5MB image limit instead of the sticker one) and
        # miscatalogs it in the media library.
        if mime_type == "image/webp":
            return MediaType.STICKER
        # Only image/video/audio are true media types. Everything else
        # (application/*, message/rfc822 .eml, text/*, multipart/*, and any
        # unknown base type) is treated as a DOCUMENT so we never raise on
        # unexpected mime types from incoming WhatsApp uploads.
        base_type = mime_type.split('/')[0]
        media_base_types = {"image", "video", "audio"}
        return MediaType(base_type) if base_type in media_base_types else MediaType.DOCUMENT