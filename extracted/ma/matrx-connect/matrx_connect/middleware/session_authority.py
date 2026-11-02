"""Transport-neutral credential-authority failures and their outer ASGI mapping."""

from __future__ import annotations

from dataclasses import dataclass

from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Scope, Receive, Send, Message


class CredentialAuthorityUnavailable(RuntimeError):
    """A credential's current authority is unreadable; preserve retry semantics."""

    code = "credential_authority_unavailable"
    public_message = "Could not verify your credentials. Please retry."


class SessionAuthorityUnavailable(CredentialAuthorityUnavailable):
    """Current login authority could not be checked; do not turn this into logout."""

    code = "session_authority_unavailable"
    public_message = "Could not verify your session. Please retry."


@dataclass(frozen=True)
class CurrentSessionDecision:
    """Fresh login and human-admin authority, separate from cached JWT crypto.

    A login-only authority cannot grant admin power. Keep current membership
    only as challenge context when assurance is insufficient.
    """

    active: bool
    current_admin_level: str | None
    admin_admitted: bool
    mfa_required: bool | None
    reason: str

    def __post_init__(self) -> None:
        if (
            type(self.active) is not bool
            or type(self.admin_admitted) is not bool
            or (
                self.current_admin_level is not None
                and not isinstance(self.current_admin_level, str)
            )
            or self.current_admin_level not in {None, "developer", "senior_admin", "super_admin"}
            or (self.mfa_required is not None and type(self.mfa_required) is not bool)
            or not isinstance(self.reason, str)
            or not self.reason
            or len(self.reason) > 64
            or (
                self.admin_admitted
                and (
                    not self.active or self.current_admin_level is None or self.mfa_required is None
                )
            )
        ):
            raise ValueError("Invalid current-session authority decision")


class ApiKeyAuthorityUnavailable(CredentialAuthorityUnavailable):
    """Current key, organization or personal-account authority is unreadable."""

    code = "api_key_authority_unavailable"
    public_message = "Could not verify your API key. Please retry."


def credential_unavailable_response(error: CredentialAuthorityUnavailable) -> JSONResponse:
    return JSONResponse(
        {
            "error": error.code,
            "code": error.code,
            "message": error.public_message,
            "retryable": True,
        },
        status_code=503,
        headers={"Retry-After": "1", "Cache-Control": "no-store"},
    )


def session_unavailable_response() -> JSONResponse:
    """Compatibility response for existing current-login adapters."""
    return credential_unavailable_response(SessionAuthorityUnavailable())


class SessionAuthorityUnavailableMiddleware:
    """Outside SDK authentication middleware, preserve outages as retryable 503s."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        started = False

        async def track_send(message: Message) -> None:
            nonlocal started
            if message["type"] in {"http.response.start", "websocket.accept"}:
                started = True
            await send(message)

        try:
            await self.app(scope, receive, track_send)
        except CredentialAuthorityUnavailable as error:
            if scope["type"] != "http" or started:
                raise
            await credential_unavailable_response(error)(scope, receive, send)
