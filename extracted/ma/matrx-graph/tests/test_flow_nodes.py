"""Tests for the flow pack: noop, sleep, wait_until, throttle.

The durability proof for ``flow.sleep`` is the scheduler-level restart: the
run parks INTERRUPTED with the sleep marker, the FIRST Scheduler instance is
thrown away entirely (the 'worker died' simulation — nothing survives in
memory), and a brand-new Scheduler resumes from the durable checkpoint with
the marker's ``resume_output`` as the wake's resume value. The payload must
arrive downstream exactly once, byte-identical.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.nodes.flow.sleep import SLEEP_MARKER
from matrx_graph.workers.sleep_wake import sleep_marker_of

from tests._fixtures import make_app_context


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


def _single_node(node_type: str, config: dict | None = None) -> Definition:
    data: dict = {}
    if config is not None:
        data["config"] = config
    return Definition.model_validate(
        {
            "nodes": [
                {"id": "n", "type": node_type, "position": {"x": 0, "y": 0}, "data": data}
            ],
            "edges": [],
        }
    )


async def _run_single(node_type: str, inputs: dict, config: dict | None = None):
    registry = _registry()
    graph = compile_graph(_single_node(node_type, config), registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    return await scheduler.run(run_id=f"t-{node_type.replace('.', '-')}", inputs=inputs)


# ---------------------------------------------------------------------------
# flow.noop
# ---------------------------------------------------------------------------


async def test_noop_passes_payload_through_unchanged():
    payload = {"a": 1, "nested": {"b": [1, 2, 3]}, "s": "text"}
    result = await _run_single("flow.noop", payload, {"note": "just a junction"})
    assert result.status is RunStatus.COMPLETED
    out = result.last_outputs["n"]
    for key, value in payload.items():
        assert out[key] == value


# ---------------------------------------------------------------------------
# flow.sleep
# ---------------------------------------------------------------------------


async def test_sleep_short_duration_runs_inline():
    result = await _run_single("flow.sleep", {"x": 42}, {"duration_seconds": 0.01})
    assert result.status is RunStatus.COMPLETED
    assert result.last_outputs["n"]["x"] == 42


async def test_sleep_long_duration_parks_with_marker_and_survives_restart():
    registry = _registry()
    checkpointer = MemoryCheckpointer()
    defn = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "sleep",
                    "type": "flow.sleep",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"duration_seconds": 3600}},
                },
                {
                    "id": "after",
                    "type": "flow.noop",
                    "position": {"x": 1, "y": 0},
                    "data": {},
                },
            ],
            "edges": [{"id": "e1", "source": "sleep", "target": "after"}],
        }
    )
    graph = compile_graph(defn, registry=registry)
    payload = {"job": "weekly-report", "n": 7}

    scheduler = Scheduler(graph, checkpointer, make_app_context(), registry=registry)
    result = await scheduler.run(run_id="t-sleep-durable", inputs=payload)
    assert result.status is RunStatus.INTERRUPTED
    assert result.interrupt is not None
    interrupt_payload = result.interrupt["payload"]

    # The marker is the durable wake contract.
    marker = interrupt_payload[SLEEP_MARKER]
    wake_at = datetime.fromisoformat(marker["wake_at"])
    remaining = (wake_at - datetime.now(UTC)).total_seconds()
    assert 3500 < remaining <= 3600
    assert interrupt_payload["resume_output"]["job"] == "weekly-report"
    # sleep_marker_of accepts both the run-row envelope and the bare payload.
    assert sleep_marker_of({"node_id": "sleep", "payload": interrupt_payload}) == marker
    assert sleep_marker_of(interrupt_payload) == marker
    assert sleep_marker_of({"prompt": "not a sleep"}) is None

    # 'Worker restart': the first scheduler is gone; only the checkpointer's
    # durable state remains. A fresh Scheduler resumes at the wake.
    checkpoint = await checkpointer.latest_checkpoint("t-sleep-durable")
    assert checkpoint is not None and checkpoint.interrupt_payload is not None
    fresh = Scheduler(graph, checkpointer, make_app_context(), registry=registry)
    resumed = await fresh.resume(
        run_id="t-sleep-durable",
        checkpoint_id=checkpoint.checkpoint_id,
        resume_value=interrupt_payload["resume_output"],
    )
    assert resumed.status is RunStatus.COMPLETED
    # The payload flowed through the sleep and the downstream junction once,
    # byte-identical.
    assert resumed.last_outputs["after"]["job"] == "weekly-report"
    assert resumed.last_outputs["after"]["n"] == 7

    # Resuming the SAME checkpoint again replays idempotently from recorded
    # outcomes — the wake can never double the payload.
    replay = Scheduler(graph, checkpointer, make_app_context(), registry=registry)
    replayed = await replay.resume(
        run_id="t-sleep-durable",
        checkpoint_id=checkpoint.checkpoint_id,
        resume_value=interrupt_payload["resume_output"],
    )
    assert replayed.status is RunStatus.COMPLETED
    assert replayed.last_outputs["after"]["n"] == 7


# ---------------------------------------------------------------------------
# flow.wait_until
# ---------------------------------------------------------------------------


async def test_wait_until_past_timestamp_passes_immediately():
    past = (datetime.now(UTC) - timedelta(hours=1)).isoformat()
    result = await _run_single("flow.wait_until", {"v": 1}, {"timestamp": past})
    assert result.status is RunStatus.COMPLETED
    assert result.last_outputs["n"]["v"] == 1


async def test_wait_until_z_suffix_parses():
    result = await _run_single(
        "flow.wait_until", {"v": 2}, {"timestamp": "2020-01-01T00:00:00Z"}
    )
    assert result.status is RunStatus.COMPLETED
    assert result.last_outputs["n"]["v"] == 2


async def test_wait_until_future_timestamp_parks_with_marker():
    future = (datetime.now(UTC) + timedelta(hours=2)).isoformat()
    result = await _run_single("flow.wait_until", {"v": 3}, {"timestamp": future})
    assert result.status is RunStatus.INTERRUPTED
    marker = result.interrupt["payload"][SLEEP_MARKER]
    assert marker["wake_at"] == datetime.fromisoformat(future).isoformat()


async def test_wait_until_interpolates_timestamp_from_inputs():
    future = (datetime.now(UTC) + timedelta(hours=3)).isoformat()
    result = await _run_single(
        "flow.wait_until", {"when": future}, {"timestamp": "{when}"}
    )
    assert result.status is RunStatus.INTERRUPTED
    assert result.interrupt["payload"][SLEEP_MARKER]["wake_at"] == future


async def test_wait_until_invalid_timestamp_is_a_node_failure():
    result = await _run_single("flow.wait_until", {}, {"timestamp": "next tuesday"})
    assert result.status is RunStatus.ERRORED


# ---------------------------------------------------------------------------
# flow.throttle
# ---------------------------------------------------------------------------


async def test_throttle_item_zero_passes_instantly():
    result = await _run_single("flow.throttle", {"x": 9}, {"interval_seconds": 60})
    assert result.status is RunStatus.COMPLETED
    assert result.last_outputs["n"]["x"] == 9


async def test_throttle_spaces_fanned_items():
    """control.map fans 3 items through the throttle; item i waits i×interval,
    so total step time ≥ 2×interval while every payload still arrives."""
    import time

    registry = _registry()
    defn = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "fan",
                    "type": "control.map",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"target_node_id": "throttle"}},
                },
                {
                    "id": "throttle",
                    "type": "flow.throttle",
                    "position": {"x": 1, "y": 0},
                    "data": {"config": {"interval_seconds": 0.05}},
                },
            ],
            "edges": [
                {
                    "id": "e1",
                    "source": "fan",
                    "target": "throttle",
                    "data": {"edge_kind": "control"},
                }
            ],
        }
    )
    graph = compile_graph(defn, registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    started = time.monotonic()
    result = await scheduler.run(run_id="t-throttle-fan", inputs={"items": [1, 2, 3]})
    elapsed = time.monotonic() - started
    assert result.status is RunStatus.COMPLETED
    assert elapsed >= 0.1  # item 2 waited 2 × 0.05s
