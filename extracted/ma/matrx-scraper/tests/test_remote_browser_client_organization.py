"""`RemoteBrowserClient` carries the organization, or refuses to send.

The scraper admits a service call only WITH `X-Organization-Id`
(`matrx_connect.service_auth`), so the outbound half must forward it. A client
that omitted it would fire a call the far side refuses — the same both-halves
mistake the aidream→scraper transport fixed on 2026-09-17.
"""

from __future__ import annotations

import httpx
import pytest

from matrx_scraper.ai_browser.client import BrowserClientError, RemoteBrowserClient

ORG_ID = "99999999-9999-4999-9999-999999999999"
USER_ID = "88888888-8888-4888-8888-888888888888"


def _client(organization_id: str | None, seen: list[httpx.Request] | None = None) -> RemoteBrowserClient:
    def handler(request: httpx.Request) -> httpx.Response:
        if seen is not None:
            seen.append(request)
        return httpx.Response(200, json={"sessions": []})

    return RemoteBrowserClient(
        base_url="https://scraper.example",
        auth_token="shared-secret",
        acting_user_id=USER_ID,
        organization_id=organization_id,
        client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )


@pytest.mark.asyncio
async def test_headers_carry_the_organization() -> None:
    seen: list[httpx.Request] = []
    await _client(ORG_ID, seen).list_sessions()
    headers = seen[0].headers
    assert headers["X-Organization-Id"] == ORG_ID
    assert headers["X-Matrx-User-Id"] == USER_ID
    assert headers["Authorization"] == "Bearer shared-secret"


@pytest.mark.asyncio
async def test_a_client_with_no_organization_refuses_before_sending() -> None:
    seen: list[httpx.Request] = []
    with pytest.raises(BrowserClientError) as excinfo:
        await _client(None, seen).list_sessions()
    assert "X-Organization-Id" in str(excinfo.value)
    assert seen == []


@pytest.mark.asyncio
async def test_from_env_passes_the_organization_through(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MATRX_SCRAPER_URL", "https://scraper.example")
    monkeypatch.setenv("MATRX_SCRAPER_TOKEN", "shared-secret")
    client = RemoteBrowserClient.from_env(acting_user_id=USER_ID, organization_id=ORG_ID)
    assert client is not None
    seen: list[httpx.Request] = []
    client._client = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda r: (seen.append(r), httpx.Response(200, json={}))[1])
    )
    await client.list_sessions()
    assert seen[0].headers["X-Organization-Id"] == ORG_ID
