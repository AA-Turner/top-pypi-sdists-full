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
    output_is_person_decline,
)
from matrx_ai.tools.registry import ToolRegistry

ON_SCREEN = "59678b3b-3620-442d-872b-0331ac74a1cf"
OTHER = "0b8c2d55-6f7e-4a1b-9c3d-2e4f5a6b7c8d"


class _NullEmitter:
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
        {ON_SCREEN: {"resource_type": "note", "surface": "matrx-user/notes", "targets": ["note_content"]}},
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
