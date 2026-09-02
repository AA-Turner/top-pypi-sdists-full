from __future__ import annotations

import time

import httpx
import pytest

from matrx_scraper import performance
from matrx_scraper.performance import GscClient, GscErrorCode


class _FakeAsyncClient:
    responses: list[httpx.Response] = []
    calls = 0

    def __init__(self, **_kwargs) -> None:
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args) -> None:
        return None

    async def post(self, *_args, **_kwargs) -> httpx.Response:
        response = self.responses[self.calls]
        type(self).calls += 1
        return response


def _response(status_code: int, *, google_status: str) -> httpx.Response:
    return httpx.Response(
        status_code,
        json={"error": {"status": google_status, "message": "provider detail"}},
        request=httpx.Request("POST", "https://searchconsole.googleapis.com/test"),
    )


@pytest.mark.asyncio
async def test_page_snapshot_classifies_property_permission_denied(monkeypatch) -> None:
    _FakeAsyncClient.calls = 0
    _FakeAsyncClient.responses = [
        _response(403, google_status="PERMISSION_DENIED"),
        _response(403, google_status="PERMISSION_DENIED"),
    ]
    monkeypatch.setattr(performance.httpx, "AsyncClient", _FakeAsyncClient)
    client = GscClient(service_account_info={"client_email": "service@example.com"})
    client._access_token = "cached-token"
    client._access_token_expires_at = time.time() + 3600

    snapshot = await client.page_snapshot(
        "https://example.com/page",
        site_url="sc-domain:example.com",
    )

    assert snapshot.error_code == GscErrorCode.PROPERTY_NOT_AUTHORIZED
    assert "not authorized" in (snapshot.error_message or "")
    assert "provider detail" not in (snapshot.error_message or "")


def test_quota_403_is_not_misclassified_as_property_authorization() -> None:
    response = _response(403, google_status="RESOURCE_EXHAUSTED")
    code, message = performance._classify_gsc_http_error(
        response,
        payload=response.json(),
        response_text=response.text,
        operation="totals",
        site_url="sc-domain:example.com",
    )

    assert code == GscErrorCode.REQUEST_FAILED
    assert "HTTP 403" in message


@pytest.mark.asyncio
async def test_unconfigured_snapshot_has_stable_error_code() -> None:
    client = GscClient(
        client_id="invalid",
        client_secret="invalid",
        refresh_token=None,
        service_account_info={},
    )

    snapshot = await client.page_snapshot("https://example.com/page")

    assert snapshot.error_code == GscErrorCode.NOT_CONFIGURED
    assert snapshot.error_message == "not_configured"
