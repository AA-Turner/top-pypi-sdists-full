"""Kimi parity K3/K4: what each open Kimi Code session LOADED, and the proof
behind "no restart needed" for Kimi (`probe._shared.kimi_live`)."""

from __future__ import annotations

import filecmp
import json
import os
import time
from pathlib import Path

import pytest

from probe._shared import kimi_live
from probe.sdk import session_marker

AGENT = Path(__file__).resolve().parents[1]
CANONICAL = AGENT / "src" / "probe" / "_shared" / "kimi_live.py"
HOOKS = AGENT / "plugins" / "probe-research" / "hooks"
KIMI = "kimi_code"  # harness-literal-ok: the registry id the hooks record


@pytest.fixture(autouse=True)
def _only_our_processes(monkeypatch):
    """The live checks list every process here: on a shared box another
    session's real Kimi (or its `tap watch`) would answer for a test. Each
    test sees only itself and the processes it starts."""
    me = os.getpid()
    listed = kimi_live._processes

    def ours(marker):
        table = listed(marker)
        if table is None:
            return None
        return {pid: info for pid, info in table.items() if pid == me or info[0] == me}

    argv_of = kimi_live._argv_of

    def our_argv(pid):
        try:
            parent = int(Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[1])
        except (OSError, IndexError, ValueError):
            return []
        return argv_of(pid) if parent == me else []

    monkeypatch.setattr(kimi_live, "_processes", ours)
    monkeypatch.setattr(kimi_live, "_argv_of", our_argv)


def test_the_hooks_carry_the_canonical_copy():
    for plugin in ("probe-research", "probe-research-daemon"):
        copy = AGENT / "plugins" / plugin / "hooks" / "_kimi_live.py"
        assert filecmp.cmp(CANONICAL, copy, shallow=False), f"{copy} drifted: run `make sync-session-marker`"


def _plugin(managed: Path, name: str, version: str, *, hooks=None, mcp=None) -> Path:
    root = managed / f"{name}@{version}"
    (root / ".kimi-plugin").mkdir(parents=True)
    manifest = {"name": name, "version": version, "skills": "./agent-skills/",
                "hooks": hooks if hooks is not None else [{"event": "UserPromptSubmit", "command": "x", "timeout": 10}],
                "mcpServers": mcp if mcp is not None else {"probe-research": {"url": "https://mcp", "auth": "oauth"}}}
    (root / ".kimi-plugin" / "plugin.json").write_text(json.dumps(manifest))
    return root


def _kimi(tmp_path: Path, plugin="0.177.0", tap="0.10.20") -> tuple[Path, Path, Path]:
    plugins = tmp_path / ".kimi-code" / "plugins"
    managed = plugins / "managed"
    probe = _plugin(managed, "probe-research", plugin)
    tap_root = _plugin(managed, "probe-research-tap", tap, mcp={})
    (plugins / "installed.json").write_text(json.dumps({"plugins": [
        {"id": "probe-research", "root": str(probe)}, {"id": "probe-research-tap", "root": str(tap_root)}]}))
    return plugins, probe, tap_root


def test_loaded_info_is_what_the_session_started_on(tmp_path):
    _plugins, probe, tap = _kimi(tmp_path)
    info = kimi_live.loaded_info(str(probe), "SessionStart")
    assert info["plugin"] == "probe-research" and info["plugin_version"] == "0.177.0"
    assert info["tap_root"] == str(tap) and info["tap_version"] == "0.10.20"
    assert info["plugin_fp"] == kimi_live.manifest_fingerprint(str(probe)) and info["late"] is False
    assert kimi_live.loaded_info(str(probe), "UserPromptSubmit")["late"] is True, "a start not seen is unproven"
    assert kimi_live.loaded_info(str(tmp_path / "nowhere"), "SessionStart") is None


def test_the_fingerprint_is_what_kimi_keeps_from_its_start(tmp_path):
    managed = tmp_path / "managed"
    base = _plugin(managed, "a", "1.0.0")
    token = _plugin(managed, "b", "1.0.0", mcp={"probe-research": {"url": "https://mcp", "auth": "oauth",
                                                                   "headers": {"Authorization": "Bearer s3cret"}}})
    bumped = _plugin(managed, "c", "2.0.0")
    hooked = _plugin(managed, "d", "1.0.0", hooks=[{"event": "Stop", "command": "y"}])
    skilled = _plugin(managed, "e", "1.0.0")
    (skilled / "agent-skills" / "probe").mkdir(parents=True)
    (skilled / "agent-skills" / "probe" / "SKILL.md").write_text("new text")
    fp = kimi_live.manifest_fingerprint
    assert fp(str(base)) == fp(str(bumped)), "a version bump alone needs no reload"
    assert fp(str(base)) != fp(str(hooked)), "new hook entries need a reload"
    assert fp(str(base)) != fp(str(token)), "a header change (token, workspace limit) needs a reload"
    assert fp(str(base)) != fp(str(skilled)), "Kimi reads skills from the folder it loaded"
    assert "s3cret" not in json.dumps(kimi_live.loaded_info(str(token), "SessionStart")), "never a header value"
    assert fp(str(base), contents=False) == fp(str(token), contents=False) == fp(str(skilled), contents=False)


def _service_holds(monkeypatch, tmp_path: Path, *session_ids: str) -> None:
    """The Probe service's saved list of what it records names `session_ids`."""
    from probe.service import paths

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    folder = paths.service_dir()
    folder.mkdir(parents=True, exist_ok=True)
    (folder / kimi_live.RECORDERS_NAME).write_text(json.dumps({"v": 1, "sessions": [{"sid": s} for s in session_ids]}))


def test_the_service_list_is_the_one_the_service_writes():
    from probe.service import recorders

    assert kimi_live.RECORDERS_NAME == recorders.RECORDERS_NAME


def _record(info: dict | None, session_id: str = "s") -> dict:
    return {"harness": KIMI, "session_id": session_id, **({"loaded": info} if info is not None else {})}


def test_why_a_live_kimi_session_needs_a_reload(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_TAP_WATCHER_DIR", str(tmp_path / "watchers"))
    (tmp_path / "watchers").mkdir()
    plugins, probe, tap = _kimi(tmp_path)
    good = kimi_live.loaded_info(str(probe), "SessionStart")
    _service_holds(monkeypatch, tmp_path, "other")
    assert "own tap watch" in kimi_live.why_not(_record(good)), "only the service's own list proves it records"
    _service_holds(monkeypatch, tmp_path, "s")
    assert kimi_live.why_not(_record(good)) is None
    assert "before Probe recorded" in kimi_live.why_not(_record(None))
    assert "not seen" in kimi_live.why_not(_record({**good, "late": True}))
    assert "0.174.0" in kimi_live.why_not(_record({**good, "plugin_version": "0.174.0"}))
    assert "0.10.17" in kimi_live.why_not(_record({**good, "tap_version": "0.10.17"}))
    # A newer plugin with other hook entries installed since it loaded.
    newer = _plugin(plugins / "managed", "probe-research", "0.178.0", hooks=[{"event": "Stop", "command": "z"}])
    (plugins / "installed.json").write_text(json.dumps({"plugins": [
        {"id": "probe-research", "root": str(newer)}, {"id": "probe-research-tap", "root": str(tap)}]}))
    assert "manifest changed" in kimi_live.why_not(_record(good))


def test_a_session_on_its_own_tap_watch_keeps_the_restart_line(tmp_path, monkeypatch):
    """O5: a sandboxed session the service refuses keeps its watcher's tap code."""
    import subprocess
    import sys

    watchers = tmp_path / "watchers"
    watchers.mkdir()
    monkeypatch.setenv("PROBE_TAP_WATCHER_DIR", str(watchers))
    _plugins, probe, _tap = _kimi(tmp_path)
    good = kimi_live.loaded_info(str(probe), "SessionStart")
    _service_holds(monkeypatch, tmp_path, "s")
    sleeper = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    try:
        (watchers / "probe-research-tap-watcher-s.pid").write_text(str(sleeper.pid))
        assert "own tap watch" in kimi_live.why_not(_record(good))
        (watchers / "probe-research-tap-watcher-s.hosted").write_text(str(sleeper.pid))
        assert "own tap watch" in kimi_live.why_not(_record(good)), "a .hosted naming no service proves nothing"
    finally:
        sleeper.kill()
        sleeper.wait()
    assert kimi_live.why_not(_record(good)) is None, "its watcher gone: nothing stale"


def _own_record(body: dict) -> Path:
    pid = os.getpid()
    path = session_marker._process_record_path(pid, session_marker._proc_linux(pid)[1])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(body))
    return path


@pytest.mark.skipif(not os.path.isdir("/proc/self"), reason="the live check reads /proc here")
def test_sessions_follow_reads_every_live_kimi_process(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_TAP_WATCHER_DIR", str(tmp_path / "watchers"))
    (tmp_path / "watchers").mkdir()
    _plugins, probe, _tap = _kimi(tmp_path)
    _service_holds(monkeypatch, tmp_path, "s")
    titles = ("kimi-code", "kimi")
    assert kimi_live.sessions_follow(KIMI, titles) is True, "no live Kimi process: nothing to restart"
    path = _own_record(_record(kimi_live.loaded_info(str(probe), "SessionStart")))
    try:
        assert kimi_live.sessions_follow(KIMI, titles) is True
        path.write_text(json.dumps(_record(None)))
        assert kimi_live.sessions_follow(KIMI, titles) is False
        path.write_text(json.dumps({**_record(None), "harness": "claude_code"}))  # harness-literal-ok: another agent
        assert kimi_live.sessions_follow(KIMI, titles) is True, "another agent's process is not Kimi's"
        path.write_text("not json")
        assert kimi_live.sessions_follow(KIMI, titles) is True, "an unreadable record of a non-Kimi process"
    finally:
        path.unlink()
    gone = session_marker._process_record_path(2 ** 22 - 1, "1")
    gone.write_text(json.dumps(_record(None)))
    try:
        assert kimi_live.sessions_follow(KIMI, titles) is True, "a dead process's record is ignored"
    finally:
        gone.unlink()


@pytest.mark.skipif(not os.path.isdir("/proc/self"), reason="retitled argv shows in /proc")
def test_a_live_kimi_process_with_no_record_is_unproven(tmp_path):
    """Codex review: a missing record is no proof (a hook that never wrote one,
    a record swept on macOS while its process lives, a Kimi without Probe)."""
    import subprocess
    import time

    kimi = subprocess.Popen(["/bin/bash", "-c", "exec -a kimi-code sleep 60"])
    try:
        for _ in range(50):
            if b"kimi-code" in Path(f"/proc/{kimi.pid}/cmdline").read_bytes():
                break
            time.sleep(0.05)
        assert kimi_live.sessions_follow(KIMI, ("kimi-code", "kimi")) is False
        assert kimi_live.sessions_follow(KIMI, ()) is True, "without titles nothing is listed"
    finally:
        kimi.kill()
        kimi.wait()


@pytest.mark.skipif(not os.path.isdir("/proc/self"), reason="the record is keyed by /proc here")
def test_the_process_record_keeps_what_was_loaded_until_a_reload(monkeypatch, tmp_path):
    """Kimi reads its plugins at its start and on /reload only (which reopens
    the same session, SessionStart `resume`, from the folder it now loads): a
    /new (`startup`), a resume of another session, the same session closed and
    reopened from the same folder (an editor's `kimi acp`), a later event, or
    another folder whose old one is gone (the entry's fallback) never rewrites it."""
    me = session_marker._ancestors(os.getpid())[0][2]
    monkeypatch.setattr(session_marker, "_ancestors", lambda pid=None: [(os.getpid(),
                        session_marker._proc_linux(os.getpid())[1], me)])
    monkeypatch.setattr(session_marker, "_process_age", lambda start: 5.0)
    a, b = tmp_path / "probe-research@0.177.0", tmp_path / "probe-research@0.178.0"
    a.mkdir()
    b.mkdir()
    sid, other = "11111111-1111-4111-8111-111111111111", "22222222-2222-4222-8222-222222222222"
    first = {"plugin_root": str(a), "plugin_version": "0.177.0", "late": False, "source": "startup"}
    path = session_marker.record_harness_process(KIMI, sid, me, loaded=first)
    try:
        def recorded():
            return json.loads(path.read_text())["loaded"]

        session_marker.record_harness_process(KIMI, sid, me, loaded={**first, "late": True, "source": ""})
        assert recorded() == first
        new_session = {**first, "tap_root": "/t2", "tap_version": "0.10.21"}  # /new: what is on disk now
        session_marker.record_harness_process(KIMI, other, me, loaded=new_session)
        assert recorded() == first, "a /new loads nothing"
        session_marker.record_harness_process(KIMI, sid, me, loaded={**new_session, "source": "resume"})
        assert recorded() == first, "the same session reopened from the same folder loads nothing (acp)"
        newer = {"plugin_root": str(b), "plugin_version": "0.178.0", "late": False, "source": "resume"}
        session_marker.record_harness_process(KIMI, other, me, loaded=newer)
        assert recorded() == first, "resuming another session than the recorded one loads nothing"
        session_marker.record_harness_process(KIMI, sid, me, loaded={**first, "late": True})
        a.rmdir()
        session_marker.record_harness_process(KIMI, sid, me, loaded=newer)
        assert recorded() == first, "another folder with the old one gone is the entry's fallback"
        a.mkdir()
        session_marker.record_harness_process(KIMI, sid, me, loaded=newer)
        assert recorded() == newer, "a /reload reopens the same session from the folder it loads now"
    finally:
        path.unlink()


@pytest.mark.skipif(not os.path.isdir("/proc/self"), reason="the record is keyed by /proc here")
def test_a_first_record_after_the_install_changed_proves_nothing(monkeypatch, tmp_path):
    """An update between Kimi's start and its first session (the TUI makes it
    at the first prompt): the record would read the new install."""
    me = session_marker._ancestors(os.getpid())[0][2]
    monkeypatch.setattr(session_marker, "_ancestors", lambda pid=None: [(os.getpid(),
                        session_marker._proc_linux(os.getpid())[1], me)])
    monkeypatch.setattr(session_marker, "_process_age", lambda start: 30.0)
    listed = tmp_path / "installed.json"
    listed.write_text("{}")
    old = time.time() - 600
    os.utime(listed, (old, old))
    info = {"plugin_root": "/a", "late": False, "source": "startup", "read_at_start": [str(listed)]}
    path = session_marker.record_harness_process(KIMI, "11111111-1111-4111-8111-111111111111", me, loaded=info)
    try:
        assert json.loads(path.read_text())["loaded"]["late"] is False
        path.unlink()
        os.utime(listed, None)  # written after the process started
        session_marker.record_harness_process(KIMI, "11111111-1111-4111-8111-111111111111", me, loaded=info)
        assert json.loads(path.read_text())["loaded"]["late"] is True
    finally:
        path.unlink(missing_ok=True)


@pytest.mark.skipif(not os.path.isdir("/proc/self"), reason="argv shows in /proc")
def test_a_kimi_session_on_its_own_watcher_is_seen_whatever_its_pid_folder(tmp_path, monkeypatch):
    """Re-review: a session on its own `tap watch` the CLI cannot see by pid
    file (another watcher folder, a sandbox's /tmp, a second session of a
    server host) is found by its process; only the running service's own
    answer proves a session is recorded."""
    import subprocess
    import sys

    _plugins, probe, tap = _kimi(tmp_path)
    good = kimi_live.loaded_info(str(probe), "SessionStart")
    assert kimi_live.why_not(_record(good), recorded={"other"}) is not None
    assert kimi_live.why_not(_record(good), recorded={"s"}) is None
    watch = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)", "-m", "tap", "watch",
                              "--session-id", "w1", "--cwd", "/", "--plugin-root", str(tap)])
    try:
        for _ in range(50):
            if b"w1" in Path(f"/proc/{watch.pid}/cmdline").read_bytes():
                break
            time.sleep(0.05)
        assert "w1" in kimi_live.own_watches()
        titles = ("kimi-code", "kimi")
        assert kimi_live.sessions_follow(KIMI, titles, recorded={"s"}) is False
        assert kimi_live.sessions_follow(KIMI, titles, recorded={"s", "w1"}) is True, "hosted by the service"
    finally:
        watch.kill()
        watch.wait()
    assert kimi_live.sessions_follow(KIMI, ("kimi-code", "kimi"), recorded=set()) is True, "no Kimi session at all"


@pytest.mark.skipif(not os.path.isdir("/proc/self"), reason="the record is keyed by /proc here")
def test_a_first_record_long_after_the_process_started_proves_nothing(monkeypatch):
    """A /new in a Kimi process older than these hooks writes its first record
    from what is on disk now, not what the process loaded: `late`."""
    me = session_marker._ancestors(os.getpid())[0][2]
    start = session_marker._proc_linux(os.getpid())[1]
    monkeypatch.setattr(session_marker, "_ancestors", lambda pid=None: [(os.getpid(), start, me)])
    age = session_marker._process_age(start)
    assert age is not None and 0 <= age < 86400 * 365, age
    monkeypatch.setattr(session_marker, "_process_age", lambda start: session_marker.LOADED_FIRST_SEEN_S + 1)
    info = {"plugin_root": "/a", "plugin_version": "0.177.0", "late": False, "source": "startup"}
    path = session_marker.record_harness_process(KIMI, "11111111-1111-4111-8111-111111111111", me, loaded=info)
    try:
        assert json.loads(path.read_text())["loaded"] == {**info, "late": True}
        assert kimi_live.why_not({"loaded": {**info, "late": True}}) == "its start was not seen"
    finally:
        path.unlink()


def test_the_process_age_reads_ps_start_times():
    when = time.strftime("%a-%b-%d-%H:%M:%S-%Y", time.gmtime(time.time() - 300))
    assert 290 < session_marker._process_age(when) < 400
    assert session_marker._process_age("not a time") is None


def test_harness_io_records_the_folder_the_session_loaded(monkeypatch, tmp_path):
    """The adapter keeps the folder its entry ran from, even after handing the
    event to the installed copy (HANDED_OVER names the session's own)."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("_kimi_harness_io_under_test", HOOKS / "harness_io.py")
    harness_io = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(harness_io)
    _plugins, probe, _tap = _kimi(tmp_path)
    seen = {}
    monkeypatch.setattr(harness_io._session_marker, "record_harness_process",
                        lambda harness, sid, titles, loaded=None: seen.update(loaded=loaded))
    monkeypatch.setenv(harness_io.HANDED_OVER, str(probe))
    harness_io._LOADED_ROOT = os.environ[harness_io.HANDED_OVER]

    class Row:
        id = KIMI
        _raw = {"process_title": "kimi-code", "binary": "kimi"}

    harness_io._record({"hook_event_name": "SessionStart", "session_id": "s"}, Row())
    assert seen["loaded"]["plugin_root"] == str(probe) and seen["loaded"]["late"] is False


#: K3: what Kimi keeps from each Probe manifest at its start (hook entries,
#: skills path, MCP servers by address). A change here means open Kimi sessions
#: need /reload for that release: update the pin AND say so in the plugin
#: CHANGELOG ("Kimi Code sessions need /reload for this release"). K4 keeps the
#: update's own message truthful either way.
MANIFEST_PINS = {
    "probe-research": "feb26713af0b27ae",
    "probe-research-daemon": "51fc97e5cc461cda",
    "probe-research-tap": "71a1b392f8264d90",
}


@pytest.mark.parametrize("plugin", sorted(MANIFEST_PINS))
def test_a_kimi_manifest_change_is_deliberate(plugin):
    got = kimi_live.manifest_fingerprint(str(AGENT / "plugins" / plugin), contents=False)
    assert got == MANIFEST_PINS[plugin], (
        f"{plugin}'s Kimi manifest changed what Kimi loads at start ({got}): open Kimi sessions need /reload "
        "for this release. Update MANIFEST_PINS and add that line to the plugin CHANGELOG."
    )


def test_a_kimi_watch_in_a_macos_ps_line_is_read_whatever_its_folders():
    """macOS `ps` gives no argv boundaries: a folder with a space in it used to
    split the `--plugin-root` and hide the watch."""
    root = "/Users/Jo Doe/.kimi-code/plugins/managed/probe-research-tap@0.10.21"
    line = f"/usr/bin/python3 -m tap watch --session-id s1 --cwd /Users/Jo Doe/work --plugin-root {root}"
    assert kimi_live._watch_in_command(line) == "s1"
    assert kimi_live._watch_in_command(line + "/") == "s1"
    assert kimi_live._watch_in_command(line.replace("managed/probe-research-tap@0.10.21", "cache/x/0.10.21")) is None
    assert kimi_live._watch_in_command("/usr/bin/python3 -m tap record --session-id s1 --plugin-root " + root) is None
    assert kimi_live._watch_in_command("vim watch --session-id s1") is None

