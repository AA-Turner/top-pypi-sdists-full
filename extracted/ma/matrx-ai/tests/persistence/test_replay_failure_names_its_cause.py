"""A replay failure names its real cause; a root-table NULL org is permanent.

SUT: :func:`matrx_ai.persistence.replay._capture_replay_failure` (via
``_safe_replay_failure_text`` / ``_captured_failure_heads``) and
:func:`matrx_ai.persistence.replay.is_permanent_failure_text`.

Live evidence (2026-11-03, ``system_errors``): 434 ``persistence_replay_quarantined``
rows all read ``RuntimeError: replay execution failed`` and 163
``persistence_replay_failed`` rows all read ``ForeignKeyViolationError: replay
execution failed [SQLSTATE 23503]``. The quarantine REASON, the original
captured failure (a check constraint, a LookupError, a schema drift) and the
FK constraint/table were all thrown away at capture, so no class could be
triaged from the error queue. Separately, ``__tool_test__`` conversations
inserted with no organization were retried five times each as an "inherited
org race" although ``chat.conversation`` inherits its organization from nothing.

Breaks these tests name: the capture collapses back to a bare class name; a
quarantine stops naming the captured failure; row VALUES (``detail=``) or bound
arguments leak into system_error; a NULL org on the root conversation is
treated as a race again.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.persistence import replay


def _fk_violation() -> Exception:
    import asyncpg.exceptions

    exc = asyncpg.exceptions.ForeignKeyViolationError(
        'insert or update on table "request" violates foreign key constraint '
        '"cx_request_user_request_id_fkey"'
    )
    exc.sqlstate = "23503"
    exc.constraint_name = "cx_request_user_request_id_fkey"
    exc.table_name = "request"
    exc.schema_name = "chat"
    exc.detail = "Key (user_request_id)=(PRIVATE_ROW_VALUE) is not present"
    return exc


def _row(error_text: str, *, table: str = "chat.message") -> dict[str, Any]:
    return {
        "id": "row-1",
        "request_id": "request-1",
        "table_target": table,
        "op_type": "insert",
        "error_text": error_text,
        "user_id": None,
        "conversation_id": None,
    }


@pytest.fixture
def captured(monkeypatch) -> dict[str, Any]:
    out: dict[str, Any] = {}

    async def capture_error(exc: Exception, **kwargs: Any) -> None:
        out["text"] = str(exc)
        out.update(kwargs)

    import matrx_connect.streaming.error_capture as error_capture

    monkeypatch.setattr(error_capture, "capture_error", capture_error)
    return out


@pytest.mark.asyncio
async def test_an_fk_replay_failure_names_constraint_and_table(captured) -> None:
    await replay._capture_replay_failure(
        _fk_violation(), request_id="request-1",
        rows=[_row("RuntimeError: coordinator drop: queue_in_phase_errored", table="chat.request")],
        phase="execute",
    )
    text = captured["text"]
    assert "constraint=cx_request_user_request_id_fkey" in text
    assert "table=chat.request" in text
    assert "[SQLSTATE 23503]" in text
    assert "PRIVATE_ROW_VALUE" not in str(captured)
    assert captured["context"]["replay_error"] == text


@pytest.mark.asyncio
async def test_a_quarantine_names_the_reason_and_the_captured_failure(captured) -> None:
    original = (
        "asyncpg.exceptions.CheckViolationError: new row for relation \"message\" "
        'violates check constraint "cx_message_source_check" [SQLSTATE 23514] '
        "constraint=cx_message_source_check table=message detail=Failing row "
        "contains (PRIVATE_MESSAGE_TEXT)"
    )
    await replay._capture_replay_failure(
        RuntimeError("Replay refused: matches no self-healing class."),
        request_id="request-1", rows=[_row(original)],
        phase="unreplayable_class", kind="persistence_replay_quarantined",
    )
    text = captured["text"]
    assert "Replay refused" in text
    assert "cx_message_source_check" in text
    assert "PRIVATE_MESSAGE_TEXT" not in str(captured)
    assert captured["context"]["captured_errors"][0].startswith(
        "asyncpg.exceptions.CheckViolationError"
    )


@pytest.mark.asyncio
async def test_an_orm_banner_never_leaks_its_bound_arguments(captured) -> None:
    from matrx_orm.exceptions import QueryTimeoutError

    await replay._capture_replay_failure(
        QueryTimeoutError(operation="execute_query", query="INSERT …", args=["PRIVATE"]),
        request_id="request-1", rows=[_row("QueryTimeoutError: lock timeout")],
        phase="execute",
    )
    assert "PRIVATE" not in str(captured)
    assert captured["text"] == "QueryTimeoutError: replay execution failed"


_ROOT_ORG_NOTNULL = (
    "asyncpg.exceptions.NotNullViolationError: null value in column "
    '"organization_id" of relation "conversation" violates not-null constraint '
    "[SQLSTATE 23502] table=conversation column=organization_id detail=Failing row"
)


def test_a_null_org_on_the_root_conversation_is_permanent() -> None:
    assert not replay.is_inherited_column_notnull_text(_ROOT_ORG_NOTNULL)
    assert replay.is_permanent_failure_text(_ROOT_ORG_NOTNULL)


def test_a_null_org_on_an_inheriting_child_is_still_a_race() -> None:
    child = _ROOT_ORG_NOTNULL.replace('"conversation"', '"request"').replace(
        "table=conversation", "table=request"
    )
    assert replay.is_inherited_column_notnull_text(child)
    assert not replay.is_permanent_failure_text(child)
