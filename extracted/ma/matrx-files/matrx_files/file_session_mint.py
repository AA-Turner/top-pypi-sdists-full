"""Shared cookie creation for host-injected current-source authority."""

from __future__ import annotations

import asyncio
import json
import logging
import math
import time
from collections.abc import Awaitable, Callable

from fastapi import HTTPException
from starlette.responses import Response

from matrx_connect.context.app_context import AppContext
from matrx_connect.middleware.file_session import (
    FileSessionCredential,
    file_session_source_from_context,
    mint_bound_file_session_value,
)
from matrx_connect.middleware.session_authority import (
    SessionAuthorityUnavailable,
    session_unavailable_response,
)
from matrx_connect.middleware.session_cookie import (
    SESSION_COOKIE_TTL_SECONDS,
    get_session_cookie_secret,
    get_session_cookie_secret_source,
    mint_session_cookie_value,
    session_cookie_headers,
)

FileSessionSourceResolver = Callable[[AppContext], Awaitable[FileSessionCredential]]


def _check_binding(ctx: AppContext, user_id: str, credential: FileSessionCredential) -> None:
    if not isinstance(credential, FileSessionCredential) or credential.user_id != user_id:
        raise PermissionError("File-session source does not match admission")
    if ctx.user_id != user_id:
        raise PermissionError("File-session identity does not match admission")
    if ctx.auth_type == "fingerprint":
        if not ctx.fingerprint_id or credential.source_kind != "guest":
            raise PermissionError("File-session source does not match admission")
    else:
        expected = file_session_source_from_context(ctx)
        if (
            credential.source_kind != expected.source_kind
            or credential.source_id != expected.source_id
            or credential.expires_at > expected.expires_at
        ):
            raise PermissionError("File-session source does not match admission")


async def mint_file_session_response(
    user_id: str,
    *,
    context: AppContext | None = None,
    source_resolver: FileSessionSourceResolver | None = None,
    require_source: bool = False,
    include_secret_source: bool = True,
    timeout_seconds: float = 5.0,
) -> Response:
    """Mint paired cookies; enabled source policy never falls back to legacy v1."""
    if require_source or source_resolver is not None:
        if source_resolver is None:
            return session_unavailable_response()
        if not isinstance(context, AppContext) or context.user_id != user_id:
            raise HTTPException(401, detail={"code": "file_session_source_refused"}, headers={"Cache-Control": "no-store"})
        try:
            if not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
                raise RuntimeError("Invalid file-session authority deadline")
            async with asyncio.timeout(timeout_seconds):
                try:
                    credential = await source_resolver(context)
                except (asyncio.CancelledError, PermissionError):
                    raise
                except Exception as exc:
                    raise SessionAuthorityUnavailable(
                        "File-session source could not be checked"
                    ) from exc
            _check_binding(context, user_id, credential)
            now = time.time()
            ttl = math.floor(credential.expires_at - now)
            if ttl < 1:
                raise PermissionError("File-session source expired before mint")
            value = mint_bound_file_session_value(credential, get_session_cookie_secret(), now=now)
        except asyncio.CancelledError:
            raise
        except (PermissionError, ValueError):
            raise HTTPException(401, detail={"code": "file_session_source_refused"}, headers={"Cache-Control": "no-store"}) from None
        except Exception as exc:
            logging.getLogger(__name__).warning(
                "File-session mint authority unavailable (%s)", type(exc).__name__
            )
            return session_unavailable_response()
    else:
        ttl = SESSION_COOKIE_TTL_SECONDS
        value = mint_session_cookie_value(user_id, get_session_cookie_secret())
    body: dict[str, object] = {"ok": True, "expires_in": ttl}
    if include_secret_source:
        body["secret_source"] = get_session_cookie_secret_source()
    response = Response(
        content=json.dumps(body),
        media_type="application/json",
        headers={"Cache-Control": "no-store"},
    )
    for header in session_cookie_headers(value, ttl_seconds=ttl):
        response.headers.append("set-cookie", header)
    return response
