"""Forcing function: a NamedAgent call can CONTINUE an existing conversation.

``NamedAgent.run`` (the class every mandated typed call, and the mandate runner's
``Offer.from_inputs`` lane, ends in) used to have no ``conversation_id``: a follow-up
turn on a thread a prior run opened (Hindsight's discuss turn) could not go through
the runner and ran ``run_agent`` directly. Gut check: remove the pass-through in
``NamedAgent.run`` and the first test fails.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from pydantic import BaseModel

from matrx_ai.agents import named as named_mod


class _In(BaseModel):
    topic: str = ""


class _Out(BaseModel):
    answer: str = ""


class _FakeAgent:
    variable_defaults: dict = {}
    request_metadata: dict = {}
    auto_tools_disabled = None
    config = SimpleNamespace(metadata={}, custom_tools=[])

    def set_variables(self, **_: object) -> None:
        return None


class _Source:
    async def load(self) -> _FakeAgent:
        return _FakeAgent()


class _Continuing(named_mod.NamedAgent):
    name = "continuing_probe"
    Inputs = _In
    Output = _Out
    source = _Source()
    child_source_app = "test"
    child_source_feature = "test"


async def _run(monkeypatch, **kw) -> dict:
    seen: dict = {}

    async def fake_run_agent(agent, **kwargs):
        seen.update(kwargs)
        return SimpleNamespace(parsed=None, success=True)

    monkeypatch.setattr(named_mod, "run_agent", fake_run_agent)
    await _Continuing.run(inputs=_In(), **kw)
    return seen


@pytest.mark.asyncio
async def test_conversation_id_reaches_the_executor(monkeypatch) -> None:
    seen = await _run(monkeypatch, conversation_id="conv-123", allow_client_delegation=False)
    assert seen["conversation_id"] == "conv-123"
    assert seen["allow_client_delegation"] is False


@pytest.mark.asyncio
async def test_default_is_a_new_conversation(monkeypatch) -> None:
    seen = await _run(monkeypatch)
    assert seen["conversation_id"] is None
    assert seen["allow_client_delegation"] is True
