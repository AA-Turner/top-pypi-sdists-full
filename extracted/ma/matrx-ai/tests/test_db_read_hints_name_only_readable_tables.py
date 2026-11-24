"""A person's read that misses is never pointed at a table it cannot read, and a table that
exists but is unreadable is reported as such (2026-11-17: ``db_read`` said
``runtime._ai_usage_calls`` does not exist while its own hint listed it in schema runtime)."""

from __future__ import annotations

import pytest

from matrx_ai.tools.implementations import database as db


@pytest.fixture
def catalog(monkeypatch):
    grouped = {"runtime": ["_ai_usage_calls", "_ai_usage_hourly", "global_execution"], "chat": ["message"]}

    async def tables_by_schema():
        return grouped

    async def schemas_for_table(name):
        return [s for s, ts in grouped.items() if name in ts]

    async def app_schemas():
        return list(grouped)

    async def readable_relations(database, *, role, exclude_schemas=None):
        assert role == db.PERSON_READ_ROLE
        return {"runtime.global_execution", "chat.message"}

    monkeypatch.setattr(db, "_tables_by_schema", tables_by_schema)
    monkeypatch.setattr(db, "_schemas_for_table", schemas_for_table)
    monkeypatch.setattr(db, "_app_schemas", app_schemas)
    monkeypatch.setattr(db, "_get_database_name", lambda: "test")
    monkeypatch.setattr("matrx_orm.catalog.readable_relations", readable_relations)


@pytest.mark.asyncio
async def test_a_person_reads_miss_lists_only_tables_it_can_read(catalog):
    from matrx_orm.operations.catalog_select import UnregisteredRelationError

    exc = UnregisteredRelationError('relation "runtime._ai_usage_hourlyy" does not exist')
    message, _ = await db._agent_db_error(exc, readable_by=db.PERSON_READ_ROLE)
    offered = message.split("\n", 1)[1]  # the first line repeats the name the caller asked for
    assert "_ai_usage" not in offered, message
    assert "global_execution" in message, message


@pytest.mark.asyncio
async def test_an_admin_miss_still_sees_every_table(catalog):
    from matrx_orm.operations.catalog_select import UnregisteredRelationError

    exc = UnregisteredRelationError('relation "runtime._ai_usage_hourlyy" does not exist')
    message, _ = await db._agent_db_error(exc)
    assert "runtime._ai_usage_hourly" in message, message


@pytest.mark.asyncio
async def test_an_unreadable_table_is_never_called_missing(catalog):
    from matrx_orm.operations.catalog_select import RelationNotReadableError

    message, _ = await db._agent_db_error(
        RelationNotReadableError("runtime", "_ai_usage_calls"), readable_by=db.PERSON_READ_ROLE
    )
    assert "does not exist" not in message
    assert "exists" in message and "runtime._ai_usage_calls" in message
