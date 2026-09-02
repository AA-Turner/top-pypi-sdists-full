"""A long, expensive run must not start when it cannot be made durable.

2026-08 incident: history.row_versions ran out of partitions, so every INSERT on
a versioned table (including chat.agent_run) failed. RunCheckpointer.start
swallowed that and returned a NullCheckpointer with run_id="". Podcast runs then
spent minutes of paid script/TTS/image calls while being unlistable, unopenable
and unresumable — the user's "I leave the page and can never find the run again".
"""

from __future__ import annotations

import pytest

from matrx_ai.agent_runners._checkpoint import (
    DurableRunUnavailable,
    NullCheckpointer,
    RunCheckpointer,
)


class _BrokenRuns:
    async def create_item(self, **_kwargs: object) -> object:
        raise RuntimeError('no partition of relation "row_versions" found for row')


class _BrokenArm:
    runs = _BrokenRuns()


@pytest.fixture
def broken_db(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "matrx_ai.agent_runners._checkpoint._arm",
        lambda: _BrokenArm(),
    )


@pytest.mark.asyncio
async def test_require_durable_refuses_instead_of_degrading(broken_db: None) -> None:
    with pytest.raises(DurableRunUnavailable) as excinfo:
        await RunCheckpointer.start(
            kind="podcast",
            user_id="u1",
            request={},
            require_durable=True,
        )

    # The refusal must say what happened and that nothing was charged.
    text = str(excinfo.value)
    assert "row_versions" in text
    assert "Nothing was charged" in text


@pytest.mark.asyncio
async def test_refusal_carries_a_named_error_info_for_the_stream(broken_db: None) -> None:
    """The streaming handler reads exc.error_info; without it the client gets
    'failed unexpectedly. Please try again or adjust your settings.' — advice
    that cannot possibly help when the database is down."""
    with pytest.raises(DurableRunUnavailable) as excinfo:
        await RunCheckpointer.start(
            kind="podcast", user_id="u1", request={}, require_durable=True
        )

    info = excinfo.value.error_info
    assert info.error_type == "durable_run_unavailable"
    assert info.is_retryable is False
    assert "nothing was charged" in info.user_message.lower()


@pytest.mark.asyncio
async def test_default_still_degrades_for_standalone_use(broken_db: None) -> None:
    """Without require_durable the old behaviour stands: no DB, no resume, but
    the pipeline still runs (standalone package use, tests, no registry)."""
    ckpt = await RunCheckpointer.start(kind="research", user_id="u1", request={})
    assert isinstance(ckpt, NullCheckpointer)
    assert ckpt.run_id == ""
