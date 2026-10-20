"""FORCING GUARD — a mandate-held thread sends the same system text every turn.

The law (Arman, 2026-10-16): "NOTHING, other than the removal of LARGE tool
outputs should ever modify text behind the cache line." "The org data in the
system prompt cannot ever flip mid conversation." Variables in the system prompt
are fine as long as they never change mid-conversation.

THE DEFECT. A Personal Staff / Chief of Staff thread is mandate-held: every turn
re-resolves the LIVE Holder (``agents/live_structure.py``) — right for the belt
and a rebound mandate — and so re-rendered its SYSTEM TEXT every turn, with the
per-turn framing values (``local_datetime``, ``channel``) filled in and the org
catalog rebuilt. The row is never frozen, so neither cache-guard layer looked.
Live: thread 3af9e95c sent a 144,074-byte system block with a different sha256
on every turn of 2026-10-03.

THE FIX. The held text is rendered once and frozen on the row
(``live_structure.HELD_PROMPT_KEY``) with two fingerprints — the Holder itself
and the org catalog. The send boundary sends the frozen text while both match;
a change to either is a deliberate, LOUD cache break. The current framing values
ride the turn context, after the cache line. The cross-turn cache guard covers
settled held rows.

Every test here failed on origin/main (no held prompt existed) and passes after.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.agents import live_structure
from matrx_ai.agents.resolver import ConversationResolver
from matrx_ai.config import UnifiedConfig, send_boundary
from matrx_ai.db.persistence import structural_conversation_update
from matrx_ai.instructions.core import SystemInstruction

CONVERSATION_ID = "3af9e95c-699d-5e78-a506-736e4768273e"
PERSON = "87a6e699-3622-4869-8843-d0867456c0dd"
ORGANIZATION = "0907939e-2b75-43e8-bfee-da758e5ea75b"
HOLDER = "4383174d-aae9-4bb8-a2ea-0498f3cc47a3"
TEMPLATE = (
    "ROLE AND POSTURE\nYou are this person's Chief of Staff. " * 30
    + "\nIt is {{local_datetime}} for them, on {{channel}}."
)
CATALOG = '<org_catalog condensed="true">Acme, Beta</org_catalog>'
BELT = ["staff_roster", "send_text", "ask_person"]


class _Holder:
    """The real Agent's contract the resolver relies on: values passed to
    ``from_agent`` are filled, and the fill keeps the authored template."""

    def __init__(self, template: str) -> None:
        self.config = UnifiedConfig(
            model="claude-sonnet-5",
            system_instruction=SystemInstruction(base_instruction=template, include_date=False),
            tools=list(BELT),
            messages=[],
        )
        self._values: dict[str, Any] = {}

    def set_variables(self, **values: Any) -> _Holder:
        self._values.update(values)
        return self

    async def run_first_turn_pass(self) -> _Holder:
        # Like UnifiedConfig.replace_variables: the authored template is kept.
        si = self.config.system_instruction
        if getattr(si, "_authored_template", None) is None:
            si._authored_template = si.base_instruction
        text = si._authored_template
        for name in ("local_datetime", "channel"):
            text = text.replace("{{" + name + "}}", str(self._values.get(name, "")))
        si.base_instruction = text
        return self


@pytest.fixture
def held_thread(monkeypatch: pytest.MonkeyPatch):
    live_structure.register_live_holder_resolver(None)  # type: ignore[arg-type]
    world: dict[str, Any] = {
        "template": TEMPLATE,
        "row": SimpleNamespace(
            id=CONVERSATION_ID,
            config={
                "model": "claude-sonnet-5",
                live_structure.LIVE_STRUCTURE_KEY: True,
                live_structure.RESPONDER_MANDATE_KEY: "personal_staff.front_line",
            },
            # A held row's column is last week's Holder — never the authority.
            system_instruction="the instructions a previous Holder left behind",
            initial_agent_id=HOLDER,
            initial_agent_version_id=None,
            created_by=PERSON,
            organization_id=ORGANIZATION,
        ),
    }

    async def load_by_id(_id: str):
        return world["row"]

    monkeypatch.setattr(
        "matrx_ai.db.cxm",
        SimpleNamespace(conversation=SimpleNamespace(load_by_id=load_by_id)),
        raising=False,
    )
    monkeypatch.setattr("matrx_ai.client_host.get_conversation_store", lambda: None, raising=False)

    async def _load_persisted_messages(_conversation_id: str) -> list:
        from matrx_ai.config import TextContent, UnifiedMessage

        return [UnifiedMessage(role="user", content=[TextContent(text="what is on today?")])]

    async def _load_unified_config(_conversation_id: str) -> UnifiedConfig:
        return UnifiedConfig(
            model="claude-sonnet-5",
            system_instruction=world["row"].system_instruction,
            messages=[],
        )

    monkeypatch.setattr("matrx_ai.agents.resolver._load_unified_config", _load_unified_config)

    async def _load_sticky_toolset(_conversation_id: str):
        return [], {}

    monkeypatch.setattr("matrx_ai.agents.resolver._load_persisted_messages", _load_persisted_messages)
    monkeypatch.setattr("matrx_ai.agents.resolver._load_sticky_toolset", _load_sticky_toolset)

    async def _finish(config, **_kwargs):
        return config

    monkeypatch.setattr(ConversationResolver, "_finish", staticmethod(_finish))

    async def from_agent(agent_id: str, is_version: bool = False, variables=None):
        # Like the real Agent.from_agent: values passed here are filled at once.
        # (A fingerprint of the FILLED text would change every turn — the
        # identity test below catches that.)
        holder = _Holder(world["template"])
        if variables:
            holder.set_variables(**variables)
            await holder.run_first_turn_pass()
        return holder

    monkeypatch.setattr("matrx_ai.agents.definition.Agent.from_agent", staticmethod(from_agent))
    monkeypatch.setattr("matrx_ai.agents.cache.AgentCache.get", staticmethod(lambda _c: None))

    breaks: list[dict[str, Any]] = []
    monkeypatch.setattr(
        "matrx_ai.providers.cache_guard.deliberate_cache_break",
        lambda **kw: breaks.append(kw),
        raising=False,
    )
    world["breaks"] = breaks
    yield world
    live_structure.register_live_holder_resolver(None)  # type: ignore[arg-type]


async def _run_turn(world: dict[str, Any], *, clock: str, catalog: str = CATALOG) -> UnifiedConfig:
    """One held turn: resolve, host injects the catalog, first send, end-of-turn write."""
    config = await ConversationResolver.from_conversation_id(
        CONVERSATION_ID,
        responder_variables={"local_datetime": clock, "channel": "sms"},
    )
    # The host's context assembly injects the org catalog AFTER the resolver.
    config.system_instruction.inject_context_block(catalog)
    # The first send's boundary step (absent on origin/main: there the text
    # simply went out as rendered, which is the defect the identity test shows).
    settle = getattr(send_boundary, "_settle_held_prompt", None)
    if settle is not None:
        settle(config, conversation_id=CONVERSATION_ID)
    row = world["row"]
    update = structural_conversation_update(
        assembled_config=config.to_storage_dict()["config"],
        existing_config=row.config,
        existing_system_instruction=row.system_instruction,
        incoming_system_instruction=config.resolved_system_instruction,
        request_already_frozen=False,
        turn_mandate_key=config.responder_mandate_key,
    )
    row.config = update.config
    return config


@pytest.mark.asyncio
async def test_two_turns_send_byte_identical_held_system_text(held_thread) -> None:
    one = await _run_turn(held_thread, clock="Friday 9:00 PM")
    two = await _run_turn(held_thread, clock="Friday 9:07 PM")
    assert one.resolved_system_instruction == two.resolved_system_instruction, (
        "the held system text changed between turns — the clock re-rendered "
        "into the cached prefix"
    )
    assert CATALOG in (two.resolved_system_instruction or "")
    assert "9:07" not in (two.resolved_system_instruction or "")
    assert held_thread["breaks"] == []


@pytest.mark.asyncio
async def test_the_current_framing_values_ride_the_turn_context(held_thread) -> None:
    await _run_turn(held_thread, clock="Friday 9:00 PM")
    two = await _run_turn(held_thread, clock="Friday 9:07 PM")
    turn_context = two.messages.render_turn_context() or ""
    assert "local_datetime: Friday 9:07 PM" in turn_context
    assert "<turn_values>" in turn_context


@pytest.mark.asyncio
async def test_a_changed_holder_rerenders_once_and_says_so(held_thread) -> None:
    await _run_turn(held_thread, clock="9:00")
    held_thread["template"] = TEMPLATE + "\nNEW RULE: always confirm before sending."
    two = await _run_turn(held_thread, clock="9:05")
    assert "NEW RULE" in (two.resolved_system_instruction or "")
    assert len(held_thread["breaks"]) == 1
    assert "Holder" in held_thread["breaks"][0]["reason"]
    three = await _run_turn(held_thread, clock="9:10")
    assert three.resolved_system_instruction == two.resolved_system_instruction
    assert len(held_thread["breaks"]) == 1


@pytest.mark.asyncio
async def test_a_changed_org_catalog_rerenders_and_says_so(held_thread) -> None:
    await _run_turn(held_thread, clock="9:00")
    new_catalog = '<org_catalog condensed="true">Acme, Beta, Gamma</org_catalog>'
    two = await _run_turn(held_thread, clock="9:05", catalog=new_catalog)
    assert new_catalog in (two.resolved_system_instruction or "")
    assert len(held_thread["breaks"]) == 1
    assert "catalog" in held_thread["breaks"][0]["reason"]


@pytest.mark.asyncio
async def test_the_send_boundary_settles_the_held_text_on_the_loop_stage(held_thread) -> None:
    """Wired into prepare_for_send, not only callable."""
    await _run_turn(held_thread, clock="9:00")
    config = await ConversationResolver.from_conversation_id(
        CONVERSATION_ID, responder_variables={"local_datetime": "9:30", "channel": "sms"}
    )
    config.system_instruction.inject_context_block(CATALOG)
    prep = await send_boundary.prepare_for_send(
        config,
        stage=send_boundary.STAGE_LOOP,
        conversation_id=CONVERSATION_ID,
        request_id="req-held",
        iteration=1,
        policy=send_boundary.TrimPolicy(),
    )
    assert "settle_held_prompt" in prep.steps
    assert config.held_prompt["settled"] is True
    assert "9:30" not in (config.resolved_system_instruction or "")


def test_the_cross_turn_cache_guard_covers_a_settled_held_row(monkeypatch) -> None:
    from matrx_ai.orchestrator.executor import _cache_prefix_is_frozen
    from matrx_ai.providers import cache_guard

    config = UnifiedConfig(model="claude-sonnet-5", messages=[])
    assert _cache_prefix_is_frozen(config) is False
    config.held_prompt = {"holder": "h", "stored": None, "settled": True}
    assert _cache_prefix_is_frozen(config) is True

    screams: list[dict[str, Any]] = []
    monkeypatch.setattr(cache_guard, "scream_cache_line_violation", lambda **kw: screams.append(kw))
    usage = {"input_tokens": 4, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 9000}
    common = dict(
        provider="anthropic",
        model="claude-sonnet-5",
        conversation_id="conv-held-guard",
        tool_names=(),
        raw_usage=usage,
        prefix_frozen=_cache_prefix_is_frozen(config),
    )
    cache_guard.observe_cache_usage(request_id="t1", system_text="A" * 5000, **common)
    cache_guard.observe_cache_usage(request_id="t2", system_text="B" * 5000, **common)
    assert [s["kind"] for s in screams] == ["system_prompt_changed_between_turns"]

    # A deliberate break resets the memory: reported once, as deliberate.
    cache_guard.forget_conversation_prefix("conv-held-guard")
    cache_guard.observe_cache_usage(request_id="t3", system_text="C" * 5000, **common)
    assert len(screams) == 1
