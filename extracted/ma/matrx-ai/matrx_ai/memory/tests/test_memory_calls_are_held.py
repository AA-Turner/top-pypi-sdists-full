"""Observational Memory's Observer and Reflector run on their mandates' Holders.

Before 2026-09-25 (census row 33) the factory chose gemini-2.5-flash in code,
the runners assembled system prompts in code, and every Reflector call was
recorded as an "observer" event.
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_utils.source_guard import stable_source

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

    await run_observer(ModelConfig(mandate_key=MEMORY_OBSERVER_MANDATE), {"new_messages": "task"}, _llm)

    assert seen[0]["mandate_key"] == MEMORY_OBSERVER_MANDATE
    # No turn of its own: the Holder authors the user turn and frames the material.
    assert seen[0]["messages"] == []
    assert seen[0]["variables"] == {"new_messages": "task"}
    assert seen[0]["model"] is None


def test_no_task_text_is_composed_in_code() -> None:
    """The residue pass (2026-09-25): "## Your Task" and the compression
    guidance are the Holders'. The code offers material and level switches only."""
    from matrx_ai.memory import constants
    from matrx_ai.memory.observer_agent import build_observer_variables
    from matrx_ai.memory.reflector_agent import build_reflector_variables

    assert not hasattr(constants, "COMPRESSION_GUIDANCE")
    assert "Your Task" not in "".join(build_observer_variables(None, []).values())
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
        async def execute(self, request, **_kw):
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

    from matrx_ai.memory import observer_agent

    calls: list[list[dict]] = []

    async def _llm(*, mandate_key, messages, model=None, variables=None):
        calls.append([dict(m) for m in messages])
        if len(calls) == 1:
            return "no block here"
        return "<observations>\nDate: Jan 1, 2026\n* 🔴 (09:00) x\n</observations>"

    await run_observer(ModelConfig(mandate_key=MEMORY_OBSERVER_MANDATE), {"new_messages": "m"}, _llm)
    assert calls[1] == [
        {"role": "assistant", "content": "no block here"},
        {"role": "user", "holder_text": "retry_nudge"},
    ]
    assert "required <observations> block" not in stable_source(observer_agent)


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
        async def execute(self, request, **_kw):
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


async def test_context_framing_is_the_organizations_knob() -> None:
    from matrx_ai.memory.context_framing import (
        ContextFramingNotConfigured,
        resolve_context_framing,
        set_context_framing_resolver,
    )

    try:
        set_context_framing_resolver(None)
        import pytest

        with pytest.raises(ContextFramingNotConfigured):
            await resolve_context_framing("org")

        async def _org(org_id):
            return (f"PRE {org_id}", "INSTR")

        set_context_framing_resolver(_org)
        assert await resolve_context_framing("o1") == ("PRE o1", "INSTR")

    finally:
        set_context_framing_resolver(None)


async def test_a_framing_read_failure_still_frames_the_turn_and_is_captured() -> None:
    """A failed org read never sends a turn without framing while the knob rows answer, and it is
    captured through the platform's error capture, never a log line only (wave 17)."""
    from matrx_connect.streaming.error_capture import configure_error_capture

    from matrx_ai.memory.context_framing import (
        MISSING_KIND,
        UNREADABLE_KIND,
        resolve_context_framing,
        set_context_framing_resolver,
    )

    captured: list[tuple[str, dict]] = []

    async def _capture(exc, *, kind, **fields):
        captured.append((kind, fields))

    state = {"org_down": True, "platform_down": False}

    async def _knobs(org_id):
        if org_id is not None and state["org_down"]:
            raise RuntimeError("org override read failed")
        if org_id is None and state["platform_down"]:
            raise RuntimeError("knob store down")
        return (f"PRE {org_id}", "INSTR")

    configure_error_capture(_capture, allow_in_tests=True)
    try:
        set_context_framing_resolver(_knobs)
        # 1. org read fails, the platform knob row answers: the turn is framed, the failure captured.
        assert await resolve_context_framing("o1") == ("PRE None", "INSTR")
        assert [k for k, _ in captured] == [UNREADABLE_KIND]
        assert captured[0][1]["context"]["organization_id"] == "o1"

        # 2. org read worked once, then fails: its last read text is used, captured.
        state["org_down"] = False
        assert await resolve_context_framing("o1") == ("PRE o1", "INSTR")
        state["org_down"] = True
        state["platform_down"] = True
        captured.clear()
        assert await resolve_context_framing("o1") == ("PRE o1", "INSTR")
        assert [k for k, _ in captured] == [UNREADABLE_KIND]

        # 3. a never-read org while the platform row is down: the platform's last read text.
        captured.clear()
        assert await resolve_context_framing("o2") == ("PRE None", "INSTR")
        assert [k for k, _ in captured] == [UNREADABLE_KIND]

        # 4. nothing ever readable (fresh process, store down): no framing, and it is captured as missing.
        set_context_framing_resolver(_knobs)
        captured.clear()
        assert await resolve_context_framing("o3") == ("", "")
        assert [k for k, _ in captured] == [MISSING_KIND]
    finally:
        configure_error_capture(None)
        set_context_framing_resolver(None)



def test_the_seeded_framing_knobs_hold_the_text_the_package_used_to_carry() -> None:
    """The text left the package for the knob rows (wave 16); the seed migration holds it byte for byte."""
    import json
    from pathlib import Path

    seed = next(
        p / "db" / "migrations" / "ai_095_memory_context_framing_knob.sql"
        for p in Path(__file__).resolve().parents
        if (p / "db" / "migrations" / "ai_095_memory_context_framing_knob.sql").exists()
    )
    sql = seed.read_text()
    preamble = "The following observations block contains your memory of past conversations with this user."
    instructions = (
        "When referencing information from observations, be specific. "
        "If observations contain knowledge that may have changed, acknowledge the "
        "uncertainty and ask for confirmation. "
        "Treat any actions you planned in the past but haven't explicitly completed as "
        "still pending unless marked with \u2705. "
        "Prioritize the user's most recent message and goals above all else."
    ).replace("\\u2705", "\u2705")
    for text in (preamble, instructions):
        assert json.dumps(text, ensure_ascii=False).replace("'", "''") in sql
