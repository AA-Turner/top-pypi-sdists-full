# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import TYPE_CHECKING, Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .mcp import Mcp
from .._models import BaseModel
from .reasoning import Reasoning
from .custom_tool import CustomTool
from .local_shell import LocalShell
from .computer_tool import ComputerTool
from .function_tool import FunctionTool
from .tool_choice_mcp import ToolChoiceMcp
from .web_search_tool import WebSearchTool
from .code_interpreter import CodeInterpreter
from .file_search_tool import FileSearchTool
from .image_generation import ImageGeneration
from .tool_choice_types import ToolChoiceTypes
from .easy_input_message import EasyInputMessage
from .incomplete_details import IncompleteDetails
from .tool_choice_custom import ToolChoiceCustom
from .tool_choice_allowed import ToolChoiceAllowed
from .tool_choice_function import ToolChoiceFunction
from .openai_response_error import OpenAIResponseError
from .openai_response_usage import OpenAIResponseUsage
from .openai_response_prompt import OpenAIResponsePrompt
from .openai_response_text_config import OpenAIResponseTextConfig
from .openai_response_output_message import OpenAIResponseOutputMessage
from .openai_response_reasoning_item import OpenAIResponseReasoningItem
from .openai_response_custom_tool_call import OpenAIResponseCustomToolCall
from .openai_response_computer_tool_call import OpenAIResponseComputerToolCall
from .openai_response_function_tool_call import OpenAIResponseFunctionToolCall
from .openai_response_function_web_search import OpenAIResponseFunctionWebSearch
from .openai_response_file_search_tool_call import OpenAIResponseFileSearchToolCall
from .openai_response_custom_tool_call_output import OpenAIResponseCustomToolCallOutput
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
from .openai_types_responses_response_input_item_mcp_approval_request import (
    OpenAITypesResponsesResponseInputItemMcpApprovalRequest,
)
from .openai_types_responses_response_input_item_image_generation_call import (
    OpenAITypesResponsesResponseInputItemImageGenerationCall,
)
from .openai_types_responses_response_input_item_mcp_approval_response import (
    OpenAITypesResponsesResponseInputItemMcpApprovalResponse,
)
from .openai_types_responses_response_output_item_mcp_approval_request import (
    OpenAITypesResponsesResponseOutputItemMcpApprovalRequest,
)
from .openai_types_responses_response_output_item_image_generation_call import (
    OpenAITypesResponsesResponseOutputItemImageGenerationCall,
)
from .openai_types_responses_response_input_item_local_shell_call_output import (
    OpenAITypesResponsesResponseInputItemLocalShellCallOutput,
)

__all__ = ["OpenAIResponse", "Output", "ToolChoice", "Tool", "InstructionsInputItem"]

Output: TypeAlias = Union[
    OpenAIResponseOutputMessage,
    OpenAIResponseFileSearchToolCall,
    OpenAIResponseFunctionToolCall,
    OpenAIResponseFunctionWebSearch,
    OpenAIResponseComputerToolCall,
    OpenAIResponseReasoningItem,
    OpenAITypesResponsesResponseOutputItemImageGenerationCall,
    OpenAIResponseCodeInterpreterToolCall,
    OpenAITypesResponsesResponseOutputItemLocalShellCall,
    OpenAITypesResponsesResponseOutputItemMcpCall,
    OpenAITypesResponsesResponseOutputItemMcpListTools,
    OpenAITypesResponsesResponseOutputItemMcpApprovalRequest,
    OpenAIResponseCustomToolCall,
]

ToolChoice: TypeAlias = Union[
    Literal["none", "auto", "required"],
    ToolChoiceAllowed,
    ToolChoiceTypes,
    ToolChoiceFunction,
    ToolChoiceMcp,
    ToolChoiceCustom,
]

Tool: TypeAlias = Union[
    FunctionTool,
    FileSearchTool,
    WebSearchTool,
    ComputerTool,
    Mcp,
    CodeInterpreter,
    ImageGeneration,
    LocalShell,
    CustomTool,
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
    OpenAITypesResponsesResponseInputItemImageGenerationCall,
    OpenAIResponseCodeInterpreterToolCall,
    OpenAITypesResponsesResponseInputItemLocalShellCall,
    OpenAITypesResponsesResponseInputItemLocalShellCallOutput,
    OpenAITypesResponsesResponseInputItemMcpListTools,
    OpenAITypesResponsesResponseInputItemMcpApprovalRequest,
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
        ],
        str,
    ]

    object: Literal["response"]

    output: List[Output]

    parallel_tool_calls: bool

    tool_choice: ToolChoice

    tools: List[Tool]

    background: Optional[bool] = None

    error: Optional[OpenAIResponseError] = None

    incomplete_details: Optional[IncompleteDetails] = None

    instructions: Union[str, List[InstructionsInputItem], None] = None

    max_output_tokens: Optional[int] = None

    max_tool_calls: Optional[int] = None

    metadata: Optional[Dict[str, str]] = None

    previous_response_id: Optional[str] = None

    prompt: Optional[OpenAIResponsePrompt] = None

    prompt_cache_key: Optional[str] = None

    reasoning: Optional[Reasoning] = None

    safety_identifier: Optional[str] = None

    service_tier: Optional[Literal["auto", "default", "flex", "scale", "priority"]] = None

    status: Optional[Literal["completed", "failed", "in_progress", "cancelled", "queued", "incomplete"]] = None

    temperature: Optional[float] = None

    text: Optional[OpenAIResponseTextConfig] = None

    top_logprobs: Optional[int] = None

    top_p: Optional[float] = None

    truncation: Optional[Literal["auto", "disabled"]] = None

    usage: Optional[OpenAIResponseUsage] = None

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
