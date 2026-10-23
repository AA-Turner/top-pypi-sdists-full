"""Stand-ins for what the Probe service runs, as real processes in a throwaway HOME.

The service runs every action, status read and update as `<the CLI's python>
-I -m probe.core.run <action>`, with the CLI's python taken from
`runtime.json`. `FakeCore` points `runtime.json` at a small script that IS a
python for everything else (it execs this interpreter, so `-m probe.service`
starts the real service), and plays `probe.core.run` from a script the test
writes: the events to print, files to wait for, the exit status. Each child
appends what it was given (argv, stdin, environment, pid) to a log the test
reads. The real `probe.core.run` children are covered by `test_core_run.py`;
these tests are about the service around them.

`fake_open` is macOS's `open` for the desktop app's update: it records its
argv and, like the app's `--background-update` run, writes `app-update.json`.
`fake_app` builds a `Probe.app` bundle under `~/Applications`.
"""

from __future__ import annotations

import json
import plistlib
import stat
import sys
import time
from pathlib import Path

from probe.service import client, paths

_FAKE_PYTHON = r'''#!{real}
import json, os, signal, sys, time

REAL = {real!r}
SCRIPT = {script!r}
BARRIER = {barrier!r}

args = sys.argv[1:]
flags = []
while args and args[0].startswith("-") and args[0] != "-m":
    flags.append(args.pop(0))
if args[:2] != ["-m", "probe.core.run"]:
    os.execv(REAL, [REAL, *flags, *args])

action = args[2]
try:
    plan = json.load(open(SCRIPT)).get(action, {{}})
except (OSError, ValueError):
    plan = {{}}
stdin = sys.stdin.read()
WATCH = ("PROBE_CONFIG_PATH", "PROBE_BASE_URL", "PROBE_TOKEN", "PROBE_AUTOUPDATE_TRIGGER",
         "PROBE_DESKTOP_HUMAN", "PROBE_TELEMETRY", "PROBE_UPDATE_FORCED", "PROBE_UPDATE_SKIP_CLI",
         "PROBE_UPDATE_BARRIER_TOKEN", "CLAUDE_CONFIG_DIR", "XDG_CONFIG_HOME", "PYTHONPATH",
         "CLAUDE_CODE_SESSION_ID", "PATH", "HTTPS_PROXY", "UV_INDEX_URL")
record = {{"action": action, "flags": flags, "stdin": stdin, "pid": os.getpid(), "cwd": os.getcwd(),
          "at": time.time(), "env": {{k: os.environ.get(k) for k in WATCH}},
          "barrier": os.path.exists(BARRIER)}}
with open(plan.get("log") or os.path.expanduser("~/fake-core.log"), "a") as handle:
    handle.write(json.dumps(record) + "\n")

if "stdout" in plan:  # a read: one JSON value, after its `before` steps
    for step in plan.get("before", []):
        if "sleep" in step:
            time.sleep(step["sleep"])
        elif "wait" in step:
            while not os.path.exists(step["wait"]):
                if not os.path.isdir(os.path.expanduser("~")):
                    sys.exit(1)  # the test and its HOME are gone: never wait forever
                time.sleep(0.02)
    sys.stdout.write(json.dumps(plan["stdout"]) + "\n")
    sys.exit(plan.get("exit", 0))

def emit(event):
    sys.stdout.write(json.dumps({{"v": 1, **event}}) + "\n")
    sys.stdout.flush()

interruptible = {{"on": False}}
def on_sigint(*_):
    if interruptible["on"]:
        emit({{"event": "error", "code": "interrupted", "message": "stopped during the browser approval"}})
        emit({{"event": "done", "ok": False, "complete": False, "exit_code": 130, "steps": []}})
        os._exit(130)
signal.signal(signal.SIGINT, on_sigint)

for step in plan.get("steps", []):
    if "event" in step:
        # `interruptible` on an event: the wait it opens starts BEFORE it is
        # printed, so a cancel sent the moment it is seen lands inside it.
        interruptible["on"] = bool(step.get("interruptible"))
        emit(step["event"])
    elif "sleep" in step:
        time.sleep(step["sleep"])
    elif "wait" in step:
        interruptible["on"] = bool(step.get("interruptible"))
        while not os.path.exists(step["wait"]):
            if not os.path.isdir(os.path.expanduser("~")):
                sys.exit(1)  # the test and its HOME are gone: never wait forever
            time.sleep(0.02)
        interruptible["on"] = False
    elif "touch" in step:
        open(step["touch"], "a").close()
    elif "exit" in step:
        sys.exit(step["exit"])
emit({{"event": "done", "ok": True, "complete": True, "exit_code": 0, "steps": []}})
sys.exit(plan.get("exit", 0))
'''

_FAKE_OPEN = r'''#!{real}
import json, os, sys, time
with open(os.path.expanduser("~/fake-open.log"), "a") as handle:
    handle.write(json.dumps({{"argv": sys.argv[1:], "at": time.time()}}) + "\n")
result = {result!r}
if result is not None:
    time.sleep({delay!r})
    target = os.path.expanduser("~/.local/state/probe/service/app-update.json")
    report = {{"version_before": "0.1.3", "version_after": "0.1.4" if result == "updated" else "0.1.3",
              "result": result, "error": {error!r},
              "finished_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime({finished_offset!r} + time.time()))}}
    with open(target + ".tmp", "w") as handle:
        json.dump(report, handle)
    os.replace(target + ".tmp", target)
'''


def _executable(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return path


class FakeCore:
    """`runtime.json` -> a python that plays `probe.core.run` from `script`."""

    def __init__(self, home: Path) -> None:
        self.home = home
        self.script = home / "fake-core.json"
        self.log = home / "fake-core.log"
        self.python = _executable(
            home / "fake-python",
            _FAKE_PYTHON.format(real=sys.executable, script=str(self.script), barrier=str(paths.barrier_path())),
        )
        self.plans: dict = {}
        self.write()
        client.write_runtime(str(self.python), "test")

    def write(self) -> None:
        self.script.write_text(json.dumps(self.plans), encoding="utf-8")

    def plan(self, action: str, **plan: object) -> None:
        self.plans[action] = plan
        self.write()

    def calls(self, action: str | None = None) -> list[dict]:
        try:
            lines = self.log.read_text(encoding="utf-8").splitlines()
        except OSError:
            return []
        found = [json.loads(line) for line in lines if line.strip()]
        return [c for c in found if action is None or c["action"] == action]


_DEFAULT_ERROR = object()


def fake_open(
    bin_dir: Path,
    *,
    result: str | None = "updated",
    delay: float = 0.0,
    finished_offset: float = 0.0,
    error: object = _DEFAULT_ERROR,
) -> Path:
    """An `open` on PATH that records its argv and writes the app's report
    (`result` None: writes nothing; `finished_offset` < 0: an old report;
    `error` defaults to the app's own: none, a reason when `failed`)."""
    if error is _DEFAULT_ERROR:
        error = "signature check failed" if result == "failed" else None
    bin_dir.mkdir(parents=True, exist_ok=True)
    fake_xattr(bin_dir)
    return _executable(
        bin_dir / "open",
        _FAKE_OPEN.format(
            real=sys.executable, result=result, delay=delay, finished_offset=finished_offset, error=error
        ),
    )


_FAKE_XATTR = r'''#!{real}
import os, sys
# macOS's `xattr -p <name> <path>`: exit 0 and the value when <path> has it set,
# else 1. A bundle carries com.apple.quarantine here when fake_app marked it.
args = sys.argv[1:]
if args[:1] == ["-p"] and len(args) == 3 and os.path.exists(os.path.join(args[2], ".fake-quarantine")):
    print("0083;6712a1b0;Safari;")
    sys.exit(0)
print(f"xattr: {{args[-1] if args else ''}}: No such xattr: {{args[1] if len(args) > 1 else ''}}", file=sys.stderr)
sys.exit(1)
'''


def fake_xattr(bin_dir: Path) -> Path:
    """macOS's `xattr` on PATH, for the quarantine check (`fake_app(quarantined=True)`)."""
    bin_dir.mkdir(parents=True, exist_ok=True)
    return _executable(bin_dir / "xattr", _FAKE_XATTR.format(real=sys.executable))


def open_calls(home: Path) -> list[dict]:
    try:
        lines = (home / "fake-open.log").read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    return [json.loads(line) for line in lines if line.strip()]


def fake_app(
    home: Path,
    *,
    bundle_id: str = "ai.prbe.desktop",
    capability: object = 1,
    version: str = "0.1.3",
    quarantined: bool = False,
) -> Path:
    """`~/Applications/Probe.app` with the Info.plist the service reads
    (`quarantined`: never opened, as `fake_xattr` reports it)."""
    app = home / "Applications" / "Probe.app"
    (app / "Contents" / "MacOS").mkdir(parents=True, exist_ok=True)
    if quarantined:
        (app / ".fake-quarantine").touch()
    info = {"CFBundleIdentifier": bundle_id, "CFBundleShortVersionString": version, "CFBundleExecutable": "Probe"}
    if capability is not None:
        info["ProbeBackgroundUpdate"] = capability
    with open(app / "Contents" / "Info.plist", "wb") as handle:
        plistlib.dump(info, handle)
    return app


def enable_auto_update(home: Path, enabled: bool = True) -> None:
    state = home / ".local" / "state" / "probe"
    state.mkdir(parents=True, exist_ok=True)
    (state / "autoupdate.json").write_text(json.dumps({"enabled": enabled}), encoding="utf-8")


def autoupdate_state(home: Path) -> dict:
    try:
        return json.loads((home / ".local" / "state" / "probe" / "autoupdate.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def last_checked(hours_ago: float) -> None:
    """The updater's record says it last checked this long ago."""
    paths.private_dir(paths.service_dir())
    paths.update_state_path().write_text(
        json.dumps({"v": 1, "last_check": time.time() - hours_ago * 3600}), encoding="utf-8"
    )


def events_until(conn, predicate, timeout: float) -> list[dict]:
    """Notifications on `conn` until one satisfies `predicate` (inclusive)."""
    seen: list[dict] = []
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        event = conn.next_event(max(0.05, deadline - time.monotonic()))
        if event is None:
            continue
        seen.append(event)
        if predicate(event):
            return seen
    raise AssertionError(f"no matching event within {timeout}s; saw {seen}")


__all__ = [
    "FakeCore",
    "autoupdate_state",
    "enable_auto_update",
    "events_until",
    "fake_app",
    "fake_open",
    "fake_xattr",
    "last_checked",
    "open_calls",
]
