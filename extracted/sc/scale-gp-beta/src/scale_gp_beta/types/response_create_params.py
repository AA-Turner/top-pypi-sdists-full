# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._types import SequenceNotStr
from .openai_response_input_file_param import OpenAIResponseInputFileParam
from .openai_response_input_text_param import OpenAIResponseInputTextParam
from .openai_response_input_image_param import OpenAIResponseInputImageParam

__all__ = [
    "ResponseCreateParams",
    "InputInputItem",
    "InputInputItemEasyInputMessageParam",
    "InputInputItemEasyInputMessageParamContentInputItem",
    "InputInputItemOpenAITypesResponsesResponseInputParamMessage",
    "InputInputItemOpenAITypesResponsesResponseInputParamMessageContent",
    "InputInputItemResponseOutputMessageParam",
    "InputInputItemResponseOutputMessageParamContent",
    "InputInputItemResponseOutputMessageParamContentResponseOutputTextParam",
    "InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotation",
    "InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationOpenAITypesResponsesResponseOutputTextParamAnnotationFileCitation",
    "InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationOpenAITypesResponsesResponseOutputTextParamAnnotationURLCitation",
    "InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationOpenAITypesResponsesResponseOutputTextParamAnnotationContainerFileCitation",
    "InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationOpenAITypesResponsesResponseOutputTextParamAnnotationFilePath",
    "InputInputItemResponseOutputMessageParamContentResponseOutputTextParamLogprob",
    "InputInputItemResponseOutputMessageParamContentResponseOutputTextParamLogprobTopLogprob",
    "InputInputItemResponseOutputMessageParamContentResponseOutputRefusalParam",
    "InputInputItemResponseFileSearchToolCallParam",
    "InputInputItemResponseFileSearchToolCallParamResult",
    "InputInputItemResponseComputerToolCallParam",
    "InputInputItemResponseComputerToolCallParamAction",
    "InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionClick",
    "InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionDoubleClick",
    "InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionDrag",
    "InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionDragPath",
    "InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionKeypress",
    "InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionMove",
    "InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionScreenshot",
    "InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionScroll",
    "InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionType",
    "InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionWait",
    "InputInputItemResponseComputerToolCallParamPendingSafetyCheck",
    "InputInputItemOpenAITypesResponsesResponseInputParamComputerCallOutput",
    "InputInputItemOpenAITypesResponsesResponseInputParamComputerCallOutputOutput",
    "InputInputItemOpenAITypesResponsesResponseInputParamComputerCallOutputAcknowledgedSafetyCheck",
    "InputInputItemResponseFunctionWebSearchParam",
    "InputInputItemResponseFunctionWebSearchParamAction",
    "InputInputItemResponseFunctionWebSearchParamActionOpenAITypesResponsesResponseFunctionWebSearchParamActionSearch",
    "InputInputItemResponseFunctionWebSearchParamActionOpenAITypesResponsesResponseFunctionWebSearchParamActionOpenPage",
    "InputInputItemResponseFunctionWebSearchParamActionOpenAITypesResponsesResponseFunctionWebSearchParamActionFind",
    "InputInputItemResponseFunctionToolCallParam",
    "InputInputItemOpenAITypesResponsesResponseInputParamFunctionCallOutput",
    "InputInputItemResponseReasoningItemParam",
    "InputInputItemResponseReasoningItemParamSummary",
    "InputInputItemResponseReasoningItemParamContent",
    "InputInputItemOpenAITypesResponsesResponseInputParamImageGenerationCall",
    "InputInputItemResponseCodeInterpreterToolCallParam",
    "InputInputItemResponseCodeInterpreterToolCallParamOutput",
    "InputInputItemResponseCodeInterpreterToolCallParamOutputOpenAITypesResponsesResponseCodeInterpreterToolCallParamOutputLogs",
    "InputInputItemResponseCodeInterpreterToolCallParamOutputOpenAITypesResponsesResponseCodeInterpreterToolCallParamOutputImage",
    "InputInputItemOpenAITypesResponsesResponseInputParamLocalShellCall",
    "InputInputItemOpenAITypesResponsesResponseInputParamLocalShellCallAction",
    "InputInputItemOpenAITypesResponsesResponseInputParamLocalShellCallOutput",
    "InputInputItemOpenAITypesResponsesResponseInputParamMcpListTools",
    "InputInputItemOpenAITypesResponsesResponseInputParamMcpListToolsTool",
    "InputInputItemOpenAITypesResponsesResponseInputParamMcpApprovalRequest",
    "InputInputItemOpenAITypesResponsesResponseInputParamMcpApprovalResponse",
    "InputInputItemOpenAITypesResponsesResponseInputParamMcpCall",
    "InputInputItemResponseCustomToolCallOutputParam",
    "InputInputItemResponseCustomToolCallParam",
    "InputInputItemOpenAITypesResponsesResponseInputParamItemReference",
]


class ResponseCreateParams(TypedDict, total=False):
    input: Required[Union[str, Iterable[InputInputItem]]]

    model: Required[str]
    """model specified as `model_vendor/model`, for example `openai/gpt-4o`"""

    include: SequenceNotStr[str]
    """Which fields to include in the response"""

    instructions: str
    """Instructions for the response generation"""

    max_output_tokens: int
    """Maximum number of output tokens"""

    metadata: Dict[str, object]
    """Metadata for the response"""

    parallel_tool_calls: bool
    """Whether to enable parallel tool calls"""

    previous_response_id: str
    """ID of the previous response for chaining"""

    reasoning: Dict[str, object]
    """Reasoning configuration for the response"""

    store: bool
    """Whether to store the response"""

    stream: bool
    """Whether to stream the response"""

    temperature: float
    """Sampling temperature for randomness control"""

    text: Dict[str, object]
    """Text configuration parameters"""

    tool_choice: Union[str, Dict[str, object]]
    """Tool choice configuration"""

    tools: Iterable[Dict[str, object]]
    """Tools available for the response"""

    top_p: float
    """Top-p sampling parameter"""

    truncation: Literal["auto", "disabled"]
    """Truncation configuration"""


InputInputItemEasyInputMessageParamContentInputItem: TypeAlias = Union[
    OpenAIResponseInputTextParam, OpenAIResponseInputImageParam, OpenAIResponseInputFileParam
]


class InputInputItemEasyInputMessageParam(TypedDict, total=False):
    content: Required[Union[str, Iterable[InputInputItemEasyInputMessageParamContentInputItem]]]

    role: Required[Literal["user", "assistant", "system", "developer"]]

    type: Literal["message"]


InputInputItemOpenAITypesResponsesResponseInputParamMessageContent: TypeAlias = Union[
    OpenAIResponseInputTextParam, OpenAIResponseInputImageParam, OpenAIResponseInputFileParam
]


class InputInputItemOpenAITypesResponsesResponseInputParamMessage(TypedDict, total=False):
    content: Required[Iterable[InputInputItemOpenAITypesResponsesResponseInputParamMessageContent]]

    role: Required[Literal["user", "system", "developer"]]

    status: Literal["in_progress", "completed", "incomplete"]

    type: Literal["message"]


class InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationOpenAITypesResponsesResponseOutputTextParamAnnotationFileCitation(
    TypedDict, total=False
):
    file_id: Required[str]

    filename: Required[str]

    index: Required[int]

    type: Required[Literal["file_citation"]]


class InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationOpenAITypesResponsesResponseOutputTextParamAnnotationURLCitation(
    TypedDict, total=False
):
    end_index: Required[int]

    start_index: Required[int]

    title: Required[str]

    type: Required[Literal["url_citation"]]

    url: Required[str]


class InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationOpenAITypesResponsesResponseOutputTextParamAnnotationContainerFileCitation(
    TypedDict, total=False
):
    container_id: Required[str]

    end_index: Required[int]

    file_id: Required[str]

    filename: Required[str]

    start_index: Required[int]

    type: Required[Literal["container_file_citation"]]


class InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationOpenAITypesResponsesResponseOutputTextParamAnnotationFilePath(
    TypedDict, total=False
):
    file_id: Required[str]

    index: Required[int]

    type: Required[Literal["file_path"]]


InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotation: TypeAlias = Union[
    InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationOpenAITypesResponsesResponseOutputTextParamAnnotationFileCitation,
    InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationOpenAITypesResponsesResponseOutputTextParamAnnotationURLCitation,
    InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationOpenAITypesResponsesResponseOutputTextParamAnnotationContainerFileCitation,
    InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationOpenAITypesResponsesResponseOutputTextParamAnnotationFilePath,
]


class InputInputItemResponseOutputMessageParamContentResponseOutputTextParamLogprobTopLogprob(TypedDict, total=False):
    token: Required[str]

    bytes: Required[Iterable[int]]

    logprob: Required[float]


class InputInputItemResponseOutputMessageParamContentResponseOutputTextParamLogprob(TypedDict, total=False):
    token: Required[str]

    bytes: Required[Iterable[int]]

    logprob: Required[float]

    top_logprobs: Required[
        Iterable[InputInputItemResponseOutputMessageParamContentResponseOutputTextParamLogprobTopLogprob]
    ]


class InputInputItemResponseOutputMessageParamContentResponseOutputTextParam(TypedDict, total=False):
    annotations: Required[Iterable[InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotation]]

    text: Required[str]

    type: Required[Literal["output_text"]]

    logprobs: Iterable[InputInputItemResponseOutputMessageParamContentResponseOutputTextParamLogprob]


class InputInputItemResponseOutputMessageParamContentResponseOutputRefusalParam(TypedDict, total=False):
    refusal: Required[str]

    type: Required[Literal["refusal"]]


InputInputItemResponseOutputMessageParamContent: TypeAlias = Union[
    InputInputItemResponseOutputMessageParamContentResponseOutputTextParam,
    InputInputItemResponseOutputMessageParamContentResponseOutputRefusalParam,
]


class InputInputItemResponseOutputMessageParam(TypedDict, total=False):
    id: Required[str]

    content: Required[Iterable[InputInputItemResponseOutputMessageParamContent]]

    role: Required[Literal["assistant"]]

    status: Required[Literal["in_progress", "completed", "incomplete"]]

    type: Required[Literal["message"]]


class InputInputItemResponseFileSearchToolCallParamResult(TypedDict, total=False):
    attributes: Dict[str, Union[str, float, bool]]

    file_id: str

    filename: str

    score: float

    text: str


class InputInputItemResponseFileSearchToolCallParam(TypedDict, total=False):
    id: Required[str]

    queries: Required[SequenceNotStr[str]]

    status: Required[Literal["in_progress", "searching", "completed", "incomplete", "failed"]]

    type: Required[Literal["file_search_call"]]

    results: Iterable[InputInputItemResponseFileSearchToolCallParamResult]


class InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionClick(
    TypedDict, total=False
):
    button: Required[Literal["left", "right", "wheel", "back", "forward"]]

    type: Required[Literal["click"]]

    x: Required[int]

    y: Required[int]


class InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionDoubleClick(
    TypedDict, total=False
):
    type: Required[Literal["double_click"]]

    x: Required[int]

    y: Required[int]


class InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionDragPath(
    TypedDict, total=False
):
    x: Required[int]

    y: Required[int]


class InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionDrag(
    TypedDict, total=False
):
    path: Required[
        Iterable[
            InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionDragPath
        ]
    ]

    type: Required[Literal["drag"]]


class InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionKeypress(
    TypedDict, total=False
):
    keys: Required[SequenceNotStr[str]]

    type: Required[Literal["keypress"]]


class InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionMove(
    TypedDict, total=False
):
    type: Required[Literal["move"]]

    x: Required[int]

    y: Required[int]


class InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionScreenshot(
    TypedDict, total=False
):
    type: Required[Literal["screenshot"]]


class InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionScroll(
    TypedDict, total=False
):
    scroll_x: Required[int]

    scroll_y: Required[int]

    type: Required[Literal["scroll"]]

    x: Required[int]

    y: Required[int]


class InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionType(
    TypedDict, total=False
):
    text: Required[str]

    type: Required[Literal["type"]]


class InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionWait(
    TypedDict, total=False
):
    type: Required[Literal["wait"]]


InputInputItemResponseComputerToolCallParamAction: TypeAlias = Union[
    InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionClick,
    InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionDoubleClick,
    InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionDrag,
    InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionKeypress,
    InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionMove,
    InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionScreenshot,
    InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionScroll,
    InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionType,
    InputInputItemResponseComputerToolCallParamActionOpenAITypesResponsesResponseComputerToolCallParamActionWait,
]


class InputInputItemResponseComputerToolCallParamPendingSafetyCheck(TypedDict, total=False):
    id: Required[str]

    code: Required[str]

    message: Required[str]


class InputInputItemResponseComputerToolCallParam(TypedDict, total=False):
    id: Required[str]

    action: Required[InputInputItemResponseComputerToolCallParamAction]

    call_id: Required[str]

    pending_safety_checks: Required[Iterable[InputInputItemResponseComputerToolCallParamPendingSafetyCheck]]

    status: Required[Literal["in_progress", "completed", "incomplete"]]

    type: Required[Literal["computer_call"]]


class InputInputItemOpenAITypesResponsesResponseInputParamComputerCallOutputOutput(TypedDict, total=False):
    type: Required[Literal["computer_screenshot"]]

    file_id: str

    image_url: str


class InputInputItemOpenAITypesResponsesResponseInputParamComputerCallOutputAcknowledgedSafetyCheck(
    TypedDict, total=False
):
    id: Required[str]

    code: str

    message: str


class InputInputItemOpenAITypesResponsesResponseInputParamComputerCallOutput(TypedDict, total=False):
    call_id: Required[str]

    output: Required[InputInputItemOpenAITypesResponsesResponseInputParamComputerCallOutputOutput]

    type: Required[Literal["computer_call_output"]]

    id: str

    acknowledged_safety_checks: Iterable[
        InputInputItemOpenAITypesResponsesResponseInputParamComputerCallOutputAcknowledgedSafetyCheck
    ]

    status: Literal["in_progress", "completed", "incomplete"]


class InputInputItemResponseFunctionWebSearchParamActionOpenAITypesResponsesResponseFunctionWebSearchParamActionSearch(
    TypedDict, total=False
):
    query: Required[str]

    type: Required[Literal["search"]]


class InputInputItemResponseFunctionWebSearchParamActionOpenAITypesResponsesResponseFunctionWebSearchParamActionOpenPage(
    TypedDict, total=False
):
    type: Required[Literal["open_page"]]

    url: Required[str]


class InputInputItemResponseFunctionWebSearchParamActionOpenAITypesResponsesResponseFunctionWebSearchParamActionFind(
    TypedDict, total=False
):
    pattern: Required[str]

    type: Required[Literal["find"]]

    url: Required[str]


InputInputItemResponseFunctionWebSearchParamAction: TypeAlias = Union[
    InputInputItemResponseFunctionWebSearchParamActionOpenAITypesResponsesResponseFunctionWebSearchParamActionSearch,
    InputInputItemResponseFunctionWebSearchParamActionOpenAITypesResponsesResponseFunctionWebSearchParamActionOpenPage,
    InputInputItemResponseFunctionWebSearchParamActionOpenAITypesResponsesResponseFunctionWebSearchParamActionFind,
]


class InputInputItemResponseFunctionWebSearchParam(TypedDict, total=False):
    id: Required[str]

    action: Required[InputInputItemResponseFunctionWebSearchParamAction]

    status: Required[Literal["in_progress", "searching", "completed", "failed"]]

    type: Required[Literal["web_search_call"]]


class InputInputItemResponseFunctionToolCallParam(TypedDict, total=False):
    arguments: Required[str]

    call_id: Required[str]

    name: Required[str]

    type: Required[Literal["function_call"]]

    id: str

    status: Literal["in_progress", "completed", "incomplete"]


class InputInputItemOpenAITypesResponsesResponseInputParamFunctionCallOutput(TypedDict, total=False):
    call_id: Required[str]

    output: Required[str]

    type: Required[Literal["function_call_output"]]

    id: str

    status: Literal["in_progress", "completed", "incomplete"]


class InputInputItemResponseReasoningItemParamSummary(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["summary_text"]]


class InputInputItemResponseReasoningItemParamContent(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["reasoning_text"]]


class InputInputItemResponseReasoningItemParam(TypedDict, total=False):
    id: Required[str]

    summary: Required[Iterable[InputInputItemResponseReasoningItemParamSummary]]

    type: Required[Literal["reasoning"]]

    content: Iterable[InputInputItemResponseReasoningItemParamContent]

    encrypted_content: str

    status: Literal["in_progress", "completed", "incomplete"]


class InputInputItemOpenAITypesResponsesResponseInputParamImageGenerationCall(TypedDict, total=False):
    id: Required[str]

    result: Required[str]

    status: Required[Literal["in_progress", "completed", "generating", "failed"]]

    type: Required[Literal["image_generation_call"]]


class InputInputItemResponseCodeInterpreterToolCallParamOutputOpenAITypesResponsesResponseCodeInterpreterToolCallParamOutputLogs(
    TypedDict, total=False
):
    logs: Required[str]

    type: Required[Literal["logs"]]


class InputInputItemResponseCodeInterpreterToolCallParamOutputOpenAITypesResponsesResponseCodeInterpreterToolCallParamOutputImage(
    TypedDict, total=False
):
    type: Required[Literal["image"]]

    url: Required[str]


InputInputItemResponseCodeInterpreterToolCallParamOutput: TypeAlias = Union[
    InputInputItemResponseCodeInterpreterToolCallParamOutputOpenAITypesResponsesResponseCodeInterpreterToolCallParamOutputLogs,
    InputInputItemResponseCodeInterpreterToolCallParamOutputOpenAITypesResponsesResponseCodeInterpreterToolCallParamOutputImage,
]


class InputInputItemResponseCodeInterpreterToolCallParam(TypedDict, total=False):
    id: Required[str]

    code: Required[str]

    container_id: Required[str]

    outputs: Required[Iterable[InputInputItemResponseCodeInterpreterToolCallParamOutput]]

    status: Required[Literal["in_progress", "completed", "incomplete", "interpreting", "failed"]]

    type: Required[Literal["code_interpreter_call"]]


class InputInputItemOpenAITypesResponsesResponseInputParamLocalShellCallAction(TypedDict, total=False):
    command: Required[SequenceNotStr[str]]

    env: Required[Dict[str, str]]

    type: Required[Literal["exec"]]

    timeout_ms: int

    user: str

    working_directory: str


class InputInputItemOpenAITypesResponsesResponseInputParamLocalShellCall(TypedDict, total=False):
    id: Required[str]

    action: Required[InputInputItemOpenAITypesResponsesResponseInputParamLocalShellCallAction]

    call_id: Required[str]

    status: Required[Literal["in_progress", "completed", "incomplete"]]

    type: Required[Literal["local_shell_call"]]


class InputInputItemOpenAITypesResponsesResponseInputParamLocalShellCallOutput(TypedDict, total=False):
    id: Required[str]

    output: Required[str]

    type: Required[Literal["local_shell_call_output"]]

    status: Literal["in_progress", "completed", "incomplete"]


class InputInputItemOpenAITypesResponsesResponseInputParamMcpListToolsTool(TypedDict, total=False):
    input_schema: Required[object]

    name: Required[str]

    annotations: object

    description: str


class InputInputItemOpenAITypesResponsesResponseInputParamMcpListTools(TypedDict, total=False):
    id: Required[str]

    server_label: Required[str]

    tools: Required[Iterable[InputInputItemOpenAITypesResponsesResponseInputParamMcpListToolsTool]]

    type: Required[Literal["mcp_list_tools"]]

    error: str


class InputInputItemOpenAITypesResponsesResponseInputParamMcpApprovalRequest(TypedDict, total=False):
    id: Required[str]

    arguments: Required[str]

    name: Required[str]

    server_label: Required[str]

    type: Required[Literal["mcp_approval_request"]]


class InputInputItemOpenAITypesResponsesResponseInputParamMcpApprovalResponse(TypedDict, total=False):
    approval_request_id: Required[str]

    approve: Required[bool]

    type: Required[Literal["mcp_approval_response"]]

    id: str

    reason: str


class InputInputItemOpenAITypesResponsesResponseInputParamMcpCall(TypedDict, total=False):
    id: Required[str]

    arguments: Required[str]

    name: Required[str]

    server_label: Required[str]

    type: Required[Literal["mcp_call"]]

    error: str

    output: str


class InputInputItemResponseCustomToolCallOutputParam(TypedDict, total=False):
    call_id: Required[str]

    output: Required[str]

    type: Required[Literal["custom_tool_call_output"]]

    id: str


class InputInputItemResponseCustomToolCallParam(TypedDict, total=False):
    call_id: Required[str]

    input: Required[str]

    name: Required[str]

    type: Required[Literal["custom_tool_call"]]

    id: str


class InputInputItemOpenAITypesResponsesResponseInputParamItemReference(TypedDict, total=False):
    id: Required[str]

    type: Literal["item_reference"]


InputInputItem: TypeAlias = Union[
    InputInputItemEasyInputMessageParam,
    InputInputItemOpenAITypesResponsesResponseInputParamMessage,
    InputInputItemResponseOutputMessageParam,
    InputInputItemResponseFileSearchToolCallParam,
    InputInputItemResponseComputerToolCallParam,
    InputInputItemOpenAITypesResponsesResponseInputParamComputerCallOutput,
    InputInputItemResponseFunctionWebSearchParam,
    InputInputItemResponseFunctionToolCallParam,
    InputInputItemOpenAITypesResponsesResponseInputParamFunctionCallOutput,
    InputInputItemResponseReasoningItemParam,
    InputInputItemOpenAITypesResponsesResponseInputParamImageGenerationCall,
    InputInputItemResponseCodeInterpreterToolCallParam,
    InputInputItemOpenAITypesResponsesResponseInputParamLocalShellCall,
    InputInputItemOpenAITypesResponsesResponseInputParamLocalShellCallOutput,
    InputInputItemOpenAITypesResponsesResponseInputParamMcpListTools,
    InputInputItemOpenAITypesResponsesResponseInputParamMcpApprovalRequest,
    InputInputItemOpenAITypesResponsesResponseInputParamMcpApprovalResponse,
    InputInputItemOpenAITypesResponsesResponseInputParamMcpCall,
    InputInputItemResponseCustomToolCallOutputParam,
    InputInputItemResponseCustomToolCallParam,
    InputInputItemOpenAITypesResponsesResponseInputParamItemReference,
]
