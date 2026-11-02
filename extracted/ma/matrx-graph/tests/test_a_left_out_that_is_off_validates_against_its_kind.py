"""A ``left_out`` that is off must satisfy the kind schema the engine checks the step against.

Live incident 2026-10-27: ``left_out`` became ``None`` ("absent unless asked") while the
registered ``filter_result`` schema still required an array, so every workflow with a
data.filter / data.dedupe / data.limit failed its output-kind check in its first step.

The engine validates ``model_dump(mode="json")`` of the step's output against the kind's
JSON schema (published from the output model). So the check here is the same one: the
real executor's output with ``left_out`` off — key present as null AND key omitted — must
validate. The registered-kind schema is the model's own; the publisher plan
(``scripts/publish_kind_catalog.py aidream.kinds.data_ops``) proves live == model.
"""

from __future__ import annotations

from types import SimpleNamespace

import jsonschema
import pytest

from matrx_graph.nodes.data.collections import BatchConfig, BatchExecutor, BatchInput
from matrx_graph.nodes.data.filter import FilterConfig, FilterExecutor, FilterInput, FilterOutput
from matrx_graph.nodes.data.rules import RulesConfig, RulesExecutor, RulesInput, RulesOutput
from matrx_graph.nodes.text.repeated_lines import (
    RemoveRepeatedLinesExecutor,
    RepeatedLinesConfig,
    RepeatedLinesInput,
)

CTX = SimpleNamespace(node_id="the_step")
PAGES = [{"url": "https://a.com/"}, {"url": "https://a.com/blog/x"}]
RULES = [{"when": "'blog' in inputs['item']['url']", "then": {"label": "skip", "reason": "blog"}}]


async def _out(executor, inputs, config):
    res = await executor.execute(CTX, inputs, config)
    assert res.status == "success", res
    return res.result


def _validates_with_and_without_the_key(out) -> None:
    schema = type(out).model_json_schema()
    dumped = out.model_dump(mode="json")
    jsonschema.validate(dumped, schema)
    omitted = {k: v for k, v in dumped.items() if k != "left_out"}
    jsonschema.validate(omitted, schema)
    assert "left_out" not in schema.get("required", [])


@pytest.mark.asyncio
async def test_filter_with_left_out_off_validates() -> None:
    out = await _out(
        FilterExecutor(),
        FilterInput(items=PAGES),
        FilterConfig(predicate="'blog' not in inputs['url']"),
    )
    assert out.left_out is None
    _validates_with_and_without_the_key(out)


@pytest.mark.asyncio
async def test_rules_with_left_out_off_validates() -> None:
    out = await _out(
        RulesExecutor(), RulesInput(pages=PAGES), RulesConfig(rules=RULES, items_path="pages")
    )
    assert out.left_out is None
    _validates_with_and_without_the_key(out)


@pytest.mark.asyncio
async def test_repeated_lines_with_left_out_off_validates() -> None:
    texts = [
        {"id": "p1", "url": "u1", "text": "Menu\nOne"},
        {"id": "p2", "url": "u2", "text": "Menu\nTwo"},
    ]
    out = await _out(
        RemoveRepeatedLinesExecutor(), RepeatedLinesInput(texts=texts), RepeatedLinesConfig()
    )
    assert out.left_out is None
    _validates_with_and_without_the_key(out)


@pytest.mark.asyncio
async def test_batch_with_left_out_off_validates() -> None:
    out = await _out(BatchExecutor(), BatchInput(items=[1, 2, 3]), BatchConfig(size=2))
    _validates_with_and_without_the_key(out)


def test_the_filter_kind_schema_does_not_require_left_out() -> None:
    assert "left_out" not in FilterOutput.model_json_schema()["required"]
    assert "left_out" not in RulesOutput.model_json_schema().get("required", [])
