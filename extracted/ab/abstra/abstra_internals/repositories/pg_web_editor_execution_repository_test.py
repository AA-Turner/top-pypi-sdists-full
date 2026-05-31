"""S5 — PgWebEditorExecutionRepository: CRUD, list() parity, context round-trip."""

import datetime
import importlib
from unittest.mock import MagicMock

import pytest

import abstra_internals.environment as environment
import abstra_internals.services.db.connection as connection
import abstra_internals.services.db.migrations as migrations
from abstra_internals.entities.execution import Execution, ExecutionStatus
from abstra_internals.entities.execution_context import ScriptContext
from abstra_internals.repositories.execution import (
    ExecutionFilter,
    PgWebEditorExecutionRepository,
)

UTC = datetime.timezone.utc


@pytest.fixture
def repo(monkeypatch, pg_uri):
    monkeypatch.setenv("ABSTRA_WEB_EDITOR_DATABASE_URI", pg_uri)
    importlib.reload(environment)
    importlib.reload(connection)
    importlib.reload(migrations)
    migrations.apply_migrations()
    # __init__ builds a WebEditorControlProducerRepository (lazy, no connection);
    # replace it with a mock for stop_* assertions.
    r = PgWebEditorExecutionRepository("amqp://guest:guest@localhost/")
    r.control_producer = MagicMock()
    yield r
    connection.close_pool()
    monkeypatch.undo()
    importlib.reload(environment)
    importlib.reload(connection)
    importlib.reload(migrations)


def _mk(
    id,
    stage_id="stage-1",
    status: ExecutionStatus = "running",
    created_at=None,
    worker_id="w1",
):
    e = Execution.create(
        id=id,
        stage_id=stage_id,
        context=ScriptContext(task_id="t"),
        worker_id=worker_id,
    )
    e.status = status
    if created_at is not None:
        e.created_at = created_at
    return e


def test_create_get_roundtrip_preserves_status_and_context(repo):
    e = _mk(
        "e1", status="finished", created_at=datetime.datetime(2026, 1, 2, tzinfo=UTC)
    )
    e.updated_at = datetime.datetime(2026, 1, 3, tzinfo=UTC)
    repo.create(e)
    got = repo.get("e1")
    assert got.id == "e1"
    assert got.status == "finished"  # NOT reset to "running"
    assert got.created_at == datetime.datetime(2026, 1, 2, tzinfo=UTC)
    assert got.updated_at == datetime.datetime(2026, 1, 3, tzinfo=UTC)
    assert isinstance(got.context, ScriptContext)
    assert got.context.task_id == "t"
    assert got.worker_id == "w1"


def test_get_not_found(repo):
    with pytest.raises(Exception) as exc:
        repo.get("ghost")
    assert "Execution with id ghost not found" in str(exc.value)


def test_update_changes_status_and_context(repo):
    e = _mk("e1")
    repo.create(e)
    e.set_status("failed")
    e.context.sent_tasks.append("task-9")
    repo.update(e)
    got = repo.get("e1")
    assert got.status == "failed"
    assert got.context.sent_tasks == ["task-9"]
    assert got.updated_at is not None


def test_set_failure_by_id_without_reading(repo):
    repo.create(_mk("e1"))
    repo.set_failure_by_id("e1")
    assert repo.get("e1").status == "failed"
    # missing id must not raise
    repo.set_failure_by_id("nope")


def test_list_filters_and_total_count(repo):
    repo.create(
        _mk(
            "e1",
            stage_id="A",
            status="running",
            created_at=datetime.datetime(2026, 1, 1, tzinfo=UTC),
        )
    )
    repo.create(
        _mk(
            "e2",
            stage_id="A",
            status="failed",
            created_at=datetime.datetime(2026, 1, 2, tzinfo=UTC),
        )
    )
    repo.create(
        _mk(
            "e3",
            stage_id="B",
            status="running",
            created_at=datetime.datetime(2026, 1, 3, tzinfo=UTC),
        )
    )

    # stage_id filter
    resp = repo.list(ExecutionFilter(stage_id="A"))
    assert resp.total_count == 2
    assert {e.id for e in resp.executions} == {"e1", "e2"}

    # status filter
    resp = repo.list(ExecutionFilter(status="running"))
    assert {e.id for e in resp.executions} == {"e1", "e3"}

    # build_id and project_id both filter against stage_id (replicated quirk)
    assert {e.id for e in repo.list(ExecutionFilter(build_id="B")).executions} == {"e3"}
    assert {e.id for e in repo.list(ExecutionFilter(project_id="A")).executions} == {
        "e1",
        "e2",
    }


def test_list_ordering_and_pagination(repo):
    for i, day in enumerate([1, 2, 3], start=1):
        repo.create(
            _mk(f"e{i}", created_at=datetime.datetime(2026, 1, day, tzinfo=UTC))
        )
    resp = repo.list(ExecutionFilter())
    assert [e.id for e in resp.executions] == ["e3", "e2", "e1"]  # newest first
    page = repo.list(ExecutionFilter(limit=1, offset=1))
    assert [e.id for e in page.executions] == ["e2"]
    assert page.total_count == 3  # total before pagination


def test_total_count_when_paging_past_end(repo):
    # Paging beyond the last page yields no rows, but total_count must still be
    # the real total (parity with LocalExecutionRepository), not 0.
    for i in range(3):
        repo.create(_mk(f"e{i}"))
    resp = repo.list(ExecutionFilter(limit=10, offset=100))
    assert resp.executions == []
    assert resp.total_count == 3


def test_list_skips_unreconstructable_context_row(repo, pg_uri):
    import psycopg

    repo.create(_mk("good"))
    # Insert a row whose context jsonb can't rebuild a ClientContext (a bare
    # number is not a valid discriminated-union object).
    with psycopg.connect(pg_uri, autocommit=True) as conn:
        conn.execute(
            "INSERT INTO executions (id, stage_id, status, pid, worker_id, context, "
            "created_at, updated_at) VALUES ('bad','s','running',1,'w','5'::jsonb, "
            "now(), NULL)"
        )
    # The poison row is skipped (logged) — the listing still returns the good one
    # and does not 500. total_count is discounted by the skipped row so the page
    # size and the total agree (a short page must not read as "the last page").
    resp = repo.list(ExecutionFilter())
    assert {e.id for e in resp.executions} == {"good"}
    assert resp.total_count == 1


def test_list_date_range(repo):
    repo.create(_mk("e1", created_at=datetime.datetime(2026, 1, 1, tzinfo=UTC)))
    repo.create(_mk("e2", created_at=datetime.datetime(2026, 1, 5, tzinfo=UTC)))
    resp = repo.list(ExecutionFilter(start_date="2026-01-03T00:00:00+00:00"))
    assert {e.id for e in resp.executions} == {"e2"}
    resp = repo.list(ExecutionFilter(end_date="2026-01-03T00:00:00+00:00"))
    assert {e.id for e in resp.executions} == {"e1"}


def test_search_is_prefix_and_wildcards_are_literal(repo):
    repo.create(_mk("abc-1"))
    repo.create(_mk("abx-2"))
    repo.create(_mk("a%c-3"))  # literal percent in id
    assert {e.id for e in repo.list(ExecutionFilter(search="ab")).executions} == {
        "abc-1",
        "abx-2",
    }
    # user '%' must be treated literally, not as a wildcard
    assert {e.id for e in repo.list(ExecutionFilter(search="a%")).executions} == {
        "a%c-3"
    }


def test_clear_truncates(repo):
    repo.create(_mk("e1"))
    repo.clear()
    assert repo.list(ExecutionFilter()).total_count == 0


def test_stop_execution_uses_control_producer(repo):
    repo.stop_execution("e1")
    repo.control_producer.stop_execution.assert_called_once_with("e1")


def test_stop_all_running_uses_control_producer(repo):
    repo.stop_all_running()
    repo.control_producer.stop_all_executions.assert_called_once_with()
