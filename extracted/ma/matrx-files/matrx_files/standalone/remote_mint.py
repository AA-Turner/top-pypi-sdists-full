"""Route-only cookie minting through an explicitly trusted identity authority."""
from __future__ import annotations

import asyncio
import logging
import math
import re
import time

from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from matrx_connect.middleware.authority_retry import REMOTE_AUTHORITY_TRY_SECONDS
from matrx_connect.middleware.file_session import classify_bound_file_session_value
from matrx_connect.middleware.remote_authority import (
    decode_authority_json,
    fetch_authority_response,
    validate_authority_url,
)
from matrx_connect.middleware.remote_file_session import RemoteFileSessionResolver
from matrx_connect.middleware.session_authority import SessionAuthorityUnavailable, session_unavailable_response
from matrx_connect.middleware.session_cookie import SESSION_COOKIE_NAME, SESSION_COOKIE_TTL_SECONDS, session_cookie_headers

MAX_AUTHORIZATION_BYTES = 8192
MAX_FINGERPRINT_BYTES = 512
MAX_COOKIE_HEADER_BYTES = 1024
_BEARER = re.compile(r"(?i:Bearer) ([!-~]+)\Z", re.ASCII)


def _refused() -> JSONResponse:
    return JSONResponse({"error": "file_session_source_refused"}, status_code=401, headers={"Cache-Control": "no-store"})


def _presented_credential(scope: Scope) -> tuple[dict[str, str], str] | None:
    authorizations = []
    fingerprints = []
    for name, value in scope.get("headers", []):
        if name.lower() == b"authorization":
            authorizations.append(value)
        elif name.lower() in {b"x-fingerprint-id", b"x-guest-fingerprint"}:
            fingerprints.append(value)
    if len(authorizations) + len(fingerprints) != 1:
        return None
    if authorizations:
        raw = authorizations[0]
        if len(raw) > MAX_AUTHORIZATION_BYTES:
            return None
        try:
            match = _BEARER.fullmatch(raw.decode("ascii"))
        except UnicodeDecodeError:
            return None
        if match is None:
            return None
        token = match[1]
        return {"Authorization": f"Bearer {token}"}, "api_key" if token.startswith("mx_") else "login"
    raw = fingerprints[0]
    if not raw or len(raw) > MAX_FINGERPRINT_BYTES or any(byte < 33 or byte > 126 for byte in raw):
        return None
    return {"X-Fingerprint-ID": raw.decode("ascii")}, "guest"


class RemoteFileSessionMint:
    """The configured main endpoint verifies/binds the presented credential.

    This adapter does not decode unverified JWT claims or duplicate a platform
    API-key parser. It checks the exact returned family, HMAC and fresh source.
    The issuer must resolve guests read-only; cookie bootstrap is not signup.
    """

    def __init__(
        self, mint_url: str | None, authority_url: str | None, signing_secret: bytes, *,
        timeout_seconds: float = REMOTE_AUTHORITY_TRY_SECONDS,
    ) -> None:
        # Each of the two remote calls (mint, then the source check) gets one full try that outlasts
        # aidream's own authority budget behind it; the whole mint is bounded by both plus headroom.
        # It was 5 s for both together and 3 s for the check (2026-10-21), so the mint gave up while
        # aidream was still inside its budget.
        self.mint_url = validate_authority_url(mint_url, timeout_seconds)
        self.timeout_seconds = timeout_seconds
        self.whole_seconds = 2 * timeout_seconds + 0.5
        self._authority = RemoteFileSessionResolver(authority_url, signing_secret, timeout_seconds=timeout_seconds)
        self._signing_secret = signing_secret

    async def __call__(self, scope: Scope) -> JSONResponse:
        presented = _presented_credential(scope)
        if presented is None or scope.get("query_string"):
            return _refused()
        headers, kind = presented
        try:
            async with asyncio.timeout(self.whole_seconds):
                response = await fetch_authority_response("POST", self.mint_url, headers, self.timeout_seconds)
                if response.status_code == 401:
                    return _refused()
                if response.status_code != 200:
                    raise SessionAuthorityUnavailable("File-session mint did not return a decision")
                body = decode_authority_json(response.body)
                if (
                    not isinstance(body, dict) or set(body) != {"ok", "expires_in"}
                    or body["ok"] is not True or type(body["expires_in"]) is not int
                    or not 0 < body["expires_in"] <= SESSION_COOKIE_TTL_SECONDS
                    or response.headers.get_list("cache-control") != ["no-store"]
                ):
                    raise SessionAuthorityUnavailable("File-session mint returned an inconsistent decision")
                cookies = response.headers.get_list("set-cookie")
                if len(cookies) != 2 or any(len(cookie) > MAX_COOKIE_HEADER_BYTES or not cookie.isascii() for cookie in cookies):
                    raise SessionAuthorityUnavailable("File-session mint returned inconsistent cookies")
                first = cookies[0].split(";", 1)[0]
                name, separator, value = first.partition("=")
                credential, _ = classify_bound_file_session_value(value, self._signing_secret)
                if (
                    name != SESSION_COOKIE_NAME or not separator or credential is None
                    or credential.source_kind != kind
                    or cookies != session_cookie_headers(value, ttl_seconds=body["expires_in"])
                ):
                    raise SessionAuthorityUnavailable("File-session mint returned inconsistent cookies")
                if await self._authority(credential) is not True:
                    return _refused()
                ttl = min(body["expires_in"], math.floor(credential.expires_at - time.time()))
                if ttl < 1:
                    return _refused()
                result = JSONResponse({"ok": True, "expires_in": ttl}, headers={"Cache-Control": "no-store"})
                for header in session_cookie_headers(value, ttl_seconds=ttl):
                    result.headers.append("set-cookie", header)
                return result
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logging.getLogger(__name__).warning("File-session mint authority unavailable (%s)", type(exc).__name__)
            return session_unavailable_response()


class RemoteFileSessionMintMiddleware:
    """Wrap local auth, inside CORS; all other operations retain their handler."""

    def __init__(self, app: ASGIApp, *, mint: RemoteFileSessionMint) -> None:
        self.app = app
        self.mint = mint

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http" and scope.get("method") == "POST" and scope.get("path") == "/files/session":
            response = await self.mint(scope)
            await response(scope, receive, send)
        else:
            await self.app(scope, receive, send)
