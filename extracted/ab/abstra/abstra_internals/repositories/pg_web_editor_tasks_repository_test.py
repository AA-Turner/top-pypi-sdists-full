"""S4 — PgWebEditorTasksRepository: contract parity, atomic lock, error parity."""

import importlib
import threading

import pytest

import abstra_internals.environment as environment
import abstra_internals.services.db.connection as connection
import abstra_internals.services.db.migrations as migrations
from abstra_internals.repositories.tasks import (
    PgWebEditorTasksRepository,
    TaskLockFailed,
)


@pytest.fixture
def repo(monkeypatch, pg_uri):
    monkeypatch.setenv("ABSTRA_WEB_EDITOR_DATABASE_URI", pg_uri)
    importlib.reload(environment)
    importlib.reload(connection)
    importlib.reload(migrations)
    migrations.apply_migrations()
    yield PgWebEditorTasksRepository()
    connection.close_pool()
    monkeypatch.undo()
    importlib.reload(environment)
    importlib.reload(connection)
    importlib.reload(migrations)


def _send(repo, **kw):
    defaults = dict(
        type="form",
        payload={"a": 1},
        target_stage_id="stage-1",
        source_stage_id="src-1",
        execution_id="exec-1",
    )
    defaults.update(kw)
    return repo.send_task(**defaults)


def test_send_and_get_by_id(repo):
    task = _send(repo)
    assert task.status == "pending"
    fetched = repo.get_by_id(task.id)
    assert fetched.id == task.id
    assert fetched.payload == {"a": 1}
    assert fetched.target_stage_id == "stage-1"
    assert fetched.created.by_execution_id == "exec-1"
    assert fetched.created.by_stage_id == "src-1"
    assert fetched.locked is None
    assert fetched.completed is None


def test_get_by_id_not_found(repo):
    with pytest.raises(Exception) as exc:
        repo.get_by_id("nope")
    assert "Task with id nope not found" in str(exc.value)


def test_lock_complete_pending_cycle(repo):
    task = _send(repo)
    repo.lock_task(task.id, execution_id="e2", stage_id="s2")
    locked = repo.get_by_id(task.id)
    assert locked.status == "locked"
    assert locked.locked.by_execution_id == "e2"
    repo.complete_task(task.id, execution_id="e3", stage_id="s3")
    completed = repo.get_by_id(task.id)
    assert completed.status == "completed"
    assert completed.completed.by_stage_id == "s3"
    repo.set_task_to_pending(task.id)
    assert repo.get_by_id(task.id).status == "pending"


def test_lock_already_locked_message(repo):
    task = _send(repo)
    repo.lock_task(task.id, "e", "s")
    with pytest.raises(TaskLockFailed) as exc:
        repo.lock_task(task.id, "e", "s")
    assert str(exc.value) == f"Task {task.id} has already locked"


def test_complete_not_pending_nor_locked_message(repo):
    task = _send(repo)
    repo.complete_task(task.id, "e", "s")
    with pytest.raises(TaskLockFailed) as exc:
        repo.complete_task(task.id, "e", "s")
    assert str(exc.value) == f"Task {task.id} has not been pending nor locked"


def test_set_pending_not_completed_message(repo):
    task = _send(repo)
    with pytest.raises(TaskLockFailed) as exc:
        repo.set_task_to_pending(task.id)
    assert str(exc.value) == f"Task {task.id} is not completed"


def test_lock_missing_task_raises_not_found(repo):
    with pytest.raises(Exception) as exc:
        repo.lock_task("ghost", "e", "s")
    assert "Task with id ghost not found" in str(exc.value)


def test_atomic_lock_only_one_winner(repo):
    task = _send(repo)
    results = []

    def attempt():
        try:
            repo.lock_task(task.id, "e", "s")
            results.append("ok")
        except TaskLockFailed:
            results.append("failed")

    threads = [threading.Thread(target=attempt) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert results.count("ok") == 1
    assert results.count("failed") == 7


def test_where_filter_payload_containment(repo):
    _send(repo, payload={"kind": "a", "n": 1})
    _send(repo, payload={"kind": "b", "n": 2})
    matched = repo.get_pending_tasks("stage-1", None, 0, {"kind": "a"})
    assert len(matched) == 1
    assert matched[0].payload["kind"] == "a"
    # empty where matches all
    all_pending = repo.get_pending_tasks("stage-1", None, 0, {})
    assert len(all_pending) == 2


def test_where_uses_top_level_equality_not_containment(repo):
    # Local _where_matches is strict equality; nested/list values must NOT match
    # by jsonb containment (the old `@>` behavior would wrongly include these).
    _send(repo, payload={"meta": {"x": 1, "y": 2}})
    _send(repo, payload={"tags": ["a", "b"]})
    # nested subset would match under @>, must NOT match under equality
    assert repo.get_pending_tasks("stage-1", None, 0, {"meta": {"x": 1}}) == []
    # list subset would match under @>, must NOT match under equality
    assert repo.get_pending_tasks("stage-1", None, 0, {"tags": ["a"]}) == []
    # exact nested/list values DO match
    assert (
        len(repo.get_pending_tasks("stage-1", None, 0, {"meta": {"x": 1, "y": 2}})) == 1
    )
    assert len(repo.get_pending_tasks("stage-1", None, 0, {"tags": ["a", "b"]})) == 1


def test_pending_ordering_and_pagination(repo):
    a = _send(repo, payload={"i": 0})
    b = _send(repo, payload={"i": 1})
    c = _send(repo, payload={"i": 2})
    # newest first
    ordered = repo.get_pending_tasks("stage-1", None, 0, {})
    assert [t.id for t in ordered] == [c.id, b.id, a.id]
    # limit + offset
    page = repo.get_pending_tasks("stage-1", 1, 1, {})
    assert [t.id for t in page] == [b.id]


def test_sent_and_stage_and_all_and_execution_queries(repo):
    t1 = _send(
        repo, source_stage_id="src-X", target_stage_id="stage-1", execution_id="ex-1"
    )
    t2 = _send(
        repo, source_stage_id="src-Y", target_stage_id="stage-2", execution_id="ex-2"
    )
    assert {t.id for t in repo.get_sent_tasks("src-X", None, 0, {})} == {t1.id}
    assert {t.id for t in repo.get_stage_tasks("stage-2")} == {t2.id}
    assert {t.id for t in repo.get_all_tasks()} == {t1.id, t2.id}
    assert {t.id for t in repo.get_execution_sent_tasks("ex-1")} == {t1.id}


def test_set_locked_tasks_to_pending(repo):
    t = _send(repo)
    repo.lock_task(t.id, "exec-9", "s")
    repo.set_locked_tasks_to_pending("exec-9")
    assert repo.get_by_id(t.id).status == "pending"


def test_clear_truncates(repo):
    _send(repo)
    _send(repo)
    repo.clear()
    assert repo.get_all_tasks() == []
