"""Artifact Hosting SDK V2 models.

This module exports all model classes for the Artifact Hosting SDK.
"""

from novita_sandbox.artifact_hosting.models.enums import (
    CANCELLABLE_STATES,
    DeploymentStatus,
    FAILURE_STATES,
    ProjectStatus,
    STATUS_NAME_TO_VALUE,
    STATUS_VALUE_TO_NAME,
    SUCCESSFUL_STATES,
    TERMINAL_STATES,
    is_cancellable,
    is_failure,
    is_successful,
    is_terminal,
)
from novita_sandbox.artifact_hosting.models.nested import (
    AccountInfo,
    ArtifactsSource,
    DatabaseInfo,
    DeploymentMetadata,
    Endpoint,
    EndpointConfig,
    ReplicaSpec,
)

__all__ = [
    # Enums
    "DeploymentStatus",
    "ProjectStatus",
    # Status sets
    "TERMINAL_STATES",
    "SUCCESSFUL_STATES",
    "FAILURE_STATES",
    "CANCELLABLE_STATES",
    # Status helper functions
    "is_terminal",
    "is_successful",
    "is_failure",
    "is_cancellable",
    # Status mappings
    "STATUS_NAME_TO_VALUE",
    "STATUS_VALUE_TO_NAME",
    # Nested objects
    "AccountInfo",
    "Endpoint",
    "EndpointConfig",
    "ArtifactsSource",
    "DeploymentMetadata",
    "ReplicaSpec",
    "DatabaseInfo",
]
