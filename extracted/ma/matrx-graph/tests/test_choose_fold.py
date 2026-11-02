"""Narrowing chains (Filter / Dedupe / Sort / Limit) fold into ONE Choose Items step — and only when Choose's
fixed stage order gives the receiving step the same thing. Each case runs the definition before and after on
the real Scheduler; each kept case names why the steps stayed apart.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.fold import fold_reshape_steps

from tests.test_fold_reshape_steps import _edge, _node, _use

ROWS = {"rows": [
    {"url": "b", "score": 2, "line": "x"}, {"url": "a", "score": 5, "line": "y"}, {"url": "B", "score": 9, "line": "x"},
    {"url": "c", "score": 1, "line": "y"}, {"url": "a", "score": 7, "line": "x"}, {"url": "d", "score": 4, "line": "z"},
]}


def _defn(*steps: dict[str, Any], extra: list[dict[str, Any]] | None = None, out: dict[str, str] | None = None) -> dict[str, Any]:
    ids = [s["id"] for s in steps]
    edges = [_edge("e0", "src", ids[0], {"items": "rows"})]
    edges += [_edge(f"e{i}", a, b, {"items": "items"}) for i, (a, b) in enumerate(zip(ids, ids[1:]), 1)]
    edges.append(_edge("e_out", ids[-1], "use", out or {"chosen": "items", "n": "kept"}))
    return {
        "nodes": [_node("src", "data.transform", {"expression": repr({**ROWS, "seen": ["c"]})}), *steps,
                  _node("use", "data.transform", {"expression": "inputs"})],
        "edges": edges + (extra or []),
    }


async def test_filter_dedupe_sort_limit_become_one_choose_step_with_the_same_answer() -> None:
    defn = _defn(
        _node("keep", "data.filter", {"predicate": "inputs['url'] not in inputs['$in']['seen']"}),
        _node("once", "data.dedupe", {"key": "url", "normalize": "case_space"}),
        _node("best", "data.sort", {"key": "score", "order": "desc"}),
        _node("top", "data.limit", {"count": 2}),
        extra=[_edge("e_seen", "src", "keep", {"seen": "seen"})],
    )
    folded, folds, kept = fold_reshape_steps(defn)
    assert [f.step_id for f in folds] == ["keep", "once", "best"], kept
    choose = next(n for n in folded["nodes"] if n["id"] == "top")
    assert choose["data"]["spec_type"] == "data.choose"
    assert choose["data"]["config"]["rules"][0]["when"] == "not (inputs['item']['url'] not in inputs['seen'])"
    assert await _use(folded) == await _use(defn)


async def test_a_filter_after_a_sort_folds_because_filtering_keeps_order() -> None:
    defn = _defn(_node("best", "data.sort", {"key": "score"}), _node("big", "data.filter", {"predicate": "inputs['score'] > 2"}))
    folded, folds, _ = fold_reshape_steps(defn)
    assert [f.step_id for f in folds] == ["best"]
    assert await _use(folded) == await _use(defn)


async def test_a_round_robin_limit_folds() -> None:
    defn = _defn(_node("best", "data.sort", {"key": "score", "order": "desc"}),
                 _node("turns", "data.limit", {"count": 4, "round_robin": {"by": "line"}}))
    folded, folds, _ = fold_reshape_steps(defn)
    assert len(folds) == 1
    assert await _use(folded) == await _use(defn)


async def test_orders_choose_cannot_keep_stay_apart_and_say_why() -> None:
    cases = [
        (_node("best", "data.sort", {"key": "score"}), _node("once", "data.dedupe", {"key": "url"})),  # first copy changes
        (_node("top", "data.limit", {"count": 3, "round_robin": {"by": "line"}}),
         _node("big", "data.filter", {"predicate": "inputs['score'] > 2"})),
        (_node("once", "data.dedupe", {"key": "url"}), _node("big", "data.filter", {"predicate": "inputs['score'] > 2"})),
    ]
    for a, b in cases:
        folded, folds, kept = fold_reshape_steps(_defn(a, b))
        assert folds == [], (a["id"], b["id"])
        assert any("stage order" in k.reason for k in kept), kept


async def test_a_receiver_reading_what_choose_words_differently_keeps_the_steps() -> None:
    defn = _defn(_node("big", "data.filter", {"predicate": "inputs['score'] > 2"}), _node("once", "data.dedupe", {"key": "url"}),
                 out={"m": "matches"})
    folded, folds, kept = fold_reshape_steps(defn)
    assert folds == [] and any("reads matches, left_out" in k.reason for k in kept)


async def test_a_filter_over_plain_values_is_not_rewritten() -> None:
    defn = _defn(_node("v", "data.filter", {"predicate": "inputs['value'] != 'x'"}), _node("top", "data.limit", {"count": 1}))
    folded, folds, kept = fold_reshape_steps(defn)
    assert folds == [] and any("plain value" in k.reason for k in kept)


async def test_review_findings_stay_apart() -> None:
    """Each was a definition whose receiver got something different after the fold (review, 2026-10-28)."""
    cases = [
        # a Filter hoisted over a Dedupe folded in earlier changes which copy survives
        (_defn(_node("once", "data.dedupe", {"key": "url"}), _node("best", "data.sort", {"key": "score"}),
               _node("big", "data.filter", {"predicate": "inputs['score'] > 2"})), "big"),
        # `dropped` would count both steps' drops
        (_defn(_node("big", "data.filter", {"predicate": "inputs['score'] != 9"}),
               _node("top", "data.limit", {"count": 2, "round_robin": {"by": "line"}}), out={"d": "dropped"}), "big"),
        # a rank written by the first step is read by the second
        (_defn(_node("pick", "data.choose", {"order_by": [{"key": "score"}], "rank_as": "rank"}),
               _node("big", "data.filter", {"predicate": "inputs['rank'] < 2"})), "pick"),
        # `inputs` as a whole holds $in in a Filter, not in a rule
        (_defn(_node("big", "data.filter", {"predicate": "len(inputs) > 2"}),
               _node("top", "data.limit", {"count": 2, "round_robin": {"by": "line"}})), "big"),
    ]
    for defn, first in cases:
        folded, folds, kept = fold_reshape_steps(defn)
        assert first not in [f.step_id for f in folds if "Choose" in f.label], (first, kept)
        assert await _use(folded) == await _use(defn)


async def test_a_filter_whose_predicate_is_a_run_input_stays_and_does_not_crash() -> None:
    defn = _defn(_node("big", "data.filter", {"predicate": {"$input": "p"}}), _node("once", "data.dedupe", {"key": "url"}))
    _, folds, kept = fold_reshape_steps(defn)
    assert folds == [] and any("run input" in k.reason for k in kept)
