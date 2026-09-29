"""The auto-replay settles EVERY row the lifecycle watchdog watches.

SUT: :func:`matrx_ai.persistence.replay._fetch_pending` (eligibility) and
:func:`matrx_ai.persistence.replay.replay_pending` in auto mode.

Live evidence (2026-09-28): four ``ops.system_write_failure`` rows sat at
``retry_count=0`` for ~68 hours and the watchdog (``recovered_at IS NULL AND
retry_count < 5``) re-fired on them every hour, because the replay's
error-class filter never selected them, so it neither retried nor gave up:

* two ``coordinator drop: queue_in_phase_errored`` captures — preserved
  byte-for-byte FOR replay, yet no class matched them;
* one inherited ``organization_id`` NOT NULL — classified recoverable by
  ``is_inherited_column_notnull_text`` but never eligible;
* one ``QueryTimeoutError`` whose own write timed out — deliberately excluded
  (ambiguous completion), and so parked below the cap forever.

Breaks these tests name: a self-healing class is dropped from eligibility; a
refused row is left unsettled (neither retried nor quarantined); a refused row
is quarantined without its one ``persistence_replay_quarantined`` capture; or a
human's explicit replay (``ids`` / ``max_attempts=None``) starts quarantining.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import pytest

from matrx_ai.persistence import replay

_DROP = "builtins.RuntimeError: coordinator drop: queue_in_phase_errored"
_INHERITED = (
    'asyncpg.exceptions.NotNullViolationError: null value in column "organization_id" '
    'of relation "observational_memory_event" violates not-null constraint [SQLSTATE 23502]'
)
_OWN_TIMEOUT = "matrx_orm.exceptions.QueryTimeoutError: Query timed out during execute_query"
_UNKNOWN = "builtins.ValueError: something no class names"


def _id_row(row_id: str, error_text: str | None) -> dict[str, Any]:
    return {
        "id": row_id,
        "error_text": error_text,
        "request_id": f"req-{row_id}",
        "table_target": "chat.message",
        "retry_count": 0,
        "failed_at": datetime.now(UTC) - timedelta(hours=68),
        "user_id": None,
        "conversation_id": None,
    }


class _Query:
    def __init__(self, rows: list[dict[str, Any]], by_id: dict[str, dict[str, Any]], kw: dict[str, Any]):
        self._rows = rows
        self._by_id = by_id
        self._kw = dict(kw)

    def filter(self, **kw: Any) -> _Query:
        return _Query(self._rows, self._by_id, {**self._kw, **kw})

    def order_by(self, *_a: Any) -> _Query:
        return self

    def limit(self, *_a: Any) -> _Query:
        return self

    async def values(self, *_cols: str) -> list[dict[str, Any]]:
        if "id" in self._kw:
            return [self._by_id[self._kw["id"]]]
        return list(self._rows)


class _Swf:
    def __init__(self, rows: list[dict[str, Any]]):
        self._rows = rows
        self._by_id = {r["id"]: r for r in rows}

    def filter(self, **kw: Any) -> _Query:
        return _Query(self._rows, self._by_id, kw)


@pytest.mark.asyncio
async def test_every_scanned_row_is_either_eligible_or_handed_back(monkeypatch) -> None:
    rows = [
        _id_row("drop", _DROP),
        _id_row("inherited", _INHERITED),
        _id_row("own-timeout", _OWN_TIMEOUT),
        _id_row("unknown", _UNKNOWN),
        _id_row("empty", None),
    ]
    monkeypatch.setattr(replay, "_swf_model", lambda: _Swf(rows))
    refused: list[dict[str, Any]] = []

    eligible = await replay._fetch_pending(
        retry_errors=replay.RECOVERABLE_RETRY_ERRORS,
        limit=200,
        max_attempts=replay.AUTO_REPLAY_MAX_ATTEMPTS,
        unreplayable=refused,
    )

    assert sorted(r["id"] for r in eligible) == ["drop", "inherited"]
    assert sorted(r["id"] for r in refused) == ["empty", "own-timeout", "unknown"]


@pytest.mark.asyncio
async def test_auto_mode_quarantines_what_it_will_never_replay(monkeypatch) -> None:
    refused_rows = [_id_row("own-timeout", _OWN_TIMEOUT), _id_row("unknown", _UNKNOWN)]

    async def fetch(**kw: Any) -> list[Any]:
        if kw.get("unreplayable") is not None:
            kw["unreplayable"].extend(refused_rows)
        return []

    captures: list[dict[str, Any]] = []
    quarantined: list[tuple[list[str], bool]] = []

    async def capture(exc: Exception, **kw: Any) -> None:
        captures.append(kw)

    async def record(rows: Any, *, max_attempts: int | None, permanent: bool = False) -> int:
        quarantined.append(([r["id"] for r in rows], permanent))
        return len(rows)

    monkeypatch.setattr(replay, "_fetch_pending", fetch)
    monkeypatch.setattr(replay, "_capture_replay_failure", capture)
    monkeypatch.setattr(replay, "_record_failed_attempt", record)
    monkeypatch.setattr(
        "matrx_ai.persistence.queue_helpers._ensure_cx_registered", lambda: None
    )

    report = await replay.replay_pending(
        dry_run=False,
        retry_errors=replay.RECOVERABLE_RETRY_ERRORS,
        limit=200,
        database="matrx",
        max_attempts=replay.AUTO_REPLAY_MAX_ATTEMPTS,
    )

    assert report.quarantined_count == 2
    assert sorted(q[0][0] for q in quarantined) == ["own-timeout", "unknown"]
    assert all(permanent for _, permanent in quarantined)
    assert [c["kind"] for c in captures] == ["persistence_replay_quarantined"] * 2
    assert {c["phase"] for c in captures} == {"unreplayable_class"}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "kwargs",
    [
        {"max_attempts": None},  # a human's force-replay never gives up
        {"max_attempts": replay.AUTO_REPLAY_MAX_ATTEMPTS, "ids": ["x"]},  # per-row admin replay
        {"max_attempts": replay.AUTO_REPLAY_MAX_ATTEMPTS, "dry_run": True},
    ],
)
async def test_a_person_asking_never_triggers_quarantine(monkeypatch, kwargs) -> None:
    seen: dict[str, Any] = {}

    async def fetch(**kw: Any) -> list[Any]:
        seen["unreplayable"] = kw.get("unreplayable")
        return []

    monkeypatch.setattr(replay, "_fetch_pending", fetch)
    monkeypatch.setattr(
        "matrx_ai.persistence.queue_helpers._ensure_cx_registered", lambda: None
    )
    await replay.replay_pending(
        dry_run=kwargs.pop("dry_run", False),
        retry_errors=replay.RECOVERABLE_RETRY_ERRORS,
        database="matrx",
        **kwargs,
    )
    assert seen["unreplayable"] is None
