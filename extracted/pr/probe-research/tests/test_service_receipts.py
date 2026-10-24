"""Each registered session's delivery receipts (plan D29, `probe.service.receipts`).

What the server has taken of a session's transcript, and what waits, read from
the recorder's own transcript journal: a REAL `session_journal.Journal` staging
and delivering to `DoorWire` (the receipts door, `test_transcript_protocol3`),
so a row written by the code that records is what the reader reads. Never the
protocol-1 `state.db`, which the recorder stopped writing at #1415.
"""

from __future__ import annotations

import asyncio
import json
import os
import sqlite3
import threading
import time

import pytest

from probe.service import receipts
from probe.tap_core.session_journal import Journal
from tests.test_transcript_protocol3 import CUSTOMER, CWD, DoorWire, _drain, _session, _start, _user, _write


#: Without a claim the service's own recorder published, the journal a session
#: records to is told from Linux's /proc/locks alone; elsewhere (macOS) it is
#: unknown by design, since probing the lock can make a recorder that is claiming
#: at that instant give up (`receipts.read`, and
#: test_without_proc_locks_or_a_published_claim_the_destination_is_unknown).
needs_proc_locks = pytest.mark.skipif(
    not receipts.PROC_LOCKS.exists(), reason="reads which recorder holds a session from /proc/locks (Linux)"
)


def _raises(call):
    try:
        call()
    except Exception as exc:  # noqa: BLE001
        return exc
    return None


def _claim(folder, sid):
    """A live recorder's claim on `sid` in the journal at `folder`, as a plain
    flock (for a journal written without `Journal`, or already closed)."""
    import fcntl

    handle = receipts.owner_lock(folder, sid).open("a+b")
    fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    return handle


def _recorded(tmp_path, lines: int = 6):
    """A session its recorder delivered whole: (sid, transcript, journal, door, root)."""
    door = DoorWire(offers=True)
    sid, path = _session(tmp_path, [_user("x", f"turn {i}", i) for i in range(lines)])
    root = tmp_path / "journal"
    journal = Journal(door.base_url, CUSTOMER, door.source, directory=root)
    # As the tap's loop does: the live claim (its owner lock) comes first.
    assert journal.claim_live(sid)
    _start(journal, door, sid, path)
    _drain(journal, door, sid)
    return sid, path, journal, door, root


@needs_proc_locks
def test_a_delivered_session_reads_its_receipt_cursor_and_when_it_landed(tmp_path):
    before = time.time()
    sid, path, journal, _door, root = _recorded(tmp_path)
    (found,) = receipts.read([sid], [root], {}).values()
    assert found == {
        "last_line": 6, "received_bytes": path.stat().st_size, "received_at": found["received_at"],
        "pending_bytes": 0, "pending_lines": 0, "pending_batch": False, "finalized": False, "retrying": False,
        "scope": {"backend": "synthetic.invalid", "customer": CUSTOMER},
    }
    # The journal stamps the receipt as it retires the batch (tap 0.10.6).
    assert before <= found["received_at"] <= time.time()
    journal.close()


@needs_proc_locks
def test_what_waits_is_the_transcript_past_the_receipt_cursor(tmp_path):
    sid, path, journal, door, root = _recorded(tmp_path)
    counts: dict = {}
    _write(path, [_user(sid, "seven", 7), _user(sid, "eight", 8)])
    with path.open("ab") as handle:
        handle.write(b'{"partial": ')  # a line still being written is not one yet
    waiting = receipts.read([sid], [root], counts)[sid]
    assert waiting["last_line"] == 6
    assert waiting["pending_lines"] == 2
    assert waiting["pending_bytes"] == path.stat().st_size - waiting["received_bytes"]
    # Staged, not yet received: the batch waits, the cursor has not moved.
    assert journal.stage(sid, cwd=CWD) is not None
    staged = receipts.read([sid], [root], counts)[sid]
    assert (staged["pending_batch"], staged["last_line"], staged["pending_lines"]) == (True, 6, 2)
    journal.deliver(sid, door)
    taken = receipts.read([sid], [root], counts)[sid]
    assert (taken["pending_batch"], taken["last_line"], taken["pending_lines"]) == (False, 8, 0)
    assert taken["pending_bytes"] == len(b'{"partial": ')
    journal.close()


def test_a_backlog_is_counted_over_several_passes_then_only_as_it_grows(tmp_path, monkeypatch):
    sid, path, journal, _door, root = _recorded(tmp_path, lines=1)
    _write(path, [_user(sid, "x" * 200, i) for i in range(40)])
    state = journal.get(sid)
    counts: dict = {}
    first = receipts.receipt(state, False, counts, sid, budget=4096)
    assert first["pending_lines"] is None and first["pending_bytes"] > 4096  # still counting
    passes = 1
    while receipts.receipt(state, False, counts, sid, budget=4096)["pending_lines"] is None:
        passes += 1
        assert passes < 50
    assert receipts.receipt(state, False, counts, sid, budget=4096)["pending_lines"] == 40
    counted = counts[sid].counted_to
    _write(path, [_user(sid, "one more", 99)])
    assert receipts.receipt(state, False, counts, sid, budget=4096)["pending_lines"] == 41
    assert counts[sid].counted_to == path.stat().st_size > counted  # only the new bytes were read
    journal.close()


@needs_proc_locks
def test_a_rewritten_transcript_starts_a_new_count(tmp_path):
    sid, path, journal, _door, root = _recorded(tmp_path)
    counts: dict = {}
    _write(path, [_user(sid, "seven", 7)])
    assert receipts.read([sid], [root], counts)[sid]["pending_lines"] == 1
    data = path.read_bytes()
    path.unlink()
    path.write_bytes(data + json.dumps(_user(sid, "eight", 8)).encode() + b"\n")  # a new inode
    assert receipts.read([sid], [root], counts)[sid]["pending_lines"] == 2
    journal.close()


@needs_proc_locks
def test_a_missing_transcript_still_reads_the_cursor(tmp_path):
    sid, path, journal, _door, root = _recorded(tmp_path)
    path.unlink()
    found = receipts.read([sid], [root], {})[sid]
    assert (found["last_line"], found["pending_bytes"], found["pending_lines"]) == (6, None, None)
    journal.close()


def test_a_row_naming_something_other_than_a_file_is_never_opened(tmp_path):
    """A FIFO with no writer would hang the read for good."""
    sid, path, journal, _door, root = _recorded(tmp_path)
    state = journal.get(sid)
    fifo = tmp_path / "fifo"
    os.mkfifo(fifo)
    answers: list = []
    reader = threading.Thread(target=lambda: answers.append(
        receipts.receipt({**state, "path": str(fifo)}, False, {}, sid)), daemon=True)
    reader.start()
    reader.join(5)
    assert not reader.is_alive(), "the reader hung on a FIFO"
    (found,) = answers
    assert (found["last_line"], found["pending_bytes"], found["pending_lines"]) == (6, None, None)
    # Past the stat (the FIFO put there between the two): the open must not hang either.
    count = receipts._Lines(str(fifo), 0, 0, 0, 0)  # noqa: SLF001
    opened = threading.Thread(target=lambda: answers.append(_raises(lambda: count.pending(1, 0, 4096))), daemon=True)
    opened.start()
    opened.join(5)
    assert not opened.is_alive() and isinstance(answers[-1], OSError)
    journal.close()


@needs_proc_locks
def test_a_session_in_two_journals_reads_the_one_its_recorder_holds(tmp_path):
    """An account switch (or staging and production) leaves the same session in
    two namespaces: the stale one never stands for it, whatever its order, even
    with a later receipt than the live one's."""
    sid, path, journal, door, root = _recorded(tmp_path)
    stale = {**journal.get(sid), "source_line_end": 1, "source_byte_end": 10, "received_at": time.time() + 3600}
    for name in ("0" * 64, "f" * 64):  # sorts before, then after, the live namespace
        folder = root / name
        folder.mkdir()
        conn = sqlite3.connect(folder / "state.sqlite3")
        conn.execute("CREATE TABLE sessions(session_id TEXT PRIMARY KEY, state TEXT NOT NULL)")
        conn.execute("INSERT INTO sessions VALUES (?, ?)", (sid, json.dumps(stale)))
        conn.commit()
        conn.close()
        assert receipts.read([sid], [root], {})[sid]["last_line"] == 6
    journal.close()


@needs_proc_locks
def test_after_an_account_switch_the_active_recorders_failures_show(tmp_path):
    """Codex P2: the old account's journal holds a full receipt; the recorder
    now records into the new account's, whose batch is staged and refused
    (401). The active recorder's namespace (its owner lock is held) is the
    one read, never the latest success anywhere."""
    sid, path, old, _door, root = _recorded(tmp_path)
    old.close()  # its recorder is gone (the account switched)
    door = DoorWire(offers=True)
    remote = {**door.receipts(sid), "customer_id": "switched"}
    new = Journal(door.base_url, "switched", door.source, directory=root)
    assert new.claim_live(sid)
    new.ensure(sid, path, remote, historical=False, cwd=CWD)
    assert new.stage(sid, cwd=CWD) is not None
    new.update(sid, error="HTTP 401: token refused")
    found = receipts.read([sid], [root], {})[sid]
    assert (found["last_line"], found["received_at"], found["pending_lines"], found["pending_batch"],
            found["retrying"]) == (0, None, 6, True, True)
    # No recorder holds the session in any journal: where it goes now is
    # unknown, so nothing is claimed for it.
    new.close()
    assert receipts.read([sid], [root], {}) == {}


def _no_locks_taken(monkeypatch):
    import fcntl

    def refuse(*_a, **_k):
        raise AssertionError("the receipt reader took a lock")

    monkeypatch.setattr(fcntl, "flock", refuse)


def test_a_hosted_recorders_published_claim_decides_and_no_lock_is_taken(tmp_path, monkeypatch):
    """Codex P2: the macOS probe could make a recorder that was claiming at
    that instant give up. The service's own recorders publish the journal they
    hold the claim in; that is read, and the reader takes no lock at all."""
    sid, _path, journal, _door, root = _recorded(tmp_path)
    folder = journal.directory
    monkeypatch.setattr(receipts, "_linux_flocks", lambda: None)  # macOS: no /proc/locks
    _no_locks_taken(monkeypatch)
    found = receipts.read([sid], [root], {}, claims={sid: str(folder)})
    assert found[sid]["last_line"] == 6
    journal.close()


def test_without_proc_locks_or_a_published_claim_the_destination_is_unknown(tmp_path, monkeypatch):
    sid, _path, journal, _door, root = _recorded(tmp_path)  # held, but nobody can tell without /proc/locks
    monkeypatch.setattr(receipts, "_linux_flocks", lambda: None)
    _no_locks_taken(monkeypatch)
    assert receipts.read([sid], [root], {}) == {}
    journal.close()


def test_a_proc_locks_row_for_the_same_inode_on_another_device_is_not_the_claim(tmp_path, monkeypatch):
    """Codex P2: /proc/locks names `major:minor:inode` (hex device parts); an
    inode alone repeats across filesystems."""
    sid, _path, journal, _door, root = _recorded(tmp_path)
    journal.close()
    info = os.stat(receipts.owner_lock(journal.directory, sid))
    major, minor = os.major(info.st_dev), os.minor(info.st_dev)
    locks = tmp_path / "locks"
    monkeypatch.setattr(receipts, "PROC_LOCKS", locks)
    locks.write_text(f"1: FLOCK  ADVISORY  WRITE 4242 {major + 1:02x}:{minor:02x}:{info.st_ino} 0 EOF\n")
    assert receipts.read([sid], [root], {}) == {}
    locks.write_text(f"1: -> FLOCK  ADVISORY  WRITE 4243 {major:02x}:{minor:02x}:{info.st_ino} 0 EOF\n"
                     f"2: FLOCK  ADVISORY  WRITE 4242 {major:02x}:{minor:02x}:{info.st_ino} 0 EOF\n")
    assert receipts.read([sid], [root], {})[sid]["last_line"] == 6


@needs_proc_locks
def test_two_accounts_receipts_carry_their_own_scopes(tmp_path):
    """Each receipt names the backend and the customer of the journal it came
    from, so the desktop app overlays only its signed-in account's."""
    first, _p1, journal_a, _d1, root = _recorded(tmp_path)
    door = DoorWire(offers=True)
    door.base_url = "https://staging.example.invalid:8443/"
    second, path = _session(tmp_path, [_user("y", "turn", 0)], name="b")
    journal_b = Journal(door.base_url, "acct-b", door.source, directory=root)
    assert journal_b.claim_live(second)
    journal_b.ensure(second, path, {**door.receipts(second), "customer_id": "acct-b"}, historical=False, cwd=CWD)
    found = receipts.read([first, second], [root], {})
    assert found[first]["scope"] == {"backend": "synthetic.invalid", "customer": CUSTOMER}
    assert found[second]["scope"] == {"backend": "staging.example.invalid:8443", "customer": "acct-b"}
    journal_a.close()
    journal_b.close()


@needs_proc_locks
def test_a_journal_whose_destination_is_not_its_own_gives_no_receipts(tmp_path):
    """A destination file that does not hash to its folder's name (copied,
    edited) names no account: no receipts are served from it."""
    sid, _path, journal, _door, root = _recorded(tmp_path)
    record = journal.directory / receipts.DESTINATION_NAME
    record.write_text(json.dumps({"base_url": "https://other.invalid", "customer_id": "someone", "source": "x"}))
    assert receipts.read([sid], [root], {}) == {}
    journal.close()


@needs_proc_locks
def test_the_destination_record_is_the_journals_and_the_fields_are_the_contracts(tmp_path):
    from probe.service import protocol
    from probe.tap_core import session_journal

    assert receipts.DESTINATION_NAME == session_journal.DESTINATION_NAME
    sid, _path, journal, _door, root = _recorded(tmp_path)
    found = receipts.read([sid], [root], {})[sid]
    assert tuple(found) == protocol.RECEIPT_FIELDS and tuple(found["scope"]) == protocol.RECEIPT_SCOPE_FIELDS
    (row,) = receipts.by_harness([{"sid": sid, "harness": "claude_code", "alive": True, "receipts": found}])
    assert set(row) == set(protocol.HARNESS_RECEIPT_FIELDS)
    journal.close()


@needs_proc_locks
def test_a_failed_read_keeps_the_last_answers(tmp_path, monkeypatch):
    sid, _path, journal, _door, root = _recorded(tmp_path)
    cache = receipts.ReceiptCache(ttl=0)

    async def scenario():
        first = await cache.get([sid], [root], wait=5)
        monkeypatch.setattr(receipts, "read", lambda *a: (_ for _ in ()).throw(OSError("disk gone")))
        return first, await cache.get([sid], [root], wait=5)

    first, after = asyncio.run(scenario())
    assert first[sid]["last_line"] == 6 and after == first
    journal.close()


def test_an_unknown_session_and_an_unreadable_folder_have_no_receipts(tmp_path):
    sid, _path, journal, _door, root = _recorded(tmp_path)
    assert receipts.read(["not-recorded"], [root, tmp_path / "absent"], {}) == {}
    assert receipts.read([sid], [tmp_path / "absent"], {}) == {}
    journal.close()


@needs_proc_locks
def test_an_older_journal_without_protocol_3_or_receipt_times_still_reads(tmp_path):
    """A journal a tap before protocol 3 made has no `fragment_sessions`, and a
    row from before 0.10.6 no `received_at`: the cursor still reads, the time
    is unknown. A protocol-3 row wins over a protocol-2 one, as in the journal.
    (Its destination record is a 0.10.6 tap's, written when it next opens it.)"""
    import hashlib

    root = tmp_path / "old"
    destination = ["https://api.example.invalid", "c-old", "claude_code"]
    folder = root / hashlib.sha256(json.dumps(destination).encode()).hexdigest()
    folder.mkdir(parents=True)
    (folder / receipts.DESTINATION_NAME).write_text(json.dumps(
        {"base_url": destination[0], "customer_id": destination[1], "source": destination[2]}))
    conn = sqlite3.connect(folder / "state.sqlite3")
    conn.executescript(
        "CREATE TABLE sessions(session_id TEXT PRIMARY KEY, state TEXT NOT NULL);"
        "CREATE TABLE pending(session_id TEXT PRIMARY KEY, body BLOB NOT NULL, digest TEXT NOT NULL);"
    )
    transcript = tmp_path / "t.jsonl"
    transcript.write_bytes(b"a\nb\n")
    conn.execute("INSERT INTO sessions VALUES (?, ?)", ("s-old", json.dumps(
        {"session_id": "s-old", "source_line_end": 1, "source_byte_end": 2, "path": str(transcript),
         "error": "network down"})))
    conn.commit()
    conn.close()
    claim = _claim(folder, "s-old")  # an older tap claims its session the same way
    found = receipts.read(["s-old"], [root], {})["s-old"]
    assert (found["last_line"], found["received_at"], found["pending_lines"], found["retrying"]) == (1, None, 1, True)

    conn = sqlite3.connect(folder / "state.sqlite3")
    conn.execute("CREATE TABLE fragment_sessions(session_id TEXT PRIMARY KEY, state TEXT NOT NULL)")
    conn.execute("INSERT INTO fragment_sessions VALUES (?, ?)", ("s-old", json.dumps(
        {"session_id": "s-old", "source_line_end": 2, "source_byte_end": 4, "path": str(transcript),
         "received_at": 1761170000.5})))
    conn.commit()
    conn.close()
    found = receipts.read(["s-old"], [root], {})["s-old"]
    assert (found["last_line"], found["received_at"], found["pending_lines"]) == (2, 1761170000.5, 0)
    claim.close()


def test_per_agent_sums_are_over_the_sessions_where_they_are_known():
    def row(sid, harness, alive, found):
        return {"sid": sid, "harness": harness, "alive": alive, "receipts": found}

    def found(at, waiting_bytes, lines, staged):
        return {"last_line": 1, "received_bytes": 1, "received_at": at, "pending_bytes": waiting_bytes,
                "pending_lines": lines, "pending_batch": staged, "finalized": False, "retrying": False}

    summary = receipts.by_harness([
        row("a", "claude_code", True, found(100.0, 10, 2, True)),
        row("b", "claude_code", False, found(300.0, 5, None, False)),
        row("c", "claude_code", True, None),
        row("d", "codex", True, None),
    ])
    assert summary == [
        {"harness": "claude_code", "scope": None, "sessions": 3, "alive": 2, "received_at": 300.0,
         "pending_bytes": 15, "pending_lines": 2, "pending_batches": 1},
        {"harness": "codex", "scope": None, "sessions": 1, "alive": 1, "received_at": None, "pending_bytes": None,
         "pending_lines": None, "pending_batches": 0},
    ]


def test_per_agent_rows_are_per_account():
    """Two accounts' sessions of one agent are never summed into one row."""
    def row(sid, customer, lines):
        scope = {"backend": "api.example.invalid", "customer": customer}
        return {"sid": sid, "harness": "codex", "alive": True, "receipts": {
            "last_line": 1, "received_bytes": 1, "received_at": 1.0, "pending_bytes": 1, "pending_lines": lines,
            "pending_batch": False, "finalized": False, "retrying": False, "scope": scope}}

    summary = receipts.by_harness([row("a", "mine", 2), row("b", "theirs", 900), row("c", "mine", 3),
                                   {"sid": "d", "harness": "codex", "alive": False, "receipts": None}])
    assert [(r["scope"] and r["scope"]["customer"], r["sessions"], r["pending_lines"]) for r in summary] == [
        (None, 1, None), ("mine", 2, 5), ("theirs", 1, 900),
    ]


def test_the_journal_folder_follows_what_a_recorder_names(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    default = tmp_path / ".probe" / "transcripts-v2"
    assert receipts.journal_roots() == [default]
    named = tmp_path / "elsewhere"
    envs = [{"PROBE_TRANSCRIPT_STATE_DIR": str(named)}, {"PROBE_TRANSCRIPT_STATE_DIR": str(named)}, {}, None,
            {"PROBE_TRANSCRIPT_STATE_DIR": "relative/dir"}]
    assert receipts.journal_roots(envs) == [default, named]


@needs_proc_locks
def test_the_cache_reads_once_per_ttl_and_never_makes_a_caller_wait_long(tmp_path, monkeypatch):
    sid, _path, journal, _door, root = _recorded(tmp_path)
    cache = receipts.ReceiptCache(ttl=60)

    async def scenario():
        first = await cache.get([sid], [root], wait=5)
        again = await cache.get([sid], [root], wait=5)
        return first, again

    first, again = asyncio.run(scenario())
    assert first[sid]["last_line"] == 6 and again == first and cache.reads == 1

    slow = receipts.ReceiptCache(ttl=0)
    monkeypatch.setattr(receipts, "read", lambda *a: (time.sleep(0.5), {sid: {"last_line": 1}})[1])

    async def impatient():
        began = time.monotonic()
        answer = await slow.get([sid], [root], wait=0.05)
        waited = time.monotonic() - began
        await asyncio.sleep(0.7)  # the read finishes on its own thread
        return answer, waited, await slow.get([sid], [root], wait=0)

    answer, waited, later = asyncio.run(impatient())
    assert answer == {sid: None} and waited < 0.4
    assert later == {sid: {"last_line": 1}}
    journal.close()


@pytest.mark.skipif(os.name != "posix", reason="journals are POSIX here")
@needs_proc_locks
def test_a_reader_never_writes_the_journal(tmp_path):
    sid, _path, journal, _door, root = _recorded(tmp_path)
    journal.close()  # its WAL folded into the file, so the file is what to compare
    (db,) = root.glob("*/state.sqlite3")
    claim = _claim(db.parent, sid)
    before = (db.read_bytes(), db.stat().st_mtime_ns)
    assert receipts.read([sid], [root], {})[sid]["last_line"] == 6
    # SQLite may open the (empty) WAL beside a read-only reader; the journal is untouched.
    assert (db.read_bytes(), db.stat().st_mtime_ns) == before
    wal = db.with_name(db.name + "-wal")
    assert not wal.exists() or wal.stat().st_size == 0
    claim.close()
