"""PgWebEditorExecutionRepository.list(): total_count stays consistent with the
rows actually returned when a row's context can't be reconstructed (so a
paginating client never reads a short page as 'the last page')."""

import importlib
from unittest.mock import MagicMock

import pytest

import abstra_internals.environment as environment
import abstra_internals.services.db.connection as connection
import abstra_internals.services.db.migrations as migrations
from abstra_internals.entities.execution import Execution
from abstra_internals.entities.execution_context import ScriptContext
from abstra_internals.repositories.execution import (
    ExecutionFilter,
    PgWebEditorExecutionRepository,
)


@pytest.fixture
def repo(monkeypatch, pg_uri):
    monkeypatch.setenv("ABSTRA_WEB_EDITOR_DATABASE_URI", pg_uri)
    importlib.reload(environment)
    importlib.reload(connection)
    importlib.reload(migrations)
    migrations.apply_migrations()
    r = PgWebEditorExecutionRepository("amqp://guest:guest@localhost/")
    r.control_producer = MagicMock()
    yield r
    connection.close_pool()
    monkeypatch.undo()
    importlib.reload(environment)
    importlib.reload(connection)
    importlib.reload(migrations)


def _mk(id):
    return Execution.create(
        id=id, stage_id="stage-1", context=ScriptContext(task_id="t"), worker_id="w1"
    )


def _insert_unreconstructable_row(repo, id):
    # A context jsonb that no ClientContext subtype can rebuild (a bare int),
    # simulating a stale row left after a context-model change.
    from psycopg.types.json import Jsonb

    with repo._connection() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO executions (id, stage_id, status, pid, worker_id, context, "
            "created_at, updated_at, db_updated_at) "
            "VALUES (%s, %s, %s, %s, %s, %s, now(), now(), now())",
            (id, "stage-1", "running", 1, "w1", Jsonb(5)),
        )


def test_total_count_excludes_unreconstructable_rows(repo):
    repo.create(_mk("ok1"))
    repo.create(_mk("ok2"))
    _insert_unreconstructable_row(repo, "broken")

    resp = repo.list(ExecutionFilter())

    assert {e.id for e in resp.executions} == {"ok1", "ok2"}
    # The broken row is skipped AND discounted from the total, so page size and
    # total agree (not count(*)=3 while only 2 rows come back).
    assert len(resp.executions) == 2
    assert resp.total_count == 2


def test_total_count_unchanged_when_all_rows_reconstruct(repo):
    repo.create(_mk("ok1"))
    repo.create(_mk("ok2"))

    resp = repo.list(ExecutionFilter())

    assert len(resp.executions) == 2
    assert resp.total_count == 2
