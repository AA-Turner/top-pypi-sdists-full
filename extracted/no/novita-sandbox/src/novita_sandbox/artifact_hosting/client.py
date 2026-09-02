"""DeploymentClient - Main entry point for Artifact Hosting SDK V2.

This module implements the DeploymentClient class according to the V2 design.
"""

import logging
import os
from typing import Any, Dict, Iterator, List, Optional

from novita_sandbox.artifact_hosting.http.client import HTTPClient
from novita_sandbox.artifact_hosting.models.nested import DatabaseInfo
from novita_sandbox.artifact_hosting.models.project import Project
from novita_sandbox.artifact_hosting.utils.validation import validate_project_name

logger = logging.getLogger("novita_sandbox.artifact_hosting")

# Environment variable name for API key
ENV_NOVITA_API_KEY = "NOVITA_API_KEY"

# Fixed API base URL (not configurable)
API_BASE_URL = "https://artifact.novita.ai/v1"


class DeploymentClient:
    """SDK client for managing deployments.
    
    The DeploymentClient is the main entry point for the Artifact Hosting SDK V2.
    It provides methods for project and deployment management.
    
    Configuration:
    - api_key: Optional. Reads from NOVITA_API_KEY env var if not provided.
    - timeout: Request timeout in seconds (default: 30.0).
    
    Args:
        api_key: API key for authentication. Falls back to NOVITA_API_KEY env var.
        timeout: Request timeout in seconds. Defaults to 30.0.
    
    Example:
        >>> # Using environment variable for API key
        >>> client = DeploymentClient()
        >>> 
        >>> # Or explicit configuration
        >>> client = DeploymentClient(api_key="your-api-key")
        >>> 
        >>> # Create a project and deploy
        >>> project = client.create_project(name="my-app")
        >>> deployment = project.deploy(
        ...     sandbox_id="sbx-123",
        ...     arti_dir="/app/source",
        ... )
        >>> print(project.url)
    
    Note:
        - account_id is no longer required for any operations.
        - The API key identifies the account through the backend.
        - Use context manager for automatic cleanup:
          >>> with DeploymentClient() as client:
          ...     project = client.create_project(name="my-app")
    """
    
    DEFAULT_TIMEOUT = 30.0
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        """Initialize the deployment client.
        
        Args:
            api_key: API key for authentication. Falls back to env var.
            timeout: Request timeout in seconds.
        
        Raises:
            ValueError: If no API key is provided or found in environment.
        """
        # Resolve API key from argument or environment
        self.api_key = api_key or os.environ.get(ENV_NOVITA_API_KEY, "")
        if not self.api_key:
            raise ValueError(
                f"API key is required. Provide via constructor or "
                f"{ENV_NOVITA_API_KEY} environment variable."
            )
        
        # Fixed API URL (not configurable)
        self.base_url = API_BASE_URL
        self.timeout = timeout
        
        # Initialize HTTP client
        self._http = HTTPClient(
            base_url=self.base_url,
            api_key=self.api_key,
            timeout=timeout,
        )
        
        logger.info(f"DeploymentClient initialized: base_url={self.base_url}")
    
    def close(self) -> None:
        """Close the client and release resources."""
        self._http.close()
        logger.debug("DeploymentClient closed")
    
    def __enter__(self) -> "DeploymentClient":
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.close()
    
    # === Project Management Methods ===
    
    def create_project(
        self,
        name: str,
        *,
        description: Optional[str] = None,
        request_timeout_seconds: Optional[str] = None,
    ) -> Project:
        """Create a new project.
        
        Args:
            name: Project name (lowercase, numbers, hyphens, 3-63 chars, starts with letter).
            description: Optional project description.
            request_timeout_seconds: Request timeout for the endpoint.
        
        Returns:
            Created Project instance.
        
        Raises:
            ValueError: If project name is invalid.
            QuotaExceededError: If account quota exceeded.
            DeploymentError: If creation fails.
        
        Example:
            >>> project = client.create_project(
            ...     name="my-app",
            ...     description="My application",
            ... )
            >>> print(project.id)
        """
        # Validate project name
        validate_project_name(name)
        
        payload: Dict[str, Any] = {
            "name": name,
        }
        if description is not None:
            payload["description"] = description
        if request_timeout_seconds is not None:
            payload["endpointConfig"] = {
                "requestTimeoutSeconds": request_timeout_seconds,
            }
        
        logger.info(f"Creating project: {name}")
        
        response_data = self._http.post(
            "/projects",
            json=payload,
            context="Create project",
        )
        
        project = Project.from_dict(response_data, self)
        logger.info(f"Project created: {project.id}")
        
        return project
    
    def get_project(self, project_id: str) -> Project:
        """Get a project by ID or name.
        
        Args:
            project_id: Project ID or name.
        
        Returns:
            Project instance.
        
        Raises:
            ProjectNotFoundError: If project not found.
        
        Example:
            >>> project = client.get_project("proj-123")
            >>> # or by name
            >>> project = client.get_project("my-app")
        """
        logger.debug(f"Getting project: {project_id}")
        
        response_data = self._http.get(
            f"/projects/{project_id}",
            context="Get project",
        )
        
        return Project.from_dict(response_data, self)
    
    def list_projects(
        self,
        *,
        status: Optional[List[int]] = None,
    ) -> Iterator[Project]:
        """List all projects for the current account.
        
        The account is identified by the API key.
        
        Args:
            status: Filter by project status values (list of integers).
        
        Yields:
            Project instances.
        
        Example:
            >>> for project in client.list_projects():
            ...     print(project.name)
        """
        params: Dict[str, Any] = {}
        if status:
            # OpenAPI spec uses 'filters.status' parameter name
            params["filters.status"] = ",".join(str(s) for s in status)
        
        logger.debug("Listing projects")
        
        response_data = self._http.get(
            "/projects",
            params=params if params else None,
            context="List projects",
        )
        
        # Backend returns list in "projects" key per OpenAPI spec
        items = response_data.get("projects", [])
        for item in items:
            yield Project.from_dict(item, self)
    
    def delete_project(self, project_id: str) -> None:
        """Delete a project (soft delete).
        
        This performs a soft delete - the project record is marked as deleted
        but deployment history is preserved.
        
        Args:
            project_id: Project ID or name.
        
        Raises:
            ProjectNotFoundError: If project not found.
            DeploymentError: If deletion fails.
        
        Example:
            >>> client.delete_project("proj-123")
        """
        logger.info(f"Deleting project: {project_id}")
        
        self._http.delete(
            f"/projects/{project_id}",
            context="Delete project",
        )

        logger.info(f"Project deleted: {project_id}")

    def ensure_project_database(self, project_id: str) -> DatabaseInfo:
        """Create or reuse the TiDB database for a project."""
        logger.info(f"Ensuring database for project: {project_id}")

        response_data = self._http.post(
            f"/projects/{project_id}/database",
            json={"projectId": project_id},
            context="Ensure project database",
        )

        database_info_data = response_data.get("databaseInfo", response_data)
        database_info = DatabaseInfo.from_dict(database_info_data)

        logger.info(f"Database ensured for project: {project_id}, status={database_info.status}")

        return database_info
