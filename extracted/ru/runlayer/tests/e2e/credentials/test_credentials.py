"""E2E tests for the hidden credentials commands."""

import json
from unittest.mock import patch

import pytest
from werkzeug import Request, Response

from tests.e2e.conftest import strip_ansi

from runlayer_cli.main import app

pytestmark = pytest.mark.no_backend_e2e


# ── add org + check lifecycle ────────────────────────────────────────


def test_add_org_and_check(runner, runlayer_home):
    host = "http://localhost:9999"

    result = runner.invoke(
        app,
        [
            "credentials",
            "add",
            "org",
            "mcp-watch",
            "--secret",
            "rl_org_abc",
            "--host",
            host,
        ],
    )
    assert result.exit_code == 0
    assert "saved" in strip_ansi(result.output)

    result = runner.invoke(
        app,
        [
            "credentials",
            "check",
            "--host",
            host,
            "--skip-user-check",
            "--org-api-key",
            "mcp-watch",
        ],
    )
    assert result.exit_code == 0
    assert "org (mcp-watch): ok" in result.output


def test_add_org_persists_to_disk(runner, runlayer_home):
    host = "http://localhost:9999"

    runner.invoke(
        app,
        ["credentials", "add", "org", "scan", "--secret", "rl_org_xyz", "--host", host],
    )

    config_file = runlayer_home / "config.yaml"
    assert config_file.exists()
    content = config_file.read_text()
    assert "scan" in content


# ── add user + check lifecycle ───────────────────────────────────────


def test_add_user_and_check(runner, runlayer_home):
    host = "http://localhost:9999"

    with patch("runlayer_cli.config.get_keyring_store", return_value=None):
        result = runner.invoke(
            app,
            ["credentials", "add", "user", "--secret", "rl_user_test", "--host", host],
        )
    assert result.exit_code == 0
    assert "saved" in strip_ansi(result.output)
    assert "config file" in result.output

    with patch("runlayer_cli.config.get_keyring_store", return_value=None):
        result = runner.invoke(
            app,
            ["credentials", "check", "--host", host, "--skip-org-check"],
        )
    assert result.exit_code == 0
    assert "user: ok" in result.output


# ── check failures ───────────────────────────────────────────────────


def test_check_missing_creds(runner, runlayer_home):
    host = "http://localhost:9999"

    with patch("runlayer_cli.config.get_keyring_store", return_value=None):
        result = runner.invoke(
            app,
            ["credentials", "check", "--host", host, "--org-api-key", "nonexistent"],
        )
    assert result.exit_code == 1
    out = strip_ansi(result.output)
    assert "user: missing" in out
    assert "org (nonexistent): missing" in out


def test_check_org_requires_label(runner, runlayer_home):
    host = "http://localhost:9999"

    result = runner.invoke(app, ["credentials", "check", "--host", host])
    assert result.exit_code == 1
    assert "--org-api-key is required" in result.output


# ── enroll (mock HTTP backend) ───────────────────────────────────────


def test_enroll_success(runner, runlayer_home, httpserver):
    httpserver.expect_request("/api/v1/mdm/enroll", method="POST").respond_with_json(
        {"api_key": "rl_user_enrolled"}
    )

    host = httpserver.url_for("")

    with patch("runlayer_cli.config.get_keyring_store", return_value=None):
        result = runner.invoke(
            app,
            ["credentials", "enroll", "rl_enroll_testkey", "--host", host],
        )
    assert result.exit_code == 0
    assert "Enrollment successful" in strip_ansi(result.output)

    with patch("runlayer_cli.config.get_keyring_store", return_value=None):
        result = runner.invoke(
            app,
            ["credentials", "check", "--host", host, "--skip-org-check"],
        )
    assert result.exit_code == 0
    assert "user: ok" in result.output


def test_enroll_sends_correct_payload(runner, runlayer_home, httpserver):
    received: list[Request] = []

    def _handler(request: Request):
        received.append(request)
        return Response(
            json.dumps({"api_key": "rl_user_enrolled"}),
            status=200,
            content_type="application/json",
        )

    httpserver.expect_request("/api/v1/mdm/enroll", method="POST").respond_with_handler(
        _handler
    )

    host = httpserver.url_for("")

    with patch("runlayer_cli.config.get_keyring_store", return_value=None):
        result = runner.invoke(
            app,
            [
                "credentials",
                "enroll",
                "rl_enroll_secret",
                "--host",
                host,
                "--username",
                "alice",
                "--device-name",
                "macbook-pro",
            ],
        )
    assert result.exit_code == 0

    assert len(received) == 1
    req = received[0]
    assert req.headers["Authorization"] == "Bearer rl_enroll_secret"
    assert "Runlayer" in req.headers["User-Agent"]
    body = req.get_json()
    assert body == {"username": "alice", "device_name": "macbook-pro"}


def test_enroll_minimal_body(runner, runlayer_home, httpserver):
    received: list[Request] = []

    def _handler(request: Request):
        received.append(request)
        return Response(
            json.dumps({"api_key": "rl_user_min"}),
            status=200,
            content_type="application/json",
        )

    httpserver.expect_request("/api/v1/mdm/enroll", method="POST").respond_with_handler(
        _handler
    )

    host = httpserver.url_for("")

    with (
        patch("runlayer_cli.config.get_keyring_store", return_value=None),
        patch("runlayer_cli.enrollment.getpass.getuser", return_value="osuser"),
        patch("runlayer_cli.enrollment.socket.gethostname", return_value="oshost"),
    ):
        result = runner.invoke(
            app,
            ["credentials", "enroll", "rl_enroll_key", "--host", host],
        )
    assert result.exit_code == 0
    assert len(received) == 1
    assert received[0].get_json() == {"username": "osuser", "device_name": "oshost"}


def test_enroll_server_error(runner, runlayer_home, httpserver):
    httpserver.expect_request("/api/v1/mdm/enroll", method="POST").respond_with_json(
        {"detail": "Invalid enrollment key"}, status=401
    )

    host = httpserver.url_for("")

    with patch("runlayer_cli.config.get_keyring_store", return_value=None):
        result = runner.invoke(
            app,
            ["credentials", "enroll", "rl_enroll_bad", "--host", host],
        )
    assert result.exit_code == 1
    out = strip_ansi(result.output)
    assert "401" in out
    assert "Invalid enrollment key" in out


def test_enroll_missing_api_key_in_response(runner, runlayer_home, httpserver):
    httpserver.expect_request("/api/v1/mdm/enroll", method="POST").respond_with_json(
        {"other": "data"}
    )

    host = httpserver.url_for("")

    with patch("runlayer_cli.config.get_keyring_store", return_value=None):
        result = runner.invoke(
            app,
            ["credentials", "enroll", "rl_enroll_key", "--host", host],
        )
    assert result.exit_code == 1
    assert "did not contain api_key" in result.output
