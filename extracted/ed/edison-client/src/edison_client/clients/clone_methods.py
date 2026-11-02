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

from edison_client.models.clone import (
    ChatCloneRequest,
    ChatCloneResponse,
    ProjectCloneRequest,
    ProjectCloneResponse,
)
from edison_client.utils.general import (
    _BASE_CONNECTION_ERRORS,
    RETRYABLE_HTTP_STATUS_CODES,
    retry_if_connection_error,
)

logger = logging.getLogger(__name__)

_PROJECT_CLONE_PATH = "/v0.1/admin/projects/{project_id}/clone"
_CHAT_CLONE_PATH = "/v0.1/admin/chat/clone"


class CloneError(Exception):
    """Base exception for admin clone operations."""


class CloneNotFoundError(CloneError):
    """Raised when the clone source (project or session) cannot be found."""


class ClonePermissionError(CloneError):
    """Raised when the caller lacks permission for clone operations."""


class CloneInvalidRequestError(CloneError):
    """Raised when the clone request is invalid."""


class CloneMethods:
    """Admin-only project and chat clone operations."""

    @property
    def client(self) -> Client:
        raise NotImplementedError("client property must be implemented by subclass")

    @property
    def async_client(self) -> AsyncClient:
        raise NotImplementedError(
            "async_client property must be implemented by subclass"
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def clone_project(
        self,
        project_id: UUID,
        *,
        name: str,
        target_owner_email: str | None = None,
    ) -> ProjectCloneResponse:
        """Clone a persona project into a new private project.

        Args:
            project_id: UUID of the source project to clone.
            name: Name for the new project.
            target_owner_email: Email of the user who should own the clone.
                When omitted the caller owns the clone.

        Returns:
            New project id and the old-to-new ``world_model`` id map.
        """
        try:
            payload = ProjectCloneRequest(
                name=name, target_owner_email=target_owner_email
            )
            response = self.client.post(
                _PROJECT_CLONE_PATH.format(project_id=project_id),
                json=payload.model_dump(mode="json", exclude_none=True),
            )
            response.raise_for_status()
            return ProjectCloneResponse.model_validate(response.json())
        except HTTPStatusError as e:
            _handle_clone_http_errors(e, "cloning project")
        except CloneError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise CloneError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aclone_project(
        self,
        project_id: UUID,
        *,
        name: str,
        target_owner_email: str | None = None,
    ) -> ProjectCloneResponse:
        """Clone a persona project into a new private project."""
        try:
            payload = ProjectCloneRequest(
                name=name, target_owner_email=target_owner_email
            )
            response = await self.async_client.post(
                _PROJECT_CLONE_PATH.format(project_id=project_id),
                json=payload.model_dump(mode="json", exclude_none=True),
            )
            response.raise_for_status()
            return ProjectCloneResponse.model_validate(response.json())
        except HTTPStatusError as e:
            _handle_clone_http_errors(e, "cloning project")
        except CloneError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise CloneError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def clone_chat(
        self,
        source_session_id: UUID,
        target_project_id: UUID,
        *,
        limit: int | None = None,
        world_model_id_map: dict[UUID, UUID] | None = None,
    ) -> ChatCloneResponse:
        """Clone a chat session's conversations into another project.

        Args:
            source_session_id: UUID of the session to copy conversations from.
            target_project_id: UUID of the target project.
            limit: Maximum number of messages to copy.
            world_model_id_map: Old-to-new ``world_model`` UUID map.

        Returns:
            Target session id and copied message count.
        """
        try:
            payload = ChatCloneRequest(
                source_session_id=source_session_id,
                target_project_id=target_project_id,
                limit=limit,
                world_model_id_map=world_model_id_map or {},
            )
            response = self.client.post(
                _CHAT_CLONE_PATH,
                json=payload.model_dump(mode="json", exclude_none=True),
            )
            response.raise_for_status()
            return ChatCloneResponse.model_validate(response.json())
        except HTTPStatusError as e:
            _handle_clone_http_errors(e, "cloning chat session")
        except CloneError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise CloneError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aclone_chat(
        self,
        source_session_id: UUID,
        target_project_id: UUID,
        *,
        limit: int | None = None,
        world_model_id_map: dict[UUID, UUID] | None = None,
    ) -> ChatCloneResponse:
        """Clone a chat session's conversations into another project."""
        try:
            payload = ChatCloneRequest(
                source_session_id=source_session_id,
                target_project_id=target_project_id,
                limit=limit,
                world_model_id_map=world_model_id_map or {},
            )
            response = await self.async_client.post(
                _CHAT_CLONE_PATH,
                json=payload.model_dump(mode="json", exclude_none=True),
            )
            response.raise_for_status()
            return ChatCloneResponse.model_validate(response.json())
        except HTTPStatusError as e:
            _handle_clone_http_errors(e, "cloning chat session")
        except CloneError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise CloneError(f"An unexpected error occurred: {e!r}") from e


def _handle_clone_http_errors(e: HTTPStatusError, operation: str) -> NoReturn:
    if e.response.status_code in RETRYABLE_HTTP_STATUS_CODES:
        raise e
    if e.response.status_code == codes.NOT_FOUND:
        raise CloneNotFoundError(
            f"Clone source not found while {operation}: {e.response.text}"
        ) from e
    if e.response.status_code == codes.FORBIDDEN:
        raise ClonePermissionError(
            f"Permission denied while {operation}: {e.response.text}"
        ) from e
    if e.response.status_code == codes.UNPROCESSABLE_ENTITY:
        raise CloneInvalidRequestError(
            f"Invalid clone request while {operation}: {e.response.text}"
        ) from e
    raise CloneError(
        f"Error {operation}: {e.response.status_code} - {e.response.text}"
    ) from e
