"""A dropped schema is the explanation; the off-contract answer is the harm.

``structured_output.enforcement_dropped`` fired 3556 times at "high" (live
2026-11-18), almost all of them recovered capability facts, and buried the
``answer_off_contract`` rows that say a person got a broken answer. The drop is
medium; the harm stays high and is never collapsed to once a day.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.providers import structured_output_findings as sof


def test_enforcement_dropped_ranks_below_the_harm_it_explains() -> None:
    order = {"low": 0, "medium": 1, "high": 2}
    assert sof._SEVERITY[sof.ENFORCEMENT_DROPPED] == "medium"
    assert sof._SEVERITY[sof.ANSWER_OFF_CONTRACT] == "high"
    assert order[sof._SEVERITY[sof.ENFORCEMENT_DROPPED]] < order[sof._SEVERITY[sof.ANSWER_OFF_CONTRACT]]


def test_the_harm_is_never_collapsed_and_the_drop_is_never_silenced() -> None:
    assert sof.ANSWER_OFF_CONTRACT not in sof._ONCE_WHEN_RECOVERED
    # An unrecovered drop is news every time: only RECOVERED repeats collapse.
    recovered, _ = sof.translation_outcome(True, True)
    assert recovered is False


@pytest.mark.asyncio
async def test_drop_is_written_at_medium_and_off_contract_at_high(monkeypatch: pytest.MonkeyPatch) -> None:
    written: list[dict[str, Any]] = []

    async def fake_capture(key: str, **kwargs: Any) -> None:
        written.append({"key": key, **kwargs})

    import matrx_ai.ops.issue_capture as issue_capture

    monkeypatch.setattr(issue_capture, "capture_issue", fake_capture)
    sof.forget_recorded_facts()
    await sof.record_structured_output_finding(
        sof.ENFORCEMENT_DROPPED, provider="anthropic", model="m", detail={"action": "a"}, was_recovered=False
    )
    await sof.record_structured_output_finding(
        sof.ANSWER_OFF_CONTRACT, provider="anthropic", model="m", detail={"failures": ["$: x"]}, was_recovered=False
    )
    by_key = {row["key"]: row for row in written}
    assert by_key[sof.ENFORCEMENT_DROPPED]["severity"] == "medium"
    assert by_key[sof.ANSWER_OFF_CONTRACT]["severity"] == "high"
