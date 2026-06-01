from datetime import datetime

import pytest

from taskchampion import Operation


def test_create():
    o = Operation.Create("10c52749-aec7-4ec9-b390-f371883b9605")
    assert repr(o) == 'Operation.Create(uuid="10c52749-aec7-4ec9-b390-f371883b9605")'
    assert o.is_create()
    assert not o.is_delete()
    assert not o.is_update()
    assert not o.is_undo_point()
    assert o.uuid == "10c52749-aec7-4ec9-b390-f371883b9605"
    with pytest.raises(AttributeError):
        o.old_task
    with pytest.raises(AttributeError):
        o.property
    with pytest.raises(AttributeError):
        o.timestamp
    with pytest.raises(AttributeError):
        o.old_value
    with pytest.raises(AttributeError):
        o.value


def test_delete():
    o = Operation.Delete("10c52749-aec7-4ec9-b390-f371883b9605", {"foo": "bar"})
    assert (
        repr(o)
        == 'Operation.Delete(uuid="10c52749-aec7-4ec9-b390-f371883b9605", old_task={"foo": "bar"})'  # noqa: E501
    )
    assert not o.is_create()
    assert o.is_delete()
    assert not o.is_update()
    assert not o.is_undo_point()
    assert o.uuid == "10c52749-aec7-4ec9-b390-f371883b9605"
    assert o.old_task == {"foo": "bar"}
    with pytest.raises(AttributeError):
        o.property
    with pytest.raises(AttributeError):
        o.timestamp
    with pytest.raises(AttributeError):
        o.old_value
    with pytest.raises(AttributeError):
        o.value


def test_update():
    ts = datetime.fromisoformat("2038-01-19T03:14:07+00:00")
    o = Operation.Update(
        "10c52749-aec7-4ec9-b390-f371883b9605",
        "foo",
        ts,
        "old",
        "new",
    )
    assert (
        repr(o)
        == 'Operation.Update(uuid="10c52749-aec7-4ec9-b390-f371883b9605", property="foo", timestamp="2038-01-19T03:14:07+00:00", old_value="old", value="new")'  # noqa: E501
    )
    assert not o.is_create()
    assert not o.is_delete()
    assert o.is_update()
    assert not o.is_undo_point()
    assert o.uuid == "10c52749-aec7-4ec9-b390-f371883b9605"
    with pytest.raises(AttributeError):
        o.old_task
    assert o.property == "foo"
    assert o.timestamp == ts
    assert o.old_value == "old"
    assert o.value == "new"


def test_update_none():
    ts = datetime.fromisoformat("2038-01-19T03:14:07+00:00")
    o = Operation.Update(
        "10c52749-aec7-4ec9-b390-f371883b9605",
        "foo",
        ts,
        None,
        None,
    )
    assert (
        repr(o)
        == 'Operation.Update(uuid="10c52749-aec7-4ec9-b390-f371883b9605", property="foo", timestamp="2038-01-19T03:14:07+00:00", old_value=None, value=None)'  # noqa: E501
    )
    assert o.old_value is None
    assert o.value is None


def test_undo_point():
    o = Operation.UndoPoint()
    assert repr(o) == "Operation.UndoPoint()"
    assert not o.is_create()
    assert not o.is_delete()
    assert not o.is_update()
    assert o.is_undo_point()
    with pytest.raises(AttributeError):
        o.uuid
    with pytest.raises(AttributeError):
        o.old_task
    with pytest.raises(AttributeError):
        o.property
    with pytest.raises(AttributeError):
        o.timestamp
    with pytest.raises(AttributeError):
        o.old_value
    with pytest.raises(AttributeError):
        o.value
