"""Current-session authority for hosts without access to the identity database."""

from __future__ import annotations

import time
from uuid import UUID

from .auth import VerifiedToken
from .authority_retry import REMOTE_AUTHORITY_TRY_SECONDS
from .remote_authority import fetch_authority_decision, validate_authority_url
from .session_authority import SessionAuthorityUnavailable


class RemoteSessionResolver:
    """Check the exact presented session at an explicitly trusted HTTPS endpoint."""

    def __init__(self, authority_url: str | None, *, timeout_seconds: float = REMOTE_AUTHORITY_TRY_SECONDS) -> None:
        self.authority_url = validate_authority_url(authority_url, timeout_seconds)
        self.timeout_seconds = timeout_seconds
        # The caller's per-attempt deadline must not fire before this request's own does.
        self.attempt_seconds = timeout_seconds + 0.5

    async def __call__(self, verified: VerifiedToken) -> bool:
        decided, result = await fetch_authority_decision(
            self.authority_url, f"Bearer {verified.token}", self.timeout_seconds
        )
        if not decided:
            return False
        try:
            matches = self._matches(result, verified)
        except ValueError as exc:
            raise SessionAuthorityUnavailable("Session authority could not be checked") from exc
        if not matches:
            raise SessionAuthorityUnavailable("Session authority returned an inconsistent decision")
        return True

    @staticmethod
    def _matches(result: object, verified: VerifiedToken) -> bool:
        if not isinstance(result, dict) or set(result) != {"user_id", "session_id", "expires_at"}:
            return False
        subject, session, expiry = result["user_id"], result["session_id"], result["expires_at"]
        if not isinstance(subject, str) or not isinstance(session, str):
            return False
        return (
            str(UUID(subject)) == subject == verified.user_id
            and str(UUID(session)) == session == verified.claims.get("session_id")
            and type(expiry) is int
            and type(verified.expires_at) is int
            and expiry == verified.expires_at
            and expiry > time.time()
        )
