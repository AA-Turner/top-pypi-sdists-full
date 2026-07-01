# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel

__all__ = [
    "FlexibleMessage",
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


class UserMessageContentUnionMember1TextUserMessageContentParts(BaseModel):
    text: str

    type: Optional[Literal["text"]] = None


class UserMessageContentUnionMember1ImageURLUserMessageContentPartsImageURL(BaseModel):
    """Specifies the image URL and level of detail. Only supported by OpenAI models"""

    url: str
    """The URL of the image. Note: only OpenAI supports this."""

    detail: Optional[Literal["low", "high", "auto"]] = None
    """Only used for OpenAI. Corresponds to OpenAI's image detail parameter."""


class UserMessageContentUnionMember1ImageURLUserMessageContentParts(BaseModel):
    image_url: UserMessageContentUnionMember1ImageURLUserMessageContentPartsImageURL
    """Specifies the image URL and level of detail. Only supported by OpenAI models"""

    type: Optional[Literal["image_url"]] = None


class UserMessageContentUnionMember1ImageDataUserMessageContentPartsImageData(BaseModel):
    """Specifies inline image data"""

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


class UserMessageContentUnionMember1ImageDataUserMessageContentParts(BaseModel):
    image_data: UserMessageContentUnionMember1ImageDataUserMessageContentPartsImageData
    """Specifies inline image data"""

    type: Optional[Literal["image_data"]] = None


UserMessageContentUnionMember1: TypeAlias = Annotated[
    Union[
        UserMessageContentUnionMember1TextUserMessageContentParts,
        UserMessageContentUnionMember1ImageURLUserMessageContentParts,
        UserMessageContentUnionMember1ImageDataUserMessageContentParts,
    ],
    PropertyInfo(discriminator="type"),
]


class UserMessage(BaseModel):
    content: Union[str, List[UserMessageContentUnionMember1]]
    """Input from the user.

    Can either be text or a list of content parts. Not all models support image
    content parts, or multiple parts.
    """

    role: Optional[Literal["user"]] = None
    """The role of the message. Must be set to 'user'.

    A user message is a message from the user to the AI. This should be the message
    used to send end user input to the AI.
    """


class AssistantMessage(BaseModel):
    content: str
    """Text response from the assistant"""

    role: Optional[Literal["assistant"]] = None
    """The role of the message. Must be set to 'assistant'.

    An assistant message is a message from the AI to the client. It is different
    from an agent message in that it cannot contain a tool request. It is simply a
    direct response from the AI to the client.
    """


class SystemMessage(BaseModel):
    content: str
    """Text input from the system."""

    role: Optional[Literal["system"]] = None
    """The role of the message. Must be set to 'system'.

    A system message is different from other messages in that it does not originate
    from a party engaged in a user/AI conversation. Instead, it is a message that is
    injected by either the application or system to guide the conversation. For
    example, a system message may be used as initial instructions for an AI entity
    or to tell the AI that it did not do something correctly.
    """


FlexibleMessage: TypeAlias = Annotated[
    Union[UserMessage, AssistantMessage, SystemMessage], PropertyInfo(discriminator="role")
]
