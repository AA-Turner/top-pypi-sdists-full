# Novita Agent Runtime SDK - Exception Definitions
# Copyright (c) 2024 Novita
# Licensed under the MIT License

"""Exception classes for Novita Agent Runtime."""

from typing import Optional, Any, Dict


class NovitaAgentRuntimeError(Exception):
    """Base exception for all Novita Agent Runtime errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.details = details or {}


class RuntimeConfigError(NovitaAgentRuntimeError):
    """Raised when there's a configuration error in the runtime."""
    pass


class RuntimeStartupError(NovitaAgentRuntimeError):
    """Raised when the runtime fails to start."""
    pass


class EntrypointNotFoundError(NovitaAgentRuntimeError):
    """Raised when the entrypoint function is not registered."""
    pass


class InvocationTimeoutError(NovitaAgentRuntimeError):
    """Raised when agent invocation times out."""
    pass


class InvocationError(NovitaAgentRuntimeError):
    """Raised when agent invocation fails."""
    pass


class ContextNotFoundError(NovitaAgentRuntimeError):
    """Raised when request context is not available."""
    pass


class MiddlewareError(NovitaAgentRuntimeError):
    """Raised when middleware execution fails."""
    pass


class ValidationError(NovitaAgentRuntimeError):
    """Raised when request validation fails."""
    pass
