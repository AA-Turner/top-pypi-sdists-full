"""Artifact Hosting Python SDK V2.

This SDK provides a Python interface for the Artifact Hosting service,
allowing users to deploy AI-generated code to production environments.

Main Components:
    - DeploymentClient: Main entry point for SDK operations
    - Project: Represents a deployable application project
    - Deployment: Represents a deployment operation
    - DeploymentStatus: Deployment status enum
    
    Example:
    >>> from novita_sandbox.artifact_hosting import DeploymentClient
        >>> 
    >>> # Initialize client (reads API key from NOVITA_API_KEY env var)
    >>> client = DeploymentClient()
    >>> 
    >>> # Create a project
    >>> project = client.create_project(name="my-app")
    >>> 
    >>> # Deploy from a Sandbox
    >>> deployment = project.deploy(
    ...     sandbox_id="sbx-123",
    ...     arti_dir="/app/source",
    ... )
    >>> 
    >>> # Access the deployed URL
    >>> print(project.url)
"""

from novita_sandbox.artifact_hosting.client import DeploymentClient
from novita_sandbox.artifact_hosting.exceptions import (
    CancellationError,
    DeploymentError,
    DeploymentNotFoundError,
    ProjectNotFoundError,
    QuotaExceededError,
    RollbackError,
    TimeoutError,
    ValidationError,
)
from novita_sandbox.artifact_hosting.models import (
    CANCELLABLE_STATES,
    DeploymentStatus,
    SUCCESSFUL_STATES,
    TERMINAL_STATES,
    is_cancellable,
    is_successful,
    is_terminal,
    AccountInfo,
    ArtifactsSource,
    DatabaseInfo,
    DeploymentMetadata,
    Endpoint,
    EndpointConfig,
    ReplicaSpec,
)
from novita_sandbox.artifact_hosting.models.deployment import Deployment
from novita_sandbox.artifact_hosting.models.log_entry import LogEntry
from novita_sandbox.artifact_hosting.models.project import Project

__all__ = [
    # Main client
    "DeploymentClient",
    # Models
    "Project",
    "Deployment",
    "LogEntry",
    # Enums and status helpers
    "DeploymentStatus",
    "TERMINAL_STATES",
    "SUCCESSFUL_STATES",
    "CANCELLABLE_STATES",
    "is_terminal",
    "is_successful",
    "is_cancellable",
    # Nested objects
    "AccountInfo",
    "Endpoint",
    "EndpointConfig",
    "ArtifactsSource",
    "DeploymentMetadata",
    "ReplicaSpec",
    "DatabaseInfo",
    # Exceptions
    "DeploymentError",
    "ProjectNotFoundError",
    "DeploymentNotFoundError",
    "RollbackError",
    "QuotaExceededError",
    "ValidationError",
    "CancellationError",
    "TimeoutError",
]

__version__ = "2.0.0"
