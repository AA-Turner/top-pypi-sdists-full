"""A tool's result reaches the model without its unset (null) fields — and keeps ``__kind``.

Defect (conversation d1e4226e, 2026-11-12): every successful ``sql`` write sent the model 535 chars
— ``{"__kind": "sql_tool_result", "rows": null, "count": null, "total": null, …, "updated": 1}`` —
twenty-odd null keys around one count, and ``context`` batch results did the same at every nesting
level. ``tool_output_text`` is THE one serialization (the model's text and the stored row), so the
lean shape is decided there: a field is left out only when its value is ``None`` AND its declared
default is ``None`` — so re-reading the JSON yields the same model. A ``None`` that differs from the
default (``DirectoryEntry.size``: default 0, ``None`` = "not reported") stays, as does every
``None`` inside plain data (a row's null column is data).
"""

from __future__ import annotations

import json
import typing

from pydantic import BaseModel
from pydantic_core import PydanticUndefined

from matrx_ai.tools.kinds import TOOL_RESULT_KINDS
from matrx_ai.tools.kinds.context_tools import ContextToolResult
from matrx_ai.tools.kinds.database_tools import SqlToolResult
from matrx_ai.tools.kinds.filesystem import DirectoryEntry
from matrx_ai.tools.models import ToolResult, to_lean_json, tool_output_text


def test_a_write_receipt_carries_only_what_happened() -> None:
    text, output_type = tool_output_text(
        SqlToolResult(updated=1, ids=["6cd9381c-baac-4c31-808e-128c20692bb3"])
    )
    assert output_type == "json"
    assert json.loads(text) == {
        "__kind": "sql_tool_result",
        "updated": 1,
        "ids": ["6cd9381c-baac-4c31-808e-128c20692bb3"],
    }
    assert len(text) < 120, text


def test_nested_kinds_are_lean_and_keep_their_kind() -> None:
    # ``ctx_batch`` nests each sub-read through ``to_lean_json`` (its entry field is a plain dict).
    inner = to_lean_json(ContextToolResult(key="k1", type="text", content="hello"))
    outer = ContextToolResult(count=1, requested=1, results=[{"key": "k1", "success": True, "output": inner}])
    data = json.loads(tool_output_text(outer)[0])
    assert data == {
        "__kind": "context_tool_result",
        "count": 1,
        "requested": 1,
        "results": [
            {
                "key": "k1",
                "success": True,
                "output": {"__kind": "context_tool_result", "key": "k1", "type": "text", "content": "hello"},
            }
        ],
    }


def test_null_data_inside_rows_is_kept() -> None:
    data = json.loads(tool_output_text(SqlToolResult(rows=[{"id": "a", "deleted_at": None}], count=1))[0])
    assert data["rows"] == [{"id": "a", "deleted_at": None}]
    assert "total" not in data


def test_a_null_that_is_not_the_default_is_kept() -> None:
    data = json.loads(tool_output_text(DirectoryEntry(name="x", size=None))[0])
    assert data["size"] is None
    # Re-reading the lean JSON gives back the same model.
    assert DirectoryEntry.model_validate(data) == DirectoryEntry(name="x", size=None)


def test_the_model_reads_the_lean_text() -> None:
    result = ToolResult(success=True, output=SqlToolResult(deleted=2), call_id="c1", tool_name="sql")
    content = result.to_tool_result_content()["content"]
    assert json.loads(content) == {"__kind": "sql_tool_result", "deleted": 2}


def test_plain_dict_output_is_untouched() -> None:
    assert json.loads(tool_output_text({"a": None, "b": 1})[0]) == {"a": None, "b": 1}


def _nullable(annotation: object) -> bool:
    return type(None) in typing.get_args(annotation) or annotation is typing.Any


def test_every_result_kind_round_trips_its_lean_form() -> None:
    """Every model reachable from a registered result kind, built with all defaults, serializes
    lean and re-validates to an equal model: the lean form never changes meaning."""
    seen: set[type[BaseModel]] = set()

    def models_in(annotation: object) -> list[type[BaseModel]]:
        found = [annotation] if isinstance(annotation, type) and issubclass(annotation, BaseModel) else []
        for arg in typing.get_args(annotation):
            found += models_in(arg)
        return found

    def walk(model: type[BaseModel]) -> None:
        if model in seen:
            return
        seen.add(model)
        for field in model.model_fields.values():
            for sub in models_in(field.annotation):
                walk(sub)

    for kind in set(TOOL_RESULT_KINDS.values()):
        walk(kind)
    checked = 0
    for model in seen:
        if not all(
            f.default is not PydanticUndefined or f.default_factory is not None
            for f in model.model_fields.values()
        ):
            continue  # a required field: cannot build with defaults alone
        try:
            instance = model()
        except Exception:
            continue
        nulled = {
            name: None
            for name, f in model.model_fields.items()
            if _nullable(f.annotation) and name != "kind_"
        }
        variant = instance.model_copy(update=nulled)
        lean = json.loads(tool_output_text(variant)[0])
        assert model.model_validate(lean) == variant, model.__name__
        checked += 1
    assert checked > 50


def test_aliased_fields_are_dropped_and_walked() -> None:
    """``to_jsonable_python`` keys a field by its alias; the lean walk must too."""
    from pydantic import Field

    class _Inner(BaseModel):
        z: int | None = None
        y: int = 1

    class _Outer(BaseModel):
        a: int | None = Field(default=None, alias="A")
        n: _Inner | None = Field(default=None, alias="N")

    assert json.loads(tool_output_text(_Outer())[0]) == {}
    assert json.loads(tool_output_text(_Outer(N=_Inner()))[0]) == {"N": {"y": 1}}
