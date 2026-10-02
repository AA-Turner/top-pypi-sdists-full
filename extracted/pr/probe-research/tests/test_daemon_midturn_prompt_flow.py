"""What a prompt typed while the Claude Code agent works does downstream.

The adapter reads it as a PROMPT (test_daemon_claude_code_queued.py). A PROMPT on
the main stream opens a daemon turn, so a correction inside one agent turn:
ends the writer's bite just before it (the bite after starts with it), wakes the
reader, and counts toward an unasked message going stale.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

from probe.daemon import bite as bite_mod
from probe.daemon import lease, mailbox
from probe.daemon import worker as worker_mod
from probe.daemon.events import Event, Kind

SID = "11111111-2222-3333-4444-555555555555"
TS = "2026-09-29T04:00:00.000Z"
HUMAN = {"kind": "human"}


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    """No real config (so no real key), no MCP: nothing leaves the box."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "no-config.json"))
    monkeypatch.delenv("PROBE_DAEMON_KEY", raising=False)
    monkeypatch.setenv("PROBE_DAEMON_MCP", "0")
    monkeypatch.delenv(worker_mod.ENV_MODE, raising=False)
    monkeypatch.delenv(mailbox.ENV_READS, raising=False)
    (tmp_path / "state" / "probe" / "sessions").mkdir(parents=True)
    (lease.sessions_dir() / f"{SID}.state").write_text("daemon")


def _line(obj: dict) -> str:
    return json.dumps(obj) + "\n"


def _call(n: int) -> list[str]:
    return [
        _line({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "id": f"t{n}", "name": "Bash", "input": {"command": f"python train.py --step {n}"}}]}}),
        _line({"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": f"t{n}", "content": "ok"}]}}),
    ]


def _worker(tmp_path: Path, lines: list[str], *, clock=time.time) -> worker_mod.Worker:
    work = tmp_path / "home" / "work"
    work.mkdir(parents=True, exist_ok=True)
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text("".join(
        [_line({"type": "permission-mode", "permissionMode": "default"}),
         _line({"type": "user", "message": {"content": "sweep lr for the MLP on digits"}, "cwd": str(work)})]
        + lines))
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"),
                          clock=clock)
    w.read_new()
    return w


def _correction(text: str = "stop, use lr 1e-4 instead") -> str:
    return _line({"type": "attachment", "timestamp": TS, "isSidechain": False, "attachment": {
        "type": "queued_command", "prompt": text, "commandMode": "prompt", "origin": HUMAN, "timestamp": TS}})


TURN_END = _line({"type": "system", "subtype": "turn_duration", "durationMs": 5})


def test_a_mid_turn_prompt_opens_a_daemon_turn_inside_the_agents_turn(tmp_path):
    w = _worker(tmp_path, _call(1) + [_correction()] + _call(2) + [TURN_END])
    events = w.store.events_between(1)
    prompts = [e for e in events if e.kind == Kind.PROMPT]
    assert [p.text for p in prompts] == ["sweep lr for the MLP on digits", "stop, use lr 1e-4 instead"]
    assert [p.turn for p in prompts] == [1, 2]
    [end] = [e for e in events if e.kind == Kind.TURN_END]
    assert end.turn == 2, "the agent's one turn ends the second daemon turn"
    before = [e for e in events if e.seq < prompts[1].seq]
    assert {e.turn for e in before} == {1}


def test_a_log_read_again_from_0_does_not_move_the_turn(tmp_path):
    """A rewritten chat log is read again from offset 0 (`Worker._read_stream`):
    the prompts already stored must not open turns again, or every event after
    them, and every unasked message's age, would be off."""
    w = _worker(tmp_path, _call(1) + [_correction()] + _call(2))
    assert w.store.current_turn() == 2
    again = []
    offset = 0
    adapter = w.adapter
    for raw in w.session.transcript.read_bytes().splitlines(keepends=True):
        offset += len(raw)
        again += adapter.parse_bytes(raw.rstrip(b"\n"), stream="main", offset=offset)
    later = Event(kind=Kind.AGENT_TEXT, stream="main", offset=offset + 1, text="lr 1e-4 wins")
    with w.store.tx():
        assert w.store.add([*again, later]) == 1
    assert w.store.current_turn() == 2
    assert w.store.events_between(1)[-1].turn == 2


def test_the_writers_bite_ends_before_the_correction_and_the_next_one_starts_with_it(tmp_path):
    now = [1000.0]
    w = _worker(tmp_path, _call(1) + [_correction()] + _call(2), clock=lambda: now[0])
    assert w.due() == "prompt", "the correction wakes the writer for what came before it"
    first, last = bite_mod.cover(w.store)
    covered = w.store.events_between(first, last)
    assert covered[-1].kind == Kind.TOOL_OUTPUT and all(e.turn == 1 for e in covered)
    w.store.mark_covered(w.store.open_bite("prompt", first, last), last)

    pending = w.store.pending()
    assert pending[0].kind == Kind.PROMPT and pending[0].text == "stop, use lr 1e-4 instead"
    assert w.due() is None, "a correction at the head of the queue waits, like any prompt"
    now[0] += worker_mod.DUE_AFTER_S
    assert w.due() == "age"
    first2, _ = bite_mod.cover(w.store)
    assert w.store.events_between(first2, first2)[0].text == "stop, use lr 1e-4 instead"


def test_the_writer_is_due_at_the_turn_end_after_a_correction(tmp_path):
    w = _worker(tmp_path, _call(1) + [_correction()] + _call(2) + [TURN_END], clock=lambda: 1000.0)
    first, last = bite_mod.cover(w.store)
    w.store.mark_covered(w.store.open_bite("prompt", first, last), last)
    assert w.due() == "turn end"


@pytest.fixture
def reader():
    """A reader lane for a worker, its model answering nothing (the reader needs
    pydantic_ai; the writer-side tests above run without it, as CI installs them)."""
    pytest.importorskip("pydantic_ai")
    from pydantic_ai.messages import ModelResponse
    from pydantic_ai.models.function import FunctionModel

    from probe.daemon import reader_lane

    return lambda w: reader_lane.ReaderLane(w, model=FunctionModel(lambda messages, info: ModelResponse(parts=[])))


def test_the_reader_wakes_on_a_mid_turn_prompt(tmp_path, reader):
    w = _worker(tmp_path, _call(1), clock=lambda: 1000.0)
    lane = reader(w)
    with w.store.tx():
        w.store.set_fact("read_cursor", w.store.events_between(1)[-1].seq)
    lane.last_turn_at = 1000.0
    assert lane.due() is None
    with w.session.transcript.open("a") as handle:
        handle.write(_correction())
    w.read_new()
    assert lane.due() == "prompt"


def _unasked(w) -> None:
    mailbox.publish(mailbox.Message(id=mailbox.new_message_id(), session=SID, kind=mailbox.Kind.MESSAGE,
                                    text="digits-mlp already swept lr 1e-2..1e-4", made_at=time.time(),
                                    origin_turn=w.store.current_turn()))


def _waiting() -> list:
    return [m for _, m in mailbox.waiting(SID)]


def test_an_unasked_message_outlives_one_correction_and_goes_stale_after_two(tmp_path, reader):
    w = _worker(tmp_path, _call(1))
    lane = reader(w)
    _unasked(w)
    for expect_kept, text in ((True, "use lr 1e-4"), (False, "no, 3e-4")):
        with w.session.transcript.open("a") as handle:
            handle.write(_correction(text))
        w.read_new()
        lane.drop_stale_unasked()
        assert bool(_waiting()) is expect_kept, text
