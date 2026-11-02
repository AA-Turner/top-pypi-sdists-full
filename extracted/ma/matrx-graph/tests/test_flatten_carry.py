"""``data.flatten`` ``carry``: each inner element keeps chosen fields of the element it came from.

Unnesting a list of parents into their children lost the parent: answers → their elements → their
options needed a For Each + template + gather per level just to keep "which element is this option
for", and search results lost the query that found them the same way.
"""

from __future__ import annotations

import pytest

from matrx_graph.errors import ExecutionError
from matrx_graph.nodes.data.flatten import FlattenConfig, FlattenExecutor, FlattenInput


class _Ctx:
    def __init__(self) -> None:
        self.flags: list[tuple[str, dict]] = []

    async def flag_for_review(self, label, message, *, category="other", payload=None):
        self.flags.append((label, payload))


async def _run(items, ctx=None, **config):
    result = await FlattenExecutor().execute(ctx, FlattenInput(items=items), FlattenConfig(**config))  # type: ignore[arg-type]
    return result.result


ANSWERS = [
    {"territory": "t1", "elements": [
        {"element": "c1_segments", "options": [{"value": {"text": "A"}}, {"value": {"text": "B"}}]},
        {"element": "c2_icp", "options": [{"value": {"text": "C"}}]},
    ]},
    {"territory": None, "elements": [{"element": "c1_segments", "options": []}]},
]


@pytest.mark.asyncio
async def test_carry_copies_parent_fields_onto_every_child():
    out = await _run(ANSWERS, path="elements", carry={"territory": "territory"})
    assert [e["element"] for e in out.items] == ["c1_segments", "c2_icp", "c1_segments"]
    assert [e["territory"] for e in out.items] == ["t1", "t1", None]
    # the parent's own list is never copied in, and the source items are not mutated
    assert "elements" not in out.items[0]
    assert "territory" not in ANSWERS[0]["elements"][0]


@pytest.mark.asyncio
async def test_two_levels_unnest_with_nested_paths_and_positions():
    elements = (await _run(ANSWERS, path="elements", carry={"territory": "territory"})).items
    out = await _run(elements, path="options", carry={"element": "element", "territory": "territory"},
                     source_index_as="element_index", index_as="option_index")
    assert [(o["element"], o["value"]["text"], o["territory"]) for o in out.items] == [
        ("c1_segments", "A", "t1"), ("c1_segments", "B", "t1"), ("c2_icp", "C", "t1")]
    assert [o["element_index"] for o in out.items] == [0, 0, 1]
    assert [o["option_index"] for o in out.items] == [0, 1, 0]


@pytest.mark.asyncio
async def test_carry_reads_a_dotted_parent_path_and_a_missing_one_is_null():
    items = [{"q": {"text": "pizza", "engine": "brave"}, "results": [{"url": "a"}]},
             {"q": {"text": "pie"}, "results": [{"url": "b"}]}]
    ctx = _Ctx()
    out = await _run(items, ctx, path="results", carry={"query": "q.text", "engine": "q.engine"})
    assert ctx.flags == []  # engine found in one parent: a hole, not a typo
    assert out.items == [{"url": "a", "query": "pizza", "engine": "brave"},
                         {"url": "b", "query": "pie", "engine": None}]


@pytest.mark.asyncio
async def test_a_child_field_the_parent_overwrites_is_counted_never_silent():
    items = [{"territory": "t9", "elements": [{"element": "x", "territory": "model-said"}]}]
    ctx = _Ctx()
    out = await _run(items, ctx, path="elements", carry={"territory": "territory"})
    assert out.items[0]["territory"] == "t9"
    assert ctx.flags == [("flatten.carry_overwrote", {"overwritten": 1, "fields": {"territory": 1}})]


@pytest.mark.asyncio
async def test_carry_onto_a_non_object_child_is_refused_loudly():
    with pytest.raises(ExecutionError, match="not an object"):
        await _run([{"tag": "a", "items": ["plain", "strings"]}], path="items", carry={"tag": "tag"})


@pytest.mark.asyncio
async def test_carry_without_a_path_is_refused():
    with pytest.raises(ValueError):
        FlattenConfig(carry={"x": "y"})


@pytest.mark.asyncio
async def test_without_carry_flatten_is_unchanged():
    ctx = _Ctx()
    out = await _run([[1, 2], [3]], ctx)
    assert out.items == [1, 2, 3] and out.count == 3 and out.sources == 2 and ctx.flags == []


@pytest.mark.asyncio
async def test_a_carry_path_found_in_no_parent_is_flagged_not_a_silent_null_column():
    ctx = _Ctx()
    out = await _run([{"q": {"text": "a"}, "results": [{"u": 1}]}], ctx, path="results", carry={"query": "q.txt"})
    assert out.items == [{"u": 1, "query": None}]
    assert ctx.flags == [("flatten.carry_missing", {"fields": {"query": "q.txt"}})]


@pytest.mark.asyncio
async def test_a_digit_step_indexes_a_list_in_the_parent():
    out = await _run([{"tags": ["x", "y"], "kids": [{"k": 1}]}], path="kids", carry={"first_tag": "tags.0"})
    assert out.items == [{"k": 1, "first_tag": "x"}]


@pytest.mark.parametrize("config", [
    {"path": "kids", "carry": {"i": "a"}, "index_as": "i"},
    {"path": "kids", "source_index_as": "n", "index_as": "n"},
    {"path": "kids", "carry": {"": "a"}},
    {"path": "kids", "carry": {"a": " "}},
])
def test_colliding_or_empty_names_are_refused_at_config_time(config):
    with pytest.raises(ValueError):
        FlattenConfig(**config)


@pytest.mark.asyncio
async def test_an_overwrite_without_a_context_still_works():
    out = await _run([{"t": "p", "kids": [{"t": "c"}]}], None, path="kids", carry={"t": "t"})
    assert out.items == [{"t": "p"}]


@pytest.mark.asyncio
async def test_path_only_output_is_exactly_the_old_output_and_the_parent_is_untouched():
    import copy
    items = [{"v": {"items": [{"a": 1}, {"a": 2}]}}, {"v": {"items": []}}]
    before = copy.deepcopy(items)
    out = await _run(items, path="v.items")
    assert out.items == [{"a": 1}, {"a": 2}] and out.sources == 2
    carried = await _run(items, path="v.items", carry={"x": "v.missing"}, index_as="pos")
    assert carried.items == [{"a": 1, "x": None, "pos": 0}, {"a": 2, "x": None, "pos": 1}]
    assert items == before
