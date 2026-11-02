"""Named parts run in the order they read each other, never the stored key order.

A Definition round-trips through jsonb, which sorts object keys shortest-first: on 2026-10-28 a live
workflow's `writer_view` stored its parts as scan, texts, views and failed with KeyError 'texts' on every run
whose passes had terms. The test feeds the parts in exactly that stored order.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from matrx_graph.nodes.data.transform import TransformConfig, TransformExecutor, TransformInput

STORED_ORDER = {
    "scan": "[t for t in inputs['texts'] if t in inputs['terms']]",
    "texts": "[lower(v) for v in inputs['views']]",
    "views": "[c['text'] for c in inputs['cells']]",
}


async def test_parts_stored_shortest_first_still_run_in_reading_order() -> None:
    config = TransformConfig(define=STORED_ORDER, expression="{'scan': inputs['scan']}")
    assert config.part_order() == ["views", "texts", "scan"]
    out = await TransformExecutor().execute(
        SimpleNamespace(node_id="writer_view"),
        TransformInput(cells=[{"text": "A"}, {"text": "B"}], terms=["b"]),
        config,
    )
    assert out.status == "success" and out.result.model_dump()["scan"] == ["b"]


def test_parts_with_no_reading_between_them_keep_the_stored_order() -> None:
    assert TransformConfig(define={"b": "1", "a": "2"}, expression="inputs['a']").part_order() == ["b", "a"]


def test_two_parts_that_read_each_other_are_refused_at_save() -> None:
    with pytest.raises(ValidationError, match="break the loop"):
        TransformConfig(define={"a": "inputs['b']", "b": "inputs['a']"}, expression="inputs['a']")


def test_a_part_name_written_as_a_key_is_not_a_read() -> None:
    config = TransformConfig(
        define={"questions": "[q for q in inputs['rows']]", "answers": "{'questions': len(inputs['questions'])}"},
        expression="inputs['answers']",
    )
    assert config.part_order() == ["questions", "answers"]


def test_a_part_that_hands_inputs_on_whole_runs_after_the_rest() -> None:
    config = TransformConfig(define={"all": "len(inputs)", "n": "1"}, expression="inputs['all']")
    assert config.part_order() == ["n", "all"]
