# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .shared_params.memory_strategy import MemoryStrategy
from .shared_params.model_parameters import ModelParameters

__all__ = [
    "ChatCompletionCreateParamsBase",
    "Message",
    "MessageUserMessage",
    "MessageUserMessageContentUnionMember1",
    "MessageUserMessageContentUnionMember1TextUserMessageContentParts",
    "MessageUserMessageContentUnionMember1ImageURLUserMessageContentParts",
    "MessageUserMessageContentUnionMember1ImageURLUserMessageContentPartsImageURL",
    "MessageUserMessageContentUnionMember1ImageDataUserMessageContentParts",
    "MessageUserMessageContentUnionMember1ImageDataUserMessageContentPartsImageData",
    "MessageAssistantMessage",
    "MessageSystemMessage",
    "ChatCompletionCreateParamsNonStreaming",
    "ChatCompletionCreateParamsStreaming",
]


class ChatCompletionCreateParamsBase(TypedDict, total=False):
    messages: Required[Iterable[Message]]
    """The list of messages in the conversation.

    Expand each message type to see how it works and when to use it. Most
    conversations should begin with a single `user` message.
    """

    model: Required[
        Literal[
            "gpt-oss-120b",
            "gpt-oss-20b",
            "o1",
            "o1-mini",
            "o3-mini",
            "gpt-4",
            "gpt-4-0613",
            "gpt-4-32k",
            "gpt-4-32k-0613",
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4o-2024-08-06",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-16k",
            "gpt-3.5-turbo-16k-0613",
            "gemini-pro",
            "gemini-1.5-pro-001",
            "gemini-1.5-pro-002",
            "gemini-1.5-pro-preview-0409",
            "gemini-1.5-pro-preview-0514",
            "llama-2-7b-chat",
            "llama-2-13b-chat",
            "llama-2-70b-chat",
            "llama-3-8b-instruct",
            "llama-3-70b-instruct",
            "llama-3-1-8b-instruct",
            "llama-3-1-70b-instruct",
            "llama-3-2-1b-instruct",
            "llama-3-2-3b-instruct",
            "llama-3-3-70b-instruct",
            "Meta-Llama-3-8B-Instruct-RMU",
            "Meta-Llama-3-8B-Instruct-RR",
            "Meta-Llama-3-8B-Instruct-DERTA",
            "Meta-Llama-3-8B-Instruct-LAT",
            "mixtral-8x7b-instruct",
            "mixtral-8x22b-instruct",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-3-5-sonnet-20240620",
            "claude-3-5-sonnet-20241022",
            "mistral-large-latest",
            "phi-3-mini-4k-instruct",
            "phi-3-cat-merged",
            "zephyr-cat-merged",
            "dolphin-2.9-llama3-8b",
            "dolphin-2.9-llama3-70b",
            "defense-llama-3-8b-instruct",
            "donovan-combat-llama",
            "llama3-1-405b-instruct-v1",
        ]
    ]
    """The ID of the model to use for chat completions.

    We only support the models listed here so far.
    """

    account_id: str
    """The account ID to use for usage tracking. This will be gradually enforced."""

    chat_template: str
    """Currently only supported for LLM-Engine models.

    A Jinja template string that defines how the chat completion API formats the
    string prompt. For Llama models, the template must take in at most a `messages`
    object, `bos_token` string, and `eos_token` string. The `messages` object is a
    list of dictionaries, each with keys `role` and `content`. For Mixtral models,
    the template must take in at most a `messages` object and `eos_token` string.
    The `messages` object looks identical to the Llama model's `messages` object,
    but the template can assume the `role` key takes on the values `user` or
    `assistant`, or `system` for the first message. The chat template either needs
    to handle this system message (which gets set via the `instructions` field or by
    the messages), or the `instructions` field must be set to `null` and the
    `messages` object must not contain any system messages.See the default chat
    template present in the Llama and Mixtral tokenizers for examples.
    """

    instructions: str
    """The initial instructions to provide to the chat completion model.

    Use this to guide the model to act in more specific ways. For example, if you
    have specific rules you want to restrict the model to follow you can specify
    them here.

    Good prompt engineering is crucial to getting performant results from the model.
    If you are having trouble getting the model to perform well, try writing more
    specific instructions here before trying more expensive techniques such as
    swapping in other models or finetuning the underlying LLM.
    """

    memory_strategy: MemoryStrategy
    """The memory strategy to use for the agent.

    A memory strategy is a way to prevent the underlying LLM's context limit from
    being exceeded. Each memory strategy uses a different technique to condense the
    input message list into a smaller payload for the underlying LLM.

    We only support the Last K memory strategy right now, but will be adding new
    strategies soon.
    """

    model_parameters: ModelParameters
    """
    Configuration parameters for the chat completion model, such as temperature,
    max_tokens, and stop_sequences.

    If not specified, the default value are:

    - temperature: 0.2
    - max_tokens: None (limited by the model's max tokens)
    - stop_sequences: None
    """


class MessageUserMessageContentUnionMember1TextUserMessageContentParts(TypedDict, total=False):
    text: Required[str]

    type: Literal["text"]


class MessageUserMessageContentUnionMember1ImageURLUserMessageContentPartsImageURL(TypedDict, total=False):
    """Specifies the image URL and level of detail. Only supported by OpenAI models"""

    url: Required[str]
    """The URL of the image. Note: only OpenAI supports this."""

    detail: Literal["low", "high", "auto"]
    """Only used for OpenAI. Corresponds to OpenAI's image detail parameter."""


class MessageUserMessageContentUnionMember1ImageURLUserMessageContentParts(TypedDict, total=False):
    image_url: Required[MessageUserMessageContentUnionMember1ImageURLUserMessageContentPartsImageURL]
    """Specifies the image URL and level of detail. Only supported by OpenAI models"""

    type: Literal["image_url"]


class MessageUserMessageContentUnionMember1ImageDataUserMessageContentPartsImageData(TypedDict, total=False):
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


class MessageUserMessageContentUnionMember1ImageDataUserMessageContentParts(TypedDict, total=False):
    image_data: Required[MessageUserMessageContentUnionMember1ImageDataUserMessageContentPartsImageData]
    """Specifies inline image data"""

    type: Literal["image_data"]


MessageUserMessageContentUnionMember1: TypeAlias = Union[
    MessageUserMessageContentUnionMember1TextUserMessageContentParts,
    MessageUserMessageContentUnionMember1ImageURLUserMessageContentParts,
    MessageUserMessageContentUnionMember1ImageDataUserMessageContentParts,
]


class MessageUserMessage(TypedDict, total=False):
    content: Required[Union[str, Iterable[MessageUserMessageContentUnionMember1]]]
    """Input from the user.

    Can either be text or a list of content parts. Not all models support image
    content parts, or multiple parts.
    """

    role: Literal["user"]
    """The role of the message. Must be set to 'user'.

    A user message is a message from the user to the AI. This should be the message
    used to send end user input to the AI.
    """


class MessageAssistantMessage(TypedDict, total=False):
    content: Required[str]
    """Text response from the assistant"""

    role: Literal["assistant"]
    """The role of the message. Must be set to 'assistant'.

    An assistant message is a message from the AI to the client. It is different
    from an agent message in that it cannot contain a tool request. It is simply a
    direct response from the AI to the client.
    """


class MessageSystemMessage(TypedDict, total=False):
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


Message: TypeAlias = Union[MessageUserMessage, MessageAssistantMessage, MessageSystemMessage]


class ChatCompletionCreateParamsNonStreaming(ChatCompletionCreateParamsBase, total=False):
    stream: Literal[False]
    """Whether or not to stream the response.

    Setting this to True will stream the completion in real-time.
    """


class ChatCompletionCreateParamsStreaming(ChatCompletionCreateParamsBase):
    stream: Required[Literal[True]]
    """Whether or not to stream the response.

    Setting this to True will stream the completion in real-time.
    """


ChatCompletionCreateParams = Union[ChatCompletionCreateParamsNonStreaming, ChatCompletionCreateParamsStreaming]
