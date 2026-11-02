"""Adversarial probes — auto-mint removal residue (KINDS_EVERYWHERE_PLAN §10/§12).

AUTO-MINT IS DEAD (registry.py): an author's declaration is exactly what they
wrote, "None stays None (and settlement's runtime propagation reads the
payload's own __kind instead — the honest answer for pass-throughs)". The
scheduler's settlement comment (scheduler.py ~2245) names the pass-throughs
that primitive exists for: "data.transform, pipe.step, subgraph.call,
tool.call...".

BUT: ``data.transform`` and ``output.to_frontend`` still declare
``output_kind="json"`` in their NodeSpecs. Pre-removal, ``register()``
explicitly treated ``"json"`` as UNDECLARED and replaced it with a minted
fingerprint slug, so the spec never reached the scheduler carrying "json".
Post-removal, "json" survives as a REAL declaration, which means for the very
nodes the runtime-propagation comment names:

  1. runtime propagation NEVER runs (node.output_kind is not None), so a
     payload that says what it is gets its identity REPLACED by "json" in the
     outcome row / node_completed event, and is validated against "json"
     (the any-value schema) instead of its own registered kind; and
  2. settlement stamping writes ``__kind: "json"`` onto every bare-dict
     output — a FORMAT word (GENERIC_KINDS in matrx_ai.kinds) stamped as if
     it were a shape, which downstream kind_of()/propagation then treats as a
     self-description.

These tests state the honest behavior the removal's own comments promise and
are xfail(strict=True) while the residue stands. When someone strips the
``output_kind="json"`` declarations (or teaches settlement that a generic
format word is not a declaration), they flip to XPASS and the markers come off.
"""

from __future__ import annotations

import pytest

from matrx_graph import Definition, RunStatus

from tests.test_kinds import _events, _run_capture, _seed_kind

pytestmark = pytest.mark.asyncio


def _transform_definition(expression: str) -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "t1",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {"expression": expression},
                        "input": {"value": {"__kind": "test_flow_result", "result": "flowed"}},
                    },
                },
            ],
            "edges": [],
        }
    )


def _seed_generic_and_real_kinds() -> None:
    # Mirror the live registry: "json" is a registered generic ("any value")
    # kind; test_flow_result is a real structural kind.
    _seed_kind("json", {})
    _seed_kind(
        "test_flow_result",
        {
            "type": "object",
            "properties": {"result": {"type": "string"}},
            "required": ["result"],
        },
    )


# FIXED (round-1 triage, 2026-08-21): the finding this test pinned is
# closed; the test now guards the fix.
async def test_passthrough_payload_identity_survives_a_json_declared_node():
    """A self-described payload flowing through data.transform should settle
    under ITS OWN kind (scheduler comment: "output kind = the kind of what
    actually flowed"), not under the format word 'json'."""
    _seed_generic_and_real_kinds()
    result, checkpointer, emitter = await _run_capture(
        _transform_definition("inputs['value']"), "adv-json-1"
    )
    assert result.status is RunStatus.COMPLETED
    completed = _events(emitter, "node_completed")
    assert completed, "the transform must settle"
    assert completed[0]["output_kind"] == "test_flow_result"
    outcome = await checkpointer.get_outcome("adv-json-1", 0, "t1", 1)
    assert outcome is not None
    assert outcome.output_kind == "test_flow_result"


# FIXED (round-1 triage, 2026-08-21): the finding this test pinned is
# closed; the test now guards the fix.
async def test_bare_output_is_not_stamped_with_the_format_word_json():
    """A kind-less dict settling through a 'json'-declared node should stay
    kind-less ("a payload carrying no __kind changes nothing — the honest
    answer"), not get __kind='json' burned into it."""
    _seed_generic_and_real_kinds()
    result, _checkpointer, emitter = await _run_capture(
        _transform_definition("{'a': 1, 'b': 2}"), "adv-json-2"
    )
    assert result.status is RunStatus.COMPLETED
    completed = _events(emitter, "node_completed")
    assert completed, "the transform must settle"
    output = completed[0].get("output")
    assert isinstance(output, dict)
    assert "__kind" not in output, (
        f"format word stamped as a kind: __kind={output.get('__kind')!r}"
    )
