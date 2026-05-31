"""S7 — age-based cleanup keeps recent rows, drops old ones across all 3 tables."""

import importlib
from typing import TYPE_CHECKING, cast

import psycopg
import pytest

if TYPE_CHECKING:
    from typing_extensions import LiteralString

import abstra_internals.environment as environment
import abstra_internals.services.db.cleanup as cleanup
import abstra_internals.services.db.connection as connection
import abstra_internals.services.db.migrations as migrations


@pytest.fixture
def db(monkeypatch, pg_uri):
    monkeypatch.setenv("ABSTRA_WEB_EDITOR_DATABASE_URI", pg_uri)
    importlib.reload(environment)
    importlib.reload(connection)
    importlib.reload(migrations)
    importlib.reload(cleanup)
    migrations.apply_migrations()
    yield pg_uri
    connection.close_pool()
    monkeypatch.undo()
    importlib.reload(environment)
    importlib.reload(connection)
    importlib.reload(migrations)
    importlib.reload(cleanup)


def _seed(uri):
    with psycopg.connect(uri, autocommit=True) as conn:
        # executions: one old, one recent (created_at drives retention)
        conn.execute(
            "INSERT INTO executions "
            "(id, stage_id, status, pid, worker_id, context, created_at, updated_at) "
            "VALUES ('old', 's', 'finished', 1, 'w', '{}'::jsonb, now() - interval '48 hours', NULL),"
            "       ('new', 's', 'finished', 1, 'w', '{}'::jsonb, now(), NULL)"
        )
        # tasks: one old, one recent
        conn.execute(
            "INSERT INTO tasks (id, type, status, target_stage_id, payload, created_at) "
            "VALUES ('old', 't', 'pending', 's', '{}'::jsonb, now() - interval '48 hours'),"
            "       ('new', 't', 'pending', 's', '{}'::jsonb, now())"
        )
        # logs: db_inserted_at drives retention
        conn.execute(
            "INSERT INTO execution_logs (execution_id, stage_id, event, text, sequence, created_at, db_inserted_at) "
            "VALUES ('old', 's', 'stdout', 'x', 1, now(), now() - interval '48 hours'),"
            "       ('new', 's', 'stdout', 'y', 2, now(), now())"
        )


def _ids(uri, table, col="id"):
    # table/col are test-controlled literals, not user input.
    query = cast("LiteralString", f"SELECT {col} FROM {table} ORDER BY {col}")
    with psycopg.connect(uri, autocommit=True) as conn:
        rows = conn.execute(query).fetchall()
    return [r[0] for r in rows]


def test_cleanup_keeps_recent_drops_old(db):
    _seed(db)
    cleanup.delete_old_records(retention_hours=24)
    assert _ids(db, "executions") == ["new"]
    assert _ids(db, "tasks") == ["new"]
    assert _ids(db, "execution_logs", "execution_id") == ["new"]


def test_cleanup_idempotent(db):
    _seed(db)
    cleanup.delete_old_records()
    cleanup.delete_old_records()  # no error, nothing else removed
    assert _ids(db, "executions") == ["new"]
