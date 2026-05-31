"""S3 — migration runner: idempotency, concurrency, versioning, schema shape."""

import importlib
import threading

import psycopg
import pytest

import abstra_internals.environment as environment
import abstra_internals.services.db.connection as connection
import abstra_internals.services.db.migrations as migrations


@pytest.fixture
def db(monkeypatch, pg_uri):
    """Point the connection module at the per-test database."""
    monkeypatch.setenv("ABSTRA_WEB_EDITOR_DATABASE_URI", pg_uri)
    importlib.reload(environment)
    importlib.reload(connection)
    importlib.reload(migrations)
    yield pg_uri
    connection.close_pool()
    monkeypatch.undo()
    importlib.reload(environment)
    importlib.reload(connection)
    importlib.reload(migrations)


def test_apply_migrations_does_not_create_the_shared_pool(db):
    # The worker runs migrations at boot, BEFORE it forks the executor
    # forkserver. Creating the process-wide pool here would make every forked
    # executor inherit a pool whose worker threads don't survive fork → every
    # connection checkout would PoolTimeout. apply_migrations must use a one-off
    # connection and leave the pool uncreated.
    assert connection._pool is None
    migrations.apply_migrations()
    assert connection._pool is None


def _table_names(uri):
    with psycopg.connect(uri, autocommit=True) as conn:
        rows = conn.execute(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema = 'public'"
        ).fetchall()
    return {r[0] for r in rows}


def _index_names(uri):
    with psycopg.connect(uri, autocommit=True) as conn:
        rows = conn.execute(
            "SELECT indexname FROM pg_indexes WHERE schemaname = 'public'"
        ).fetchall()
    return {r[0] for r in rows}


def test_creates_schema_and_indexes(db):
    migrations.apply_migrations()
    tables = _table_names(db)
    assert {"executions", "tasks", "execution_logs", "_migrations"} <= tables
    indexes = _index_names(db)
    assert {
        "idx_executions_db_updated",
        "idx_tasks_target_status_created",
        "idx_logs_execution",
        "idx_logs_db_inserted",
    } <= indexes


def test_versioning_recorded(db):
    migrations.apply_migrations()
    with psycopg.connect(db, autocommit=True) as conn:
        versions = conn.execute(
            "SELECT version FROM _migrations ORDER BY version"
        ).fetchall()
    assert [v[0] for v in versions] == [m[0] for m in migrations.MIGRATIONS]


def test_idempotent_second_run_is_noop(db):
    migrations.apply_migrations()
    migrations.apply_migrations()  # must not raise nor duplicate
    with psycopg.connect(db, autocommit=True) as conn:
        row = conn.execute("SELECT count(*) FROM _migrations").fetchone()
    assert row is not None and row[0] == len(migrations.MIGRATIONS)


def test_concurrent_boots_serialize_without_ddl_race(db):
    errors = []

    def run():
        try:
            migrations.apply_migrations()
        except Exception as exc:  # noqa: BLE001 - capture for assertion
            errors.append(exc)

    threads = [threading.Thread(target=run) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert errors == []
    with psycopg.connect(db, autocommit=True) as conn:
        row = conn.execute("SELECT count(*) FROM _migrations").fetchone()
    assert row is not None and row[0] == len(migrations.MIGRATIONS)
