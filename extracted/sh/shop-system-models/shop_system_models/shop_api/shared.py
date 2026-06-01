from typing import Optional

from pydantic import BaseModel


class Thumbnail(BaseModel):
    signedUrl: Optional[str] = None
    path: Optional[str] = None


class Thumbnails(BaseModel):
    tiny: Optional[Thumbnail]
    small: Optional[Thumbnail]
    card_cover: Optional[Thumbnail]


class ImageMetadata(BaseModel):
    id: Optional[str] = None
    url: Optional[str] = None
    title: Optional[str] = None
    mimetype: Optional[str] = None
    thumbnails: Optional[Thumbnails]
    path: Optional[str] = None
    signedUrl: Optional[str] = None
