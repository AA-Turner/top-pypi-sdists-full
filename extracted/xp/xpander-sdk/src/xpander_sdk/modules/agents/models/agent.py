"""
Agent models and configuration classes for the xpander.ai SDK.

This module contains all data models and enums related to agent creation,
configuration, and management within the xpander.ai Backend-as-a-Service platform.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Literal, Optional, Type
from pydantic import BaseModel, computed_field

from xpander_sdk.models.orchestrations import (
    DuplicationPreventionSettings,
    OrchestrationIterativeStrategy,
    OrchestrationRetryStrategy,
    OrchestrationStopStrategy,
)
from xpander_sdk.models.shared import XPanderSharedModel
from xpander_sdk.modules.tools_repository.models.mcp import MCPServerDetails


class AgentDeploymentType(str, Enum):
    """
    Enumeration of supported deployment types for agents.

    Values:
        Serverless: Serverless agent.
        Container: Containerized agent.
    """

    Serverless = "serverless"
    Container = "container"


class AgentStatus(str, Enum):
    """
    Enumeration of possible agent statuses.

    Values:
        DRAFT: Agent is in a draft state and not yet active.
        ACTIVE: Agent is active and operational, ready to handle tasks.
        INACTIVE: Agent is inactive and not operational.
    """

    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class AgentInstructions(BaseModel):
    """
    Model for agent instructions and configuration.

    This model defines the instructions and goals that guide an agent's behavior,
    including role definitions, goals, and general guidance.

    Attributes:
        role (List[str]): List of role-specific instructions for the agent.
        goal (List[str]): List of goals the agent should achieve.
        general (str): General instructions or description for the agent.
        dynamic_prompt_enabled (Optional[bool]): Whether the dynamic prompt code runs
            at prompt-build time.
        dynamic_prompt_code (Optional[str]): User Python defining
            ``xpander_dynamic_prompt() -> str``; its returned string is added to
            the system prompt. Mirrors ``AIAgentInstructions`` in xpander_dev_utils.
        dynamic_prompt_position (Optional[Literal]): Where the returned string is
            placed relative to the system prompt: ``"before"`` or ``"after"``.
    """

    role: List[str] = []
    goal: List[str] = []
    general: str = ""
    dynamic_prompt_enabled: Optional[bool] = False
    dynamic_prompt_code: Optional[str] = None
    dynamic_prompt_position: Optional[Literal["before", "after"]] = "after"

    @computed_field
    @property
    def description(self) -> str:
        """
        Get the general description of the agent.

        Returns:
            str: The general instructions/description.
        """
        return self.general

    def _blocks(self, with_description: bool = False) -> str:
        """Render only the non-empty instruction blocks, so a consolidated single-field agent doesn't emit empty <instructions>/<goals> wrappers."""
        parts: List[str] = []
        if with_description and self.general:
            parts.append(f"        <description>\n            {self.description}\n        </description>")
        if self.role:
            parts.append(f"        <instructions>\n            {self.role}\n        </instructions>")
        if self.goal:
            parts.append(f"        <goals>\n            {self.goal_str}\n        </goals>")
        return ("\n" + "\n".join(parts) + "\n        ") if parts else ""

    @computed_field
    @property
    def instructions(self) -> str:
        """
        Get the role-specific instructions for the agent.

        Returns:
            List[str]: List of role instructions.
        """
        return self._blocks()

    @computed_field
    @property
    def full(self) -> str:
        """
        Get the role-specific instructions for the agent.

        Returns:
            List[str]: List of role instructions.
        """
        return self._blocks(with_description=True)

    @computed_field
    @property
    def goal_str(self) -> str:
        """
        Get goals as a newline-separated string.

        Returns:
            str: Goals joined with newlines, or empty string if no goals.
        """
        return "\n".join(self.goal) if self.goal and isinstance(self.goal, list) else ""


class SourceNodeType(str, Enum):
    """
    Enumeration of source node types for agent graphs.

    Values:
        WORKBENCH: Workbench-based source node.
        SDK: SDK-based source node.
        TASK: Task-based source node.
        ASSISTANT: Assistant-based source node.
        WEBHOOK: Webhook-triggered source node.
        MCP: Model Context Protocol source node.
        A2A: Agent-to-Agent communication source node.
        TELEGRAM: Telegram bots integration.
        SLACK: Slackbots integration.
        EMAIL: Inbound email trigger source node.
        API: REST API / SDK task trigger source node.
    """

    WORKBENCH = "workbench"
    SDK = "sdk"
    TASK = "task"
    ASSISTANT = "assistant"
    WEBHOOK = "webhook"
    MCP = "mcp"
    A2A = "a2a"
    TELEGRAM = "telegram"
    SLACK = "slack"
    EMAIL = "email"
    API = "api"


class AgentSourceNode(BaseModel):
    """
    Model for agent source nodes in the execution graph.

    Attributes:
        id (Optional[str]): Unique identifier for the source node.
        type (SourceNodeType): Type of the source node.
        targets (Optional[List[str]]): List of target node IDs.
        metadata (Optional[Dict]): Additional metadata for the source node.
    """

    id: Optional[str] = None
    type: SourceNodeType
    targets: Optional[list[str]] = None
    metadata: Optional[Dict] = {}


class AgentAccessScope(str, Enum):
    """
    Enumeration of agent access scopes.

    Values:
        Personal: Agent is accessible only to the creator.
        Organizational: Agent is accessible to the entire organization.
    """

    Personal = "personal"
    Organizational = "organizational"


class AgentGraphItemType(str, Enum):
    """
    Enumeration of agent graph item types.

    Values:
        SOURCE_NODE: Entry point for agent execution.
        AGENT: Standard agent node.
        WORKFLOW: Workflow node.
        TOOL: Tool or function node.
        HUMAN_IN_THE_LOOP: Human approval/interaction node.
        SLEEP: Allow the agent to sleep between iterations.
        CUSTOM_AGENT: Custom agent implementation.
        STORAGE: Data storage node.
        CODING_AGENT: Specialized coding agent.
        MCP: Model Context Protocol node.
        LOCAL_DB: Local DB
        SKILLS: Skills list
    """

    SOURCE_NODE = "source_node"
    AGENT = "agent"
    WORKFLOW = "workflow"
    TOOL = "tool"
    HUMAN_IN_THE_LOOP = "human_in_the_loop"
    SLEEP = "xpsleep-agent-delay"
    CUSTOM_AGENT = "custom_agent"
    STORAGE = "storage"
    CODING_AGENT = "coding_agent"
    MCP = "mcp"
    LOCAL_DB = "local_db"
    SKILLS = "skills"


class AgentGraphItemSubType(str, Enum):
    """
    Enumeration of agent graph item subtypes.

    Values:
        SDK: SDK-based implementation.
        TASK: Task-based implementation.
        ASSISTANT: Assistant-based implementation.
        WEBHOOK: Webhook-triggered implementation.
        OPERATION: Operation-based tool.
        CUSTOM_FUNCTION: Custom function tool.
        LOCAL_TOOL: Local tool implementation.
    """

    # Source node subtypes
    SDK = "sdk"
    TASK = "task"
    ASSISTANT = "assistant"
    WEBHOOK = "webhook"

    # Tool subtypes
    OPERATION = "operation"
    CUSTOM_FUNCTION = "custom_function"
    LOCAL_TOOL = "local_tool"


class AgentGraphItemAdvancedFilteringOption(BaseModel):
    """
    Model for advanced filtering options in agent graph items.

    Attributes:
        returnables (Optional[List[str]]): List of returnable fields.
        searchables (Optional[List[str]]): List of searchable fields.
        globally_enabled (Optional[bool]): Whether filtering is globally enabled.
    """

    returnables: Optional[List[str]] = None
    searchables: Optional[List[str]] = None
    globally_enabled: Optional[bool] = False


class AgentGraphItemSchema(BaseModel):
    """
    Model for defining input/output schemas for agent graph items.

    Attributes:
        input (Optional[dict]): Input schema definition.
        output (Optional[dict]): Output schema definition.
    """

    input: Optional[dict] = None
    output: Optional[dict] = None


class AgentHITLType(str, Enum):
    """
    Enumeration of Human-in-the-Loop integration types.

    Values:
        SLACK: Slack integration for human approval.
    """

    SLACK = "slack"


class AgentGraphItemHITLSettings(BaseModel):
    """
    Model for Human-in-the-Loop settings in agent graph items.

    Attributes:
        title (Optional[str]): Title for the HITL request.
        description (Optional[str]): Description of what requires approval.
        recipients (Optional[List[str]]): List of recipient IDs for approval requests.
        hitl_type (Optional[AgentHITLType]): Type of HITL integration.
        slack_app (Optional[str]): Slack app identifier for notifications.
        should_approve_with_current_user (Optional[bool]): Whether to auto-approve with current user.
    """

    title: Optional[str] = None
    description: Optional[str] = None
    recipients: Optional[List[str]] = None
    hitl_type: Optional[AgentHITLType] = None
    slack_app: Optional[str] = None
    should_approve_with_current_user: Optional[bool] = True


class AgentGraphItemA2ASettings(BaseModel):
    """
    Model for Agent-to-Agent communication settings.

    Attributes:
        url (Optional[str]): URL endpoint for A2A communication.
    """

    url: Optional[str] = None


class AgentGraphItemCodingAgentSettings(BaseModel):
    """
    Model for coding agent specific settings.

    Attributes:
        type (Optional[Literal["codex"]]): Type of coding agent, defaults to "codex".
    """

    type: Optional[Literal["codex"]] = "codex"


class AgentGraphItemSkillsSettings(BaseModel):
    enabled_skills: Optional[List[str]] = []


class AgentGraphItemSettings(BaseModel):
    """
    Comprehensive settings model for agent graph items.

    This model consolidates all possible settings for different types of
    agent graph items, including instructions, schemas, and specialized configurations.

    Attributes:
        instructions (Optional[str]): Specific instructions for this graph item.
        description (Optional[str]): Description of the graph item's purpose.
        schemas (Optional[AgentGraphItemSchema]): Input/output schemas.
        advanced_filtering_options (Optional[AgentGraphItemAdvancedFilteringOption]): Advanced filtering settings.
        hitl_options (Optional[AgentGraphItemHITLSettings]): Human-in-the-loop settings.
        a2a_options (Optional[AgentGraphItemA2ASettings]): Agent-to-agent communication settings.
        coding_agent_settings (Optional[AgentGraphItemCodingAgentSettings]): Coding agent specific settings.
        mcp_settings (Optional[MCPServerDetails]): Model Context Protocol settings.
        skills_settings (Optional[AgentGraphItemSkillsSettings]): Optional skills settings.
    """

    instructions: Optional[str] = None
    description: Optional[str] = None
    schemas: Optional[AgentGraphItemSchema] = None
    advanced_filtering_options: Optional[AgentGraphItemAdvancedFilteringOption] = None
    hitl_options: Optional[AgentGraphItemHITLSettings] = None
    a2a_options: Optional[AgentGraphItemA2ASettings] = None
    coding_agent_settings: Optional[AgentGraphItemCodingAgentSettings] = None
    mcp_settings: Optional[MCPServerDetails] = None
    skills_settings: Optional[AgentGraphItemSkillsSettings] = None


class AgentGraphItem(BaseModel):
    """
    Model representing a single item in an agent's execution graph.

    This model defines a node in the agent's execution graph, including its
    configuration, connections, and processing settings.

    Attributes:
        id (Optional[str]): Unique identifier for the graph item.
        item_id (str): Reference ID for the underlying item.
        name (Optional[str]): Human-readable name for the graph item.
        type (AgentGraphItemType): Type of the graph item.
        sub_type (Optional[AgentGraphItemSubType]): Subtype for more specific categorization.
        targets (List[str]): List of target graph item IDs for execution flow.
        settings (Optional[AgentGraphItemSettings]): Configuration settings for the item.
        is_first (Optional[bool]): Whether this is the first item in the execution graph.
    """

    id: Optional[str] = None
    item_id: str
    name: Optional[str] = None
    type: AgentGraphItemType
    sub_type: Optional[AgentGraphItemSubType] = None
    targets: List[str]
    settings: Optional[AgentGraphItemSettings] = None
    is_first: Optional[bool] = False


class LLMReasoningEffort(str, Enum):
    Low = "low"
    Medium = "medium"
    High = "high"
    XHigh = "xhigh"


class AIAgentConnectivityDetailsA2AAuthType(str, Enum):
    NoAuth = "none"
    ApiKey = "api_key"
    Basic = "basic"
    Bearer = "bearer"


class AIAgentConnectivityDetailsBase(XPanderSharedModel):
    custom_headers: Optional[Dict[str, str]] = {}
    auth_type: Optional[AIAgentConnectivityDetailsA2AAuthType] = (
        AIAgentConnectivityDetailsA2AAuthType.NoAuth
    )
    api_key_header_name: Optional[str] = "X-API-Key"
    auth_value: Optional[str] = None


class AIAgentConnectivityDetailsA2A(AIAgentConnectivityDetailsBase):
    agent_url: str


class AIAgentConnectivityDetailsCurl(AIAgentConnectivityDetailsBase):
    curl_command: str
    invoke_url: Optional[str] = None  # post analysis (auto populate by llm)
    method: Optional[str] = "POST"  # post analysis (auto populate by llm)
    prompt_field_name: Optional[str] = (
        ""  # post analysis (auto populate by llm) - CAN BE SET BY THE USER
    )
    files_field_name: Optional[str] = (
        ""  # post analysis (auto populate by llm) - CAN BE SET BY THE USER
    )
    task_id_field_name: Optional[str] = (
        ""  # post analysis (auto populate by llm) - CAN BE SET BY THE USER
    )


class AgentType(str, Enum):
    """
    Enumeration of agent types.

    Values:
        Manager: Agent that manages and coordinates other agents.
        Regular: Standard agent for individual task execution.
        A2A: Agent that is used via A2A protocol.
        Curl: Custom Agent that is used via curl.
        Orchestration: marks the agent as an Orchestration object.
    """

    Manager = "manager"
    Regular = "regular"
    A2A = "a2a"
    Curl = "curl"
    Orchestration = "orchestration"


@dataclass
class ConnectionURIResponse:
    """
    Data class for database connection URI responses.

    Attributes:
        uri (str): The database connection URI string.
    """

    uri: str


class StreamingSpecResponse(BaseModel):
    """
    Response model for the streaming spec check.

    Attributes:
        url (Optional[str]): The streaming URL for the agent, or None if not available.
        api_key (Optional[str]): API key to authenticate with the container's /invoke endpoint.
    """

    url: Optional[str] = None
    api_key: Optional[str] = None


class DatabaseConnectionString(BaseModel):
    """
    Model for database connection string configuration.

    Attributes:
        id (str): Unique identifier for the connection.
        name (str): Human-readable name for the connection.
        organization_id (Optional[str]): Organization ID associated with the connection.
        connection_uri (Optional[ConnectionURIResponse]): Connection URI details.
    """

    id: str
    name: str
    organization_id: Optional[str] = None
    connection_uri: Optional[ConnectionURIResponse] = None


class AgentOutput(BaseModel):
    """
    Model for agent output configuration and formatting.

    Attributes:
        output_schema (Optional[Type[BaseModel]]): Pydantic model for structured output validation.
        is_markdown (Optional[bool]): Whether output should be formatted as Markdown.
        use_json_mode (Optional[bool]): Whether to use JSON mode for output formatting.
    """

    output_schema: Optional[Type[BaseModel]] = None
    is_markdown: Optional[bool] = False
    use_json_mode: Optional[bool] = False


class TaskLevelStrategies(XPanderSharedModel):
    """
    Configuration object for task-level execution strategies.

    This model groups optional strategy configurations that control how a task is
    executed and managed over time, including retries, iterative execution,
    stopping conditions, and daily run limits.

    Attributes:
        retry_strategy:
            Optional retry policy configuration that defines how the task should
            behave when execution fails (e.g., max attempts, backoff rules).

        iterative_strategy:
            Optional iterative execution configuration for tasks that may run in
            repeated cycles/steps until completion or a stop condition is met.

        stop_strategy:
            Optional stopping policy configuration that defines when the task
            should stop running (e.g., timeout, max iterations, success criteria).

        max_runs_per_day:
            Optional limit on how many times the task is allowed to run within a
            24-hour period. If not set, no explicit daily limit is enforced.

        agentic_context_enabled:
            if agentic memory is enabled and accesible to the executor.

        slackbot_formatting_instructions:
            Optional SlackBot formatting instructions
    """

    retry_strategy: Optional[OrchestrationRetryStrategy] = None
    iterative_strategy: Optional[OrchestrationIterativeStrategy] = None
    stop_strategy: Optional[OrchestrationStopStrategy] = None
    max_runs_per_day: Optional[int] = None
    agentic_context_enabled: Optional[bool] = False
    duplication_prevention: Optional[DuplicationPreventionSettings] = None
    slackbot_formatting_instructions: Optional[str] = None
