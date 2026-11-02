"""finishing: become the finisher on a base Python outside every env being deleted."""

from __future__ import annotations

import contextlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
TAIL_NAME = "tail.json"
FINISHER_NAME = "finisher.py"


# -- finishing (U-T9) ----------------------------------------------------------------------------


def _python_works(python: str) -> bool:
    """Does `python` start, isolated, as a Python >= 3.8 within 5 s? (macOS's
    /usr/bin/python3 without the developer tools is a stub that does not.)"""
    try:
        done = subprocess.run([python, "-I", "-S", "-c", "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 3)"],
                              capture_output=True, timeout=5, check=False, stdin=subprocess.DEVNULL)
    except (OSError, subprocess.SubprocessError):
        return False
    return done.returncode == 0


def base_python(plan: dict) -> str | None:
    """The interpreter the finisher runs on, never one inside an env being
    deleted: this process's own (`realpath(sys.executable)`, which for a uv
    env is the uv-managed Python it was made from), else the first of the
    env's base (`pyvenv.cfg`'s home), `sys._base_executable`, `python3` on PATH
    and /usr/bin/python3 that passes `_python_works`. None: run it in-process."""
    from probe.service.updater import lifeboat

    doomed = [Path(p) for p in plan.get("env_generations", [])]
    for path in plan.get("paths", []):
        if path.get("stage") == "finish" and path.get("kind") in ("dir", "link"):
            doomed.append(Path(path["path"]))

    def inside(candidate: str) -> bool:
        real = os.path.realpath(candidate)
        for root in doomed:
            for spelling in {str(root), os.path.realpath(root)}:
                prefix = spelling.rstrip(os.sep) + os.sep
                if candidate.startswith(prefix) or real.startswith(prefix):
                    return True
        return False

    own = os.path.realpath(sys.executable) if sys.executable else ""
    if own and os.path.isfile(own) and not inside(own):
        return own
    candidates = [lifeboat.base_python(Path(sys.prefix)), getattr(sys, "_base_executable", None),
                  shutil.which("python3"), "/usr/bin/python3"]
    for candidate in candidates:
        if isinstance(candidate, str) and os.path.isfile(candidate) and os.access(candidate, os.X_OK) \
                and not inside(candidate) and _python_works(candidate):
            return candidate
    return None


def _phase_finishing(run: Run) -> int:
    """Become the finisher. Returns only when that could not happen (then it
    runs in this process instead, and its exit status is returned)."""
    from probe.shared.updates import finisher, handoff
    from probe.core import events
    from probe.foundation.service_api import paths

    if run.options.embedded:
        return _finish_here(run)
    folder = paths.uninstall_dir()
    plan_path = paths.uninstall_plan_path()
    copy = folder / FINISHER_NAME
    shutil.copyfile(finisher.__file__, copy)
    os.chmod(copy, 0o600)
    from probe.cli.wizard import terminal as tui

    tui.leave_window()  # the menu's window, when Uninstall came from it: nothing after this closes it
    json_mode = events.enabled()
    tail, events_fd = events.handover()
    if json_mode:
        # `resumed` for the finisher's own `reason` (exit 1): a finish of an earlier run.
        (folder / TAIL_NAME).write_text(json.dumps({**tail, "resumed": run.resumed}), encoding="utf-8")
    python = base_python(run.plan)
    argv = ["-I", "-S", str(copy), "--plan", str(plan_path), *(["--json"] if json_mode else [])]
    env = dict(os.environ)
    if run.lock_fd is not None:
        os.set_inheritable(run.lock_fd, True)
        env[handoff.LOCK_FD_ENV] = str(run.lock_fd)
    for stream in (sys.stdout, sys.stderr):
        with contextlib.suppress(Exception):
            stream.flush()
    if json_mode and events_fd is not None:
        os.dup2(events_fd, 1)  # the finisher ends the event stream on stdout
    if python is not None:
        try:
            os.execve(python, [python, *argv], env)
        except OSError:
            pass
    # No interpreter outside the env (or the exec failed): finish here. The
    # env's files go from under this process, which needs none of them again.
    os.environ.update({k: v for k, v in env.items() if k == handoff.LOCK_FD_ENV})
    code = finisher.run(str(plan_path), json_mode=json_mode)
    os._exit(code)  # the stream ended with the finisher's `done`: nothing more may be written


def _finish_here(run: Run) -> int:
    """The finisher in THIS process, for an installer that goes on after it:
    every planned path but the env this process runs from (the installer's
    own `prune` takes it once nothing runs from it)."""
    from probe.shared.updates import finisher, handoff
    from probe.cli.install.uninstall import plan as uninstall_plan
    from probe.foundation.service_api import paths

    here = os.path.realpath(sys.prefix)

    def in_use(entry: dict) -> bool:
        real = os.path.realpath(entry.get("path") or "")
        return here == real or here.startswith(real.rstrip(os.sep) + os.sep)

    plan = dict(run.plan)
    plan["paths"] = [e for e in plan.get("paths", []) if not (e.get("kind") == "dir" and in_use(e))]
    uninstall_plan.write(plan)
    shutil.copyfile(finisher.__file__, paths.uninstall_dir() / FINISHER_NAME)
    held = run.lock_fd
    if held is None:
        held = handoff._held.get(str(handoff.lock_path(uninstall_plan.primary_versions_root())))  # noqa: SLF001
    previous = os.environ.get(handoff.LOCK_FD_ENV)
    if held is not None:
        os.environ[handoff.LOCK_FD_ENV] = str(held)
    try:
        return finisher.run(str(paths.uninstall_plan_path()))
    finally:
        if previous is None:
            os.environ.pop(handoff.LOCK_FD_ENV, None)
        else:
            os.environ[handoff.LOCK_FD_ENV] = previous
from probe.cli.install.uninstall.state import Run  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.uninstall.uninstall import run  # noqa: E402 -- pieces need each other; the front door loads this one first
