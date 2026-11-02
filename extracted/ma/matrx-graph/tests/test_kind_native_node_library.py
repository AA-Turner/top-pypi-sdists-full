"""The kind-native built-in library, proven on a REAL run — plan §10d-B2 + B3.

Not a model-construction test: this compiles a real graph, runs it through the
real scheduler, and reads what actually came out. Every assertion is about what
the ENGINE produced, so the test fails if any link in the chain (model → dump →
settlement → routing → last_outputs → event) stops carrying the identity.

  1. Several converted built-ins in one pipeline — each settled output SAYS
     what it is, at every hop, without settlement having to inject anything.
  2. A nested kind is self-describing INSIDE its parent (``aggregate_group``),
     which is what makes recursive rendering through the registry possible.
  3. One kind, one model: ``data.filter`` / ``data.dedupe`` / ``data.limit``
     all answer with the SAME class under the SAME slug — the second class is
     gone, so they cannot drift apart.
  4. A deliberate node failure puts ``node_error`` on the wire, nested in the
     ``node_outcome`` packet, alongside the successes.
"""

from __future__ import annotations

from typing import Any

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.content_ir.model import kind_of
from matrx_graph.nodes.data.collections import KeptListOutput
from matrx_graph.nodes.data.filter import FilterOutput
from matrx_graph.nodes.data.merge import MergeOutput
from matrx_graph.nodes.data.pick_omit import _PickOmitOutput
from matrx_graph.nodes.data.json_io import StringifyJsonOutput
from matrx_graph.nodes.text.manipulate import JoinOutput

from tests._fixtures import FakeEmitter, make_app_context


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


def _node(
    node_id: str,
    node_type: str,
    config: dict[str, Any] | None = None,
    inputs: dict[str, Any] | None = None,
) -> dict:
    # ``inputs`` DECLARES what the step needs (W68: a definition that saves is
    # a definition that can start). The runs below still deliver the values
    # through ``node_inputs``, which wins at merge time.
    return {
        "id": node_id,
        "type": node_type,
        "position": {"x": 0, "y": 0},
        "data": {"config": config or {}, **({"inputs": inputs} if inputs else {})},
    }


async def _run(definition: dict, run_id: str, node_inputs: dict[str, Any] | None = None):
    graph = compile_graph(Definition.model_validate(definition), registry=_registry())
    emitter = FakeEmitter()
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(emitter), registry=_registry()
    )
    result = await scheduler.run(run_id=run_id, node_inputs=node_inputs or {})
    return result, emitter


def _events(emitter: FakeEmitter, name: str) -> list[dict]:
    return [
        e
        for k, e in emitter.events
        if k == "data" and isinstance(e, dict) and e.get("event") == name
    ]


# ---------------------------------------------------------------------------
# 3 — one kind, one model (checked without running anything: it is a TYPE fact)
# ---------------------------------------------------------------------------


def test_shared_slugs_are_one_class_not_two():
    """The twin classes are GONE, not merely kept in sync.

    ``filter_result`` and ``record_result`` each had two node classes carrying
    one registered slug — which is how two nodes drift apart while both
    claiming to answer with the same kind. Identity, not equality, is the
    assertion: a copy can be edited apart again, an alias cannot.
    """
    assert KeptListOutput is FilterOutput
    assert _PickOmitOutput is MergeOutput
    assert FilterOutput.kind_slug == "filter_result"
    assert MergeOutput.kind_slug == "record_result"
    # …and the well-known ``text`` shape is ONE model for both producers.
    assert JoinOutput is StringifyJsonOutput
    assert JoinOutput.kind_slug == "text"


# ---------------------------------------------------------------------------
# 1 + 2 — a real multi-node run: every hop is self-describing
# ---------------------------------------------------------------------------


async def test_a_real_pipeline_settles_self_describing_payloads_at_every_hop():
    result, emitter = await _run(
        {
            "nodes": [
                _node(
                    "keep_big",
                    "data.filter",
                    {"predicate": "inputs['n'] > 1"},
                    inputs={"items": []},
                ),
                _node(
                    "totals",
                    "data.aggregate",
                    {"operation": "sum", "value_key": "n", "group_by": "team"},
                ),
                _node(
                    "stamp",
                    "crypto.hash",
                    {"algorithm": "sha256", "truncate": 12},
                    inputs={"text": ""},
                ),
            ],
            "edges": [
                {
                    "id": "e1",
                    "source": "keep_big",
                    "target": "totals",
                    "data": {"mappings": {"items": "items"}},
                },
            ],
        },
        "b2-pipeline",
        node_inputs={
            "keep_big": {
                "items": [
                    {"n": 1, "team": "red"},
                    {"n": 4, "team": "red"},
                    {"n": 7, "team": "blue"},
                ]
            },
            "stamp": {"text": "the-dedupe-key"},
        },
    )
    assert result.status is RunStatus.COMPLETED, result

    # Every settled output says what it is — read from the ENGINE's own
    # last_outputs, not from a model we constructed.
    assert kind_of(result.last_outputs["keep_big"]) == "filter_result"
    assert kind_of(result.last_outputs["totals"]) == "aggregate_result"
    assert kind_of(result.last_outputs["stamp"]) == "hash_result"

    # The data is still the data — identity was ADDED, nothing was displaced.
    assert result.last_outputs["keep_big"]["kept"] == 2
    assert result.last_outputs["keep_big"]["dropped"] == 1
    assert len(result.last_outputs["stamp"]["digest"]) == 12
    assert result.last_outputs["stamp"]["truncated_to"] == 12

    # THE NESTING (§4.4): the repeated group inside aggregate_result carries
    # its OWN identity, which is what lets a renderer recurse through the
    # registry instead of hand-rendering a child.
    groups = result.last_outputs["totals"]["groups"]
    assert groups, "the aggregate grouped by team, so it must report groups"
    assert all(kind_of(g) == "aggregate_group" for g in groups)
    assert {g["key"] for g in groups} == {"red", "blue"}

    # The same truth reaches the wire: node_completed carries it, and the
    # runtime wrapper names the kind it is carrying.
    completed = {e["node_id"]: e for e in _events(emitter, "node_completed")}
    assert kind_of(completed["totals"]["output"]) == "aggregate_result"
    assert completed["totals"]["wrapper"]["output_kind"] == "aggregate_result"


# ---------------------------------------------------------------------------
# 4 — a deliberate failure rides the same wire as the successes
# ---------------------------------------------------------------------------


async def test_a_deliberate_failure_puts_node_error_on_the_wire():
    """``data.assert`` with a predicate that does not hold — a real node
    failing for a real reason, beside a node that succeeded."""
    result, emitter = await _run(
        {
            "nodes": [
                _node("slugify", "text.slug", {}, inputs={"text": ""}),
                _node("gate", "data.assert", {"predicate": "inputs['n'] > 100"}),
            ],
            "edges": [],
        },
        "b2-failure",
        node_inputs={"slugify": {"text": "Hello, World!"}, "gate": {"n": 3}},
    )
    assert result.status is RunStatus.ERRORED  # no ERROR edge → the run parks

    # The success half still says what it is.
    assert kind_of(result.last_outputs["slugify"]) == "slug_result"
    assert result.last_outputs["slugify"]["slug"] == "hello-world"

    # …and so does the failure (§10d-B3), in the same packet shape.
    failed = _events(emitter, "node_failed")
    assert len(failed) == 1 and failed[0]["node_id"] == "gate"
    assert kind_of(failed[0]["error"]) == "node_error"
    assert failed[0]["error"]["code"]
    wrapper = failed[0]["wrapper"]
    assert kind_of(wrapper) == "node_outcome"
    assert wrapper["status"] == "failed"
    assert kind_of(wrapper["error"]) == "node_error"
