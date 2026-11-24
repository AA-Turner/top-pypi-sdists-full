"""A refused sign-in says WHY — still the same 401 and error code (2026-11-09).

Live: REST v1 answered "Authentication required. Please sign in." to a script whose admin@admin.com session had been
ended by another agent's second-factor verify (every verify ends that account's password-only sessions), and to a
token simply past its expiry. Both read as "you are not signed in", so callers concluded they lacked access. Now the
401 carries ``reason`` (``expired`` / ``session_ended``) and a sentence saying what to do; an unreadable token stays
the bare refusal, and nothing is admitted that was refused before.
"""

from __future__ import annotations

import time

import jwt
import pytest
from fastapi import HTTPException
from matrx_connect.dependencies import require_authenticated
from matrx_connect.middleware.auth import AuthMiddleware

SECRET = "s" * 64
USER = "11111111-1111-4111-8111-111111111111"


def _token(exp_offset: int) -> str:
    now = int(time.time())
    return jwt.encode(
        {"sub": USER, "role": "authenticated", "session_id": "22222222-2222-4222-8222-222222222222",
         "iat": now - 10, "exp": now + exp_offset, "aud": "authenticated"},
        SECRET, algorithm="HS256",
    )


class _App:
    context = None

    async def __call__(self, scope, receive, send) -> None:
        self.context = (scope.get("state") or {}).get("context")
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"ok"})


async def _context(token: str, *, session_active: bool = True):
    async def current_session(_verified):
        return session_active

    app = _App()
    mw = AuthMiddleware(app, jwt_secret=SECRET, log_requests=False, resolve_current_session=current_session)
    scope = {"type": "http", "method": "GET", "path": "/v1/tables", "query_string": b"",
             "headers": [(b"authorization", f"Bearer {token}".encode())], "client": ("127.0.0.1", 1), "state": {}}

    async def receive() -> dict:
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(_message: dict) -> None:
        return None

    await mw(scope, receive, send)
    return app.context


async def _refusal(ctx) -> dict:
    request = type("R", (), {"state": type("S", (), {"context": ctx})()})()
    with pytest.raises(HTTPException) as refused:
        await require_authenticated(request)
    assert refused.value.status_code == 401
    return refused.value.detail


@pytest.mark.asyncio
async def test_an_expired_token_says_it_expired() -> None:
    ctx = await _context(_token(-60))
    assert not ctx.is_authenticated
    detail = await _refusal(ctx)
    assert detail["error"] == "token_required" and detail["reason"] == "expired"
    assert "expired" in detail["user_message"]


@pytest.mark.asyncio
async def test_an_ended_session_says_its_session_ended() -> None:
    ctx = await _context(_token(3600), session_active=False)
    assert not ctx.is_authenticated
    detail = await _refusal(ctx)
    assert detail["error"] == "token_required" and detail["reason"] == "session_ended"


@pytest.mark.asyncio
async def test_a_live_session_is_still_admitted_and_garbage_says_it_was_not_accepted() -> None:
    # The same middleware still admits a live token (the organization gate after it is not this test's concern).
    async def current_session(_verified):
        return True

    mw = AuthMiddleware(_App(), jwt_secret=SECRET, log_requests=False, resolve_current_session=current_session)
    verified = await mw.verify_token_raw(_token(3600))
    assert verified is not None and verified.user_id == USER
    # A presented-and-refused credential always says so (2026-11-12): a bare "token required" to a caller that
    # SENT one read as "send a header" (action-requests complete, 8 refusals 2026-11-06 with no reason kept).
    garbage = await _context("not-a-jwt")
    assert not garbage.is_authenticated
    detail = await _refusal(garbage)
    assert detail["error"] == "token_required" and detail["reason"] == "not_accepted"
    assert "not accepted" in detail["user_message"]
