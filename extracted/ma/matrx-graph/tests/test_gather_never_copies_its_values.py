"""A gather carries what its items returned; it never copies it (research read OOM, 2026-11-17).

The research read step's outer gather received four keyword results, each a subgraph result carrying every
page's every step output. Validating those values again as ``JsonValue`` (plus a ``model_dump`` of the input)
rebuilt the whole tree three or four times at once and took a 4 GB host past its limit (exit 137). The gather
must hand on the very objects that arrived, in ``values``, ``pairs`` and ``holes`` alike, add no memory
proportional to their size, and keep its published JSON schema and its dumped output unchanged.
"""

from __future__ import annotations

import asyncio
import tracemalloc

from matrx_graph.nodes.control.gather import (
    GatherConfig,
    GatherExecutor,
    GatherHole,
    GatherInput,
    GatherPair,
)


def _big_value(i: int) -> dict:
    # A page read as it returns: its text and thousands of small link records (the containers are what a
    # copy rebuilds; strings are shared either way).
    return {
        "last_outputs": {
            "fetch": {
                "text": f"page {i} " * 40_000,
                "link_records": [{"url": f"https://example.com/{i}/{n}", "text": "a link", "n": n} for n in range(5_000)],
            },
            "result": {"read": [{"id": str(i), "is_good": True}]},
        }
    }


def _gather(items: list, dispatched: list) -> tuple:
    raw = {"items": items, "jobs": dispatched}
    inputs = GatherInput.model_validate(raw)
    return asyncio.run(GatherExecutor().execute(None, inputs, GatherConfig(items_from="jobs"))), raw


def test_values_pairs_and_holes_are_the_objects_that_arrived() -> None:
    values = [_big_value(i) for i in range(3)]
    items = [{"item_index": i, "status": "succeeded", "value": v} for i, v in enumerate(values)]
    items.append({"item_index": 3, "status": "skipped", "value": None})
    dispatched = [{"keyword": {"id": str(i)}} for i in range(4)]

    res, _ = _gather(items, dispatched)
    out = res.result

    assert all(out.values[i] is values[i] for i in range(3)), "gather copied its values"
    assert all(out.pairs[i].value is values[i] for i in range(3)), "gather copied a pair's value"
    assert all(out.pairs[i].item is dispatched[i] for i in range(3)), "gather copied a pair's item"
    assert out.holes[0].item is dispatched[3], "gather copied a hole's item"


def test_gathering_adds_no_memory_in_proportion_to_the_values() -> None:
    values = [_big_value(i) for i in range(8)]  # 40,000 records across the items
    items = [{"item_index": i, "status": "succeeded", "value": v} for i, v in enumerate(values)]
    dispatched = [{"n": i} for i in range(8)]

    tracemalloc.start()
    base = tracemalloc.get_traced_memory()[0]
    _gather(items, dispatched)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Before the fix this peaked at ~+27 MB (every record rebuilt); carrying it costs bookkeeping only.
    assert peak - base < 1_000_000, f"gather peaked at +{(peak - base) / 1e6:.1f} MB carrying its values"


def test_the_dumped_output_is_what_validated_models_dump() -> None:
    value = {"a": [1, 2.5, "x", None, {"b": True}]}
    built = GatherPair.model_construct(item_index=0, item={"k": 1}, value=value)
    validated = GatherPair(item_index=0, item={"k": 1}, value=value)
    assert built.model_dump(mode="json") == validated.model_dump(mode="json")

    hole_built = GatherHole.model_construct(item_index=1, status="skipped", error=None, item={"k": 2})
    hole_validated = GatherHole(item_index=1, status="skipped", error=None, item={"k": 2})
    assert hole_built.model_dump(mode="json") == hole_validated.model_dump(mode="json")

    res, _ = _gather(
        [{"item_index": 0, "status": "succeeded", "value": value}, {"item_index": 1, "status": "skipped"}],
        [{"k": 1}, {"k": 2}],
    )
    dumped = res.result.model_dump(mode="json")
    assert dumped["values"] == [value]
    assert dumped["pairs"] == [validated.model_dump(mode="json")]
    assert dumped["holes"] == [hole_validated.model_dump(mode="json")]
    assert dumped["__kind"] == "gather_result"
