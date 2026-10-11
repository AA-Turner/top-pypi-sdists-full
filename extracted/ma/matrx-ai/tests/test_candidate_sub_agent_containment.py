"""A mandate candidate's SUB-AGENT runs contained — through the REAL ``agent_call`` body.

Mandate Candidates, handoff step 4. ``agent_call`` / ``mandate_call`` /
``staff_escalate`` start a child agent run. Inside a candidate that child must be
contained exactly like the parent: the marker and the ONE shared ledger reach it,
each of its calls is decided real / borrowed / stopped, and a stop in the child
ends the parent terminally with the child's proposed call as ``stopped_at``.

Every test drives the REAL ``ToolExecutor.execute`` → the REAL ``agent_call`` body
→ ``run_agent`` (doubled only at its edge: the double enters the real
``child_agent_context`` and makes the child's tool call through the same
executor). Doubles: tool bodies (record whether they ran), the agent row load,
the durable tool-row writes.

* write child → the write body never runs; the parent's ``agent_call`` ends
  ``candidate_stopped``; ``stopped_at`` is the child's call with its arguments;
  ``tool_dispositions`` = ``agent_call: contained`` then ``<write>: stopped``.
* read child → the read runs; the parent gets the child's answer and continues;
  ``agent_call`` is recorded ``contained``, never ``stopped``.
* the child's conversation is the hidden ``mandate_candidate`` lane — including a
  ``history_mode='fork'`` child, whose fork the host would otherwise stamp ``subagent``.

The aidream half (``mandate_call`` / ``staff_escalate`` never hand off inside a
candidate) is ``aidream/services/mandates/candidates/tests/test_sub_agent_never_hands_off.py``;
the live end-to-end proof is ``…/candidates/tests/test_sub_agent_containment_live.py``.
"""

from __future__ import annotations

import contextlib
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect.emitters.silent_emitter import SilentEmitter

from matrx_ai.tools.executor import ToolExecutor
from matrx_ai.tools.logger import ToolExecutionLogger
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolResult, ToolType
from matrx_ai.tools.registry import ToolRegistry

USER_ID = "11111111-1111-4111-8111-111111111111"
AGENT_ID = "22222222-2222-4222-8222-222222222222"
CALLER_CONV = "33333333-3333-4333-8333-333333333333"
FORK_CONV = "55555555-5555-4555-8555-555555555555"
MARKER = {
    "candidate_id": "aaaaaaaa-1111-4111-8111-111111111111",
    "candidate_run_id": "bbbbbbbb-2222-4222-8222-222222222222",
    "live_request_id": "cccccccc-3333-4333-8333-333333333333",
}


class _FakeAgent:
    name = "child"
    output_schema = None

    def __init__(self) -> None:
        self.config = SimpleNamespace(messages=[SimpleNamespace(role="user", authored=True)])


async def _value(value: Any) -> Any:
    return value


@pytest.fixture
def world(monkeypatch: pytest.MonkeyPatch):
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import (
        child_agent_context,
        clear_app_context,
        set_app_context,
    )

    import matrx_ai.persistence.queue_helpers as qh
    from matrx_ai import _ext
    from matrx_ai.agents import executor as executor_mod
    from matrx_ai.agents.definition import Agent
    from matrx_ai.agents.executor import AgentRunResult
    from matrx_ai.db.agx_manager import AgxDefinition
    from matrx_ai.db.conversation_gate import _resolve_conversation_type
    from matrx_ai.tools.candidate_containment import candidate_context_metadata
    from matrx_ai.tools.implementations.agent_call import agent_call

    monkeypatch.setattr(qh, "get_coordinator", lambda: None)

    async def _log_started(self, ctx, tool_def, arguments, **kw):
        return f"row-{tool_def.name}-{ctx.call_id}"

    async def _noop(self, *_a, **_kw):
        return None

    monkeypatch.setattr(ToolExecutionLogger, "log_started", _log_started)
    for name in ("log_abandoned", "log_completed", "log_error", "delegate_durably"):
        monkeypatch.setattr(ToolExecutionLogger, name, _noop)

    @contextlib.asynccontextmanager
    async def acting_as_caller(_ctx: Any = None):
        yield

    monkeypatch.setitem(_ext._registry, "acting_as_caller", acting_as_caller)

    async def load_agent(_cls, _agent_id):
        return SimpleNamespace(id=AGENT_ID, created_by=USER_ID, is_active=True, is_archived=False)

    monkeypatch.setattr(AgxDefinition, "load_by_id_or_none", classmethod(load_agent))
    monkeypatch.setattr(
        Agent, "from_agent", classmethod(lambda _cls, *_a, **_k: _value(_FakeAgent()))
    )

    registry = ToolRegistry.get_instance()
    saved = dict(registry._tools)
    executor = ToolExecutor(registry=registry)
    bag: dict[str, Any] = {
        "invoked": [],
        "child": [],  # what the child's context looked like
        "child_call": None,  # (tool, args) the child makes
        "forks": [],
    }

    def add_tool(name: str, side_effect_class: str | None, output: Any = "done") -> None:
        async def body(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
            bag["invoked"].append((name, dict(args)))
            return ToolResult(success=True, output=output, tool_name=name, call_id=ctx.call_id)

        definition = ToolDefinition(
            name=name,
            description=f"{name} test tool",
            parameters={},
            tool_type=ToolType.LOCAL,
            function_path=f"tests.fake.{name}",
            side_effect_class=side_effect_class,
        )
        definition._callable = body
        registry._tools[name] = definition

    sub_agent = ToolDefinition(
        name="agent_call",
        description="run another agent",
        parameters={},
        tool_type=ToolType.LOCAL,
        function_path="matrx_ai.tools.implementations.agent_call.agent_call",
        side_effect_class="platform_meta",
    )
    sub_agent._callable = agent_call
    registry._tools["agent_call"] = sub_agent

    async def fake_run_agent(_agent, **kwargs):
        """``run_agent``'s edge: the REAL child fork, then the child's one tool call."""
        async with child_agent_context(
            "child", emit_lifecycle=False, conversation_id=kwargs.get("conversation_id")
        ) as child_ctx:
            bag["child"].append(
                {
                    "metadata": child_ctx.metadata,
                    "conversation_type": _resolve_conversation_type(child_ctx),
                }
            )
            tool, args = bag["child_call"]
            _content, child_result = await executor.execute(
                tool, args, ToolContext(call_id="child-call-1", tool_name=tool)
            )
        if getattr(child_result, "candidate_stopped", False):
            return AgentRunResult(
                success=True,
                output="",
                metadata={"status": "candidate_stopped", "conversation_id": "child-conv"},
            )
        return AgentRunResult(
            success=True,
            output=f"child answer: {child_result.output}",
            metadata={"conversation_id": "child-conv"},
        )

    monkeypatch.setattr(executor_mod, "run_agent", fake_run_agent)

    async def forker(**kwargs):
        bag["forks"].append(kwargs)
        return {"conversation_id": FORK_CONV, "message_count": 1}

    monkeypatch.setitem(_ext._registry, "conversation_forker", forker)

    async def _load_unified_config(_conversation_id: str):
        return SimpleNamespace(messages=[])

    from matrx_ai.agents import resolver as resolver_mod

    monkeypatch.setattr(resolver_mod, "_load_unified_config", _load_unified_config)

    import matrx_ai.db as db_pkg

    async def _owned(**_kw):
        return [SimpleNamespace(id=CALLER_CONV, conversation_type="mandate_candidate")]

    monkeypatch.setattr(
        db_pkg,
        "cxm",
        SimpleNamespace(conversation=SimpleNamespace(filter_items=_owned)),
        raising=False,
    )

    metadata = candidate_context_metadata(MARKER)
    token = set_app_context(
        AppContext(
            emitter=SilentEmitter(),
            user_id=USER_ID,
            conversation_id=CALLER_CONV,
            metadata=metadata,
            is_authenticated=True,
        )
    )
    bag.update(
        executor=executor,
        add_tool=add_tool,
        ledger=metadata["mandate_candidate_containment"],
    )
    try:
        yield bag
    finally:
        clear_app_context(token)
        registry._tools = saved


def _dispositions(ledger: dict[str, Any]) -> list[tuple[str, str]]:
    return [(d["tool"], d["disposition"]) for d in ledger["tool_dispositions"]]


async def _call_sub_agent(world: dict[str, Any], **extra: Any):
    return await world["executor"].execute(
        "agent_call",
        {"agent_id": AGENT_ID, "user_input": "go", **extra},
        ToolContext(call_id="parent-call-1", tool_name="agent_call"),
    )


async def test_a_sub_agent_write_halts_the_candidate_with_zero_effect(world) -> None:
    world["add_tool"]("send_text_test", "sends_to_human")
    world["child_call"] = ("send_text_test", {"to": "+15550100", "body": "hello"})

    content, result = await _call_sub_agent(world)

    assert world["child"], "the child never ran — the proof proves nothing"
    child = world["child"][0]
    assert child["metadata"].get("mandate_candidate") == MARKER, "the child lost the marker"
    assert child["metadata"].get("mandate_candidate_containment") is world["ledger"], (
        "the child got its own ledger — its dispositions and stop are invisible to the parent"
    )
    assert world["invoked"] == [], "the child's write RAN inside a candidate"
    assert result.candidate_stopped is True, (
        "the parent was handed an answer after the child stopped"
    )
    assert "child answer" not in str(content)
    stop = world["ledger"]["stopped_at"]
    assert stop["tool"] == "send_text_test"
    assert stop["args"] == {"to": "+15550100", "body": "hello"}, (
        "the proposed write was not recorded"
    )
    assert _dispositions(world["ledger"]) == [
        ("agent_call", "contained"),
        ("send_text_test", "stopped"),
    ]


async def test_a_sub_agent_that_only_reads_runs_and_the_parent_continues(world) -> None:
    world["add_tool"]("lookup_test", "read_only", output="3 rows")
    world["child_call"] = ("lookup_test", {"q": "plants"})

    _content, result = await _call_sub_agent(world)

    assert world["invoked"] == [("lookup_test", {"q": "plants"})], "the child's read did not run"
    assert not getattr(result, "candidate_stopped", False)
    assert result.success is True, result.error
    assert "child answer: 3 rows" in str(result.output)
    assert world["ledger"]["stopped_at"] is None
    assert _dispositions(world["ledger"]) == [
        ("agent_call", "contained"),
        ("lookup_test", "real"),
    ]
    entry = world["ledger"]["tool_dispositions"][0]
    assert entry["side_effect_class"] == "agent" and entry["stopped_reason"] is None


async def test_the_childs_conversation_is_the_hidden_candidate_lane(world) -> None:
    world["add_tool"]("lookup_test", "read_only")
    world["child_call"] = ("lookup_test", {"q": "x"})

    await _call_sub_agent(world)

    assert world["child"][0]["conversation_type"] == "mandate_candidate"


async def test_a_forked_childs_conversation_is_the_hidden_candidate_lane(world) -> None:
    """``history_mode='fork'`` writes the child's conversation through the host's
    forker BEFORE the child runs, so the conversation gate never stamps it: the
    fork itself must ask for the hidden lane, never ``subagent``."""
    world["add_tool"]("lookup_test", "read_only")
    world["child_call"] = ("lookup_test", {"q": "x"})

    _content, result = await _call_sub_agent(
        world, history_mode="fork", history_conversation_id=CALLER_CONV
    )

    assert result.success is True, result.error
    assert len(world["forks"]) == 1
    assert world["forks"][0]["conversation_type"] == "mandate_candidate"
    assert world["child"][0]["conversation_type"] == "mandate_candidate"
