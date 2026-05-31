"""S8a — poller log scan: D9 stdio shape, dedup, window overlap, forward-only."""

import datetime
import importlib
import json
import time

import psycopg
import pytest

import abstra_internals.environment as environment
import abstra_internals.services.db.connection as connection
import abstra_internals.services.db.migrations as migrations
import abstra_internals.services.db.poller as poller

UTC = datetime.timezone.utc


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


def _insert_log(conn, event="stdout", text="x", inserted_sql="now()"):
    conn.execute(
        "INSERT INTO execution_logs "
        "(execution_id, stage_id, event, text, sequence, created_at, db_inserted_at) "
        f"VALUES ('e1','s1',%s,%s,1, now(), {inserted_sql})",
        (event, text),
    )


def _now(conn, expr="now()"):
    return conn.execute(f"SELECT {expr}").fetchone()[0]


def test_stdio_shape_is_snake_case_with_log_and_type(db, captured):
    with _conn(db) as conn:
        _insert_log(conn, event="stdout", text="hello")
        boot = _now(conn, "now() - interval '10 seconds'")
        last_tick = _now(conn)
        poller._poll_logs(conn, boot, last_tick, {})

    assert len(captured) == 1
    msg = json.loads(captured[0])
    assert msg["type"] == "stdio"
    assert set(msg["payload"].keys()) == {"type", "log", "execution_id", "stage_id"}
    assert msg["payload"]["type"] == "stdout"
    assert msg["payload"]["log"] == "hello"
    assert msg["payload"]["execution_id"] == "e1"
    assert msg["payload"]["stage_id"] == "s1"


def test_execution_finished_line_carries_through_for_ui_transition(db, captured):
    # D10: the UI derives "finished/failed" from stdout content.
    with _conn(db) as conn:
        _insert_log(conn, event="stdout", text="Execution finished")
        boot = _now(conn, "now() - interval '10 seconds'")
        poller._poll_logs(conn, boot, _now(conn), {})
    payload = json.loads(captured[0])["payload"]
    assert payload["type"] == "stdout"
    assert "Execution finished" in payload["log"]


def test_dedup_by_id_across_ticks(db, captured):
    seen = {}
    with _conn(db) as conn:
        _insert_log(conn, text="a")
        _insert_log(conn, text="b")
        boot = _now(conn, "now() - interval '10 seconds'")
        poller._poll_logs(conn, boot, _now(conn), seen)
        assert len(captured) == 2
        # same window again → nothing re-broadcast
        poller._poll_logs(conn, boot, _now(conn), seen)
        assert len(captured) == 2


def test_window_overlap_catches_slightly_late_row(db, captured):
    with _conn(db) as conn:
        _insert_log(conn, text="late", inserted_sql="now() - interval '1 second'")
        boot = _now(conn, "now() - interval '1 hour'")  # floor far in the past
        last_tick = _now(conn)
        poller._poll_logs(conn, boot, last_tick, {})
    assert len(captured) == 1
    assert json.loads(captured[0])["payload"]["log"] == "late"


def test_forward_only_ignores_pre_boot_rows(db, captured):
    with _conn(db) as conn:
        _insert_log(conn, text="history")
        boot = _now(conn)  # boot cursor captured AFTER the historic insert
        last_tick = boot
        poller._poll_logs(conn, boot, last_tick, {})
    assert captured == []


def test_prune_seen_keeps_only_window(db):
    now = datetime.datetime(2026, 1, 1, 12, 0, 0, tzinfo=UTC)
    seen = {
        1: now - datetime.timedelta(seconds=10),  # stale
        2: now - datetime.timedelta(seconds=1),  # within 2s window
    }
    poller._prune_seen(seen, now)
    assert set(seen.keys()) == {2}


def test_start_poller_streams_new_logs(db, captured):
    stop, _thread = poller.start_poller()
    try:
        time.sleep(0.3)  # let the poller capture its boot cursor
        with _conn(db) as conn:
            _insert_log(conn, text="live")
        deadline = time.time() + 3.0
        while time.time() < deadline and not captured:
            time.sleep(0.1)
        assert any(json.loads(m)["payload"]["log"] == "live" for m in captured)
    finally:
        stop.set()
