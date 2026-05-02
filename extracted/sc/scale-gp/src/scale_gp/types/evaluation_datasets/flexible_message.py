# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel

__all__ = [
    "FlexibleMessage",
    "UserMessage",
    "UserMessageContentUserMessageContentPart",
    "UserMessageContentUserMessageContentPartTextUserMessageContentParts",
    "UserMessageContentUserMessageContentPartImageURLUserMessageContentParts",
    "UserMessageContentUserMessageContentPartImageURLUserMessageContentPartsImageURL",
    "UserMessageContentUserMessageContentPartImageDataUserMessageContentParts",
    "UserMessageContentUserMessageContentPartImageDataUserMessageContentPartsImageData",
    "AssistantMessage",
    "SystemMessage",
]


class UserMessageContentUserMessageContentPartTextUserMessageContentParts(BaseModel):
    text: str

    type: Optional[Literal["text"]] = None


class UserMessageContentUserMessageContentPartImageURLUserMessageContentPartsImageURL(BaseModel):
    url: str
    """The URL of the image. Note: only OpenAI supports this."""

    detail: Optional[Literal["low", "high", "auto"]] = None
    """Only used for OpenAI. Corresponds to OpenAI's image detail parameter."""


class UserMessageContentUserMessageContentPartImageURLUserMessageContentParts(BaseModel):
    image_url: UserMessageContentUserMessageContentPartImageURLUserMessageContentPartsImageURL

    type: Optional[Literal["image_url"]] = None


class UserMessageContentUserMessageContentPartImageDataUserMessageContentPartsImageData(BaseModel):
    data: str
    """The base64-encoded image data."""

    media_type: str
    """The media/mime type of the image data.

    For example, 'image/png'. Check providers' documentation for supported media
    types.
    """

    detail: Optional[Literal["low", "high", "auto"]] = None
    """Only used for OpenAI. Corresponds to OpenAI's image detail parameter."""

    type: Optional[Literal["base64"]] = None
    """The type of the image data. Only base64 is supported."""


class UserMessageContentUserMessageContentPartImageDataUserMessageContentParts(BaseModel):
    image_data: UserMessageContentUserMessageContentPartImageDataUserMessageContentPartsImageData

    type: Optional[Literal["image_data"]] = None


UserMessageContentUserMessageContentPart: TypeAlias = Annotated[
    Union[
        UserMessageContentUserMessageContentPartTextUserMessageContentParts,
        UserMessageContentUserMessageContentPartImageURLUserMessageContentParts,
        UserMessageContentUserMessageContentPartImageDataUserMessageContentParts,
    ],
    PropertyInfo(discriminator="type"),
]


class UserMessage(BaseModel):
    content: Union[str, List[UserMessageContentUserMessageContentPart]]

    role: Optional[Literal["user"]] = None


class AssistantMessage(BaseModel):
    content: str

    role: Optional[Literal["assistant"]] = None


class SystemMessage(BaseModel):
    content: str

    role: Optional[Literal["system"]] = None


FlexibleMessage: TypeAlias = Annotated[
    Union[UserMessage, AssistantMessage, SystemMessage], PropertyInfo(discriminator="role")
]
