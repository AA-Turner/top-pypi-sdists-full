"""Hosted MCP OAuth discovery: RFC 9728 metadata + WWW-Authenticate challenge."""

from __future__ import annotations

import asyncio
import json

import pytest

from probe.mcp.server import with_auth_and_health


async def _inner(scope: dict, receive, send) -> None:
    """A stand-in for the real MCP app: 200 means the request passed the wrapper."""
    await send({"type": "http.response.start", "status": 200, "headers": []})
    await send({"type": "http.response.body", "body": b'{"ok":true}'})


def _call(app, path: str, headers: list | None = None) -> dict:
    out: dict = {}

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(msg):
        if msg["type"] == "http.response.start":
            out["status"] = msg["status"]
            out["headers"] = {k.decode(): v.decode() for k, v in msg["headers"]}
        elif msg["type"] == "http.response.body":
            out["body"] = msg.get("body", b"")

    scope = {"type": "http", "method": "GET", "path": path, "headers": headers or []}
    asyncio.run(app(scope, receive, send))
    return out


@pytest.fixture
def discovery_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PROBE_MCP_OAUTH", "1")
    monkeypatch.setenv("PROBE_MCP_RESOURCE_URL", "https://mcp.test")
    monkeypatch.setenv("PROBE_MCP_AUTH_SERVER", "https://api.test")


def test_protected_resource_metadata(discovery_env) -> None:
    app = with_auth_and_health(_inner)
    res = _call(app, "/.well-known/oauth-protected-resource")
    assert res["status"] == 200
    meta = json.loads(res["body"])
    assert meta["resource"] == "https://mcp.test"
    assert meta["authorization_servers"] == ["https://api.test"]
    assert meta["scopes_supported"] == ["research:read"]


def test_unauthenticated_mcp_request_gets_challenge(discovery_env) -> None:
    app = with_auth_and_health(_inner, mcp_path="/mcp")
    res = _call(app, "/mcp")
    assert res["status"] == 401
    challenge = res["headers"]["www-authenticate"]
    assert challenge.startswith("Bearer ")
    assert 'resource_metadata="https://mcp.test/.well-known/oauth-protected-resource"' in challenge
    assert 'scope="research:read"' in challenge


def test_bearer_request_passes_through(discovery_env) -> None:
    app = with_auth_and_health(_inner, mcp_path="/mcp")
    res = _call(app, "/mcp", headers=[(b"authorization", b"Bearer ros_pat_abc")])
    assert res["status"] == 200  # reached the inner app
    assert json.loads(res["body"]) == {"ok": True}


def test_healthz_always_ok(discovery_env) -> None:
    app = with_auth_and_health(_inner)
    res = _call(app, "/healthz")
    assert res["status"] == 200
    assert json.loads(res["body"]) == {"status": "ok"}


def test_discovery_disabled_skips_challenge(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PROBE_MCP_OAUTH", "0")
    app = with_auth_and_health(_inner, mcp_path="/mcp")
    # No challenge: an unauthenticated request falls through to the inner app.
    assert _call(app, "/mcp")["status"] == 200
    # Metadata endpoint is not served either (falls through to inner).
    assert json.loads(_call(app, "/.well-known/oauth-protected-resource")["body"]) == {"ok": True}


def test_legacy_ros_env_spelling_still_works_with_warning(monkeypatch: pytest.MonkeyPatch) -> None:
    """The pre-rename ROS_MCP_* vars keep working (deprecated) so existing deploys don't break."""
    monkeypatch.delenv("PROBE_MCP_RESOURCE_URL", raising=False)
    monkeypatch.setenv("ROS_MCP_OAUTH", "1")
    monkeypatch.setenv("ROS_MCP_RESOURCE_URL", "https://legacy.test")
    with pytest.warns(UserWarning, match="ROS_MCP_RESOURCE_URL is deprecated"):
        app = with_auth_and_health(_inner)
    res = _call(app, "/.well-known/oauth-protected-resource")
    assert json.loads(res["body"])["resource"] == "https://legacy.test"


def test_probe_env_wins_over_legacy(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PROBE_MCP_RESOURCE_URL", "https://new.test")
    monkeypatch.setenv("ROS_MCP_RESOURCE_URL", "https://legacy.test")
    app = with_auth_and_health(_inner)
    res = _call(app, "/.well-known/oauth-protected-resource")
    assert json.loads(res["body"])["resource"] == "https://new.test"


# -- why a request was refused --------------------------------------------------


@pytest.fixture
def refusals(caplog):
    """The refusal log's lines. Its logger does not propagate (the hosted root
    handler wraps lines), so the capture handler is attached to it directly."""
    import logging

    log = logging.getLogger("probe.mcp.auth")
    log.addHandler(caplog.handler)
    caplog.set_level("INFO", logger="probe.mcp.auth")
    yield lambda: [r.getMessage() for r in caplog.records if r.getMessage().startswith("mcp 401")]
    log.removeHandler(caplog.handler)


@pytest.mark.parametrize("oauth", ["1", "0"], ids=["oauth-on", "oauth-off"])
def test_the_helpers_no_token_placeholder_is_refused_without_asking_the_api(
    monkeypatch, refusals, oauth
) -> None:
    """The Claude Code plugin's helper sends NO_TOKEN_PLACEHOLDER when the computer
    holds no token (never nothing: a bare request draws "Needs authentication" and
    a 15-minute skip in Claude Code). It is refused like a bad token, with the
    wizard named, the API is never asked about it, and it never reaches a tool --
    with OAuth discovery on or off (self-host)."""
    from probe.mcp.server import NO_TOKEN_PLACEHOLDER
    from probe.sdk.session_marker import WIZARD_HINT

    monkeypatch.setenv("PROBE_MCP_OAUTH", oauth)
    monkeypatch.setenv("PROBE_MCP_RESOURCE_URL", "https://mcp.test")
    monkeypatch.setenv("PROBE_MCP_AUTH_SERVER", "https://api.test")

    async def never(_token: str) -> bool:
        raise AssertionError("asked the API about the placeholder")

    app = with_auth_and_health(_inner, mcp_path="/mcp", token_rejected=never)
    res = _call(app, "/mcp", headers=[
        (b"authorization", f"Bearer {NO_TOKEN_PLACEHOLDER}".encode()),
        (b"x-probe-client", b"plugin"),
        (b"x-probe-client-version", b"0.200.0"),
        (b"x-probe-agent", b"claude_code"),
        (b"user-agent", b"claude-code/2.1.296 (external, cli)"),
    ])
    assert res["status"] == 401
    body = json.loads(res["body"])
    assert body == {"error": "invalid_token", "error_description": f"no Probe token on this computer: {WIZARD_HINT}"}
    challenge = res["headers"].get("www-authenticate")
    if oauth == "1":
        # No resource_metadata: there is no sign-in for a client to start from it.
        assert challenge == 'Bearer realm="research", error="invalid_token"'
    else:
        assert challenge is None
    assert refusals() == [
        "mcp 401 reason=no_token_on_device client=plugin/0.200.0 agent=claude_code user_agent=claude-code/2.1.296"
    ]


@pytest.mark.parametrize(
    ("headers", "rejected", "reason"),
    [
        ([], False, "missing"),
        ([(b"authorization", b"Bearer probe_pat_gone")], True, "rejected"),
        ([(b"authorization", b"Bearer \xff\xfe")], False, "rejected"),
        ([(b"authorization", "Bearer probe_pat_é".encode())], False, "rejected"),
    ],
    ids=["missing", "refused", "undecodable", "non-ascii"],
)
def test_every_refusal_logs_its_reason_and_never_the_token(discovery_env, refusals, headers, rejected, reason) -> None:
    async def rejects(_token: str) -> bool:
        return rejected

    app = with_auth_and_health(_inner, mcp_path="/mcp", token_rejected=rejects)
    res = _call(app, "/mcp", headers=headers)
    assert res["status"] == 401 and json.loads(res["body"]) == {"error": "invalid_token"}
    assert "resource_metadata=" in res["headers"]["www-authenticate"]
    (line,) = refusals()
    assert line.startswith(f"mcp 401 reason={reason} ") and "probe_pat_gone" not in line


def test_caller_text_is_logged_only_as_validated_fields(discovery_env, refusals) -> None:
    """Every header but the token is caller-chosen text: a refusal logs only values
    already validated (client kind/version, a known agent) and a User-Agent's
    `product/version`, so a credential pasted into one never reaches the log."""

    async def rejects(_token: str) -> bool:
        return True

    app = with_auth_and_health(_inner, mcp_path="/mcp", token_rejected=rejects)
    _call(app, "/mcp", headers=[
        (b"authorization", b"Bearer probe_pat_gone"),
        (b"x-probe-client", b"plugin reason=missing"),
        (b"x-probe-agent", b"x reason=missing"),
        (b"user-agent", b"probe_pat_secret_in_the_user_agent"),
    ])
    (line,) = refusals()
    assert line == "mcp 401 reason=rejected client=-/- agent=- user_agent=other"
