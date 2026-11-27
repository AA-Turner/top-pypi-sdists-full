from collections.abc import Callable

from mistralai.client.models import (
    AssistantMessage,
    ChatCompletionRequest,
    ChatCompletionRequestMessage,
    ChatCompletionResponse,
    ConversationRequest,
    ConversationResponse,
    CreateAgentRequest,
    DeltaMessage,
    EmbeddingRequest,
    EmbeddingResponse,
    Function,
    FunctionCall,
    OCRRequest,
    OCRResponse,
    ResponseFormat,
    SystemMessage,
    Tool,
    ToolCall,
    ToolMessage,
    UserMessage,
)
from mistralai.workflows.core.rate_limiting.rate_limit import clear_rate_limit, set_rate_limit
from mistralai.workflows.plugins.mistralai.activities import (
    MistralEmbeddingsParams,
    chat_parse_to_model,
    mistralai_append_conversation,
    mistralai_append_conversation_stream,
    mistralai_chat_complete,
    mistralai_chat_parse,
    mistralai_chat_stream,
    mistralai_create_agent,
    mistralai_embeddings,
    mistralai_ocr,
    mistralai_start_conversation,
    mistralai_start_conversation_stream,
    mistralai_update_agent,
)
from mistralai.workflows.plugins.mistralai.agent import Agent
from mistralai.workflows.plugins.mistralai.connectors import (
    ConnectorAuthInterceptor,
    ConnectorAuthTimeout,
    ConnectorClient,
    ConnectorError,
    ConnectorSlot,
    ConnectorToolCallError,
    ResolvedConnectorBinding,
    connector,
    connector_get_auth_url,
    connector_get_mcp_app_resource_uris,
    connector_resolve,
    connector_tool_call,
    uses_connectors,
)
from mistralai.workflows.plugins.mistralai.lechat import (
    ACCEPT_OPTION_VALUE,
    DECLINE_OPTION_VALUE,
    LE_CHAT_INPUT_TAG,
    AcceptDeclineConfirmation,
    CanvasInput,
    CanvasPayload,
    CanvasResource,
    ChatAssistantWorkflowOutput,
    ChatAssistantWorkingTask,
    ChatInput,
    ChatInputModel,
    ConfirmationInput,
    ConfirmationInputModel,
    ContentChunk,
    ResourceOutput,
    TextChunk,
    TextOutput,
    TodoList,
    TodoListItem,
    UIComponentResource,
    input_tag,
    is_accepted,
    le_chat_input,
    send_assistant_message,
)
from mistralai.workflows.plugins.mistralai.mcp import (
    MCPConfig,
    MCPSSEConfig,
    MCPStdioConfig,
    MCPStreamableHTTPConfig,
    collect_mcp_tools,
    execute_mcp_tool,
)
from mistralai.workflows.plugins.mistralai.models import AgentUpdateRequest, ConversationAppendRequest
from mistralai.workflows.plugins.mistralai.runner import Runner
from mistralai.workflows.plugins.mistralai.session.local_session import (
    LocalSession,
    LocalSessionInputs,
    LocalSessionOutputs,
)
from mistralai.workflows.plugins.mistralai.session.remote_session import (
    RemoteSession,
    RemoteSessionInputs,
    RemoteSessionOutputs,
)
from mistralai.workflows.plugins.mistralai.utils import _get_agent_llm_rate_limit, get_mistral_client

_LLM_ACTIVITIES: tuple[Callable, ...] = (
    mistralai_create_agent,
    mistralai_start_conversation,
    mistralai_append_conversation,
    mistralai_update_agent,
    mistralai_chat_complete,
    mistralai_chat_stream,
    mistralai_start_conversation_stream,
    mistralai_append_conversation_stream,
    mistralai_chat_parse,
    mistralai_embeddings,
    mistralai_ocr,
)


def configure_for_worker(workflows: list[type]) -> None:
    del workflows
    rate_limit = _get_agent_llm_rate_limit()
    for activity in _LLM_ACTIVITIES:
        if rate_limit is None:
            clear_rate_limit(activity)
        else:
            set_rate_limit(activity, rate_limit)


def get_worker_interceptors(workflows: list[type]) -> list[ConnectorAuthInterceptor]:
    """Plugin hook called by the core worker to collect worker interceptors."""
    return [ConnectorAuthInterceptor(workflows=workflows)]


__all__ = [
    "AcceptDeclineConfirmation",
    "ACCEPT_OPTION_VALUE",
    "DECLINE_OPTION_VALUE",
    "Agent",
    "LE_CHAT_INPUT_TAG",
    "CreateAgentRequest",
    "AgentUpdateRequest",
    "AssistantMessage",
    "ChatCompletionRequest",
    "ChatCompletionResponse",
    "ConversationAppendRequest",
    "ConversationRequest",
    "ConversationResponse",
    "DeltaMessage",
    "EmbeddingRequest",
    "EmbeddingResponse",
    "Function",
    "FunctionCall",
    "ChatCompletionRequestMessage",
    "OCRRequest",
    "OCRResponse",
    "ResponseFormat",
    "LocalSession",
    "LocalSessionInputs",
    "LocalSessionOutputs",
    "RemoteSession",
    "RemoteSessionInputs",
    "RemoteSessionOutputs",
    "Runner",
    "SystemMessage",
    "TextChunk",
    "Tool",
    "ToolCall",
    "ToolMessage",
    "UserMessage",
    "CanvasInput",
    "ChatAssistantWorkflowOutput",
    "ChatAssistantWorkingTask",
    "ChatInput",
    "ChatInputModel",
    "ConfirmationInput",
    "ConfirmationInputModel",
    "is_accepted",
    "le_chat_input",
    "input_tag",
    "TextOutput",
    "TodoListItem",
    "TodoList",
    "send_assistant_message",
    "CanvasPayload",
    "CanvasResource",
    "ContentChunk",
    "ResourceOutput",
    "UIComponentResource",
    "get_mistral_client",
    # Activities
    "chat_parse_to_model",
    "collect_mcp_tools",
    "execute_mcp_tool",
    "MistralEmbeddingsParams",
    "mistralai_append_conversation",
    "mistralai_append_conversation_stream",
    "mistralai_chat_complete",
    "mistralai_chat_parse",
    "mistralai_chat_stream",
    "mistralai_create_agent",
    "mistralai_embeddings",
    "mistralai_ocr",
    "mistralai_start_conversation",
    "mistralai_start_conversation_stream",
    "mistralai_update_agent",
    # MCP
    "MCPConfig",
    "MCPSSEConfig",
    "MCPStdioConfig",
    "MCPStreamableHTTPConfig",
    # Connectors
    "ConnectorAuthInterceptor",
    "ConnectorAuthTimeout",
    "ConnectorClient",
    "ConnectorError",
    "ConnectorSlot",
    "ConnectorToolCallError",
    "ResolvedConnectorBinding",
    "connector",
    "connector_get_auth_url",
    "connector_get_mcp_app_resource_uris",
    "connector_resolve",
    "connector_tool_call",
    "uses_connectors",
]
