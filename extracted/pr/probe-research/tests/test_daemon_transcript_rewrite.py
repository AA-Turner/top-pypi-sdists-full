"""A chat log rewritten under the daemon's cursor stops that stream; it is never
read again from 0 and never read on from inside bytes it never read.

Kimi Code rewrites its wire in place (an atomic temp-file + rename) when it
migrates an older protocol on resume, normalizes a legacy record or repairs a
torn tail. An event's id is `<stream>:<offset>:<index>`: read again from 0, a
rewritten file whose lines moved would hand the daemon every old event again
under new ids -- duplicate writes. The worker keeps the file's inode and a hash
of the GUARD_BYTES before its cursor (in the store, so it survives a restart)
and stops the stream on any mismatch, with one notice.

The wires are real (`fixtures/daemon_adapters/kimi_code/session1.jsonl`).
"""

from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path

import pytest

from probe.daemon import bite as bite_mod
from probe.daemon import lease, mailbox
from probe.daemon import worker as worker_mod
from probe.daemon.events import Kind
from probe.daemon.store import FORMAT_VERSION, Store

SID = "9b40c4c4-d58a-4ed7-9372-cfecf8469b05"
WIRE = Path(__file__).parent / "fixtures" / "daemon_adapters" / "kimi_code" / "session1.jsonl"
LINES = WIRE.read_bytes().splitlines(keepends=True)
#: The first turn (through its `turn.ended`); the second follows.
FIRST_TURN = next(i for i, raw in enumerate(LINES) if json.loads(raw)["type"] == "turn.ended") + 1


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


def _worker(tmp_path: Path, transcript: Path, source: str = "kimi_code") -> worker_mod.Worker:
    work = tmp_path / "home" / "proj"
    work.mkdir(parents=True, exist_ok=True)
    return worker_mod.Worker(worker_mod.Session(SID, transcript, work, source, home=tmp_path / "home"))


def _read_all(w: worker_mod.Worker) -> int:
    added = 0
    for _ in range(10):
        n = w.read_new()
        added += n
        if not n:
            break
    return added


def _chat(w: worker_mod.Worker) -> list[tuple[str, Kind]]:
    """Every event from the chat log (not the daemon's own notices), in store order."""
    return [(e.event_id, e.kind) for e in w.store.events_between(1) if e.stream != bite_mod.NOTICE_STREAM]


def _notices(w: worker_mod.Worker) -> list[str]:
    return [e.text for e in w.store.events_between(1) if e.stream == bite_mod.NOTICE_STREAM]


def _errors(tmp_path: Path) -> str:
    path = tmp_path / "state" / "probe" / "daemon-errors.log"
    return path.read_text() if path.exists() else ""


def _one_pass(source: str, data: bytes) -> list[tuple[str, Kind]]:
    """What reading `data` once from 0 gives: the ids an untouched append yields."""
    from probe.daemon import adapters

    a, out, off = adapters.for_source(source), [], 0
    for raw in data.splitlines(keepends=True):
        off += len(raw)
        out += [(e.event_id, e.kind) for e in a.parse_bytes(raw.rstrip(b"\n"), stream="main", offset=off)]
    return out


def _started(tmp_path: Path, lines: list[bytes] = LINES[:FIRST_TURN]) -> tuple[worker_mod.Worker, Path]:
    transcript = tmp_path / "wire.jsonl"
    transcript.write_bytes(b"".join(lines))
    w = _worker(tmp_path, transcript)
    assert _read_all(w) > 0
    assert w.store.cursor("main")[1] == transcript.stat().st_size
    return w, transcript


def _assert_stopped_without_replay(tmp_path, w, before, why: str) -> None:
    """CRITICAL: not one chat event after the rewrite -- nothing replayed under a
    new id, nothing read from inside the new bytes -- and exactly one notice."""
    cursor = w.store.cursor("main")[1]
    _read_all(w)  # the first poll only suspects a rewrite
    assert _notices(w) == [] and w.store.fact(f"{worker_mod.STREAM_SUSPECT}:main") == cursor
    _read_all(w)  # the next one, at the same cursor, stops the stream
    assert _chat(w) == before, "no event may be replayed or read after a rewrite"
    [notice] = _notices(w)
    assert why in notice and f"byte {cursor:,}" in notice
    assert w.store.fact(f"{worker_mod.STREAM_STOPPED}:main")["offset"] == cursor
    assert w.store.cursor("main")[1] == cursor, "the cursor stays where the reading stopped"
    assert "was rewritten in place" in _errors(tmp_path)
    # Polls after it read nothing and say nothing more.
    with w.session.transcript.open("ab") as handle:
        handle.write(b"".join(LINES[FIRST_TURN:]))
    assert _read_all(w) == 0
    assert _chat(w) == before and len(_notices(w)) == 1
    assert _errors(tmp_path).count("was rewritten in place") == 1


def test_appends_read_on_with_no_notice(tmp_path):
    w, transcript = _started(tmp_path)
    for raw in LINES[FIRST_TURN:]:  # line by line, as Kimi appends
        with transcript.open("ab") as handle:
            handle.write(raw)
        w.read_new()
    assert _chat(w) == _one_pass("kimi_code", b"".join(LINES))
    assert _notices(w) == [] and _errors(tmp_path) == ""
    assert w.store.fact(f"{worker_mod.STREAM_STOPPED}:main") is None


def test_a_partial_line_is_waited_for_not_mistaken_for_a_rewrite(tmp_path):
    w, transcript = _started(tmp_path)
    nxt = LINES[FIRST_TURN]
    with transcript.open("ab") as handle:
        handle.write(nxt[:20])
    w.read_new()
    with transcript.open("ab") as handle:
        handle.write(nxt[20:] + b"".join(LINES[FIRST_TURN + 1:]))
    _read_all(w)
    assert _chat(w) == _one_pass("kimi_code", b"".join(LINES)) and _notices(w) == []


def test_an_equal_size_rewrite_stops_the_stream(tmp_path):
    w, transcript = _started(tmp_path)
    before = _chat(w)
    data = transcript.read_bytes()
    assert data.count(b"hello-from-kimi") >= 1
    inode = transcript.stat().st_ino
    with transcript.open("r+b") as handle:  # in place: same inode, same size
        handle.write(data.replace(b"hello-from-kimi", b"HELLO-FROM-KIMI"))
    assert transcript.stat().st_ino == inode and transcript.stat().st_size == len(data)
    with transcript.open("ab") as handle:
        handle.write(b"".join(LINES[FIRST_TURN:]))
    _assert_stopped_without_replay(tmp_path, w, before, "changed")


def test_a_smaller_rewrite_stops_the_stream_and_replays_nothing(tmp_path):
    """The hazard the old reset had: the same records, written shorter (here the
    session's opening records gone, as a migration might drop them), moved every
    line -- read again from 0, each old event came back under a new id."""
    w, transcript = _started(tmp_path)
    before = _chat(w)
    shorter = b"".join(LINES[3:FIRST_TURN])
    assert len(shorter) < transcript.stat().st_size
    moved = {i for i, _ in _one_pass("kimi_code", shorter)}
    assert moved - {i for i, _ in before}, "a re-read from 0 would have stored these as new events"
    transcript.write_bytes(shorter)  # truncate + write: same inode, shorter than the cursor
    _assert_stopped_without_replay(tmp_path, w, before, "shorter")


def test_a_larger_rewrite_with_a_changed_prefix_stops_the_stream(tmp_path):
    """A migration that writes MORE (an upgraded metadata record in front): the
    cursor would land inside bytes it never read."""
    w, transcript = _started(tmp_path)
    before = _chat(w)
    head = json.dumps({"type": "metadata", "protocol_version": "1.6", "created_at": 1791169873750,
                       "migrated_from": "1.5"}).encode() + b"\n"
    larger = head + b"".join(LINES[1:])
    assert len(larger) > transcript.stat().st_size
    with transcript.open("r+b") as handle:
        handle.write(larger)
    _assert_stopped_without_replay(tmp_path, w, before, "changed")


def test_a_file_swapped_in_by_rename_with_the_same_bytes_reads_on(tmp_path):
    """Kimi (and any atomic writer, a copy, a network mount) can give the same
    bytes a new inode: the bytes decide, so reading goes on, with no notice."""
    w, transcript = _started(tmp_path)
    tmp = transcript.with_name("wire.jsonl.tmp")
    tmp.write_bytes(b"".join(LINES))  # the same prefix, the rest appended
    old_inode = transcript.stat().st_ino
    os.replace(tmp, transcript)
    assert transcript.stat().st_ino != old_inode
    _read_all(w)
    assert _chat(w) == _one_pass("kimi_code", b"".join(LINES)) and _notices(w) == []


def test_a_file_swapped_in_by_rename_with_changed_bytes_stops_the_stream(tmp_path):
    w, transcript = _started(tmp_path)
    before = _chat(w)
    tmp = transcript.with_name("wire.jsonl.tmp")
    tmp.write_bytes(b"".join(LINES).replace(b"hello-from-kimi", b"HELLO-FROM-KIMI"))
    os.replace(tmp, transcript)
    _assert_stopped_without_replay(tmp_path, w, before, "changed")


def test_a_rewrite_seen_once_and_gone_by_the_next_poll_is_forgiven(tmp_path):
    """A writer caught between truncating and writing the same bytes back."""
    w, transcript = _started(tmp_path)
    data = transcript.read_bytes()
    transcript.write_bytes(data[: len(data) // 2])
    _read_all(w)
    assert w.store.fact(f"{worker_mod.STREAM_SUSPECT}:main") is not None
    transcript.write_bytes(data + b"".join(LINES[FIRST_TURN:]))
    _read_all(w)
    assert _chat(w) == _one_pass("kimi_code", b"".join(LINES)) and _notices(w) == []
    assert w.store.fact(f"{worker_mod.STREAM_SUSPECT}:main") is None


def test_the_guard_survives_a_restart(tmp_path):
    w, transcript = _started(tmp_path)
    before = _chat(w)
    w.store.close()
    data = transcript.read_bytes()
    with transcript.open("r+b") as handle:
        handle.write(data.replace(b"hello-from-kimi", b"HELLO-FROM-KIMI"))
    with transcript.open("ab") as handle:
        handle.write(b"".join(LINES[FIRST_TURN:]))
    later = _worker(tmp_path, transcript)  # a fresh worker on the same store
    _read_all(later)
    _read_all(later)
    assert _chat(later) == before and len(_notices(later)) == 1


def test_a_cursor_saved_without_a_guard_is_trusted_once_and_guarded_after(tmp_path):
    """A store from before the guard (or a cursor an older CLI moved since: its
    `tail_at` is behind) is read on as before, and guarded from then."""
    w, transcript = _started(tmp_path)
    w.store.db.execute("UPDATE cursors SET tail_hash = NULL, tail_at = NULL, inode = NULL")
    assert w.store.cursor_guard("main") == (None, None)
    with transcript.open("ab") as handle:
        handle.write(LINES[FIRST_TURN])
    w.read_new()
    assert w.store.cursor_guard("main")[1] is not None and _notices(w) == []
    w.store.db.execute("UPDATE cursors SET tail_at = 1")  # an older CLI moved the cursor on
    assert w.store.cursor_guard("main") == (None, None)
    with transcript.open("ab") as handle:
        handle.write(b"".join(LINES[FIRST_TURN + 1:]))
    _read_all(w)
    assert _chat(w) == _one_pass("kimi_code", b"".join(LINES)) and _notices(w) == []


def test_every_harness_is_guarded(tmp_path):
    """The reader is shared: a Claude Code transcript rewritten shorter stops too
    (it used to be read again from 0)."""
    lines = [json.dumps(obj).encode() + b"\n" for obj in (
        {"type": "permission-mode", "permissionMode": "default"},
        {"type": "user", "message": {"content": "sweep lr"}, "cwd": "/w"},
        {"type": "assistant", "message": {"content": [
            {"type": "tool_use", "id": "t1", "name": "Bash", "input": {"command": "python sweep.py"}}]}},
        {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "t1", "content": "ok"}]}},
        {"type": "system", "subtype": "turn_duration", "durationMs": 5},
    )]
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_bytes(b"".join(lines))
    w = _worker(tmp_path, transcript, source="claude_code")
    _read_all(w)
    before = _chat(w)
    assert before
    transcript.write_bytes(b"".join(lines[1:]))
    _read_all(w)
    _read_all(w)  # confirmed by a second poll
    assert _chat(w) == before and len(_notices(w)) == 1


def test_the_store_change_is_additive(tmp_path):
    """A store an earlier build wrote (cursors without the guard columns) opens,
    gains them, keeps its cursor and stays format 1: a bump would lock every
    released CLI out of its own stores."""
    path = tmp_path / "old.sqlite"
    db = sqlite3.connect(path)
    db.execute("CREATE TABLE cursors (stream TEXT PRIMARY KEY, path TEXT NOT NULL, offset INTEGER NOT NULL)")
    db.execute("INSERT INTO cursors VALUES ('main', '/x/wire.jsonl', 1234)")
    db.commit()
    db.close()
    st = Store(path)
    assert {r["name"] for r in st.db.execute("PRAGMA table_info(cursors)")} >= {"inode", "tail_hash", "tail_at"}
    assert st.cursor("main") == ("/x/wire.jsonl", 1234) and st.cursor_guard("main") == (None, None)
    assert FORMAT_VERSION == 1 and st.meta("format_version") == "1"
    # What a released CLI writes still works against the new table.
    st.db.execute("INSERT INTO cursors (stream, path, offset) VALUES ('sub', '/y', 5) "
                  "ON CONFLICT(stream) DO UPDATE SET path = excluded.path, offset = excluded.offset")
    assert st.cursor("sub") == ("/y", 5)
