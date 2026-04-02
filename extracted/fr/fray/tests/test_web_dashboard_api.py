import json
import socketserver
import threading
import time
from typing import Dict
from urllib import request as urllib_request

import pytest

from fray import web_dashboard


class _DashboardServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


@pytest.fixture
def share_backend(monkeypatch):
    state: Dict[str, Dict] = {
        "shares": {
            "share123": {
                "domain": "acme.com",
                "expires_at": "2030-01-01T00:00:00Z",
                "shared_at": "2029-12-01T00:00:00Z",
            }
        },
        "share_calls": [],
        "extend_calls": [],
    }

    def fake_list_shares():
        # Return a shallow copy so the handler cannot mutate the internal dict.
        return {k: dict(v) for k, v in state["shares"].items()}

    def fake_share_domain(domain, expires_days=30, verbose=False):
        state["share_calls"].append((domain, expires_days, verbose))
        return f"https://share.example/{domain}?id=new123"

    def fake_extend_share(share_id, days=30, verbose=False):
        state["extend_calls"].append((share_id, days, verbose))
        if share_id in state["shares"]:
            state["shares"][share_id]["expires_at"] = "2099-01-01T00:00:00Z"
            return f"https://share.example/{share_id}"
        return None

    monkeypatch.setattr("fray.cloud_sync.list_shares", fake_list_shares)
    monkeypatch.setattr("fray.cloud_sync.share_domain", fake_share_domain)
    monkeypatch.setattr("fray.cloud_sync.extend_share", fake_extend_share)
    return state


@pytest.fixture
def dashboard_server(share_backend):  # pylint: disable=unused-argument
    server = _DashboardServer(("127.0.0.1", 0), web_dashboard.DashboardHandler)
    port = server.server_address[1]
    web_dashboard._DASHBOARD_PORT = port  # ensure CORS header matches test port
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    # Give the server a moment to bind before issuing requests.
    time.sleep(0.05)
    yield port
    server.shutdown()
    server.server_close()
    thread.join(timeout=1)


def _request_json(port: int, method: str, path: str, body: Dict = None):
    url = f"http://127.0.0.1:{port}{path}"
    data = None
    headers = {}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib_request.Request(url, data=data, method=method)
    for key, value in headers.items():
        req.add_header(key, value)
    with urllib_request.urlopen(req, timeout=5) as resp:  # nosec B310
        payload = json.loads(resp.read().decode("utf-8"))
        return resp.status, payload


def test_api_shares_lists_backend_state(dashboard_server, share_backend):
    status, payload = _request_json(dashboard_server, "GET", "/api/shares")
    assert status == 200
    # share_status() now enriches each share with a 'status' field — check
    # that core fields are present rather than exact equality
    for share_id, share_data in share_backend["shares"].items():
        assert share_id in payload
        for key in ("domain", "expires_at", "shared_at"):
            assert key in payload.get(share_id, {})


def test_api_share_creates_snapshot(dashboard_server, share_backend):
    status, payload = _request_json(
        dashboard_server,
        "POST",
        "/api/share/example.com",
        {"expires_days": 45},
    )
    assert status == 200
    assert payload["status"] == "shared"
    assert payload["domain"] == "example.com"
    assert payload["expires_days"] == 45
    assert share_backend["share_calls"][-1] == ("example.com", 45, False)


def test_api_share_extend_updates_expiry(dashboard_server, share_backend):
    status, payload = _request_json(
        dashboard_server,
        "POST",
        "/api/share-extend/share123",
        {"days": 10},
    )
    assert status == 200
    assert payload["status"] == "extended"
    assert payload["id"] == "share123"
    assert payload["url"].endswith("/share123")
    assert payload["expires_at"] == "2099-01-01T00:00:00Z"
    assert share_backend["extend_calls"][-1] == ("share123", 10, False)
