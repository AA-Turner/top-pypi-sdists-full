"""While `probe uninstall` runs, nothing of Probe starts or updates anything (clean-uninstall U-T3, C3).

The barrier (`S/uninstall/barrier.json`) is written by the uninstall and read
by ONE reader, `probe._shared.uninstall_barrier`. These are the release-side
places that must honour it: `client.ensure`, the service's own start, the
keeper, the guard, a daemon worker's start, `write_runtime`, and the update's
first step (`core.adopt.begin`, the hand-off's adopt included). The tap's
copy of the client, which cannot import `probe`, honours the file's presence.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from probe._shared import uninstall_barrier
from probe.service import client, paths

TAP_ROOT = Path(__file__).resolve().parent.parent / "plugins" / "probe-research-tap"


def _barrier(phase: str = "stopping", *, pid: int | None = None) -> dict:
    from probe.service import procid

    pid = os.getpid() if pid is None else pid
    record = {"v": 1, "pid": pid, "start": procid.start_time(pid) or "1", "at": 0, "phase": phase,
              "plan": str(paths.uninstall_plan_path())}
    paths.private_dir(paths.uninstall_dir())
    paths.uninstall_barrier_path().write_text(json.dumps(record))
    return record


def test_the_paths_agree_with_the_one_reader():
    assert paths.uninstall_barrier_path() == uninstall_barrier.path()
    assert paths.uninstall_plan_path().parent == uninstall_barrier.path().parent
    from probe.cli import uninstall

    assert tuple(str(p) for p in uninstall.PHASES) == uninstall_barrier.PHASES


def test_ensure_starts_nothing_and_writes_nothing():
    _barrier()
    before = sorted(p for p in paths.state_dir().rglob("*"))
    assert client.ensure(wait=0.1) == client.Ensured.UNINSTALLING
    assert sorted(p for p in paths.state_dir().rglob("*")) == before
    assert not paths.service_dir().exists()


def test_the_service_will_not_start():
    from probe.service import server

    _barrier()
    assert server.run_service() == 0
    assert not paths.service_dir().exists()


def test_the_keeper_does_nothing_and_installs_nothing(monkeypatch):
    from probe.service import keeper

    _barrier()
    monkeypatch.setattr(keeper, "wanted", lambda: True)
    monkeypatch.setattr(keeper, "needed", lambda: pytest.fail("the keeper looked for sessions"))
    assert keeper.main() == 0
    assert keeper.install() == "not wanted (uninstalling)"
    assert keeper.install_lifeboat() == "not wanted (uninstalling)"


def test_the_guard_neither_waits_nor_switches_back(monkeypatch):
    from probe.service import guard

    _barrier()
    monkeypatch.setattr(guard, "check", lambda *a, **k: pytest.fail("the guard watched"))
    monkeypatch.setattr(guard, "switch_back", lambda *a, **k: pytest.fail("the guard switched back"))
    assert guard.main(["--from", "1.0.0", "--to", "1.0.1", "--old-python", sys.executable]) == 0


def test_runtime_json_is_not_written_again():
    _barrier()
    assert client.write_runtime(sys.executable, "1.0.0") is False
    assert not paths.runtime_path().exists()


def test_a_daemon_worker_comes_back_later():
    from probe import _entry
    from probe.service import barrier

    _barrier()
    assert _entry._update_barrier(["daemon", "worker", "--session-id", "x"]) == barrier.WORKER_BUSY_EXIT_CODE
    assert _entry._update_barrier(["status"]) is None  # every other command runs


def test_the_update_and_the_handoffs_adopt_stop_at_their_first_step(monkeypatch):
    from probe._shared import handoff
    from probe.core import adopt

    _barrier("server", pid=999999999)  # past the point of no return: LIVE without its owner
    adopt.reset()
    monkeypatch.setenv(handoff.ADOPT_ENV, "/nowhere/probe-versions/9.9.9/probe-research")
    monkeypatch.setenv(handoff.FROM_ENV, "1.0.0")
    monkeypatch.setattr(adopt, "adopt", lambda: pytest.fail("adopted during an uninstall"))
    monkeypatch.setattr(handoff, "stage1", lambda *a, **k: pytest.fail("handed off during an uninstall"))
    ending = adopt.begin("manual")
    assert ending is not None and ending.status == adopt.DEFERRED_EXIT and "uninstall" in ending.message
    assert handoff.ADOPT_ENV not in os.environ and handoff.FROM_ENV not in os.environ
    adopt.reset()


def test_an_update_whose_handoff_answers_uninstalling_ends_there(monkeypatch):
    """The hand-off (v3) reads the barrier itself and answers `uninstalling`:
    the update ENDS, it never goes on in this release instead."""
    from probe._shared import handoff
    from probe.core import adopt

    adopt.reset()
    monkeypatch.delenv(handoff.ADOPT_ENV, raising=False)
    monkeypatch.setattr(adopt, "runs_managed_cli", lambda: True)
    monkeypatch.setattr(adopt, "install_inputs", lambda: {})
    monkeypatch.setattr(handoff, "stage1", lambda *a, **k: {"result": "uninstalling"})
    ending = adopt.begin("manual")
    assert ending is not None and ending.status == adopt.DEFERRED_EXIT
    adopt.reset()


def test_a_stale_barrier_holds_nothing_back():
    _barrier("draining", pid=999999999)
    assert client.uninstall_barrier() is None
    assert uninstall_barrier.clear_stale() is not None
    assert not paths.uninstall_barrier_path().exists()


def test_the_taps_copy_honours_the_barrier_without_probe(tmp_path):
    home = tmp_path / "home"
    folder = home / ".local" / "state" / "probe" / "uninstall"
    folder.mkdir(parents=True)
    (folder / "barrier.json").write_text("{}")
    script = (
        "import sys; sys.path.insert(0, sys.argv[1]); "
        "from tap.service import client; "
        "print(client.ensure()); assert 'probe' not in sys.modules"
    )
    done = subprocess.run([sys.executable, "-I", "-S", "-c", script, str(TAP_ROOT)], capture_output=True, text=True,
                          timeout=30, env={"HOME": str(home), "PATH": os.environ.get("PATH", "")})
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "uninstalling"
    assert not (home / ".local" / "state" / "probe" / "service").exists()
