"""Two index-aligned lists pair up without a join node.

Deep Research saves one research.rs_content row per scraped page, and each row
needs the id of the rs_source record written for the SAME page. The pages and
the saved records are two lists in the same order; ``{$index}`` as an indirect
segment reads the same position of the second list. After a fan-out, gather's
``item_indexes`` names which dispatched item each value came from, so a hole
never pairs an analysis with the wrong page (``{$item}`` follows it).
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_graph.errors import ExecutionError
from matrx_graph.nodes._template import substitute_template
from matrx_graph.nodes.control.gather import GatherConfig, GatherExecutor, GatherInput


def test_index_segment_reads_the_same_position_of_another_list() -> None:
    extra = {"saved": [{"id": "s0"}, {"id": "s1"}]}
    got = [
        substitute_template({"url": "$item.url", "source_id": "$in.saved.{$index}.id"}, item, index=i, extra=extra)
        for i, item in enumerate([{"url": "a"}, {"url": "b"}])
    ]
    assert got == [{"url": "a", "source_id": "s0"}, {"url": "b", "source_id": "s1"}]


def test_item_segment_follows_a_position_held_by_the_element() -> None:
    extra = {"jobs": [{"c": "c0"}, {"c": "c1"}, {"c": "c2"}]}
    got = [substitute_template("$in.jobs.{$item}.c", item, index=i, extra=extra) for i, item in enumerate([0, 2])]
    assert got == ["c0", "c2"]


def test_index_segment_without_a_position_is_refused() -> None:
    with pytest.raises(ExecutionError):
        substitute_template("$in.saved.{$index}.id", {}, index=None, extra={"saved": []})


def test_item_segment_on_an_object_is_refused() -> None:
    with pytest.raises(ExecutionError):
        substitute_template("$in.jobs.{$item}", {"a": 1}, index=0, extra={"jobs": []})


async def test_gather_names_the_dispatched_item_of_every_value() -> None:
    items: list[dict[str, Any]] = [
        {"item_index": 0, "status": "succeeded", "value": {"v": "a"}},
        {"item_index": 1, "status": "skipped", "value": {}},
        {"item_index": 2, "status": "succeeded", "value": {"v": "c"}},
    ]
    result = await GatherExecutor().execute(
        None,  # type: ignore[arg-type]
        GatherInput.model_validate({"items": items}),
        GatherConfig(),
    )
    out = result.result
    assert [v["v"] for v in out.values] == ["a", "c"]
    assert out.item_indexes == [0, 2]
