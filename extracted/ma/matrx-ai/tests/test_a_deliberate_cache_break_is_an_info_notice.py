"""A deliberate prompt-cache break (the Holder or the org catalog changed) is a lawful,
recorded event, never an open error row: it reaches ``record_error`` marked
``context.severity == "info"``, which the capture door logs instead of filing
(2026-11-17: every Chief of Staff save filed a ``prompt_cache_deliberate_break`` row)."""

from __future__ import annotations

import pytest

from matrx_ai import _ext
from matrx_ai.providers import cache_guard


@pytest.mark.asyncio
async def test_a_deliberate_break_is_captured_as_info(monkeypatch) -> None:
    captured: list[dict] = []

    def fake_record_error(exc, **kwargs):
        captured.append(kwargs)

    monkeypatch.setitem(_ext._EXT if hasattr(_ext, "_EXT") else {}, "record_error", fake_record_error)
    monkeypatch.setattr("matrx_ai._ext.get_ext", lambda name: fake_record_error if name == "record_error" else None)

    await cache_guard._record_deliberate_break(
        kind="held_prompt_rerendered",
        reason="the Holder changed",
        conversation_id="3755cc8a-4ab8-5127-b99d-955819018c6e",
        prev_len=10,
        new_len=12,
        where="test",
    )

    assert len(captured) == 1
    assert captured[0]["kind"] == "prompt_cache_deliberate_break"
    assert (captured[0].get("context") or {}).get("severity") == "info", (
        "a lawful cache break must be an info notice, never an open system_error row"
    )
