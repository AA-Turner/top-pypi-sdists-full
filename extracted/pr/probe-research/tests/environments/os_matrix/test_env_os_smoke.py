"""The SDK smoke for the macOS / Windows matrix (.github/workflows/agent-os-matrix.yml).

Plain processes on the runner's own OS, against the served fake (or a real
server): the customer loop, an interrupt, and the outbox carried across a
"restart". Written to run unchanged on Linux too -- that is how it is checked
before the workflow exists on main.

Interrupts per OS: POSIX sends SIGINT (Ctrl-C) and expects the run
`canceled` and the process to die BY SIGINT. Windows has no SIGINT for a
child: it sends CTRL_BREAK_EVENT to the child's own process group (Python's
default SIGBREAK action ends the process at once, like SIGKILL), so it asserts
only what the SDK can promise there -- no hang, and nothing logged is lost.
"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest

from tests.environments import envlib
from tests.environments.envlib import LoopEvents, record

pytestmark = [envlib.requires_env]

IS_WIN = sys.platform == "win32"
TERMINAL = {"completed", "failed", "crashed", "canceled"}
LOOP_TIMEOUT = 780  # init's 90 s budget + finish's 600 s + margin: past it, a hang


def _loop(sdk_py: str, *args: str) -> list[str]:
    return [sdk_py, str(envlib.CUSTOMER_LOOP), *args]


def _popen(argv, env, cwd) -> subprocess.Popen:
    flags = subprocess.CREATE_NEW_PROCESS_GROUP if IS_WIN else 0
    return subprocess.Popen(
        argv, env=env, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, creationflags=flags,
    )


def _wait_for_ready(proc: subprocess.Popen, timeout: float) -> list[str]:
    """Read the child's stdout until customer_loop says `ready`."""
    lines: list[str] = []
    deadline = time.monotonic() + timeout
    assert proc.stdout is not None
    while time.monotonic() < deadline:
        line = proc.stdout.readline()
        if not line:
            break
        lines.append(line)
        if '"event": "ready"' in line:
            return lines
    proc.kill()
    raise AssertionError(f"child never became ready:\n{''.join(lines)}\n{envlib.tail(proc.stderr.read())}")


def _kill_workers(home: Path) -> list[int]:
    """A machine restart: every detached outbox worker serving this test's
    HOME dies. Found through the caps file each worker writes beside its
    queue, and by command line as a backstop."""
    import json

    killed: list[int] = []
    for caps in home.rglob(".worker-caps.json"):
        try:
            pid = int(json.loads(caps.read_text()).get("pid") or 0)
        except (OSError, ValueError):
            continue
        if pid > 0:
            killed.append(pid)
    try:
        import psutil

        for p in psutil.process_iter(["pid", "cmdline"]):
            cmd = " ".join(p.info.get("cmdline") or [])
            if "outbox_worker" in cmd and str(home) in cmd:
                killed.append(p.info["pid"])
    except ImportError:
        pass
    for pid in set(killed):
        try:
            os.kill(pid, signal.SIGTERM if IS_WIN else signal.SIGKILL)
        except OSError:
            pass
    return sorted(set(killed))


def test_env_os_smoke_customer_loop(be, sdk_py, sdk_version, tmp_path):
    env = envlib.child_env(be, tmp_path)
    work = tmp_path / "work"
    work.mkdir()
    started = time.time()
    proc = envlib.run_child(
        _loop(sdk_py, "--name", "os-smoke", "--steps", "0:50", "--config", "--small-artifact"),
        env=env, cwd=work, timeout=LOOP_TIMEOUT,
    )
    run_id = LoopEvents.parse(proc.stdout).run_id
    assert run_id, envlib.tail(proc.stderr)
    rec = be.wait_points(run_id, envlib.expected_points(range(0, 50)), timeout=60)
    status = be.wait_status(run_id, TERMINAL, timeout=60)
    run = be.run(run_id)
    arts = {a.get("name"): a.get("status") for a in be.artifacts(run_id)}
    home = envlib.real_home_writes(started, [run_id, str(tmp_path)])
    record(
        "os/smoke-loop",
        sdk=sdk_version,
        platform=sys.platform,
        exit=proc.returncode,
        points=rec.summary(),
        status=status,
        config=(run.get("config") or {}).get("model") == envlib.CONFIG["model"],
        small_artifact=arts.get("small.txt"),
        real_home_writes=home,
    )
    assert proc.returncode == 0, envlib.tail(proc.stderr)
    assert rec.ok, rec.summary()
    assert status == "completed"
    assert (run.get("config") or {}).get("model") == envlib.CONFIG["model"]
    assert arts.get("small.txt") == "complete"
    assert home == []


def test_env_os_smoke_interrupt(be, sdk_py, sdk_version, tmp_path):
    env = envlib.child_env(be, tmp_path)
    work = tmp_path / "work"
    work.mkdir()
    proc = _popen(_loop(sdk_py, "--name", "os-interrupt", "--steps", "0:30", "--then", "wait"), env, work)
    try:
        lines = _wait_for_ready(proc, timeout=180)
        time.sleep(2.0)  # the SDK's normal delivery lag, so the interrupt tests the close
        proc.send_signal(signal.CTRL_BREAK_EVENT if IS_WIN else signal.SIGINT)
        out, err = proc.communicate(timeout=LOOP_TIMEOUT)
    except subprocess.TimeoutExpired:
        proc.kill()
        raise AssertionError("the interrupted child hung") from None
    run_id = LoopEvents.parse("".join(lines) + out).run_id
    rec = be.wait_points(run_id, envlib.expected_points(range(0, 30)), timeout=60)
    status = be.wait_status(run_id, TERMINAL, timeout=30 if IS_WIN else 60)
    record(
        "os/interrupt",
        sdk=sdk_version,
        platform=sys.platform,
        signal="CTRL_BREAK_EVENT" if IS_WIN else "SIGINT",
        exit=proc.returncode,
        points=rec.summary(),
        status=status,
        stderr_tail=envlib.tail(err, 400),
    )
    assert rec.ok, rec.summary()
    if not IS_WIN:
        assert proc.returncode in (-signal.SIGINT, 128 + signal.SIGINT), (proc.returncode, envlib.tail(err))
        assert status == "canceled"


@pytest.mark.parametrize("ending", ["deferred-finish", "hard-kill"])
def test_env_os_smoke_outbox_drain_across_restart(be, sdk_py, sdk_version, tmp_path, ending):
    """Job A logs while the server is busy, so its writes wait in the outbox
    on this machine's disk; A then ends (a finish whose 5 s budget runs out,
    or a hard kill) and the machine "restarts" -- its detached worker dies.
    Job B starts on the same machine with the server healthy.

    Pass = job B's first writes wake delivery for the WHOLE queue: A's points
    arrive, and after a deferred finish A's terminal status too. On a real
    server the busy period cannot be arranged, so A's queue may already be
    empty; the test still checks nothing is lost."""
    env = envlib.child_env(be, tmp_path, PROBE_FINISH_TIMEOUT_SEC="5")
    work = tmp_path / "work"
    work.mkdir()
    busy = be.set_metrics_busy(True)
    steps_a = range(0, 50)
    if ending == "deferred-finish":
        a = envlib.run_child(
            _loop(sdk_py, "--name", "os-restart-a", "--steps", "0:50", "--config"),
            env=env, cwd=work, timeout=LOOP_TIMEOUT,
        )
        a_out, a_exit = a.stdout, a.returncode
    else:
        p = _popen(_loop(sdk_py, "--name", "os-restart-a", "--steps", "0:50", "--config", "--then", "wait"), env, work)
        lines = _wait_for_ready(p, timeout=180)
        p.kill()
        rest, _ = p.communicate(timeout=60)
        a_out, a_exit = "".join(lines) + rest, p.returncode
    run_a = LoopEvents.parse(a_out).run_id
    assert run_a, a_out
    killed = _kill_workers(tmp_path / "home")
    queued = envlib.reconcile(envlib.expected_points(steps_a), be.points(run_a))
    be.set_metrics_busy(False)

    b = envlib.run_child(
        _loop(sdk_py, "--name", "os-restart-b", "--steps", "0:10"),
        env=env, cwd=work, timeout=LOOP_TIMEOUT,
    )
    run_b = LoopEvents.parse(b.stdout).run_id
    rec_a = be.wait_points(run_a, envlib.expected_points(steps_a), timeout=90)
    status_a = be.wait_status(run_a, TERMINAL, timeout=60 if ending == "deferred-finish" else 5)
    rec_b = be.wait_points(run_b, envlib.expected_points(range(0, 10)), timeout=60) if run_b else None
    record(
        f"os/outbox-across-restart[{ending}]",
        sdk=sdk_version,
        platform=sys.platform,
        busy_server_arranged=busy,
        a_exit=a_exit,
        workers_killed=len(killed),
        a_undelivered_at_restart=queued.expected - queued.delivered,
        a_points=rec_a.summary(),
        a_status=status_a,
        b_exit=b.returncode,
        b_points=rec_b.summary() if rec_b else None,
    )
    assert b.returncode == 0, envlib.tail(b.stderr)
    assert rec_b is not None and rec_b.ok
    assert rec_a.ok, f"job A's queue was not delivered after the restart: {rec_a.summary()}"
    if ending == "deferred-finish":
        assert a_exit == 0
        assert status_a == "completed", f"A's deferred finish never arrived: {status_a!r}"
