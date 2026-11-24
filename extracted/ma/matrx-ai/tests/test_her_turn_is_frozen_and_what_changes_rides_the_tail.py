"""Her turn's platform block is frozen for the turn; what changes mid-turn rides AFTER the cache line.

PB-08 k=30 (2026-11-09): every lead conversation filed prompt_cache_prefix_drift because the helper
roster was re-rendered into her turn, behind the cache line, on every tool-loop send (c67b7ef9,
snapshots 8068a980 -> 93ffd79d: "4 in all, 0 running" -> "5 in all, 1 running"). The first fix
(af398c1c65d1, reverted) froze the block only on a turn's first person send and left the model a stale
roster on notice sends, the old lab's identity after a reroute, and no freeze at all on woken or
resumed turns. The rule this guards, on EVERY send kind (tool result, notice, woken, resumed):

- her turn carries the block its turn's FIRST send placed, byte for byte;
- the live roster and a CURRENT copy of every other slot that changed ride the tail, after the
  cache line, labelled as current;
- a new turn freezes its own block (reset at turn start), never an earlier turn's.

Fixture: the two real roster blocks from those snapshots (``fixtures/pb08_c67b7ef9_helper_roster_rounds.json``).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from matrx_ai.config import (
    MessageList,
    TextContent,
    ToolCallContent,
    ToolResultContent,
    UnifiedConfig,
    UnifiedMessage,
    helper_roster,
    message_config,
)
from matrx_ai.config.agent_identity import IDENTITY_SLOT
from matrx_ai.config.message_config import host_authored_user_turn
from matrx_ai.config.send_boundary import keep_turn_context_for_next_turn, order_for_wire
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.testing.profile_factory import make_profile

ROUNDS = json.loads((Path(__file__).parent / "fixtures" / "pb08_c67b7ef9_helper_roster_rounds.json").read_text())
NEW_HELPER = "write-3-000-16bfc0"
TURN_CONTEXT_CURRENT_OPEN = getattr(
    message_config, "TURN_CONTEXT_CURRENT_OPEN", '<turn_context source="platform" as_of="now">'
)


async def _send(config, roster: str, iteration: int):
    async def source(_conversation, _org):
        return roster

    helper_roster.set_helper_roster_source(source)
    try:
        await helper_roster.stage_helper_roster(config, conversation_id="c", organization_id=None)
    finally:
        helper_roster.set_helper_roster_source(None)
    profile = make_profile(model_name="claude-haiku-5-5", wire_format="anthropic_chat")
    prep = order_for_wire(config, profile, iteration=iteration)
    return AnthropicTranslator().build_request(prep.wire_config or config, profile)


def _tool_round(config, n: int) -> None:
    config.messages.append(
        UnifiedMessage(role="assistant", content=[ToolCallContent(id=f"c{n}", name="t", arguments={})])
    )
    config.messages.append(
        UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id=f"c{n}", name="t", content=f"r{n} " * 40)])
    )


def _config(messages, *, page: str | None = "<active_context>PAGE-AT-START</active_context>"):
    config = UnifiedConfig(model="claude-haiku-5-5", messages=MessageList(_messages=messages))
    config.system_instruction = "lead " * 50
    if page:
        config.messages.attach_turn_context(page, slot="context_manifest")
    return config


def _her_turn(body: dict, *, person_words: str) -> str:
    """Everything up to and including her own words: the part behind the cache line."""
    out = []
    for item in body["messages"]:
        out.append(json.dumps(item, sort_keys=True))
        if person_words in json.dumps(item):
            return "".join(out)
    raise AssertionError(f"her words {person_words!r} are not on the wire")


def _tail(body: dict) -> str:
    """The trailing host turn the translator appended after the newest message."""
    last = body["messages"][-1]
    return json.dumps(last) if last.get("role") == "user" else ""


# ── tool-loop sends ────────────────────────────────────────────────────────────────────────────────


async def test_a_tool_loop_never_rewrites_her_turn_and_the_live_roster_rides_the_tail():
    config = _config([UnifiedMessage(role="user", content=[TextContent(text="do it")])])
    await _send(config, ROUNDS["round_2"], 1)
    _tool_round(config, 1)
    second = await _send(config, ROUNDS["round_2"], 2)
    _tool_round(config, 2)
    third = await _send(config, ROUNDS["round_3"], 3)
    assert _her_turn(second, person_words="do it") == _her_turn(third, person_words="do it"), (
        "her turn was re-rendered between rounds (PB-08 c67b7ef9)"
    )
    assert NEW_HELPER in _tail(third), "the live roster did not reach the model after the tool result"


# ── notice sends: ceiling wrap-up, loop guard, answer check, change-claim correction ────────────────


@pytest.mark.parametrize(
    "reason",
    ["iteration_ceiling_wrap_up", "loop_guard_approaching", "answer_check", "change_claim_correction"],
)
async def test_a_notice_send_sees_the_live_roster_and_keeps_her_turn(reason):
    config = _config([UnifiedMessage(role="user", content=[TextContent(text="do it")])])
    first_loop = None
    await _send(config, ROUNDS["round_2"], 1)
    _tool_round(config, 1)
    first_loop = await _send(config, ROUNDS["round_2"], 2)
    config.messages.append(host_authored_user_turn("Write your result now.", reason=reason))
    notice = await _send(config, ROUNDS["round_3"], 3)
    assert NEW_HELPER in _tail(notice), f"{reason}: the notice send carried only the turn-start roster"
    assert _her_turn(first_loop, person_words="do it") == _her_turn(notice, person_words="do it")


# ── woken turns, resumed runs, a first send with no block ─────────────────────────────────────────


async def test_a_woken_turn_freezes_its_own_block_and_sees_the_live_roster():
    config = _config(
        [
            UnifiedMessage(role="user", content=[TextContent(text="start helpers")]),
            UnifiedMessage(role="assistant", content=[TextContent(text="started")]),
            host_authored_user_turn("<helper_report>done</helper_report>", reason="inbox_driver"),
        ]
    )
    await _send(config, ROUNDS["round_2"], 1)
    _tool_round(config, 1)
    second = await _send(config, ROUNDS["round_2"], 2)
    _tool_round(config, 2)
    third = await _send(config, ROUNDS["round_3"], 3)
    assert _her_turn(second, person_words="start helpers") == _her_turn(third, person_words="start helpers")
    assert NEW_HELPER in _tail(third)


async def test_a_resumed_run_freezes_on_its_first_send():
    config = _config([UnifiedMessage(role="user", content=[TextContent(text="do it")])])
    _tool_round(config, 0)  # the run resumes on a tool result: nothing was frozen in this process
    first = await _send(config, ROUNDS["round_2"], 1)
    _tool_round(config, 1)
    second = await _send(config, ROUNDS["round_3"], 2)
    assert _her_turn(first, person_words="do it") == _her_turn(second, person_words="do it")
    assert NEW_HELPER in _tail(second)


async def test_a_turn_whose_first_send_had_no_block_stays_stable():
    config = _config([UnifiedMessage(role="user", content=[TextContent(text="do it")])], page=None)
    await _send(config, "", 1)
    _tool_round(config, 1)
    second = await _send(config, ROUNDS["round_2"], 2)
    _tool_round(config, 2)
    third = await _send(config, ROUNDS["round_3"], 3)
    assert _her_turn(second, person_words="do it") == _her_turn(third, person_words="do it")
    assert NEW_HELPER in _tail(third)


# ── slots that change mid-turn: identity on a reroute, page values ─────────────────────────────────


@pytest.mark.parametrize(
    ("slot", "before", "after"),
    [
        (IDENTITY_SLOT, "You were made by AI Matrx with a model from Anthropic.", "You were made by AI Matrx with a model from OpenAI."),
        ("context_manifest", "<active_context>PAGE-AT-START</active_context>", "<active_context>PAGE-NOW</active_context>"),
    ],
)
async def test_a_slot_changed_mid_turn_rides_the_tail_as_the_current_copy(slot, before, after):
    config = _config([UnifiedMessage(role="user", content=[TextContent(text="do it")])], page=None)
    config.messages.attach_turn_context(before, slot=slot)
    await _send(config, "", 1)
    _tool_round(config, 1)
    unchanged = await _send(config, "", 2)
    assert TURN_CONTEXT_CURRENT_OPEN not in json.dumps(unchanged), "an unchanged slot was restated"
    config.messages.attach_turn_context(after, slot=slot)  # a reroute restages the identity
    _tool_round(config, 2)
    changed = await _send(config, "", 3)
    tail = _tail(changed)
    assert after in tail and json.dumps(TURN_CONTEXT_CURRENT_OPEN)[1:-1] in tail, f"{slot}: current copy missing"
    assert _her_turn(unchanged, person_words="do it") == _her_turn(changed, person_words="do it")
    # The same holds on a notice send.
    config.messages.append(host_authored_user_turn("Write your result now.", reason="iteration_ceiling_wrap_up"))
    assert after in _tail(await _send(config, "", 4))


# ── turn boundaries ───────────────────────────────────────────────────────────────────────────────


async def test_a_previous_turns_freeze_is_never_replayed(monkeypatch):
    import matrx_ai.orchestrator.executor as executor_mod

    config = _config([UnifiedMessage(role="user", content=[TextContent(text="turn one")])])
    await _send(config, ROUNDS["round_2"], 1)
    _tool_round(config, 1)
    assert config.messages.placed_turn_context()
    # The turn ends without its finalize (a crash): the next turn starts through the executor.

    class _Ctx:
        conversation_id = "c"
        user_id = "u"
        parent_conversation_id = None
        request_id = "r"
        store = False

    seen = {}

    async def fake_inner(*, initial_request, **_kw):
        seen["freeze"] = initial_request.config.messages.placed_turn_context()
        return "done"

    class _Request:
        metadata = None

    request = _Request()
    request.config = config
    monkeypatch.setattr(executor_mod, "get_app_context", lambda: _Ctx())
    monkeypatch.setattr(executor_mod, "_execute_until_complete_inner", fake_inner)
    monkeypatch.setattr(executor_mod, "_reply_contract_for_run", lambda *_a, **_k: None)
    assert await executor_mod.execute_until_complete(initial_request=request, client=object()) == "done"
    assert seen["freeze"] is None, "a new turn started with the previous turn's frozen block"


async def test_the_ledger_rebuild_between_rounds_keeps_the_freeze():
    from types import SimpleNamespace

    from matrx_ai.orchestrator.requests import AIMatrixRequest

    config = _config([UnifiedMessage(role="user", content=[TextContent(text="do it")])])
    await _send(config, ROUNDS["round_2"], 1)
    request = AIMatrixRequest(conversation_id="c", config=config)
    response = SimpleNamespace(
        messages=[UnifiedMessage(role="assistant", content=[ToolCallContent(id="c1", name="t", arguments={})])]
    )
    rebuilt = AIMatrixRequest.add_response(
        request, response, tool_results=[ToolResultContent(tool_use_id="c1", name="t", content="r")]
    )
    assert rebuilt.config.messages.placed_turn_context() == config.messages.placed_turn_context()


async def test_the_turn_keeps_what_its_sends_placed_not_a_re_render():
    config = _config([UnifiedMessage(role="user", content=[TextContent(text="do it")])])
    await _send(config, ROUNDS["round_2"], 1)
    _tool_round(config, 1)
    await _send(config, ROUNDS["round_3"], 2)
    kept = keep_turn_context_for_next_turn(config)
    assert kept is not None
    from matrx_ai.config.typed_text_last import STORED_TURN_CONTEXT_KEY

    stored = kept[1].metadata[STORED_TURN_CONTEXT_KEY]
    assert "0 running" in stored and NEW_HELPER not in stored


# ── review of 1804266da0b9 ──────────────────────────────────────────────────────────────────────────


def _builders():
    from matrx_ai.providers.generic_openai.translator import GenericOpenAITranslator
    from matrx_ai.providers.google.translator import GoogleTranslator
    from matrx_ai.providers.openai.translator import OpenAITranslator

    return {
        "anthropic": ("claude-haiku-5-5", "anthropic_chat", lambda c, p: AnthropicTranslator().build_request(c, p)),
        "openai_responses": ("gpt-5", "openai_responses", lambda c, p: OpenAITranslator().to_openai(c, p)),
        "generic_chat": ("kimi-k2", "generic_openai_chat", lambda c, p: GenericOpenAITranslator().to_generic_openai(c, p)),
        "google": ("gemini-3-pro", "google_chat", lambda c, p: GoogleTranslator().to_google(c, p)),
    }


def _dump(body) -> str:
    if hasattr(body, "model_dump"):
        body = body.model_dump()
    return json.dumps(body, default=lambda o: getattr(o, "__dict__", str(o)))


async def _send_on(config, provider: str, roster: str, *, identity: str | None = None, strict: bool = False) -> str:
    model, wire_format, build = _builders()[provider]

    async def source(_conversation, _org):
        return roster

    helper_roster.set_helper_roster_source(source)
    try:
        await helper_roster.stage_helper_roster(config, conversation_id="c", organization_id=None)
    finally:
        helper_roster.set_helper_roster_source(None)
    if identity is not None:
        config.messages.attach_turn_context(identity, slot=IDENTITY_SLOT)
    capabilities = None
    if strict:
        capabilities = {
            "input": ["text"], "output": ["text"],
            "features": ["function_calling", "strict_role_alternation"], "interaction": "turn",
        }
    profile = make_profile(model_name=model, wire_format=wire_format, capabilities=capabilities)
    config.model = model
    prep = order_for_wire(config, profile, iteration=1)
    return _dump(build(prep.wire_config or config, profile))


@pytest.mark.parametrize("provider", ["anthropic", "openai_responses", "generic_chat", "google"])
async def test_a_rerouted_retry_of_her_first_send_names_the_new_lab(provider):
    """An overload reroute retries the same messages: nothing was cached, so the block re-renders."""
    config = _config([UnifiedMessage(role="user", content=[TextContent(text="do it")])])
    await _send_on(config, provider, ROUNDS["round_2"], identity="IDENT-LAB-A")
    retried = await _send_on(config, provider, ROUNDS["round_2"], identity="IDENT-LAB-B")
    assert retried.count("IDENT-LAB-B") == 1 and "IDENT-LAB-A" not in retried, provider


async def test_a_woken_turn_keeps_her_previous_turn_exactly_as_it_was_cached():
    config = _config([UnifiedMessage(role="user", content=[TextContent(text="start helpers")])])
    await _send(config, ROUNDS["round_2"], 1)
    _tool_round(config, 1)
    last_of_turn = await _send(config, ROUNDS["round_2"], 2)
    assert keep_turn_context_for_next_turn(config) is not None
    config.messages.clear_turn_context()
    config.messages.attach_turn_context("<active_context>PAGE-AT-START</active_context>", slot="context_manifest")
    config.messages.append(UnifiedMessage(role="assistant", content=[TextContent(text="started")]))
    config.messages.append(host_authored_user_turn("<helper_report>done</helper_report>", reason="inbox_driver"))
    config.messages.forget_turn_freeze()
    woken = await _send(config, ROUNDS["round_3"], 1)
    assert _her_turn(last_of_turn, person_words="start helpers") == _her_turn(woken, person_words="start helpers"), (
        "the woken turn rewrote her previous turn behind the cache line"
    )
    assert NEW_HELPER in _tail(woken), "the woken turn's live roster is missing"
    # The woken turn's later sends keep the same bytes too.
    _tool_round(config, 2)
    later = await _send(config, ROUNDS["round_3"], 2)
    assert _her_turn(woken, person_words="start helpers") == _her_turn(later, person_words="start helpers")


async def test_a_resumed_run_places_the_block_its_turn_already_cached():
    config = _config([UnifiedMessage(role="user", content=[TextContent(text="do it")])])
    await _send(config, ROUNDS["round_2"], 1)
    _tool_round(config, 1)
    before = await _send(config, ROUNDS["round_2"], 2)
    assert keep_turn_context_for_next_turn(config) is not None
    # A new process resumes the run: a fresh ledger with the stored metadata, nothing frozen.
    resumed = _config(list(config.messages))
    _tool_round(resumed, 2)
    after = await _send(resumed, ROUNDS["round_3"], 3)
    assert _her_turn(before, person_words="do it") == _her_turn(after, person_words="do it")
    assert NEW_HELPER in _tail(after)


async def test_an_unchanged_roster_is_sent_once_on_a_woken_turns_first_send():
    config = _config(
        [
            UnifiedMessage(role="user", content=[TextContent(text="start helpers")]),
            UnifiedMessage(role="assistant", content=[TextContent(text="started")]),
            host_authored_user_turn("<helper_report>done</helper_report>", reason="inbox_driver"),
        ]
    )
    body = json.dumps(await _send(config, ROUNDS["round_2"], 1))
    assert body.count("brainstorm-15-startup-647b5b") == 1, "the roster rode twice"


async def test_a_strict_alternation_notice_send_carries_the_roster_once():
    config = _config([UnifiedMessage(role="user", content=[TextContent(text="do it")])])
    await _send_on(config, "generic_chat", ROUNDS["round_2"], strict=True)
    _tool_round(config, 1)
    config.messages.append(host_authored_user_turn("Write your result now.", reason="iteration_ceiling_wrap_up"))
    body = await _send_on(config, "generic_chat", ROUNDS["round_3"], strict=True)
    assert body.count(NEW_HELPER) == 1, "the roster rode twice on a strict-alternation notice send"
