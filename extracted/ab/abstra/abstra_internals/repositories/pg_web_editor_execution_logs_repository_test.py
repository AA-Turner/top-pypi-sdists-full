"""S6 — PgWebEditorExecutionLogsRepository: batching, flush semantics, recovery."""

import importlib
import threading
import time

import pytest

import abstra_internals.environment as environment
import abstra_internals.services.db.connection as connection
import abstra_internals.services.db.migrations as migrations
from abstra_internals.repositories.execution_logs import (
    PgWebEditorExecutionLogsRepository,
)


@pytest.fixture
def repo(monkeypatch, pg_uri):
    monkeypatch.setenv("ABSTRA_WEB_EDITOR_DATABASE_URI", pg_uri)
    importlib.reload(environment)
    importlib.reload(connection)
    importlib.reload(migrations)
    migrations.apply_migrations()
    r = PgWebEditorExecutionLogsRepository()
    yield r
    r._stop.set()
    connection.close_pool()
    monkeypatch.undo()
    importlib.reload(environment)
    importlib.reload(connection)
    importlib.reload(migrations)


# --- DB-backed -------------------------------------------------------------


def test_final_flush_persists_and_orders_by_id(repo):
    for i in range(3):
        repo.insert_stdio("e1", "s1", "stdout", f"line-{i}")
    repo.final_flush()
    logs = repo.get("e1")
    assert [log.payload["text"] for log in logs] == ["line-0", "line-1", "line-2"]


def test_final_flush_empties_buffer(repo):
    repo.insert_stdio("e1", "s1", "stdout", "x")
    repo.final_flush()
    with repo._lock:
        assert len(repo._buffer) == 0


def test_get_event_filter(repo):
    repo.insert_stdio("e1", "s1", "stdout", "out")
    repo.insert_stdio("e1", "s1", "stderr", "err")
    repo.final_flush()
    assert [log.payload["text"] for log in repo.get("e1", event="stdout")] == ["out"]
    assert [log.payload["text"] for log in repo.get("e1", event="stderr")] == ["err"]
    assert len(repo.get("e1")) == 2


def test_periodic_flush_survives_after_final_flush(repo):
    # D5 regression: _final_flush must NOT stop the daemon loop, so a second
    # execution served by the same repo still gets periodic flushing.
    repo.insert_stdio("e1", "s1", "stdout", "first")
    repo.final_flush()
    repo.insert_stdio("e1", "s1", "stdout", "second")
    deadline = time.time() + 3.0
    while time.time() < deadline and len(repo.get("e1")) < 2:
        time.sleep(0.1)
    assert [log.payload["text"] for log in repo.get("e1")] == ["first", "second"]


def test_concurrent_final_flush_no_loss_no_corruption(quiet_repo, monkeypatch):
    # Uses a mock pool so DB connection instability in CI can't cause false negatives.
    # The test validates that the in-memory buffer is not corrupted or silently drained
    # when final_flush() is called concurrently from multiple threads.
    import abstra_internals.services.db.connection as connection

    captured: list = []
    cap_lock = threading.Lock()

    class _CapCur:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def execute(self, sql, params=None):
            if params:
                n = len(params) // 6
                with cap_lock:
                    for i in range(n):
                        captured.append(params[i * 6 + 3])  # text is 4th of 6 params

    class _CapConn:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def cursor(self, **kw):
            return _CapCur()

    class _CapPool:
        def connection(self):
            return _CapConn()

    monkeypatch.setattr(connection, "get_pool", lambda: _CapPool())

    stop = threading.Event()

    def hammer_flush():
        while not stop.is_set():
            quiet_repo.final_flush()

    flushers = [threading.Thread(target=hammer_flush) for _ in range(3)]
    for t in flushers:
        t.start()
    for i in range(100):
        quiet_repo.insert_stdio("e1", "s1", "stdout", f"m{i}")
    stop.set()
    for t in flushers:
        t.join()
    quiet_repo.final_flush()

    assert sorted(captured) == sorted(f"m{i}" for i in range(100))


def test_clear_truncates(repo):
    repo.insert_stdio("e1", "s1", "stdout", "x")
    repo.final_flush()
    repo.clear()
    assert repo.get("e1") == []


# --- Mock-based (no Docker) ------------------------------------------------


class _FakeCur:
    def __init__(self):
        self.calls = []

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def execute(self, sql, params=None):
        self.calls.append((sql, params))


class _FakeConn:
    def __init__(self, cur):
        self._cur = cur

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def cursor(self, **kw):
        return self._cur


class _FakePool:
    def __init__(self, cur):
        self._conn = _FakeConn(cur)

    def connection(self):
        return self._conn


@pytest.fixture
def quiet_repo(monkeypatch):
    """A repo whose daemon flush loop is stopped, for deterministic mock tests."""
    monkeypatch.setenv("ABSTRA_WEB_EDITOR_DATABASE_URI", "postgresql://u:p@h:5432/db")
    importlib.reload(environment)
    importlib.reload(connection)
    r = PgWebEditorExecutionLogsRepository()
    r._stop.set()
    r._flush_thread.join(timeout=1)
    yield r
    monkeypatch.undo()
    importlib.reload(environment)
    importlib.reload(connection)


def test_flush_is_single_multirow_insert(quiet_repo, monkeypatch):
    cur = _FakeCur()
    monkeypatch.setattr(connection, "get_pool", lambda: _FakePool(cur))
    for i in range(3):
        quiet_repo.insert_stdio("e1", "s1", "stdout", f"l{i}")
    quiet_repo._flush()
    assert len(cur.calls) == 1  # one statement for the whole batch
    sql, params = cur.calls[0]
    assert sql.count("(%s,%s,%s,%s,%s,%s)") == 3  # three value groups
    assert len(params) == 3 * 6


def test_flush_is_best_effort_and_recovers_on_next_flush(quiet_repo, monkeypatch):
    cur = _FakeCur()
    calls = {"n": 0}

    def flaky_get_pool():
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("pool down")
        return _FakePool(cur)

    monkeypatch.setattr(connection, "get_pool", flaky_get_pool)

    quiet_repo.insert_stdio("e1", "s1", "stdout", "lost")
    quiet_repo._flush()  # pool down → swallowed, counted as dropped
    assert quiet_repo._dropped == 1
    assert len(cur.calls) == 0

    quiet_repo.insert_stdio("e1", "s1", "stdout", "ok")
    quiet_repo._flush()  # pool back → persists
    assert len(cur.calls) == 1


def test_save_never_raises_when_pool_unavailable(quiet_repo, monkeypatch):
    def boom():
        raise RuntimeError("pool down")

    monkeypatch.setattr(connection, "get_pool", boom)
    quiet_repo.insert_stdio("e1", "s1", "stdout", "x")
    quiet_repo._flush()  # must not raise
    quiet_repo.final_flush()  # must not raise


def test_nul_bytes_are_stripped_before_insert(quiet_repo, monkeypatch):
    cur = _FakeCur()
    monkeypatch.setattr(connection, "get_pool", lambda: _FakePool(cur))
    quiet_repo.insert_stdio("e1", "s1", "stdout", "a\x00b\x00c")
    quiet_repo._flush()
    _, params = cur.calls[0]
    # text is the 4th of each 6-tuple; NUL replaced, no 0x00 reaches Postgres.
    text = params[3]
    assert "\x00" not in text
    assert text == "a�b�c"


def test_large_batch_is_chunked_under_param_cap(quiet_repo, monkeypatch):
    cur = _FakeCur()
    monkeypatch.setattr(connection, "get_pool", lambda: _FakePool(cur))
    n = quiet_repo.MAX_ROWS_PER_INSERT + 1  # forces a second chunk
    for i in range(n):
        quiet_repo.insert_stdio("e1", "s1", "stdout", f"l{i}")
    quiet_repo._flush()
    assert len(cur.calls) == 2  # chunked into two INSERTs
    # every chunk stays within the 65535 bound-parameter wire cap
    for _, params in cur.calls:
        assert len(params) <= 65535
