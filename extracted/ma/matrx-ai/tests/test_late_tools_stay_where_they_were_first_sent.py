"""🚨 A WARM SEND ONLY APPENDS — late tool definitions stay on the turn that first sent them, inside the cached prefix.

Live (2026-11-19, the test admin's staff thread 3af9e95c, Anthropic): every ask carried ~31.5k uncached input tokens.
The newest person turn's ``<turn_context>`` block was 86,522 chars and sat after the rolling cache mark; 67,286 of
them were ``late_tools`` — 30 tool definitions, byte-identical on every ask — re-sent at full price because the
block moved to the newest turn on every send and the previous turn kept nothing.

Now a late tool's definition stays on the person turn whose send first placed it (``late_tools_in_cache`` on her
message, or inside her kept whole block) and every later send replays it there, before the rolling mark; the newest
turn carries only the definitions that are new or changed, plus one short slot naming which earlier ones are
available now. The guard runs the REAL pieces end to end: stored rows → real rebuild → real resolver → real loop
stage of ``prepare_for_send`` → the Anthropic translator → the real turn end (``executor._strip_ephemeral_for_storage``
writing her row's metadata) → real ``persistence._refresh_cache_state``. Only the database reads/writes and the
catalog's model profile are in-memory doubles.

(i)   the definitions' bytes lie before the rolling mark on the second send;
(ii)  the model sees the same tools declared available and the same context facts;
(iii) a late tool added between sends is APPENDED in the newest turn; the prefix bytes are held;
(iv)  the history window cutting the carrying turn re-emits its definitions, and the prefix is recorded as moved;
(v)   a tool named available has its full definition on the send, once — under fit pressure too (review of
      c8a79d95939: F1), with carriers only when the send splits late tools (F2), never an availability claim outside
      the newest turn's names slot (F3), canonical digests and no carrier pile-up (F4), carriers stamped only on a
      warm cadence (F6), and the tool-loop, Google and OpenAI wires (F9).
Every case builds from rows rebuilt from storage (the fixture), never hand-built messages.
"""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect.context.app_context import (
    AppContext,
    clear_app_context,
    get_app_context,
    set_app_context,
)

from matrx_ai import _ext
from matrx_ai.db._registry import configure_db

# The rebuild resolves its row models from the registry at import time; it only uses them as type references.
configure_db(models={name: SimpleNamespace for name in ("CxMessage", "CxToolCall", "CxMedia", "Message", "ToolCall", "Media")})

from matrx_ai.agents.cache import AgentCache  # noqa: E402
from matrx_ai.agents.definition import Agent  # noqa: E402
from matrx_ai.agents.resolver import ConversationResolver  # noqa: E402
from matrx_ai.config import (  # noqa: E402
    TextContent,
    UnifiedConfig,
    UnifiedMessage,
    context_trim,
    input_fit,
    send_boundary,
)
from matrx_ai.config.cache_plan import configure_prompt_cache_knobs  # noqa: E402
from matrx_ai.config.context_trim import TrimPolicy  # noqa: E402
from matrx_ai.config.history_budget import HistoryWindowPolicy  # noqa: E402
from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send  # noqa: E402
from matrx_ai.config.typed_text_last import turn_person_index  # noqa: E402
from matrx_ai.db import persistence  # noqa: E402
from matrx_ai.db.conversation_rebuild import rebuild_conversation_messages  # noqa: E402
from matrx_ai.orchestrator import executor  # noqa: E402
from matrx_ai.providers import late_tools  # noqa: E402
from matrx_ai.providers.anthropic.translator import AnthropicTranslator  # noqa: E402
from matrx_ai.testing.profile_factory import make_profile  # noqa: E402
from matrx_ai.tools import declaration_ledger  # noqa: E402
from matrx_ai.tools import registry as registry_module  # noqa: E402
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolResult, ToolType  # noqa: E402
from matrx_ai.tools.registry import ToolRegistry  # noqa: E402

CONVERSATION = "3af9e95c-0000-4000-8000-0000000017e5"
AUTHORED = ["memory", "use_tool"]
LATE = ["late_calendar_probe", "late_notes_probe"]
ADDED = "late_documents_probe"
PROFILE = make_profile(model_name="claude-opus-5-5", wire_format="anthropic_chat")
PROFILES = {
    "anthropic": PROFILE,
    "google": make_profile(model_name="gemini-3.5-flash", wire_format="google_chat"),
    "openai": make_profile(model_name="gpt-5.5", wire_format="openai_chat"),
}


async def _probe(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    return ToolResult(success=True, output={"ok": True}, tool_name=ctx.tool_name, call_id=ctx.call_id)


def _definition(name: str) -> ToolDefinition:
    return ToolDefinition(
        name=name,
        description=f"The {name} tool. " + "It reads and writes the person's records carefully. " * 20,
        parameters={"q": {"type": "string", "description": "A query.", "required": True}},
        tool_type=ToolType.LOCAL,
        function_path=f"{__name__}._probe",
    )


class _Thread:
    """The staff thread as the database holds it: message rows and the conversation row."""

    def __init__(self) -> None:
        self.provider = "anthropic"
        self.messages: list[SimpleNamespace] = []
        self.cache_state: dict[str, Any] = {
            "last_response_at": (datetime.now(UTC) - timedelta(hours=3)).isoformat(),
            "est_cache_ttl_secs": 300,
            "last_provider": "anthropic",
        }

    def row(self, role: str, text: str) -> SimpleNamespace:
        n = len(self.messages)
        row = SimpleNamespace(
            id=f"00000000-0000-4000-8000-{n:012d}", role=role, position=n, content=[{"type": "text", "text": text}],
            created_at=None, status="active", metadata={}, deleted_at=None, is_visible_to_model=True,
        )
        self.messages.append(row)
        return row

    def by_id(self, row_id: str) -> SimpleNamespace:
        return next(r for r in self.messages if r.id == row_id)

    def go_warm(self) -> None:
        """The person's last ask was answered a moment ago: the next ask finds the cache warm (a warm cadence)."""
        self.cache_state["last_response_at"] = datetime.now(UTC).isoformat()

    def go_cold(self) -> None:
        self.cache_state["last_response_at"] = (datetime.now(UTC) - timedelta(hours=3)).isoformat()


@pytest.fixture
def thread(monkeypatch):
    db = _Thread()
    for i in range(3):
        db.row("user", f"What is on my calendar on day {i}?")
        db.row("assistant", f"Day {i} is clear.")

    async def load_conversation_by_id(_cid: str) -> Any:
        return SimpleNamespace(
            id=CONVERSATION, cache_state=dict(db.cache_state), config={}, last_request_status="completed",
            system_prompt_frozen=None, created_at=None,
        )

    async def load_by_id(_cid: str) -> Any:
        return None  # not mandate-held: the process-cache path

    async def rebuilt(_cid: str) -> list[Any]:
        return await rebuild_conversation_messages(list(db.messages), [], [])

    fake = SimpleNamespace(
        conversation=SimpleNamespace(load_conversation_by_id=load_conversation_by_id, load_by_id=load_by_id),
        get_rebuilt_conversation_messages=rebuilt,
    )
    monkeypatch.setattr("matrx_ai.db.cxm", fake, raising=False)
    monkeypatch.setattr("matrx_ai.client_host.get_conversation_store", lambda: None, raising=False)
    monkeypatch.setattr(persistence, "_cxm", lambda: fake)
    monkeypatch.setattr(persistence, "_get_live_coordinator", lambda: object())

    def write_conversation(_cid: str, **fields: Any) -> None:
        db.cache_state = json.loads(json.dumps(fields["cache_state"], default=str))  # a jsonb round trip

    monkeypatch.setattr(persistence, "_queue_conversation_update", write_conversation)

    def write_message(row_id: str, **fields: Any) -> None:
        db.by_id(row_id).metadata = json.loads(json.dumps(fields["metadata"], default=str))

    # The executor's turn end writes her row's metadata through this one queue door.
    monkeypatch.setattr("matrx_ai.persistence.queue_helpers.queue_message_update", write_message)

    async def profile(config: Any, *, conversation_id: str | None, iteration: int | None = None) -> Any:
        return PROFILES[db.provider]  # the catalog read

    monkeypatch.setattr(send_boundary, "_send_profile", profile)

    window_turns = {"turns": 40}

    async def window(*, conversation_id: str, structure_is_live: bool):
        return HistoryWindowPolicy(turns=window_turns["turns"], token_budget=400_000, waits_for_cold_cache=True)

    async def markers(*, conversation_id: str, structure_is_live: bool):
        return True

    monkeypatch.setitem(_ext._registry, "conversation_history_window", window)
    monkeypatch.setitem(_ext._registry, "perishable_state_marker", markers)
    previous_resolver = context_trim.get_trim_policy_resolver()

    async def holding_policy(_organization_id: Any) -> TrimPolicy:
        return TrimPolicy(cache_gate_mode="legacy", cache_gate_min_saved_tokens=10**9)

    context_trim.set_trim_policy_resolver(holding_policy)

    reg = ToolRegistry()
    reg.load_from_definitions([_definition(n) for n in (*AUTHORED, *LATE, ADDED)])
    reg._loaded = True
    monkeypatch.setattr(registry_module.ToolRegistry, "_instance", reg)
    late_tools.reset_for_tests()
    declaration_ledger.reset_for_tests()
    knobs = {"late_tools_enabled": True, "late_tools_scope": "all"}
    configure_prompt_cache_knobs(lambda key: knobs.get(key))

    _forget_this_process()
    AgentCache.set(CONVERSATION, Agent(config=_agent_config(LATE)))
    token = set_app_context(AppContext(emitter=None, user_id="u", organization_id="o", conversation_id=CONVERSATION))
    db.window = window_turns
    yield db
    clear_app_context(token)
    input_fit.set_input_budget_resolver(None)
    context_trim.set_trim_policy_resolver(previous_resolver)
    configure_prompt_cache_knobs(None)
    declaration_ledger.reset_for_tests()
    late_tools.reset_for_tests()
    _forget_this_process()
    AgentCache.clear()


def _agent_config(late: list[str]) -> UnifiedConfig:
    config = UnifiedConfig(model="claude-opus-5-5", system_instruction="You are the person's chief of staff. " * 30, messages=[])
    config.tools = [*AUTHORED, *late]
    config.authored_tools = list(AUTHORED)
    config.dynamic_tools = list(late)
    return config


def _forget_this_process() -> None:
    """The next ask lands on another server task: only the rows (messages, ``cache_state``) carry over."""
    for memo in (
        "_CACHE_STATE_MEMO", "_HISTORY_CUT_MEMO", "_TRIM_REPLAY_MEMO", "_TRIM_REPLAY_DROPPED", "_PREFIX_BYTES_MEMO",
        "_WIRE_TEXT_STUBS", "_WIRE_TEXT_CUTS", "_REPLAYED_CONTEXT_DROPPED", "_LAST_SEND_AT",
    ):
        getattr(send_boundary, memo, {}).clear()


def _texts(message: dict[str, Any]) -> list[str]:
    content = message["content"]
    return [content] if isinstance(content, str) else [b.get("text") or "" for b in content if isinstance(b, dict)]


def _definitions(messages: list[dict[str, Any]]) -> dict[str, str]:
    """Every late tool definition on the wire: wire name → its whole ``<late_tools>`` block."""
    found: dict[str, str] = {}
    for message in messages:
        for text in _texts(message):
            for block in re.findall(r"<late_tools>\n.*?\n</late_tools>", text, flags=re.S):
                name = re.search(r"^### (\S+)$", block, flags=re.M)
                assert name, block
                found.setdefault(name.group(1), block)
    return found


def _definition_counts(messages: list[dict[str, Any]]) -> dict[str, int]:
    """How many times each late tool is DEFINED on the wire (a whole ``<late_tools>`` entry)."""
    counts: dict[str, int] = {}
    for message in messages:
        for text in _texts(message):
            for name, _digest in late_tools.wire_definitions([text]):
                counts[name] = counts.get(name, 0) + 1
    return counts


def _over_budget_by_one(_ctx: Any, _config: Any, prompt_tokens: int) -> tuple[int, int, bool]:
    """A host input budget every call is over (enforced): every fit pass runs, the last-resort stubs included."""
    return max(1, prompt_tokens - 1), prompt_tokens, True


def _rolling_mark(messages: list[dict[str, Any]]) -> int:
    marked = [i for i, m in enumerate(messages) if isinstance(m["content"], list) and any("cache_control" in b for b in m["content"] if isinstance(b, dict))]
    assert marked, "the request carries no rolling cache mark"
    return marked[-1]


def _translate(provider: str, wire: Any) -> Any:
    from matrx_ai.providers.google.translator import GoogleTranslator
    from matrx_ai.providers.openai.translator import OpenAITranslator
    from matrx_ai.providers.unified_client import _build_provider_wire_config

    profile = PROFILES[provider]
    if provider == "anthropic":
        return AnthropicTranslator().build_request(wire, profile)
    translator = GoogleTranslator() if provider == "google" else OpenAITranslator()
    return translator.build_request(_build_provider_wire_config(wire, profile), profile)


def _strings(value: Any) -> list[str]:
    """Every string in a provider request (dicts, lists, SDK models), in order."""
    if isinstance(value, str):
        return [value]
    if hasattr(value, "model_dump"):
        value = value.model_dump(exclude_none=True)
    if isinstance(value, dict):
        return [s for v in value.values() for s in _strings(v)]
    if isinstance(value, (list, tuple)):
        return [s for v in value for s in _strings(v)]
    return []


async def _ask(
    db: _Thread, n: int, question: str, *, late: list[str] = LATE, loop: bool = False
) -> dict[str, Any]:
    """One staff ask: resolve (real resolver), its sends (real loop stage + translator; ``loop``: one tool round
    first), the turn's end (real executor turn end writing her row), the request's end (real persistence)."""
    from matrx_ai.config import ToolCallContent, ToolResultContent

    get_app_context().metadata.pop("history_cut", None)
    AgentCache.set(CONVERSATION, Agent(config=_agent_config(late)))
    config = await ConversationResolver.from_conversation_id(CONVERSATION, user_input=question)
    # The host's per-turn context (a changing fact).
    config.messages.attach_turn_context(f"<live_date>Ask {n}: it is now 09:0{n}.</live_date>", slot="live_date")
    prep = await prepare_for_send(config, stage=STAGE_LOOP, conversation_id=CONVERSATION, request_id=f"req-{n}", iteration=1)
    request = _translate(db.provider, prep.wire_config if prep.wire_config is not None else config)
    verdict = dict(get_app_context().metadata.get("history_cut") or {})
    at = turn_person_index(list(config.messages))
    if loop:
        config.messages.append(UnifiedMessage(role="assistant", content=[ToolCallContent(id=f"c{n}", name="memory", arguments={"q": "week"})]))
        config.messages.append(UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id=f"c{n}", name="memory", content="Nothing saved for that week.")]))
        prep = await prepare_for_send(config, stage=STAGE_LOOP, conversation_id=CONVERSATION, request_id=f"req-{n}", iteration=2)
        request = _translate(db.provider, prep.wire_config if prep.wire_config is not None else config)
    # The reply lands; the turn ends exactly as the executor ends it.
    her = db.row("user", question)
    config.messages.append(UnifiedMessage(role="assistant", content=[TextContent(text=f"Here is the plan ({n}).")]))
    executor._strip_ephemeral_for_storage(config, SimpleNamespace(reserved_message_ids={at: her.id}))
    db.row("assistant", f"Here is the plan ({n}).")
    await persistence._refresh_cache_state(CONVERSATION, [{"provider": db.provider, "ai_model": PROFILES[db.provider].model_name, "raw_usage": {}}], None)
    sent = {"request": request, "verdict": verdict, "prep": prep, "config": config, "strings": _strings(request)}
    if db.provider == "anthropic":
        messages = request["messages"]
        sent.update(messages=messages, mark=_rolling_mark(messages))
    return sent


def _newest_turn_text(sent: dict[str, Any]) -> str:
    return "\n".join(t for m in sent["messages"][sent["mark"] + 1 :] for t in _texts(m))


@pytest.mark.asyncio
@pytest.mark.parametrize("next_ask_on", ["same_task", "another_task"])
async def test_a_warm_ask_reads_the_late_tools_from_the_cached_prefix(thread, next_ask_on) -> None:
    thread.go_warm()  # a warm cadence: this ask stamps its carrier
    first = await _ask(thread, 1, "Plan my week.")
    first_defs = _definitions(first["messages"])
    assert set(first_defs) == set(LATE), first_defs
    assert set(_definitions(first["messages"][first["mark"] + 1 :])) == set(LATE), "the first ask carries them in its newest turn"
    if next_ask_on == "another_task":
        _forget_this_process()

    second = await _ask(thread, 2, "And next week?")
    before, after = second["messages"][: second["mark"] + 1], second["messages"][second["mark"] + 1 :]
    # (i) every definition lies BEFORE the rolling mark: read from the cache, never re-sent after it.
    assert set(_definitions(before)) == set(LATE), f"the late tools are not inside the cached prefix: {_definitions(before).keys()}"
    assert not _definitions(after), "the newest turn re-sent late tool definitions an earlier turn already carries"
    # (ii) the model sees the same tools, defined byte for byte as on the first ask, named as available now, and
    # the same context facts; nothing is declared twice and no late tool rides the tools list.
    assert _definitions(second["messages"]) == first_defs
    newest = _newest_turn_text(second)
    assert "<late_tools_available>" in newest and all(name in newest for name in LATE), newest[-600:]
    assert "Ask 2: it is now 09:02." in newest
    assert sum(t.count("### late_calendar_probe") for m in second["messages"] for t in _texts(m)) == 1
    assert not set(LATE) & {t.get("name") for t in second["request"]["tools"]}
    assert _newest_turn_text(second).rstrip().endswith("And next week?")
    # The a749a4cd1df byte check: a warm send held the prefix the last send cached, byte for byte.
    prefix = second["verdict"]["prefix"]
    assert prefix["action"] == "held", prefix
    assert prefix["bytes"]["first_difference"] is None and prefix["bytes"]["compared"] > 0, prefix


@pytest.mark.asyncio
async def test_a_late_tool_added_between_sends_is_appended_and_the_prefix_holds(thread) -> None:
    thread.go_warm()  # a warm cadence: this ask stamps its carrier
    await _ask(thread, 1, "Plan my week.")
    second = await _ask(thread, 2, "And next week?")
    third = await _ask(thread, 3, "Draft the agenda document.", late=[*LATE, ADDED])
    # (iii) only the new definition rides the newest turn; the earlier ones stay where they were.
    assert set(_definitions(third["messages"][third["mark"] + 1 :])) == {ADDED}
    assert set(_definitions(third["messages"][: third["mark"] + 1])) == set(LATE)
    newest = _newest_turn_text(third)
    assert all(name in newest.split("<late_tools_available>", 1)[1] for name in LATE), newest[-600:]
    # Everything the second send cached is sent again byte for byte (cache marks aside).
    strip = lambda ms: [{**m, "content": [{k: v for k, v in b.items() if k != "cache_control"} for b in m["content"]]} if isinstance(m["content"], list) else m for m in ms]  # noqa: E731
    assert strip(third["messages"][: second["mark"] + 1]) == strip(second["messages"][: second["mark"] + 1])
    prefix = third["verdict"]["prefix"]
    assert prefix["action"] == "held" and prefix["bytes"]["first_difference"] is None, prefix


@pytest.mark.asyncio
async def test_a_window_that_cuts_the_carrying_turn_re_emits_it_and_says_moved(thread) -> None:
    thread.go_warm()  # a warm cadence: this ask stamps its carrier
    await _ask(thread, 1, "Plan my week.")
    await _ask(thread, 2, "And next week?")
    # (iv) the cache goes cold and the window keeps only the last turn: the turn carrying the definitions is cut.
    thread.go_cold()
    thread.window["turns"] = 1
    _forget_this_process()
    third = await _ask(thread, 3, "Draft the agenda document.")
    assert set(_definitions(third["messages"][third["mark"] + 1 :])) == set(LATE), "a cut carrier's tools were lost"
    assert set(_definitions(third["messages"])) == set(LATE)
    prefix = third["verdict"]["prefix"]
    assert prefix["action"] == "moved" and any("history window moved" in r for r in prefix["reasons"]), prefix


def test_a_fit_that_drops_a_kept_block_leaves_its_late_tools_behind() -> None:
    """A whole kept block may leave the wire when it does not fit; the late tool definitions inside it may not."""
    from matrx_ai.config.message_config import MessageList
    from matrx_ai.config.typed_text_last import (
        LATE_TOOLS_CARRIER_KEY,
        REPLAYED_LATE_SLOTS_KEY,
        REPLAYED_TURN_KEY,
        host_turn,
    )

    person = UnifiedMessage(role="user", content=[TextContent(text="Plan my week.")])
    defined = {"late_tools:late_calendar_probe": "<late_tools>\nThese tools are available now.\n\n### late_calendar_probe\nx\n</late_tools>"}
    kept = host_turn(person, "<turn_context source=\"platform\">\nkept\n</turn_context>")
    kept.metadata = {REPLAYED_TURN_KEY: True, REPLAYED_LATE_SLOTS_KEY: defined}
    page = host_turn(person, "<turn_context source=\"platform\">\npage only\n</turn_context>")
    page.metadata = {REPLAYED_TURN_KEY: True}
    wire = SimpleNamespace(messages=MessageList(_messages=[kept, person, page, person]))
    assert send_boundary._drop_replayed_turn_context(wire) == 2
    left = list(wire.messages)
    assert len(left) == 3 and left[0].metadata.get(LATE_TOOLS_CARRIER_KEY)
    assert "### late_calendar_probe" in left[0].content[0].text and "kept" not in left[0].content[0].text
    # A carrier is never dropped again (a sticky drop rebuilds the same bytes).
    assert send_boundary._drop_replayed_turn_context(wire) == 0 and len(list(wire.messages)) == 3


@pytest.mark.asyncio
async def test_fit_pressure_never_stubs_a_carrier(thread) -> None:
    """F1 (review of c8a79d95939): under input-fit pressure the last-resort pass stubbed earlier texts oldest first,
    the carrier among them — the newest turn named the tools available and their definitions were gone (sticky)."""
    thread.go_warm()  # a warm cadence: this ask stamps its carrier
    await _ask(thread, 1, "Plan my week.")
    input_fit.set_input_budget_resolver(_over_budget_by_one)
    second = await _ask(thread, 2, "And next week?")
    assert _definition_counts(second["messages"]) == dict.fromkeys(LATE, 1), _definition_counts(second["messages"])
    newest = _newest_turn_text(second)
    assert all(name in newest for name in LATE), newest[-600:]
    # The stubs are sticky: the next send of the same pressure still carries every definition whole, once.
    third = await _ask(thread, 3, "Draft the agenda document.")
    assert _definition_counts(third["messages"]) == dict.fromkeys(LATE, 1), _definition_counts(third["messages"])


@pytest.mark.asyncio
async def test_a_definition_a_fit_pass_left_off_the_wire_goes_out_in_the_newest_turn_and_says_moved(thread, monkeypatch) -> None:
    """The second layer, alone: a fit pass that DID stub a carrier (the first layer switched off) leaves its
    definitions off the wire; they go out in the newest turn, once, and the prefix is recorded moved."""
    thread.go_warm()  # a warm cadence: this ask stamps its carrier
    await _ask(thread, 1, "Plan my week.")
    monkeypatch.setattr(input_fit, "holds_late_tool_definitions", lambda _message: False)
    input_fit.set_input_budget_resolver(_over_budget_by_one)
    second = await _ask(thread, 2, "And next week?")
    assert _definition_counts(second["messages"]) == dict.fromkeys(LATE, 1), _definition_counts(second["messages"])
    after = second["messages"][second["mark"] + 1 :]
    assert set(_definitions(after)) == set(LATE), "a stubbed carrier's definitions were not re-sent in the newest turn"
    prefix = second["verdict"]["prefix"]
    assert prefix["action"] == "moved" and any("late tool definitions re-sent" in r for r in prefix["reasons"]), prefix
    assert second["prep"].late_tools_resent == sorted(f"late_tools:{n}" for n in LATE)


#: The words that claim availability. Only the newest turn's names slot may say which late tools are available.
CLAIM = "These tools are available now"


def _carrier_count(messages: list[dict[str, Any]]) -> int:
    return sum(text.count(late_tools.CARRIER_OPEN) for m in messages for text in _texts(m))


def _available_names(text: str) -> str:
    found = re.findall(r"<late_tools_available>\n(.*?)\n</late_tools_available>", text, flags=re.S)
    assert len(found) == 1, found
    return found[0]


def _stored(thread: _Thread, question: str) -> dict[str, Any]:
    """Her row's metadata as the database holds it (the executor's turn end wrote it)."""
    return next(r for r in thread.messages if r.role == "user" and r.content[0]["text"] == question).metadata


@pytest.mark.asyncio
async def test_a_tool_loop_turns_kept_block_carries_its_late_tools_once(thread) -> None:
    """F9: a tool-loop turn keeps its WHOLE block (late definitions inside, by slot) on her row; the next ask replays
    that block and gets no separate carrier, every definition once, inside the cached prefix — under fit pressure too.
    (The loop's own tool rows are not stored here: what is replayed rides her row's metadata.)"""
    from matrx_ai.config.typed_text_last import STORED_LATE_TOOLS_KEY, STORED_TURN_CONTEXT_KEY

    thread.go_warm()
    await _ask(thread, 1, "Plan my week.", loop=True)
    stored = _stored(thread, "Plan my week.")
    assert all(f"### {n}" in stored[STORED_TURN_CONTEXT_KEY] for n in LATE) and STORED_LATE_TOOLS_KEY not in stored
    second = await _ask(thread, 2, "And next week?")
    assert _definition_counts(second["messages"]) == dict.fromkeys(LATE, 1), _definition_counts(second["messages"])
    assert set(_definitions(second["messages"][: second["mark"] + 1])) == set(LATE)
    assert _carrier_count(second["messages"]) == 0
    assert all(n in _available_names(_newest_turn_text(second)) for n in LATE)
    assert not any(CLAIM in t for t in second["strings"]), "a replayed definition claims availability"
    input_fit.set_input_budget_resolver(_over_budget_by_one)
    third = await _ask(thread, 3, "Draft the agenda document.")
    assert _definition_counts(third["messages"]) == dict.fromkeys(LATE, 1), _definition_counts(third["messages"])
    assert all(n in _available_names(_newest_turn_text(third)) for n in LATE)


@pytest.mark.asyncio
async def test_a_converted_chats_tool_loop_kept_block_carries_its_late_tools_once(thread) -> None:
    """Chat conversion (aidream ``tooling/chat_mode.py``): a converted run forces its added tools late
    (``late_tools.FORCED_KEY``) whatever the scope. Under scope ``enrolled`` with an agent that is NOT enrolled,
    the forced run's tool-loop kept block carries every late definition once and no carrier rides twice — the
    same cache stability across the tool loop as the enrolled case above (chat-agent-skills R5)."""
    configure_prompt_cache_knobs(lambda key: {"late_tools_enabled": True, "late_tools_scope": "enrolled"}.get(key))
    assert not late_tools._in_scope(), "the fixture's agent must not be enrolled for this case to mean anything"
    get_app_context().metadata[late_tools.FORCED_KEY] = True
    thread.go_warm()
    await _ask(thread, 1, "Plan my week.", loop=True)
    second = await _ask(thread, 2, "And next week?")
    assert _definition_counts(second["messages"]) == dict.fromkeys(LATE, 1), _definition_counts(second["messages"])
    assert set(_definitions(second["messages"][: second["mark"] + 1])) == set(LATE)
    assert _carrier_count(second["messages"]) == 0
    third = await _ask(thread, 3, "Draft the agenda document.")
    assert _definition_counts(third["messages"]) == dict.fromkeys(LATE, 1), _definition_counts(third["messages"])
    assert set(LATE).isdisjoint({t.get("name") for t in third["request"].get("tools") or []})


@pytest.mark.asyncio
async def test_a_tool_no_longer_offered_is_never_said_available_and_is_refused_cleanly(thread, monkeypatch) -> None:
    """F3: a revoked late tool keeps its definition in its old carrier (the cached prefix holds), but nothing on the
    wire says it is available — the newest turn's names slot lists exactly this send's offer — and a call to it is
    refused with a message the model can act on."""
    from matrx_ai.orchestrator.executor import _resolve_allowed_tools
    from matrx_ai.persistence import queue_helpers
    from matrx_ai.tools.executor import ToolExecutor

    thread.go_warm()
    await _ask(thread, 1, "Plan my week.")
    kept, revoked = LATE
    second = await _ask(thread, 2, "And next week?", late=[kept])
    assert _definition_counts(second["messages"]) == dict.fromkeys(LATE, 1)
    assert not any(CLAIM in t for t in second["strings"]), "a definition claims availability"
    named = _available_names(_newest_turn_text(second))
    assert kept in named and revoked not in named, named
    prefix = second["verdict"]["prefix"]
    assert prefix["action"] == "held" and prefix["bytes"]["first_difference"] is None, prefix

    class _Silent:
        def prepare_metadata(self, *_a: Any, **_k: Any) -> None:
            return None

        def __getattr__(self, _name: str) -> Any:
            async def _noop(*_a: Any, **_k: Any) -> None:
                return None

            return _noop

    monkeypatch.setattr(queue_helpers, "get_coordinator", lambda: None)
    tool_executor = ToolExecutor(registry=registry_module.ToolRegistry._instance, execution_logger=_Silent())
    _, refused = await tool_executor.execute(
        revoked, {"q": "x"}, ToolContext(call_id="gone-1", tool_name=revoked),
        allowed_tools=_resolve_allowed_tools(second["config"]),
    )
    assert not refused.success and refused.error.error_type == "not_allowed", refused.error
    assert "names as available now" in refused.error.suggested_action, refused.error.suggested_action


@pytest.mark.asyncio
async def test_the_knob_turned_off_after_stamping_is_a_clean_rollback(thread) -> None:
    """F2: with ``agents.prompt_cache.late_tools_enabled`` off the tools ride the tools list again and the stamped
    carrier is not replayed — no tool declared twice, no names slot, no late-tools text at all (the old wire)."""
    thread.go_warm()
    await _ask(thread, 1, "Plan my week.")
    assert _stored(thread, "Plan my week.").get("late_tools_in_cache")
    configure_prompt_cache_knobs(lambda key: {"late_tools_enabled": False}.get(key))
    second = await _ask(thread, 2, "And next week?")
    assert set(LATE) <= {t.get("name") for t in second["request"]["tools"]}
    assert not any("<late_tools" in t or late_tools.CARRIER_OPEN in t for t in second["strings"]), [
        t[:200] for t in second["strings"] if "late_tools" in t
    ]


def _reregister(ask: int, *, changing: str | None) -> None:
    """The registry as another process loads it: the late tools' parameters in an order that flips every ask
    (a jsonb round trip reorders keys), and — with ``changing`` — that tool's description really changes."""
    reg = registry_module.ToolRegistry._instance
    params = [
        ("q", {"type": "string", "description": "A query.", "required": True}),
        ("limit", {"description": "How many.", "required": True, "type": "integer"}),
    ]
    if ask % 2:
        params = [(k, dict(reversed(list(v.items())))) for k, v in reversed(params)]
    definitions = []
    for name in LATE:
        definition = _definition(name)
        definition.parameters = dict(params)
        if name == changing:
            definition.description += f" Revision {ask}."
        definitions.append(definition)
    reg.load_from_definitions(definitions)


@pytest.mark.asyncio
@pytest.mark.parametrize("changing", [None, "late_calendar_probe"])
async def test_thirty_asks_never_accumulate_carriers(thread, changing) -> None:
    """F4: a definition whose key order varies between processes is the SAME definition (canonical digest and
    render): stamped once, read from the cache on every later ask. One that truly changes every ask is re-sent in
    the newest turn and its superseded copies leave the wire: each tool defined exactly once, one carrier, always."""
    for ask in range(1, 31):
        thread.go_warm()
        _reregister(ask, changing=changing)
        sent = await _ask(thread, ask, f"Ask number {ask}?")
        if ask == 1:
            continue
        assert _definition_counts(sent["messages"]) == dict.fromkeys(LATE, 1), (ask, _definition_counts(sent["messages"]))
        assert _carrier_count(sent["messages"]) == 1, (ask, _carrier_count(sent["messages"]))
        after = set(_definitions(sent["messages"][sent["mark"] + 1 :]))
        assert after == ({changing} if changing else set()), (ask, after)
        if changing is None and ask > 2:
            prefix = sent["verdict"]["prefix"]
            assert prefix["action"] == "held" and prefix["bytes"]["first_difference"] is None, (ask, prefix)


@pytest.mark.asyncio
async def test_a_cold_cadence_stamps_no_carrier_and_a_warm_one_does(thread) -> None:
    """F6: a carrier is written before the rolling mark (1.25x on a cold send). An ask that found the cache cold
    stamps nothing (the next ask sends its definitions in the newest turn, 1x); an ask that found it warm stamps,
    and the ask after reads them from the cache — the prefix the warm ask cached held byte for byte."""
    await _ask(thread, 1, "Plan my week.")  # three hours after the last answer: cold
    assert "late_tools_in_cache" not in _stored(thread, "Plan my week.")
    second = await _ask(thread, 2, "And next week?")  # a moment later: warm
    assert set(_definitions(second["messages"][second["mark"] + 1 :])) == set(LATE)
    assert _carrier_count(second["messages"]) == 0
    assert set(_stored(thread, "And next week?").get("late_tools_in_cache") or {}) == {f"late_tools:{n}" for n in LATE}
    third = await _ask(thread, 3, "Draft the agenda document.")
    assert not _definitions(third["messages"][third["mark"] + 1 :])
    assert _definition_counts(third["messages"]) == dict.fromkeys(LATE, 1) and _carrier_count(third["messages"]) == 1
    prefix = third["verdict"]["prefix"]
    assert prefix["action"] == "held" and prefix["bytes"]["first_difference"] is None, prefix


def _declared_names(provider: str, request: Any) -> set[str]:
    if provider == "google":
        tools = getattr(request["config"], "tools", None) or []
        return {d.name for tool in tools for d in (getattr(tool, "function_declarations", None) or [])}
    return {t.get("name") or (t.get("function") or {}).get("name") for t in request.get("tools") or []}


@pytest.mark.asyncio
@pytest.mark.parametrize("provider", ["google", "openai"])
async def test_the_google_and_openai_wire_define_each_late_tool_once(thread, provider) -> None:
    """F9: the same rows through the Google and OpenAI translators: the request builds, each late tool is defined
    exactly once (none in the tools list) and the names slot lists every one — removed one included in the test."""
    thread.provider = provider
    thread.go_warm()
    await _ask(thread, 1, "Plan my week.")
    for n, late in ((2, LATE), (3, [LATE[0]])):
        sent = await _ask(thread, n, f"Ask {n}?", late=late)
        counts: dict[str, int] = {}
        for name, _digest in late_tools.wire_definitions(sent["strings"]):
            counts[name] = counts.get(name, 0) + 1
        assert counts == dict.fromkeys(LATE, 1), (provider, n, counts)
        assert not set(LATE) & _declared_names(provider, sent["request"]), _declared_names(provider, sent["request"])
        names = [t for t in sent["strings"] if "<late_tools_available>" in t]
        assert names and all(x in _available_names(names[-1]) for x in late), names
        assert not any(CLAIM in t for t in sent["strings"])
