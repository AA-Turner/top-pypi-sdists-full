"""The Observer and Reflector hand every value over BY NAME (2026-10-07).

Before, the code joined the existing observations, current task, pending hint,
new messages and config instruction into one ``{{material}}`` block of
"## …" sections. Now each value is offered by name and the Holder's authored
user turn frames them. These tests drive the real runners through the real
adapter and the real ``hold_code_call`` against inline Holders, and read the
messages the provider client was actually handed.
"""

from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from matrx_ai.code_call_mandate_keys import MEMORY_OBSERVER_MANDATE, MEMORY_REFLECTOR_MANDATE
from matrx_ai.memory import llm_adapter
from matrx_ai.memory.observer_agent import build_observer_variables, run_observer
from matrx_ai.memory.reflector_agent import run_reflector
from matrx_ai.memory.types import Message, MessageRole, ModelConfig

_OBS_NAMES = (
    "existing_observations",
    "current_task",
    "pending_response_hint",
    "new_messages",
    "memory_instructions",
)
_REF_NAMES = ("observations", "current_task", "memory_instructions", "compression_guidance_level_2")


def _turn(names: tuple[str, ...]) -> str:
    return "\n".join(f"{name}=<{{{{{name}}}}}>" for name in names)


def _messages() -> list[Message]:
    at = datetime(2026, 10, 6, 21, 30, tzinfo=UTC)
    return [
        Message(id="m1", thread_id="t", resource_id="r", role=MessageRole.USER,
                content="Our clinic moved to Irvine; update the address on every page.", created_at=at),
        Message(id="m2", thread_id="t", resource_id="r", role=MessageRole.ASSISTANT,
                content="Updated 14 pages to 4 Park Plaza, Irvine.", created_at=at),
    ]


@pytest.fixture
def sent(monkeypatch: pytest.MonkeyPatch) -> list[list[str]]:
    from matrx_ai.testing.holders import install_inline_holders

    install_inline_holders(
        monkeypatch,
        {
            MEMORY_OBSERVER_MANDATE: {
                "model": "holder-model",
                "messages": [{"role": "system", "content": "OBSERVER RULES"},
                             {"role": "user", "content": _turn(_OBS_NAMES)}],
                "variables": [{"name": n, "defaultValue": "-"} for n in _OBS_NAMES],
            },
            MEMORY_REFLECTOR_MANDATE: {
                "model": "holder-model",
                "messages": [{"role": "system", "content": "REFLECTOR RULES"},
                             {"role": "user", "content": _turn(_REF_NAMES)}],
                "variables": [
                    *({"name": n, "defaultValue": "-"} for n in _REF_NAMES[:-1]),
                    {"name": "compression_guidance_level_2", "defaultValue": "LEVEL TWO GUIDANCE"},
                ],
            },
        },
    )
    calls: list[list[str]] = []

    class _Client:
        async def execute(self, request, **_kw):
            calls.append([
                "".join(getattr(part, "text", "") for part in (m.content or []))
                for m in request.config.messages
            ])
            return SimpleNamespace(
                messages=[SimpleNamespace(role="assistant", content=[SimpleNamespace(
                    text="<observations>\nDate: Oct 6, 2026\n* 🔴 (21:30) Clinic moved to Irvine\n</observations>")])],
                usage=None,
            )

    async def _noop(**_kwargs):
        return None

    monkeypatch.setattr(llm_adapter, "_get_client", lambda: _Client())
    monkeypatch.setattr(llm_adapter, "_write_event", _noop)
    monkeypatch.setattr(llm_adapter, "_emit_event", _noop)
    return calls


async def test_the_observer_sends_its_holders_turn_with_every_value(sent) -> None:
    adapter = llm_adapter.MemoryLLMAdapter(ctx=SimpleNamespace(), conversation_id="c")
    variables = build_observer_variables(
        "Date: Oct 5, 2026\n* 🟡 (10:00) Clinic is in Tustin",
        _messages(),
        timezone="America/Los_Angeles",
        current_task="Keep the site's contact details current.",
        previous_response_hint="Confirm the new phone number.",
        instruction="Record addresses verbatim.",
    )
    await run_observer(ModelConfig(mandate_key=MEMORY_OBSERVER_MANDATE), variables, adapter)
    user = sent[0][-1]
    assert "existing_observations=<Date: Oct 5, 2026\n* 🟡 (10:00) Clinic is in Tustin>" in user
    assert "current_task=<Keep the site's contact details current.>" in user
    assert "pending_response_hint=<Confirm the new phone number.>" in user
    assert "new_messages=<Oct 6 2026:\nUser (2:30 PM): Our clinic moved to Irvine" in user
    assert "Assistant (2:30 PM): Updated 14 pages to 4 Park Plaza, Irvine.>" in user
    assert "memory_instructions=<Record addresses verbatim.>" in user
    assert "## Existing Observations" not in user and "## New Messages" not in user


async def test_an_absent_value_leaves_the_holders_default(sent) -> None:
    adapter = llm_adapter.MemoryLLMAdapter(ctx=SimpleNamespace(), conversation_id="c")
    await run_observer(
        ModelConfig(mandate_key=MEMORY_OBSERVER_MANDATE), build_observer_variables(None, _messages()), adapter
    )
    user = sent[0][-1]
    assert "existing_observations=<->" in user and "current_task=<->" in user
    assert "memory_instructions=<->" in user


async def test_the_reflector_sends_the_observations_by_name(sent) -> None:
    adapter = llm_adapter.MemoryLLMAdapter(ctx=SimpleNamespace(), conversation_id="c")
    await run_reflector(
        ModelConfig(mandate_key=MEMORY_REFLECTOR_MANDATE),
        observations="Date: Oct 6, 2026\n* 🔴 (21:30) Clinic moved to Irvine",
        current_task="Keep the site's contact details current.",
        target_threshold=10_000,
        count_tokens_fn=len,
        llm_call_fn=adapter,
        instruction="Keep every street address.",
        max_compression_levels=0,
    )
    user = sent[0][-1]
    assert "observations=<Date: Oct 6, 2026\n* 🔴 (21:30) Clinic moved to Irvine>" in user
    assert "current_task=<Keep the site's contact details current.>" in user
    assert "memory_instructions=<Keep every street address.>" in user
    # Level 0: every level's guidance is sent empty.
    assert "compression_guidance_level_2=<>" in user
    assert "## Observations to Compress" not in user



def test_no_composed_material_block_is_offered() -> None:
    """The 2026-10-07 transition is over: the Holders frame the named values, and
    the old composed ``material`` / ``additional_instructions`` blocks are gone."""
    from matrx_ai.memory.reflector_agent import build_reflector_variables

    observer = build_observer_variables("OBS", [], current_task="TASK", instruction="EXTRA")
    reflector = build_reflector_variables("OBS", current_task="TASK", manual_prompt="EXTRA")
    for offered in (observer, reflector):
        assert "material" not in offered and "additional_instructions" not in offered
        assert not any("## " in str(value) for value in offered.values())
