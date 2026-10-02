"""The vendor the executor reports (telemetry, error classifier, issue
registry) is the PINNED class's, not the preferred class's.

Live 2026-10-01: a Qwen3.8 27B run pinned to Matrx Lightning (cerebras) was
logged, classified and issue-registered as groq (Matrx Fast)."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

from matrx_ai.orchestrator import executor


def test_vendor_label_uses_the_pinned_offering(monkeypatch):
    seen: dict = {}

    async def fake_resolve(model, endpoint_hint=None, *, offering_id=None):
        seen["offering_id"] = offering_id
        return SimpleNamespace(vendor="cerebras" if offering_id == "lightning" else "groq")

    import matrx_ai.catalog.resolve as resolve

    monkeypatch.setattr(resolve, "resolve_call_profile", fake_resolve)
    config = SimpleNamespace(model="qwen", matrx_model_name=None, routing_offering_id="lightning")
    assert asyncio.run(executor._catalog_vendor_for(config)) == "cerebras"
    assert seen["offering_id"] == "lightning"
