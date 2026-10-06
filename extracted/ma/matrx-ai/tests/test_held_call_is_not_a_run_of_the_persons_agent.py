"""A held code call (the conversation labeler, a cleaner) runs INSIDE a person's
agent request but is not a run of that agent.

It inherited the request's ``agent_id`` / ``agent_version_id`` /
``initial_variables``, so the labeler's side conversation was stamped with the
person's agent and variables and surfaced in the agent builder's "Recent runs"
as a test case whose input was the labeler prompt (2026-10-05). And when the
person typed nothing, no ``__agent_user_input__`` was recorded, so readers fell
back to the first stored message — the rendered template — as "what was typed".
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock

import pytest
from matrx_connect.context.app_context import (
    AppContext,
    clear_app_context,
    set_app_context,
    try_get_app_context,
)

import matrx_ai.mandates as mandates
import matrx_ai.orchestrator.executor as executor
from matrx_ai.agents.variable_kinds import typed_user_text
from matrx_ai.mandates import HeldCall


def _held() -> HeldCall:
    async def complete(result, variables, spilled):  # noqa: ANN001
        return None

    return HeldCall(
        mandate_key="conversation.label.agent_run",
        model="claude-sonnet-5",
        system="s",
        temperature=None,
        max_output_tokens=None,
        turns=[],
        config=None,
        metadata={},
        complete=complete,
    )


def test_held_call_drops_the_persons_agent_and_variables(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: list[AppContext | None] = []

    async def fake_execute(*_args, **_kwargs):  # noqa: ANN002, ANN003
        seen.append(try_get_app_context())
        raise RuntimeError("stop after capturing the context")

    monkeypatch.setattr(executor, "execute_ai_request", fake_execute)
    monkeypatch.setattr(mandates, "held_request_config", lambda *a, **k: None)

    parent = AppContext(
        emitter=AsyncMock(),
        user_id="e4687a9c-acf7-469f-aa12-860eb4d948d0",
        request_id="req-1",
        agent_id="994566d5-33b6-45ab-8556-2abe28ad4038",
        agent_version_id="596fc5be-4aff-4e66-a279-d497dc2fea86",
        initial_variables={"brand_context": "Viva España", "__agent_user_input__": ""},
        initial_overrides={"temperature": 0.2},
    )
    token = set_app_context(parent)
    try:
        with pytest.raises(RuntimeError):
            asyncio.run(mandates.run_held_call(_held()))
    finally:
        clear_app_context(token)

    child = seen[0]
    assert child is not None
    assert child.agent_id is None
    assert child.agent_version_id is None
    assert child.initial_variables == {}
    assert child.initial_overrides == {}
    assert child.system_run is True


def test_typed_user_text_is_always_a_string() -> None:
    assert typed_user_text(None) == ""
    assert typed_user_text("") == ""
    assert typed_user_text("make it punchy") == "make it punchy"
    assert (
        typed_user_text(
            [
                {"type": "text", "text": "first"},
                {"type": "media", "kind": "image", "url": "https://x/y.png"},
                {"type": "text", "text": "second"},
            ]
        )
        == "first\nsecond"
    )
    assert typed_user_text([{"type": "media", "kind": "image"}]) == ""
