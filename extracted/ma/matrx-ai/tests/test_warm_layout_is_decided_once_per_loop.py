"""Always-warm is decided ONCE per provider loop (providers/prompt_warm.profile_for).

Live 2026-11-18 (three loops, ``prompt_cache_prefix_drift: system changed``): a server copy was still
loading an enrolled agent's prompt, so round 1 went out unwarmed (one system block, 5m mark); the load
finished before round 2, which went out in the warm layout (shared block + rest, 1h marks). The system
channel changed shape mid-loop, so round 2 read 0 and re-wrote the whole 37k-42k-token prefix at the
1h price. The first round's answer is now pinned on the loop's ExecutionState.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.config import UnifiedConfig
from matrx_ai.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_ai.orchestrator.execution_state import (
    ExecutionState,
    _execution_state,
    set_execution_state,
)
from matrx_ai.providers import prompt_warm
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.providers.cache_guard import compare_wire_prefix, wire_prefix
from matrx_ai.providers.unified_client import _build_provider_wire_config
from matrx_ai.testing.profile_factory import make_profile

AGENT = "0c0ffee0-1111-4222-8333-444455556666"
AUTHORED = "You are the front line. " + "Answer plainly and check your facts. " * 40
SYSTEM = AUTHORED + "\n\n<!--matrx:current_date-->Current date: 2026-11-18"
LOADED = prompt_warm.WarmProfile(shared_text=AUTHORED.rstrip(), prompt_chars=len(AUTHORED))
PENDING = prompt_warm.WarmProfile(shared_text="", prompt_chars=0, pending_reason="still loading")


class _LoadsAfterFirstSend:
    """The host reader as it behaves on a fresh server copy: pending until the background load lands."""

    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, agent_id: str) -> prompt_warm.WarmProfile | None:
        self.calls += 1
        return PENDING if self.calls == 1 else LOADED


@pytest.fixture(autouse=True)
def _no_leaked_loop_state():
    """Every test here starts OUTSIDE any loop. Another test in the full run may leave an
    ExecutionState in this context (set without a reset), and a leaked one would pin this file's
    pending/loaded answers across tests; the pre-test value is restored after."""
    token = _execution_state.set(None)
    yield
    _execution_state.reset(token)


@pytest.fixture(autouse=True)
def _ctx():
    token = set_app_context(AppContext(emitter=None, user_id="u1", agent_id=AGENT, conversation_id="c1"))
    yield
    clear_app_context(token)
    prompt_warm.configure_prompt_warm(None, None)
    prompt_warm.take_layout()


def _round(history: list[dict[str, Any]]) -> dict[str, Any]:
    config = UnifiedConfig.from_dict(
        {"model": "claude-opus-5-5", "system_instruction": SYSTEM, "messages": history}
    )
    profile = make_profile(model_name="claude-opus-5-5", wire_format="anthropic_chat")
    return AnthropicTranslator().to_anthropic(_build_provider_wire_config(config, profile), profile)


def _two_rounds() -> tuple[dict[str, Any], dict[str, Any]]:
    first = [{"role": "user", "content": [{"type": "text", "text": "What changed today?"}]}]
    second = first + [
        {"role": "assistant", "content": [{"type": "text", "text": "Let me look."}]},
        {"role": "user", "content": [{"type": "text", "text": "Go on."}]},
    ]
    return _round(first), _round(second)


def test_a_profile_that_loads_mid_loop_does_not_relayout_the_system_channel() -> None:
    prompt_warm.configure_prompt_warm(_LoadsAfterFirstSend(), None)
    token = set_execution_state(ExecutionState())
    try:
        one, two = _two_rounds()
    finally:
        _execution_state.reset(token)
    assert one["system"] == two["system"], "the system channel changed shape between rounds of one loop"
    drift = compare_wire_prefix(wire_prefix(one), wire_prefix(two))
    assert drift.stable, f"cache guard reads a mid-loop prefix change: {drift.changed}"


def test_the_next_loop_takes_the_loaded_profile() -> None:
    reader = _LoadsAfterFirstSend()
    prompt_warm.configure_prompt_warm(reader, None)
    first_loop = set_execution_state(ExecutionState())
    try:
        assert prompt_warm.profile_for(AGENT) is PENDING
        assert prompt_warm.profile_for(AGENT) is PENDING
    finally:
        _execution_state.reset(first_loop)
    next_loop = set_execution_state(ExecutionState())
    try:
        assert prompt_warm.profile_for(AGENT) is LOADED
    finally:
        _execution_state.reset(next_loop)
    assert reader.calls == 2, "the reader is asked once per loop, not once per round"


def test_outside_a_loop_each_send_decides_for_itself() -> None:
    prompt_warm.configure_prompt_warm(_LoadsAfterFirstSend(), None)
    assert prompt_warm.profile_for(AGENT) is PENDING
    assert prompt_warm.profile_for(AGENT) is LOADED
