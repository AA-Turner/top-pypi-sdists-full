"""The sql tool's write paths honour the same `match` contract as reads:
a list is IN, None is IS NULL. 2026-09-12: an `update` with
match={"id": [three uuids]} bound the list as one uuid and failed."""

from matrx_ai.tools.implementations.database import _orm_lookups


def test_list_becomes_in_lookup():
    assert _orm_lookups({"id": ["a", "b"]}) == {"id__in": ["a", "b"]}


def test_none_becomes_isnull_and_scalars_pass():
    assert _orm_lookups({"deleted_at": None, "name": "x"}) == {
        "deleted_at__isnull": True,
        "name": "x",
    }
