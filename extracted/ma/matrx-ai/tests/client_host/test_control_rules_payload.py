"""Client-host param shaping must follow DB-authored control_rules.

The 2026-07 regression: matrx-local (a client-host client host) shaped Anthropic
params from the hardcoded per-wire fallback (`mode: budget`), sending
``thinking.type=enabled`` to adaptive-only models (sonnet-5, fable-5,
opus-4.6+) — a guaranteed provider 400. The fix: the server exports each
model's resolved control rules into the catalog payload
(``AiCatalogManager.export_model_routing``) and
``build_catalog_call_profile`` consumes them ahead of the fallback.
"""

from __future__ import annotations

from matrx_ai.catalog.host_catalog import CatalogModel, build_catalog_call_profile
from matrx_ai.config import UnifiedConfig
from matrx_ai.providers.outbound_params import resolve_outbound_params

ADAPTIVE_RULES = {
    "reasoning_effort": {
        "supported": True,
        "processor": "anthropic_thinking",
        "processor_config": {
            "mode": "adaptive",
            "order": 100,
            "consumes": [
                "thinking_budget",
                "thinking_level",
                "include_thoughts",
                "reasoning_summary",
                "clear_thinking",
            ],
            "effort_ceiling": "high",
            "default_max_tokens": 32768,
        },
    },
    "temperature": {"supported": False},
    "top_p": {"supported": False},
    "top_k": {"supported": False},
    "max_output_tokens": {"provider_key": "max_tokens"},
}


def _config() -> UnifiedConfig:
    return UnifiedConfig(
        model="claude-sonnet-5", messages=[], reasoning_effort="low", stream=True
    )


def test_control_rules_payload_drives_adaptive_thinking():
    model = CatalogModel(
        {
            "id": "m1",
            "name": "claude-sonnet-5",
            "wire_format": "anthropic_chat",
            "control_rules": ADAPTIVE_RULES,
        }
    )
    profile = build_catalog_call_profile(model)
    params = resolve_outbound_params(_config(), profile.controls)
    assert params["thinking"] == {"type": "adaptive", "display": "summarized"}
    assert params["output_config"] == {"effort": "low"}
    assert "budget_tokens" not in params.get("thinking", {})


def test_missing_control_rules_falls_back_to_per_wire_rules():
    model = CatalogModel(
        {"id": "m2", "name": "claude-3-7-sonnet", "wire_format": "anthropic_chat"}
    )
    profile = build_catalog_call_profile(model)
    params = resolve_outbound_params(_config(), profile.controls)
    # Conservative fallback stays budget-mode for legacy dicts.
    assert params["thinking"]["type"] == "enabled"


def test_invalid_control_rules_fall_back_loudly_not_fatally():
    model = CatalogModel(
        {
            "id": "m3",
            "name": "claude-sonnet-5",
            "wire_format": "anthropic_chat",
            "control_rules": {"reasoning_effort": {"processor_config": {"mode": "adaptive"}}},
        }
    )
    # processor_config without processor is invalid → fallback, no raise.
    profile = build_catalog_call_profile(model)
    params = resolve_outbound_params(_config(), profile.controls)
    assert params["thinking"]["type"] == "enabled"
