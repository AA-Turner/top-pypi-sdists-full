"""Regression guard: `sql insert`/`upsert` must only stamp `user_id` on tables
that actually own the column.

Before this fix, the tool unconditionally did `row.setdefault("user_id", ...)`
on every insert/upsert. Against a global lookup table with no user_id column
(ai_model, ai_provider, ai_endpoint, …) PostgREST rejected the whole call with
`PGRST204: Could not find the 'user_id' column`. Now stamping is schema-aware:
the target table's columns are looked up (and cached) and user_id is only added
when the column exists. When the schema lookup fails we fall back to stamping,
because a missing ownership stamp on a user-owned table is a silent leak —
worse than a loud PGRST204.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.tools.implementations import database


@pytest.fixture(autouse=True)
def _clear_cache():
    database._TABLE_COLUMNS_CACHE.clear()
    yield
    database._TABLE_COLUMNS_CACHE.clear()


def _ctx(user_id: str = "user-123"):
    return SimpleNamespace(user_id=user_id)


async def test_stamps_user_id_when_table_owns_column(monkeypatch):
    async def fake_columns(schema, name):
        return frozenset({"id", "user_id", "name"})

    monkeypatch.setattr(database, "_get_table_columns", fake_columns)

    rows = [{"name": "a"}, {"name": "b"}]
    await database._stamp_auto_fields("public", "my_table", rows, _ctx())
    assert all(r["user_id"] == "user-123" for r in rows)


async def test_stamps_created_by_when_table_owns_only_created_by(monkeypatch):
    async def fake_columns(schema, name):
        return frozenset({"id", "created_by", "name"})

    monkeypatch.setattr(database, "_get_table_columns", fake_columns)

    rows = [{"name": "a"}]
    await database._stamp_auto_fields("chat", "conversation", rows, _ctx())
    assert rows[0]["created_by"] == "user-123"
    assert "user_id" not in rows[0]


async def test_stamps_both_on_dual_column_table(monkeypatch):
    async def fake_columns(schema, name):
        return frozenset({"id", "user_id", "created_by", "name"})

    monkeypatch.setattr(database, "_get_table_columns", fake_columns)

    rows = [{"name": "a"}]
    await database._stamp_auto_fields("tool", "tool_call", rows, _ctx())
    assert rows[0]["user_id"] == "user-123"
    assert rows[0]["created_by"] == "user-123"


async def test_does_not_stamp_user_id_on_global_lookup_table(monkeypatch):
    async def fake_columns(schema, name):
        # ai.model_definition has no user_id column.
        return frozenset({"id", "name", "model_class", "provider_id"})

    monkeypatch.setattr(database, "_get_table_columns", fake_columns)

    rows = [{"name": "grok-test", "model_class": "test"}]
    await database._stamp_auto_fields("ai", "model_definition", rows, _ctx())
    assert "user_id" not in rows[0]


async def test_does_not_overwrite_caller_supplied_user_id(monkeypatch):
    async def fake_columns(schema, name):
        return frozenset({"id", "user_id"})

    monkeypatch.setattr(database, "_get_table_columns", fake_columns)

    rows = [{"user_id": "explicit-owner"}]
    await database._stamp_auto_fields("public", "my_table", rows, _ctx())
    assert rows[0]["user_id"] == "explicit-owner"


async def test_falls_back_to_stamping_when_schema_lookup_fails(monkeypatch):
    async def boom(schema, name):
        raise RuntimeError("schema lookup down")

    monkeypatch.setattr(database, "_get_table_columns", boom)

    rows = [{"name": "a"}]
    await database._stamp_auto_fields("public", "unknown_table", rows, _ctx())
    # Fail-safe toward attribution: stamp the canonical owner column only —
    # blind user_id stamping breaks inserts on canonicalized (created_by-only) tables.
    assert rows[0]["created_by"] == "user-123"
    assert "user_id" not in rows[0]


async def test_falls_back_to_stamping_on_empty_column_set(monkeypatch):
    async def empty(schema, name):
        return frozenset()

    monkeypatch.setattr(database, "_get_table_columns", empty)

    rows = [{"name": "a"}]
    await database._stamp_auto_fields("public", "maybe_missing", rows, _ctx())
    assert rows[0]["created_by"] == "user-123"
    assert "user_id" not in rows[0]


async def test_get_table_columns_caches_positive_lookup(monkeypatch):
    from matrx_orm import catalog

    calls = {"n": 0}

    async def fake_describe(_database, *, schema, table):
        calls["n"] += 1
        return [{"column_name": "id"}, {"column_name": "user_id"}]

    monkeypatch.setattr(catalog, "describe_relation_columns", fake_describe)

    cols1 = await database._get_table_columns("chat", "message")
    cols2 = await database._get_table_columns("chat", "message")  # same schema.table key
    assert cols1 == frozenset({"id", "user_id"})
    assert cols2 == cols1
    assert calls["n"] == 1  # second call served from cache


async def test_get_table_columns_does_not_cache_empty(monkeypatch):
    from matrx_orm import catalog

    async def fake_describe(_database, *, schema, table):
        return []

    monkeypatch.setattr(catalog, "describe_relation_columns", fake_describe)

    await database._get_table_columns("public", "missing_table")
    assert "public.missing_table" not in database._TABLE_COLUMNS_CACHE


async def test_resolve_table_refuses_duplicate_name_even_when_public_exists(monkeypatch):
    async def fake_schemas_for_table(name):
        assert name == "definition"
        return ["public", "workflow", "tool"]

    monkeypatch.setattr(database, "_schemas_for_table", fake_schemas_for_table)

    assert await database._resolve_table("definition") == (
        None,
        "definition",
        ["public.definition", "workflow.definition", "tool.definition"],
    )


async def test_resolve_table_preserves_exact_qualified_identity(monkeypatch):
    async def should_not_run(name):
        raise AssertionError(f"unexpected bare lookup for {name}")

    monkeypatch.setattr(database, "_schemas_for_table", should_not_run)
    assert await database._resolve_table("workflow.definition") == (
        "workflow",
        "definition",
        [],
    )
