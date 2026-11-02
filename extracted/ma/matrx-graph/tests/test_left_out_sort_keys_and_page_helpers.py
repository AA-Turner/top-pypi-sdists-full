"""Fewer, stronger steps (generic-only FEWER-STRONGER-STEPS.md, 2026-10-27).

Left out with a reason (data.filter / data.limit / data.rules / data.batch / text.remove_repeated_lines),
multi-key data.sort with position-in-a-list, the url_path / url_depth / matches helpers, items mode on
text.remove_repeated_lines and write_key on data.group. Each option is off by default: the first test of
each block proves an unchanged config answers exactly as before.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_graph.errors import ExecutionError
from matrx_graph.nodes._sandbox import safe_eval
from matrx_graph.nodes.data.collections import (
    BatchConfig,
    BatchExecutor,
    BatchInput,
    LimitConfig,
    LimitExecutor,
    LimitInput,
    SortConfig,
    SortExecutor,
    SortInput,
)
from matrx_graph.nodes.data.filter import FilterConfig, FilterExecutor, FilterInput
from matrx_graph.nodes.data.group import GroupConfig, GroupExecutor, GroupInput
from matrx_graph.nodes.data.rules import RulesConfig, RulesExecutor, RulesInput
from matrx_graph.nodes.text.repeated_lines import (
    RemoveRepeatedLinesExecutor,
    RepeatedLinesConfig,
    RepeatedLinesInput,
)

CTX = SimpleNamespace(node_id="the_step")
PAGES = [{"url": "https://a.com/"}, {"url": "https://a.com/blog/x"}, {"url": "https://a.com/about"}]


async def _ok(executor, inputs, config):
    res = await executor.execute(CTX, inputs, config)
    assert res.status == "success", res
    return res.result


# --- left out: filter ---------------------------------------------------------


async def test_filter_left_out_is_off_by_default() -> None:
    out = await _ok(FilterExecutor(), FilterInput(items=PAGES), FilterConfig(predicate="'blog' not in inputs['url']"))
    assert out.kept == 2 and out.left_out is None


async def test_filter_left_out_names_each_dropped_item_with_a_filled_reason() -> None:
    cfg = FilterConfig(
        predicate="'blog' not in inputs['url']",
        left_out=True,
        left_out_label_path="url",
        left_out_reason="blog page ({item.url}), skip words {words}",
    )
    out = await _ok(FilterExecutor(), FilterInput(items=PAGES, words="blog"), cfg)
    assert [e.model_dump() for e in out.left_out] == [
        {"item": 1, "label": "https://a.com/blog/x", "reason": "blog page (https://a.com/blog/x), skip words blog",
         "step": "the_step"}
    ]


# --- left out: limit ----------------------------------------------------------


async def test_limit_left_out_lists_everything_past_the_count() -> None:
    plain = await _ok(LimitExecutor(), LimitInput(items=PAGES), LimitConfig(count=1))
    assert plain.left_out is None
    out = await _ok(LimitExecutor(), LimitInput(items=PAGES), LimitConfig(count=1, left_out=True))
    assert [(e.item, e.label, e.reason) for e in out.left_out] == [
        (1, "Item 1", "past the limit of 1"),
        (2, "Item 2", "past the limit of 1"),
    ]


async def test_limit_round_robin_left_out_is_what_the_rotation_did_not_pick() -> None:
    items = [{"g": "a", "n": 1}, {"g": "a", "n": 2}, {"g": "b", "n": 3}]
    cfg = LimitConfig(count=2, round_robin={"by": "g", "group_order": "first_seen"}, left_out=True,
                      left_out_label_path="n")
    out = await _ok(LimitExecutor(), LimitInput(items=items), cfg)
    assert [i["n"] for i in out.items] == [1, 3]
    assert [(e.item, e.label) for e in out.left_out] == [(1, "2")]


# --- left out: rules ----------------------------------------------------------


RULES = [
    {"when": "matches(inputs['item']['url'], '/blog(/|$)')", "then": {"label": "skip", "reason": "blog page"}},
    {"when": "url_depth(inputs['item']['url']) == 0", "then": {"label": "keep", "fields": {"kind": "home"}}},
]


async def test_rules_left_out_labels_split_kept_from_left_out_with_the_rows_reason() -> None:
    plain = await _ok(RulesExecutor(), RulesInput(pages=PAGES),
                      RulesConfig(rules=RULES, items_path="pages", default={"label": "keep", "fields": {"kind": "other"}}))
    assert plain.kept_items is None and plain.left_out is None
    cfg = RulesConfig(rules=RULES, items_path="pages", write_fields=True, left_out_labels=["skip"],
                      left_out_label_path="url", default={"label": "keep", "fields": {"kind": "other"}})
    out = await _ok(RulesExecutor(), RulesInput(pages=PAGES), cfg)
    assert out.kept_items == [{"url": "https://a.com/", "kind": "home"}, {"url": "https://a.com/about", "kind": "other"}]
    assert [e.model_dump() for e in out.left_out] == [
        {"item": 1, "label": "https://a.com/blog/x", "reason": "blog page", "step": "the_step"}
    ]


# --- left out: batch keeps its shape and gains the reason --------------------------


async def test_batch_left_out_keeps_position_size_label_and_gains_reason_and_step() -> None:
    cfg = BatchConfig(size=5, measure="chars", overflow="left_out", text_path="t", label_path="t",
                      split_oversized=False)
    out = await _ok(BatchExecutor(), BatchInput(items=[{"t": "abc"}, {"t": "abcdef"}]), cfg)
    assert [e.model_dump() for e in out.left_out] == [
        {"item": 1, "label": "abcdef", "reason": "did not fit the budget of 5 chars", "step": "the_step", "size": 6}
    ]


# --- multi-key sort -------------------------------------------------------------


async def test_sort_single_key_unchanged() -> None:
    out = await _ok(SortExecutor(), SortInput(items=[{"s": 2}, {"s": 1}]), SortConfig(key="s"))
    assert out.items == [{"s": 1}, {"s": 2}]


async def test_sort_by_several_keys_with_position_in_an_input_list() -> None:
    items = [
        {"kind": "other", "url": "https://a.com/zz"},
        {"kind": "pricing", "url": "https://a.com/pricing"},
        {"kind": "about", "url": "https://a.com/about/team"},
        {"kind": "home", "url": "https://a.com/"},
        {"kind": "about", "url": "https://a.com/about"},
    ]
    cfg = SortConfig(order_by=[
        {"expression": "inputs['kind'] != 'home'"},
        {"key": "kind", "position_in": "kinds_first"},
        {"expression": "url_depth(inputs['url'])"},
        {"expression": "len(inputs['url'])"},
    ])
    out = await _ok(SortExecutor(), SortInput(items=items, kinds_first=["about", "pricing"]), cfg)
    assert [i["url"] for i in out.items] == [
        "https://a.com/", "https://a.com/about", "https://a.com/about/team", "https://a.com/pricing", "https://a.com/zz",
    ]


async def test_sort_position_in_a_missing_input_is_refused() -> None:
    with pytest.raises(ExecutionError, match="position_in"):
        await SortExecutor().execute(CTX, SortInput(items=[{"k": 1}]),
                                     SortConfig(order_by=[{"key": "k", "position_in": "nope"}]))


# --- expression helpers ---------------------------------------------------------


def test_url_path_depth_and_matches() -> None:
    assert safe_eval("url_path(inputs['u'])", {"u": "https://a.com/x/y/?q=1#f"}) == "/x/y/"
    assert safe_eval("url_path(inputs['u'])", {"u": "https://a.com"}) == "/"
    assert safe_eval("url_depth(inputs['u'])", {"u": "https://a.com/x/y/"}) == 2
    assert safe_eval("url_depth(inputs['u'])", {"u": "https://a.com/"}) == 0
    # No scheme: a PATH, not a host ("about/team" is depth 2); "//host/x" is an address.
    assert safe_eval("url_path(inputs['u'])", {"u": "about/team"}) == "/about/team"
    assert safe_eval("url_depth(inputs['u'])", {"u": "about/team"}) == 2
    assert safe_eval("url_path(inputs['u'])", {"u": "/x?q=1"}) == "/x"
    assert safe_eval("url_path(inputs['u'])", {"u": "//a.com/x/y"}) == "/x/y"
    assert safe_eval("matches(inputs['u'], '(^|[/_-])about(-us)?($|[/_.-])', True)", {"u": "/ABOUT-us/"}) is True
    assert safe_eval("matches(inputs['u'], '(^|/)blogs?(/|$)')", {"u": "/weblog"}) is False
    assert safe_eval("matches(inputs['u'], 'x')", {"u": None}) is False


# --- remove repeated lines: items mode --------------------------------------------


async def test_repeated_lines_items_mode_returns_whole_items_and_leaves_out_the_emptied() -> None:
    texts = [
        {"id": "p1", "url": "u1", "text": "Menu\nOne"},
        {"id": "p2", "url": "u2", "text": "Menu\nTwo"},
        {"id": "p3", "url": "u3", "text": "Menu"},
    ]
    plain = await _ok(RemoveRepeatedLinesExecutor(), RepeatedLinesInput(texts=texts), RepeatedLinesConfig())
    assert plain.kept_items is None and plain.repeated_text is None
    out = await _ok(RemoveRepeatedLinesExecutor(), RepeatedLinesInput(texts=texts), RepeatedLinesConfig(items_mode=True))
    assert out.kept_items == [{"id": "p1", "url": "u1", "text": "One"}, {"id": "p2", "url": "u2", "text": "Two"}]
    assert [(e.item, e.label, e.step) for e in out.left_out] == [(2, "p3", "the_step")]
    assert out.repeated_text == "Menu"


# --- group: write_key -----------------------------------------------------------


async def test_group_write_key_puts_key_rank_and_size_on_every_item() -> None:
    items = [{"id": "a", "f": "x"}, {"id": "b", "f": "y"}, {"id": "c", "f": "x"}]
    plain = await _ok(GroupExecutor(), GroupInput(items=items), GroupConfig(key="f"))
    assert plain.keyed_items is None
    out = await _ok(GroupExecutor(), GroupInput(items=items), GroupConfig(key="f", write_key="family"))
    assert [(i["id"], i["family_rank"], i["family_size"]) for i in out.keyed_items] == [("a", 1, 2), ("b", 1, 1), ("c", 2, 2)]
    assert out.keyed_items[0]["family"] == out.keyed_items[2]["family"] != out.keyed_items[1]["family"]


# --- review fixes ---------------------------------------------------------------


async def test_sort_expression_reading_a_missing_field_is_a_hole_placed_by_missing() -> None:
    items = [{"d": 2}, {"x": 1}, {"d": 1}]
    cfg = SortConfig(order_by=[{"expression": "inputs['d']"}])
    out = await _ok(SortExecutor(), SortInput(items=items), cfg)
    assert out.items == [{"d": 1}, {"d": 2}, {"x": 1}]
    out = await _ok(SortExecutor(), SortInput(items=items), SortConfig(order_by=[{"expression": "inputs['d']"}], missing="first"))
    assert out.items == [{"x": 1}, {"d": 1}, {"d": 2}]


async def test_sort_expression_that_fails_names_the_item_and_expression() -> None:
    cfg = SortConfig(order_by=[{"expression": "10 / inputs['d']"}])
    with pytest.raises(ExecutionError) as err:
        await SortExecutor().execute(CTX, SortInput(items=[{"d": 5}, {"d": 0}]), cfg)
    assert "item 1" in str(err.value) and "10 / inputs['d']" in str(err.value)


async def test_limit_from_end_reason_says_last_n_even_with_an_offset() -> None:
    out = await _ok(LimitExecutor(), LimitInput(items=PAGES), LimitConfig(count=1, from_end=True, offset=1, left_out=True))
    assert [e.item for e in out.left_out] == [0, 1]
    assert {e.reason for e in out.left_out} == {"outside the last 1 items"}


async def test_left_out_reason_fills_name_from_the_item_when_no_input_has_it() -> None:
    out = await _ok(
        LimitExecutor(), LimitInput(items=PAGES),
        LimitConfig(count=1, left_out=True, left_out_reason="skipped {url}"),
    )
    assert [e.reason for e in out.left_out] == ["skipped https://a.com/blog/x", "skipped https://a.com/about"]


def test_split_replace_before_after_and_their_pattern_forms() -> None:
    """2026-10-28: text cut and swapped inside one expression (no method calls in the sandbox)."""
    assert safe_eval("split(inputs['t'], ', ')", {"t": "Austin, TX"}) == ["Austin", "TX"]
    assert safe_eval("split(inputs['t'], '=', 1)", {"t": "k=v=w"}) == ["k", "v=w"]
    assert safe_eval("split(inputs['t'], ' > ')", {"t": None}) == []
    assert safe_eval("replace(inputs['t'], '-', ' ')", {"t": "red-leather-wallet"}) == "red leather wallet"
    assert safe_eval("replace(inputs['t'], '&amp;', '&')", {"t": ["A &amp; B", None]}) == ["A & B", None]
    assert safe_eval("before(inputs['t'], '@')", {"t": "jo@example.com"}) == "jo"
    assert safe_eval("before(inputs['t'], ' | ')", {"t": "no bar"}) == "no bar"
    assert safe_eval("after(inputs['t'], '@')", {"t": "jo@example.com"}) == "example.com"
    assert safe_eval("after(inputs['t'], ':')", {"t": "none"}) == ""
    assert safe_eval("regex_split(inputs['t'], '[,;] *')", {"t": "a, b;c"}) == ["a", "b", "c"]
    assert safe_eval("regex_split(inputs['t'], '[,;] *', 1)", {"t": "a, b;c"}) == ["a", "b;c"]
    assert safe_eval("regex_replace(inputs['t'], '[^0-9]', '')", {"t": "(949) 555-0100"}) == "9495550100"
    # The replacement is literal text, never a group reference.
    assert safe_eval("regex_replace(inputs['t'], '(a)', '\\\\1')", {"t": "a"}) == "\\1"
    with pytest.raises(ExecutionError):
        safe_eval("split(inputs['t'], '')", {"t": "x"})
    with pytest.raises(ExecutionError, match=r"^regex_split\(\)"):
        safe_eval("regex_split(inputs['t'], '(a+)+$')", {"t": "aaa"})
    with pytest.raises(ExecutionError, match=r"^regex_replace\(\)"):
        safe_eval("regex_replace(inputs['t'], '(a+)+$', '')", {"t": "aaa"})
    # A captured group is kept between the parts (documented on regex_split).
    assert safe_eval("regex_split(inputs['t'], '([0-9])')", {"t": "a1b2c"}) == ["a", "1", "b", "2", "c"]
