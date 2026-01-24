from enum import Enum
from typing import Any, Dict, Generator, List, Literal, Optional, Union

from pydantic import BaseModel, Field, RootModel, model_validator
from typing_extensions import Annotated


class MessageRole(str, Enum):
    agent = "agent"
    assistant = "assistant"
    developer = "developer"
    function = "function"
    system = "system"
    tool = "tool"
    user = "user"


class Message(BaseModel):
    content: str
    role: MessageRole
    tool_call_id: Optional[str] = None
    tool_calls: Optional[List["ToolCall"]] = None

    @model_validator(mode="before")
    def _allow_null_content_with_tool_calling(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        # Some APIs (like OpenAI) often set content to None when there are tool calls.
        # This is a workaround to allow for that case without changing the type of the field.
        # TODO: Consider making the content field nullable.
        if data.get("content") is None:
            if data.get("tool_calls") is None:
                raise ValueError("at most one of 'content' and 'tool_calls' can be None, but both were None")
            # Deep copy and preserve key order
            data = {k: "" if k == "content" else v for k, v in data.items()}
        return data


class Messages(RootModel[List[Message]]):
    def __len__(self) -> int:
        return len(self.root)

    def __iter__(self) -> Generator[Message, None, None]:  # type: ignore[override]
        yield from self.root

    def __getitem__(self, item: int) -> Message:
        return self.root[item]


class ToolCall(BaseModel):
    id: str
    function: "ToolCallFunction"


class ToolCallFunction(BaseModel):
    name: str
    arguments: str


class EventType(str, Enum):
    """Types of events that can appear in reasoning/multi-turn model outputs."""

    message = "message"
    reasoning = "reasoning"
    internal_tool_call = "internal_tool_call"
    image_generation = "image_generation"
    mcp_call = "mcp_call"
    mcp_list_tools = "mcp_list_tools"
    mcp_approval_request = "mcp_approval_request"
    web_search_call = "web_search_call"


class EventStatus(str, Enum):
    """Common status values for events."""

    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"
    incomplete = "incomplete"


class BaseEvent(BaseModel):
    """Base class for all event types with common fields."""

    type: EventType = Field(description="The type of event")
    id: Optional[str] = Field(default=None, description="Unique identifier for the event")
    status: Optional[EventStatus] = Field(default=None, description="Status of the event")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Provider-specific metadata and additional fields"
    )
    error_message: Optional[str] = Field(default=None, description="Error message if the event failed")


class MessageEvent(BaseEvent):
    """An output message from the model."""

    type: Literal[EventType.message] = EventType.message
    role: MessageRole = Field(description="Role of the message sender")
    content: Optional[str] = Field(default=None, description="Text content of the message")
    content_parts: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Structured content items (text, audio, images, etc.)"
    )


class ReasoningEvent(BaseEvent):
    """Internal reasoning/thinking from the model (e.g., OpenAI o1/o3 reasoning tokens)."""

    type: Literal[EventType.reasoning] = EventType.reasoning
    content: Optional[str] = Field(default=None, description="The reasoning/thinking content")
    summary: Optional[Union[str, List[Dict[str, Any]]]] = Field(default=None, description="Summary of the reasoning")


class InternalToolCall(BaseEvent):
    """A tool call executed internally by the model during reasoning.

    This represents internal tools like web search, code execution, file search, etc.
    that the model invokes (not user-defined functions or MCP tools).
    """

    type: Literal[EventType.internal_tool_call] = EventType.internal_tool_call
    name: str = Field(description="Name of the internal tool (e.g., 'web_search', 'code_interpreter', 'file_search')")
    input: Optional[Dict[str, Any]] = Field(default=None, description="Input/arguments to the tool call")
    output: Optional[Dict[str, Any]] = Field(default=None, description="Output/results from the tool call")


class WebSearchAction(BaseModel):
    """Action payload for a web search call event."""

    type: Literal["search"] = Field(description="Type of web search action")
    query: Optional[str] = Field(default=None, description="Search query string")
    sources: Optional[Any] = Field(default=None, description="Optional provider-specific sources")


class WebSearchCallEvent(BaseEvent):
    """An OpenAI-style web search call event."""

    type: Literal[EventType.web_search_call] = EventType.web_search_call
    action: WebSearchAction = Field(description="Web search action payload")


class ImageGenerationEvent(BaseEvent):
    """An image generation event from the model."""

    type: Literal[EventType.image_generation] = EventType.image_generation
    prompt: Optional[str] = Field(default=None, description="The prompt used for image generation")
    images: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Generated images with URLs or base64 data"
    )
    model: Optional[str] = Field(default=None, description="Image generation model used")


class MCPCallEvent(BaseEvent):
    """A Model Context Protocol (MCP) tool call.

    MCP is a protocol for connecting LLMs to external tools/data sources.
    This is distinct from internal tools because it involves external integrations.
    """

    type: Literal[EventType.mcp_call] = EventType.mcp_call
    tool_name: Optional[str] = Field(default=None, description="Name of the MCP tool being called")
    server_name: Optional[str] = Field(default=None, description="Name of the MCP server")
    arguments: Optional[Dict[str, Any]] = Field(default=None, description="Arguments for the MCP tool call")
    result: Optional[Dict[str, Any]] = Field(default=None, description="Result from the MCP tool call")


class MCPListToolsEvent(BaseEvent):
    """MCP list tools event - when the model queries available MCP tools."""

    type: Literal[EventType.mcp_list_tools] = EventType.mcp_list_tools
    server_name: Optional[str] = Field(default=None, description="Name of the MCP server")
    tools: Optional[List[Dict[str, Any]]] = Field(default=None, description="List of available MCP tools")


class MCPApprovalRequestEvent(BaseEvent):
    """MCP approval request - when human approval is needed for an MCP tool call."""

    type: Literal[EventType.mcp_approval_request] = EventType.mcp_approval_request
    tool_name: Optional[str] = Field(default=None, description="Name of the MCP tool requiring approval")
    tool_invocation: Optional[Dict[str, Any]] = Field(
        default=None, description="Details of the tool invocation requiring approval"
    )
    approved: Optional[bool] = Field(default=None, description="Whether the request was approved")


# Union of all event types with discriminator
Event = Annotated[
    Union[
        MessageEvent,
        ReasoningEvent,
        InternalToolCall,
        WebSearchCallEvent,
        ImageGenerationEvent,
        MCPCallEvent,
        MCPListToolsEvent,
        MCPApprovalRequestEvent,
    ],
    Field(discriminator="type"),
]
