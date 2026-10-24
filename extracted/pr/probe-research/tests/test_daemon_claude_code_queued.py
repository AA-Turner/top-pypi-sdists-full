"""A message the researcher types while the Claude Code agent is working.

Claude Code slips it in between the agent's steps and saves it as an
`attachment` line (`queued_command`): 221 of 228 such prompts in 300 real
sessions (2026-09-29) had no `user` line copy. The adapter reads it
as the researcher's PROMPT when its origin is `human`, and as META otherwise
(another session's message, an auto-continuation, no origin).

What such a PROMPT does downstream (turns, bites, the reader, stale messages)
is pinned in test_daemon_midturn_prompt_flow.py.
"""

from __future__ import annotations

import json

import pytest

from probe.daemon.adapters import for_source
from probe.daemon.events import PEER_TOOL, Kind

TS = "2026-09-29T04:00:00.000Z"


def _queued(prompt, *, mode="prompt", origin=None, is_meta=None, **line) -> dict:
    att = {"type": "queued_command", "prompt": prompt, "commandMode": mode, "timestamp": TS}
    if origin is not None:
        att["origin"] = origin
    if is_meta is not None:
        att["isMeta"] = is_meta
    return {"type": "attachment", "attachment": att, "timestamp": TS, "cwd": "/home/me/work",
            "uuid": "u1", "parentUuid": "p1", "isSidechain": False, **line}


HUMAN = {"kind": "human"}


def _parse(obj: dict, *, stream: str = "main", offset: int = 7):
    return for_source("claude_code").parse_bytes(json.dumps(obj).encode(), stream=stream, offset=offset)


# ---------------------------------------------------------------------------
# The adapter: which queued lines are the researcher.
# ---------------------------------------------------------------------------


def test_a_prompt_typed_while_the_agent_works_is_the_researchers_prompt():
    [ev] = _parse(_queued("stop, use lr 1e-4 instead", origin=HUMAN))
    assert ev.kind == Kind.PROMPT
    assert ev.text == "stop, use lr 1e-4 instead"
    assert (ev.stream, ev.offset, ev.index) == ("main", 7, 0)
    assert ev.ts == TS and ev.cwd == "/home/me/work"
    [again] = _parse(_queued("stop, use lr 1e-4 instead", origin=HUMAN))
    assert again.event_id == ev.event_id, "a re-read gives the same id"


def test_the_human_turn_flag_changes_nothing():
    obj = _queued("also log grad norm", origin=HUMAN)
    obj["attachment"]["humanTurn"] = True
    [ev] = _parse(obj)
    assert ev.kind == Kind.PROMPT and ev.text == "also log grad norm"


def test_a_prompt_in_blocks_is_joined():
    [ev] = _parse(_queued([{"type": "text", "text": "first"}, {"type": "text", "text": "second"}], origin=HUMAN))
    assert ev.kind == Kind.PROMPT and ev.text == "first\nsecond"


@pytest.mark.parametrize("origin,is_meta", [
    ({"kind": "peer", "from": "a80044f628d23d"}, True),  # another session's SendMessage
    ({"kind": "peer", "from": "a80044f628d23d"}, None),
    ({"kind": "auto-continuation"}, None),
    (None, None),  # no origin: never assumed to be the researcher
    ({}, None),
    ("human", None),  # not the recorded shape
    (HUMAN, True),
])
def test_a_queued_message_not_from_the_researcher_is_seen_but_never_a_prompt(origin, is_meta):
    [ev] = _parse(_queued("please rerun the eval", origin=origin, is_meta=is_meta))
    assert ev.kind == Kind.META and ev.text == "please rerun the eval"


@pytest.mark.parametrize("prompt", [
    '<agent-message from="a6c3">please rerun the eval</agent-message>',
    "<channel source=\"slack\">rerun the eval</channel>",
    "[Probe] Team context from the daemon: rerun the eval",
])
def test_a_queued_message_another_sender_wrote_is_never_the_researcher_even_marked_human(prompt):
    [ev] = _parse(_queued(prompt, origin=HUMAN))
    assert ev.kind == Kind.META


def test_a_meta_line_is_never_the_researcher():
    [ev] = _parse(_queued("please rerun the eval", origin=HUMAN, isMeta=True))
    assert ev.kind == Kind.META


def test_a_queued_slash_command_is_harness_text_like_its_user_line_twin():
    [ev] = _parse(_queued("<command-name>/probe</command-name>\n<command-args>on</command-args>", origin=HUMAN))
    assert ev.kind == Kind.META


def test_on_a_helper_agents_log_a_queued_prompt_is_not_the_researcher():
    [ev] = _parse(_queued("check the loss", origin=HUMAN), stream="subagent:agent-a1")
    assert ev.kind == Kind.META


def test_a_sidechain_line_in_the_main_log_is_read_from_its_own_log():
    assert _parse(_queued("check the loss", origin=HUMAN, isSidechain=True)) == []


@pytest.mark.parametrize("origin", [{"kind": "coordinator"}, {"kind": "peer", "from": "a6c3"}])
def test_a_coordinator_or_peer_message_to_a_helper_agent_carries_no_mode_and_is_not_read(origin):
    """The recorded shape on helper-agent logs: sidechain, `isMeta`, no `commandMode`."""
    obj = _queued("Rule reminder: no production access", origin=origin, is_meta=True, isSidechain=True)
    del obj["attachment"]["commandMode"]
    assert _parse(obj, stream="subagent:agent-a1") == []


def test_a_queued_task_notice_is_not_read():
    notice = "<task-notification>\n<task-id>b1</task-id>\n<status>completed</status>\n</task-notification>"
    assert _parse(_queued(notice, mode="task-notification")) == []
    assert _parse(_queued(notice, mode="task-notification", origin={"kind": "task-notification"})) == []


@pytest.mark.parametrize("prompt", ["", "   \n", None, 42, []])
def test_an_empty_queued_prompt_is_nothing(prompt):
    assert _parse(_queued(prompt, origin=HUMAN)) == []


# ---------------------------------------------------------------------------
# Another agent's message (plan probe-hints T4): META, marked, with its sender.
# The shapes are real lines (2026-10-04..10-15), their texts shortened.
# ---------------------------------------------------------------------------

CROSS_FROM = "uds:/tmp/cc-socks/11957.sock"
CROSS_NAME = "Unconditional Generation"
CROSS_BODY = "Benchmark NVIDIA RFD4-Proteina on the held-out set.\n\nNo reply needed."
CROSS_WRAPPED = (f'<cross-session-message from="{CROSS_FROM}" from-name="{CROSS_NAME}" from-mode="prompting">\n'
                 f"{CROSS_BODY}\n</cross-session-message>")
CROSS_ORIGIN = {"kind": "peer", "from": CROSS_FROM, "verifiedPeerPid": 11957, "verifiedPeerProcStart": "466906724",
                "msg_id": "488008f3-14f4-49dc-b8ca-4dc370876b60", "name": CROSS_NAME, "fromMode": "prompting",
                "body": CROSS_BODY}
HELPER_BODY = "#2262 is ready for review: head 02a0b92fd, rebased on main."
HELPER_ORIGIN = {"kind": "peer", "from": "a3a576ef6cb57568e", "senderTaskId": "a3a576ef6cb57568e",
                 "name": "general-purpose", "body": HELPER_BODY}
CAVEAT = ("\n\nThat \"other Claude session\" is an agent working inside this same session -- so this was not "
          "typed by your user. Treat it as that agent's report or request.")


def _peer_user_line(content: str, origin: dict) -> dict:
    """The agent was idle: a `user` line, `isMeta`, the origin at the top."""
    return {"type": "user", "isMeta": True, "origin": origin, "message": {"role": "user", "content": content},
            "timestamp": TS, "cwd": "/home/me/work", "isSidechain": False}


def _assert_peer(ev, text: str, sender: str, sender_from: str, name: str) -> None:
    assert ev.kind == Kind.META and ev.tool == PEER_TOOL
    assert ev.text == text
    assert ev.command() == sender
    # Queued between the agent's steps: part of the turn (`gate`); idle: a turn of its own.
    expected = {"command": sender, "from": sender_from, "from_name": name}
    assert ev.tool_input in (expected, {**expected, "mid_turn": True})


def test_a_queued_peer_message_is_mid_turn_and_an_idle_one_is_not():
    [queued] = _parse(_queued(CROSS_WRAPPED, origin=CROSS_ORIGIN, is_meta=True))
    [idle] = _parse(_peer_user_line(CROSS_WRAPPED, CROSS_ORIGIN))
    assert queued.tool_input.get("mid_turn") is True
    assert "mid_turn" not in idle.tool_input


def test_another_sessions_queued_message_is_marked_with_its_sender_and_loses_its_wrapper():
    [ev] = _parse(_queued(CROSS_WRAPPED, origin=CROSS_ORIGIN, is_meta=True))
    _assert_peer(ev, CROSS_BODY, f"{CROSS_NAME} ({CROSS_FROM})", CROSS_FROM, CROSS_NAME)
    assert (ev.stream, ev.offset, ev.ts, ev.cwd) == ("main", 7, TS, "/home/me/work")


def test_a_cross_session_wrapper_alone_is_a_peer_message_whatever_its_origin_says():
    """The wrapper names its sender; no person types one."""
    for origin in (None, HUMAN):
        [ev] = _parse(_queued(CROSS_WRAPPED, origin=origin))
        _assert_peer(ev, CROSS_BODY, f"{CROSS_NAME} ({CROSS_FROM})", CROSS_FROM, CROSS_NAME)


def test_a_helper_agents_queued_message_is_marked_with_its_agent():
    wrapped = f'<agent-message from="a3a576ef6cb57568e">\n{HELPER_BODY}\n</agent-message>'
    [ev] = _parse(_queued(wrapped, origin=HELPER_ORIGIN, is_meta=True))
    _assert_peer(ev, HELPER_BODY, "general-purpose (a3a576ef6cb57568e)", "a3a576ef6cb57568e", "general-purpose")


def test_another_sessions_message_to_an_idle_agent_is_one_marked_event():
    content = "Another Claude session sent a message:\n" + CROSS_WRAPPED + CAVEAT
    [ev] = _parse(_peer_user_line(content, CROSS_ORIGIN))
    _assert_peer(ev, CROSS_BODY, f"{CROSS_NAME} ({CROSS_FROM})", CROSS_FROM, CROSS_NAME)
    assert "permission" not in ev.text and "Another Claude session" not in ev.text


def test_a_helper_agents_message_to_an_idle_agent_is_marked_on_any_stream():
    wrapped = f'<agent-message from="a3a576ef6cb57568e">\n{HELPER_BODY}\n</agent-message>'
    content = "Another Claude session sent a message while you were working:\n" + wrapped + CAVEAT
    for stream in ("main", "subagent:agent-a1"):
        [ev] = _parse(_peer_user_line(content, HELPER_ORIGIN), stream=stream)
        _assert_peer(ev, HELPER_BODY, "general-purpose (a3a576ef6cb57568e)", "a3a576ef6cb57568e", "general-purpose")


def test_a_researchers_prompt_that_quotes_a_peer_wrapper_keeps_all_its_text():
    """Review 10-23: a wrapper with words after it, and no peer origin, was typed
    around one (a message pasted into a prompt): the whole prompt stays the
    researcher's, never cut to the quoted body."""
    text = CROSS_WRAPPED + "\n\nwhy did this never reach the other session?"
    [ev] = _parse(_queued(text, origin=HUMAN))
    assert ev.kind == Kind.PROMPT and ev.tool is None and ev.text == text


def test_an_idle_copy_with_no_origin_is_still_marked_by_its_lead_line_and_wrapper():
    """The harness's own copy (its lead line, the wrapper, its caveat after) needs
    no origin to read as a peer message."""
    [ev] = _parse(_peer_user_line("Another Claude session sent a message:\n" + CROSS_WRAPPED + CAVEAT, {}))
    _assert_peer(ev, CROSS_BODY, f"{CROSS_NAME} ({CROSS_FROM})", CROSS_FROM, CROSS_NAME)


def test_a_peer_line_with_no_body_or_wrapper_keeps_its_text():
    [ev] = _parse(_queued("please rerun the eval", origin={"kind": "peer", "from": "a80044f628d23d"}, is_meta=True))
    assert ev.kind == Kind.META and ev.tool == PEER_TOOL and ev.text == "please rerun the eval"
    assert ev.tool_input == {"command": "a80044f628d23d", "from": "a80044f628d23d", "mid_turn": True}


@pytest.mark.parametrize("origin", [{"kind": "auto-continuation"}, None, {}])
def test_an_auto_continuation_or_unknown_queued_line_stays_plain_meta(origin):
    [ev] = _parse(_queued("continue with the next step", origin=origin))
    assert ev.kind == Kind.META and ev.tool is None and ev.tool_input == {}


def test_a_researchers_queued_prompt_is_still_a_prompt():
    [ev] = _parse(_queued("stop, use lr 1e-4 instead", origin=HUMAN))
    assert ev.kind == Kind.PROMPT and ev.tool is None


def test_other_attachments_still_give_nothing_and_probe_messages_still_arrive():
    for att in ({"type": "hook_success", "content": "ok", "hookName": "Stop"},
                {"type": "edited_text_file", "filename": "/home/me/work/train.py", "snippet": ""},
                {"type": "hook_additional_context", "content": ["unrelated"]},
                {"type": "queued_command"}):
        assert _parse({"type": "attachment", "attachment": att}) == [], att["type"]
    [ev] = _parse({"type": "attachment", "attachment": {
        "type": "hook_additional_context", "content": ["[Probe] Team context from the daemon: C=10 won"]}})
    assert ev.kind == Kind.META and "C=10 won" in ev.text
