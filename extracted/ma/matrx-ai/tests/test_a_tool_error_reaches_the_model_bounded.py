"""A failed tool call hands the model a BOUNDED error, however long the exception's text.

Benchmark P6 (live, 2026-11-03, conversation d9af0249): four knowledge_search calls timed out in
the ORM; each error carried the query's 1024-number embedding in its message and traceback, so each
tool_result was 50,864 chars. Those four errors were 200k of the 240k chars of one send; the next
send was refused by the 200,000-token input guard and the person got no answer.

Green only when real: the text checked is exactly what the model and a rebuilt conversation read
(``to_agent_message`` / ``persisted_message``).
"""

from __future__ import annotations

from matrx_ai.tools.models import ToolError

VECTOR = "[" + ",".join(f"{-0.0675 + i / 1e5:.17f}" for i in range(1024)) + "]"
ORM_TEXT = (
    "Matrx ORM  |  QueryTimeoutError\n\nQuery timed out during call_function:rag.recall_vector\n"
    f"  Operation: call_function:rag.recall_vector\n  Args:      ['embeddings_voyage_4_large_1024', '{VECTOR}']\n"
)


def _err() -> ToolError:
    try:
        raise TimeoutError(ORM_TEXT)
    except TimeoutError as exc:
        return ToolError.from_exception(exc, error_type="search_failed", message=f"The passage search failed ({ORM_TEXT})")


def test_the_models_view_of_a_huge_error_is_bounded() -> None:
    err = _err()
    assert len(err.message) > 20_000  # the raw text is kept for the operator surfaces
    for text in (err.to_agent_message(), err.persisted_message()):
        assert len(text) < 8_000, len(text)
        assert "The passage search failed" in text[:120]
        assert "QueryTimeoutError" in text  # what failed survives the cut
        assert "chars cut" in text  # the cut is announced, never silent


def test_a_short_error_is_untouched() -> None:
    err = ToolError(error_type="bad_args", message="The range A1:B is not valid.")
    assert err.to_agent_message() == "TOOL ERROR [bad_args]: The range A1:B is not valid."


async def test_a_call_rejected_before_dispatch_stores_a_bounded_error(monkeypatch) -> None:
    """The pre-dispatch row (``log_rejected``) is what a rebuilt conversation replays to the model
    (``_synthesise_error_content``): it stores the same bounded text as every other error row."""
    from types import SimpleNamespace

    import matrx_ai.tools.logger as logger_mod
    from matrx_ai.tools.logger import ToolExecutionLogger
    from matrx_ai.tools.models import ToolResult

    inserts: list[dict] = []

    async def _no_parents(**kw):
        return None

    coord = SimpleNamespace(queue=lambda *a, **k: "op-1")
    monkeypatch.setattr(logger_mod, "_should_persist_tool_call", lambda: True)
    monkeypatch.setattr(logger_mod, "_ensure_tool_call_parents", _no_parents)
    monkeypatch.setattr(logger_mod, "_get_coordinator", lambda: coord)
    monkeypatch.setattr(logger_mod, "_queue_tool_call_create", lambda **kw: inserts.append(kw))
    monkeypatch.setattr(logger_mod, "stamp_row_owner", lambda data, user_id: None)
    ctx = SimpleNamespace(conversation_id="conv-bounded", request_id="req-1", call_id="toolu_bounded", iteration=1, message_id=None, user_id="u")
    result = ToolResult(success=False, call_id="toolu_bounded", tool_name="knowledge_search", error=_err())
    await ToolExecutionLogger().log_rejected(ctx, tool_name="knowledge_search", arguments={"query": "x"}, result=result)
    assert inserts, "log_rejected must write its row"
    stored = inserts[-1]["error_message"]
    assert len(stored) < 8_000, len(stored)
    assert "chars cut" in stored
