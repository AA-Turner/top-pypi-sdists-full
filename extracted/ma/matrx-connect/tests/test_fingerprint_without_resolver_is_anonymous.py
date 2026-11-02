"""A guest fingerprint is never an identity unless the host wired a resolver.

2026-09-26: the standalone matrx-files service (files.matrxserver.com) mounts
``AuthMiddleware`` without ``resolve_guest``. The middleware then set
``user_id = <raw fingerprint>``, so:

* ``X-Guest-Fingerprint: <any user's uuid>`` with NO token downloaded that
  user's private files (reproduced live against the admin test account), and
* any non-uuid fingerprint (what browsers actually send) answered 500
  ``InvalidTextRepresentationError`` instead of an honest 401.

The rule: without a resolver the fingerprint header is ignored for identity and
the request stays anonymous. With a resolver, the resolver's answer is the
identity — never the header itself.
"""

from __future__ import annotations

import pytest
from matrx_connect.middleware.auth import AuthMiddleware

VICTIM_USER_ID = "87a6e699-3622-4869-8843-d0867456c0dd"
RESOLVED_GUEST_ID = "55555555-5555-4555-8555-555555555555"


class _App:
    def __init__(self) -> None:
        self.context = None

    async def __call__(self, scope, receive, send) -> None:
        self.context = (scope.get("state") or {}).get("context")
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"ok"})


def _scope(headers: dict[str, str]) -> dict:
    return {
        "type": "http",
        "method": "GET",
        # A byte-serving path: the org-admission gate admits guest/anonymous here.
        "path": "/files/00000000-0000-4000-8000-000000000000/download",
        "query_string": b"",
        "headers": [(k.lower().encode(), v.encode()) for k, v in headers.items()],
        "client": ("127.0.0.1", 12345),
        "state": {},
    }


async def _run(mw: AuthMiddleware, app: _App, headers: dict[str, str]):
    async def receive() -> dict:
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message: dict) -> None:
        return None

    await mw(_scope(headers), receive, send)
    return app.context


@pytest.mark.asyncio
@pytest.mark.parametrize("header", ["x-guest-fingerprint", "x-fingerprint-id"])
@pytest.mark.parametrize("value", [VICTIM_USER_ID, "fp-browser-abc123"])
async def test_no_resolver_means_the_fingerprint_is_not_an_identity(header: str, value: str) -> None:
    app = _App()
    mw = AuthMiddleware(app, jwt_secret="x" * 64, log_requests=False)
    ctx = await _run(mw, app, {header: value})
    assert ctx is not None
    assert ctx.user_id != value, "a caller-chosen header became the user id"
    assert not ctx.user_id
    assert ctx.auth_type != "fingerprint"
    assert not ctx.is_authenticated


@pytest.mark.asyncio
async def test_with_a_resolver_the_resolver_decides_the_identity() -> None:
    seen: list[str] = []

    async def resolver(fingerprint: str, ip, user_agent, *, route=None) -> str:
        seen.append(fingerprint)
        return RESOLVED_GUEST_ID

    app = _App()
    mw = AuthMiddleware(app, jwt_secret="x" * 64, resolve_guest=resolver, log_requests=False)
    ctx = await _run(mw, app, {"x-guest-fingerprint": VICTIM_USER_ID})
    assert seen == [VICTIM_USER_ID]
    assert ctx.user_id == RESOLVED_GUEST_ID
    assert ctx.auth_type == "fingerprint"
