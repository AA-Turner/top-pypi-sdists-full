"""Probe off, in the tap itself (tap 0.10.19): `tap/capture_gate.py`.

The canonical copy is `probe.tap_core.capture_gate` (byte-identical to the
tap's, `tests/test_tap_core_sync.py`), read by `session_journal.stage` in every
process that drains a journal: a `tap watch`, the Probe service's recorders,
`probe import`. These tests drive the journal against the receipts door's fake
(`test_transcript_protocol3.DoorWire`, protocols 2 and 3) and read what a
batch carries.
"""

from __future__ import annotations

import json
import multiprocessing
import os
import threading
from pathlib import Path

import pytest

from probe.tap_core import capture_gate as tg
from probe.tap_core import session_journal as sj
from test_transcript_protocol3 import CWD, DoorWire, _journal, _session, _start, _user, _write

SID = "s-0123456789"


@pytest.fixture
def state(tmp_path, monkeypatch):
    """A private state folder and config; no override in the environment."""
    for name in ("PROBE_SESSION_STATE", "PROBE_SESSION_TRACKING", "PROBE_CONFIG_PATH"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "xdg-state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg-config"))
    sessions = tmp_path / "xdg-state" / "probe" / "sessions"
    sessions.mkdir(parents=True)
    yield sessions
    tg.host(None)


def _switch(sessions: Path, sid: str, word: str) -> None:
    (sessions / f"{sid}.state").write_text(word + "\n", encoding="utf-8")


def _events(body: bytes | None) -> list[str]:
    """The texts a batch carries (protocol 2 events, protocol 3 fragments)."""
    if body is None:
        return []
    text = json.dumps(json.loads(body))
    return [t for t in ("on-1", "on-2", "on-3", "SECRET-1", "SECRET-2", "SECRET-3", "transcript line not sent")
            if t in text]


def _drain(journal, wire, sid) -> list[bytes]:
    sent = []
    while (body := journal.stage(sid, cwd=CWD)) is not None:
        journal.deliver(sid, wire)
        sent.append(body)
    return sent


def _offsets(path: Path) -> list[int]:
    """Each line's start offset."""
    out, at = [], 0
    for raw in path.read_bytes().splitlines(keepends=True):
        out.append(at)
        at += len(raw)
    return out + [at]


# -- the switch: what `session_marker` says -------------------------------------------


@pytest.mark.parametrize("case", [
    {}, {"state": "off"}, {"state": "full"}, {"state": "read-only"}, {"state": "daemon"}, {"state": "junk"},
    {"tracking": "off"}, {"tracking": "on"}, {"off_file": True}, {"config": {"defaults": {"session_state": "off"}}},
    {"config": {"defaults": {"session_state": "disabled"}}}, {"config": {"defaults": {"session_tracking": "off"}}},
    {"config": "not json"}, {"env": {"PROBE_SESSION_STATE": "off"}}, {"env": {"PROBE_SESSION_STATE": "0"}},
    {"env": {"PROBE_SESSION_TRACKING": "off"}}, {"env": {"PROBE_SESSION_STATE": "read"}, "state": "off"},
    {"env": {"PROBE_SESSION_STATE": "off"}, "state": "full"},
])
def test_the_switch_reads_as_the_session_marker_reads_it(tmp_path, monkeypatch, case):
    from probe.sdk import session_marker

    sid = "s-" + os.urandom(6).hex()
    state_home, config_home = tmp_path / "state", tmp_path / "config"
    sessions = state_home / "probe" / "sessions"
    sessions.mkdir(parents=True)
    if case.get("state"):
        (sessions / f"{sid}.state").write_text(case["state"] + "\n")
    if case.get("tracking"):
        (sessions / f"{sid}.tracking").write_text(case["tracking"] + "\n")
    if case.get("off_file"):
        (sessions / f"{sid}.off").write_text("")
    if "config" in case:
        (config_home / "probe").mkdir(parents=True)
        value = case["config"]
        (config_home / "probe" / "config.json").write_text(value if isinstance(value, str) else json.dumps(value))
    for name in ("PROBE_SESSION_STATE", "PROBE_SESSION_TRACKING", "PROBE_CONFIG_PATH"):
        monkeypatch.delenv(name, raising=False)
    env = {"HOME": str(tmp_path / "home"), "XDG_STATE_HOME": str(state_home), "XDG_CONFIG_HOME": str(config_home),
           **case.get("env", {})}
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    expected = session_marker.session_state(sid) or session_marker.resolve_state_default(None)[0]
    assert tg.switch(sid) == expected
    assert tg.sessions_dir() == session_marker.sessions_dir()
    assert tg.config_path() == session_marker.config_path()


def test_a_switch_that_is_there_and_cannot_be_read_now_reads_off(state, tmp_path, monkeypatch):
    """Fail closed: a `.state` (or a config) that is there and cannot be read
    is `off`, never the default on a guess."""
    (state / f"{SID}.state").mkdir()  # there, and reading it fails (IsADirectoryError)
    assert tg.switch(SID) == tg.OFF
    (state / f"{SID}.state").rmdir()
    assert tg.switch(SID) == "full"
    config = tmp_path / "xdg-config" / "probe" / "config.json"
    config.mkdir(parents=True)
    assert tg.switch(SID) == tg.OFF


def test_the_session_marker_and_this_gate_name_the_same_gap_file_and_format(state):
    from probe.sdk import session_marker
    from probe.service import capture_gate as service_gate

    assert tg.GAP_FILE_SUFFIX == session_marker.GAPS_SUFFIX == service_gate.GAP_FILE_SUFFIX
    assert tg.GAP_FILE_VERSION == service_gate.GAP_FILE_VERSION and tg.MAX_GAPS == service_gate.MAX_GAPS
    assert service_gate.write_gap_file(state, SID, [[3, 9], [20, None]], "/t.jsonl")
    assert tg.read_gaps(SID) == [[3, 9], [20, None]]
    assert tg.record_on(SID, 30, "/t.jsonl") == [[3, 9], [20, 30]]
    assert service_gate.read_gap_file(state, SID) == [[3, 9], [20, 30]]
    data = json.loads(tg.gap_file(SID).read_text())
    assert set(data) == {"v", "sid", "transcript", "gaps", "updated_at"} and data["transcript"] == "/t.jsonl"


@pytest.mark.parametrize("body", ["{", '{"v": 2, "gaps": []}', '{"v": 1, "gaps": [[5, 1]]}', "\xff"])
def test_a_gap_file_that_does_not_read_covers_the_whole_session(state, body):
    tg.gap_file(SID).write_bytes(body.encode("latin-1"))
    assert tg.read_gaps(SID) == [[0, None]]
    assert tg.verdict(SID).blocked


# -- the drains: `Journal.stage` ------------------------------------------------------


@pytest.mark.parametrize("offers", [False, True], ids=["protocol-2", "protocol-3"])
def test_stage_sends_nothing_while_off_and_reads_a_gaps_lines_past_as_nothing(state, tmp_path, offers):
    wire = DoorWire(offers=offers)
    journal = _journal(tmp_path, wire)
    sid, path = _session(tmp_path, [])
    _write(path, [_user(sid, "on-1", 1)])
    _switch(state, sid, "full")
    _start(journal, wire, sid, path)
    assert [_events(b) for b in _drain(journal, wire, sid)] == [["on-1"]]

    _switch(state, sid, "off")
    gap_start = path.stat().st_size
    _write(path, [_user(sid, "SECRET-1", 2), _user(sid, "SECRET-2", 3)])
    assert journal.stage(sid, cwd=CWD) is None  # off: nothing new, not even an empty batch
    assert wire.streams[sid]["source_byte_end"] == gap_start
    assert tg.record_off(sid, gap_start, str(path)) == [[gap_start, None]]

    _switch(state, sid, "full")
    assert journal.stage(sid, cwd=CWD) is None  # its gap is still open: nothing until it closes
    assert tg.record_on(sid, path.stat().st_size, str(path)) == [[gap_start, path.stat().st_size]]
    _write(path, [_user(sid, "on-2", 4)])
    sent = _drain(journal, wire, sid)
    assert [t for b in sent for t in _events(b)] == ["on-2"]
    assert wire.streams[sid]["source_byte_end"] == path.stat().st_size  # every byte accounted for
    assert "SECRET" not in b"".join(wire.calls).decode()


def test_a_batch_staged_before_the_switch_moved_still_goes(state, tmp_path):
    wire = DoorWire(offers=False)
    journal = _journal(tmp_path, wire)
    sid, path = _session(tmp_path, [])
    _write(path, [_user(sid, "on-1", 1)])
    _start(journal, wire, sid, path)
    staged = journal.stage(sid, cwd=CWD)
    _switch(state, sid, "off")
    assert journal.stage(sid, cwd=CWD) == staged  # pending: it may flush, nothing is deleted


def test_the_oversize_placeholder_of_a_line_inside_a_gap_is_not_sent(state, tmp_path, monkeypatch):
    """A line too long to read stands as `[transcript line not sent: N
    bytes...]`, except one written while off: nothing of it goes."""
    monkeypatch.setattr(sj, "MAX_SOURCE_LINE", 600)
    wire = DoorWire(offers=False)
    journal = _journal(tmp_path, wire)
    sid, path = _session(tmp_path, [])
    _write(path, [_user(sid, "on-1", 1), _user(sid, "SECRET-1 " + "x" * 2000, 2), _user(sid, "on-2", 3),
                  _user(sid, "on-3 " + "y" * 2000, 4)])
    at = _offsets(path)
    tg.write_gaps(sid, [[at[1], at[2]]], str(path))
    _start(journal, wire, sid, path)
    sent = b"".join(_drain(journal, wire, sid)).decode()
    assert "SECRET" not in sent and "on-1" in sent and "on-2" in sent
    assert sent.count("transcript line not sent") == 1  # the one outside the gap
    assert f"{len(path.read_bytes().splitlines(keepends=True)[3]):,} bytes" in sent


def test_a_title_written_while_off_is_never_read(state, tmp_path):
    wire = DoorWire(offers=False)
    journal = _journal(tmp_path, wire)
    sid, path = _session(tmp_path, [])
    _write(path, [_user(sid, "on-1", 1), {"type": "custom-title", "customTitle": "SECRET-title", "sessionId": sid}])
    at = _offsets(path)
    tg.write_gaps(sid, [[at[1], at[2]]], str(path))
    _start(journal, wire, sid, path)
    _drain(journal, wire, sid)
    assert "SECRET" not in json.dumps(journal.get(sid))


def test_a_host_settling_a_session_stages_it_while_off_with_its_gaps_read_past(state, tmp_path):
    """The Probe service settles a session that ended while off: on its
    thread the switch does not block it, and every line from its open gap on
    goes as nothing; another thread is still blocked meanwhile."""
    wire = DoorWire(offers=False)
    journal = _journal(tmp_path, wire)
    sid, path = _session(tmp_path, [])
    _write(path, [_user(sid, "on-1", 1)])
    _start(journal, wire, sid, path)
    _drain(journal, wire, sid)
    _switch(state, sid, "off")
    gap = [[path.stat().st_size, None]]
    _write(path, [_user(sid, "SECRET-1", 2)])
    seen: dict = {}
    with tg.settling(sid, gap):
        thread = threading.Thread(target=lambda: seen.setdefault("other", tg.verdict(sid)))
        thread.start()
        thread.join()
        body = journal.stage(sid, cwd=CWD, finalize=True)
    assert seen["other"].blocked
    assert body is not None and "SECRET" not in body.decode()
    journal.deliver(sid, wire)
    assert wire.streams[sid]["source_byte_end"] == path.stat().st_size


def test_a_hosts_own_gaps_count_before_its_gap_file_has_them(state, tmp_path):
    wire = DoorWire(offers=False)
    journal = _journal(tmp_path, wire)
    sid, path = _session(tmp_path, [])
    _write(path, [_user(sid, "on-1", 1), _user(sid, "SECRET-1", 2), _user(sid, "on-2", 3)])
    at = _offsets(path)
    tg.host(lambda s: [[at[1], at[2]]] if s == sid else [])
    assert tg.host_records()
    _start(journal, wire, sid, path)
    sent = b"".join(_drain(journal, wire, sid)).decode()
    assert "SECRET" not in sent and "on-2" in sent
    tg.host(lambda s: 1 / 0)  # a host that cannot say: the whole session
    assert tg.verdict(sid).blocked


def test_probe_import_decides_the_switch_itself_but_never_crosses_a_gap(state, tmp_path, monkeypatch):
    """`probe import` skips a session whose own `.state` says off; one that only
    takes the machine's default (history from before it changed) is imported,
    still without what its gap file covers."""
    monkeypatch.setenv("PROBE_SESSION_STATE", "off")
    wire = DoorWire(offers=False)
    journal = _journal(tmp_path, wire)
    sid, path = _session(tmp_path, [])
    _write(path, [_user(sid, "on-1", 1), _user(sid, "SECRET-1", 2)])
    at = _offsets(path)
    tg.write_gaps(sid, [[at[1], at[2]]], str(path))
    _start(journal, wire, sid, path)
    assert journal.stage(sid, cwd=CWD) is None
    with tg.switch_decided():
        sent = b"".join(_drain(journal, wire, sid)).decode()
    assert "on-1" in sent and "SECRET" not in sent


# -- the session's own recorder -------------------------------------------------------


def test_the_recorder_opens_where_the_switch_was_last_seen_on_and_closes_at_the_flip(state, tmp_path):
    path = tmp_path / "t.jsonl"
    path.write_text("one\n")
    recorder = tg.Recorder(SID, path)
    assert recorder.look() is False and recorder.on_mark == 4
    path.write_text("one\ntwo\n")  # written, not looked at yet
    _switch(state, SID, "off")
    assert recorder.look() is True
    assert tg.read_gaps(SID) == [[4, None]]  # from where it was last seen on: "two" may be off
    path.write_text("one\ntwo\nthree\npartial")
    assert recorder.look() is True and tg.read_gaps(SID) == [[4, None]]  # opened once
    _switch(state, SID, "full")
    assert recorder.look() is False
    assert tg.read_gaps(SID) == [[4, 14]]  # closed at the complete-line end now
    assert json.loads(tg.gap_file(SID).read_text())["transcript"] == str(path)


def test_a_recorder_that_first_sees_its_session_off_starts_the_gap_at_the_first_byte(state, tmp_path):
    path = tmp_path / "t.jsonl"
    path.write_text("one\ntwo\n")
    _switch(state, SID, "off")
    assert tg.Recorder(SID, path).look() is True
    assert tg.read_gaps(SID) == [[0, None]]


def test_a_recorder_whose_gap_file_cannot_be_written_says_so_once_and_stays_blocked(state, tmp_path, monkeypatch):
    path = tmp_path / "t.jsonl"
    path.write_text("one\n")
    said: list[str] = []
    recorder = tg.Recorder(SID, path, said.append)
    _switch(state, SID, "off")
    monkeypatch.setattr(tg, "write_gaps", lambda *a, **k: False)
    assert recorder.look() is True and recorder.look() is True
    assert len([m for m in said if "could not be written" in m]) == 1
    assert tg.verdict(SID).blocked  # the switch itself still blocks every drain
    assert not tg.gap_file(SID).exists() and recorder.held == [[0, None]]
    assert recorder.recorded()  # held here, the session ends finalized without it


# -- writers: never two at once, never a gap lost --------------------------------------


def _hammer(state_home: str, sid: str, start: int, rounds: int) -> None:
    os.environ["XDG_STATE_HOME"] = state_home
    for i in range(rounds):
        mark = start + 10 * i
        assert tg._update(sid, lambda gaps, m=mark: gaps + [[m, m + 5]], None) is not None


def test_writers_in_many_processes_at_once_never_lose_a_gap(state, tmp_path):
    """Every write is a read-modify-write under the session's lock: four
    processes adding gaps to one session's file at once keep every one (an
    unlocked read-modify-write loses the gaps another wrote in between)."""
    context = multiprocessing.get_context("spawn")
    workers = [context.Process(target=_hammer, args=(str(tmp_path / "xdg-state"), SID, 1000 * n, 12))
               for n in range(4)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join(60)
        assert worker.exitcode == 0
    gaps = tg.read_gaps(SID)
    assert len(gaps) == 48, gaps
    assert all(tg.in_gap(gaps, 1000 * n + 10 * i) for n in range(4) for i in range(12))


def test_an_opening_seen_after_a_later_one_starts_the_gap_earlier_and_a_stale_close_never_cuts_it():
    assert tg.opened([[50, None]], 20) == [[20, None]]  # what lay between is off too
    assert tg.opened([[20, None]], 50) == [[20, None]]
    assert tg.opened([[0, 5], [30, 40]], 20) == [[0, 5], [20, None]]  # a later closed one is inside it
    assert tg.closed([[50, None]], 20) == [[50, None]]  # seen on before it was seen off again: stays open
    assert tg.closed([[50, None]], 60) == [[50, 60]]
    assert tg.closed([[0, 5]], 1) == [[0, 5]]


def test_a_writer_waits_for_the_lock_and_gives_up_for_now_after_a_while(state, monkeypatch):
    """One writer at a time; one that cannot have the lock in time writes
    nothing now (its caller looks again), never without the lock."""
    monkeypatch.setattr(tg, "LOCK_WAIT_S", 0.2)
    with tg.locked(SID):
        with pytest.raises(OSError):
            with tg.locked(SID):
                pass
        assert tg.record_off(SID, 0) is None
        assert not tg.gap_file(SID).exists()
    assert tg.record_off(SID, 0) == [[0, None]]


def test_a_session_id_no_file_can_be_named_for_is_never_written(state):
    assert tg.record_off("../escape-me-0", 0) is None
    assert not any(state.parent.rglob("*escape*"))


# -- a gap file that cannot be written, and growth (review of #3387) -------------------------


def _lock_unsupported(monkeypatch):
    """`flock` failing as on a network folder with no lock daemon (ENOLCK)."""
    import errno

    real = tg.fcntl.flock

    def flock(fd, op):
        if op & tg.fcntl.LOCK_EX:
            raise OSError(errno.ENOLCK, "No locks available")
        return real(fd, op)

    monkeypatch.setattr(tg.fcntl, "flock", flock)


def _on_off_on(state, tmp_path, recorder_path_hook=None):
    """A journal and a Recorder over one session: on-1 sent, then off."""
    wire = DoorWire(offers=False)
    journal = _journal(tmp_path, wire)
    sid, path = _session(tmp_path, [])
    _write(path, [_user(sid, "on-1", 1)])
    _switch(state, sid, "full")
    recorder = tg.Recorder(sid, str(path))
    assert recorder.look() is False
    _start(journal, wire, sid, path)
    assert [t for b in _drain(journal, wire, sid) for t in _events(b)] == ["on-1"]
    return wire, journal, sid, path, recorder


@pytest.mark.skipif(tg.fcntl is None, reason="flock")
def test_where_the_folder_cannot_be_locked_the_stretch_is_written_without_the_lock(state, tmp_path, monkeypatch):
    """Review of #3387: with `flock` answering ENOLCK every gap write failed,
    and the stretch went out once the switch read on. Locking that is not
    available at all (not merely held) writes without it."""
    wire, journal, sid, path, recorder = _on_off_on(state, tmp_path)
    _lock_unsupported(monkeypatch)
    _switch(state, sid, "off")
    assert recorder.look() is True
    _write(path, [_user(sid, "SECRET-1", 2)])
    assert recorder.look() is True
    assert journal.stage(sid, cwd=CWD) is None
    assert recorder.recorded() and tg.is_open(tg.read_gaps(sid))  # written, unlocked
    _switch(state, sid, "full")
    recorder.look()
    _write(path, [_user(sid, "on-2", 3)])
    sent = [t for b in _drain(journal, wire, sid) for t in _events(b)]
    assert sent == ["on-2"], sent


def test_a_lock_file_that_cannot_be_opened_writes_without_the_lock(state):
    (state / f"{SID}.gaps.lock").mkdir()  # a folder stands where the lock file goes
    assert tg.record_off(SID, 5) == [[5, None]]
    assert tg.read_gaps(SID) == [[5, None]]


def test_a_stretch_whose_gap_file_cannot_be_written_is_held_and_skipped_here_and_written_later(
        state, tmp_path, monkeypatch):
    """No write lands for the whole stretch (a full disk, a read-only folder):
    the recorder keeps it, this process's drains stay blocked while it is
    open and skip its lines once it closes, and it reaches the file at the
    first look whose write lands."""
    wire, journal, sid, path, recorder = _on_off_on(state, tmp_path)
    said: list[str] = []
    recorder.log = said.append
    real_write = tg.write_gaps
    monkeypatch.setattr(tg, "write_gaps", lambda *a, **k: False)
    _switch(state, sid, "off")
    start = path.stat().st_size
    assert recorder.look() is True
    _write(path, [_user(sid, "SECRET-1", 2)])
    assert recorder.look() is True
    assert not tg.gap_file(sid).exists() and recorder.held == [[start, None]]
    assert tg.verdict(sid).blocked
    _switch(state, sid, "full")
    assert recorder.look() is False
    end = path.stat().st_size
    assert recorder.held == [[start, end]] and tg.verdict(sid) == (False, [[start, end]])
    assert recorder.recorded() is False and recorder.gaps() == [[start, end]]
    _write(path, [_user(sid, "on-2", 3)])
    sent = [t for b in _drain(journal, wire, sid) for t in _events(b)]
    assert sent == ["on-2"], sent
    assert len([m for m in said if "could not be written" in m]) == 1
    monkeypatch.setattr(tg, "write_gaps", real_write)
    recorder.look()
    assert tg.read_gaps(sid) == [[start, end]] and recorder.held == []
    assert not tg.verdict(sid).blocked


def test_a_watch_drops_the_stretches_the_servers_cursor_is_past(state, tmp_path):
    """Growth (review of #3387): after a delivery the session's own recorder
    drops the closed stretches that end at or below the server's cursor; one
    still ahead of it, and an open one, stay."""
    path = tmp_path / "t.jsonl"
    path.write_text("x\n")
    recorder = tg.Recorder(SID, path)
    assert tg.write_gaps(SID, [[0, 5], [10, 20], [30, 40], [50, None]], str(path))
    recorder.held = [[2, 4], [42, 45]]
    recorder.settled(20)
    assert tg.read_gaps(SID) == [[30, 40], [50, None]]
    assert recorder.held == [[42, 45]]
    assert tg.write_gaps(SID, [[0, 5]], str(path))
    recorder.held = []
    recorder.settled(5)
    assert not tg.gap_file(SID).exists()
