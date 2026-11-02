"""Gather exposes the USEFUL shape of AI items, not only the raw results.

Live 2026-09-12 (run ``cdde033d``): a For-Each ran four ledger agents, a Gather
collected them, and the merge step after it could only be pointed at the raw
per-item results — each carrying its whole ``messages`` history. The merge's
prompt came to 1,019,616 tokens against a 1,000,000 window.

Gather now projects, index-aligned with ``values``:
  * ``structured_outputs`` — each item's ``structured_output``,
  * ``final_texts``      — each item's ``final_text``,
  * ``ai_item_count``    — so an all-empty projection is legible as "no AI
    items here", never as silent loss.
``values`` keeps the RAW objects for callers that genuinely want them, and
``__kind`` markers ride through untouched.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.nodes.control.gather import GatherConfig, GatherExecutor, GatherInput


def _item(index: int, value: Any, status: str = "succeeded") -> dict[str, Any]:
    return {"item_index": index, "status": status, "value": value}


def _ai(text: str, entries: list[str]) -> dict[str, Any]:
    return {
        "final_text": text,
        "messages": [{"role": "user", "content": "a very long document" * 100}],
        "usage": {"output_tokens": 22000},
        "structured_output": {"__kind": "ledger", "entries": entries},
    }


async def _gather(items: list[dict[str, Any]]):
    result = await GatherExecutor().execute(
        None,  # ctx unused in engine mode
        GatherInput.model_validate({"items": items}),
        GatherConfig(),
    )
    return result.result  # type: ignore[union-attr]


async def test_gather_projects_structured_output_and_final_text():
    out = await _gather(
        [_item(0, _ai("ledger one", ["a", "b"])), _item(1, _ai("ledger two", ["c"]))]
    )

    assert out.ai_item_count == 2
    assert out.final_texts == ["ledger one", "ledger two"]
    assert out.structured_outputs == [
        {"__kind": "ledger", "entries": ["a", "b"]},  # __kind is NOT stripped
        {"__kind": "ledger", "entries": ["c"]},
    ]
    # The raw objects stay available under their own key.
    assert out.values[0]["messages"]
    assert out.count == 2


async def test_projection_is_index_aligned_with_values():
    out = await _gather([_item(0, _ai("one", ["a"])), _item(1, {"plain": "not an ai result"})])

    assert len(out.structured_outputs) == len(out.final_texts) == len(out.values) == 2
    assert out.structured_outputs[1] is None
    assert out.final_texts[1] == ""
    assert out.ai_item_count == 1  # one AI item, one not — legible, not lost


async def test_holes_do_not_shift_the_projection():
    out = await _gather(
        [
            _item(0, _ai("one", ["a"])),
            _item(1, None, status="skipped"),
            _item(2, _ai("three", ["c"])),
        ]
    )

    assert out.final_texts == ["one", "three"]  # aligned with the SUCCEEDED values
    assert out.skipped_indexes == [1]
    assert [h.item_index for h in out.holes] == [1]
