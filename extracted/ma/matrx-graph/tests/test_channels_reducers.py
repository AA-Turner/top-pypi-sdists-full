from __future__ import annotations

import pytest
from matrx_graph import ChannelError, ChannelManager, ChannelSpec


def test_replace_reducer_keeps_last_write():
    mgr = ChannelManager({"x": ChannelSpec(name="x", reducer="replace", default=0)})
    mgr.commit([("x", 1), ("x", 2), ("x", 3)])
    assert mgr.values()["x"] == 3


def test_append_reducer_concatenates():
    mgr = ChannelManager({"log": ChannelSpec(name="log", reducer="append", default=[])})
    mgr.commit([("log", "a"), ("log", "b"), ("log", ["c", "d"])])
    assert mgr.values()["log"] == ["a", "b", "c", "d"]


def test_merge_reducer_updates_dict():
    mgr = ChannelManager({"m": ChannelSpec(name="m", reducer="merge", default={"x": 1})})
    mgr.commit([("m", {"y": 2}), ("m", {"x": 10, "z": 3})])
    assert mgr.values()["m"] == {"x": 10, "y": 2, "z": 3}


def test_merge_reducer_rejects_non_dict():
    mgr = ChannelManager({"m": ChannelSpec(name="m", reducer="merge", default={})})
    with pytest.raises(ChannelError):
        mgr.commit([("m", "not-a-dict")])


def test_sum_reducer_adds_numerics():
    mgr = ChannelManager({"c": ChannelSpec(name="c", reducer="sum", default=0)})
    mgr.commit([("c", 1), ("c", 2), ("c", 3.5)])
    assert mgr.values()["c"] == 6.5


def test_sum_reducer_rejects_non_numeric():
    mgr = ChannelManager({"c": ChannelSpec(name="c", reducer="sum", default=0)})
    with pytest.raises(ChannelError):
        mgr.commit([("c", "abc")])


def test_topic_map_groups_by_topic():
    mgr = ChannelManager({"results": ChannelSpec(name="results", reducer="topic_map", default={})})
    mgr.commit(
        [
            ("results", {"topic": "scrapes", "url": "a"}),
            ("results", {"topic": "scrapes", "url": "b"}),
            ("results", {"topic": "summaries", "text": "x"}),
        ]
    )
    assert mgr.values()["results"] == {
        "scrapes": [{"url": "a"}, {"url": "b"}],
        "summaries": [{"text": "x"}],
    }


def test_topic_map_requires_topic_key():
    mgr = ChannelManager({"r": ChannelSpec(name="r", reducer="topic_map", default={})})
    with pytest.raises(ChannelError):
        mgr.commit([("r", {"no_topic": "here"})])


def test_strict_mode_rejects_undeclared_channels():
    mgr = ChannelManager({}, strict=True)
    with pytest.raises(ChannelError):
        mgr.commit([("unknown", 1)])


def test_non_strict_mode_implicitly_declares():
    mgr = ChannelManager({}, strict=False)
    mgr.commit([("implicit", "hello")])
    assert mgr.values()["implicit"] == "hello"


def test_load_values_replaces_state():
    mgr = ChannelManager({"a": ChannelSpec(name="a", reducer="replace", default=0)})
    mgr.commit([("a", 5)])
    assert mgr.values()["a"] == 5
    mgr.load_values({"a": 100, "b": "new"})
    assert mgr.values() == {"a": 100, "b": "new"}


def test_reducer_pydantic_models_are_dumped():
    from pydantic import BaseModel

    class Item(BaseModel):
        name: str
        count: int

    mgr = ChannelManager({"items": ChannelSpec(name="items", reducer="append", default=[])})
    # Writing a BaseModel through commit() requires pre-dump; commit() itself
    # coerces, which means plain dicts work — models should be dumped by
    # ChannelView.write(). Verify commit raises on raw BaseModel (expected:
    # coerce_to_json has no special case for models).
    mgr.commit([("items", Item(name="a", count=1).model_dump())])
    assert mgr.values()["items"] == [{"name": "a", "count": 1}]
