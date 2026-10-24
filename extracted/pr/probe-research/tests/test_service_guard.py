"""The switch's guard: the new version must start and keep answering, else back (plan D5).

A real service in a throwaway HOME (`service_harness`), and a fake side-by-side
layout (`test_side_by_side_installs`'s fake environments) for the switch back.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

import probe
from probe._shared import installs
from probe.service import guard
from tests.service_fakes import FakeCore
from tests.service_harness import service_home, wait_for  # noqa: F401 -- a fixture
from tests.test_side_by_side_installs import _fake_env, _uv

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="the service is POSIX-only (plan S8)")


@pytest.fixture
def switched(service_home, monkeypatch):
    """0.1.0 was today's install; the update just switched the tool path to 0.2.0."""
    FakeCore(service_home.home)  # runtime.json -> an interpreter that starts the real service
    tools = service_home.home / "share" / "uv" / "tools"
    _fake_env(tools / installs.DIST, "0.1.0")
    monkeypatch.setenv("UV_TOOL_DIR", str(tools))
    new = installs.install("0.2.0", "x", tools=tools, run=_uv("0.2.0"))
    installs.activate(new, tools=tools)
    monkeypatch.setattr(guard, "GONE_S", 5.0)
    monkeypatch.setattr(guard, "START_S", 10.0)
    return tools


def test_a_version_that_starts_and_keeps_answering_stays(switched, monkeypatch):
    monkeypatch.setenv(guard.WATCH_ENV, "1")
    assert guard.main(["--from", "0.1.0", "--to", probe.__version__, "--old-python", sys.executable]) == 0
    assert guard.read()["ok"] is True
    assert installs.active(switched).parent.name == "0.2.0"


def test_a_guard_with_no_new_privs_never_calls_a_good_version_bad(switched, monkeypatch):
    """Review (round 4): from a no_new_privs process `ensure` starts no
    service, so the watch saw "did not answer" and switched a good release
    back. There is nothing to watch from there: the version stays."""
    from probe.service import client

    monkeypatch.setattr(client, "no_new_privs", lambda: True)
    monkeypatch.setenv(guard.WATCH_ENV, "1")
    assert guard.main(["--from", "0.1.0", "--to", "9.9.9", "--old-python", sys.executable]) == 0
    assert installs.active(switched).parent.name == "0.2.0"
    assert "9.9.9" not in installs.rejected(switched)


def test_a_version_that_answers_as_another_is_switched_back(switched, service_home, monkeypatch):
    monkeypatch.setenv(guard.WATCH_ENV, "1")
    # `--from` is what the switched-back service answers as: this code's version.
    assert guard.main(["--from", probe.__version__, "--to", "9.9.9", "--old-python", sys.executable]) == 1
    record = guard.read()
    assert record["ok"] is False and record["rollback"] == "done"
    assert record["answering"] == probe.__version__
    assert "answered as" in record["reason"]
    assert installs.active(switched).parent.name == "0.1.0"
    assert "9.9.9" in installs.rejected(switched)
    # The service runs again (on the version switched back to).
    assert wait_for(lambda: service_home.status(), 10.0)


def test_an_idle_new_service_is_held_through_the_watch(switched, service_home, monkeypatch):
    """No session and no app window: a healthy service rightly stops after its
    grace. The guard's own keep-alive connection holds it for the watch, so
    stopping idle is never read as a failed release."""
    monkeypatch.setenv("PROBE_SERVICE_GRACE_S", "0.3")
    monkeypatch.setenv(guard.WATCH_ENV, "3")
    assert guard.main(["--from", "0.1.0", "--to", probe.__version__, "--old-python", sys.executable]) == 0
    assert guard.read()["ok"] is True


def test_a_new_service_another_client_started_first_is_taken(switched, service_home, monkeypatch):
    """A tap reconnecting started the new service before the guard looked: the
    old service (its exact process) is gone, so that one is the new version."""
    import subprocess

    from probe.service import procid

    monkeypatch.setenv(guard.WATCH_ENV, "1")
    gone = subprocess.Popen(["true"])
    start = wait_for(lambda: procid.start_time(gone.pid), 2.0) or "x"
    gone.wait()
    service_home.start()
    args = ["--from", "0.1.0", "--to", probe.__version__, "--old-python", sys.executable,
            "--old-pid", str(gone.pid), "--old-start", start]
    assert guard.main(args) == 0
    assert guard.read()["ok"] is True


def test_a_new_service_that_hangs_is_killed_by_its_lock_file(switched, service_home, monkeypatch):
    """It answers nothing, so no hello names it: the pid it wrote into the
    lock file does. SIGTERM, which it ignores, then SIGKILL."""
    import subprocess

    from probe.service import paths

    monkeypatch.setattr(guard, "STOP_WAIT_S", 1.0)
    hung = subprocess.Popen([sys.executable, "-c", (
        "import fcntl, os, signal, sys, time\n"
        "signal.signal(signal.SIGTERM, signal.SIG_IGN)\n"
        "from probe.service import paths, procid\n"
        "fd = os.open(paths.lock_path(), os.O_RDWR | os.O_CREAT, 0o600)\n"
        "fcntl.flock(fd, fcntl.LOCK_EX)\n"
        "os.ftruncate(fd, 0); os.pwrite(fd, f'{os.getpid()} {procid.start_time(os.getpid())}'.encode(), 0)\n"
        "print('held', flush=True)\n"
        "time.sleep(60)\n")], stdout=subprocess.PIPE, text=True)
    try:
        assert hung.stdout.readline().strip() == "held"
        assert guard.holder() is not None and guard.holder()[0] == hung.pid
        guard._stop_new(sys.executable)
        assert hung.wait(5) == -9
        assert guard._lock_free()
        assert paths.lock_path().exists()
    finally:
        if hung.poll() is None:
            hung.kill()


def test_a_new_service_restarting_on_purpose_in_its_watch_is_no_crash(switched, service_home, monkeypatch):
    """It restarts onto a newer tap (or a person stops it) while the guard
    watches: the stop it recorded says so, and the watch goes on with the next
    one (the R2 local live run: a healthy release was switched back)."""
    import threading

    from probe.service.protocol import Method

    monkeypatch.setenv(guard.WATCH_ENV, "5")
    first = service_home.start()

    def restart():
        import time as _t

        _t.sleep(2.0)  # inside the watch
        service_home.call(Method.STOP)

    threading.Thread(target=restart, daemon=True).start()
    assert guard.main(["--from", "0.1.0", "--to", probe.__version__, "--old-python", sys.executable,
                       *_gone_old()]) == 0
    assert guard.read()["ok"] is True
    assert guard.last_stop()["pid"] == first["pid"]
    assert service_home.status()["pid"] != first["pid"]


def test_a_new_service_that_dies_without_a_word_is_a_crash(switched, service_home, monkeypatch):
    import os
    import signal
    import threading

    monkeypatch.setenv(guard.WATCH_ENV, "5")
    first = service_home.start()

    def kill():
        import time as _t

        _t.sleep(2.0)  # inside the watch
        os.kill(first["pid"], signal.SIGKILL)

    threading.Thread(target=kill, daemon=True).start()
    assert guard.main(["--from", probe.__version__, "--to", probe.__version__, "--old-python", sys.executable,
                       *_gone_old()]) == 1
    assert "crashed" in guard.read()["reason"] or "stopped answering" in guard.read()["reason"]


def _gone_old() -> list:
    """`--old-pid`/`--old-start` of a process that already exited."""
    import subprocess

    from probe.service import procid

    gone = subprocess.Popen(["sleep", "0.2"])
    start = wait_for(lambda: procid.start_time(gone.pid), 2.0) or "x"
    gone.wait()
    return ["--old-pid", str(gone.pid), "--old-start", start]
