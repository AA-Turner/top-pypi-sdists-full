# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "FlexibleMessageParam",
    "UserMessage",
    "UserMessageContentUnionMember1",
    "UserMessageContentUnionMember1TextUserMessageContentParts",
    "UserMessageContentUnionMember1ImageURLUserMessageContentParts",
    "UserMessageContentUnionMember1ImageURLUserMessageContentPartsImageURL",
    "UserMessageContentUnionMember1ImageDataUserMessageContentParts",
    "UserMessageContentUnionMember1ImageDataUserMessageContentPartsImageData",
    "AssistantMessage",
    "SystemMessage",
]


class UserMessageContentUnionMember1TextUserMessageContentParts(TypedDict, total=False):
    text: Required[str]

    type: Literal["text"]


class UserMessageContentUnionMember1ImageURLUserMessageContentPartsImageURL(TypedDict, total=False):
    """Specifies the image URL and level of detail. Only supported by OpenAI models"""

    url: Required[str]
    """The URL of the image. Note: only OpenAI supports this."""

    detail: Literal["low", "high", "auto"]
    """Only used for OpenAI. Corresponds to OpenAI's image detail parameter."""


class UserMessageContentUnionMember1ImageURLUserMessageContentParts(TypedDict, total=False):
    image_url: Required[UserMessageContentUnionMember1ImageURLUserMessageContentPartsImageURL]
    """Specifies the image URL and level of detail. Only supported by OpenAI models"""

    type: Literal["image_url"]


class UserMessageContentUnionMember1ImageDataUserMessageContentPartsImageData(TypedDict, total=False):
    """Specifies inline image data"""

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


class UserMessageContentUnionMember1ImageDataUserMessageContentParts(TypedDict, total=False):
    image_data: Required[UserMessageContentUnionMember1ImageDataUserMessageContentPartsImageData]
    """Specifies inline image data"""

    type: Literal["image_data"]


UserMessageContentUnionMember1: TypeAlias = Union[
    UserMessageContentUnionMember1TextUserMessageContentParts,
    UserMessageContentUnionMember1ImageURLUserMessageContentParts,
    UserMessageContentUnionMember1ImageDataUserMessageContentParts,
]


class UserMessage(TypedDict, total=False):
    content: Required[Union[str, Iterable[UserMessageContentUnionMember1]]]
    """Input from the user.

    Can either be text or a list of content parts. Not all models support image
    content parts, or multiple parts.
    """

    role: Literal["user"]
    """The role of the message. Must be set to 'user'.

    A user message is a message from the user to the AI. This should be the message
    used to send end user input to the AI.
    """


class AssistantMessage(TypedDict, total=False):
    content: Required[str]
    """Text response from the assistant"""

    role: Literal["assistant"]
    """The role of the message. Must be set to 'assistant'.

    An assistant message is a message from the AI to the client. It is different
    from an agent message in that it cannot contain a tool request. It is simply a
    direct response from the AI to the client.
    """


class SystemMessage(TypedDict, total=False):
    content: Required[str]
    """Text input from the system."""

    role: Literal["system"]
    """The role of the message. Must be set to 'system'.

    A system message is different from other messages in that it does not originate
    from a party engaged in a user/AI conversation. Instead, it is a message that is
    injected by either the application or system to guide the conversation. For
    example, a system message may be used as initial instructions for an AI entity
    or to tell the AI that it did not do something correctly.
    """


FlexibleMessageParam: TypeAlias = Union[UserMessage, AssistantMessage, SystemMessage]
