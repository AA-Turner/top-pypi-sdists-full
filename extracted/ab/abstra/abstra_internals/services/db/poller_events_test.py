"""S8b — poller execution:update and task event scans."""

import importlib
import json

import psycopg
import pytest

import abstra_internals.environment as environment
import abstra_internals.services.db.connection as connection
import abstra_internals.services.db.migrations as migrations
import abstra_internals.services.db.poller as poller


@pytest.fixture
def db(monkeypatch, pg_uri):
    monkeypatch.setenv("ABSTRA_WEB_EDITOR_DATABASE_URI", pg_uri)
    importlib.reload(environment)
    importlib.reload(connection)
    importlib.reload(migrations)
    importlib.reload(poller)
    migrations.apply_migrations()
    yield pg_uri
    connection.close_pool()
    monkeypatch.undo()
    importlib.reload(environment)
    importlib.reload(connection)
    importlib.reload(migrations)
    importlib.reload(poller)


@pytest.fixture
def captured(monkeypatch):
    msgs = []
    monkeypatch.setattr(
        poller.BroadcastController, "broadcast", lambda *, msg: msgs.append(msg)
    )
    return msgs


def _conn(uri):
    return psycopg.connect(uri, autocommit=True)


def _now(conn, expr="now()"):
    return conn.execute(f"SELECT {expr}").fetchone()[0]


def test_poll_executions_emits_execution_update(db, captured):
    with _conn(db) as conn:
        conn.execute(
            "INSERT INTO executions (id, stage_id, status, pid, worker_id, context, created_at, updated_at) "
            "VALUES ('ex-1', 's', 'running', 1, 'w', '{}'::jsonb, now(), NULL)"
        )
        boot = _now(conn, "now() - interval '10 seconds'")
        poller._poll_executions(conn, boot, _now(conn))

    assert len(captured) == 1
    msg = json.loads(captured[0])
    assert msg == {"type": "execution:update", "payload": {"execution_id": "ex-1"}}


def test_poll_tasks_emits_task_dump(db, captured):
    with _conn(db) as conn:
        conn.execute(
            "INSERT INTO tasks (id, type, status, target_stage_id, payload, created_at, "
            "created_by_execution, created_by_stage) "
            "VALUES ('tk-1', 'form', 'pending', 'stage-1', '{\"k\": 1}'::jsonb, now(), 'ex-9', 'src-1')"
        )
        boot = _now(conn, "now() - interval '10 seconds'")
        poller._poll_tasks(conn, boot, _now(conn))

    assert len(captured) == 1
    msg = json.loads(captured[0])
    assert msg["type"] == "task"
    payload = msg["payload"]
    # TaskDTO.dump() uses camelCase aliases — matches the frontend task handler.
    assert payload["id"] == "tk-1"
    assert payload["status"] == "pending"
    assert payload["targetStageId"] == "stage-1"
    assert payload["payload"] == {"k": 1}
    assert payload["created"]["byExecutionId"] == "ex-9"


def test_events_have_no_dedup_reemission_is_harmless(db, captured):
    with _conn(db) as conn:
        conn.execute(
            "INSERT INTO executions (id, stage_id, status, pid, worker_id, context, created_at, updated_at) "
            "VALUES ('ex-1', 's', 'running', 1, 'w', '{}'::jsonb, now(), NULL)"
        )
        boot = _now(conn, "now() - interval '10 seconds'")
        poller._poll_executions(conn, boot, _now(conn))
        poller._poll_executions(conn, boot, _now(conn))
    # re-emitted within the window (no dedup, by design) — both carry full state
    assert len(captured) == 2


def test_forward_only_ignores_pre_boot_events(db, captured):
    with _conn(db) as conn:
        conn.execute(
            "INSERT INTO executions (id, stage_id, status, pid, worker_id, context, created_at, updated_at) "
            "VALUES ('old', 's', 'running', 1, 'w', '{}'::jsonb, now(), NULL)"
        )
        boot = _now(conn)  # captured after the insert
        poller._poll_executions(conn, boot, boot)
        poller._poll_tasks(conn, boot, boot)
    assert captured == []
