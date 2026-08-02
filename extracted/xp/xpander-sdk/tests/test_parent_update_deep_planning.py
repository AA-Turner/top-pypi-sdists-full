"""A task that reports back to a parent agent must be told to create + start a
plan before any other tool call — otherwise the runtime rejects the first
non-plan tool call with a 400. The SDK surfaces this via the
``should_update_parent`` flag and injects mandatory deep-planning guidance when
plan tools are available.
"""

from __future__ import annotations

from types import SimpleNamespace

from xpander_sdk.modules.backend.frameworks.agno import (
    DEEP_PLANNING_INSTRUCTIONS,
    PARENT_UPDATE_PLAN_REQUIREMENT,
    SEEDED_PLAN_INSTRUCTIONS,
    _configure_deep_planning_guidance,
)
from xpander_sdk.models.configuration import Configuration
from xpander_sdk.modules.tasks.sub_modules.task import Task


def _plan_tool():
    # Detection reads __name__ then .name; mimic an agno Function by name.
    return SimpleNamespace(name="xpcreate_agent_plan")


def _other_tool():
    return SimpleNamespace(name="xpsome-other-tool")


def _fake_task(must_deep_plan: bool):
    # deep_planning.enabled stays False so the enabled-gated branch (which calls
    # task.reload() over HTTP) is skipped — we only exercise the must_deep_plan path.
    return SimpleNamespace(
        should_update_parent=must_deep_plan,
        must_deep_plan=must_deep_plan,
        deep_planning=SimpleNamespace(enabled=False),
    )


def _fake_agent():
    return SimpleNamespace(deep_planning=False)


def test_parent_update_with_plan_tools_injects_requirement():
    args = {"instructions": "base", "tools": [_plan_tool(), _other_tool()]}
    _configure_deep_planning_guidance(
        args=args, agent=_fake_agent(), task=_fake_task(True)
    )
    assert DEEP_PLANNING_INSTRUCTIONS in args["instructions"]
    assert PARENT_UPDATE_PLAN_REQUIREMENT in args["instructions"]


def test_no_parent_update_skips_requirement():
    args = {"instructions": "base", "tools": [_plan_tool()]}
    _configure_deep_planning_guidance(
        args=args, agent=_fake_agent(), task=_fake_task(False)
    )
    assert PARENT_UPDATE_PLAN_REQUIREMENT not in args["instructions"]
    assert DEEP_PLANNING_INSTRUCTIONS not in args["instructions"]


def test_parent_update_without_plan_tools_skips_requirement():
    args = {"instructions": "base", "tools": [_other_tool()]}
    _configure_deep_planning_guidance(
        args=args, agent=_fake_agent(), task=_fake_task(True)
    )
    assert PARENT_UPDATE_PLAN_REQUIREMENT not in args["instructions"]
    assert DEEP_PLANNING_INSTRUCTIONS not in args["instructions"]


def _dp_agent():
    return SimpleNamespace(deep_planning=True)


def _task_with_plan(*, started: bool, tasks):
    # reload() is stubbed so the enabled-gated branch doesn't hit HTTP.
    dp = SimpleNamespace(
        enabled=True,
        started=started,
        tasks=tasks,
        model_dump_json=lambda: '{"tasks":[]}',
    )
    return SimpleNamespace(
        should_update_parent=False,
        must_deep_plan=False,
        deep_planning=dp,
        reload=lambda: None,
    )


def test_started_seeded_plan_uses_seeded_instructions():
    args = {"instructions": "base", "tools": [_plan_tool()]}
    _configure_deep_planning_guidance(
        args=args,
        agent=_dp_agent(),
        task=_task_with_plan(
            started=True,
            tasks=[SimpleNamespace(id="step-1", title="Do work", completed=False)],
        ),
    )
    # already started → execute/complete guidance, never the create-first guidance
    assert SEEDED_PLAN_INSTRUCTIONS in args["instructions"]
    assert DEEP_PLANNING_INSTRUCTIONS not in args["instructions"]
    assert "Execution plan steps" in args.get("additional_context", "")


def test_enabled_unstarted_plan_uses_create_instructions():
    args = {"instructions": "base", "tools": [_plan_tool()]}
    _configure_deep_planning_guidance(
        args=args,
        agent=_dp_agent(),
        task=_task_with_plan(started=False, tasks=[]),
    )
    assert DEEP_PLANNING_INSTRUCTIONS in args["instructions"]
    assert SEEDED_PLAN_INSTRUCTIONS not in args["instructions"]


def test_should_update_parent_round_trips_from_api_payload():
    task = Task.model_validate(
        {
            "id": "t1",
            "agent_id": "a1",
            "organization_id": "o1",
            "input": {"text": "hi"},
            "created_at": "2026-06-02T00:00:00Z",
            "should_update_parent": True,
            "configuration": Configuration(api_key="k", organization_id="o"),
        }
    )
    assert task.should_update_parent is True


def test_plan_block_prepended_before_volatile_context():
    """Stable plan block must precede volatile task context in the cached region."""
    args = {
        "instructions": "base",
        "tools": [_plan_tool()],
        "additional_context": "compaction summary + ledger (volatile)",
    }
    _configure_deep_planning_guidance(
        args=args,
        agent=_dp_agent(),
        task=_task_with_plan(
            started=True,
            tasks=[SimpleNamespace(id="step-1", title="Do work", completed=False)],
        ),
    )
    ctx = args["additional_context"]
    assert ctx.index("Execution plan steps") < ctx.index("volatile")


def test_plan_block_renders_when_seeded_but_agent_deep_planning_off():
    """SEEDED instructions reference the plan block, so it must render even when
    agent.deep_planning is falsy (must_plan gate) — the gates were asymmetric."""
    task = _task_with_plan(
        started=True,
        tasks=[SimpleNamespace(id="step-1", title="Do work", completed=False)],
    )
    task.must_deep_plan = True
    args = {"instructions": "base", "tools": [_plan_tool()]}
    _configure_deep_planning_guidance(args=args, agent=_fake_agent(), task=task)
    assert SEEDED_PLAN_INSTRUCTIONS in args["instructions"]
    assert "Execution plan steps" in args.get("additional_context", "")


def test_empty_plan_renders_create_hint_not_live_status_label():
    """No tasks yet → no contradictory live-status label, just a create hint."""
    args = {"instructions": "base", "tools": [_plan_tool()]}
    _configure_deep_planning_guidance(
        args=args,
        agent=_dp_agent(),
        task=_task_with_plan(started=False, tasks=[]),
    )
    ctx = args.get("additional_context", "")
    assert "No execution plan exists yet" in ctx
    assert "Execution plan steps" not in ctx


def test_plan_completion_flip_keeps_plan_block_stable():
    """The rendered block must not change when a step completes (cache stability)."""

    def _ctx(completed: bool) -> str:
        args = {"instructions": "base", "tools": [_plan_tool()]}
        _configure_deep_planning_guidance(
            args=args,
            agent=_dp_agent(),
            task=_task_with_plan(
                started=True,
                tasks=[
                    SimpleNamespace(id="step-1", title="Do work", completed=completed),
                    SimpleNamespace(id="step-2", title="More work", completed=False),
                ],
            ),
        )
        return args["additional_context"]

    assert _ctx(False) == _ctx(True)
