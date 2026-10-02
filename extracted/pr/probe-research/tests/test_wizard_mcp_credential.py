"""Saved MCP grants are checked using the read token, with no login or writes."""

from __future__ import annotations

import httpx
import pytest

from probe.cli.capabilities import verify_mcp_credential
from probe.sdk import config


@pytest.fixture
def read_check(monkeypatch, tmp_path):
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config.json"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_BASE_URL", "https://unrelated.example.test")
    monkeypatch.setenv("PROBE_TOKEN", "unrelated-api-token")
    monkeypatch.setenv("PROBE_MCP_TOKEN", "unrelated-mcp-token")
    monkeypatch.setenv("PROBE_ASYNC", "1")
    monkeypatch.setattr(config, "save_context", lambda *_a, **_kw: pytest.fail("read-only check"))
    real_client = httpx.Client
    requests = []
    clients = []

    def install_response(outcome):
        def respond(request):
            requests.append(request)
            assert request.method == "GET"
            assert str(request.url) == "https://selected.example.test/v1/me"
            assert request.headers["Authorization"] == "Bearer selected-read-token"
            assert request.headers["X-Probe-Surface"] == "mcp"
            assert "X-Probe-Device" not in request.headers
            assert all(0 < value <= 5.0 for value in request.extensions["timeout"].values())
            if isinstance(outcome, Exception):
                raise outcome
            return httpx.Response(outcome, json={"email": "researcher@example.test"})

        def make_client(**kwargs):
            client = real_client(**kwargs, transport=httpx.MockTransport(respond))
            clients.append(client)
            return client

        monkeypatch.setattr(httpx, "Client", make_client)

    yield install_response, requests
    assert all(client.is_closed for client in clients)
    assert list(tmp_path.rglob("*")) == [], "validation must not save credentials or local state"


@pytest.mark.parametrize(
    "status,expected",
    [(200, True), (401, False), (403, False), (404, None), (429, None), (500, None)],
)
def test_mcp_read_token_validation(read_check, status, expected):
    respond, requests = read_check
    respond(status)

    assert verify_mcp_credential(
        base_url="https://selected.example.test", token="selected-read-token"
    ) is expected
    assert len(requests) == 1, "credential checks must not retry unavailable endpoints"


@pytest.mark.parametrize(
    "error",
    [httpx.ConnectError("offline"), httpx.ReadTimeout("timeout"), ValueError("invalid response")],
)
def test_unavailable_mcp_check_keeps_the_saved_token_reusable(read_check, error):
    respond, requests = read_check
    respond(error)

    assert verify_mcp_credential(
        base_url="https://selected.example.test", token="selected-read-token"
    ) is None
    assert len(requests) == 1
