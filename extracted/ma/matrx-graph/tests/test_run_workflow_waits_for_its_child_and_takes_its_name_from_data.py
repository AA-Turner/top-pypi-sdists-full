"""Run Workflow waits for the workflow it called, and can take that workflow's name from data.

Two gaps found building the research topic pass (2026-11-10):

1. The step sat under the ten-minute limit every single step gets
   (``workflow.step_clock.default_step_seconds``), so no called workflow could run longer than
   that: the pass's ``read`` step was cut off at 600 s while its child was working. The called
   workflow's own steps each run under their own limit; the calling step only waits. Its limit
   is now the longest the engine allows, and an author sets a shorter one on the step.

2. The step could only name its workflow in its settings, so a pass could not walk a table of
   step names. ``workflow_key_input`` names one of the step's inputs as the carrier of the name;
   the call then resolves exactly like a fixed name (the host decides: a workflow the caller may
   run, its latest published version, or a refusal).
"""

from __future__ import annotations

import asyncio

import pytest
from pydantic import ValidationError

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph import knobs as graph_knobs
from matrx_graph.nodes.subgraph.call import (
    SubgraphCallConfig,
    SubgraphCallExecutor,
    SubgraphCallInput,
    SubgraphCallRefused,
    SubgraphTarget,
    named_call,
    set_subgraph_resolver,
    set_subgraph_target_resolver,
)
from matrx_graph.types.result import Failure, Success
from tests._fixtures import FakeEmitter, make_app_context

#: The names a data-named step in these tests is allowed to run (``allowed_workflow_keys``).
ALLOWED = ["research.journey.read", "platform:research.journey.score", "someone.elses"]


@pytest.fixture(autouse=True)
def _clean():
    set_subgraph_resolver(None)
    set_subgraph_target_resolver(None)
    graph_knobs.clear_knob_cache()
    yield
    set_subgraph_resolver(None)
    set_subgraph_target_resolver(None)
    graph_knobs.clear_knob_cache()


# ── the time limit ─────────────────────────────────────────────────────────


def _pin_every_steps_limit(monkeypatch: pytest.MonkeyPatch, seconds: int) -> None:
    async def _values(feature: str):
        if feature == graph_knobs.STEP_CLOCK_FEATURE:
            return {graph_knobs.DEFAULT_STEP_SECONDS_KEY: seconds}
        return None

    monkeypatch.setattr(graph_knobs, "_feature_values", _values)
    monkeypatch.setattr(graph_knobs, "MIN_STEP_SECONDS", 1)


def _calling(data: dict | None = None) -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "read",
                    "type": "subgraph.call",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"workflow_key": "research.journey.read"}, **(data or {})},
                }
            ],
            "edges": [],
        }
    )


async def _run(definition: Definition) -> tuple[object, FakeEmitter]:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    graph = compile_graph(definition, registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    return await asyncio.wait_for(scheduler.run(run_id="pass"), timeout=30), emitter


def _failures(emitter: FakeEmitter) -> list[dict]:
    return [e for k, e in emitter.events if k == "data" and isinstance(e, dict) and e.get("event") == "node_failed"]


async def test_a_called_workflow_may_run_longer_than_the_limit_every_step_gets(monkeypatch):
    _pin_every_steps_limit(monkeypatch, 1)

    async def _child(_ctx, _config, _inputs):
        await asyncio.sleep(2.5)  # the called workflow is still working past the caller's 1 s
        return {"run_id": "child-1", "last_outputs": {"done": {"read": 163}}, "channel_values": {}}

    set_subgraph_resolver(_child)
    result, emitter = await _run(_calling())
    assert _failures(emitter) == []
    assert result.status is RunStatus.COMPLETED


async def test_a_time_limit_set_on_the_step_still_stops_it(monkeypatch):
    _pin_every_steps_limit(monkeypatch, 600)
    cancelled = asyncio.Event()

    async def _child(_ctx, _config, _inputs):
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            cancelled.set()
            raise

    set_subgraph_resolver(_child)
    result, emitter = await _run(_calling({"step_clock": {"seconds": 5}}))
    assert result.status is RunStatus.ERRORED
    failed = _failures(emitter)
    assert len(failed) == 1 and failed[0]["error_type"] == "NodeTimeoutError"
    assert "time limit its author set" in failed[0]["error_message"]
    assert cancelled.is_set()


def test_the_steps_own_limit_is_the_longest_the_engine_allows():
    assert SubgraphCallExecutor.spec.timeout_ms == graph_knobs.MAX_STEP_SECONDS * 1000


# ── the name from data ─────────────────────────────────────────────────────


def test_a_step_names_its_workflow_fixed_or_from_an_input_never_both():
    assert SubgraphCallConfig(workflow_key_input="step", allowed_workflow_keys=ALLOWED).workflow_key_input == "step"
    with pytest.raises(ValidationError, match="not both"):
        SubgraphCallConfig(workflow_key_input="step", allowed_workflow_keys=ALLOWED, workflow_key="research.journey.read")
    with pytest.raises(ValidationError, match="not both"):
        SubgraphCallConfig(workflow_key_input="step", allowed_workflow_keys=ALLOWED, definition_id="d-1")
    with pytest.raises(ValidationError, match="latest published version"):
        SubgraphCallConfig(workflow_key_input="step", allowed_workflow_keys=ALLOWED, version_number=3)
    with pytest.raises(ValidationError, match="cannot be 'inputs'"):
        SubgraphCallConfig(workflow_key_input="inputs", allowed_workflow_keys=ALLOWED)
    with pytest.raises(ValidationError, match="Choose the workflow"):
        SubgraphCallConfig(workflow_key_input="  ")


def test_a_data_named_step_must_list_the_workflows_it_may_run():
    with pytest.raises(ValidationError, match="allowed_workflow_keys"):
        SubgraphCallConfig(workflow_key_input="step")
    with pytest.raises(ValidationError, match="set workflow_key_input too"):
        SubgraphCallConfig(workflow_key="research.journey.read", allowed_workflow_keys=["research.journey.read"])
    # Both spellings of a name mean the same workflow.
    config = SubgraphCallConfig(workflow_key_input="step", allowed_workflow_keys=ALLOWED)
    assert config.allowed_workflow_keys == ["research.journey.read", "research.journey.score", "someone.elses"]


@pytest.mark.parametrize("name", ["research.journey.delete_everything", "platform:research.journey.purge"])
async def test_a_data_named_workflow_outside_the_list_is_refused_and_starts_nothing(name):
    started: list[object] = []

    async def _resolver(_ctx, config, _inputs):
        started.append(config)
        return {"run_id": "child-1"}

    set_subgraph_resolver(_resolver)
    result = await SubgraphCallExecutor().execute(
        None, SubgraphCallInput(step=name), SubgraphCallConfig(workflow_key_input="step", allowed_workflow_keys=ALLOWED)
    )
    assert isinstance(result, Failure)
    assert result.error.code == "workflow_name_not_allowed"
    assert name.removeprefix("platform:") in result.error.message
    assert started == []


async def test_a_listed_name_written_as_its_tag_is_allowed():
    seen: dict = {}

    async def _resolver(_ctx, config, _inputs):
        seen["key"] = config.workflow_key
        return {"run_id": "child-1", "last_outputs": {}, "channel_values": {}}

    set_subgraph_resolver(_resolver)
    result = await SubgraphCallExecutor().execute(
        None, SubgraphCallInput(step="research.journey.score"),
        SubgraphCallConfig(workflow_key_input="step", allowed_workflow_keys=ALLOWED),
    )
    assert isinstance(result, Success) and seen["key"] == "research.journey.score"


async def test_the_named_workflow_runs_and_the_outcome_says_which_one_ran():
    seen: dict = {}

    async def _resolver(_ctx, config, inputs):
        seen["config"], seen["child_inputs"] = config, inputs.child_inputs
        return {
            "run_id": "child-1",
            "definition_id": "def-read",
            "version_number": 4,
            "last_outputs": {},
            "channel_values": {},
        }

    set_subgraph_resolver(_resolver)
    result = await SubgraphCallExecutor().execute(
        None,
        SubgraphCallInput(step="platform:research.journey.read", topic_id="t-1", inputs={"limit": 5}),
        SubgraphCallConfig(workflow_key_input="step", allowed_workflow_keys=ALLOWED, max_steps=900),
    )
    assert isinstance(result, Success)
    # The host resolves it exactly as a fixed name: by key, latest published version, same cap.
    assert seen["config"].workflow_key == "research.journey.read"
    assert seen["config"].workflow_key_input is None and seen["config"].definition_id is None
    assert seen["config"].version_number is None and seen["config"].max_steps == 900
    # The name is not one of the called workflow's inputs; everything else still is.
    assert seen["child_inputs"] == {"topic_id": "t-1", "limit": 5}
    assert (result.result.definition_id, result.result.version_number) == ("def-read", 4)


@pytest.mark.parametrize("given", [{}, {"step": ""}, {"step": "   "}, {"step": None}, {"step": 7}, {"step": ["a"]}])
async def test_a_missing_or_malformed_name_fails_the_step_and_starts_nothing(given):
    started: list[object] = []

    async def _resolver(_ctx, config, _inputs):
        started.append(config)
        return {"run_id": "child-1"}

    set_subgraph_resolver(_resolver)
    result = await SubgraphCallExecutor().execute(
        None, SubgraphCallInput(**given), SubgraphCallConfig(workflow_key_input="step", allowed_workflow_keys=ALLOWED)
    )
    assert isinstance(result, Failure)
    assert result.error.code == "workflow_name_missing"
    assert "'step'" in result.error.message
    assert started == []


async def test_a_name_the_caller_may_not_run_is_the_hosts_refusal_word_for_word():
    async def _resolver(_ctx, config, _inputs):
        raise SubgraphCallRefused(
            "subgraph_not_found",
            f"No workflow named '{config.workflow_key}' that you can use exists.",
            {"workflow_key": config.workflow_key},
        )

    set_subgraph_resolver(_resolver)
    result = await SubgraphCallExecutor().execute(
        None, SubgraphCallInput(step="someone.elses"), SubgraphCallConfig(workflow_key_input="step", allowed_workflow_keys=ALLOWED)
    )
    assert isinstance(result, Failure)
    assert result.error.code == "subgraph_not_found"
    assert "someone.elses" in result.error.message


async def test_a_saved_result_is_reused_only_for_the_same_named_workflow_version():
    async def _target(_ctx, config):
        return SubgraphTarget(
            definition_id=f"def-{config.workflow_key}", name=config.workflow_key, version_number=2
        )

    set_subgraph_target_resolver(_target)
    executor = SubgraphCallExecutor()
    config = SubgraphCallConfig(workflow_key_input="step", allowed_workflow_keys=ALLOWED)
    read = await executor.result_version(None, SubgraphCallInput(step="research.journey.read"), config)
    score = await executor.result_version(None, SubgraphCallInput(step="research.journey.score"), config)
    assert read and score and read != score


def test_a_fixed_call_is_left_exactly_as_it_is():
    config = SubgraphCallConfig(workflow_key="research.journey.read")
    inputs = SubgraphCallInput(step="not a name here", topic_id="t-1")
    assert named_call(config, inputs) == (config, inputs)
    assert inputs.child_inputs == {"step": "not a name here", "topic_id": "t-1"}
