"""Choose Items (data.choose, FEWER-STRONGER-STEPS N2): rules → repeats → order → per group → at most N in ONE
step, every left-out item listed once with its stage's reason.

The first test is the contract: on the same list, Choose Items answers exactly what the chain of steps it
replaces answers (Rules with left_out_labels → Dedupe → Sort → Limit), and lists the same items as left out.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from matrx_graph.errors import ExecutionError
from matrx_graph.nodes.data.choose import ChooseConfig, ChooseExecutor, ChooseInput
from matrx_graph.nodes.data.collections import (
    DedupeConfig,
    DedupeExecutor,
    DedupeInput,
    LimitConfig,
    LimitExecutor,
    LimitInput,
    SortConfig,
    SortExecutor,
    SortInput,
)
from matrx_graph.nodes.data.rules import RulesConfig, RulesExecutor, RulesInput

CTX = SimpleNamespace(node_id="choose")
PAGES = [
    {"url": "https://a.com/about", "kind": "about"},
    {"url": "https://a.com/blog/x", "kind": "blog"},
    {"url": "https://a.com/", "kind": "home"},
    {"url": "https://a.com/About", "kind": "about"},
    {"url": "https://a.com/pricing", "kind": "pricing"},
    {"url": "https://a.com/team", "kind": "team"},
]
SKIP = [{"when": "inputs['item']['kind'] in inputs['skip']", "then": {"label": "skip", "reason": "a {item.kind} page"}}]


async def _run(config: dict, items: list = PAGES, **others):
    res = await ChooseExecutor().execute(CTX, ChooseInput(items=items, **others), ChooseConfig(**config))
    assert res.status == "success", res
    return res.result


async def test_choose_answers_what_the_chain_it_replaces_answers() -> None:
    others = {"skip": ["blog"], "kinds_first": ["home", "about", "pricing"]}
    order = [{"key": "kind", "position_in": "kinds_first"}]
    chosen = await _run(
        {"rules": SKIP, "left_out_labels": ["skip"], "unique_by": {"key": "url", "normalize": "case_space"},
         "order_by": order, "limit": 3},
        **others,
    )
    ruled = (await RulesExecutor().execute(
        CTX, RulesInput(items=PAGES, **others),
        RulesConfig(rules=SKIP, items_path="items", left_out_labels=["skip"]),
    )).result
    deduped = (await DedupeExecutor().execute(
        CTX, DedupeInput(items=ruled.kept_items), DedupeConfig(key="url", normalize="case_space")
    )).result
    ordered = (await SortExecutor().execute(
        CTX, SortInput(items=deduped.items, **others), SortConfig(order_by=order)
    )).result
    limited = (await LimitExecutor().execute(CTX, LimitInput(items=ordered.items), LimitConfig(count=3))).result
    assert chosen.items == limited.items
    assert [p["kind"] for p in chosen.items] == ["home", "about", "pricing"]
    # Left out: the blog page (rule), the repeated About (repeat), the team page (limit) — input positions.
    assert [(e.item, e.reason) for e in chosen.left_out] == [
        (1, "a blog page"), (3, "a repeat of item 0"), (5, "past the limit of 3")
    ]
    assert chosen.counts == {"rules": 1, "repeats": 1, "per_group": 0, "limit": 1}
    assert (chosen.kept, chosen.dropped) == (3, 3)


async def test_no_stage_set_returns_the_list_unchanged() -> None:
    out = await _run({})
    assert out.items == PAGES and out.left_out == [] and out.dropped == 0


async def test_rules_write_their_fields_and_decision_onto_each_item() -> None:
    rules = [{"when": "inputs['item']['kind'] == 'home'", "then": {"label": "lead", "score": 1, "fields": {"tier": "a"}}}]
    out = await _run({"rules": rules, "default": {"label": "rest", "score": 0}, "decision_keys": {"label": "group"}})
    assert out.items[2] == {"url": "https://a.com/", "kind": "home", "tier": "a", "group": "lead"}
    assert out.items[0]["group"] == "rest" and "tier" not in out.items[0]


async def test_per_group_leaves_out_or_moves_the_rest_last() -> None:
    items = [{"id": i, "fam": f} for i, f in enumerate(["x", "x", "y", "x", "y"])]
    out = await _run({"per_group": {"by": "fam", "max": 1}, "label_path": "id"}, items)
    assert [i["id"] for i in out.items] == [0, 2]
    assert [(e.item, e.label, e.reason) for e in out.left_out] == [
        (1, "1", "more than 1 of its group"), (3, "3", "more than 1 of its group"), (4, "4", "more than 1 of its group")
    ]
    out = await _run({"per_group": {"by": "fam", "max": 1, "overflow": "last"}, "limit": 3}, items)
    assert [i["id"] for i in out.items] == [0, 2, 1]
    assert out.counts["per_group"] == 0 and out.counts["limit"] == 2


async def test_round_robin_limit_takes_turns_across_groups() -> None:
    items = [{"id": i, "line": l} for i, l in enumerate(["a", "a", "a", "b", "c"])]
    out = await _run({"limit": 3, "round_robin": {"by": "line", "group_order": "first_seen"}}, items)
    assert [i["id"] for i in out.items] == [0, 3, 4]
    assert [e.item for e in out.left_out] == [1, 2]


async def test_reasons_read_the_item_and_other_inputs_and_rank_is_written() -> None:
    out = await _run(
        {"limit": 2, "limit_reason": "past max_pages ({max_pages}): {item.url}", "rank_as": "rank"},
        max_pages=2,
    )
    assert [p["rank"] for p in out.items] == [1, 2]
    assert out.left_out[0].reason == "past max_pages (2): https://a.com/"


async def test_refusals_are_loud() -> None:
    with pytest.raises(ValidationError):
        ChooseConfig(left_out_labels=["skip"])  # left out by rules, but no rules
    with pytest.raises(ValidationError):
        ChooseConfig(round_robin={"by": "line"})  # turns need a limit
    with pytest.raises(ValidationError):
        ChooseConfig(rules=[{"when": "__import__('os')", "then": {"label": "x"}}])  # the sandbox check, at save
    with pytest.raises(ValidationError, match="no rule or default"):
        ChooseConfig(rules=SKIP, left_out_labels=["skp"])  # a mistyped label would never match
    for orphan in ({"missing": "first"}, {"limit_reason": "x"}, {"mode": "all_match"}):
        with pytest.raises(ValidationError):
            ChooseConfig(**orphan)  # a setting that would do nothing
    with pytest.raises(ValidationError):
        ChooseConfig(rules=SKIP, decision_keys={"label": "n"}, rank_as="n")  # two writers of one field
    with pytest.raises(ExecutionError, match="Rename that input"):  # an input named 'item' would shadow the rule's item
        await ChooseExecutor().execute(CTX, ChooseInput(items=PAGES, item=1), ChooseConfig(rules=SKIP))


async def test_rules_read_the_whole_list_and_labels_come_from_the_item_as_it_came_in() -> None:
    rules = [{"when": "len(inputs['items']) > 2 and inputs['index'] == 0", "then": {"label": "x", "fields": {"nm": "N"}}}]
    out = await _run({"rules": rules, "left_out_labels": ["x"], "label_path": "nm"}, [{"a": 1}, {"a": 2}, {"a": 3}])
    assert [(e.item, e.label) for e in out.left_out] == [(0, "Item 0")]


async def test_rank_and_rule_fields_refuse_items_that_are_not_objects() -> None:
    with pytest.raises(ExecutionError):
        await ChooseExecutor().execute(CTX, ChooseInput(items=["a", "b"]), ChooseConfig(rank_as="rank"))
    rules = [{"when": "True", "then": {"label": "x", "fields": {"tier": "a"}}}]
    with pytest.raises(ExecutionError):
        await ChooseExecutor().execute(CTX, ChooseInput(items=["a"]), ChooseConfig(rules=rules))
