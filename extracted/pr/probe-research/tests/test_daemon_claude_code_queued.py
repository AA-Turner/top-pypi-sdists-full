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
from probe.daemon.events import Kind

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


def test_other_attachments_still_give_nothing_and_probe_messages_still_arrive():
    for att in ({"type": "hook_success", "content": "ok", "hookName": "Stop"},
                {"type": "edited_text_file", "filename": "/home/me/work/train.py", "snippet": ""},
                {"type": "hook_additional_context", "content": ["unrelated"]},
                {"type": "queued_command"}):
        assert _parse({"type": "attachment", "attachment": att}) == [], att["type"]
    [ev] = _parse({"type": "attachment", "attachment": {
        "type": "hook_additional_context", "content": ["[Probe] Team context from the daemon: C=10 won"]}})
    assert ev.kind == Kind.META and "C=10 won" in ev.text
