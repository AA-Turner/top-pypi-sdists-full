# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "FlexibleMessageParam",
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


class UserMessageContentUserMessageContentPartTextUserMessageContentParts(TypedDict, total=False):
    text: Required[str]

    type: Literal["text"]


class UserMessageContentUserMessageContentPartImageURLUserMessageContentPartsImageURL(TypedDict, total=False):
    url: Required[str]
    """The URL of the image. Note: only OpenAI supports this."""

    detail: Literal["low", "high", "auto"]
    """Only used for OpenAI. Corresponds to OpenAI's image detail parameter."""


class UserMessageContentUserMessageContentPartImageURLUserMessageContentParts(TypedDict, total=False):
    image_url: Required[UserMessageContentUserMessageContentPartImageURLUserMessageContentPartsImageURL]

    type: Literal["image_url"]


class UserMessageContentUserMessageContentPartImageDataUserMessageContentPartsImageData(TypedDict, total=False):
    data: Required[str]
    """The base64-encoded image data."""

    media_type: Required[str]
    """The media/mime type of the image data.

    For example, 'image/png'. Check providers' documentation for supported media
    types.
    """

    detail: Literal["low", "high", "auto"]
    """Only used for OpenAI. Corresponds to OpenAI's image detail parameter."""

    type: Literal["base64"]
    """The type of the image data. Only base64 is supported."""


class UserMessageContentUserMessageContentPartImageDataUserMessageContentParts(TypedDict, total=False):
    image_data: Required[UserMessageContentUserMessageContentPartImageDataUserMessageContentPartsImageData]

    type: Literal["image_data"]


UserMessageContentUserMessageContentPart: TypeAlias = Union[
    UserMessageContentUserMessageContentPartTextUserMessageContentParts,
    UserMessageContentUserMessageContentPartImageURLUserMessageContentParts,
    UserMessageContentUserMessageContentPartImageDataUserMessageContentParts,
]


class UserMessage(TypedDict, total=False):
    content: Required[Union[str, Iterable[UserMessageContentUserMessageContentPart]]]

    role: Literal["user"]


class AssistantMessage(TypedDict, total=False):
    content: Required[str]

    role: Literal["assistant"]


class SystemMessage(TypedDict, total=False):
    content: Required[str]

    role: Literal["system"]


FlexibleMessageParam: TypeAlias = Union[UserMessage, AssistantMessage, SystemMessage]
