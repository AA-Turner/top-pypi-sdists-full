"""E2E tests for scan command submission with a mock HTTP backend."""

import json

import httpx
import pytest
from werkzeug import Request, Response

from tests.e2e.conftest import strip_ansi

from runlayer_cli.main import app
from runlayer_cli.scan.client_presence import DetectedClient
from runlayer_cli.scan.service import ScanResult

pytestmark = pytest.mark.no_backend_e2e

SCAN_RESPONSE = {
    "servers_processed": 1,
    "shadow_servers_found": 1,
    "managed_servers_matched": 0,
}


def _invoke_scan(runner, httpserver, **extra_args):
    host = httpserver.url_for("")
    args = ["scan", "--no-projects", "--secret", "rl_org_test", "--host", host]
    for k, v in extra_args.items():
        args.extend([f"--{k}", str(v)])
    return runner.invoke(app, args)


# ── Happy path: server scan ──────────────────────────────────────────


def test_scan_submit_server(runner, scan_home, httpserver):
    received: list[Request] = []

    def _handler(request: Request):
        received.append(request)
        return Response(
            json.dumps(SCAN_RESPONSE), status=200, content_type="application/json"
        )

    httpserver.expect_request(
        "/api/v1/ai-watch/scan", method="POST"
    ).respond_with_handler(_handler)
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/submit", method="POST"
    ).respond_with_json({})
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/submit", method="POST"
    ).respond_with_json({"plugin_id": "x", "created": False})

    result = _invoke_scan(runner, httpserver)
    assert result.exit_code == 0, strip_ansi(result.output)

    out = strip_ansi(result.output)
    assert "Scan complete" in out

    assert len(received) == 1
    body = received[0].get_json()
    assert "configurations" in body
    assert len(body["configurations"]) >= 1
    assert "device_id" in body
    assert "hostname" in body
    assert "os" in body
    assert body["configurations"][0]["servers"][0]["name"] == "test-server"


def test_scan_submit_detected_client_without_mcp_config(
    runner, httpserver, monkeypatch
):
    received: list[Request] = []
    detected_result = ScanResult(
        device_id="device-1",
        hostname="host-1",
        os="darwin",
        os_version="15.0",
        username="user-1",
        org_device_id=None,
        scan_duration_ms=1,
        collector_version="1.2.3",
        configurations=[],
        detected_clients=[
            DetectedClient(
                client="cursor",
                display_name="Cursor",
                client_version="1.0.0",
                detected_via=["app"],
            )
        ],
    )

    def _handler(request: Request):
        received.append(request)
        return Response(
            json.dumps(
                {
                    "servers_processed": 0,
                    "shadow_servers_found": 0,
                    "managed_servers_matched": 0,
                }
            ),
            status=200,
            content_type="application/json",
        )

    monkeypatch.setattr(
        "runlayer_cli.commands.scan.scan_all_clients",
        lambda **_kwargs: detected_result,
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.scan._submit_scan_checkins_best_effort",
        lambda *_args: None,
    )
    httpserver.expect_request(
        "/api/v1/ai-watch/scan", method="POST"
    ).respond_with_handler(_handler)

    result = _invoke_scan(runner, httpserver)

    assert result.exit_code == 0, strip_ansi(result.output)
    assert "1 AI clients detected" in strip_ansi(result.output)
    assert len(received) == 1
    assert received[0].get_json()["detected_clients"] == [
        {
            "client": "cursor",
            "display_name": "Cursor",
            "client_version": "1.0.0",
            "detected_via": ["app"],
            "config_paths": [],
        }
    ]


def test_scan_submit_with_findings_skips_detect_checkin(
    runner, scan_home, httpserver, monkeypatch
):
    detect_checkins = []

    monkeypatch.setattr(
        "runlayer_cli.aiwatch_checkin.submit_detect_checkin",
        lambda _client, scan_result: detect_checkins.append(scan_result),
    )
    monkeypatch.setattr(
        "runlayer_cli.aiwatch_checkin.submit_enforce_validation_checkin",
        lambda _client, **_kwargs: None,
    )
    monkeypatch.setattr(
        "runlayer_cli.aiwatch_checkin.submit_sessions_validation_checkin",
        lambda _client, **_kwargs: None,
    )

    httpserver.expect_request("/api/v1/ai-watch/scan", method="POST").respond_with_json(
        SCAN_RESPONSE
    )
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/submit", method="POST"
    ).respond_with_json({})
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/submit", method="POST"
    ).respond_with_json({"plugin_id": "x", "created": False})

    result = _invoke_scan(runner, httpserver)

    assert result.exit_code == 0, strip_ansi(result.output)
    assert detect_checkins == []


def test_scan_no_findings_records_detect_checkin(runner, httpserver, monkeypatch):
    empty_result = ScanResult(
        device_id="device-1",
        hostname="host-1",
        os="darwin",
        os_version="15.0",
        username="user-1",
        org_device_id=None,
        scan_duration_ms=1,
        collector_version="1.2.3",
        configurations=[],
    )
    detect_checkins = []

    monkeypatch.setattr(
        "runlayer_cli.commands.scan.scan_all_clients",
        lambda **_kwargs: empty_result,
    )
    monkeypatch.setattr(
        "runlayer_cli.aiwatch_checkin.submit_detect_checkin",
        lambda _client, scan_result: detect_checkins.append(scan_result),
    )
    monkeypatch.setattr(
        "runlayer_cli.aiwatch_checkin.submit_enforce_validation_checkin",
        lambda _client, **_kwargs: None,
    )
    monkeypatch.setattr(
        "runlayer_cli.aiwatch_checkin.submit_sessions_validation_checkin",
        lambda _client, **_kwargs: None,
    )

    result = _invoke_scan(runner, httpserver)

    assert result.exit_code == 0, strip_ansi(result.output)
    assert (
        "No AI clients, MCP servers, skills, plugins, agents, processes, "
        "or containers found." in strip_ansi(result.output)
    )
    assert detect_checkins == [empty_result]


# ── Skill: unknown -> lookup + submit ────────────────────────────────


def test_scan_submit_skill_unknown(runner, scan_home, httpserver):
    skill_requests: list[Request] = []

    def _skill_lookup(request: Request):
        skill_requests.append(request)
        return Response(
            json.dumps({"known": False}), status=200, content_type="application/json"
        )

    def _skill_submit(request: Request):
        skill_requests.append(request)
        return Response(json.dumps({}), status=200, content_type="application/json")

    httpserver.expect_request("/api/v1/ai-watch/scan", method="POST").respond_with_json(
        SCAN_RESPONSE
    )
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/lookup", method="POST"
    ).respond_with_handler(_skill_lookup)
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/submit", method="POST"
    ).respond_with_handler(_skill_submit)
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/submit", method="POST"
    ).respond_with_json({"plugin_id": "x", "created": False})

    result = _invoke_scan(runner, httpserver)
    assert result.exit_code == 0, strip_ansi(result.output)

    assert len(skill_requests) == 2
    lookup_body = skill_requests[0].get_json()
    assert "identifier" in lookup_body
    assert "artifact_type" in lookup_body
    submit_body = skill_requests[1].get_json()
    assert "files" in submit_body
    assert "identifier" in submit_body


# ── Skill: known -> submit with empty files ──────────────────────────


def test_scan_submit_skill_known(runner, scan_home, httpserver):
    submit_bodies: list[dict] = []

    def _submit_handler(request: Request):
        submit_bodies.append(request.get_json())
        return Response("{}", status=200, content_type="application/json")

    httpserver.expect_request("/api/v1/ai-watch/scan", method="POST").respond_with_json(
        SCAN_RESPONSE
    )
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/submit", method="POST"
    ).respond_with_handler(_submit_handler)
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/submit", method="POST"
    ).respond_with_json({"plugin_id": "x", "created": False})

    result = _invoke_scan(runner, httpserver)
    assert result.exit_code == 0, strip_ansi(result.output)
    assert len(submit_bodies) >= 1
    assert submit_bodies[0]["files"] == []


# ── Plugin: unknown -> lookup + submit ───────────────────────────────


def test_scan_submit_plugin_unknown(runner, scan_home, httpserver):
    plugin_requests: list[Request] = []

    def _plugin_lookup(request: Request):
        plugin_requests.append(request)
        return Response(
            json.dumps({"known": False}), status=200, content_type="application/json"
        )

    def _plugin_submit(request: Request):
        plugin_requests.append(request)
        return Response(
            json.dumps({"plugin_id": "x", "created": True}),
            status=200,
            content_type="application/json",
        )

    httpserver.expect_request("/api/v1/ai-watch/scan", method="POST").respond_with_json(
        SCAN_RESPONSE
    )
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/submit", method="POST"
    ).respond_with_json({})
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/lookup", method="POST"
    ).respond_with_handler(_plugin_lookup)
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/submit", method="POST"
    ).respond_with_handler(_plugin_submit)

    result = _invoke_scan(runner, httpserver)
    assert result.exit_code == 0, strip_ansi(result.output)

    assert len(plugin_requests) == 2
    lookup_body = plugin_requests[0].get_json()
    assert "identifier" in lookup_body
    submit_body = plugin_requests[1].get_json()
    assert "files" in submit_body
    assert "name" in submit_body


# ── Plugin: known -> submit with empty files ─────────────────────────


def test_scan_submit_plugin_known(runner, scan_home, httpserver):
    submit_bodies: list[dict] = []

    def _submit_handler(request: Request):
        submit_bodies.append(request.get_json())
        return Response(
            json.dumps({"plugin_id": "x", "created": False}),
            status=200,
            content_type="application/json",
        )

    httpserver.expect_request("/api/v1/ai-watch/scan", method="POST").respond_with_json(
        SCAN_RESPONSE
    )
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/submit", method="POST"
    ).respond_with_json({})
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/submit", method="POST"
    ).respond_with_handler(_submit_handler)

    result = _invoke_scan(runner, httpserver)
    assert result.exit_code == 0, strip_ansi(result.output)
    assert len(submit_bodies) >= 1
    assert submit_bodies[0]["files"] == []


# ── Fallback: ai-watch 404 -> mcp-watch ─────────────────────────────


def test_scan_fallback_to_mcp_watch(runner, scan_home, httpserver):
    fallback_requests: list[Request] = []

    def _mcp_watch_handler(request: Request):
        fallback_requests.append(request)
        return Response(
            json.dumps(SCAN_RESPONSE), status=200, content_type="application/json"
        )

    httpserver.expect_request("/api/v1/ai-watch/scan", method="POST").respond_with_json(
        {}, status=404
    )
    httpserver.expect_request(
        "/api/v1/mcp-watch/scan", method="POST"
    ).respond_with_handler(_mcp_watch_handler)
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/submit", method="POST"
    ).respond_with_json({})
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/submit", method="POST"
    ).respond_with_json({"plugin_id": "x", "created": False})

    result = _invoke_scan(runner, httpserver)
    assert result.exit_code == 0, strip_ansi(result.output)
    assert "Scan complete" in strip_ansi(result.output)
    assert len(fallback_requests) == 1


# ── Unsupported: both 404 ────────────────────────────────────────────


def test_scan_unsupported_server(runner, scan_home, httpserver):
    httpserver.expect_request("/api/v1/ai-watch/scan", method="POST").respond_with_json(
        {}, status=404
    )
    httpserver.expect_request(
        "/api/v1/mcp-watch/scan", method="POST"
    ).respond_with_json({}, status=404)
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/submit", method="POST"
    ).respond_with_json({})
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/submit", method="POST"
    ).respond_with_json({"plugin_id": "x", "created": False})

    result = _invoke_scan(runner, httpserver)
    assert result.exit_code == 2, strip_ansi(result.output)
    assert "not supported" in strip_ansi(result.output)


def test_scan_submission_failure_is_not_reported_as_unsupported(
    runner, scan_home, httpserver, monkeypatch
):
    httpserver.expect_request("/api/v1/ai-watch/scan", method="POST").respond_with_json(
        SCAN_RESPONSE
    )
    monkeypatch.setattr(
        "runlayer_cli.scan.service.submit_discovered_skills",
        lambda client, skills, scan_result=None, artifact_cache=None: "failed",
    )
    monkeypatch.setattr(
        "runlayer_cli.scan.service.submit_discovered_plugins",
        lambda client, plugins, scan_result=None, artifact_cache=None: "success",
    )

    result = _invoke_scan(runner, httpserver)
    out = strip_ansi(result.output)

    assert result.exit_code == 3, out
    assert "Could not submit skills; scan may be incomplete" in out
    assert "Shadow Skill Detection not supported" not in out


# ── Exit codes: skills/plugins unsupported / failed / precedence ─────


def test_scan_skills_unsupported_exits_2(runner, scan_home, httpserver, monkeypatch):
    httpserver.expect_request("/api/v1/ai-watch/scan", method="POST").respond_with_json(
        SCAN_RESPONSE
    )
    monkeypatch.setattr(
        "runlayer_cli.scan.service.submit_discovered_skills",
        lambda client, skills, scan_result=None, artifact_cache=None: "unsupported",
    )
    monkeypatch.setattr(
        "runlayer_cli.scan.service.submit_discovered_plugins",
        lambda client, plugins, scan_result=None, artifact_cache=None: "success",
    )

    result = _invoke_scan(runner, httpserver)
    out = strip_ansi(result.output)

    assert result.exit_code == 2, out
    assert "Shadow Skill Detection not supported" in out


def test_scan_plugins_failed_exits_3(runner, scan_home, httpserver, monkeypatch):
    httpserver.expect_request("/api/v1/ai-watch/scan", method="POST").respond_with_json(
        SCAN_RESPONSE
    )
    monkeypatch.setattr(
        "runlayer_cli.scan.service.submit_discovered_skills",
        lambda client, skills, scan_result=None, artifact_cache=None: "success",
    )
    monkeypatch.setattr(
        "runlayer_cli.scan.service.submit_discovered_plugins",
        lambda client, plugins, scan_result=None, artifact_cache=None: "failed",
    )

    result = _invoke_scan(runner, httpserver)
    out = strip_ansi(result.output)

    assert result.exit_code == 3, out
    assert "Could not submit plugins; scan may be incomplete" in out


def test_scan_failed_outranks_unsupported(runner, scan_home, httpserver, monkeypatch):
    httpserver.expect_request("/api/v1/ai-watch/scan", method="POST").respond_with_json(
        SCAN_RESPONSE
    )
    monkeypatch.setattr(
        "runlayer_cli.scan.service.submit_discovered_skills",
        lambda client, skills, scan_result=None, artifact_cache=None: "unsupported",
    )
    monkeypatch.setattr(
        "runlayer_cli.scan.service.submit_discovered_plugins",
        lambda client, plugins, scan_result=None, artifact_cache=None: "failed",
    )

    result = _invoke_scan(runner, httpserver)

    assert result.exit_code == 3, strip_ansi(result.output)


def test_scan_server_network_error_exits_3(runner, scan_home, httpserver, monkeypatch):
    def _boom(self, payload):
        raise httpx.ConnectError("backend unreachable")

    monkeypatch.setattr("runlayer_cli.api.RunlayerClient.submit_mcp_watch_scan", _boom)
    monkeypatch.setattr(
        "runlayer_cli.scan.service.submit_discovered_skills",
        lambda client, skills, scan_result=None, artifact_cache=None: "success",
    )
    monkeypatch.setattr(
        "runlayer_cli.scan.service.submit_discovered_plugins",
        lambda client, plugins, scan_result=None, artifact_cache=None: "success",
    )

    result = _invoke_scan(runner, httpserver)
    out = strip_ansi(result.output)

    assert result.exit_code == 3, out
    assert "Could not submit servers; scan may be incomplete" in out


# ── Submit 5xx (HTTP status error) must fail, not silent-green ───────


def test_scan_skill_submit_500_exits_3(runner, scan_home, httpserver):
    httpserver.expect_request("/api/v1/ai-watch/scan", method="POST").respond_with_json(
        SCAN_RESPONSE
    )
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/submit", method="POST"
    ).respond_with_json({"detail": "boom"}, status=500)
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/submit", method="POST"
    ).respond_with_json({"plugin_id": "x", "created": False})

    result = _invoke_scan(runner, httpserver)
    out = strip_ansi(result.output)

    assert result.exit_code == 3, out
    assert "Could not submit skills; scan may be incomplete" in out


def test_scan_plugin_submit_500_exits_3(runner, scan_home, httpserver):
    httpserver.expect_request("/api/v1/ai-watch/scan", method="POST").respond_with_json(
        SCAN_RESPONSE
    )
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/submit", method="POST"
    ).respond_with_json({})
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/submit", method="POST"
    ).respond_with_json({"detail": "boom"}, status=500)

    result = _invoke_scan(runner, httpserver)
    out = strip_ansi(result.output)

    assert result.exit_code == 3, out
    assert "Could not submit plugins; scan may be incomplete" in out


def test_scan_server_500_still_submits_skills_and_plugins(
    runner, scan_home, httpserver
):
    skill_submits: list[Request] = []
    plugin_submits: list[Request] = []

    def _skill_submit(request: Request):
        skill_submits.append(request)
        return Response(json.dumps({}), status=200, content_type="application/json")

    def _plugin_submit(request: Request):
        plugin_submits.append(request)
        return Response(
            json.dumps({"plugin_id": "x", "created": False}),
            status=200,
            content_type="application/json",
        )

    httpserver.expect_request("/api/v1/ai-watch/scan", method="POST").respond_with_json(
        {"detail": "boom"}, status=500
    )
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/submit", method="POST"
    ).respond_with_handler(_skill_submit)
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/submit", method="POST"
    ).respond_with_handler(_plugin_submit)

    result = _invoke_scan(runner, httpserver)
    out = strip_ansi(result.output)

    assert result.exit_code == 3, out
    assert "Could not submit servers; scan may be incomplete" in out
    assert len(skill_submits) >= 1
    assert len(plugin_submits) >= 1


# ── No-findings check-in failures stay best-effort (exit 0) ──────────


def test_scan_no_findings_checkin_failure_still_exits_0(
    runner, httpserver, monkeypatch
):
    empty_result = ScanResult(
        device_id="device-1",
        hostname="host-1",
        os="darwin",
        os_version="15.0",
        username="user-1",
        org_device_id=None,
        scan_duration_ms=1,
        collector_version="1.2.3",
        configurations=[],
    )

    monkeypatch.setattr(
        "runlayer_cli.commands.scan.scan_all_clients",
        lambda **_kwargs: empty_result,
    )

    def _boom(_client, _result):
        raise httpx.ConnectError("backend unreachable")

    monkeypatch.setattr("runlayer_cli.aiwatch_checkin.submit_detect_checkin", _boom)
    monkeypatch.setattr(
        "runlayer_cli.aiwatch_checkin.submit_enforce_validation_checkin",
        lambda _client, **_kwargs: None,
    )
    monkeypatch.setattr(
        "runlayer_cli.aiwatch_checkin.submit_sessions_validation_checkin",
        lambda _client, **_kwargs: None,
    )

    result = _invoke_scan(runner, httpserver)

    assert result.exit_code == 0, strip_ansi(result.output)
    assert (
        "No AI clients, MCP servers, skills, plugins, agents, processes, "
        "or containers found." in strip_ansi(result.output)
    )


# ── Error: 401 ───────────────────────────────────────────────────────


def test_scan_auth_error(runner, scan_home, httpserver):
    httpserver.expect_request("/api/v1/ai-watch/scan", method="POST").respond_with_json(
        {"detail": "Unauthorized"}, status=401
    )

    result = _invoke_scan(runner, httpserver)
    assert result.exit_code == 1


# ── Error: 401/403 on skill/plugin submit -> exit 1 (auth, not exit 3) ─


def test_scan_skill_submit_401_exits_1(runner, scan_home, httpserver):
    """A 401 while submitting skills is an auth error: exit 1, not exit 3.

    Skills/plugins share the server submission contract: 401/403 re-raise so
    the scan reports the generic auth error rather than a submission failure.
    """
    httpserver.expect_request("/api/v1/ai-watch/scan", method="POST").respond_with_json(
        SCAN_RESPONSE
    )
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/submit", method="POST"
    ).respond_with_json({"detail": "Unauthorized"}, status=401)

    result = _invoke_scan(runner, httpserver)
    out = strip_ansi(result.output)

    assert result.exit_code == 1, out
    assert "Could not submit skills" not in out


def test_scan_plugin_submit_403_exits_1(runner, scan_home, httpserver):
    """A 403 while submitting plugins is an auth error: exit 1, not exit 3."""
    httpserver.expect_request("/api/v1/ai-watch/scan", method="POST").respond_with_json(
        SCAN_RESPONSE
    )
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/submit", method="POST"
    ).respond_with_json({})
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/submit", method="POST"
    ).respond_with_json({"detail": "Forbidden"}, status=403)

    result = _invoke_scan(runner, httpserver)
    out = strip_ansi(result.output)

    assert result.exit_code == 1, out
    assert "Could not submit plugins" not in out


# ── Error: 500 (submission failure, not silent-green) ────────────────


def test_scan_server_error(runner, scan_home, httpserver):
    httpserver.expect_request("/api/v1/ai-watch/scan", method="POST").respond_with_json(
        {"detail": "Internal Server Error"}, status=500
    )
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/skills/submit", method="POST"
    ).respond_with_json({})
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/lookup", method="POST"
    ).respond_with_json({"known": True})
    httpserver.expect_request(
        "/api/v1/ai-watch/plugins/submit", method="POST"
    ).respond_with_json({"plugin_id": "x", "created": False})

    result = _invoke_scan(runner, httpserver)
    out = strip_ansi(result.output)

    assert result.exit_code == 3, out
    assert "Could not submit servers; scan may be incomplete" in out
