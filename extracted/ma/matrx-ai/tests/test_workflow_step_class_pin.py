"""A workflow step's chosen model CLASS runs — the ``offering_id`` beside ``model``.

Rule (2026-10-01): a model's class is its serving endpoint ("Matrx Fast",
"Matrx Lightning"); the person's choice travels as ``offering_id`` and MUST run.
A class belongs to one model, so a step's ``offering_id`` rides only with the
``model`` the same step names; a pin with no model, or of another model, is
dropped loudly. Live shape: Qwen3.8 27B = Fast 2245f5ca… (groq) + Lightning
29874e67… (cerebras).

Each test here failed against the code before this change (the node schemas
had no ``offering_id``; ``hold_step`` filled a Holder's pin onto any model or
dropped the author's; ``HeldCall.pin_for`` took no explicit class; the agent
step layered override dicts with a bare spread).
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

import matrx_ai.mandates as mandates
from matrx_ai.agents.named import AgentSource
from matrx_ai.graph_nodes import class_pin
from matrx_ai.graph_nodes.mandates import hold_step
from matrx_ai.mandates import MandateResolution
from matrx_ai.orchestrator.mandate_carrier import reset_reported_signatures

QWEN = "572667d5-bc84-449c-800e-e89acd36b5f5"
MINI = "11111111-2222-4333-8444-555555555555"
FAST = "2245f5ca-2dd2-4fed-b34f-7f30aa2c1c6d"
LIGHTNING = "29874e67-5683-40c2-9adb-fb797ea9a176"


@pytest.fixture(autouse=True)
def _fresh_scream_dedupe():
    reset_reported_signatures()
    yield
    reset_reported_signatures()


class _FakeCatalog:
    """The slice of AiCatalogManager ``node_class_pin`` reads."""

    _loaded = True

    def offering(self, offering_id: str) -> Any:
        owners = {FAST: QWEN, LIGHTNING: QWEN}
        owner = owners.get(str(offering_id))
        return SimpleNamespace(model_id=owner) if owner else None

    def resolve_model_ref(self, ref: str) -> str:
        return {"qwen3.8-27b": QWEN}.get(ref, ref)


@pytest.fixture
def catalog(monkeypatch: pytest.MonkeyPatch) -> _FakeCatalog:
    import matrx_ai.catalog.manager as manager_mod

    fake = _FakeCatalog()
    monkeypatch.setattr(manager_mod, "ai_catalog_manager", fake)
    return fake


# ── 1. node_class_pin: the one rule ──────────────────────────────────────────


def test_a_class_beside_its_own_model_runs(catalog: _FakeCatalog) -> None:
    assert class_pin.node_class_pin(QWEN, LIGHTNING, where="t") == LIGHTNING
    assert class_pin.node_class_pin("qwen3.8-27b", LIGHTNING, where="t") == LIGHTNING


def test_a_class_with_no_model_is_dropped_loudly(catalog, caplog) -> None:
    with caplog.at_level("WARNING"):
        assert class_pin.node_class_pin(None, LIGHTNING, where="ai.llm.chat") is None
    assert "DROPPED" in caplog.text


def test_a_class_of_another_model_is_dropped_loudly(catalog, caplog) -> None:
    with caplog.at_level("WARNING"):
        assert class_pin.node_class_pin(MINI, LIGHTNING, where="ai.llm.chat") is None
    assert "belongs to model_id" in caplog.text


# ── 2. A held call: the author's explicit class wins with the author's model ──


def _held(offering_id: str | None = FAST) -> mandates.HeldCall:
    return mandates.HeldCall(
        mandate_key="x.y",
        model=QWEN,
        system="S",
        temperature=None,
        max_output_tokens=None,
        turns=[],
        config=SimpleNamespace(),
        metadata={},
        offering_id=offering_id,
    )


def test_held_call_runs_the_authors_class_for_the_authors_model(catalog) -> None:
    assert _held().pin_for(QWEN, LIGHTNING) == {"offering_id": LIGHTNING}
    # Author's class with no author model: dropped; the Holder's own pin stays.
    assert _held().pin_for(None, LIGHTNING) == {"offering_id": FAST}
    # Another model's class beside MINI: dropped; MINI is not the Holder's model.
    assert _held().pin_for(MINI, LIGHTNING) == {}


@pytest.mark.asyncio
async def test_run_held_pydantic_carries_the_authors_class(monkeypatch, catalog) -> None:
    import matrx_ai.graph_nodes._strict_json as funnel

    seen: dict[str, Any] = {}

    async def _fake(**kwargs: Any) -> Any:
        seen.update(kwargs)
        return SimpleNamespace(model_dump=lambda **_k: {})

    async def _finish(*_a: Any, **_k: Any) -> None:
        return None

    monkeypatch.setattr(funnel, "llm_to_pydantic", _fake)
    monkeypatch.setattr(mandates.HeldCall, "finish", _finish)
    held = _held(FAST)  # the Holder runs QWEN·Fast; the author picked QWEN·Lightning
    await mandates.run_held_pydantic(
        held, output_cls=dict, user="hi", model=QWEN, offering_id=LIGHTNING
    )
    assert seen["model"] == QWEN
    assert seen["offering_id"] == LIGHTNING


# ── 3. hold_step: the class goes with whoever chose the model ────────────────


class _PinnedHolderConfig:
    model = QWEN
    offering_id = FAST
    system_instruction = "RULES"
    temperature = None


class _PinnedHolder:
    name = "Holder"
    config = _PinnedHolderConfig()


class _Source(AgentSource):
    agent_id: str = "holder"
    is_version: bool = False

    async def load(self) -> Any:
        return _PinnedHolder()


def _install(monkeypatch, overrides: dict[str, Any] | None = None) -> None:
    async def _resolver(_key: str) -> MandateResolution:
        return MandateResolution(source=_Source(), config_overrides=overrides)

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", _resolver)


@pytest.mark.asyncio
async def test_authors_class_runs_with_authors_model(monkeypatch, catalog) -> None:
    _install(monkeypatch)
    held = await hold_step(
        {"model": QWEN, "offering_id": LIGHTNING, "messages": []},
        spec_type="ai.llm",
        consumer="ai.llm.chat",
    )
    assert held.config["offering_id"] == LIGHTNING


@pytest.mark.asyncio
async def test_holders_class_never_lands_on_the_authors_model(monkeypatch, catalog) -> None:
    """The Holder runs QWEN·Fast; the author picked MINI with no class — the
    Holder's Fast pin used to be filled onto MINI (a pin of another model)."""
    _install(monkeypatch)
    held = await hold_step(
        {"model": MINI, "offering_id": None, "messages": []},
        spec_type="ai.llm",
        consumer="ai.llm.chat",
    )
    assert held.config["offering_id"] is None


@pytest.mark.asyncio
async def test_holders_class_rides_when_the_holder_chose_the_model(monkeypatch, catalog) -> None:
    _install(monkeypatch)
    held = await hold_step(
        {"model": None, "offering_id": None, "messages": []},
        spec_type="ai.llm",
        consumer="ai.llm.chat",
    )
    assert held.config["model"] == QWEN
    assert held.config["offering_id"] == FAST


@pytest.mark.asyncio
async def test_a_binding_that_moves_the_model_drops_the_holders_class(monkeypatch, catalog) -> None:
    _install(monkeypatch, overrides={"model": MINI})
    held = await hold_step(
        {"model": None, "offering_id": None, "messages": []},
        spec_type="ai.llm",
        consumer="ai.llm.chat",
    )
    assert held.config["model"] == MINI
    assert held.config["offering_id"] is None


# ── 4. Every ai.* node: the class field exists and reaches the call ──────────


def _all_node_schemas() -> list[tuple[str, dict[str, Any]]]:
    from matrx_graph.actions.registry import default_action_registry

    from matrx_ai.graph_nodes import register_with_graph

    register_with_graph()
    found: list[tuple[str, dict[str, Any]]] = []
    for spec in default_action_registry().all():
        found.append((f"{spec.name}:input", spec.input_schema.model_json_schema()))
        found.append((f"{spec.name}:config", spec.node_spec.config_json_schema()))
    return found


def test_every_model_field_declares_its_class_field() -> None:
    missing: list[str] = []
    checked = 0
    for name, schema in _all_node_schemas():
        props = schema.get("properties") or {}
        for key, prop in props.items():
            named_model = key == "model" or key.endswith("_model")
            if prop.get("ui:widget") != "model_picker" and not named_model:
                continue
            checked += 1
            sibling = prop.get("ui:class_field")
            if prop.get("ui:widget") != "model_picker" or not sibling or sibling not in props:
                missing.append(f"{name}.{key}")
    assert checked >= 8, "the census must actually see the ai.* model fields"
    assert missing == [], f"model fields with no class field: {missing}"


@pytest.mark.asyncio
async def test_ai_llm_chat_runs_the_chosen_class(monkeypatch, catalog) -> None:
    import matrx_ai.orchestrator.executor as executor
    from matrx_ai.graph_nodes.llm_action import LlmChatInput, llm_chat

    _install(monkeypatch)
    sent: dict[str, Any] = {}

    class _Stop(Exception):
        pass

    async def _fake_execute(config: Any, **_k: Any) -> Any:
        sent["model"] = config.model
        sent["offering_id"] = config.offering_id
        raise _Stop

    monkeypatch.setattr(executor, "execute_ai_request", _fake_execute)
    with pytest.raises(_Stop):
        await llm_chat(
            SimpleNamespace(),
            LlmChatInput(model=QWEN, offering_id=LIGHTNING, prompt="hi"),
        )
    assert sent == {"model": QWEN, "offering_id": LIGHTNING}


# ── 5. The agent step layers overrides with THE one merge ────────────────


def test_agent_step_drops_the_mandates_class_when_the_author_moves_the_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Mandate binding {QWEN, Fast} under the author's {MINI}: the bare spread
    sent {MINI, Fast} — a pin of another model, which the resolver refuses."""
    from matrx_ai import _ext
    from matrx_ai.graph_nodes.agent_action import AgentStartInput, StepAgent, build_agent_request

    class _Req:
        @classmethod
        def model_validate(cls, payload: dict[str, Any]) -> Any:
            return SimpleNamespace(**payload)

    monkeypatch.setitem(_ext._registry, "AgentStartRequest", _Req)
    request = build_agent_request(
        SimpleNamespace(organization_id="org-1", node_id="n1"),
        AgentStartInput(agent_id="a1", config_overrides={"model": MINI}),
        StepAgent(
            agent_id="a1",
            is_version=False,
            config_overrides={"model": QWEN, "offering_id": FAST},
            declared_output_kind=None,
        ),
        node_type="ai.agent.start",
    )
    assert request.config_overrides == {"model": MINI}


# ── 6. Observational memory: the memory model's class rides the memory call ──


def test_memory_factory_carries_the_memory_models_class(monkeypatch, catalog) -> None:
    import matrx_ai.memory.factory as factory

    monkeypatch.setattr(factory, "DbObservationalMemoryStorage", lambda: object())
    om = factory.build_observational_memory(
        SimpleNamespace(
            memory_enabled=True,
            store=True,
            user_id="u1",
            organization_id="o1",
            memory_model=QWEN,
            memory_offering_id=LIGHTNING,
            memory_scope="thread",
        ),
        "conv-1",
    )
    assert om is not None
    assert om.config.observation.model.offering_id == LIGHTNING
    assert om.config.reflection.model.offering_id == LIGHTNING


@pytest.mark.asyncio
async def test_observer_hands_the_class_to_the_memory_call() -> None:
    from matrx_ai.memory.observer_agent import run_observer
    from matrx_ai.memory.types import ModelConfig

    seen: dict[str, Any] = {}

    async def _llm(**kwargs: Any) -> str:
        seen.update(kwargs)
        return "<observations>\n* note\n</observations>"

    try:
        await run_observer(
            ModelConfig(mandate_key="memory.observer", model=QWEN, offering_id=LIGHTNING),
            "material",
            _llm,
        )
    except ValueError:
        pass  # parsing is not under test; the call's arguments are
    assert seen["model"] == QWEN
    assert seen["offering_id"] == LIGHTNING


def test_memory_model_fields_on_agent_and_conversation_steps_carry_a_class() -> None:
    from matrx_ai.graph_nodes.agent_action import AgentStartInput
    from matrx_ai.graph_nodes.conversation_action import ConversationContinueInput

    for model in (AgentStartInput, ConversationContinueInput):
        props = model.model_json_schema()["properties"]
        assert props["memory_model"]["ui:widget"] == "model_picker"
        assert props["memory_model"]["ui:class_field"] == "memory_offering_id"
        assert "memory_offering_id" in props
