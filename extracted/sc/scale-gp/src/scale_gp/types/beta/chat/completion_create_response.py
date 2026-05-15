# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import TYPE_CHECKING, Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from ...._models import BaseModel
from .chat_completion_chunk_v5 import ChatCompletionChunkV5

__all__ = [
    "CompletionCreateResponse",
    "EgpAPIBackendServerAPIModelsInferenceModelsChatCompletion",
    "EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoice",
    "EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessage",
    "EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageAnnotation",
    "EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageAnnotationURLCitation",
    "EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageAudio",
    "EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageFunctionCall",
    "EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageToolCall",
    "EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageToolCallChatCompletionMessageFunctionToolCall",
    "EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageToolCallChatCompletionMessageFunctionToolCallFunction",
    "EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageToolCallChatCompletionMessageCustomToolCall",
    "EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageToolCallChatCompletionMessageCustomToolCallCustom",
    "EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceLogprobs",
    "EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceLogprobsContent",
    "EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceLogprobsContentTopLogprob",
    "EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceLogprobsRefusal",
    "EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceLogprobsRefusalTopLogprob",
    "EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionUsage",
    "EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionUsageCompletionTokensDetails",
    "EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionUsagePromptTokensDetails",
]


class EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageAnnotationURLCitation(BaseModel):
    """A URL citation when using web search."""

    end_index: int

    start_index: int

    title: str

    url: str

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageAnnotation(BaseModel):
    """A URL citation when using web search."""

    type: Literal["url_citation"]

    url_citation: EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageAnnotationURLCitation
    """A URL citation when using web search."""

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageAudio(BaseModel):
    """
    If the audio output modality is requested, this object contains data
    about the audio response from the model. [Learn more](https://platform.openai.com/docs/guides/audio).
    """

    id: str

    data: str

    expires_at: int

    transcript: str

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageFunctionCall(BaseModel):
    """Deprecated and replaced by `tool_calls`.

    The name and arguments of a function that should be called, as generated by the model.
    """

    arguments: str

    name: str

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageToolCallChatCompletionMessageFunctionToolCallFunction(
    BaseModel
):
    """The function that the model called."""

    arguments: str

    name: str

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageToolCallChatCompletionMessageFunctionToolCall(
    BaseModel
):
    """A call to a function tool created by the model."""

    id: str

    function: EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageToolCallChatCompletionMessageFunctionToolCallFunction
    """The function that the model called."""

    type: Literal["function"]

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageToolCallChatCompletionMessageCustomToolCallCustom(
    BaseModel
):
    """The custom tool that the model called."""

    input: str

    name: str

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageToolCallChatCompletionMessageCustomToolCall(
    BaseModel
):
    """A call to a custom tool created by the model."""

    id: str

    custom: EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageToolCallChatCompletionMessageCustomToolCallCustom
    """The custom tool that the model called."""

    type: Literal["custom"]

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageToolCall: TypeAlias = Union[
    EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageToolCallChatCompletionMessageFunctionToolCall,
    EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageToolCallChatCompletionMessageCustomToolCall,
]


class EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessage(BaseModel):
    """A chat completion message generated by the model."""

    role: Literal["assistant"]

    annotations: Optional[List[EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageAnnotation]] = None

    audio: Optional[EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageAudio] = None
    """
    If the audio output modality is requested, this object contains data about the
    audio response from the model.
    [Learn more](https://platform.openai.com/docs/guides/audio).
    """

    content: Optional[str] = None

    function_call: Optional[EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageFunctionCall] = None
    """Deprecated and replaced by `tool_calls`.

    The name and arguments of a function that should be called, as generated by the
    model.
    """

    refusal: Optional[str] = None

    tool_calls: Optional[List[EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageToolCall]] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceLogprobsContentTopLogprob(BaseModel):
    token: str

    logprob: float

    bytes: Optional[List[int]] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceLogprobsContent(BaseModel):
    token: str

    logprob: float

    top_logprobs: List[EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceLogprobsContentTopLogprob]

    bytes: Optional[List[int]] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceLogprobsRefusalTopLogprob(BaseModel):
    token: str

    logprob: float

    bytes: Optional[List[int]] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceLogprobsRefusal(BaseModel):
    token: str

    logprob: float

    top_logprobs: List[EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceLogprobsRefusalTopLogprob]

    bytes: Optional[List[int]] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceLogprobs(BaseModel):
    """Log probability information for the choice."""

    content: Optional[List[EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceLogprobsContent]] = None

    refusal: Optional[List[EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceLogprobsRefusal]] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoice(BaseModel):
    finish_reason: Literal["stop", "length", "tool_calls", "content_filter", "function_call"]

    index: int

    message: EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessage
    """A chat completion message generated by the model."""

    logprobs: Optional[EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceLogprobs] = None
    """Log probability information for the choice."""

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionUsageCompletionTokensDetails(BaseModel):
    """Breakdown of tokens used in a completion."""

    accepted_prediction_tokens: Optional[int] = None

    audio_tokens: Optional[int] = None

    reasoning_tokens: Optional[int] = None

    rejected_prediction_tokens: Optional[int] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionUsagePromptTokensDetails(BaseModel):
    """Breakdown of tokens used in the prompt."""

    audio_tokens: Optional[int] = None

    cached_tokens: Optional[int] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionUsage(BaseModel):
    """Usage statistics for the completion request."""

    completion_tokens: int

    prompt_tokens: int

    total_tokens: int

    completion_tokens_details: Optional[
        EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionUsageCompletionTokensDetails
    ] = None
    """Breakdown of tokens used in a completion."""

    prompt_tokens_details: Optional[
        EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionUsagePromptTokensDetails
    ] = None
    """Breakdown of tokens used in the prompt."""

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class EgpAPIBackendServerAPIModelsInferenceModelsChatCompletion(BaseModel):
    id: str

    choices: List[EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoice]

    created: int

    model: str

    object: Optional[Literal["chat.completion"]] = None

    service_tier: Optional[Literal["auto", "default", "flex", "scale", "priority"]] = None

    system_fingerprint: Optional[str] = None

    usage: Optional[EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionUsage] = None
    """Usage statistics for the completion request."""

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, builtins.object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> builtins.object: ...
    else:
        __pydantic_extra__: Dict[str, builtins.object]


CompletionCreateResponse: TypeAlias = Union[
    EgpAPIBackendServerAPIModelsInferenceModelsChatCompletion, ChatCompletionChunkV5
]
