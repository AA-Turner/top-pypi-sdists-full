"""Core data models for IATP."""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, HttpUrl
from enum import Enum


class MCPServerType(str, Enum):
    """Types of MCP servers."""
    STREAMABLE_HTTP = "streamable-http"


class MCPServer(BaseModel):
    """MCP Server specification."""
    id: Optional[str] = Field(default=None, description="Unique identifier")
    name: str = Field(..., description="Name of the MCP server")
    url: str = Field(..., description="URL or path to connect to the MCP server")
    server_type: MCPServerType = Field(default=MCPServerType.STREAMABLE_HTTP, description="Type of MCP server connection")
    description: str = Field(..., description="Description of what the server enables")
    capabilities: List[str] = Field(default_factory=list, description="List of capabilities/APIs")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class ConfigDict:
        json_encoders = {HttpUrl: str}


class AgentSkill(BaseModel):
    """IATP Agent skill definition."""
    id: str = Field(..., description="Unique skill identifier")
    name: str = Field(..., description="Human-readable skill name")
    description: str = Field(..., description="Detailed skill description")
    examples: List[str] = Field(default_factory=list, description="Example usage patterns")
    input_modes: List[str] = Field(default_factory=list, description="Supported input modes")
    output_modes: List[str] = Field(default_factory=list, description="Supported output modes")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")


class AgentCapabilities(BaseModel):
    """IATP Agent capabilities."""
    streaming: bool = Field(default=False, description="Supports SSE streaming")
    push_notifications: bool = Field(default=False, description="Supports push notifications")
    state_transition_history: bool = Field(default=False, description="Maintains state history")
    custom_features: Dict[str, Any] = Field(default_factory=dict, description="Custom capabilities")


class AgentCard(BaseModel):
    """IATP Agent card for discovery and initialization."""
    name: str = Field(..., description="Agent name")
    description: str = Field(..., description="Agent description")
    version: str = Field(..., description="Agent version")
    skills: List[AgentSkill] = Field(default_factory=list, description="Available skills")
    capabilities: AgentCapabilities = Field(default_factory=AgentCapabilities, description="Agent capabilities")
    default_input_modes: List[str] = Field(default_factory=list, description="Default input modes")
    default_output_modes: List[str] = Field(default_factory=list, description="Default output modes")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class IATPEndpoints(BaseModel):
    """IATP server endpoints configuration.
    
    Note: The A2A protocol only defines a minimal set of endpoints:
    - Root path (/) for JSON-RPC
    - /.well-known/agent.json for agent card
    - /a2a/tasks/* for SSE subscriptions (if streaming is supported)
    
    Health and info endpoints are NOT part of the A2A protocol standard.
    """
    base_url: str = Field(..., description="Base URL of the IATP server")
    iatp_endpoint: str = Field(..., description="Main IATP JSON-RPC endpoint (usually at root path)")
    streaming_endpoint: Optional[str] = Field(None, description="SSE streaming endpoint (same as iatp_endpoint when supported)")
    health_endpoint: Optional[str] = Field(None, description="Health check endpoint (not part of A2A protocol)")
    info_endpoint: Optional[str] = Field(None, description="Agent info endpoint (not part of A2A protocol)")
    agent_card_endpoint: str = Field(..., description="Agent card endpoint (.well-known/agent.json)")
    subscribe_endpoint: Optional[str] = Field(None, description="SSE subscription endpoint (/a2a/tasks/subscribe)")
    resubscribe_endpoint: Optional[str] = Field(None, description="SSE resubscription endpoint (/a2a/tasks/resubscribe)")


class UtilityAgentStatus(str, Enum):
    """Status of a utility agent."""
    GENERATED = "generated"
    DEPLOYING = "deploying"
    DEPLOYED = "deployed"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"


#this is the model for internal management of utility agents by their creator and traia protocol (should be persisted into db)
class UtilityAgent(BaseModel):
    """Utility Agent configuration and metadata."""
    id: str = Field(..., description="Unique identifier for the agent")
    name: str = Field(..., description="Name of the utility agent")
    description: str = Field(..., description="Description of the agent's purpose")
    mcp_server_id: str = Field(..., description="ID of the associated MCP server")
    
    # IATP specific fields
    agent_card: Optional[AgentCard] = Field(None, description="IATP agent card for discovery")
    endpoints: Optional[IATPEndpoints] = Field(None, description="IATP endpoints configuration")
    
    capabilities: List[str] = Field(default_factory=list, description="List of exposed capabilities")
    status: UtilityAgentStatus = Field(default=UtilityAgentStatus.GENERATED)
    code_path: Optional[str] = Field(None, description="Path to generated code")
    docker_image: Optional[str] = Field(None, description="Docker image name when built")
    github_repo: Optional[str] = Field(None, description="GitHub repository URL")
    cloud_run_url: Optional[str] = Field(None, description="Cloud Run deployment URL")
    
    # X402 payment configuration
    contract_address: Optional[str] = Field(None, description="On-chain utility agent contract address")
    operator_address: Optional[str] = Field(None, description="Operator address for signing attestations")
    d402_enabled: bool = Field(default=False, description="Whether d402 payments are enabled")
    d402_config: Optional[Dict[str, Any]] = Field(None, description="X402 payment configuration")
    
    # Search and discovery
    search_text: Optional[str] = Field(None, description="Concatenated searchable text")
    tags: List[str] = Field(default_factory=list, description="Tags for search and categorization")
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class ConfigDict:
        json_encoders = {HttpUrl: str, datetime: lambda v: v.isoformat()}


#this is a model for registry discovery that will be used by the mongodb indexes
class UtilityAgentRegistryEntry(BaseModel):
    """Registry entry for a deployed utility agent."""
    agent_id: str = Field(..., description="ID of the utility agent")
    name: str = Field(..., description="Name for discovery")
    description: str = Field(..., description="Description for search")
    
    # MCP server reference
    mcp_server_id: Optional[str] = Field(None, description="ID of the MCP server this agent wraps")
    
    # Base URL for the agent - all endpoints are derived from this
    base_url: Optional[str] = Field(None, description="Base URL of the deployed agent")
    
    # Enhanced IATP discovery fields
    agent_card: Optional[AgentCard] = Field(None, description="IATP agent card")
    endpoints: Optional[IATPEndpoints] = Field(None, description="IATP endpoints")
    
    capabilities: List[str] = Field(..., description="List of capabilities")
    skills: List[AgentSkill] = Field(default_factory=list, description="Detailed skills from agent card")
    tags: List[str] = Field(default_factory=list, description="Tags for search")
    
    # X402 payment information
    contract_address: Optional[str] = Field(None, description="On-chain utility agent contract address")
    d402_enabled: bool = Field(default=False, description="Whether d402 payments are enabled")
    d402_payment_info: Optional[Dict[str, Any]] = Field(None, description="X402 payment information")
    
    # Search optimization
    search_text: Optional[str] = Field(None, description="Full text for search")
    
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    registered_at: datetime = Field(default_factory=datetime.utcnow)
    last_health_check: Optional[datetime] = Field(None, description="Last successful health check")
    is_active: bool = Field(default=True, description="Whether the agent is active")
    
    class ConfigDict:
        json_encoders = {HttpUrl: str, datetime: lambda v: v.isoformat()}


class IATPRequest(BaseModel):
    """IATP protocol request."""
    action: str = Field(..., description="Action to perform")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Action parameters")
    context: Dict[str, Any] = Field(default_factory=dict, description="Request context")


class IATPResponse(BaseModel):
    """IATP protocol response."""
    result: Any = Field(..., description="Result of the action")
    status: str = Field(..., description="Status of the response")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Response metadata") 