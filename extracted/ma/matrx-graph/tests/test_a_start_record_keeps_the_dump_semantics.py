"""A step's node_started record is what the old full dump gave — only cheaper (review 6h, M1).

L-SPEED 6e part 2 recorded an argument that parsed equal to the delivered object AS that object, skipping its dump.
The review found three ways that changed the record: a datetime / tuple leaf stayed raw (the dump made an ISO
string / a list), a NaN stayed NaN (the dump made null), and a ``Field(exclude=True)`` argument appeared (the dump
left it out). Sharing now needs a JSON-native value and a field whose dump is its value (no exclude, no custom
serializer). Differential: old record == new record on every case; plain JSON rows are still shared, not dumped.
Red before: 5 of the cases differ.
"""

from __future__ import annotations

import datetime
import json
from typing import Annotated, Any

import pytest
from pydantic import BaseModel, ConfigDict, Field, JsonValue, PlainSerializer, field_serializer

from matrx_graph.executor.json_dump import model_dump_json
from matrx_graph.executor.scheduler import _share_delivered, _started_dump


class Open(BaseModel):
    model_config = ConfigDict(extra="allow")
    rows: list[JsonValue] = Field(default_factory=list)


class AnyRows(BaseModel):
    model_config = ConfigDict(extra="allow")
    rows: list[Any] = Field(default_factory=list)


class Hidden(BaseModel):
    rows: list[dict[str, Any]] = Field(default_factory=list, exclude=True)
    name: str = "x"


class Serialized(BaseModel):
    rows: list[dict[str, Any]] = Field(default_factory=list)

    @field_serializer("rows")
    def _rows(self, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [{"n": len(rows)}]


class Plain(BaseModel):
    rows: Annotated[list[dict[str, Any]], PlainSerializer(lambda v: {"count": len(v)})] = Field(default_factory=list)


CASES: dict[str, tuple[type[BaseModel], dict[str, Any]]] = {
    "extra with datetime leaf": (Open, {"blob": [{"at": datetime.datetime(2026, 1, 1)}]}),
    "extra with tuple leaf": (Open, {"blob": [{"pair": (1, 2)}]}),
    "list[Any] with NaN": (AnyRows, {"rows": [{"v": float("nan")}]}),
    "list[Any] with date": (AnyRows, {"rows": [{"at": datetime.date(2026, 1, 1)}]}),
    "Field(exclude=True)": (Hidden, {"rows": [{"secret": "s"}]}),
    "field_serializer": (Serialized, {"rows": [{"a": 1}, {"a": 2}]}),
    "PlainSerializer": (Plain, {"rows": [{"a": 1}]}),
    "int keys": (AnyRows, {"rows": [{1: "a"}]}),
    "plain JSON rows": (Open, {"rows": [{"a": 1}], "blob": {"k": [1, 2]}}),
}


def _js(value: Any) -> str:
    try:
        return json.dumps(value, allow_nan=False, sort_keys=True)
    except Exception as e:  # noqa: BLE001
        return f"<not JSON: {type(e).__name__}>"


@pytest.mark.parametrize("name", list(CASES))
def test_the_start_record_equals_the_full_dump(name: str) -> None:
    cls, delivered = CASES[name]
    model = cls.model_validate(delivered)
    old = _share_delivered(model_dump_json(model), delivered)
    new = _share_delivered(_started_dump(model, delivered, "test"), delivered)
    assert _js(new) == _js(old), name
    assert list(new) == list(old), f"{name}: key order"


def test_plain_json_rows_are_shared_not_dumped() -> None:
    delivered = {"rows": [{"a": i, "b": [1.5, None, True]} for i in range(100)]}
    model = Open.model_validate(delivered)
    out = _started_dump(model, delivered, "test")
    assert out["rows"] is delivered["rows"], "an unchanged JSON-native argument is recorded as delivered, never dumped"
