"""The WebSocket lane gets the SAME organization admission as HTTP.

Before this change, ``AuthMiddleware.__call__`` had a dedicated early return
for ``scope["type"] == "websocket"`` that called straight into ``self.app``
without ever building an ``AppContext`` — no identity resolution, no
organization check, for ANY WebSocket connection on ANY host. The HTTP
admission gate (``_organization_admission_failure`` / API-T03) was therefore
a complete no-op for every WS endpoint in the system (cloud_browser,
google_specialized realtime, conversation_relay) — an authenticated caller
with no organization sailed straight through.

These tests lock the parity:

* an authenticated (header/cookie-carried) WS handshake with NO organization
  is refused BEFORE the app is entered — the socket is closed with a clear
  ASGI close code/reason, never silently dropped or left to hang
* the same handshake WITH a verified organization is admitted (positive
  control)
* an ANONYMOUS handshake (no identity at all) is admitted through unchanged —
  many WS handlers (e.g. google_specialized) authenticate via a message sent
  AFTER ``websocket.accept()``, which this handshake-time gate cannot see,
  and is not what this gate polices
* an exempt path is admitted through without an organization, same as HTTP
"""

from __future__ import annotations

import time

import jwt
import pytest
from matrx_connect.middleware.auth import AuthMiddleware

JWT_SECRET = "test-secret-do-not-use-in-prod-test-secret-do-not-use-in-prod-AB"
USER_ID = "11111111-1111-4111-8111-111111111111"
ORG_ID = "33333333-3333-4333-8333-333333333333"


class _WsApp:
    """Terminal ASGI app that records whether the WS connection was ever
    handed to it, and the AppContext it was admitted with."""

    def __init__(self) -> None:
        self.entered = False
        self.context = None

    async def __call__(self, scope, receive, send) -> None:
        self.entered = True
        state = scope.get("state") or {}
        self.context = state.get("context")


def _token(**claims) -> str:
    payload = {
        "sub": USER_ID,
        "aud": "authenticated",
        "exp": int(time.time()) + 3600,
        **claims,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


async def _member_only_resolver(user_id: str, claimed: str | None) -> str | None:
    if claimed == ORG_ID and user_id == USER_ID:
        return ORG_ID
    return None


def _ws_scope(path: str, headers: dict[str, str]) -> dict:
    return {
        "type": "websocket",
        "path": path,
        "query_string": b"",
        "headers": [(k.lower().encode(), v.encode()) for k, v in headers.items()],
        "client": ("127.0.0.1", 12345),
        "state": {},
    }


def _receive_factory():
    """One ``websocket.connect`` event, then hangs — a refusal must consume
    exactly one message and never ask for a second."""

    sent_connect = False

    async def receive() -> dict:
        nonlocal sent_connect
        if not sent_connect:
            sent_connect = True
            return {"type": "websocket.connect"}
        raise AssertionError("receive() called again after the connect event")

    return receive


def _middleware(app: _WsApp) -> AuthMiddleware:
    return AuthMiddleware(
        app,
        jwt_secret=JWT_SECRET,
        resolve_active_organization=_member_only_resolver,
        log_requests=False,
    )


@pytest.mark.asyncio
async def test_authenticated_websocket_without_organization_is_refused_at_handshake() -> None:
    app = _WsApp()
    mw = _middleware(app)
    sent: list[dict] = []

    async def send(message: dict) -> None:
        sent.append(message)

    await mw(
        _ws_scope("/ws/anything", {"authorization": f"Bearer {_token()}"}),
        _receive_factory(),
        send,
    )

    # The point of the gate: the app never saw this connection.
    assert app.entered is False
    assert len(sent) == 1
    assert sent[0]["type"] == "websocket.close"
    assert sent[0]["reason"] == "organization_required"


@pytest.mark.asyncio
async def test_authenticated_websocket_with_verified_organization_is_admitted() -> None:
    """Positive control — a gate that refused every WS would also pass the
    test above for the wrong reason."""
    app = _WsApp()
    mw = _middleware(app)
    sent: list[dict] = []

    async def send(message: dict) -> None:
        sent.append(message)

    await mw(
        _ws_scope(
            "/ws/anything",
            {"authorization": f"Bearer {_token()}", "x-organization-id": ORG_ID},
        ),
        _receive_factory(),
        send,
    )

    assert app.entered is True
    assert app.context is not None
    assert app.context.organization_id == ORG_ID
    assert sent == []


@pytest.mark.asyncio
async def test_anonymous_websocket_handshake_is_admitted_through_unchanged() -> None:
    """No identity at handshake (e.g. a client that authenticates via a
    post-accept message) is not this gate's business — it is admitted, and
    receive()/send() are left completely untouched for the app to drive its
    own handshake."""
    app = _WsApp()
    mw = _middleware(app)
    sent: list[dict] = []

    async def send(message: dict) -> None:
        sent.append(message)

    receive_calls = 0

    async def receive() -> dict:
        nonlocal receive_calls
        receive_calls += 1
        return {"type": "websocket.connect"}

    await mw(_ws_scope("/ws/anything", {}), receive, send)

    assert app.entered is True
    assert app.context is not None
    assert not app.context.user_id
    # The middleware must not have consumed the connect event on this path —
    # the app (or a Starlette WebSocket wrapper inside it) still needs it.
    assert receive_calls == 0
    assert sent == []


@pytest.mark.asyncio
async def test_exempt_websocket_path_is_admitted_without_an_organization() -> None:
    app = _WsApp()
    mw = _middleware(app)
    sent: list[dict] = []

    async def send(message: dict) -> None:
        sent.append(message)

    await mw(
        _ws_scope("/health/ws", {"authorization": f"Bearer {_token()}"}),
        _receive_factory(),
        send,
    )

    assert app.entered is True
    assert sent == []
