"""Public content blocks retained in Session history."""

from typing import Annotated, Literal

from pydantic import Field, model_validator

from .base import SessionModel
from .common import Uri


class TextContentBlock(SessionModel):
    type: Literal["text"] = "text"
    text: str = ""


class ImageContentBlock(SessionModel):
    type: Literal["image"] = "image"
    uri: Uri
    media_type: str | None = None
    alt_text: str | None = None


class ResourceLinkContentBlock(SessionModel):
    type: Literal["resource_link"] = "resource_link"
    uri: Uri
    name: str | None = None
    title: str | None = None
    description: str | None = None
    media_type: str | None = None
    size: int | None = Field(default=None, ge=0)


class EmbeddedResourceContentBlock(SessionModel):
    type: Literal["embedded_resource"] = "embedded_resource"
    uri: Uri
    media_type: str | None = None
    text: str | None = None
    blob: str | None = None

    @model_validator(mode="after")
    def validate_content(self) -> "EmbeddedResourceContentBlock":
        if (self.text is None) == (self.blob is None):
            raise ValueError("Embedded resources require exactly one of text or blob")
        return self


type ContentBlock = Annotated[
    TextContentBlock | ImageContentBlock | ResourceLinkContentBlock | EmbeddedResourceContentBlock,
    Field(discriminator="type"),
]
