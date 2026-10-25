# ruff: noqa: F811 — pytest fixtures imported from test_device_served_via
"""On a device route a MISSING function-calling fact is unknown, never false (L5 D2).

Every local GGUF catalog model ships ``capabilities.features = []`` and a person's own model
has no definition at all, so "function_calling not in features" said nothing about the model —
and the no-function-calling strip removed every tool from a Qwen 3.5 2B run
(``tools_removed_no_function_calling``, "Removed: math_calculate", wire device_chat). The ruling:
on ``route_kind == "device"`` with no declared features, tools are SENT and llama-server
(``--jinja``) decides; a refusal comes back typed (``device_invalid_request``), never a silent
strip. A device model whose features ARE declared without function_calling still strips, and a
cloud model with ``features: []`` strips exactly as before.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from test_device_served_via import (  # noqa: F401
    FILE_ID,
    MODEL_ID,
    SV,
    _own_sv,
    _seed,
    own_file_placement,
    placement,
)

from matrx_ai.config.served_via import ServedVia


def _tooled_config() -> Any:
    from matrx_ai.config import MessageList, UnifiedConfig

    return UnifiedConfig(model=MODEL_ID, tools=["math_calculate"], messages=MessageList())


async def _device_profile(monkeypatch, features: list[str]) -> Any:
    from matrx_ai.catalog.resolve import resolve_call_profile
    from matrx_ai.db.ai_models.ai_model_manager import ai_model_manager_instance

    _seed(monkeypatch, with_offering=False)

    async def load_model(ref: str) -> Any:
        return SimpleNamespace(
            id=MODEL_ID,
            name="qwen3.5-2b",
            provider_id="prov-qwen",
            max_tokens=8192,
            metadata={},
            capabilities={"input": ["text"], "output": ["text"], "features": features},
        )

    monkeypatch.setattr(ai_model_manager_instance, "load_model", load_model)
    return await resolve_call_profile(MODEL_ID, served_via=ServedVia.model_validate(SV))


@pytest.mark.asyncio
async def test_a_device_model_with_no_declared_features_keeps_its_tools(
    monkeypatch, placement
) -> None:  # noqa: F811
    from matrx_ai.providers.unified_client import _strip_tools_for_no_function_calling

    profile = await _device_profile(monkeypatch, [])
    config = _tooled_config()
    assert _strip_tools_for_no_function_calling(config, profile.capabilities, "device_chat") is None
    assert list(config.tools) == ["math_calculate"]


@pytest.mark.asyncio
async def test_a_device_model_declared_without_function_calling_still_strips(
    monkeypatch, placement
) -> None:  # noqa: F811
    from matrx_ai.providers.unified_client import _strip_tools_for_no_function_calling

    profile = await _device_profile(monkeypatch, ["json_mode"])
    adaptation = _strip_tools_for_no_function_calling(
        _tooled_config(), profile.capabilities, "device_chat"
    )
    assert adaptation is not None and adaptation.code == "tools_removed_no_function_calling"


def test_a_cloud_model_with_empty_features_strips_exactly_as_before() -> None:
    from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities
    from matrx_ai.providers.unified_client import _strip_tools_for_no_function_calling

    caps = resolve_model_capabilities(
        SimpleNamespace(
            name="cloud-x", capabilities={"input": ["text"], "output": ["text"], "features": []}
        )
    )
    adaptation = _strip_tools_for_no_function_calling(_tooled_config(), caps, "openai_chat")
    assert adaptation is not None and adaptation.removed == ["math_calculate"]


@pytest.mark.asyncio
async def test_an_own_file_profile_keeps_a_server_tool(own_file_placement) -> None:
    """A person's own file has no definition: its tool fact is UNKNOWN, so tools are sent."""
    from matrx_ai.catalog.resolve import resolve_call_profile
    from matrx_ai.providers.unified_client import _strip_tools_for_no_function_calling

    profile = await resolve_call_profile(FILE_ID, served_via=_own_sv())
    config = _tooled_config()
    assert _strip_tools_for_no_function_calling(config, profile.capabilities, "device_chat") is None
    assert list(config.tools) == ["math_calculate"]
    facts = profile.offering_metadata["device_facts"]
    assert facts["function_calling"] == {"value": None, "source": "unknown"}


@pytest.mark.asyncio
@pytest.mark.parametrize("reported", [True, False])
async def test_an_own_file_tools_flag_the_device_reports_decides(own_file_placement, reported) -> None:
    from matrx_ai.catalog import device_placement
    from matrx_ai.catalog.resolve import resolve_call_profile
    from matrx_ai.providers.unified_client import _strip_tools_for_no_function_calling

    own_file_placement["value"] = device_placement.DeviceOwnFile(
        file_id=FILE_ID, name="my-finetune.gguf",
        metadata={"gguf": {"supports_tools": reported}},
    )
    profile = await resolve_call_profile(FILE_ID, served_via=_own_sv())
    stripped = _strip_tools_for_no_function_calling(_tooled_config(), profile.capabilities, "device_chat")
    assert (stripped is None) is reported
    facts = profile.offering_metadata["device_facts"]
    assert facts["function_calling"] == {"value": reported, "source": "device_reported"}

def _contract() -> dict:
    """The pinned device-model contract, read from the package both sides test against."""
    import json
    from pathlib import Path

    path = Path(__file__).resolve().parents[3] / "apps" / "shared" / "desktop-protocol" / "fixtures" / "device-model-contract.json"
    return json.loads(path.read_text())



@pytest.mark.asyncio
async def test_the_pinned_own_row_tool_flag_is_read_and_a_guessed_name_is_not(own_file_placement) -> None:
    from matrx_ai.catalog import device_placement
    from matrx_ai.catalog.resolve import resolve_call_profile

    pinned = _contract()["own_row"]["metadata"]
    assert pinned["gguf"]["supports_tools"] is True
    for metadata, expected in (
        (pinned, {"value": True, "source": "device_reported"}),
        ({"gguf": {"chat_template_supports_tools": False, "tools": False}}, {"value": None, "source": "unknown"}),
        (_contract()["own_row"]["metadata_without_known_tool_support"], {"value": None, "source": "unknown"}),
    ):
        own_file_placement["value"] = device_placement.DeviceOwnFile(file_id=FILE_ID, name="my-finetune.gguf", metadata=metadata)
        profile = await resolve_call_profile(FILE_ID, served_via=_own_sv())
        assert profile.offering_metadata["device_facts"]["function_calling"] == expected
