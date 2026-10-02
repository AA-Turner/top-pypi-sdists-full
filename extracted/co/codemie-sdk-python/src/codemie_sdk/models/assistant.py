"""Models for assistant-related data structures."""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Type, Optional, List, Union, Dict

from pydantic import BaseModel, Field, ConfigDict, model_validator

from .categories import Category
from .common import User
from .integration import Integration
from .errors import AgentErrorDetails, ToolErrorDetails


class ToolDetails(BaseModel):
    """Model for tool details."""

    model_config = ConfigDict(extra="ignore")

    name: str
    label: str | None = None
    settings_config: bool = False
    user_description: str | None = None
    settings: Integration | None = None


class ToolKitDetails(BaseModel):
    """Model for toolkit details."""

    model_config = ConfigDict(extra="ignore")

    toolkit: str
    tools: list[ToolDetails]
    label: str = ""
    settings_config: bool = False
    is_external: bool = False
    settings: Integration | None = None


class ContextType(str, Enum):
    """Enum for context types."""

    KNOWLEDGE_BASE = "knowledge_base"
    CODE = "code"
    PROVIDER = "provider"


class Context(BaseModel):
    """Model for context configuration."""

    model_config = ConfigDict(extra="ignore")

    context_type: ContextType
    name: str


class PromptVariable(BaseModel):
    """Model for assistant prompt variables."""

    model_config = ConfigDict(extra="ignore")

    key: str
    description: str | None = None
    default_value: str


class MCPServerConfig(BaseModel):
    """
    Configuration for an MCP server.

    Defines how to start and connect to an MCP server instance, including
    command, arguments, environment variables, and authentication parameters.

    Attributes:
        command (str): The command used to invoke the MCP server
        args (list[str] | None): list of arguments for the server command
        env (dict[str, Any] | None): Environment variables for the server process
        auth_token (str | None): Authentication token for MCP-Connect server
    """

    command: str | None = Field(
        None,
        description="The command used to invoke the MCP server (e.g., 'npx', 'uvx') using a stdio transport",
    )
    url: str | None = Field(
        None,
        description="The HTTP URL of a remote MCP server (use when connecting over HTTP/streamable-http).",
    )
    args: list[str] | None = Field(
        default_factory=list,
        description="List of arguments to pass to the MCP server command",
    )
    headers: dict[str, str] | None = Field(
        default_factory=dict,
        description="HTTP headers to include when connecting to an MCP server via `url`.",
    )
    env: dict[str, Any] | None = Field(
        default_factory=dict,
        description="Environment variables to be set for the MCP server process",
    )
    type: str | None = Field(
        None,
        description="Transport type. Set to 'streamable-http' to use a streamable HTTP transport; "
        "leave null for stdio/sse command transports.",
    )
    auth_token: str | None = Field(
        None, description="Authentication token for the MCP-Connect server"
    )
    single_usage: bool = Field(
        False,
        description="Whether this MCP server configuration is for single use only",
    )
    tools: list[str] | None = Field(
        None, description="List of tool names available in this MCP server"
    )


class MCPServerDetails(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str
    description: str | None
    enabled: bool
    mcp_config_id: str | None = None
    use_custom_config: bool = False
    config: MCPServerConfig | None = None
    mcp_connect_url: str | None = None
    tools_tokens_size_limit: int | None = None
    command: str | None = None
    arguments: str | None = None
    settings: Integration | None = None
    integration_alias: str | None = None
    mcp_connect_auth_token: Integration | None = None
    resolve_dynamic_values_in_arguments: bool = False
    tools: list[str] | None = None


class SystemPromptHistory(BaseModel):
    """Model for system prompt history."""

    model_config = ConfigDict(extra="ignore")

    system_prompt: str
    date: datetime
    created_by: User | None = None


class BuiltinSubagent(BaseModel):
    """Model for a built-in subagent entry from the catalog."""

    model_config = ConfigDict(extra="ignore")

    id: str
    display_name: str | None = None


class AssistantBase(BaseModel):
    """Base model for assistant with common fields."""

    def __getitem__(self, key):
        return getattr(self, key)

    model_config = ConfigDict(extra="ignore")

    id: str | None = None
    created_by: User | None = None
    name: str
    description: str
    icon_url: str | None = None


class AssistantListResponse(BaseModel):
    """Model for assistant list response."""

    model_config = ConfigDict(extra="ignore")

    id: str
    name: str
    slug: str | None = None
    created_by: User | None = None


class ToolCallPolicy(str, Enum):
    """Policy governing when tool calls require user approval."""

    AUTO_APPROVE = "auto_approve"
    APPROVE_FOR_ME = "approve_for_me"
    ASK_FOR_APPROVAL = "ask_for_approval"


class ToolCallAction(str, Enum):
    """User action on a pending tool-call confirmation."""

    ALLOW = "allow"
    DENY = "deny"


class ToolPermissionsConfig(BaseModel):
    """Configuration for tool-call approval policy on an assistant."""

    model_config = ConfigDict(extra="ignore")

    tool_call_policy: ToolCallPolicy = ToolCallPolicy.AUTO_APPROVE
    allow_override: bool = True


class ToolCallResumeRequest(BaseModel):
    """Request body for POST /v1/assistants/{id}/model/tool-call/resume."""

    model_config = ConfigDict(extra="ignore", use_enum_values=True)

    conversation_id: str = Field(
        description="Conversation ID that has a pending tool-call checkpoint"
    )
    action: ToolCallAction = Field(
        description="User decision: 'allow' executes the tool, 'deny' rejects it"
    )
    stream: bool = Field(default=True, description="Enable streaming NDJSON response")


class Assistant(AssistantBase):
    """Full assistant model with additional fields."""

    model_config = ConfigDict(extra="ignore", use_enum_values=True)

    system_prompt: str
    system_prompt_history: list[SystemPromptHistory] = Field(default_factory=list)
    project: str
    llm_model_type: str | None = None
    toolkits: list[ToolKitDetails] = Field(default_factory=list)
    conversation_starters: list[str] = Field(
        default_factory=list,
        description="List of suggested conversation starter prompts",
    )
    shared: bool = False
    is_react: bool = False
    is_global: bool = False
    created_date: datetime | None = None
    updated_date: datetime | None = None
    creator: str = "system"
    slug: str | None = None
    temperature: float | None = None
    top_p: float | None = None
    tools_tokens_size_limit: int | None = None
    context: list[Context] = Field(default_factory=list)
    user_abilities: list[Any] | None = None
    display_name: str | None = None
    mcp_servers: list[MCPServerDetails] = Field(default_factory=list)
    assistant_ids: list[str] = Field(default_factory=list)
    enabled_builtin_subagents: list[str] = Field(default_factory=list)
    version_count: int | None = None
    prompt_variables: list[PromptVariable] | None = Field(default=None)
    categories: list[str | Category] | None = Field(
        default_factory=list,
        description="List of categories for marketplace classification (e.g., 'quality-assurance', 'data-analysis')",
    )
    unique_users_count: int | None = Field(
        default=0,
        description="Number of unique users who have interacted with this assistant",
    )
    unique_likes_count: int | None = Field(
        default=None,
        description="Number of unique likes for this assistant",
    )
    unique_dislikes_count: int | None = Field(
        default=None,
        description="Number of unique dislikes for this assistant",
    )
    clone_count: int | None = Field(
        default=None,
        description="Number of times this assistant has been cloned in the Marketplace",
    )
    tool_permissions: ToolPermissionsConfig | None = None


class AssistantRequestBase(AssistantBase):
    """Base model for assistant requests with common request fields."""

    def __getitem__(self, key):
        return getattr(self, key)

    model_config = ConfigDict(extra="ignore", use_enum_values=True)

    system_prompt: str
    project: str
    context: list[Context] = Field(default_factory=list)
    llm_model_type: str
    toolkits: list[ToolKitDetails] = Field(default_factory=list)
    conversation_starters: list[str] = Field(
        default_factory=list,
        description="List of suggested conversation starter prompts",
    )
    shared: bool = False
    is_react: bool = False
    is_global: bool | None = False
    categories: list[str] = Field(
        default_factory=list,
        description="List of categories for marketplace classification (e.g., 'quality-assurance', 'data-analysis')",
    )
    slug: str | None = None
    temperature: float | None = None
    top_p: float | None = None
    tools_tokens_size_limit: int | None = None
    mcp_servers: list[MCPServerDetails] = Field(default_factory=list)
    assistant_ids: list[str] = Field(default_factory=list)
    enabled_builtin_subagents: list[str] | None = None
    prompt_variables: list[PromptVariable] = Field(default_factory=list)
    skip_integration_validation: bool | None = Field(default=False)
    tool_permissions: ToolPermissionsConfig | None = None


class AssistantCreateRequest(AssistantRequestBase):
    """Model for creating a new assistant."""

    pass


class AssistantUpdateRequest(AssistantRequestBase):
    """Model for updating an existing assistant."""

    pass


class MissingIntegration(BaseModel):
    """Model representing a single missing tool credential."""

    model_config = ConfigDict(extra="ignore")

    toolkit: str = Field(..., description="Toolkit name (e.g., 'Data Management')")
    tool: str = Field(..., description="Tool name (e.g., 'sql')")
    label: str = Field(..., description="Display label for the tool (e.g., 'SQL')")
    credential_type: str | None = Field(
        None, description="Credential type required (e.g., 'AWS', 'Jira')"
    )


class MissingIntegrationsByCredentialType(BaseModel):
    """Model representing missing tools grouped by credential type."""

    model_config = ConfigDict(extra="ignore")

    credential_type: str = Field(
        ..., description="Credential type (e.g., 'AWS', 'Jira', 'Confluence')"
    )
    missing_tools: list[MissingIntegration] = Field(
        ..., description="List of missing tools requiring this credential type"
    )
    # Optional sub-assistant context
    assistant_id: str | None = Field(
        None, description="Sub-assistant ID (if from sub-assistant)"
    )
    assistant_name: str | None = Field(
        None, description="Sub-assistant name (if from sub-assistant)"
    )
    icon_url: str | None = Field(
        None, description="Sub-assistant icon URL (if from sub-assistant)"
    )


class IntegrationValidationResult(BaseModel):
    """Complete validation result for assistant integrations."""

    model_config = ConfigDict(extra="ignore")

    has_missing_integrations: bool = Field(
        ..., description="Whether any integrations are missing"
    )
    missing_by_credential_type: list[MissingIntegrationsByCredentialType] = Field(
        default_factory=list,
        description="Missing tools in main assistant grouped by credential type",
    )
    sub_assistants_missing: list[MissingIntegrationsByCredentialType] = Field(
        default_factory=list,
        description="Missing tools in sub-assistants grouped by credential type",
    )
    message: str | None = Field(
        None, description="User-friendly message about missing integrations"
    )


class AssistantCreateResponse(BaseModel):
    """Response model for assistant creation with validation."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    message: str = Field(..., description="Response message")
    assistant_id: str | None = Field(
        None,
        alias="assistantId",
        description="Created assistant ID (None if validation failed)",
    )
    validation: IntegrationValidationResult | None = Field(
        None,
        description="Validation result (populated if validation found missing integrations)",
    )


class AssistantUpdateResponse(BaseModel):
    """Response model for assistant update with validation."""

    model_config = ConfigDict(extra="ignore")

    message: str = Field(..., description="Response message")
    validation: IntegrationValidationResult | None = Field(
        None,
        description="Validation result (populated if validation found missing integrations)",
    )


class AssistantVersion(BaseModel):
    """Immutable snapshot of assistant configuration for a specific version."""

    model_config = ConfigDict(extra="ignore", use_enum_values=True)

    version_number: int
    created_date: datetime
    created_by: User | None = None
    change_notes: str | None = None
    description: str | None = None
    system_prompt: str
    llm_model_type: str | None = None
    temperature: float | None = None
    top_p: float | None = None
    context: list[Context] = Field(default_factory=list)
    toolkits: list[ToolKitDetails] = Field(default_factory=list)
    mcp_servers: list[MCPServerDetails] = Field(default_factory=list)
    assistant_ids: list[str] = Field(default_factory=list)
    prompt_variables: list[PromptVariable] = Field(default_factory=list)


class ChatRole(str, Enum):
    """Enum for chat message roles."""

    ASSISTANT = "Assistant"
    USER = "User"


class ChatMessage(BaseModel):
    """Model for chat message."""

    role: ChatRole
    message: str | None = Field(default="")


class ToolConfig(BaseModel):
    name: str
    tool_creds: dict[str, Any] | None = None
    integration_id: str | None = None

    @model_validator(mode="after")
    def validate_credentials_provided(self) -> "ToolConfig":
        """
        Validate that either tool_creds or integration_id is provided.

        At least one of these fields must be specified for the tool configuration
        to be valid. This ensures that the tool has a way to obtain credentials.
        """
        if not self.tool_creds and not self.integration_id:
            raise ValueError("Either tool_creds or integration_id must be provided")
        if self.tool_creds and self.integration_id:
            raise ValueError(
                "Either tool_creds or integration_id must be provided, but not both"
            )
        return self


class AssistantChatRequest(BaseModel):
    """Model for chat request to assistant."""

    conversation_id: str | None = Field(
        default_factory=lambda: str(uuid.uuid4()), description="Conversation identifier"
    )
    text: str = Field(description="User's input")
    content_raw: str | None = Field(default="", description="Raw content input")
    file_names: list[str] = Field(
        default_factory=list, description="List of file names"
    )
    llm_model: str | None = Field(default=None, description="Specific LLM model to use")
    history: list[ChatMessage | None] | str = Field(
        default_factory=list,
        description="Conversation history as list of messages or string",
    )
    history_index: int = Field(
        default=None, description="DataSource in conversation history"
    )
    stream: bool = Field(default=False, description="Enable streaming response")
    propagate_headers: bool = Field(
        default=False,
        description="Enable propagation of X-* HTTP headers to MCP servers during tool execution",
    )
    custom_metadata: dict[str, Any] | None = Field(
        default=None,
        description="Custom metadata for the AI Assistant",
    )
    top_k: int = Field(default=10, description="Top K results to consider")
    system_prompt: str = Field(default="", description="Override system prompt")
    background_task: bool = Field(default=False, description="Run as background task")
    metadata: dict[str, Any] | None = Field(
        default=None, description="Provide additional metadata"
    )
    tools_config: list[ToolConfig] | None = None
    output_schema: dict | Type[BaseModel] | None = Field(
        default=None,
        description="Structured output schema for the agent. \
            If specified, `generated` field in response will have the same type",
    )
    mcp_server_single_usage: bool | None = Field(
        default=None,
        description="Override conversation-level MCP server lifecycle setting for this request. \
            When true, MCP servers are created fresh and destroyed after use. \
            When false, MCP servers are cached and reused. \
            If not specified, uses conversation's default setting.",
    )


class AgentMode(str, Enum):
    """Enum for agent execution mode."""

    GENERAL = "general"
    PLAN_EXECUTE = "plan_execute"


class VirtualAssistantChatRequest(BaseModel):
    """Request model for ephemeral virtual assistant inference.

    The assistant definition is provided inline; no database record is used.
    History is never persisted regardless of save_history value.
    """

    model_config = ConfigDict(extra="ignore", use_enum_values=True)

    # --- Assistant definition fields ---
    system_prompt: str = Field(
        default="", description="System prompt for the virtual assistant."
    )
    llm_model_type: Optional[str] = Field(
        default=None,
        description="LLM model identifier. Falls back to deployment default if omitted.",
    )
    temperature: Optional[float] = Field(default=None, ge=0.0, le=2.0)
    top_p: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    toolkits: List[ToolKitDetails] = Field(default_factory=list)
    context: List[Context] = Field(default_factory=list)
    mcp_servers: List[MCPServerDetails] = Field(default_factory=list)
    skill_ids: List[str] = Field(default_factory=list)
    assistant_ids: List[str] = Field(default_factory=list)
    agent_mode: AgentMode = Field(default=AgentMode.GENERAL)
    plan_prompt: Optional[str] = Field(default=None)
    smart_tool_selection_enabled: bool = Field(default=False)
    prompt_variables: List[PromptVariable] = Field(default_factory=list)

    # --- Chat parameters ---
    conversation_id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Conversation identifier. Auto-generated if omitted.",
    )
    text: Optional[str] = Field(default=None, description="User message text.")
    content_raw: Optional[str] = Field(default="")
    file_names: Optional[List[str]] = Field(default_factory=list)
    history: Union[List[ChatMessage], str] = Field(default_factory=list)
    stream: bool = Field(default=False)
    output_schema: Optional[Union[dict, Type[BaseModel]]] = Field(default=None)
    tools_config: Optional[List[ToolConfig]] = Field(default=None)
    metadata: Optional[Dict[str, Any]] = Field(default=None)
    top_k: int = Field(default=10)
    propagate_headers: bool = Field(default=False)
    disable_cache: Optional[bool] = Field(default=False)
    mcp_server_single_usage: Optional[bool] = Field(default=None)
    save_history: bool = Field(
        default=False,
        description="Always False for virtual assistants. Field is accepted but ignored.",
    )


class BaseModelResponse(BaseModel):
    """
    Model for chat response from assistant.

    Error fields expose agent and tool errors without breaking backward
    compatibility (all error fields default to None).
    """

    generated: str | dict | BaseModel = Field(
        description="Generated response. If output_schema in request is specified, corresponds with its type"
    )
    time_elapsed: float | None = Field(
        default=None, alias="timeElapsed", description="Time taken for generation"
    )
    tokens_used: int | None = Field(
        default=None, alias="tokensUsed", description="Number of tokens used"
    )
    thoughts: list[dict] | None = Field(
        default=None, description="Thought process details"
    )
    task_id: str | None = Field(
        default=None, alias="taskId", description="Background task identifier"
    )
    # Error handling fields
    success: bool = Field(
        default=True, description="Whether the agent execution was successful"
    )
    agent_error: AgentErrorDetails | None = Field(
        default=None,
        alias="agentError",
        description="Agent-level error details (callbacks, timeouts, etc.)",
    )
    tool_errors: list[ToolErrorDetails] | None = Field(
        default=None, alias="toolErrors", description="Tool execution error details"
    )

    model_config = ConfigDict(populate_by_name=True)


class EnvVars(BaseModel):
    azure_openai_url: str | None = None
    azure_openai_api_key: str | None = None
    openai_api_type: str | None = None
    openai_api_version: str | None = None
    models_env: str | None = None


class ExportAssistantPayload(BaseModel):
    env_vars: EnvVars | None = None


class AssistantEvaluationRequest(BaseModel):
    """Model for assistant evaluation request."""

    model_config = ConfigDict(extra="ignore")

    dataset_id: str = Field(description="ID of the dataset to use for evaluation")
    experiment_name: str = Field(description="Name of the evaluation experiment")
    system_prompt: str | None = Field(
        default=None, description="System prompt to use for evaluation"
    )
    llm_model: str | None = Field(
        default=None, description="LLM model to use for evaluation"
    )


class ReactionType(str, Enum):
    """Enum for reaction types."""

    LIKE = "like"
    DISLIKE = "dislike"


class ReactionRequest(BaseModel):
    """Model for assistant reaction request."""

    model_config = ConfigDict(extra="ignore", use_enum_values=True)

    reaction: ReactionType = Field(description="Reaction type: 'like' or 'dislike'")
