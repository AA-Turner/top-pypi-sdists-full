"""E2E tests for scan command submission with a mock HTTP backend."""

import json

import pytest
from werkzeug import Request, Response

from tests.e2e.conftest import strip_ansi

from runlayer_cli.main import app

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
    assert result.exit_code == 0, strip_ansi(result.output)
    assert "not supported" in strip_ansi(result.output)


def test_scan_submission_failure_is_not_reported_as_unsupported(
    runner, scan_home, httpserver, monkeypatch
):
    httpserver.expect_request("/api/v1/ai-watch/scan", method="POST").respond_with_json(
        SCAN_RESPONSE
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.scan.submit_discovered_skills",
        lambda client, skills, scan_result=None: "failed",
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.scan.submit_discovered_plugins",
        lambda client, plugins, scan_result=None: "success",
    )

    result = _invoke_scan(runner, httpserver)
    out = strip_ansi(result.output)

    assert result.exit_code == 0, out
    assert "Could not submit skills; scan may be incomplete" in out
    assert "Shadow Skill Detection not supported" not in out


# ── Error: 401 ───────────────────────────────────────────────────────


def test_scan_auth_error(runner, scan_home, httpserver):
    httpserver.expect_request("/api/v1/ai-watch/scan", method="POST").respond_with_json(
        {"detail": "Unauthorized"}, status=401
    )

    result = _invoke_scan(runner, httpserver)
    assert result.exit_code == 1


# ── Error: 500 ───────────────────────────────────────────────────────


def test_scan_server_error(runner, scan_home, httpserver):
    httpserver.expect_request("/api/v1/ai-watch/scan", method="POST").respond_with_json(
        {"detail": "Internal Server Error"}, status=500
    )

    result = _invoke_scan(runner, httpserver)
    assert result.exit_code == 1
