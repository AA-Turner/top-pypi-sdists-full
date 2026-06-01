"""E2E tests for the hooks relay command with a mock HTTP backend."""

import json
from unittest.mock import patch
from urllib.parse import urlparse

import pytest
from werkzeug import Request, Response

from runlayer_cli.config import Config, save_config
from runlayer_cli.main import app

pytestmark = pytest.mark.no_backend_e2e

TEST_SECRET = "rl_test_relay_secret"


def _seed_config(host_url: str):
    """Write a config.yaml with default_host and secret pointing at the mock server."""
    parsed = urlparse(host_url)
    port = parsed.port
    host_key = f"{parsed.hostname}:{port}" if port else parsed.hostname

    config = Config(
        default_host=host_url,
        hosts={
            host_key: {
                "url": host_url,
                "secret": TEST_SECRET,
            }
        },
    )
    save_config(config)


# ── Enforce endpoint ─────────────────────────────────────────────────


def test_relay_enforce_posts_to_correct_endpoint(runner, runlayer_home, httpserver):
    received: list[Request] = []

    def _handler(request: Request):
        received.append(request)
        return Response(
            json.dumps({"permission": "allow"}),
            status=200,
            content_type="application/json",
        )

    httpserver.expect_request(
        "/api/v1/hooks/cursor", method="POST"
    ).respond_with_handler(_handler)

    host = httpserver.url_for("")
    with patch("runlayer_cli.config.get_keyring_store", return_value=None):
        _seed_config(host)
        result = runner.invoke(
            app, ["hooks", "relay", "enforce"], input='{"tool": "bash"}'
        )

    assert result.exit_code == 0
    assert '{"permission": "allow"}' in result.output

    assert len(received) == 1
    req = received[0]
    body = json.loads(req.get_data(as_text=True))
    assert body == {"tool": "bash"}
    assert req.headers["x-runlayer-api-key"] == TEST_SECRET
    assert "Runlayer" in req.headers["User-Agent"]
    assert req.headers["Content-Type"] == "application/json"


# ── Event endpoint ───────────────────────────────────────────────────


def test_relay_event_posts_to_correct_endpoint(runner, runlayer_home, httpserver):
    received: list[Request] = []

    def _handler(request: Request):
        received.append(request)
        return Response("{}", status=200, content_type="application/json")

    httpserver.expect_request(
        "/api/v1/hooks/events", method="POST"
    ).respond_with_handler(_handler)

    host = httpserver.url_for("")
    with patch("runlayer_cli.config.get_keyring_store", return_value=None):
        _seed_config(host)
        result = runner.invoke(
            app, ["hooks", "relay", "event"], input='{"event": "start"}'
        )

    assert result.exit_code == 0
    assert len(received) == 1
    body = json.loads(received[0].get_data(as_text=True))
    assert body == {"event": "start"}


# ── Response body forwarded to stdout ────────────────────────────────


def test_relay_forwards_response_body(runner, runlayer_home, httpserver):
    response_body = '{"status": "ok", "actions": ["log", "notify"]}'

    httpserver.expect_request("/api/v1/hooks/cursor", method="POST").respond_with_data(
        response_body, content_type="application/json"
    )

    host = httpserver.url_for("")
    with patch("runlayer_cli.config.get_keyring_store", return_value=None):
        _seed_config(host)
        result = runner.invoke(app, ["hooks", "relay", "enforce"], input="{}")

    assert result.exit_code == 0
    assert response_body in result.output


# ── Auth header matches config secret ────────────────────────────────


def test_relay_auth_header_sent(runner, runlayer_home, httpserver):
    received: list[Request] = []

    def _handler(request: Request):
        received.append(request)
        return Response("{}", status=200, content_type="application/json")

    httpserver.expect_request(
        "/api/v1/hooks/cursor", method="POST"
    ).respond_with_handler(_handler)

    host = httpserver.url_for("")
    with patch("runlayer_cli.config.get_keyring_store", return_value=None):
        _seed_config(host)
        result = runner.invoke(app, ["hooks", "relay", "enforce"], input="{}")

    assert result.exit_code == 0
    assert received[0].headers["x-runlayer-api-key"] == TEST_SECRET


# ── Server error -> exit 2 ───────────────────────────────────────────


def test_relay_server_error_exits_2(runner, runlayer_home, httpserver):
    httpserver.expect_request("/api/v1/hooks/cursor", method="POST").respond_with_json(
        {"error": "internal"}, status=500
    )

    host = httpserver.url_for("")
    with patch("runlayer_cli.config.get_keyring_store", return_value=None):
        _seed_config(host)
        result = runner.invoke(app, ["hooks", "relay", "enforce"], input="{}")

    assert result.exit_code == 2
    assert "internal" in result.output


# ── Unknown target -> exit 1 ─────────────────────────────────────────


def test_relay_unknown_target_exits_1(runner, runlayer_home):
    result = runner.invoke(app, ["hooks", "relay", "bogus"], input="{}")
    assert result.exit_code == 1
    assert "Unknown target" in result.output
