"""Observational Memory's Observer and Reflector run on their mandates' Holders.

Before 2026-09-25 (census row 33) the factory chose gemini-2.5-flash in code,
the runners assembled system prompts in code, and every Reflector call was
recorded as an "observer" event.
"""

from __future__ import annotations

from types import SimpleNamespace

import matrx_ai.mandates as mandates
from matrx_ai.code_call_mandate_keys import MEMORY_OBSERVER_MANDATE, MEMORY_REFLECTOR_MANDATE
from matrx_ai.memory import factory
from matrx_ai.memory.observer_agent import run_observer
from matrx_ai.memory.types import ModelConfig, ObservationConfig, ReflectionConfig


def test_no_model_is_chosen_in_code() -> None:
    assert not hasattr(factory, "_DEFAULT_MODEL")
    assert ObservationConfig().model == ModelConfig(mandate_key=MEMORY_OBSERVER_MANDATE)
    assert ReflectionConfig().model == ModelConfig(mandate_key=MEMORY_REFLECTOR_MANDATE)


async def test_observer_sends_no_system_prompt_of_its_own() -> None:
    seen: list[dict] = []

    async def _llm(*, mandate_key, messages, model=None, variables=None):
        seen.append(
            {"mandate_key": mandate_key, "messages": messages, "model": model, "variables": variables}
        )
        return "<observations>\nDate: Jan 1, 2026\n* 🔴 (09:00) x\n</observations>"

    await run_observer(ModelConfig(mandate_key=MEMORY_OBSERVER_MANDATE), "task", _llm)

    assert seen[0]["mandate_key"] == MEMORY_OBSERVER_MANDATE
    # No turn of its own: the Holder authors the user turn and frames the material.
    assert seen[0]["messages"] == []
    assert seen[0]["variables"] == {"material": "task"}
    assert seen[0]["model"] is None


def test_no_task_text_is_composed_in_code() -> None:
    """The residue pass (2026-09-25): "## Your Task" and the compression
    guidance are the Holders'. The code offers material and level switches only."""
    from matrx_ai.memory import constants
    from matrx_ai.memory.observer_agent import build_observer_prompt
    from matrx_ai.memory.reflector_agent import build_reflector_variables

    assert not hasattr(constants, "COMPRESSION_GUIDANCE")
    assert "Your Task" not in build_observer_prompt(None, [])
    level_two = build_reflector_variables("obs", compression_level=2)
    assert "compression_guidance_level_2" not in level_two  # the Holder's text applies
    assert all(level_two[f"compression_guidance_level_{n}"] == "" for n in (1, 3, 4))
    assert "Your Task" not in "".join(level_two.values())


async def test_adapter_holds_the_call_and_names_the_reflector(monkeypatch) -> None:
    from matrx_ai.memory import llm_adapter

    held_keys: list[str] = []
    events: list[str] = []

    async def _hold(mandate_key, **_kwargs):
        held_keys.append(mandate_key)
        return mandates.HeldCall(
            mandate_key=mandate_key,
            model="holder-model",
            system="HOLDER",
            temperature=0.0,
            max_output_tokens=16000,
            turns=[{"role": "user", "content": "HOLDER TURN"}],
            config=SimpleNamespace(),
            metadata={},
        )

    class _Client:
        async def execute(self, request):
            assert request.config.model == "holder-model"
            assert str(request.config.system_instruction).endswith("HOLDER")
            return SimpleNamespace(
                messages=[SimpleNamespace(role="assistant", content=[SimpleNamespace(text="ok")])],
                usage=None,
            )

    async def _write_event(**kwargs):
        events.append(kwargs["event_type"])

    async def _emit(**_kwargs):
        return None

    monkeypatch.setattr(mandates, "hold_code_call", _hold)
    monkeypatch.setattr(llm_adapter, "_get_client", lambda: _Client())
    monkeypatch.setattr(llm_adapter, "_write_event", _write_event)
    monkeypatch.setattr(llm_adapter, "_emit_event", _emit)

    adapter = llm_adapter.MemoryLLMAdapter(ctx=SimpleNamespace(), conversation_id="c")
    out = await adapter(
        mandate_key=MEMORY_REFLECTOR_MANDATE, messages=[{"role": "user", "content": "x"}]
    )
    import asyncio

    for _ in range(10):
        await asyncio.sleep(0)
    assert out == "ok"
    assert held_keys == [MEMORY_REFLECTOR_MANDATE]
    assert events == ["reflector"]


async def test_adapter_refuses_a_holder_that_authors_no_user_turn(monkeypatch) -> None:
    import pytest

    from matrx_ai.memory import llm_adapter

    async def _hold(mandate_key, **_kwargs):
        return mandates.HeldCall(
            mandate_key=mandate_key,
            model="holder-model",
            system="HOLDER",
            temperature=0.0,
            max_output_tokens=16000,
            turns=[],
            config=SimpleNamespace(),
            metadata={},
        )

    monkeypatch.setattr(mandates, "hold_code_call", _hold)
    adapter = llm_adapter.MemoryLLMAdapter(ctx=SimpleNamespace(), conversation_id="c")
    with pytest.raises(mandates.MandateResolutionUnavailable, match="authors none"):
        await adapter(mandate_key=MEMORY_OBSERVER_MANDATE, messages=[], variables={"material": "m"})


async def test_observer_retry_nudge_is_the_holders_text() -> None:
    """Residue pass 2 (2026-09-25): the retry nudge is the Holder's
    ``retry_nudge`` variable — the code names it, never types it."""
    import inspect

    from matrx_ai.memory import observer_agent

    calls: list[list[dict]] = []

    async def _llm(*, mandate_key, messages, model=None, variables=None):
        calls.append([dict(m) for m in messages])
        if len(calls) == 1:
            return "no block here"
        return "<observations>\nDate: Jan 1, 2026\n* 🔴 (09:00) x\n</observations>"

    await run_observer(ModelConfig(mandate_key=MEMORY_OBSERVER_MANDATE), "m", _llm)
    assert calls[1] == [
        {"role": "assistant", "content": "no block here"},
        {"role": "user", "holder_text": "retry_nudge"},
    ]
    assert "required <observations> block" not in inspect.getsource(observer_agent)


async def test_adapter_sends_the_holders_retry_text_and_refuses_without_it(monkeypatch) -> None:
    import pytest

    from matrx_ai.memory import llm_adapter

    sent: list[list] = []
    values = {"retry_nudge": "HOLDER NUDGE"}

    async def _hold(mandate_key, **_kwargs):
        return mandates.HeldCall(
            mandate_key=mandate_key,
            model="holder-model",
            system="HOLDER",
            temperature=0.0,
            max_output_tokens=16000,
            turns=[{"role": "user", "content": "HOLDER TURN"}],
            config=SimpleNamespace(),
            metadata={},
            holder_values=dict(values),
        )

    class _Client:
        async def execute(self, request):
            sent.append(request.config.messages)
            return SimpleNamespace(
                messages=[SimpleNamespace(role="assistant", content=[SimpleNamespace(text="ok")])],
                usage=None,
            )

    async def _noop(**_kwargs):
        return None

    monkeypatch.setattr(mandates, "hold_code_call", _hold)
    monkeypatch.setattr(llm_adapter, "_get_client", lambda: _Client())
    monkeypatch.setattr(llm_adapter, "_write_event", _noop)
    monkeypatch.setattr(llm_adapter, "_emit_event", _noop)
    adapter = llm_adapter.MemoryLLMAdapter(ctx=SimpleNamespace(), conversation_id="c")
    retry = [{"role": "assistant", "content": "bad"}, {"role": "user", "holder_text": "retry_nudge"}]
    await adapter(mandate_key=MEMORY_OBSERVER_MANDATE, messages=retry, variables={"material": "m"})
    texts = [
        "".join(getattr(part, "text", "") for part in (m.content or []))
        for m in sent[0]
    ]
    assert texts[-1] == "HOLDER NUDGE"

    values.clear()  # a Holder rebound to an agent that carries no nudge
    with pytest.raises(mandates.MandateResolutionUnavailable, match="retry_nudge"):
        await adapter(mandate_key=MEMORY_OBSERVER_MANDATE, messages=retry, variables={"material": "m"})


async def test_context_framing_is_the_organizations_knob(caplog) -> None:
    from matrx_ai.memory import constants
    from matrx_ai.memory.context_framing import (
        resolve_context_framing,
        set_context_framing_resolver,
    )

    try:
        set_context_framing_resolver(None)
        assert await resolve_context_framing("org") == (
            constants.OBSERVATION_CONTEXT_PROMPT,
            constants.OBSERVATION_CONTEXT_INSTRUCTIONS,
        )

        async def _org(org_id):
            return (f"PRE {org_id}", "INSTR")

        set_context_framing_resolver(_org)
        assert await resolve_context_framing("o1") == ("PRE o1", "INSTR")

        async def _broken(_org_id):
            raise RuntimeError("knob store down")

        set_context_framing_resolver(_broken)
        with caplog.at_level("ERROR"):
            got = await resolve_context_framing("o1")
        assert got[0] == constants.OBSERVATION_CONTEXT_PROMPT
        assert "knob could not be read" in caplog.text
    finally:
        set_context_framing_resolver(None)
