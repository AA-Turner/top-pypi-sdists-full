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

from edison_client.models.session import Session
from edison_client.utils.general import (
    _BASE_CONNECTION_ERRORS,
    RETRYABLE_HTTP_STATUS_CODES,
    retry_if_connection_error,
)

logger = logging.getLogger(__name__)


class SessionError(Exception):
    """Base exception for session operations."""


class SessionFetchError(SessionError):
    """Raised when there's an error fetching session data."""


class SessionMethods:
    """Session methods for RestClient.

    Wraps the ``/v0.1/sessions`` endpoints with typed responses so callers
    don't have to drop down to the raw http client to look up a session by
    id (e.g. to recover the owning ``project_id``).
    """

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
    def get_session(self, session_id: UUID) -> list[Session]:
        """Get all session rows for a given session id.

        A single ``session_id`` can correspond to multiple rows (the
        conversation row plus any trajectories that share the id), which is
        why the API — and therefore this method — returns a list.

        Args:
            session_id: Session ID to look up.

        Returns:
            Non-empty list of ``Session`` records.

        Raises:
            SessionFetchError: If there's an error fetching the session
                (including a 404 when the session does not exist).
        """
        try:
            response = self.client.get(f"/v0.1/sessions/{session_id}")
            response.raise_for_status()
            return [Session.model_validate(item) for item in response.json()]
        except HTTPStatusError as e:
            _handle_session_http_errors(e, "fetching session", SessionFetchError)
        except SessionError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise SessionFetchError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aget_session(self, session_id: UUID) -> list[Session]:
        """Get all session rows for a given session id (async).

        See :meth:`get_session` for details.
        """
        try:
            response = await self.async_client.get(f"/v0.1/sessions/{session_id}")
            response.raise_for_status()
            return [Session.model_validate(item) for item in response.json()]
        except HTTPStatusError as e:
            _handle_session_http_errors(e, "fetching session", SessionFetchError)
        except SessionError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise SessionFetchError(f"An unexpected error occurred: {e!r}") from e


def _handle_session_http_errors(
    e: HTTPStatusError, operation: str, exc_class: type[SessionError] = SessionError
) -> NoReturn:
    """Handle common HTTP errors for session operations."""
    if e.response.status_code in RETRYABLE_HTTP_STATUS_CODES:
        raise e
    if e.response.status_code == codes.FORBIDDEN:
        raise exc_class(
            f"Error {operation}: {e.response.status_code} - {e.response.text}"
        ) from e
    if e.response.status_code == codes.UNPROCESSABLE_ENTITY:
        raise exc_class(f"Invalid request payload: {e.response.text}") from e
    raise exc_class(
        f"Error {operation}: {e.response.status_code} - {e.response.text}"
    ) from e
