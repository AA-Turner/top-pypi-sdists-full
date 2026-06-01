import uuid
from pathlib import Path

import pytest

from taskchampion import AccessMode, Operation, Operations, Replica, Status


@pytest.fixture
def empty_replica() -> Replica:
    return Replica.new_in_memory()


@pytest.fixture
def replica_with_tasks(empty_replica: Replica):
    ops = Operations()
    _ = empty_replica.create_task(str(uuid.uuid4()), ops)
    _ = empty_replica.create_task(str(uuid.uuid4()), ops)
    _ = empty_replica.create_task(str(uuid.uuid4()), ops)
    empty_replica.commit_operations(ops)

    return empty_replica


def test_constructor(tmp_path: Path):
    r = Replica.new_on_disk(str(tmp_path), True)
    assert r is not None


def test_sync_to_local(tmp_path: Path):
    u = str(uuid.uuid4())
    r = Replica.new_in_memory()
    ops = Operations()
    r.create_task(u, ops)
    r.commit_operations(ops)
    r.sync_to_local(str(tmp_path), False)

    # Verify that task syncs to another replica.
    r2 = Replica.new_in_memory()
    r2.sync_to_local(str(tmp_path), False)
    task = r2.get_task(u)
    assert task


def test_constructor_throws_error_with_missing_database(tmp_path: Path):
    with pytest.raises(RuntimeError):
        Replica.new_on_disk(str(tmp_path), False)


def test_read_only(tmp_path: Path):
    r = Replica.new_on_disk(str(tmp_path), True, AccessMode.ReadOnly)
    ops = Operations()
    r.create_task(str(uuid.uuid4()), ops)
    with pytest.raises(RuntimeError):
        r.commit_operations(ops)


def test_create_task(empty_replica: Replica):
    u = uuid.uuid4()

    ops = Operations()
    _ = empty_replica.create_task(str(u), ops)
    empty_replica.commit_operations(ops)

    tasks = empty_replica.all_task_uuids()

    assert len(tasks) == 1


def test_all_task_uuids(empty_replica: Replica):
    ops = Operations()
    _ = empty_replica.create_task(str(uuid.uuid4()), ops)
    _ = empty_replica.create_task(str(uuid.uuid4()), ops)
    _ = empty_replica.create_task(str(uuid.uuid4()), ops)
    empty_replica.commit_operations(ops)
    tasks = empty_replica.all_task_uuids()
    assert len(tasks) == 3


def test_all_tasks(empty_replica: Replica):
    ops = Operations()
    _ = empty_replica.create_task(str(uuid.uuid4()), ops)
    _ = empty_replica.create_task(str(uuid.uuid4()), ops)
    _ = empty_replica.create_task(str(uuid.uuid4()), ops)
    empty_replica.commit_operations(ops)

    tasks = empty_replica.all_tasks()

    assert len(tasks) == 3
    keys = tasks.keys()

    for key in keys:
        assert tasks[key] != 0


def test_get_task(replica_with_tasks: Replica):
    uuid = replica_with_tasks.all_task_uuids()[0]

    task = replica_with_tasks.get_task(uuid)

    assert task is not None


def test_num_local_operations(replica_with_tasks: Replica):
    assert replica_with_tasks.num_local_operations() == 3

    ops = Operations()
    _ = replica_with_tasks.create_task(str(uuid.uuid4()), ops)
    replica_with_tasks.commit_operations(ops)

    assert replica_with_tasks.num_local_operations() == 4


def test_num_undo_points(replica_with_tasks: Replica):
    assert replica_with_tasks.num_undo_points() == 0

    ops = Operations()
    ops.append(Operation.UndoPoint())
    replica_with_tasks.commit_operations(ops)

    assert replica_with_tasks.num_undo_points() == 1


def test_pending_tasks(empty_replica: Replica):
    ops = Operations()
    t1 = empty_replica.create_task(str(uuid.uuid4()), ops)
    t1.set_status(Status.Pending, ops)
    t2 = empty_replica.create_task(str(uuid.uuid4()), ops)
    t2.set_status(Status.Completed, ops)
    empty_replica.commit_operations(ops)

    pending = empty_replica.pending_tasks()
    assert len(pending) == 1
    assert pending[0].get_uuid() == t1.get_uuid()


def test_pending_task_data(empty_replica: Replica):
    ops = Operations()
    t1 = empty_replica.create_task(str(uuid.uuid4()), ops)
    t1.set_status(Status.Pending, ops)
    t2 = empty_replica.create_task(str(uuid.uuid4()), ops)
    t2.set_status(Status.Completed, ops)
    empty_replica.commit_operations(ops)

    pending = empty_replica.pending_task_data()
    assert len(pending) == 1
    assert pending[0].get_uuid() == t1.get_uuid()


def test_get_task_operations(empty_replica: Replica):
    u = str(uuid.uuid4())
    ops = Operations()
    t = empty_replica.create_task(u, ops)
    t.set_status(Status.Pending, ops)
    t.set_description("hello", ops)
    empty_replica.commit_operations(ops)

    task_ops = empty_replica.get_task_operations(u)
    assert len(task_ops) > 0
    assert any(op.is_create() for op in (task_ops[i] for i in range(len(task_ops))))


def test_undo(empty_replica: Replica):
    u = str(uuid.uuid4())

    ops = Operations()
    ops.append(Operation.UndoPoint())
    empty_replica.commit_operations(ops)

    ops = Operations()
    empty_replica.create_task(u, ops)
    empty_replica.commit_operations(ops)
    assert empty_replica.get_task(u) is not None

    undo_ops = empty_replica.get_undo_operations()
    assert len(undo_ops) > 0
    assert empty_replica.commit_reversed_operations(undo_ops) is True
    assert empty_replica.get_task(u) is None


def test_expire_tasks(empty_replica: Replica):
    empty_replica.expire_tasks()

    u = str(uuid.uuid4())
    ops = Operations()
    task = empty_replica.create_task(u, ops)
    task.set_status(Status.Deleted, ops)
    empty_replica.commit_operations(ops)

    empty_replica.expire_tasks()
    assert empty_replica.get_task(u) is not None


def test_rebuild_working_set(empty_replica: Replica):
    ops = Operations()
    t1 = empty_replica.create_task(str(uuid.uuid4()), ops)
    t1.set_status(Status.Pending, ops)
    t2 = empty_replica.create_task(str(uuid.uuid4()), ops)
    t2.set_status(Status.Completed, ops)
    empty_replica.commit_operations(ops)

    empty_replica.rebuild_working_set(False)
    assert not empty_replica.working_set().is_empty()

    empty_replica.rebuild_working_set(True)
    assert not empty_replica.working_set().is_empty()


def test_sync_to_remote_invalid_uuid(empty_replica: Replica):
    """Smoke test: sync_to_remote exists, signature accepted, error path works.

    Uses an invalid UUID for client_id, which fails at uuid2tc parse before
    any network call is made.
    """
    with pytest.raises(ValueError):
        empty_replica.sync_to_remote(
            "http://example.invalid/", "not-a-valid-uuid", "secret", False
        )


def test_sync_to_gcp_invalid_credentials(empty_replica: Replica):
    """Smoke test: sync_to_gcp exists, signature accepted, error path works.

    Uses a non-existent credential path, which fails during ServerConfig
    instantiation before any network call is made.
    """
    with pytest.raises(RuntimeError):
        empty_replica.sync_to_gcp(
            "no-such-bucket", "/no/such/credentials.json", "secret", False
        )
