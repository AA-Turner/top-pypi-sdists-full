"""A task that reports back to a parent agent must be told to create + start a
plan before any other tool call — otherwise the runtime rejects the first
non-plan tool call with a 400. The SDK surfaces this via the
``should_update_parent`` flag and injects mandatory deep-planning guidance when
plan tools are available.
"""

from __future__ import annotations

import inspect
from types import SimpleNamespace

import pytest

from xpander_sdk.modules.backend.frameworks.agno import (
    DEEP_PLANNING_INSTRUCTIONS,
    PARENT_UPDATE_PLAN_REQUIREMENT,
    SEEDED_PLAN_INSTRUCTIONS,
    _configure_deep_planning_guidance,
)
from xpander_sdk.models.configuration import Configuration
from xpander_sdk.modules.tasks.sub_modules.task import Task


def test_deep_planning_guidance_stays_async() -> None:
    """A sync reload() here re-enters the live loop and kills the worker."""
    assert inspect.iscoroutinefunction(_configure_deep_planning_guidance)


def _plan_tool():
    # Detection reads __name__ then .name; mimic an agno Function by name.
    return SimpleNamespace(name="xpcreate_agent_plan")


def _other_tool():
    return SimpleNamespace(name="xpsome-other-tool")


def _fake_task(must_deep_plan: bool):
    # deep_planning.enabled stays False so the enabled-gated branch (which calls
    # task.areload() over HTTP) is skipped - we only exercise the must_deep_plan path.
    return SimpleNamespace(
        should_update_parent=must_deep_plan,
        must_deep_plan=must_deep_plan,
        deep_planning=SimpleNamespace(enabled=False),
    )


def _fake_agent():
    return SimpleNamespace(deep_planning=False)


@pytest.mark.asyncio
async def test_parent_update_with_plan_tools_injects_requirement() -> None:
    args = {"instructions": "base", "tools": [_plan_tool(), _other_tool()]}
    await _configure_deep_planning_guidance(
        args=args, agent=_fake_agent(), task=_fake_task(True)
    )
    assert DEEP_PLANNING_INSTRUCTIONS in args["instructions"]
    assert PARENT_UPDATE_PLAN_REQUIREMENT in args["instructions"]


@pytest.mark.asyncio
async def test_no_parent_update_skips_requirement() -> None:
    args = {"instructions": "base", "tools": [_plan_tool()]}
    await _configure_deep_planning_guidance(
        args=args, agent=_fake_agent(), task=_fake_task(False)
    )
    assert PARENT_UPDATE_PLAN_REQUIREMENT not in args["instructions"]
    assert DEEP_PLANNING_INSTRUCTIONS not in args["instructions"]


@pytest.mark.asyncio
async def test_parent_update_without_plan_tools_skips_requirement() -> None:
    args = {"instructions": "base", "tools": [_other_tool()]}
    await _configure_deep_planning_guidance(
        args=args, agent=_fake_agent(), task=_fake_task(True)
    )
    assert PARENT_UPDATE_PLAN_REQUIREMENT not in args["instructions"]
    assert DEEP_PLANNING_INSTRUCTIONS not in args["instructions"]


def _dp_agent():
    return SimpleNamespace(deep_planning=True)


async def _noop_areload() -> None:
    return None


def _task_with_plan(*, started: bool, tasks):
    # areload() is stubbed so the enabled-gated branch doesn't hit HTTP.
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
        areload=_noop_areload,
    )


@pytest.mark.asyncio
async def test_started_seeded_plan_uses_seeded_instructions() -> None:
    args = {"instructions": "base", "tools": [_plan_tool()]}
    await _configure_deep_planning_guidance(
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


@pytest.mark.asyncio
async def test_enabled_unstarted_plan_uses_create_instructions() -> None:
    args = {"instructions": "base", "tools": [_plan_tool()]}
    await _configure_deep_planning_guidance(
        args=args,
        agent=_dp_agent(),
        task=_task_with_plan(started=False, tasks=[]),
    )
    assert DEEP_PLANNING_INSTRUCTIONS in args["instructions"]
    assert SEEDED_PLAN_INSTRUCTIONS not in args["instructions"]


def test_should_update_parent_round_trips_from_api_payload() -> None:
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


@pytest.mark.asyncio
async def test_plan_block_prepended_before_volatile_context() -> None:
    """Stable plan block must precede volatile task context in the cached region."""
    args = {
        "instructions": "base",
        "tools": [_plan_tool()],
        "additional_context": "compaction summary + ledger (volatile)",
    }
    await _configure_deep_planning_guidance(
        args=args,
        agent=_dp_agent(),
        task=_task_with_plan(
            started=True,
            tasks=[SimpleNamespace(id="step-1", title="Do work", completed=False)],
        ),
    )
    ctx = args["additional_context"]
    assert ctx.index("Execution plan steps") < ctx.index("volatile")


@pytest.mark.asyncio
async def test_plan_block_renders_when_seeded_but_agent_deep_planning_off() -> None:
    """SEEDED instructions reference the plan block, so it must render even when
    agent.deep_planning is falsy (must_plan gate) — the gates were asymmetric."""
    task = _task_with_plan(
        started=True,
        tasks=[SimpleNamespace(id="step-1", title="Do work", completed=False)],
    )
    task.must_deep_plan = True
    args = {"instructions": "base", "tools": [_plan_tool()]}
    await _configure_deep_planning_guidance(args=args, agent=_fake_agent(), task=task)
    assert SEEDED_PLAN_INSTRUCTIONS in args["instructions"]
    assert "Execution plan steps" in args.get("additional_context", "")


@pytest.mark.asyncio
async def test_empty_plan_renders_create_hint_not_live_status_label() -> None:
    """No tasks yet → no contradictory live-status label, just a create hint."""
    args = {"instructions": "base", "tools": [_plan_tool()]}
    await _configure_deep_planning_guidance(
        args=args,
        agent=_dp_agent(),
        task=_task_with_plan(started=False, tasks=[]),
    )
    ctx = args.get("additional_context", "")
    assert "No execution plan exists yet" in ctx
    assert "Execution plan steps" not in ctx


@pytest.mark.asyncio
async def test_plan_completion_flip_keeps_plan_block_stable() -> None:
    """The rendered block must not change when a step completes (cache stability)."""

    async def _ctx(completed: bool) -> str:
        args = {"instructions": "base", "tools": [_plan_tool()]}
        await _configure_deep_planning_guidance(
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

    assert await _ctx(False) == await _ctx(True)
