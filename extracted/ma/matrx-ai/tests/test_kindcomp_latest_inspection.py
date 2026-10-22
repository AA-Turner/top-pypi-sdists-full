"""kindcomp_get_context carries the host's newest measured inspection per component; without the host seam it
carries nothing, and a failing host never fails the context."""

from __future__ import annotations

import pytest

from matrx_ai import _ext
from matrx_ai.tools.implementations import kind_component as kc


@pytest.mark.asyncio
async def test_no_host_seam_means_no_inspections(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delitem(_ext._registry, kc.INSPECTION_EXT_KEY, raising=False)
    assert await kc._latest_inspections(["c-1"]) == []


@pytest.mark.asyncio
async def test_the_host_answer_is_returned_per_component_and_none_is_skipped(monkeypatch: pytest.MonkeyPatch) -> None:
    async def seam(*, component_id: str):
        return {"component_id": component_id, "verdict": "problems"} if component_id == "c-1" else None

    monkeypatch.setitem(_ext._registry, kc.INSPECTION_EXT_KEY, seam)
    assert await kc._latest_inspections(["c-1", "c-2"]) == [{"component_id": "c-1", "verdict": "problems"}]


@pytest.mark.asyncio
async def test_a_failing_host_is_reported_inside_the_bundle(monkeypatch: pytest.MonkeyPatch) -> None:
    async def seam(*, component_id: str):
        raise RuntimeError("ledger down")

    monkeypatch.setitem(_ext._registry, kc.INSPECTION_EXT_KEY, seam)
    out = await kc._latest_inspections(["c-1"])
    assert out[0]["verdict"] == "unavailable" and "ledger down" in out[0]["reason"]
