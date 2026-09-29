"""A billed failure reaches the model WITH its resume handle, and a named remedy
never erases a tool's own next step.

Contract: OPENSEO-TOOLS-SPEC §7. The model sees only rendered text (memory law:
agent tools must show the model the whole result), so every assertion here is on
the RENDERED string — ``to_agent_message()`` and the provider ``content`` that
``ToolResult.to_tool_result_content()`` builds — never on a field.

Breaks these tests name:
* ``ToolError.recovery`` missing, or present but never rendered;
* ``annotate_tool_error`` overwriting a tool's own ``suggested_action``;
* the executor's generic placeholder surviving in front of a named remedy.
"""

from __future__ import annotations

import pytest

from matrx_ai.tools.error_remedy import UNDECLARED_ACTOR_SYSTEM, annotate_tool_error
from matrx_ai.tools.models import ToolError, ToolRecovery, ToolResult

LIVE_REFUSAL = (
    "This write declares actor_tier=code, but names no actor_system … "
    "x-matrx-actor-system on the client channel, or the app.actor_system GUC "
    "on a server channel"
)


def _billed() -> ToolError:
    return ToolError(
        error_type="provider_failed",
        message="The keyword research run failed at DataForSEO after it was billed.",
        suggested_action="Call seo_keywords with action='research' and collection_run_id='run-7'.",
        recovery=ToolRecovery(
            handle_type="collection_run",
            handle="run-7",
            resume_cost="free",
            retry_after_seconds=30,
        ),
    )


def test_recovery_is_rendered_into_the_agent_message() -> None:
    text = _billed().to_agent_message()
    assert "Suggested action: Call seo_keywords" in text
    assert "Recovery: call again with collection_run=run-7 (free), retry after 30s" in text


def test_recovery_without_retry_after_has_no_retry_clause() -> None:
    err = ToolError(
        error_type="needs_approval",
        message="Spend above the approval.",
        suggested_action="Call again with spend_approval_id='sa-1'.",
        recovery=ToolRecovery(handle_type="spend_approval", handle="sa-1", resume_cost="paid"),
    )
    text = err.to_agent_message()
    assert text.splitlines()[-1] == "Recovery: call again with spend_approval=sa-1 (paid)"


def test_recovery_reaches_the_provider_content_the_model_reads() -> None:
    result = ToolResult(success=False, error=_billed(), call_id="c1", tool_name="seo_keywords")
    content = result.to_tool_result_content()["content"]
    assert "Recovery: call again with collection_run=run-7 (free)" in content
    assert "Suggested action:" in content


def test_recovery_handle_type_is_closed() -> None:
    with pytest.raises(ValueError):
        ToolRecovery(handle_type="anything", handle="x", resume_cost="free")  # type: ignore[arg-type]


def test_from_exception_keeps_recovery() -> None:
    rec = ToolRecovery(handle_type="provider_task", handle="t-9", resume_cost="free")
    try:
        raise RuntimeError("boom")
    except RuntimeError as exc:
        err = ToolError.from_exception(exc, error_type="x", suggested_action="y", recovery=rec)
    assert "Recovery: call again with provider_task=t-9 (free)" in err.to_agent_message()


def test_annotate_appends_to_a_tools_own_suggested_action() -> None:
    own = "Call cms_page with action='update' and page_id='p1' after fixing the slug."
    err = ToolError(error_type="execution", message=LIVE_REFUSAL, suggested_action=own)
    annotate_tool_error(err)
    assert err.suggested_action == f"{own} Also: {UNDECLARED_ACTOR_SYSTEM.remedy}"
    text = err.to_agent_message()
    assert own in text and UNDECLARED_ACTOR_SYSTEM.remedy in text


def test_annotate_sets_the_remedy_when_the_tool_gave_none() -> None:
    err = ToolError(error_type="execution", message=LIVE_REFUSAL)
    annotate_tool_error(err)
    assert err.suggested_action == UNDECLARED_ACTOR_SYSTEM.remedy


def test_annotate_replaces_the_executors_generic_placeholder() -> None:
    err = ToolError(
        error_type="execution",
        message=LIVE_REFUSAL,
        suggested_action="Check the error details and try with different parameters.",
    )
    annotate_tool_error(err)
    assert err.suggested_action == UNDECLARED_ACTOR_SYSTEM.remedy


def test_annotate_is_idempotent() -> None:
    own = "Call x with y=1."
    err = ToolError(error_type="execution", message=LIVE_REFUSAL, suggested_action=own)
    annotate_tool_error(err)
    once = err.suggested_action
    err.message = LIVE_REFUSAL  # a second pass over the same class
    annotate_tool_error(err)
    assert err.suggested_action == once


def test_a_rebuilt_turn_replays_the_remedy_and_recovery_it_was_shown_live() -> None:
    """The error row the logger persists is what a LATER turn's model sees
    (``_synthesise_error_content`` replays ``error_type: error_message``). It must
    carry the suggested action and the recovery handle, not the bare message."""
    from types import SimpleNamespace

    from matrx_ai.db._conversation_rebuild_impl import _synthesise_error_content
    from matrx_ai.tools.models import ToolError, ToolRecovery

    error = ToolError(
        error_type="provider_failed",
        message="The keyword lookup failed at the provider.",
        suggested_action="Call seo_keywords action 'research' again with resume=abc.",
        recovery=ToolRecovery(handle_type="collection_run", handle="abc", resume_cost="free"),
    )
    row = SimpleNamespace(
        error_type=error.error_type, error_message=error.persisted_message(), tool_name="seo"
    )
    replayed = _synthesise_error_content(row)
    assert "Suggested action: Call seo_keywords" in replayed
    assert "Recovery: call again with collection_run=abc (free)" in replayed


@pytest.mark.asyncio
async def test_the_logger_persists_the_instruction_lines(monkeypatch) -> None:
    from matrx_ai.tools.logger import ToolExecutionLogger
    from matrx_ai.tools.models import ToolError, ToolRecovery, ToolResult

    written: list[dict] = []

    async def capture(self, row_id, data, coordinator=None):
        written.append(data)

    monkeypatch.setattr(ToolExecutionLogger, "_update_row", capture)
    result = ToolResult(
        success=False,
        error=ToolError(
            error_type="provider_failed",
            message="The lookup failed.",
            suggested_action="Call it again with resume=abc.",
            recovery=ToolRecovery(handle_type="collection_run", handle="abc", resume_cost="free"),
        ),
        tool_name="seo_keywords",
        call_id="call-1",
    )
    await ToolExecutionLogger().log_error("row-1", result)
    stored = written[-1]["error_message"]
    assert stored.startswith("The lookup failed.")
    assert "Suggested action: Call it again with resume=abc." in stored
    assert "Recovery: call again with collection_run=abc (free)" in stored
