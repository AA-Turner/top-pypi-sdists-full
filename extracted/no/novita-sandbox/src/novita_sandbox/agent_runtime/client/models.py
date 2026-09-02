"""
Agent Runtime Client Data Models

Defines data models used by the client
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

# Import shared PingResponse model
from ..runtime.models import PingResponse, PingStatus


class SessionStatus(str, Enum):
    """Session status"""
    ACTIVE = "active"      # Running, can process requests
    PAUSED = "paused"      # Paused, retains state but does not process requests
    INACTIVE = "inactive"  # Inactive state
    CLOSED = "closed"      # Closed, resources released
    ERROR = "error"        # Error state


class AgentTemplate(BaseModel):
    """Agent template information"""
    template_id: str
    name: str
    version: str
    description: Optional[str] = None
    author: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    status: str
    
    # Agent metadata (core field)
    metadata: Dict[str, str] = Field(default_factory=dict)
    """
    Agent metadata, contains complete AgentConfig data structure, consistent with CLI tool configuration file format.
    
    Typical structure example (following Kubernetes-style YAML configuration format):
    {
      "agent": {
        "apiVersion": "v1",
        "kind": "Agent",
        "metadata": {
          "name": "string",              // Agent name
          "version": "string",           // Agent version
          "author": "string",            // Author email (required)
          "description": "string",       // Agent description
          "created": "string"            // Creation time (ISO 8601 format)
        },
        "spec": {
          "entrypoint": "string",        // Python entry file, e.g. "agent.py" (must be .py file)
          "runtime": {
            "timeout": "number",         // Startup timeout in seconds, converted to readyCmd timeout parameter (1-3600)
            "memory_limit": "string",    // Memory limit, converted to memoryMb (supports formats like "512Mi", "1Gi")
            "cpu_limit": "string"        // CPU limit, converted to cpuCount (supports formats like "1", "1000m")
          },
          "sandbox": {
            "template_id": "string"      // Template ID after deployment
          }
        },
        // Status fields - used to track deployment and build status (maintained by system, users should not modify manually)
        "status": {
          "phase": "string",            // Current deployment phase
          "template_id": "string",      // Actual template ID after successful build (for subsequent updates)
          "last_deployed": "string",    // Last deployment time
          "build_id": "string"          // Unique identifier for deployment
        }
      }
    }
    """
    
    # Extended fields
    size: Optional[int] = None  # Template size (bytes)
    build_time: Optional[float] = None  # Build time (seconds)
    dependencies: List[str] = Field(default_factory=list)
    runtime_info: Optional[Dict[str, Any]] = None


class RuntimeConfig(BaseModel):
    """Runtime configuration (AWS Agentcore compatible)"""
    timeout_seconds: int = Field(default=300, alias="timeoutSeconds")
    memory_limit: Optional[str] = Field(default=None, alias="memoryLimit")  # e.g. "512Mi", "1Gi"
    cpu_limit: Optional[str] = Field(default=None, alias="cpuLimit")     # e.g. "500m", "1"
    env_vars: Optional[Dict[str, str]] = Field(default_factory=dict, alias="envVars")
    volumes: List[Dict[str, str]] = Field(default_factory=list)
    ports: List[int] = Field(default_factory=lambda: [8080])
    startup_cmd: Optional[str] = Field(default=None, alias="startupCmd")
    
    class Config:
        validate_by_name = True


# Backward compatibility alias
SandboxConfig = RuntimeConfig


class ClientConfig(BaseModel):
    """Client configuration (AWS Agentcore compatible)"""
    timeout: int = 300  # Simplified - removed base_url for AWS compatibility
    max_retries: int = 3
    retry_delay: float = 1.0
    
    # Connection pool configuration
    max_connections: int = 100
    max_keepalive_connections: int = 20
    keepalive_expiry: float = 30.0


class InvocationResponse(BaseModel):
    """Invocation response model (for reference only)
    
    NOTE: This model is NOT enforced by the client.
    The actual response format depends on the server implementation.
    
    This model is kept for documentation and type hints.
    """
    result: Any
    status: str = "success"
    duration: float
    
    # AWS compatible fields
    agent_id: Optional[str] = Field(default=None, alias="agentId")
    runtime_session_id: Optional[str] = Field(default=None, alias="runtimeSessionId")
    
    # Metadata
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_type: Optional[str] = Field(default=None, alias="errorType")
    
    # Performance information
    processing_time: Optional[float] = Field(default=None, alias="processingTime")
    queue_time: Optional[float] = Field(default=None, alias="queueTime")
    
    # Usage statistics
    tokens_used: Optional[int] = Field(default=None, alias="tokensUsed")
    cost: Optional[float] = None
    
    # Multimodal response support
    output_files: Optional[List[Dict[str, Any]]] = Field(default=None, alias="outputFiles")
    
    # AWS compatible properties
    @property
    def agentId(self) -> Optional[str]:
        """Agent ID (camelCase for AWS compatibility)"""
        return self.agent_id
    
    @property
    def runtimeSessionId(self) -> Optional[str]:
        """Runtime Session ID (camelCase for AWS compatibility)"""
        return self.runtime_session_id
    
    class Config:
        validate_by_name = True


# === AWS Agentcore Compatible Models ===

class AgentRuntimeRequest(BaseModel):
    """AWS Agentcore compatible request model"""
    agent_id: str = Field(alias="agentId")
    payload: bytes
    runtime_session_id: Optional[str] = Field(default=None, alias="runtimeSessionId")
    timeout: Optional[int] = None
    
    class Config:
        validate_by_name = True


class AgentRuntimeResponse(BaseModel):
    """AWS Agentcore compatible response model"""
    response: Any
    runtime_session_id: str = Field(alias="runtimeSessionId")
    status: str = "success"
    agent_id: str = Field(alias="agentId")
    
    class Config:
        validate_by_name = True


class StreamingChunk(BaseModel):
    """Streaming response chunk model"""
    chunk: Any
    runtime_session_id: str = Field(alias="runtimeSessionId")
    agent_id: str = Field(alias="agentId")
    sequence_number: Optional[int] = Field(default=None, alias="sequenceNumber")
    is_final: bool = Field(default=False, alias="isFinal")
    
    class Config:
        validate_by_name = True


class MultimodalContent(BaseModel):
    """Multimodal content support"""
    content_type: str = Field(alias="contentType")
    data: bytes
    filename: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        validate_by_name = True


# === Error Response Models (AWS Compatible) ===

class ErrorResponse(BaseModel):
    """AWS Agentcore compatible error response"""
    error_code: str = Field(alias="errorCode")
    message: str
    request_id: Optional[str] = Field(default=None, alias="requestId")
    details: Optional[Dict[str, Any]] = None
    
    class Config:
        validate_by_name = True


class ValidationError(BaseModel):
    """Validation error details"""
    field: str
    message: str
    code: str

