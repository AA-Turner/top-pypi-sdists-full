"""Deployment model for Artifact Hosting SDK V2.

This module implements the Deployment class according to the V2 design.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Iterator, Optional

from novita_sandbox.artifact_hosting.models.enums import (
    CANCELLABLE_STATES,
    DeploymentStatus,
    SUCCESSFUL_STATES,
    TERMINAL_STATES,
)
from novita_sandbox.artifact_hosting.models.nested import (
    AccountInfo,
    ArtifactsSource,
    DeploymentMetadata,
)

logger = logging.getLogger("novita_sandbox.artifact_hosting")

if TYPE_CHECKING:
    from novita_sandbox.artifact_hosting.client import DeploymentClient
    from novita_sandbox.artifact_hosting.models.log_entry import LogEntry
    from novita_sandbox.artifact_hosting.models.project import Project


@dataclass
class Deployment:
    """Represents a deployment operation.
    
    A deployment is a snapshot of code deployed to the cluster.
    
    Attributes:
        id: Unique deployment identifier (maps from deploymentId).
        project_id: Parent project identifier.
        status: Current deployment status (DeploymentStatus enum).
        message: Optional deployment message/description.
        error_message: Error message if deployment failed.
        account_info: Account information object.
        artifacts_source: Source of deployment artifacts.
        metadata: Deployment configuration metadata.
        created_at: When the deployment was created (UTC).
    
    Convenience attributes (mapped from metadata):
        cpu: CPU quota.
        memory: Memory quota.
        max_replicas: Maximum replicas.
        min_replicas: Minimum replicas.
        http_port: HTTP port.
    
    Note:
        - version, is_current, url, build_logs_url, runtime_logs_url have been removed.
        - Use deploy(wait=True) instead of wait_for_completion().
        - Use client.get_deployment() to get fresh data instead of refresh().
    """
    
    id: str
    project_id: str
    status: DeploymentStatus
    message: Optional[str]
    error_message: Optional[str]
    account_info: AccountInfo
    artifacts_source: ArtifactsSource
    metadata: DeploymentMetadata
    created_at: datetime
    _client: "DeploymentClient" = field(repr=False)
    _project: Optional["Project"] = field(default=None, repr=False)
    _data: Dict[str, Any] = field(default_factory=dict, repr=False)
    
    # Convenience properties mapped from metadata
    @property
    def cpu(self) -> str:
        """CPU quota (from metadata.replica_spec.cpu)."""
        return self.metadata.replica_spec.cpu
    
    @property
    def memory(self) -> str:
        """Memory quota (from metadata.replica_spec.memory)."""
        return self.metadata.replica_spec.memory
    
    @property
    def max_replicas(self) -> int:
        """Maximum replicas (from metadata.replica_spec.max_replicas)."""
        return self.metadata.replica_spec.max_replicas
    
    @property
    def min_replicas(self) -> int:
        """Minimum replicas (from metadata.replica_spec.min_replicas)."""
        return self.metadata.replica_spec.min_replicas
    
    @property
    def http_port(self) -> int:
        """HTTP port (from metadata.http_port)."""
        return self.metadata.http_port
    
    @property
    def environment_variables(self) -> Dict[str, str]:
        """Environment variables (from metadata.environment_variables)."""
        return self.metadata.environment_variables
    
    @property
    def is_terminal(self) -> bool:
        """Check if deployment is in a terminal state."""
        return self.status in TERMINAL_STATES
    
    @property
    def is_successful(self) -> bool:
        """Check if deployment completed successfully."""
        return self.status in SUCCESSFUL_STATES
    
    @property
    def is_cancellable(self) -> bool:
        """Check if deployment can be cancelled."""
        return self.status in CANCELLABLE_STATES
    
    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
        client: "DeploymentClient",
        project: Optional["Project"] = None,
    ) -> "Deployment":
        """Create Deployment from API response dictionary.
        
        Args:
            data: Dictionary containing deployment fields (camelCase from API).
            client: DeploymentClient instance for API calls.
            project: Optional parent Project instance.
        
        Returns:
            Deployment instance.
        """
        # Parse datetime
        def parse_datetime(value: Any) -> datetime:
            if isinstance(value, datetime):
                return value
            if isinstance(value, str):
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            return datetime.now()
        
        # Parse status (integer enum or string like "DEPLOYMENT_STATUS_BUILD_FAILED")
        status_value = data.get("status", 0)
        if isinstance(status_value, int):
            status = DeploymentStatus(status_value)
        elif isinstance(status_value, str):
            # Remove "DEPLOYMENT_STATUS_" prefix if present
            status_str = status_value.upper()
            if status_str.startswith("DEPLOYMENT_STATUS_"):
                status_str = status_str[len("DEPLOYMENT_STATUS_"):]
            # Try to parse as enum name
            try:
                status = DeploymentStatus[status_str]
            except KeyError:
                logger.warning(f"Unknown deployment status: {status_value}, defaulting to QUEUED")
                status = DeploymentStatus.QUEUED
        else:
            status = DeploymentStatus.QUEUED
        
        # Parse nested objects
        account_info_data = data.get("accountInfo", {})
        artifacts_source_data = data.get("artifactsSource", {})
        metadata_data = data.get("metadata", {})
        
        return cls(
            id=data.get("deploymentId", data.get("id", "")),
            project_id=data.get("projectId", project.id if project else ""),
            status=status,
            message=data.get("message"),
            error_message=data.get("errorMessage"),
            account_info=AccountInfo.from_dict(account_info_data),
            artifacts_source=ArtifactsSource.from_dict(artifacts_source_data),
            metadata=DeploymentMetadata.from_dict(metadata_data),
            created_at=parse_datetime(data.get("createdAt")),
            _client=client,
            _project=project,
            _data=data,
        )
    
    def stream_logs(self) -> Iterator["LogEntry"]:
        """Stream deployment logs via SSE.
        
        Connects to the log streaming endpoint and yields log entries
        as they are received. The stream will continue until the deployment
        completes or an error occurs.
        
        Yields:
            LogEntry instances containing log messages.
        
        Raises:
            DeploymentError: If streaming fails or receives an error event.
        
        Example:
            >>> for log in deployment.stream_logs():
            ...     print(log.message)
            Starting build task...
            Step 1/5: FROM ubuntu:22.04
        
        Note:
            SSE event types:
            - connected: Connection established (with deployment_id)
            - log: Log line data (yields LogEntry)
            - complete: Deployment completed (with status, stops iteration)
            - error: Error occurred (raises DeploymentError)
        """
        import json
        from novita_sandbox.artifact_hosting.exceptions import DeploymentError
        from novita_sandbox.artifact_hosting.models.log_entry import LogEntry
        
        logger.info(f"Streaming logs for deployment {self.id} (project: {self.project_id})")
        
        # API endpoint: GET /v1/projects/{projectId}/deployments/{deploymentId}/logs/stream
        path = f"/projects/{self.project_id}/deployments/{self.id}/logs/stream"
        
        try:
            for event_type, data_str in self._client._http.stream_sse_events(path):
                if event_type == "connected":
                    logger.debug("SSE connection established")
                    continue
                elif event_type == "complete":
                    logger.info("Deployment completed, ending log stream")
                    return
                elif event_type == "error":
                    error_msg = data_str if data_str else "Unknown error during log streaming"
                    logger.error(f"SSE error event: {error_msg}")
                    raise DeploymentError(error_msg)
                elif event_type == "log":
                    try:
                        # Parse log data as JSON
                        log_data = json.loads(data_str)
                        log_entry = LogEntry.from_dict(log_data)
                        yield log_entry
                    except json.JSONDecodeError as e:
                        logger.warning(f"Failed to parse log entry JSON: {e}, data: {data_str}")
                        continue
                else:
                    # Unknown event type, log and skip
                    logger.debug(f"Unknown SSE event type: {event_type}")
                    continue
        except KeyboardInterrupt:
            logger.info("Log streaming interrupted by user")
            return
        except DeploymentError:
            raise
        except Exception as e:
            logger.error(f"Error streaming logs: {e}")
            raise
    
    def cancel(self, *, reason: Optional[str] = None) -> "Deployment":
        """Cancel a pending or building deployment.
        
        Only deployments in QUEUED, BUILDING, or DEPLOYING status can be cancelled.
        
        Args:
            reason: Optional reason for cancelling the deployment.
        
        Returns:
            Updated Deployment instance with CANCELLED status.
        
        Raises:
            DeploymentError: If deployment cannot be cancelled (not in cancellable state).
        
        Example:
            >>> deployment = project.deploy(...)
            >>> # If you need to cancel before completion:
            >>> cancelled = deployment.cancel(reason="Found a bug")
            >>> print(cancelled.status)
            DeploymentStatus.CANCELLED
        """
        from novita_sandbox.artifact_hosting.exceptions import DeploymentError
        
        if not self.is_cancellable:
            raise DeploymentError(
                f"Deployment {self.id} cannot be cancelled. "
                f"Current status: {self.status.name}. "
                f"Only QUEUED, BUILDING, or DEPLOYING deployments can be cancelled."
            )
        
        # Build request payload per OpenAPI CancelDeploymentRequest_Payload
        payload: Dict[str, Any] = {}
        if reason:
            payload["reason"] = reason
        
        logger.info(f"Cancelling deployment {self.id} (project: {self.project_id})")
        
        response_data = self._client._http.post(
            f"/projects/{self.project_id}/deployments/{self.id}/cancel",
            json=payload,
            context="Cancel deployment",
        )
        
        # Response contains: projectId, deploymentId, previousStatus, currentStatus
        previous_status = response_data.get("previousStatus")
        current_status = response_data.get("currentStatus")
        
        logger.info(
            f"Deployment {self.id} cancelled. "
            f"Status changed from {previous_status} to {current_status}"
        )
        
        # Update local status. Backend may return either integer enum values or
        # strings like "DEPLOYMENT_STATUS_CANCELLED".
        if isinstance(current_status, int):
            self.status = DeploymentStatus(current_status)
        elif isinstance(current_status, str):
            try:
                self.status = DeploymentStatus.from_string(current_status)
            except ValueError:
                logger.warning(f"Unknown deployment status after cancel: {current_status}")
        
        return self
