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
    type: Literal["url_citation"]

    url_citation: EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageAnnotationURLCitation

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
    id: str

    function: EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageToolCallChatCompletionMessageFunctionToolCallFunction

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
    id: str

    custom: EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageToolCallChatCompletionMessageCustomToolCallCustom

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
    role: Literal["assistant"]

    annotations: Optional[List[EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageAnnotation]] = None

    audio: Optional[EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageAudio] = None

    content: Optional[str] = None

    function_call: Optional[EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceMessageFunctionCall] = None

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

    logprobs: Optional[EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionChoiceLogprobs] = None

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
    completion_tokens: int

    prompt_tokens: int

    total_tokens: int

    completion_tokens_details: Optional[
        EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionUsageCompletionTokensDetails
    ] = None

    prompt_tokens_details: Optional[
        EgpAPIBackendServerAPIModelsInferenceModelsChatCompletionUsagePromptTokensDetails
    ] = None

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
