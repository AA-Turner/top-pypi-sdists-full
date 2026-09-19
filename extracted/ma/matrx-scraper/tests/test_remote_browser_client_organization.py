"""`RemoteBrowserClient` carries the organization, or refuses to send.

The scraper admits a service call only WITH `X-Organization-Id`
(`matrx_connect.service_auth`), so the outbound half must forward it. A client
that omitted it would fire a call the far side refuses — the same both-halves
mistake the aidream→scraper transport fixed on 2026-09-17.
"""

from __future__ import annotations

import pytest

from matrx_scraper.ai_browser.client import BrowserClientError, RemoteBrowserClient

ORG_ID = "99999999-9999-4999-9999-999999999999"
USER_ID = "88888888-8888-4888-8888-888888888888"


def _client(organization_id: str | None) -> RemoteBrowserClient:
    return RemoteBrowserClient(
        base_url="https://scraper.example",
        auth_token="shared-secret",
        acting_user_id=USER_ID,
        organization_id=organization_id,
    )


def test_headers_carry_the_organization() -> None:
    headers = _client(ORG_ID)._headers()
    assert headers["X-Organization-Id"] == ORG_ID
    assert headers["X-Matrx-User-Id"] == USER_ID
    assert headers["Authorization"] == "Bearer shared-secret"


def test_a_client_with_no_organization_refuses_before_sending() -> None:
    with pytest.raises(BrowserClientError) as excinfo:
        _client(None)._headers()
    assert "X-Organization-Id" in str(excinfo.value)


def test_from_env_passes_the_organization_through(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MATRX_SCRAPER_URL", "https://scraper.example")
    monkeypatch.setenv("MATRX_SCRAPER_TOKEN", "shared-secret")
    client = RemoteBrowserClient.from_env(acting_user_id=USER_ID, organization_id=ORG_ID)
    assert client is not None
    assert client._headers()["X-Organization-Id"] == ORG_ID
