# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._types import SequenceNotStr
from .local_environment_param import LocalEnvironmentParam
from .container_reference_param import ContainerReferenceParam
from .mcp_approval_request_param import McpApprovalRequestParam
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
    "InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationAnnotationFileCitation",
    "InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationOpenAITypesResponsesResponseOutputTextParamAnnotationURLCitation",
    "InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationAnnotationContainerFileCitation",
    "InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationAnnotationFilePath",
    "InputInputItemResponseOutputMessageParamContentResponseOutputTextParamLogprob",
    "InputInputItemResponseOutputMessageParamContentResponseOutputTextParamLogprobTopLogprob",
    "InputInputItemResponseOutputMessageParamContentResponseOutputRefusalParam",
    "InputInputItemResponseFileSearchToolCallParam",
    "InputInputItemResponseFileSearchToolCallParamResult",
    "InputInputItemResponseComputerToolCallParam",
    "InputInputItemResponseComputerToolCallParamAction",
    "InputInputItemResponseComputerToolCallParamActionActionClick",
    "InputInputItemResponseComputerToolCallParamActionActionDoubleClick",
    "InputInputItemResponseComputerToolCallParamActionActionDrag",
    "InputInputItemResponseComputerToolCallParamActionActionDragPath",
    "InputInputItemResponseComputerToolCallParamActionActionKeypress",
    "InputInputItemResponseComputerToolCallParamActionActionMove",
    "InputInputItemResponseComputerToolCallParamActionActionScreenshot",
    "InputInputItemResponseComputerToolCallParamActionActionScroll",
    "InputInputItemResponseComputerToolCallParamActionActionType",
    "InputInputItemResponseComputerToolCallParamActionActionWait",
    "InputInputItemResponseComputerToolCallParamPendingSafetyCheck",
    "InputInputItemOpenAITypesResponsesResponseInputParamComputerCallOutput",
    "InputInputItemOpenAITypesResponsesResponseInputParamComputerCallOutputOutput",
    "InputInputItemOpenAITypesResponsesResponseInputParamComputerCallOutputAcknowledgedSafetyCheck",
    "InputInputItemResponseFunctionWebSearchParam",
    "InputInputItemResponseFunctionWebSearchParamAction",
    "InputInputItemResponseFunctionWebSearchParamActionOpenAITypesResponsesResponseFunctionWebSearchParamActionSearch",
    "InputInputItemResponseFunctionWebSearchParamActionOpenAITypesResponsesResponseFunctionWebSearchParamActionSearchSource",
    "InputInputItemResponseFunctionWebSearchParamActionOpenAITypesResponsesResponseFunctionWebSearchParamActionOpenPage",
    "InputInputItemResponseFunctionWebSearchParamActionActionFind",
    "InputInputItemResponseFunctionToolCallParam",
    "InputInputItemOpenAITypesResponsesResponseInputParamFunctionCallOutput",
    "InputInputItemOpenAITypesResponsesResponseInputParamFunctionCallOutputOutputOutputContentList",
    "InputInputItemOpenAITypesResponsesResponseInputParamFunctionCallOutputOutputOutputContentListResponseInputTextContentParam",
    "InputInputItemOpenAITypesResponsesResponseInputParamFunctionCallOutputOutputOutputContentListResponseInputImageContentParam",
    "InputInputItemOpenAITypesResponsesResponseInputParamFunctionCallOutputOutputOutputContentListResponseInputFileContentParam",
    "InputInputItemResponseReasoningItemParam",
    "InputInputItemResponseReasoningItemParamSummary",
    "InputInputItemResponseReasoningItemParamContent",
    "InputInputItemResponseCompactionItemParamParam",
    "InputInputItemOpenAITypesResponsesResponseInputParamImageGenerationCall",
    "InputInputItemResponseCodeInterpreterToolCallParam",
    "InputInputItemResponseCodeInterpreterToolCallParamOutput",
    "InputInputItemResponseCodeInterpreterToolCallParamOutputOutputLogs",
    "InputInputItemResponseCodeInterpreterToolCallParamOutputOutputImage",
    "InputInputItemOpenAITypesResponsesResponseInputParamLocalShellCall",
    "InputInputItemOpenAITypesResponsesResponseInputParamLocalShellCallAction",
    "InputInputItemOpenAITypesResponsesResponseInputParamLocalShellCallOutput",
    "InputInputItemOpenAITypesResponsesResponseInputParamShellCall",
    "InputInputItemOpenAITypesResponsesResponseInputParamShellCallAction",
    "InputInputItemOpenAITypesResponsesResponseInputParamShellCallEnvironment",
    "InputInputItemOpenAITypesResponsesResponseInputParamShellCallOutput",
    "InputInputItemOpenAITypesResponsesResponseInputParamShellCallOutputOutput",
    "InputInputItemOpenAITypesResponsesResponseInputParamShellCallOutputOutputOutcome",
    "InputInputItemOpenAITypesResponsesResponseInputParamShellCallOutputOutputOutcomeOutcomeTimeout",
    "InputInputItemOpenAITypesResponsesResponseInputParamShellCallOutputOutputOutcomeOutcomeExit",
    "InputInputItemOpenAITypesResponsesResponseInputParamApplyPatchCall",
    "InputInputItemOpenAITypesResponsesResponseInputParamApplyPatchCallOperation",
    "InputInputItemOpenAITypesResponsesResponseInputParamApplyPatchCallOperationApplyPatchCallOperationCreateFile",
    "InputInputItemOpenAITypesResponsesResponseInputParamApplyPatchCallOperationApplyPatchCallOperationDeleteFile",
    "InputInputItemOpenAITypesResponsesResponseInputParamApplyPatchCallOperationApplyPatchCallOperationUpdateFile",
    "InputInputItemOpenAITypesResponsesResponseInputParamApplyPatchCallOutput",
    "InputInputItemOpenAITypesResponsesResponseInputParamMcpListTools",
    "InputInputItemOpenAITypesResponsesResponseInputParamMcpListToolsTool",
    "InputInputItemOpenAITypesResponsesResponseInputParamMcpApprovalResponse",
    "InputInputItemOpenAITypesResponsesResponseInputParamMcpCall",
    "InputInputItemResponseCustomToolCallOutputParam",
    "InputInputItemResponseCustomToolCallOutputParamOutputOutputContentList",
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


class InputInputItemEasyInputMessageParam(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """
    A message input to the model with a role indicating instruction following
    hierarchy. Instructions given with the `developer` or `system` role take
    precedence over instructions given with the `user` role. Messages with the
    `assistant` role are presumed to have been generated by the model in previous
    interactions.
    """

    content: Required[Union[str, Iterable[InputInputItemEasyInputMessageParamContentInputItem]]]

    role: Required[Literal["user", "assistant", "system", "developer"]]

    phase: Literal["commentary", "final_answer"]

    type: Literal["message"]


InputInputItemOpenAITypesResponsesResponseInputParamMessageContent: TypeAlias = Union[
    OpenAIResponseInputTextParam, OpenAIResponseInputImageParam, OpenAIResponseInputFileParam
]


class InputInputItemOpenAITypesResponsesResponseInputParamMessage(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """
    A message input to the model with a role indicating instruction following
    hierarchy. Instructions given with the `developer` or `system` role take
    precedence over instructions given with the `user` role.
    """

    content: Required[Iterable[InputInputItemOpenAITypesResponsesResponseInputParamMessageContent]]

    role: Required[Literal["user", "system", "developer"]]

    status: Literal["in_progress", "completed", "incomplete"]

    type: Literal["message"]


class InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationAnnotationFileCitation(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A citation to a file."""

    file_id: Required[str]

    filename: Required[str]

    index: Required[int]

    type: Required[Literal["file_citation"]]


class InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationOpenAITypesResponsesResponseOutputTextParamAnnotationURLCitation(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A citation for a web resource used to generate a model response."""

    end_index: Required[int]

    start_index: Required[int]

    title: Required[str]

    type: Required[Literal["url_citation"]]

    url: Required[str]


class InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationAnnotationContainerFileCitation(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A citation for a container file used to generate a model response."""

    container_id: Required[str]

    end_index: Required[int]

    file_id: Required[str]

    filename: Required[str]

    start_index: Required[int]

    type: Required[Literal["container_file_citation"]]


class InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationAnnotationFilePath(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A path to a file."""

    file_id: Required[str]

    index: Required[int]

    type: Required[Literal["file_path"]]


InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotation: TypeAlias = Union[
    InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationAnnotationFileCitation,
    InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationOpenAITypesResponsesResponseOutputTextParamAnnotationURLCitation,
    InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationAnnotationContainerFileCitation,
    InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotationAnnotationFilePath,
]


class InputInputItemResponseOutputMessageParamContentResponseOutputTextParamLogprobTopLogprob(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """The top log probability of a token."""

    token: Required[str]

    bytes: Required[Iterable[int]]

    logprob: Required[float]


class InputInputItemResponseOutputMessageParamContentResponseOutputTextParamLogprob(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """The log probability of a token."""

    token: Required[str]

    bytes: Required[Iterable[int]]

    logprob: Required[float]

    top_logprobs: Required[
        Iterable[InputInputItemResponseOutputMessageParamContentResponseOutputTextParamLogprobTopLogprob]
    ]


class InputInputItemResponseOutputMessageParamContentResponseOutputTextParam(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A text output from the model."""

    annotations: Required[Iterable[InputInputItemResponseOutputMessageParamContentResponseOutputTextParamAnnotation]]

    text: Required[str]

    type: Required[Literal["output_text"]]

    logprobs: Iterable[InputInputItemResponseOutputMessageParamContentResponseOutputTextParamLogprob]


class InputInputItemResponseOutputMessageParamContentResponseOutputRefusalParam(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A refusal from the model."""

    refusal: Required[str]

    type: Required[Literal["refusal"]]


InputInputItemResponseOutputMessageParamContent: TypeAlias = Union[
    InputInputItemResponseOutputMessageParamContentResponseOutputTextParam,
    InputInputItemResponseOutputMessageParamContentResponseOutputRefusalParam,
]


class InputInputItemResponseOutputMessageParam(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """An output message from the model."""

    id: Required[str]

    content: Required[Iterable[InputInputItemResponseOutputMessageParamContent]]

    role: Required[Literal["assistant"]]

    status: Required[Literal["in_progress", "completed", "incomplete"]]

    type: Required[Literal["message"]]

    phase: Literal["commentary", "final_answer"]


class InputInputItemResponseFileSearchToolCallParamResult(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    attributes: Dict[str, Union[str, float, bool]]

    file_id: str

    filename: str

    score: float

    text: str


class InputInputItemResponseFileSearchToolCallParam(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """The results of a file search tool call.

    See the
    [file search guide](https://platform.openai.com/docs/guides/tools-file-search) for more information.
    """

    id: Required[str]

    queries: Required[SequenceNotStr[str]]

    status: Required[Literal["in_progress", "searching", "completed", "incomplete", "failed"]]

    type: Required[Literal["file_search_call"]]

    results: Iterable[InputInputItemResponseFileSearchToolCallParamResult]


class InputInputItemResponseComputerToolCallParamActionActionClick(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A click action."""

    button: Required[Literal["left", "right", "wheel", "back", "forward"]]

    type: Required[Literal["click"]]

    x: Required[int]

    y: Required[int]


class InputInputItemResponseComputerToolCallParamActionActionDoubleClick(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A double click action."""

    type: Required[Literal["double_click"]]

    x: Required[int]

    y: Required[int]


class InputInputItemResponseComputerToolCallParamActionActionDragPath(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """An x/y coordinate pair, e.g. `{ x: 100, y: 200 }`."""

    x: Required[int]

    y: Required[int]


class InputInputItemResponseComputerToolCallParamActionActionDrag(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A drag action."""

    path: Required[Iterable[InputInputItemResponseComputerToolCallParamActionActionDragPath]]

    type: Required[Literal["drag"]]


class InputInputItemResponseComputerToolCallParamActionActionKeypress(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A collection of keypresses the model would like to perform."""

    keys: Required[SequenceNotStr[str]]

    type: Required[Literal["keypress"]]


class InputInputItemResponseComputerToolCallParamActionActionMove(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A mouse move action."""

    type: Required[Literal["move"]]

    x: Required[int]

    y: Required[int]


class InputInputItemResponseComputerToolCallParamActionActionScreenshot(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A screenshot action."""

    type: Required[Literal["screenshot"]]


class InputInputItemResponseComputerToolCallParamActionActionScroll(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A scroll action."""

    scroll_x: Required[int]

    scroll_y: Required[int]

    type: Required[Literal["scroll"]]

    x: Required[int]

    y: Required[int]


class InputInputItemResponseComputerToolCallParamActionActionType(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """An action to type in text."""

    text: Required[str]

    type: Required[Literal["type"]]


class InputInputItemResponseComputerToolCallParamActionActionWait(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A wait action."""

    type: Required[Literal["wait"]]


InputInputItemResponseComputerToolCallParamAction: TypeAlias = Union[
    InputInputItemResponseComputerToolCallParamActionActionClick,
    InputInputItemResponseComputerToolCallParamActionActionDoubleClick,
    InputInputItemResponseComputerToolCallParamActionActionDrag,
    InputInputItemResponseComputerToolCallParamActionActionKeypress,
    InputInputItemResponseComputerToolCallParamActionActionMove,
    InputInputItemResponseComputerToolCallParamActionActionScreenshot,
    InputInputItemResponseComputerToolCallParamActionActionScroll,
    InputInputItemResponseComputerToolCallParamActionActionType,
    InputInputItemResponseComputerToolCallParamActionActionWait,
]


class InputInputItemResponseComputerToolCallParamPendingSafetyCheck(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A pending safety check for the computer call."""

    id: Required[str]

    code: str

    message: str


class InputInputItemResponseComputerToolCallParam(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A tool call to a computer use tool.

    See the
    [computer use guide](https://platform.openai.com/docs/guides/tools-computer-use) for more information.
    """

    id: Required[str]

    action: Required[InputInputItemResponseComputerToolCallParamAction]
    """A click action."""

    call_id: Required[str]

    pending_safety_checks: Required[Iterable[InputInputItemResponseComputerToolCallParamPendingSafetyCheck]]

    status: Required[Literal["in_progress", "completed", "incomplete"]]

    type: Required[Literal["computer_call"]]


class InputInputItemOpenAITypesResponsesResponseInputParamComputerCallOutputOutput(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A computer screenshot image used with the computer use tool."""

    type: Required[Literal["computer_screenshot"]]

    file_id: str

    image_url: str


class InputInputItemOpenAITypesResponsesResponseInputParamComputerCallOutputAcknowledgedSafetyCheck(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A pending safety check for the computer call."""

    id: Required[str]

    code: str

    message: str


class InputInputItemOpenAITypesResponsesResponseInputParamComputerCallOutput(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """The output of a computer tool call."""

    call_id: Required[str]

    output: Required[InputInputItemOpenAITypesResponsesResponseInputParamComputerCallOutputOutput]
    """A computer screenshot image used with the computer use tool."""

    type: Required[Literal["computer_call_output"]]

    id: str

    acknowledged_safety_checks: Iterable[
        InputInputItemOpenAITypesResponsesResponseInputParamComputerCallOutputAcknowledgedSafetyCheck
    ]

    status: Literal["in_progress", "completed", "incomplete"]


class InputInputItemResponseFunctionWebSearchParamActionOpenAITypesResponsesResponseFunctionWebSearchParamActionSearchSource(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A source used in the search."""

    type: Required[Literal["url"]]

    url: Required[str]


class InputInputItemResponseFunctionWebSearchParamActionOpenAITypesResponsesResponseFunctionWebSearchParamActionSearch(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """Action type "search" - Performs a web search query."""

    query: Required[str]

    type: Required[Literal["search"]]

    queries: SequenceNotStr[str]

    sources: Iterable[
        InputInputItemResponseFunctionWebSearchParamActionOpenAITypesResponsesResponseFunctionWebSearchParamActionSearchSource
    ]


class InputInputItemResponseFunctionWebSearchParamActionOpenAITypesResponsesResponseFunctionWebSearchParamActionOpenPage(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """Action type "open_page" - Opens a specific URL from search results."""

    type: Required[Literal["open_page"]]

    url: str


class InputInputItemResponseFunctionWebSearchParamActionActionFind(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """Action type "find_in_page": Searches for a pattern within a loaded page."""

    pattern: Required[str]

    type: Required[Literal["find_in_page"]]

    url: Required[str]


InputInputItemResponseFunctionWebSearchParamAction: TypeAlias = Union[
    InputInputItemResponseFunctionWebSearchParamActionOpenAITypesResponsesResponseFunctionWebSearchParamActionSearch,
    InputInputItemResponseFunctionWebSearchParamActionOpenAITypesResponsesResponseFunctionWebSearchParamActionOpenPage,
    InputInputItemResponseFunctionWebSearchParamActionActionFind,
]


class InputInputItemResponseFunctionWebSearchParam(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """The results of a web search tool call.

    See the
    [web search guide](https://platform.openai.com/docs/guides/tools-web-search) for more information.
    """

    id: Required[str]

    action: Required[InputInputItemResponseFunctionWebSearchParamAction]
    """Action type "search" - Performs a web search query."""

    status: Required[Literal["in_progress", "searching", "completed", "failed"]]

    type: Required[Literal["web_search_call"]]


class InputInputItemResponseFunctionToolCallParam(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A tool call to run a function.

    See the
    [function calling guide](https://platform.openai.com/docs/guides/function-calling) for more information.
    """

    arguments: Required[str]

    call_id: Required[str]

    name: Required[str]

    type: Required[Literal["function_call"]]

    id: str

    status: Literal["in_progress", "completed", "incomplete"]


class InputInputItemOpenAITypesResponsesResponseInputParamFunctionCallOutputOutputOutputContentListResponseInputTextContentParam(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A text input to the model."""

    text: Required[str]

    type: Required[Literal["input_text"]]


class InputInputItemOpenAITypesResponsesResponseInputParamFunctionCallOutputOutputOutputContentListResponseInputImageContentParam(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """An image input to the model.

    Learn about [image inputs](https://platform.openai.com/docs/guides/vision)
    """

    type: Required[Literal["input_image"]]

    detail: Literal["low", "high", "auto"]

    file_id: str

    image_url: str


class InputInputItemOpenAITypesResponsesResponseInputParamFunctionCallOutputOutputOutputContentListResponseInputFileContentParam(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A file input to the model."""

    type: Required[Literal["input_file"]]

    file_data: str

    file_id: str

    file_url: str

    filename: str


InputInputItemOpenAITypesResponsesResponseInputParamFunctionCallOutputOutputOutputContentList: TypeAlias = Union[
    InputInputItemOpenAITypesResponsesResponseInputParamFunctionCallOutputOutputOutputContentListResponseInputTextContentParam,
    InputInputItemOpenAITypesResponsesResponseInputParamFunctionCallOutputOutputOutputContentListResponseInputImageContentParam,
    InputInputItemOpenAITypesResponsesResponseInputParamFunctionCallOutputOutputOutputContentListResponseInputFileContentParam,
]


class InputInputItemOpenAITypesResponsesResponseInputParamFunctionCallOutput(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """The output of a function tool call."""

    call_id: Required[str]

    output: Required[
        Union[
            str, Iterable[InputInputItemOpenAITypesResponsesResponseInputParamFunctionCallOutputOutputOutputContentList]
        ]
    ]

    type: Required[Literal["function_call_output"]]

    id: str

    status: Literal["in_progress", "completed", "incomplete"]


class InputInputItemResponseReasoningItemParamSummary(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A summary text from the model."""

    text: Required[str]

    type: Required[Literal["summary_text"]]


class InputInputItemResponseReasoningItemParamContent(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """Reasoning text from the model."""

    text: Required[str]

    type: Required[Literal["reasoning_text"]]


class InputInputItemResponseReasoningItemParam(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """
    A description of the chain of thought used by a reasoning model while generating
    a response. Be sure to include these items in your `input` to the Responses API
    for subsequent turns of a conversation if you are manually
    [managing context](https://platform.openai.com/docs/guides/conversation-state).
    """

    id: Required[str]

    summary: Required[Iterable[InputInputItemResponseReasoningItemParamSummary]]

    type: Required[Literal["reasoning"]]

    content: Iterable[InputInputItemResponseReasoningItemParamContent]

    encrypted_content: str

    status: Literal["in_progress", "completed", "incomplete"]


class InputInputItemResponseCompactionItemParamParam(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """
    A compaction item generated by the [`v1/responses/compact` API](https://platform.openai.com/docs/api-reference/responses/compact).
    """

    encrypted_content: Required[str]

    type: Required[Literal["compaction"]]

    id: str


class InputInputItemOpenAITypesResponsesResponseInputParamImageGenerationCall(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """An image generation request made by the model."""

    id: Required[str]

    result: Required[str]

    status: Required[Literal["in_progress", "completed", "generating", "failed"]]

    type: Required[Literal["image_generation_call"]]


class InputInputItemResponseCodeInterpreterToolCallParamOutputOutputLogs(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """The logs output from the code interpreter."""

    logs: Required[str]

    type: Required[Literal["logs"]]


class InputInputItemResponseCodeInterpreterToolCallParamOutputOutputImage(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """The image output from the code interpreter."""

    type: Required[Literal["image"]]

    url: Required[str]


InputInputItemResponseCodeInterpreterToolCallParamOutput: TypeAlias = Union[
    InputInputItemResponseCodeInterpreterToolCallParamOutputOutputLogs,
    InputInputItemResponseCodeInterpreterToolCallParamOutputOutputImage,
]


class InputInputItemResponseCodeInterpreterToolCallParam(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A tool call to run code."""

    id: Required[str]

    code: Required[str]

    container_id: Required[str]

    outputs: Required[Iterable[InputInputItemResponseCodeInterpreterToolCallParamOutput]]

    status: Required[Literal["in_progress", "completed", "incomplete", "interpreting", "failed"]]

    type: Required[Literal["code_interpreter_call"]]


class InputInputItemOpenAITypesResponsesResponseInputParamLocalShellCallAction(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """Execute a shell command on the server."""

    command: Required[SequenceNotStr[str]]

    env: Required[Dict[str, str]]

    type: Required[Literal["exec"]]

    timeout_ms: int

    user: str

    working_directory: str


class InputInputItemOpenAITypesResponsesResponseInputParamLocalShellCall(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A tool call to run a command on the local shell."""

    id: Required[str]

    action: Required[InputInputItemOpenAITypesResponsesResponseInputParamLocalShellCallAction]
    """Execute a shell command on the server."""

    call_id: Required[str]

    status: Required[Literal["in_progress", "completed", "incomplete"]]

    type: Required[Literal["local_shell_call"]]


class InputInputItemOpenAITypesResponsesResponseInputParamLocalShellCallOutput(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """The output of a local shell tool call."""

    id: Required[str]

    output: Required[str]

    type: Required[Literal["local_shell_call_output"]]

    status: Literal["in_progress", "completed", "incomplete"]


class InputInputItemOpenAITypesResponsesResponseInputParamShellCallAction(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """The shell commands and limits that describe how to run the tool call."""

    commands: Required[SequenceNotStr[str]]

    max_output_length: int

    timeout_ms: int


InputInputItemOpenAITypesResponsesResponseInputParamShellCallEnvironment: TypeAlias = Union[
    LocalEnvironmentParam, ContainerReferenceParam
]


class InputInputItemOpenAITypesResponsesResponseInputParamShellCall(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A tool representing a request to execute one or more shell commands."""

    action: Required[InputInputItemOpenAITypesResponsesResponseInputParamShellCallAction]
    """The shell commands and limits that describe how to run the tool call."""

    call_id: Required[str]

    type: Required[Literal["shell_call"]]

    id: str

    environment: InputInputItemOpenAITypesResponsesResponseInputParamShellCallEnvironment

    status: Literal["in_progress", "completed", "incomplete"]


class InputInputItemOpenAITypesResponsesResponseInputParamShellCallOutputOutputOutcomeOutcomeTimeout(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """Indicates that the shell call exceeded its configured time limit."""

    type: Required[Literal["timeout"]]


class InputInputItemOpenAITypesResponsesResponseInputParamShellCallOutputOutputOutcomeOutcomeExit(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """Indicates that the shell commands finished and returned an exit code."""

    exit_code: Required[int]

    type: Required[Literal["exit"]]


InputInputItemOpenAITypesResponsesResponseInputParamShellCallOutputOutputOutcome: TypeAlias = Union[
    InputInputItemOpenAITypesResponsesResponseInputParamShellCallOutputOutputOutcomeOutcomeTimeout,
    InputInputItemOpenAITypesResponsesResponseInputParamShellCallOutputOutputOutcomeOutcomeExit,
]


class InputInputItemOpenAITypesResponsesResponseInputParamShellCallOutputOutput(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """Captured stdout and stderr for a portion of a shell tool call output."""

    outcome: Required[InputInputItemOpenAITypesResponsesResponseInputParamShellCallOutputOutputOutcome]
    """Indicates that the shell call exceeded its configured time limit."""

    stderr: Required[str]

    stdout: Required[str]


class InputInputItemOpenAITypesResponsesResponseInputParamShellCallOutput(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """The streamed output items emitted by a shell tool call."""

    call_id: Required[str]

    output: Required[Iterable[InputInputItemOpenAITypesResponsesResponseInputParamShellCallOutputOutput]]

    type: Required[Literal["shell_call_output"]]

    id: str

    max_output_length: int

    status: Literal["in_progress", "completed", "incomplete"]


class InputInputItemOpenAITypesResponsesResponseInputParamApplyPatchCallOperationApplyPatchCallOperationCreateFile(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """Instruction for creating a new file via the apply_patch tool."""

    diff: Required[str]

    path: Required[str]

    type: Required[Literal["create_file"]]


class InputInputItemOpenAITypesResponsesResponseInputParamApplyPatchCallOperationApplyPatchCallOperationDeleteFile(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """Instruction for deleting an existing file via the apply_patch tool."""

    path: Required[str]

    type: Required[Literal["delete_file"]]


class InputInputItemOpenAITypesResponsesResponseInputParamApplyPatchCallOperationApplyPatchCallOperationUpdateFile(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """Instruction for updating an existing file via the apply_patch tool."""

    diff: Required[str]

    path: Required[str]

    type: Required[Literal["update_file"]]


InputInputItemOpenAITypesResponsesResponseInputParamApplyPatchCallOperation: TypeAlias = Union[
    InputInputItemOpenAITypesResponsesResponseInputParamApplyPatchCallOperationApplyPatchCallOperationCreateFile,
    InputInputItemOpenAITypesResponsesResponseInputParamApplyPatchCallOperationApplyPatchCallOperationDeleteFile,
    InputInputItemOpenAITypesResponsesResponseInputParamApplyPatchCallOperationApplyPatchCallOperationUpdateFile,
]


class InputInputItemOpenAITypesResponsesResponseInputParamApplyPatchCall(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """
    A tool call representing a request to create, delete, or update files using diff patches.
    """

    call_id: Required[str]

    operation: Required[InputInputItemOpenAITypesResponsesResponseInputParamApplyPatchCallOperation]
    """Instruction for creating a new file via the apply_patch tool."""

    status: Required[Literal["in_progress", "completed"]]

    type: Required[Literal["apply_patch_call"]]

    id: str


class InputInputItemOpenAITypesResponsesResponseInputParamApplyPatchCallOutput(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """The streamed output emitted by an apply patch tool call."""

    call_id: Required[str]

    status: Required[Literal["completed", "failed"]]

    type: Required[Literal["apply_patch_call_output"]]

    id: str

    output: str


class InputInputItemOpenAITypesResponsesResponseInputParamMcpListToolsTool(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A tool available on an MCP server."""

    input_schema: Required[object]

    name: Required[str]

    annotations: object

    description: str


class InputInputItemOpenAITypesResponsesResponseInputParamMcpListTools(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A list of tools available on an MCP server."""

    id: Required[str]

    server_label: Required[str]

    tools: Required[Iterable[InputInputItemOpenAITypesResponsesResponseInputParamMcpListToolsTool]]

    type: Required[Literal["mcp_list_tools"]]

    error: str


class InputInputItemOpenAITypesResponsesResponseInputParamMcpApprovalResponse(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A response to an MCP approval request."""

    approval_request_id: Required[str]

    approve: Required[bool]

    type: Required[Literal["mcp_approval_response"]]

    id: str

    reason: str


class InputInputItemOpenAITypesResponsesResponseInputParamMcpCall(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """An invocation of a tool on an MCP server."""

    id: Required[str]

    arguments: Required[str]

    name: Required[str]

    server_label: Required[str]

    type: Required[Literal["mcp_call"]]

    approval_request_id: str

    error: str

    output: str

    status: Literal["in_progress", "completed", "incomplete", "calling", "failed"]


InputInputItemResponseCustomToolCallOutputParamOutputOutputContentList: TypeAlias = Union[
    OpenAIResponseInputTextParam, OpenAIResponseInputImageParam, OpenAIResponseInputFileParam
]


class InputInputItemResponseCustomToolCallOutputParam(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """The output of a custom tool call from your code, being sent back to the model."""

    call_id: Required[str]

    output: Required[Union[str, Iterable[InputInputItemResponseCustomToolCallOutputParamOutputOutputContentList]]]

    type: Required[Literal["custom_tool_call_output"]]

    id: str


class InputInputItemResponseCustomToolCallParam(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A call to a custom tool created by the model."""

    call_id: Required[str]

    input: Required[str]

    name: Required[str]

    type: Required[Literal["custom_tool_call"]]

    id: str


class InputInputItemOpenAITypesResponsesResponseInputParamItemReference(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """An internal identifier for an item to reference."""

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
    InputInputItemResponseCompactionItemParamParam,
    InputInputItemOpenAITypesResponsesResponseInputParamImageGenerationCall,
    InputInputItemResponseCodeInterpreterToolCallParam,
    InputInputItemOpenAITypesResponsesResponseInputParamLocalShellCall,
    InputInputItemOpenAITypesResponsesResponseInputParamLocalShellCallOutput,
    InputInputItemOpenAITypesResponsesResponseInputParamShellCall,
    InputInputItemOpenAITypesResponsesResponseInputParamShellCallOutput,
    InputInputItemOpenAITypesResponsesResponseInputParamApplyPatchCall,
    InputInputItemOpenAITypesResponsesResponseInputParamApplyPatchCallOutput,
    InputInputItemOpenAITypesResponsesResponseInputParamMcpListTools,
    McpApprovalRequestParam,
    InputInputItemOpenAITypesResponsesResponseInputParamMcpApprovalResponse,
    InputInputItemOpenAITypesResponsesResponseInputParamMcpCall,
    InputInputItemResponseCustomToolCallOutputParam,
    InputInputItemResponseCustomToolCallParam,
    InputInputItemOpenAITypesResponsesResponseInputParamItemReference,
]
