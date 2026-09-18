from typing import Any

import pytest

from matrx_ai.persistence import replay
from matrx_ai.persistence.replay import RECOVERABLE_RETRY_ERRORS


def test_coordinator_hard_deadline_is_auto_replayable() -> None:
    """A cancelled flush with fully preserved ops must finish after DB recovery."""
    assert any("commit hard-deadline" in marker for marker in RECOVERABLE_RETRY_ERRORS)


def test_query_timeout_is_not_an_auto_replay_candidate() -> None:
    """Unknown COMMIT outcomes require an explicit human recovery decision."""
    assert not any("QueryTimeoutError" in marker for marker in RECOVERABLE_RETRY_ERRORS)


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
