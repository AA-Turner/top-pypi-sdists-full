"""A device turn's reasoning reaches the chat template in the form that template reads.

Live shapes (2026-10-27):
* Qwen 3 4B's device offering (ai_131) compiles ``reasoning_effort`` to ui_values [auto, none],
  default auto — the template's ``enable_thinking`` switch (thinks by default).
* Qwen 3.5 2B / Gemma 4 compile [none, high], default none (thinks only when asked).
* gpt-oss's template reads ``reasoning_effort`` low/medium/high and has no off; Mistral Small 4's
  raises on any value other than none/high. Both read it from ``chat_template_kwargs``.

The device route reads the model's device offering's compiled controls (never the generic
fallback when an offering exists), and DeviceChat sends what the controls shaped: the boolean
switch for templates that have one, the level by name for templates that read it. A person's own
file maps the thinking-switch fact its computer reported (metadata.gguf.thinking_switch, pinned by
the desktop-protocol fixture) to the matching device profile, by the compiled rule, never a name.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from matrx_ai.catalog.manager import AiCatalogManager
from matrx_ai.catalog.resolve import _OWN_FILE_THINKING_KEY, _OWN_FILE_THINKING_VALUES, _own_file_thinking_fact
from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.served_via import ServedVia
from matrx_ai.providers.device.device_api import DeviceChat
from matrx_ai.testing.profile_factory import make_profile

FIXTURE = Path(__file__).resolve().parents[3] / "apps/shared/desktop-protocol/fixtures/device-model-contract.json"
DEVICE = "506e6752-13b3-4616-b99e-dab6f0e436ab"

PROFILES = {
    # model id: (provider key, the profile's compiled reasoning_effort rule)
    "qwen-3-4b": {"ui_values": ["auto", "none"], "default": "auto"},
    "qwen-3.5-2b": {"ui_values": ["none", "high"], "default": "none"},
    # Proposed (ai_133, awaiting main's go): exactly the values each template accepts.
    "gpt-oss-20b": {"value_map": {"none": "low", "low": "low", "medium": "medium", "high": "high"},
                    "on_unmapped": "nearest", "ui_values": ["low", "medium", "high"], "default": "low"},
    "mistral-small-4": {"value_map": {"none": "none", "high": "high"}, "on_unmapped": "nearest",
                        "ui_values": ["none", "high"], "default": "none"},
}


def _manager() -> AiCatalogManager:
    manager = AiCatalogManager()
    manager.load_from_rows(
        endpoints=[{"id": "ep-device", "vendor": "device", "internal_name": "This computer", "display_name": "This computer"}],
        apis=[{"id": "api-device", "name": "device_chat", "display_name": "Device chat", "translator_key": "device_chat",
               "rules": {"params": {}, "constraints": []}}],
        offerings=[
            {"id": f"off-{m}", "model_id": m, "endpoint_id": "ep-device", "api_id": "api-device", "provider_model_id": m,
             "priority": 1000, "override": {"params": {"reasoning_effort": rule}, "constraints": []}}
            for m, rule in PROFILES.items()
        ],
        settings=[{"key": "reasoning_effort", "value_type": "enum",
                   "canonical_values": ["auto", "none", "minimal", "low", "medium", "high", "xhigh", "max"]}],
    )
    return manager


def _body(model: str, effort: str | None) -> dict[str, Any]:
    controls = _manager().device_controls_for(model)
    assert controls is not None, model
    profile = make_profile(
        model_name=model, wire_format="device_chat", vendor="device", provider_model_id=model, controls=controls,
    ).model_copy(update={"route_kind": "device", "model_id": model, "served_via": ServedVia.model_validate(
        {"provider": "device", "app_instance_id": DEVICE, "local_model_id": model})})
    config = UnifiedConfig(model=model, reasoning_effort=effort, messages=MessageList(
        _messages=[UnifiedMessage(role="user", content=[TextContent(text="hi")])]))
    return DeviceChat().to_provider_config(config, profile)


def test_off_sends_the_switch_off_and_nothing_else() -> None:
    body = _body("qwen-3-4b", "none")
    assert body["chat_template_kwargs"] == {"enable_thinking": False}
    assert "reasoning_effort" not in body


def test_auto_leaves_the_template_its_own_default() -> None:
    assert "chat_template_kwargs" not in _body("qwen-3-4b", "auto") or not _body("qwen-3-4b", "auto")["chat_template_kwargs"]


def test_off_by_default_template_turns_on_only_when_asked() -> None:
    assert _body("qwen-3.5-2b", "none")["chat_template_kwargs"] == {"enable_thinking": False}
    assert _body("qwen-3.5-2b", "high")["chat_template_kwargs"]["enable_thinking"] is True


@pytest.mark.parametrize("effort", ["low", "medium", "high"])
def test_gpt_oss_reads_its_level_by_name(effort: str) -> None:
    kwargs = _body("gpt-oss-20b", effort)["chat_template_kwargs"]
    assert kwargs["reasoning_effort"] == effort
    assert "reasoning_effort" not in _body("gpt-oss-20b", effort)


@pytest.mark.parametrize("effort", ["none", "minimal", "low", "medium", "high", "xhigh", "max"])
def test_mistral_small_4_never_receives_a_level_it_raises_on(effort: str) -> None:
    kwargs = _body("mistral-small-4", effort).get("chat_template_kwargs") or {}
    assert kwargs.get("reasoning_effort") in (None, "high"), (effort, kwargs)


def test_an_own_file_maps_its_thinking_switch_to_the_device_profile() -> None:
    manager = _manager()
    on = manager.device_thinking_controls("on_by_default")
    off = manager.device_thinking_controls("off_by_default")
    assert on is not None and on.rules["reasoning_effort"].default == "auto"
    assert off is not None and off.rules["reasoning_effort"].default == "none"
    assert "none" in (off.rules["reasoning_effort"].ui_values or [])
    assert manager.device_thinking_controls("none") is None
    assert manager.device_thinking_controls(None) is None


def test_the_server_reads_the_fact_the_contract_names() -> None:
    contract = json.loads(FIXTURE.read_text())
    rule = contract["thinking_rule"]
    assert rule["key"] == _OWN_FILE_THINKING_KEY
    assert set(rule["values"]) == set(_OWN_FILE_THINKING_VALUES)
    meta = contract["own_row"]["metadata"]
    assert _own_file_thinking_fact(meta) == meta["gguf"][_OWN_FILE_THINKING_KEY]
    assert _own_file_thinking_fact(contract["own_row"]["metadata_without_known_tool_support"]) is None
