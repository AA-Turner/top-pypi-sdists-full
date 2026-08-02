"""Planning tools are hidden when deep planning isn't active for the task.

Inline agent-gateway children run with deep_planning.enabled=False and
must_deep_plan=False; the SDK must strip the planning tool family from the
agent's tool list so the downstream agent can't call it. When deep planning is
active (or the task must plan before reporting to a parent), the tools stay.
"""

from __future__ import annotations

from types import SimpleNamespace

from xpander_sdk.modules.backend.frameworks.agno import (
    _PLAN_TOOLS,
    _strip_planning_tools_if_inactive,
)


def _plan_tool(name="xpcreate_agent_plan"):
    # Detection reads __name__ then .name; mimic an agno Function by name.
    return SimpleNamespace(name=name)


def _other_tool():
    return SimpleNamespace(name="web_search")


def _agent(deep_planning=True):
    return SimpleNamespace(deep_planning=deep_planning)


def _task(*, enabled, must_deep_plan=False):
    return SimpleNamespace(
        deep_planning=SimpleNamespace(enabled=enabled),
        must_deep_plan=must_deep_plan,
    )


def _names(args):
    return {getattr(t, "__name__", getattr(t, "name", "")) for t in args["tools"]}


def test_strips_planning_family_when_inactive():
    args = {"tools": [_plan_tool(n) for n in _PLAN_TOOLS] + [_other_tool()]}
    _strip_planning_tools_if_inactive(
        args=args, agent=_agent(True), task=_task(enabled=False)
    )
    assert _names(args) == {"web_search"}


def test_keeps_planning_when_deep_planning_enabled():
    args = {"tools": [_plan_tool(), _other_tool()]}
    _strip_planning_tools_if_inactive(
        args=args, agent=_agent(True), task=_task(enabled=True)
    )
    assert "xpcreate_agent_plan" in _names(args)


def test_keeps_planning_when_must_deep_plan():
    # parent-reporting child: plan disabled but must plan before any tool call
    args = {"tools": [_plan_tool(), _other_tool()]}
    _strip_planning_tools_if_inactive(
        args=args, agent=_agent(True), task=_task(enabled=False, must_deep_plan=True)
    )
    assert "xpcreate_agent_plan" in _names(args)


def test_non_planning_tools_untouched_when_inactive():
    args = {"tools": [_other_tool()]}
    _strip_planning_tools_if_inactive(
        args=args, agent=_agent(True), task=_task(enabled=False)
    )
    assert _names(args) == {"web_search"}
