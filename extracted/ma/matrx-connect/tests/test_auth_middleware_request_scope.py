"""The request-scope hook: a host declares request-wide facts ONCE, at the
boundary that knows the caller, and every handler inherits them.

Locked-in behaviors:

* the hook is called with the ADMITTED context (identity settled) and its
  context manager is entered around the downstream app, in the request's own
  task — a ContextVar it sets is visible inside the app and reset after
* a hook returning None declares nothing (anonymous callers)
* no hook configured ⇒ no behavior change (standalone matrx-connect)
* a refused request (organization mismatch) never enters the hook
"""

from __future__ import annotations

import time
from contextlib import asynccontextmanager
from contextvars import ContextVar

import jwt
import pytest
from matrx_connect.middleware.auth import ApiKeyIdentity, AuthMiddleware

JWT_SECRET = "test-secret-do-not-use-in-prod-test-secret-do-not-use-in-prod-AB"
JWT_USER_ID = "11111111-1111-4111-8111-111111111111"
SERVICE_USER_ID = "22222222-2222-4222-8222-222222222222"
ORG_ID = "33333333-3333-4333-8333-333333333333"
GOOD_KEY = "mx_live_abc123DEF456_" + "s" * 43

_declared: ContextVar[str | None] = ContextVar("_test_declared", default=None)


async def _resolver(token: str) -> ApiKeyIdentity | None:
    if token == GOOD_KEY:
        return ApiKeyIdentity(user_id=SERVICE_USER_ID, organization_id=ORG_ID, key_name="ci-key")
    return None


class _App:
    def __init__(self) -> None:
        self.seen_inside: str | None = "unset"
        self.context = None

    async def __call__(self, scope, receive, send) -> None:
        self.context = (scope.get("state") or {}).get("context")
        self.seen_inside = _declared.get()
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"ok"})


def _scope(headers: dict[str, str]) -> dict:
    return {
        "type": "http",
        "method": "GET",
        "path": "/auth/whoami",
        "query_string": b"",
        "headers": [(k.lower().encode(), v.encode()) for k, v in headers.items()],
        "client": ("127.0.0.1", 12345),
        "state": {},
    }


async def _receive() -> dict:
    return {"type": "http.request", "body": b"", "more_body": False}


async def _call(mw: AuthMiddleware, headers: dict[str, str]) -> int:
    sent: list[dict] = []

    async def send(message: dict) -> None:
        sent.append(message)

    await mw(_scope(headers), _receive, send)
    return next(m["status"] for m in sent if m["type"] == "http.response.start")


def _jwt() -> str:
    now = int(time.time())
    return jwt.encode(
        {"sub": JWT_USER_ID, "aud": "authenticated", "iat": now, "exp": now + 3600},
        JWT_SECRET,
        algorithm="HS256",
    )


def _hook_calls() -> tuple[list, object]:
    calls: list = []

    def hook(ctx):
        calls.append(ctx)
        if not ctx.user_id:
            return None

        @asynccontextmanager
        async def scope():
            token = _declared.set(f"{ctx.auth_type}:{ctx.user_id}")
            try:
                yield
            finally:
                _declared.reset(token)

        return scope()

    return calls, hook


@pytest.mark.asyncio
async def test_hook_receives_admitted_context_and_wraps_the_app() -> None:
    calls, hook = _hook_calls()
    app = _App()
    mw = AuthMiddleware(
        app, jwt_secret=JWT_SECRET, resolve_api_key=_resolver, request_scope=hook, log_requests=False
    )

    assert await _call(mw, {"authorization": f"Bearer {_jwt()}"}) == 200
    assert calls[-1].user_id == JWT_USER_ID and calls[-1].auth_type == "token"
    assert app.seen_inside == f"token:{JWT_USER_ID}"
    assert _declared.get() is None, "the declaration must not leak past the request"

    assert await _call(mw, {"authorization": f"Bearer {GOOD_KEY}"}) == 200
    assert calls[-1].auth_type == "api_key"
    assert app.seen_inside == f"api_key:{SERVICE_USER_ID}"
    assert _declared.get() is None


@pytest.mark.asyncio
async def test_hook_returning_none_declares_nothing() -> None:
    calls, hook = _hook_calls()
    app = _App()
    mw = AuthMiddleware(app, jwt_secret=JWT_SECRET, request_scope=hook, log_requests=False)
    assert await _call(mw, {}) == 200
    assert calls[-1].user_id == "" and calls[-1].is_authenticated is False
    assert app.seen_inside is None


@pytest.mark.asyncio
async def test_no_hook_is_no_behaviour_change() -> None:
    app = _App()
    mw = AuthMiddleware(app, jwt_secret=JWT_SECRET, log_requests=False)
    assert await _call(mw, {"authorization": f"Bearer {_jwt()}"}) == 200
    assert app.context.user_id == JWT_USER_ID
    assert app.seen_inside is None


@pytest.mark.asyncio
async def test_refused_request_never_enters_the_hook() -> None:
    calls, hook = _hook_calls()
    app = _App()
    mw = AuthMiddleware(
        app, jwt_secret=JWT_SECRET, resolve_api_key=_resolver, request_scope=hook, log_requests=False
    )
    other_org = "44444444-4444-4444-8444-444444444444"
    status = await _call(mw, {"authorization": f"Bearer {GOOD_KEY}", "x-organization-id": other_org})
    assert status == 409
    assert calls == []
