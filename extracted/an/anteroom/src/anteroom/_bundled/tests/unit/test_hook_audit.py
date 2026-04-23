"""Unit tests for hook audit lineage (#1490).

Covers:
- emit_hook_lifecycle payload shape and severity rules
- _emit_hook_audit mapping (outcome × error_type → lifecycle event)
- audit_writer threading through run_pre_tool_hooks / run_post_tool_hooks
- timeout and exception paths recorded distinctly
- disabled writer is a no-op (never raises)
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.services.audit import AuditEntry
from anteroom.services.hooks import (
    HookDecision,
    _emit_hook_audit,
    run_post_tool_hooks,
    run_pre_tool_hooks,
)
from anteroom.services.lineage import emit_hook_lifecycle

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _capture_writer() -> tuple[Any, list[AuditEntry]]:
    captured: list[AuditEntry] = []
    writer = MagicMock()
    writer.emit.side_effect = captured.append
    return writer, captured


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
# emit_hook_lifecycle
# ---------------------------------------------------------------------------


class TestEmitHookLifecycle:
    def test_completed_emits_info_severity(self) -> None:
        writer, captured = _capture_writer()
        emit_hook_lifecycle(
            writer,
            "completed",
            hook_id="h1",
            hook_event="pre_tool",
            tool_name="bash",
            outcome="allow",
            execution_ms=12.5,
        )
        assert len(captured) == 1
        e = captured[0]
        assert e.event_type == "hook.completed"
        assert e.severity == "info"
        assert e.details["hook_id"] == "h1"
        assert e.details["hook_event"] == "pre_tool"
        assert e.details["tool_name"] == "bash"
        assert e.details["outcome"] == "allow"
        assert e.details["execution_ms"] == 12.5

    @pytest.mark.parametrize("event", ["denied", "timed_out", "failed"])
    def test_non_completed_events_are_warning(self, event: str) -> None:
        writer, captured = _capture_writer()
        emit_hook_lifecycle(
            writer,
            event,
            hook_id="h1",
            hook_event="pre_tool",
            tool_name="bash",
            outcome="allow",
        )
        assert captured[0].severity == "warning"
        assert captured[0].event_type == f"hook.{event}"

    def test_message_included_when_present(self) -> None:
        writer, captured = _capture_writer()
        emit_hook_lifecycle(
            writer,
            "denied",
            hook_id="h1",
            hook_event="pre_tool",
            tool_name="bash",
            outcome="deny",
            message="not allowed",
        )
        assert captured[0].details["message"] == "not allowed"

    def test_message_omitted_when_empty(self) -> None:
        writer, captured = _capture_writer()
        emit_hook_lifecycle(
            writer,
            "completed",
            hook_id="h1",
            hook_event="pre_tool",
            tool_name="bash",
            outcome="allow",
        )
        assert "message" not in captured[0].details

    def test_conversation_id_included_when_provided(self) -> None:
        writer, captured = _capture_writer()
        emit_hook_lifecycle(
            writer,
            "completed",
            hook_id="h1",
            hook_event="pre_tool",
            tool_name="bash",
            outcome="allow",
            conversation_id="conv-123",
        )
        assert captured[0].details["conversation_id"] == "conv-123"

    def test_tool_call_id_included_when_provided(self) -> None:
        writer, captured = _capture_writer()
        emit_hook_lifecycle(
            writer,
            "completed",
            hook_id="h1",
            hook_event="pre_tool",
            tool_name="bash",
            outcome="allow",
            tool_call_id="call-123",
        )
        assert captured[0].details["tool_call_id"] == "call-123"

    def test_user_id_stored_on_audit_entry_when_provided(self) -> None:
        writer, captured = _capture_writer()
        emit_hook_lifecycle(
            writer,
            "completed",
            hook_id="h1",
            hook_event="pre_tool",
            tool_name="bash",
            outcome="allow",
            user_id="user-123",
        )
        assert captured[0].user_id == "user-123"

    def test_extra_details_merged(self) -> None:
        writer, captured = _capture_writer()
        emit_hook_lifecycle(
            writer,
            "completed",
            hook_id="h1",
            hook_event="pre_tool",
            tool_name="bash",
            outcome="allow",
            details={"runner_type": "command"},
        )
        assert captured[0].details["runner_type"] == "command"

    def test_unknown_event_drops_silently(self, caplog: pytest.LogCaptureFixture) -> None:
        writer, captured = _capture_writer()
        with caplog.at_level("WARNING", logger="anteroom.services.lineage"):
            emit_hook_lifecycle(
                writer,
                "unknown_event",
                hook_id="h1",
                hook_event="pre_tool",
                tool_name="bash",
                outcome="allow",
            )
        assert len(captured) == 0
        assert "unknown_event" in caplog.text

    def test_none_writer_is_noop(self) -> None:
        emit_hook_lifecycle(
            None,
            "completed",
            hook_id="h1",
            hook_event="pre_tool",
            tool_name="bash",
            outcome="allow",
        )

    def test_execution_ms_rounded_to_two_decimals(self) -> None:
        writer, captured = _capture_writer()
        emit_hook_lifecycle(
            writer,
            "completed",
            hook_id="h1",
            hook_event="pre_tool",
            tool_name="bash",
            outcome="allow",
            execution_ms=1.23456789,
        )
        assert captured[0].details["execution_ms"] == 1.23


# ---------------------------------------------------------------------------
# _emit_hook_audit — mapping (outcome × error_type) → lifecycle event
# ---------------------------------------------------------------------------


class TestEmitHookAuditMapping:
    def test_normal_allow_emits_completed(self) -> None:
        writer, captured = _capture_writer()
        decision = HookDecision(outcome="allow", hook_id="h1")
        _emit_hook_audit(writer, decision, hook_event="pre_tool", tool_name="bash")
        assert captured[0].event_type == "hook.completed"

    def test_deny_emits_denied(self) -> None:
        writer, captured = _capture_writer()
        decision = HookDecision(outcome="deny", hook_id="h1", message="blocked")
        _emit_hook_audit(writer, decision, hook_event="pre_tool", tool_name="bash")
        assert captured[0].event_type == "hook.denied"

    def test_ask_emits_completed(self) -> None:
        writer, captured = _capture_writer()
        decision = HookDecision(outcome="ask", hook_id="h1")
        _emit_hook_audit(writer, decision, hook_event="pre_tool", tool_name="bash")
        assert captured[0].event_type == "hook.completed"
        assert captured[0].details["outcome"] == "ask"

    def test_timeout_error_type_emits_timed_out(self) -> None:
        writer, captured = _capture_writer()
        decision = HookDecision(outcome="allow", hook_id="h1", error_type="timeout")
        _emit_hook_audit(writer, decision, hook_event="pre_tool", tool_name="bash")
        assert captured[0].event_type == "hook.timed_out"

    def test_exception_error_type_emits_failed(self) -> None:
        writer, captured = _capture_writer()
        decision = HookDecision(outcome="allow", hook_id="h1", error_type="exception")
        _emit_hook_audit(writer, decision, hook_event="pre_tool", tool_name="bash")
        assert captured[0].event_type == "hook.failed"

    def test_none_writer_is_noop(self) -> None:
        decision = HookDecision(outcome="allow", hook_id="h1")
        _emit_hook_audit(None, decision, hook_event="pre_tool", tool_name="bash")

    def test_emit_raises_does_not_propagate(self) -> None:
        writer = MagicMock()
        writer.emit.side_effect = RuntimeError("db offline")
        decision = HookDecision(outcome="deny", hook_id="h1")
        _emit_hook_audit(writer, decision, hook_event="pre_tool", tool_name="bash")


# ---------------------------------------------------------------------------
# Audit threading through run_pre_tool_hooks / run_post_tool_hooks
# ---------------------------------------------------------------------------


class TestAuditThreadingPreHooks:
    @pytest.mark.asyncio
    async def test_audit_writer_receives_event_on_allow(self) -> None:
        writer, captured = _capture_writer()
        entry = _Entry(runner=_Runner(command='echo \'{"decision": "allow"}\''))
        cfg = _HooksConfig(pre_tool=[entry])
        await run_pre_tool_hooks(cfg, "bash", {}, audit_writer=writer)  # type: ignore[arg-type]
        assert len(captured) == 1
        assert captured[0].event_type == "hook.completed"
        assert captured[0].details["tool_name"] == "bash"
        assert captured[0].details["hook_event"] == "pre_tool"

    @pytest.mark.asyncio
    async def test_audit_writer_receives_denied_event(self) -> None:
        writer, captured = _capture_writer()
        entry = _Entry(runner=_Runner(command='echo \'{"decision": "deny", "message": "blocked"}\''))
        cfg = _HooksConfig(pre_tool=[entry])
        await run_pre_tool_hooks(cfg, "bash", {}, audit_writer=writer)  # type: ignore[arg-type]
        assert captured[0].event_type == "hook.denied"
        assert captured[0].severity == "warning"

    @pytest.mark.asyncio
    async def test_audit_writer_receives_timed_out_event(self) -> None:
        writer, captured = _capture_writer()
        entry = _Entry(runner=_Runner(command="sleep 10", timeout=1))
        cfg = _HooksConfig(pre_tool=[entry])
        await run_pre_tool_hooks(cfg, "bash", {}, audit_writer=writer)  # type: ignore[arg-type]
        assert captured[0].event_type == "hook.timed_out"
        assert captured[0].severity == "warning"

    @pytest.mark.asyncio
    async def test_no_hooks_no_audit_events(self) -> None:
        writer, captured = _capture_writer()
        cfg = _HooksConfig(pre_tool=[])
        await run_pre_tool_hooks(cfg, "bash", {}, audit_writer=writer)  # type: ignore[arg-type]
        assert len(captured) == 0

    @pytest.mark.asyncio
    async def test_non_matching_hook_no_audit_event(self) -> None:
        writer, captured = _capture_writer()
        entry = _Entry(
            matcher=_Matcher(tool_name="write_file"),
            runner=_Runner(command='echo \'{"decision": "allow"}\''),
        )
        cfg = _HooksConfig(pre_tool=[entry])
        await run_pre_tool_hooks(cfg, "bash", {}, audit_writer=writer)  # type: ignore[arg-type]
        assert len(captured) == 0

    @pytest.mark.asyncio
    async def test_none_writer_does_not_raise(self) -> None:
        entry = _Entry(runner=_Runner(command='echo \'{"decision": "allow"}\''))
        cfg = _HooksConfig(pre_tool=[entry])
        await run_pre_tool_hooks(cfg, "bash", {}, audit_writer=None)  # type: ignore[arg-type]

    @pytest.mark.asyncio
    async def test_execution_ms_is_positive(self) -> None:
        writer, captured = _capture_writer()
        entry = _Entry(runner=_Runner(command='echo \'{"decision": "allow"}\''))
        cfg = _HooksConfig(pre_tool=[entry])
        await run_pre_tool_hooks(cfg, "bash", {}, audit_writer=writer)  # type: ignore[arg-type]
        assert captured[0].details["execution_ms"] >= 0.0

    @pytest.mark.asyncio
    async def test_correlation_fields_threaded_into_pre_hook_audit(self) -> None:
        writer, captured = _capture_writer()
        entry = _Entry(runner=_Runner(command='echo \'{"decision": "allow"}\''))
        cfg = _HooksConfig(pre_tool=[entry])
        await run_pre_tool_hooks(
            cfg,
            "bash",
            {},
            audit_writer=writer,  # type: ignore[arg-type]
            tool_call_id="call-123",
            conversation_id="conv-123",
            user_id="user-123",
        )
        assert captured[0].details["tool_call_id"] == "call-123"
        assert captured[0].details["conversation_id"] == "conv-123"
        assert captured[0].user_id == "user-123"


class TestAuditThreadingPostHooks:
    @pytest.mark.asyncio
    async def test_post_hook_audit_emits_hook_event_post_tool(self) -> None:
        writer, captured = _capture_writer()
        entry = _Entry(event="post_tool", runner=_Runner(command='echo \'{"decision": "allow"}\''))
        cfg = _HooksConfig(post_tool=[entry])
        await run_post_tool_hooks(cfg, "bash", {}, {"result": "ok"}, audit_writer=writer)  # type: ignore[arg-type]
        assert len(captured) == 1
        assert captured[0].details["hook_event"] == "post_tool"

    @pytest.mark.asyncio
    async def test_post_hook_deny_emits_denied(self) -> None:
        writer, captured = _capture_writer()
        entry = _Entry(event="post_tool", runner=_Runner(command='echo \'{"decision": "deny"}\''))
        cfg = _HooksConfig(post_tool=[entry])
        await run_post_tool_hooks(cfg, "bash", {}, {}, audit_writer=writer)  # type: ignore[arg-type]
        assert captured[0].event_type == "hook.denied"

    @pytest.mark.asyncio
    async def test_correlation_fields_threaded_into_post_hook_audit(self) -> None:
        writer, captured = _capture_writer()
        entry = _Entry(event="post_tool", runner=_Runner(command='echo \'{"decision": "allow"}\''))
        cfg = _HooksConfig(post_tool=[entry])
        await run_post_tool_hooks(
            cfg,
            "bash",
            {},
            {"result": "ok"},
            audit_writer=writer,  # type: ignore[arg-type]
            tool_call_id="call-456",
            conversation_id="conv-456",
            user_id="user-456",
        )
        assert captured[0].details["tool_call_id"] == "call-456"
        assert captured[0].details["conversation_id"] == "conv-456"
        assert captured[0].user_id == "user-456"


# ---------------------------------------------------------------------------
# Exception path recorded distinctly
# ---------------------------------------------------------------------------


class TestExceptionPathAudit:
    @pytest.mark.asyncio
    async def test_subprocess_exception_emits_failed(self) -> None:
        writer, captured = _capture_writer()

        async def _raise(*a: Any, **kw: Any) -> Any:
            raise OSError("no subprocess")

        entry = _Entry(runner=_Runner(command="echo ok"))
        cfg = _HooksConfig(pre_tool=[entry])
        with patch("asyncio.create_subprocess_shell", side_effect=_raise):
            await run_pre_tool_hooks(cfg, "bash", {}, audit_writer=writer)  # type: ignore[arg-type]
        assert captured[0].event_type == "hook.failed"

    @pytest.mark.asyncio
    async def test_webhook_exception_emits_failed(self) -> None:
        writer, captured = _capture_writer()
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(side_effect=ConnectionRefusedError("refused"))
        entry = _Entry(runner=_Runner(type="webhook", url="http://example.test/hook"))
        cfg = _HooksConfig(pre_tool=[entry])
        with patch("httpx.AsyncClient", return_value=mock_client):
            await run_pre_tool_hooks(cfg, "bash", {}, audit_writer=writer)  # type: ignore[arg-type]
        assert captured[0].event_type == "hook.failed"

    @pytest.mark.asyncio
    async def test_webhook_timeout_emits_timed_out(self) -> None:
        writer, captured = _capture_writer()
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(side_effect=asyncio.TimeoutError())
        entry = _Entry(runner=_Runner(type="webhook", url="http://example.test/hook"))
        cfg = _HooksConfig(pre_tool=[entry])
        with patch("httpx.AsyncClient", return_value=mock_client):
            await run_pre_tool_hooks(cfg, "bash", {}, audit_writer=writer)  # type: ignore[arg-type]
        assert captured[0].event_type == "hook.timed_out"

    @pytest.mark.asyncio
    async def test_webhook_httpx_timeout_emits_timed_out(self) -> None:
        """httpx.TimeoutException is NOT a subclass of asyncio.TimeoutError.

        Regression: before the fix, a real httpx timeout was caught by the
        generic ``except Exception`` branch and logged as ``hook.failed``
        instead of ``hook.timed_out``, corrupting the audit signal for
        misconfigured webhooks that actually timed out.
        """
        import httpx

        writer, captured = _capture_writer()
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(side_effect=httpx.ReadTimeout("read timeout"))
        entry = _Entry(runner=_Runner(type="webhook", url="http://example.test/hook"))
        cfg = _HooksConfig(pre_tool=[entry])
        with patch("httpx.AsyncClient", return_value=mock_client):
            await run_pre_tool_hooks(cfg, "bash", {}, audit_writer=writer)  # type: ignore[arg-type]
        assert captured[0].event_type == "hook.timed_out"
        assert captured[0].severity == "warning"


# ---------------------------------------------------------------------------
# hook_id is preserved through fail-open paths
# ---------------------------------------------------------------------------


class TestHookIdPreservation:
    """Audit events must carry the originating ``hook_id`` even when the
    runner short-circuits on empty/malformed responses or non-2xx HTTP."""

    @pytest.mark.asyncio
    async def test_empty_stdout_preserves_hook_id(self) -> None:
        writer, captured = _capture_writer()
        entry = _Entry(id="pre-guard", runner=_Runner(command="true"))
        cfg = _HooksConfig(pre_tool=[entry])
        await run_pre_tool_hooks(cfg, "bash", {}, audit_writer=writer)  # type: ignore[arg-type]
        assert captured[0].details["hook_id"] == "pre-guard"
        assert captured[0].event_type == "hook.completed"

    @pytest.mark.asyncio
    async def test_malformed_json_preserves_hook_id(self) -> None:
        writer, captured = _capture_writer()
        entry = _Entry(id="pre-guard", runner=_Runner(command="echo not-json-at-all"))
        cfg = _HooksConfig(pre_tool=[entry])
        await run_pre_tool_hooks(cfg, "bash", {}, audit_writer=writer)  # type: ignore[arg-type]
        assert captured[0].details["hook_id"] == "pre-guard"
        assert captured[0].event_type == "hook.completed"

    @pytest.mark.asyncio
    async def test_webhook_http_400_preserves_hook_id(self) -> None:
        writer, captured = _capture_writer()
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_resp.text = ""
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(return_value=mock_resp)
        entry = _Entry(id="pre-webhook", runner=_Runner(type="webhook", url="http://example.test/hook"))
        cfg = _HooksConfig(pre_tool=[entry])
        with patch("httpx.AsyncClient", return_value=mock_client):
            await run_pre_tool_hooks(cfg, "bash", {}, audit_writer=writer)  # type: ignore[arg-type]
        assert captured[0].details["hook_id"] == "pre-webhook"
        assert captured[0].event_type == "hook.completed"
