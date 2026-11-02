import logging
from typing import NoReturn
from uuid import UUID

from httpx import AsyncClient, Client, HTTPStatusError, codes
from tenacity import (
    before_sleep_log,
    retry,
    stop_after_attempt,
    wait_exponential,
)

from edison_client.models.data_storage_methods import DataStorageResponse
from edison_client.models.workspace import (
    CreateWorkspacePayload,
    UpdateWorkspacePayload,
)
from edison_client.utils.general import (
    _BASE_CONNECTION_ERRORS,
    RETRYABLE_HTTP_STATUS_CODES,
    retry_if_connection_error,
)

logger = logging.getLogger(__name__)

_WORKSPACES_PATH = "/v0.1/data-storage/workspaces"


class WorkspaceError(Exception):
    """Base exception for workspace operations."""


class WorkspaceNotFoundError(WorkspaceError):
    """Raised when a workspace entry cannot be found."""


class WorkspacePermissionError(WorkspaceError):
    """Raised when the user lacks permission for a workspace operation."""


class WorkspaceMethods:
    """Workspace CRUD methods for RestClient.

    Provides sync and async wrappers around the
    ``/v0.1/data-storage/workspaces`` endpoints.
    """

    @property
    def client(self) -> Client:
        raise NotImplementedError("client property must be implemented by subclass")

    @property
    def async_client(self) -> AsyncClient:
        raise NotImplementedError(
            "async_client property must be implemented by subclass"
        )

    def _handle_workspace_http_errors(  # noqa: PLR6301
        self,
        e: HTTPStatusError,
        operation: str,
    ) -> NoReturn:
        if e.response.status_code in RETRYABLE_HTTP_STATUS_CODES:
            raise e
        if e.response.status_code == codes.NOT_FOUND:
            raise WorkspaceNotFoundError(
                f"Workspace not found while {operation}: {e.response.text}"
            ) from e
        if e.response.status_code == codes.FORBIDDEN:
            raise WorkspacePermissionError(
                f"Permission denied while {operation}: {e.response.text}"
            ) from e
        if e.response.status_code == codes.UNPROCESSABLE_ENTITY:
            raise WorkspaceError(f"Invalid request payload: {e.response.text}") from e
        raise WorkspaceError(
            f"Error {operation}: {e.response.status_code} - {e.response.text}"
        ) from e

    # ------------------------------------------------------------------
    # create
    # ------------------------------------------------------------------

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def create_workspace(
        self,
        name: str,
        *,
        description: str | None = None,
        project_id: UUID | None = None,
        tags: list[str] | None = None,
    ) -> DataStorageResponse:
        """Create a new workspace.

        Args:
            name: Human-readable name for the workspace.
            description: Optional description.
            project_id: Project to associate (inherits project sharing).
            tags: Additional tags (``workspace`` is always added server-side).

        Returns:
            DataStorageResponse with the created workspace entry.
        """
        try:
            payload = CreateWorkspacePayload(
                name=name,
                description=description,
                project_id=project_id,
                tags=tags,
            )
            response = self.client.post(
                _WORKSPACES_PATH,
                json=payload.model_dump(mode="json", exclude_none=True),
            )
            response.raise_for_status()
            return DataStorageResponse.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_workspace_http_errors(e, "creating workspace")
        except WorkspaceError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise WorkspaceError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def acreate_workspace(
        self,
        name: str,
        *,
        description: str | None = None,
        project_id: UUID | None = None,
        tags: list[str] | None = None,
    ) -> DataStorageResponse:
        """Create a new workspace (async).

        Args:
            name: Human-readable name for the workspace.
            description: Optional description.
            project_id: Project to associate (inherits project sharing).
            tags: Additional tags (``workspace`` is always added server-side).

        Returns:
            DataStorageResponse with the created workspace entry.
        """
        try:
            payload = CreateWorkspacePayload(
                name=name,
                description=description,
                project_id=project_id,
                tags=tags,
            )
            response = await self.async_client.post(
                _WORKSPACES_PATH,
                json=payload.model_dump(mode="json", exclude_none=True),
            )
            response.raise_for_status()
            return DataStorageResponse.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_workspace_http_errors(e, "creating workspace")
        except WorkspaceError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise WorkspaceError(f"An unexpected error occurred: {e!r}") from e

    # ------------------------------------------------------------------
    # get
    # ------------------------------------------------------------------

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def get_workspace(self, workspace_id: UUID) -> DataStorageResponse:
        """Retrieve a workspace by its DSS entry ID.

        Args:
            workspace_id: UUID of the workspace entry.

        Returns:
            DataStorageResponse with the workspace entry.
        """
        try:
            response = self.client.get(f"{_WORKSPACES_PATH}/{workspace_id}")
            response.raise_for_status()
            return DataStorageResponse.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_workspace_http_errors(e, "fetching workspace")
        except WorkspaceError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise WorkspaceError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aget_workspace(self, workspace_id: UUID) -> DataStorageResponse:
        """Retrieve a workspace by its DSS entry ID (async).

        Args:
            workspace_id: UUID of the workspace entry.

        Returns:
            DataStorageResponse with the workspace entry.
        """
        try:
            response = await self.async_client.get(f"{_WORKSPACES_PATH}/{workspace_id}")
            response.raise_for_status()
            return DataStorageResponse.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_workspace_http_errors(e, "fetching workspace")
        except WorkspaceError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise WorkspaceError(f"An unexpected error occurred: {e!r}") from e

    # ------------------------------------------------------------------
    # update
    # ------------------------------------------------------------------

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def update_workspace(
        self,
        workspace_id: UUID,
        *,
        name: str | None = None,
        description: str | None = None,
    ) -> DataStorageResponse:
        """Update a workspace's mutable fields.

        Only the workspace owner can update.

        Args:
            workspace_id: UUID of the workspace entry.
            name: New name (``None`` leaves unchanged).
            description: New description (``None`` leaves unchanged).

        Returns:
            DataStorageResponse with the updated workspace entry.
        """
        try:
            payload = UpdateWorkspacePayload(name=name, description=description)
            response = self.client.patch(
                f"{_WORKSPACES_PATH}/{workspace_id}",
                json=payload.model_dump(mode="json", exclude_none=True),
            )
            response.raise_for_status()
            return DataStorageResponse.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_workspace_http_errors(e, "updating workspace")
        except WorkspaceError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise WorkspaceError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aupdate_workspace(
        self,
        workspace_id: UUID,
        *,
        name: str | None = None,
        description: str | None = None,
    ) -> DataStorageResponse:
        """Update a workspace's mutable fields (async).

        Only the workspace owner can update.

        Args:
            workspace_id: UUID of the workspace entry.
            name: New name (``None`` leaves unchanged).
            description: New description (``None`` leaves unchanged).

        Returns:
            DataStorageResponse with the updated workspace entry.
        """
        try:
            payload = UpdateWorkspacePayload(name=name, description=description)
            response = await self.async_client.patch(
                f"{_WORKSPACES_PATH}/{workspace_id}",
                json=payload.model_dump(mode="json", exclude_none=True),
            )
            response.raise_for_status()
            return DataStorageResponse.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_workspace_http_errors(e, "updating workspace")
        except WorkspaceError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise WorkspaceError(f"An unexpected error occurred: {e!r}") from e

    # ------------------------------------------------------------------
    # delete
    # ------------------------------------------------------------------

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def delete_workspace(self, workspace_id: UUID) -> None:
        """Soft-delete a workspace.  Only the owner can delete.

        Args:
            workspace_id: UUID of the workspace entry.
        """
        try:
            response = self.client.delete(f"{_WORKSPACES_PATH}/{workspace_id}")
            response.raise_for_status()
        except HTTPStatusError as e:
            self._handle_workspace_http_errors(e, "deleting workspace")
        except WorkspaceError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise WorkspaceError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def adelete_workspace(self, workspace_id: UUID) -> None:
        """Soft-delete a workspace (async).  Only the owner can delete.

        Args:
            workspace_id: UUID of the workspace entry.
        """
        try:
            response = await self.async_client.delete(
                f"{_WORKSPACES_PATH}/{workspace_id}"
            )
            response.raise_for_status()
        except HTTPStatusError as e:
            self._handle_workspace_http_errors(e, "deleting workspace")
        except WorkspaceError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise WorkspaceError(f"An unexpected error occurred: {e!r}") from e
