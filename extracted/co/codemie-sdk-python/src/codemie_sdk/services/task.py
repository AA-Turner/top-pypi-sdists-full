"""Task service implementation."""

from ..models.task import BackgroundTaskEntity
from ..utils.http import ApiRequestHandler, TokenSource


class TaskService:
    """Service for managing background tasks."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the Task service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates. Default: True
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def get(self, task_id: str) -> BackgroundTaskEntity:
        """Get a background task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            BackgroundTaskEntity: The task details

        Raises:
            ApiError: If the task doesn't exist or there's an API error
        """
        return self._api.get(
            f"/v1/tasks/{task_id}", BackgroundTaskEntity, wrap_response=False
        )
