from typing import Optional

from pydantic import BaseModel


class Image(BaseModel):
    url: str
    width: Optional[int] = None
    height: Optional[int] = None
    format: Optional[str] = None


class Text(BaseModel):
    content: str
    metadata: dict


__all__ = ["Image", "Text"]
