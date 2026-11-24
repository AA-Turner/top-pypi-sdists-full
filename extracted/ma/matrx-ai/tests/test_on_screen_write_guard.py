"""W-60 — a record open on the person's screen is written only through its page.

Production, 2026-10-01 (conversation ceba31ec…, note 59678b3b…): the person
declined the agent's ``apply_surface_write`` on the approval card, and in the
same turn the agent wrote the same change through the server ``note`` tool
(``patch``). These tests drive the REAL ``ToolExecutor.execute`` with a ``note``
tool whose body records whether it ran — a refused write must never reach it.

  (a) page-scoped + server note patch on the on-screen note → refused, door named
  (b) same patch on a different note → runs
  (c) after the person declined this turn → refused, decline named
  (d) no surface scope → unchanged (runs)
  plus: reads of the on-screen note stay open; delegated tools are never guarded.
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_connect.emitters.silent_emitter import SilentEmitter

from matrx_ai.tools.executor import ToolExecutor
from matrx_ai.tools.guardrails import GuardrailEngine
from matrx_ai.tools.lifecycle import ToolLifecycleManager
from matrx_ai.tools.logger import ToolExecutionLogger
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolResult, ToolType
from matrx_ai.tools.on_screen_write_guard import (
    ON_SCREEN_DECLINED_KEY,
    ON_SCREEN_RECORDS_KEY,
    arm_on_screen_write_guard,
    guarded_write_refusal,
    on_screen_surface_redirect,
    output_is_person_decline,
)
from matrx_ai.tools.registry import ToolRegistry

ON_SCREEN = "59678b3b-3620-442d-872b-0331ac74a1cf"
OTHER = "0b8c2d55-6f7e-4a1b-9c3d-2e4f5a6b7c8d"


class _NullEmitter(SilentEmitter):
    """Every Emitter method is a no-op (SilentEmitter mirrors the protocol); overrides below."""

    async def send_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_reasoning_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_data(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_phase(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_warning(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_error(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_tool_event(self, *_a: Any, **_kw: Any) -> None: ...
    async def fatal_error(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_end(self, *_a: Any, **_kw: Any) -> None: ...


@pytest.fixture
def registry():
    reg = ToolRegistry.get_instance()
    saved = dict(reg._tools)
    yield reg
    reg._tools = saved


@pytest.fixture
def executor(registry):
    return ToolExecutor(
        registry=registry,
        guardrails=GuardrailEngine(),
        execution_logger=ToolExecutionLogger(),
        lifecycle=ToolLifecycleManager.get_instance(),
    )


@pytest.fixture
def app_metadata():
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    ctx = AppContext(emitter=_NullEmitter(), metadata={}, is_authenticated=True)
    token = set_app_context(ctx)
    yield ctx.metadata
    clear_app_context(token)


@pytest.fixture
def note_tool(registry):
    """A ``note`` tool whose body records every call that reaches it."""
    ran: list[dict[str, Any]] = []

    async def body(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
        ran.append(dict(args))
        return ToolResult(success=True, output={"id": args.get("note_id")}, tool_name="note")

    definition = ToolDefinition(
        name="note",
        description="notes",
        parameters={},
        tool_type=ToolType.LOCAL,
        function_path="tests.fake.note",
    )
    definition._callable = body
    registry._tools["note"] = definition
    return ran


def _ctx() -> ToolContext:
    return ToolContext(call_id="call-w60", tool_name="note", emitter=_NullEmitter())


def _patch(note_id: str) -> dict[str, Any]:
    return {
        "action": "patch",
        "note_id": note_id,
        "search_text": "Routing line: Los Angeles",
        "replacement_text": "Routing line: Port of Oakland",
    }


def _arm(metadata: dict[str, Any], *, declined: bool = False) -> None:
    arm_on_screen_write_guard(
        metadata,
        {
            ON_SCREEN: {
                "resource_type": "note",
                "surface": "matrx-user/notes",
                # The live order puts a non-patchable target FIRST, so the ready call must pick by patchable.
                "targets": ["note_title", "note_content", "append_to_note"],
                "patchable_targets": ["note_content"],
            }
        },
        declined=declined,
    )


async def test_a_patch_on_the_on_screen_note_is_refused_and_names_the_door(
    executor, app_metadata, note_tool
) -> None:
    _arm(app_metadata)
    _content, result = await executor.execute("note", _patch(ON_SCREEN), _ctx())
    assert note_tool == [], "the refused write reached the note body"
    assert result.success is False
    assert result.error is not None and result.error.error_type == "record_on_screen"
    assert "apply_surface_write" in result.error.message
    assert "note_content" in result.error.message
    assert "Nothing was changed" in result.error.message
    # The redirect keeps the SMALL edit small (2026-10-01): it names the
    # anchored-edit value shape, so the model does not resend the whole note.
    assert '"command": "str_replace"' in result.error.message
    assert "old_str" in result.error.message and "new_str" in result.error.message


async def test_b_the_same_patch_on_a_different_note_runs(executor, app_metadata, note_tool) -> None:
    _arm(app_metadata)
    _content, result = await executor.execute("note", _patch(OTHER), _ctx())
    assert [c["note_id"] for c in note_tool] == [OTHER]
    assert result.success is True


async def test_c_after_the_person_declined_the_write_is_refused_as_a_decline(
    executor, app_metadata, note_tool
) -> None:
    _arm(app_metadata, declined=True)
    _content, result = await executor.execute("note", _patch(ON_SCREEN), _ctx())
    assert note_tool == []
    assert result.error is not None and result.error.error_type == "person_declined_this_change"
    assert "declined" in result.error.message


async def test_d_without_a_surface_scope_nothing_changes(executor, app_metadata, note_tool) -> None:
    arm_on_screen_write_guard(app_metadata, {})
    assert ON_SCREEN_RECORDS_KEY not in app_metadata
    _content, result = await executor.execute("note", _patch(ON_SCREEN), _ctx())
    assert [c["note_id"] for c in note_tool] == [ON_SCREEN]
    assert result.success is True


async def test_reading_the_on_screen_note_stays_open(executor, app_metadata, note_tool) -> None:
    _arm(app_metadata)
    _content, result = await executor.execute("note", {"action": "get", "note_id": ON_SCREEN}, _ctx())
    assert [c["note_id"] for c in note_tool] == [ON_SCREEN]
    assert result.success is True


def test_the_data_tool_and_nested_ids_are_guarded_too() -> None:
    metadata: dict[str, Any] = {}
    _arm(metadata)
    refused = guarded_write_refusal(
        "data", {"action": "patch", "resource_type": "note", "id": ON_SCREEN.upper()}, metadata
    )
    assert refused is not None and refused[0] == "record_on_screen"
    nested = guarded_write_refusal(
        "data", {"action": "update", "items": [{"id": ON_SCREEN, "content": "x"}]}, metadata
    )
    assert nested is not None
    assert guarded_write_refusal("data", {"action": "get", "id": ON_SCREEN}, metadata) is None


def test_a_new_turn_clears_the_decline() -> None:
    metadata: dict[str, Any] = {}
    _arm(metadata, declined=True)
    assert metadata[ON_SCREEN_DECLINED_KEY] is True
    _arm(metadata, declined=False)
    assert ON_SCREEN_DECLINED_KEY not in metadata


def test_the_stored_decline_output_is_recognised() -> None:
    stored = (
        '{"status": "declined_by_person", "declined": true, '
        '"reason": "declined_with_instructions", "message": "Nothing was changed."}'
    )
    assert output_is_person_decline(stored) is True
    assert output_is_person_decline('{"ok": true, "status": "applied_now"}') is False
    assert output_is_person_decline(None) is False


async def test_the_redirect_is_not_a_dead_end_and_hands_back_the_ready_call(
    executor, app_metadata, note_tool
) -> None:
    """Q-05 (2026-11-09, conversation 7f041c85): an agent told "if the patch fails, say so and stop"
    read the old refusal as a failed patch and stopped; the person never got the approval card.
    The refusal states facts only: not a failed edit, the change goes to the person as an approval
    card, and the same edit as a ready call on the record's PATCHABLE target (never targets[0]).
    It never tells the model to set aside its own instructions (review C74)."""
    import json

    _arm(app_metadata)
    _content, result = await executor.execute("note", _patch(ON_SCREEN), _ctx())
    assert result.error is not None and result.error.error_type == "record_on_screen"
    message = result.error.message
    assert message.startswith("Not a failed edit"), message
    lowered = message.lower()
    for override in ("does not apply", "ignore", "regardless of", "instruction", "rule"):
        assert override not in lowered, f"refusal tells the model to override its prompt: {override!r}"
    ready = message.split("approval card: apply_surface_write ", 1)[1].split(". It is the same patch", 1)[0]
    assert json.loads(ready) == {
        "target": "note_content",
        "value": {
            "command": "str_replace",
            "old_str": "Routing line: Los Angeles",
            "new_str": "Routing line: Port of Oakland",
        },
    }
    suggested = result.error.suggested_action or ""
    assert "apply_surface_write" in suggested
    assert "tell the person" not in suggested.lower()


def test_a_many_match_edit_gets_no_single_str_replace() -> None:
    """The page's anchored edit replaces exactly one match: a replace_all / occurrence call is never
    handed back as one str_replace (it would change one place and drop the rest)."""
    metadata: dict[str, Any] = {}
    _arm(metadata)
    for extra in ({"replace_all": True}, {"occurrence": 2}, {"occurrences": "all"}):
        refused = guarded_write_refusal("note", {**_patch(ON_SCREEN), **extra}, metadata)
        assert refused is not None and refused[0] == "record_on_screen"
        assert "as that approval card" not in refused[1], extra
        assert "exactly one match" in refused[1] and "note_content" in refused[1], extra
    # occurrence 1 is the single-match edit: the ready call stands.
    one = guarded_write_refusal("note", {**_patch(ON_SCREEN), "occurrence": 1}, metadata)
    assert one is not None and "as that approval card" in one[1]


def test_no_patchable_target_means_no_ready_call() -> None:
    metadata: dict[str, Any] = {}
    arm_on_screen_write_guard(
        metadata,
        {ON_SCREEN: {"resource_type": "note", "targets": ["note_title"], "patchable_targets": []}},
    )
    refused = guarded_write_refusal("note", _patch(ON_SCREEN), metadata)
    assert refused is not None and "as that approval card" not in refused[1]


# ── Q-05 (2026-11-10, conversation 12c200b3): the right edit IS the approval card ──────────
# The model's ``note`` patch on the note open on screen was the right edit, yet it came back as
# a failed tool call (tool result ca1e86ad, is_error true) and the model had to repeat it through
# ``apply_surface_write``. With the page offering that door, the executor now sends the same edit
# to the person as the card, under the same call id: no failed call, nothing written by the server.

DOOR = "apply_surface_write"


@pytest.fixture
def door(registry, executor, monkeypatch):
    """The page's ``apply_surface_write`` (a request-registered client tool) + a delegation spy."""
    registry.ensure_registered(DOOR, description="page write", parameters={})
    delegated: list[dict[str, Any]] = []

    async def fake_delegate(tool_def, args, ctx, row_id="", authorization_metadata=None):
        delegated.append({"tool": tool_def.name, "args": dict(args), "call_id": ctx.call_id})
        return ToolResult(success=False, delegated_pending=True, tool_name=tool_def.name, call_id=ctx.call_id)

    monkeypatch.setattr(executor, "_execute_delegated", fake_delegate)
    return delegated


async def test_the_right_patch_on_the_on_screen_note_goes_to_the_person_as_the_card(
    executor, app_metadata, note_tool, door
) -> None:
    _arm(app_metadata)
    _content, result = await executor.execute(
        "note", _patch(ON_SCREEN), _ctx(), client_tools=frozenset({DOOR})
    )
    assert note_tool == [], "the server note write ran on the note open on screen"
    assert result.error is None, f"the right edit came back as a failed call: {result.error}"
    assert result.delegated_pending is True
    assert door == [
        {
            "tool": DOOR,
            "args": {
                "target": "note_content",
                "value": {
                    "command": "str_replace",
                    "old_str": "Routing line: Los Angeles",
                    "new_str": "Routing line: Port of Oakland",
                },
            },
            "call_id": "call-w60",
        }
    ]


async def test_after_a_decline_the_patch_is_still_refused_never_sent_again(
    executor, app_metadata, note_tool, door
) -> None:
    _arm(app_metadata, declined=True)
    _content, result = await executor.execute(
        "note", _patch(ON_SCREEN), _ctx(), client_tools=frozenset({DOOR})
    )
    assert door == [] and note_tool == []
    assert result.error is not None and result.error.error_type == "person_declined_this_change"


async def test_a_many_match_edit_is_not_sent_as_one_card(executor, app_metadata, note_tool, door) -> None:
    _arm(app_metadata)
    _content, result = await executor.execute(
        "note", {**_patch(ON_SCREEN), "replace_all": True}, _ctx(), client_tools=frozenset({DOOR})
    )
    assert door == [] and note_tool == []
    assert result.error is not None and result.error.error_type == "record_on_screen"


async def test_with_no_page_door_this_turn_the_refusal_stands(executor, app_metadata, note_tool, door) -> None:
    _arm(app_metadata)
    _content, result = await executor.execute("note", _patch(ON_SCREEN), _ctx())
    assert door == [] and note_tool == []
    assert result.error is not None and result.error.error_type == "record_on_screen"


def test_the_rebuilt_result_answers_the_name_the_model_called() -> None:
    """Gemini pairs functionResponse to functionCall by name: the redirected row is stored under
    the door's name, but the rebuilt result answers ``note``."""
    from types import SimpleNamespace

    from matrx_ai.db._conversation_rebuild_impl import _rebuild_tool_result_content

    row = SimpleNamespace(
        call_id="call-w60", tool_name=DOOR, output='{"status": "applied"}', is_error=False,
        output_chars=21, output_preview=None, model_stub_at=None,
        metadata={"on_screen_redirect": {"from_tool": "note:patch", "answers_name": "note"}},
    )
    plain = SimpleNamespace(**{**row.__dict__, "metadata": {}})
    assert _rebuild_tool_result_content([row])[0]["name"] == "note"
    assert _rebuild_tool_result_content([plain])[0]["name"] == DOOR


# ── REVIEW-C105: the card is the call the model made, never a part of it ────────────────────
# The redirect used to fire for ANY census writer carrying a find/replace pair and the on-screen id
# ANYWHERE in its arguments, silently dropping every other argument. It now fires only when the
# on-screen id is the call's own top-level subject and the pair is the only edit-bearing argument.


async def test_a_patch_that_also_renames_the_note_is_refused_not_sent_as_a_partial_card(
    executor, app_metadata, note_tool, door
) -> None:
    _arm(app_metadata)
    _content, result = await executor.execute(
        "note", {**_patch(ON_SCREEN), "title": "Oakland routing"}, _ctx(), client_tools=frozenset({DOOR})
    )
    assert door == [], "the card dropped the title the model asked for"
    assert note_tool == []
    assert result.error is not None and result.error.error_type == "record_on_screen"


@pytest.mark.parametrize("flag", [{"regex": True}, {"case_sensitive": False}, {"ignore_case": True}])
async def test_a_patch_with_a_match_flag_is_refused_not_sent_as_an_exact_card(
    executor, app_metadata, note_tool, door, flag
) -> None:
    _arm(app_metadata)
    _content, result = await executor.execute(
        "note", {**_patch(ON_SCREEN), **flag}, _ctx(), client_tools=frozenset({DOOR})
    )
    assert door == [], f"the card dropped the match flag {flag}"
    assert note_tool == []
    assert result.error is not None and result.error.error_type == "record_on_screen"


def test_a_call_whose_subject_is_not_the_on_screen_record_is_never_a_card_for_it() -> None:
    """data:update naming the on-screen note only inside items[] (not as its subject), and a call
    on another note that merely mentions the on-screen id, are refused, never a card patching it."""
    metadata: dict[str, Any] = {}
    _arm(metadata)
    nested = {
        "action": "update",
        "items": [{"id": ON_SCREEN}],
        "search_text": "Routing line: Los Angeles",
        "replacement_text": "Routing line: Port of Oakland",
    }
    assert on_screen_surface_redirect("data", nested, metadata) is None
    assert guarded_write_refusal("data", nested, metadata) is not None
    mentions = {**_patch(OTHER), "replacement_text": f"see note {ON_SCREEN}"}
    assert on_screen_surface_redirect("note", mentions, metadata) is None
    # The plain patch on the on-screen subject (and the data tool's own subject) still goes to the card.
    assert on_screen_surface_redirect("note", _patch(ON_SCREEN), metadata) is not None
    data_patch = {
        "action": "patch",
        "resource_type": "note",
        "id": ON_SCREEN,
        "search_text": "a",
        "replacement_text": "b",
    }
    assert on_screen_surface_redirect("data", data_patch, metadata) is not None
    # An optional field echoed as null carries nothing.
    assert on_screen_surface_redirect("note", {**_patch(ON_SCREEN), "title": None}, metadata) is not None


async def test_the_card_is_marked_requires_person_for_the_page(
    executor, app_metadata, note_tool, registry, monkeypatch
) -> None:
    """Q-05 minor: the page applies apply_surface_write per the target's policy; the redirected
    call carries ``requires_person`` so an "auto" target still asks the person."""
    registry.ensure_registered(DOOR, description="page write", parameters={})
    seen: list[Any] = []

    async def fake_delegate(tool_def, args, ctx, row_id="", authorization_metadata=None):
        seen.append(authorization_metadata)
        return ToolResult(success=False, delegated_pending=True, tool_name=tool_def.name, call_id=ctx.call_id)

    monkeypatch.setattr(executor, "_execute_delegated", fake_delegate)
    _arm(app_metadata)
    await executor.execute("note", _patch(ON_SCREEN), _ctx(), client_tools=frozenset({DOOR}))
    assert len(seen) == 1 and seen[0] is not None
    assert seen[0].get("requires_person") is True and seen[0].get("on_screen_redirect") is True
