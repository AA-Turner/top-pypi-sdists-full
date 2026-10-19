"""One wizard run that changes the device at a time (`probe.cli.wizard_lock`).

The terminal wizard and the desktop app write to one Probe install. A second
run that would change it exits 75 at once, having changed nothing; a run that
only reads never waits on the lock; and a holder that dies frees it with no
cleanup, because the kernel drops an `flock` with its process.
"""

from __future__ import annotations

import contextlib
import json
import os
import signal
import subprocess
import sys
import textwrap
import time

import pytest
from typer.testing import CliRunner

from probe._shared import oscompat
from probe.cli import autoupdate, capture, upgrading, version_refresh, wizard_lock
from probe.sdk.config import load_context, save_context
from tests import test_wizard_json_events as events

device = events.device
main = events.main

#: A `probe wizard` whose session, once it holds the lock, waits for the test
#: to say `release`. Each process says `ready` once imported, then starts on `go`.
CONTENDER = textwrap.dedent(
    """
    import importlib, os, sys, time
    main = importlib.import_module("probe.cli.main")
    folder = sys.argv[1]
    def hold(**_):
        open(os.path.join(folder, f"holding.{os.getpid()}"), "w").close()
        deadline = time.monotonic() + 60
        while not os.path.exists(os.path.join(folder, "release")) and time.monotonic() < deadline:
            time.sleep(0.02)
    main._wizard_session = hold
    open(os.path.join(folder, f"ready.{os.getpid()}"), "w").close()
    while not os.path.exists(os.path.join(folder, "go")):
        time.sleep(0.002)
    raise SystemExit(main.main(sys.argv[2:]))
    """
)

#: Takes the lock, says so, and sleeps until it is killed.
HOLDER = textwrap.dedent(
    """
    import sys, time
    from probe.cli import wizard_lock
    with wizard_lock.held():
        open(sys.argv[1], "w").close()
        time.sleep(300)
    """
)


def _env(tmp_path) -> dict[str, str]:
    empty = tmp_path / "empty-path"
    empty.mkdir(exist_ok=True)
    return {
        **os.environ,
        "PATH": str(empty),
        "XDG_STATE_HOME": str(tmp_path / "state"),
        "PROBE_BASE_URL": "http://127.0.0.1:9",
    }


def _wait_for(predicate, timeout: float = 60.0) -> None:
    deadline = time.monotonic() + timeout
    while not predicate():
        if time.monotonic() > deadline:
            raise AssertionError("timed out")
        time.sleep(0.02)


@pytest.fixture
def contenders(tmp_path):
    """Two `probe wizard --action update --yes --json` started at the same instant."""
    folder = tmp_path / "signals"
    folder.mkdir()
    argv = [sys.executable, "-c", CONTENDER, str(folder), "wizard", "--action", "update", "--yes", "--json"]
    procs = [
        subprocess.Popen(argv, env=_env(tmp_path), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for _ in range(2)
    ]
    try:
        _wait_for(lambda: len(list(folder.glob("ready.*"))) == 2)
        (folder / "go").touch()
        # The loser leaves at once; the holder waits for `release`. Two holders
        # at once is the failure, so it ends the wait too.
        _wait_for(
            lambda: any(proc.poll() is not None for proc in procs)
            or len(list(folder.glob("holding.*"))) == 2
        )
        (folder / "release").touch()
        outputs = [proc.communicate(timeout=60) for proc in procs]
    finally:
        for proc in procs:
            proc.kill()
    return [(proc.returncode, out, err) for proc, (out, err) in zip(procs, outputs)]


def test_of_two_runs_started_together_exactly_one_proceeds(contenders):
    assert sorted(code for code, _, _ in contenders) == [0, wizard_lock.BUSY_EXIT_CODE]


def test_the_run_turned_away_says_busy(contenders):
    out = next(out for code, out, _ in contenders if code == wizard_lock.BUSY_EXIT_CODE)
    events = [json.loads(line) for line in out.splitlines()]
    assert [(event["event"], event.get("code")) for event in events][:1] == [("error", "busy")]


def test_the_run_turned_away_still_ends_with_done(contenders):
    out = next(out for code, out, _ in contenders if code == wizard_lock.BUSY_EXIT_CODE)
    done = json.loads(out.splitlines()[-1])
    assert (done["event"], done["exit_code"]) == ("done", wizard_lock.BUSY_EXIT_CODE)


def test_a_lock_left_by_a_killed_process_is_free_at_once(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    marker = tmp_path / "held"
    holder = subprocess.Popen([sys.executable, "-c", HOLDER, str(marker)], env=_env(tmp_path))
    try:
        _wait_for(marker.exists)
        with pytest.raises(wizard_lock.Busy):  # the holder really holds it
            with wizard_lock.held():
                pass
        holder.send_signal(signal.SIGKILL)
        holder.wait(timeout=30)
        with wizard_lock.held():
            pass  # no wait, no stale-lock cleanup
    finally:
        holder.kill()


# -- in one process: what a person at the terminal sees --------------------------


@contextlib.contextmanager
def _held_by_another_process():
    """The lock as another process holds it: its own open file, flocked. Not
    `wizard_lock.held()`, which this process would re-enter."""
    path = wizard_lock.lock_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a+") as handle:
        oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        yield


@pytest.fixture
def held_elsewhere(device, monkeypatch):
    """Another setup holds the lock. A run that got past it would reach real
    work, so that work fails the test instead of happening. The update's body
    is what is forbidden, so `perform_update` itself still takes the lock."""
    from probe.cli import upgrading

    def forbidden(*_a, **_k):
        pytest.fail("a run turned away by the lock must change nothing")

    monkeypatch.setattr(upgrading, "_perform_update", forbidden)
    monkeypatch.setattr(main, "device_login", forbidden)
    monkeypatch.setattr(main, "_client", forbidden)
    with _held_by_another_process():
        yield


def test_a_second_wizard_at_the_terminal_exits_75(held_elsewhere):
    result = CliRunner().invoke(main.app, ["wizard", "--action", "update", "--yes"])
    assert result.exit_code == wizard_lock.BUSY_EXIT_CODE


def test_a_second_wizard_at_the_terminal_says_another_setup_is_running(held_elsewhere):
    result = CliRunner().invoke(main.app, ["wizard", "--action", "update", "--yes"])
    assert "another Probe setup is running" in result.stderr


def test_a_second_sign_in_is_turned_away_too(held_elsewhere):
    result = CliRunner().invoke(main.app, ["wizard", "--action", "login", "--no-browser"])
    assert result.exit_code == wizard_lock.BUSY_EXIT_CODE


def test_diagnose_runs_while_another_setup_holds_the_lock(held_elsewhere):
    result = CliRunner().invoke(main.app, ["wizard", "--action", "diagnose"])
    assert result.exit_code == 0, result.output


# -- every way in to the same writes respects it --------------------------------


def test_probe_update_is_turned_away_with_75(held_elsewhere):
    result = CliRunner().invoke(main.app, ["update", "--yes"])
    assert (result.exit_code, "probe update: another Probe setup is running" in result.stderr) == (
        wizard_lock.BUSY_EXIT_CODE,
        True,
    )


def test_a_turned_away_update_is_a_skip_doctor_shows(held_elsewhere):
    CliRunner().invoke(main.app, ["update", "--yes"])
    assert autoupdate.load().last_skip.reason == autoupdate.SKIP_SETUP_RUNNING


def test_a_wizard_update_turned_away_is_a_skip_too(held_elsewhere):
    CliRunner().invoke(main.app, ["wizard", "--action", "update", "--yes"])
    assert autoupdate.load().last_skip.reason == autoupdate.SKIP_SETUP_RUNNING


def test_probe_login_is_turned_away_and_saves_nothing(held_elsewhere):
    result = CliRunner().invoke(main.app, ["login", "--token", "probe_pat_new", "--endpoint-only"])
    assert (result.exit_code, (load_context() or {}).get("token")) == (wizard_lock.BUSY_EXIT_CODE, None)


def test_probe_logout_is_turned_away_and_clears_nothing(held_elsewhere):
    save_context({"token": "probe_pat_kept"})
    result = CliRunner().invoke(main.app, ["logout"])
    assert (result.exit_code, (load_context() or {}).get("token")) == (
        wizard_lock.BUSY_EXIT_CODE,
        "probe_pat_kept",
    )


def test_the_detached_auto_updater_exits_75(held_elsewhere):
    assert version_refresh.main(["--apply", "--no-daemon"]) == wizard_lock.BUSY_EXIT_CODE


def test_the_detached_auto_updater_records_the_skip(held_elsewhere):
    version_refresh.main(["--apply", "--no-daemon"])
    assert autoupdate.load().last_skip.reason == autoupdate.SKIP_SETUP_RUNNING


def test_the_run_end_auto_updater_exits_75_when_an_update_is_due(held_elsewhere, monkeypatch):
    from probe.cli import updater

    monkeypatch.setattr(updater, "fetch_latest", lambda _base: {"cli": {"latest": "99.9.9"}})
    assert version_refresh.main(["--apply-if-newer", "--no-daemon"]) == wizard_lock.BUSY_EXIT_CODE


def test_the_auto_updater_takes_the_lock_only_after_its_spawner_exits(held_elsewhere, monkeypatch):
    """The spawner can be a `probe wizard` holding the lock until it exits: the
    lock is asked for after that wait, never before it."""
    order: list[str] = []
    monkeypatch.setenv(autoupdate.WAIT_FOR_PID_ENV, "4242")
    monkeypatch.setattr(autoupdate, "wait_for_pid_exit", lambda _pid, **_: order.append("waited"))
    real_held = wizard_lock.held

    def held():
        order.append("locked")
        return real_held()

    monkeypatch.setattr(wizard_lock, "held", held)
    version_refresh.main(["--apply", "--no-daemon"])
    assert order == ["waited", "locked"]


@pytest.fixture
def update_ran(device, monkeypatch):
    """The update's body, recorded instead of run; `perform_update` around it
    (its spawner wait and its lock) is real."""
    ran: list[dict] = []

    def body(**kwargs):
        ran.append(kwargs)
        return upgrading.UpdateOutcome(lines=["Updated."], ok=True, restart_needed=False)

    monkeypatch.setattr(upgrading, "_perform_update", body)
    return ran


def test_the_wizards_own_update_action_is_not_turned_away_by_itself(update_ran):
    """The wizard holds the lock when its Update action calls `perform_update`,
    which takes it too: the same process holding it goes through."""
    result = CliRunner().invoke(main.app, ["wizard", "--action", "update", "--yes", "--agent", "claude"])
    assert (result.exit_code, len(update_ran)) == (0, 1), result.output


def test_probe_update_is_not_turned_away_by_itself(update_ran):
    result = CliRunner().invoke(main.app, ["update", "--yes"])
    assert (result.exit_code, len(update_ran)) == (0, 1), result.output


def test_the_lock_is_free_once_the_outer_hold_ends():
    with wizard_lock.held():
        with wizard_lock.held():
            pass
        with pytest.raises(BlockingIOError):  # still held after the inner block
            with _held_by_another_process():
                pass
    with _held_by_another_process():
        pass


def test_a_run_turned_away_leaves_pis_sign_in_marker_alone(held_elsewhere):
    """The D4 clean-up writes, so it waits for the lock like every other write."""
    marker = capture.tap_plugin_dir("pi") / ".disabled"
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(capture.AWAITING_CONFIRMATION, encoding="utf-8")
    CliRunner().invoke(main.app, ["wizard", "--action", "update", "--yes"])
    assert marker.exists()
