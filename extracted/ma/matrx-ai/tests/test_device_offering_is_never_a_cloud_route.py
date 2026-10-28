"""A device offering (api wire ``device_chat``) is never a cloud route.

Live shape (ai_131, 2026-10-27): Qwen 3 4B (2fdd7f94…) has exactly one offering — the device
route "This computer" (endpoint vendor ``device``, api ``device_chat``, priority 1000). It exists
so ai.resolve_model_config can carry the GGUF template's thinking switch. A call WITHOUT
``served_via`` used to pick that offering as the model's preferred route and dispatch to
DeviceChat, which refused it ("Your computer couldn't read that request"). The ONE rule: the
cloud candidate list (``offerings_for`` — preferred, pins, classes, overload ladder, client-host
routing export) never holds a device-wire offering; the device route reads it by name
(``device_offering_for``); a request without ``served_via`` on a device-only model is refused
with a sentence that says where the model runs.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.catalog import resolve as resolve_mod
from matrx_ai.catalog.errors import CatalogRoutingError
from matrx_ai.catalog.manager import AiCatalogManager
from matrx_ai.catalog.resolve import select_offering

QWEN_4B = "2fdd7f94-40b0-48b4-9522-11167398ce9c"
QWEN_9B = "qwen-3-5-9b-model"  # a model with a cloud offering AND a device offering
DEVICE_OFFERING = "a7f0c1d2-0000-4000-8000-000000000131"


def _rows() -> dict[str, Any]:
    return {
        "endpoints": [
            {"id": "ep-device", "vendor": "device", "internal_name": "This computer", "display_name": "This computer"},
            {"id": "ep-together", "vendor": "together", "internal_name": "together", "display_name": "Matrx Open"},
        ],
        "apis": [
            {"id": "api-device", "name": "device_chat", "display_name": "Device chat", "translator_key": "device_chat",
             "rules": {"params": {}, "constraints": []}},
            {"id": "api-together", "name": "together_chat", "display_name": "Together", "translator_key": "generic_openai_chat",
             "rules": {"params": {}, "constraints": []}},
        ],
        "offerings": [
            {"id": DEVICE_OFFERING, "model_id": QWEN_4B, "endpoint_id": "ep-device", "api_id": "api-device",
             "provider_model_id": "qwen-3-4b", "priority": 1000},
            {"id": "off-9b-device", "model_id": QWEN_9B, "endpoint_id": "ep-device", "api_id": "api-device",
             "provider_model_id": "qwen-3.5-9b", "priority": 1},
            {"id": "off-9b-cloud", "model_id": QWEN_9B, "endpoint_id": "ep-together", "api_id": "api-together",
             "provider_model_id": "Qwen/Qwen3.5-9B", "priority": 100},
        ],
        "settings": [],
        "models": [{"id": QWEN_4B, "name": "qwen-3-4b"}, {"id": QWEN_9B, "name": "qwen-3.5-9b"}],
    }


def _manager() -> AiCatalogManager:
    manager = AiCatalogManager()
    manager.load_from_rows(**_rows())
    return manager


def test_a_device_only_model_has_no_cloud_route() -> None:
    manager = _manager()
    assert manager.offerings_for(QWEN_4B) == []
    assert manager.model_classes(QWEN_4B) == []
    assert manager.export_model_routing(QWEN_4B) is None
    assert manager.wire_format_for(QWEN_4B) is None


def test_the_device_route_still_reads_its_offering() -> None:
    manager = _manager()
    offering = manager.device_offering_for(QWEN_4B)
    assert offering is not None and offering.id == DEVICE_OFFERING
    assert manager.is_device_offering(offering)


def test_a_device_offering_never_outranks_the_cloud_one() -> None:
    """Even at a lower priority number, the device offering is not the preferred cloud route."""
    manager = _manager()
    assert [o.id for o in manager.offerings_for(QWEN_9B)] == ["off-9b-cloud"]
    assert select_offering(QWEN_9B, manager=manager).id == "off-9b-cloud"


def test_a_pin_of_the_device_offering_is_not_a_cloud_call() -> None:
    with pytest.raises(CatalogRoutingError):
        select_offering(QWEN_4B, DEVICE_OFFERING, manager=_manager())


def test_a_call_without_served_via_is_refused_naming_the_computer(monkeypatch: pytest.MonkeyPatch) -> None:
    manager = _manager()

    async def _loaded() -> None:
        return None

    monkeypatch.setattr(manager, "ensure_loaded", _loaded)
    monkeypatch.setattr(resolve_mod, "ai_catalog_manager", manager)

    class _Models:
        async def load_model(self, ref: str) -> Any:
            return SimpleNamespace(id=QWEN_4B, name="qwen-3-4b", provider_id=None, capabilities={})

    import matrx_ai.db.ai_models.ai_model_manager as amm

    monkeypatch.setattr(amm, "ai_model_manager_instance", _Models())
    with pytest.raises(CatalogRoutingError, match="computer") as refused:
        asyncio.run(resolve_mod.resolve_call_profile(QWEN_4B))

    # Its own typed device error, never the generic "model route that is no longer available":
    # the person's sentence says where to pick it, and fits a notice card's line.
    from matrx_ai.providers.device.errors import (
        DEVICE_ERROR_TYPES,
        DEVICE_NOT_CHOSEN,
        DeviceNotChosenError,
    )
    from matrx_ai.providers.errors import classify_provider_error

    assert isinstance(refused.value, DeviceNotChosenError)
    assert DEVICE_NOT_CHOSEN in DEVICE_ERROR_TYPES
    info = classify_provider_error("device", refused.value)
    assert info.error_type == DEVICE_NOT_CHOSEN
    assert info.is_retryable is False
    assert info.user_message == "Pick this model under Your computers."
    assert len(info.user_message) <= 40
    assert "no longer available" not in info.user_message
    assert info.details["code"] == DEVICE_NOT_CHOSEN and info.details["provider"] == "device"
    info_any = classify_provider_error("openai", refused.value)
    assert info_any.error_type == DEVICE_NOT_CHOSEN
