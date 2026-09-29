"""An earlier turn's reading of a live machine reaches the model marked STALE.

THE STATE BEFORE THIS TEST (measured live, Lanes AU3/AU4, 2026-09-26 and
2026-09-28). A Personal Staff thread never ends. Asked "what files are in my
workspace?", the Chief answered from an ``fs_list`` result turns back — five old
marker files — and missed the file it had created in turn 1. Asked to run
``uname -a``, it recited an earlier ``shell_execute`` output and ran nothing.
Nothing in the history said those results were old: an ``fs_list`` from an hour
ago read exactly like one from this turn.

WHAT MUST HOLD. On a conversation the host marks permanent, the send boundary
(resolve stage) prefixes every perishable tool result BEFORE the current turn
with ``[STALE — this is what <tool> returned at <its own time> …]``. This turn's
results, action receipts (``fs_write``) and media are untouched; the pass is
idempotent and byte-stable; a conversation the host has no opinion about is
never touched; a host door that raises costs the send nothing.
"""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from matrx_ai import _ext
from matrx_ai.config import (
    TextContent,
    ToolCallContent,
    ToolResultContent,
    UnifiedMessage,
)
from matrx_ai.config.perishable_state import (
    STALE_MARKER,
    is_perishable_tool,
    mark_perishable_state,
)
from matrx_ai.config.send_boundary import STAGE_RESOLVE, prepare_for_send

STAFF = "3af9e95c-699d-5e78-a506-736e4768273e"
ORDINARY = "11111111-2222-3333-4444-555555555555"

OLD_LISTING = "always-on-marker-1790425567.txt\nnotes.md"
OLD_UNAME = "Linux box 6.1.0 #1 SMP x86_64 GNU/Linux"


def _assistant_call(call_id: str, name: str) -> UnifiedMessage:
    return UnifiedMessage(
        role="assistant",
        content=[ToolCallContent(id=call_id, name=name, arguments={"path": "."})],
    )


def _tool(call_id: str, name: str, output, at: str | None) -> UnifiedMessage:
    return UnifiedMessage(
        role="tool",
        timestamp=at,
        content=[
            ToolResultContent(
                tool_use_id=call_id,
                call_id=call_id,
                name=name,
                content=output,
                output_chars=len(str(output)),
            )
        ],
    )


def _say(role: str, text: str) -> UnifiedMessage:
    return UnifiedMessage(role=role, content=[TextContent(text=text)])


def _thread() -> list[UnifiedMessage]:
    """Two earlier turns (a listing, a uname, a write) then the person's new text."""
    return [
        _say("user", "create a marker file"),
        _assistant_call("c-write", "fs_write"),
        _tool("c-write", "fs_write", "wrote 15 bytes to always-on-marker-1790562806.txt",
              "2026-09-28T02:33:40+00:00"),
        _say("assistant", "Done."),
        _say("user", "what files are in my workspace?"),
        _assistant_call("c-list", "fs_list"),
        _tool("c-list", "fs_list", OLD_LISTING, "2026-09-28T02:40:12+00:00"),
        _say("assistant", "You have a marker and notes.md."),
        _say("user", "run uname -a"),
        _assistant_call("c-uname", "shell_execute"),
        _tool("c-uname", "shell_execute", {"stdout": OLD_UNAME, "exit_code": 0},
              "2026-09-28T02:44:05+00:00"),
        _say("assistant", "It printed Linux."),
        # ── the current turn ──
        _say("user", "what files are in my workspace? just list the names."),
    ]


def _result(messages: list[UnifiedMessage], call_id: str) -> ToolResultContent:
    for message in messages:
        for block in message.content:
            if getattr(block, "type", None) == "tool_result" and block.call_id == call_id:
                return block
    raise AssertionError(f"no tool_result for {call_id}")


# ── the pure pass ───────────────────────────────────────────────────────────


def test_an_old_listing_and_an_old_uname_are_marked_stale_with_their_own_time() -> None:
    messages = _thread()
    report = mark_perishable_state(messages)

    listing = _result(messages, "c-list").content
    assert listing.startswith(STALE_MARKER), listing
    assert "fs_list returned at 2026-09-28 02:40 UTC" in listing
    assert "run the tool again" in listing
    assert listing.endswith(OLD_LISTING), "the reading itself stays readable"

    uname = _result(messages, "c-uname").content
    assert uname.startswith(STALE_MARKER)
    assert "shell_execute returned at 2026-09-28 02:44 UTC" in uname
    assert OLD_UNAME in uname

    assert report.blocks_marked == 2
    assert sorted(report.tools) == ["fs_list", "shell_execute"]


def test_an_action_receipt_is_not_a_reading_and_stays_as_it_was() -> None:
    messages = _thread()
    mark_perishable_state(messages)
    assert _result(messages, "c-write").content.startswith("wrote 15 bytes")


def test_this_turns_own_readings_are_the_truth_and_are_never_marked() -> None:
    messages = _thread()
    messages += [
        _assistant_call("c-now", "fs_list"),
        _tool("c-now", "fs_list", "always-on-marker-1790562806.txt", "2026-09-28T02:50:00+00:00"),
    ]
    mark_perishable_state(messages)
    assert _result(messages, "c-now").content == "always-on-marker-1790562806.txt"


def test_the_pass_is_idempotent_and_byte_stable_for_the_prompt_cache() -> None:
    messages = _thread()
    mark_perishable_state(messages)
    once = [json.dumps(m.content, default=str) for m in messages]
    second = mark_perishable_state(messages)
    assert second.blocks_marked == 0
    assert [json.dumps(m.content, default=str) for m in messages] == once

    fresh = _thread()
    mark_perishable_state(fresh)
    assert [json.dumps(m.content, default=str) for m in fresh] == once, (
        "the stamp must come from the result's own time, never 'now'"
    )


def test_pairing_fields_survive_the_rewrite() -> None:
    messages = _thread()
    mark_perishable_state(messages)
    block = _result(messages, "c-list")
    assert (block.tool_use_id, block.call_id, block.name, block.is_error) == (
        "c-list",
        "c-list",
        "fs_list",
        False,
    )


def test_rebuilt_dict_blocks_are_marked_too() -> None:
    """The DB rebuild hands dicts, not dataclasses — both shapes coexist."""
    messages = [
        _say("user", "list"),
        UnifiedMessage(
            role="tool",
            timestamp="2026-09-28T02:40:12+00:00",
            content=[{"type": "tool_result", "call_id": "d", "tool_use_id": "d",
                      "name": "fs_list", "content": OLD_LISTING}],
        ),
        _say("user", "list again"),
    ]
    mark_perishable_state(messages)
    assert messages[1].content[0]["content"].startswith(STALE_MARKER)


def test_the_census_of_perishable_tools() -> None:
    for name in ("fs_list", "fs_read", "fs_search", "shell_execute", "shell_python",
                 "browser_get_text", "cloud_browser_snapshot", "computer_screenshot"):
        assert is_perishable_tool(name), name
    for name in ("fs_write", "fs_mkdir", "fs_delete", "record_timezone", "web_search", ""):
        assert not is_perishable_tool(name), name


# ── through THE send boundary ───────────────────────────────────────────────


@pytest.fixture
def host_marks_staff(monkeypatch):
    async def _marker(*, conversation_id: str) -> bool:
        return conversation_id == STAFF

    monkeypatch.setitem(_ext._registry, "perishable_state_marker", _marker)
    return _marker


def _config(messages: list[UnifiedMessage]) -> SimpleNamespace:
    return SimpleNamespace(messages=messages, system_instruction=None, prompt_cache_key=None)


@pytest.mark.asyncio
async def test_the_staff_thread_reaches_the_model_with_old_readings_marked(host_marks_staff) -> None:
    config = _config(_thread())
    prep = await prepare_for_send(config, stage=STAGE_RESOLVE, conversation_id=STAFF)
    assert "perishable_state" in prep.steps
    assert prep.perishable_report == {"blocks_marked": 2, "tools": ["fs_list", "shell_execute"]}
    assert _result(config.messages, "c-list").content.startswith(STALE_MARKER)


@pytest.mark.asyncio
async def test_a_conversation_the_host_has_no_opinion_about_is_never_touched(host_marks_staff) -> None:
    config = _config(_thread())
    prep = await prepare_for_send(config, stage=STAGE_RESOLVE, conversation_id=ORDINARY)
    assert prep.perishable_report is None
    assert _result(config.messages, "c-list").content == OLD_LISTING


@pytest.mark.asyncio
async def test_with_no_host_matrx_ai_behaves_exactly_as_before(monkeypatch) -> None:
    monkeypatch.delitem(_ext._registry, "perishable_state_marker", raising=False)
    config = _config(_thread())
    await prepare_for_send(config, stage=STAGE_RESOLVE, conversation_id=STAFF)
    assert _result(config.messages, "c-list").content == OLD_LISTING


@pytest.mark.asyncio
async def test_a_host_door_that_raises_costs_the_send_nothing(monkeypatch, caplog) -> None:
    async def _boom(*, conversation_id: str) -> bool:
        raise RuntimeError("knob table unreachable")

    monkeypatch.setitem(_ext._registry, "perishable_state_marker", _boom)
    config = _config(_thread())
    prep = await prepare_for_send(config, stage=STAGE_RESOLVE, conversation_id=STAFF)
    assert "perishable_state" not in prep.steps
    assert "perishable_state' failed (ignored)" in caplog.text
