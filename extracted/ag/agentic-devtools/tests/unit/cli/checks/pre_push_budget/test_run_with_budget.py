"""Streaming, exit status, and bounded process-group cleanup."""

import os
import subprocess
import sys
from pathlib import Path
from threading import Event, Thread
from unittest.mock import MagicMock, Mock, mock_open, patch

import pytest

from agentic_devtools.cli.checks import pre_push_budget

pytestmark = pytest.mark.skipif(os.name != "posix", reason="Budget execution requires POSIX process-group cleanup")


@pytest.mark.parametrize("status", [*range(11), 42])
def test_child_status_and_merged_output(status, tmp_path, capsys, monkeypatch):
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    log = tmp_path / "output"
    assert (
        pre_push_budget.run_with_budget(
            [
                sys.executable,
                "-u",
                "-c",
                f"import sys; print('stdout'); print('stderr', file=sys.stderr); sys.exit({status})",
            ],
            10,
            log,
        )
        == status
    )
    output = capsys.readouterr().out
    assert output.startswith("AGDT pre-push: cloud-agent budget 10s\n")
    assert "stdout" in output and "stderr" in output
    assert log.read_text() == output
    assert "GITHUB_ACTIONS=true\n" in output


def test_unset_actions_and_partial_invalid_output(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    log = tmp_path / "output"
    assert (
        pre_push_budget.run_with_budget(
            [sys.executable, "-c", "import os; os.write(1, b'partial\\xff')"],
            10,
            log,
        )
        == 0
    )
    assert "GITHUB_ACTIONS=<unset>" in log.read_text()
    assert log.read_text().endswith("partial\ufffd")
    assert capsys.readouterr().out == log.read_text()


@pytest.mark.parametrize("budget", [0, -1])
def test_invalid_budget_blocks(budget, tmp_path):
    with pytest.raises(ValueError):
        pre_push_budget.run_with_budget([sys.executable], budget, tmp_path / "output")


def test_launch_failure_blocks(tmp_path):
    with pytest.raises(OSError):
        pre_push_budget.run_with_budget([str(tmp_path / "missing")], 1, tmp_path / "output")


def test_completed_child_is_not_signalled(tmp_path):
    with patch.object(pre_push_budget.os, "killpg", side_effect=ProcessLookupError) as killpg:
        status = pre_push_budget.run_with_budget(
            [sys.executable, "-c", "pass"],
            10,
            tmp_path / "output",
        )
    assert status == 0
    killpg.assert_called_once_with(killpg.call_args.args[0], 0)


def test_observed_failure_breaks_inherited_pipe_wait(tmp_path):
    read_fd, write_fd = os.pipe()
    os.close(write_fd)
    process = Mock(pid=12345, stdout=os.fdopen(read_fd, "rb", buffering=0))
    process.wait.return_value = 10
    process.poll.return_value = 10
    selector = MagicMock()
    selector.__enter__.return_value = selector
    selector.select.return_value = []

    class ImmediateThread:
        def __init__(self, target, daemon):
            self.target = target

        def start(self):
            self.target()

        def join(self):
            return None

    with (
        patch.object(pre_push_budget.subprocess, "Popen", return_value=process),
        patch.object(pre_push_budget, "Thread", ImmediateThread),
        patch.object(pre_push_budget.selectors, "DefaultSelector", return_value=selector),
        patch.object(pre_push_budget.os, "killpg", side_effect=ProcessLookupError),
    ):
        result = pre_push_budget.run_with_budget(["checks"], 10, tmp_path / "output")

    assert result == 10
    selector.select.assert_called_once()
    assert "AGDT_PRE_PUSH_BUDGET_EXHAUSTED" not in (tmp_path / "output").read_text()


def test_log_open_failure_blocks(tmp_path):
    with pytest.raises(OSError):
        pre_push_budget.run_with_budget([sys.executable], 1, tmp_path)


@pytest.mark.skipif(os.name != "posix", reason="Requires POSIX process groups and signals")
@pytest.mark.parametrize("parent_exits", [False, True])
def test_timeout_terminates_grandchild(parent_exits, tmp_path, capsys):
    pid_file = tmp_path / "pid"
    # A TERM handler reaps the grandchild, including on runners without a reaping PID 1.
    script = (
        "import os, signal, subprocess, sys, time\n"
        "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])\n"
        f"open({str(pid_file)!r}, 'w').write(str(child.pid))\n"
        "def stop(*args):\n"
        " child.wait()\n"
        " sys.exit(0)\n"
        "signal.signal(signal.SIGTERM, stop)\n"
        + ("os.close(1); os.close(2)\n" if parent_exits else "")
        + "time.sleep(60)\n"
    )
    log = tmp_path / "output"
    assert pre_push_budget.run_with_budget([sys.executable, "-u", "-c", script], 1, log) == 0
    marker = "AGDT_PRE_PUSH_BUDGET_EXHAUSTED budget=1s: targeted checks did not finish; push allowed, CI is the gate"
    assert marker in capsys.readouterr().out.splitlines()
    assert marker in log.read_text().splitlines()
    with pytest.raises(ProcessLookupError):
        os.kill(int(pid_file.read_text()), 0)


@pytest.mark.parametrize("stage", ["selector", "observer", "pipe_entry", "missing_pipe"])
def test_setup_failure_cleans_launched_group(stage, tmp_path):
    processes = []
    original = subprocess.Popen

    def launch(*args, **kwargs):
        process = original(*args, **kwargs)
        processes.append(process)
        if stage == "missing_pipe":
            process.stdout.close()
            process.stdout = None
        elif stage == "pipe_entry":
            pipe = process.stdout
            process.stdout = MagicMock(wraps=pipe)
            process.stdout.__enter__.side_effect = OSError("setup failed")
        return process

    target = "Thread" if stage == "observer" else "selectors.DefaultSelector"
    try:
        with (
            patch.object(pre_push_budget.subprocess, "Popen", side_effect=launch),
            patch(f"{pre_push_budget.__name__}.{target}", side_effect=OSError("setup failed")),
            pytest.raises((OSError, AssertionError)),
        ):
            pre_push_budget.run_with_budget(
                [sys.executable, "-c", "import time; time.sleep(60)"], 1, tmp_path / "output"
            )
        assert len(processes) == 1
        with pytest.raises(ProcessLookupError):
            os.killpg(processes[0].pid, 0)
    finally:
        for process in processes:
            pre_push_budget._stop_group(process)
            if process.stdout is not None:
                process.stdout.close()


@pytest.mark.parametrize("cleaned", [False, True])
def test_shutdown_output_is_drained_and_decoder_finalized(cleaned, tmp_path, monkeypatch):
    original_stop = pre_push_budget._stop_group
    stopped = []

    def stop(process, status=None):
        confirmed = original_stop(process, status)
        stopped.append(confirmed)
        return confirmed and cleaned

    monkeypatch.setattr(pre_push_budget, "_stop_group", stop)
    script = (
        "import os, signal, sys, time\n"
        "def stop(*args):\n"
        " os.write(1, b'shutdown diagnostics\\xe2\\x82')\n"
        " sys.exit(0)\n"
        "signal.signal(signal.SIGTERM, stop)\n"
        "print('ready', flush=True)\n"
        "time.sleep(60)\n"
    )
    log = tmp_path / "output"
    result = pre_push_budget.run_with_budget([sys.executable, "-u", "-c", script], 1, log)
    assert result == int(not cleaned)
    assert stopped == [True]
    assert "shutdown diagnostics\ufffd" in log.read_text()
    assert ("AGDT_PRE_PUSH_BUDGET_EXHAUSTED" in log.read_text()) == cleaned


@pytest.mark.skipif(os.name != "posix", reason="Requires POSIX SIGKILL escalation")
def test_ignoring_term_escalates(tmp_path, monkeypatch):
    monkeypatch.setattr(pre_push_budget, "TERM_GRACE_SECONDS", 0.1)
    assert (
        pre_push_budget.run_with_budget(
            [
                sys.executable,
                "-u",
                "-c",
                "import signal,time; signal.signal(signal.SIGTERM, signal.SIG_IGN); print('ready'); time.sleep(60)",
            ],
            1,
            tmp_path / "output",
        )
        == 0
    )


def test_non_posix_timeout_fails_closed(tmp_path, capsys):
    with patch.object(pre_push_budget.os, "name", "nt"):
        with pytest.raises(ValueError, match="POSIX"):
            pre_push_budget.run_with_budget(
                [sys.executable, "-c", "import time; time.sleep(60)"],
                1,
                tmp_path / "output",
            )
    assert "AGDT_PRE_PUSH_BUDGET_EXHAUSTED" not in capsys.readouterr().out


@pytest.mark.skipif(os.name != "posix", reason="Requires POSIX process-group probing")
def test_unconfirmed_cleanup_blocks(tmp_path, capsys, monkeypatch):
    real_killpg = os.killpg

    def killpg(pid, sig):
        if sig != 0:
            real_killpg(pid, sig)

    monkeypatch.setattr(pre_push_budget.os, "killpg", killpg)
    monkeypatch.setattr(pre_push_budget, "TERM_GRACE_SECONDS", 0)
    monkeypatch.setattr(pre_push_budget, "KILL_GRACE_SECONDS", 0)
    assert (
        pre_push_budget.run_with_budget(
            [sys.executable, "-c", "import time; time.sleep(60)"],
            1,
            tmp_path / "output",
        )
        == 1
    )
    assert "AGDT_PRE_PUSH_BUDGET_EXHAUSTED" not in capsys.readouterr().out


@pytest.mark.skipif(os.name != "posix", reason="Requires POSIX process-group signals")
def test_log_write_failure_cleans_child(tmp_path):
    process = None
    original = subprocess.Popen

    def launch(*args, **kwargs):
        nonlocal process
        process = original(*args, **kwargs)
        return process

    with patch.object(pre_push_budget.subprocess, "Popen", side_effect=launch):
        with patch.object(pre_push_budget.sys.stdout, "write", side_effect=OSError("output failed")):
            with patch.object(pre_push_budget.os, "write", side_effect=OSError("output failed")):
                with pytest.raises(OSError):
                    pre_push_budget.run_with_budget(
                        [sys.executable, "-c", "import time; print('ready', flush=True); time.sleep(60)"],
                        1,
                        tmp_path / "output",
                    )
    # Banner failure happens before spawning: no unchecked process may be launched.
    assert process is None


def test_stream_failure_cleans_child(tmp_path):
    process = None
    original = subprocess.Popen
    original_read = os.read

    def launch(*args, **kwargs):
        nonlocal process
        process = original(*args, **kwargs)
        return process

    def read(fd, count):
        if process is not None and fd == process.stdout.fileno():
            raise OSError("read failed")
        return original_read(fd, count)

    with patch.object(pre_push_budget.subprocess, "Popen", side_effect=launch):
        with patch.object(pre_push_budget.os, "read", side_effect=read):
            with pytest.raises(OSError, match="read failed"):
                pre_push_budget.run_with_budget(
                    [sys.executable, "-c", "print('ready', flush=True); import time; time.sleep(60)"],
                    1,
                    tmp_path / "output",
                )
    assert process is not None
    assert process.poll() is not None


def test_eof_does_not_remove_process_budget(tmp_path):
    log = tmp_path / "output"
    assert (
        pre_push_budget.run_with_budget(
            [sys.executable, "-c", "import os,time; os.close(1); os.close(2); time.sleep(60)"],
            1,
            log,
        )
        == 0
    )
    assert "AGDT_PRE_PUSH_BUDGET_EXHAUSTED budget=1s:" in log.read_text()


def test_required_log_write_failure_cleans_child(tmp_path):
    processes = []
    original = subprocess.Popen

    def launch(*args, **kwargs):
        process = original(*args, **kwargs)
        processes.append(process)
        return process

    opened = mock_open()
    opened.return_value.write.side_effect = [None, None, OSError("disk full")]
    with patch.object(Path, "open", opened), patch.object(pre_push_budget.subprocess, "Popen", side_effect=launch):
        with pytest.raises(OSError, match="disk full"):
            pre_push_budget.run_with_budget(
                [sys.executable, "-c", "import time; print('ready', flush=True); time.sleep(60)"],
                1,
                tmp_path / "output",
            )
    assert len(processes) == 1
    assert processes[0].poll() is not None


@pytest.mark.parametrize("status", [1, 10, 42])
@pytest.mark.parametrize("forwarding_delayed", [False, True])
@pytest.mark.parametrize("cleaned", [False, True])
def test_failure_survives_inherited_pipe_and_delayed_forwarding(
    status, forwarding_delayed, cleaned, tmp_path, capsys, monkeypatch
):
    # An open writer models a descendant retaining the leader's stdout after exit.
    read_fd, write_fd = os.pipe()
    clock = [0.0]
    signalled = []
    process = Mock(pid=12345)
    process.stdout = os.fdopen(read_fd, "rb", buffering=0)
    process.poll.return_value = status

    def wait(timeout):
        raise subprocess.TimeoutExpired("checks", timeout)

    def killpg(pid, sig):
        if sig:
            signalled.append(sig)
        elif signalled and cleaned:
            raise ProcessLookupError

    def select(timeout):
        clock[0] += timeout
        return [(None, None)] if forwarding_delayed else []

    original_write = sys.stdout.write

    def write(text):
        if "failure output" in text:
            clock[0] = 2.0  # Forwarding crosses the one-second deadline.
        return original_write(text)

    process.wait.side_effect = wait
    selector = MagicMock()
    selector.__enter__.return_value = selector
    selector.select.side_effect = select
    monkeypatch.setattr(pre_push_budget.subprocess, "Popen", Mock(return_value=process))
    monkeypatch.setattr(pre_push_budget.selectors, "DefaultSelector", Mock(return_value=selector))
    monkeypatch.setattr(pre_push_budget.time, "monotonic", lambda: clock[0])
    monkeypatch.setattr(pre_push_budget.os, "killpg", killpg)
    monkeypatch.setattr(pre_push_budget, "TERM_GRACE_SECONDS", 0.1)
    monkeypatch.setattr(pre_push_budget, "KILL_GRACE_SECONDS", 0.1)
    monkeypatch.setattr(pre_push_budget.time, "sleep", lambda delay: clock.__setitem__(0, clock[0] + delay))
    monkeypatch.setattr(pre_push_budget.sys.stdout, "write", write)
    log = tmp_path / "output"
    try:
        if forwarding_delayed:
            os.write(write_fd, b"failure output")
        result = pre_push_budget.run_with_budget(["checks"], 1, log)
    finally:
        os.close(write_fd)
    assert result == (status if cleaned else 1)
    assert signalled
    output = capsys.readouterr().out
    assert "AGDT_PRE_PUSH_BUDGET_EXHAUSTED" not in output
    assert "AGDT_PRE_PUSH_BUDGET_EXHAUSTED" not in log.read_text()
    if not cleaned:
        assert "cleanup unconfirmed" in output


def test_unread_stdout_pipe_does_not_stall_deadline(tmp_path, monkeypatch):
    read_fd, write_fd = os.pipe()
    sink = os.fdopen(write_fd, "w", buffering=1)
    pid_file = tmp_path / "child-pid"
    script = (
        "import os, signal, subprocess, sys, time\n"
        "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])\n"
        f"open({str(pid_file)!r}, 'w').write(str(child.pid))\n"
        "def stop(*args):\n"
        " child.wait()\n"
        " sys.exit(0)\n"
        "signal.signal(signal.SIGTERM, stop)\n"
        "for _ in range(1024): os.write(1, b'x' * 4096)\n"
        "time.sleep(60)\n"
    )
    completed = Event()
    result = []
    failure = []

    def run():
        with patch.object(pre_push_budget.sys, "stdout", sink):
            try:
                result.append(
                    pre_push_budget.run_with_budget(
                        [sys.executable, "-u", "-c", script],
                        1,
                        tmp_path / "output",
                    )
                )
            except BaseException as exc:
                failure.append(exc)
            finally:
                completed.set()

    monkeypatch.setattr(pre_push_budget, "TERM_GRACE_SECONDS", 0.1)
    monkeypatch.setattr(pre_push_budget, "KILL_GRACE_SECONDS", 0.1)
    runner = Thread(target=run, daemon=True)
    runner.start()
    returned_without_reader = completed.wait(timeout=5)

    reader = None
    if not returned_without_reader:

        def drain_pipe():
            while os.read(read_fd, 4096):
                pass

        reader = Thread(target=drain_pipe, daemon=True)
        reader.start()
        completed.wait(timeout=3)

    sink.close()
    os.close(read_fd)
    runner.join(timeout=1)
    if reader is not None:
        reader.join(timeout=1)

    assert returned_without_reader
    assert not runner.is_alive()
    assert not failure
    assert result == [0]
    log = (tmp_path / "output").read_bytes()
    assert log.count(b"x") > 65536
    assert b"AGDT_PRE_PUSH_BUDGET_EXHAUSTED budget=1s:" in log
    with pytest.raises(ProcessLookupError):
        os.kill(int(pid_file.read_text()), 0)
