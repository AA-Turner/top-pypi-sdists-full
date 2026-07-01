"""
Tests for the chat capture helper — verifies that every chat turn
emits the expected event spine events with correct metadata.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def isolated_spine(tmp_path, monkeypatch):
    monkeypatch.setenv("CVC_EVENTS_ROOT", str(tmp_path))
    import cvc.events.spine as spine
    if spine._file_lock_fd is not None:
        spine._release_file_lock()
    yield tmp_path


def test_chat_capture_session_start_emits_two_events():
    """session_start emits session_start + user_message."""
    from cvc.events.chat_capture import ChatCapture
    from cvc.events.spine import query

    cap = ChatCapture(
        workspace="/tmp/proj",
        channel="web",
        actor="Jai",
        session_id="s1",
        turn_id="t1",
    )
    cap.session_start(user_message="hello world")

    events = query(reverse=False)  # oldest-first for ordering checks
    assert len(events) == 2
    assert events[0]["kind"] == "chat.session_start"
    assert events[1]["kind"] == "chat.user_message"
    assert events[1]["summary"] == "hello world"
    assert events[1]["parent_event_id"] == events[0]["id"]


def test_chat_capture_tool_call_and_result():
    from cvc.events.chat_capture import ChatCapture
    from cvc.events.spine import query

    cap = ChatCapture(
        workspace="/tmp/proj",
        channel="web",
        session_id="s1",
    )
    cap.session_start(user_message="check the dev branch")
    cap.tool_call(name="terminal", call_id="c1", args={"command": "git status"})
    cap.tool_result(name="terminal", call_id="c1", output="On branch dev\nnothing to commit")

    events = query()
    kinds = [e["kind"] for e in events]
    assert "chat.tool_call" in kinds
    assert "chat.tool_result" in kinds

    tool_result = next(e for e in events if e["kind"] == "chat.tool_result")
    assert tool_result["data"]["name"] == "terminal"
    assert "On branch dev" in tool_result["data"]["output"]
    assert tool_result["status"] == "ok"


def test_chat_capture_tool_result_with_error():
    from cvc.events.chat_capture import ChatCapture
    from cvc.events.spine import query

    cap = ChatCapture(workspace="/p", channel="telegram", session_id="s1")
    cap.session_start(user_message="hi")
    cap.tool_call(name="terminal", call_id="c1", args={})
    cap.tool_result(name="terminal", call_id="c1", output="", status="err", error="command failed")

    res = next(e for e in query() if e["kind"] == "chat.tool_result")
    assert res["status"] == "err"
    assert res["error"] == "command failed"


def test_chat_capture_assistant_message_with_tokens():
    from cvc.events.chat_capture import ChatCapture
    from cvc.events.spine import query

    cap = ChatCapture(workspace="/p", channel="web", session_id="s1")
    cap.session_start(user_message="hi")
    cap.assistant_message(text="hello back", tokens_in=5, tokens_out=10)
    cap.session_end(status="ok")

    assistant = next(e for e in query() if e["kind"] == "chat.assistant_message")
    assert assistant["tokens_in"] == 5
    assert assistant["tokens_out"] == 10
    assert assistant["actor"] == "assistant"


def test_chat_capture_long_text_truncated_to_200():
    from cvc.events.chat_capture import ChatCapture
    from cvc.events.spine import query

    cap = ChatCapture(workspace="/p", session_id="s1")
    cap.session_start(user_message="x")
    cap.assistant_message(text="x" * 1000)

    assistant = next(e for e in query() if e["kind"] == "chat.assistant_message")
    assert len(assistant["summary"]) == 200


def test_chat_capture_error_event():
    from cvc.events.chat_capture import ChatCapture
    from cvc.events.spine import query

    cap = ChatCapture(workspace="/p", session_id="s1")
    cap.session_start(user_message="hi")
    cap.error(message="something broke")

    err = next(e for e in query() if e["kind"] == "chat.error")
    assert err["status"] == "err"
    assert err["error"] == "something broke"


def test_chat_capture_session_end_with_status():
    from cvc.events.chat_capture import ChatCapture
    from cvc.events.spine import query

    cap = ChatCapture(workspace="/p", session_id="s1")
    cap.session_start(user_message="hi")
    cap.session_end(status="err")

    end = next(e for e in query() if e["kind"] == "chat.session_end")
    assert end["status"] == "err"


def test_chat_capture_context_manager_records_exception():
    from cvc.events.chat_capture import ChatCapture
    from cvc.events.spine import query

    with pytest.raises(ValueError):
        with ChatCapture(workspace="/p", session_id="s1") as cap:
            cap.session_start(user_message="hi")
            raise ValueError("kaboom")

    end = next(e for e in query() if e["kind"] == "chat.session_end")
    assert end["status"] == "err"


def test_chat_capture_full_lifecycle():
    """One full turn: session_start, user_msg, tool_call, tool_result, assistant, session_end."""
    from cvc.events.chat_capture import ChatCapture
    from cvc.events.spine import query

    cap = ChatCapture(workspace="/p", channel="web", session_id="s1", turn_id="t1")
    cap.session_start(user_message="check the dev branch")
    cap.tool_call(name="terminal", call_id="c1", args={"command": "git status"})
    cap.tool_result(name="terminal", call_id="c1", output="On dev\nclean")
    cap.assistant_message(text="All clean", tokens_in=8, tokens_out=15)
    cap.session_end()

    events = query(reverse=False)
    kinds = [e["kind"] for e in events]
    assert kinds == [
        "chat.session_start",
        "chat.user_message",
        "chat.tool_call",
        "chat.tool_result",
        "chat.assistant_message",
        "chat.session_end",
    ]


def test_chat_capture_compact_args():
    """Large args get truncated; dict preserved."""
    from cvc.events.chat_capture import ChatCapture
    from cvc.events.spine import query

    cap = ChatCapture(workspace="/p", session_id="s1")
    cap.session_start(user_message="hi")
    cap.tool_call(
        name="terminal",
        call_id="c1",
        args={
            "command": "git log --all --oneline " + "x" * 500,  # huge
            "extra": "ok",
        },
    )

    call_evt = next(e for e in query() if e["kind"] == "chat.tool_call")
    cmd = call_evt["data"]["args"]["command"]
    assert len(cmd) <= 200


def test_chat_capture_channel_distinct():
    """Different channels produce events tagged with their channel."""
    from cvc.events.chat_capture import ChatCapture
    from cvc.events.spine import query

    for ch in ("web", "telegram", "tui"):
        cap = ChatCapture(workspace="/p", channel=ch, session_id=f"s-{ch}")
        cap.session_start(user_message="hi")

    events = query()
    channels = {e["channel"] for e in events}
    assert channels == {"web", "telegram", "tui"}