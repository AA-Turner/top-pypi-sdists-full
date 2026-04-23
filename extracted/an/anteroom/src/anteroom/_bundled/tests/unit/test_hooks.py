"""Unit tests for services/hooks.py (#1271)."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.services.hooks import (
    _ALLOW,
    HookDecision,
    _parse_decision,
    match_hook,
    run_command_hook,
    run_post_tool_hooks,
    run_pre_tool_hooks,
    run_webhook_hook,
)

# ---------------------------------------------------------------------------
# Helpers to build minimal config objects without importing AppConfig
# ---------------------------------------------------------------------------


@dataclass
class _Matcher:
    tool_name: str = "*"
    arguments: dict[str, str] = field(default_factory=dict)


@dataclass
class _Runner:
    type: str = "command"
    command: str = ""
    url: str = ""
    timeout: int = 5


@dataclass
class _Entry:
    id: str = "test-hook"
    event: str = "pre_tool"
    matcher: _Matcher = field(default_factory=_Matcher)
    runner: _Runner = field(default_factory=_Runner)
    message: str = ""
    trust_source: str = "personal"

    @property
    def is_executable(self) -> bool:
        return self.trust_source in ("personal", "team")


@dataclass
class _HooksConfig:
    pre_tool: list[_Entry] = field(default_factory=list)
    post_tool: list[_Entry] = field(default_factory=list)


# ---------------------------------------------------------------------------
# HookDecision
# ---------------------------------------------------------------------------


class TestHookDecision:
    def test_default_is_allow(self) -> None:
        d = HookDecision()
        assert d.outcome == "allow"
        assert d.message == ""
        assert d.hook_id == ""

    def test_allow_sentinel(self) -> None:
        assert _ALLOW.outcome == "allow"

    def test_frozen(self) -> None:
        d = HookDecision(outcome="deny", message="blocked")
        with pytest.raises(Exception):
            d.outcome = "allow"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# _parse_decision
# ---------------------------------------------------------------------------


class TestParseDecision:
    def test_allow(self) -> None:
        d = _parse_decision('{"decision": "allow"}', "h1")
        assert d.outcome == "allow"

    def test_deny_with_message(self) -> None:
        d = _parse_decision('{"decision": "deny", "message": "not allowed"}', "h1")
        assert d.outcome == "deny"
        assert d.message == "not allowed"
        assert d.hook_id == "h1"

    def test_ask(self) -> None:
        d = _parse_decision('{"decision": "ask", "message": "please confirm"}', "h1")
        assert d.outcome == "ask"
        assert d.message == "please confirm"

    def test_empty_string_returns_allow(self) -> None:
        assert _parse_decision("", "h1").outcome == "allow"

    def test_non_json_returns_allow(self) -> None:
        assert _parse_decision("not json", "h1").outcome == "allow"

    def test_non_dict_json_returns_allow(self) -> None:
        assert _parse_decision("[1, 2, 3]", "h1").outcome == "allow"

    def test_unknown_decision_returns_allow(self) -> None:
        assert _parse_decision('{"decision": "block"}', "h1").outcome == "allow"

    def test_missing_decision_key_returns_allow(self) -> None:
        assert _parse_decision('{"status": "ok"}', "h1").outcome == "allow"


# ---------------------------------------------------------------------------
# match_hook
# ---------------------------------------------------------------------------


class TestMatchHook:
    def test_wildcard_matches_any_tool(self) -> None:
        entry = _Entry(matcher=_Matcher(tool_name="*"))
        assert match_hook(entry, "bash", {}) is True
        assert match_hook(entry, "read_file", {}) is True

    def test_exact_name_match(self) -> None:
        entry = _Entry(matcher=_Matcher(tool_name="bash"))
        assert match_hook(entry, "bash", {}) is True
        assert match_hook(entry, "read_file", {}) is False

    def test_fnmatch_pattern(self) -> None:
        entry = _Entry(matcher=_Matcher(tool_name="*file*"))
        assert match_hook(entry, "read_file", {}) is True
        assert match_hook(entry, "write_file", {}) is True
        assert match_hook(entry, "bash", {}) is False

    def test_argument_filter_all_match(self) -> None:
        entry = _Entry(matcher=_Matcher(tool_name="*", arguments={"path": "/etc/hosts"}))
        assert match_hook(entry, "read_file", {"path": "/etc/hosts"}) is True

    def test_argument_filter_partial_match_fails(self) -> None:
        entry = _Entry(matcher=_Matcher(tool_name="*", arguments={"path": "/etc/hosts"}))
        assert match_hook(entry, "read_file", {"path": "/tmp/other"}) is False

    def test_argument_filter_missing_key_fails(self) -> None:
        entry = _Entry(matcher=_Matcher(tool_name="*", arguments={"path": "/etc/hosts"}))
        assert match_hook(entry, "read_file", {}) is False

    def test_empty_argument_filter_matches_anything(self) -> None:
        entry = _Entry(matcher=_Matcher(tool_name="bash", arguments={}))
        assert match_hook(entry, "bash", {"command": "ls"}) is True
        assert match_hook(entry, "bash", {}) is True


# ---------------------------------------------------------------------------
# run_command_hook
# ---------------------------------------------------------------------------


class TestRunCommandHook:
    @pytest.mark.asyncio
    async def test_allow_response(self) -> None:
        entry = _Entry(runner=_Runner(type="command", command='echo \'{"decision": "allow"}\''))
        d = await run_command_hook(entry, "pre_tool", "bash", {"command": "ls"})
        assert d.outcome == "allow"

    @pytest.mark.asyncio
    async def test_deny_response(self) -> None:
        entry = _Entry(runner=_Runner(type="command", command='echo \'{"decision": "deny", "message": "blocked"}\''))
        d = await run_command_hook(entry, "pre_tool", "bash", {"command": "rm -rf /"})
        assert d.outcome == "deny"
        assert d.message == "blocked"

    @pytest.mark.asyncio
    async def test_nonzero_exit_defaults_to_allow(self) -> None:
        entry = _Entry(runner=_Runner(type="command", command="exit 1"))
        d = await run_command_hook(entry, "pre_tool", "bash", {})
        assert d.outcome == "allow"

    @pytest.mark.asyncio
    async def test_empty_command_returns_allow(self) -> None:
        entry = _Entry(runner=_Runner(type="command", command=""))
        d = await run_command_hook(entry, "pre_tool", "bash", {})
        assert d.outcome == "allow"

    @pytest.mark.asyncio
    async def test_timeout_returns_allow(self) -> None:
        entry = _Entry(runner=_Runner(type="command", command="sleep 10", timeout=1))
        d = await run_command_hook(entry, "pre_tool", "bash", {})
        assert d.outcome == "allow"

    @pytest.mark.asyncio
    async def test_hook_env_variables_set(self) -> None:
        # Verify ANTEROOM_HOOK_EVENT and ANTEROOM_HOOK_TOOL_NAME are injected.
        captured_env: dict[str, str] = {}

        async def _mock_shell(cmd: str, **kw: Any) -> Any:
            captured_env.update(kw.get("env", {}))
            proc = AsyncMock()
            proc.communicate = AsyncMock(return_value=(b'{"decision":"allow"}', b""))
            proc.returncode = 0
            return proc

        entry = _Entry(runner=_Runner(type="command", command="echo ok"))
        with patch("asyncio.create_subprocess_shell", side_effect=_mock_shell):
            d = await run_command_hook(entry, "pre_tool", "bash", {"command": "ls"})
        assert d.outcome == "allow"
        assert captured_env.get("ANTEROOM_HOOK_EVENT") == "pre_tool"
        assert captured_env.get("ANTEROOM_HOOK_TOOL_NAME") == "bash"

    @pytest.mark.asyncio
    async def test_post_tool_output_env_set(self) -> None:
        # Verify ANTEROOM_HOOK_OUTPUT is injected for post-tool calls.
        captured_env: dict[str, str] = {}

        async def _mock_shell(cmd: str, **kw: Any) -> Any:
            captured_env.update(kw.get("env", {}))
            proc = AsyncMock()
            proc.communicate = AsyncMock(return_value=(b'{"decision":"allow"}', b""))
            proc.returncode = 0
            return proc

        entry = _Entry(runner=_Runner(type="command", command="echo ok"))
        with patch("asyncio.create_subprocess_shell", side_effect=_mock_shell):
            d = await run_command_hook(entry, "post_tool", "bash", {}, output={"result": "ok"})
        assert d.outcome == "allow"
        assert "ANTEROOM_HOOK_OUTPUT" in captured_env

    @pytest.mark.asyncio
    async def test_not_executable_returns_allow(self) -> None:
        entry = _Entry(trust_source="pack", runner=_Runner(type="command", command="exit 2"))
        d = await run_command_hook(entry, "pre_tool", "bash", {})
        assert d.outcome == "allow"


# ---------------------------------------------------------------------------
# run_webhook_hook
# ---------------------------------------------------------------------------


class TestRunWebhookHook:
    @pytest.mark.asyncio
    async def test_allow_response(self) -> None:
        entry = _Entry(runner=_Runner(type="webhook", url="http://example.test/hook"))
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = '{"decision": "allow"}'
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(return_value=mock_resp)
        with patch("httpx.AsyncClient", return_value=mock_client):
            result = await run_webhook_hook(entry, "pre_tool", "bash", {})
        assert result.outcome == "allow"

    @pytest.mark.asyncio
    async def test_timeout_returns_allow(self) -> None:
        entry = _Entry(runner=_Runner(type="webhook", url="http://example.test/hook"))
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(side_effect=asyncio.TimeoutError())
        with patch("httpx.AsyncClient", return_value=mock_client):
            result = await run_webhook_hook(entry, "pre_tool", "bash", {})
        assert result.outcome == "allow"

    @pytest.mark.asyncio
    async def test_deny_response_via_mock_client(self) -> None:
        entry = _Entry(runner=_Runner(type="webhook", url="http://example.test/hook"))
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = '{"decision": "deny", "message": "webhook denied"}'
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(return_value=mock_resp)
        with patch("httpx.AsyncClient", return_value=mock_client):
            result = await run_webhook_hook(entry, "pre_tool", "bash", {})
        assert result.outcome == "deny"
        assert result.message == "webhook denied"

    @pytest.mark.asyncio
    async def test_http_error_returns_allow(self) -> None:
        entry = _Entry(runner=_Runner(type="webhook", url="http://example.test/hook"))
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_resp.text = "internal error"
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(return_value=mock_resp)
        with patch("httpx.AsyncClient", return_value=mock_client):
            result = await run_webhook_hook(entry, "pre_tool", "bash", {})
        assert result.outcome == "allow"

    @pytest.mark.asyncio
    async def test_transport_exception_returns_allow(self) -> None:
        entry = _Entry(runner=_Runner(type="webhook", url="http://example.test/hook"))
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(side_effect=ConnectionRefusedError("refused"))
        with patch("httpx.AsyncClient", return_value=mock_client):
            result = await run_webhook_hook(entry, "pre_tool", "bash", {})
        assert result.outcome == "allow"

    @pytest.mark.asyncio
    async def test_empty_url_returns_allow(self) -> None:
        entry = _Entry(runner=_Runner(type="webhook", url=""))
        d = await run_webhook_hook(entry, "pre_tool", "bash", {})
        assert d.outcome == "allow"

    @pytest.mark.asyncio
    async def test_egress_allowlist_block_returns_allow(self) -> None:
        entry = _Entry(runner=_Runner(type="webhook", url="http://blocked.example.test/hook"))
        with patch("anteroom.services.egress_allowlist.check_egress_allowed", return_value=False):
            result = await run_webhook_hook(entry, "pre_tool", "bash", {})
        assert result.outcome == "allow"

    @pytest.mark.asyncio
    async def test_egress_check_exception_fails_closed(self) -> None:
        """If egress allowlist check raises, webhook must be skipped (fail-closed)."""
        entry = _Entry(runner=_Runner(type="webhook", url="http://internal.test/hook"))
        with patch("anteroom.services.egress_allowlist.check_egress_allowed", side_effect=RuntimeError("db error")):
            result = await run_webhook_hook(entry, "pre_tool", "bash", {})
        assert result.outcome == "allow"

    @pytest.mark.asyncio
    async def test_egress_policy_is_passed_to_allowlist(self) -> None:
        entry = _Entry(runner=_Runner(type="webhook", url="http://hooks.example.test/hook"))
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = '{"decision": "allow"}'
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(return_value=mock_resp)
        with (
            patch("anteroom.services.egress_allowlist.check_egress_allowed", return_value=True) as check_egress,
            patch("httpx.AsyncClient", return_value=mock_client),
        ):
            result = await run_webhook_hook(
                entry,
                "pre_tool",
                "bash",
                {},
                allowed_domains=["hooks.example.test"],
                block_localhost=True,
            )
        assert result.outcome == "allow"
        check_egress.assert_called_once_with(
            "http://hooks.example.test/hook",
            ["hooks.example.test"],
            block_localhost=True,
        )


# ---------------------------------------------------------------------------
# _run_single_hook — unknown runner type
# ---------------------------------------------------------------------------


class TestRunSingleHook:
    @pytest.mark.asyncio
    async def test_unknown_runner_type_returns_allow(self) -> None:
        from anteroom.services.hooks import _run_single_hook

        entry = _Entry(runner=_Runner(type="grpc", command=""))
        d = await _run_single_hook(entry, "pre_tool", "bash", {})
        assert d.outcome == "allow"


# ---------------------------------------------------------------------------
# run_pre_tool_hooks / run_post_tool_hooks
# ---------------------------------------------------------------------------


class TestRunPreToolHooks:
    @pytest.mark.asyncio
    async def test_no_hooks_returns_allow(self) -> None:
        cfg = _HooksConfig(pre_tool=[])
        d = await run_pre_tool_hooks(cfg, "bash", {})  # type: ignore[arg-type]
        assert d.outcome == "allow"

    @pytest.mark.asyncio
    async def test_non_matching_hook_skipped(self) -> None:
        entry = _Entry(
            matcher=_Matcher(tool_name="write_file"), runner=_Runner(command='echo \'{"decision": "deny"}\'')
        )
        cfg = _HooksConfig(pre_tool=[entry])
        d = await run_pre_tool_hooks(cfg, "bash", {})  # type: ignore[arg-type]
        assert d.outcome == "allow"

    @pytest.mark.asyncio
    async def test_matching_deny_blocks(self) -> None:
        entry = _Entry(runner=_Runner(command='echo \'{"decision": "deny", "message": "blocked"}\''))
        cfg = _HooksConfig(pre_tool=[entry])
        d = await run_pre_tool_hooks(cfg, "bash", {})  # type: ignore[arg-type]
        assert d.outcome == "deny"
        assert d.message == "blocked"

    @pytest.mark.asyncio
    async def test_first_deny_short_circuits(self) -> None:
        entry1 = _Entry(id="h1", runner=_Runner(command='echo \'{"decision": "deny", "message": "first"}\''))
        entry2 = _Entry(id="h2", runner=_Runner(command='echo \'{"decision": "deny", "message": "second"}\''))
        cfg = _HooksConfig(pre_tool=[entry1, entry2])
        d = await run_pre_tool_hooks(cfg, "bash", {})  # type: ignore[arg-type]
        assert d.outcome == "deny"
        assert d.message == "first"

    @pytest.mark.asyncio
    async def test_ask_propagates(self) -> None:
        entry = _Entry(runner=_Runner(command='echo \'{"decision": "ask", "message": "please confirm"}\''))
        cfg = _HooksConfig(pre_tool=[entry])
        d = await run_pre_tool_hooks(cfg, "bash", {})  # type: ignore[arg-type]
        assert d.outcome == "ask"
        assert d.message == "please confirm"

    @pytest.mark.asyncio
    async def test_non_executable_hook_skipped(self) -> None:
        entry = _Entry(trust_source="pack", runner=_Runner(command='echo \'{"decision": "deny"}\''))
        cfg = _HooksConfig(pre_tool=[entry])
        d = await run_pre_tool_hooks(cfg, "bash", {})  # type: ignore[arg-type]
        assert d.outcome == "allow"


class TestRunPostToolHooks:
    @pytest.mark.asyncio
    async def test_no_hooks_returns_allow(self) -> None:
        cfg = _HooksConfig(post_tool=[])
        d = await run_post_tool_hooks(cfg, "bash", {}, {"output": "ok"})  # type: ignore[arg-type]
        assert d.outcome == "allow"

    @pytest.mark.asyncio
    async def test_deny_on_output(self) -> None:
        entry = _Entry(
            event="post_tool",
            runner=_Runner(command='echo \'{"decision": "deny", "message": "dangerous output"}\''),
        )
        cfg = _HooksConfig(post_tool=[entry])
        d = await run_post_tool_hooks(cfg, "bash", {}, {"stdout": "rm -rf /"})  # type: ignore[arg-type]
        assert d.outcome == "deny"
        assert d.message == "dangerous output"

    @pytest.mark.asyncio
    async def test_allow_continues(self) -> None:
        entry = _Entry(event="post_tool", runner=_Runner(command='echo \'{"decision": "allow"}\''))
        cfg = _HooksConfig(post_tool=[entry])
        d = await run_post_tool_hooks(cfg, "bash", {}, {})  # type: ignore[arg-type]
        assert d.outcome == "allow"


# ---------------------------------------------------------------------------
# Hard-deny precedence — verify hooks cannot override static rule enforcer
# ---------------------------------------------------------------------------


class TestHardDenyPrecedence:
    """These tests verify the ordering invariant via ToolRegistry.call_tool."""

    @pytest.mark.asyncio
    async def test_hard_deny_blocks_before_hooks(self) -> None:
        """A hook deny cannot be reached if the static rule enforcer hard-denies first."""
        from anteroom.tools import ToolRegistry

        registry = ToolRegistry()

        async def _mock_handler(**kwargs: Any) -> dict[str, Any]:
            return {"result": "ok"}

        registry.register("test_tool", _mock_handler, {"name": "test_tool", "description": "test", "parameters": {}})

        mock_enforcer = MagicMock()
        mock_enforcer.check_tool_call.return_value = (True, "hard block", "rule::fqn")

        hook_called = []

        async def _spy_pre(*args: Any, **kwargs: Any) -> HookDecision:
            hook_called.append(True)
            return HookDecision(outcome="deny", message="hook deny")

        hook_entry = _Entry(runner=_Runner(command='echo \'{"decision": "deny"}\''))
        hooks_cfg = _HooksConfig(pre_tool=[hook_entry])

        with patch("anteroom.services.hooks.run_pre_tool_hooks", _spy_pre):
            result = await registry.call_tool(
                "test_tool",
                {},
                rule_enforcer_override=mock_enforcer,
                _hooks_config=hooks_cfg,  # type: ignore[arg-type]
            )

        assert result.get("_approval_decision") == "hard_denied"
        assert not hook_called, "hooks must not run when hard-denied"

    @pytest.mark.asyncio
    async def test_pre_hook_ask_with_no_callback_denies(self) -> None:
        """Hook returning 'ask' with no approval callback must deny (fail closed)."""
        from anteroom.tools import ToolRegistry

        registry = ToolRegistry()

        async def _mock_handler(**kwargs: Any) -> dict[str, Any]:
            return {"result": "ok"}

        registry.register("test_tool2", _mock_handler, {"name": "test_tool2", "description": "t", "parameters": {}})

        async def _ask_pre(*args: Any, **kwargs: Any) -> HookDecision:
            return HookDecision(outcome="ask", message="please confirm")

        hook_entry = _Entry(runner=_Runner(command='echo \'{"decision": "ask"}\''))
        hooks_cfg = _HooksConfig(pre_tool=[hook_entry])

        with patch("anteroom.services.hooks.run_pre_tool_hooks", _ask_pre):
            result = await registry.call_tool(
                "test_tool2",
                {},
                confirm_callback=None,
                _hooks_config=hooks_cfg,  # type: ignore[arg-type]
            )

        assert result.get("_approval_decision") == "denied"
