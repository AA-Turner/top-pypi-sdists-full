"""A failed tool call's system_error row says WHY, and a refusal in words files no row.

2026-11-02: 28 rows read only "Tool execution failed: tables_automation" — every one was the
records store refusing an agent's automation spec in its own words ("That is not a property of
the table it should be set on."), and the sentence lived only in chat.tool_call.
"""

from types import SimpleNamespace

import pytest

from matrx_ai.tools.executor import (
    TOOL_EXECUTION_FAILED_KIND,
    _capture_tool_execution_failed,
    _is_expected_domain_failure,
)


def test_a_refusal_in_words_is_an_expected_domain_failure() -> None:
    for tool in ("tables_automation", "tables_share", "drill", "attention", "spend_desk"):
        assert _is_expected_domain_failure(tool_name=tool, error_type="refused")
    # An operational failure still reaches the repair queue.
    assert not _is_expected_domain_failure(tool_name="tables_automation", error_type="unavailable")
    assert not _is_expected_domain_failure(tool_name="tables_automation", error_type="execution")


@pytest.mark.asyncio
async def test_an_unexpected_failure_row_carries_the_tools_sentence_and_traceback(monkeypatch) -> None:
    captured: list[tuple[BaseException, dict[str, object]]] = []

    async def fake_capture_error(exc: BaseException, **kwargs: object) -> None:
        captured.append((exc, kwargs))

    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", fake_capture_error)
    ctx = SimpleNamespace(request_id="req-1", user_id="user-1", conversation_id="conv-1", call_id="call-1")

    await _capture_tool_execution_failed(
        ctx=ctx,
        tool_name="tables_export",
        error_type="unavailable",
        message="Cloud file sync has no S3 backend.",
        traceback_text="Traceback (most recent call last):\n  boom",
    )

    assert len(captured) == 1
    exc, row = captured[0]
    assert str(exc) == "Tool execution failed: tables_export (unavailable): Cloud file sync has no S3 backend."
    assert row["kind"] == TOOL_EXECUTION_FAILED_KIND
    assert row["traceback_text"] == "Traceback (most recent call last):\n  boom"
    assert row["context"] == {"tool_name": "tables_export", "call_id": "call-1"}
    assert "args" not in repr(row)


def test_a_records_store_refusal_is_an_expected_domain_failure() -> None:
    """2026-11-04: 78 open rows were the records store refusing an agent's call in its own words
    (store_23505 "You already have a column called \\"Patient\\".", store_02000 "There is no
    Employee you can open with that id …", store_23514, store_22023, store_42501)."""
    for code in ("23505", "02000", "23514", "22023", "22004", "PT409", "P0001"):
        assert _is_expected_domain_failure(
            tool_name="records", error_type=f"store_{code}", message="The store said why."
        ), code
    assert _is_expected_domain_failure(
        tool_name="records_read", error_type="store_42501", message="You do not have access to this record."
    )
    # Postgres' own privilege wording is a connection carrying the wrong role: a fault.
    assert not _is_expected_domain_failure(
        tool_name="records_read", error_type="store_42501", message="permission denied for table rows"
    )
    # A lock collision or an aborted transaction is operational, never a refusal.
    for code in ("55P03", "25P02", "57014"):
        assert not _is_expected_domain_failure(tool_name="records", error_type=f"store_{code}"), code


def test_a_read_only_forbidden_or_bad_params_refusal_is_expected() -> None:
    assert _is_expected_domain_failure(tool_name="scope_system", error_type="read_only")
    assert _is_expected_domain_failure(tool_name="kindcomp_patch_code", error_type="forbidden")
    assert _is_expected_domain_failure(tool_name="desktop_git", error_type="invalid_params")


def test_a_policy_permission_refusal_from_any_tool_is_expected() -> None:
    # Live 2026-11-18 (2 rows): actions_run relayed the mail Action's own refusal, typed
    # ``permission`` with a suggested next step, and the executor filed it as a platform error.
    assert _is_expected_domain_failure(
        tool_name="actions_run",
        error_type="permission",
        message="An agent may send mail only from a named inbox it can open.",
    )
    # A real failure of the same tool is still filed.
    assert not _is_expected_domain_failure(tool_name="actions_run", error_type="execution", message="boom")
