"""Every update's first step in release code (`probe.core.adopt`, plan A1, A2).

`begin` runs first on every update entry -- the service's child
(`probe.core.actions.update`), `probe wizard --action update`, `probe update`,
the detached `version_refresh --apply` -- and either runs the frozen hand-off's
stage 1 (tested in test_handoff.py, the real exec included) or, in the release
a hand-off exec'd (PROBE_UPDATE_ADOPT), adopts: switches the CLI to itself
under the lock it was handed, then lets the update go on with the CLI half
done. HOME, XDG_*, CLAUDE_CONFIG_DIR, CODEX_HOME, PI_CODING_AGENT_DIR and
UV_TOOL_DIR are tmp dirs; nothing is installed for real.
"""

from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

import probe
from probe._shared import handoff, installs
from probe.cli import updater, upgrading
from probe.core import adopt

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="POSIX symlinks and flock")

FAKE_PYTHON = "#!/bin/sh\nexit 0\n"
REAL_RUNS_FROM = adopt._runs_from


def _env(env: Path, version: str) -> Path:
    site = env / "lib" / "python3.12" / "site-packages"
    (site / f"probe_research-{version}.dist-info").mkdir(parents=True, exist_ok=True)
    (env / "bin").mkdir(parents=True, exist_ok=True)
    (env / "bin" / "python").write_text(FAKE_PYTHON)
    (env / "bin" / "python").chmod(0o755)
    return env


@pytest.fixture(autouse=True)
def isolated(tmp_path, monkeypatch):
    for name in ("HOME", "XDG_STATE_HOME", "XDG_CONFIG_HOME", "XDG_DATA_HOME", "CLAUDE_CONFIG_DIR", "CODEX_HOME",
                 "PI_CODING_AGENT_DIR"):
        monkeypatch.setenv(name, str(tmp_path / name.lower()))
    names = (handoff.ADOPT_ENV, handoff.LOCK_FD_ENV, handoff.TRIGGER_ENV, handoff.FROM_ENV,
             handoff.DROPPED_WITH_ENV, upgrading.SKIP_CLI_ENV, "PROBE_UPDATE_BARRIER_TOKEN",
             "PROBE_AUTOUPDATE_TRIGGER", "PROBE_AUTOUPDATE_WAIT_PID")
    for name in names:
        # Set, then taken out: monkeypatch puts back what was there before,
        # also over what an adopt writes into os.environ itself.
        monkeypatch.setenv(name, "x")
        monkeypatch.delenv(name)
    adopt.reset()
    yield
    adopt.reset()
    handoff._held.clear()


@pytest.fixture
def machine(tmp_path, monkeypatch):
    """The CLI as side-by-side installs leave it: the tool path a link to
    0.1.0's env, and 0.2.0's env installed beside it by a hand-off."""
    tools = tmp_path / "share" / "uv" / "tools"
    tools.mkdir(parents=True)
    root = tools.parent / installs.VERSIONS_DIRNAME
    old = _env(root / "0.1.0" / installs.DIST, "0.1.0")
    (tools / installs.DIST).symlink_to(old, target_is_directory=True)
    (root / installs.ACTIVE_NAME).write_text(json.dumps({"active": str(old)}))
    new = _env(root / "0.2.0" / installs.DIST, "0.2.0")
    monkeypatch.setenv("UV_TOOL_DIR", str(tools))
    monkeypatch.setattr(adopt, "_runs_from", lambda target: True)
    monkeypatch.setattr(adopt, "selftest", lambda: None)

    class Machine:
        pass

    m = Machine()
    m.tools, m.root, m.old, m.new = tools, root, old, new
    return m


def _handed(monkeypatch, machine, *, came_from: str = "0.1.0") -> int:
    """What a hand-off's exec leaves: PROBE_UPDATE_ADOPT, the trigger and the
    version it came from, and the install lock's fd held and inherited (not
    this process's own take: `handoff._held` does not know it)."""
    fd = handoff.take_lock(machine.root, wait_s=0)
    assert fd is not None
    handoff._held.clear()
    monkeypatch.setenv(handoff.ADOPT_ENV, str(machine.new))
    monkeypatch.setenv(handoff.LOCK_FD_ENV, str(fd))
    monkeypatch.setenv(handoff.TRIGGER_ENV, "session_start")
    monkeypatch.setenv(handoff.FROM_ENV, came_from)
    return fd


def _closed(fd: int) -> bool:
    try:
        os.fstat(fd)
    except OSError:
        return True
    return False


# -- begin: stage 1 first ----------------------------------------------------------


def test_a_cli_this_machine_does_not_manage_never_hands_off(monkeypatch):
    """An editable checkout, a pip or pipx install, a project's venv: stage 1
    is never asked (plan D4), and the update goes on as before."""
    monkeypatch.setattr(handoff, "stage1", lambda *a, **k: pytest.fail("stage 1 ran"))
    assert adopt.runs_managed_cli() is False  # this test run: an editable install
    assert adopt.begin("cli") is None and adopt.stage1_answer() is None


def test_the_managed_cli_runs_stage_one_first_and_once(monkeypatch, tmp_path):
    asked = []
    monkeypatch.setenv("UV_TOOL_DIR", str(tmp_path / "tools"))
    monkeypatch.setattr(adopt, "runs_managed_cli", lambda: True)
    monkeypatch.setattr(adopt, "install_inputs", lambda: {"extras": ["all"], "with": [], "python_request": None,
                                                         "uv": "/bin/uv"})
    monkeypatch.setattr(handoff, "stage1", lambda trigger, **kw: asked.append((trigger, kw)) or {
        "result": handoff.Result.CURRENT})
    assert adopt.begin("manual", argv=["-m", "probe.cli", "update"]) is None
    assert adopt.begin("manual") is None  # an entry nested in another: not again
    ((trigger, kw),) = asked
    assert trigger == "manual" and kw["argv"] == ["-m", "probe.cli", "update"]
    assert kw["current"] == probe.__version__ and kw["tools"] == str(tmp_path / "tools")
    assert kw["install_inputs"]["uv"] == "/bin/uv"
    assert adopt.stage1_answer() == {"result": handoff.Result.CURRENT}


def test_a_stage_one_that_raises_lets_the_update_go_on(monkeypatch):
    monkeypatch.setattr(adopt, "runs_managed_cli", lambda: True)
    monkeypatch.setattr(adopt, "install_inputs", lambda: {})

    def boom(*_a, **_k):
        raise OSError("disk full")

    monkeypatch.setattr(handoff, "stage1", boom)
    assert adopt.begin("cli") is None
    assert adopt.stage1_answer()["result"] == "error" and "disk full" in adopt.stage1_answer()["detail"]


# -- adopt: the new release switches -------------------------------------------------


def test_the_new_release_switches_under_the_lock_it_was_handed(machine, monkeypatch):
    fd = _handed(monkeypatch, machine)
    real_take = handoff.take_lock
    monkeypatch.setattr(handoff, "take_lock", lambda *a, **k: pytest.fail("flocked a second fd"))

    assert adopt.begin("cli") is None

    assert (machine.tools / installs.DIST).resolve() == machine.new.resolve()
    assert installs.record(machine.tools)["previous"] == str(machine.old.resolve())
    runtime = json.loads((Path.home() / ".local/state/probe/service/runtime.json").read_text())
    assert runtime == {"python": str(machine.new / "bin" / "python"), "cli_version": probe.__version__}
    # The update goes on with the CLI half done; nothing it starts adopts again.
    assert os.environ[upgrading.SKIP_CLI_ENV] == "1"
    assert handoff.ADOPT_ENV not in os.environ and handoff.LOCK_FD_ENV not in os.environ
    # The lock was let go once the switch was made: the plugin steps never hold it.
    assert _closed(fd)
    taken = real_take(machine.root, wait_s=0)
    assert taken is not None
    handoff.release_lock(taken)
    res = adopt.cli_result(probe.__version__)
    assert res.ok and res.changed and res.before == "0.1.0" and res.after == probe.__version__
    assert "CLI upgraded 0.1.0 → " in res.message


def test_a_release_whose_own_update_does_not_load_switches_nothing(machine, monkeypatch):
    fd = _handed(monkeypatch, machine)
    monkeypatch.setattr(adopt, "selftest", lambda: "ImportError: cannot import name 'x'")
    ending = adopt.begin("cli")
    assert ending.status == adopt.FAILED_EXIT and "does not start (ImportError" in ending.message
    assert (machine.tools / installs.DIST).resolve() == machine.old.resolve()
    assert probe.__version__ in installs.rejected(machine.tools)  # stage 1 skips it for 24 h
    assert _closed(fd) and upgrading.SKIP_CLI_ENV not in os.environ


def test_a_release_whose_service_does_not_start_is_never_switched_to(machine, monkeypatch):
    """The checks every switch makes (`installs.selftest`: the service's start
    path and the CLI's import, by the env's own interpreter), before the
    switch: an in-process update (the app's `--json`, the menu) has no guard
    after it."""
    (machine.new / "bin" / "python").write_text(
        '#!/bin/sh\ncase "$*" in *--selftest*) echo "ImportError: no service" >&2; exit 1;; esac\nexit 0\n')
    fd = _handed(monkeypatch, machine)
    ending = adopt.begin("cli")
    assert ending.status == adopt.FAILED_EXIT and "the Probe service would not start" in ending.message
    assert (machine.tools / installs.DIST).resolve() == machine.old.resolve()
    assert probe.__version__ in installs.rejected(machine.tools) and _closed(fd)


def test_the_hand_offs_variables_never_reach_what_the_update_starts(machine, monkeypatch):
    from probe.cli import update_report

    _handed(monkeypatch, machine)
    assert adopt.begin("cli") is None
    for name in (handoff.ADOPT_ENV, handoff.LOCK_FD_ENV, handoff.TRIGGER_ENV, handoff.FROM_ENV,
                 handoff.DROPPED_WITH_ENV):
        assert name not in os.environ, name
    # The report still says what asked for it.
    assert update_report.trigger_from_env(update_report.Trigger.CLI) is update_report.Trigger.SESSION_START


def test_only_the_install_locks_own_fd_is_closed(machine, tmp_path, monkeypatch):
    other = os.open(tmp_path / "not-the-lock", os.O_RDWR | os.O_CREAT)
    try:
        monkeypatch.setenv(handoff.LOCK_FD_ENV, str(other))
        handoff.release_inherited(machine.root)
        assert not _closed(other) and handoff.LOCK_FD_ENV not in os.environ
    finally:
        os.close(other)


def test_an_update_asked_for_in_place_is_never_handed_off(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "prefix", str(tmp_path / "share/uv/probe-versions/0.1.0/probe-research"))
    monkeypatch.setattr(updater, "detect_install", lambda: updater.Install(updater.Method.UV_TOOL))
    monkeypatch.setattr(updater, "kept_from_uv_receipt", lambda prefix=None: updater.KeptInstall())
    assert adopt.runs_managed_cli() is True
    monkeypatch.setenv(updater.IN_PLACE_ENV, "1")
    assert adopt.runs_managed_cli() is False


def test_the_left_out_with_packages_are_forgotten_once_back(machine, monkeypatch):
    _handed(monkeypatch, machine)
    monkeypatch.setenv(handoff.DROPPED_WITH_ENV, json.dumps(["wandb>=0.17", "torch"]))
    assert adopt.begin("cli") is None
    assert installs.dropped_with(machine.tools) == ["wandb>=0.17", "torch"]
    # The next release installed with wandb again (the hand-off tries them first).
    newer = _env(machine.root / "0.3.0" / installs.DIST, "0.3.0")
    (newer / "uv-receipt.toml").write_text(
        '[tool]\nrequirements = [{ name = "probe-research" }, { name = "wandb", specifier = ">=0.17" }]\n')
    adopt.reset()
    machine.new = newer
    _handed(monkeypatch, machine, came_from="0.2.0")
    assert adopt.begin("cli") is None
    assert installs.dropped_with(machine.tools) == ["torch"]


def test_what_the_new_env_lacks_is_read_from_the_receipts_not_remembered(machine, monkeypatch):
    """An earlier hand-off installed 0.2.0 without wandb and was never switched
    to (its check timed out), so its drop reached no record; this one reuses
    that env, drops nothing itself, and hands over no
    PROBE_HANDOFF_DROPPED_WITH. The receipts still say it: the running env had
    wandb and an exact Python, the new one has neither. Recorded, and doctor
    prints how to put both back."""
    from probe.cli import doctor

    (machine.old / "uv-receipt.toml").write_text(
        f'[tool]\npython = "{sys.executable}"\nrequirements = [{{ name = "probe-research" }}, '
        '{ name = "wandb", specifier = ">=0.17" }]\n')
    _handed(monkeypatch, machine)
    assert adopt.begin("cli") is None
    assert installs.dropped_with(machine.tools) == ["wandb>=0.17"]
    assert installs.dropped_python(machine.tools) == sys.executable
    monkeypatch.setattr(sys, "prefix", str(machine.new))
    left, command = doctor._dropped_with_rows()
    assert "wandb>=0.17" in left and f"Python {sys.executable}" in left
    assert command.rstrip().endswith(f"--with 'wandb>=0.17' --python {sys.executable}")


def test_the_adopted_cli_line_says_what_the_old_receipt_could_not_carry(machine, monkeypatch):
    (machine.old / "uv-receipt.toml").write_text(
        '[tool]\nrequirements = [{ name = "probe-research" }, { name = "mine", editable = "/src/mine" }]\n')
    _handed(monkeypatch, machine)
    assert adopt.begin("cli") is None
    assert "--with mine" in adopt.cli_result(probe.__version__).message


def test_an_env_this_interpreter_does_not_run_from_is_never_switched_to(machine, monkeypatch):
    # The real check: this test's interpreter is not 0.2.0's env.
    monkeypatch.setattr(adopt, "_runs_from", REAL_RUNS_FROM)
    _handed(monkeypatch, machine)
    ending = adopt.begin("cli")
    assert ending.status == adopt.FAILED_EXIT and "refusing to switch" in ending.message
    assert (machine.tools / installs.DIST).resolve() == machine.old.resolve()


def test_the_tool_folder_is_the_one_whose_versions_hold_the_handed_env(machine, monkeypatch, tmp_path):
    """A lifeboat's exec can carry a PATH without uv, and uv's default folder
    is not every machine's: the folder the last switch recorded is used, and
    with none that holds the env nothing is switched."""
    monkeypatch.setenv("UV_TOOL_DIR", str(tmp_path / "elsewhere" / "tools"))
    record = json.loads((machine.root / installs.ACTIVE_NAME).read_text())
    (machine.root / installs.ACTIVE_NAME).write_text(json.dumps({**record, "tools": str(machine.tools)}))
    assert adopt.tools_for(machine.new) == machine.tools
    _handed(monkeypatch, machine)
    assert adopt.begin("cli") is None
    assert (machine.tools / installs.DIST).resolve() == machine.new.resolve()

    adopt.reset()
    (machine.root / installs.ACTIVE_NAME).write_text(json.dumps({}))
    _handed(monkeypatch, machine)
    ending = adopt.begin("cli")
    assert ending.status == adopt.FAILED_EXIT and "no uv tool folder" in ending.message


def test_the_with_packages_a_hand_off_left_out_are_recorded_for_doctor(machine, monkeypatch):
    _handed(monkeypatch, machine)
    monkeypatch.setenv(handoff.DROPPED_WITH_ENV, json.dumps(["wandb>=0.17"]))
    assert adopt.begin("cli") is None
    assert installs.dropped_with(machine.tools) == ["wandb>=0.17"]
    assert handoff.DROPPED_WITH_ENV not in os.environ
    missing, command = updater.dropped_with_command(str(machine.new))
    assert missing == ["wandb>=0.17"]
    assert command.startswith("uv tool install 'probe-research[") and command.endswith("--with 'wandb>=0.17'")
    assert f"]=={probe.__version__}'" in command
    from probe.cli import doctor

    monkeypatch.setattr(sys, "prefix", str(machine.new))
    rows = doctor._dropped_with_rows()
    assert "wandb>=0.17" in rows[0] and command in rows[1]
    # Once they are back in the env's receipt, doctor stops naming them.
    (machine.new / "uv-receipt.toml").write_text(
        '[tool]\nrequirements = [{ name = "probe-research" }, { name = "wandb", specifier = ">=0.17" }]\n')
    assert doctor._dropped_with_rows() == []


# -- the first switch waits for a quiet machine ------------------------------------


@pytest.fixture
def unmigrated(machine):
    """Today's install as uv made it: a real folder at the tool path (0.1.0)."""
    (machine.tools / installs.DIST).unlink()
    _env(machine.tools / installs.DIST, "0.1.0")
    (machine.root / "0.1.0").rename(machine.root / "0.1.0-gone")
    return machine


def _busy(monkeypatch, *reasons):
    from probe.service import updater as service_updater

    busy = service_updater.Busy(run="run_in_flight" in reasons, setup="setup_running" in reasons)
    monkeypatch.setattr(service_updater, "look", lambda **_k: busy)


def test_the_first_switch_waits_while_a_run_is_live(unmigrated, monkeypatch):
    from probe._shared import autoupdate

    _handed(monkeypatch, unmigrated)
    _busy(monkeypatch, "run_in_flight")
    ending = adopt.begin("cli")
    assert ending.status == adopt.DEFERRED_EXIT and "quiet machine" in ending.message
    assert not (unmigrated.tools / installs.DIST).is_symlink() and unmigrated.new.exists()
    assert isinstance(installs.record(unmigrated.tools)[adopt.FIRST_SWITCH_WAIT_KEY], float)
    assert autoupdate.load().last_skip.reason == autoupdate.SKIP_RUN_IN_FLIGHT


def test_the_first_switch_goes_ahead_when_the_service_looked(unmigrated, monkeypatch):
    """The service's child: its quiet check (or its 24 h limit) let it run, and
    its barrier holds new `probe` starts while it switches."""
    _handed(monkeypatch, unmigrated)
    _busy(monkeypatch, "run_in_flight")
    monkeypatch.setenv("PROBE_UPDATE_BARRIER_TOKEN", "abc")
    assert adopt.begin("cli") is None
    assert (unmigrated.tools / installs.DIST).resolve() == unmigrated.new.resolve()


_DAY = 24 * 3600


@pytest.mark.parametrize(
    ("found", "switches"),
    [
        ({"run": True}, True),
        # A setup counts by its own age (plan C1), as the service counts it: a
        # wizard.lock held a day is gone past, one taken a minute ago is not --
        # however long this switch itself has waited.
        ({"run": True, "setup": True, "setup_since": -(_DAY + 3600)}, True),
        ({"run": True, "setup": True, "setup_since": -60}, False),
        # A wizard menu waiting on a person runs from the files this switch
        # moves: its marker holds it, a day at most.
        ({"menu": True, "menu_since": -60}, False),
        ({"menu": True, "menu_since": -(_DAY + 3600)}, True),
        # A holder from before the record: this switch's own wait counts.
        ({"setup": True}, True),
    ],
    ids=["run", "setup-held-a-day", "setup-just-taken", "menu-waiting", "menu-waited-a-day", "setup-no-record"],
)
def test_the_first_switch_goes_past_what_held_it_a_day(unmigrated, monkeypatch, found, switches):
    from probe.service import updater as service_updater

    now = time.time()
    installs.set_fields(unmigrated.tools, **{adopt.FIRST_SWITCH_WAIT_KEY: now - 25 * 3600})
    _handed(monkeypatch, unmigrated)
    fields = {k: now + v if k.endswith("_since") else v for k, v in found.items()}
    monkeypatch.setattr(service_updater, "look", lambda **_k: service_updater.Busy(**fields))
    ending = adopt.begin("cli")
    if switches:
        assert ending is None
        assert (unmigrated.tools / installs.DIST).resolve() == unmigrated.new.resolve()
        assert adopt.FIRST_SWITCH_WAIT_KEY not in installs.record(unmigrated.tools)
    else:
        assert ending.status == adopt.DEFERRED_EXIT


@pytest.mark.parametrize(("whose", "switches"), [("its-own", True), ("another-menu", False)])
def test_the_first_switch_never_waits_for_its_own_menu(unmigrated, monkeypatch, whose, switches):
    """A wizard menu's Update execs into the new release with the same pid,
    its menu marker still there: that is no setup to wait for (24 h), while
    another terminal's waiting menu is."""
    from probe._shared import setup_marks
    from probe.service import paths, procid

    state = paths.state_dir()
    if whose == "its-own":
        setup_marks.mark_menu(state)
    other = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"])
    try:
        if whose == "another-menu":
            state.mkdir(parents=True, exist_ok=True)
            setup_marks.menu_path(state, other.pid).write_text(
                json.dumps({"pid": other.pid, "start": procid.start_time(other.pid), "at": time.time() - 60})
            )
        _handed(monkeypatch, unmigrated)
        ending = adopt.begin("cli")
    finally:
        other.kill()
        other.wait(timeout=30)
    assert (ending is None) is switches, ending


# -- every entry runs it first -------------------------------------------------------


@pytest.fixture
def ended(monkeypatch):
    """`begin` answering that the update ends now (an adopt that must wait),
    with what each entry asked it."""
    asked = []
    monkeypatch.setattr(adopt, "begin", lambda trigger, **kw: asked.append((trigger, kw)) or adopt.Ending(
        adopt.DEFERRED_EXIT, "the first switch waits for a quiet machine"))
    return asked


def test_the_service_child_runs_it_before_any_wizard_code(ended, monkeypatch):
    from probe.core import actions, events

    monkeypatch.setattr(actions, "_wizard", lambda *a, **k: pytest.fail("the wizard ran"))
    monkeypatch.setenv("PROBE_AUTOUPDATE_TRIGGER", "session_start")
    seen: list[dict] = []
    assert actions.update(seen.append) == 75
    assert ended == [("session_start", {})]
    assert [e["event"] for e in seen][-2:] == [events.Event.ERROR.value, events.Event.DONE.value]
    assert seen[-2]["code"] == events.ErrorCode.BUSY.value and seen[-1]["exit_code"] == 75


def test_the_service_child_asked_for_plugins_only_runs_no_hand_off(monkeypatch):
    """PROBE_UPDATE_SKIP_CLI: daemon workers run from the CLI's env, which this
    update must leave alone -- installing and switching to a newer one too."""
    from probe.core import actions

    monkeypatch.setenv(upgrading.SKIP_CLI_ENV, "1")
    monkeypatch.setattr(adopt, "begin", lambda *a, **k: pytest.fail("handed off"))
    monkeypatch.setattr(actions, "_wizard", lambda sink, flags: 0)
    assert actions.update() == 0 and adopt.SKIP_CLI_ENV == upgrading.SKIP_CLI_ENV


def test_a_terminal_update_that_adopted_stays_here(monkeypatch):
    """`probe wizard --action update --yes` switched the CLI to the newest
    release in this process: the rest runs here, never sent to the (old)
    service."""
    from typer.testing import CliRunner

    main = importlib.import_module("probe.cli.main")

    def adopted(trigger, **kw):
        adopt._adopted_from = "0.1.0"

    seen = []
    monkeypatch.setattr(adopt, "begin", adopted)
    monkeypatch.setattr(main, "_wizard_on_service", lambda **k: pytest.fail("sent to the old service"))
    monkeypatch.setattr(main, "_wizard_session", lambda **kw: seen.append(kw["action"]))
    result = CliRunner().invoke(main.app, ["wizard", "--action", "update", "--yes"])
    assert result.exit_code == 0, result.output and seen == ["update"]


def test_the_newest_release_gets_the_root_options_and_the_agents(ended, monkeypatch):
    from typer.testing import CliRunner

    main = importlib.import_module("probe.cli.main")
    result = CliRunner().invoke(main.app, ["--base-url", "https://probe.example", "update", "--yes"])
    assert result.exit_code == 75
    assert ended[0][1]["argv"] == ["-m", "probe.cli", "--base-url", "https://probe.example", "update", "--yes"]
    assert main._update_argv(yes=False, agent=["claude_code", "codex"]) == [
        "wizard", "--action", "update", "--agent", "claude_code", "--agent", "codex"]


def test_the_service_child_goes_on_to_the_wizard_after_it(monkeypatch):
    from probe.core import actions

    order = []
    monkeypatch.setattr(adopt, "begin", lambda trigger, **kw: order.append("begin"))
    monkeypatch.setattr(actions, "_wizard", lambda sink, flags: order.append(("wizard", flags["action"])) or 0)
    assert actions.update() == 0 and order == ["begin", ("wizard", "update")]


def test_probe_update_runs_it_before_taking_the_wizard_lock(ended, monkeypatch):
    from typer.testing import CliRunner

    from probe.cli import wizard_lock

    main = importlib.import_module("probe.cli.main")
    monkeypatch.setattr(wizard_lock, "held", lambda: pytest.fail("took the wizard lock"))
    result = CliRunner().invoke(main.app, ["update", "--yes"])
    assert result.exit_code == 75 and "quiet machine" in result.output
    assert ended[0][1]["argv"] == ["-m", "probe.cli", "update", "--yes"]


def test_the_wizards_update_runs_it_first_and_keeps_its_json_contract(ended, monkeypatch):
    from typer.testing import CliRunner

    main = importlib.import_module("probe.cli.main")
    monkeypatch.setattr(main, "_wizard_on_service", lambda **k: pytest.fail("routed before the hand-off"))
    result = CliRunner().invoke(main.app, ["wizard", "--action", "update", "--yes", "--json", "--agent", "codex"])
    assert result.exit_code == 75
    events = [json.loads(line) for line in result.stdout.splitlines() if line.startswith("{")]
    assert events[-1]["event"] == "done" and events[-1]["exit_code"] == 75
    assert any(e.get("code") == "busy" for e in events)
    assert ended[0][1]["argv"] == ["-m", "probe.cli", "wizard", "--action", "update", "--agent", "codex", "--yes",
                                   "--json"]


def test_the_detached_auto_update_runs_it_and_gives_its_lock_back_before_an_exec(ended, monkeypatch):
    from probe.cli import autoupdate, version_refresh

    monkeypatch.setattr(upgrading, "perform_update", lambda **k: pytest.fail("updated in the old code"))
    assert version_refresh._apply() == 75
    ((trigger, kw),) = ended
    assert trigger == "cli" and kw["argv"] == list(version_refresh.APPLY_ARGV)
    assert "before_exec" not in kw  # the lock goes across the exec, never given back first
    assert autoupdate.acquire_lock()  # released either way
    autoupdate.release_lock()


def test_the_auto_update_lock_is_its_holders_across_an_exec(monkeypatch):
    """The exec keeps the pid: the `--apply` run of the newest release finds
    the single-writer lock handed to it (LOCK_HELD_ENV, the file naming this
    pid) and goes on -- once; nothing else takes a held lock."""
    from probe.cli import autoupdate, update_report, version_refresh

    seen = []
    monkeypatch.setattr(adopt, "begin", lambda *a, **k: seen.append(os.environ.get(autoupdate.LOCK_HELD_ENV)))
    assert autoupdate.acquire_lock()
    try:
        assert not autoupdate.acquire_lock()  # held, and not handed over
        version_refresh._hand_off(update_report.Trigger.CLI)
        assert seen == [str(os.getpid())] and autoupdate.LOCK_HELD_ENV not in os.environ
        monkeypatch.setenv(autoupdate.LOCK_HELD_ENV, str(os.getpid()))  # as after the exec
        assert autoupdate.acquire_lock() and autoupdate.LOCK_HELD_ENV not in os.environ
        assert not autoupdate.acquire_lock()  # once
        autoupdate.lock_path().write_text("1")  # another process's
        monkeypatch.setenv(autoupdate.LOCK_HELD_ENV, str(os.getpid()))
        assert not autoupdate.acquire_lock()
    finally:
        autoupdate.release_lock()


# -- the report ----------------------------------------------------------------------


def test_the_report_names_the_trigger_the_hand_off_ran_under(monkeypatch):
    from probe.cli import update_report

    monkeypatch.setenv("PROBE_AUTOUPDATE_TRIGGER", "manual")
    monkeypatch.setenv(handoff.TRIGGER_ENV, "session_start")
    assert update_report.trigger_from_env(update_report.Trigger.CLI) is update_report.Trigger.SESSION_START
    monkeypatch.setenv(handoff.TRIGGER_ENV, "not-a-trigger")  # passed over
    assert update_report.trigger_from_env(update_report.Trigger.CLI) is update_report.Trigger.MANUAL
    monkeypatch.delenv(handoff.TRIGGER_ENV)
    monkeypatch.delenv("PROBE_AUTOUPDATE_TRIGGER")
    assert update_report.trigger_from_env(update_report.Trigger.CLI) is update_report.Trigger.CLI


def test_an_adopted_update_reports_the_cli_it_came_from(monkeypatch):
    """The CLI step of the release that took the update over is the switch it
    made: `before` is the hand-off's version, in the local record, the
    server's report and the wizard's line."""
    from probe.cli import autoupdate

    recorded, reports = [], []
    adopt._adopted_from = "0.1.0"
    monkeypatch.setenv(upgrading.SKIP_CLI_ENV, "1")
    monkeypatch.setattr(updater, "fetch_latest", lambda base: {"cli": {"latest": probe.__version__}})
    monkeypatch.setattr(updater, "detect_install", lambda: updater.Install(updater.Method.UV_TOOL))
    monkeypatch.setattr(updater, "upgrade_cli", lambda *a: pytest.fail("the CLI was upgraded twice"))
    monkeypatch.setattr(autoupdate, "record_attempt", lambda attempt, agent=None: recorded.append(attempt))
    monkeypatch.setattr(upgrading, "_report_attempt", lambda build, **k: reports.append(build()))
    outcome = upgrading.perform_update(base_url="https://x", include_plugin=False)
    assert outcome.ok and outcome.cli == f"Probe CLI {probe.__version__} (updated from 0.1.0)"
    assert recorded[-1].from_version == "0.1.0" and recorded[-1].to_version == probe.__version__
    assert reports[-1]["cli"]["before"] == "0.1.0" and reports[-1]["cli"]["result"] == "updated"


def test_a_rebuild_of_a_broken_env_reports_as_a_change(monkeypatch):
    """The lifeboat rebuilt this very version beside a broken env (hand-off
    v3, `broken_env`) and hands over `PROBE_HANDOFF_FROM=<version>+broken`:
    the CLI step is a change from the broken env -- never "already at", never
    an empty `before` -- in the local record and the server's report (whose
    version pattern takes the local label)."""
    from probe.cli import autoupdate, update_report

    broken = f"{probe.__version__}{handoff.BROKEN_MARK}"
    assert update_report._version(broken) == broken
    recorded, reports = [], []
    adopt._adopted_from = broken
    res = adopt.cli_result(probe.__version__)
    assert res.changed and res.before == broken and res.after == probe.__version__
    monkeypatch.setenv(upgrading.SKIP_CLI_ENV, "1")
    monkeypatch.setattr(updater, "fetch_latest", lambda base: {"cli": {"latest": probe.__version__}})
    monkeypatch.setattr(updater, "detect_install", lambda: updater.Install(updater.Method.UV_TOOL))
    monkeypatch.setattr(updater, "upgrade_cli", lambda *a: pytest.fail("the CLI was upgraded twice"))
    monkeypatch.setattr(autoupdate, "record_attempt", lambda attempt, agent=None: recorded.append(attempt))
    monkeypatch.setattr(upgrading, "_report_attempt", lambda build, **k: reports.append(build()))
    outcome = upgrading.perform_update(base_url="https://x", include_plugin=False)
    assert outcome.ok and outcome.cli == f"Probe CLI {probe.__version__} (updated from {broken})"
    assert recorded[-1].from_version == broken and recorded[-1].to_version == probe.__version__
    assert reports[-1]["cli"]["before"] == broken and reports[-1]["cli"]["after"] == probe.__version__
    assert reports[-1]["cli"]["result"] == "updated"
