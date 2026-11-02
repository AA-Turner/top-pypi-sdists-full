"""A guest account is minted only by a request that DOES something.

2026-09-30 junk-data census: ~1,050 anonymous ``auth.users`` (each with its own
auto organization) existed, 664 of them never used for anything — a bare read
(GET) from a fresh browser fingerprint minted one. Rule: a READ from a
fingerprint with no identity yet stays anonymous; a write mints; a fingerprint
that already owns an identity resolves on reads exactly as before.
"""

from __future__ import annotations

import pytest
from matrx_connect.middleware.auth import AuthMiddleware

MINTED = "66666666-6666-4666-8666-666666666666"


class _App:
    context = None

    async def __call__(self, scope, receive, send) -> None:
        self.context = (scope.get("state") or {}).get("context")
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"ok"})


async def _run(method: str, *, known: bool, with_peek: bool = True, exempt=None, path: str = "/files/00000000-0000-4000-8000-000000000000/download"):
    minted: list[str] = []

    async def resolver(fp, ip, ua, *, route=None) -> str:
        minted.append(fp)
        return MINTED

    async def has_identity(fp) -> bool:
        return known

    app = _App()
    mw = AuthMiddleware(
        app,
        jwt_secret="x" * 64,
        log_requests=False,
        resolve_guest=resolver,
        has_guest_identity=has_identity if with_peek else None,
        guest_mint_exempt=exempt,
    )
    scope = {
        "type": "http",
        "method": method,
        "path": path,
        "query_string": b"",
        "headers": [(b"x-fingerprint-id", b"fp-browser-abc123")],
        "client": ("127.0.0.1", 1),
        "state": {},
    }

    async def receive() -> dict:
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message: dict) -> None:
        return None

    await mw(scope, receive, send)
    return app.context, minted


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["GET", "HEAD", "OPTIONS"])
async def test_a_read_from_a_new_visitor_mints_no_account(method: str) -> None:
    ctx, minted = await _run(method, known=False)
    assert minted == []
    assert not ctx.user_id


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["POST", "PUT", "PATCH", "DELETE"])
async def test_a_write_from_a_new_visitor_mints_the_account(method: str) -> None:
    ctx, minted = await _run(method, known=False)
    assert minted == ["fp-browser-abc123"]
    assert ctx.user_id == MINTED


@pytest.mark.asyncio
async def test_a_read_from_a_known_visitor_still_resolves() -> None:
    ctx, minted = await _run("GET", known=True)
    assert minted == ["fp-browser-abc123"]
    assert ctx.user_id == MINTED


@pytest.mark.asyncio
async def test_hosts_without_the_peek_keep_the_old_behaviour() -> None:
    ctx, minted = await _run("GET", known=False, with_peek=False)
    assert minted == ["fp-browser-abc123"]


def _incidental(method: str, path: str, query: str) -> bool:
    return path.startswith("/esign/signing/")


@pytest.mark.asyncio
async def test_an_incidental_write_from_a_new_visitor_mints_no_account() -> None:
    ctx, minted = await _run("POST", known=False, exempt=_incidental, path="/esign/signing/outsider/open")
    assert minted == []
    assert not ctx.user_id


@pytest.mark.asyncio
async def test_an_incidental_write_from_a_known_visitor_still_resolves() -> None:
    ctx, minted = await _run("POST", known=True, exempt=_incidental, path="/esign/signing/outsider/open")
    assert minted == ["fp-browser-abc123"]
    assert ctx.user_id == MINTED


@pytest.mark.asyncio
async def test_a_meaningful_write_still_mints_with_an_exemption_wired() -> None:
    ctx, minted = await _run("POST", known=False, exempt=_incidental, path="/ai/mandates/app.x")
    assert minted == ["fp-browser-abc123"]
    assert ctx.user_id == MINTED
