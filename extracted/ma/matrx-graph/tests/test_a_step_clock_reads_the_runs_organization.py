"""Guard (research gaps round 7, 2026-11-10): a step clock on a setting is read as the run's organization sees it.

The code path times each triage call on ``research.triage`` ``call_timeout_seconds`` read FOR THE ORGANIZATION
(``research/source_triage.py`` → ``scoped_knob_raw(feature, key, organization_id)``). The twin's judge step
declares ``data.step_clock`` on the same setting, but the engine read only the platform row, so an organization's
own value never reached the clock. Now the clock asks the host's setting reader for the run's organization (no
person's override, like the code) and falls back to the platform row only when that read gives nothing.

Real ``Scheduler`` over a step that takes longer than the platform value and less than the organization's.
"""

from __future__ import annotations

import asyncio
import dataclasses

import pytest

from matrx_graph import MemoryCheckpointer, RunStatus, Scheduler, compile_graph
from matrx_graph import knobs as graph_knobs
from matrx_graph import settings as graph_settings
from tests._fixtures import FakeEmitter, make_app_context
from tests.test_scheduler_step_wall_clock import SlowExecutor, _registry, _slow_definition

CLOCK = {
    "seconds": graph_knobs.MIN_STEP_SECONDS,
    "knob": {"feature": "research.triage", "key": "call_timeout_seconds"},
}
ORG = "11111111-2222-3333-4444-555555555555"


@pytest.fixture(autouse=True)
def platform_row_is_the_minimum(monkeypatch):
    async def _values(feature: str):
        if feature == "research.triage":
            return {"call_timeout_seconds": graph_knobs.MIN_STEP_SECONDS}
        return {graph_knobs.DEFAULT_STEP_SECONDS_KEY: graph_knobs.MIN_STEP_SECONDS}

    monkeypatch.setattr(graph_knobs, "_feature_values", _values)
    graph_knobs.clear_knob_cache()
    yield
    graph_settings.set_setting_reader(None)


async def _run(run_id: str, organization_id: str | None) -> RunStatus:
    registry = _registry(SlowExecutor())
    graph = compile_graph(_slow_definition(CLOCK), registry=registry)
    app = dataclasses.replace(make_app_context(FakeEmitter()), organization_id=organization_id)
    result = await asyncio.wait_for(
        Scheduler(graph, MemoryCheckpointer(), app, registry=registry).run(run_id=run_id), 30
    )
    return result.status


async def test_the_organizations_own_value_sets_the_clock():
    asked: list[tuple] = []

    async def reader(feature, key, organization_id, user_id):
        asked.append((feature, key, organization_id, user_id))
        return (20 if organization_id == ORG else graph_knobs.MIN_STEP_SECONDS), "organization"

    graph_settings.set_setting_reader(reader)
    assert await _run("org-clock", ORG) is RunStatus.COMPLETED
    assert (
        "research.triage",
        "call_timeout_seconds",
        ORG,
        None,
    ) in asked  # the organization's view, no person


async def test_without_an_organization_value_the_platform_row_decides():
    async def broken(feature, key, organization_id, user_id):
        raise RuntimeError("no settings store")

    graph_settings.set_setting_reader(broken)
    assert await _run("platform-clock", ORG) is RunStatus.ERRORED
    seconds, _ = await graph_knobs.step_timeout_seconds(
        None,
        node_clock=compile_graph(_slow_definition(CLOCK), registry=_registry(SlowExecutor()))
        .nodes["audio"]
        .step_clock,
        organization_id=None,
    )
    assert seconds == float(graph_knobs.MIN_STEP_SECONDS)
