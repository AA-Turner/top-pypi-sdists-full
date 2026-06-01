import uuid

import pytest

from taskchampion import Operation, Operations, TaskData


@pytest.fixture
def all_ops() -> Operations:
    "Return Operations containing one of each type of operation."
    ops = Operations()
    task = TaskData.create(str(uuid.uuid4()), ops)
    task.update("foo", "new", ops)
    task.delete(ops)
    ops.append(Operation.UndoPoint())
    return ops


def test_constructor():
    ops = Operations()
    assert not ops
    assert len(ops) == 0


def test_repr():
    ops = Operations()
    assert repr(ops) == "Operations([])"
    ops.append(Operation.UndoPoint())
    assert repr(ops) == "Operations([Operation.UndoPoint()])"


def test_len(all_ops: Operations):
    assert all_ops
    assert len(all_ops) == 4


def test_indexing(all_ops: Operations):
    assert all_ops[0].is_create()
    assert all_ops[1].is_update()
    assert all_ops[2].is_delete()
    assert all_ops[3].is_undo_point()
    assert all_ops[-1].is_undo_point()
    assert all_ops[-4].is_create()
    with pytest.raises(IndexError):
        all_ops[4]
    with pytest.raises(IndexError):
        all_ops[-5]
    with pytest.raises(TypeError):
        all_ops["nope"]  # type: ignore[call-overload]


def test_slicing(all_ops: Operations):
    first_two = all_ops[0:2]
    assert isinstance(first_two, Operations)
    assert len(first_two) == 2
    assert first_two[0].is_create()
    assert first_two[1].is_update()

    reversed_ops = all_ops[::-1]
    assert isinstance(reversed_ops, Operations)
    assert len(reversed_ops) == 4
    assert reversed_ops[0].is_undo_point()

    empty = all_ops[10:20]
    assert isinstance(empty, Operations)
    assert len(empty) == 0


def test_iteration(all_ops: Operations):
    seen_undo_point = False
    for op in all_ops:
        print(repr(op))
        if op.is_undo_point():
            seen_undo_point = True
    assert seen_undo_point
