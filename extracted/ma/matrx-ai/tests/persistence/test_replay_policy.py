from typing import Any

import pytest

from matrx_ai.persistence import replay
from matrx_ai.persistence.replay import RECOVERABLE_RETRY_ERRORS


def test_coordinator_hard_deadline_is_auto_replayable() -> None:
    """A cancelled flush with fully preserved ops must finish after DB recovery."""
    assert any("commit hard-deadline" in marker for marker in RECOVERABLE_RETRY_ERRORS)


def test_query_timeout_replays_the_operation_but_never_a_timed_out_capture() -> None:
    """The line moved on 2026-09-17, and it moved to a FINER place, not a laxer one.

    This test used to assert the blanket opposite — that "QueryTimeoutError"
    never appears in RECOVERABLE_RETRY_ERRORS — on the rationale that an
    unknown COMMIT outcome needs a human. `6fa1cb67bc` split that case in two
    and left the test behind, so the file has been contradicting itself and
    its own third test ever since:

      * The OPERATION timed out, its transaction has already ROLLED BACK, and
        the failure was captured on a fresh connection. The outcome is known,
        not ambiguous, so a bounded replay is the recovery — and a persistent
        failure still hits the five-attempt quarantine.
      * The CAPTURE itself timed out, so what the row says about the
        transaction cannot be trusted. That row is still excluded, by
        `_is_query_timeout_capture_text` at the fetch boundary.

    The exclusion is what protects the unknown-COMMIT case, and
    `test_timeout_head_excludes_recoverable_marker_in_bound_arguments` below
    proves it end to end — including against a marker spoofed into bound
    arguments. So this assertion pins the marker's presence, and that one pins
    the boundary that keeps it honest.
    """
    assert any("QueryTimeoutError" in marker for marker in RECOVERABLE_RETRY_ERRORS)
    assert replay._is_query_timeout_capture_text(
        "matrx_orm.exceptions.QueryTimeoutError: statement timed out"
    )
    assert not replay._is_query_timeout_capture_text(
        "ForeignKeyViolationError: parent not committed [SQLSTATE 23503]"
    )


@pytest.mark.asyncio
async def test_timeout_head_excludes_recoverable_marker_in_bound_arguments(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """User-controlled timeout arguments cannot select an unknown-COMMIT replay."""
    candidates = [
        {
            "id": "timeout-with-spoofed-marker",
            "error_text": "matrx_orm.exceptions.QueryTimeoutError: statement timed out\\n"
            "Args: ['PRIVATE_SENTINEL ForeignKeyViolationError']",
        },
        {
            "id": "real-fk-race",
            "error_text": "ForeignKeyViolationError: parent not committed [SQLSTATE 23503]",
        },
    ]

    class _Query:
        def __init__(self, filters: dict[str, Any]) -> None:
            self.filters = filters

        def filter(self, **kwargs: Any) -> "_Query":
            return _Query({**self.filters, **kwargs})

        def order_by(self, *_: str) -> "_Query":
            return self

        def limit(self, _: int) -> "_Query":
            return self

        async def values(self, *_: str) -> list[dict[str, Any]]:
            row_id = self.filters.get("id")
            if row_id is None:
                return candidates
            return [{**next(row for row in candidates if row["id"] == row_id), "payload": {}}]

    class _Failures:
        @staticmethod
        def filter(**kwargs: Any) -> _Query:
            return _Query(kwargs)

    monkeypatch.setattr(replay, "_swf_model", lambda: _Failures)
    rows = await replay._fetch_pending(
        retry_errors=RECOVERABLE_RETRY_ERRORS,
        limit=10,
        max_attempts=replay.AUTO_REPLAY_MAX_ATTEMPTS,
    )

    assert [row["id"] for row in rows] == ["real-fk-race"]
