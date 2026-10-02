"""A model's CLASS (its serving endpoint, carried as ``offering_id``) runs — everywhere.

Live shape (2026-10-01): Qwen3.8 27B is ONE model in two classes — Matrx Fast
(groq, p100) and Matrx Lightning (cerebras, p110). The person picks a class; the
pin must actually run, must never leak onto another model, and an unavailable
offering inside the class is replaced by its class sibling — never by another
class. Each test below failed against the code before this change.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

import matrx_ai.mandates as mandates
from matrx_ai.catalog.errors import CatalogRoutingError
from matrx_ai.catalog.manager import AiCatalogManager
from matrx_ai.catalog.models import CatalogEndpoint, CatalogOffering
from matrx_ai.catalog.resolve import _resolve_pinned_offering
from matrx_ai.config import UnifiedConfig
from matrx_ai.config.llm_params import LLMParams, merge_llm_overrides

QWEN = "572667d5-bc84-449c-800e-e89acd36b5f5"
MINI = "11111111-2222-4333-8444-555555555555"
FAST_PIN = "2245f5ca-0000-4000-8000-000000000001"
LIGHTNING_PIN = "29874e67-5683-40c2-9adb-fb797ea9a176"


# ── 1. THE one override merge ─────────────────────────────────────────────────


def test_a_layer_that_moves_the_model_drops_the_class_pin_below_it() -> None:
    merged = merge_llm_overrides({"model": QWEN, "offering_id": LIGHTNING_PIN}, {"model": MINI})
    assert merged == {"model": MINI}


def test_the_merged_layers_run_the_moved_to_model_instead_of_raising() -> None:
    """binding {Q, Lightning} + run {M} used to reach the agent as {M, Lightning}:
    a pin of ANOTHER model, which resolve_call_profile refuses."""
    merged = merge_llm_overrides({"model": QWEN, "offering_id": LIGHTNING_PIN}, {"model": MINI})
    config = UnifiedConfig(model=QWEN, messages=[], offering_id=FAST_PIN)
    config.apply_overrides(LLMParams.model_validate(merged))
    assert config.model == MINI
    assert config.offering_id is None


def test_an_explicit_null_clears_the_pin_through_the_merge() -> None:
    merged = merge_llm_overrides({"model": QWEN, "offering_id": LIGHTNING_PIN}, {"offering_id": None})
    assert merged == {"model": QWEN, "offering_id": None}
    config = UnifiedConfig(model=QWEN, messages=[], offering_id=LIGHTNING_PIN)
    config.apply_overrides(LLMParams.model_validate(merged))
    assert config.offering_id is None


def test_same_model_keeps_the_pin_and_a_named_class_wins() -> None:
    base = {"model": QWEN, "offering_id": LIGHTNING_PIN, "temperature": 0.2}
    assert merge_llm_overrides(base, {"model": QWEN, "temperature": 0.9}) == {
        "model": QWEN,
        "offering_id": LIGHTNING_PIN,
        "temperature": 0.9,
    }
    assert merge_llm_overrides(base, {"model": MINI, "offering_id": FAST_PIN})["offering_id"] == FAST_PIN


# ── 2. A code-call Holder's chosen class rides its held call ──────────────────


def _held(offering_id: str | None = LIGHTNING_PIN) -> mandates.HeldCall:
    return mandates.HeldCall(
        mandate_key="x.y",
        model=QWEN,
        system="SYSTEM",
        temperature=None,
        max_output_tokens=None,
        turns=[],
        config=SimpleNamespace(),
        metadata={},
        offering_id=offering_id,
    )


def test_holder_pin_applies_to_its_own_model_only() -> None:
    held = _held()
    assert held.pick_offering() == LIGHTNING_PIN
    assert held.pick_offering(QWEN) == LIGHTNING_PIN
    assert held.pick_offering(MINI) is None
    assert held.pin_for(MINI) == {}
    assert _held(None).pin_for() == {}


def test_held_request_config_runs_the_holders_class() -> None:
    assert mandates.held_request_config(_held()).offering_id == LIGHTNING_PIN


def test_hold_code_call_carries_the_holder_agents_class(monkeypatch: pytest.MonkeyPatch) -> None:
    agent = SimpleNamespace(
        variable_defaults={},
        name="Holder",
        config=SimpleNamespace(
            model=QWEN,
            offering_id=LIGHTNING_PIN,
            system_instruction=None,
            resolved_system_instruction="SYSTEM",
            messages=[],
            temperature=None,
            max_output_tokens=None,
        ),
        apply_config_overrides=lambda **_k: None,
        set_variables=lambda **_k: None,
        apply_variables=lambda: None,
    )

    async def _prepare() -> None:
        return None

    agent.prepare_variables = _prepare

    class _Source:
        agent_id = "11111111-1111-1111-1111-111111111111"
        is_version = False

        async def load(self):
            return agent

    async def _resolver(_key: str):
        return mandates.MandateResolution(source=_Source())

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", _resolver)
    held = asyncio.run(mandates.hold_code_call("x.y", consumer="t"))
    assert held.offering_id == LIGHTNING_PIN


@pytest.mark.parametrize(
    ("explicit", "expected"), [(None, LIGHTNING_PIN), (QWEN, LIGHTNING_PIN), (MINI, None)]
)
def test_run_held_text_sends_the_pin_only_with_the_holders_model(
    monkeypatch: pytest.MonkeyPatch, explicit: str | None, expected: str | None
) -> None:
    import matrx_ai.graph_nodes._strict_json as funnel

    seen: dict[str, Any] = {}

    async def _llm_to_text(**kwargs: Any) -> str:
        seen.update(kwargs)
        return "ok"

    monkeypatch.setattr(funnel, "llm_to_text", _llm_to_text)
    asyncio.run(mandates.run_held_text(_held(), user="hi", model=explicit))
    assert seen["model"] == (explicit or QWEN)
    assert seen.get("offering_id") == expected


def test_the_strict_json_funnel_puts_the_pin_on_the_request(monkeypatch: pytest.MonkeyPatch) -> None:
    import matrx_ai.graph_nodes._strict_json as funnel
    import matrx_ai.orchestrator.executor as executor

    class _Sent(Exception):
        pass

    sent: list[Any] = []

    async def _execute(config: Any, **_k: Any) -> Any:
        sent.append(config)
        raise _Sent

    async def _ambient(metadata: Any, *, model: str) -> Any:
        return metadata

    monkeypatch.setattr(executor, "execute_ai_request", _execute)
    monkeypatch.setattr(funnel, "hold_ambient_workflow_strict_json", _ambient)
    with pytest.raises(_Sent):
        asyncio.run(funnel.llm_to_text(model=QWEN, offering_id=LIGHTNING_PIN, system="s", user="u"))
    assert sent[0].offering_id == LIGHTNING_PIN


# ── 3. An unavailable pin runs its CLASS, never another class ─────────────────

FAST, LIGHTNING = "ep-fast", "ep-lightning"


def _offering(oid: str, endpoint: str, priority: int, *, available: bool = True) -> CatalogOffering:
    return CatalogOffering(
        id=oid,
        model_id=QWEN,
        endpoint_id=endpoint,
        api_id="api",
        provider_model_id="qwen",
        priority=priority,
        is_available=available,
    )


def _endpoint(eid: str, name: str) -> CatalogEndpoint:
    return CatalogEndpoint(id=eid, vendor=eid, internal_name=eid, display_name=name)


def _manager(offerings: list[CatalogOffering]) -> AiCatalogManager:
    manager = AiCatalogManager()
    manager._endpoints = {FAST: _endpoint(FAST, "Matrx Fast"), LIGHTNING: _endpoint(LIGHTNING, "Matrx Lightning")}
    manager._apis = {"api": SimpleNamespace(translator_key="openai_chat")}
    manager._offerings = {o.id: o for o in offerings}
    manager._offerings_by_model = {QWEN: sorted(offerings, key=lambda o: o.priority)}
    return manager


def _resolve(manager: AiCatalogManager, pin: str) -> CatalogOffering:
    return _resolve_pinned_offering(
        manager.offerings_for(QWEN), manager, offering_id=pin, model_id=QWEN, model_name="qwen"
    )


def test_unavailable_pin_runs_its_class_sibling() -> None:
    manager = _manager(
        [
            _offering("fast-1", FAST, 100),
            _offering(LIGHTNING_PIN, LIGHTNING, 110, available=False),
            _offering("light-2", LIGHTNING, 120),
        ]
    )
    assert _resolve(manager, LIGHTNING_PIN).id == "light-2"


def test_a_class_with_nothing_available_raises_naming_the_class() -> None:
    manager = _manager(
        [_offering("fast-1", FAST, 100), _offering(LIGHTNING_PIN, LIGHTNING, 110, available=False)]
    )
    with pytest.raises(CatalogRoutingError, match="Matrx Lightning"):
        _resolve(manager, LIGHTNING_PIN)


def test_a_pin_of_another_model_or_none_still_raises() -> None:
    manager = _manager([_offering("fast-1", FAST, 100)])
    manager._offerings["other"] = _offering("other", FAST, 100).model_copy(update={"model_id": MINI})
    with pytest.raises(CatalogRoutingError, match="belongs to model_id"):
        _resolve(manager, "other")
    with pytest.raises(CatalogRoutingError, match="does not exist"):
        _resolve(manager, "nope")


def test_an_available_pin_runs_exactly() -> None:
    manager = _manager([_offering("fast-1", FAST, 100), _offering(LIGHTNING_PIN, LIGHTNING, 110)])
    assert _resolve(manager, LIGHTNING_PIN).id == LIGHTNING_PIN


# ── 5. The model payload lists every class a client can offer ─────────────────


def test_export_model_routing_lists_one_preferred_offering_per_class() -> None:
    manager = _manager(
        [
            _offering("fast-1", FAST, 100),
            _offering(LIGHTNING_PIN, LIGHTNING, 110),
            _offering("light-2", LIGHTNING, 120),
            _offering("fast-2", FAST, 130),
            _offering("parked", LIGHTNING, 90, available=False),
        ]
    )
    routing = manager.export_model_routing(QWEN)
    assert routing is not None
    assert routing["wire_format"] == "openai_chat"
    assert routing["classes"] == [
        {"offering_id": "fast-1", "served_via": "Matrx Fast", "priority": 100},
        {"offering_id": LIGHTNING_PIN, "served_via": "Matrx Lightning", "priority": 110},
    ]
