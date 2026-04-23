"""Unit tests for hook/approval ordering and interplay (#1492).

Covers:
- classify_pre_hook_result helper
- hard-deny always wins over hook allow/ask
- hook deny blocks before tier-based approval
- hook ask → user approves → hook_escalated_approved
- hook ask → user denies → hook_escalated_denied
- hook allow → proceeds to tier-based approval unchanged
- no-hook fast path
- hook.approval_resolved audit emission
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from anteroom.services.hooks import _ALLOW, HookDecision, classify_pre_hook_result
from anteroom.tools.safety import SafetyVerdict

# ---------------------------------------------------------------------------
# Minimal config stubs (no full AppConfig needed)
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
# classify_pre_hook_result
# ---------------------------------------------------------------------------


class TestClassifyPreHookResult:
    def test_allow_maps_to_continue(self) -> None:
        assert classify_pre_hook_result(HookDecision(outcome="allow")) == "continue"

    def test_deny_maps_to_deny(self) -> None:
        assert classify_pre_hook_result(HookDecision(outcome="deny", message="blocked")) == "deny"

    def test_ask_maps_to_require_approval(self) -> None:
        assert classify_pre_hook_result(HookDecision(outcome="ask", message="confirm")) == "require_approval"

    def test_sentinel_allow_maps_to_continue(self) -> None:
        assert classify_pre_hook_result(_ALLOW) == "continue"


# ---------------------------------------------------------------------------
# Ordering invariants via ToolRegistry.call_tool
# ---------------------------------------------------------------------------


@pytest.fixture()
def registry() -> Any:
    from anteroom.tools import ToolRegistry

    r = ToolRegistry()

    async def _handler(**kwargs: Any) -> dict[str, Any]:
        return {"result": "ok"}

    r.register("echo_tool", _handler, {"name": "echo_tool", "description": "test", "parameters": {}})
    return r


class TestOrderingInvariants:
    @pytest.mark.asyncio
    async def test_hard_deny_wins_over_hook_allow(self, registry: Any) -> None:
        """Static hard deny must block before hooks ever run."""
        mock_enforcer = MagicMock()
        mock_enforcer.check_tool_call.return_value = (True, "hard block", "rule::fqn")

        hook_called: list[bool] = []

        async def _allow_hook(*args: Any, **kwargs: Any) -> HookDecision:
            hook_called.append(True)
            return HookDecision(outcome="allow")

        hooks_cfg = _HooksConfig(pre_tool=[_Entry()])
        with patch("anteroom.services.hooks.run_pre_tool_hooks", _allow_hook):
            result = await registry.call_tool(
                "echo_tool",
                {},
                rule_enforcer_override=mock_enforcer,
                _hooks_config=hooks_cfg,  # type: ignore[arg-type]
            )

        assert result["_approval_decision"] == "hard_denied"
        assert not hook_called, "hooks must never run when rule enforcer hard-denies"

    @pytest.mark.asyncio
    async def test_hard_deny_wins_over_hook_ask(self, registry: Any) -> None:
        """A hook ask cannot override a static rule enforcer hard deny."""
        mock_enforcer = MagicMock()
        mock_enforcer.check_tool_call.return_value = (True, "hard block", "rule::fqn")

        async def _ask_hook(*args: Any, **kwargs: Any) -> HookDecision:
            return HookDecision(outcome="ask", message="please confirm")

        hooks_cfg = _HooksConfig(pre_tool=[_Entry()])
        with patch("anteroom.services.hooks.run_pre_tool_hooks", _ask_hook):
            result = await registry.call_tool(
                "echo_tool",
                {},
                rule_enforcer_override=mock_enforcer,
                _hooks_config=hooks_cfg,  # type: ignore[arg-type]
            )

        assert result["_approval_decision"] == "hard_denied"

    @pytest.mark.asyncio
    async def test_hook_deny_blocks_before_tier_approval(self, registry: Any) -> None:
        """Hook deny must block unconditionally — no tier-based approval prompt."""
        approval_called: list[bool] = []

        async def _approval_cb(verdict: SafetyVerdict) -> bool:
            approval_called.append(True)
            return True  # would approve if reached

        async def _deny_hook(*args: Any, **kwargs: Any) -> HookDecision:
            return HookDecision(outcome="deny", message="hook says no")

        hooks_cfg = _HooksConfig(pre_tool=[_Entry()])
        with patch("anteroom.services.hooks.run_pre_tool_hooks", _deny_hook):
            result = await registry.call_tool(
                "echo_tool",
                {},
                confirm_callback=_approval_cb,
                _hooks_config=hooks_cfg,  # type: ignore[arg-type]
            )

        assert result.get("hook_blocked") is True
        assert result["_approval_decision"] == "hook_denied"
        assert not approval_called, "tier-based approval must not run after hook deny"

    @pytest.mark.asyncio
    async def test_hook_ask_user_approves(self, registry: Any) -> None:
        """Hook ask + user approves → tool runs with hook_escalated_approved."""

        async def _ask_hook(*args: Any, **kwargs: Any) -> HookDecision:
            return HookDecision(outcome="ask", message="please confirm", hook_id="hook-1")

        async def _approve_cb(verdict: SafetyVerdict) -> bool:
            return True

        hooks_cfg = _HooksConfig(pre_tool=[_Entry()])
        with patch("anteroom.services.hooks.run_pre_tool_hooks", _ask_hook):
            result = await registry.call_tool(
                "echo_tool",
                {},
                confirm_callback=_approve_cb,
                _hooks_config=hooks_cfg,  # type: ignore[arg-type]
            )

        assert result.get("result") == "ok", "tool should have executed"
        assert result["_approval_decision"] == "hook_escalated_approved"

    @pytest.mark.asyncio
    async def test_hook_ask_user_denies(self, registry: Any) -> None:
        """Hook ask + user denies → tool blocked with hook_escalated_denied."""

        async def _ask_hook(*args: Any, **kwargs: Any) -> HookDecision:
            return HookDecision(outcome="ask", message="please confirm", hook_id="hook-1")

        async def _deny_cb(verdict: SafetyVerdict) -> bool:
            return False

        hooks_cfg = _HooksConfig(pre_tool=[_Entry()])
        with patch("anteroom.services.hooks.run_pre_tool_hooks", _ask_hook):
            result = await registry.call_tool(
                "echo_tool",
                {},
                confirm_callback=_deny_cb,
                _hooks_config=hooks_cfg,  # type: ignore[arg-type]
            )

        assert result["_approval_decision"] == "hook_escalated_denied"
        assert "error" in result

    @pytest.mark.asyncio
    async def test_hook_ask_no_callback_denies(self, registry: Any) -> None:
        """Hook ask with no approval callback must fail closed."""

        async def _ask_hook(*args: Any, **kwargs: Any) -> HookDecision:
            return HookDecision(outcome="ask", message="please confirm")

        hooks_cfg = _HooksConfig(pre_tool=[_Entry()])
        with patch("anteroom.services.hooks.run_pre_tool_hooks", _ask_hook):
            result = await registry.call_tool(
                "echo_tool",
                {},
                confirm_callback=None,
                _hooks_config=hooks_cfg,  # type: ignore[arg-type]
            )

        assert result.get("_approval_decision") == "denied"
        assert result.get("hook_blocked") is True

    @pytest.mark.asyncio
    async def test_hook_allow_proceeds_to_tier_approval(self, registry: Any) -> None:
        """Hook allow does not bypass tier-based approval when tool requires it."""
        from anteroom.config import SafetyConfig
        from anteroom.tools.tiers import ToolTier

        registry.set_safety_config(SafetyConfig(approval_mode="ask"))

        # Override tier so echo_tool requires approval
        with patch("anteroom.tools.get_tool_tier", return_value=ToolTier.WRITE):
            approval_called: list[bool] = []

            async def _ask_hook(*args: Any, **kwargs: Any) -> HookDecision:
                return HookDecision(outcome="allow")

            async def _approval_cb(verdict: SafetyVerdict) -> bool:
                approval_called.append(True)
                return True

            hooks_cfg = _HooksConfig(pre_tool=[_Entry()])
            with patch("anteroom.services.hooks.run_pre_tool_hooks", _ask_hook):
                result = await registry.call_tool(
                    "echo_tool",
                    {},
                    confirm_callback=_approval_cb,
                    _hooks_config=hooks_cfg,  # type: ignore[arg-type]
                )

        assert approval_called, "tier-based approval must still run after hook allow"
        assert result.get("result") == "ok"

    @pytest.mark.asyncio
    async def test_no_hooks_fast_path(self, registry: Any) -> None:
        """When no hooks are configured, the tool runs without any hook overhead."""
        result = await registry.call_tool("echo_tool", {})
        assert result.get("result") == "ok"
        assert result["_approval_decision"] == "auto"

    @pytest.mark.asyncio
    async def test_hook_escalated_approved_not_overwritten_by_tier_approval(self, registry: Any) -> None:
        """hook_escalated_approved must survive when the tool ALSO needs tier approval.

        Regression guard for the missing `if approval_decision == "auto"` guard
        on the tier-approval path (tools/__init__.py).  Without the guard, a
        hook-escalated approval followed by tier-based approval would silently
        overwrite the decision to "allowed_once" in the audit record.
        """
        from anteroom.config import SafetyConfig
        from anteroom.tools.tiers import ToolTier

        registry.set_safety_config(SafetyConfig(approval_mode="ask"))

        with patch("anteroom.tools.get_tool_tier", return_value=ToolTier.WRITE):
            callback_calls: list[str] = []

            async def _ask_hook(*args: Any, **kwargs: Any) -> HookDecision:
                return HookDecision(outcome="ask", hook_id="guard-test-hook")

            async def _approve_cb(verdict: SafetyVerdict) -> bool:
                callback_calls.append("approved")
                return True

            hooks_cfg = _HooksConfig(pre_tool=[_Entry()])
            with patch("anteroom.services.hooks.run_pre_tool_hooks", _ask_hook):
                result = await registry.call_tool(
                    "echo_tool",
                    {},
                    confirm_callback=_approve_cb,
                    _hooks_config=hooks_cfg,  # type: ignore[arg-type]
                )

        # Both the hook escalation and tier-based approval prompted the user.
        assert len(callback_calls) == 2, "expect approval prompt for both hook escalation and tier gate"
        # The hook decision must win — not "allowed_once" from the tier gate.
        assert result["_approval_decision"] == "hook_escalated_approved"
        assert result.get("result") == "ok"


# ---------------------------------------------------------------------------
# hook.approval_resolved audit emission
# ---------------------------------------------------------------------------


class TestHookApprovalResolvedAudit:
    @pytest.mark.asyncio
    async def test_emit_on_user_approve(self, registry: Any) -> None:
        """hook.approval_resolved is emitted with resolution=approved when user approves."""

        mock_writer = MagicMock()

        async def _ask_hook(*args: Any, **kwargs: Any) -> HookDecision:
            return HookDecision(outcome="ask", hook_id="h-audit")

        async def _approve_cb(verdict: SafetyVerdict) -> bool:
            return True

        hooks_cfg = _HooksConfig(pre_tool=[_Entry()])
        with patch("anteroom.services.hooks.run_pre_tool_hooks", _ask_hook):
            await registry.call_tool(
                "echo_tool",
                {},
                confirm_callback=_approve_cb,
                _hooks_config=hooks_cfg,  # type: ignore[arg-type]
                _audit_writer=mock_writer,
            )

        emitted_types = [call[0][0].event_type for call in mock_writer.emit.call_args_list]
        assert "hook.approval_resolved" in emitted_types

        resolved_entries = [
            call[0][0] for call in mock_writer.emit.call_args_list if call[0][0].event_type == "hook.approval_resolved"
        ]
        assert resolved_entries[0].details["resolution"] == "approved"
        assert resolved_entries[0].details["hook_id"] == "h-audit"

    @pytest.mark.asyncio
    async def test_emit_on_user_deny(self, registry: Any) -> None:
        """hook.approval_resolved is emitted with resolution=denied when user denies."""

        async def _ask_hook(*args: Any, **kwargs: Any) -> HookDecision:
            return HookDecision(outcome="ask", hook_id="h-deny-audit")

        async def _deny_cb(verdict: SafetyVerdict) -> bool:
            return False

        mock_writer = MagicMock()
        hooks_cfg = _HooksConfig(pre_tool=[_Entry()])
        with patch("anteroom.services.hooks.run_pre_tool_hooks", _ask_hook):
            await registry.call_tool(
                "echo_tool",
                {},
                confirm_callback=_deny_cb,
                _hooks_config=hooks_cfg,  # type: ignore[arg-type]
                _audit_writer=mock_writer,
            )

        emitted_types = [call[0][0].event_type for call in mock_writer.emit.call_args_list]
        assert "hook.approval_resolved" in emitted_types

        resolved_entries = [
            call[0][0] for call in mock_writer.emit.call_args_list if call[0][0].event_type == "hook.approval_resolved"
        ]
        assert resolved_entries[0].details["resolution"] == "denied"

    def test_emit_hook_approval_resolved_bad_resolution_drops(self) -> None:
        """emit_hook_approval_resolved drops unknown resolution values."""
        from anteroom.services.lineage import emit_hook_approval_resolved

        mock_writer = MagicMock()
        emit_hook_approval_resolved(mock_writer, hook_id="h1", tool_name="bash", resolution="maybe")
        mock_writer.emit.assert_not_called()

    def test_emit_hook_approval_resolved_none_writer_is_noop(self) -> None:
        from anteroom.services.lineage import emit_hook_approval_resolved

        emit_hook_approval_resolved(None, hook_id="h1", tool_name="bash", resolution="approved")

    def test_emit_hook_approval_resolved_severity_approved_is_info(self) -> None:
        """Approved resolution uses severity=info."""
        from anteroom.services.lineage import emit_hook_approval_resolved

        mock_writer = MagicMock()
        emit_hook_approval_resolved(mock_writer, hook_id="h1", tool_name="bash", resolution="approved")
        entry = mock_writer.emit.call_args[0][0]
        assert entry.severity == "info"

    def test_emit_hook_approval_resolved_severity_denied_is_warning(self) -> None:
        """Denied resolution uses severity=warning."""
        from anteroom.services.lineage import emit_hook_approval_resolved

        mock_writer = MagicMock()
        emit_hook_approval_resolved(mock_writer, hook_id="h1", tool_name="bash", resolution="denied")
        entry = mock_writer.emit.call_args[0][0]
        assert entry.severity == "warning"

    def test_emit_hook_approval_resolved_includes_optional_context_fields(self) -> None:
        """Optional tool_call_id and conversation_id are included when provided."""
        from anteroom.services.lineage import emit_hook_approval_resolved

        mock_writer = MagicMock()
        emit_hook_approval_resolved(
            mock_writer,
            hook_id="h1",
            tool_name="bash",
            resolution="approved",
            tool_call_id="tc-123",
            conversation_id="conv-456",
            user_id="user-789",
        )
        entry = mock_writer.emit.call_args[0][0]
        assert entry.details["tool_call_id"] == "tc-123"
        assert entry.details["conversation_id"] == "conv-456"
        assert entry.user_id == "user-789"

    @pytest.mark.asyncio
    async def test_emit_exception_does_not_propagate(self, registry: Any) -> None:
        """If emit_hook_approval_resolved raises, call_tool must not propagate the error."""

        async def _ask_hook(*args: Any, **kwargs: Any) -> HookDecision:
            return HookDecision(outcome="ask", hook_id="h-exc")

        async def _approve_cb(verdict: SafetyVerdict) -> bool:
            return True

        broken_writer = MagicMock()
        broken_writer.emit.side_effect = RuntimeError("audit failure")

        hooks_cfg = _HooksConfig(pre_tool=[_Entry()])
        with patch("anteroom.services.hooks.run_pre_tool_hooks", _ask_hook):
            result = await registry.call_tool(
                "echo_tool",
                {},
                confirm_callback=_approve_cb,
                _hooks_config=hooks_cfg,  # type: ignore[arg-type]
                _audit_writer=broken_writer,
            )

        assert result.get("result") == "ok", "tool must execute even when audit emission fails"
        assert result["_approval_decision"] == "hook_escalated_approved"
