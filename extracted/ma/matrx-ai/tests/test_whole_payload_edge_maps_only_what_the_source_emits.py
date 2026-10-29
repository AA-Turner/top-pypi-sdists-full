"""A whole-payload edge into a converted mandate step maps only keys its source emits.

Live 2026-10-28, Agent Foundry v1 (051fb0aa) ``e_brief_mint``: ``provision_values: $FULL_PAYLOAD`` was
expanded into ALL 12 of the Holder's variables while the source (``kind_brief``) emits 3 — every run
failed with EdgeRoutingError and later saves were refused. Optional variables the source does not
provide stay unmapped (the agent's default); none is invented.
"""

from __future__ import annotations

from typing import Any

from matrx_ai.graph_nodes.step_conversion import MANDATE_STEP, MandateFacts, convert_step

EMITTED = ("brief", "kind_name", "audience")
DECLARED = EMITTED + tuple(f"extra_{i}" for i in range(9))  # 12 agent variables


def _entry(target: str) -> dict[str, Any]:
    return {"target": target, "compact": False, "deliver": "variable", "mapType": "offered_value",
            "required": False, "when_absent": "skip", "item_separator": "\n"}


FACTS = MandateFacts(
    mandate_key="foundry.mint", holder_type="agent", holder_id="aaaaaaaa-0000-0000-0000-000000000001",
    output_kind="study_summary", goal="Mint the kind.", goal_grounding="H",
    consumption_map={v: _entry(v) for v in DECLARED},
)


def _definition() -> dict[str, Any]:
    return {
        "nodes": [
            {"id": "kind_brief", "type": "data.transform", "data": {"spec_type": "data.transform", "config": {}}},
            {"id": "mint", "type": MANDATE_STEP, "data": {
                "spec_type": MANDATE_STEP, "config": {},
                "input": {"source_app": "w", "source_feature": "f", "mandate_key": "foundry.mint"}}},
        ],
        "edges": [{"id": "e_brief_mint", "source": "kind_brief", "target": "mint",
                   "data": {"kind": "data", "mappings": {"provision_values": "$FULL_PAYLOAD"}}}],
    }


def _mapped(source_outputs: dict[str, frozenset[str]] | None) -> tuple[dict[str, Any], list[str]]:
    conv = convert_step(_definition(), "mint", "agent", FACTS, source_outputs=source_outputs)
    return conv.edges[0]["data"]["mappings"], conv.notes


def test_only_the_keys_the_source_kind_emits_are_mapped() -> None:
    maps, _ = _mapped({"kind_brief": frozenset(EMITTED)})
    assert maps == {k: k for k in EMITTED}  # 3 of 12; red before the fix (12 keys)


def test_a_source_with_unknown_keys_says_so_instead_of_guessing_silently() -> None:
    maps, notes = _mapped(None)
    assert set(maps) == set(DECLARED)
    assert any("e_brief_mint" in n and "whole payload" in n for n in notes)
