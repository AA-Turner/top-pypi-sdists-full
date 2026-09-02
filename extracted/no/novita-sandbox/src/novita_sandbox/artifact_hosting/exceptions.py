"""Exception classes for Artifact Hosting SDK V2.

Exception hierarchy:
    DeploymentError (base)
    ├── ProjectNotFoundError
    ├── DeploymentNotFoundError
    ├── RollbackError
    ├── QuotaExceededError
    ├── ValidationError
    └── CancellationError
"""

from typing import Optional


class DeploymentError(Exception):
    """Base exception for Artifact Hosting SDK.
    
    All SDK-specific exceptions inherit from this class,
    allowing users to catch all SDK errors with a single except clause.
    
    Args:
        message: Human-readable error message.
        code: Optional error code from backend API.
    """
    
    def __init__(self, message: str, code: Optional[str] = None):
        self.code = code
        super().__init__(message)


class ProjectNotFoundError(DeploymentError):
    """Project not found.
    
    Raised when attempting to access a project that doesn't exist
    or the user doesn't have access to.
    """
    pass


class DeploymentNotFoundError(DeploymentError):
    """Deployment not found.
    
    Raised when attempting to access a deployment that doesn't exist.
    """
    pass


class RollbackError(DeploymentError):
    """Rollback operation failed.
    
    Raised when a rollback cannot be performed, such as when
    the target deployment is not in a valid state.
    """
    pass


class QuotaExceededError(DeploymentError):
    """Account quota exceeded.
    
    Raised when the account has reached its resource limits,
    such as maximum number of projects or deployments.
    """
    pass


class ValidationError(DeploymentError):
    """Validation error.
    
    Raised when input validation fails, such as invalid project name
    or environment variable format.
    """
    pass


class CancellationError(DeploymentError):
    """Cancellation operation failed.
    
    Raised when a deployment cannot be cancelled, such as when
    it's already in a terminal state.
    """
    pass


class TimeoutError(DeploymentError):
    """Operation timed out.
    
    Raised when an operation exceeds the configured timeout,
    such as waiting for deployment to complete.
    """
    pass
