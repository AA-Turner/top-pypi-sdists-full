"""The engine's knobs: live rows win, an unreadable row degrades LOUDLY.

``workflow.checkpoint_write`` sits inside the write path it protects, so a
missing row must never raise (it would turn a survivable timeout into a hard
failure, and brick a standalone install with no ``platform.feature_knob`` table
at all) — and must never be quiet either.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_graph import knobs


@pytest.fixture(autouse=True)
def _clean() -> Any:
    knobs.clear_knob_cache()
    yield
    knobs.clear_knob_cache()


class _Rows:
    def __init__(self, rows: list[dict[str, Any]] | None, raises: bool = False) -> None:
        self.rows = rows
        self.raises = raises

    def filter(self, **_kwargs: Any) -> _Rows:
        return self

    async def values(self, *_columns: str) -> list[dict[str, Any]]:
        if self.raises:
            raise RuntimeError("relation \"platform.feature_knob\" does not exist")
        return self.rows or []


@pytest.mark.asyncio
async def test_live_rows_are_used(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        knobs,
        "_feature_knob_model",
        lambda: _Rows(
            [
                {"key": "statement_timeout_ms", "value": 45000},
                {"key": "max_retries", "value": 3},
                {"key": "retry_backoff_ms", "value": 100},
                {"key": "warn_bytes", "value": 2_097_152},
            ]
        ),
    )
    policy = await knobs.checkpoint_write_policy()
    assert policy.statement_timeout_ms == 45_000
    assert policy.statement_timeout_seconds == 45.0
    assert policy.max_retries == 3
    assert policy.warn_bytes == 2_097_152


@pytest.mark.asyncio
async def test_an_unreadable_table_degrades_loudly_not_silently(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    monkeypatch.setattr(knobs, "_feature_knob_model", lambda: _Rows(None, raises=True))
    with caplog.at_level("ERROR", logger="matrx_graph.knobs"):
        policy = await knobs.checkpoint_write_policy()
    assert policy == knobs.STARTING_CHECKPOINT_POLICY
    assert any("REMEDY" in r.getMessage() for r in caplog.records)


@pytest.mark.asyncio
async def test_a_missing_key_names_it(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    monkeypatch.setattr(
        knobs,
        "_feature_knob_model",
        lambda: _Rows([{"key": "max_retries", "value": 3}]),
    )
    with caplog.at_level("ERROR", logger="matrx_graph.knobs"):
        policy = await knobs.checkpoint_write_policy()
    assert policy == knobs.STARTING_CHECKPOINT_POLICY
    assert any("statement_timeout_ms" in r.getMessage() for r in caplog.records)


@pytest.mark.asyncio
async def test_an_absurd_value_is_clamped_not_obeyed(monkeypatch: pytest.MonkeyPatch) -> None:
    """An admin cannot hand the engine a 3-hour statement ceiling by typo."""
    monkeypatch.setattr(
        knobs,
        "_feature_knob_model",
        lambda: _Rows(
            [
                {"key": "statement_timeout_ms", "value": 99_999_999},
                {"key": "max_retries", "value": 500},
                {"key": "retry_backoff_ms", "value": 0},
                {"key": "warn_bytes", "value": 1},
            ]
        ),
    )
    policy = await knobs.checkpoint_write_policy()
    assert policy.statement_timeout_ms == 600_000
    assert policy.max_retries == 10
    assert policy.retry_backoff_ms == 1
    assert policy.warn_bytes == 1_024


def test_backoff_is_jittered_and_bounded() -> None:
    policy = knobs.STARTING_CHECKPOINT_POLICY
    for attempt in range(5):
        value = policy.backoff_seconds(attempt)
        assert 0.0 <= value <= 10.0
