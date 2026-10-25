"""A model on a person's Matrx 2 computer is just another way to serve a catalog model.

L5 design REVISION 1 (R1, R2, R5 call record). Guards, one per failure class:

* G7  — ``LLMParams`` accepts ``served_via`` and refuses an unknown provider value.
* G9  — the pick lives with the chat: stored, restored, cleared by a cloud pick, kept when no
        model is named, reverted after a "this message only" pick, dropped when an override
        layer moves the model.
* G1  — ``served_via`` resolves a device profile (``route_kind="device"``, ``device_chat``,
        no offering) whether or not the model has cloud offerings; without it nothing changes.
* G12 — a model not installed on that device is refused (``model_not_on_device``) before
        anything is dispatched, and so is a process with no placement check wired.
* G2/G8 — no site moves a device run: reroute, offering ladder, overload policy, model
        fallback, free-tier swap, child-safety swap, same-model retries.
* G13 — a mandate's overrides cannot set ``served_via``.
* G14 — a child agent and a workflow step never inherit it.
* call record — the usage row says where the call ran.
"""

from __future__ import annotations

import contextlib
from types import SimpleNamespace
from typing import Any

import pytest
from pydantic import ValidationError

from matrx_ai.config.llm_params import LLMParams, merge_llm_overrides
from matrx_ai.config.served_via import ServedVia, ServedViaRefusedError

DEVICE = "6f1c2a7e-3b9d-4c1e-8f0a-2d4b6c8e0a13"
OTHER_DEVICE = "0a9b8c7d-6e5f-4a3b-9c2d-1e0f2a3b4c5d"
FILE_ID = "9d2e4f60-1a3b-4c5d-8e7f-0a1b2c3d4e5f"
VARIANT = "4b5c6d7e-8f90-4a1b-9c2d-3e4f5a6b7c8d"
MODEL_ID = "2c4e6a80-9b1d-4f3e-8a5c-7e9f1b3d5a70"
SV = {"provider": "device", "app_instance_id": DEVICE, "local_model_id": "qwen3-4b-q4_k_m"}


# ── G7 ───────────────────────────────────────────────────────────────────────
def test_g7_llm_params_accepts_served_via_and_refuses_an_unknown_provider() -> None:
    params = LLMParams(model=MODEL_ID, served_via=SV)
    assert isinstance(params.served_via, ServedVia)
    assert params.served_via.app_instance_id == DEVICE
    with pytest.raises(ValidationError):
        LLMParams(served_via={**SV, "provider": "cloud"})
    with pytest.raises(ValidationError):
        LLMParams(served_via={**SV, "endpoint": "https://elsewhere"})
    with pytest.raises(ValidationError):
        LLMParams(served_via={**SV, "app_instance_id": "not-a-uuid"})


# ── G9 ───────────────────────────────────────────────────────────────────────
def _config(**kw: Any) -> Any:
    from matrx_ai.config import MessageList, UnifiedConfig

    return UnifiedConfig(model=kw.pop("model", MODEL_ID), messages=MessageList(), **kw)


def test_g9_served_via_is_stored_and_restored_with_the_conversation() -> None:
    from matrx_ai.config import UnifiedConfig

    config = _config()
    config.apply_overrides(LLMParams(model=MODEL_ID, served_via=SV))
    stored = config.to_storage_dict()
    assert stored["config"]["served_via"]["app_instance_id"] == DEVICE
    restored = UnifiedConfig.from_dict({"model": stored["model"], **stored["config"], "messages": []})
    assert restored.served_via == ServedVia.model_validate(SV)


def test_g9_a_turn_without_a_model_keeps_the_device_pick() -> None:
    config = _config()
    config.apply_overrides(LLMParams(model=MODEL_ID, served_via=SV))
    config.apply_overrides(LLMParams(temperature=0.3))
    assert config.served_via is not None and config.served_via.app_instance_id == DEVICE


def test_g9_a_model_pick_without_served_via_is_a_cloud_pick_and_clears_it() -> None:
    config = _config()
    config.apply_overrides(LLMParams(model=MODEL_ID, served_via=SV))
    config.apply_overrides(LLMParams(model=MODEL_ID))
    assert config.served_via is None
    assert "served_via" not in config.to_storage_dict()["config"]


def test_g9_a_this_message_only_device_pick_reverts_after_the_turn() -> None:
    config = _config()
    config.begin_model_this_turn_only()
    config.apply_overrides(LLMParams(model=MODEL_ID, served_via=SV))
    assert config.served_via is not None
    assert "served_via" not in config.to_storage_dict()["config"], "the row keeps its own pick"
    assert config.end_model_this_turn_only() is True
    assert config.served_via is None


def test_g9_an_override_layer_that_moves_the_model_drops_the_device_pick() -> None:
    merged = merge_llm_overrides({"model": MODEL_ID, "served_via": SV}, {"model": "gpt-5.4-nano"})
    assert "served_via" not in merged
    kept = merge_llm_overrides({"model": MODEL_ID, "served_via": SV}, {"temperature": 0.2})
    assert kept["served_via"] == SV


# ── G1 / G12: resolution ─────────────────────────────────────────────────────
def _seed(monkeypatch: pytest.MonkeyPatch, *, with_offering: bool) -> None:
    from matrx_ai.catalog.manager import ai_catalog_manager
    from matrx_ai.db.ai_models.ai_model_manager import ai_model_manager_instance

    ai_catalog_manager.load_from_rows(
        endpoints=[{"id": "ep-groq", "vendor": "groq", "internal_name": "groq_direct",
                    "display_name": "Matrx Fast", "is_active": True}],
        apis=[{"id": "api-groq", "name": "groq_chat", "display_name": "Groq Chat",
               "translator_key": "groq_chat", "rules": {"params": {}, "constraints": []}}],
        offerings=(
            [{"id": "off-groq", "model_id": MODEL_ID, "endpoint_id": "ep-groq", "api_id": "api-groq",
              "provider_model_id": "qwen/qwen3-32b", "is_available": True,
              "override": {"params": {}, "constraints": []}}]
            if with_offering
            else []
        ),
        settings=[],
        providers={"prov-qwen": "Qwen"},
        models=[{"id": MODEL_ID, "name": "qwen3-4b", "provider_id": "prov-qwen"}],
    )

    async def load_model(ref: str) -> Any:
        if ref not in (MODEL_ID, "qwen3-4b"):
            return None
        return SimpleNamespace(
            id=MODEL_ID, name="qwen3-4b", provider_id="prov-qwen", max_tokens=8192,
            capabilities={"input": ["text"], "output": ["text"], "features": ["tools"]},
            pricing={"input": 1.0},
        )

    monkeypatch.setattr(ai_model_manager_instance, "load_model", load_model)


@pytest.fixture
def placement(monkeypatch: pytest.MonkeyPatch):
    from matrx_ai.catalog import device_placement

    seen: list[tuple[ServedVia, str]] = []
    installed: dict[str, bool] = {"value": True}

    async def check(served_via: ServedVia, *, model_id: str) -> bool:
        seen.append((served_via, model_id))
        return installed["value"]

    device_placement.configure_device_placement(check)
    yield SimpleNamespace(seen=seen, installed=installed)
    device_placement.configure_device_placement(None)


@pytest.mark.asyncio
@pytest.mark.parametrize("with_offering", [False, True])
async def test_g1_served_via_resolves_one_device_route(monkeypatch, placement, with_offering) -> None:
    from matrx_ai.catalog.resolve import resolve_call_profile

    _seed(monkeypatch, with_offering=with_offering)
    profile = await resolve_call_profile(MODEL_ID, served_via=ServedVia.model_validate(SV))
    assert profile.route_kind == "device"
    assert profile.client_attr == "device_chat"
    assert profile.wire_format == "device_chat"
    assert profile.vendor == "device"
    assert profile.served_via == ServedVia.model_validate(SV)
    assert profile.offering_id == f"device:{DEVICE}", "no ai.offering is ever chosen"
    assert profile.model_id == MODEL_ID and profile.model_name == "qwen3-4b"
    assert profile.pricing is None, "the cloud offering's price never rides a device run"
    assert profile.capabilities is not None
    assert placement.seen == [(ServedVia.model_validate(SV), MODEL_ID)]


@pytest.mark.asyncio
async def test_g1_without_served_via_nothing_changes(monkeypatch, placement) -> None:
    from matrx_ai.catalog.errors import CatalogRoutingError
    from matrx_ai.catalog.resolve import resolve_call_profile

    _seed(monkeypatch, with_offering=False)
    with pytest.raises(CatalogRoutingError):
        await resolve_call_profile(MODEL_ID)
    _seed(monkeypatch, with_offering=True)
    profile = await resolve_call_profile(MODEL_ID)
    assert profile.route_kind == "offering"
    assert profile.client_attr == "groq_chat" and profile.served_via is None
    assert placement.seen == []


@pytest.mark.asyncio
async def test_g1_the_dispatch_seams_thread_served_via_from_the_config(monkeypatch, placement) -> None:
    from matrx_ai.catalog.resolve import resolve_tts_call_profile

    _seed(monkeypatch, with_offering=True)
    profile = await resolve_tts_call_profile(
        MODEL_ID, None, served_via=ServedVia.model_validate(SV)
    )
    assert profile.route_kind == "device"
    from matrx_utils.source_guard import stable_source

    from matrx_ai.agents import batch_render
    from matrx_ai.config import send_boundary
    from matrx_ai.orchestrator import executor
    from matrx_ai.providers import unified_client

    for module in (unified_client, send_boundary, batch_render, executor):
        source = stable_source(module)
        assert "served_via" in source, f"{module.__name__} resolves without the device pick"


@pytest.mark.asyncio
async def test_g12_a_model_not_on_that_device_is_refused_before_dispatch(monkeypatch, placement) -> None:
    from matrx_ai.catalog.resolve import resolve_call_profile
    from matrx_ai.providers.device.errors import ModelNotOnDeviceError

    _seed(monkeypatch, with_offering=True)
    placement.installed["value"] = False
    with pytest.raises(ModelNotOnDeviceError) as raised:
        await resolve_call_profile(MODEL_ID, served_via=ServedVia.model_validate(SV))
    assert raised.value.error_info.error_type == "model_not_on_device"
    assert raised.value.error_info.details["code"] == "not_on_device"
    assert raised.value.error_info.is_retryable is False


@pytest.mark.asyncio
async def test_g12_no_placement_check_wired_refuses_too(monkeypatch) -> None:
    from matrx_ai.catalog import device_placement
    from matrx_ai.catalog.resolve import resolve_call_profile
    from matrx_ai.providers.device.errors import ModelNotOnDeviceError

    device_placement.configure_device_placement(None)
    _seed(monkeypatch, with_offering=True)
    with pytest.raises(ModelNotOnDeviceError):
        await resolve_call_profile(MODEL_ID, served_via=ServedVia.model_validate(SV))


# ── G2 / G8: nothing moves a device run ──────────────────────────────────────
def _overload() -> Any:
    from matrx_ai.providers.errors import RetryableError

    return RetryableError(
        error_type="provider_overloaded", message="busy", status_code=529, is_retryable=True
    )


def test_g8_reroute_predicate_and_decision_refuse_a_device_run() -> None:
    from matrx_ai.orchestrator.overload_reroute import (
        OverloadPolicy,
        decide_overload_action,
        is_reroutable_provider_error,
    )

    sv = ServedVia.model_validate(SV)
    assert is_reroutable_provider_error(_overload()) is True
    assert is_reroutable_provider_error(_overload(), served_via=sv) is False
    decision = decide_overload_action(
        error_info=_overload(), current_model=MODEL_ID, attempts_on_model=9,
        policy=OverloadPolicy(retry_max_attempts=1, fallback_ref="gpt-5.4-nano"),
        models_tried=[], hops=0, produced_output=False,
        current_offering_id="off-1", sibling_offering_ids=["off-2"], served_via=sv,
    )
    assert decision.action == "give_up" and decision.to_model is None


@pytest.mark.asyncio
async def test_g8_policy_and_ladder_are_empty_for_a_device_run(monkeypatch) -> None:
    from matrx_ai.orchestrator.overload_reroute import (
        OverloadRerouteState,
        load_offering_ladder,
        load_overload_policy,
    )

    _seed(monkeypatch, with_offering=True)
    sv = ServedVia.model_validate(SV)
    policy = await load_overload_policy(MODEL_ID, OverloadRerouteState(), served_via=sv)
    assert policy.retry_max_attempts == 0 and policy.fallback_ref is None
    ladder = await load_offering_ladder(
        MODEL_ID, routing_offering_id=None, offerings_tried=[], served_via=sv
    )
    assert ladder is None


def test_g8_same_model_retries_never_run_for_a_device_run() -> None:
    from matrx_ai.providers.device.route_guard import may_retry_provider_error

    config = _config(served_via=ServedVia.model_validate(SV))
    assert may_retry_provider_error(config, _overload()) is False
    assert may_retry_provider_error(_config(), _overload()) is True
    from matrx_utils.source_guard import stable_source

    from matrx_ai.orchestrator import executor

    source = stable_source(executor)
    assert "may_retry_provider_error(" in source, "the executor's retry decision skips the guard"
    assert "is_reroutable_provider_error(error_info, served_via=" in source


@pytest.mark.asyncio
async def test_g8_free_tier_swap_never_moves_a_device_run(monkeypatch) -> None:
    from matrx_ai.providers import free_tier_models

    monkeypatch.setattr(free_tier_models, "policy_for", lambda _ctx: SimpleNamespace(tier="free"))

    async def target(*_a: Any, **_k: Any) -> Any:
        return ("gpt-5.4-nano", None)

    monkeypatch.setattr(free_tier_models, "free_tier_target", target)
    config = _config(served_via=ServedVia.model_validate(SV))
    profile = SimpleNamespace(
        model_name="qwen3-4b", route_kind="device", capabilities=SimpleNamespace(interaction="turn")
    )
    assert await free_tier_models.swap_for_free_tier(config, profile) is False
    assert config.model == MODEL_ID and config.served_via is not None


@pytest.mark.asyncio
async def test_g8_a_child_safety_swap_refuses_a_device_run_instead_of_moving_it() -> None:
    from matrx_ai.providers import child_safety_gate
    from matrx_ai.providers.device.errors import DeviceRouteMoveRefusedError

    async def swap_to_safe_model(config: Any) -> None:
        if config is not None:
            config.model = "safe-cloud-model"

    child_safety_gate.set_child_safety_host(swap_to_safe_model)
    try:
        config = _config(served_via=ServedVia.model_validate(SV))
        with pytest.raises(DeviceRouteMoveRefusedError) as raised:
            await child_safety_gate.admit_child_safety(config)
        assert raised.value.error_info.is_retryable is False
        assert config.model == MODEL_ID, "the device run is never moved to the swap target"
        cloud = _config()
        await child_safety_gate.admit_child_safety(cloud)
        assert cloud.model == "safe-cloud-model"
    finally:
        child_safety_gate.set_child_safety_host(None)


@pytest.mark.asyncio
async def test_g2_device_chat_is_registered_and_without_a_device_route_calls_nothing() -> None:
    from matrx_ai.config.provider_profiles import STRICT_ALTERNATION_WIRES, chat_provider_of
    from matrx_ai.providers import DeviceChat
    from matrx_ai.providers.device.errors import DeviceRouteError
    from matrx_ai.providers.provider_io_capabilities import endpoint_serializer_style
    from matrx_ai.providers.unified_client import _WIRE_CAPTURED_CLIENT_ATTRS, UnifiedAIClient

    assert UnifiedAIClient._PROVIDER_FACTORIES["device_chat"] == "DeviceChat"
    assert "device_chat" in _WIRE_CAPTURED_CLIENT_ATTRS
    assert "device_chat" in STRICT_ALTERNATION_WIRES
    assert endpoint_serializer_style("device_chat") == "openai_chat"
    assert chat_provider_of(SimpleNamespace(capabilities=None, client_attr="device_chat",
                                            wire_format="device_chat")) == "generic_openai"
    client = DeviceChat()
    assert client.provider_name == "device"
    # A profile that is not a resolved device route is refused before anything is sent (the
    # transport's own guards: tests/test_device_relay_transport.py).
    with pytest.raises(DeviceRouteError) as raised:
        await client.execute(_config(), SimpleNamespace(served_via=ServedVia.model_validate(SV)))
    assert raised.value.error_info.is_retryable is False


# ── call record ──────────────────────────────────────────────────────────────
def test_the_usage_row_says_where_the_call_ran() -> None:
    from matrx_ai.config.usage_config import TokenUsage
    from matrx_ai.providers.unified_client import UnifiedAIClient

    usage = TokenUsage(input_tokens=10, output_tokens=5)
    profile = SimpleNamespace(
        offering_id=f"device:{DEVICE}", resolution_route="preferred", route_kind="device",
        served_via=ServedVia.model_validate(SV),
    )
    UnifiedAIClient._stamp_offering_usage(SimpleNamespace(usage=usage), profile, _config())
    served = usage.metadata["served_via"]
    assert (served["provider"], served["app_instance_id"]) == ("device", DEVICE)
    # The row also names the model the computer ran (an own file has no ai_model_id).
    assert served["local_model_id"] == SV["local_model_id"]
    assert set(served) == {"provider", "app_instance_id", "local_model_id", "model_key", "model_name"}
    assert usage.metadata["device_served"] is True


# ── G13 / G14 ────────────────────────────────────────────────────────────────
def test_g13_a_mandate_cannot_set_served_via() -> None:
    from matrx_ai.mandates import HolderRef, MandateResolution

    with pytest.raises(ServedViaRefusedError):
        MandateResolution(config_overrides={"model": MODEL_ID, "served_via": SV})
    with pytest.raises(ServedViaRefusedError):
        HolderRef(type="agent", id=MODEL_ID, config_overrides={"served_via": SV})
    assert MandateResolution(config_overrides={"model": MODEL_ID}).config_overrides


def test_g14_a_workflow_step_cannot_carry_served_via() -> None:
    from matrx_ai.graph_nodes.agent_action import AgentStartInput

    with pytest.raises(ValidationError, match="served_via"):
        AgentStartInput(agent_id=MODEL_ID, config_overrides={"served_via": SV})
    with pytest.raises(ValidationError, match="served_via"):
        AgentStartInput(agent_id=MODEL_ID, runtime_config_overrides={"served_via": SV})


@pytest.mark.asyncio
async def test_g14_a_child_agent_runs_its_own_model(monkeypatch) -> None:
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    import matrx_ai._ext as ext
    from matrx_ai.agents import executor as executor_mod
    from matrx_ai.agents.definition import Agent
    from matrx_ai.agents.executor import AgentRunResult
    from matrx_ai.db.agx_manager import AgxDefinition
    from matrx_ai.tools.implementations.agent_call import agent_call
    from matrx_ai.tools.models import ToolContext

    @contextlib.asynccontextmanager
    async def acting_as_caller(_ctx: Any = None):
        yield

    async def _value(v: Any) -> Any:
        return v

    monkeypatch.setitem(ext._registry, "acting_as_caller", acting_as_caller)
    monkeypatch.setattr(
        AgxDefinition, "load_by_id_or_none",
        classmethod(lambda _cls, _id: _value(SimpleNamespace(
            id=MODEL_ID, created_by=DEVICE, is_active=True, is_archived=False))),
    )
    built: list[dict[str, Any]] = []

    class _Child:
        name = "Summarizer"
        output_schema = None

    def from_agent(_cls: Any, *a: Any, **k: Any) -> Any:
        built.append(k)
        return _value(_Child())

    monkeypatch.setattr(Agent, "from_agent", classmethod(from_agent))

    async def fake_run_agent(_agent: Any, **_k: Any) -> AgentRunResult:
        return AgentRunResult(success=True, output="done", metadata={})

    monkeypatch.setattr(executor_mod, "run_agent", fake_run_agent)
    token = set_app_context(AppContext(emitter=None, user_id=DEVICE))
    try:
        await agent_call(
            {"agent_id": MODEL_ID, "settings": {"served_via": SV, "model": MODEL_ID}},
            ToolContext(call_id="call-1"),
        )
    finally:
        clear_app_context(token)
    assert built and built[0].get("config_overrides") is None


def test_the_cx_request_row_carries_where_the_call_ran() -> None:
    from matrx_ai.config.usage_config import TokenUsage
    from matrx_ai.context.app_context import AppContext, clear_app_context, set_app_context
    from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest

    usage = TokenUsage(
        input_tokens=10, output_tokens=5, matrx_model_name="qwen3-4b", api="device_chat",
        offering_id=f"device:{DEVICE}", offering_route="pinned",
        metadata={"served_via": {"provider": "device", "app_instance_id": DEVICE}},
    )
    request = AIMatrixRequest(
        conversation_id="c1", config=_config(served_via=ServedVia.model_validate(SV)),
        usage_history=[usage],
    )
    token = set_app_context(AppContext(emitter=None, user_id="u1"))
    try:
        row = CompletedRequest(request=request, iterations=1, final_response=None).to_storage_dict()[
            "requests"
        ][0]
    finally:
        clear_app_context(token)
    assert row["metadata"]["served_via"] == {"provider": "device", "app_instance_id": DEVICE}


# ── L3: a cloud → device switch mid-conversation sends a body llama-server accepts ──
def test_a_cloud_to_device_switch_sends_paired_tools_and_no_foreign_reasoning() -> None:
    import json
    from pathlib import Path

    from matrx_ai.config.message_config import UnifiedMessage
    from matrx_ai.config.unified_content import TextContent, ThinkingContent
    from matrx_ai.orchestrator.requests import AIMatrixRequest
    from matrx_ai.providers.generic_openai.translator import GenericOpenAITranslator
    from matrx_ai.testing.profile_factory import make_profile

    fixture = Path(__file__).parent / "fixtures" / "wire_replay" / "gemini_tool_turn_snapshot.json"
    config = AIMatrixRequest.from_dict(dict(json.loads(fixture.read_text())["unified_payload"])).config
    last = config.messages[-1]
    if last.role == "assistant" and any(getattr(c, "type", None) == "tool_call" for c in last.content):
        config.messages.pop()  # a finished run: the open call is closed the way the run did
    config.messages.append(UnifiedMessage(role="assistant", content=[
        ThinkingContent(text="Three violations; summarize.", provider="google", signature=b"SIG"),
        ThinkingContent(text="Anthropic-signed thought.", provider="anthropic", signature="sig-anthropic"),
        TextContent(text="Audit complete: 3 violations."),
    ]))
    config.apply_overrides(LLMParams(model=MODEL_ID, served_via=SV))
    config.append_or_extend_user_input("Now on my computer: list the three violations.")
    assert config.served_via is not None
    profile = make_profile(
        model_name="qwen3-4b", wire_format="device_chat",
        capabilities={"input": ["text"], "output": ["text"],
                      "features": ["function_calling"], "interaction": "turn"},
    )
    body = GenericOpenAITranslator().build_request(config, profile)
    messages = body["messages"]
    assert any(m.get("tool_calls") for m in messages), "the fixture's tool turns reach the device"

    called: list[str] = []
    for index, message in enumerate(messages):
        for call in message.get("tool_calls") or []:
            called.append(call["id"])
            answered = [m for m in messages[index + 1:] if m.get("role") == "tool"]
            assert call["id"] in [m.get("tool_call_id") for m in answered], f"orphan call {call['id']}"
    for message in messages:
        if message.get("role") == "tool":
            assert message.get("tool_call_id") in called, "a tool result with no call"
    wire = json.dumps(body, default=str)
    for foreign in ("thought_signature", "thoughtSignature", "redacted_thinking", "__b64",
                    '"signature"', '"type": "thinking"', "SIG", "sig-anthropic"):
        assert foreign not in wire, f"{foreign} would be rejected by llama-server"
    for message in messages:
        content = message.get("content")
        if isinstance(content, list):
            assert {p.get("type") for p in content} <= {"text", "image_url"}


# ── a person's own uncatalogued file: model = local_model_id = device_model_file.id ──
def _own_sv() -> ServedVia:
    return ServedVia.model_validate({**SV, "local_model_id": FILE_ID})


@pytest.fixture
def own_file_placement(monkeypatch: pytest.MonkeyPatch):
    from matrx_ai.catalog import device_placement
    from matrx_ai.db.ai_models.ai_model_manager import ai_model_manager_instance

    async def load_model(_ref: str) -> Any:
        return None  # not in ai.model_definition

    monkeypatch.setattr(ai_model_manager_instance, "load_model", load_model)
    verdict: dict[str, Any] = {
        "value": device_placement.DeviceOwnFile(
            file_id=FILE_ID, name="my-finetune.gguf", metadata={"gguf": {"context_length": 32768}}
        )
    }

    async def check(served_via: ServedVia, *, model_id: str) -> Any:
        return verdict["value"]

    device_placement.configure_device_placement(check)
    yield verdict
    device_placement.configure_device_placement(None)


@pytest.mark.asyncio
async def test_an_own_file_resolves_from_what_the_file_knows(own_file_placement) -> None:
    from matrx_ai.catalog.resolve import resolve_call_profile

    profile = await resolve_call_profile(FILE_ID, served_via=_own_sv())
    assert profile.route_kind == "device" and profile.client_attr == "device_chat"
    assert profile.model_id == FILE_ID and profile.model_name == "my-finetune"
    assert profile.provider_model_id == FILE_ID and profile.pricing is None
    facts = profile.offering_metadata["device_facts"]
    assert facts["source"] == "device_model_file"
    assert facts["context_window"] == {"value": 32768, "source": "device_reported"}
    assert "max_output_tokens" in facts["unknown"] and "function_calling" in facts["unknown"]


@pytest.mark.asyncio
async def test_an_own_file_with_no_reported_context_says_unknown(own_file_placement) -> None:
    from matrx_ai.catalog import device_placement
    from matrx_ai.catalog.resolve import resolve_call_profile

    own_file_placement["value"] = device_placement.DeviceOwnFile(file_id=FILE_ID, name=None, metadata={})
    profile = await resolve_call_profile(FILE_ID, served_via=_own_sv())
    facts = profile.offering_metadata["device_facts"]
    assert facts["context_window"] == {"value": None, "source": "unknown"}
    assert "context_window" in facts["unknown"]
    assert profile.model_name == f"own model file {FILE_ID}"


@pytest.mark.asyncio
async def test_an_own_file_the_placement_refuses_raises_its_twin_code(own_file_placement) -> None:
    from matrx_ai.catalog import device_placement
    from matrx_ai.catalog.resolve import resolve_call_profile
    from matrx_ai.providers.device.errors import ModelNotOnDeviceError

    for code in ("file_not_usable", "not_own_file", "unknown_model"):
        own_file_placement["value"] = device_placement.DevicePlacementRefusal(code=code, message=code)
        with pytest.raises(ModelNotOnDeviceError) as raised:
            await resolve_call_profile(FILE_ID, served_via=_own_sv())
        assert raised.value.error_info.details["code"] == code
    # Admitted, but as a CATALOG model: the uncatalogued ref is still not an own file.
    own_file_placement["value"] = None
    with pytest.raises(ModelNotOnDeviceError) as raised:
        await resolve_call_profile(FILE_ID, served_via=_own_sv())
    assert raised.value.error_info.details["code"] == "not_own_file"


@pytest.mark.asyncio
async def test_an_unknown_model_without_a_matching_device_pick_still_refuses(own_file_placement) -> None:
    from matrx_ai.catalog.errors import CatalogRoutingError
    from matrx_ai.catalog.resolve import resolve_call_profile

    with pytest.raises(CatalogRoutingError, match="unknown model"):
        await resolve_call_profile(FILE_ID)
    with pytest.raises(CatalogRoutingError, match="unknown model"):
        await resolve_call_profile(MODEL_ID, served_via=_own_sv())  # model != local_model_id
