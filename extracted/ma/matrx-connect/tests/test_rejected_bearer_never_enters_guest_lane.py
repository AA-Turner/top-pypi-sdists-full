"""A refused Bearer token never falls through to the guest (fingerprint) lane.

2026-09-30 census: 172 anonymous ``auth.users`` (each with its own organization)
were minted on GET /admin/system-errors/open-outages — an admin-only route —
because the browser client sends BOTH ``Authorization: Bearer <jwt>`` and
``X-Guest-Fingerprint``; when the JWT had expired the middleware fell through
to the guest lane and minted an account. A presented-and-refused credential is
a lapsed session, never a guest: the request stays anonymous (the route 401s).
"""

from __future__ import annotations

import pytest
from matrx_connect.middleware.auth import AuthMiddleware

MINTED = "77777777-7777-4777-8777-777777777777"


class _App:
    context = None

    async def __call__(self, scope, receive, send) -> None:
        self.context = (scope.get("state") or {}).get("context")
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"ok"})


async def _run(method: str, headers: list[tuple[bytes, bytes]]):
    calls: list[tuple[str, str | None]] = []

    async def resolver(fp, ip, ua, *, route=None) -> str:
        calls.append((fp, route))
        return MINTED

    async def has_identity(fp) -> bool:
        return True  # a known fingerprint: reads would resolve too

    app = _App()
    mw = AuthMiddleware(
        app,
        jwt_secret="x" * 64,
        log_requests=False,
        resolve_guest=resolver,
        has_guest_identity=has_identity,
    )
    scope = {
        "type": "http",
        "method": method,
        "path": "/admin/system-errors/open-outages",
        "query_string": b"",
        "headers": headers,
        "client": ("127.0.0.1", 1),
        "state": {},
    }

    async def receive() -> dict:
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message: dict) -> None:
        return None

    await mw(scope, receive, send)
    return app.context, calls


FP = (b"x-guest-fingerprint", b"fp-browser-abc123")


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["GET", "POST"])
@pytest.mark.parametrize(
    "authorization",
    [b"Bearer not-a-valid-jwt", b"Basic dXNlcjpwYXNz", b"Bearer"],
    ids=["expired_or_bad_jwt", "wrong_scheme", "malformed"],
)
async def test_refused_bearer_with_fingerprint_mints_nothing(method: str, authorization: bytes) -> None:
    ctx, calls = await _run(method, [(b"authorization", authorization), FP])
    assert calls == []
    assert not ctx.user_id
    assert not ctx.is_authenticated
    assert ctx.auth_type != "fingerprint"


@pytest.mark.asyncio
async def test_fingerprint_alone_still_resolves_the_guest_with_its_route() -> None:
    # Positive control: without it, a middleware that refuses every guest passes.
    ctx, calls = await _run("POST", [FP])
    assert calls == [("fp-browser-abc123", "POST /admin/system-errors/open-outages")]
    assert ctx.user_id == MINTED
    assert ctx.auth_type == "fingerprint"
