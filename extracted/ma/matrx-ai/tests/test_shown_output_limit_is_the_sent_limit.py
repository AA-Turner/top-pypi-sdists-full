"""The output limit a person sees is the limit the provider is sent — device and cloud.

L3 final walk (2026-10-24): the first local turn died with "the limit is 300 tokens" while
Model and overrides showed 45 000. The panel shows the conversation agent's own
``max_output_tokens`` (its base settings); the root cause was the client painting a different
agent than the mandate door ran (chat package guard
``the-agent-on-screen-is-the-agent-that-runs.test.ts``). This is the payload half: whatever
limit the agent carries — and whatever override the person sets — reaches the wire unchanged on
the device route (``served_via``) and on a cloud route.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.config.served_via import ServedVia

DEVICE = "0100cebb-e4c6-4f82-b863-5817398ccee8"
MODEL_ID = "2fdd7f94-40b0-48b4-9522-11167398ce9c"
SV = {"provider": "device", "app_instance_id": DEVICE, "local_model_id": MODEL_ID}


def _config(max_output_tokens: int) -> Any:
    from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage

    config = UnifiedConfig(
        model="cloud-model",
        max_output_tokens=max_output_tokens,
        messages=MessageList(_messages=[UnifiedMessage(role="user", content=[TextContent(text="hi")])]),
    )
    config.snapshot_authored_settings()
    return config


def _profile(device: bool) -> Any:
    from matrx_ai.catalog.host_catalog import _fallback_controls
    from matrx_ai.testing.profile_factory import make_profile

    if device:
        return make_profile(
            model_name="qwen3-4b", wire_format="device_chat", vendor="device",
            provider_model_id="qwen3-4b", controls=_fallback_controls("generic_openai_chat"),
        ).model_copy(update={"route_kind": "device", "served_via": ServedVia.model_validate(SV), "model_id": MODEL_ID})
    return make_profile(
        model_name="cloud-model", wire_format="generic_openai_chat", vendor="generic",
        provider_model_id="cloud-model", controls=_fallback_controls("generic_openai_chat"),
    )


def _body(config: Any, device: bool) -> dict[str, Any]:
    from matrx_ai.providers.device import DeviceChat
    from matrx_ai.providers.generic_openai.generic_openai_api import GenericOpenAIChat

    client = DeviceChat() if device else GenericOpenAIChat(base_url="https://cloud.invalid/v1", api_key="test")
    return client.to_provider_config(config, _profile(device))


@pytest.mark.parametrize("device", [True, False], ids=["device_served_via", "cloud_control"])
@pytest.mark.parametrize("agent_limit", [300, 45000])
def test_the_agents_own_limit_reaches_the_wire(device: bool, agent_limit: int) -> None:
    from matrx_ai.config.llm_params import LLMParams

    config = _config(agent_limit)
    if device:
        config.apply_overrides(LLMParams(model=MODEL_ID, served_via=SV))
    assert _body(config, device)["max_tokens"] == agent_limit


@pytest.mark.parametrize("device", [True, False], ids=["device_served_via", "cloud_control"])
def test_the_persons_override_is_the_limit_sent(device: bool) -> None:
    from matrx_ai.config.llm_params import LLMParams

    config = _config(300)
    config.apply_overrides(
        LLMParams(model=MODEL_ID, served_via=SV, max_output_tokens=6000)
        if device
        else LLMParams(max_output_tokens=6000)
    )
    assert _body(config, device)["max_tokens"] == 6000
