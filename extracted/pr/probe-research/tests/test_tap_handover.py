"""A session on a `tap watch` too old to hand it to the Probe service moves to the service at a prompt (plan C0).

`hooks/tap_handover.py`, a prompt route of the Probe plugin (whose hooks run
the installed copy at every event): a live wrapper proven to be this session's
`tap watch`, from a tap before 0.10.13 (no `tap/handback.py`), with a newer tap
installed that has it, is replaced the way the tap's own session-start.sh
replaces one on resume: `tap record` with the NEWEST installed tap first, then
the old wrapper's group stopped and its pid and version files removed. Never a
wrapper it cannot prove is this session's; never on the prompt's clock; once
per wrapper. The old tap's own hooks still run in the session: its prompt
healer is kept quiet (the REAL old `ensure-daemon.sh` of each tap line, from
git). Real processes (stand-in wrappers, a stand-in service and a stand-in
tap), a scratch HOME, and watcher files in a folder of the test's own
(PROBE_TAP_WATCHER_DIR), never the shared /tmp.
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import signal
import subprocess
import sys
import time
import uuid
from pathlib import Path

import pytest

from tests.service_harness import wait_for

AGENT = Path(__file__).resolve().parents[1]
REPO = AGENT.parent
HOOKS = AGENT / "plugins" / "probe-research" / "hooks"
SCRIPT = HOOKS / "tap_handover.py"
MARKET = "research-os-agent"
#: What the hook dispatcher sets for its own call (`dispatch.OWNED_ENV`).
OWNED = ("PROBE_HOOKS_HANDED_OVER", "PROBE_HOOK_HOSTED", "PROBE_HOOK_HOST", "PROBE_HOOK_DEADLINE",
         "PROBE_HOOK_PARENT_PID")

pytestmark = pytest.mark.skipif(os.name != "posix", reason="the hooks are POSIX shell")

#: The stand-in tap's `python -m tap record`: what it was run with, then the
#: exit the test asked for; recording, it names the stand-in service in the
#: session's `.hosted` marker, as the real one does.
_TAP_MAIN = r'''
import json, os, sys
argv = sys.argv[1:]
with open(os.environ["PROBE_TEST_RECORDED"], "a") as handle:
    handle.write(json.dumps({"argv": argv, "source": os.environ.get("PROBE_TAP_SOURCE"),
                             "root": os.environ.get("CLAUDE_PLUGIN_ROOT"),
                             "pythonpath": os.environ.get("PYTHONPATH"),
                             "owned": {k: os.environ.get(k) for k in %r}}) + "\n")
code = int(os.environ.get("PROBE_TEST_RECORD_EXIT", "0"))
service = os.environ.get("PROBE_TEST_SERVICE_PID")
if code == 0 and service:
    sid = argv[argv.index("--session-id") + 1]
    prefix = "prbe-codex-tap" if os.environ.get("PROBE_TAP_SOURCE") == "codex" else "probe-research-tap"
    with open(os.path.join(os.environ["PROBE_TAP_WATCHER_DIR"], prefix + "-watcher-" + sid + ".hosted"), "w") as h:
        h.write(service)
sys.exit(code)
''' % (OWNED,)

#: Each line of the old tap's prompt healer (`hooks/ensure-daemon.sh`, a new
#: blob at each of these releases; `git log -- agent/plugins/probe-research-tap/
#: .claude-plugin/plugin.json`): the version and its release commit.
OLD_HEALERS = {
    "0.5.0": "725e336d10",   # the first one (no UserPromptSubmit hook before it)
    "0.5.2": "0512b4f38c",   # 0.5.2 .. 0.9.5
    "0.9.6": "2e4ec8145f",
    "0.9.25": "aba5102661",  # 0.9.7 .. 0.9.25
    "0.10.0": "323ad448b1",  # reads the `.hosted` marker
    "0.10.2": "0bb6433136",  # 0.10.1 .. 0.10.2: a dead `.hosted` skips the ten minutes
    "0.10.5": "08da5f1fb0",  # 0.10.3 .. 0.10.5
    "0.10.12": "7d34a66aef",  # 0.10.6 .. 0.10.12, the last before the hand-back
}


def _tap(cache: Path, version: str, *, handback: bool = True) -> Path:
    root = cache / MARKET / "probe-research-tap" / version
    (root / "tap").mkdir(parents=True)
    (root / ".claude-plugin").mkdir()
    (root / ".claude-plugin" / "plugin.json").write_text(json.dumps({"name": "probe-research-tap", "version": version}))
    for name in ("__init__.py", "record_client.py", "hosted.py", *(("handback.py",) if handback else ())):
        (root / "tap" / name).write_text(f'__version__ = "{version}"\n' if name == "__init__.py" else "")
    (root / "tap" / "__main__.py").write_text(_TAP_MAIN)
    return root


def _sleeper(*argv: str, **kwargs) -> subprocess.Popen:
    return subprocess.Popen([sys.executable, "-c", "import time; time.sleep(300)", *argv], **kwargs)


@pytest.fixture
def box(tmp_path):
    home = tmp_path / "home"
    claude = home / ".claude"
    cache = claude / "plugins" / "cache"
    old, new = _tap(cache, "0.10.0", handback=False), _tap(cache, "0.10.20")
    probe = cache / MARKET / "probe-research" / "0.171.0"
    probe.mkdir(parents=True)
    (claude / "plugins" / "installed_plugins.json").write_text(json.dumps({"version": 2, "plugins": {
        f"probe-research-tap@{MARKET}": [{"scope": "user", "installPath": str(new)}],
        f"probe-research@{MARKET}": [{"scope": "user", "installPath": str(probe)}],
    }}))
    watchers = tmp_path / "watchers"
    watchers.mkdir()
    sid = str(uuid.uuid4())
    stem = watchers / f"probe-research-tap-watcher-{sid}"
    processes: list[subprocess.Popen] = []
    service = _sleeper("probe.service", start_new_session=True)
    processes.append(service)
    env = {
        "HOME": str(home), "PATH": os.environ.get("PATH", "/usr/bin:/bin"), "CLAUDE_CONFIG_DIR": str(claude),
        "XDG_STATE_HOME": str(home / ".local" / "state"), "CLAUDECODE": "1", "CLAUDE_CODE_SESSION_ID": sid,
        "CLAUDE_PLUGIN_ROOT": str(HOOKS.parent), "PROBE_TEST_RECORDED": str(tmp_path / "recorded.jsonl"),
        "PROBE_TAP_WATCHER_DIR": str(watchers), "PROBE_TEST_SERVICE_PID": str(service.pid),
    }

    class Box:
        pass

    b = Box()
    b.home, b.old, b.new, b.sid, b.stem, b.env, b.tmp = home, old, new, sid, stem, env, tmp_path
    b.watchers, b.service = watchers, service
    b.recorded = tmp_path / "recorded.jsonl"
    b.markers = home / ".local" / "state" / "probe" / "hooks" / "tap-handover"
    b.tap_state = home / ".claude" / "plugins" / "probe-research-tap"

    def wrapper(command: str | None = None, version: str | None = "0.10.0", **kwargs) -> subprocess.Popen:
        """A wrapper standing in for `tap watch`: a group leader whose command line is the
        one given, else the shape the tap's session-start.sh gives it: `bash -c '<a script over
        several lines, naming tap watch>' wrapper <sid> ...`."""
        if command is None:
            script = 'while :; do\n  "$PY" -m tap watch --session-id "$SID" &\n  wait\ndone'
            proc = _sleeper(script, "wrapper", sid, "/cwd", start_new_session=True)
            probe = "wrapper"
        elif command.startswith("bash-script:"):
            proc = subprocess.Popen(["/bin/bash", "-c", command[len("bash-script:"):], "wrapper", sid],
                                    start_new_session=True, **kwargs)
            probe = "wrapper"
        else:
            proc = subprocess.Popen(["/bin/bash", "-c", f"exec -a '{command}' sleep 300"], start_new_session=True)
            probe = command.split()[0]
        processes.append(proc)
        assert wait_for(lambda: probe in Path(f"/proc/{proc.pid}/cmdline").read_bytes().decode(), 3)
        Path(f"{stem}.pid").write_text(str(proc.pid))
        if version is not None:
            Path(f"{stem}.version").write_text(version)
        return proc

    b.wrapper = wrapper

    def prompt(extra: dict | None = None) -> subprocess.CompletedProcess:
        payload = {"session_id": sid, "hook_event_name": "UserPromptSubmit", "prompt": "go",
                   "transcript_path": str(tmp_path / f"{sid}.jsonl"), "cwd": str(tmp_path)}
        return subprocess.run([sys.executable, str(SCRIPT)], input=json.dumps(payload), capture_output=True,
                              text=True, timeout=30, env={**env, **(extra or {})})

    b.prompt = prompt

    def records() -> list[dict]:
        try:
            return [json.loads(line) for line in b.recorded.read_text().splitlines()]
        except OSError:
            return []

    b.records = records

    def age(path: Path, seconds: float = 3600) -> None:
        os.utime(path, (time.time() - seconds, time.time() - seconds))

    b.age = age
    try:
        yield b
    finally:
        for proc in processes:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except OSError:
                pass
            proc.wait(5)


def _marker(box) -> Path:
    return box.markers / box.sid


def _tries(box) -> int:
    try:
        return int(Path(f"{_marker(box)}.tries").read_text())
    except (OSError, ValueError):
        return 0


def _fresh(path: Path) -> bool:
    try:
        return time.time() - path.stat().st_mtime < 60
    except OSError:
        return False


def _moved(box, count: int) -> None:
    """The swap ran to its end: `tap record` twice per move, the log line written."""
    assert wait_for(lambda: len(box.records()) == count, 10), box.records()
    assert wait_for(lambda: Path(f"{_marker(box)}.moved").exists(), 10)


def test_an_old_watcher_is_replaced_by_the_service_recording_on_the_newest_tap(box):
    """Live test bug 1 (2026-10-24): a session whose `tap watch` started from tap
    0.10.0 (the service could not start at its SessionStart) stayed on it for
    good. At its next prompt, the newest installed tap's `tap record` asks the
    service to record it, then the old wrapper's group is stopped."""
    old = box.wrapper()
    started = time.monotonic()
    done = box.prompt()
    took = time.monotonic() - started
    assert done.returncode == 0 and done.stdout == "", done.stderr
    assert took < 2.0, f"the swap ran on the prompt's clock ({took:.1f} s)"
    _moved(box, 2)
    # Before the old watcher is stopped, and once more after (the service's
    # recorder, which stepped back while the old one held the session, takes it now).
    record, again = box.records()
    assert again == record
    assert record["source"] == "claude_code" and record["pythonpath"] == str(box.new)
    assert record["root"] == str(box.new)
    argv = record["argv"]
    assert argv[:1] == ["record"] and argv[argv.index("--plugin-root") + 1] == str(box.new)
    assert argv[argv.index("--session-id") + 1] == box.sid
    assert argv[argv.index("--transcript") + 1] == str(box.tmp / f"{box.sid}.jsonl")
    assert wait_for(lambda: old.poll() is not None, 10), "the old wrapper still runs"
    assert wait_for(lambda: not Path(f"{box.stem}.pid").exists() and not Path(f"{box.stem}.version").exists(), 5)
    assert Path(f"{_marker(box)}.{old.pid}").exists() and not _marker(box).exists()
    log_file = box.tap_state / "logs" / f"{box.sid}.log"
    said = r"the Probe service records this session on tap 0\.10\.20; the tap 0\.10\.0 watcher"
    assert wait_for(lambda: log_file.exists() and re.search(said, log_file.read_text()), 10)
    # The service records it now (its `.hosted` marker): the next prompt does nothing.
    assert box.prompt().returncode == 0
    time.sleep(1.0)
    assert len(box.records()) == 2


def test_the_swap_hands_tap_record_none_of_the_dispatchers_env(box):
    """The dispatcher's own variables (a deadline, a host) are its call's: `tap
    record` keeps every PROBE_* variable as the session's environment, which
    the service saves and its daemon workers inherit."""
    box.wrapper()
    assert box.prompt({name: "1" for name in OWNED} | {"PROBE_HOOK_DEADLINE": str(time.time() + 5)}).returncode == 0
    _moved(box, 2)
    assert all(record["owned"] == dict.fromkeys(OWNED) for record in box.records()), box.records()


def test_an_old_watcher_the_service_will_not_take_keeps_recording(box):
    """No service can record it (none starts here, a sandbox, its agent gone):
    the old wrapper is never stopped first, so the session is never left with
    nothing recording it."""
    old = box.wrapper()
    assert box.prompt({"PROBE_TEST_RECORD_EXIT": "1"}).returncode == 0
    assert wait_for(lambda: box.records(), 10)
    time.sleep(0.5)
    assert old.poll() is None and Path(f"{box.stem}.pid").read_text() == str(old.pid)


def test_a_failed_tap_record_is_tried_again_later(box):
    """A failed `tap record` is not the end of it: a service restarting right
    after the update that brought this route (or a restart onto a newer tap
    longer than `tap record`'s 6 s) fails once. The swap is tried again after
    LATER_S, MAX_TRIES times in all; only then is the session left on its
    watcher for good."""
    th = _load()
    old = box.wrapper()
    later = Path(f"{_marker(box)}.later")
    for attempt in range(1, th.MAX_TRIES):
        assert box.prompt({"PROBE_TEST_RECORD_EXIT": "1"}).returncode == 0
        assert wait_for(lambda: _tries(box) == attempt and _fresh(later), 10), attempt
        assert len(box.records()) == attempt
        assert not Path(f"{_marker(box)}.{old.pid}").exists()
        assert not _marker(box).exists() and old.poll() is None
        assert box.prompt().returncode == 0
        time.sleep(0.5)
        assert len(box.records()) == attempt, "within LATER_S it does not look again"
        box.age(later)
    # Aged past LATER_S, with a service that records it now: moved.
    assert box.prompt().returncode == 0
    _moved(box, th.MAX_TRIES - 1 + 2)
    assert wait_for(lambda: old.poll() is not None, 10)


def test_the_last_failed_try_leaves_the_watcher_for_good(box):
    th = _load()
    old = box.wrapper()
    later = Path(f"{_marker(box)}.later")
    for attempt in range(1, th.MAX_TRIES + 1):
        if later.exists():
            box.age(later)
        assert box.prompt({"PROBE_TEST_RECORD_EXIT": "1"}).returncode == 0
        assert wait_for(lambda: _tries(box) == attempt, 10), attempt
        assert len(box.records()) == attempt
    assert wait_for(lambda: _marker(box).exists(), 5), "never given up on"
    box.age(later)
    assert box.prompt().returncode == 0
    time.sleep(0.5)
    assert len(box.records()) == th.MAX_TRIES and old.poll() is None


def test_a_dead_pid_file_is_looked_at_once_per_later(box):
    """A wrapper that gave up after its 5 restarts leaves its pid file behind:
    one look per LATER_S, never a python start at every prompt."""
    gone = subprocess.Popen(["true"])
    gone.wait()
    Path(f"{box.stem}.pid").write_text(str(gone.pid))
    Path(f"{box.stem}.version").write_text("0.10.0")
    assert box.prompt().returncode == 0
    later = Path(f"{_marker(box)}.later")
    assert later.exists() and not _marker(box).exists()
    assert box.records() == []
    assert _route(box) is False


@pytest.mark.parametrize("case", ["not-a-tap-watch", "another-session", "new-enough", "no-newer-tap", "no-pid-file"])
def test_what_it_cannot_prove_or_need_not_do_it_leaves_alone(box, case):
    """A pid reused by another process, another session's watcher, a watcher
    that hands back by itself (0.10.13+), no newer tap installed, no watcher."""
    if case == "not-a-tap-watch":
        proc = box.wrapper(command=f"vim notes-{box.sid}.md")
    elif case == "another-session":
        proc = box.wrapper(command=f"python3 -m tap watch --session-id {uuid.uuid4()}")
    elif case == "new-enough":
        proc = box.wrapper(version="0.10.13")
    elif case == "no-newer-tap":
        proc = box.wrapper(version="0.10.20")
    else:
        proc = None
    done = box.prompt()
    assert done.returncode == 0 and done.stdout == ""
    time.sleep(1.0)
    assert box.records() == []
    if proc is not None:
        assert proc.poll() is None and Path(f"{box.stem}.pid").exists()


def test_a_tap_installed_after_the_plugin_is_found_at_a_later_prompt(box):
    """The tap's own update can land after this plugin's: a watcher with no
    newer tap yet is looked at again (every LATER_S), never given up on."""
    ledger = box.home / ".claude" / "plugins" / "installed_plugins.json"
    installed = ledger.read_text()
    ledger.write_text(installed.replace(str(box.new), str(box.old)))  # the tap not updated yet
    old = box.wrapper()
    assert box.prompt().returncode == 0
    time.sleep(0.5)
    assert box.records() == [] and not _marker(box).exists()
    later = Path(f"{_marker(box)}.later")
    assert later.exists()
    ledger.write_text(installed)  # its update lands
    assert box.prompt().returncode == 0
    time.sleep(0.5)
    assert box.records() == [], "within LATER_S it does not look again"
    box.age(later)
    assert box.prompt().returncode == 0
    assert wait_for(lambda: box.records(), 10)
    assert wait_for(lambda: old.poll() is not None, 10)


def test_a_watcher_from_before_version_files_is_read_from_its_command_line(box):
    """Taps before 0.9.16 wrote no `.version`: the versioned folder in the
    wrapper's command line says (as the tap's session-start.sh reads it)."""
    old = box.wrapper(
        command=f"bash -c x /h/.claude/plugins/cache/m/probe-research-tap/0.9.24/hooks python3 -m tap watch "
                f"--session-id {box.sid}",
        version=None,
    )
    assert box.prompt().returncode == 0
    assert wait_for(lambda: box.records(), 10)
    assert wait_for(lambda: old.poll() is not None, 10)


def test_the_worker_is_asked_to_hand_over_before_the_wrapper_is_stopped(box):
    """The old wrapper's stop reaches its companion, which stops the session's
    daemon worker: without a hand-over ask that worker ends the session as
    `stopped`, and a prompt before the service's worker takes the lease reads
    "recording is back with you". The `.handover` marker beside the worker's
    lock is there, dated ahead, before the wrapper gets its SIGTERM."""
    holder, handover = _hold_worker_lock(box)
    try:
        seen = box.tmp / "seen-at-term"
        old = box.wrapper(
            command='bash-script:trap "if [ -e \\"$H\\" ]; then echo yes > \\"$F\\"; else echo no > \\"$F\\"; '
                    'fi; exit 0" TERM; : tap watch; while :; do sleep 0.1; done',
            env={**os.environ, "H": str(handover), "F": str(seen)},
        )
        assert box.prompt().returncode == 0
        _moved(box, 2)
        assert wait_for(lambda: old.poll() is not None, 10)
        assert seen.read_text().strip() == "yes", "the wrapper was stopped before the worker was asked"
        assert handover.stat().st_mtime > time.time() + 60
    finally:
        holder.kill()
        holder.wait(5)


def test_no_worker_no_handover_marker(box):
    """With no worker holding the session's lock, nothing is asked: a marker
    left dated ahead would make a later worker hand over at its session's end."""
    box.wrapper()
    assert box.prompt().returncode == 0
    _moved(box, 2)
    assert not (box.home / ".local" / "state" / "probe" / "daemon" / f"{box.sid}.handover").exists()


def test_a_wrapper_respawned_after_the_swap_is_moved_again(box):
    """The old tap's SessionStart runs again on a compact (and on a `/resume`
    of the session in the same process): a tap before 0.10.0 knows no service
    and starts a wrapper. Its `tap watch` cannot take the journal's claim from
    the service's recorder and gives up within a minute; one still alive at a
    prompt is a new pid, moved again."""
    first = box.wrapper()
    assert box.prompt().returncode == 0
    _moved(box, 2)
    assert wait_for(lambda: first.poll() is not None, 10)
    respawned = box.wrapper(version="0.9.25")
    assert box.prompt().returncode == 0
    assert wait_for(lambda: len(box.records()) == 4, 10), box.records()
    assert wait_for(lambda: respawned.poll() is not None, 10)
    assert Path(f"{_marker(box)}.{respawned.pid}").exists()


def _hold_worker_lock(box) -> tuple[subprocess.Popen, Path]:
    """A process holding the session's daemon worker lock, as a worker does."""
    daemon = box.home / ".local" / "state" / "probe" / "daemon"
    daemon.mkdir(parents=True, exist_ok=True)
    holder = subprocess.Popen(
        [sys.executable, "-c", "import fcntl, sys, time; f = open(sys.argv[1], 'a'); "
         "fcntl.flock(f, fcntl.LOCK_EX); print('held', flush=True); time.sleep(60)", str(daemon / f"{box.sid}.lock")],
        stdout=subprocess.PIPE, text=True,
    )
    assert holder.stdout.readline().strip() == "held"
    return holder, daemon / f"{box.sid}.handover"


def test_a_reswap_asks_no_hand_over_of_the_services_worker(box):
    """A wrapper the old tap started again (a compact) is moved while the
    service already records the session: the worker holding the lock is then
    the SERVICE's, and nothing stops it. A hand-over ask dated ahead would make
    it hand over to nobody at the session's end instead of finishing its queue
    (`RecorderHost._hand_over`: never for a session that is ending)."""
    first = box.wrapper()
    assert box.prompt().returncode == 0
    _moved(box, 2)
    assert wait_for(lambda: first.poll() is not None, 10)
    holder, handover = _hold_worker_lock(box)
    try:
        respawned = box.wrapper(version="0.9.25")
        assert box.prompt().returncode == 0
        assert wait_for(lambda: len(box.records()) == 4, 10), box.records()
        assert wait_for(lambda: respawned.poll() is not None, 10)
        time.sleep(0.3)
        assert not handover.exists() or handover.stat().st_mtime <= time.time(), "asked the service's worker"
    finally:
        holder.kill()
        holder.wait(5)


def test_a_dead_pid_file_left_after_a_move_does_not_block_the_heal(box):
    """A wrapper the old tap started again that gave up (5 restarts) leaves its
    pid file naming a dead pid, and the quieted old healer never removes it.
    In a moved session it names nothing: removed, and the session recorded
    again when nothing records it."""
    first = box.wrapper()
    assert box.prompt().returncode == 0
    _moved(box, 2)
    assert wait_for(lambda: first.poll() is not None, 10)
    gone = subprocess.Popen(["true"])
    gone.wait()
    Path(f"{box.stem}.pid").write_text(str(gone.pid))
    Path(f"{box.stem}.version").write_text("0.9.25")
    Path(f"{box.stem}.hosted").unlink()  # and later the service let go of it
    assert box.prompt().returncode == 0
    assert wait_for(lambda: len(box.records()) == 3, 10), box.records()
    assert not Path(f"{box.stem}.pid").exists()


@pytest.mark.parametrize("kind", ["swap", "heal"])
def test_a_session_switched_off_is_not_recorded_by_this_route(box, kind):
    """Off means not captured (owner, 2026-10-24): neither the move nor the
    heal records a session whose Probe switch is `off` (`dispatch.session_off`).
    Looked at again later: a session switched back on is moved then."""
    sessions = box.home / ".local" / "state" / "probe" / "sessions"
    if kind == "heal":
        box.wrapper()
        assert box.prompt().returncode == 0
        _moved(box, 2)
        Path(f"{box.stem}.hosted").unlink()
    else:
        old = box.wrapper()
    sessions.mkdir(parents=True, exist_ok=True)
    (sessions / f"{box.sid}.state").write_text("off")
    before = len(box.records())
    assert box.prompt().returncode == 0
    time.sleep(0.5)
    assert len(box.records()) == before and Path(f"{_marker(box)}.later").exists()
    if kind == "swap":
        assert old.poll() is None
    (sessions / f"{box.sid}.state").write_text("daemon")
    box.age(Path(f"{_marker(box)}.later"))
    assert box.prompt().returncode == 0
    assert wait_for(lambda: len(box.records()) > before, 10)


def test_a_moved_session_nothing_records_is_recorded_again(box):
    """The swap quiets the old tap's healer, so a moved session nothing records
    any more (`probe capture off` then on, a service gone) is recorded again
    here, as that healer would have: at most every LATER_S, never while capture
    is off."""
    box.wrapper()
    assert box.prompt().returncode == 0
    _moved(box, 2)
    Path(f"{box.stem}.hosted").unlink()  # the service let go of it
    disabled = box.tap_state / ".disabled"
    disabled.parent.mkdir(parents=True, exist_ok=True)
    disabled.write_text("")
    later = Path(f"{_marker(box)}.later")
    assert box.prompt().returncode == 0
    time.sleep(0.5)
    assert len(box.records()) == 2 and later.exists(), "recorded while capture is off"
    disabled.unlink()
    box.age(later)
    assert box.prompt().returncode == 0
    assert wait_for(lambda: len(box.records()) == 3, 10), box.records()
    assert wait_for(lambda: Path(f"{box.stem}.hosted").exists(), 5)
    Path(f"{box.stem}.hosted").unlink()
    assert box.prompt().returncode == 0
    time.sleep(0.5)
    assert len(box.records()) == 3, "within LATER_S it does not look again"


# -- the old tap's own hooks, after the swap ----------------------------------------


def _git_show(rev: str, path: str) -> bytes:
    try:
        done = subprocess.run(["git", "-C", str(REPO), "show", f"{rev}:{path}"], capture_output=True, timeout=30)
    except (OSError, subprocess.SubprocessError) as exc:
        pytest.skip(f"git cannot run here: {exc}")
    if done.returncode != 0:
        pytest.skip(f"{rev} is not in this clone's history (a shallow checkout): {done.stderr.decode()[:200]}")
    return done.stdout


def _old_tap(tmp: Path, version: str) -> tuple[Path, Path]:
    """The real `ensure-daemon.sh` of tap `version` from git, beside a stand-in
    session-start.sh that only says it ran (what the healer would respawn)."""
    rev = OLD_HEALERS[version]
    manifest = json.loads(_git_show(rev, "agent/plugins/probe-research-tap/.claude-plugin/plugin.json"))
    assert manifest["version"] == version, (rev, manifest)
    root = tmp / f"old-tap-{version}"
    (root / "hooks").mkdir(parents=True)
    healer = root / "hooks" / "ensure-daemon.sh"
    healer.write_bytes(_git_show(rev, "agent/plugins/probe-research-tap/hooks/ensure-daemon.sh"))
    healer.chmod(0o755)
    spawned = tmp / f"spawned-{version}"
    (root / "hooks" / "session-start.sh").write_text(f'#!/bin/sh\necho "$$" >> "{spawned}"\n')
    (root / "hooks" / "session-start.sh").chmod(0o755)
    return healer, spawned


def _heal(healer: Path, sid: str, home: Path, source: str = "claude_code") -> subprocess.CompletedProcess:
    """One prompt through the old healer, as its hooks.json runs it."""
    root_env = "PLUGIN_ROOT" if source == "codex" else "CLAUDE_PLUGIN_ROOT"
    env = {"HOME": str(home), "PATH": os.environ.get("PATH", "/usr/bin:/bin"), root_env: str(healer.parents[1])}
    if source == "codex":
        env["PROBE_TAP_SOURCE"] = "codex"
    payload = {"session_id": sid, "hook_event_name": "UserPromptSubmit", "prompt": "go", "cwd": str(home)}
    return subprocess.run(["/bin/bash", str(healer)], input=json.dumps(payload), capture_output=True, text=True,
                          env=env, timeout=30)


@pytest.mark.parametrize("version", list(OLD_HEALERS))
def test_the_real_old_tap_healer_spawns_nothing_after_the_swap(box, version):
    """The old tap's hooks run in the moved session for its whole life. Its
    prompt healer respawns a wrapper whenever no pid file names a live one
    (the swap removes it) and its heal stamp is ten minutes old: the swap
    dates the stamp ahead, so the REAL `ensure-daemon.sh` of every tap line
    from 0.5.0 (the first) to 0.10.12 (the last before the hand-back) respawns
    nothing. Its watcher files are under /tmp, where a fresh session id names
    none (read, never written)."""
    healer, spawned = _old_tap(box.tmp, version)
    # The stand-in proves a respawn would show: a session never moved gets one.
    assert _heal(healer, str(uuid.uuid4()), box.home).returncode == 0
    assert spawned.exists(), "the stand-in session-start.sh never ran: this test proves nothing"
    spawned.unlink()
    old = box.wrapper(version=version)
    assert box.prompt().returncode == 0
    _moved(box, 2)
    assert wait_for(lambda: old.poll() is not None, 10)
    stamp = box.tap_state / "heal" / box.sid
    assert stamp.stat().st_mtime > time.time() + 7 * 24 * 3600, "the heal stamp is not dated ahead"
    for _ in range(2):
        _heal(healer, box.sid, box.home)
    assert not spawned.exists(), f"tap {version}'s healer respawned a wrapper beside the service's recorder"


@pytest.mark.parametrize("legacy", [False, True])
def test_a_codex_old_healer_reads_the_stamp_the_swap_dates(tmp_path, monkeypatch, legacy):
    """Codex's tap keeps its state under ~/.codex/state (a legacy folder while
    only that one exists): the stamp lands where its real healer reads it, and
    never creates the current folder beside a legacy one (that would move the
    old tap's pairing and outbox)."""
    th = _load()
    home = tmp_path / "home"
    state = home / ".codex" / "state"
    if legacy:
        (state / "prbe-codex-tap-plugin").mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("PRBE_CODEX_TAP_PLUGIN_DIR", raising=False)
    harness = th._sibling("_hook_harness").registry().get("codex")
    folder = harness.capture.state_dir(os.environ)
    sid = str(uuid.uuid4())
    healer, spawned = _old_tap(tmp_path, "0.9.25")
    th.quiet_old_healer(str(folder), sid)
    _heal(healer, sid, home, source="codex")
    assert not spawned.exists()
    assert (state / "probe-research-tap").exists() is (not legacy)
    _heal(healer, str(uuid.uuid4()), home, source="codex")
    assert spawned.exists(), "the stand-in never ran: this test proves nothing"


# -- the route --------------------------------------------------------------------


def _load():
    name = "_tap_handover_under_test"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _command(plugin: str = "probe-research") -> str:
    wiring = json.loads((AGENT / "plugins" / plugin / "hooks" / "routes.json").read_text())
    (command,) = [h["command"] for g in wiring["hooks"]["UserPromptSubmit"] for h in g["hooks"]
                  if "tap_handover.py" in h["command"]]
    return command


def _python_shim(tmp: Path) -> Path:
    shim = tmp / "shim-bin"
    shim.mkdir(exist_ok=True)
    (shim / "python3").write_text(f'#!/bin/sh\ncat > "{tmp / "python-ran"}"\n')
    (shim / "python3").chmod(0o755)
    return shim


def _route(box) -> bool:
    """Run the route's shell with a python that only says it ran: did it start?"""
    ran = box.tmp / "python-ran"
    ran.unlink(missing_ok=True)
    payload = json.dumps({"session_id": box.sid, "prompt": "go"})
    env = {**box.env, "PATH": f"{_python_shim(box.tmp)}:/usr/bin:/bin"}
    subprocess.run(["/bin/bash", "-c", _command()[len("/bin/bash -c '"):-1]], input=payload, text=True,
                   capture_output=True, env=env, timeout=10)
    return ran.exists()


def test_the_route_is_a_prompt_route_of_both_tracking_plugins_with_a_shell_fast_path():
    """Every prompt runs it, so with no watcher pid file for the session (every
    session the service records) or once it has looked, its shell exits before
    any python starts."""
    for plugin in ("probe-research", "probe-research-daemon"):
        command = _command(plugin)
        assert (AGENT / "plugins" / plugin / "hooks" / "tap_handover.py").read_bytes() == SCRIPT.read_bytes()
        fast = command.index("tap-handover/$SID")
        assert command.index("PROBE_TAP_WATCHER_DIR") < fast < command.index("command -v python3"), command
        assert command.index('-watcher-"$SID".pid') < command.index("command -v python3"), command
    # The shell's wait is the module's.
    assert f"-mmin -{_load().LATER_S // 60} " in _command()


def test_the_fast_path_starts_no_python_without_a_watcher(tmp_path):
    shim = _python_shim(tmp_path)
    marker = tmp_path / "python-ran"
    watchers = tmp_path / "watchers"
    watchers.mkdir()
    env = {"PATH": f"{shim}:/usr/bin:/bin", "HOME": str(tmp_path), "CLAUDE_PLUGIN_ROOT": str(HOOKS.parent),
           "PROBE_TAP_WATCHER_DIR": str(watchers)}
    body = _command()[len("/bin/bash -c '"):-1]
    for payload in ("{}", json.dumps({"session_id": str(uuid.uuid4()), "prompt": "go"})):
        done = subprocess.run(["/bin/bash", "-c", body], input=payload, text=True, capture_output=True, env=env,
                              timeout=10)
        assert done.returncode == 0 and not marker.exists(), payload
    # A watcher pid file for the session: python runs, and gets the payload.
    sid = str(uuid.uuid4())
    (watchers / f"probe-research-tap-watcher-{sid}.pid").write_text("1")
    payload = json.dumps({"session_id": sid, "prompt": "go"})
    subprocess.run(["/bin/bash", "-c", body], input=payload, text=True, capture_output=True, env=env, timeout=10)
    assert json.loads(marker.read_text()) == {"session_id": sid, "prompt": "go"}


@pytest.mark.parametrize("case", ["handled-wrapper", "given-up", "later", "moved-recorded", "moved-unrecorded",
                                  "never-moved"])
def test_the_fast_path_after_a_look(box, case):
    """What the shell decides alone: a wrapper handled already, a session given
    up on, a look made less than LATER_S ago, and a moved session the service's
    `.hosted` marker names a live pid for start no python; a moved session with
    no live recorder does (to record it again)."""
    markers = box.markers
    markers.mkdir(parents=True)
    pid_file = Path(f"{box.stem}.pid")
    if case == "handled-wrapper":
        pid_file.write_text("4242\n")
        (markers / f"{box.sid}.4242").write_text("")
    elif case == "given-up":
        pid_file.write_text("4242")
        (markers / box.sid).write_text("")
    elif case == "later":
        pid_file.write_text("4242")
        (markers / f"{box.sid}.later").write_text("")
    elif case.startswith("moved"):
        (markers / f"{box.sid}.moved").write_text("")
        gone = subprocess.Popen(["true"])
        gone.wait()
        Path(f"{box.stem}.hosted").write_text(str(box.service.pid if case == "moved-recorded" else gone.pid))
    assert _route(box) is (case == "moved-unrecorded"), case


def test_windows_is_left_alone(monkeypatch):
    """No pid of a Git Bash wrapper can be proven from Windows's Python (and
    `os.kill(pid, 0)` there sends a console control event): never looked at."""
    th = _load()
    monkeypatch.setattr(th, "_WINDOWS", True)
    plan = th.decide({"session_id": str(uuid.uuid4())}, {})
    assert plan is not None and "skip" in plan and "Windows" in plan["skip"]


def test_hosted_off_is_a_definite_no(box):
    """PROBE_TAP_HOSTED=0: the service never records a session here, so the
    session is never looked at again (no `tap record` is even tried)."""
    old = box.wrapper()
    assert box.prompt({"PROBE_TAP_HOSTED": "0"}).returncode == 0
    time.sleep(0.5)
    assert box.records() == [] and _marker(box).exists() and old.poll() is None


def test_a_watcher_file_that_is_a_link_names_nothing(box):
    """The watcher folder is shared: only a regular file of this user's own is read."""
    old = box.wrapper()
    real = box.tmp / "elsewhere.pid"
    real.write_text(str(old.pid))
    Path(f"{box.stem}.pid").unlink()
    Path(f"{box.stem}.pid").symlink_to(real)
    assert box.prompt().returncode == 0
    time.sleep(1.0)
    assert box.records() == [] and old.poll() is None


def test_only_a_provably_gone_pid_file_is_removed(monkeypatch):
    """A moved session's pid file is removed only when its pid is dead or is
    readably something else: a live pid whose command line cannot be read may
    be the respawned wrapper itself, and removing its file would leave it
    recording on the old tap with nothing able to move it again."""
    th = _load()
    sid = str(uuid.uuid4())
    dead = subprocess.Popen([sys.executable, "-c", "pass"])
    dead.wait(10)
    assert th._gone(dead.pid, sid)
    assert th._gone(os.getpid(), sid), "a live pid that is not a tap watch is a reused pid"
    monkeypatch.setattr(th, "_cmdline", lambda pid: "")
    assert not th._gone(os.getpid(), sid), "an unreadable live pid is kept"
    monkeypatch.setattr(th, "_cmdline", lambda pid: f"bash -c : tap watch wrapper {sid}")
    assert not th._gone(os.getpid(), sid)
