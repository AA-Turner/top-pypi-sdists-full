"""``data.rules`` ``sum_scores`` — a table of +/- points adds up per item, through the real scheduler.

Unit 9's candidate rank (SMART-ADD-IDENTIFY.md behavior 9) and person-or-business (9-e) need ONE
number per item from every matching row; ``all_match`` alone returned the rows but no total.
"""

from __future__ import annotations

from typing import Any

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
from matrx_graph.nodes.data.rules import RulesConfig

from tests._fixtures import make_app_context

RANK = [
    {"when": "inputs['item']['name_exact']", "then": {"label": "named", "reason": "name exact", "score": 3}},
    {"when": "inputs['item']['place']", "then": {"reason": "place on page", "score": 1.5}},
    {"when": "inputs['item']['not_them']", "then": {"reason": "namesake word", "score": -4}},
    {"when": "inputs['item']['linkedin']", "then": {"reason": "LinkedIn profile"}},
]


async def _run(inputs: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    defn = Definition.model_validate(
        {"nodes": [{"id": "n", "type": "data.rules", "position": {"x": 0, "y": 0},
                    "data": {"config": config, "inputs": inputs}}], "edges": []}
    )
    graph = compile_graph(defn, registry=reg)
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=reg).run(
        run_id="t-rules-sum", inputs=inputs
    )
    assert result.status is RunStatus.COMPLETED, result.error
    return result.last_outputs["n"]


def _cand(**flags: bool) -> dict[str, Any]:
    base = {"name_exact": False, "place": False, "not_them": False, "linkedin": False}
    return {**base, **flags}


async def test_each_item_carries_the_sum_of_every_matching_row_and_writes_it_for_the_sort() -> None:
    items = [
        _cand(name_exact=True, place=True, linkedin=True),  # 3 + 1.5 + 0
        _cand(name_exact=True, not_them=True),  # 3 - 4
        _cand(),  # nothing → default 0.25
    ]
    out = await _run(
        {"candidates": items},
        {
            "rules": RANK,
            "mode": "all_match",
            "sum_scores": True,
            "items_path": "candidates",
            "default": {"label": "weak", "score": 0.25},
            "write_fields": True,
            "decision_keys": {"total_score": "rank"},
        },
    )
    assert [i["total_score"] for i in out["items"]] == [4.5, -1.0, 0.25]
    assert [i["rank"] for i in out["updated_items"]] == [4.5, -1.0, 0.25]
    # every reason is still there beside the total
    assert [m["then"]["reason"] for m in out["items"][0]["matches"]] == [
        "name exact", "place on page", "LinkedIn profile"
    ]
    # the headline score stays the first row's own
    assert out["items"][0]["score"] == 3


async def test_single_mode_sums_and_the_option_off_leaves_no_total() -> None:
    on = await _run({"place": True, "x": 1}, {
        "rules": [{"when": "inputs['place']", "then": {"score": 2}},
                  {"when": "inputs['x'] == 1", "then": {"score": 0.5}}],
        "mode": "all_match", "sum_scores": True})
    assert on["total_score"] == 2.5
    off = await _run({"place": True}, {"rules": [{"when": "inputs['place']", "then": {"score": 2}}],
                                       "mode": "all_match"})
    assert "total_score" not in off  # off: exactly the keys the published kind had


def test_sum_scores_needs_all_match_and_the_total_key_needs_sum_scores() -> None:
    with pytest.raises(ValidationError, match="all_match"):
        RulesConfig.model_validate({"rules": RANK, "sum_scores": True})
    with pytest.raises(ValidationError, match="sum_scores"):
        RulesConfig.model_validate({"rules": RANK, "mode": "all_match", "items_path": "c",
                                    "write_fields": True, "decision_keys": {"total_score": "rank"}})
