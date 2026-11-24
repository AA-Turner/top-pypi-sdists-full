"""``RunStore.list_recent(record_ids=)``: the runs ABOUT a record, children included.

"Every run about this record" is ``metadata.record_id`` for every lane (table-event, store and system/mandate runs
stamp it; subgraph children carry their parent's). The read also lists the unstamped DIRECT children of a match
(children written before they inherited the stamp). Fake-backed: pins the query the store BUILDS — the scope still
binds, children are not hidden, an empty id list matches nothing (never every run)."""

from __future__ import annotations

from typing import Any

import pytest

from matrx_orm import Predicate

import matrx_graph.db.run_store as rs

OWNER = "11111111-1111-4111-8111-111111111111"
ITEM = "5b1f0c2e-8a44-4f7e-9d1b-2f0a6c3e9d71"
PRODUCT = "0e6c9a51-3d2f-4b8e-a7c4-91d2f5e8b603"
PARENT = "22222222-2222-4222-8222-222222222222"


class _FakeQuery:
    def __init__(self, log: list[dict[str, Any]], parents: list[dict[str, Any]]):
        self.log = log
        self.parents = parents
        self.entry: dict[str, Any] = {}

    def filter(self, *args: Any, **kwargs: Any) -> _FakeQuery:
        self.entry = {"args": args, "kwargs": kwargs}
        self.log.append(self.entry)
        return self

    def order_by(self, *fields: str) -> _FakeQuery:
        return self

    def limit(self, n: int) -> _FakeQuery:
        self.entry["limit"] = n
        return self

    def offset(self, n: int) -> _FakeQuery:
        return self

    async def values(self, *fields: str) -> list[dict[str, Any]]:
        return self.parents if fields == ("id",) else []


def _sql(args: tuple[Any, ...]) -> tuple[str, list[Any]]:
    """The WHERE text the store's typed predicates render, and their bound values."""
    params: list[Any] = []
    rendered = [a.as_sql(params) for a in args if isinstance(a, Predicate)]
    return " AND ".join(rendered), params


@pytest.fixture()
def calls(monkeypatch) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    log: list[dict[str, Any]] = []
    parents: list[dict[str, Any]] = []
    monkeypatch.setattr(rs, "get_model", lambda name: _FakeQuery(log, parents))
    return log, parents


async def test_runs_about_records_match_record_id_and_unstamped_children(calls) -> None:
    log, parents = calls
    parents.append({"id": PARENT})
    await rs.RunStore().list_recent(user_id=OWNER, record_ids=[ITEM, PRODUCT], omit_output=False)
    scan, final = log
    assert scan["limit"] == rs.RECORD_PARENT_SCAN_MAX
    sql, params = _sql(final["args"])
    # metadata ->> 'record_id' = ANY(...): the shape the run_record_id_idx expression index serves
    # (metadata @> {...} was a sequential scan of workflow.run).
    assert sql == '((metadata ->> $1) = ANY($2) OR parent_run_id = ANY($3::uuid[]))', sql
    assert params == ["record_id", [ITEM, PRODUCT], [PARENT]]
    # the access scope still binds and children are NOT hidden
    assert final["kwargs"]["created_by"] == OWNER
    assert "parent_run_id__isnull" not in final["kwargs"]


async def test_no_match_means_no_parent_arm(calls) -> None:
    log, _ = calls
    await rs.RunStore().list_recent(user_id=OWNER, record_ids=[ITEM])
    sql, params = _sql(log[-1]["args"])
    assert sql == '(metadata ->> $1) = ANY($2)', sql
    assert params == ["record_id", [ITEM]]


async def test_an_empty_record_list_matches_nothing(calls) -> None:
    log, _ = calls
    assert await rs.RunStore().list_recent(user_id=OWNER, record_ids=["", "  "]) == []
    assert log == []


async def test_without_records_children_stay_hidden(calls) -> None:
    log, _ = calls
    await rs.RunStore().list_recent(user_id=OWNER)
    assert len(log) == 1 and log[0]["kwargs"]["parent_run_id__isnull"] is True
