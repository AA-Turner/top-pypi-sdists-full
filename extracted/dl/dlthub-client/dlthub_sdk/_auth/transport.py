"""Transport: the only layer that touches the generated auth client.

Each method is one request and one result. Nothing here loops, sleeps, prints,
or opens a browser — a device flow is driven by its caller, which is the only
side that knows how long a human should be kept waiting.
"""

from __future__ import annotations

# Python internals
from typing import Any, Callable, TypeVar

# Other libraries
import httpx

# Current package
from dlthub_sdk._auth.types import DeviceFlowStart, Pending, Tokens
from dlthub_sdk._gen.auth.api.default import create_session_swap_code, refresh
from dlthub_sdk._gen.auth.api.workos import (
    workos_auth_code_exchange,
    workos_auth_code_start,
    workos_device_flow_complete,
    workos_device_flow_start,
)
from dlthub_sdk._gen.auth.client import Client as AuthClient
from dlthub_sdk._gen.auth.errors import UnexpectedStatus
from dlthub_sdk._gen.auth.models import (
    LoginResponse,
    RefreshRequest,
    RefreshResponse,
    SwapCodeRequest,
    SwapCodeResponse,
    WorkosAuthCodeExchangeRequest,
    WorkosAuthCodeStartRequest,
    WorkosAuthCodeStartResponse,
    WorkosDeviceFlowLoginRequest,
    WorkosDeviceFlowStartResponse,
)
from dlthub_sdk.errors import (
    ApiError,
    BadRequest,
    ConnectionFailed,
    InvalidResponse,
    NotAuthenticated,
    ServerError,
    TransportTimeout,
)

T = TypeVar("T")

#: While a device code is neither approved nor rejected the service answers 403,
#: which the generated client raises because no model is declared for it.
_PENDING_STATUS = 403


class AuthTransport:
    """Calls the auth service. Holds no token: these calls are how you get one."""

    def __init__(
        self,
        base_url: str,
        *,
        headers: dict[str, str] | None = None,
        verify_ssl: bool = True,
    ) -> None:
        """Build a transport against one auth service.

        Args:
            base_url: The auth service's base URL.
            headers: Sent with every request. The caller owns what goes in here;
                the SDK adds nothing of its own.
            verify_ssl: Whether to verify the service's certificate.
        """
        # Undeclared statuses must raise rather than parse to None, so the
        # device flow's pending 403 stays distinguishable from a failure.
        self._client = AuthClient(
            base_url=base_url,
            headers=headers or {},
            verify_ssl=verify_ssl,
            raise_on_unexpected_status=True,
        )

    def device_flow_start(self) -> DeviceFlowStart:
        """Begin a device-code login.

        Returns:
            The codes and URLs to show a human, and how often to poll.

        Raises:
            ApiError: The service refused to start a flow.
        """
        parsed = _unwrap(
            _call(lambda: workos_device_flow_start.sync_detailed(client=self._client)),
            WorkosDeviceFlowStartResponse,
        )
        return DeviceFlowStart(
            device_code=parsed.device_code,
            user_code=parsed.user_code,
            verification_uri=parsed.verification_uri,
            verification_uri_complete=parsed.verification_uri_complete,
            interval=parsed.interval,
        )

    def device_flow_complete(self, *, device_code: str) -> Tokens | Pending:
        """Ask once whether a device code has been approved.

        Args:
            device_code: From :meth:`device_flow_start`.

        Returns:
            The tokens once approved, or :class:`~dlthub_sdk._auth.types.Pending`
            while nobody has approved it yet.

        Raises:
            ApiError: The code was rejected, or has expired.
        """
        resp = _call_pollable(
            lambda: workos_device_flow_complete.sync_detailed(
                client=self._client,
                body=WorkosDeviceFlowLoginRequest(device_code=device_code),
            ),
        )
        if isinstance(resp, Pending):
            return resp
        login = _unwrap(resp, LoginResponse)
        return Tokens(access_token=login.jwt, refresh_token=login.refresh_token)

    def auth_code_start(
        self, *, redirect_uri: str, code_challenge: str, state: str
    ) -> str:
        """Ask for the authorization URL a browser should be sent to.

        Args:
            redirect_uri: Where the browser comes back to.
            code_challenge: The PKCE challenge.
            state: Opaque value echoed back, to tie the callback to this attempt.

        Returns:
            The absolute authorization URL.

        Raises:
            ApiError: The service refused to start a flow.
        """
        parsed = _unwrap(
            _call(
                lambda: workos_auth_code_start.sync_detailed(
                    client=self._client,
                    body=WorkosAuthCodeStartRequest(
                        redirect_uri=redirect_uri,
                        code_challenge=code_challenge,
                        state=state,
                    ),
                )
            ),
            WorkosAuthCodeStartResponse,
        )
        return parsed.authorization_url

    def auth_code_exchange(self, *, code: str, code_verifier: str) -> Tokens:
        """Trade an authorization code for tokens.

        Args:
            code: The code the callback carried.
            code_verifier: The PKCE verifier matching the challenge.

        Returns:
            The tokens.

        Raises:
            ApiError: The code or verifier was rejected.
        """
        login = _unwrap(
            _call(
                lambda: workos_auth_code_exchange.sync_detailed(
                    client=self._client,
                    body=WorkosAuthCodeExchangeRequest(
                        code=code, code_verifier=code_verifier
                    ),
                )
            ),
            LoginResponse,
        )
        return Tokens(access_token=login.jwt, refresh_token=login.refresh_token)

    def refresh(self, *, refresh_token: str) -> Tokens | None:
        """Exchange a refresh token for a fresh pair.

        Args:
            refresh_token: The stored refresh token.

        Returns:
            The new pair, or ``None`` when the service rejected the token —
            expired, revoked, or already used. A rejection is an answer, not a
            failure; anything else raises.

        Raises:
            ApiError: The service failed for a reason other than rejection.
        """
        resp = _call(
            lambda: refresh.sync_detailed(
                client=self._client, body=RefreshRequest(refresh_token=refresh_token)
            )
        )
        if not isinstance(resp.parsed, RefreshResponse):
            return None
        return Tokens(
            access_token=resp.parsed.jwt, refresh_token=resp.parsed.refresh_token
        )

    def create_session_swap_code(self, *, refresh_token: str) -> str | None:
        """Mint a single-use code that signs the web app into this session.

        Args:
            refresh_token: The stored refresh token.

        Returns:
            The swap code, or ``None`` when the service rejected the token.

        Raises:
            ApiError: The service failed for a reason other than rejection.
        """
        resp = _call(
            lambda: create_session_swap_code.sync_detailed(
                client=self._client, body=SwapCodeRequest(refresh_token=refresh_token)
            )
        )
        if not isinstance(resp.parsed, SwapCodeResponse):
            return None
        return resp.parsed.swap_code


def _call(op: Callable[[], T]) -> T:
    """Run one generated operation, turning every failure into an SDK error.

    Args:
        op: Calls the generated operation.

    Returns:
        Its response.

    Raises:
        TransportTimeout: The request timed out.
        ConnectionFailed: The service could not be reached.
        ApiError: The service answered a status the operation does not declare.
    """
    try:
        return op()
    except UnexpectedStatus as e:
        raise _status_error(int(e.status_code), None) from e
    except httpx.TimeoutException as e:
        raise TransportTimeout(f"auth service timed out: {e}") from e
    except httpx.HTTPError as e:
        raise ConnectionFailed(f"auth service could not be reached: {e}") from e


def _call_pollable(op: Callable[[], T]) -> T | Pending:
    """Run an operation whose "not finished yet" answer is a status, not a body.

    Args:
        op: Calls the generated operation.

    Returns:
        Its response, or :class:`~dlthub_sdk._auth.types.Pending`.

    Raises:
        ApiError: The service answered any other undeclared status.
    """
    try:
        return op()
    except UnexpectedStatus as e:
        if int(e.status_code) == _PENDING_STATUS:
            return Pending()
        raise _status_error(int(e.status_code), None) from e
    except httpx.TimeoutException as e:
        raise TransportTimeout(f"auth service timed out: {e}") from e
    except httpx.HTTPError as e:
        raise ConnectionFailed(f"auth service could not be reached: {e}") from e


def _unwrap(resp: Any, model: type[T]) -> T:
    """Return the success model off a generated response, or raise.

    Args:
        resp: The generated ``Response``.
        model: The success model this operation declares.

    Returns:
        The parsed success model.

    Raises:
        ApiError: The service answered with an error status.
        InvalidResponse: A success status whose body did not parse.
    """
    if isinstance(resp.parsed, model):
        return resp.parsed
    raise _status_error(int(resp.status_code), resp.parsed)


def _status_error(status: int, parsed: object) -> ApiError | NotAuthenticated:
    """Map an auth-service status onto an SDK error.

    Args:
        status: The HTTP status.
        parsed: The parsed error model, when there was one.

    Returns:
        The error to raise.
    """
    detail = getattr(parsed, "detail", None) or getattr(parsed, "message", None)
    text = str(detail) if detail else f"auth service returned {status}"
    if status == 401:
        return NotAuthenticated(text, status=status)
    if status == 400:
        return BadRequest(text, status=status)
    if status >= 500:
        return ServerError(text, status=status)
    if 200 <= status < 300:
        return InvalidResponse(f"auth service returned an unreadable {status} body")
    return ApiError(text, status=status)
