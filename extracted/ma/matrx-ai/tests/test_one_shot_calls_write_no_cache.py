"""FORCING GUARD — a one-shot call writes no prompt cache unless the knob says otherwise.

A cache mark is a WRITE (Anthropic: 1.25x input for 5 minutes) and pays only when a later
call reads it. Every workflow writer step and every strict-JSON funnel call is one-shot, yet
the Anthropic translator always placed the system mark and the rolling last-message mark: agent
build 665d38ad wrote 37,842 cache tokens across five Opus writer calls and read 2,669
(common-docs masterwork/agent-creation-studio/projects/rebuild/lane-3A-l.md). The decision now
lives at the ONE send boundary (``config/cache_plan.py``); a call with no cache_control mark on
the wire produces no cache_creation tokens. Red before the plan existed, green after.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from matrx_ai.config import UnifiedConfig, cache_plan
from matrx_ai.config.context_trim import TrimPolicy
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send, reset_loop_state
from matrx_ai.config.unified_content import TextContent
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.testing.profile_factory import make_profile

SYSTEM = "You write one careful contract for an agent build. " * 60


@pytest.fixture(autouse=True)
def _fresh_plan_state():
    cache_plan.reset_for_tests()
    yield
    cache_plan.reset_for_tests()


def _config(*, system: str = SYSTEM, long_cache: bool | None = None, tools: list | None = None) -> UnifiedConfig:
    return UnifiedConfig(
        model="claude-opus-5-5",
        system_instruction=system,
        messages=[UnifiedMessage(role="user", content=[TextContent(text="Write the contract for: thank donors.")])],
        extended_prompt_cache=long_cache,
        tools=list(tools or []),
    )


def _marks(payload: Any) -> list[dict[str, Any]]:
    """Every cache_control mark anywhere on the literal provider payload."""
    found: list[dict[str, Any]] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if "cache_control" in node:
                found.append(node["cache_control"])
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(payload)
    return found


def _send(config: UnifiedConfig, *, conversation_id: str = "conv-one-shot") -> dict[str, Any]:
    """The real hop: the send boundary's loop pass, then the Anthropic translator on its wire copy."""
    prep = asyncio.run(
        prepare_for_send(
            config,
            stage=STAGE_LOOP,
            conversation_id=conversation_id,
            request_id=f"req-{conversation_id}",
            iteration=1,
            policy=TrimPolicy(),
        )
    )
    reset_loop_state(conversation_id, f"req-{conversation_id}")
    wire = prep.wire_config or config
    return AnthropicTranslator().to_anthropic(
        wire, make_profile(model_name="claude-opus-5-5", wire_format="anthropic_chat")
    )


def _one_shot(config: UnifiedConfig, **kw: Any) -> dict[str, Any]:
    with cache_plan.one_shot_call():
        return _send(config, **kw)


def test_a_one_shot_call_sends_no_cache_mark() -> None:
    payload = _one_shot(_config())
    assert _marks(payload) == [], (
        "a one-shot call (no tools, nothing continues it) put cache_control marks on the wire: "
        "every marked token is billed as a cache WRITE that no later call reads"
    )
    assert isinstance(payload["system"], str) and SYSTEM.strip() in payload["system"]


def test_a_conversation_keeps_every_mark() -> None:
    marks = _marks(_send(_config()))
    assert len(marks) == 2  # system + rolling


def test_a_one_shot_tool_loop_keeps_the_rolling_mark() -> None:
    tool = {"name": "lookup", "description": "look", "input_schema": {"type": "object", "properties": {}}}
    plan = None
    with cache_plan.one_shot_call():
        plan = cache_plan.decide_cache_plan(_config(tools=[tool]))
    assert plan.marks == cache_plan.MARKS_ALL and plan.reason == "tool_loop"


def test_the_long_cache_switch_keeps_its_one_hour_prefix_and_drops_the_rolling_mark() -> None:
    """The 1-hour switch exists so runs spaced up to an hour apart reuse the stable prefix."""
    payload = _one_shot(_config(long_cache=True))
    assert _marks(payload) == [{"type": "ephemeral", "ttl": "1h"}]
    assert "cache_control" not in payload["messages"][-1]["content"][-1]


def test_a_repeated_prefix_is_marked_on_its_second_send() -> None:
    first = _one_shot(_config(), conversation_id="conv-a")
    second = _one_shot(_config(), conversation_id="conv-b")
    assert _marks(first) == []
    assert _marks(second) == [{"type": "ephemeral"}]  # system only, no rolling mark


def test_a_different_prefix_is_not_a_repeat() -> None:
    _one_shot(_config(), conversation_id="conv-a")
    assert _marks(_one_shot(_config(system="Another writer. " * 80), conversation_id="conv-b")) == []


@pytest.mark.parametrize(
    ("policy", "expected"),
    [("always", 2), ("prefix", 1), ("never", 0), ("when_read_expected", 0), ("garbage", 0)],
)
def test_the_knob_decides_what_a_one_shot_call_writes(policy: str, expected: int) -> None:
    cache_plan.configure_prompt_cache_knobs(lambda key: policy if key == cache_plan.ONE_SHOT_MARKS_KEY else None)
    assert len(_marks(_one_shot(_config()))) == expected


def test_never_wins_over_long_cache() -> None:
    cache_plan.configure_prompt_cache_knobs(lambda _key: "never")
    assert _marks(_one_shot(_config(long_cache=True))) == []


def test_a_failing_knob_reader_falls_back_to_the_mirror() -> None:
    def broken(_key: str) -> Any:
        raise RuntimeError("knob cache not primed")

    cache_plan.configure_prompt_cache_knobs(broken)
    assert cache_plan.one_shot_marks_policy() == cache_plan.ONE_SHOT_MARKS_MIRROR


def test_the_strict_json_funnel_declares_its_call_one_shot(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.graph_nodes import _strict_json
    from matrx_ai.orchestrator import executor

    seen: list[bool] = []

    async def fake_execute(*_a: Any, **_kw: Any) -> Any:
        seen.append(cache_plan.is_one_shot_call())
        raise RuntimeError("stop after the declaration was read")

    monkeypatch.setattr(executor, "execute_ai_request", fake_execute)
    with pytest.raises(RuntimeError, match="stop after"):
        asyncio.run(
            _strict_json._run_completion_measured(
                [{"role": "user", "content": "hi"}], "system", model="claude-opus-5-5", max_tokens=10
            )
        )
    assert seen == [True]
    assert cache_plan.is_one_shot_call() is False  # the scope ends with the call


def test_a_workflow_agent_step_declares_its_run_one_shot(monkeypatch: pytest.MonkeyPatch) -> None:
    from types import SimpleNamespace

    from matrx_connect.context.app_context import AppContext

    from matrx_ai.graph_nodes import agent_action

    class _Emitter:
        async def send_record_reserved(self, _payload: Any) -> None:
            return None

    seen: list[bool] = []

    async def runner(_agent_id: str, _request: Any, _ctx: Any) -> str:
        seen.append(cache_plan.is_one_shot_call())
        return "done"

    monkeypatch.setattr(agent_action, "get_ext", lambda name: runner)
    monkeypatch.setattr(agent_action, "has_ext", lambda name: False)
    root = AppContext(emitter=_Emitter(), user_id="e4687a9c-acf7-469f-aa12-860eb4d948d0", request_id="r-root")
    step = SimpleNamespace(app=root.fork_for_workflow_step("conv-write-contract"), node_id="write_contract")
    assert asyncio.run(agent_action.run_step_agent(step, "agent-1", object())) == "done"  # type: ignore[arg-type]
    assert seen == [True]
    assert cache_plan.is_one_shot_call() is False


def test_only_the_send_boundary_stamps_the_plan() -> None:
    """The class half lives in test_send_boundary_guard.py (seam 'prompt_cache_marks assignment')."""
    from pathlib import Path

    guard = (Path(__file__).parent / "test_send_boundary_guard.py").read_text()
    assert 'name="prompt_cache_marks assignment"' in guard


def test_the_cache_miss_alarm_stays_quiet_when_the_plan_sent_no_mark(monkeypatch: pytest.MonkeyPatch) -> None:
    """A zero read after a send with no mark is the plan (knob ``never``), not broken caching."""
    from matrx_ai.providers import cache_guard

    reds: list[str] = []
    monkeypatch.setattr(
        cache_guard,
        "vcprint",
        lambda *a, color=None, **_kw: reds.append(" ".join(map(str, a))) if color == "red" else None,
    )
    cache_guard._LOOPS.clear()
    common: dict[str, Any] = dict(
        provider="anthropic", model="claude-sonnet-5", conversation_id="conv-w", request_id="req-w",
        system_text="SYS " * 500, tool_names=(), raw_usage={"input_tokens": 6000},
    )
    cache_guard.observe_cache_usage(marks_withheld=True, **common)
    cache_guard.observe_cache_usage(marks_withheld=True, **common)
    assert not any("ZERO CACHE READ" in r for r in reds)
    cache_guard._LOOPS.clear()
    cache_guard.observe_cache_usage(**common)
    cache_guard.observe_cache_usage(**common)
    assert any("ZERO CACHE READ" in r for r in reds), "the alarm must still fire when marks were sent"
