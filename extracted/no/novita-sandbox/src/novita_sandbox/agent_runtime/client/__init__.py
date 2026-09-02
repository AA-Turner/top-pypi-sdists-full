"""
Novita Agent Runtime Client Module

Provides client functionality for AI Agents, targeted at backend developers
"""

# Main client class
from .client import AgentRuntimeClient

# Session management
from .session import SandboxSession

# Authentication and template management
from .auth import AuthManager
from .template import TemplateManager

# Data models
from .models import (
    AgentTemplate,
    ClientConfig,
    InvocationResponse,
    RuntimeConfig,  # New AWS-compatible name
    SandboxConfig,  # Backward compatibility alias
    SessionStatus,
    # PingResponse imported from runtime module
    PingResponse,
    PingStatus,
    # AWS Agentcore compatible models
    AgentRuntimeRequest,
    AgentRuntimeResponse,
    StreamingChunk,
    MultimodalContent,
    ErrorResponse,
    ValidationError
)

# Exception classes
from .exceptions import (
    AgentClientError,
    AuthenticationError,
    InvocationError,
    NetworkError,
    QuotaExceededError,
    RateLimitError,
    SandboxCreationError,
    SandboxOperationError,
    SessionNotFoundError,
    TemplateNotFoundError,
    # AWS Agentcore compatible exceptions
    ValidationException,
    ResourceNotFoundException,
    AccessDeniedException,
    ThrottlingException,
    InternalServerError,
    ServiceUnavailableException,
    ConflictException
)

# Agent ID utilities
from .agent_id_utils import (
    extract_agent_id_from_arn,
    extract_template_id_from_agent_id,
    extract_agent_name_from_agent_id,
    normalize_agent_name,
    create_agent_id,
    parse_agent_id
)

__version__ = "1.0.0"

__all__ = [
    # Core client classes
    "AgentRuntimeClient",
    "SandboxSession",
    "AuthManager", 
    "TemplateManager",
    
    # Data models
    "AgentTemplate",
    "ClientConfig",
    "InvocationResponse",
    "PingResponse",
    "PingStatus",
    "RuntimeConfig",  # New AWS-compatible name
    "SandboxConfig",  # Backward compatibility
    "SessionStatus",
    # AWS Agentcore compatible models
    "AgentRuntimeRequest",
    "AgentRuntimeResponse",
    "StreamingChunk",
    "MultimodalContent",
    "ErrorResponse",
    "ValidationError",
    
    # Exception classes
    "AgentClientError",
    "AuthenticationError",
    "InvocationError",
    "NetworkError",
    "QuotaExceededError",
    "RateLimitError",
    "SandboxCreationError",
    "SandboxOperationError",
    "SessionNotFoundError",
    "TemplateNotFoundError",
    # AWS Agentcore compatible exceptions
    "ValidationException",
    "ResourceNotFoundException",
    "AccessDeniedException",
    "ThrottlingException",
    "InternalServerError",
    "ServiceUnavailableException",
    "ConflictException",
    
    # Agent ID utilities
    "extract_agent_id_from_arn",
    "extract_template_id_from_agent_id",
    "extract_agent_name_from_agent_id",
    "normalize_agent_name",
    "create_agent_id",
    "parse_agent_id",
]