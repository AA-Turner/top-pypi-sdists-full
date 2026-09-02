"""Status enums with integer mapping for API compatibility."""

from enum import IntEnum
from typing import Dict, Set


class ProjectStatus(IntEnum):
    """Status of a project (matching backend API format).
    
    Values are integers matching Backend API format.
    Backend returns status as string like "PROJECT_STATUS_ACTIVE",
    SDK handles both integer and string formats.
    """
    
    UNSPECIFIED = 0     # Unspecified/unknown status
    ACTIVE = 1          # Project is active and can accept deployments
    INACTIVE = 2        # Project is inactive (no running deployments)
    DEPLOYING = 3       # Deployment in progress
    ROLLING_BACK = 4    # Rollback in progress
    ERROR = 5           # Project is in error state
    
    @classmethod
    def from_string(cls, value: str) -> "ProjectStatus":
        """Convert string status to enum.
        
        Handles both formats:
        - "PROJECT_STATUS_ACTIVE" (backend format)
        - "ACTIVE" (short format)
        
        Args:
            value: Status string.
        
        Returns:
            ProjectStatus enum value.
        
        Raises:
            ValueError: If value is not a valid status.
        """
        # Remove "PROJECT_STATUS_" prefix if present
        status_str = value.upper()
        if status_str.startswith("PROJECT_STATUS_"):
            status_str = status_str[len("PROJECT_STATUS_"):]
        
        try:
            return cls[status_str]
        except KeyError:
            raise ValueError(f"Invalid project status: {value}")
    
    def to_string(self) -> str:
        """Convert enum to string representation.
        
        Returns:
            Lowercase string (e.g., "active", "deploying").
        """
        return self.name.lower()
    
    def to_api_string(self) -> str:
        """Convert enum to backend API format string.
        
        Returns:
            Full backend format (e.g., "PROJECT_STATUS_ACTIVE").
        """
        return f"PROJECT_STATUS_{self.name}"


class DeploymentStatus(IntEnum):
    """Status of a deployment (matching backend API format).
    
    Values are integers matching Backend API format.
    Backend returns status as string like "DEPLOYMENT_STATUS_RUNNING",
    SDK handles both integer and string formats.
    
    State transitions:
        QUEUED → BUILDING → DEPLOYING → RUNNING
                    ↓           ↓
               BUILD_FAILED   DEPLOY_FAILED
                              
        RUNNING → IDLE (no traffic)
        RUNNING → INACTIVE (stopped)
        QUEUED/BUILDING/DEPLOYING → CANCELLED (cancelled by user)
    """
    
    UNSPECIFIED = 0     # Unspecified/unknown status
    QUEUED = 1          # Waiting in queue
    BUILDING = 2        # Build in progress
    BUILD_FAILED = 3    # Build failed
    DEPLOYING = 4       # Deployment in progress
    DEPLOY_FAILED = 5   # Deployment failed
    RUNNING = 6         # Running successfully
    IDLE = 7            # Idle (no traffic, scaled down)
    INACTIVE = 8        # Inactive (stopped)
    CANCELLED = 9       # Cancelled by user
    
    @classmethod
    def from_string(cls, value: str) -> "DeploymentStatus":
        """Convert string status to enum.
        
        Handles both formats:
        - "DEPLOYMENT_STATUS_RUNNING" (backend format)
        - "RUNNING" (short format)
        
        Args:
            value: Status string.
        
        Returns:
            DeploymentStatus enum value.
        
        Raises:
            ValueError: If value is not a valid status.
        """
        # Remove "DEPLOYMENT_STATUS_" prefix if present
        status_str = value.upper()
        if status_str.startswith("DEPLOYMENT_STATUS_"):
            status_str = status_str[len("DEPLOYMENT_STATUS_"):]
        
        try:
            return cls[status_str]
        except KeyError:
            raise ValueError(f"Invalid deployment status: {value}")
    
    def to_string(self) -> str:
        """Convert enum to string representation.
        
        Returns:
            Lowercase string (e.g., "running", "building").
        """
        return self.name.lower()
    
    def to_api_string(self) -> str:
        """Convert enum to backend API format string.
        
        Returns:
            Full backend format (e.g., "DEPLOYMENT_STATUS_RUNNING").
        """
        return f"DEPLOYMENT_STATUS_{self.name}"


# Status name to value mapping (for string -> int conversion)
STATUS_NAME_TO_VALUE: Dict[str, int] = {
    status.name: status.value for status in DeploymentStatus
}

# Status value to name mapping (for int -> string conversion)
STATUS_VALUE_TO_NAME: Dict[int, str] = {
    status.value: status.name for status in DeploymentStatus
}


# Terminal states - deployment is complete (success or failure)
TERMINAL_STATES: Set[DeploymentStatus] = {
    DeploymentStatus.BUILD_FAILED,
    DeploymentStatus.DEPLOY_FAILED,
    DeploymentStatus.CANCELLED,
    DeploymentStatus.RUNNING,
    DeploymentStatus.IDLE,
    DeploymentStatus.INACTIVE,
}

# Successful states - deployment completed successfully
SUCCESSFUL_STATES: Set[DeploymentStatus] = {
    DeploymentStatus.RUNNING,
    DeploymentStatus.IDLE,
}

# Failure states - deployment failed
FAILURE_STATES: Set[DeploymentStatus] = {
    DeploymentStatus.BUILD_FAILED,
    DeploymentStatus.DEPLOY_FAILED,
}

# Cancellable states - deployment can be cancelled
CANCELLABLE_STATES: Set[DeploymentStatus] = {
    DeploymentStatus.QUEUED,
    DeploymentStatus.BUILDING,
    DeploymentStatus.DEPLOYING,
}


def is_terminal(status: DeploymentStatus) -> bool:
    """Check if status is terminal (deployment complete).
    
    Args:
        status: DeploymentStatus to check.
    
    Returns:
        True if terminal, False otherwise.
    """
    return status in TERMINAL_STATES


def is_successful(status: DeploymentStatus) -> bool:
    """Check if status indicates successful deployment.
    
    Args:
        status: DeploymentStatus to check.
    
    Returns:
        True if successful, False otherwise.
    """
    return status in SUCCESSFUL_STATES


def is_failure(status: DeploymentStatus) -> bool:
    """Check if status indicates failed deployment.
    
    Args:
        status: DeploymentStatus to check.
    
    Returns:
        True if failed, False otherwise.
    """
    return status in FAILURE_STATES


def is_cancellable(status: DeploymentStatus) -> bool:
    """Check if deployment can be cancelled.
    
    Args:
        status: DeploymentStatus to check.
    
    Returns:
        True if cancellable, False otherwise.
    """
    return status in CANCELLABLE_STATES
