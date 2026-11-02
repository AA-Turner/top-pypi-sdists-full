# ruff: noqa: ARG001
"""Tests for the warm pool sizing methods on RestClient."""

import json
from typing import Any

import httpx
import pytest

from edison_client.clients.rest_client import RestClient
from edison_client.models.app import Stage
from edison_client.models.rest import SetWarmPoolResponse

CROW_KEY = "job-futurehouse-dummy-env"
# The server's own wait budget (warmpool_ready_wait_timeout_seconds). A client
# ceiling at or below this would cut off a wait the server was still honouring.
SERVER_WAIT_BUDGET_SECONDS = 300.0


class _Recorder:
    """Captures what the client sent, and stands in for the server's answer."""

    def __init__(self) -> None:
        self.requests: list[httpx.Request] = []
        self.timeouts: list[float | None] = []
        self.response_body: dict[str, Any] = _body()
        self.status_code: int = 200

    def set_response(self, body: dict[str, Any], code: int = 200) -> None:
        self.response_body = body
        self.status_code = code


def _body(**overrides: Any) -> dict[str, Any]:
    return {
        "crow_key": CROW_KEY,
        "node_pool": "agent-sandbox-small",
        "replicas": 5,
        "ready_replicas": 5,
        "waited": False,
        "timed_out": False,
    } | overrides


@pytest.fixture(name="rest_client")
def fixture_rest_client() -> RestClient:
    return RestClient(stage=Stage.LOCAL, api_key="test-key", cleanup_on_exit=False)


@pytest.fixture(name="recorder")
def fixture_recorder(rest_client: RestClient, monkeypatch) -> _Recorder:
    """Route the client at a mock transport and record the timeout it asked for."""
    recorder = _Recorder()

    def handle(request: httpx.Request) -> httpx.Response:
        recorder.requests.append(request)
        return httpx.Response(recorder.status_code, json=recorder.response_body)

    def sync_handler(request: httpx.Request) -> httpx.Response:
        request.read()
        return handle(request)

    async def async_handler(request: httpx.Request) -> httpx.Response:
        await request.aread()
        return handle(request)

    def fake_get_client(
        content_type: str | None = "application/json",
        authenticated: bool = True,
        async_client: bool = False,
        timeout: float | None = None,
    ) -> httpx.Client | httpx.AsyncClient:
        recorder.timeouts.append(timeout)
        if async_client:
            return httpx.AsyncClient(
                base_url=Stage.LOCAL.value,
                transport=httpx.MockTransport(async_handler),
            )
        return httpx.Client(
            base_url=Stage.LOCAL.value, transport=httpx.MockTransport(sync_handler)
        )

    monkeypatch.setattr(rest_client, "get_client", fake_get_client)
    return recorder


def test_set_crow_warmpool_posts_the_target_and_parses_the_response(
    rest_client: RestClient, recorder: _Recorder
):
    result = rest_client.set_crow_warmpool(CROW_KEY, replicas=5)

    assert isinstance(result, SetWarmPoolResponse)
    assert result.replicas == 5
    assert result.ready_replicas == 5
    request = recorder.requests[0]
    assert request.method == "POST"
    assert request.url.path == f"/v0.1/crows/{CROW_KEY}/warmpool"
    assert json.loads(request.read()) == {"replicas": 5, "wait": False}


def test_waiting_raises_the_client_timeout_above_the_server_budget(
    rest_client: RestClient, recorder: _Recorder
):
    """The whole point of the override: REQUEST_TIMEOUT cannot outlast a wait."""
    rest_client.set_crow_warmpool(CROW_KEY, replicas=5, wait=True)

    assert recorder.timeouts == [RestClient.WARMPOOL_READY_TIMEOUT]
    assert RestClient.WARMPOOL_READY_TIMEOUT > SERVER_WAIT_BUDGET_SECONDS
    assert RestClient.REQUEST_TIMEOUT < SERVER_WAIT_BUDGET_SECONDS


def test_not_waiting_keeps_the_general_request_timeout(
    rest_client: RestClient, recorder: _Recorder
):
    rest_client.set_crow_warmpool(CROW_KEY, replicas=5)

    assert recorder.timeouts == [RestClient.REQUEST_TIMEOUT]


def test_an_explicit_timeout_wins_over_both_defaults(
    rest_client: RestClient, recorder: _Recorder
):
    rest_client.set_crow_warmpool(CROW_KEY, replicas=5, wait=True, timeout=42.0)

    assert recorder.timeouts == [42.0]


def test_a_wait_that_timed_out_is_not_an_error(
    rest_client: RestClient, recorder: _Recorder
):
    """A partial wait carries the ready count; it must not raise and lose it."""
    recorder.set_response(_body(ready_replicas=3, waited=True, timed_out=True))

    result = rest_client.set_crow_warmpool(CROW_KEY, replicas=5, wait=True)

    assert result.replicas == 5
    assert result.ready_replicas == 3
    assert result.timed_out is True


async def test_aset_crow_warmpool_matches_the_sync_method(
    rest_client: RestClient, recorder: _Recorder
):
    result = await rest_client.aset_crow_warmpool(CROW_KEY, replicas=5, wait=True)

    assert result.replicas == 5
    assert recorder.timeouts == [RestClient.WARMPOOL_READY_TIMEOUT]
    assert recorder.requests[0].url.path == f"/v0.1/crows/{CROW_KEY}/warmpool"
