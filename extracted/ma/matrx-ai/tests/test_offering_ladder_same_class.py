"""load_offering_ladder keeps failover inside the failing offering's class.

Live shape (2026-10-01): Qwen3.8 27B is one model with a Matrx Fast (groq) and a
Matrx Lightning (cerebras) offering. Those are two products the person picks
between — a Lightning call that is overloaded must never silently run on Fast.
Equivalent offerings on the SAME endpoint remain valid siblings."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

from matrx_ai.catalog.models import CatalogOffering
from matrx_ai.orchestrator import overload_reroute

FAST, LIGHTNING = "ep-fast", "ep-lightning"
OFFERINGS = [
    CatalogOffering(id="fast-1", model_id="m", endpoint_id=FAST, api_id="a", provider_model_id="q", priority=100),
    CatalogOffering(id="light-1", model_id="m", endpoint_id=LIGHTNING, api_id="a", provider_model_id="q", priority=110),
    CatalogOffering(id="light-2", model_id="m", endpoint_id=LIGHTNING, api_id="b", provider_model_id="q2", priority=120),
    CatalogOffering(id="fast-2", model_id="m", endpoint_id=FAST, api_id="b", provider_model_id="q2", priority=130),
]


class _Manager:
    async def ensure_loaded(self):
        return None

    def offerings_for(self, model_id):
        return list(OFFERINGS)

    def offering(self, offering_id):
        return next((o for o in OFFERINGS if o.id == offering_id), None)


class _Models:
    async def load_model(self, ref):
        return SimpleNamespace(id="m")


def _ladder(monkeypatch, pin):
    import matrx_ai.catalog.manager as cm
    import matrx_ai.db.ai_models.ai_model_manager as mm

    monkeypatch.setattr(cm, "ai_catalog_manager", _Manager())
    monkeypatch.setattr(mm, "ai_model_manager_instance", _Models())
    return asyncio.run(
        overload_reroute.load_offering_ladder("m", routing_offering_id=pin, offerings_tried=[])
    )


def test_pinned_lightning_never_fails_over_to_fast(monkeypatch):
    ladder = _ladder(monkeypatch, "light-1")
    assert ladder.current_offering_id == "light-1"
    assert ladder.sibling_offering_ids == ["light-2"]


def test_unpinned_preferred_stays_in_its_own_class(monkeypatch):
    ladder = _ladder(monkeypatch, None)
    assert ladder.current_offering_id == "fast-1"
    assert ladder.sibling_offering_ids == ["fast-2"]
