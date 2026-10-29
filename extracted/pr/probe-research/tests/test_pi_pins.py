"""kimi/pi update parity P1/P7: the pi package's pins and the proof that open
pi sessions switch to the new version with no /reload (`probe.cli.pi_pins`)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from probe.cli import pi_config, pi_pins

#: (SHIM_API, digest of the shim's files): see `test_the_frozen_shim_files_change_only_with_their_api`.
#: (1, a094d27e96a07523) until notes parity forwarded `agent_before_settle`: an open pi on the
#: older shim just never delivers it (the send-back waits for /reload); no implementation needs it.
FROZEN_SHIM = (1, "cc338ef5f1d5b712")


def _clone(root: Path, version: str = "0.7.0") -> Path:
    """pi's clone of the mirror: the package with the shim's impl, its sibling
    plugins, node_modules (with a .bin link) and the root package.json."""
    package = root / "plugins" / "probe-research-pi"
    (package / "src").mkdir(parents=True)
    (package / "src" / "impl.ts").write_text("export const REQUIRES_SHIM_API = 1;\n")
    (package / "src" / "extension.ts").write_text(
        "export const STATE_SCHEMA = 1;\nexport const MIGRATES_FROM: readonly number[] = [];\n")
    (package / "package.json").write_text(json.dumps({"name": "probe-research-pi", "version": version}))
    for sibling in ("probe-research-tap", "probe-research", "probe-research-daemon"):
        (root / "plugins" / sibling).mkdir(parents=True)
        (root / "plugins" / sibling / "README.md").write_text(sibling)
    sdk = root / "node_modules" / "@modelcontextprotocol" / "sdk"
    sdk.mkdir(parents=True)
    (sdk / "index.js").write_text("module.exports = {}")
    (root / "node_modules" / ".bin").mkdir()
    os.symlink("../@modelcontextprotocol/sdk/index.js", root / "node_modules" / ".bin" / "mcp")
    (root / "package.json").write_text(json.dumps({"pi": {"skills": ["plugins/probe-research-pi/skills/probe"]}}))
    skill = package / "skills" / "probe"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: probe\ndescription: the switch\n---\nBody v1\n")
    (root / ".git").mkdir()
    (root / ".git" / "HEAD").write_text("ref: refs/heads/main\n")
    (root / ".git" / "refs" / "heads").mkdir(parents=True)
    (root / ".git" / "refs" / "heads" / "main").write_text("a" * 40 + "\n")
    return package


@pytest.fixture
def pi(tmp_path, monkeypatch):
    clone = tmp_path / "agent" / "git" / "github.com" / "prbe-ai" / "research-os-agent"
    package = _clone(clone)
    monkeypatch.setattr(pi_config, "installed_package_dir", lambda env=None: package)
    # Only the pi processes a test starts: other sessions on a shared box run pi too.
    real = pi_pins._pi_pids

    def mine(titles):
        found = real(titles)
        if found is None:
            return None
        return {pid for pid in found if _parent(pid) == os.getpid()}

    monkeypatch.setattr(pi_pins, "_pi_pids", mine)
    return clone


def _parent(pid: int) -> int | None:
    try:
        return int(Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[1])
    except (OSError, IndexError, ValueError):
        return None


def test_the_installed_package_is_pinned_whole_and_made_current(pi):
    pin = pi_pins.pin_installed()
    assert pin is not None and pin.parent == pi_pins.pi_dir() / pi_pins.PINS_DIRNAME
    for rel in pi_pins.SOURCES:
        assert (pin / rel).exists(), rel
    assert (pin / "node_modules" / ".bin" / "mcp").is_symlink(), "links stay links (they point inside the pin)"
    assert pi_pins.read_current() == {"pin": pin.name, "version": "0.7.0", "from": str(pi), "head": "a" * 40}
    assert pi_pins.pin_due() is False
    assert pi_pins.pin_installed() == pin, "the same files: the same pin"


def test_an_update_pi_has_not_finished_is_never_pinned(pi):
    (pi.parent / f".{pi.name}.pi-update-incomplete").write_text("")
    assert pi_pins.pin_installed() is None and pi_pins.read_current() is None


def test_a_package_before_the_shim_or_a_local_checkout_is_not_pinned(tmp_path, monkeypatch):
    old = tmp_path / "old" / "plugins" / "probe-research-pi"
    old.mkdir(parents=True)
    monkeypatch.setattr(pi_config, "installed_package_dir", lambda env=None: old)
    assert pi_pins.pin_installed() is None and pi_pins.pin_due() is False
    local = tmp_path / "checkout" / "probe-research-pi"
    (local / "src").mkdir(parents=True)
    (local / "src" / "impl.ts").write_text("")
    monkeypatch.setattr(pi_config, "installed_package_dir", lambda env=None: local)
    assert pi_pins.pin_installed() is None


def test_pruning_never_removes_a_pin_a_live_pi_runs(pi):
    first = pi_pins.pin_installed()
    live = pi_pins.pi_dir() / pi_pins.LIVE_DIRNAME
    live.mkdir(parents=True)
    (live / f"{os.getpid()}.json").write_text(json.dumps({"pin": first.name, "fallback_pin": None}))
    made = [first]
    for minor in range(1, 6):
        (pi / "plugins" / "probe-research-pi" / "package.json").write_text(
            json.dumps({"name": "probe-research-pi", "version": f"0.7.{minor}"}))
        made.append(pi_pins.pin_installed())
        time.sleep(0.01)
    left = {p.name for p in (pi_pins.pi_dir() / pi_pins.PINS_DIRNAME).iterdir() if p.is_dir()}
    assert first.name in left, "this process still runs it"
    assert made[-1].name in left and pi_pins.read_current()["version"] == "0.7.5"
    assert len(left) <= 1 + 1 + 3, left


def test_every_pin_a_live_pi_has_run_is_kept(pi):
    """Review: after two switches with no session start, the version in the
    middle may still own the watcher or the MCP client."""
    middle = pi_pins.pin_installed()
    live = pi_pins.pi_dir() / pi_pins.LIVE_DIRNAME
    live.mkdir(parents=True)
    (live / f"{os.getpid()}.json").write_text(json.dumps({"pin": "x", "pins_used": [middle.name, "x"]}))
    assert middle.name in pi_pins.referenced()


def test_a_moved_clone_rewrites_current(pi, monkeypatch, tmp_path):
    pin = pi_pins.pin_installed()
    moved = tmp_path / "moved" / "research-os-agent"
    moved.parent.mkdir()
    pi.rename(moved)
    monkeypatch.setattr(pi_config, "installed_package_dir", lambda env=None: moved / "plugins" / "probe-research-pi")
    assert pi_pins.pin_due() is True
    pi_pins.pin_installed()
    assert pi_pins.read_current()["from"] == str(moved) and pi_pins.pin_due() is False
    assert pin.exists()


@pytest.mark.skipif(not os.path.isdir("/proc/self"), reason="the live check reads /proc here")
def test_a_pi_titled_otherwise_is_still_read(pi):
    """Review: `pi-rpc`, a pi embedded in another program: its shim's record
    counts whatever its process is called."""
    pi_pins.pin_installed()
    live = pi_pins.pi_dir() / pi_pins.LIVE_DIRNAME
    live.mkdir(parents=True, exist_ok=True)
    (live / f"{os.getpid()}.json").write_text(json.dumps(_record(recorded=False)))
    assert pi_pins.sessions_follow(("pi",)) is False
    (live / f"{os.getpid()}.json").write_text(json.dumps(_record()))
    assert pi_pins.sessions_follow(("pi",)) is True


@pytest.mark.skipif(not os.path.isdir("/proc/self"), reason="argv shows in /proc")
def test_a_pi_without_a_shim_record_is_found_by_its_rpc_title_or_its_package_path(pi):
    """Re-review: a pre-shim pi (0.6.3) writes no record, so it must be found
    as a process: `pi-rpc` (its RPC mode's title) or `node .../pi-coding-agent/
    .../cli.js` (how macOS `ps` shows it) counts as pi."""
    pi_pins.pin_installed()
    rpc = subprocess.Popen(["/bin/bash", "-c", "exec -a pi-rpc sleep 60"])
    node = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)",
                             "/x/node_modules/@earendil-works/pi-coding-agent/dist/bundle/cli.js"])
    try:
        for proc in (rpc, node):
            for _ in range(50):
                if proc.pid in (pi_pins._pi_pids(("pi",)) or set()):
                    break
                time.sleep(0.05)
        found = pi_pins._pi_pids(("pi",))
        assert rpc.pid in found and node.pid in found
        assert pi_pins.sessions_follow(("pi",)) is False, "a pi with no record: its package predates the shim"
    finally:
        for proc in (rpc, node):
            proc.kill()
            proc.wait()


def test_what_counts_as_a_pi_command_line():
    """Codex review: `node /usr/local/bin/pi` (an npm bin on macOS) is a pi too."""
    names = {"pi", "pi-rpc"}
    assert pi_pins._is_pi(["pi"], names) and pi_pins._is_pi(["/home/u/.pi/agent/bin/pi", "-c"], names)
    assert pi_pins._is_pi(["pi-rpc"], names)
    assert pi_pins._is_pi(["node", "/usr/local/bin/pi"], names)
    assert pi_pins._is_pi(["/usr/bin/node", "/x/node_modules/@earendil-works/pi-coding-agent/dist/bundle/cli.js"], names)
    assert not pi_pins._is_pi(["node", "/x/other/cli.js"], names) and not pi_pins._is_pi([], names)
    assert not pi_pins._is_pi(["/usr/bin/pip", "install"], names)


def test_a_pi_in_a_folder_with_a_space_counts_on_macos():
    """macOS `ps` gives no argv boundaries: `node /Users/A B/bin/pi` splits."""
    names = {"pi", "pi-rpc"}
    assert pi_pins._ends_in_pi("node /Users/Jo Doe/.npm/bin/pi", names)
    assert pi_pins._ends_in_pi("node /Users/Jo Doe/.npm/bin/pi-rpc --mode rpc", names)
    assert not pi_pins._ends_in_pi("node /Users/Jo Doe/bin/pipeline", names)
    assert not pi_pins._is_pi("node /Users/Jo Doe/.npm/bin/pi".split(), names), "why the line itself is read"


def test_a_clone_that_moved_while_it_was_copied_is_not_pinned(pi, monkeypatch):
    """Re-review: `head` is read before the copy; a `pi update` meanwhile makes
    the copy a mix of two commits, which is never made `current`."""
    real = pi_pins.pins.make

    def moving(*args, **kwargs):
        made = real(*args, **kwargs)
        (pi / ".git" / "refs" / "heads" / "main").write_text("c" * 40 + "\n")
        return made

    monkeypatch.setattr(pi_pins.pins, "make", moving)
    assert pi_pins.pin_installed() is None and pi_pins.read_current() is None


def test_the_frozen_shim_files_change_only_with_their_api(pi):
    """The shim (`index.ts`, `src/shim.ts` and what it imports) stays loaded
    in every open pi until /reload: a change to it reaches no open session.
    A change here is deliberate: bump SHIM_API when a version needs it
    (`REQUIRES_SHIM_API` in `src/impl.ts`), then pin the new digest."""
    import hashlib

    package = Path(__file__).resolve().parents[1] / "plugins" / "probe-research-pi"
    digest = hashlib.sha256()
    for rel in ("index.ts", "src/shim.ts", "src/core/paths.ts"):
        digest.update(rel.encode() + b"\0" + (package / rel).read_bytes())
    api = int(__import__("re").search(r"export const SHIM_API = (\d+);", (package / "src" / "shim.ts").read_text())[1])
    assert (api, digest.hexdigest()[:16]) == FROZEN_SHIM


def test_a_dead_pis_record_is_removed(pi):
    live = pi_pins.pi_dir() / pi_pins.LIVE_DIRNAME
    live.mkdir(parents=True)
    dead = live / f"{2 ** 22 - 1}.json"
    dead.write_text("{}")
    assert pi_pins.live_records() == {} and not dead.exists()


def _record(**overrides) -> dict:
    current = pi_pins.read_current() or {}
    return {"shim_api": 1, "state_schema": 1, "pin": "0.7.0-x", "fallback_pin": None, "bad_pins": [],
            "resources_pin": current.get("pin"), "pins_used": [], "install": current.get("from"), "recorded": True,
            "skills_reload_needed": False, "shim_reload_needed": False, **overrides}


def test_why_an_open_pi_session_needs_a_reload(pi):
    pin = pi_pins.pin_installed()
    current = pi_pins.read_current()
    assert pi_pins.why_not(_record(), current) is None
    assert "predates the shim" in pi_pins.why_not(None, current)
    assert "no pinned version" in pi_pins.why_not(_record(), None)
    assert "failed to load" in pi_pins.why_not(_record(bad_pins=[pin.name]), current)
    assert "newer shim" in pi_pins.why_not(_record(shim_reload_needed=True), current)
    (pin / pi_pins.PACKAGE / "src" / "impl.ts").write_text("export const REQUIRES_SHIM_API = 2;\n")
    assert "newer shim" in pi_pins.why_not(_record(), current)
    (pin / pi_pins.PACKAGE / "src" / "impl.ts").write_text("export const REQUIRES_SHIM_API = 1;\n")
    assert "skills" in pi_pins.why_not(_record(skills_reload_needed=True), current)
    assert "own tap watch" in pi_pins.why_not(_record(recorded=False), current)
    assert "skills change" in pi_pins.why_not(_record(resources_pin=None), current), "skills from the clone: unknown"
    assert "another install" in pi_pins.why_not(_record(install="/elsewhere"), current)
    assert "state" in pi_pins.why_not(_record(state_schema=2), current)
    (pin / pi_pins.PACKAGE / "src" / "extension.ts").write_text(
        "export const STATE_SCHEMA = 2;\nexport const MIGRATES_FROM: readonly number[] = [1];\n")
    assert pi_pins.why_not(_record(), current) is None, "a version that migrates the state takes over"
    (pin / pi_pins.PACKAGE / "src" / "impl.ts").write_text("export { REQUIRES_SHIM_API } from './elsewhere';\n")
    assert "newer shim" in pi_pins.why_not(_record(), current), "unreadable: unknown, never 1"


def test_a_new_version_whose_skills_pi_loaded_already_needs_no_reload(pi):
    """Codex review: the update claims no /reload before the shim switches, so
    it compares the skills pi loaded (`resources_pin`) with the new version's."""
    package = pi / "plugins" / "probe-research-pi"
    first = pi_pins.pin_installed()
    (package / "package.json").write_text(json.dumps({"name": "probe-research-pi", "version": "0.7.1"}))
    (package / "skills" / "probe" / "SKILL.md").write_text("---\nname: probe\ndescription: the switch\n---\nBody v2\n")
    second = pi_pins.pin_installed()
    current = pi_pins.read_current()
    assert current["pin"] == second.name != first.name
    assert pi_pins.why_not(_record(resources_pin=first.name), current) is None, "a skill body is read when used"
    (package / "package.json").write_text(json.dumps({"name": "probe-research-pi", "version": "0.7.2"}))
    (package / "skills" / "probe" / "SKILL.md").write_text("---\nname: probe\ndescription: renamed\n---\nBody v2\n")
    pi_pins.pin_installed()
    current = pi_pins.read_current()
    assert "skills change" in pi_pins.why_not(_record(resources_pin=first.name), current)
    assert "skills change" in pi_pins.why_not(_record(resources_pin="0.0.1-gone"), current)


def test_a_clone_moved_without_a_new_version_is_pinned_again(pi):
    """Codex review: a `pi update` that changes files but not the package
    version moves the clone's commit, which `pin_due` reads."""
    pi_pins.pin_installed()
    assert pi_pins.pin_due() is False
    (pi / ".git" / "refs" / "heads" / "main").write_text("b" * 40 + "\n")
    assert pi_pins.pin_due() is True
    (pi / "plugins" / "probe-research-tap" / "README.md").write_text("changed")
    pi_pins.pin_installed()
    assert pi_pins.read_current()["head"] == "b" * 40 and pi_pins.pin_due() is False


@pytest.mark.skipif(not os.path.isdir("/proc/self"), reason="retitled argv shows in /proc")
def test_sessions_follow_reads_every_live_pi_process(pi):
    pi_pins.pin_installed()
    assert pi_pins.sessions_follow(("pi",)) is True, "no pi running: nothing to reload"
    proc = subprocess.Popen(["/bin/bash", "-c", "exec -a pi sleep 60"])
    try:
        for _ in range(50):
            if Path(f"/proc/{proc.pid}/cmdline").read_bytes().startswith(b"pi"):
                break
            time.sleep(0.05)
        assert pi_pins.sessions_follow(("pi",)) is False, "a pi with no shim record (0.6.3 and before)"
        live = pi_pins.pi_dir() / pi_pins.LIVE_DIRNAME
        live.mkdir(parents=True, exist_ok=True)
        (live / f"{proc.pid}.json").write_text(json.dumps(_record()))
        assert pi_pins.sessions_follow(("pi",)) is True
        (live / f"{proc.pid}.json").write_text(json.dumps(_record(recorded=False)))
        assert pi_pins.sessions_follow(("pi",)) is False
    finally:
        proc.kill()
        proc.wait()


def test_the_update_says_no_restart_only_when_open_sessions_switch(pi, monkeypatch):
    from probe.cli import upgrading
    from probe.cli.claude_cli import Result

    versions = iter([(0, 6, 3), (0, 7, 0)])
    monkeypatch.setattr(pi_config, "installed_package_version", lambda env=None: next(versions))
    monkeypatch.setattr(pi_config, "update_package", lambda env=None: Result(ok=True, detail="updated"))
    monkeypatch.setattr(pi_pins, "sessions_follow", lambda titles: True)
    step = upgrading._update_pi_package()
    assert step.lines[-1].endswith("(open pi sessions switch to it at their next turn, no restart needed)")
    assert pi_pins.read_current() is not None, "the update pinned what it installed"


def test_the_shim_and_this_module_agree_on_the_files(pi):
    """The on-disk contract: names the shim reads (src/shim.ts) and this writes."""
    shim = (Path(__file__).resolve().parents[1] / "plugins" / "probe-research-pi" / "src" / "shim.ts").read_text()
    for name in (pi_pins.PI_DIRNAME, pi_pins.PINS_DIRNAME, pi_pins.CURRENT_NAME, pi_pins.LIVE_DIRNAME):
        assert f'"{name}"' in shim, name
    assert "REQUIRES_SHIM_API" in shim or "REQUIRES_SHIM_API" in (
        Path(__file__).resolve().parents[1] / "plugins" / "probe-research-pi" / "src" / "impl.ts").read_text()
    assert sys.version_info >= (3, 9)
