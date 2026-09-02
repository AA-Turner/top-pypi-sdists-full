"""
Agent Runtime Client Exception Definitions

Defines client-specific exception types for handling various error conditions
"""

from typing import Optional


class AgentClientError(Exception):
    """Base client exception"""
    
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class AuthenticationError(AgentClientError):
    """Authentication error"""
    pass


class TemplateNotFoundError(AgentClientError):
    """Template not found error"""
    pass


class SandboxCreationError(AgentClientError):
    """Sandbox creation error"""
    pass


class SessionNotFoundError(AgentClientError):
    """Session not found error"""
    pass


class InvocationError(AgentClientError):
    """Invocation error"""
    pass


class NetworkError(AgentClientError):
    """Network error"""
    pass


class RateLimitError(AgentClientError):
    """Rate limit error"""
    pass


class QuotaExceededError(AgentClientError):
    """Quota exceeded error"""
    pass


class SandboxOperationError(AgentClientError):
    """Sandbox operation error (pause, resume, restart, etc.)"""
    pass


# === AWS Agentcore Compatible Exceptions ===

class ValidationException(AgentClientError):
    """Request validation failed (AWS Agentcore compatible)"""
    pass


class ResourceNotFoundException(AgentClientError):
    """Resource not found (AWS Agentcore compatible)"""
    pass


class AccessDeniedException(AgentClientError):
    """Access denied (AWS Agentcore compatible)"""
    pass


class ThrottlingException(AgentClientError):
    """Request was throttled (AWS Agentcore compatible)"""
    pass


class InternalServerError(AgentClientError):
    """Internal server error (AWS Agentcore compatible)"""
    pass


class ServiceUnavailableException(AgentClientError):
    """Service temporarily unavailable (AWS Agentcore compatible)"""
    pass


class ConflictException(AgentClientError):
    """Request conflicts with current resource state (AWS Agentcore compatible)"""
    pass