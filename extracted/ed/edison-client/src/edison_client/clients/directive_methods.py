import logging
from typing import NoReturn

from httpx import AsyncClient, Client, HTTPStatusError
from tenacity import (
    before_sleep_log,
    retry,
    stop_after_attempt,
    wait_exponential,
)

from edison_client.models.directive import DirectiveResolveResponse
from edison_client.utils.general import (
    _BASE_CONNECTION_ERRORS,
    RETRYABLE_HTTP_STATUS_CODES,
    retry_if_connection_error,
)

logger = logging.getLogger(__name__)

_RESOLVE_URL = "/v0.1/directives/resolve"


class DirectiveResolveError(Exception):
    pass


class DirectiveMethods:
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
    def resolve_directives(
        self,
        *,
        profile_key: str,
    ) -> DirectiveResolveResponse:
        try:
            response = self.client.post(_RESOLVE_URL, json=_payload(profile_key))
            response.raise_for_status()
            return DirectiveResolveResponse.model_validate(response.json())
        except HTTPStatusError as e:
            _handle_directive_http_errors(e)
        except DirectiveResolveError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise DirectiveResolveError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aresolve_directives(
        self,
        *,
        profile_key: str,
    ) -> DirectiveResolveResponse:
        try:
            response = await self.async_client.post(
                _RESOLVE_URL, json=_payload(profile_key)
            )
            response.raise_for_status()
            return DirectiveResolveResponse.model_validate(response.json())
        except HTTPStatusError as e:
            _handle_directive_http_errors(e)
        except DirectiveResolveError:
            raise
        except Exception as e:
            if isinstance(e, _BASE_CONNECTION_ERRORS):
                raise
            raise DirectiveResolveError(f"An unexpected error occurred: {e!r}") from e


def _payload(profile_key: str) -> dict:
    return {"profile_key": profile_key}


def _handle_directive_http_errors(e: HTTPStatusError) -> NoReturn:
    if e.response.status_code in RETRYABLE_HTTP_STATUS_CODES:
        raise e
    raise DirectiveResolveError(
        f"Error resolving directives: {e.response.status_code} - {e.response.text}"
    ) from e
