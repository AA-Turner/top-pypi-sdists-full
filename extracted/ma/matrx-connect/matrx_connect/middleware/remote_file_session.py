"""Exact current-source introspection for hosts sharing the file signing key."""

from __future__ import annotations

import time
from dataclasses import asdict

from .file_session import FileSessionCredential, mint_bound_file_session_value
from .authority_retry import REMOTE_AUTHORITY_TRY_SECONDS
from .remote_authority import fetch_authority_decision, validate_authority_url
from .session_authority import SessionAuthorityUnavailable


class RemoteFileSessionResolver:
    """Admission callback for a locally HMAC-verified source-bound credential.

    A host passes its explicit stable shared signing key. Re-signing the exact
    binding reconstructs the original deterministic v2 value; the authority
    verifies that signature and rechecks the source, rather than trusting IDs.
    """

    def __init__(self, authority_url: str | None, signing_secret: bytes, *, timeout_seconds: float = REMOTE_AUTHORITY_TRY_SECONDS) -> None:
        if not isinstance(signing_secret, bytes) or not signing_secret:
            raise ValueError("File-session authority requires an explicit shared signing key")
        self.authority_url = validate_authority_url(authority_url, timeout_seconds)
        self.timeout_seconds = timeout_seconds
        # The caller's per-attempt deadline must not fire before this request's own does.
        self.attempt_seconds = timeout_seconds + 0.5
        self._signing_secret = signing_secret

    async def __call__(self, credential: FileSessionCredential) -> bool:
        try:
            value = mint_bound_file_session_value(credential, self._signing_secret)
        except ValueError:
            return False
        decided, result = await fetch_authority_decision(
            self.authority_url, f"FileSession {value}", self.timeout_seconds
        )
        if not decided:
            return False
        if (
            not isinstance(result, dict)
            or result != asdict(credential)
            or type(result.get("expires_at")) is not int
        ):
            raise SessionAuthorityUnavailable("File-session authority returned an inconsistent decision")
        return credential.expires_at > time.time()
