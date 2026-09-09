"""``sql`` tool ``match`` → typed ORM filters.

Guards the 2026-09-08 gap: an agent needing "the offerings for THESE model
ids" had no filter shape for it (match was equality-only), so it dumped the
whole table (163,817 chars) and then re-queried one model at a time.
"""

from __future__ import annotations

from matrx_ai.tools.implementations.database import match_filters


def test_scalar_is_equality() -> None:
    (f,) = match_filters({"status": "active"})
    assert (f.field, f.operator, f.value) == ("status", "eq", "active")


def test_list_is_in() -> None:
    (f,) = match_filters({"model_id": ["a", "b"]})
    assert (f.field, f.operator, f.value) == ("model_id", "in", ["a", "b"])


def test_tuple_is_in() -> None:
    (f,) = match_filters({"id": ("a",)})
    assert (f.operator, f.value) == ("in", ["a"])


def test_none_is_isnull() -> None:
    (f,) = match_filters({"deleted_at": None})
    assert (f.field, f.operator, f.value) == ("deleted_at", "isnull", True)


def test_order_and_mixture_preserved() -> None:
    fs = match_filters({"a": 1, "b": [1, 2], "c": None})
    assert [f.operator for f in fs] == ["eq", "in", "isnull"]
