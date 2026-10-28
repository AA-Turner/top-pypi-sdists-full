"""The lifeboat: a hand-off kept outside every release, and its frozen wrapper
(plan fool-proof-updates B1, B2, B5; `probe.service.lifeboat`).

What these hold:
  * the wrapper (`/bin/sh L/lifeboat.sh <trigger>`, run here under /bin/sh)
    picks its python in the contract's order (env.json's base_python, `uv
    python find`, /usr/bin/python3, env.json's active_python), runs
    `current/handoff.py`, and falls back to `known-good/` when current is
    missing, fails --selftest or exits non-zero; it always exits 0, and for
    `keeper` runs the active release's keeper after;
  * a release writes only `current/`, only when its HANDOFF_VERSION is higher
    or current is missing or broken, and only a copy that passes --selftest;
    `known-good/` is bootstrapped once and otherwise only promoted, after
    current ran and a cycle ended at the manifest's latest, never from a test
    HOME;
  * what the lifeboat did (`acted.json`) is read and dropped as the contract says;
  * the wrapper and the keeper's unit writers are frozen (digest-pinned).

Every test runs in a throwaway HOME (with XDG_STATE_HOME, XDG_CONFIG_HOME,
CLAUDE_CONFIG_DIR, CODEX_HOME and PI_CODING_AGENT_DIR beside it): the real
account's lifeboat, units and user manager are never touched. The hand-off is
a stub (`_stub`): PR A's `handoff.py` is pinned by its own frozen test.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

from probe.service import keeper, lifeboat, paths

pytestmark = pytest.mark.skipif(os.name != "posix", reason="the lifeboat is POSIX-only (/bin/sh)")

SHARED = Path(lifeboat.__file__).resolve().parent.parent / "_shared"
#: `keeper.wanted` as the suite has it: False (a test HOME, PROBE_SERVICE_KEEPER=0).
_WANTED = keeper.wanted
#: sha256(lifeboat.sh)[:16]. FROZEN: every keeper unit and every session start
#: on every machine runs this file, whatever release is installed. Change it
#: deliberately (a new release cannot take a broken one back), then pin it here.
FROZEN_WRAPPER = "d6a8824481ec05c0"
#: sha256 of the keeper's unit text for a fixed wrapper path[:16]: the systemd
#: timer and service, and the launchd agent (`keeper._systemd_units`,
#: `keeper._plist`). FROZEN with the wrapper: change deliberately.
FROZEN_UNITS = "daa5f4ce81412a70"


@pytest.fixture
def home(tmp_path, monkeypatch):
    """A throwaway HOME and every agent/state folder beside it."""
    root = tmp_path / "home"
    root.mkdir()
    for name, sub in (("HOME", ""), ("XDG_STATE_HOME", ".xdg-state"), ("XDG_CONFIG_HOME", ".config"),
                      ("CLAUDE_CONFIG_DIR", ".claude"), ("CODEX_HOME", ".codex"),
                      ("PI_CODING_AGENT_DIR", ".pi")):
        monkeypatch.setenv(name, str(root / sub) if sub else str(root))
    assert lifeboat.root() == root / ".local" / "state" / "probe" / "lifeboat"
    return root


def _stub(path: Path, *, version: int = 1, selftest: int = 0, run: int = 0, acts: bool = False,
          replaced: bool = False) -> Path:
    """A stand-in handoff.py: its version, what --selftest and lifeboat mode
    exit with, and a line per call in $LIFEBOAT_TEST_LOG (which slot, which
    interpreter, what it was asked). `acts`: its lifeboat mode starts a
    rescue, as handoff.py records one (state.json's `last_act`, written before
    it detaches stage 1). `replaced`: a release places a new copy over it while
    it runs."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"HANDOFF_VERSION = {version}\n"
        "import json, os, sys, time\n"
        "def _log(what):\n"
        "    log = os.environ.get('LIFEBOAT_TEST_LOG')\n"
        "    if log:\n"
        "        with open(log, 'a') as out:\n"
        "            out.write(json.dumps({'slot': os.path.basename(os.path.dirname(os.path.abspath(__file__))),\n"
        "                                  'what': what, 'python': sys.executable, 'argv': sys.argv[1:]}) + '\\n')\n"
        "if '--selftest' in sys.argv:\n"
        f"    _log('selftest'); sys.exit({selftest})\n"
        "_log('lifeboat')\n"
        "L = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n"
        f"if {acts}:\n"
        "    state = os.path.join(L, 'state.json')\n"
        "    with open(state, 'w') as out:\n"
        "        json.dump({'v': 1, 'first_seen_behind': 1.0, 'behind_version': '0.330.0', 'last_act':\n"
        "                   {'at': time.time(), 'reason': 'behind', 'from': '0.325.0', 'to': '0.330.0'}}, out)\n"
        f"if {replaced}:\n"
        "    with open(os.path.abspath(__file__), 'a') as out:\n"
        "        out.write('# a newer copy\\n')\n"
        f"sys.exit({run})\n"
    )
    return path


def _fake_python(folder: Path, name: str, *, works: bool = True, keeper_ok: bool = True) -> Path:
    """An interpreter stand-in: logs `<name> <args>` to $LIFEBOAT_TEST_PYLOG,
    then runs the real one (`works`) or fails as a missing one would. Asked for
    the keeper (`-m probe.service.keeper`), it only logs."""
    folder.mkdir(parents=True, exist_ok=True)
    script = folder / name
    body = f'exec "{sys.executable}" "$@"' if works else "exit 127"
    keeper_line = 'case "$*" in *probe.service.keeper*) exit 0 ;; esac\n' if keeper_ok else ""
    script.write_text(
        "#!/bin/sh\n"
        f'printf "%s %s\\n" "{name}" "$*" >> "$LIFEBOAT_TEST_PYLOG"\n'
        f"{keeper_line}{body}\n"
    )
    script.chmod(0o755)
    return script


def _fake_uv(folder: Path, finds: Path | None) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    uv = folder / "uv"
    answer = f'echo "{finds}"; exit 0' if finds is not None else "exit 2"
    uv.write_text(f'#!/bin/sh\ncase "$1 $2" in "python find") {answer} ;; esac\nexit 2\n')
    uv.chmod(0o755)
    return uv


class Boat:
    """A lifeboat folder laid out by hand, and its wrapper run under /bin/sh."""

    def __init__(self, home: Path, tmp: Path) -> None:
        self.home = home
        self.tmp = tmp
        self.root = lifeboat.root()
        self.root.mkdir(parents=True, mode=0o700)
        shutil.copyfile(SHARED / "lifeboat.sh", self.root / "lifeboat.sh")
        self.bin = tmp / "bin"
        self.bin.mkdir()
        self.log = tmp / "handoff.log"
        self.pylog = tmp / "python.log"

    def env_json(self, **fields) -> None:
        (self.root / "env.json").write_text(json.dumps({"v": 1, **fields}, indent=1) + "\n")

    def run(self, trigger: str = "session", **extra: str) -> subprocess.CompletedProcess:
        env = {
            "HOME": str(self.home), "PATH": f"{self.bin}:/usr/bin:/bin",
            "LIFEBOAT_TEST_LOG": str(self.log), "LIFEBOAT_TEST_PYLOG": str(self.pylog), **extra,
        }
        return subprocess.run(["/bin/sh", str(self.root / "lifeboat.sh"), trigger], env=env,
                              capture_output=True, text=True, timeout=120, cwd="/")

    def calls(self) -> list[dict]:
        return [json.loads(line) for line in self.log.read_text().splitlines()] if self.log.exists() else []

    def pythons(self) -> list[str]:
        return self.pylog.read_text().splitlines() if self.pylog.exists() else []


@pytest.fixture
def boat(home, tmp_path):
    return Boat(home, tmp_path)


# -- the wrapper -------------------------------------------------------------------


def test_the_wrapper_runs_current_with_the_first_python_in_the_contracts_order(boat):
    """base_python first; a broken one is passed over for `uv python find`'s;
    active_python is never needed while an earlier one works."""
    base = _fake_python(boat.tmp / "py", "base", works=False)
    found = _fake_python(boat.tmp / "py", "uvpython")
    active = _fake_python(boat.tmp / "py", "active")
    _fake_uv(boat.bin, found)
    boat.env_json(base_python=str(base), active_python=str(active))
    _stub(boat.root / "current" / "handoff.py")
    assert boat.run("cli").returncode == 0
    order = [line.split(" ", 1)[0] for line in boat.pythons()]
    assert order == ["base", "uvpython", "uvpython"], "base fails its selftest; uv's passes it and runs it"
    assert [(c["slot"], c["what"]) for c in boat.calls()] == [("current", "selftest"), ("current", "lifeboat")]
    assert boat.calls()[-1]["argv"] == ["--lifeboat", "--trigger", "cli"]
    assert "-I -S" in boat.pythons()[-1], "isolated, no site: the hand-off is stdlib only"


def test_env_jsons_uv_is_used_when_none_is_on_path(boat):
    found = _fake_python(boat.tmp / "py", "uvpython")
    uv = _fake_uv(boat.tmp / "uv-home", found)
    boat.env_json(uv=str(uv))
    _stub(boat.root / "current" / "handoff.py")
    boat.run()
    assert [line.split(" ", 1)[0] for line in boat.pythons()] == ["uvpython", "uvpython"]


@pytest.mark.skipif(not os.access("/usr/bin/python3", os.X_OK), reason="no /usr/bin/python3 on this machine")
def test_the_system_python_comes_before_the_active_envs(boat):
    base = _fake_python(boat.tmp / "py", "base", works=False)
    active = _fake_python(boat.tmp / "py", "active")
    boat.env_json(base_python=str(base), active_python=str(active))
    _stub(boat.root / "current" / "handoff.py")
    boat.run()
    assert [c["python"] for c in boat.calls()] == ["/usr/bin/python3"] * 2
    assert [line.split(" ", 1)[0] for line in boat.pythons()] == ["base"], "the active env's never asked"


def test_the_active_envs_python_is_the_last_candidate(boat, monkeypatch):
    """Python's own list (the installer's selftest) is the wrapper's, in order."""
    base = _fake_python(boat.tmp / "py", "base", works=False)
    found = _fake_python(boat.tmp / "py", "uvpython")
    active = _fake_python(boat.tmp / "py", "active")
    uv = _fake_uv(boat.tmp / "uv-home", found)
    monkeypatch.setattr(lifeboat, "SYSTEM_PYTHON", str(boat.tmp / "no-such-python"))
    monkeypatch.setenv("PATH", "/usr/bin:/bin")  # no uv of this machine's
    env = {"base_python": str(base), "uv": str(uv), "active_python": str(active)}
    assert list(lifeboat.candidates(env)) == [str(base), str(found), str(active)]
    assert list(lifeboat.candidates({"base_python": str(active), "active_python": str(active)})) == [str(active)]


def test_a_missing_current_falls_back_to_known_good(boat):
    boat.env_json(base_python=sys.executable)
    _stub(boat.root / "known-good" / "handoff.py")
    assert boat.run().returncode == 0
    assert [(c["slot"], c["what"]) for c in boat.calls()] == [("known-good", "selftest"), ("known-good", "lifeboat")]


@pytest.mark.parametrize(
    "current",
    [
        pytest.param({"selftest": 1}, id="fails-its-selftest"),
        pytest.param({"run": 3}, id="internal-error-exit-3"),
        pytest.param({"run": 1}, id="a-traceback-exit-1"),
    ],
)
def test_a_broken_current_falls_back_to_known_good(boat, current):
    boat.env_json(base_python=sys.executable)
    _stub(boat.root / "current" / "handoff.py", **current)
    _stub(boat.root / "known-good" / "handoff.py")
    assert boat.run().returncode == 0
    slots = [(c["slot"], c["what"]) for c in boat.calls()]
    assert slots[-2:] == [("known-good", "selftest"), ("known-good", "lifeboat")]
    if current.get("selftest"):
        assert ("current", "lifeboat") not in slots, "a copy that fails its selftest is never run"
    assert not (boat.root / "current" / ".acted").exists()


def _current(boat) -> Path:
    return boat.root / "current" / "handoff.py"


def test_a_run_that_did_nothing_proves_nothing(boat):
    """`.ran` used to be touched by any run that exited 0, a no-op one too."""
    boat.env_json(base_python=sys.executable)
    _stub(_current(boat))
    _stub(boat.root / "known-good" / "handoff.py")
    boat.run()
    assert [c["slot"] for c in boat.calls()] == ["current", "current"]
    assert not (boat.root / "current" / ".acted").exists()
    assert lifeboat.rescued_at(_current(boat)) is None


def test_a_run_that_started_a_rescue_stamps_its_slot(boat):
    boat.env_json(base_python=sys.executable)
    _stub(_current(boat), acts=True)
    _stub(boat.root / "known-good" / "handoff.py")
    boat.run("keeper")
    assert lifeboat.rescued_at(_current(boat)) is not None, "this copy rescued the machine"
    assert not (boat.root / "known-good" / ".acted").exists()


def test_a_copy_replaced_while_it_ran_is_never_stamped(boat):
    """An old copy finishing after a release placed a new one proves nothing of the new one."""
    boat.env_json(base_python=sys.executable)
    _stub(_current(boat), acts=True, replaced=True)
    boat.run()
    assert not (boat.root / "current" / ".acted").exists()


def _rescued_hours_ago(boat, hours: float, *, behind: str | None = "0.330.0", to: str = "0.330.0") -> None:
    """current/ started a rescue `hours` ago, for `to`; state.json now says `behind`."""
    stamp = boat.root / "current" / ".acted"
    stamp.touch()
    at = time.time() - hours * 3600
    os.utime(_current(boat), (at - 60, at - 60))
    os.utime(stamp, (at, at))
    (boat.root / "state.json").write_text(json.dumps({
        "v": 1, "first_seen_behind": 1.0 if behind else None, "behind_version": behind,
        "last_act": {"at": at, "reason": "behind", "from": "0.325.0", "to": to},
    }))


def test_known_good_runs_instead_once_currents_own_rescue_failed(boat):
    """Two hours after current's rescue the machine is still behind that
    release: current's rescue is what failed (R12), so known-good acts."""
    boat.env_json(base_python=sys.executable)
    _stub(_current(boat))
    _stub(boat.root / "known-good" / "handoff.py")
    _rescued_hours_ago(boat, 2.5)
    assert boat.run().returncode == 0
    assert [c["slot"] for c in boat.calls()] == ["known-good", "known-good"], "current is not run at all"


@pytest.mark.parametrize(
    "hours, behind, to",
    [
        pytest.param(1.0, "0.330.0", "0.330.0", id="its-rescue-still-has-time"),
        pytest.param(3.0, None, "0.330.0", id="the-machine-caught-up"),
        pytest.param(3.0, "0.331.0", "0.330.0", id="a-newer-release-is-currents-to-try"),
    ],
)
def test_current_keeps_running_while_its_rescue_has_not_failed(boat, hours, behind, to):
    boat.env_json(base_python=sys.executable)
    _stub(_current(boat))
    _stub(boat.root / "known-good" / "handoff.py")
    _rescued_hours_ago(boat, hours, behind=behind, to=to)
    boat.run()
    assert [c["slot"] for c in boat.calls()] == ["current", "current"]


def test_a_rescue_by_the_copy_before_says_nothing_of_a_new_current(boat):
    boat.env_json(base_python=sys.executable)
    _stub(boat.root / "known-good" / "handoff.py")
    _stub(_current(boat))
    _rescued_hours_ago(boat, 3.0)
    os.utime(_current(boat), None)  # a release placed a new copy since that rescue
    boat.run()
    assert [c["slot"] for c in boat.calls()] == ["current", "current"]


@pytest.mark.parametrize("trigger", ["keeper", "session", "cli", "bogus", ""])
def test_the_wrapper_always_exits_0(boat, trigger):
    boat.env_json(base_python=sys.executable)
    _stub(boat.root / "current" / "handoff.py", run=3)
    _stub(boat.root / "known-good" / "handoff.py", run=3)
    done = boat.run(trigger)
    assert done.returncode == 0, done.stderr
    if trigger in lifeboat.TRIGGERS:
        assert [c["slot"] for c in boat.calls() if c["what"] == "lifeboat"] == ["current", "known-good"]
    else:
        assert boat.calls() == [], "an unknown trigger runs nothing"


def _bounded(tmp_path: Path, body: str) -> Path:
    """The wrapper's own watchdog (`bounded`, its tick set-up), then `body`."""
    text = (SHARED / "lifeboat.sh").read_text()
    start = text.index("if sleep 0.0")
    end = text.index("\n}\n", text.index("bounded() {")) + 3
    script = tmp_path / "bounded.sh"
    script.write_text(text[start:end] + body)
    return script


def _left_in_session(sid: int) -> list[str]:
    """Every process still in session `sid` (what systemd finds in a stopped unit)."""
    left = []
    for stat in Path("/proc").glob("[0-9]*/stat"):
        try:
            raw = stat.read_text()
        except OSError:
            continue
        fields = raw[raw.rfind(")") + 2:].split()
        if len(fields) > 3 and fields[3] == str(sid):
            left.append(raw[raw.find("(") + 1: raw.rfind(")")])
    return left


#: /bin/sh (dash on Debian/Ubuntu), and bash in POSIX mode: macOS's /bin/sh.
SHELLS = [["/bin/sh"]] + ([["/bin/bash", "--posix"]] if os.access("/bin/bash", os.X_OK) else [])


@pytest.mark.skipif(not Path("/proc/self/stat").exists(), reason="reads /proc for what a run leaves behind")
@pytest.mark.parametrize("shell", SHELLS, ids=lambda argv: " ".join(argv))
def test_the_watchdog_stops_a_hung_child_and_leaves_no_process_behind(tmp_path, shell):
    """A child past its limit gets TERM, one that ignores it KILL 5 s later; a
    quick one returns at once. Afterwards nothing of the wrapper's runs on:
    the watchdog's sleeps used to (killed mid-`sleep 1`), and systemd logged
    each one as left in the stopped keeper unit, 4 times a minute (harness P3)."""
    script = _bounded(tmp_path, (
        "bounded 1 sh -c 'trap \"\" TERM; exec sleep 30'; echo \"rc=$?\"\n"
        "bounded 1 sh -c 'exec sleep 30'; echo \"rc=$?\"\n"
        "bounded 30 sh -c 'exit 3'; echo \"rc=$?\"\n"
    ))
    began = time.monotonic()
    run = subprocess.Popen([*shell, str(script)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                           text=True, start_new_session=True)
    out, _ = run.communicate(timeout=60)
    took = time.monotonic() - began
    assert out.split() == ["rc=137", "rc=143", "rc=3"]
    assert 7.0 < took < 12.0, "about 1 + 5 s, then 1 s, then at once"
    assert _left_in_session(run.pid) == []


@pytest.mark.heavy
@pytest.mark.skipif(not Path("/proc/self/stat").exists(), reason="reads /proc for what a run leaves behind")
@pytest.mark.parametrize("shell", SHELLS, ids=lambda argv: " ".join(argv))
def test_a_child_that_will_not_die_is_left_behind_30_s_past_its_limit(tmp_path, shell):
    """A process in an uninterruptible wait ignores TERM and KILL alike: the
    wrapper goes on without it (124) 30 s past its limit, never forever.
    Stood in by a `kill` that does not deliver them."""
    script = _bounded(tmp_path, (
        'kill() { case $1 in -TERM|-KILL) return 0 ;; esac; command kill "$@"; }\n'
        'bounded 1 sleep 120 >/dev/null; echo "rc=$?"\n'  # the sleep left behind holds no pipe
    ))
    began = time.monotonic()
    run = subprocess.Popen([*shell, str(script)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                           text=True, start_new_session=True)
    try:
        out, _ = run.communicate(timeout=90)
    finally:
        import signal

        with contextlib.suppress(OSError):
            os.killpg(run.pid, signal.SIGKILL)  # the sleep it left behind
    assert out.split() == ["rc=124"]
    assert 30.0 < time.monotonic() - began < 45.0


def test_with_nothing_installed_the_wrapper_still_exits_0(boat):
    assert boat.run("keeper").returncode == 0
    assert boat.calls() == []


def test_the_keeper_trigger_runs_the_active_keeper_after_the_hand_off(boat):
    active = _fake_python(boat.tmp / "py", "active")
    boat.env_json(base_python=sys.executable, active_python=str(active))
    _stub(boat.root / "current" / "handoff.py")
    boat.run("keeper")
    assert boat.pythons()[-1] == "active -I -m probe.service.keeper"
    assert [c["what"] for c in boat.calls()] == ["selftest", "lifeboat"], "the hand-off ran first"
    boat.pylog.unlink()
    boat.run("session")
    assert not any("probe.service.keeper" in line for line in boat.pythons()), "only the keeper's trigger"


def test_with_no_env_json_the_keeper_is_found_through_runtime_json(boat):
    """A lifeboat whose env.json is gone still runs the keeper every minute (as
    the unit did before it): runtime.json's python, the CLI's own record."""
    active = _fake_python(boat.tmp / "py", "runtime")
    runtime = paths.runtime_path()
    runtime.parent.mkdir(parents=True, exist_ok=True)
    runtime.write_text(json.dumps({"python": str(active), "cli_version": "0.325.1"}))
    assert boat.run("keeper").returncode == 0
    assert boat.pythons() == ["runtime -I -m probe.service.keeper"]


# -- the slots, as a release writes them ---------------------------------------------


@pytest.fixture
def release(home, tmp_path, monkeypatch):
    """This release's packaged files (the real wrapper, a stub hand-off) and an
    env.json that names this interpreter, with no uv and no login shell asked."""
    shared = tmp_path / "release" / "_shared"
    shared.mkdir(parents=True)
    shutil.copyfile(SHARED / "lifeboat.sh", shared / "lifeboat.sh")
    _stub(shared / "handoff.py", version=2)
    monkeypatch.setattr(lifeboat, "_SHARED", shared)
    monkeypatch.setattr(lifeboat, "env_record", lambda login=None: {
        "v": 1, "base_python": sys.executable, "active_python": sys.executable, "uv": None,
    })
    monkeypatch.setattr(lifeboat, "SYSTEM_PYTHON", str(tmp_path / "no-system-python"))
    monkeypatch.setenv("PATH", "/usr/bin:/bin")  # no uv: `uv python find` is never this machine's
    return shared


def _slot(name: str) -> Path:
    return lifeboat.root() / name / "handoff.py"


def test_the_first_install_writes_current_and_bootstraps_known_good_from_it(release):
    assert lifeboat.install() == "installed (lifeboat.sh, current, known-good)"
    assert _slot("current").read_bytes() == (release / "handoff.py").read_bytes() == _slot("known-good").read_bytes()
    assert (lifeboat.root() / "lifeboat.sh").read_bytes() == (SHARED / "lifeboat.sh").read_bytes()
    assert json.loads((lifeboat.root() / "env.json").read_text())["base_python"] == sys.executable
    assert oct(lifeboat.root().stat().st_mode & 0o777) == "0o700"
    assert lifeboat.install() == "current", "nothing changed: nothing written"


def test_a_higher_handoff_version_replaces_current_and_never_known_good(release):
    _stub(_slot("current"), version=1)
    _stub(_slot("known-good"), version=1)
    known = _slot("known-good").read_bytes()
    assert lifeboat.install() == "installed (lifeboat.sh, current)"
    assert lifeboat.handoff_version(_slot("current")) == 2
    assert _slot("known-good").read_bytes() == known


@pytest.mark.parametrize("installed", [2, 3])
def test_an_equal_or_lower_packaged_version_leaves_a_working_current(release, installed):
    """A release switched back to (older code) never undoes a newer lifeboat."""
    _stub(_slot("current"), version=installed)
    _stub(_slot("known-good"), version=1)
    before = _slot("current").read_bytes()
    assert lifeboat.install() == "installed (lifeboat.sh)"
    assert _slot("current").read_bytes() == before


def test_a_current_that_fails_its_selftest_is_replaced_whatever_its_version(release):
    _stub(_slot("current"), version=9, selftest=1)
    _stub(_slot("known-good"), version=1)
    assert lifeboat.install() == "installed (lifeboat.sh, current)"
    assert lifeboat.handoff_version(_slot("current")) == 2


def test_a_packaged_copy_that_fails_its_selftest_is_never_placed(release):
    _stub(release / "handoff.py", version=5, selftest=1)
    _stub(_slot("current"), version=1)
    outcome = lifeboat.install()
    assert outcome.startswith("failed: this release's handoff.py passes --selftest under no python")
    assert lifeboat.handoff_version(_slot("current")) == 1
    assert not list(_slot("current").parent.glob(".handoff.py.*")), "the trial copy goes"
    assert not _slot("known-good").exists(), "nothing proven: no known-good from a broken copy"


def test_a_new_current_must_prove_itself_again(release):
    _stub(_slot("current"), version=1)
    (_slot("current").parent / ".acted").touch()
    lifeboat.install()
    assert lifeboat.rescued_at(_slot("current")) is None, "the old copy's rescue proves nothing of the new one"
    assert not (_slot("current").parent / ".acted").exists()


def test_install_lifeboat_has_the_keepers_guards(release, monkeypatch):
    """The end of an update and `probe doctor` install it too (a pod where no
    service runs), never under a test's HOME, never after an Uninstall."""
    assert keeper.install_lifeboat() == "not wanted"
    assert not lifeboat.root().exists()
    monkeypatch.setattr(keeper, "wanted", lambda: True)
    assert keeper.install_lifeboat({"UV_INDEX_URL": "https://pypi.internal/simple"}).startswith("installed")
    assert _slot("current").is_file() and _slot("known-good").is_file()
    paths.private_dir(paths.root_dir())
    (paths.root_dir() / keeper.OFF_NAME).touch()
    assert keeper.install_lifeboat() == "not wanted (uninstalled)"


@pytest.fixture
def an_update(monkeypatch):
    """`perform_update(s)` with its halves stood in (as test_parallel_install_update's),
    the CLI's step answering `cli["ok"]`, and every lifeboat refresh counted."""
    from probe.cli import updater, upgrading

    cli = {"ok": True}
    refreshed: list = []
    monkeypatch.setattr(updater, "fetch_latest", lambda base: {})
    monkeypatch.setattr(updater, "detect_install", lambda: updater.Install(updater.Method.UV_TOOL))
    monkeypatch.setattr(upgrading, "_report_attempt", lambda *a, **k: None)
    monkeypatch.setattr(updater, "upgrade_cli", lambda install, current, target: updater.CliResult(
        ran=True, ok=cli["ok"], changed=False, before=current, after=current, message="cli step"))
    monkeypatch.setattr(upgrading, "_update_pi_package", lambda: upgrading._PiUpdate(["pi current"]))
    plugin = updater.PluginResult(attempted=True, confirmed=True, changed=False, before="1", after="1",
                                  message="plugin current")
    monkeypatch.setattr(updater, "update_plugin", lambda *a: plugin)
    monkeypatch.setattr(updater, "update_codex_plugins", lambda *a: plugin)
    monkeypatch.setattr(updater, "stale_tap_daemons", lambda *a, **k: ())
    monkeypatch.setattr(updater, "follows_without_restart", lambda *a, **k: False)
    monkeypatch.setattr(upgrading.root_skills, "refresh", lambda source: [])
    monkeypatch.setattr(keeper, "refresh_lifeboat", lambda: refreshed.append(1) or "current")
    return SimpleNamespace(cli=cli, refreshed=refreshed, upgrading=upgrading)


@pytest.mark.parametrize("many", [False, True], ids=["perform_update", "perform_updates"])
def test_every_update_whose_cli_step_ended_ok_refreshes_the_lifeboat(an_update, many):
    """Whatever ran it: the service's child, a session start's own update on a
    pod with no service, `probe update`, a run's end (all of them end here)."""
    def run():
        if many:
            return an_update.upgrading.perform_updates(["claude_code", "codex"], base_url="https://x")
        return an_update.upgrading.perform_update(base_url="https://x")

    run()
    assert an_update.refreshed == [1]
    an_update.cli["ok"] = False
    run()
    assert an_update.refreshed == [1], "a CLI step that failed installed no release to take it from"


def test_an_update_a_live_run_deferred_refreshes_nothing(an_update, monkeypatch):
    from probe.cli import autoupdate, run_lock, update_report

    monkeypatch.setattr(run_lock, "any_live", lambda: True)
    monkeypatch.setattr(autoupdate, "record_skip", lambda *a, **k: None)
    monkeypatch.setattr(update_report, "flush", lambda *a, **k: None)
    monkeypatch.delenv(an_update.upgrading.FORCED_ENV, raising=False)
    an_update.upgrading.perform_update(base_url="https://x")
    assert an_update.refreshed == []


def test_a_refresh_asks_the_login_shell_with_a_clean_environment(monkeypatch):
    """An update or `probe doctor` can run inside an agent's sandbox, whose
    localhost proxy only its own processes can use: never stored. The login
    shell is asked with the service's clean environment; no answer keeps the
    last index settings (`install_lifeboat(None)`)."""
    import asyncio

    from probe.service import loginenv

    seen: dict = {}

    async def read(**kwargs):
        seen.update(kwargs)
        return None

    monkeypatch.setattr(loginenv, "read", read)
    monkeypatch.setenv("HTTPS_PROXY", "http://localhost:3128")
    assert lifeboat.login_env() is None
    assert "HTTPS_PROXY" not in seen["env"] and seen["env"]["HOME"] == os.environ["HOME"]
    asked: list = []
    monkeypatch.setattr(keeper, "install_lifeboat", lambda login=None: asked.append(login) or "current")
    assert keeper.refresh_lifeboat() == "not wanted" and asked == []
    monkeypatch.setattr(keeper, "wanted", lambda: True)
    assert keeper.refresh_lifeboat() == "current" and asked == [None]
    assert asyncio.run(read(env={})) is None


def test_probe_doctor_refreshes_the_lifeboat(monkeypatch):
    import importlib
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import capabilities, doctor, probe_config_cli, service_calls

    main = importlib.import_module("probe.cli.main")
    asked: list = []
    monkeypatch.setattr(capabilities, "refresh_mcp_token_verdict", lambda: None)
    monkeypatch.setattr(doctor, "collect", lambda: SimpleNamespace(outbox_status=None))
    monkeypatch.setattr(doctor, "rescue_outbox", lambda: None)
    monkeypatch.setattr(doctor, "render", lambda *args, **kwargs: "rendered")
    monkeypatch.setattr(doctor, "codex_hook_rows", lambda caps: [])
    monkeypatch.setattr(service_calls, "view", lambda: {})
    monkeypatch.setattr(probe_config_cli, "doctor_rows", lambda fix: [])
    monkeypatch.setattr(keeper, "refresh_lifeboat", lambda: asked.append(1) or "current")
    result = CliRunner().invoke(main.app, ["doctor"])
    assert result.exit_code == 0, result.output
    assert asked == [1]


def test_a_release_without_a_handoff_installs_the_wrapper_only(release):
    (release / "handoff.py").unlink()
    assert lifeboat.install() == "no handoff in this release (lifeboat.sh)"
    assert lifeboat.wrapper_path().is_file() and not _slot("current").exists()


def test_the_service_installs_nothing_under_a_test_home(home):
    """The keeper's guards are the lifeboat's: a HOME that is not the account's own."""
    assert keeper.install() == "not wanted"
    assert not lifeboat.root().exists()


# -- promotion -------------------------------------------------------------------------


@pytest.fixture
def placed(release, monkeypatch):
    """A current/ placed (v2) beside an older known-good/ (v1), the keeper wanted."""
    _stub(_slot("current"), version=1)
    _stub(_slot("known-good"), version=1)
    lifeboat.install()
    monkeypatch.setattr(keeper, "wanted", lambda: True)
    return _slot("current")


def _acted(current: Path) -> float:
    """current/'s copy started a rescue (the wrapper's stamp), a moment after it was placed."""
    stamp = current.parent / ".acted"
    stamp.touch()
    later = current.stat().st_mtime_ns + 1_000_000
    os.utime(stamp, ns=(later, later))
    return later / 1e9


def test_a_current_that_rescued_is_promoted_after_a_later_cycle_ended_at_the_latest(placed):
    at = _acted(placed)
    assert lifeboat.promote(ok=True, active="0.330.0", latest="0.330.0", ended_at=at - 1) is False, (
        "a cycle that ended before the rescue proves nothing of it")
    assert lifeboat.promote(ok=True, active="0.330.0", latest="0.330.0", ended_at=at + 60) is True
    assert _slot("known-good").read_bytes() == placed.read_bytes()
    assert not (placed.parent / ".acted").exists(), "the proof is spent by the promotion"
    assert lifeboat.promote(ok=True, active="0.330.0", latest="0.330.0") is False


def test_a_current_whose_rescue_failed_is_never_promoted_by_known_goods_rescue(placed):
    """current/'s rescue fails; two hours on the wrapper runs known-good/,
    whose rescue works (its own `.acted`); the next cycle ends at the latest.
    That proves known-good, never current: promoting current would leave the
    broken copy in both slots (R12; reproduced against the real promote)."""
    at = _acted(placed)
    known = _slot("known-good")
    before = known.read_bytes()
    stamp = known.parent / ".acted"
    stamp.touch()
    os.utime(stamp, (at + 2 * 3600, at + 2 * 3600))
    assert lifeboat.promote(ok=True, active="0.330.0", latest="0.330.0", ended_at=at + 3 * 3600) is False
    assert known.read_bytes() == before


@pytest.mark.parametrize(
    "acted, ok, active, latest",
    [
        pytest.param(False, True, "0.330.0", "0.330.0", id="current-only-ran-never-rescued"),
        pytest.param(True, False, "0.330.0", "0.330.0", id="the-cycle-failed"),
        pytest.param(True, True, "0.329.0", "0.330.0", id="still-behind"),
        pytest.param(True, True, "0.330.0", None, id="latest-unknown"),
    ],
)
def test_no_promotion_without_proof(placed, acted, ok, active, latest):
    if acted:
        _acted(placed)
    assert lifeboat.promote(ok=ok, active=active, latest=latest) is False
    assert lifeboat.handoff_version(_slot("known-good")) == 1


def test_never_promoted_from_a_test_home(placed, monkeypatch):
    monkeypatch.setattr(keeper, "wanted", _WANTED)  # as it is: the suite's HOME is not the account's own
    _acted(placed)
    assert keeper.wanted() is False
    assert lifeboat.promote(ok=True, active="0.330.0", latest="0.330.0") is False


def test_after_a_cycle_the_active_version_is_the_self_steps(placed, monkeypatch):
    _acted(placed)
    monkeypatch.setattr(lifeboat, "manifest_latest", lambda: "0.330.0")
    done = {"ok": True, "deferred": None, "steps": {"self": {"state": "done", "to_version": "0.329.0"}}}
    assert lifeboat.after_cycle(done) is False
    done["steps"]["self"]["to_version"] = "0.330.0"
    assert lifeboat.after_cycle({**done, "deferred": "run_in_flight"}) is False
    assert lifeboat.after_cycle(done) is True


# -- what it did ------------------------------------------------------------------------


def test_acted_is_read_and_cleared(home):
    lifeboat.root().mkdir(parents=True)
    record = {"at": time.time(), "reason": "behind", "from": "0.325.0", "to": "0.330.0", "trigger": "keeper"}
    (lifeboat.root() / "acted.json").write_text(json.dumps(record))
    assert lifeboat.read_acted() == record
    lifeboat.clear_acted()
    assert lifeboat.read_acted() is None


@pytest.mark.parametrize("kind", ["not-json", "eight-days-old", "not-an-object"])
def test_an_unreadable_or_week_old_record_is_dropped(home, kind):
    body = {"not-json": "{not json", "not-an-object": "[]",
            "eight-days-old": json.dumps({"at": time.time() - 8 * 86400, "reason": "behind"})}[kind]
    lifeboat.root().mkdir(parents=True)
    (lifeboat.root() / "acted.json").write_text(body)
    assert lifeboat.read_acted() is None
    assert not (lifeboat.root() / "acted.json").exists()


# -- env.json -------------------------------------------------------------------------


def test_env_json_never_stores_a_credential(home):
    login = {"UV_INDEX_URL": "https://pypi.internal/simple", "HTTPS_PROXY": "http://ben:hunter2@proxy:8080",
             "NO_PROXY": "localhost", "AWS_SECRET_ACCESS_KEY": "x"}
    assert lifeboat.index_env(login) == {"UV_INDEX_URL": "https://pypi.internal/simple", "NO_PROXY": "localhost"}


@pytest.mark.parametrize("name", ["UV_EXTRA_INDEX_URL", "UV_INDEX", "PIP_EXTRA_INDEX_URL"])
@pytest.mark.parametrize("separator", [" ", ",", "\n", " , "])
def test_a_list_of_indexes_with_one_credential_is_never_stored(home, name, separator):
    public = "https://pypi.org/simple"
    secret = separator.join([public, "https://user:tok@priv.example.com/simple"])
    assert lifeboat.index_env({name: secret}) == {}
    assert lifeboat.index_env({name: separator.join([public, "https://priv.example.com/simple"])}) != {}


def test_saving_the_auto_update_setting_rewrites_env_json_at_once(home):
    """Turned off, the lifeboat stops at its next run: it never rescued a
    machine 12 h after a person turned updates off (the setting was read at
    the last service start only)."""
    from probe._shared import autoupdate

    autoupdate.save(enabled=True)
    assert not lifeboat.root().exists(), "no lifeboat here: nothing is made"
    paths.private_dir(lifeboat.root())
    (lifeboat.root() / "env.json").write_text(json.dumps({"v": 1, "auto_update": True, "managed": True}, indent=1))
    autoupdate.save(enabled=False)
    written = json.loads((lifeboat.root() / "env.json").read_text())
    assert written == {"v": 1, "auto_update": False, "managed": True}
    autoupdate.save(enabled=True)
    assert json.loads((lifeboat.root() / "env.json").read_text())["auto_update"] is True


def test_the_service_start_records_the_login_shells_index_settings(home, monkeypatch):
    """`write_env(login)` at every start: index settings follow the login shell,
    and a shell that gave no answer keeps the last ones (never wipes them)."""
    monkeypatch.setenv("PATH", "/usr/bin:/bin")
    lifeboat.write_env(login={"UV_INDEX_URL": "https://old.example.com/simple"})
    monkeypatch.setattr(lifeboat, "login_env", lambda: None)
    assert lifeboat.write_env()["index_env"] == {"UV_INDEX_URL": "https://old.example.com/simple"}
    assert lifeboat.write_env(login={"UV_INDEX_URL": "https://new.example.com/simple"})["index_env"] == {
        "UV_INDEX_URL": "https://new.example.com/simple"}


def test_env_json_records_the_receipt_and_the_base_python(home, tmp_path):
    env = tmp_path / "tool-env"
    env.mkdir()
    pybin = Path(sys.executable).resolve().parent
    version = f"{sys.version_info.major}.{sys.version_info.minor}"
    (env / "pyvenv.cfg").write_text(f"home = {pybin}\nversion_info = {version}.0\n")
    (env / "uv-receipt.toml").write_text(
        '[tool]\nrequirements = [\n'
        '  { name = "probe-research", extras = ["all", "daemon"] },\n'
        '  { name = "wandb", specifier = ">=0.18" },\n'
        ']\npython = "3.12"\n'
    )
    assert lifeboat.receipt(env) == {"extras": ["all", "daemon"], "with": ["wandb>=0.18"], "python": "3.12"}
    assert lifeboat.base_python(env) in (str(pybin / f"python{version}"), str(pybin / "python3"))


# -- with the real hand-off (lane A's frozen file) ---------------------------------------


def test_the_wrapper_runs_the_real_handoff(boat):
    """`handoff.py --selftest` under `-I -S`, then `--lifeboat --trigger t`:
    a machine that is not a managed CLI is a quick no-op, exit 0, no rescue."""
    (boat.root / "current").mkdir()
    shutil.copyfile(SHARED / "handoff.py", boat.root / "current" / "handoff.py")
    (boat.root / "known-good").mkdir()
    _stub(boat.root / "known-good" / "handoff.py")
    boat.env_json(base_python=sys.executable, managed=False, auto_update=True)
    done = boat.run("session")
    assert done.returncode == 0, done.stderr
    assert boat.calls() == [], "current ran and exited 0: known-good never did"
    assert lifeboat.rescued_at(boat.root / "current" / "handoff.py") is None


def test_the_real_handoff_under_the_wrapper_does_nothing_during_an_uninstall(boat, tmp_path):
    """An uninstall past its point of no return (`S/uninstall/barrier.json`,
    phase `server`): the keeper's run of the real hand-off reads nothing,
    writes none of its clocks and exits 0, so known-good never runs either."""
    from probe._shared import handoff

    (boat.root / "current").mkdir()
    shutil.copyfile(SHARED / "handoff.py", boat.root / "current" / "handoff.py")
    (boat.root / "known-good").mkdir()
    _stub(boat.root / "known-good" / "handoff.py")
    closed = "http://127.0.0.1:9"  # were it to look: refused at once, never the real API
    boat.env_json(base_python=sys.executable, managed=True, auto_update=True, base_url=closed,
                  tools=str(tmp_path / "tools"), socket=str(tmp_path / "none.sock"))
    barrier = handoff.barrier_path()
    assert barrier == paths.state_dir() / "uninstall" / "barrier.json"
    barrier.parent.mkdir(parents=True)
    barrier.write_text(json.dumps({"v": 1, "pid": 999999999, "start": "0", "at": 1.0, "phase": "server"}))
    done = boat.run("keeper", PROBE_HANDOFF_PYPI_URL=closed + "/pypi")
    assert done.returncode == 0, done.stderr
    assert boat.calls() == [] and not (boat.root / "state.json").exists()


def test_this_releases_real_handoff_is_what_a_first_install_places(home, tmp_path, monkeypatch):
    from probe._shared import handoff

    monkeypatch.setattr(lifeboat, "env_record", lambda login=None: {"v": 1, "base_python": sys.executable})
    monkeypatch.setattr(lifeboat, "SYSTEM_PYTHON", str(tmp_path / "no-system-python"))
    monkeypatch.setenv("PATH", "/usr/bin:/bin")
    assert lifeboat.install() == "installed (lifeboat.sh, current, known-good)"
    assert _slot("current").read_bytes() == (SHARED / "handoff.py").read_bytes() == _slot("known-good").read_bytes()
    assert lifeboat.handoff_version(_slot("current")) == handoff.HANDOFF_VERSION


#: Byte copies of the hand-off as released: HANDOFF_VERSION 1 (CLI 0.328.0)
#: and 2 (CLI 0.329.1), what a machine's slots hold today.
DEPLOYED = Path(__file__).resolve().parent / "fixtures" / "handoff_deployed"
DEPLOYED_DIGESTS = {
    1: "46dea4b6613ba332d09bd0508d2c23d964cb00c5431c2213f7b59a01a0da81af",
    2: "4ca1fabf2b99ea060ae414387ad621e1b336aafec0dd00bb8ac753e739523438",
}


def _deployed(version: int) -> bytes:
    data = (DEPLOYED / f"v{version}" / "handoff.py").read_bytes()
    assert hashlib.sha256(data).hexdigest() == DEPLOYED_DIGESTS[version], "not the released copy"
    return data


@pytest.mark.parametrize("current, known_good", [(2, 1), (2, 2), (1, 1)])
def test_the_real_v3_replaces_a_deployed_current_and_keeps_known_good(home, tmp_path, monkeypatch, current,
                                                                        known_good):
    """HANDOFF_VERSION 3 (a broken env is rebuilt at any version; nothing
    runs during an uninstall) reaching a machine whose slots hold the
    released v1/v2 copies: the packaged v3 becomes `current/`, and
    `known-good/` stays as it is until v3 proves itself (`promote`: a rescue
    of its own, then a cycle at the latest) -- with the real files."""
    from probe._shared import handoff

    assert handoff.HANDOFF_VERSION == 3
    v3 = (SHARED / "handoff.py").read_bytes()
    for slot, version in (("current", current), ("known-good", known_good)):
        _slot(slot).parent.mkdir(parents=True, exist_ok=True)
        _slot(slot).write_bytes(_deployed(version))
    monkeypatch.setattr(lifeboat, "env_record", lambda login=None: {"v": 1, "base_python": sys.executable})
    monkeypatch.setattr(lifeboat, "SYSTEM_PYTHON", str(tmp_path / "no-system-python"))
    monkeypatch.setenv("PATH", "/usr/bin:/bin")
    assert lifeboat.install() == "installed (lifeboat.sh, current)"
    assert _slot("current").read_bytes() == v3 and lifeboat.handoff_version(_slot("current")) == 3
    assert _slot("known-good").read_bytes() == _deployed(known_good)
    assert lifeboat.install() == "current", "a second install changes nothing"
    monkeypatch.setattr(keeper, "wanted", lambda: True)
    assert not lifeboat.promote(ok=True, active="0.330.0", latest="0.330.0"), "v3 has rescued nothing yet"
    assert _slot("known-good").read_bytes() == _deployed(known_good)


def test_a_deployed_v2_release_never_replaces_a_v3_current(home, tmp_path, monkeypatch):
    """A machine switched back to a v2 release (its service starts and
    installs the lifeboat): the v3 `current/` stays (2 is not higher)."""
    shared = tmp_path / "v2-release" / "_shared"
    shared.mkdir(parents=True)
    shutil.copyfile(SHARED / "lifeboat.sh", shared / "lifeboat.sh")
    (shared / "handoff.py").write_bytes(_deployed(2))
    v3 = (SHARED / "handoff.py").read_bytes()
    for slot in ("current", "known-good"):
        _slot(slot).parent.mkdir(parents=True, exist_ok=True)
        _slot(slot).write_bytes(v3)
    monkeypatch.setattr(lifeboat, "_SHARED", shared)
    monkeypatch.setattr(lifeboat, "env_record", lambda login=None: {"v": 1, "base_python": sys.executable})
    monkeypatch.setattr(lifeboat, "SYSTEM_PYTHON", str(tmp_path / "no-system-python"))
    monkeypatch.setenv("PATH", "/usr/bin:/bin")
    lifeboat.install()
    assert _slot("current").read_bytes() == v3 == _slot("known-good").read_bytes()


def test_env_json_carries_every_key_the_handoff_reads(home, monkeypatch):
    """The two lanes' contract: release code writes env.json, `handoff.py`
    reads it. A key it reads that no writer writes is a lifeboat that never acts."""
    import re

    monkeypatch.setenv("PATH", "/usr/bin:/bin")
    source = (SHARED / "handoff.py").read_text()
    read = set(re.findall(r'(?:cfg|source)(?:\.get\(|\[)"([a-z_]+)"', source))
    assert {"auto_update", "managed", "socket", "tools", "active_python", "extras", "with"} <= read
    written = lifeboat.write_env(login={"UV_INDEX_URL": "https://pypi.internal/simple"})
    assert read <= set(written), sorted(read - set(written))
    on_disk = json.loads((lifeboat.root() / "env.json").read_text())
    assert on_disk == json.loads(json.dumps(written)) and on_disk["v"] == 1
    assert on_disk["socket"] == str(paths.socket_path()) and on_disk["index_env"] == {
        "UV_INDEX_URL": "https://pypi.internal/simple"}
    assert isinstance(on_disk["auto_update"], bool) and isinstance(on_disk["managed"], bool)


# -- frozen ---------------------------------------------------------------------------


def _digest(*parts: str | bytes) -> str:
    digest = hashlib.sha256()
    for part in parts:
        digest.update((part.encode() if isinstance(part, str) else part) + b"\0")
    return digest.hexdigest()[:16]


def test_the_wrapper_is_frozen():
    """Every keeper unit and session start runs it, whatever release is
    installed: a change reaches every machine and no newer release can take
    it back. Change it deliberately, then pin the new digest."""
    assert _digest((SHARED / "lifeboat.sh").read_bytes()) == FROZEN_WRAPPER


def test_the_keepers_unit_writers_are_frozen():
    """The units name the wrapper by its fixed path and nothing of a release's
    (R12): a release cannot point the keeper anywhere else. Change deliberately."""
    path = "/home/someone/.local/state/probe/lifeboat/lifeboat.sh"
    units = keeper._systemd_units(path)
    assert _digest(*(f"{name}\n{text}" for name, text in sorted(units.items())), keeper._plist(path)) == FROZEN_UNITS
    assert lifeboat.wrapper_path() == paths.state_dir() / "lifeboat" / "lifeboat.sh"
