from __future__ import annotations

import base64
from datetime import datetime, timedelta, timezone
from json import JSONDecodeError
import threading
from typing import ClassVar, NoReturn, Optional
from urllib.parse import urljoin

from benchling_api_client.v2.benchling_client import AuthorizationMethod, BenchlingApiClient
import httpx

from benchling_sdk.errors import BenchlingError
from benchling_sdk.helpers.logging_helpers import sdk_logger

logger = sdk_logger.getChild(__name__)

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

    _data_for_token_request: ClassVar[dict] = {
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

        # Handle network-level failures (DNS, connection refused, timeout)
        try:
            response: httpx.Response = self.httpx_client.post(
                token_url,
                data=ClientCredentialsOAuth2._data_for_token_request,
                headers=self._header_for_token_request,
            )
        except httpx.InvalidURL as exc:
            detail = f"Invalid URL: {exc}"
            _raise_token_error(
                token_url=token_url,
                status_code=400,
                detail=detail,
                message=(
                    f"Failed to reach the Benchling token endpoint at {token_url}. {detail}. "
                    "Please verify the tenant URL is correct."
                ),
            )
        except httpx.UnsupportedProtocol as exc:
            detail = f"Unsupported protocol: {exc}"
            _raise_token_error(
                token_url=token_url,
                status_code=400,
                detail=detail,
                message=(
                    f"Failed to reach the Benchling token endpoint at {token_url}. {detail}. "
                    "Please verify the tenant URL is correct."
                ),
            )
        except httpx.RequestError as exc:
            detail = f"A network error occurred: {exc}"
            _raise_token_error(
                token_url=token_url,
                status_code=500,
                detail=detail,
                message=(
                    f"Failed to reach the Benchling token endpoint at {token_url}. {detail}. "
                    "Please verify the tenant URL is correct and the endpoint is reachable."
                ),
            )

        # Handle HTTP error responses
        if response.status_code >= 400:
            detail = _get_error_detail_from_response(response)
            _raise_error_from_response(
                response,
                token_url=token_url,
                detail=detail,
                message=(
                    f"OAuth token request to {token_url} failed with HTTP {response.status_code}: {detail}. "
                    "Please verify that the tenant URL is correct and the OAuth application credentials "
                    "(client_id / client_secret) are valid and have not been revoked."
                ),
            )

        # Handle malformed success responses (200 but unparseable body)
        try:
            as_json = response.json()
            self._token = Token.from_token_response(as_json)
        except (JSONDecodeError, ValueError, TypeError, KeyError, AssertionError) as exc:
            # Use generic detail to avoid leaking raw HTML from exception text
            detail = _get_parse_error_detail(response, exc)
            _raise_token_error(
                token_url=token_url,
                status_code=response.status_code,
                detail=detail,
                message=(
                    f"Received HTTP {response.status_code} from {token_url} but failed to parse the token response. "
                    f"{detail} The token endpoint may be returning an unexpected content type."
                ),
                headers=dict(response.headers),
                content=response.content,
            )

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


def _raise_token_error(
    *,
    token_url: str,
    status_code: int,
    detail: str,
    message: str,
    headers: Optional[dict] = None,
    json_content: Optional[dict] = None,
    content: Optional[bytes] = None,
) -> NoReturn:
    """
    Log and raise a BenchlingError for OAuth token vending failures.

    This is the single pattern for raising token-related errors, consolidating
    logging and error construction into one place.
    """
    _log_token_error(token_url=token_url, status_code=status_code, detail=detail)
    raise BenchlingError(
        status_code=status_code,
        headers=headers or {},
        json=json_content,
        content=content,
        parsed=None,
        message=message,
    )


def _raise_error_from_response(
    response: httpx.Response, *, token_url: str, detail: str, message: str
) -> NoReturn:
    """Raise a BenchlingError from an HTTP error response."""
    json_content = None
    # Rather than rely on Content-Type header, try to parse JSON
    # If the response isn't JSON, just swallow the exception
    try:
        json_content = response.json()
    except JSONDecodeError as e:
        sdk_logger.debug(
            "Received error response without JSON OAuth vending token",
            exc_info=e,
        )
    _raise_token_error(
        token_url=token_url,
        status_code=response.status_code,
        detail=detail,
        message=message,
        headers=dict(response.headers),
        json_content=json_content,
        content=response.content,
    )


def _log_token_error(*, token_url: str, status_code: int, detail: str) -> None:
    """Log a structured error for Datadog-compatible logging."""
    try:
        logger.error(
            "Benchling OAuth2 token request failed",
            extra={
                "dd": {"tag": "benchling.sdk.auth.token_vend_error"},
                "benchling.auth.token_url": token_url,
                "benchling.auth.status_code": status_code,
                "benchling.auth.error_detail": detail,
                "benchling.auth.client_id_prefix": "(redacted)",
            },
        )
    except Exception:
        # Logging must never mask the auth error
        pass


def _get_error_detail_from_response(response: httpx.Response) -> str:
    """Extract a human-readable error detail from an HTTP error response."""
    # Try to parse JSON and extract error details
    try:
        json_body = response.json()
        if isinstance(json_body, dict):
            # Check for error_description (OAuth2 standard)
            if "error_description" in json_body:
                return str(json_body["error_description"])
            # Check for message field
            if "message" in json_body:
                return str(json_body["message"])
            # Check for error.message (Benchling API format)
            error_obj = json_body.get("error")
            if isinstance(error_obj, dict):
                if "message" in error_obj:
                    return str(error_obj["message"])
    except (JSONDecodeError, ValueError, TypeError):
        pass

    # Detect HTML error pages (404/502 etc.)
    if _response_contains_html(response):
        return (
            "The token endpoint returned an HTML error page instead of a JSON response. "
            "This typically indicates the URL is incorrect or the tenant is unreachable."
        )

    # Fall back to HTTP reason phrase
    return response.reason_phrase or f"HTTP {response.status_code} error"


def _get_parse_error_detail(response: httpx.Response, exc: Exception) -> str:
    """Extract a sanitized error detail for parse failures, avoiding raw HTML leakage."""
    # Check if response contains HTML to avoid leaking it via exception text
    if _response_contains_html(response):
        return (
            "The token endpoint returned an HTML page instead of a JSON token response. "
            "This typically indicates the URL is incorrect or the tenant is unreachable."
        )
    # For non-HTML responses, we can safely include a generic error type
    return f"Parse error: {type(exc).__name__}."


def _response_contains_html(response: httpx.Response) -> bool:
    """Check if the response body contains HTML content."""
    content = response.content
    if not content:
        return False
    # Only inspect a small prefix to avoid decoding very large error pages
    content_prefix = content[:4096]
    try:
        content_str = content_prefix.decode("utf-8", errors="ignore").lower()
    except Exception:
        content_str = str(content_prefix).lower()
    return "<!doctype" in content_str or "<html" in content_str
