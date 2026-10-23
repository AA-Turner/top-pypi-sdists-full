"""Watch AI raw capture over ONE tool call (matrx_utils.raw_capture + ToolExecutor.execute).

Fixture: a real recorded ``web`` read (chat.tool_call b8393cef…, copied by SELECT). Nothing is
called: ``_execute_pipeline`` is replaced by a stand-in that does what the real read did — window
the page text through the real ``window_page_content`` and gate the content through ``_note_gate_cut``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from matrx_utils import raw_capture

from matrx_ai.tools.executor import ToolExecutor, _note_gate_cut
from matrx_ai.tools.implementations._web_read_caps import window_page_content
from matrx_ai.tools.models import ToolContext, ToolResult, tool_output_text

FIXTURE = json.loads((Path(__file__).parent / "fixtures/raw_capture/web_read_tool_call.json").read_text())


class _Logger:
    def row_id_for_call(self, ctx: ToolContext) -> str:
        return FIXTURE["tool_call"]["id"]


@pytest.fixture
def delivered(monkeypatch: pytest.MonkeyPatch) -> list[raw_capture.CaptureScope]:
    got: list[raw_capture.CaptureScope] = []
    raw_capture.register_raw_capture_sink(got.append)
    yield got
    raw_capture.clear_raw_capture_sink()


def _executor(pipeline: Any) -> ToolExecutor:
    executor = ToolExecutor(registry=object(), execution_logger=_Logger())
    executor._execute_pipeline = pipeline  # type: ignore[method-assign]
    return executor


def _ctx() -> ToolContext:
    return ToolContext(call_id=FIXTURE["tool_call"]["call_id"], tool_name="web", iteration=1)


async def test_an_uncut_result_points_at_the_stored_row_and_names_every_size(delivered) -> None:
    output = FIXTURE["output"]
    page = output["pages"][0]

    async def pipeline(*_a: Any, **_k: Any) -> tuple[dict[str, Any], ToolResult]:
        # The real windowing of the recorded page text at the call's own chars=3000 … at a smaller
        # window, so the read's cut shows: the page text recorded here IS the 3,000 chars stored.
        window_page_content(page["content"], url=page["url"], chars=2_000)
        result = ToolResult(success=True, output=output, tool_name="web", call_id=_ctx().call_id)
        content = result.to_tool_result_content()
        _note_gate_cut(content["content"], content["content"], truncated=False)
        return content, result

    await _executor(pipeline).execute("web", FIXTURE["tool_call"]["arguments"], _ctx())

    (scope,) = delivered
    assert scope.target["row_id"] == FIXTURE["tool_call"]["id"]
    assert scope.target["call_id"] == "toolu_01L4LiS8WM9dNcak5ZZdwfyu"
    assert scope.facts["result_chars"] == FIXTURE["tool_call"]["output_chars"] == 3796
    assert scope.facts["sent_chars"] == 3796
    assert scope.facts["gate_truncated"] is False
    cut = scope.cuts[0].as_dict()
    assert cut["where"] == "web read window" and cut["before"] == 3000 and cut["after"] == 2000
    labels = [i.label for i in scope.items]
    assert "Before web read window · " + page["url"] in labels
    whole = next(i for i in scope.items if i.label == "Tool result as returned")
    # Nothing cut for storage or by the gate → RAW is the stored row itself, never a copy.
    assert whole.data is None and whole.ref == {"table": "chat.tool_call", "column": "output", "chars": 3796}


async def test_a_gate_cut_keeps_the_whole_result_and_the_pre_cut_text(delivered) -> None:
    # The recorded page, repeated past the 50,000-char soft cap (a records_read of 406,747 chars on
    # 2026-10-13 reached the model as 55,099 and its whole copy expired with a 30-minute cache).
    big = {"rows": [FIXTURE["output"]["pages"][0]] * 20}
    full_text, _ = tool_output_text(big)
    assert len(full_text) > 50_000

    async def pipeline(*_a: Any, **_k: Any) -> tuple[dict[str, Any], ToolResult]:
        result = ToolResult(success=True, output=big, tool_name="records_read", call_id=_ctx().call_id)
        content = result.to_tool_result_content()
        sent = {**content, "content": content["content"][:50_000] + "\n\n[notice]"}
        _note_gate_cut(content["content"], sent["content"], truncated=True)
        return sent, result

    await _executor(pipeline).execute("records_read", {}, _ctx())

    (scope,) = delivered
    gate = next(c for c in scope.cuts if c.where == "size gate")
    assert gate.before == len(full_text) and gate.after == 50_000 + len("\n\n[notice]")
    assert gate.limit_name == "TOOL_RESULT_SOFT_CAP_CHARS"
    whole = next(i for i in scope.items if i.label == "Tool result as returned")
    assert whole.data == full_text.encode("utf-8")
    assert any(i.label == "Before size gate" for i in scope.items)


async def test_without_a_sink_nothing_is_kept_and_the_call_is_unchanged() -> None:
    raw_capture.clear_raw_capture_sink()

    async def pipeline(*_a: Any, **_k: Any) -> tuple[dict[str, Any], ToolResult]:
        result = ToolResult(success=True, output=FIXTURE["output"], tool_name="web", call_id="c")
        return result.to_tool_result_content(), result

    content, result = await _executor(pipeline).execute("web", {}, _ctx())
    assert result.output == FIXTURE["output"]
    assert raw_capture.current_scope() is None
