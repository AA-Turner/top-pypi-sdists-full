"""sql action=patch: str_replace on one text column of exactly one row."""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.tools.arg_models.db_args import SqlArgs, SqlPatchWire
from matrx_ai.tools.implementations import database
from matrx_ai.tools.models import ToolContext


class _Row:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data


class _Query:
    def __init__(self, rows: list[_Row]) -> None:
        self._rows = rows

    async def all(self) -> list[_Row]:
        return self._rows


def _model(store: list[dict[str, Any]]):
    class Meta:
        primary_keys = ["id"]

    class Model:
        _meta = Meta
        writes: list[dict[str, Any]] = []

        @classmethod
        def filter(cls, **lookups: Any) -> _Query:
            return _Query([_Row(r) for r in store if all(r.get(k) == v for k, v in lookups.items())])

        @classmethod
        async def update_where(cls, lookups: dict[str, Any], **data: Any) -> None:
            cls.writes.append(data)
            for r in store:
                if all(r.get(k) == v for k, v in lookups.items()):
                    r.update(data)

    return Model


@pytest.fixture
def store(monkeypatch):
    rows = [
        {"id": "a", "kind": "x", "body": "one\ntwo\ntwo\nthree"},
        {"id": "b", "kind": "x", "body": "other"},
    ]
    Model = _model(rows)

    async def target(table: str):
        return "skill", "definition", None, None

    monkeypatch.setattr(database, "_resolve_write_target", target)
    monkeypatch.setattr(database, "_resolve_write_model", lambda s, n: Model)
    monkeypatch.setattr(database, "_instance_to_dict", lambda r: dict(r.data))
    monkeypatch.setattr(database, "_orm_lookups", lambda m: dict(m))
    monkeypatch.setattr(database, "_guard_catalog_rules", lambda s, n, r: None)
    monkeypatch.setattr(database, "_guard_vocabulary", lambda s, n, r: (None, []))
    monkeypatch.setattr(database, "_after_catalog_write", lambda *a: None)
    monkeypatch.setattr(database, "_attach_rows_receipt", lambda result, **kw: result)
    return rows, Model


async def _patch(**args: Any):
    return await database._sql_patch({"table": "skill.definition", **args}, ToolContext(call_id="c"), 1.0)


def test_patch_is_a_sql_variant() -> None:
    parsed = SqlArgs.model_validate(
        {"action": "patch", "table": "t", "match": {"id": "a"}, "old_str": "x", "new_str": "y"}
    ).root
    assert isinstance(parsed, SqlPatchWire) and parsed.column == "body"


@pytest.mark.asyncio
async def test_unique_match_replaces_once(store) -> None:
    rows, Model = store
    r = await _patch(match={"id": "a"}, old_str="three", new_str="3")
    assert r.success and r.output["replacements"] == 1
    assert rows[0]["body"] == "one\ntwo\ntwo\n3" and rows[1]["body"] == "other"


@pytest.mark.asyncio
async def test_no_match_writes_nothing(store) -> None:
    rows, Model = store
    r = await _patch(match={"id": "a"}, old_str="zzz", new_str="y")
    assert not r.success and r.error.error_type == "patch_no_match" and not Model.writes


@pytest.mark.asyncio
async def test_ambiguous_names_lines_and_writes_nothing(store) -> None:
    rows, Model = store
    r = await _patch(match={"id": "a"}, old_str="two", new_str="2")
    assert r.error.error_type == "patch_ambiguous" and "[2, 3]" in r.error.message
    assert not Model.writes


@pytest.mark.asyncio
async def test_replace_all(store) -> None:
    rows, _ = store
    r = await _patch(match={"id": "a"}, old_str="two", new_str="2", replace_all=True)
    assert r.success and r.output["replacements"] == 2 and rows[0]["body"] == "one\n2\n2\nthree"


@pytest.mark.asyncio
async def test_match_must_select_exactly_one_row(store) -> None:
    rows, Model = store
    r = await _patch(match={"kind": "x"}, old_str="o", new_str="0")
    assert not r.success and "2 rows" in r.error.message and not Model.writes
