"""Mixpeek._request retries a retryable 429/503 for long enough to outlast a
vector-store writer booting (about 2 min), honoring the server's advised wait:
the Retry-After header first, then the error body's retry_after_seconds.

Before 2026-10-17 it read retry_after_seconds only from ``detail.error.details``,
while the API's error body carries it at ``error.details`` and in Retry-After,
so every 503 waited the 2 s default, and it gave up after 3 retries (about 6 s):
a write refused with a retryable 503 during a writer boot was dropped."""

from __future__ import annotations

import json

import pytest

from mixpeek._client.client import (
    MAX_RETRY_WAIT_S,
    RETRY_BUDGET_S,
    Mixpeek,
    MixpeekAPIError,
)

pytestmark = pytest.mark.unit


class _FakeResponse:
    def __init__(self, status: int, payload, headers: dict | None = None) -> None:
        self.status = status
        self.data = json.dumps(payload).encode("utf-8")
        self.headers = headers or {}


class _FakeHttp:
    def __init__(self, responses: list[_FakeResponse]) -> None:
        self.responses = list(responses)
        self.calls = 0

    def request(self, method, url, *, body=None, headers=None):
        resp = self.responses[min(self.calls, len(self.responses) - 1)]
        self.calls += 1
        return resp


def _client() -> Mixpeek:
    return Mixpeek(api_key="sk_test", namespace="ns_test")


def _writer_booting() -> _FakeResponse:
    """The API's answer to a write while the vector store's writer boots."""
    return _FakeResponse(
        503,
        {
            "success": False,
            "status": 503,
            "error": {
                "message": "The write was refused and nothing was stored: ...",
                "type": "WriterReadOnlyError",
                "details": {"retryable": True, "retry_after_seconds": 15},
            },
        },
        {"Retry-After": "15"},
    )


@pytest.fixture
def slept(monkeypatch):
    waits: list[float] = []
    monkeypatch.setattr("time.sleep", lambda s: waits.append(s))
    return waits


def test_a_503_with_retry_after_15_waits_15s_and_then_succeeds(slept):
    client = _client()
    client._http = _FakeHttp([_writer_booting(), _FakeResponse(200, {"ok": True})])

    assert client._request("POST", "/namespaces/ns_test/documents/upsert") == {
        "ok": True
    }
    assert client._http.calls == 2
    assert slept == [15.0]


def test_the_header_wins_over_the_body(slept):
    client = _client()
    client._http = _FakeHttp(
        [
            _FakeResponse(
                503,
                {"error": {"details": {"retry_after_seconds": 9}}},
                {"Retry-After": "4"},
            ),
            _FakeResponse(200, {"ok": True}),
        ]
    )
    client._request("GET", "/namespaces/ns_test")
    assert slept == [4.0]


@pytest.mark.parametrize(
    "payload",
    [
        {"error": {"details": {"retry_after_seconds": 7}}},
        {"detail": {"error": {"details": {"retry_after_seconds": 7}}}},
    ],
)
def test_the_body_hint_is_read_in_either_shape(slept, payload):
    client = _client()
    client._http = _FakeHttp([_FakeResponse(503, payload), _FakeResponse(200, {})])
    client._request("GET", "/namespaces/ns_test")
    assert slept == [7.0]


def test_a_writer_boot_of_two_and_a_half_minutes_is_survived(slept):
    """Ten 503s with Retry-After 15 (150 s), then the writer takes writes."""
    client = _client()
    client._http = _FakeHttp(
        [_writer_booting()] * 10 + [_FakeResponse(200, {"ok": True})]
    )

    assert client._request("POST", "/namespaces/ns_test/documents/upsert") == {
        "ok": True
    }
    assert client._http.calls == 11
    assert sum(slept) == 150.0


def test_an_outage_longer_than_the_budget_raises_retryable(slept):
    client = _client()
    client._http = _FakeHttp([_writer_booting()])

    with pytest.raises(MixpeekAPIError) as exc_info:
        client._request("POST", "/namespaces/ns_test/documents/upsert")

    assert sum(slept) <= RETRY_BUDGET_S
    assert sum(slept) > RETRY_BUDGET_S - 15
    assert client._http.calls == len(slept) + 1
    assert exc_info.value.retryable is True
    assert exc_info.value.status == 503
    assert exc_info.value.retry_after == 15.0


def test_with_no_hint_the_wait_backs_off_and_is_capped(slept):
    client = _client()
    client._http = _FakeHttp([_FakeResponse(429, {})] * 6 + [_FakeResponse(200, {})])
    client._request("GET", "/namespaces/ns_test")
    assert slept == [2.0, 4.0, 8.0, 16.0, 30.0, 30.0]


def test_a_wait_longer_than_the_cap_is_capped(slept):
    client = _client()
    client._http = _FakeHttp(
        [_FakeResponse(503, {}, {"Retry-After": "90"}), _FakeResponse(200, {})]
    )
    client._request("GET", "/namespaces/ns_test")
    assert slept == [MAX_RETRY_WAIT_S]


def test_a_422_is_not_retried(monkeypatch):
    client = _client()
    client._http = _FakeHttp(
        [
            _FakeResponse(
                422,
                {
                    "error": {
                        "message": "The write was refused and nothing was stored: ...",
                        "details": {"retryable": False},
                    }
                },
            )
        ]
    )
    monkeypatch.setattr("time.sleep", lambda s: pytest.fail("must not sleep"))

    with pytest.raises(MixpeekAPIError) as exc_info:
        client._request("POST", "/namespaces/ns_test/documents/upsert")

    assert client._http.calls == 1
    assert exc_info.value.retryable is False


def test_a_503_marked_not_retryable_is_not_retried(monkeypatch):
    client = _client()
    client._http = _FakeHttp(
        [_FakeResponse(503, {"error": {"details": {"retryable": False}}})]
    )
    monkeypatch.setattr("time.sleep", lambda s: pytest.fail("must not sleep"))

    with pytest.raises(MixpeekAPIError):
        client._request("GET", "/namespaces/ns_test")
    assert client._http.calls == 1


def test_a_404_is_not_retried(monkeypatch):
    client = _client()
    client._http = _FakeHttp([_FakeResponse(404, {"detail": "not found"})])
    monkeypatch.setattr("time.sleep", lambda s: pytest.fail("must not sleep"))

    with pytest.raises(MixpeekAPIError) as exc_info:
        client._request("GET", "/namespaces/ns_test")

    assert client._http.calls == 1
    assert exc_info.value.retryable is False
