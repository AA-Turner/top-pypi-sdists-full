"""A DELIVERY NEVER PRESENTS A HOLLOW SHELL AS A FINISHED ANSWER.

WALL W59 (Expert Book Challenge, 2026-09-12). Production run
``9347de24-efcf-4a4f-876a-b00aa4e13f34``, node ``deliver``
(``output.to_frontend``, presentation ``showcase``) emitted exactly this to a
parent::

    {"the_regimen": {"instructions": [], "headline_finding": "", …},
     "watsons_words": "Your boy of two and a half is not obstinate…"}

A full letter on one side, an empty-but-schema-valid regimen on the other, and
the screen said nothing about the difference. Now the emission ARRIVES NAMED:
``empty_values`` lists the hollow keys and ``empty_notice`` is the sentence a
presenter shows instead of rendering a blank panel as a completed result.

Forcing, not decorative: the payload is the REAL one
(``tests/fixtures/w59_empty_prescriber_output.json``, read from the production
database), it runs through the REAL engine — compile, Scheduler, the real
``output.to_frontend`` executor, the real emitter — and the assertions read the
event bytes the frontend receives. Delete the ``_empty_verdict`` call in
``nodes/output/to_frontend.py`` and ``test_the_hollow_regimen_is_named`` goes
red on the shipped payload.

Run with:  uv run pytest packages/matrx-graph/tests/test_empty_deliverable_is_named.py -v
"""

from __future__ import annotations

import json
from pathlib import Path

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.emptiness import empty_structured_output, is_zero_value, zero_valued_keys

from tests._fixtures import FakeEmitter, make_app_context

FIXTURE = json.loads((Path(__file__).parent / "fixtures" / "w59_empty_prescriber_output.json").read_text())
DELIVER_PAYLOAD = FIXTURE["deliver_payload"]
EMPTY_REGIMEN = FIXTURE["structured_output"]


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


def _data_events(emitter: FakeEmitter) -> list[dict]:
    return [p for k, p in emitter.events if k == "data" and isinstance(p, dict)]


async def _emit(payload: dict, *, run_id: str) -> dict:
    """Run the REAL deliver step on ``payload`` and return its node_emitted event."""
    registry = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "deliver",
                    "type": "output.to_frontend",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {
                            "mode": "full",
                            "title": "Watson's answer",
                            "presentation": "showcase",
                        }
                    },
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(definition, registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    result = await scheduler.run(run_id=run_id, node_inputs={"deliver": payload})
    assert result.status is RunStatus.COMPLETED
    emitted = [e for e in _data_events(emitter) if e.get("event") == "node_emitted"]
    assert len(emitted) == 1
    return emitted[0]


async def test_the_hollow_regimen_is_named():
    """The exact payload run 9347de24 presented to a parent."""
    event = await _emit(DELIVER_PAYLOAD, run_id="w59-real")

    assert event["empty_values"] == ["the_regimen"], (
        "the empty half of the deliverable was presented unmarked again"
    )
    notice = event["empty_notice"]
    assert notice and "the_regimen" in notice
    assert "not as a completed answer" in notice
    # The letter is untouched: this names what is hollow, it never censors.
    assert event["payload"]["watsons_words"].startswith("Your boy of two and a half")


async def test_a_full_deliverable_is_not_marked():
    """Nothing changes for an answer that carries something."""
    full = {
        "the_regimen": dict(EMPTY_REGIMEN, headline_finding="The handling built the rage."),
        "watsons_words": DELIVER_PAYLOAD["watsons_words"],
    }
    event = await _emit(full, run_id="w59-full")

    assert event["empty_values"] == []
    assert event["empty_notice"] is None


async def test_the_emission_still_ships_when_everything_is_empty():
    """An emit is never load-bearing — a wholly empty payload is still SHOWN,
    and still says what it is."""
    event = await _emit({"the_regimen": EMPTY_REGIMEN}, run_id="w59-all-empty")

    assert event["payload"] == {"the_regimen": EMPTY_REGIMEN}
    assert event["empty_values"] == ["the_regimen"]
    assert event["empty_notice"]


# ── The primitive itself ────────────────────────────────────────────────────


def test_zero_values_are_the_values_nothing_was_said_with():
    for value in (None, "", "   ", [], {}, False, 0, 0.0):
        assert is_zero_value(value), value
    for value in ("x", [0], {"a": 1}, True, 1, -1):
        assert not is_zero_value(value), value


def test_the_required_list_decides_which_fields_are_judged():
    schema = {"type": "object", "required": ["headline_finding", "instructions"]}
    # An optional field carrying something does NOT rescue an empty promise.
    payload = dict(EMPTY_REGIMEN, an_optional_note="see the letter")
    verdict = empty_structured_output(payload, schema=schema)
    assert verdict is not None
    assert verdict.fields == ("headline_finding", "instructions")
    assert verdict.considered == "required"
    assert "nothing to deliver" in verdict.sentence(what="the_regimen")


def test_the_three_wire_shapes_of_a_declared_schema_all_read():
    bare = {"type": "object", "required": ["headline_finding"]}
    envelope = {"name": "the_regimen", "schema": bare}
    response_format = {"type": "json_schema", "json_schema": envelope}
    for schema in (bare, envelope, response_format):
        assert empty_structured_output(EMPTY_REGIMEN, schema=schema) is not None


def test_the_marker_is_identity_not_content():
    assert empty_structured_output({"__kind": "regimen"}) is None, (
        "an object with only its marker has nothing to judge — never a verdict"
    )
    assert empty_structured_output({"__kind": "regimen", "items": []}) is not None
    assert zero_valued_keys({"__kind": "deliverable", "a": {"x": ""}}) == ("a",)


def test_a_scalar_is_never_judged():
    for value in ("", None, 0, False, "text"):
        assert empty_structured_output(value) is None
