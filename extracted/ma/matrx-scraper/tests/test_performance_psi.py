from __future__ import annotations

import ast
import inspect
import threading

import httpx
import pytest
from matrx_scraper import performance


@pytest.mark.asyncio
async def test_psi_http_failure_retains_provider_evidence_and_headers(monkeypatch) -> None:
    response = httpx.Response(
        429,
        json={
            "error": {
                "code": 429,
                "message": "quota exceeded",
                "status": "RESOURCE_EXHAUSTED",
            }
        },
        headers={"Retry-After": "10", "X-Goog-Quota-Project": "project-1"},
        request=httpx.Request("GET", performance.PSI_ENDPOINT),
    )

    class FakeAsyncClient:
        def __init__(self, **_kwargs) -> None:
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *_args) -> None:
            pass

        async def get(self, _url, *, params):
            assert ("key", "fixture-key") in params
            return response

    monkeypatch.setattr(performance.httpx, "AsyncClient", FakeAsyncClient)
    snapshot = await performance.PsiClient(api_key="fixture-key").fetch(
        "https://example.com", strategy="mobile"
    )

    assert snapshot.error_message.startswith("PSI HTTP 429")
    assert snapshot.raw == response.json()
    assert snapshot.http_status == 429
    assert snapshot.response_headers["retry-after"] == "10"
    assert snapshot.request_count == 1


@pytest.mark.asyncio
async def test_psi_malformed_http_200_is_a_typed_failure(monkeypatch) -> None:
    response = httpx.Response(
        200,
        json=["not", "an", "object"],
        request=httpx.Request("GET", performance.PSI_ENDPOINT),
    )

    class FakeAsyncClient:
        def __init__(self, **_kwargs) -> None:
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *_args) -> None:
            pass

        async def get(self, _url, *, params):
            return response

    monkeypatch.setattr(performance.httpx, "AsyncClient", FakeAsyncClient)
    snapshot = await performance.PsiClient(api_key="fixture-key").fetch(
        "https://example.com", strategy="mobile"
    )

    assert snapshot.http_status == 200
    assert snapshot.error_message == "PSI returned a malformed HTTP 200 response"
    assert snapshot.raw["malformed_response"]["body"] == ["not", "an", "object"]


@pytest.mark.asyncio
async def test_psi_json_decode_runs_off_the_event_loop(monkeypatch) -> None:
    response = httpx.Response(
        200,
        json={"lighthouseResult": {"categories": {}, "audits": {}}},
        request=httpx.Request("GET", performance.PSI_ENDPOINT),
    )
    event_loop_thread = threading.get_ident()
    decode_thread: int | None = None
    original_json = response.json

    def tracked_json():
        nonlocal decode_thread
        decode_thread = threading.get_ident()
        return original_json()

    monkeypatch.setattr(response, "json", tracked_json)

    class FakeAsyncClient:
        def __init__(self, **_kwargs) -> None:
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *_args) -> None:
            pass

        async def get(self, _url, *, params):
            return response

    monkeypatch.setattr(performance.httpx, "AsyncClient", FakeAsyncClient)
    snapshot = await performance.PsiClient(api_key="fixture-key").fetch(
        "https://example.com", strategy="mobile"
    )

    assert snapshot.error_message is None
    assert decode_thread is not None
    assert decode_thread != event_loop_thread


def test_async_provider_clients_never_decode_json_on_the_event_loop() -> None:
    source = inspect.getsource(performance)
    tree = ast.parse(source)
    violations: list[str] = []

    for function in (node for node in ast.walk(tree) if isinstance(node, ast.AsyncFunctionDef)):
        for node in ast.walk(function):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "json"
            ):
                violations.append(f"{function.name}:{node.lineno}")

    assert violations == []


@pytest.mark.asyncio
async def test_expired_psi_key_is_preserved_and_logged_without_blind_retry(
    monkeypatch, caplog
) -> None:
    expired = httpx.Response(
        400,
        json={
            "error": {
                "code": 400,
                "message": "API key expired. Please renew the API key.",
                "status": "INVALID_ARGUMENT",
            }
        },
        request=httpx.Request("GET", performance.PSI_ENDPOINT),
    )

    class FakeAsyncClient:
        def __init__(self, **_kwargs) -> None:
            self.request_count = 0

        async def __aenter__(self):
            return self

        async def __aexit__(self, *_args) -> None:
            pass

        async def get(self, _url, *, params):
            self.request_count += 1
            assert self.request_count == 1
            assert ("key", "expired-key") in params
            return expired

    monkeypatch.setattr(performance.httpx, "AsyncClient", FakeAsyncClient)
    snapshot = await performance.PsiClient(api_key="expired-key").fetch(
        "https://example.com", strategy="mobile"
    )

    # The surfaced message is OPERATOR-truthful: it names the platform key
    # and explicitly rules out the user's Google connection, so the expired
    # platform key can never masquerade as an OAuth problem.
    assert snapshot.error_message is not None
    assert "platform PageSpeed Insights API key" in snapshot.error_message
    assert "expired" in snapshot.error_message
    assert "NOT your Google account connection" in snapshot.error_message
    assert snapshot.http_status == 400
    assert snapshot.request_count == 1
    assert snapshot.raw == expired.json()
    assert "platform credential must be rotated" in caplog.text
