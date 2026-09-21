"""ONE TOOL, NOT EVERY TOOL — and the ceilings come from settings rows.

Measured 2026-09-20 on ``chat.tool_call`` (2026-03-19 → 2026-09-20):

* 38 of 2,329 (run, tool) pairs ever reached the failure ceiling — the guard's
  decision is rare and expensive;
* of 2,054 adjacent same-tool failures only 416 (20.3%) repeat BYTE-IDENTICAL
  arguments, so four shut-offs in five landed on an agent that was adapting —
  and it lost its ENTIRE tool belt for it, because the guard set
  ``config.tools = []`` / ``custom_tools = []``;
* the four ceilings were module constants with no row, no org scope and no
  admin edit, and the one production caller passed no override.

These drive the REAL functions the orchestrator calls — the real threshold
loader through the real injected seam, the real tool chooser, the real
config mutation, the real verdict reader, the real branch — not a re-statement
of them. Each one fails if the corresponding behaviour is reverted.

Run with:
  uv run pytest packages/matrx-ai/tests/test_loop_guard_one_tool_and_settings.py -v
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai import _ext
from matrx_ai.orchestrator.executor import _tool_call_details_from_content
from matrx_ai.orchestrator.loop_guard import (
    LOOP_GUARD_KNOB_FEATURE,
    LOOP_GUARD_KNOB_KEYS,
    STANDOFF_MANDATE_KEY,
    LoopGuardThresholds,
    build_standoff_provision,
    decide_tool_standoff,
    disable_failing_tool,
    disabled_tool_notice,
    evaluate_loop_health,
    failing_tool_from_history,
    load_loop_guard_thresholds,
    standoff_branch,
    verdict_from_mandate_output,
)
from matrx_ai.orchestrator.tracking import ToolCallUsage


class _InlineTool:
    """Duck-typed CustomTool — the guard only ever reads ``.name``."""

    def __init__(self, name: str) -> None:
        self.name = name


def _config(tools: list[str], custom: list[str] | None = None) -> SimpleNamespace:
    return SimpleNamespace(
        tools=list(tools),
        custom_tools=[_InlineTool(n) for n in (custom or [])],
        model_id="gpt-5",
    )


def _history(pattern: list[tuple[str, bool]]) -> list[ToolCallUsage]:
    """One usage row per call, in order, in the live detail shape."""
    return [
        ToolCallUsage(
            iteration=i,
            tool_calls_count=1,
            tool_calls_details=[
                {
                    "name": name,
                    "id": f"call_{i}",
                    "call_id": f"call_{i}",
                    "success": ok,
                    **(
                        {}
                        if ok
                        else {
                            "arguments": {"id": f"arg-{i}"},
                            "agent_error": "boom",
                            "error": {"message": "boom", "error_type": "validation"},
                        }
                    ),
                }
            ],
        )
        for i, (name, ok) in enumerate(pattern, start=1)
    ]


def _warnings(caplog) -> str:
    """Everything the guard announced. vcprint routes through logging, so a
    warning that reaches nobody fails these tests."""
    return "\n".join(record.getMessage() for record in caplog.records)


@pytest.fixture(autouse=True)
def _capture_warnings(caplog):
    caplog.set_level("WARNING")


@pytest.fixture(autouse=True)
def _clean_seams():
    """Every test owns the injected seams; none leaks into the next."""
    saved = dict(_ext._registry)
    _ext._registry.pop("loop_guard_threshold_reader", None)
    _ext._registry.pop("tool_failure_standoff_decider", None)
    yield
    _ext._registry.clear()
    _ext._registry.update(saved)


# ── (a) ONLY the failing tool is removed ─────────────────────────────────────


def test_only_the_failing_tool_is_removed_and_the_run_keeps_the_rest():
    """The 2026-09-20 defect verbatim: 8 failures on one tool used to empty
    ``config.tools`` AND ``config.custom_tools``."""
    history = _history([("dataset", False)] * 8 + [("search", True)] * 0)
    config = _config(["dataset", "search", "memory"], custom=["browser_dom"])

    failing = failing_tool_from_history(history, window_size=20)
    assert failing == "dataset"

    outcome = disable_failing_tool(config, failing)

    assert outcome.removed is True
    assert outcome.was_only_tool is False
    # THE ASSERTION THE OLD CODE FAILS: everything else is still callable.
    assert config.tools == ["search", "memory"]
    assert [t.name for t in config.custom_tools] == ["browser_dom"]
    assert set(outcome.remaining_tools) == {"search", "memory", "browser_dom"}


def test_an_inline_custom_tool_is_removed_by_name_and_only_it():
    config = _config(["search"], custom=["browser_dom", "screenshot"])
    outcome = disable_failing_tool(config, "browser_dom")
    assert outcome.removed is True
    assert config.tools == ["search"]
    assert [t.name for t in config.custom_tools] == ["screenshot"]


def test_the_only_tool_is_still_a_pause_not_a_toolless_pretence():
    """When the failing tool WAS the whole belt there is no 'carry on with the
    rest' — the caller must keep the pause-for-a-human path."""
    outcome = disable_failing_tool(_config(["dataset"]), "dataset")
    assert outcome.removed is True
    assert outcome.was_only_tool is True
    assert outcome.remaining_tools == ()


def test_an_already_disabled_tool_is_never_blamed_twice():
    """Its failures stay in the window; re-choosing it would trip forever."""
    history = _history([("dataset", False)] * 8)
    assert failing_tool_from_history(history, window_size=20, exclude=("dataset",)) is None


def test_the_assistant_is_told_which_tool_left_and_why():
    """A control that vanished without a word is the dead screen the platform
    forbids."""
    outcome = disable_failing_tool(_config(["dataset", "search"]), "dataset")
    note = disabled_tool_notice(outcome, reason="it failed 8 time(s) in this run")
    assert "dataset" in note
    assert "search" in note
    assert "failed 8" in note


# ── (b) the setting rows are read ────────────────────────────────────────────


@pytest.mark.asyncio
async def test_thresholds_come_from_the_settings_door_and_govern_the_verdict():
    """An org that raises its ceiling to 12 must not be judged at 8."""
    seen: dict[str, object] = {}

    async def reader(*, organization_id, user_id):
        seen["organization_id"] = organization_id
        seen["user_id"] = user_id
        return {
            "window_size": 20,
            "min_calls_before_check": 8,
            "failure_threshold": 12,
            "recovery_window": 0,
            "standoff_decision_confidence": 0.9,
        }

    _ext.configure_ext(loop_guard_threshold_reader=reader)
    limits = await load_loop_guard_thresholds(organization_id="org-1", user_id="u-1")

    assert seen == {"organization_id": "org-1", "user_id": "u-1"}
    assert limits.source == "knobs"
    assert limits.failure_threshold == 12
    assert limits.standoff_decision_confidence == 0.9

    # 10 failures: stuck at the package default of 8, healthy at the org's 12.
    history = _history([("dataset", False)] * 10)
    assert evaluate_loop_health(history).verdict == "stuck"
    assert evaluate_loop_health(history, thresholds=limits).verdict == "healthy"


@pytest.mark.asyncio
async def test_a_key_the_door_omits_keeps_its_declared_default():
    async def reader(*, organization_id, user_id):
        return {"failure_threshold": 3}

    _ext.configure_ext(loop_guard_threshold_reader=reader)
    limits = await load_loop_guard_thresholds(organization_id="org-1")
    assert limits.failure_threshold == 3
    assert limits.window_size == LoopGuardThresholds().window_size


@pytest.mark.asyncio
async def test_a_failing_settings_door_never_breaks_the_run(caplog):
    async def reader(*, organization_id, user_id):
        raise RuntimeError("pool exhausted")

    _ext.configure_ext(loop_guard_threshold_reader=reader)
    limits = await load_loop_guard_thresholds(organization_id="org-1")

    assert limits == LoopGuardThresholds()
    assert LOOP_GUARD_KNOB_FEATURE in _warnings(caplog)


def test_every_threshold_field_is_a_settings_key():
    """A field added here without a row would be a constant in a new coat."""
    assert set(LOOP_GUARD_KNOB_KEYS) == {
        f for f in LoopGuardThresholds().__dataclass_fields__ if f != "source"
    }


# ── (c) no Holder → the fallback, and it says so ─────────────────────────────


@pytest.mark.asyncio
async def test_no_holder_bound_falls_back_to_disabling_only_this_tool(caplog):
    async def decider(provision):
        return None  # exactly what the host returns for an unfulfilled mandate

    _ext.configure_ext(tool_failure_standoff_decider=decider)
    verdict = await decide_tool_standoff({"tool_name": "dataset"})

    assert verdict.action == "disable_this_tool"
    assert verdict.source == "fallback"
    out = _warnings(caplog)
    assert STANDOFF_MANDATE_KEY in out
    assert "dataset" in out


@pytest.mark.asyncio
async def test_no_decider_wired_at_all_also_falls_back_out_loud(caplog):
    verdict = await decide_tool_standoff({"tool_name": "memory"})
    assert verdict.action == "disable_this_tool"
    assert verdict.source == "fallback"
    assert STANDOFF_MANDATE_KEY in _warnings(caplog)


@pytest.mark.asyncio
async def test_a_decider_that_raises_falls_back_rather_than_killing_the_run(caplog):
    async def decider(provision):
        raise RuntimeError("model unavailable")

    _ext.configure_ext(tool_failure_standoff_decider=decider)
    verdict = await decide_tool_standoff({"tool_name": "dataset"})
    assert verdict.source == "fallback"
    assert STANDOFF_MANDATE_KEY in _warnings(caplog)


# ── (d) a bound Holder drives the branch ─────────────────────────────────────


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("action", "expected_branch"),
    [
        ("disable_this_tool", "disable_tool"),
        ("continue", "continue_with_note"),
        ("continue_with_hint", "continue_with_note"),
        ("stop_the_run", "pause_for_human"),
    ],
)
async def test_a_stubbed_holder_drives_the_branch_the_orchestrator_takes(action, expected_branch):
    async def decider(provision):
        return {
            "action": {"value": action, "probability": 0.95},
            "hint": "pass the rulebook UUID, not its slug",
        }

    _ext.configure_ext(tool_failure_standoff_decider=decider)
    verdict = await decide_tool_standoff({"tool_name": "rulebook"})

    assert verdict.source == "mandate"
    assert verdict.action == action
    assert standoff_branch(verdict.action, already_continued=False) == expected_branch


def test_the_second_keep_going_in_one_run_disables_instead():
    assert standoff_branch("continue", already_continued=True) == "disable_tool"


@pytest.mark.asyncio
async def test_an_under_confident_verdict_falls_back_rather_than_letting_it_run(caplog):
    async def decider(provision):
        return {"action": {"value": "continue", "probability": 0.4}}

    _ext.configure_ext(tool_failure_standoff_decider=decider)
    verdict = await decide_tool_standoff(
        {"tool_name": "dataset"},
        thresholds=LoopGuardThresholds(standoff_decision_confidence=0.7),
    )
    assert verdict.action == "disable_this_tool"
    assert verdict.source == "fallback"
    assert STANDOFF_MANDATE_KEY in _warnings(caplog)


def test_an_action_outside_the_declared_set_is_not_acted_on():
    assert verdict_from_mandate_output({"action": "delete_everything"}) is None


def test_a_hintless_continue_with_hint_is_not_an_intervention():
    """Injecting an empty hint would be a silent no-op dressed as an action."""
    assert verdict_from_mandate_output({"action": "continue_with_hint", "hint": "  "}) is None


# ── (e) the arguments the verdict needs actually reach it ────────────────────


def test_a_failed_platform_tool_call_carries_its_arguments_into_the_provision():
    """The guard's persisted evidence blob deliberately carries no arguments, so
    a verdict built from it could never answer 'are these the same call again?'.
    This drives the REAL detail builder the executor uses and then the REAL
    provision builder, and asserts the arguments and the error class survive.
    """
    content_results = [
        {
            "call_id": "c1",
            "name": "rulebook",
            "is_error": True,
            "content": 'invalid input syntax for type uuid: "org-newsroom"',
            "error": {"message": "invalid uuid", "error_type": "validation"},
        }
    ]
    raw_calls = [
        {"call_id": "c1", "name": "rulebook", "arguments": {"rulebook_id": "org-newsroom"}}
    ]
    details = _tool_call_details_from_content(content_results, raw_calls=raw_calls)
    assert details[0]["arguments"] == {"rulebook_id": "org-newsroom"}

    history = [ToolCallUsage(iteration=1, tool_calls_count=1, tool_calls_details=details)]
    health = evaluate_loop_health(history)
    provision = build_standoff_provision(
        history, tool_name="rulebook", health=health, config=_config(["rulebook", "search"])
    )

    assert provision["recent_calls_json"][0]["arguments"] == {"rulebook_id": "org-newsroom"}
    assert "org-newsroom" in provision["recent_calls_text"]
    assert provision["error_classes"] == ["validation"]
    assert provision["other_tools_available"] == ["search"]
    assert provision["failures_this_tool"] == 1


def test_identical_repeats_are_a_fact_not_an_impression():
    """20.3% of adjacent same-tool failures ARE byte-identical; the fingerprints
    let a verdict confirm that instead of eyeballing prose."""
    same = {
        "name": "dataset",
        "call_id": "c",
        "success": False,
        "arguments": {"id": "x"},
        "error": {"message": "no", "error_type": "not_found"},
    }
    history = [
        ToolCallUsage(iteration=1, tool_calls_count=2, tool_calls_details=[same, dict(same)])
    ]
    provision = build_standoff_provision(
        history, tool_name="dataset", health=evaluate_loop_health(history)
    )
    prints = provision["arguments_fingerprints"]
    assert len(prints) == 2
    assert prints[0] == prints[1]


def test_adapting_arguments_do_not_look_like_a_repeat():
    history = _history([("dataset", False), ("dataset", False)])
    provision = build_standoff_provision(
        history, tool_name="dataset", health=evaluate_loop_health(history)
    )
    prints = provision["arguments_fingerprints"]
    assert prints[0] != prints[1]
