"""Tests for the terminal Agent Handoff (Pattern 1).

A handoff-flagged agent tool ends the caller's loop: the child's answer
persists as the conversation's own assistant response (one barrier with the
stub), the tool plumbing hides from the user view, control returns to the
caller only on error. The batch policy is enforced BEFORE dispatch (a post-hoc
rejection cannot un-stream or un-spend a run child).
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

import matrx_ai._ext as ext
from matrx_ai.tools.agent_tool import _finalize_handoff_result
from matrx_ai.tools.models import (
    HandoffOutcome,
    ToolContext,
    ToolDefinition,
    ToolResult,
    ToolType,
)


def _handoff_tool() -> ToolDefinition:
    return ToolDefinition(
        name="custom_tool_1",
        tool_type=ToolType.AGENT,
        prompt_id="agent-b",
        handoff_terminal=True,
    )


class _FakeAgent:
    name = "closer"
    source_id = "agent-b"
    source_is_version = False
    output_schema = None


def _run_result(output: str = "", status: str = "", model_id: str = "m1"):
    from matrx_ai.agents.executor import AgentRunResult

    metadata = {"status": status} if status else {}
    return AgentRunResult(success=True, output=output, metadata=metadata, model_id=model_id)


# ── _finalize_handoff_result ─────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_successful_handoff_returns_terminal_stub(monkeypatch):
    ext._registry.pop("conversation_value_writer", None)
    result = await _finalize_handoff_result(
        _FakeAgent(),
        _handoff_tool(),
        _run_result(output="The final answer."),
        ToolContext(call_id="c1"),
        0.0,
        child_execution_id="exe-9",
    )
    assert result.success is True
    assert result.handoff_final is True
    assert isinstance(result.handoff, HandoffOutcome)
    assert result.handoff.final_text == "The final answer."
    assert result.handoff.child_execution_id == "exe-9"
    # The stub NEVER duplicates B's text (the next assistant message IS it).
    assert "final answer" not in str(result.output)
    assert result.output["status"] == "handoff_delivered"
    assert result.output_self_capped is True


@pytest.mark.asyncio
async def test_suspended_child_is_a_handoff_failure():
    result = await _finalize_handoff_result(
        _FakeAgent(),
        _handoff_tool(),
        _run_result(output="partial", status="suspended_awaiting_client"),
        ToolContext(call_id="c1"),
        0.0,
    )
    assert result.success is False
    assert result.handoff_final is False
    assert result.error.error_type == "agent_suspended"


@pytest.mark.asyncio
async def test_truncated_child_is_blocked_like_paused():
    # A truncated child hit its output token limit mid-sentence — its partial
    # text must NEVER persist as the conversation's final bubble. Treated like
    # paused (matching the summary mapping truncated→paused, commit 6bc8bbf5a):
    # delivery blocked, control returns to the caller with a resumable reason.
    result = await _finalize_handoff_result(
        _FakeAgent(),
        _handoff_tool(),
        _run_result(output="A cut-off mid-sentence answ", status="truncated"),
        ToolContext(call_id="c1"),
        0.0,
    )
    assert result.success is False
    assert result.handoff_final is False
    assert result.error.error_type == "child_truncated"
    assert result.error.is_retryable is True
    # The partial text is never delivered as a handoff outcome.
    assert result.handoff is None


@pytest.mark.asyncio
async def test_empty_child_answer_is_a_handoff_failure():
    result = await _finalize_handoff_result(
        _FakeAgent(),
        _handoff_tool(),
        _run_result(output="   "),
        ToolContext(call_id="c1"),
        0.0,
    )
    assert result.success is False
    assert result.error.error_type == "agent_empty_response"


@pytest.mark.asyncio
async def test_version_pinned_handoff_routes_id_to_version_column():
    """A handoff whose child agent was loaded from a VERSION row must put the id
    on HandoffOutcome.agent_version_id, NEVER agent_id (that promoted column is
    an FK to agent.definition; a version UUID passes the shape guard then fails
    the FK at the one handoff barrier, killing a delivered turn). The value-store
    writer must likewise receive source_agent_id=None for a version-sourced
    child — a version id in the agent_id FK column is the same failure class."""
    captured: dict[str, Any] = {}

    async def fake_writer(**kwargs):
        captured.update(kwargs)
        return {"key": "handoff-versioned", "description": kwargs["description"]}

    class _VersionAgent:
        name = "versioned-closer"
        source_id = "version-uuid-123"
        source_is_version = True
        output_schema = None

    before = ext._registry.get("conversation_value_writer")
    ext.configure_ext(conversation_value_writer=fake_writer)
    try:
        result = await _finalize_handoff_result(
            _VersionAgent(),
            _handoff_tool(),
            _run_result(output="Answer text"),
            ToolContext(call_id="cv"),
            0.0,
        )
        assert result.handoff.agent_id is None
        assert result.handoff.agent_version_id == "version-uuid-123"
        # The FK-bound column never receives a version id.
        assert captured["source_agent_id"] is None
    finally:
        if before is None:
            ext._registry.pop("conversation_value_writer", None)
        else:
            ext._registry["conversation_value_writer"] = before


@pytest.mark.asyncio
async def test_handoff_stores_answer_as_value_when_writer_configured():
    captured: dict[str, Any] = {}

    async def fake_writer(**kwargs):
        captured.update(kwargs)
        return {"key": "handoff-closer", "description": kwargs["description"]}

    before = ext._registry.get("conversation_value_writer")
    ext.configure_ext(conversation_value_writer=fake_writer)
    try:
        result = await _finalize_handoff_result(
            _FakeAgent(),
            _handoff_tool(),
            _run_result(output="Answer text"),
            ToolContext(call_id="c7"),
            0.0,
        )
        assert result.handoff.value_ref_key == "handoff-closer"
        assert result.value_ref_key == "handoff-closer"
        assert captured["value"] == "Answer text"
        assert captured["source_call_id"] == "c7"
    finally:
        if before is None:
            ext._registry.pop("conversation_value_writer", None)
        else:
            ext._registry["conversation_value_writer"] = before


# ── handoff finalize never scans the child's text as the caller's directives ──


class _Stop(Exception):
    """Short-circuits _finalize_and_persist right after the turn-directive scan."""


@pytest.mark.asyncio
async def test_handoff_finalize_does_not_scan_child_text_as_turn_directives(monkeypatch):
    """On the handoff finalize path (skip_structured_output=True) the synthetic
    final_response is the CHILD's text. It must NEVER be scanned as the CALLER's
    turn-authored directives — a groom fence the child wrote grooms ITS
    conversation (already applied by the child's own finalize); re-scanning it
    would re-execute against the PARENT. Pin: the turn-directive handler is
    invoked with NO child text on the handoff path, but WOULD receive it on a
    normal (non-handoff) finalize."""
    import matrx_ai._ext as _ext
    import matrx_ai.orchestrator.executor as executor_mod
    from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
    from matrx_ai.config.unified_config import UnifiedResponse
    from matrx_ai.orchestrator.requests import AIMatrixRequest

    GROOM_FENCE = (
        '```matrx\n{"matrx_version":1,"kind":"output_directive",'
        '"type":"context_groom","items":[{"key":"x"}]}\n```'
    )
    child_text = f"The specialist's answer. {GROOM_FENCE}"
    child_resp = UnifiedResponse(
        messages=[UnifiedMessage(role="assistant", content=[TextContent(text=child_text)])]
    )

    seen: list[str] = []

    async def rec_handler(*, turn_text, config, auto_stub_keys):
        seen.append(turn_text)

    real_apply = executor_mod._apply_turn_directives

    async def apply_then_stop(response, current_request, *, auto_stub_keys=None):
        # Run the REAL scan (so the handler is invoked with the correctly-gated
        # text), then short-circuit the heavy persistence tail.
        await real_apply(response, current_request, auto_stub_keys=auto_stub_keys)
        raise _Stop()

    before_handler = _ext._registry.get("turn_directive_handler")
    _ext.configure_ext(turn_directive_handler=rec_handler)
    monkeypatch.setattr(executor_mod, "_apply_turn_directives", apply_then_stop)

    def _req():
        cfg = UnifiedConfig(
            model="claude-test",
            messages=MessageList(
                _messages=[UnifiedMessage(role="user", content=[TextContent(text="hi")])]
            ),
        )
        return AIMatrixRequest(conversation_id="conv-1", config=cfg, request_id="req-1")

    try:
        # Handoff path: child text must NOT be scanned.
        with pytest.raises(_Stop):
            await executor_mod._finalize_and_persist(
                current_request=_req(),
                iteration=1,
                final_response=child_resp,
                metadata={"finish_reason": "handoff"},
                trigger_position=0,
                pre_execution_message_count=1,
                state=None,
                skip_structured_output=True,
            )
        assert seen == [""]
        assert GROOM_FENCE not in seen[0]

        # Contrast — a normal finalize DOES hand the model's text to the handler,
        # proving the gate above is load-bearing (not a vacuous empty scan).
        seen.clear()
        with pytest.raises(_Stop):
            await executor_mod._finalize_and_persist(
                current_request=_req(),
                iteration=1,
                final_response=child_resp,
                metadata={"finish_reason": "stop"},
                trigger_position=0,
                pre_execution_message_count=1,
                state=None,
                skip_structured_output=False,
            )
        assert seen and GROOM_FENCE in seen[0]
    finally:
        monkeypatch.undo()
        if before_handler is None:
            _ext._registry.pop("turn_directive_handler", None)
        else:
            _ext._registry["turn_directive_handler"] = before_handler


# ── batch policy (pre-dispatch) ──────────────────────────────────────────────


def _policy_env(monkeypatch, handoff_names: set[str]):
    import matrx_ai.tools.handle_tool_calls as htc

    monkeypatch.setattr(htc, "_is_handoff_call", lambda name: name in handoff_names)
    dispatched: list[list[str]] = []

    class _FakeExecutor:
        guardrails = None

        async def execute_batch(self, calls, ctx, *, client_tools=None, allowed_tools=None):
            dispatched.append([c["name"] for c in calls])
            content = [
                {
                    "tool_use_id": c["call_id"],
                    "call_id": c["call_id"],
                    "name": c["name"],
                    "content": "ok",
                    "is_error": False,
                }
                for c in calls
            ]
            results = [
                ToolResult(success=True, output="ok", tool_name=c["name"], call_id=c["call_id"])
                for c in calls
            ]
            return content, results

    monkeypatch.setattr(htc, "get_executor", lambda: _FakeExecutor())

    class _FakeLifecycle:
        sweep_running = True

    monkeypatch.setattr(
        htc.ToolLifecycleManager, "get_instance", classmethod(lambda cls: _FakeLifecycle())
    )
    return dispatched


@pytest.mark.asyncio
async def test_two_handoffs_are_blocked_pre_dispatch(monkeypatch):
    import matrx_ai.tools.handle_tool_calls as htc

    dispatched = _policy_env(monkeypatch, {"h1", "h2"})
    content, usages, pending, auto, outcome = await htc.handle_tool_calls_v2(
        [
            {"name": "h1", "arguments": {}, "call_id": "a"},
            {"name": "h2", "arguments": {}, "call_id": "b"},
            {"name": "normal", "arguments": {}, "call_id": "c"},
        ],
        iteration=1,
    )
    # Only the non-handoff call ran…
    assert dispatched == [["normal"]]
    # …both handoffs came back as policy errors, and no terminal outcome.
    errors = [c for c in content if c["is_error"]]
    assert {e["name"] for e in errors} == {"h1", "h2"}
    assert all("handoff_policy" in e["content"] for e in errors)
    assert outcome is None


@pytest.mark.asyncio
async def test_handoff_with_delegated_call_is_blocked(monkeypatch):
    import matrx_ai.tools.handle_tool_calls as htc

    dispatched = _policy_env(monkeypatch, {"h1"})
    content, *_rest, outcome = await htc.handle_tool_calls_v2(
        [
            {"name": "h1", "arguments": {}, "call_id": "a"},
            {"name": "client_thing", "arguments": {}, "call_id": "b"},
        ],
        iteration=1,
        client_tools=frozenset({"client_thing"}),
    )
    assert dispatched == [["client_thing"]]
    errors = [c for c in content if c["is_error"]]
    assert [e["name"] for e in errors] == ["h1"]
    assert outcome is None


@pytest.mark.asyncio
async def test_single_handoff_dispatches_and_partitions_outcome(monkeypatch):
    import matrx_ai.tools.handle_tool_calls as htc

    monkeypatch.setattr(htc, "_is_handoff_call", lambda name: name == "h1")

    class _FakeExecutor:
        async def execute_batch(self, calls, ctx, *, client_tools=None, allowed_tools=None):
            content, results = [], []
            for c in calls:
                content.append(
                    {
                        "tool_use_id": c["call_id"],
                        "call_id": c["call_id"],
                        "name": c["name"],
                        "content": "stub",
                        "is_error": False,
                    }
                )
                r = ToolResult(
                    success=True, output="stub", tool_name=c["name"], call_id=c["call_id"]
                )
                if c["name"] == "h1":
                    r.handoff_final = True
                    r.handoff = HandoffOutcome(final_text="B's answer")
                results.append(r)
            return content, results

    monkeypatch.setattr(htc, "get_executor", lambda: _FakeExecutor())

    class _FakeLifecycle:
        sweep_running = True

    monkeypatch.setattr(
        htc.ToolLifecycleManager, "get_instance", classmethod(lambda cls: _FakeLifecycle())
    )

    content, usages, pending, auto, outcome = await htc.handle_tool_calls_v2(
        [{"name": "h1", "arguments": {}, "call_id": "a"}], iteration=1
    )
    assert outcome is not None and outcome.final_text == "B's answer"


# ── lifecycle suppression ────────────────────────────────────────────────────


class _RecordingEmitter:
    def __init__(self):
        self.events: list[str] = []

    async def send_init(self, payload):
        self.events.append("init")

    async def send_completion(self, payload):
        self.events.append(f"completion:{payload.status}")


@pytest.mark.asyncio
async def test_child_lifecycle_suppressed_on_success_kept_on_failure():
    from matrx_connect.context.app_context import (
        AppContext,
        child_agent_context,
        mark_child_agent_failed,
        set_app_context,
    )

    emitter = _RecordingEmitter()
    set_app_context(AppContext(emitter=emitter, user_id="u1"))
    async with child_agent_context("handoff-child", emit_lifecycle=False):
        pass
    assert emitter.events == []  # invisible on success

    with pytest.raises(RuntimeError):
        async with child_agent_context("handoff-child", emit_lifecycle=False):
            raise RuntimeError("boom")
    # The FAILED completion is NEVER suppressed — the client's rewind signal.
    assert emitter.events == ["completion:failed"]

    emitter.events.clear()
    async with child_agent_context("handoff-child", emit_lifecycle=False):
        mark_child_agent_failed("status=failed")
    # Contained failures do not raise, but they carry the same rewind signal.
    assert emitter.events == ["completion:failed"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("output", "status"),
    [
        ("partial specialist text", "failed"),
        ("cut off specialist text", "truncated"),
        ("", "completed"),
    ],
)
async def test_run_agent_marks_contained_incomplete_handoff_for_rewind(output, status):
    from matrx_connect.context.app_context import AppContext, set_app_context

    from matrx_ai.agents.executor import run_agent

    emitter = _RecordingEmitter()
    set_app_context(AppContext(emitter=emitter, user_id="u1"))

    async def execute(user_input=None):
        return SimpleNamespace(
            output=output,
            assistant_response=None,
            config=SimpleNamespace(model="test-model"),
            usage=None,
            usage_history=[],
            metadata={"status": status},
        )

    agent = SimpleNamespace(
        name="specialist",
        config=SimpleNamespace(model="test-model"),
        source_id=None,
        source_is_version=False,
        execute=execute,
    )

    result = await run_agent(
        agent,
        label="handoff-child",
        source_app="test",
        source_feature="agent_tool",
        emit_lifecycle=False,
        require_complete_output=True,
    )

    assert result.output == output
    assert emitter.events == ["completion:failed"]
