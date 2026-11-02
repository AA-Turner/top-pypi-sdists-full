"""``data.apportion`` — a whole number shared by weight; the shares always add up.

Red before 2026-10-27: there was no step, so "share 40 items across 6 parts" was written as a
4,766-character ``data.transform`` (Produce items across material, ``part_plan``).
"""

from __future__ import annotations

import asyncio

import pytest
from matrx_utils.splitting import apportion

from matrx_graph import NodeRegistry
from matrx_graph.nodes import BUILTIN_VALUES_ARE, register_builtin_nodes
from matrx_graph.nodes.data.apportion import (
    ApportionConfig,
    ApportionExecutor,
    ApportionInput,
    plan_apportion,
)
from matrx_graph.types.result import Failure, Success


def _run(items, *, total=None, ipc=None, min_each=None, **config):
    return asyncio.run(
        ApportionExecutor().execute(
            None,
            ApportionInput(items=items, total=total, items_per_call=ipc, min_each=min_each),
            ApportionConfig(**config),
        )
    )


@pytest.mark.parametrize(
    ("weights", "total"),
    [
        ([1200, 300, 4500, 800, 50, 2200], 40),
        ([1, 1, 1], 10),
        ([7], 13),
        ([0.25, 0.75], 9),
        ([3, 3, 3, 3, 3, 3, 3], 100),
        ([999_999, 1], 3),
    ],
)
def test_the_shares_always_sum_to_the_total(weights, total) -> None:
    out = plan_apportion(weights, total)
    assert sum(out.shares) == total == out.total == out.asked
    assert out.exact
    assert len(out.shares) == len(weights)


def test_shares_follow_the_weights() -> None:
    out = plan_apportion([100, 300], 8)
    assert out.shares == [2, 6]


def test_a_zero_weight_earns_nothing_beyond_min_each() -> None:
    assert plan_apportion([0, 10, 10], 10).shares == [0, 5, 5]
    assert plan_apportion([0, 10, 10], 10, min_each=1).shares == [1, 5, 4]
    # The library default still counts an empty part (the study-kit planners rely on it).
    assert plan_apportion([0, 1, 1], 3).shares == [0, 2, 1]
    assert apportion([0, 1, 1], 3, min_each=0) == [1, 1, 1]


def test_all_zero_weights_share_evenly_and_say_so() -> None:
    out = plan_apportion([0, 0, 0], 7)
    assert out.shares == [3, 2, 2]
    assert any("evenly" in n for n in out.notes)


def test_min_each_is_honoured_and_a_too_small_total_is_reported() -> None:
    out = plan_apportion([1, 1000, 1], 10, min_each=2)
    assert min(out.shares) >= 2 and sum(out.shares) == 10
    short = plan_apportion([5, 5, 5], 4, min_each=2)
    assert short.shares == [2, 2, 2] and not short.exact
    assert any("not the 4 asked" in n for n in short.notes)


def test_each_share_is_cut_into_calls_of_at_most_items_per_call() -> None:
    out = plan_apportion([300, 700], 23, items_per_call=5)
    assert out.shares == [7, 16]
    assert [p.call_counts for p in out.parts] == [[4, 3], [4, 4, 4, 4]]
    assert all(c.count <= 5 for c in out.calls)
    assert [(c.part, c.call, c.of, c.count) for c in out.calls] == [
        (0, 1, 2, 4), (0, 2, 2, 3), (1, 1, 4, 4), (1, 2, 4, 4), (1, 3, 4, 4), (1, 4, 4, 4),
    ]
    assert sum(c.count for c in out.calls) == 23


def test_max_calls_caps_the_calls_and_says_so() -> None:
    out = plan_apportion([1], 100, items_per_call=1, max_calls=30)
    assert out.parts[0].calls == 30
    assert sum(out.parts[0].call_counts) == 100
    assert max(out.parts[0].call_counts) == 4
    assert any("max_calls=30" in n for n in out.notes)


def test_a_zero_share_makes_no_calls() -> None:
    out = plan_apportion([0, 5], 3, items_per_call=2)
    assert out.parts[0].calls == 0 and out.parts[0].call_counts == []
    assert {c.part for c in out.calls} == {1}


def test_weights_from_a_path_into_records() -> None:
    parts = [{"title": "A", "size": 100}, {"title": "B", "size": 300}]
    result = _run(parts, total=8, weight_path="size")
    assert isinstance(result, Success)
    assert result.result.shares == [2, 6]


def test_inputs_win_over_the_steps_own_settings() -> None:
    result = _run([1, 1], total=4, ipc=1, items_per_call=10)
    assert isinstance(result, Success)
    assert len(result.result.calls) == 4


@pytest.mark.parametrize(
    ("items", "code"),
    [
        ([{"size": 1}, {"title": "no size"}], "weight_missing"),
        ([1, "two"], "weight_not_a_number"),
        ([1, True], "weight_not_a_number"),
        ([1, -2], "weight_negative"),
    ],
)
def test_a_bad_weight_fails_naming_the_item(items, code) -> None:
    result = _run(items, total=5, weight_path="size" if isinstance(items[0], dict) else "")
    assert isinstance(result, Failure)
    assert result.error.code == code
    assert "Item 1" in result.error.message


def test_no_total_fails() -> None:
    result = _run([1, 2])
    assert isinstance(result, Failure) and result.error.code == "missing_total"


def test_registered_and_deterministic() -> None:
    # A registry of this test's OWN: the process-wide default one is shared, and any earlier
    # test (or host boot) that registered the built-ins would make a plain call here raise
    # "control.branch already registered".
    registry = register_builtin_nodes(NodeRegistry())
    spec = registry.get("data.apportion").spec
    assert spec.output_kind == "apportioned_shares"
    assert spec.input_kind == "apportion_request"
    assert BUILTIN_VALUES_ARE["data.apportion"] == "deterministic"


def test_shares_of_1000_tenths_are_exact_and_ties_go_to_the_earlier_part():
    # The 36-question panel case: 26 / 6 / 2 / 1 answers in tenths of a percent.
    assert plan_apportion([26, 6, 2, 1], 1000).shares == [743, 171, 57, 29]
    # A 50/50 tie: the earlier part takes the odd unit.
    assert plan_apportion([1, 1], 1001).shares == [501, 500]
    # Three remainders of exactly 2/3: floats used to hand the units out of order.
    assert plan_apportion([0, 1, 4, 1], 1000).shares == [0, 167, 667, 166]
