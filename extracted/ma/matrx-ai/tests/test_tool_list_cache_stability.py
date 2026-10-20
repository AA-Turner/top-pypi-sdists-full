"""The provider tools array is append-only for the life of a conversation.

Real failures this pins (common-docs projects/agent-evaluation/reports/
tool-list-cache-stability.md):
- the loop guard removed ``records`` mid-turn (74 -> 73 tools): 170,818 tokens
  re-written, 92.3 cents, in conversation 3787dd66;
- the filesystem-authority gate flipped ``local_file``/``local_shell`` out and in
  on every suspend/resume (60b6f5e7, 86d096b9, 6f713c93);
- the per-request re-merge after resume reordered the list;
- a bundle load inserted 57 registered tools BEFORE the inline
  ``apply_surface_write`` instead of after it.
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_connect.emitters.silent_emitter import SilentEmitter

from matrx_ai.providers import cache_guard
from matrx_ai.tools import declaration_ledger


class _NullEmitter(SilentEmitter):
    def __getattr__(self, _name: str):
        async def _noop(*_a: Any, **_kw: Any) -> None: ...

        return _noop


class _Config:
    def __init__(self, custom_tools: list[Any]):
        self.tools: list[str] = []
        self.custom_tools = custom_tools


class _Inline:
    def __init__(self, name: str, description: str = "d"):
        self.name = name
        self.description = description

    def get_provider_format(self, provider: str) -> dict[str, Any]:
        return {"name": self.name, "description": self.description, "input_schema": {}}


@pytest.fixture()
def translator():
    from matrx_ai.providers.base_translator import BaseTranslator

    class _T(BaseTranslator):
        def _assemble_request(self, config, api_class=""):  # pragma: no cover
            return None

    return _T()


@pytest.fixture()
def conversation():
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    ctx = AppContext(
        emitter=_NullEmitter(),
        metadata={},
        is_authenticated=True,
        conversation_id="11111111-1111-4111-8111-111111111111",
    )
    token = set_app_context(ctx)
    yield ctx
    clear_app_context(token)


def _names(decls: list[dict[str, Any]]) -> list[str]:
    return [d["name"] for d in decls]


def _send(translator, *names: str, described: dict[str, str] | None = None):
    described = described or {}
    config = _Config([_Inline(n, described.get(n, "d")) for n in names])
    return translator.build_provider_tools(config, "anthropic")


def test_a_withdrawn_tool_stays_declared(translator, conversation):
    _send(translator, "research_web", "records", "memory")
    after = _send(translator, "research_web", "memory")
    assert _names(after) == ["research_web", "records", "memory"]


def test_order_is_pinned_by_first_sight(translator, conversation):
    _send(translator, "a", "b", "c")
    assert _names(_send(translator, "c", "a", "b")) == ["a", "b", "c"]


def test_new_tools_are_appended_after_every_earlier_one(translator, conversation):
    _send(translator, "research_web", "apply_surface_write")
    after = _send(translator, "research_web", "mcp.notion.fetch", "apply_surface_write")
    assert _names(after) == ["research_web", "apply_surface_write", "mcp__notion__fetch"]


def test_changed_definition_is_adopted_once_as_a_recorded_break(translator, conversation):
    conv = conversation.conversation_id
    _send(translator, "a", "b", described={"b": "original"})
    later = _send(translator, "a", "b", described={"b": "new mcp version"})
    assert [d["description"] for d in later] == ["d", "new mcp version"]
    events = declaration_ledger.drain_events(conv)
    assert [e["kind"] for e in events] == ["tool_definition_updated"]
    _send(translator, "a", "b", described={"b": "new mcp version"})
    assert declaration_ledger.drain_events(conv) == []  # one break, not one per request


def test_toolless_call_is_untouched(translator, conversation):
    _send(translator, "a", "b")
    assert _send(translator) == []


def test_whole_belt_swap_is_a_recorded_announced_break(translator, conversation):
    """Adversarial I2 (2026-10-18): a toolset sharing NO name with the ledger (an
    agent switch mid-conversation) replaced the tools head silently — no event,
    no capture, no client warning, and the ledger kept the old array. It is now
    adopted as a deliberate break: recorded, seq bumped, announced."""
    conv = conversation.conversation_id
    _send(translator, "a", "b")
    seq_before = declaration_ledger.export_record(conv)["anthropic"]["seq"]
    assert _names(_send(translator, "c", "d")) == ["c", "d"]
    events = declaration_ledger.drain_events(conv)
    assert [e["kind"] for e in events] == ["tool_belt_replaced"], events
    assert events[0]["previous_tools"] == ["a", "b"] and events[0]["tools"] == ["c", "d"]
    record = declaration_ledger.export_record(conv)["anthropic"]
    assert [t["name"] for t in record["tools"]] == ["c", "d"]
    assert record["seq"] > seq_before
    # The new belt is now the ledger: it stays append-only from here.
    assert _names(_send(translator, "d", "e")) == ["c", "d", "e"]
    assert declaration_ledger.drain_events(conv) == []
    from matrx_ai.orchestrator.executor import _TOOL_LEDGER_EVENT_TEXT

    assert "tool_belt_replaced" in _TOOL_LEDGER_EVENT_TEXT


def test_a_call_without_a_conversation_is_never_tracked(translator):
    assert _names(_send(translator, "a", "b")) == ["a", "b"]
    assert _names(_send(translator, "judge_tool")) == ["judge_tool"]


def test_loop_guard_removal_keeps_declaration_and_refuses_with_reason(
    translator, conversation
):
    from matrx_ai.orchestrator.loop_guard import disable_failing_tool

    config = _Config([_Inline("records"), _Inline("memory")])
    translator.build_provider_tools(config, "anthropic")
    outcome = disable_failing_tool(config, "records")
    assert outcome.removed
    declaration_ledger.note_unavailable(["records"], "it failed 9 time(s) in this run")
    after = translator.build_provider_tools(config, "anthropic")
    assert _names(after) == ["records", "memory"]
    reason = declaration_ledger.retained_reason("records")
    assert reason is not None and "failed 9" in reason
    assert declaration_ledger.retained_reason("memory") is None


@pytest.mark.asyncio
async def test_executor_refuses_a_retained_tool_by_name(translator, conversation):
    from matrx_ai.tools.executor import ToolExecutor
    from matrx_ai.tools.models import ToolContext, ToolResult
    from matrx_ai.tools.registry import ToolRegistry

    async def _ran(args: dict[str, Any], ctx: Any) -> Any:
        return ToolResult(success=True, output={"ran": True}, tool_name=ctx.tool_name)

    registry = ToolRegistry.get_instance()
    registry.clear()
    registry.register_local(name="local_file", func=_ran, description="files")
    try:
        _send(translator, "local_file", "memory")
        _send(translator, "memory")  # desktop went quiet: local_file withdrawn
        declaration_ledger.note_unavailable(["local_file"], "My Computer is not answering")
        _content, result = await ToolExecutor(registry=registry).execute(
            "local_file",
            {},
            ToolContext(call_id="c1", tool_name="local_file"),
            allowed_tools=frozenset({"memory"}),
        )
        assert result.success is False
        assert result.error.error_type == "tool_unavailable"
        assert "My Computer is not answering" in result.error.message
        # No allowlist this request: a withdrawn tool still must not run.
        _content, result = await ToolExecutor(registry=registry).execute(
            "local_file",
            {},
            ToolContext(call_id="c2", tool_name="local_file"),
            allowed_tools=None,
        )
        assert result.error is not None and result.error.error_type == "tool_unavailable"
    finally:
        registry.clear()


# ── the independent wire-level guard ─────────────────────────────────────────


def _payload(*names: str, described: dict[str, str] | None = None) -> dict[str, Any]:
    described = described or {}
    return {
        "model": "claude-opus-5-5",
        "tools": [{"name": n, "description": described.get(n, "d")} for n in names],
    }


@pytest.fixture()
def captured(monkeypatch):
    seen: list[dict[str, Any]] = []
    monkeypatch.setattr(cache_guard, "_schedule_tool_list_capture", seen.append)
    return seen


CONV = "22222222-2222-4222-8222-222222222222"


def _observe(payload):
    return cache_guard.observe_tool_declarations(
        provider="anthropic", conversation_id=CONV, payload=payload
    )


def test_guard_silent_on_append(captured):
    assert _observe(_payload("a", "b")) is None
    assert _observe(_payload("a", "b", "c")) is None
    assert captured == []


@pytest.mark.parametrize(
    ("second", "kind"),
    [
        (_payload("a", "c"), "tool_removed_mid_conversation"),
        (_payload("b", "a", "c"), "tool_reordered_mid_conversation"),
        (_payload("a", "b", "c", described={"b": "x"}), "tool_definition_changed_mid_conversation"),
        (_payload("a", "z", "b", "c"), "tool_inserted_before_existing_tools"),
    ],
)
def test_guard_screams_on_any_non_append_change(captured, second, kind):
    _observe(_payload("a", "b", "c"))
    assert _observe(second) == kind
    assert captured and captured[0]["kind"] == kind


def test_guard_screams_on_a_silent_whole_belt_swap(captured):
    _observe(_payload("a", "b", "c"))
    assert _observe(_payload("x", "y")) == "tool_belt_replaced_mid_conversation"
    assert captured and captured[0]["kind"] == "tool_belt_replaced_mid_conversation"
    # The swapped-in belt is now the baseline.
    assert _observe(_payload("x", "y", "z")) is None


def test_ledger_belt_swap_does_not_double_scream(translator, conversation, captured):
    conv = conversation.conversation_id
    for names in (("a", "b"), ("c", "d")):
        decls = _send(translator, *names)
        assert (
            cache_guard.observe_tool_declarations(
                provider="anthropic", conversation_id=conv, payload={"tools": decls}
            )
            is None
        )
    assert captured == []


def test_guard_ignores_cache_control_marker(captured):
    _observe(_payload("a", "b"))
    marked = _payload("a", "b")
    marked["tools"][-1]["cache_control"] = {"type": "ephemeral"}
    assert _observe(marked) is None


def test_ledger_and_guard_together_stay_silent(translator, conversation, captured):
    conv = conversation.conversation_id
    for names in (("a", "b", "c"), ("a", "c"), ("c", "a", "b", "d")):
        decls = _send(translator, *names)
        assert (
            cache_guard.observe_tool_declarations(
                provider="anthropic", conversation_id=conv, payload={"tools": decls}
            )
            is None
        )
    assert captured == []


# ── durable record: survives restart / crash recovery / another server ───────


def test_record_restores_the_array_after_a_restart(translator, conversation):
    from matrx_ai.config.unified_config import UnifiedConfig
    from matrx_ai.orchestrator.executor import _export_tool_ledger, _hydrate_tool_ledger

    conv = conversation.conversation_id
    _send(translator, "research_web", "records", "apply_surface_write")
    _send(translator, "research_web", "records", "mcp.notion.fetch", "apply_surface_write")
    live = UnifiedConfig(model="claude-opus-5-5", messages=[])
    _export_tool_ledger(conv, live)
    # Persist and reload the conversation config exactly as a resume does.
    stored = live.to_dict()
    assert stored["tool_declarations"]["anthropic"]["tools"][0]["name"] == "research_web"

    declaration_ledger.reset_for_tests()  # restart: process memory is gone
    reloaded = UnifiedConfig.from_dict(stored)
    _hydrate_tool_ledger(conv, reloaded)
    # The resumed loop's live set lost `records` (e.g. the guard) and re-merged
    # the rest in another order; the provider must still see the same array.
    after = _send(translator, "apply_surface_write", "mcp.notion.fetch", "research_web")
    assert _names(after) == [
        "research_web",
        "records",
        "apply_surface_write",
        "mcp__notion__fetch",
    ]


def test_the_newer_of_memory_and_record_wins(translator, conversation):
    conv = conversation.conversation_id
    _send(translator, "a", "b", "c")
    mine = declaration_ledger.export_record(conv)
    seq = mine["anthropic"]["seq"]
    older = {"anthropic": {"seq": seq - 1, "tools": [{"name": "z", "declaration": {"name": "z"}}]}}
    assert declaration_ledger.hydrate_from_record(conv, older) is False
    assert _names(_send(translator, "a", "b", "c")) == ["a", "b", "c"]
    # Another server appended `d` and saved seq+5: this server must take it.
    newer = {"anthropic": {"seq": seq + 5, "tools": mine["anthropic"]["tools"]
             + [{"name": "d", "declaration": {"name": "d", "description": "d", "input_schema": {}}}]}}
    assert declaration_ledger.hydrate_from_record(conv, newer) is True
    assert _names(_send(translator, "a", "b", "c")) == ["a", "b", "c", "d"]


def test_loop_guard_notice_does_not_list_the_belt():
    from matrx_ai.orchestrator.loop_guard import ToolDisableOutcome, disabled_tool_notice

    belt = tuple(f"mcp.notion.tool_{i}" for i in range(70))
    text = disabled_tool_notice(
        ToolDisableOutcome(tool="records", removed=True, remaining_tools=belt, was_only_tool=False),
        reason="it failed 9 time(s) in this run",
    )
    assert "records" in text and "still work" in text
    assert "mcp.notion.tool_0" not in text
    assert len(text) < 400


# ── saved after each accepted send; kept out of snapshots ───────────────────


def test_snapshot_unified_payload_omits_the_record():
    from matrx_ai.orchestrator.executor import _omit_tool_declaration_record

    unified = {"config": {"tool_declarations": {"anthropic": {"seq": 3, "tools": [{"name": "a"}, {"name": "b"}]}}}}
    _omit_tool_declaration_record(unified)
    assert unified["config"]["tool_declarations"] == {"anthropic": "2 declarations, seq 3 (omitted)"}


def test_export_saves_only_when_the_array_changed(translator, conversation, monkeypatch):
    from matrx_ai.config.unified_config import UnifiedConfig
    from matrx_ai.orchestrator import executor as orch

    saved: list[dict] = []
    monkeypatch.setattr(orch, "detached_task", lambda coro, name=None: (saved.append(name), coro.close()))
    conv = conversation.conversation_id
    live = UnifiedConfig(model="claude-opus-5-5", messages=[])
    _send(translator, "a", "b")
    orch._export_tool_ledger(conv, live, store=True)
    orch._export_tool_ledger(conv, live, store=True)  # unchanged: no second save
    _send(translator, "a", "b", "c")
    orch._export_tool_ledger(conv, live, store=True)  # appended: saved again
    assert saved == ["tool_declaration_record_save", "tool_declaration_record_save"]


@pytest.mark.asyncio
async def test_record_save_replaces_only_its_key_on_an_existing_row(monkeypatch):
    import contextlib

    import matrx_ai.persistence as persistence_pkg
    from matrx_ai.db import persistence

    class _Row:
        config = {"model": "m", "dynamic_tools": ["x"]}

    class _Conv:
        async def load_conversation_by_id(self, _id):
            return _Row() if _id == "exists" else None

    class _Cxm:
        conversation = _Conv()

    queued: list[tuple[str, dict]] = []

    @contextlib.asynccontextmanager
    async def _standalone(**_kw):
        yield None

    monkeypatch.setattr(persistence, "_cxm", lambda: _Cxm())
    monkeypatch.setattr(persistence, "_queue_conversation_update", lambda cid, **f: queued.append((cid, f)))
    monkeypatch.setattr(persistence_pkg, "standalone_coordinator", _standalone)
    record = {"anthropic": {"seq": 2, "tools": [{"name": "a", "declaration": {"name": "a"}}]}}
    assert await persistence.save_tool_declaration_record("exists", record) is True
    assert queued == [("exists", {"config": {"model": "m", "dynamic_tools": ["x"], "tool_declarations": record}})]
    assert await persistence.save_tool_declaration_record("first-turn", record) is False
    # A row already holding a NEWER record (another server) is never overwritten.
    _Row.config = {"tool_declarations": {"anthropic": {"seq": 9, "tools": []}}}
    queued.clear()
    assert await persistence.save_tool_declaration_record("exists", record) is False
    assert queued == []


# ── review 2026-10-17 item 2: ceiling, recycled names, guard, announcements ──


def test_provider_ceiling_evicts_the_longest_withdrawn_first(conversation):
    conv = conversation.conversation_id

    def send(*names, ceiling=4):
        decls = [{"name": n, "description": "d"} for n in names]
        return declaration_ledger.stabilize_declarations(
            "openai", decls, name_of=lambda d: d.get("name"), max_tools=ceiling, identities={}
        )

    send("a", "b", "c", "d")
    send("b", "c", "d")  # a withdrawn first
    send("c", "d")  # then b
    result = send("c", "d", "e", "f")
    assert [d["name"] for d in result.declarations] == ["c", "d", "e", "f"]
    events = declaration_ledger.drain_events(conv)
    assert events and events[-1]["kind"] == "tool_ceiling_eviction"
    assert events[-1]["tools"] == ["a", "b"]


def test_openai_wires_carry_the_documented_ceiling():
    from matrx_ai.providers.tool_count_limits import provider_tool_ceiling

    assert provider_tool_ceiling("openai") == 128
    assert provider_tool_ceiling("anthropic") is None


def test_recycled_projection_name_is_re_described_for_its_new_agent(translator, conversation):
    from matrx_ai.tools.agent_projection import PROJECTED_AGENT_TOOLS_KEY

    conv = conversation.conversation_id
    conversation.metadata[PROJECTED_AGENT_TOOLS_KEY] = {"custom_tool_1": {"prompt_id": "agent-A"}}
    _send(translator, "memory", "custom_tool_1", described={"custom_tool_1": "Agent A: writes poems"})
    # Next request numbers a DIFFERENT agent as custom_tool_1.
    conversation.metadata[PROJECTED_AGENT_TOOLS_KEY] = {"custom_tool_1": {"prompt_id": "agent-B"}}
    after = _send(translator, "memory", "custom_tool_1", described={"custom_tool_1": "Agent B: files taxes"})
    assert after[1]["description"] == "Agent B: files taxes"
    assert [e["kind"] for e in declaration_ledger.drain_events(conv)] == [
        "tool_name_reassigned"
    ]


def test_guard_does_not_rescream_a_deliberate_break(translator, conversation, captured):
    conv = conversation.conversation_id
    first = _send(translator, "a", "b", described={"b": "v1"})
    cache_guard.observe_tool_declarations(provider="anthropic", conversation_id=conv, payload={"tools": first})
    second = _send(translator, "a", "b", described={"b": "v2"})
    assert (
        cache_guard.observe_tool_declarations(
            provider="anthropic", conversation_id=conv, payload={"tools": second}
        )
        is None
    )
    assert captured == []


@pytest.mark.asyncio
async def test_deliberate_breaks_are_captured_and_warned(translator, conversation, monkeypatch):
    import matrx_connect.streaming.error_capture as ec

    from matrx_ai.orchestrator.executor import _announce_tool_ledger_events

    conv = conversation.conversation_id
    captures: list[str] = []

    async def _capture(exc, *, kind, **fields):
        captures.append(fields.get("error_type"))

    warnings: list[Any] = []

    class _Emitter:
        async def send_warning(self, payload):
            warnings.append(payload)

    class _Ctx:
        emitter = _Emitter()

    monkeypatch.setattr(ec, "capture_error", _capture)
    _send(translator, "a", "b", described={"b": "v1"})
    _send(translator, "a", "b", described={"b": "v2"})
    await _announce_tool_ledger_events(conv, _Ctx())
    assert captures == ["tool_definition_updated"]
    assert warnings and warnings[0].code == "tool_definition_updated"


def test_forget_releases_memory_and_reasons(translator, conversation):
    conv = conversation.conversation_id
    _send(translator, "a", "b")
    declaration_ledger.note_unavailable(["b"], "gone")
    declaration_ledger.forget_conversation(conv)
    assert declaration_ledger.export_record(conv) is None
    assert declaration_ledger.retained_reason("b") is None


def test_a_tool_offered_again_drops_its_stale_reason(translator, conversation):
    _send(translator, "a", "b")
    _send(translator, "a")
    declaration_ledger.note_unavailable(["b"], "old cause")
    _send(translator, "a", "b")  # b is back
    _send(translator, "a")  # withdrawn again, no reason recorded this time
    assert declaration_ledger.retained_reason("b") == declaration_ledger.DEFAULT_UNAVAILABLE_REASON
