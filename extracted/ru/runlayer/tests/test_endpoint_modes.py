"""Focused endpoint-mode behavior for AI Watch hooks."""

from __future__ import annotations

import json
import os
import sys
from io import StringIO
from unittest.mock import patch

import pytest

from runlayer_cli.hook import dispatch
from runlayer_cli.hook.clients import Client, HookResponse
from runlayer_cli.mdm_config import AIWatchMode


def _mark_frozen_aiwatch(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    executable = tmp_path / "aiwatch"
    executable.write_text("")
    monkeypatch.setattr(sys, "executable", str(executable), raising=False)


def test_frozen_protect_mode_overrides_legacy_enforcement(
    monkeypatch, tmp_path
) -> None:
    _mark_frozen_aiwatch(monkeypatch, tmp_path)
    monkeypatch.setattr(
        "runlayer_cli.mdm_config.read_managed_config",
        lambda: {"mode": AIWatchMode.PROTECT, "enforcement": True},
    )

    assert dispatch._resolve_mode() is AIWatchMode.PROTECT


def test_operator_hook_uses_explicit_mode(monkeypatch, tmp_path) -> None:
    """The mode persisted by ``setup hooks`` controls the unfrozen hook."""
    monkeypatch.setattr(
        sys,
        "argv",
        [str(tmp_path / "runlayer"), "--client", "cursor", "--mode", "protect"],
    )

    assert dispatch._resolve_mode() is AIWatchMode.PROTECT


def test_frozen_monitor_resolves_metadata_only_profile(monkeypatch, tmp_path) -> None:
    _mark_frozen_aiwatch(monkeypatch, tmp_path)
    monkeypatch.setattr(
        "runlayer_cli.mdm_config.read_managed_config",
        lambda: {
            "mode": AIWatchMode.MONITOR,
            "sessions": False,
            "mcp_usage_metadata": True,
        },
    )

    assert dispatch._resolve_metadata_only() is True


def test_frozen_monitor_scan_only_profile_resolves_noop(monkeypatch, tmp_path) -> None:
    _mark_frozen_aiwatch(monkeypatch, tmp_path)
    monkeypatch.setattr(
        "runlayer_cli.mdm_config.read_managed_config",
        lambda: {
            "mode": AIWatchMode.MONITOR,
            "sessions": False,
            "mcp_usage_metadata": False,
        },
    )

    assert dispatch._resolve_scan_only() is True
    assert dispatch._resolve_metadata_only() is False


def test_stale_hook_on_scan_only_profile_sends_nothing(
    monkeypatch, tmp_path, capsys
) -> None:
    """Monitor + Sessions off + MCPUsageMetadata off is scan-only: a stale
    installed hook must allow without relaying any content — the settings the
    profile disables must not fall through to full Monitor dispatch."""
    _mark_frozen_aiwatch(monkeypatch, tmp_path)
    monkeypatch.setattr(
        "runlayer_cli.mdm_config.read_managed_config",
        lambda: {
            "mode": AIWatchMode.MONITOR,
            "sessions": False,
            "mcp_usage_metadata": False,
        },
    )
    for relay_name in (
        "forward_event",
        "forward_tool_lifecycle",
        "check_tool_lifecycle",
        "enforce",
        "forward_mcp_usage_metadata",
    ):
        monkeypatch.setattr(
            dispatch,
            relay_name,
            lambda *_args, _relay=relay_name, **_kwargs: pytest.fail(
                f"scan-only profile relayed content via {_relay}"
            ),
        )
    monkeypatch.setattr(
        dispatch.flow_spool,
        "spool_append",
        lambda *_: pytest.fail("scan-only profile spooled flow telemetry"),
    )
    payload = {
        "hook_event_name": "beforeMCPExecution",
        "tool_name": "create_issue",
        "tool_input": {"body": "SECRET-MUST-STAY-LOCAL"},
        "conversation_id": "session-must-stay-local",
    }
    env = {
        key: value
        for key, value in os.environ.items()
        if key not in {"CURSOR_VERSION", "HOOK_EVENT_NAME", "RUNLAYER_HOOK_CLIENT"}
    }
    monkeypatch.setattr(sys, "stdin", StringIO(json.dumps(payload)))

    with (
        patch.dict(os.environ, env, clear=True),
        patch.object(sys, "argv", ["/usr/local/bin/aiwatch"]),
    ):
        dispatch.run_hook()

    assert json.loads(capsys.readouterr().out) == {"permission": "allow"}


def test_sessions_key_absent_stays_scan_only(monkeypatch, tmp_path, capsys) -> None:
    """MCPUsageMetadata=true with the Sessions key ABSENT must fail closed:
    metadata-only requires an explicit Sessions=false, so no hooks should be
    installed and a firing hook must relay nothing — never fall through to
    full Monitor dispatch (David's repro, assertion flipped)."""
    _mark_frozen_aiwatch(monkeypatch, tmp_path)
    monkeypatch.setattr(
        "runlayer_cli.mdm_config.read_managed_config",
        lambda: {"mode": AIWatchMode.MONITOR, "mcp_usage_metadata": True},
    )
    forwarded: list[object] = []
    monkeypatch.setattr(
        dispatch,
        "forward_event",
        lambda _client, _event, payload, **_kw: forwarded.append(payload),
    )
    monkeypatch.setattr(
        dispatch,
        "forward_mcp_usage_metadata",
        lambda **kwargs: forwarded.append(kwargs),
    )
    monkeypatch.setattr(dispatch.flow_spool, "spool_append", lambda *_: None)
    payload = {
        "hook_event_name": "PreToolUse",
        "tool_name": "mcp__github__create_issue",
        "tool_input": {"body": "SECRET-MUST-STAY-LOCAL"},
        "session_id": "session-must-stay-local",
    }
    env = {
        key: value
        for key, value in os.environ.items()
        if key not in {"CURSOR_VERSION", "HOOK_EVENT_NAME", "RUNLAYER_HOOK_CLIENT"}
    }
    env["CLAUDE_CODE"] = "1"
    monkeypatch.setattr(sys, "stdin", StringIO(json.dumps(payload)))

    with (
        patch.dict(os.environ, env, clear=True),
        patch.object(sys, "argv", ["/usr/local/bin/aiwatch"]),
    ):
        dispatch.run_hook()

    capsys.readouterr()
    assert forwarded == []


def test_metadata_only_ignores_post_call_events(monkeypatch, capsys) -> None:
    """A stale PostToolUse hook firing into the metadata profile must not
    produce a second observation for the same call."""
    observed: list[dict[str, object]] = []
    monkeypatch.setattr(
        dispatch,
        "forward_mcp_usage_metadata",
        lambda **kwargs: observed.append(kwargs),
    )

    for hook_type in ("PreToolUse", "PostToolUse"):
        dispatch._handle_mcp_usage_metadata_only(
            hook_type=hook_type,
            original_hook_type=hook_type,
            client=Client.CLAUDE_CODE,
            resp=HookResponse(Client.CLAUDE_CODE, hook_type),
            input_data={
                "tool_name": "mcp__github__create_issue",
                "tool_response": {"body": "SECRET-MUST-STAY-LOCAL"},
            },
            debug=False,
        )

    assert len(observed) == 1
    assert observed[0]["tool_name"] == "mcp__github__create_issue"
    capsys.readouterr()


def test_metadata_only_allows_before_forwarding(monkeypatch) -> None:
    """The allow response is written before the best-effort observation send,
    so the daemon-less sync fallback never sits in front of the tool call."""
    order: list[str] = []
    monkeypatch.setattr(dispatch, "_write", lambda *_a, **_k: order.append("allow"))
    monkeypatch.setattr(
        dispatch,
        "forward_mcp_usage_metadata",
        lambda **_kwargs: order.append("forward"),
    )

    dispatch._handle_mcp_usage_metadata_only(
        hook_type="PreToolUse",
        original_hook_type="PreToolUse",
        client=Client.CLAUDE_CODE,
        resp=HookResponse(Client.CLAUDE_CODE, "PreToolUse"),
        input_data={"tool_name": "mcp__github__create_issue"},
        debug=False,
    )

    assert order == ["allow", "forward"]


def test_metadata_pre_call_events_match_install_profile() -> None:
    """Dispatch's pre-call gate must equal the union of the per-client
    metadata install profile (single source lives in hook_install.clients;
    dispatch keeps a literal copy because the install module imports yaml,
    which must stay off the hook hot path)."""
    from runlayer_cli.hook_install.clients import _MCP_USAGE_METADATA_HOOKS

    installed = {
        name for names in _MCP_USAGE_METADATA_HOOKS.values() for name in names
    }
    assert dispatch._MCP_USAGE_PRE_CALL_EVENTS == frozenset(installed)


def test_metadata_only_dispatch_sends_name_not_tool_contents(
    monkeypatch, capsys
) -> None:
    observed: list[dict[str, object]] = []
    for full_payload_relay in (
        "forward_event",
        "forward_tool_lifecycle",
        "check_tool_lifecycle",
        "enforce",
    ):
        monkeypatch.setattr(
            dispatch,
            full_payload_relay,
            lambda *_args, _relay=full_payload_relay, **_kwargs: pytest.fail(
                f"metadata-only dispatch called {_relay}"
            ),
        )
    monkeypatch.setattr(
        dispatch,
        "forward_mcp_usage_metadata",
        lambda **kwargs: observed.append(kwargs),
    )

    dispatch._handle_mcp_usage_metadata_only(
        hook_type="PreToolUse",
        original_hook_type="PreToolUse",
        client=Client.CLAUDE_CODE,
        resp=HookResponse(Client.CLAUDE_CODE, "PreToolUse"),
        input_data={
            "tool_name": "mcp__github__create_issue",
            "tool_input": {"body": "SECRET-MUST-STAY-LOCAL"},
            "session_id": "session-must-stay-local",
        },
        debug=False,
    )

    assert observed == [
        {
            "client_name": "claude_code",
            "tool_name": "mcp__github__create_issue",
            "mcp_server_name": "github",
            "debug": False,
        }
    ]
    assert capsys.readouterr().out == ""


def test_metadata_only_cursor_allow_never_echoes_tool_contents(
    monkeypatch, capsys
) -> None:
    observed: list[dict[str, object]] = []
    monkeypatch.setattr(
        dispatch,
        "forward_mcp_usage_metadata",
        lambda **kwargs: observed.append(kwargs),
    )

    dispatch._handle_mcp_usage_metadata_only(
        hook_type="beforeMCPExecution",
        original_hook_type="beforeMCPExecution",
        client=Client.CURSOR,
        resp=HookResponse(Client.CURSOR, "beforeMCPExecution"),
        input_data={
            "command": "github",
            "tool_name": "create_issue",
            "tool_input": {"body": "SECRET-MUST-STAY-LOCAL"},
        },
        debug=False,
    )

    assert observed == [
        {
            "client_name": "cursor",
            "tool_name": "create_issue",
            "mcp_server_name": "github",
            "debug": False,
        }
    ]
    assert capsys.readouterr().out == '{"permission":"allow"}'


def test_metadata_only_cursor_strips_mcp_scope_metadata(monkeypatch, capsys) -> None:
    observed: list[dict[str, object]] = []
    monkeypatch.setattr(
        dispatch,
        "forward_mcp_usage_metadata",
        lambda **kwargs: observed.append(kwargs),
    )

    dispatch._handle_mcp_usage_metadata_only(
        hook_type="beforeMCPExecution",
        original_hook_type="beforeMCPExecution",
        client=Client.CURSOR,
        resp=HookResponse(Client.CURSOR, "beforeMCPExecution"),
        input_data={
            "command": "user-github::mcpScope:profile:aWQ6TWpBMllqZzROV00:cfg:OWM0MmE2YzA",
            "tool_name": "create_issue",
        },
        debug=False,
    )

    assert observed == [
        {
            "client_name": "cursor",
            "tool_name": "create_issue",
            # ::mcpScope: routing metadata stripped AND the user- profile
            # prefix normalized away, matching mcp_lookup's aliasing so
            # observed rows share the enforce path's aggregation key.
            "mcp_server_name": "github",
            "debug": False,
        }
    ]
    assert capsys.readouterr().out == '{"permission":"allow"}'


def test_protect_scans_read_without_enforce_policy_and_sends_mode(
    monkeypatch, capsys
) -> None:
    checks: list[str] = []
    requests: list[dict[str, object]] = []
    monkeypatch.setattr(
        dispatch,
        "check_file_read",
        lambda _path: pytest.fail("Protect must not apply local file policy"),
    )
    monkeypatch.setattr(dispatch, "forward_event", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        "runlayer_cli.hook.relay._load_credentials",
        lambda: ("https://runlayer.example", "secret"),
    )

    def _post(_host, _secret, payload, *, target, **_kwargs):
        checks.append(target)
        requests.append(json.loads(payload))
        return '{"permission":"allow"}'

    monkeypatch.setattr("runlayer_cli.hook.relay._post", _post)

    dispatch._handle_pre_tool_use(
        client=Client.CLAUDE_CODE,
        resp=HookResponse(Client.CLAUDE_CODE, "PreToolUse"),
        input_data={
            "tool_name": "Read",
            "tool_input": {"file_path": "/project/.env"},
        },
        original_hook_type="PreToolUse",
        mode=AIWatchMode.PROTECT,
        debug=False,
    )

    assert checks == ["tool-pre"]
    assert requests[0]["mode"] == "protect"
    assert capsys.readouterr().out == ""


def _run_protect_configured_mcp() -> None:
    dispatch._handle_pre_tool_use(
        client=Client.CLAUDE_CODE,
        resp=HookResponse(Client.CLAUDE_CODE, "PreToolUse"),
        input_data={
            "tool_name": "mcp__linear__list_issues",
            "tool_input": {"query": "security"},
        },
        original_hook_type="PreToolUse",
        mode=AIWatchMode.PROTECT,
        debug=False,
    )


def _configure_protect_configured_mcp(
    monkeypatch,
    *,
    response: str = '{"permission":"allow","evaluated_mode":"protect"}',
    relay_error: dispatch.RelayError | None = None,
    lookup_error: Exception | None = None,
) -> tuple[list[dict[str, object]], list[str], list[str]]:
    requests: list[dict[str, object]] = []
    checks: list[str] = []
    events: list[str] = []

    def _lookup(*_args, **_kwargs):
        if lookup_error is not None:
            raise lookup_error
        return {"url": "https://mcp.linear.example/sse"}

    def _enforce(payload: str, **_kwargs) -> str:
        requests.append(json.loads(payload))
        if relay_error is not None:
            raise relay_error
        return response

    def _check(target, *_args, **_kwargs) -> str:
        checks.append(target)
        return '{"permission":"allow"}'

    monkeypatch.setattr(
        dispatch,
        "forward_event",
        lambda _client, event, *_args, **_kwargs: events.append(event),
    )
    monkeypatch.setattr(dispatch, "lookup_mcp_server", _lookup)
    monkeypatch.setattr(dispatch, "enforce", _enforce)
    monkeypatch.setattr(dispatch, "check_tool_lifecycle", _check)
    return requests, checks, events


def test_protect_scans_configured_mcp_after_denylist_allow(monkeypatch, capsys) -> None:
    requests, checks, events = _configure_protect_configured_mcp(monkeypatch)

    _run_protect_configured_mcp()

    assert requests[0]["mode"] == "protect"
    assert requests[0]["url"] == "https://mcp.linear.example/sse"
    assert checks == ["tool-pre"]
    assert events == ["PreToolUse"]
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize("evaluated_mode", ["protect", "enforce"])
def test_protect_configured_mcp_blocks_acknowledged_deny(
    monkeypatch, capsys, evaluated_mode
) -> None:
    _, checks, _ = _configure_protect_configured_mcp(
        monkeypatch,
        response=json.dumps(
            {
                "permission": "deny",
                "user_message": "MCP server blocked by organization denylist",
                "evaluated_mode": evaluated_mode,
            }
        ),
    )

    with pytest.raises(SystemExit) as exc:
        _run_protect_configured_mcp()

    assert exc.value.code == 0
    assert checks == []
    output = json.loads(capsys.readouterr().out)
    assert output["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert (
        "organization denylist"
        in output["hookSpecificOutput"]["permissionDecisionReason"]
    )


@pytest.mark.parametrize(
    "failure",
    ["relay-error", "lookup-error", "old-backend-deny"],
)
def test_protect_configured_mcp_source_failure_continues_scanner(
    monkeypatch, capsys, failure
) -> None:
    kwargs: dict[str, object] = {}
    if failure == "relay-error":
        kwargs["relay_error"] = dispatch.RelayError(2, "network down")
    elif failure == "lookup-error":
        kwargs["lookup_error"] = OSError("config unavailable")
    else:
        kwargs["response"] = json.dumps(
            {
                "permission": "deny",
                "user_message": "Only Runlayer-managed MCP servers are allowed.",
            }
        )
    requests, checks, events = _configure_protect_configured_mcp(
        monkeypatch,
        **kwargs,
    )

    _run_protect_configured_mcp()

    assert len(requests) == (0 if failure == "lookup-error" else 1)
    assert checks == ["tool-pre"]
    assert events == ["PreToolUse"]
    assert capsys.readouterr().out == ""


def _run_protect_cursor_mcp() -> None:
    dispatch._dispatch(
        hook_type="beforeMCPExecution",
        original_hook_type="beforeMCPExecution",
        client=Client.CURSOR,
        resp=HookResponse(Client.CURSOR, "beforeMCPExecution"),
        input_data={
            "hook_event_name": "beforeMCPExecution",
            "conversation_id": "conversation-123",
            "generation_id": "generation-456",
            "tool_name": "list_issues",
            "tool_input": {"query": "security"},
            "url": "https://mcp.linear.example/sse",
        },
        raw_input="{}",
        mode=AIWatchMode.PROTECT,
        debug=False,
    )


@pytest.mark.parametrize(
    "response",
    [
        pytest.param(
            '{"permission":"allow","evaluated_mode":"protect"}',
            id="acknowledged-allow",
        ),
        pytest.param(
            json.dumps(
                {
                    "permission": "deny",
                    "user_message": "Only Runlayer-managed MCP servers are allowed.",
                }
            ),
            id="old-backend-unacknowledged-deny",
        ),
    ],
)
def test_protect_cursor_mcp_sends_mode_and_returns_version_safe_allow(
    monkeypatch, capsys, response
) -> None:
    requests: list[dict[str, object]] = []

    def _enforce(payload: str, **_kwargs) -> str:
        requests.append(json.loads(payload))
        return response

    monkeypatch.setattr(dispatch, "forward_event", lambda *args, **kwargs: None)
    monkeypatch.setattr(dispatch, "enforce", _enforce)

    _run_protect_cursor_mcp()

    assert requests[0]["mode"] == "protect"
    assert json.loads(capsys.readouterr().out) == {"permission": "allow"}


def test_protect_scans_cursor_mcp_pretooluse(monkeypatch, capsys) -> None:
    checks: list[str] = []
    monkeypatch.setattr(dispatch, "forward_event", lambda *args, **kwargs: None)

    def _check(target, *args, **kwargs):
        checks.append(target)
        return '{"permission":"allow"}'

    monkeypatch.setattr(dispatch, "check_tool_lifecycle", _check)

    dispatch._handle_pre_tool_use(
        client=Client.CURSOR,
        resp=HookResponse(Client.CURSOR, "PreToolUse"),
        input_data={
            "tool_name": "MCP:searchJiraIssuesUsingJql",
            "tool_input": {"jql": "project = SECURITY"},
        },
        original_hook_type="preToolUse",
        mode=AIWatchMode.PROTECT,
        debug=False,
    )

    assert checks == ["tool-pre"]
    assert json.loads(capsys.readouterr().out) == {"permission": "allow"}


def test_protect_applies_mask_to_mcp_output(monkeypatch, capsys) -> None:
    monkeypatch.setattr(dispatch, "forward_event", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        dispatch,
        "check_tool_lifecycle",
        lambda *args, **kwargs: json.dumps(
            {"blocked": False, "modified_output": "SSN [REDACTED]"}
        ),
    )

    dispatch._dispatch(
        hook_type="PostToolUse",
        original_hook_type="PostToolUse",
        client=Client.CLAUDE_CODE,
        resp=HookResponse(Client.CLAUDE_CODE, "PostToolUse"),
        input_data={
            "tool_name": "mcp__records__read",
            "tool_response": "SSN 482-61-9357",
        },
        raw_input="{}",
        mode=AIWatchMode.PROTECT,
        debug=False,
    )

    response = json.loads(capsys.readouterr().out)
    assert response["hookSpecificOutput"]["updatedToolOutput"] == "SSN [REDACTED]"


@pytest.mark.parametrize("modified_output", [{"safe": "replacement"}, [], True, 1])
def test_non_string_modified_output_fails_closed(
    monkeypatch, capsys, modified_output: object
) -> None:
    monkeypatch.setattr(dispatch, "forward_event", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        dispatch,
        "check_tool_lifecycle",
        lambda *args, **kwargs: json.dumps(
            {"blocked": False, "modified_output": modified_output}
        ),
    )

    with pytest.raises(SystemExit) as exc:
        dispatch._dispatch(
            hook_type="PostToolUse",
            original_hook_type="PostToolUse",
            client=Client.CLAUDE_CODE,
            resp=HookResponse(Client.CLAUDE_CODE, "PostToolUse"),
            input_data={"tool_name": "Read", "tool_response": "secret raw output"},
            raw_input="{}",
            mode=AIWatchMode.PROTECT,
            debug=False,
        )

    assert exc.value.code == 0
    response = json.loads(capsys.readouterr().out)
    assert response["decision"] == "block"
    assert "Invalid response from Runlayer API" in response["reason"]
    assert "secret raw output" not in json.dumps(response)


@pytest.mark.parametrize(
    "response_data",
    [{"blocked": False}, {"blocked": False, "modified_output": None}],
)
def test_no_modified_output_is_observational(
    monkeypatch, capsys, response_data: dict[str, object]
) -> None:
    monkeypatch.setattr(dispatch, "forward_event", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        dispatch,
        "check_tool_lifecycle",
        lambda *args, **kwargs: json.dumps(response_data),
    )

    dispatch._dispatch(
        hook_type="PostToolUse",
        original_hook_type="PostToolUse",
        client=Client.CLAUDE_CODE,
        resp=HookResponse(Client.CLAUDE_CODE, "PostToolUse"),
        input_data={"tool_name": "Read", "tool_response": "safe output"},
        raw_input="{}",
        mode=AIWatchMode.PROTECT,
        debug=False,
    )

    assert capsys.readouterr().out == ""


@pytest.mark.parametrize("mode", [AIWatchMode.MONITOR, AIWatchMode.ENFORCE])
@pytest.mark.parametrize("hook_type", ["PostToolUse", "PostToolUseFailure"])
def test_non_protect_mcp_post_preserves_gateway_event_only(
    monkeypatch, capsys, mode, hook_type
) -> None:
    forwarded_events: list[str] = []
    monkeypatch.setattr(
        dispatch,
        "forward_event",
        lambda _client, event, *_args, **_kwargs: forwarded_events.append(event),
    )
    monkeypatch.setattr(
        dispatch,
        "forward_tool_lifecycle",
        lambda *args, **kwargs: pytest.fail(
            "Monitor must not add local lifecycle calls for MCP"
        ),
    )
    monkeypatch.setattr(
        dispatch,
        "check_tool_lifecycle",
        lambda *args, **kwargs: pytest.fail(
            "Enforce must not rescan gateway MCP output"
        ),
    )

    dispatch._dispatch(
        hook_type=hook_type,
        original_hook_type=hook_type,
        client=Client.CLAUDE_CODE,
        resp=HookResponse(Client.CLAUDE_CODE, hook_type),
        input_data={
            "tool_name": "mcp__records__read",
            "tool_response": "already gateway-scanned",
        },
        raw_input="{}",
        mode=mode,
        debug=False,
    )

    assert forwarded_events == [hook_type]
    assert capsys.readouterr().out == ""


def test_protect_failed_output_is_observational_when_client_cannot_replace(
    monkeypatch, capsys
) -> None:
    forwarded: list[str] = []
    monkeypatch.setattr(
        dispatch,
        "forward_tool_lifecycle",
        lambda target, *args, **kwargs: forwarded.append(target),
    )
    monkeypatch.setattr(dispatch, "forward_event", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        dispatch,
        "check_tool_lifecycle",
        lambda *args, **kwargs: pytest.fail(
            "Claude cannot replace PostToolUseFailure output"
        ),
    )

    dispatch._dispatch(
        hook_type="PostToolUseFailure",
        original_hook_type="PostToolUseFailure",
        client=Client.CLAUDE_CODE,
        resp=HookResponse(Client.CLAUDE_CODE, "PostToolUseFailure"),
        input_data={"tool_name": "Read", "error": "secret"},
        raw_input="{}",
        mode=AIWatchMode.PROTECT,
        debug=False,
    )

    assert forwarded == ["tool-post"]
    assert capsys.readouterr().out == ""
