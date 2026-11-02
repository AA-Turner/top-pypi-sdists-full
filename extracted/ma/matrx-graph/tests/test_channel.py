from __future__ import annotations

import pytest
from matrx_graph import ChannelError, ChannelSpec, coerce_to_json
from pydantic import BaseModel


class _Msg(BaseModel):
    role: str
    content: str


def test_channel_spec_defaults():
    c = ChannelSpec(name="messages")
    assert c.reducer == "replace"
    assert c.default is None


def test_channel_spec_accepts_json_default():
    c = ChannelSpec(name="counts", default={"a": 1, "b": [1, 2, 3]})
    assert c.default == {"a": 1, "b": [1, 2, 3]}


def test_channel_spec_rejects_non_json_default():
    with pytest.raises(Exception):
        ChannelSpec(name="bad", default=object())


def test_channel_spec_rejects_non_string_keys_in_default():
    with pytest.raises(Exception):
        ChannelSpec(name="bad", default={1: "not-allowed"})


def test_coerce_to_json_dumps_pydantic_model():
    m = _Msg(role="user", content="hi")
    out = coerce_to_json(m)
    assert out == {"role": "user", "content": "hi"}


def test_coerce_to_json_dumps_list_of_models():
    # Nested models inside a list still need explicit dump at the call site;
    # coerce_to_json only walks plain containers.
    models = [_Msg(role="user", content="a"), _Msg(role="bot", content="b")]
    with pytest.raises(ChannelError):
        coerce_to_json(models)


def test_coerce_to_json_rejects_non_json_primitive():
    with pytest.raises(ChannelError):
        coerce_to_json({"created_at": object()})


def test_coerce_to_json_passes_through_json_dict():
    v = {"a": 1, "b": [True, False, None, "x"]}
    assert coerce_to_json(v) == v


def test_channel_spec_reducer_variants():
    for reducer in (
        "replace",
        "append",
        "merge",
        "sum",
        "last_writer_wins",
        "topic_map",
    ):
        ChannelSpec(name=f"ch_{reducer}", reducer=reducer)  # type: ignore[arg-type]


def test_channel_spec_rejects_unknown_reducer():
    with pytest.raises(Exception):
        ChannelSpec(name="bad", reducer="multiply")  # type: ignore[arg-type]
