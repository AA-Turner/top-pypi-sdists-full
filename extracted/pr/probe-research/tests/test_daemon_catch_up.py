"""A session's first worker on history it did not see happen (daemon cost round 6):
switched on late, or an old session resumed after the daemon became the default.
Only the last `CATCH_UP_S` before the newest event is new; older events are
context (no notice: the writer's divider already says so), and the reader starts
at the current turn.
Also the reader's file changes: a header line, the body one `session` away.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

pytest.importorskip("pydantic_ai")

from probe.daemon import bite as bite_mod  # noqa: E402
from probe.daemon import store as store_mod  # noqa: E402
from probe.daemon import worker as worker_mod  # noqa: E402
from probe.daemon.events import Kind  # noqa: E402

SID = "11111111-2222-3333-4444-555555555555"
NOW = datetime(2026, 10, 14, 12, 0, tzinfo=timezone.utc)


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "no-config.json"))
    monkeypatch.delenv("PROBE_DAEMON_KEY", raising=False)
    monkeypatch.setenv("PROBE_DAEMON_MCP", "0")
    monkeypatch.delenv(worker_mod.ENV_CATCH_UP_S, raising=False)
    (tmp_path / "state" / "probe" / "sessions").mkdir(parents=True)
    (tmp_path / "state" / "probe" / "sessions" / f"{SID}.state").write_text("daemon")


def _stamp(at: datetime) -> str:
    return at.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def _turn(prompt: str, answer: str, at: datetime, cwd: Path) -> str:
    lines = [
        {"type": "user", "timestamp": _stamp(at), "cwd": str(cwd), "message": {"content": prompt}},
        {"type": "assistant", "timestamp": _stamp(at + timedelta(minutes=1)),
         "message": {"content": [{"type": "text", "text": answer}]}},
        {"type": "system", "subtype": "turn_duration", "durationMs": 5, "timestamp": _stamp(at + timedelta(minutes=2))},
    ]
    return "".join(json.dumps(line) + "\n" for line in lines)


def _worker(tmp_path: Path, starts: list[datetime]) -> worker_mod.Worker:
    work = tmp_path / "home" / "work"
    work.mkdir(parents=True, exist_ok=True)
    transcript = tmp_path / f"{SID}.jsonl"
    if not transcript.exists():
        transcript.write_text("".join(_turn(f"prompt {i}", f"answer {i}", at, work) for i, at in enumerate(starts, 1)))
    return worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"))


def _bites(w: worker_mod.Worker) -> dict[int, set]:
    out: dict[int, set] = {}
    for row in w.store.db.execute("SELECT turn, bite FROM events WHERE stream = 'main'"):
        out.setdefault(int(row["turn"]), set()).add(row["bite"])
    return out


def test_an_old_sessions_history_is_context_and_the_last_two_hours_are_new(tmp_path):
    w = _worker(tmp_path, [NOW - timedelta(days=29), NOW - timedelta(days=3), NOW - timedelta(hours=1)])
    assert w.catching_up()
    assert w.read_new() > 0
    assert not w.catching_up()
    by_turn = _bites(w)
    assert by_turn[1] == {store_mod.BEFORE_DAEMON_BITE} and by_turn[2] == {store_mod.BEFORE_DAEMON_BITE}
    assert by_turn[3] == {None}  # within 2 h of the newest: the writer's to record
    pending = w.store.pending()
    assert {ev.turn for ev in pending if ev.stream == "main"} == {3}
    # No notice: one naming the skipped turns told the writer not to record the current turn.
    assert not [ev for ev in pending if ev.stream == "daemon"]
    # The reader starts at the current turn, never the history.
    assert int(w.store.fact("read_cursor")) == w.store.first_seq_of_turn(3) - 1
    # Covered, not hidden: the writer's view and `session` still have it.
    assert any(ev.turn == 1 for ev in w.store.events_between(1, None, recorded=True))


def test_a_session_the_worker_starts_with_is_not_touched(tmp_path):
    w = _worker(tmp_path, [NOW - timedelta(minutes=30), NOW - timedelta(minutes=10)])
    w.read_new()
    assert not w.catching_up()
    assert all(bites == {None} for bites in _bites(w).values())
    assert not [ev for ev in w.store.pending() if ev.stream == "daemon"]
    assert w.store.fact("read_cursor") is None


def test_nothing_runs_until_the_whole_history_is_read(tmp_path, monkeypatch):
    monkeypatch.setattr(worker_mod, "READ_CHUNK_BYTES", 300)
    w = _worker(tmp_path, [NOW - timedelta(days=5), NOW - timedelta(days=2), NOW - timedelta(minutes=5)])
    w.read_new()
    assert w.catching_up() and w.stream_behind["main"]
    assert "reading the history" in (w._bite_blocked() or "")
    assert not any(store_mod.BEFORE_DAEMON_BITE in bites for bites in _bites(w).values())
    for _ in range(50):
        if not w.catching_up():
            break
        w.read_new()
    assert not w.catching_up()
    assert _bites(w)[1] == {store_mod.BEFORE_DAEMON_BITE} and _bites(w)[3] == {None}


def test_a_restarted_worker_does_not_judge_again(tmp_path):
    starts = [NOW - timedelta(days=4), NOW - timedelta(minutes=20)]
    first = _worker(tmp_path, starts)
    first.read_new()
    marked = first.store.db.execute("SELECT count(*) AS n FROM events WHERE bite = ?",
                                    (store_mod.BEFORE_DAEMON_BITE,)).fetchone()["n"]
    first.store.db.close()
    again = _worker(tmp_path, starts)
    assert not again.catching_up()
    again.read_new()
    assert again.store.db.execute("SELECT count(*) AS n FROM events WHERE bite = ?",
                                  (store_mod.BEFORE_DAEMON_BITE,)).fetchone()["n"] == marked
    assert {ev.turn for ev in again.store.pending() if ev.stream == "main"} == {2}


def test_the_window_is_configurable(tmp_path, monkeypatch):
    monkeypatch.setenv(worker_mod.ENV_CATCH_UP_S, str(10 * 24 * 3600))
    w = _worker(tmp_path, [NOW - timedelta(days=5), NOW - timedelta(minutes=5)])
    w.read_new()
    assert all(bites == {None} for bites in _bites(w).values())


def _file_event(text: str) -> store_mod.StoredEvent:
    return store_mod.StoredEvent(seq=7, event_id="folders:7:0", stream="folders", kind=Kind.FILE_CHANGE, turn=2,
                                 ts=None, noticed=0.0, text=text, tool=None, call_id=None, command=None,
                                 is_error=False, side_file=None, chars=len(text), bite=None, offset=7)


def test_a_file_change_is_its_first_line_for_reader_and_writer_alike():
    """One render for both daemons (swarm friction T17, R40): the writer no longer
    gets the diff either; it opens the event when it cares."""
    diff = "changed /w/train.py (1,200 -> 1,350 bytes)\n@@ -1 +1 @@\n-lr = 1e-3\n+lr = 3e-4"
    ev = _file_event(diff)
    shown = bite_mod.render(ev)
    assert shown == ("[file changed · folders:7:0] changed /w/train.py (1,200 -> 1,350 bytes) · 3 more lines: "
                     "session op=open event_id=folders:7:0")
    long = _file_event("changed /w/train.log (10 -> 9,000 bytes)\n" + "step 1 loss 0.5\n" * 400)
    assert len(bite_mod.render(long)) <= bite_mod.shown_chars(long) < 200
    bare = _file_event("new file /w/empty.txt (0 bytes)")
    assert bite_mod.render(bare) == "[file changed · folders:7:0] new file /w/empty.txt (0 bytes)"


def test_one_long_turn_starts_the_reader_at_the_first_new_event(tmp_path):
    """A 24/7 agent's one prompt began days ago: the reader starts where the new
    events start, never back at that prompt (it would read the history a window
    every 30 minutes)."""
    work = tmp_path / "home" / "work"
    work.mkdir(parents=True)
    start = NOW - timedelta(days=3)
    lines = [{"type": "user", "timestamp": _stamp(start), "cwd": str(work), "message": {"content": "run forever"}}]
    for hours in (0.5, 30, 60, 71.5, 71.9):
        lines.append({"type": "assistant", "timestamp": _stamp(start + timedelta(hours=hours)),
                      "message": {"content": [{"type": "text", "text": f"progress at {hours} h"}]}})
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text("".join(json.dumps(line) + "\n" for line in lines))
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"))
    w.read_new()
    first_new = w.store.first_uncovered_seq()
    assert [ev.text for ev in w.store.pending()] == ["progress at 71.5 h", "progress at 71.9 h"]
    assert int(w.store.fact("read_cursor")) == first_new - 1


def _old_helper_logs(transcript: Path, count: int = 2, lines: int = 50) -> None:
    """Helper-agent logs from 29 days ago: read after the main chat's chunk, so
    their events get seqs after the current turn's."""
    sub = transcript.with_suffix("") / "subagents"
    sub.mkdir(parents=True)
    for n in range(count):
        body = [{"type": "assistant", "timestamp": _stamp(NOW - timedelta(days=29, seconds=-i)),
                 "message": {"content": [{"type": "text", "text": f"OLD HELPER {n} LINE {i}"}]}} for i in range(lines)]
        (sub / f"agent-{n}.jsonl").write_text("".join(json.dumps(line) + "\n" for line in body))


def test_old_helper_agent_lines_are_never_shown_as_new(tmp_path, monkeypatch):
    """Review (#2853, critical): a span of new events reached across the old helper
    lines (higher seqs), and every bite render showed them below the divider."""
    work = tmp_path / "home" / "work"
    work.mkdir(parents=True)
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text("".join(_turn(f"prompt {i}", f"answer {i}", at, work) for i, at in
                                  enumerate([NOW - timedelta(days=29), NOW - timedelta(minutes=30)], 1)))
    _old_helper_logs(transcript)
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"))
    w.read_new()
    assert not [ev for ev in w.store.pending() if ev.stream.startswith("subagent:")]  # markers included
    # The live turn goes on after the catch-up: the next span covers the old lines' seqs.
    with transcript.open("a") as handle:
        handle.write(json.dumps({"type": "assistant", "timestamp": _stamp(NOW),
                                 "message": {"content": [{"type": "text", "text": "still working"}]}}) + "\n")
    w.read_new()
    first, last = bite_mod.cover(w.store)
    assert any(ev.bite == store_mod.BEFORE_DAEMON_BITE for ev in w.store.events_between(first, last))
    nxt = bite_mod.build_next(w.store, trigger="t", instructions="")
    assert "still working" in nxt.prompt and "OLD HELPER" not in nxt.prompt
    fresh = bite_mod.build(w.store, trigger="t", context_line="", pending_lines=[], recent_writes=[])
    assert "OLD HELPER" not in fresh.prompt.split(bite_mod.DIVIDER, 1)[1]
    assert not [ev for ev in w.store.events_between(first, last, recorded=True, new=True)
                if ev.bite == store_mod.BEFORE_DAEMON_BITE]
    # Nor in the reader's windows (the oldest, and the newest with prompt wakes off),
    # nor as a reason to wake it.
    from probe.daemon import model as model_mod
    from probe.daemon import reader_lane as rl

    reader = rl.ReaderLane(w)
    assert not [ev for ev in reader.new_events() if ev.bite == store_mod.BEFORE_DAEMON_BITE]
    monkeypatch.setenv(model_mod.ENV_READER_PROMPT_WAKE, "off")
    newest = reader.next_window()
    assert newest and not [ev for ev in newest if ev.bite == store_mod.BEFORE_DAEMON_BITE]


def test_a_stream_rewritten_mid_catch_up_does_not_stall_it(tmp_path, monkeypatch):
    """Review (#2853, high): a stream left "behind" by an early return kept the
    catch-up (and every bite and reader turn) waiting for the worker's life."""
    monkeypatch.setattr(worker_mod, "READ_CHUNK_BYTES", 300)
    w = _worker(tmp_path, [NOW - timedelta(days=5), NOW - timedelta(days=2), NOW - timedelta(minutes=5)])
    w.read_new()
    assert w.catching_up() and w.stream_behind["main"]
    w.session.transcript.write_text(_turn("rewritten", "short", NOW, w.session.cwd)[:150] + "\n")
    for _ in range(5):
        w.read_new()
    assert not w.catching_up()


def test_a_large_sdk_inbox_is_read_before_the_judgment(tmp_path, monkeypatch):
    """Review (#2853, medium): the inbox was read a chunk a poll but never counted
    as behind, so its later (older) messages were judged new."""
    monkeypatch.setattr(worker_mod, "READ_CHUNK_BYTES", 400)
    w = _worker(tmp_path, [NOW - timedelta(days=5), NOW - timedelta(minutes=5)])
    inbox = worker_mod.inbox_path(SID)
    inbox.parent.mkdir(parents=True, exist_ok=True)
    msgs = [{"event": "run started", "run_id": f"r{i}", "session_id": SID, "name": "x" * 120,
             "received_at": (NOW - timedelta(days=4)).timestamp()} for i in range(10)]
    inbox.write_text("".join(json.dumps(m) + "\n" for m in msgs))
    for _ in range(40):  # every chunk of both streams
        w.read_new()
    assert not w.catching_up()
    assert len([ev for ev in w.store.events_between(1) if ev.stream == "sdk"]) == 10
    assert not [ev for ev in w.store.pending() if ev.stream == "sdk"]


def test_an_ask_is_answered_while_the_history_is_read(tmp_path, monkeypatch):
    """Review (#2853, medium): an ask waited for the whole catch-up (up to minutes
    on a large transcript, against its 10-minute timeout)."""
    from probe.daemon import reader_lane as rl

    monkeypatch.setattr(worker_mod, "READ_CHUNK_BYTES", 300)
    w = _worker(tmp_path, [NOW - timedelta(days=5), NOW - timedelta(days=2), NOW - timedelta(minutes=5)])
    w.read_new()
    assert w.catching_up()
    reader = rl.ReaderLane(w)
    assert reader.due() is None  # no unasked turn on the history
    with w.store.tx():
        w.store.add_read_ask("a1", "what did the team try?", NOW.timestamp(), False)
    assert reader.due() == "ask"


def test_a_helper_log_deleted_mid_catch_up_does_not_stall_it(tmp_path, monkeypatch):
    """Review (#2853, second pass): a helper log that vanished while "behind" was
    never read again, so its flag kept the catch-up waiting."""
    monkeypatch.setattr(worker_mod, "READ_CHUNK_BYTES", 600)
    work = tmp_path / "home" / "work"
    work.mkdir(parents=True)
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text(_turn("prompt", "answer", NOW - timedelta(minutes=5), work))
    _old_helper_logs(transcript, count=1, lines=40)
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "claude_code", home=tmp_path / "home"))
    w.read_new()
    assert w.catching_up() and w.stream_behind.get("subagent:agent-0")
    (transcript.with_suffix("") / "subagents" / "agent-0.jsonl").unlink()
    w.read_new()
    assert not w.catching_up()
