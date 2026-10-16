"""Golden: RemoteBrowserClient puts exactly these identity headers, method, path and body on the wire.

Pinned against the hand-built httpx transport BEFORE it moved onto ``matrx_api`` and kept green after, so the switch
is provably a no-op on the wire. Anything else on the wire (X-Request-Id, Content-Type) is the transport's own and never
an identity.
"""

from __future__ import annotations

import json

import httpx
import pytest

from matrx_scraper.ai_browser.client import BrowserClientError, RemoteBrowserClient

ORG = "99999999-9999-4999-9999-999999999999"
USER = "88888888-8888-4888-8888-888888888888"
IDENTITY = {"authorization", "x-organization-id", "x-matrx-user-id"}


def _client(handler, *, token: str | None = "shared-secret", user: str | None = USER) -> RemoteBrowserClient:
    return RemoteBrowserClient(
        base_url="https://scraper.example/",
        auth_token=token,
        acting_user_id=user,
        organization_id=ORG,
        client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )


def _identity(request: httpx.Request) -> dict[str, str]:
    return {k: v for k, v in request.headers.items() if k in IDENTITY}


@pytest.mark.asyncio
async def test_post_action_sends_identity_method_path_and_body():
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"success": True, "session_id": "s1", "url": "https://e.com", "title": "T"})

    out = await _client(handler).navigate("https://e.com", session_id="s1")
    req = seen[0]
    assert req.method == "POST"
    assert str(req.url) == "https://scraper.example/api/scraper/browser/navigate"
    assert _identity(req) == {
        "authorization": "Bearer shared-secret",
        "x-organization-id": ORG,
        "x-matrx-user-id": USER,
    }
    assert req.headers["accept"] == "application/json"
    assert json.loads(req.content) == {
        "url": "https://e.com", "wait_until": "load", "timeout_ms": 30000, "extract_text": False, "session_id": "s1",
    }
    assert out.session_id == "s1"


@pytest.mark.asyncio
async def test_delete_and_list_use_the_same_identity():
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"ok": True})

    c = _client(handler)
    assert await c.close("sess-9") == {"ok": True}
    assert await c.list_sessions() == {"ok": True}
    close_req, list_req = seen
    assert (close_req.method, str(close_req.url)) == ("DELETE", "https://scraper.example/api/scraper/browser/sessions/sess-9")
    assert (list_req.method, str(list_req.url)) == ("GET", "https://scraper.example/api/scraper/browser/sessions")
    for req in seen:
        assert _identity(req) == {
            "authorization": "Bearer shared-secret", "x-organization-id": ORG, "x-matrx-user-id": USER,
        }


@pytest.mark.asyncio
async def test_no_token_and_no_user_send_neither_header():
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={})

    await _client(handler, token=None, user=None).list_sessions()
    assert _identity(seen[0]) == {"x-organization-id": ORG}


@pytest.mark.asyncio
async def test_http_error_and_transport_error_raise_browser_client_error():
    def boom(request: httpx.Request) -> httpx.Response:
        return httpx.Response(502, json={"detail": "bad gateway"})

    with pytest.raises(BrowserClientError) as excinfo:
        await _client(boom).click("s1", "#a")
    assert "502" in str(excinfo.value) and "bad gateway" in str(excinfo.value)

    def down(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("refused")

    with pytest.raises(BrowserClientError) as excinfo:
        await _client(down).click("s1", "#a")
    assert "transport error" in str(excinfo.value)


@pytest.mark.asyncio
async def test_missing_organization_refuses_before_any_request():
    def never(request: httpx.Request) -> httpx.Response:  # pragma: no cover
        raise AssertionError("must not send")

    c = RemoteBrowserClient(
        base_url="https://scraper.example", auth_token="t", organization_id=None,
        client=httpx.AsyncClient(transport=httpx.MockTransport(never)),
    )
    with pytest.raises(BrowserClientError, match="X-Organization-Id"):
        await c.list_sessions()
