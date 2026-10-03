"""A tool call's stored output is the text the model read — never a Python repr.

Defect (clone census 2026-10-02): ``ToolExecutionLogger._serialize_output`` stored any output that
was not a str / dict / list with ``str()``. A pydantic kind model (``ContextToolResult`` and 36
other tools' result kinds) was stored as ``kind_='context_tool_result' key=…`` — and the turn
rebuild (``_rebuild_tool_result_content``) replays ``chat.tool_call.output`` to the model, so every
later turn read that repr instead of the JSON it had read live. The one serializer is
``tool_output_text``; the live content and the stored row are both built from it.
"""

from __future__ import annotations

import dataclasses
import json
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.db._conversation_rebuild_impl import _rebuild_tool_result_content
from matrx_ai.tools.kinds.context_tools import ContextToolResult, ContextWriteResult
from matrx_ai.tools.logger import ToolExecutionLogger
from matrx_ai.tools.models import ToolResult


@dataclasses.dataclass
class _Plain:
    city: str
    units: int


def _outputs() -> list[Any]:
    return [
        ContextToolResult(
            key="route_brief",
            type="text",
            label="Route Brief",
            content="Départ 06:40 — quai nord.",
            total_chars=25,
        ),
        ContextWriteResult(key="route_brief", command="append", persist="never"),
        {"note": "Départ — naïve café", "rows": [1, 2]},
        ["ünïcode", {"k": 1}],
        _Plain(city="Zürich", units=3),
        "already text",
    ]


def _live_content(output: Any) -> str:
    result = ToolResult(success=True, output=output, call_id="call_1", tool_name="context")
    content = result.to_tool_result_content()["content"]
    assert isinstance(content, str)
    return content


@pytest.mark.parametrize("output", _outputs(), ids=lambda o: type(o).__name__)
def test_the_stored_output_is_the_text_the_model_received(output: Any) -> None:
    stored, output_type, chars = ToolExecutionLogger._serialize_output(output)
    assert stored == _live_content(output)
    assert chars == len(stored)
    if not isinstance(output, str):
        assert output_type == "json"
        json.loads(stored)  # JSON, never a repr
        assert "kind_=" not in stored


@pytest.mark.parametrize("output", _outputs(), ids=lambda o: type(o).__name__)
def test_a_rebuilt_turn_replays_the_bytes_the_model_read_live(output: Any) -> None:
    stored, _type, chars = ToolExecutionLogger._serialize_output(output)
    row = SimpleNamespace(
        output=stored,
        is_error=False,
        model_stub_at=None,
        execution_events=[],
        call_id="call_1",
        tool_name="context",
        output_chars=chars,
        output_preview=None,
    )
    (block,) = _rebuild_tool_result_content([row])  # type: ignore[list-item]
    assert block["content"] == _live_content(output)


def test_a_kind_model_previews_its_json() -> None:
    output = ContextWriteResult(key="route_brief", command="append", persist="never")
    _stored, output_type, chars = ToolExecutionLogger._serialize_output(output)
    preview = ToolExecutionLogger._synthesize_preview(output, output_type, chars)
    assert preview.get("key") == "route_brief"
