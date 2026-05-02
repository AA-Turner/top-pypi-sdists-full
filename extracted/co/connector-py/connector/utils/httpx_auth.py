from typing import Any

import httpx

from connector.oai.errors import MissingParameterError


class BearerAuth(httpx.Auth):
    """Authorization schema for authorization via token in header with default Bearer prefix."""

    def __init__(
        self,
        token: str,
        token_prefix: str = "Bearer",
        auth_header: str = "Authorization",
        custom_headers: dict[str, Any] | None = None,
    ) -> None:
        if custom_headers is None:
            custom_headers = {"Content-Type": "application/json"}

        if not token:
            raise MissingParameterError(
                message="Token credential is required and cannot be empty.",
            )

        self._token = token
        self._token_prefix = token_prefix
        self._auth_header = auth_header
        self._custom_headers = custom_headers

    def auth_flow(self, request: httpx.Request):
        request.headers[
            self._auth_header
        ] = f"{self._token_prefix}{' ' if self._token_prefix else ''}{self._token}"
        request.headers.update(self._custom_headers)
        yield request
