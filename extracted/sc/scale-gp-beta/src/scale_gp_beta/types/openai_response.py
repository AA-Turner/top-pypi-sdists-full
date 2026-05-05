# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import TYPE_CHECKING, Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .reasoning import Reasoning
from .shell_call import ShellCall
from .custom_tool import CustomTool
from .conversation import Conversation
from .computer_tool import ComputerTool
from .function_tool import FunctionTool
from .tool_choice_mcp import ToolChoiceMcp
from .web_search_tool import WebSearchTool
from .apply_patch_call import ApplyPatchCall
from .apply_patch_tool import ApplyPatchTool
from .file_search_tool import FileSearchTool
from .shell_call_output import ShellCallOutput
from .tool_choice_shell import ToolChoiceShell
from .tool_choice_types import ToolChoiceTypes
from .easy_input_message import EasyInputMessage
from .incomplete_details import IncompleteDetails
from .tool_choice_custom import ToolChoiceCustom
from .function_shell_tool import FunctionShellTool
from .tool_choice_allowed import ToolChoiceAllowed
from .mcp_approval_request import McpApprovalRequest
from .tool_choice_function import ToolChoiceFunction
from .openai_response_error import OpenAIResponseError
from .openai_response_usage import OpenAIResponseUsage
from .openai_response_prompt import OpenAIResponsePrompt
from .apply_patch_call_output import ApplyPatchCallOutput
from .tool_choice_apply_patch import ToolChoiceApplyPatch
from .web_search_preview_tool import WebSearchPreviewTool
from .response_compaction_item import ResponseCompactionItem
from .openai_response_text_config import OpenAIResponseTextConfig
from .openai_response_output_message import OpenAIResponseOutputMessage
from .openai_response_reasoning_item import OpenAIResponseReasoningItem
from .response_apply_patch_tool_call import ResponseApplyPatchToolCall
from .response_compaction_item_param import ResponseCompactionItemParam
from .openai_response_custom_tool_call import OpenAIResponseCustomToolCall
from .container_network_policy_disabled import ContainerNetworkPolicyDisabled
from .response_function_shell_tool_call import ResponseFunctionShellToolCall
from .container_network_policy_allowlist import ContainerNetworkPolicyAllowlist
from .openai_response_computer_tool_call import OpenAIResponseComputerToolCall
from .openai_response_function_tool_call import OpenAIResponseFunctionToolCall
from .openai_response_function_web_search import OpenAIResponseFunctionWebSearch
from .openai_response_file_search_tool_call import OpenAIResponseFileSearchToolCall
from .response_apply_patch_tool_call_output import ResponseApplyPatchToolCallOutput
from .openai_response_custom_tool_call_output import OpenAIResponseCustomToolCallOutput
from .response_function_shell_tool_call_output import ResponseFunctionShellToolCallOutput
from .openai_response_code_interpreter_tool_call import OpenAIResponseCodeInterpreterToolCall
from .openai_types_responses_response_input_item_message import OpenAITypesResponsesResponseInputItemMessage
from .openai_types_responses_response_input_item_mcp_call import OpenAITypesResponsesResponseInputItemMcpCall
from .openai_types_responses_response_output_item_mcp_call import OpenAITypesResponsesResponseOutputItemMcpCall
from .openai_types_responses_response_input_item_item_reference import (
    OpenAITypesResponsesResponseInputItemItemReference,
)
from .openai_types_responses_response_input_item_mcp_list_tools import OpenAITypesResponsesResponseInputItemMcpListTools
from .openai_types_responses_response_output_item_mcp_list_tools import (
    OpenAITypesResponsesResponseOutputItemMcpListTools,
)
from .openai_types_responses_response_input_item_local_shell_call import (
    OpenAITypesResponsesResponseInputItemLocalShellCall,
)
from .openai_types_responses_response_output_item_local_shell_call import (
    OpenAITypesResponsesResponseOutputItemLocalShellCall,
)
from .openai_types_responses_response_input_item_computer_call_output import (
    OpenAITypesResponsesResponseInputItemComputerCallOutput,
)
from .openai_types_responses_response_input_item_function_call_output import (
    OpenAITypesResponsesResponseInputItemFunctionCallOutput,
)
from .openai_types_responses_response_input_item_image_generation_call import (
    OpenAITypesResponsesResponseInputItemImageGenerationCall,
)
from .openai_types_responses_response_input_item_mcp_approval_response import (
    OpenAITypesResponsesResponseInputItemMcpApprovalResponse,
)
from .openai_types_responses_response_output_item_image_generation_call import (
    OpenAITypesResponsesResponseOutputItemImageGenerationCall,
)
from .openai_types_responses_response_input_item_local_shell_call_output import (
    OpenAITypesResponsesResponseInputItemLocalShellCallOutput,
)

__all__ = [
    "OpenAIResponse",
    "Output",
    "ToolChoice",
    "Tool",
    "ToolMcp",
    "ToolMcpAllowedTools",
    "ToolMcpAllowedToolsMcpAllowedToolsMcpToolFilter",
    "ToolMcpRequireApproval",
    "ToolMcpRequireApprovalMcpRequireApprovalMcpToolApprovalFilter",
    "ToolMcpRequireApprovalMcpRequireApprovalMcpToolApprovalFilterAlways",
    "ToolMcpRequireApprovalMcpRequireApprovalMcpToolApprovalFilterNever",
    "ToolCodeInterpreter",
    "ToolCodeInterpreterContainer",
    "ToolCodeInterpreterContainerCodeInterpreterContainerCodeInterpreterToolAuto",
    "ToolCodeInterpreterContainerCodeInterpreterContainerCodeInterpreterToolAutoNetworkPolicy",
    "ToolImageGeneration",
    "ToolImageGenerationInputImageMask",
    "ToolLocalShell",
    "InstructionsInputItem",
]

Output: TypeAlias = Union[
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

ToolChoice: TypeAlias = Union[
    Literal["none", "auto", "required"],
    ToolChoiceAllowed,
    ToolChoiceTypes,
    ToolChoiceFunction,
    ToolChoiceMcp,
    ToolChoiceCustom,
    ToolChoiceApplyPatch,
    ToolChoiceShell,
]


class ToolMcpAllowedToolsMcpAllowedToolsMcpToolFilter(BaseModel):
    """A filter object to specify which tools are allowed."""

    read_only: Optional[bool] = None

    tool_names: Optional[List[str]] = None

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


ToolMcpAllowedTools: TypeAlias = Union[List[str], ToolMcpAllowedToolsMcpAllowedToolsMcpToolFilter]


class ToolMcpRequireApprovalMcpRequireApprovalMcpToolApprovalFilterAlways(BaseModel):
    """A filter object to specify which tools are allowed."""

    read_only: Optional[bool] = None

    tool_names: Optional[List[str]] = None

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


class ToolMcpRequireApprovalMcpRequireApprovalMcpToolApprovalFilterNever(BaseModel):
    """A filter object to specify which tools are allowed."""

    read_only: Optional[bool] = None

    tool_names: Optional[List[str]] = None

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


class ToolMcpRequireApprovalMcpRequireApprovalMcpToolApprovalFilter(BaseModel):
    """Specify which of the MCP server's tools require approval.

    Can be
    `always`, `never`, or a filter object associated with tools
    that require approval.
    """

    always: Optional[ToolMcpRequireApprovalMcpRequireApprovalMcpToolApprovalFilterAlways] = None
    """A filter object to specify which tools are allowed."""

    never: Optional[ToolMcpRequireApprovalMcpRequireApprovalMcpToolApprovalFilterNever] = None
    """A filter object to specify which tools are allowed."""

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


ToolMcpRequireApproval: TypeAlias = Union[
    ToolMcpRequireApprovalMcpRequireApprovalMcpToolApprovalFilter, Literal["always", "never"]
]


class ToolMcp(BaseModel):
    """
    Give the model access to additional tools via remote Model Context Protocol
    (MCP) servers. [Learn more about MCP](https://platform.openai.com/docs/guides/tools-remote-mcp).
    """

    server_label: str

    type: Literal["mcp"]

    allowed_tools: Optional[ToolMcpAllowedTools] = None
    """A filter object to specify which tools are allowed."""

    authorization: Optional[str] = None

    connector_id: Optional[
        Literal[
            "connector_dropbox",
            "connector_gmail",
            "connector_googlecalendar",
            "connector_googledrive",
            "connector_microsoftteams",
            "connector_outlookcalendar",
            "connector_outlookemail",
            "connector_sharepoint",
        ]
    ] = None

    headers: Optional[Dict[str, str]] = None

    require_approval: Optional[ToolMcpRequireApproval] = None
    """Specify which of the MCP server's tools require approval.

    Can be `always`, `never`, or a filter object associated with tools that require
    approval.
    """

    server_description: Optional[str] = None

    server_url: Optional[str] = None

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


ToolCodeInterpreterContainerCodeInterpreterContainerCodeInterpreterToolAutoNetworkPolicy: TypeAlias = Union[
    ContainerNetworkPolicyDisabled, ContainerNetworkPolicyAllowlist
]


class ToolCodeInterpreterContainerCodeInterpreterContainerCodeInterpreterToolAuto(BaseModel):
    """Configuration for a code interpreter container.

    Optionally specify the IDs of the files to run the code on.
    """

    type: Literal["auto"]

    file_ids: Optional[List[str]] = None

    memory_limit: Optional[Literal["1g", "4g", "16g", "64g"]] = None

    network_policy: Optional[
        ToolCodeInterpreterContainerCodeInterpreterContainerCodeInterpreterToolAutoNetworkPolicy
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


ToolCodeInterpreterContainer: TypeAlias = Union[
    str, ToolCodeInterpreterContainerCodeInterpreterContainerCodeInterpreterToolAuto
]


class ToolCodeInterpreter(BaseModel):
    """A tool that runs Python code to help generate a response to a prompt."""

    container: ToolCodeInterpreterContainer
    """Configuration for a code interpreter container.

    Optionally specify the IDs of the files to run the code on.
    """

    type: Literal["code_interpreter"]

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


class ToolImageGenerationInputImageMask(BaseModel):
    """Optional mask for inpainting.

    Contains `image_url`
    (string, optional) and `file_id` (string, optional).
    """

    file_id: Optional[str] = None

    image_url: Optional[str] = None

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


class ToolImageGeneration(BaseModel):
    """A tool that generates images using the GPT image models."""

    type: Literal["image_generation"]

    action: Optional[Literal["generate", "edit", "auto"]] = None

    background: Optional[Literal["transparent", "opaque", "auto"]] = None

    input_fidelity: Optional[Literal["high", "low"]] = None

    input_image_mask: Optional[ToolImageGenerationInputImageMask] = None
    """Optional mask for inpainting.

    Contains `image_url` (string, optional) and `file_id` (string, optional).
    """

    model: Union[str, Literal["gpt-image-1", "gpt-image-1-mini", "gpt-image-1.5"], None] = None

    moderation: Optional[Literal["auto", "low"]] = None

    output_compression: Optional[int] = None

    output_format: Optional[Literal["png", "webp", "jpeg"]] = None

    partial_images: Optional[int] = None

    quality: Optional[Literal["low", "medium", "high", "auto"]] = None

    size: Optional[Literal["1024x1024", "1024x1536", "1536x1024", "auto"]] = None

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


class ToolLocalShell(BaseModel):
    """A tool that allows the model to execute shell commands in a local environment."""

    type: Literal["local_shell"]

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


Tool: TypeAlias = Union[
    FunctionTool,
    FileSearchTool,
    ComputerTool,
    WebSearchTool,
    ToolMcp,
    ToolCodeInterpreter,
    ToolImageGeneration,
    ToolLocalShell,
    FunctionShellTool,
    CustomTool,
    WebSearchPreviewTool,
    ApplyPatchTool,
]

InstructionsInputItem: TypeAlias = Union[
    EasyInputMessage,
    OpenAITypesResponsesResponseInputItemMessage,
    OpenAIResponseOutputMessage,
    OpenAIResponseFileSearchToolCall,
    OpenAIResponseComputerToolCall,
    OpenAITypesResponsesResponseInputItemComputerCallOutput,
    OpenAIResponseFunctionWebSearch,
    OpenAIResponseFunctionToolCall,
    OpenAITypesResponsesResponseInputItemFunctionCallOutput,
    OpenAIResponseReasoningItem,
    ResponseCompactionItemParam,
    OpenAITypesResponsesResponseInputItemImageGenerationCall,
    OpenAIResponseCodeInterpreterToolCall,
    OpenAITypesResponsesResponseInputItemLocalShellCall,
    OpenAITypesResponsesResponseInputItemLocalShellCallOutput,
    ShellCall,
    ShellCallOutput,
    ApplyPatchCall,
    ApplyPatchCallOutput,
    OpenAITypesResponsesResponseInputItemMcpListTools,
    McpApprovalRequest,
    OpenAITypesResponsesResponseInputItemMcpApprovalResponse,
    OpenAITypesResponsesResponseInputItemMcpCall,
    OpenAIResponseCustomToolCallOutput,
    OpenAIResponseCustomToolCall,
    OpenAITypesResponsesResponseInputItemItemReference,
]


class OpenAIResponse(BaseModel):
    id: str

    created_at: float

    model: Union[
        Literal[
            "gpt-5.2",
            "gpt-5.2-2025-12-11",
            "gpt-5.2-chat-latest",
            "gpt-5.2-pro",
            "gpt-5.2-pro-2025-12-11",
            "gpt-5.1",
            "gpt-5.1-2025-11-13",
            "gpt-5.1-codex",
            "gpt-5.1-mini",
            "gpt-5.1-chat-latest",
            "gpt-5",
            "gpt-5-mini",
            "gpt-5-nano",
            "gpt-5-2025-08-07",
            "gpt-5-mini-2025-08-07",
            "gpt-5-nano-2025-08-07",
            "gpt-5-chat-latest",
            "gpt-4.1",
            "gpt-4.1-mini",
            "gpt-4.1-nano",
            "gpt-4.1-2025-04-14",
            "gpt-4.1-mini-2025-04-14",
            "gpt-4.1-nano-2025-04-14",
            "o4-mini",
            "o4-mini-2025-04-16",
            "o3",
            "o3-2025-04-16",
            "o3-mini",
            "o3-mini-2025-01-31",
            "o1",
            "o1-2024-12-17",
            "o1-preview",
            "o1-preview-2024-09-12",
            "o1-mini",
            "o1-mini-2024-09-12",
            "gpt-4o",
            "gpt-4o-2024-11-20",
            "gpt-4o-2024-08-06",
            "gpt-4o-2024-05-13",
            "gpt-4o-audio-preview",
            "gpt-4o-audio-preview-2024-10-01",
            "gpt-4o-audio-preview-2024-12-17",
            "gpt-4o-audio-preview-2025-06-03",
            "gpt-4o-mini-audio-preview",
            "gpt-4o-mini-audio-preview-2024-12-17",
            "gpt-4o-search-preview",
            "gpt-4o-mini-search-preview",
            "gpt-4o-search-preview-2025-03-11",
            "gpt-4o-mini-search-preview-2025-03-11",
            "chatgpt-4o-latest",
            "codex-mini-latest",
            "gpt-4o-mini",
            "gpt-4o-mini-2024-07-18",
            "gpt-4-turbo",
            "gpt-4-turbo-2024-04-09",
            "gpt-4-0125-preview",
            "gpt-4-turbo-preview",
            "gpt-4-1106-preview",
            "gpt-4-vision-preview",
            "gpt-4",
            "gpt-4-0314",
            "gpt-4-0613",
            "gpt-4-32k",
            "gpt-4-32k-0314",
            "gpt-4-32k-0613",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k",
            "gpt-3.5-turbo-0301",
            "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-1106",
            "gpt-3.5-turbo-0125",
            "gpt-3.5-turbo-16k-0613",
            "o1-pro",
            "o1-pro-2025-03-19",
            "o3-pro",
            "o3-pro-2025-06-10",
            "o3-deep-research",
            "o3-deep-research-2025-06-26",
            "o4-mini-deep-research",
            "o4-mini-deep-research-2025-06-26",
            "computer-use-preview",
            "computer-use-preview-2025-03-11",
            "gpt-5-codex",
            "gpt-5-pro",
            "gpt-5-pro-2025-10-06",
            "gpt-5.1-codex-max",
        ],
        str,
    ]

    object: Literal["response"]

    output: List[Output]

    parallel_tool_calls: bool

    tool_choice: ToolChoice
    """Constrains the tools available to the model to a pre-defined set."""

    tools: List[Tool]

    background: Optional[bool] = None

    completed_at: Optional[float] = None

    conversation: Optional[Conversation] = None
    """The conversation that this response belonged to.

    Input items and output items from this response were automatically added to this
    conversation.
    """

    error: Optional[OpenAIResponseError] = None
    """An error object returned when the model fails to generate a Response."""

    incomplete_details: Optional[IncompleteDetails] = None
    """Details about why the response is incomplete."""

    instructions: Union[str, List[InstructionsInputItem], None] = None

    max_output_tokens: Optional[int] = None

    max_tool_calls: Optional[int] = None

    metadata: Optional[Dict[str, str]] = None

    previous_response_id: Optional[str] = None

    prompt: Optional[OpenAIResponsePrompt] = None
    """
    Reference to a prompt template and its variables.
    [Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts).
    """

    prompt_cache_key: Optional[str] = None

    prompt_cache_retention: Optional[Literal["in-memory", "24h"]] = None

    reasoning: Optional[Reasoning] = None
    """**gpt-5 and o-series models only**

    Configuration options for
    [reasoning models](https://platform.openai.com/docs/guides/reasoning).
    """

    safety_identifier: Optional[str] = None

    service_tier: Optional[Literal["auto", "default", "flex", "scale", "priority"]] = None

    status: Optional[Literal["completed", "failed", "in_progress", "cancelled", "queued", "incomplete"]] = None

    temperature: Optional[float] = None

    text: Optional[OpenAIResponseTextConfig] = None
    """Configuration options for a text response from the model.

    Can be plain text or structured JSON data. Learn more:

    - [Text inputs and outputs](https://platform.openai.com/docs/guides/text)
    - [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
    """

    top_logprobs: Optional[int] = None

    top_p: Optional[float] = None

    truncation: Optional[Literal["auto", "disabled"]] = None

    usage: Optional[OpenAIResponseUsage] = None
    """
    Represents token usage details including input tokens, output tokens, a
    breakdown of output tokens, and the total tokens used.
    """

    user: Optional[str] = None

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
