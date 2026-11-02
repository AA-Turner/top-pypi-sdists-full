import logging
from collections.abc import Collection, Generator
from typing import ClassVar

import httpx

from edison_client.models.app import APIKeyPayload, AuthType

logger = logging.getLogger(__name__)

JWT_TOKEN_CACHE_EXPIRY: int = 300  # seconds


def _run_auth(
    client: httpx.Client,
    auth_type: AuthType = AuthType.API_KEY,
    api_key: str | None = None,
    jwt: str | None = None,
) -> str:
    auth_payload: APIKeyPayload | None
    if auth_type == AuthType.API_KEY:
        if api_key is None:
            raise ValueError("API key required for API key authentication.")
        auth_payload = APIKeyPayload(api_key=api_key)
    elif auth_type == AuthType.JWT:
        auth_payload = None
    try:
        if auth_payload:
            response = client.post("/auth/login", json=auth_payload.model_dump())
            response.raise_for_status()
            token_data = response.json()
            return token_data["access_token"]
        if jwt:
            return jwt
        raise ValueError("JWT token required for JWT authentication.")
    except Exception as e:
        raise Exception("Failed to authenticate") from e  # noqa: TRY002


class RefreshingJWT(httpx.Auth):
    """Automatically (re-)inject a JWT and transparently retry exactly once when we hit a 401/403."""

    RETRY_STATUSES: ClassVar[Collection[httpx.codes]] = {
        httpx.codes.UNAUTHORIZED,
        httpx.codes.FORBIDDEN,
    }

    def __init__(
        self,
        auth_client: httpx.Client,
        auth_type: AuthType = AuthType.API_KEY,
        api_key: str | None = None,
        jwt: str | None = None,
    ):
        self.auth_type = auth_type
        self.auth_client = auth_client
        self.api_key = api_key
        self._jwt = _run_auth(
            client=auth_client,
            jwt=jwt,
            auth_type=auth_type,
            api_key=api_key,
        )

    def refresh_token(self) -> None:
        self._jwt = _run_auth(
            client=self.auth_client,
            auth_type=self.auth_type,
            api_key=self.api_key,
        )

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        request.headers["Authorization"] = f"Bearer {self._jwt}"
        response = yield request

        # jwt auth has no way to mint a new token; let the original error propagate
        if self.auth_type == AuthType.JWT:
            return

        # If it failed, refresh once and replay the request
        if response.status_code in self.RETRY_STATUSES:
            logger.info(
                "Received %s for request [%s %s], refreshing token and retrying …",
                response.status_code,
                request.method,
                request.url,
            )
            self.refresh_token()
            request.headers["Authorization"] = f"Bearer {self._jwt}"
            yield request  # second (and final) attempt, again or use a while loop
