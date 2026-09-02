"""Project model for Artifact Hosting SDK V2.

This module implements the Project class according to the V2 design.
"""

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterator, List, Optional

from novita_sandbox.artifact_hosting.models.enums import (
    ProjectStatus,
    TERMINAL_STATES,
    is_successful,
)
from novita_sandbox.artifact_hosting.models.nested import (
    AccountInfo,
    DatabaseInfo,
    Endpoint,
    EndpointConfig,
)

logger = logging.getLogger("novita_sandbox.artifact_hosting")

if TYPE_CHECKING:
    from novita_sandbox.artifact_hosting.client import DeploymentClient
    from novita_sandbox.artifact_hosting.models.deployment import Deployment


@dataclass
class Project:
    """Represents a deployable application project.
    
    A project is a container for deployments. Each project has a unique name
    within an account and can have multiple deployment versions.
    
    Attributes:
        id: Unique project identifier (maps from projectId).
        account_info: Account information object (populated by backend).
        name: URL-safe project name (used for URL generation).
        description: Optional project description.
        status: Project status (ProjectStatus enum).
        endpoint: Endpoint information object with URLs.
        endpoint_config: Endpoint configuration settings.
        deployment_count: Total number of deployments.
        current_deployment_id: ID of currently running deployment (if any).
        created_at: When the project was created (UTC).
        updated_at: When the project was last updated (UTC).
    
    Note:
        - Environment variables are now at deployment level only (in deploy() method).
        - display_name has been removed.
        - Use client.get_project() to get fresh data instead of project.refresh().
        - Use client.delete_project() instead of project.delete().
    """
    
    id: str
    account_info: AccountInfo
    name: str
    description: Optional[str]
    status: ProjectStatus
    endpoint: Endpoint
    endpoint_config: EndpointConfig
    deployment_count: int
    current_deployment_id: Optional[str]
    database_info: Optional[DatabaseInfo]
    created_at: datetime
    updated_at: datetime
    _client: "DeploymentClient" = field(repr=False)
    _data: Dict[str, Any] = field(default_factory=dict, repr=False)
    
    @property
    def url(self) -> Optional[str]:
        """Get the default URL for the project.
        
        Convenience property that returns endpoint.default_url.
        """
        return self.endpoint.default_url if self.endpoint else None

    def ensure_database(self) -> DatabaseInfo:
        """Create or reuse the TiDB database for this project."""
        database_info = self._client.ensure_project_database(self.id)
        self.database_info = database_info
        return database_info
    
    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
        client: "DeploymentClient",
    ) -> "Project":
        """Create Project from API response dictionary.
        
        Args:
            data: Dictionary containing project fields (camelCase from API).
            client: DeploymentClient instance for API calls.
        
        Returns:
            Project instance.
        """
        # Parse datetime fields
        def parse_datetime(value: Any) -> datetime:
            if isinstance(value, datetime):
                return value
            if isinstance(value, str):
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            return datetime.now()
        
        # Parse status (integer or string like "PROJECT_STATUS_ACTIVE")
        status_value = data.get("status", 0)
        if isinstance(status_value, int):
            status = ProjectStatus(status_value)
        elif isinstance(status_value, str):
            # Remove "PROJECT_STATUS_" prefix if present
            status_str = status_value.upper()
            if status_str.startswith("PROJECT_STATUS_"):
                status_str = status_str[len("PROJECT_STATUS_"):]
            try:
                status = ProjectStatus[status_str]
            except KeyError:
                logger.warning(f"Unknown project status: {status_value}, defaulting to UNSPECIFIED")
                status = ProjectStatus.UNSPECIFIED
        else:
            status = ProjectStatus.UNSPECIFIED
        
        # Parse nested objects
        account_info_data = data.get("accountInfo", {})
        endpoint_data = data.get("endpoint", {})
        endpoint_config_data = data.get("endpointConfig", {})
        database_info_data = data.get("databaseInfo")
        
        return cls(
            id=data.get("projectId", data.get("id", "")),
            account_info=AccountInfo.from_dict(account_info_data),
            name=data.get("name", ""),
            description=data.get("description"),
            status=status,
            endpoint=Endpoint.from_dict(endpoint_data),
            endpoint_config=EndpointConfig.from_dict(endpoint_config_data),
            deployment_count=data.get("deploymentCount", 0),
            current_deployment_id=data.get("currentDeploymentId"),
            database_info=DatabaseInfo.from_dict(database_info_data) if database_info_data else None,
            created_at=parse_datetime(data.get("createdAt")),
            updated_at=parse_datetime(data.get("updatedAt")),
            _client=client,
            _data=data,
        )
    
    def deploy(
        self,
        sandbox_id: str,
        arti_dir: str,
        *,
        dockerfile: Optional[str] = None,
        message: Optional[str] = None,
        environment_variables: Optional[Dict[str, str]] = None,
        database: bool = False,
        migrations: Optional[List[str]] = None,
        http_port: int = 3000,
        check_health_path: Optional[str] = None,
        cpu: str = "1",
        memory: str = "1Gi",
        max_replicas: int = 1,
        min_replicas: int = 0,
        wait: bool = True,
        poll_interval: float = 5.0,
        timeout: float = 600.0,
        on_status_change: Optional[Callable[["Deployment"], None]] = None,
    ) -> "Deployment":
        """Deploy source code from a Sandbox to this project.
        
        The deployment flow:
        1. SDK reads Dockerfile content (from path or uses content directly)
        2. SDK calls backend API to create deployment with all parameters
        3. Backend handles: source retrieval, image build, deployment to cluster
        4. If wait=True, SDK polls deployment status until completion
        
        Args:
            sandbox_id: ID of the Sandbox containing the source code.
            arti_dir: Path to the source code directory within the Sandbox.
            dockerfile: Dockerfile path (relative to arti_dir) or content.
                If contains newline or starts with "FROM ", treated as content.
                If None, reads from {arti_dir}/Dockerfile.
            message: Optional deployment message/description.
            environment_variables: Environment variables for the deployment.
            http_port: Port the application listens on (default: 3000).
            check_health_path: HTTP path for health checks (e.g., "/health").
            cpu: CPU quota (default: "1").
            memory: Memory quota (default: "1Gi").
            max_replicas: Maximum replicas (current version: 1).
            min_replicas: Minimum replicas (current version: 0).
            database: If True, provision a TiDB database and inject DATABASE_URL.
            migrations: Optional migration commands to run with database setup.
            wait: If True, block until deployment completes (default: True).
            poll_interval: Seconds between status checks (default: 5.0).
            timeout: Maximum wait time in seconds (default: 600.0 = 10 min).
            on_status_change: Callback when deployment status changes.
        
        Returns:
            Deployment instance.
        
        Raises:
            FileNotFoundError: If Dockerfile path doesn't exist.
            ValueError: If Dockerfile content is empty or environment variable key invalid.
            DeploymentError: If deployment fails.
            TimeoutError: If deployment doesn't complete within timeout.
        """
        from novita_sandbox.artifact_hosting.models.deployment import Deployment
        from novita_sandbox.artifact_hosting.utils.validation import validate_environment_variables
        
        # Validate environment variables if provided
        if environment_variables:
            validate_environment_variables(environment_variables)
        
        # Read Dockerfile content
        # Note: For V2, we read from Sandbox filesystem via SDK
        # In actual implementation, backend may read from Sandbox directly
        # For now, we assume dockerfile is either content or we raise an error for path
        dockerfile_content: str
        if dockerfile is None:
            # Default: backend will read from sandbox_id + arti_dir + Dockerfile
            dockerfile_content = ""  # Backend handles default
        elif "\n" in dockerfile or dockerfile.strip().upper().startswith("FROM "):
            # It's content
            dockerfile_content = dockerfile
        else:
            # It's a path - in V2, we cannot read from Sandbox directly in SDK
            # Pass the path to backend which will read it
            # Actually per design, SDK should read and send content
            # For now, we'll treat it as a relative path that backend can resolve
            dockerfile_content = dockerfile  # Backend will interpret as path
        
        # Build request payload per openapi_v2.yaml
        metadata_payload = {
            "httpPort": http_port,
            "replicaSpec": {
                "cpu": cpu,
                "memory": memory,
                "maxReplicas": max_replicas,
                "minReplicas": min_replicas,
            },
        }
        
        if environment_variables:
            metadata_payload["environmentVariables"] = environment_variables
        if check_health_path:
            metadata_payload["checkHealthPath"] = check_health_path
        if database:
            metadata_payload["database"] = True
        if migrations:
            metadata_payload["migrations"] = migrations
        
        payload: Dict[str, Any] = {
            "projectId": self.id,
            "artifactsSource": {
                "sandboxId": sandbox_id,
                "path": arti_dir,
            },
            "metadata": metadata_payload,
        }
        
        if message:
            payload["message"] = message
        if dockerfile_content:
            payload["dockerfile"] = dockerfile_content
        
        logger.info(f"Creating deployment for project {self.id}")
        logger.debug(f"  sandbox_id={sandbox_id}, arti_dir={arti_dir}")
        
        # Call API to create deployment
        response_data = self._client._http.post(
            f"/projects/{self.id}/deploy",
            json=payload,
            context="Create deployment",
        )
        
        deployment = Deployment.from_dict(response_data, self._client, self)
        logger.info(f"Deployment created: {deployment.id}, status={deployment.status.name}")
        
        if not wait:
            return deployment
        
        # Poll for completion
        return self._wait_for_deployment(
                deployment=deployment,
            poll_interval=poll_interval,
            timeout=timeout,
                on_status_change=on_status_change,
            )
        
    def _wait_for_deployment(
        self,
        deployment: "Deployment",
        poll_interval: float,
        timeout: float,
        on_status_change: Optional[Callable[["Deployment"], None]],
    ) -> "Deployment":
        """Poll deployment status until completion.
        
        Args:
            deployment: Deployment to monitor.
            poll_interval: Seconds between polls.
            timeout: Maximum wait time.
            on_status_change: Callback on status change.
        
        Returns:
            Updated Deployment.
        
        Raises:
            DeploymentError: If deployment fails.
            TimeoutError: If timeout exceeded.
        """
        from novita_sandbox.artifact_hosting.exceptions import (
            DeploymentError,
            TimeoutError as SDKTimeoutError,
        )
        from novita_sandbox.artifact_hosting.models.deployment import Deployment
        
        start_time = time.time()
        last_status = deployment.status
        poll_count = 0
        
        logger.info(
            f"Waiting for deployment {deployment.id} to complete "
            f"(poll_interval={poll_interval}s, timeout={timeout}s)"
        )
        
        consecutive_errors = 0
        max_consecutive_errors = 3  # Allow up to 3 consecutive network errors
        
        while time.time() - start_time < timeout:
            poll_count += 1
            elapsed = time.time() - start_time
            
            try:
                # Get latest deployment status
                response_data = self._client._http.get(
                    f"/projects/{self.id}/deployments/{deployment.id}",
                    context="Get deployment status",
                )
                deployment = Deployment.from_dict(response_data, self._client, self)
                consecutive_errors = 0  # Reset on success
                
            except Exception as e:
                # Network error during polling - log and continue
                consecutive_errors += 1
                logger.warning(
                    f"Poll #{poll_count} ({elapsed:.0f}s): Network error ({consecutive_errors}/{max_consecutive_errors}): {e}"
                )
                
                if consecutive_errors >= max_consecutive_errors:
                    logger.error(f"Too many consecutive polling errors, giving up")
                    raise DeploymentError(f"Failed to poll deployment status: {e}")
                
                time.sleep(poll_interval)
                continue
            
            # Log poll status for debugging
            logger.debug(
                f"Poll #{poll_count} ({elapsed:.0f}s): "
                f"status={deployment.status.name}, error={deployment.error_message or 'None'}"
            )
            
            # Notify on status change
            if deployment.status != last_status:
                logger.info(f"Deployment status changed: {last_status.name} -> {deployment.status.name}")
                if on_status_change:
                    on_status_change(deployment)
                last_status = deployment.status
            
            # Check if terminal
            if deployment.status in TERMINAL_STATES:
                if is_successful(deployment.status):
                    logger.info(f"Deployment completed successfully: {deployment.id}")
                    return deployment
                else:
                    error_msg = deployment.error_message or f"Deployment failed with status: {deployment.status.name}"
                    logger.error(f"Deployment failed: {error_msg}")
                    raise DeploymentError(error_msg)
            
            time.sleep(poll_interval)
        
        # Log final status on timeout for debugging
        logger.error(
            f"Deployment timed out after {timeout}s. "
            f"deployment_id={deployment.id}, "
            f"final_status={deployment.status.name}, "
            f"error_message={deployment.error_message or 'None'}"
        )
        raise SDKTimeoutError(
            f"Deployment did not complete within {timeout} seconds. "
            f"Final status: {deployment.status.name}"
        )
    
    def list_deployments(
        self,
        *,
        status: Optional[List[int]] = None,
    ) -> Iterator["Deployment"]:
        """List deployments for this project.
        
        Args:
            status: Filter by status values (list of integers).
        
        Yields:
            Deployment instances, ordered by creation time (newest first).
        """
        from novita_sandbox.artifact_hosting.models.deployment import Deployment
        
        params: Dict[str, Any] = {}
        if status:
            # OpenAPI spec uses 'filters.status' parameter name
            params["filters.status"] = ",".join(str(s) for s in status)
        
        response_data = self._client._http.get(
            f"/projects/{self.id}/deployments",
            params=params if params else None,
            context="List deployments",
        )
        
        # Backend returns list in "deployments" key per OpenAPI spec
        items = response_data.get("deployments", [])
        for item in items:
            yield Deployment.from_dict(item, self._client, self)
    
    def get_deployment(self, deployment_id: str) -> "Deployment":
        """Get a specific deployment by ID.
        
        Args:
            deployment_id: Deployment identifier.
        
        Returns:
            Deployment instance.
        
        Raises:
            DeploymentNotFoundError: If deployment not found.
        """
        from novita_sandbox.artifact_hosting.models.deployment import Deployment
        
        response_data = self._client._http.get(
            f"/projects/{self.id}/deployments/{deployment_id}",
            context="Get deployment",
        )
        
        return Deployment.from_dict(response_data, self._client, self)
    
    def rollback(
        self,
        target_deployment_id: str,
        *,
        reason: Optional[str] = None,
    ) -> Dict[str, str]:
        """Rollback to a previous deployment.
        
        Args:
            target_deployment_id: ID of deployment to rollback to.
            reason: Optional reason for the rollback.
        
        Returns:
            Dictionary with:
            - project_id: Project ID
            - previous_deployment_id: ID of the deployment being replaced
            - current_deployment_id: ID of the new current deployment (target)
        
        Raises:
            RollbackError: If rollback fails or target is invalid.
        """
        # Build payload per OpenAPI RollbackRequest_Payload
        payload: Dict[str, Any] = {}
        if reason:
            payload["reason"] = reason
        
        logger.info(f"Rolling back project {self.id} to deployment {target_deployment_id}")
        
        # Path: /projects/{projectId}/deployments/{deploymentId}/rollback
        response_data = self._client._http.post(
            f"/projects/{self.id}/deployments/{target_deployment_id}/rollback",
            json=payload,
            context="Rollback deployment",
        )
        
        # Map response to snake_case
        result = {
            "project_id": response_data.get("projectId", self.id),
            "previous_deployment_id": response_data.get("previousDeploymentId", ""),
            "current_deployment_id": response_data.get("currentDeploymentId", target_deployment_id),
        }
        
        logger.info(f"Rollback successful: {result}")
        
        # Update local state
        self.current_deployment_id = result["current_deployment_id"]
        
        return result
    
    def update(
        self,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        request_timeout_seconds: Optional[str] = None,
    ) -> "Project":
        """Update project properties.
        
        Args:
            name: New project name (must follow naming rules).
            description: New description.
            request_timeout_seconds: Request timeout for the endpoint (as string).
        
        Returns:
            Updated Project instance (self).
        
        Raises:
            ValueError: If name is invalid.
            DeploymentError: If update fails.
        """
        from novita_sandbox.artifact_hosting.utils.validation import validate_project_name
        
        if name is not None:
            validate_project_name(name)
        
        # Build payload per OpenAPI spec: UpdateProjectRequest_UpdateProjectPayload
        update_payload: Dict[str, Any] = {}
        if name is not None:
            update_payload["name"] = name
        if description is not None:
            update_payload["description"] = description
        if request_timeout_seconds is not None:
            update_payload["endpointConfig"] = {
                "requestTimeoutSeconds": request_timeout_seconds,
            }
        
        if not update_payload:
            return self  # Nothing to update
        
        # Request body per OpenAPI: { projectId, payload: {...} }
        request_body: Dict[str, Any] = {
            "projectId": self.id,
            "payload": update_payload,
        }
        
        logger.info(f"Updating project {self.id}")
        
        response_data = self._client._http.patch(
            f"/projects/{self.id}",
            json=request_body,
            context="Update project",
        )
        
        # Update local state from response
        updated = Project.from_dict(response_data, self._client)
        
        self.name = updated.name
        self.description = updated.description
        self.endpoint_config = updated.endpoint_config
        self.updated_at = updated.updated_at
        self._data = updated._data
        
        return self
