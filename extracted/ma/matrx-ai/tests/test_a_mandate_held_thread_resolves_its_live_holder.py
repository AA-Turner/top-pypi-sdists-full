"""Every continuation of a mandate-held conversation gets the LIVE Holder.

THE DEFECT. A person's Personal Staff thread is answered by whoever holds
`personal_staff.front_line` right now. Five continuation surfaces run turns on
that one thread — the agent route (which the in-app `/staff` door and the SMS
worker both use), `POST /conversations/{id}`, crash recovery, the voice runtime,
and the deferred-result inbox driver — and only the first opened the door that
repaired the row. So when `ask_person` joined the Chief of Staff's belt, the
door's next turn saw nineteen tools and every other surface saw the frozen
eighteen.

WHY THE FIX IS HERE AND NOT IN FIVE PLACES. All five reach
``ConversationResolver.from_conversation_id``. A repair in the SMS worker leaves
a person's staff amnesiac on a phone call; a repair in each of the five is four
chances to drift. The rule lives at the one seam:
``matrx_ai/agents/live_structure.py``.

WHAT THESE WOULD CATCH. Delete the mandate-held branch in the resolver and the
first two go red — the resolver hands back the row's frozen belt. Drop the
mandate key and take the row's named agent instead, and
``test_rebinding_the_mandate_moves_the_thread_on_the_very_next_turn`` goes red,
which is the difference between "live-ish" and live.
"""

from __future__ import annotations

from copy import deepcopy
from types import SimpleNamespace

import pytest

from matrx_ai.agents import live_structure
from matrx_ai.agents.resolver import ConversationResolver
from matrx_ai.config import UnifiedConfig

CONVERSATION_ID = "3af9e95c-699d-5e78-a506-736e4768273e"
PERSON = "87a6e699-3622-4869-8843-d0867456c0dd"
ORGANIZATION = "0907939e-2b75-43e8-bfee-da758e5ea75b"

YESTERDAYS_HOLDER = "4383174d-aae9-4bb8-a2ea-0498f3cc47a3"
TODAYS_HOLDER = "5c0ffee5-0000-4000-8000-00000000d00d"

#: What the row really carried on 2026-09-21: the old belt plus automatics,
#: frozen, with no `ask_person` in it.
THE_FROZEN_BELT = [
    "staff_roster",
    "staff_escalate",
    "mandate_call",
    "agent_call",
    "send_text",
    "memory",
    "research_web",
    "task",
    "cloud_browser",
    "credential_login",
]

THE_LIVE_BELT = [*THE_FROZEN_BELT, "ask_person"]


class _Row(SimpleNamespace):
    pass


def prompt_of(config) -> str:
    """The instruction text, whichever shape the config carries it in."""
    instruction = config.system_instruction
    return str(getattr(instruction, "base_instruction", instruction) or "")


@pytest.fixture(autouse=True)
def _no_registered_resolver():
    """The seam is process-global; never leak one test's Holder into another."""
    live_structure.register_live_holder_resolver(None)  # type: ignore[arg-type]
    yield
    live_structure.register_live_holder_resolver(None)  # type: ignore[arg-type]


@pytest.fixture
def staff_thread(monkeypatch: pytest.MonkeyPatch):
    """A staff row: mandate-held, and carrying a stale frozen structure."""

    row = _Row(
        id=CONVERSATION_ID,
        config={
            "model": "claude-sonnet-5",
            "tools": list(THE_FROZEN_BELT),
            "system_prompt_frozen": True,
            live_structure.LIVE_STRUCTURE_KEY: True,
            live_structure.RESPONDER_MANDATE_KEY: "personal_staff.front_line",
        },
        initial_agent_id=YESTERDAYS_HOLDER,
        initial_agent_version_id=None,
        created_by=PERSON,
        organization_id=ORGANIZATION,
    )

    async def load_by_id(_id: str):
        return row

    monkeypatch.setattr(
        "matrx_ai.db.cxm",
        SimpleNamespace(conversation=SimpleNamespace(load_by_id=load_by_id)),
        raising=False,
    )
    monkeypatch.setattr(
        "matrx_ai.client_host.get_conversation_store", lambda: None, raising=False
    )

    frozen = UnifiedConfig(
        model="claude-sonnet-5",
        system_instruction="the instructions the Chief had yesterday",
        tools=list(THE_FROZEN_BELT),
        messages=[],
    )

    async def _load_unified_config(_conversation_id: str) -> UnifiedConfig:
        return deepcopy(frozen)

    async def _load_persisted_messages(_conversation_id: str) -> list:
        return []

    monkeypatch.setattr(
        "matrx_ai.agents.resolver._load_unified_config", _load_unified_config
    )
    monkeypatch.setattr(
        "matrx_ai.agents.resolver._load_persisted_messages", _load_persisted_messages
    )

    async def _finish(config, **_kwargs):
        # The send boundary is a different contract with its own guard. What is
        # under test is WHICH structural half reaches it.
        return config

    monkeypatch.setattr(ConversationResolver, "_finish", staticmethod(_finish))

    holders = {
        # The agent the ROW names — which gained a tool and new instructions
        # today, while the row still carries yesterday's copy of both.
        YESTERDAYS_HOLDER: UnifiedConfig(
            model="claude-sonnet-5",
            system_instruction="the instructions the Chief has today",
            tools=list(THE_LIVE_BELT),
            messages=[],
        ),
        TODAYS_HOLDER: UnifiedConfig(
            model="claude-opus-5",
            system_instruction="the instructions the Chief has today",
            tools=list(THE_LIVE_BELT),
            messages=[],
        ),
    }

    async def from_agent(agent_id: str, is_version: bool = False, variables=None):
        return SimpleNamespace(config=deepcopy(holders[str(agent_id)]))

    monkeypatch.setattr(
        "matrx_ai.agents.definition.Agent.from_agent", staticmethod(from_agent)
    )
    monkeypatch.setattr("matrx_ai.agents.cache.AgentCache.get", staticmethod(lambda _c: None))

    return holders


@pytest.mark.asyncio
async def test_a_continuation_with_no_agent_id_gets_the_live_belt(staff_thread) -> None:
    """The shape crash recovery and the inbox driver arrive in: no agent named."""
    config = await ConversationResolver.from_conversation_id(CONVERSATION_ID)
    assert "ask_person" in (config.tools or []), (
        "the resolver handed back the belt frozen on the row. On a phone this "
        "is the Chief refusing to send a login link five minutes after it was "
        "given the tool to send one."
    )


@pytest.mark.asyncio
async def test_the_rows_frozen_prompt_is_not_the_authority(staff_thread) -> None:
    config = await ConversationResolver.from_conversation_id(CONVERSATION_ID)
    assert prompt_of(config) == "the instructions the Chief has today"


@pytest.mark.asyncio
async def test_rebinding_the_mandate_moves_the_thread_on_the_very_next_turn(
    staff_thread,
) -> None:
    """The row still NAMES yesterday's agent. The mandate names today's.

    This is the whole reason the row records a mandate key and not only an
    agent id: rebinding the Holder in the console must not wait for somebody to
    reopen the thread.
    """

    async def holder_for_mandate(mandate_key, user_id, organization_id):
        assert mandate_key == "personal_staff.front_line"
        assert user_id == PERSON
        assert organization_id == ORGANIZATION
        return TODAYS_HOLDER

    live_structure.register_live_holder_resolver(holder_for_mandate)

    config = await ConversationResolver.from_conversation_id(CONVERSATION_ID)
    assert config.model == "claude-opus-5"
    assert prompt_of(config) == "the instructions the Chief has today"


@pytest.mark.asyncio
async def test_an_unresolvable_mandate_falls_back_to_the_named_agent(
    staff_thread,
) -> None:
    """Loud degradation, never a dead turn."""

    async def holder_for_mandate(mandate_key, user_id, organization_id):
        raise RuntimeError("the ladder is down")

    live_structure.register_live_holder_resolver(holder_for_mandate)

    config = await ConversationResolver.from_conversation_id(CONVERSATION_ID)
    # Still the LIVE definition of the agent the row names — never the belt
    # that was frozen onto the row.
    assert "ask_person" in (config.tools or [])


@pytest.mark.asyncio
async def test_an_ordinary_conversation_still_runs_its_own_frozen_structure(
    staff_thread, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The positive control: no marker, no re-resolution."""

    async def load_by_id(_id: str):
        return _Row(
            id=CONVERSATION_ID,
            config={"model": "claude-sonnet-5", "system_prompt_frozen": True},
            initial_agent_id=YESTERDAYS_HOLDER,
            initial_agent_version_id=None,
            created_by=PERSON,
            organization_id=ORGANIZATION,
        )

    monkeypatch.setattr(
        "matrx_ai.db.cxm",
        SimpleNamespace(conversation=SimpleNamespace(load_by_id=load_by_id)),
        raising=False,
    )

    config = await ConversationResolver.from_conversation_id(CONVERSATION_ID)
    assert config.tools == THE_FROZEN_BELT
    assert prompt_of(config) == "the instructions the Chief had yesterday"


@pytest.mark.asyncio
async def test_the_resolved_turn_carries_the_mandate_key_it_was_built_from(
    staff_thread,
) -> None:
    """The second layer is only a layer if somebody fills it.

    Persistence re-reads the conversation row to decide whether to freeze, and
    that read can fail. When it does, the ONLY thing left that knows this turn
    came from a mandate's live Holder is the turn itself — so the resolver
    stamps it here, at the one place that has just established it. Without this
    line `persist_completed_request` falls back to "not mandate-held", freezes
    the belt onto the row, and the next turn reaches the provider with none of
    the Holder's authored tools (measured live 2026-09-21).
    """
    config = await ConversationResolver.from_conversation_id(CONVERSATION_ID)
    assert config.responder_mandate_key == "personal_staff.front_line"


@pytest.mark.asyncio
async def test_an_ordinary_responder_turn_is_not_marked_mandate_held(
    staff_thread, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A mirrored coding session uses the same responder path and is NOT
    mandate-held — it must keep freezing normally."""
    config = await ConversationResolver.from_conversation_id(
        CONVERSATION_ID, responder_agent_id=TODAYS_HOLDER
    )
    assert config.responder_mandate_key is None
