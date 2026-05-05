# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .openai_response import OpenAIResponse
from .part_reasoning_text import PartReasoningText
from .mcp_approval_request import McpApprovalRequest
from .response_compaction_item import ResponseCompactionItem
from .openai_response_output_text import OpenAIResponseOutputText
from .openai_response_output_message import OpenAIResponseOutputMessage
from .openai_response_output_refusal import OpenAIResponseOutputRefusal
from .openai_response_reasoning_item import OpenAIResponseReasoningItem
from .response_apply_patch_tool_call import ResponseApplyPatchToolCall
from .openai_response_custom_tool_call import OpenAIResponseCustomToolCall
from .response_function_shell_tool_call import ResponseFunctionShellToolCall
from .openai_response_computer_tool_call import OpenAIResponseComputerToolCall
from .openai_response_function_tool_call import OpenAIResponseFunctionToolCall
from .openai_response_function_web_search import OpenAIResponseFunctionWebSearch
from .openai_response_file_search_tool_call import OpenAIResponseFileSearchToolCall
from .response_apply_patch_tool_call_output import ResponseApplyPatchToolCallOutput
from .response_function_shell_tool_call_output import ResponseFunctionShellToolCallOutput
from .openai_response_code_interpreter_tool_call import OpenAIResponseCodeInterpreterToolCall
from .openai_types_responses_response_output_item_mcp_call import OpenAITypesResponsesResponseOutputItemMcpCall
from .openai_types_responses_response_output_item_mcp_list_tools import (
    OpenAITypesResponsesResponseOutputItemMcpListTools,
)
from .openai_types_responses_response_output_item_local_shell_call import (
    OpenAITypesResponsesResponseOutputItemLocalShellCall,
)
from .openai_types_responses_response_output_item_image_generation_call import (
    OpenAITypesResponsesResponseOutputItemImageGenerationCall,
)

__all__ = [
    "ResponseCreateResponse",
    "ResponseAudioDeltaEvent",
    "ResponseAudioDoneEvent",
    "ResponseAudioTranscriptDeltaEvent",
    "ResponseAudioTranscriptDoneEvent",
    "ResponseCodeInterpreterCallCodeDeltaEvent",
    "ResponseCodeInterpreterCallCodeDoneEvent",
    "ResponseCodeInterpreterCallCompletedEvent",
    "ResponseCodeInterpreterCallInProgressEvent",
    "ResponseCodeInterpreterCallInterpretingEvent",
    "ResponseCompletedEvent",
    "ResponseContentPartAddedEvent",
    "ResponseContentPartAddedEventPart",
    "ResponseContentPartDoneEvent",
    "ResponseContentPartDoneEventPart",
    "ResponseCreatedEvent",
    "ResponseErrorEvent",
    "ResponseFileSearchCallCompletedEvent",
    "ResponseFileSearchCallInProgressEvent",
    "ResponseFileSearchCallSearchingEvent",
    "ResponseFunctionCallArgumentsDeltaEvent",
    "ResponseFunctionCallArgumentsDoneEvent",
    "ResponseInProgressEvent",
    "ResponseFailedEvent",
    "ResponseIncompleteEvent",
    "ResponseOutputItemAddedEvent",
    "ResponseOutputItemAddedEventItem",
    "ResponseOutputItemDoneEvent",
    "ResponseOutputItemDoneEventItem",
    "ResponseReasoningSummaryPartAddedEvent",
    "ResponseReasoningSummaryPartAddedEventPart",
    "ResponseReasoningSummaryPartDoneEvent",
    "ResponseReasoningSummaryPartDoneEventPart",
    "ResponseReasoningSummaryTextDeltaEvent",
    "ResponseReasoningSummaryTextDoneEvent",
    "ResponseReasoningTextDeltaEvent",
    "ResponseReasoningTextDoneEvent",
    "ResponseRefusalDeltaEvent",
    "ResponseRefusalDoneEvent",
    "ResponseTextDeltaEvent",
    "ResponseTextDeltaEventLogprob",
    "ResponseTextDeltaEventLogprobTopLogprob",
    "ResponseTextDoneEvent",
    "ResponseTextDoneEventLogprob",
    "ResponseTextDoneEventLogprobTopLogprob",
    "ResponseWebSearchCallCompletedEvent",
    "ResponseWebSearchCallInProgressEvent",
    "ResponseWebSearchCallSearchingEvent",
    "ResponseImageGenCallCompletedEvent",
    "ResponseImageGenCallGeneratingEvent",
    "ResponseImageGenCallInProgressEvent",
    "ResponseImageGenCallPartialImageEvent",
    "ResponseMcpCallArgumentsDeltaEvent",
    "ResponseMcpCallArgumentsDoneEvent",
    "ResponseMcpCallCompletedEvent",
    "ResponseMcpCallFailedEvent",
    "ResponseMcpCallInProgressEvent",
    "ResponseMcpListToolsCompletedEvent",
    "ResponseMcpListToolsFailedEvent",
    "ResponseMcpListToolsInProgressEvent",
    "ResponseOutputTextAnnotationAddedEvent",
    "ResponseQueuedEvent",
    "ResponseCustomToolCallInputDeltaEvent",
    "ResponseCustomToolCallInputDoneEvent",
    "GenericResponseEvent",
]


class ResponseAudioDeltaEvent(BaseModel):
    """Emitted when there is a partial audio response."""

    delta: str

    sequence_number: int

    type: Literal["response.audio.delta"]

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


class ResponseAudioDoneEvent(BaseModel):
    """Emitted when the audio response is complete."""

    sequence_number: int

    type: Literal["response.audio.done"]

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


class ResponseAudioTranscriptDeltaEvent(BaseModel):
    """Emitted when there is a partial transcript of audio."""

    delta: str

    sequence_number: int

    type: Literal["response.audio.transcript.delta"]

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


class ResponseAudioTranscriptDoneEvent(BaseModel):
    """Emitted when the full audio transcript is completed."""

    sequence_number: int

    type: Literal["response.audio.transcript.done"]

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


class ResponseCodeInterpreterCallCodeDeltaEvent(BaseModel):
    """Emitted when a partial code snippet is streamed by the code interpreter."""

    delta: str

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.code_interpreter_call_code.delta"]

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


class ResponseCodeInterpreterCallCodeDoneEvent(BaseModel):
    """Emitted when the code snippet is finalized by the code interpreter."""

    code: str

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.code_interpreter_call_code.done"]

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


class ResponseCodeInterpreterCallCompletedEvent(BaseModel):
    """Emitted when the code interpreter call is completed."""

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.code_interpreter_call.completed"]

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


class ResponseCodeInterpreterCallInProgressEvent(BaseModel):
    """Emitted when a code interpreter call is in progress."""

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.code_interpreter_call.in_progress"]

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


class ResponseCodeInterpreterCallInterpretingEvent(BaseModel):
    """Emitted when the code interpreter is actively interpreting the code snippet."""

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.code_interpreter_call.interpreting"]

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


class ResponseCompletedEvent(BaseModel):
    """Emitted when the model response is complete."""

    response: OpenAIResponse

    sequence_number: int

    type: Literal["response.completed"]

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


ResponseContentPartAddedEventPart: TypeAlias = Union[
    OpenAIResponseOutputText, OpenAIResponseOutputRefusal, PartReasoningText
]


class ResponseContentPartAddedEvent(BaseModel):
    """Emitted when a new content part is added."""

    content_index: int

    item_id: str

    output_index: int

    part: ResponseContentPartAddedEventPart
    """A text output from the model."""

    sequence_number: int

    type: Literal["response.content_part.added"]

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


ResponseContentPartDoneEventPart: TypeAlias = Union[
    OpenAIResponseOutputText, OpenAIResponseOutputRefusal, PartReasoningText
]


class ResponseContentPartDoneEvent(BaseModel):
    """Emitted when a content part is done."""

    content_index: int

    item_id: str

    output_index: int

    part: ResponseContentPartDoneEventPart
    """A text output from the model."""

    sequence_number: int

    type: Literal["response.content_part.done"]

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


class ResponseCreatedEvent(BaseModel):
    """An event that is emitted when a response is created."""

    response: OpenAIResponse

    sequence_number: int

    type: Literal["response.created"]

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


class ResponseErrorEvent(BaseModel):
    """Emitted when an error occurs."""

    message: str

    sequence_number: int

    type: Literal["error"]

    code: Optional[str] = None

    param: Optional[str] = None

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


class ResponseFileSearchCallCompletedEvent(BaseModel):
    """Emitted when a file search call is completed (results found)."""

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.file_search_call.completed"]

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


class ResponseFileSearchCallInProgressEvent(BaseModel):
    """Emitted when a file search call is initiated."""

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.file_search_call.in_progress"]

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


class ResponseFileSearchCallSearchingEvent(BaseModel):
    """Emitted when a file search is currently searching."""

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.file_search_call.searching"]

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


class ResponseFunctionCallArgumentsDeltaEvent(BaseModel):
    """Emitted when there is a partial function-call arguments delta."""

    delta: str

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.function_call_arguments.delta"]

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


class ResponseFunctionCallArgumentsDoneEvent(BaseModel):
    """Emitted when function-call arguments are finalized."""

    arguments: str

    item_id: str

    name: str

    output_index: int

    sequence_number: int

    type: Literal["response.function_call_arguments.done"]

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


class ResponseInProgressEvent(BaseModel):
    """Emitted when the response is in progress."""

    response: OpenAIResponse

    sequence_number: int

    type: Literal["response.in_progress"]

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


class ResponseFailedEvent(BaseModel):
    """An event that is emitted when a response fails."""

    response: OpenAIResponse

    sequence_number: int

    type: Literal["response.failed"]

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


class ResponseIncompleteEvent(BaseModel):
    """An event that is emitted when a response finishes as incomplete."""

    response: OpenAIResponse

    sequence_number: int

    type: Literal["response.incomplete"]

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


ResponseOutputItemAddedEventItem: TypeAlias = Union[
    OpenAIResponseOutputMessage,
    OpenAIResponseFileSearchToolCall,
    OpenAIResponseFunctionToolCall,
    OpenAIResponseFunctionWebSearch,
    OpenAIResponseComputerToolCall,
    OpenAIResponseReasoningItem,
    ResponseCompactionItem,
    OpenAITypesResponsesResponseOutputItemImageGenerationCall,
    OpenAIResponseCodeInterpreterToolCall,
    OpenAITypesResponsesResponseOutputItemLocalShellCall,
    ResponseFunctionShellToolCall,
    ResponseFunctionShellToolCallOutput,
    ResponseApplyPatchToolCall,
    ResponseApplyPatchToolCallOutput,
    OpenAITypesResponsesResponseOutputItemMcpCall,
    OpenAITypesResponsesResponseOutputItemMcpListTools,
    McpApprovalRequest,
    OpenAIResponseCustomToolCall,
]


class ResponseOutputItemAddedEvent(BaseModel):
    """Emitted when a new output item is added."""

    item: ResponseOutputItemAddedEventItem
    """An output message from the model."""

    output_index: int

    sequence_number: int

    type: Literal["response.output_item.added"]

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


ResponseOutputItemDoneEventItem: TypeAlias = Union[
    OpenAIResponseOutputMessage,
    OpenAIResponseFileSearchToolCall,
    OpenAIResponseFunctionToolCall,
    OpenAIResponseFunctionWebSearch,
    OpenAIResponseComputerToolCall,
    OpenAIResponseReasoningItem,
    ResponseCompactionItem,
    OpenAITypesResponsesResponseOutputItemImageGenerationCall,
    OpenAIResponseCodeInterpreterToolCall,
    OpenAITypesResponsesResponseOutputItemLocalShellCall,
    ResponseFunctionShellToolCall,
    ResponseFunctionShellToolCallOutput,
    ResponseApplyPatchToolCall,
    ResponseApplyPatchToolCallOutput,
    OpenAITypesResponsesResponseOutputItemMcpCall,
    OpenAITypesResponsesResponseOutputItemMcpListTools,
    McpApprovalRequest,
    OpenAIResponseCustomToolCall,
]


class ResponseOutputItemDoneEvent(BaseModel):
    """Emitted when an output item is marked done."""

    item: ResponseOutputItemDoneEventItem
    """An output message from the model."""

    output_index: int

    sequence_number: int

    type: Literal["response.output_item.done"]

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


class ResponseReasoningSummaryPartAddedEventPart(BaseModel):
    """The summary part that was added."""

    text: str

    type: Literal["summary_text"]

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


class ResponseReasoningSummaryPartAddedEvent(BaseModel):
    """Emitted when a new reasoning summary part is added."""

    item_id: str

    output_index: int

    part: ResponseReasoningSummaryPartAddedEventPart
    """The summary part that was added."""

    sequence_number: int

    summary_index: int

    type: Literal["response.reasoning_summary_part.added"]

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


class ResponseReasoningSummaryPartDoneEventPart(BaseModel):
    """The completed summary part."""

    text: str

    type: Literal["summary_text"]

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


class ResponseReasoningSummaryPartDoneEvent(BaseModel):
    """Emitted when a reasoning summary part is completed."""

    item_id: str

    output_index: int

    part: ResponseReasoningSummaryPartDoneEventPart
    """The completed summary part."""

    sequence_number: int

    summary_index: int

    type: Literal["response.reasoning_summary_part.done"]

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


class ResponseReasoningSummaryTextDeltaEvent(BaseModel):
    """Emitted when a delta is added to a reasoning summary text."""

    delta: str

    item_id: str

    output_index: int

    sequence_number: int

    summary_index: int

    type: Literal["response.reasoning_summary_text.delta"]

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


class ResponseReasoningSummaryTextDoneEvent(BaseModel):
    """Emitted when a reasoning summary text is completed."""

    item_id: str

    output_index: int

    sequence_number: int

    summary_index: int

    text: str

    type: Literal["response.reasoning_summary_text.done"]

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


class ResponseReasoningTextDeltaEvent(BaseModel):
    """Emitted when a delta is added to a reasoning text."""

    content_index: int

    delta: str

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.reasoning_text.delta"]

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


class ResponseReasoningTextDoneEvent(BaseModel):
    """Emitted when a reasoning text is completed."""

    content_index: int

    item_id: str

    output_index: int

    sequence_number: int

    text: str

    type: Literal["response.reasoning_text.done"]

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


class ResponseRefusalDeltaEvent(BaseModel):
    """Emitted when there is a partial refusal text."""

    content_index: int

    delta: str

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.refusal.delta"]

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


class ResponseRefusalDoneEvent(BaseModel):
    """Emitted when refusal text is finalized."""

    content_index: int

    item_id: str

    output_index: int

    refusal: str

    sequence_number: int

    type: Literal["response.refusal.done"]

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


class ResponseTextDeltaEventLogprobTopLogprob(BaseModel):
    token: Optional[str] = None

    logprob: Optional[float] = None

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


class ResponseTextDeltaEventLogprob(BaseModel):
    """
    A logprob is the logarithmic probability that the model assigns to producing
    a particular token at a given position in the sequence. Less-negative (higher)
    logprob values indicate greater model confidence in that token choice.
    """

    token: str

    logprob: float

    top_logprobs: Optional[List[ResponseTextDeltaEventLogprobTopLogprob]] = None

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


class ResponseTextDeltaEvent(BaseModel):
    """Emitted when there is an additional text delta."""

    content_index: int

    delta: str

    item_id: str

    logprobs: List[ResponseTextDeltaEventLogprob]

    output_index: int

    sequence_number: int

    type: Literal["response.output_text.delta"]

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


class ResponseTextDoneEventLogprobTopLogprob(BaseModel):
    token: Optional[str] = None

    logprob: Optional[float] = None

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


class ResponseTextDoneEventLogprob(BaseModel):
    """
    A logprob is the logarithmic probability that the model assigns to producing
    a particular token at a given position in the sequence. Less-negative (higher)
    logprob values indicate greater model confidence in that token choice.
    """

    token: str

    logprob: float

    top_logprobs: Optional[List[ResponseTextDoneEventLogprobTopLogprob]] = None

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


class ResponseTextDoneEvent(BaseModel):
    """Emitted when text content is finalized."""

    content_index: int

    item_id: str

    logprobs: List[ResponseTextDoneEventLogprob]

    output_index: int

    sequence_number: int

    text: str

    type: Literal["response.output_text.done"]

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


class ResponseWebSearchCallCompletedEvent(BaseModel):
    """Emitted when a web search call is completed."""

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.web_search_call.completed"]

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


class ResponseWebSearchCallInProgressEvent(BaseModel):
    """Emitted when a web search call is initiated."""

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.web_search_call.in_progress"]

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


class ResponseWebSearchCallSearchingEvent(BaseModel):
    """Emitted when a web search call is executing."""

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.web_search_call.searching"]

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


class ResponseImageGenCallCompletedEvent(BaseModel):
    """
    Emitted when an image generation tool call has completed and the final image is available.
    """

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.image_generation_call.completed"]

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


class ResponseImageGenCallGeneratingEvent(BaseModel):
    """
    Emitted when an image generation tool call is actively generating an image (intermediate state).
    """

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.image_generation_call.generating"]

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


class ResponseImageGenCallInProgressEvent(BaseModel):
    """Emitted when an image generation tool call is in progress."""

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.image_generation_call.in_progress"]

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


class ResponseImageGenCallPartialImageEvent(BaseModel):
    """Emitted when a partial image is available during image generation streaming."""

    item_id: str

    output_index: int

    partial_image_b64: str

    partial_image_index: int

    sequence_number: int

    type: Literal["response.image_generation_call.partial_image"]

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


class ResponseMcpCallArgumentsDeltaEvent(BaseModel):
    """
    Emitted when there is a delta (partial update) to the arguments of an MCP tool call.
    """

    delta: str

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.mcp_call_arguments.delta"]

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


class ResponseMcpCallArgumentsDoneEvent(BaseModel):
    """Emitted when the arguments for an MCP tool call are finalized."""

    arguments: str

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.mcp_call_arguments.done"]

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


class ResponseMcpCallCompletedEvent(BaseModel):
    """Emitted when an MCP  tool call has completed successfully."""

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.mcp_call.completed"]

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


class ResponseMcpCallFailedEvent(BaseModel):
    """Emitted when an MCP  tool call has failed."""

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.mcp_call.failed"]

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


class ResponseMcpCallInProgressEvent(BaseModel):
    """Emitted when an MCP  tool call is in progress."""

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.mcp_call.in_progress"]

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


class ResponseMcpListToolsCompletedEvent(BaseModel):
    """Emitted when the list of available MCP tools has been successfully retrieved."""

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.mcp_list_tools.completed"]

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


class ResponseMcpListToolsFailedEvent(BaseModel):
    """Emitted when the attempt to list available MCP tools has failed."""

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.mcp_list_tools.failed"]

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


class ResponseMcpListToolsInProgressEvent(BaseModel):
    """
    Emitted when the system is in the process of retrieving the list of available MCP tools.
    """

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.mcp_list_tools.in_progress"]

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


class ResponseOutputTextAnnotationAddedEvent(BaseModel):
    """Emitted when an annotation is added to output text content."""

    annotation: object

    annotation_index: int

    content_index: int

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.output_text.annotation.added"]

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


class ResponseQueuedEvent(BaseModel):
    """Emitted when a response is queued and waiting to be processed."""

    response: OpenAIResponse

    sequence_number: int

    type: Literal["response.queued"]

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


class ResponseCustomToolCallInputDeltaEvent(BaseModel):
    """Event representing a delta (partial update) to the input of a custom tool call."""

    delta: str

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.custom_tool_call_input.delta"]

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


class ResponseCustomToolCallInputDoneEvent(BaseModel):
    """Event indicating that input for a custom tool call is complete."""

    input: str

    item_id: str

    output_index: int

    sequence_number: int

    type: Literal["response.custom_tool_call_input.done"]

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


class GenericResponseEvent(BaseModel):
    type: str

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


ResponseCreateResponse: TypeAlias = Union[
    OpenAIResponse,
    ResponseAudioDeltaEvent,
    ResponseAudioDoneEvent,
    ResponseAudioTranscriptDeltaEvent,
    ResponseAudioTranscriptDoneEvent,
    ResponseCodeInterpreterCallCodeDeltaEvent,
    ResponseCodeInterpreterCallCodeDoneEvent,
    ResponseCodeInterpreterCallCompletedEvent,
    ResponseCodeInterpreterCallInProgressEvent,
    ResponseCodeInterpreterCallInterpretingEvent,
    ResponseCompletedEvent,
    ResponseContentPartAddedEvent,
    ResponseContentPartDoneEvent,
    ResponseCreatedEvent,
    ResponseErrorEvent,
    ResponseFileSearchCallCompletedEvent,
    ResponseFileSearchCallInProgressEvent,
    ResponseFileSearchCallSearchingEvent,
    ResponseFunctionCallArgumentsDeltaEvent,
    ResponseFunctionCallArgumentsDoneEvent,
    ResponseInProgressEvent,
    ResponseFailedEvent,
    ResponseIncompleteEvent,
    ResponseOutputItemAddedEvent,
    ResponseOutputItemDoneEvent,
    ResponseReasoningSummaryPartAddedEvent,
    ResponseReasoningSummaryPartDoneEvent,
    ResponseReasoningSummaryTextDeltaEvent,
    ResponseReasoningSummaryTextDoneEvent,
    ResponseReasoningTextDeltaEvent,
    ResponseReasoningTextDoneEvent,
    ResponseRefusalDeltaEvent,
    ResponseRefusalDoneEvent,
    ResponseTextDeltaEvent,
    ResponseTextDoneEvent,
    ResponseWebSearchCallCompletedEvent,
    ResponseWebSearchCallInProgressEvent,
    ResponseWebSearchCallSearchingEvent,
    ResponseImageGenCallCompletedEvent,
    ResponseImageGenCallGeneratingEvent,
    ResponseImageGenCallInProgressEvent,
    ResponseImageGenCallPartialImageEvent,
    ResponseMcpCallArgumentsDeltaEvent,
    ResponseMcpCallArgumentsDoneEvent,
    ResponseMcpCallCompletedEvent,
    ResponseMcpCallFailedEvent,
    ResponseMcpCallInProgressEvent,
    ResponseMcpListToolsCompletedEvent,
    ResponseMcpListToolsFailedEvent,
    ResponseMcpListToolsInProgressEvent,
    ResponseOutputTextAnnotationAddedEvent,
    ResponseQueuedEvent,
    ResponseCustomToolCallInputDeltaEvent,
    ResponseCustomToolCallInputDoneEvent,
    GenericResponseEvent,
]
