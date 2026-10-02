"""`probe._shared.oscompat`: the lock, the pid probe and the binary flag the SDK
path uses, checked on the OS the suite runs on.

Listed in the OS matrix (os_matrix/os_sensitive_tests.txt), which is where these
earn their keep: on Linux every name is the POSIX call itself, so the file
mostly pins that the semantics the Windows branch copies are the ones callers
rely on. Real processes wherever a claim is about another process -- a lock
another process holds, a lease another process reads, a pid probe that must not
kill -- because a fake of the other side is exactly what would hide a Windows
difference.
"""

from __future__ import annotations

import os
import subprocess
import sys
import textwrap
import threading
import time

import pytest

from probe._shared import oscompat

# A child that takes the lock on argv[1], writes a lease body, prints "held",
# and keeps it until stdin closes.
_HOLDER = textwrap.dedent(
    """
    import sys
    from probe._shared import oscompat

    handle = open(sys.argv[1], "a+")
    oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
    handle.seek(0)
    handle.truncate()
    handle.write('{"pid": 4242}')
    handle.flush()
    print("held", flush=True)
    sys.stdin.read()
    """
)


def _holder(path) -> subprocess.Popen:
    child = subprocess.Popen(
        [sys.executable, "-c", _HOLDER, str(path)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    assert child.stdout is not None
    assert child.stdout.readline().strip() == "held"
    return child


def _release(child: subprocess.Popen) -> None:
    try:
        child.stdin.close()
        child.wait(timeout=30)
    finally:
        if child.poll() is None:
            child.kill()


def test_a_lock_another_process_holds_refuses_a_non_blocking_take(tmp_path):
    path = tmp_path / "lease.lock"
    child = _holder(path)
    try:
        with open(path, "a+") as handle:
            with pytest.raises(BlockingIOError):
                oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
    finally:
        _release(child)
    # Control: the holder is gone, so the same take succeeds.
    with open(path, "a+") as handle:
        oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        oscompat.flock(handle.fileno(), oscompat.LOCK_UN)


def test_a_held_lease_stays_readable_by_other_processes(tmp_path):
    """Windows locks are mandatory: a lock over the lease's own bytes would
    make its pid unreadable to everyone else (`_kill_workers`, `probe outbox
    status`). The lock sits past the content, so a reader gets the body."""
    path = tmp_path / "lease.lock"
    child = _holder(path)
    try:
        read = subprocess.run(
            [sys.executable, "-c", "import sys; print(open(sys.argv[1]).read())", str(path)],
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert read.returncode == 0, read.stderr
        assert read.stdout.strip() == '{"pid": 4242}'
    finally:
        _release(child)


def test_a_second_handle_in_the_same_process_conflicts(tmp_path):
    """flock is per open file description, so a probe that opens its own
    handle (`_lease_is_free`, `_flock_is_held`) reads a lock held by THIS
    process correctly. The Windows lock must be per handle too."""
    path = tmp_path / "item.lock"
    with open(path, "a+") as first, open(path, "a+") as second:
        oscompat.flock(first.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        with pytest.raises(BlockingIOError):
            oscompat.flock(second.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        oscompat.flock(first.fileno(), oscompat.LOCK_UN)
        oscompat.flock(second.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        oscompat.flock(second.fileno(), oscompat.LOCK_UN)


def test_a_blocking_take_waits_for_the_holder_and_then_holds(tmp_path):
    path = tmp_path / "append.lock"
    with open(path, "a+") as holder, open(path, "a+") as waiter:
        oscompat.flock(holder.fileno(), oscompat.LOCK_EX)
        threading.Timer(0.3, lambda: oscompat.flock(holder.fileno(), oscompat.LOCK_UN)).start()
        started = time.monotonic()
        oscompat.flock(waiter.fileno(), oscompat.LOCK_EX)
        waited = time.monotonic() - started
        assert 0.2 <= waited < 10, waited
        # It holds now: the first handle cannot take it back.
        with pytest.raises(BlockingIOError):
            oscompat.flock(holder.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        oscompat.flock(waiter.fileno(), oscompat.LOCK_UN)


def test_closing_the_handle_releases_the_lock(tmp_path):
    path = tmp_path / "worker.lock"
    first = open(path, "a+")
    oscompat.flock(first.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
    first.close()
    with open(path, "a+") as second:
        oscompat.flock(second.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)


def test_unlocking_an_unlocked_handle_is_a_no_op(tmp_path):
    with open(tmp_path / "x.lock", "a+") as handle:
        oscompat.flock(handle.fileno(), oscompat.LOCK_UN)


def test_locking_leaves_the_handle_where_it_was(tmp_path):
    """The Windows lock moves the descriptor to reach its byte; a lease its
    holder goes on writing (run_lock writes its pid after locking) must not
    notice."""
    path = tmp_path / "run.flock"
    with open(path, "w+") as handle:
        handle.write("abc")
        handle.flush()
        oscompat.flock(handle, oscompat.LOCK_EX | oscompat.LOCK_NB)  # a file object, as fcntl takes
        handle.write("def")
        handle.flush()
        oscompat.flock(handle, oscompat.LOCK_UN)
        handle.write("ghi")
    assert path.read_text() == "abcdefghi"


def test_probe_pid_finds_a_live_process_and_leaves_it_alive():
    """On Windows `os.kill(pid, 0)` is TerminateProcess(pid, 0): the check
    that a worker is alive killed it. The probe must leave it running."""
    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    try:
        oscompat.probe_pid(child.pid)
        time.sleep(0.2)
        assert child.poll() is None, f"the probe ended the process (rc={child.returncode})"
    finally:
        child.kill()
        child.wait(timeout=30)


def test_probe_pid_says_a_finished_process_is_gone():
    child = subprocess.Popen([sys.executable, "-c", "pass"])
    child.wait(timeout=60)
    with pytest.raises(ProcessLookupError):
        oscompat.probe_pid(child.pid)


def test_probe_pid_finds_this_process():
    oscompat.probe_pid(os.getpid())


def test_binary_descriptors_keep_every_byte(tmp_path):
    """`os.open` without O_BINARY is a TEXT descriptor on Windows: "\\n" is
    written as "\\r\\n" and a read stops at 0x1A. Upload copies and op files
    go through `os.open`."""
    payload = b"line\nnext\r\nctrl-z:\x1a:after\n"
    path = tmp_path / "blob"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | oscompat.O_BINARY, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(payload)
    assert path.read_bytes() == payload
    fd = os.open(path, os.O_RDONLY | oscompat.O_BINARY)
    try:
        assert os.read(fd, 1024) == payload
    finally:
        os.close(fd)


def test_replace_lands_once_a_reader_lets_go(tmp_path):
    """Windows refuses to rename onto a file another handle has open; the
    retry waits out a short read (a status.json poll) instead of failing the
    write. POSIX renames at once."""
    target = tmp_path / "status.json"
    target.write_text("old")
    source = tmp_path / "status.json.tmp"
    source.write_text("new")
    reader = open(target)
    threading.Timer(0.2, reader.close).start()
    oscompat.replace(source, target)
    assert target.read_text() == "new"
    assert not source.exists()


def test_a_detached_child_runs_on_its_own():
    """`DETACHED` is what the outbox worker spawns with: the child must start
    and exit normally under it on every OS."""
    child = subprocess.Popen(
        [sys.executable, "-c", "import sys; sys.exit(7)"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True,
        **oscompat.DETACHED,
    )
    assert child.wait(timeout=60) == 7
