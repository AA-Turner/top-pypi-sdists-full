"""An agent's reasoning_effort survives a cloud turn that TRANSLATES it and reaches a device turn.

L5 closing walk (2026-10-24): an agent whose own reasoning_effort is "none" took a cloud turn on a
model that has no "none" (gpt-oss: none→low on the wire), then a local turn through the
/ai/conversations continuation, and Qwen thought. The per-route translation is a WIRE fact: it
must never be stored back as the person's choice, and the agent's own "none" must reach the
device as enable_thinking false.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.config.served_via import ServedVia

DEVICE = "6f1c2a7e-3b9d-4c1e-8f0a-2d4b6c8e0a13"
MODEL_ID = "2c4e6a80-9b1d-4f3e-8a5c-7e9f1b3d5a70"
SV = {"provider": "device", "app_instance_id": DEVICE, "local_model_id": MODEL_ID}


def _agent_config() -> Any:
    from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage

    return UnifiedConfig(
        model="gpt-oss-120b",
        reasoning_effort="none",
        messages=MessageList(_messages=[UnifiedMessage(role="user", content=[TextContent(text="hi")])]),
    )


def _gpt_oss_controls() -> Any:
    from matrx_ai.catalog.controls import CompiledControlsMap
    from matrx_ai.catalog.models import ControlRule

    # gpt-oss: no "none" — the offering maps it to its lowest level on the wire.
    return CompiledControlsMap(
        rules={"reasoning_effort": ControlRule.model_validate(
            {"value_map": {"none": "low", "low": "low", "medium": "medium", "high": "high"}}
        )}
    )


def _device_profile() -> Any:
    from matrx_ai.catalog.host_catalog import _fallback_controls
    from matrx_ai.testing.profile_factory import make_profile

    return make_profile(
        model_name="qwen3.5-2b", wire_format="device_chat", vendor="device",
        provider_model_id="qwen3.5-2b", controls=_fallback_controls("generic_openai_chat"),
    ).model_copy(update={"route_kind": "device", "served_via": ServedVia.model_validate(SV), "model_id": MODEL_ID})


@pytest.mark.parametrize("this_turn_only", [False, True])
def test_none_survives_a_translating_cloud_turn_and_reaches_the_device(this_turn_only: bool) -> None:
    from matrx_ai.config import UnifiedConfig
    from matrx_ai.config.llm_params import LLMParams
    from matrx_ai.providers.device import DeviceChat
    from matrx_ai.providers.outbound_params import resolve_outbound_params

    config = _agent_config()
    # Turn 1 (cloud): the wire carries the translation...
    wire = resolve_outbound_params(config, _gpt_oss_controls())
    assert wire.get("reasoning_effort") == "low"
    # ...and the conversation keeps the person's / agent's own choice.
    assert config.reasoning_effort == "none"
    stored = config.to_storage_dict()
    assert stored["config"]["reasoning_effort"] == "none"

    # Turn 2 (device) through the continuation: the stored config + this turn's model pick.
    restored = UnifiedConfig.from_dict({"model": stored["model"], **stored["config"], "messages": []})
    if this_turn_only:
        restored.begin_model_this_turn_only()
    restored.apply_overrides(LLMParams(model=MODEL_ID, served_via=SV))
    assert restored.reasoning_effort == "none"
    body = DeviceChat().to_provider_config(restored, _device_profile())
    assert body["chat_template_kwargs"] == {"enable_thinking": False}


# ── the layering (main's ruling 2026-10-24): model default < agent < the person's override ──
def _null_reasoning(**kw: Any) -> Any:
    from matrx_ai.config.llm_params import LLMParams

    params = LLMParams(reasoning_effort=None, **kw)
    assert "reasoning_effort" in params.model_fields_set  # an EXPLICIT null: the override removed
    return params


@pytest.mark.parametrize("via_storage", [False, True])
def test_a_removed_override_falls_back_to_the_agents_own_setting(via_storage: bool) -> None:
    from matrx_ai.config import UnifiedConfig
    from matrx_ai.providers.device import DeviceChat
    from matrx_ai.providers.outbound_params import resolve_outbound_params

    config = _agent_config()
    config.snapshot_authored_settings()  # what Agent._build_from_config does
    if via_storage:  # the continuation restores the stored conversation
        stored = config.to_storage_dict()
        config = UnifiedConfig.from_dict({"model": stored["model"], **stored["config"], "messages": []})

    # A cloud turn whose request removes the person's override: the agent's "none" stands,
    # translated on gpt-oss's wire.
    cloud = UnifiedConfig.from_dict({**config.to_storage_dict()["config"], "model": config.model, "messages": []})
    cloud.apply_overrides(_null_reasoning())
    assert cloud.reasoning_effort == "none"
    assert resolve_outbound_params(cloud, _gpt_oss_controls()).get("reasoning_effort") == "low"

    # A device turn with the same removal reaches llama as thinking OFF.
    config.apply_overrides(_null_reasoning(model=MODEL_ID, served_via=SV))
    assert config.reasoning_effort == "none"
    body = DeviceChat().to_provider_config(config, _device_profile())
    assert body["chat_template_kwargs"] == {"enable_thinking": False}


def test_without_an_agent_layer_a_null_still_returns_the_model_default() -> None:
    config = _agent_config()  # no agent snapshot: a plain chat's own settings
    config.apply_overrides(_null_reasoning())
    assert config.reasoning_effort is None
