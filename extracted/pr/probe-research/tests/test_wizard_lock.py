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
from probe.cli import autoupdate, capture, tui, upgrading, version_refresh, wizard_lock
from probe.cli import setup as wizard_setup
from probe.cli.actions import Action
from probe.sdk.config import load_context, save_context
from tests import test_wizard_json_events as events
from tests.test_wizard_auth_entry import entry  # noqa: F401 -- a fixture: the wizard's menu, scripted

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


# -- nothing a person leaves open keeps the lock from updates for a day (C1) -----


def test_a_holder_says_since_when_it_holds_the_lock_and_the_service_reads_it(device):
    """The Probe service updates past a setup that has held the lock for a day
    (`probe.service.updater.LIMITED`). It can tell how long only from the
    record the holder writes into the lock file as it takes it."""
    from probe.service import updater

    before = time.time()
    with wizard_lock.held():
        since = updater.setup_held_since(wizard_lock.lock_path())
    assert since is not None and before <= since <= time.time()
    # Cleared as it lets go: a holder from before the record taking the lock
    # next must not inherit this one's date.
    assert (wizard_lock.lock_path().read_text(), updater.setup_held_since(wizard_lock.lock_path())) == ("", None)


@pytest.mark.parametrize("writer", ["gone", "a-reused-pid"])
def test_a_record_whose_writer_is_not_running_says_nothing_of_the_holder(device, writer):
    """A holder killed with SIGKILL leaves its record behind; a setup from
    before the record that takes the lock next writes none. That old date must
    not read as how long the lock has been held -- nor must it when its pid
    now names another process (a start time that is not the record's): the
    service then counts its own deferrals instead."""
    from probe.service import procid, updater

    if writer == "gone":
        gone = subprocess.Popen([sys.executable, "-c", "pass"])
        gone.wait(timeout=30)
        pid, start = gone.pid, "1"
    else:
        pid, start = os.getpid(), f"{procid.start_time(os.getpid())}0"
    path = wizard_lock.lock_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"pid": pid, "start": start, "at": time.time() - 3 * 86400}))
    assert updater.setup_held_since(path) is None


@pytest.fixture
def menu_elsewhere(device, tmp_path):
    """Another process's `probe wizard` menu waits on a person, its marker
    dated `age` seconds ago (`setup_marks.menu_path`)."""
    from probe._shared import setup_marks
    from probe.sdk import session_marker
    from probe.service import procid

    other = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"])
    start = procid.start_time(other.pid)

    def mark(age: float = 60.0) -> None:
        folder = session_marker.state_dir()
        folder.mkdir(parents=True, exist_ok=True)
        setup_marks.menu_path(folder, other.pid).write_text(
            json.dumps({"pid": other.pid, "start": start, "at": time.time() - age})
        )

    try:
        yield mark
    finally:
        other.kill()
        other.wait(timeout=30)


@pytest.mark.parametrize(
    ("age", "leaves_cli", "runs"),
    [
        (60, None, False),  # it may move the menu's files: in place, or the first switch
        # Bound to go beside the running version (the service says so, and that
        # update never falls back to in place): the files stay where they are.
        (60, "PROBE_UPDATE_SIDE_BY_SIDE", True),
        # Plugins only (the service's, or what follows an adopt's switch).
        (60, "PROBE_UPDATE_SKIP_CLI", True),
        (25 * 3600, None, True),  # a day of waiting at most, as the lock
    ],
)
def test_a_menu_waiting_elsewhere_holds_off_an_update_that_would_move_its_files(
    update_ran, menu_elsewhere, monkeypatch, age, leaves_cli, runs
):
    """The menu lets go of the lock while it waits on a person (C1), but it
    still runs from the CLI's files: an update in place (or the first switch)
    under it fails its next import mid-write. Its marker holds that off, for a
    day at most. Only an update bound to go side by side passes: a side-by-side
    machine still falls back to in place (`PROBE_UPDATE_IN_PLACE`, a receipt
    it cannot restate, no target known), so "this machine can" is not enough."""
    from probe.cli import updater as cli_updater
    from probe.service import updater as service_updater

    assert {cli_updater.REQUIRE_SIDE_BY_SIDE_ENV, upgrading.SKIP_CLI_ENV} == {
        "PROBE_UPDATE_SIDE_BY_SIDE", "PROBE_UPDATE_SKIP_CLI"
    }
    menu_elsewhere(age)
    monkeypatch.setattr(service_updater, "side_by_side", lambda: True)
    if leaves_cli:
        monkeypatch.setenv(leaves_cli, "1")
    result = CliRunner().invoke(main.app, ["wizard", "--action", "update", "--yes", "--agent", "claude"])
    expected = (0, 1) if runs else (wizard_lock.BUSY_EXIT_CODE, 0)
    assert (result.exit_code, len(update_ran)) == expected, result.output
    if not runs:
        assert autoupdate.load().last_skip.reason == autoupdate.SKIP_SETUP_RUNNING
        # The detached auto-updater too, which takes no wizard run lock of its own.
        assert version_refresh.main(["--apply", "--no-daemon"]) == wizard_lock.BUSY_EXIT_CODE


def test_two_menus_each_keep_their_own_marker(menu_elsewhere):
    """Two terminals, two menus: one shared marker let the second overwrite
    the first's and delete it on exit, and an update then ran in place under
    the first. Each has its own; a menu's own Update passes only its own."""
    from probe._shared import setup_marks
    from probe.sdk import session_marker

    menu_elsewhere(60)  # menu A, in another process
    state = session_marker.state_dir()
    setup_marks.mark_menu(state)  # menu B, this process
    assert setup_marks.menu_waiting(state, exclude_pid=os.getpid())[0] is True  # B's Update: A still waits
    assert upgrading.menu_holds_update_off() is True
    setup_marks.unmark_menu(state)  # B exits
    assert setup_marks.menu_waiting(state)[0] is True, "B's exit took A's marker with it"


def test_an_update_the_menu_turns_away_holds_no_lock_while_it_says_so(menu, menu_elsewhere, monkeypatch):
    """Turned away by another menu's marker, the menu's Update takes no lock:
    the page that says so waits on a person, and must hold nothing meanwhile."""
    menu_elsewhere(60)
    picks = iter([Action.UPDATE, Action.EXIT])
    pages: list = []
    monkeypatch.setattr(wizard_setup, "run_action_menu", lambda _caps: next(picks))
    monkeypatch.setattr(tui, "page", lambda lines, **kw: pages.append((lines, wizard_lock.running())))
    monkeypatch.setattr(main, "_run_wizard_action", lambda *a, **kw: pytest.fail("updated under another menu"))
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output
    (lines, locked), = pages
    assert (any(wizard_lock.BUSY_MESSAGE in line for line in lines), locked) == (True, False)


@pytest.mark.parametrize(
    ("forced", "runs"),
    [("setup_running", True), ("run_in_flight,setup_running", True), ("run_in_flight", False)],
)
def test_an_update_the_service_forced_past_a_setup_runs_beside_it(update_ran, monkeypatch, forced, runs):
    """The service updates past a setup that has held the lock for a day and
    tells its update child so (`upgrading.FORCED_ENV`). The child must not then
    turn itself away on that same lock, in the wizard's run lock or in
    `perform_update`'s own; forced past a run alone, it still is."""
    monkeypatch.setenv(upgrading.FORCED_ENV, forced)
    with _held_by_another_process():
        result = CliRunner().invoke(main.app, ["wizard", "--action", "update", "--yes", "--agent", "claude"])
    expected = (0, 1) if runs else (wizard_lock.BUSY_EXIT_CODE, 0)
    assert (result.exit_code, len(update_ran)) == expected, result.output


@pytest.fixture
def menu(entry, tmp_path, monkeypatch):  # noqa: F811 -- `entry` is the imported fixture
    """The interactive wizard, its menu and its actions scripted
    (`test_wizard_auth_entry.entry`), signed in, in a home of its own."""
    for name, sub in (("HOME", "home"), ("CLAUDE_CONFIG_DIR", "claude"), ("CODEX_HOME", "codex"),
                      ("PI_CODING_AGENT_DIR", "pi")):
        monkeypatch.setenv(name, str(tmp_path / sub))
    save_context({"token": "probe_pat_existing", "base_url": "https://api.test"})
    return entry


def test_the_menu_holds_the_lock_only_while_an_action_runs(menu, monkeypatch):
    """The menu held the lock for as long as it stayed open, so a `probe
    wizard` left open in a terminal held every update off, for good (C1). It
    holds it while an action runs, and lets go while it waits on a person: at
    the menu, and at an action's result page. While it waits it says so in its
    marker (an update must not move the files it runs from), gone once the
    wizard exits."""
    from probe._shared import setup_marks
    from probe.sdk import session_marker

    def waiting() -> bool:
        return setup_marks.menu_waiting(session_marker.state_dir())[0]

    seen: list[tuple[str, bool | None, bool]] = []
    picks = iter([Action.SETTINGS, Action.EXIT])
    monkeypatch.setattr(
        wizard_setup, "run_action_menu",
        lambda _caps: seen.append(("menu", wizard_lock.running(), waiting())) or next(picks),
    )
    monkeypatch.setattr(
        main, "_run_wizard_action",
        lambda *a, **kw: seen.append(("action", wizard_lock.running(), waiting())) or ["Saved."],
    )
    monkeypatch.setattr(tui, "page", lambda *a, **kw: seen.append(("page", wizard_lock.running(), waiting())))
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output
    assert seen == [("menu", False, True), ("action", True, True), ("page", False, True), ("menu", False, True)]
    assert not waiting()


def test_an_action_picked_after_another_setup_took_the_lock_changes_nothing(menu, monkeypatch):
    """With the lock let go at the menu, another setup (the desktop app) can
    take it meanwhile: the action picked then is turned away, having run
    nothing, and the menu comes back."""
    other: list = []

    def pick(_caps):
        if not other:
            other.append(open(wizard_lock.lock_path(), "a+"))  # noqa: SIM115 -- closed at the next pick
            oscompat.flock(other[0].fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
            return Action.SETTINGS
        other[0].close()
        return Action.EXIT

    pages: list = []
    monkeypatch.setattr(wizard_setup, "run_action_menu", pick)
    monkeypatch.setattr(tui, "page", lambda lines, **kw: pages.append(lines))
    monkeypatch.setattr(main, "_run_wizard_action", lambda *a, **kw: pytest.fail("ran while another setup held it"))
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output
    assert len(other) == 1 and any(wizard_lock.BUSY_MESSAGE in line for line in pages[0])
