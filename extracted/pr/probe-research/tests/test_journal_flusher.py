"""The timed fsync (plan T6, D1 = A): `log()` leaves its op file's fsync to `JournalFlusher`,
which forces it to disk within a second and at finish, the SIGTERM close and exit;
`PROBE_OUTBOX_FSYNC=each`, a dead flusher thread and a backlog keep the per-op fsync."""

from __future__ import annotations

import os
import threading
import time

import pytest

from probe.sdk.delivery.journal import flusher as flusher_module
from probe.sdk.delivery.journal.flusher import FsyncMode, JournalFlusher, get_fsync_mode
from probe.sdk.delivery.journal.journal import Journal

RUN = "6f1c1d1e-0000-4000-8000-0000000000f5"


@pytest.fixture
def synced(monkeypatch):
    """Every path os.fsync was called on, in order. Linux only: fds map to paths via /proc."""
    if not os.path.isdir("/proc/self/fd"):
        pytest.skip("maps fds to paths via /proc")
    paths: list[str] = []
    real = os.fsync

    def spy(fd):
        try:
            paths.append(os.readlink(f"/proc/self/fd/{fd}"))
        except OSError:
            pass
        return real(fd)

    monkeypatch.setattr(os, "fsync", spy)
    return paths


@pytest.fixture
def fresh_flusher(monkeypatch):
    registered: list = []
    monkeypatch.setattr(flusher_module.atexit, "register", registered.append)
    flusher = JournalFlusher()
    monkeypatch.setattr(flusher_module, "_FLUSHER", flusher)
    flusher.registered = registered
    return flusher


@pytest.fixture
def interval(monkeypatch):
    """The default mode, named: Windows defaults to `each`."""
    monkeypatch.setenv("PROBE_OUTBOX_FSYNC", "interval")


def _log(journal: Journal, step: int = 0) -> str:
    journal.append_http("POST", f"/v1/runs/{RUN}/metrics", {"points": [{"key": "loss", "value": 1.0, "step_index": step}]})
    return str(sorted(journal.ops_dir.iterdir())[-1])


def _files_in(paths, journal):
    """The fsynced files in ops/, a write's `.tmp` sibling included (the per-op fsync lands there)."""
    return [p for p in paths if p.startswith(str(journal.ops_dir) + os.sep)]


def _record(flusher: JournalFlusher, folder, count: int) -> list[str]:
    """``count`` op files recorded the way `record` does, without starting the thread."""
    os.makedirs(folder, exist_ok=True)
    paths = []
    for index in range(count):
        path = os.path.join(folder, f"op-{index}.json")
        with open(path, "w") as handle:
            handle.write("{}\n")
        paths.append(path)
    flusher._paths.extend(paths)
    flusher._paths_since = time.monotonic()
    return paths


@pytest.mark.parametrize(
    ("raw", "system", "expected"),
    [
        (None, "posix", "interval"),
        ("each", "posix", "each"),
        ("EACH", "posix", "each"),
        ("interval", "posix", "interval"),
        ("sometimes", "posix", "interval"),
        (None, "nt", "each"),
        ("interval", "nt", "interval"),
    ],
)
def test_the_mode_defaults_to_interval_except_on_windows(monkeypatch, raw, system, expected):
    if raw is None:
        monkeypatch.delenv("PROBE_OUTBOX_FSYNC", raising=False)
    else:
        monkeypatch.setenv("PROBE_OUTBOX_FSYNC", raw)
    real = os.name
    os.name = system  # set back at once: pathlib reads it, and fixture teardown uses pathlib
    try:
        mode = get_fsync_mode()
    finally:
        os.name = real
    assert mode == FsyncMode(expected)


def test_interval_mode_fsyncs_the_op_within_a_second_not_in_log(tmp_path, interval, synced, fresh_flusher):
    journal = Journal(tmp_path / "outbox")
    journal._ensure()
    synced.clear()
    op = _log(journal)
    assert _files_in(synced, journal) == [], "log() itself fsyncs nothing in ops/, its temp included"
    deadline = time.monotonic() + 2.0
    # The flusher syncs the files, then their folder: wait for both, not just the first.
    while not (op in synced and str(journal.ops_dir) in synced) and time.monotonic() < deadline:
        time.sleep(0.02)
    assert op in synced, "the flusher fsynced the op within its second"
    assert str(journal.ops_dir) in synced, "and then its folder, so the rename lasts too"


def test_each_mode_fsyncs_every_op_before_log_returns(tmp_path, monkeypatch, synced, fresh_flusher):
    monkeypatch.setenv("PROBE_OUTBOX_FSYNC", "each")
    journal = Journal(tmp_path / "outbox")
    journal._ensure()
    synced.clear()
    _log(journal)
    files = _files_in(synced, journal)
    assert len(files) == 1 and files[0].endswith(".tmp"), "one fsync, of the op's temp before its rename"
    assert fresh_flusher._thread is None, "no flusher in today's mode"


def test_flush_forces_everything_recorded_to_disk_at_once(tmp_path, interval, synced, fresh_flusher):
    journal = Journal(tmp_path / "outbox")
    written = [_log(journal, step) for step in range(5)]
    synced.clear()
    assert flusher_module.flush_journal() == 5
    assert all(path in synced for path in written)
    assert fresh_flusher.registered == [fresh_flusher._flush_at_exit], "and at exit (atexit)"


def test_a_dead_flusher_thread_falls_back_to_the_per_op_fsync(tmp_path, interval, synced, fresh_flusher):
    journal = Journal(tmp_path / "outbox")
    first = _log(journal, 0)
    dead = threading.Thread(target=lambda: None)
    dead.start()
    dead.join()
    fresh_flusher._thread = dead  # it died (an exception, a C extension's abort)
    synced.clear()
    _log(journal, 1)
    assert first in synced, "what it held is flushed by the next write"
    own = [p for p in _files_in(synced, journal) if p != first]
    assert len(own) == 1 and own[0].endswith(".tmp"), "and that write fsyncs itself"
    assert fresh_flusher.can_defer_fsync() is False


def test_finish_flushes_before_it_drains_within_its_deadline(app, tmp_path, interval, monkeypatch, fresh_flusher):
    from tests.conftest import make_client, open_run

    monkeypatch.setattr(flusher_module, "FLUSH_EVERY_SECONDS", 3600.0)  # the tick cannot do it
    flushes: list = []
    real_flush = fresh_flusher.flush

    def spy(**kw):
        posted = sum(1 for request in app.requests if request.url.path.endswith("/metrics"))
        flushes.append((posted, kw.get("deadline")))
        return real_flush(**kw)

    monkeypatch.setattr(fresh_flusher, "flush", spy)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = open_run(client, experiment="flush")
    run.log({"loss": 1.0}, step=0)
    assert fresh_flusher._paths, "the op waits for the flusher"
    run.finish()
    assert flushes, "finish() forced the run's ops to disk"
    posted, deadline = flushes[0]
    assert posted == 0, "before its drain sent them"
    assert deadline is not None, "within the close's deadline (review C2)"
    assert any(request.url.path.endswith("/metrics") for request in app.requests)


def test_the_sigterm_close_flushes_and_dying_never_waits(monkeypatch):
    from probe.sdk.run.launch import preempt

    calls: list = []
    monkeypatch.setattr(flusher_module, "flush_journal", lambda **kw: calls.append(("flush", kw)) or 0)
    monkeypatch.setattr(preempt, "_close_runs", lambda: calls.append(("close", None)))
    monkeypatch.setattr(preempt._state, "ending", preempt.Ending(15, time.monotonic() + 9.0, 143))
    preempt._close()
    assert [name for name, _ in calls] == ["close", "flush"]
    assert calls[1][1]["deadline"] == preempt._state.ending.deadline, "within the close's deadline"
    monkeypatch.setattr(preempt.signal, "raise_signal", lambda signum: calls.append(("die", None)))
    monkeypatch.setattr(preempt.signal, "signal", lambda *a: None)
    monkeypatch.setattr(preempt.os, "_exit", lambda code: calls.append(("exit", None)))
    preempt._die(quiet=True)
    assert [name for name, _ in calls[2:4]] == ["flush", "die"], "the default action skips atexit: flushed first"
    assert calls[2][1]["wait"] is False, "dying never waits for a flush it may have interrupted (review C1)"


def test_a_torn_op_is_moved_to_failed_and_counted(tmp_path):
    from probe.sdk.delivery.outbox.drain.drain import drain

    journal = Journal(tmp_path / "outbox")
    journal._ensure()
    (journal.ops_dir / "000000000001-00000000000000000001-deadbeef.json").write_text("")
    (journal.ops_dir / "000000000002-00000000000000000002-cafef00d.json").write_text('{"kind": "ht')
    report = drain(journal, client_factory=lambda ctx: None)
    assert report.dead_lettered == 0 and list(journal.ops_dir.iterdir()) == []
    assert {p.name for p in journal.failed_dir.iterdir()} >= {
        "000000000001-00000000000000000001-deadbeef.json",
        "000000000002-00000000000000000002-cafef00d.json",
    }
    status = Journal.read_status(journal.dir)
    assert status["torn"] == 2
    torn = [r for r in journal.recent_dead_letters() if r.get("reason") == "torn"]
    assert {r["op_id"] for r in torn} == {"deadbeef", "cafef00d"} and all(r["run_ref"] is None for r in torn)
    assert journal.read_failed()[1] == 2


def test_the_torn_count_survives_a_status_rewrite_that_drops_it(tmp_path):
    """Review I11: an older SDK rewrites status.json without `torn`; the count is read from the
    torn files in failed/, which no rewrite touches."""
    from probe.sdk.delivery.outbox.drain.drain import drain

    journal = Journal(tmp_path / "outbox")
    journal._ensure()
    (journal.ops_dir / "000000000001-00000000000000000001-deadbeef.json").write_text("")
    drain(journal, client_factory=lambda ctx: None)
    status = Journal.read_status(journal.dir, include_receipts=False)
    status.pop("torn")
    journal.status_file.write_text(__import__("json").dumps(status))
    assert journal.read_failed()[1] == 1


# -- never blocks a close (review C1, C2) ---------------------------------------------------------


def test_a_flush_another_thread_is_in_never_holds_a_close_past_its_wait(tmp_path, synced, fresh_flusher):
    """Review C1: the running flush may be the frame a SIGTERM interrupted. A close waits for it
    at most `_LOCK_WAIT_SECONDS`, then syncs that flush's files itself; dying does not wait."""
    in_flight = _record(fresh_flusher, tmp_path / "ops", 3)
    fresh_flusher._take()  # a flush took them and is stuck mid-fsync
    assert fresh_flusher._flushing.acquire(blocking=False)
    try:
        synced.clear()
        started = time.monotonic()
        assert fresh_flusher.flush(deadline=time.monotonic() + 5.0) == 3
        assert time.monotonic() - started < flusher_module._LOCK_WAIT_SECONDS + 0.5
        assert all(path in synced for path in in_flight), "the stuck flush's batch is down anyway"
        synced.clear()
        started = time.monotonic()
        fresh_flusher.flush(deadline=time.monotonic() + 5.0, wait=False)
        # Under the lock wait, not a fixed 0.2 s: the four fsyncs here are real disk calls, and a
        # flush that waited for the lock would take at least _LOCK_WAIT_SECONDS.
        assert time.monotonic() - started < flusher_module._LOCK_WAIT_SECONDS, "dying never waits for the lock"
        assert all(path in synced for path in in_flight)
    finally:
        fresh_flusher._flushing.release()


def test_a_deadline_stops_the_fsyncs_and_keeps_the_rest_for_later(tmp_path, monkeypatch, fresh_flusher):
    paths = _record(fresh_flusher, tmp_path / "ops", 3)
    monkeypatch.setattr(os, "fsync", lambda fd: time.sleep(0.3))  # a slow disk
    assert fresh_flusher.flush(deadline=time.monotonic() + 0.1) == 1, "the fsync it started finishes; no other starts"
    assert fresh_flusher._retry == paths[1:] + paths[:1], "the rest waits, first in line, then the one whose folder waits"
    monkeypatch.setattr(os, "fsync", lambda fd: None)
    assert fresh_flusher.flush() == 3


def test_past_the_backlog_cap_writers_fsync_their_own_op(tmp_path, interval, fresh_flusher, monkeypatch):
    """Review C2: a disk slower than the writes never builds a backlog a close must wait out."""
    fresh_flusher._thread = threading.current_thread()  # alive, and never flushing
    _record(fresh_flusher, tmp_path / "ops", flusher_module.BACKLOG_MAX_FILES - 1)
    assert fresh_flusher.can_defer_fsync() is True
    _record(fresh_flusher, tmp_path / "more", 1)
    assert fresh_flusher.can_defer_fsync() is False, "too many files wait"
    fresh_flusher._paths[:] = fresh_flusher._paths[:1]
    fresh_flusher._paths_since = time.monotonic()
    assert fresh_flusher.can_defer_fsync() is True
    fresh_flusher._paths_since = time.monotonic() - flusher_module.BACKLOG_MAX_SECONDS - 0.1
    assert fresh_flusher.can_defer_fsync() is False, "the oldest waited too long"


def test_a_flusher_that_cannot_start_never_drops_the_write(tmp_path, interval, synced, fresh_flusher, monkeypatch):
    """Review C5: starting the thread raised (interpreter shutdown, a thread limit) after the op
    was on disk, and the append counted it dropped. The op stays queued and is synced in place."""

    def refuse(self):
        raise RuntimeError("can't create new thread at interpreter shutdown")

    monkeypatch.setattr(flusher_module.threading.Thread, "start", refuse)
    journal = Journal(tmp_path / "outbox")
    journal._ensure()
    synced.clear()
    op_id = journal.append_http("POST", f"/v1/runs/{RUN}/metrics", {"points": [{"key": "loss", "value": 1.0, "step_index": 0}]})
    assert op_id and [path for path, _ in journal.pending()], "queued, not dropped"
    assert str(journal.pending()[0][0]) in synced, "synced where it was written"
    assert fresh_flusher.can_defer_fsync() is False, "and every later write syncs its own"


def test_a_failed_fsync_is_counted_at_once_said_once_and_tried_once_more(tmp_path, monkeypatch, fresh_flusher):
    """Review of #3785, I8: a failed fsync was swallowed and its file forgotten. Counted at once
    (a retry that succeeds proves nothing: Linux reports a writeback error once), tried once
    more, and said once, from `finish()`'s flush too, not only the flusher thread."""
    good, bad = _record(fresh_flusher, tmp_path / "ops", 2)
    monkeypatch.setattr(flusher_module, "_FLUSHER", fresh_flusher)
    warned: list = []
    monkeypatch.setattr(flusher_module._diagnostics, "warn", lambda message, **kw: warned.append(message))
    bad_fds: set = set()
    real_open = os.open

    def opening(path, flags, *a):
        fd = real_open(path, flags, *a)
        if str(path) == bad:
            bad_fds.add(fd)
        return fd

    def failing(fd):
        if fd in bad_fds:
            raise OSError(5, "Input/output error")

    monkeypatch.setattr(os, "open", opening)
    monkeypatch.setattr(os, "fsync", failing)
    assert flusher_module.flush_journal(warn=True) == 1
    assert fresh_flusher._retry == [bad] and fresh_flusher.failed_fsync_count == 1, "counted, kept for one more try"
    assert len(warned) == 1 and "1 queued write(s) could not be forced to disk" in warned[0]
    assert flusher_module.flush_journal(warn=True) == 0
    assert fresh_flusher._retry == [] and fresh_flusher.failed_fsync_count == 1, "then forgotten, counted once"
    assert len(warned) == 1, "said once"


def test_a_file_that_cannot_be_opened_is_counted_not_taken_for_delivered(tmp_path, monkeypatch, fresh_flusher):
    """Review of #3785 (adversarial): only a missing file was delivered; EMFILE or EACCES left
    one unsynced and untracked."""
    [path] = _record(fresh_flusher, tmp_path / "ops", 1)
    real_open = os.open

    def refusing(target, flags, *a):
        if str(target) == path:
            raise OSError(24, "Too many open files")
        return real_open(target, flags, *a)

    monkeypatch.setattr(os, "open", refusing)
    monkeypatch.setattr(os, "fsync", lambda fd: None)
    assert fresh_flusher.flush() == 0
    assert fresh_flusher._retry == [path] and fresh_flusher.failed_fsync_count == 1


def test_a_deadline_before_the_folder_keeps_its_files_for_later(tmp_path, monkeypatch, fresh_flusher):
    """Codex review: the deadline passed after a file's fsync but before its folder's, and the
    file was forgotten, so its rename was never forced to disk."""
    [path] = _record(fresh_flusher, tmp_path / "ops", 1)
    monkeypatch.setattr(os, "fsync", lambda fd: time.sleep(0.2))  # past the deadline after the file
    folders: list = []
    monkeypatch.setattr(flusher_module, "fsync_directory", folders.append)
    assert fresh_flusher.flush(deadline=time.monotonic() + 0.1) == 1
    assert folders == [] and fresh_flusher._retry == [path], "the folder is still to do"
    assert fresh_flusher.flush() == 1 and folders == [str(tmp_path / "ops")]


def test_files_left_over_are_kept_even_while_a_writer_holds_the_list(tmp_path, monkeypatch, fresh_flusher):
    """Codex review: putting unfinished files back needed the writers' lock; a writer holding
    it (a frame SIGTERM interrupted) made the flush drop them for good."""
    paths = _record(fresh_flusher, tmp_path / "ops", 2)
    monkeypatch.setattr(os, "fsync", lambda fd: time.sleep(0.2))
    assert fresh_flusher._lock.acquire(blocking=False)
    try:
        fresh_flusher.flush(deadline=time.monotonic() + 0.1)
    finally:
        fresh_flusher._lock.release()
    assert sorted(fresh_flusher._retry) == paths, "kept for the next flush, none dropped"


def test_a_backlog_in_flight_counts_too(tmp_path, interval, fresh_flusher):
    """Review of #3785, C2: the slow disk's backlog is the batch a flush took and has not got
    down yet, not only what was recorded since."""
    fresh_flusher._thread = threading.current_thread()
    _record(fresh_flusher, tmp_path / "ops", 3)
    fresh_flusher._take()
    assert fresh_flusher._in_flight and not fresh_flusher._paths
    assert fresh_flusher.can_defer_fsync() is True
    fresh_flusher._in_flight_since = time.monotonic() - flusher_module.BACKLOG_MAX_SECONDS - 0.1
    assert fresh_flusher.can_defer_fsync() is False, "its oldest waited too long"
    fresh_flusher._in_flight_since = time.monotonic()
    fresh_flusher._in_flight.extend(["x"] * (flusher_module.BACKLOG_MAX_FILES - 3))
    assert fresh_flusher.can_defer_fsync() is False, "too many in flight"


#: A process that installed the SIGTERM close, recorded three op files and is flushing them on
#: its main thread through a slow disk (1 s per fsync) when SIGTERM lands. No run is open, so the
#: handler takes `_die()`; QA reproduced the hang twice on 0.357.0 (review C1).
_SIGTERM_MID_FLUSH = """
import os, sys, threading, time
os.environ["PROBE_SIGTERM_FLUSH_SECONDS"] = "4"
from probe.sdk.run.launch import preempt
from probe.sdk.delivery.journal import flusher as flusher_module

assert preempt.install(), "handler not installed"
flusher = flusher_module.get_journal_flusher()
work = sys.argv[1]
for i in range(3):
    path = os.path.join(work, f"op-{i}.json")
    with open(path, "w") as handle:
        handle.write("{}\\n")
    flusher.record(path)
real_fsync = os.fsync

def slow_fsync(fd):
    time.sleep(1.0)  # a slow disk: NFS, a busy cluster filesystem
    return real_fsync(fd)

os.fsync = slow_fsync
threading.Timer(0.3, lambda: os.kill(os.getpid(), 15)).start()
flusher.flush()
print("survived SIGTERM", flush=True)
"""


@pytest.mark.skipif(os.name != "posix", reason="the SIGTERM close is POSIX-only")
def test_a_sigterm_during_a_main_thread_flush_still_ends_the_process(tmp_path):
    """Review C1: `_die()` flushed through the lock the interrupted frame held; the process
    never exited. It must die of SIGTERM within a few seconds, whatever the disk does."""
    import signal
    import subprocess
    import sys

    started = time.monotonic()
    child = subprocess.Popen([sys.executable, "-c", _SIGTERM_MID_FLUSH, str(tmp_path)], stdout=subprocess.PIPE)
    try:
        code = child.wait(timeout=15)
    except subprocess.TimeoutExpired:
        child.kill()
        child.wait()
        code = None
    took = time.monotonic() - started
    assert code == -signal.SIGTERM, f"ended with {code!r} after {took:.1f} s (None: hung, killed by the test)"
    assert took < 8.0, took


# -- the loop's cadence, the batch a signal sees, a flusher that never started (final review) --------


def test_a_flush_taking_its_batch_never_hides_a_file_from_a_signal(tmp_path, fresh_flusher):
    """SIGTERM landing inside `_take` between clearing the lists and publishing `_in_flight`
    left the dying flush (which copies all three) with none of those files to sync."""
    import sys

    paths = _record(fresh_flusher, tmp_path / "ops", 2)
    fresh_flusher._retry, fresh_flusher._retry_since = [paths[0]], time.monotonic()
    fresh_flusher._paths[:] = [paths[1]]
    seen: list = []

    def visible() -> set:
        return set(fresh_flusher._retry) | set(fresh_flusher._in_flight) | set(fresh_flusher._paths)

    def tracer(frame, event, arg):
        if frame.f_code is not JournalFlusher._take.__code__:
            return None
        if event == "line":
            seen.append(visible())  # what a signal arriving before this line would find
        return tracer

    previous = sys.gettrace()  # coverage's or a debugger's: put back, not dropped
    sys.settrace(tracer)
    try:
        fresh_flusher._take()
    finally:
        sys.settrace(previous)
    seen.append(visible())
    assert seen and all(found == set(paths) for found in seen), seen


def test_the_flusher_waits_from_the_oldest_file_not_from_its_last_flush(tmp_path, fresh_flusher, monkeypatch):
    """The loop slept a whole second AFTER each flush, so the oldest file was (that flush's time
    + 1 s) old when the next one began, and the 2 s age cap sent `log()` back to its own fsync
    while the flusher was keeping up. It flushes once the oldest waiting file is a second old."""
    _record(fresh_flusher, tmp_path / "ops", 1)
    fresh_flusher._paths_since = time.monotonic() - 0.6  # recorded while the last flush ran
    fresh_flusher._work.set()
    pauses: list = []

    class Stop(BaseException):
        pass

    def tick(timeout=None):
        pauses.append(timeout)
        raise Stop

    monkeypatch.setattr(fresh_flusher._tick, "wait", tick)
    with pytest.raises(Stop):
        fresh_flusher._loop()
    assert pauses and pauses[0] <= flusher_module.FLUSH_EVERY_SECONDS - 0.5, pauses


def test_a_flusher_that_never_started_still_syncs_what_it_left(tmp_path, interval, fresh_flusher, monkeypatch):
    """A flusher whose thread could not start syncs the write in place, but a file whose fsync
    failed there sat in `_retry` for good: later writes fsync their own and never looked at it,
    and no exit flush was registered. The exit flush is registered first now, and a later write
    retries what is left."""

    def refuse(self):
        raise RuntimeError("can't create new thread at interpreter shutdown")

    monkeypatch.setattr(flusher_module.threading.Thread, "start", refuse)
    failing = {"left": 1}
    real_fsync = os.fsync

    def fsync(fd):
        if failing["left"]:
            failing["left"] -= 1
            raise OSError(5, "Input/output error")
        return real_fsync(fd)

    monkeypatch.setattr(os, "fsync", fsync)
    [path] = _record(fresh_flusher, tmp_path / "ops", 1)
    fresh_flusher._paths.clear()
    fresh_flusher.record(path)
    assert fresh_flusher._retry == [path], "the failed fsync is kept for one more try"
    assert fresh_flusher.registered == [fresh_flusher._flush_at_exit], "and the exit flush is registered"
    assert fresh_flusher.can_defer_fsync() is False
    assert fresh_flusher._retry == [], "the next write retried it"


def test_a_flusher_wakes_early_on_a_fast_disk_before_the_count_cap(tmp_path, interval, fresh_flusher):
    """A loop logging ~1,000 ops/s filled the 1,000-file cap before the flusher's one-second
    wait ended, so every `log()` fsynced its own op for the rest of each second though the disk
    kept up. The flusher is woken once half the cap waits."""
    fresh_flusher._thread = threading.current_thread()  # alive; nothing flushes in this test
    folder = tmp_path / "ops"
    folder.mkdir()
    half = flusher_module.BACKLOG_MAX_FILES // 2
    for index in range(half):
        if index == half - 1:
            assert not fresh_flusher._tick.is_set(), "woken before half the cap"
        path = folder / f"op-{index}.json"
        path.write_text("{}\n")
        fresh_flusher.record(str(path))
    assert fresh_flusher._tick.is_set(), "half the cap waits and the flusher was not woken"

def test_an_interrupted_flush_keeps_what_it_took(tmp_path, fresh_flusher, monkeypatch):
    """Ctrl-C inside a flush (finish()'s, on the main thread) after `_take` emptied the lists:
    the `finally` dropped the whole batch, so those files were never fsynced by anyone."""
    paths = _record(fresh_flusher, tmp_path / "ops", 3)
    calls = {"n": 0}

    def fsync(fd):
        calls["n"] += 1
        if calls["n"] == 2:
            raise KeyboardInterrupt

    monkeypatch.setattr(os, "fsync", fsync)
    with pytest.raises(KeyboardInterrupt):
        fresh_flusher.flush()
    kept = set(fresh_flusher._retry) | set(fresh_flusher._paths)
    assert set(paths[1:]) <= kept, (paths, kept)


#: As `_SIGTERM_MID_FLUSH`, but the disk never answers: every fsync blocks for good (a hung
#: network mount). SIGTERM's default action must still end the process.
_SIGTERM_STALLED_DISK = """
import os, sys, threading
os.environ["PROBE_SIGTERM_FLUSH_SECONDS"] = "4"
from probe.sdk.run.launch import preempt
from probe.sdk.delivery.journal import flusher as flusher_module

assert preempt.install(), "handler not installed"
flusher = flusher_module.get_journal_flusher()
work = sys.argv[1]
for i in range(3):
    path = os.path.join(work, f"op-{i}.json")
    with open(path, "w") as handle:
        handle.write("{}\\n")
    flusher.record(path)
os.fsync = lambda fd: threading.Event().wait()
threading.Timer(0.3, lambda: os.kill(os.getpid(), 15)).start()
flusher.flush()
print("survived SIGTERM", flush=True)
"""


@pytest.mark.skipif(os.name != "posix", reason="the SIGTERM close is POSIX-only")
def test_a_sigterm_on_a_stalled_disk_still_ends_the_process(tmp_path):
    """Final review of #3794 (Codex): `_die()` flushed on the thread that must end the process,
    and an fsync a stalled disk never answers kept SIGTERM's default action from ever running.
    The dying flush runs on a thread of its own, waited for at most `_DIE_FLUSH_SECONDS`."""
    import signal
    import subprocess
    import sys

    started = time.monotonic()
    child = subprocess.Popen([sys.executable, "-c", _SIGTERM_STALLED_DISK, str(tmp_path)], stdout=subprocess.PIPE)
    try:
        code = child.wait(timeout=15)
    except subprocess.TimeoutExpired:
        child.kill()
        child.wait()
        code = None
    took = time.monotonic() - started
    assert code == -signal.SIGTERM, f"ended with {code!r} after {took:.1f} s (None: hung, killed by the test)"
    assert took < 8.0, took


#: `_die()` runs inside the SIGTERM handler, which may interrupt `threading.enumerate()` or
#: `Thread.start()` while it holds `threading`'s limbo lock: the dying flush's thread start must
#: still return there and its wait stay bounded (preempt DESIGN.md, RE-ENTRANCY).
_DIE_FLUSH_UNDER_THREADING_LOCK = """
import os, sys, threading, time
from probe.sdk.run.launch import preempt
from probe.sdk.delivery.journal import flusher as flusher_module

assert preempt.install(), "handler not installed"
flusher = flusher_module.get_journal_flusher()
work = sys.argv[1]
for i in range(3):
    path = os.path.join(work, f"op-{i}.json")
    with open(path, "w") as handle:
        handle.write("{}\\n")
    flusher._paths.append(path)  # recorded: only the dying flush syncs them
flusher._paths_since = time.monotonic()
flusher._loop = lambda: threading.Event().wait()  # a live flusher thread that never flushes,
flusher._start()  # as in production, so the flush asks which thread it is on
synced = []
real_fsync = os.fsync
os.fsync = lambda fd: synced.append(fd) or real_fsync(fd)
with threading._active_limbo_lock:
    preempt._flush_journal_bounded(time.monotonic() + 2.0)
    print(f"returned synced={len(synced)}", flush=True)
"""


@pytest.mark.skipif(os.name != "posix", reason="the SIGTERM close is POSIX-only")
def test_the_dying_flush_returns_while_the_handler_holds_threadings_lock(tmp_path):
    """Final review of #3794 (red team): the dying flush's thread is started inside the handler,
    whose interrupted frame may hold `threading`'s limbo lock. The start returns, the wait stays
    bounded, and the flush runs anyway (convergence review: a `threading` thread, or one asking
    `current_thread()`, waited on that lock and synced nothing)."""
    import subprocess
    import sys

    try:
        out = subprocess.run(
            [sys.executable, "-c", _DIE_FLUSH_UNDER_THREADING_LOCK, str(tmp_path)],
            capture_output=True, text=True, timeout=15,
        ).stdout
    except subprocess.TimeoutExpired:
        out = "hung"
    assert "returned synced=" in out, out
    assert int(out.split("synced=")[1].split()[0]) >= 3, out



def test_a_file_that_keeps_failing_its_fsync_never_sticks_the_backlog(tmp_path, interval, fresh_flusher, monkeypatch):
    """A failed fsync's file went back with the batch's OLD age, so on a disk failing fsync the
    retry list stayed "older than 2 s" for good: the flusher looped without a pause and every
    `log()` went to an inline fsync that fails on that disk, dropping the write. A file put back
    is aged from when it was put back."""
    fresh_flusher._thread = threading.current_thread()
    [path] = _record(fresh_flusher, tmp_path / "ops", 1)
    fresh_flusher._paths_since = time.monotonic() - 5.0  # recorded long ago

    def failing(fd):
        raise OSError(5, "Input/output error")

    monkeypatch.setattr(os, "fsync", failing)
    fresh_flusher.flush()
    assert fresh_flusher._retry == [path]
    assert fresh_flusher.can_defer_fsync() is True, "one fresh retry is no backlog"
    assert fresh_flusher._get_pause() > 0.5, "and the flusher does not spin on it"


def test_a_ctrl_c_as_a_flush_takes_its_batch_keeps_it(tmp_path, fresh_flusher, monkeypatch):
    """`_take()` ran outside the guard that puts an interrupted batch back: a Ctrl-C landing
    inside it, after the lists were moved to `_in_flight`, lost them to the `finally`."""
    paths = _record(fresh_flusher, tmp_path / "ops", 2)

    def interrupted():
        raise KeyboardInterrupt

    monkeypatch.setattr(fresh_flusher._work, "clear", interrupted)
    with pytest.raises(KeyboardInterrupt):
        fresh_flusher.flush()
    kept = set(fresh_flusher._retry) | set(fresh_flusher._paths) | set(fresh_flusher._in_flight)
    assert set(paths) <= kept, kept


@pytest.mark.parametrize(
    "error, torn",
    [
        (OSError(24, "Too many open files"), 0),
        (FileNotFoundError(2, "No such file or directory"), 0),
        (PermissionError(13, "Permission denied"), 1),
        (OSError(5, "I/O error"), 1),
    ],
    ids=["EMFILE", "ENOENT", "EACCES", "EIO"],
)
def test_an_unreadable_dead_letter_is_torn_only_when_it_stays_unreadable(tmp_path, monkeypatch, error, torn):
    """A file that cannot be read right now (EMFILE: too many open files) is not torn. One that
    stays unreadable (EACCES, EIO) is what `quarantine_paths` moved here as torn, and skipping it
    left it in no count at all of `probe outbox status` (red team, convergence review)."""
    from pathlib import Path

    journal = Journal(tmp_path / "outbox")
    journal._ensure()
    (journal.failed_dir / "000000000001-00000000000000000001-0000beef.json").write_text("{}")
    real = Path.read_text

    def refusing(self, *args, **kwargs):
        if self.parent == journal.failed_dir:
            raise error
        return real(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", refusing)
    assert journal.read_failed() == ([], torn)


def test_the_dying_flush_skips_rather_than_flush_on_the_dying_thread(monkeypatch):
    """No thread to be had (a thread limit): flushing in place put a stalled fsync back on the
    thread that must end the process. The process now dies without that flush."""
    from probe.sdk.run.launch import preempt

    flushed: list = []
    monkeypatch.setattr(preempt, "_flush_journal", lambda **kw: flushed.append(kw))

    def refuse(self):
        raise RuntimeError("can't start new thread")

    import _thread

    monkeypatch.setattr(preempt.threading.Thread, "start", refuse)
    monkeypatch.setattr(_thread, "start_new_thread", lambda *a, **k: refuse(None))
    preempt._flush_journal_bounded(time.monotonic() + 0.2)
    assert flushed == []


# -- convergence review of #3804 ------------------------------------------------------------------


def test_a_batch_is_as_old_as_its_oldest_file_not_its_last_put_back(tmp_path, fresh_flusher):
    """`_take` aged the in-flight batch by the retry list's stamp whenever there was one, and a
    file put back is stamped when it is put back: a batch holding files recorded earlier read
    younger than it was, so the 2 s age cap tripped late on a disk that keeps failing fsyncs."""
    retried, recorded = _record(fresh_flusher, tmp_path / "ops", 2)
    oldest = time.monotonic() - 1.5
    fresh_flusher._paths[:], fresh_flusher._paths_since = [recorded], oldest
    fresh_flusher._retry, fresh_flusher._retry_since = [retried], time.monotonic() - 0.1
    fresh_flusher._take()
    assert fresh_flusher._in_flight_since == oldest


def test_a_ctrl_c_as_a_flush_puts_back_what_it_left_keeps_it(tmp_path, fresh_flusher, monkeypatch):
    """The put-back of the files a flush left (a deadline, a failed fsync) ran outside the guard
    that keeps an interrupted batch: a Ctrl-C landing there lost them to the `finally`."""
    paths = _record(fresh_flusher, tmp_path / "ops", 2)
    monkeypatch.setattr(fresh_flusher, "_sync", lambda batch, deadline: (0, list(batch)))
    real_put_back = fresh_flusher._put_back
    calls = {"n": 0}

    def put_back(left):
        calls["n"] += 1
        if calls["n"] == 1:
            raise KeyboardInterrupt  # as the put-back starts
        return real_put_back(left)

    monkeypatch.setattr(fresh_flusher, "_put_back", put_back)
    with pytest.raises(KeyboardInterrupt):
        fresh_flusher.flush()
    assert set(paths) <= set(fresh_flusher._retry) | set(fresh_flusher._paths), fresh_flusher._retry


def test_a_flush_whose_deadline_passed_leaves_every_list_alone(tmp_path, fresh_flusher):
    """A flush that may start no fsync still took the batch and put it back: run beside a dying
    flush's copy of the three lists (the SIGTERM close's, after its deadline), the files moved
    under the copy and it could find none of them."""
    paths = _record(fresh_flusher, tmp_path / "ops", 2)
    since = fresh_flusher._paths_since
    assert fresh_flusher.flush(deadline=time.monotonic() - 0.01) == 0
    assert fresh_flusher._paths == paths and fresh_flusher._paths_since == since
    assert fresh_flusher._retry == [] and fresh_flusher._in_flight == []


def test_the_sigterm_close_starts_no_thread(monkeypatch):
    """The handler waits for the close while the frame it interrupted may hold `threading`'s
    limbo lock (inside `Thread.start()` or `threading.enumerate()`): a close that starts a
    thread waits on that lock to the deadline, and its flush never runs (native adversarial)."""
    from probe.sdk.run.launch import preempt

    monkeypatch.setattr(preempt, "_state", preempt._State())
    monkeypatch.setattr(preempt, "_close_runs", lambda: None)
    flushed: list = []
    monkeypatch.setattr(preempt, "_flush_journal", lambda **kw: flushed.append(kw))
    preempt._state.ending = preempt.Ending(15, time.monotonic() + 5.0, 143)
    ready, go = threading.Event(), threading.Event()

    def close() -> None:
        ready.set()
        if go.wait(5):
            preempt._close()

    closer = threading.Thread(target=close, daemon=True)
    closer.start()
    assert ready.wait(5)
    with threading._active_limbo_lock:  # held, as by the main thread the signal interrupted
        go.set()
        finished = preempt._state.done.wait(2.0)
    closer.join(10)
    assert finished, "the close waited on threading's lock"
    assert len(flushed) == 1


@pytest.mark.parametrize("stuck", ["close", "flush"])
def test_an_unanswered_sigterm_close_ends_the_process_by_its_deadline(monkeypatch, stuck):
    """With the main thread stuck in a C call the worker's close is the only way out, and it
    ended the process only once the close returned: a close stuck on what that thread holds
    (the journal's append lock around an inline fsync) or in a stalled fsync never reached
    `os._exit` (red team). The close runs on a side thread, waited for until the deadline."""
    from probe.sdk.run.launch import preempt

    stalled, exited = threading.Event(), threading.Event()
    monkeypatch.setattr(preempt, "_state", preempt._State())
    monkeypatch.setattr(preempt, "_close_runs", lambda: stalled.wait(30) if stuck == "close" else None)
    monkeypatch.setattr(preempt, "_flush_journal", lambda **kw: stalled.wait(30) if stuck == "flush" else None)
    monkeypatch.setattr(preempt, "_note", lambda message: None)
    monkeypatch.setattr(preempt.os, "_exit", lambda code: exited.set())
    preempt._state.ending = preempt.Ending(15, time.monotonic() + 0.3, None)
    closer = threading.Thread(target=preempt._close_unanswered, daemon=True)
    closer.start()
    try:
        assert exited.wait(3.0), "the unanswered close never reached os._exit"
    finally:
        stalled.set()
        closer.join(5)


#: As `_SIGTERM_STALLED_DISK`, and a SIGINT (a Ctrl-C, torch's parent death signal) lands while
#: the dying flush is waited for: the process must still die of SIGTERM.
_SIGINT_WHILE_DYING = _SIGTERM_STALLED_DISK.replace(
    "threading.Timer(0.3, lambda: os.kill(os.getpid(), 15)).start()",
    "threading.Timer(0.3, lambda: os.kill(os.getpid(), 15)).start()\n"
    "threading.Timer(0.6, lambda: os.kill(os.getpid(), 2)).start()",
)


@pytest.mark.skipif(os.name != "posix", reason="the SIGTERM close is POSIX-only")
def test_a_sigint_while_dying_still_ends_the_process_by_sigterm(tmp_path):
    """The dying flush's wait let a SIGINT's KeyboardInterrupt out of `_die()`: the process
    unwound instead of dying, and as `_DYING` ignored every later SIGTERM (red team)."""
    import signal
    import subprocess
    import sys

    assert "os.kill(os.getpid(), 2)" in _SIGINT_WHILE_DYING
    child = subprocess.Popen([sys.executable, "-c", _SIGINT_WHILE_DYING, str(tmp_path)], stdout=subprocess.PIPE)
    try:
        code = child.wait(timeout=15)
    except subprocess.TimeoutExpired:
        child.kill()
        child.wait()
        code = None
    assert code == -signal.SIGTERM, f"ended with {code!r} (None: hung, killed by the test)"


def test_a_dead_letter_that_is_not_utf8_is_skipped_not_raised(tmp_path):
    """`quarantine_paths` moves a file that is not even UTF-8 into failed/ (any ValueError), and
    `failed()`, which `finish()` reads, let its UnicodeDecodeError out while `read_failed` counts
    the same file torn (native adversarial, maintainability)."""
    journal = Journal(tmp_path / "outbox")
    journal._ensure()
    (journal.failed_dir / "000000000001-00000000000000000001-0000beef.json").write_bytes(b"\xff{")
    assert journal.failed() == []
    assert journal.read_failed() == ([], 1)


def _unanswered_close(monkeypatch, *, close_runs) -> tuple:
    """`_close_unanswered` on a thread of its own, held at a start line; `os._exit` recorded."""
    from probe.sdk.run.launch import preempt

    exited, go = threading.Event(), threading.Event()
    monkeypatch.setattr(preempt, "_state", preempt._State())
    monkeypatch.setattr(preempt, "_close_runs", close_runs)
    monkeypatch.setattr(preempt, "_flush_journal", lambda **kw: None)
    monkeypatch.setattr(preempt, "_note", lambda message: None)
    monkeypatch.setattr(preempt.os, "_exit", lambda code: exited.set())
    preempt._state.ending = preempt.Ending(15, time.monotonic() + 0.5, None)
    ready = threading.Event()

    def run() -> None:
        ready.set()
        if go.wait(5):
            preempt._close_unanswered()

    closer = threading.Thread(target=run, daemon=True)
    closer.start()
    assert ready.wait(5)
    return closer, go, exited


def test_an_unanswered_close_ends_the_process_while_the_stuck_thread_holds_threadings_lock(monkeypatch):
    """The stuck main thread's interrupted frame may hold `threading`'s limbo lock (a SIGTERM inside
    `threading.enumerate()`, then a chained handler stuck in a collective), and the side thread the
    unanswered close started through `Thread.start()` waited on it with no timeout: `os._exit` was
    never reached (maintainability, testing, Codex adversarial)."""
    closer, go, exited = _unanswered_close(monkeypatch, close_runs=lambda: None)
    with threading._active_limbo_lock:  # held, as by the stuck main thread
        go.set()
        has_exited = exited.wait(2.0)
    closer.join(10)
    assert has_exited, "the unanswered close waited on threading's lock"


def test_an_unanswered_close_with_no_thread_to_be_had_ends_the_process_without_it(monkeypatch):
    """With no thread to be had the close ran on the only thread that can end the process, and a
    close blocked on what the stuck thread holds kept it alive past the deadline (Codex
    adversarial). No thread: no close, and the process ends."""
    import _thread

    from probe.sdk.run.launch import preempt

    closed: list = []
    stalled = threading.Event()
    closer, go, exited = _unanswered_close(
        monkeypatch, close_runs=lambda: closed.append(True) or stalled.wait(30)
    )

    def refuse(*args, **kwargs):
        raise RuntimeError("can't start new thread")

    monkeypatch.setattr(preempt.threading.Thread, "start", refuse)
    monkeypatch.setattr(_thread, "start_new_thread", refuse)
    go.set()
    try:
        assert exited.wait(3.0), "the close ran inline and held the process"
        assert closed == []
    finally:
        stalled.set()
        closer.join(10)


#: SIGTERM with no run open (the default action), and a SIGINT that lands while dying outside any
#: wait: the process must still die of SIGTERM.
_SIGINT_OUTSIDE_A_WAIT = """
import os, signal, sys, time
os.environ["PROBE_SIGTERM_FLUSH_SECONDS"] = "4"
from probe.sdk.run.launch import preempt

assert preempt.install(), "handler not installed"

def interrupted(deadline):
    os.kill(os.getpid(), signal.SIGINT)  # handled at the next bytecodes, inside no wait
    for _ in range(200000):
        pass

preempt._flush_journal_bounded = interrupted
os.kill(os.getpid(), signal.SIGTERM)
time.sleep(5)
print("survived SIGTERM", flush=True)
"""


@pytest.mark.skipif(os.name != "posix", reason="the SIGTERM close is POSIX-only")
def test_a_sigint_anywhere_in_dying_still_ends_the_process_by_sigterm():
    """Guarding the waits left every other bytecode of dying open to a SIGINT's
    KeyboardInterrupt (Codex adversarial, native adversarial): dying ignores SIGINT from its start."""
    import signal
    import subprocess
    import sys

    try:
        code = subprocess.run([sys.executable, "-c", _SIGINT_OUTSIDE_A_WAIT], capture_output=True, timeout=15).returncode
    except subprocess.TimeoutExpired:
        code = None
    assert code == -signal.SIGTERM, f"ended with {code!r} (None: hung, killed by the test)"


def test_a_note_never_holds_the_process_on_a_stderr_nobody_reads(monkeypatch):
    """`_note` wrote straight to fd 2 on the thread that must end the process: a stderr pipe nobody
    reads blocked it there, before `_die()` or `os._exit` (native adversarial)."""
    from probe.sdk.run.launch import preempt

    blocked = threading.Event()

    class BlockingWrites:
        def __getattr__(self, name):
            return getattr(os, name)

        @staticmethod
        def write(fd, data):
            blocked.wait(30)
            return len(data)

    monkeypatch.setattr(preempt, "os", BlockingWrites())
    started = time.monotonic()
    try:
        preempt._note("probe: a note\n")
        assert time.monotonic() - started < 2.0, "the note waited on a stderr nobody reads"
    finally:
        blocked.set()


#: A run open (a stand-in), a close that returns at once, and a stdout whose flush never returns
#: (buffered output to a pipe nobody reads): SIGTERM's default action must still end the process.
_SIGTERM_WITH_A_STUCK_STDOUT = """
import os, sys, threading, time
os.environ["PROBE_SIGTERM_FLUSH_SECONDS"] = "2"
from probe.sdk.run.launch import preempt

assert preempt.install(), "handler not installed"

class OpenRun:
    def _has_open_run(self):
        return True

class StuckStream:
    def write(self, text):
        return len(text)

    def flush(self):
        threading.Event().wait()

preempt._fluent = OpenRun()
preempt._close_runs = lambda: None
sys.stdout = StuckStream()
os.kill(os.getpid(), 15)
time.sleep(10)
"""

#: As above with a close that never finishes, and a SIGINT that lands in the takeover, after the
#: close's wait and outside any wait: the process must still die of SIGTERM.
_SIGINT_IN_THE_TAKEOVER = """
import os, signal, time
os.environ["PROBE_SIGTERM_FLUSH_SECONDS"] = "2"
from probe.sdk.run.launch import preempt

assert preempt.install(), "handler not installed"

class OpenRun:
    def _has_open_run(self):
        return True

def noted(message):
    os.kill(os.getpid(), signal.SIGINT)  # handled at the next bytecodes, in the takeover
    for _ in range(200000):
        pass

preempt._fluent = OpenRun()
preempt._close_runs = lambda: time.sleep(10)
preempt._note = noted
os.kill(os.getpid(), signal.SIGTERM)
time.sleep(10)
"""


@pytest.mark.skipif(os.name != "posix", reason="the SIGTERM close is POSIX-only")
@pytest.mark.parametrize(
    "script", [_SIGTERM_WITH_A_STUCK_STDOUT, _SIGINT_IN_THE_TAKEOVER], ids=["stuck-stdout", "sigint-in-takeover"]
)
def test_a_sigterm_close_ends_the_process_by_sigterm_whatever_holds_it(script):
    """Pass 3 (Codex and native adversarial, testing specialist): `_die()` flushed stdout and
    stderr inline on the thread that must end the process, so a stream whose flush never returns
    kept it alive; and nothing showed that the takeover's own SIGINT guard holds."""
    import signal
    import subprocess
    import sys

    try:
        code = subprocess.run([sys.executable, "-c", script], capture_output=True, timeout=15).returncode
    except subprocess.TimeoutExpired:
        code = None
    assert code == -signal.SIGTERM, f"ended with {code!r} (None: hung, killed by the test)"


#: As above with a stdout nobody blocks: the last line printed sits in its buffer (a pipe is
#: block-buffered), and SIGTERM's default action flushes nothing.
_SIGTERM_WITH_A_BUFFERED_LINE = """
import os, time
os.environ["PROBE_SIGTERM_FLUSH_SECONDS"] = "2"
from probe.sdk.run.launch import preempt

assert preempt.install(), "handler not installed"

class OpenRun:
    def _has_open_run(self):
        return True

preempt._fluent = OpenRun()
preempt._close_runs = lambda: None
print("the last line before the preemption")
os.kill(os.getpid(), 15)
time.sleep(10)
"""


@pytest.mark.skipif(os.name != "posix", reason="the SIGTERM close is POSIX-only")
def test_a_sigterm_close_still_delivers_the_last_buffered_output():
    """The dying flush of stdout and stderr, now on a side thread bounded to half a second, is
    what still hands the last lines to a reader that is alive (testing specialist, review of
    #3804's last five commits: with no flush at all every other SIGTERM test still passed)."""
    import signal
    import subprocess
    import sys

    out = subprocess.run(
        [sys.executable, "-c", _SIGTERM_WITH_A_BUFFERED_LINE], capture_output=True, text=True, timeout=15
    )
    assert out.returncode == -signal.SIGTERM, (out.returncode, out.stderr[-400:])
    assert "the last line before the preemption" in out.stdout, (out.stdout, out.stderr[-400:])
