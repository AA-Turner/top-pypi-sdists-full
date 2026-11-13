"""Lifted verbatim from fitevict/cli/installer.py (sha256 f9080232225dcfc9): InstallError, Plan, execute, probe_host, render_env and what they reach in that file.
Written by tools/refactors/core-off-fitevict-20261110/lift.py; the definitions below are the original text."""
from __future__ import annotations

import sys
import threading
import time
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Callable, Dict, List

from abstract_essentials.env_utils.environment import read_env          # noqa: F401  (as fitevict's installer exposed them)
from abstract_essentials.file_ops.file_ops import write_file            # noqa: F401
from hugpy_resources.imports.functions.ports import port_free           # noqa: F401

PROGRESS_INTERVAL_S = 15            # imports.constants.cli.INSTALLER_PROGRESS_INTERVAL_S
SERVICE = 'hugpy-wrapper'           # imports.constants.cli.INSTALLER_SERVICE


class InstallError(RuntimeError):
    """Preflight or a step failed; nothing after it ran."""


def render_env(values: Dict[str, str]) -> str:
    lines = [f"# {SERVICE} service configuration — written by `fitevict install`.",
             "# Edit and run `fitevict install` again (or restart the service) to apply."]
    for k in sorted(values):
        v = str(values[k])
        if any(c in v for c in "\n\r\"\\"):
            raise InstallError(f"{k}: newlines, quotes and backslashes are not allowed in values")
        lines.append(f'{k}="{v}"' if (" " in v or "#" in v) else f"{k}={v}")
    return "\n".join(lines) + "\n"


def probe_host(host: str) -> str:
    return "127.0.0.1" if host in ("0.0.0.0", "") else ("::1" if host == "::" else host)


@dataclass
class Step:
    name: str
    detail: str
    run: Callable[[], None]


@dataclass
class Plan:
    steps: List[Step] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    def add(self, name: str, detail: str, run: Callable[[], None]) -> None:
        self.steps.append(Step(name, detail, run))


_PROGRESS = ContextVar("installer_progress", default=None)


class _StepProgress:
    def __init__(self, name, out):
        self.name, self.out = name, out
        self.started = self.last_output = time.monotonic()
        self.lock = threading.Lock()
        self.stopped = threading.Event()

    def write(self, text):
        with self.lock:
            self.out.write(text)
            self.out.flush()
            self.last_output = time.monotonic()

    def heartbeat(self):
        while not self.stopped.wait(PROGRESS_INTERVAL_S):
            with self.lock:
                now = time.monotonic()
                if now - self.last_output >= PROGRESS_INTERVAL_S:
                    print(f"  {self.name}: still running ({now - self.started:.0f}s elapsed)",
                          file=self.out, flush=True)
                    self.last_output = now


def execute(plan: Plan, dry_run: bool, out=sys.stdout) -> None:
    for i, s in enumerate(plan.steps, 1):
        print(f"[{i}/{len(plan.steps)}] {s.name}: {s.detail}", file=out, flush=True)
        if not dry_run:
            progress = _StepProgress(s.name, out)
            token = _PROGRESS.set(progress)
            heartbeat = threading.Thread(target=progress.heartbeat, daemon=True)
            heartbeat.start()
            try:
                s.run()
            except BaseException:
                progress.write(f"  {s.name}: failed ({time.monotonic() - progress.started:.1f}s elapsed)\n")
                raise
            else:
                progress.write(f"  {s.name}: done ({time.monotonic() - progress.started:.1f}s elapsed)\n")
            finally:
                progress.stopped.set()
                heartbeat.join()
                _PROGRESS.reset(token)
    for n in plan.notes:
        print(f"note: {n}", file=out, flush=True)
    print("dry run: nothing was changed" if dry_run else "installed", file=out, flush=True)
