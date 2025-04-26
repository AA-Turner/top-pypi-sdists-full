from __future__ import annotations

import base64
from datetime import datetime, timedelta, timezone
from json import JSONDecodeError
import threading
import typing
from typing import NoReturn, Optional
from urllib.parse import urljoin

from benchling_api_client.v2.benchling_client import AuthorizationMethod, BenchlingApiClient
import httpx

from benchling_sdk.errors import BenchlingError
from benchling_sdk.helpers.logging_helpers import sdk_logger

MINIMUM_TOKEN_EXPIRY_BUFFER = 60


class Token:
    """Represents an OAuth2 token response model."""

    def __init__(self, access_token: str, refresh_time: datetime):
        """
        Initialize Token.

        :param access_token: The raw token value for authorizing with the API
        :param refresh_time: Calculated value off of token time-to-live for when a new token should be generated.
        """
        self.access_token = access_token
        self.refresh_time = refresh_time

    def valid(self) -> bool:
        """Return whether token is still valid for use or should be regenerated."""
        return datetime.now(timezone.utc) < self.refresh_time

    @classmethod
    def from_token_response(cls, token_response) -> Token:
        """
        Construct Token from deserializing token endpoint response.

        Deserializes response from token endpoint and calculates expiry time with buffer for when token should be
        regenerated.

        :param token_response: The response from an RFC6749 POST /token endpoint.
        """
        token_type: str = token_response.get("token_type")
        access_token: str = token_response.get("access_token")
        expires_in: float = token_response.get("expires_in")
        assert token_type == "Bearer"
        # Add in a buffer to safeguard against race conditions with token expiration.
        # Buffer is 10% of expires_in time, clamped between [1, MINIMUM_TOKEN_EXPIRY_BUFFER] seconds.
        refresh_delta = expires_in - max(1, min(MINIMUM_TOKEN_EXPIRY_BUFFER, expires_in * 0.1))
        refresh_time = datetime.now(timezone.utc) + timedelta(seconds=refresh_delta)
        return cls(access_token, refresh_time)


class ClientCredentialsOAuth2(AuthorizationMethod):
    """
    OAuth2 client credentials for authorization.

    Use in combination with the Benchling() client constructor to be authorized with OAuth2 client_credentials grant
    type.
    """

    _data_for_token_request: typing.ClassVar[dict] = {
        "grant_type": "client_credentials",
    }

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        token_url: Optional[str] = None,
        httpx_client: Optional[httpx.Client] = None,
    ):
        """
        Initialize ClientCredentialsOAuth2.

        :param client_id: Client id in client_credentials grant type
        :param client_secret: Client secret in client_credentials grant type
        :param token_url: A fully-qualified URL pointing at the access token request endpoint such as
                          https://benchling.com/api/v2/token. Can be omitted to default to /api/v2/token appended to
                          the server base URL.
        :param httpx_client: An optional httpx Client which will be used to execute HTTP calls. The Client can be used
                             to modify the behavior of the HTTP calls made to Benchling through means such as adding
                             proxies and certificates or introducing retry logic for transport-level errors.
        """
        self._token_url = token_url
        token_encoded = base64.b64encode(f"{client_id}:{client_secret}".encode())
        self._header_for_token_request = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {token_encoded.decode()}",
            "User-Agent": BenchlingApiClient._get_user_agent("BenchlingSDK", "benchling-sdk"),
        }
        self._token: Optional[Token] = None
        self._lock = threading.Lock()
        if not httpx_client:
            httpx_client = httpx.Client()
        self.httpx_client = httpx_client

    def vend_new_token(self, base_url: str):
        """Make RFC6749 request to token URL to generate a new bearer token for client credentials OAuth2 flow."""
        token_url = self._token_url if self._token_url is not None else urljoin(base_url, "/api/v2/token")
        response: httpx.Response = self.httpx_client.post(
            token_url,
            data=ClientCredentialsOAuth2._data_for_token_request,
            headers=self._header_for_token_request,
        )

        if response.status_code == 200:
            as_json = response.json()
            self._token = Token.from_token_response(as_json)
        else:
            _raise_error_from_response(response)

    def get_authorization_header(self, base_url: str) -> str:
        """
        Generate HTTP Authorization request header.

        If a token has not yet been requested or is close to its expiry time, a new token is requested.
        Otherwise, re-use existing valid token.
        """
        with self._lock:
            if self._token is None or not self._token.valid():
                self.vend_new_token(base_url)
        assert self._token is not None
        return f"Bearer {self._token.access_token}"


def _raise_error_from_response(response: httpx.Response) -> NoReturn:
    json_content = None
    # Rather than rely on Content-Type header, try to parse JSON
    # If the response isn't JSON, just swallow the exception
    try:
        json_content = response.json()
    except JSONDecodeError as e:
        sdk_logger.debug("Received error response without JSON OAuth vending token", e)
    raise BenchlingError(
        status_code=response.status_code,
        headers=response.headers,
        json=json_content,
        content=response.content,
        parsed=None,
    )
