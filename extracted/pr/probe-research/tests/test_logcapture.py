"""The tee behind `run.log`: exact bytes, exit codes, the cap, and never a hang.

`run_teed` is what `probe exec` runs the child through; `InProcessTee` is what
`probe.init()` swaps fds 1/2 for. The in-process cases run in a subprocess,
because pytest owns this process's file descriptors.
"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import threading
import time

import pytest

from probe.sdk.logcapture import (
    LIVE_UNSHIPPED_BYTES,
    CappedLog,
    LiveSpool,
    list_segments,
    live_dir,
    omitted_marker,
    pump,
    read_eof,
    run_teed,
)

PY = sys.executable

# The tee is POSIX-only by design: it swaps fds 1/2 for pipes or ptys read by a
# helper, and `outputs.in_process_log_supported()` keeps it off on Windows, where a run's
# folder is still captured but its console log is not.
pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="log tee is POSIX-only (outputs.in_process_log_supported)")


def test_the_tee_is_exact_and_keeps_the_streams_apart(tmp_path):
    child = tmp_path / "prog.py"
    child.write_text(
        "import sys, os\n"
        "sys.stdout.buffer.write(b'a\\r\\nb\\x00\\xff\\rprogress 1\\rprogress 2\\n'); sys.stdout.flush()\n"
        "os.write(2, b'ERR\\n')\n"
    )
    driver = tmp_path / "driver.py"
    driver.write_text(
        "import json, sys\n"
        "from probe.sdk.logcapture import run_teed\n"
        f"res, stats = run_teed([sys.executable, {str(child)!r}], log_path={str(tmp_path / 'run.log')!r})\n"
        "sys.stderr.write('RESULT ' + json.dumps({'rc': res.returncode, **stats}))\n"
    )
    proc = subprocess.run([PY, str(driver)], capture_output=True, timeout=60)
    assert proc.stdout == b"a\r\nb\x00\xff\rprogress 1\rprogress 2\n"  # terminal side, exact
    assert proc.stderr.startswith(b"ERR\n")  # stderr stays stderr
    log = (tmp_path / "run.log").read_bytes()
    assert log.count(b"ERR\n") == 1 and b"a\r\nb\x00\xff\rprogress 1\rprogress 2\n" in log


@pytest.mark.parametrize(("code", "expected"), [("0", 0), ("3", 3)])
def test_the_exit_code_is_kept(tmp_path, code, expected):
    child = tmp_path / "prog.py"
    child.write_text(f"import sys; print('hi'); sys.exit({code})\n")
    result, _stats = run_teed([PY, str(child)], log_path=str(tmp_path / "run.log"))
    assert result.returncode == expected


def test_a_child_that_aborts_is_reported_by_signal(tmp_path):
    child = tmp_path / "prog.py"
    child.write_text("import os; os.write(2, b'dying\\n'); os.abort()\n")
    result, _stats = run_teed([PY, str(child)], log_path=str(tmp_path / "run.log"))
    assert result.returncode == -6
    assert b"dying" in (tmp_path / "run.log").read_bytes()


def test_huge_output_keeps_head_and_tail(tmp_path):
    log = CappedLog(str(tmp_path / "run.log"), head_bytes=10, tail_bytes=20)
    for i in range(1000):
        log.write(f"line {i:04d}\n".encode())
    log.close()
    body = (tmp_path / "run.log").read_bytes()
    total = sum(len(f"line {i:04d}\n") for i in range(1000))
    assert body.startswith(b"line 0000\n")
    assert body.endswith(b"line 0998\nline 0999\n")
    assert omitted_marker(total - 30) in body
    assert log.stats() == {"total_bytes": total, "omitted_bytes": total - 30}


def test_under_the_cap_nothing_is_inserted(tmp_path):
    log = CappedLog(str(tmp_path / "run.log"), head_bytes=10, tail_bytes=100)
    log.write(b"short\r")
    log.write(b"and exact\n")
    log.close()
    assert (tmp_path / "run.log").read_bytes() == b"short\rand exact\n"


def test_a_failing_log_never_stops_the_forwarding(tmp_path):
    """Codex P1: a full disk under the log used to stop the reader, the pipe
    filled, and the child blocked forever."""

    class DiskFull:
        def write(self, data):
            raise OSError(28, "No space left on device")

    src_r, src_w = os.pipe()
    dst_r, dst_w = os.pipe()
    received = bytearray()
    reader = threading.Thread(target=lambda: received.extend(iter_read(dst_r)), daemon=True)
    reader.start()
    pumping = threading.Thread(target=pump, args=([(src_r, dst_w)], DiskFull()), daemon=True)
    pumping.start()
    payload = b"x" * (512 * 1024)  # far more than a pipe buffer

    def write_all():
        view = memoryview(payload)
        while view:
            view = view[os.write(src_w, view):]
        os.close(src_w)

    # In a thread: on the regression this guards, the write blocks forever,
    # and the test must fail rather than hang.
    writer = threading.Thread(target=write_all, daemon=True)
    writer.start()
    writer.join(10)
    assert not writer.is_alive(), "the pump stopped reading: the writer is blocked"
    pumping.join(10)
    os.close(dst_w)
    reader.join(10)
    assert not pumping.is_alive()
    assert bytes(received) == payload


def iter_read(fd):
    while True:
        chunk = os.read(fd, 65536)
        if not chunk:
            return
        yield from chunk


def test_in_process_capture_survives_a_hard_crash(tmp_path):
    """faulthandler's traceback before abort() is the output a person most
    needs; the helper process forwards and logs it after the run is gone."""
    script = tmp_path / "crash.py"
    script.write_text(
        "import os, faulthandler\n"
        "from probe.sdk.logcapture import InProcessTee\n"
        f"tee = InProcessTee({str(tmp_path / 'run.log')!r})\n"
        "tee.start()\n"
        "print('before', flush=True)\n"
        "os.write(1, b'c-level\\n')\n"
        "faulthandler.enable()\n"
        "os.abort()\n"
    )
    proc = subprocess.run([PY, str(script)], capture_output=True, timeout=60)
    assert proc.returncode != 0
    assert b"before" in proc.stdout and b"c-level" in proc.stdout
    assert b"Fatal Python error: Aborted" in proc.stderr
    import time

    deadline = time.monotonic() + 10
    while time.monotonic() < deadline and not os.path.exists(str(tmp_path / "run.log") + ".meta.json"):
        time.sleep(0.1)
    log = (tmp_path / "run.log").read_bytes()
    assert b"c-level" in log and b"Fatal Python error: Aborted" in log


def test_in_process_capture_stops_cleanly(tmp_path):
    script = tmp_path / "ok.py"
    script.write_text(
        "import json, os, subprocess, sys\n"
        "from probe.sdk.logcapture import InProcessTee\n"
        f"tee = InProcessTee({str(tmp_path / 'run.log')!r})\n"
        "tee.start()\n"
        "print('py', flush=True); os.write(2, b'fd2\\n')\n"
        "subprocess.run(['echo', 'from child'])\n"
        "stats = tee.stop()\n"
        "print('after-stop ' + json.dumps(stats))\n"
    )
    proc = subprocess.run([PY, str(script)], capture_output=True, timeout=60)
    assert proc.returncode == 0, proc.stderr
    log = (tmp_path / "run.log").read_bytes()
    assert b"py\n" in log and b"fd2\n" in log and b"from child\n" in log
    assert b"after-stop" not in log  # restored: nothing after stop() is captured
    assert b"after-stop" in proc.stdout and b'"omitted_bytes": 0' in proc.stdout
    assert os.path.exists(str(tmp_path / "run.log") + ".stopped")


# -- review fixes (PR #1959) ------------------------------------------------------------
def _wait_for(predicate, timeout=20.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.05)
    return False


def test_a_closed_reader_stops_the_writer_as_it_would_have(tmp_path):
    """`probe exec yes | head`: once head exits the writer must get EPIPE, not
    run on forever into a stream nobody reads."""
    src_r, src_w = os.pipe()
    dst_r, dst_w = os.pipe()
    os.close(dst_r)  # the reader is gone
    pumping = threading.Thread(target=pump, args=([(src_r, dst_w)], None), daemon=True)
    pumping.start()
    os.write(src_w, b"first\n")
    pumping.join(10)
    assert not pumping.is_alive()
    old = signal.signal(signal.SIGPIPE, signal.SIG_IGN)
    try:
        with pytest.raises(BrokenPipeError):
            for _ in range(100):
                os.write(src_w, b"x" * 4096)
    finally:
        signal.signal(signal.SIGPIPE, old)
        os.close(src_w)
        os.close(dst_w)


def test_a_background_process_keeps_its_output_after_exec_returns(tmp_path):
    """A command that leaves tensorboard running: after `probe exec` returns,
    the background process must keep a working stdout (the helper outlives
    exec), not die of SIGPIPE on its next line."""
    marker = tmp_path / "survived"
    driver = tmp_path / "driver.py"
    driver.write_text(
        "import sys\n"
        "from probe.sdk.logcapture import run_teed\n"
        "cmd = 'echo main; (sleep 1; echo late; touch " + str(marker) + ") &'\n"
        f"res, _ = run_teed(['sh', '-c', cmd], log_path={str(tmp_path / 'run.log')!r})\n"
        "print('exec returned', res.returncode, flush=True)\n"
    )
    proc = subprocess.run([PY, str(driver)], capture_output=True, timeout=60)
    assert b"exec returned 0" in proc.stdout
    assert b"late" in proc.stdout and marker.exists()


def test_the_helper_survives_scheduler_signals(tmp_path):
    """Slurm `--signal=USR1@90`, submitit's USR2, Ctrl-\\ reach every process
    of a job step. A helper that died of one turned the next print into
    BrokenPipeError."""
    script = tmp_path / "job.py"
    script.write_text(
        "import os, signal, time\n"
        "from probe.sdk.logcapture import InProcessTee\n"
        f"tee = InProcessTee({str(tmp_path / 'run.log')!r})\n"
        "tee.start()\n"
        "for sig in (signal.SIGUSR1, signal.SIGUSR2, signal.SIGQUIT, signal.SIGHUP, signal.SIGALRM):\n"
        "    os.kill(tee.helper_pid, sig)\n"
        "time.sleep(0.5)\n"
        "print('still printing', flush=True)\n"
        "tee.stop()\n"
    )
    proc = subprocess.run([PY, str(script)], capture_output=True, timeout=60)
    assert proc.returncode == 0, proc.stderr
    assert b"still printing" in proc.stdout
    assert b"still printing" in (tmp_path / "run.log").read_bytes()


def test_a_signal_that_kills_exec_does_not_kill_its_child(tmp_path):
    """SIGUSR1 kills `probe exec` (no handler, as before). Its child must keep
    a working stdout and finish -- not die of a closed pipe at its next line."""
    marker = tmp_path / "finished"
    child = tmp_path / "child.py"
    child.write_text(
        "import time\n"
        "for i in range(10):\n"
        "    print('step', i, flush=True); time.sleep(0.1)\n"
        f"open({str(marker)!r}, 'w').write('ok')\n"
    )
    driver = tmp_path / "driver.py"
    driver.write_text(
        "import sys\n"
        "from probe.sdk.logcapture import run_teed\n"
        f"run_teed([sys.executable, {str(child)!r}], log_path={str(tmp_path / 'run.log')!r})\n"
    )
    proc = subprocess.Popen([PY, str(driver)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Signal once the child is writing through the tee, not after a fixed
    # sleep: on a loaded runner 0.4 s could end `exec` before it started the
    # child at all (macOS py3.12, agent-os-matrix run 36409012762).
    first = proc.stdout.readline()
    assert first == b"step 0\n", first
    proc.send_signal(signal.SIGUSR1)
    out, _err = proc.communicate(timeout=60)  # EOF only once the child is done
    assert proc.returncode == -signal.SIGUSR1  # exec died as it always did
    assert marker.exists() and b"step 9" in first + out


def test_a_hard_crash_hands_the_record_to_a_recovery_process(tmp_path):
    """Under `subprocess.run(capture_output=True)` the crashed process stays an
    unreaped zombie while the launcher drains its pipes, and `kill(pid, 0)`
    still answers for a zombie. The helper must see the crash anyway."""
    entry = tmp_path / "rec.json"
    entry.write_text("{}")  # recover() deletes its entry even when it cannot finish
    script = tmp_path / "crash.py"
    script.write_text(
        "import os\n"
        "from probe.sdk.logcapture import InProcessTee\n"
        f"InProcessTee({str(tmp_path / 'run.log')!r}, recovery_entry={str(entry)!r}).start()\n"
        "print('x', flush=True)\n"
        "os.abort()\n"
    )
    subprocess.run([PY, str(script)], capture_output=True, timeout=60)
    assert _wait_for(lambda: not entry.exists()), "no recovery process ran"


def test_a_terminal_child_sees_a_terminal_and_the_log_gets_its_exact_bytes(tmp_path):
    """Through a pty, with OPOST cleared: isatty() stays true and no \\n turns
    into \\r\\n on the way to the terminal or the log."""
    import pty

    child = tmp_path / "child.py"
    child.write_text("import sys, os\nprint(sys.stdout.isatty(), flush=True)\nos.write(1, b'a' + bytes([10]) + b'b' + bytes([10]))\n")
    driver = tmp_path / "driver.py"
    driver.write_text(
        "import sys\n"
        "from probe.sdk.logcapture import run_teed\n"
        f"run_teed([sys.executable, {str(child)!r}], log_path={str(tmp_path / 'run.log')!r})\n"
    )
    master, slave = pty.openpty()
    proc = subprocess.Popen([PY, str(driver)], stdout=slave, stderr=slave, stdin=subprocess.DEVNULL)
    os.close(slave)
    seen = b""
    while True:
        try:
            chunk = os.read(master, 4096)
        except OSError:
            break
        if not chunk:
            break
        seen += chunk
    proc.wait(timeout=60)
    os.close(master)
    assert (tmp_path / "run.log").read_bytes() == b"True\na\nb\n"


def test_stdout_and_stderr_into_one_file_keep_their_order(tmp_path):
    """`> out.log 2>&1` is ONE stream: two pipes would let the tee reorder
    lines the program wrote in order."""
    child = tmp_path / "child.py"
    child.write_text(
        "import os\n"
        "for i in range(200):\n"
        "    os.write(1 if i % 2 == 0 else 2, f'{i}\\n'.encode())\n"
    )
    driver = tmp_path / "driver.py"
    driver.write_text(
        "import sys\n"
        "from probe.sdk.logcapture import run_teed\n"
        f"run_teed([sys.executable, {str(child)!r}], log_path={str(tmp_path / 'run.log')!r})\n"
    )
    with open(tmp_path / "out.log", "wb") as out:
        subprocess.run([PY, str(driver)], stdout=out, stderr=subprocess.STDOUT, timeout=60)
    expected = "".join(f"{i}\n" for i in range(200)).encode()
    assert (tmp_path / "out.log").read_bytes() == expected
    assert (tmp_path / "run.log").read_bytes() == expected


def test_stopping_leaves_the_programs_own_redirection_alone(tmp_path):
    script = tmp_path / "job.py"
    script.write_text(
        "import os\n"
        "from probe.sdk.logcapture import InProcessTee\n"
        f"tee = InProcessTee({str(tmp_path / 'run.log')!r})\n"
        "tee.start()\n"
        f"fd = os.open({str(tmp_path / 'mine.txt')!r}, os.O_WRONLY | os.O_CREAT)\n"
        "os.dup2(fd, 1)\n"
        "tee.stop()\n"
        "os.write(1, b'after stop')\n"
    )
    subprocess.run([PY, str(script)], capture_output=True, timeout=60)
    assert (tmp_path / "mine.txt").read_bytes() == b"after stop"


def test_a_tee_that_cannot_start_still_runs_the_command(tmp_path, monkeypatch):
    import probe.sdk.logcapture as logcapture

    def no_pipes(self):
        raise OSError(24, "Too many open files")

    monkeypatch.setattr(logcapture._Tee, "open", no_pipes)
    result, stats = run_teed([PY, "-c", "raise SystemExit(4)"], log_path=str(tmp_path / "run.log"))
    assert result.returncode == 4 and stats is None


# -- second review round (PR #1959) ------------------------------------------------------
def test_a_helper_that_dies_starting_is_never_handed_the_output(tmp_path):
    """An interpreter that cannot run the helper (`-I -S` on a relocated or
    embedded Python): the program must keep its own stdout, and a command under
    exec runs untouched, never told its output is logged."""
    child = tmp_path / "child.py"
    child.write_text("import os\nprint('child ok', os.environ.get('TEED') or 'not teed', flush=True)\n")
    script = tmp_path / "job.py"
    script.write_text(
        "import sys\n"
        f"real = sys.executable\n"
        "sys.executable = '/bin/false'  # the helper dies as it starts\n"
        "from probe.sdk.logcapture import InProcessTee, run_teed\n"
        f"tee = InProcessTee({str(tmp_path / 'a.log')!r})\n"
        "try:\n"
        "    tee.start()\n"
        "    print('started?!', flush=True)\n"
        "except OSError:\n"
        "    print('refused', flush=True)\n"
        "print('prints fine', flush=True)\n"
        f"res, stats = run_teed([real, {str(child)!r}], log_path={str(tmp_path / 'b.log')!r}, teed_env={{'TEED': '1'}})\n"
        "print('exec', res.returncode, stats, flush=True)\n"
    )
    proc = subprocess.run([PY, str(script)], capture_output=True, timeout=60)
    assert proc.returncode == 0, proc.stderr
    assert b"refused" in proc.stdout and b"prints fine" in proc.stdout
    assert b"child ok not teed" in proc.stdout and b"exec 0 None" in proc.stdout


def test_a_program_with_stdin_closed_keeps_its_stdout(tmp_path):
    """`python train.py <&-`: a new descriptor takes number 0, and the helper's
    stdin=DEVNULL used to land on it -- forwarding stdout into /dev/null."""
    child = tmp_path / "child.py"
    child.write_text("print('visible', flush=True)\n")
    driver = tmp_path / "driver.py"
    driver.write_text(
        "import sys\n"
        "from probe.sdk.logcapture import run_teed, InProcessTee\n"
        f"run_teed([sys.executable, {str(child)!r}], log_path={str(tmp_path / 'a.log')!r})\n"
        f"tee = InProcessTee({str(tmp_path / 'b.log')!r}); tee.start()\n"
        "print('in-process too', flush=True)\n"
        "tee.stop()\n"
    )
    out = tmp_path / "out.txt"
    subprocess.run(["sh", "-c", f"exec {PY} {driver} <&- > {out} 2>&1"], timeout=60)
    text = out.read_bytes()
    assert b"visible" in text and b"in-process too" in text


# -- live mode (plan item (h)): the spool a shipper streams from -----------------------
def _spooled(directory) -> bytes:
    return b"".join(open(path, "rb").read() for _start, path, _size in list_segments(str(directory)))


def test_live_segments_concatenate_to_the_exact_stream(tmp_path):
    """Every byte the program wrote, in order, split across 1 MiB segments
    named by their raw offset: the same bytes the terminal and the log got."""
    log_path = tmp_path / "run.log"
    os.makedirs(live_dir(str(log_path)))
    child = tmp_path / "prog.py"
    child.write_text(
        "import os, sys\n"
        "for i in range(2600):\n"
        "    sys.stdout.buffer.write(b'line %05d \\x00\\xff\\r' % i + b'x' * 1000 + b'\\n')\n"
        "sys.stdout.flush()\n"
        "os.write(2, b'stderr too\\n')\n"
    )
    result, stats = run_teed([PY, str(child)], log_path=str(log_path))
    assert result.returncode == 0 and stats["omitted_bytes"] == 0
    spool = live_dir(str(log_path))
    segments = list_segments(spool)
    assert len(segments) == 3  # ~2.6 MB in 1 MiB segments
    assert [start for start, _p, _s in segments] == [0, 1024 * 1024, 2 * 1024 * 1024]
    assert _spooled(spool) == log_path.read_bytes()
    assert read_eof(spool) == stats["total_bytes"]


def test_no_spool_directory_means_no_live_mode(tmp_path):
    log_path = tmp_path / "run.log"
    result, _stats = run_teed([PY, "-c", "print('hi')"], log_path=str(log_path))
    assert result.returncode == 0 and log_path.read_bytes() == b"hi\n"
    assert not os.path.exists(live_dir(str(log_path)))


def test_a_full_spool_drops_its_oldest_segments(tmp_path):
    spool = LiveSpool(str(tmp_path), segment_bytes=10, budget_bytes=35)
    data = bytes(range(100))
    spool.write(data)
    spool.close()
    segments = list_segments(str(tmp_path))
    kept = sum(size for _s, _p, size in segments)
    assert kept <= 35 and spool.dropped == 100 - kept
    oldest = segments[0][0]
    assert oldest == spool.dropped  # the jump in offsets IS the recorded gap
    assert _spooled(tmp_path) == data[oldest:]
    assert read_eof(str(tmp_path)) == 100


def test_budget_overflow_never_blocks_the_program(tmp_path):
    """Nothing reads the spool: 24 MiB still flow to the terminal at full
    speed, and the spool never holds more than its budget."""
    log_path = tmp_path / "run.log"
    os.makedirs(live_dir(str(log_path)))
    child = tmp_path / "prog.py"
    child.write_text(
        "import sys\n"
        "block = (b'y' * 1023 + b'\\n') * 1024\n"
        "for _ in range(24):\n"
        "    sys.stdout.buffer.write(block)\n"
    )
    driver = tmp_path / "driver.py"
    driver.write_text(
        "import json, sys, time\n"
        "from probe.sdk.logcapture import run_teed\n"
        "t = time.monotonic()\n"
        f"res, stats = run_teed([sys.executable, {str(child)!r}], log_path={str(log_path)!r})\n"
        "sys.stderr.write('RESULT ' + json.dumps({'rc': res.returncode, 'secs': time.monotonic() - t, **stats}))\n"
    )
    proc = subprocess.run([PY, str(driver)], capture_output=True, timeout=120)
    assert len(proc.stdout) == 24 * 1024 * 1024
    import json as _json

    result = _json.loads(proc.stderr.split(b"RESULT ", 1)[1])
    assert result["rc"] == 0 and result["total_bytes"] == 24 * 1024 * 1024
    spool = live_dir(str(log_path))
    held = sum(size for _s, _p, size in list_segments(spool))
    assert held <= LIVE_UNSHIPPED_BYTES
    assert read_eof(spool) == 24 * 1024 * 1024
    # What is left is the END of the stream, contiguous.
    assert _spooled(spool) == ((b"y" * 1023 + b"\n") * 1024 * 24)[-held:]


def test_a_spool_that_cannot_be_written_leaves_the_stream_and_the_log_alone(tmp_path):
    """A full disk under the spool (here: a spool directory the helper cannot
    write to) costs the live view only."""
    log_path = tmp_path / "run.log"
    spool = live_dir(str(log_path))
    os.makedirs(spool)
    os.chmod(spool, 0o500)
    try:
        result, stats = run_teed([PY, "-c", "print('still here')"], log_path=str(log_path))
    finally:
        os.chmod(spool, 0o700)
    assert result.returncode == 0 and log_path.read_bytes() == b"still here\n"
    assert stats["total_bytes"] == len(b"still here\n")


# -- SDK reliability 2.2: the helper reports its writer's death at once ----------


def _kill_pidfile(path) -> None:
    try:
        os.kill(int(path.read_text()), signal.SIGKILL)
    except (OSError, ValueError):
        pass


def _hard_death_with_a_grandchild(tmp_path, *, watch_parent: bool):
    """The run's process is SIGKILLed while a grandchild it started still holds
    its stdout: the helper sees no EOF, so only watching the parent can tell."""
    entry = tmp_path / "rec.json"
    entry.write_text("{}")
    pidfile = tmp_path / "grandchild.pid"
    script = tmp_path / "killed.py"
    script.write_text(
        "import os, signal, subprocess\n"
        "from probe.sdk.logcapture import InProcessTee\n"
        f"InProcessTee({str(tmp_path / 'run.log')!r}, recovery_entry={str(entry)!r}, "
        f"watch_parent={watch_parent!r}).start()\n"
        "print('training', flush=True)\n"
        "child = subprocess.Popen(['sleep', '30'])\n"
        f"open({str(pidfile)!r}, 'w').write(str(child.pid))\n"
        "os.kill(os.getpid(), signal.SIGKILL)\n"
    )
    # DEVNULL, not capture_output: a pipe would make this wait for the grandchild.
    proc = subprocess.run(
        [PY, str(script)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60
    )
    assert proc.returncode == -signal.SIGKILL
    return entry, pidfile


def test_a_killed_writer_is_reported_while_a_grandchild_holds_its_stdout(tmp_path):
    entry, pidfile = _hard_death_with_a_grandchild(tmp_path, watch_parent=True)
    gone = tmp_path / "rec.json.gone"
    try:
        started = time.monotonic()
        assert _wait_for(gone.exists, timeout=15.0), "no writer-gone report was started"
        # Seconds, not the reaper's 900: the helper polls its parent every 0.2 s
        # and the reporter claims the record before importing anything heavy.
        assert time.monotonic() - started < 15.0
    finally:
        _kill_pidfile(pidfile)


def test_without_the_watch_a_held_stdout_hides_the_death(tmp_path):
    """The control, and today's behaviour: recovery waits for EOF, which the
    grandchild never gives, so nothing is reported."""
    entry, pidfile = _hard_death_with_a_grandchild(tmp_path, watch_parent=False)
    try:
        time.sleep(3.0)
        assert not (tmp_path / "rec.json.gone").exists()
    finally:
        _kill_pidfile(pidfile)


def test_a_clean_stop_reports_no_death(tmp_path):
    entry = tmp_path / "rec.json"
    entry.write_text("{}")
    script = tmp_path / "ok.py"
    script.write_text(
        "import subprocess\n"
        "from probe.sdk.logcapture import InProcessTee\n"
        f"tee = InProcessTee({str(tmp_path / 'run.log')!r}, recovery_entry={str(entry)!r}, "
        "watch_parent=True)\n"
        "tee.start()\n"
        "print('done', flush=True)\n"
        "subprocess.Popen(['sleep', '2'])\n"  # still holds stdout after we exit
        "tee.stop()\n"
    )
    proc = subprocess.run(
        [PY, str(script)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60
    )
    assert proc.returncode == 0
    time.sleep(3.0)
    assert not (tmp_path / "rec.json.gone").exists()


def test_a_launchers_death_is_not_its_childs(tmp_path):
    """Under `run_teed` (probe exec) the helper's parent is the LAUNCHER; the
    child may still be writing, so its death is never reported as the run's."""
    entry = tmp_path / "rec.json"
    entry.write_text("{}")
    script = tmp_path / "launcher.py"
    script.write_text(
        "import os, signal, sys, threading, time\n"
        "from probe.sdk.logcapture import run_teed\n"
        "threading.Timer(0.5, lambda: os.kill(os.getpid(), signal.SIGKILL)).start()\n"
        f"run_teed([sys.executable, '-c', 'import time; time.sleep(2)'], "
        f"log_path={str(tmp_path / 'run.log')!r}, recovery_entry={str(entry)!r})\n"
    )
    proc = subprocess.run(
        [PY, str(script)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60
    )
    assert proc.returncode == -signal.SIGKILL
    time.sleep(4.0)
    assert not (tmp_path / "rec.json.gone").exists()
