"""Golden: the scraper -> aidream GSC credential hop sends exactly these identity headers, method, path and query.

Pinned against the hand-built httpx call BEFORE it moved onto ``matrx_api`` and kept green after, so the switch is
provably a no-op on the wire (X-Request-Id is the transport's own, never an identity).
"""

from __future__ import annotations

import httpx
import pytest

from matrx_scraper.web_crawl.gsc_sync import resolve_google_credential

ORG = "3f2b8c1e-0a4d-4c55-9e0f-1a2b3c4d5e6f"
USER = "11111111-2222-4333-8444-555555555555"
IDENTITY = {"authorization", "x-organization-id", "x-matrx-user-id"}


@pytest.fixture
def wire(monkeypatch):
    monkeypatch.setenv("AIDREAM_URL", "https://server.example/")
    monkeypatch.setenv("AIDREAM_SERVICE_TOKEN", "svc-token")
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(
            200, json={"refresh_token": "1//r", "client_id": "c.apps.googleusercontent.com", "client_secret": "s"}
        )

    real = httpx.AsyncClient

    def factory(*args, **kwargs):
        kwargs["transport"] = httpx.MockTransport(handler)
        return real(*args, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", factory)
    return seen


@pytest.mark.asyncio
async def test_credential_lookup_sends_identity_method_path_and_query(wire):
    credential = await resolve_google_credential(
        credential_ref="conn-1",
        site_organization_id=ORG,
        user_id=USER,
        resource_type="search_console_property",
        resource_ref="sc-domain:example.com",
        site_id="site-1",
    )
    assert credential.refresh_token == "1//r"
    req = wire[0]
    assert req.method == "GET"
    assert req.url.scheme + "://" + req.url.host + req.url.path == "https://server.example/api/google-integrations/internal/credential"
    assert dict(req.url.params) == {
        "connection_id": "conn-1", "organization_id": ORG, "resource_type": "search_console_property",
        "resource_ref": "sc-domain:example.com", "site_id": "site-1",
    }
    assert {k: v for k, v in req.headers.items() if k in IDENTITY} == {
        "authorization": "Bearer svc-token", "x-organization-id": ORG, "x-matrx-user-id": USER,
    }


@pytest.mark.asyncio
async def test_http_error_is_loud_with_the_status(monkeypatch):
    monkeypatch.setenv("AIDREAM_URL", "https://server.example")
    monkeypatch.setenv("AIDREAM_SERVICE_TOKEN", "svc-token")
    real = httpx.AsyncClient
    monkeypatch.setattr(
        httpx, "AsyncClient",
        lambda *a, **k: real(*a, **{**k, "transport": httpx.MockTransport(lambda r: httpx.Response(409, json={"detail": "needs re-authentication"}))}),
    )
    with pytest.raises(RuntimeError, match="HTTP 409"):
        await resolve_google_credential(credential_ref="conn-1", site_organization_id=ORG, user_id=USER)
