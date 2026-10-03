"""An extraction run resolves the CLASS the run is pinned to.

A model's class is its serving offering. ``config.routing_offering_id`` (the
user's pin, or the reroute's runtime pin) must reach ``resolve_call_profile`` —
never the preferred offering behind the run's back.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

import matrx_ai.catalog.resolve as catalog_resolve
import matrx_ai.extraction as extraction
from matrx_ai.providers.fastino import SpanExtractionResult
from matrx_ai.providers.unified_client import UnifiedAIClient

PIN = "e500ce86-d54d-4e0e-af27-101bdc5cbf1d"


class _Stop(Exception):
    pass


def test_extract_spans_resolves_the_pinned_offering(monkeypatch):
    seen: dict[str, object] = {}

    async def fake_resolve(model_ref, endpoint_hint=None, *, offering_id=None):
        seen["model_ref"] = model_ref
        seen["offering_id"] = offering_id
        raise _Stop

    monkeypatch.setattr(catalog_resolve, "resolve_call_profile", fake_resolve)
    with pytest.raises(_Stop):
        asyncio.run(extraction.extract_spans("gliner2", "Ada", ["person"], offering_id=PIN))
    assert seen == {"model_ref": "gliner2", "offering_id": PIN}


def test_extract_spans_without_pin_resolves_the_preferred_class(monkeypatch):
    seen: dict[str, object] = {}

    async def fake_resolve(model_ref, endpoint_hint=None, *, offering_id=None):
        seen["offering_id"] = offering_id
        raise _Stop

    monkeypatch.setattr(catalog_resolve, "resolve_call_profile", fake_resolve)
    with pytest.raises(_Stop):
        asyncio.run(extraction.extract_spans("gliner2", "Ada", ["person"]))
    assert seen == {"offering_id": None}


@pytest.mark.parametrize("pin", [PIN, None])
def test_extraction_turn_passes_the_run_class(monkeypatch, pin):
    seen: dict[str, object] = {}

    async def fake_extract(model, text, labels, *, threshold=0.3, client=None, offering_id=None):
        seen["offering_id"] = offering_id
        return SpanExtractionResult(model=model, spans=[])

    monkeypatch.setattr(extraction, "extract_spans", fake_extract)
    monkeypatch.setattr(UnifiedAIClient, "_last_user_text", staticmethod(lambda config: "Ada"))
    config = SimpleNamespace(
        metadata={"extraction": {"labels": ["person"]}},
        routing_offering_id=pin,
    )
    asyncio.run(UnifiedAIClient()._execute_extraction(config, "fastino", "gliner2"))
    assert seen == {"offering_id": pin}
