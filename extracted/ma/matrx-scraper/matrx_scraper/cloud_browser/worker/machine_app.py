"""One supervised app process on the person's Cloud Computer (machines plan 4b part 2 item 3).

The host (AI Dream) decides WHAT runs — argv, working folder, loopback port and the exact
environment — and hands it over through the worker's ``PUT /machine/app`` (machine agent
token). The worker owns the process: it starts it, restarts it when it exits (backoff, like
``AgentDaemon.run_forever``), writes its output to a log in the home, and ends it when the
host says stop or the worker itself shuts down (the machine stopping). The worker's
``/app/{path}`` door relays to that loopback port, so the host reaches the app through the
same authenticated door it reaches the agent daemon through.

**The app's environment is exactly what the spec names, on top of a minimal base** (PATH,
HOME, LANG). Nothing of the worker's own launch environment reaches it — the launch carries
the machine's files token and the host's service address, and the app is not entitled to
either. The host keeps its side of the rule: it sends identity plus a public-by-design
allowlist, never its own credentials.

This module knows nothing about what the app is; it is the generic primitive.
"""

from __future__ import annotations

import asyncio
import contextlib
import hashlib
import json
import logging
import os
import signal
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

#: Where app output goes, under the home (survives stops; the person can read it).
APP_LOG_DIR = ".matrx/app"
#: A log past this size is rotated to ``<name>.log.1`` at the next (re)start.
APP_LOG_MAX_BYTES = 20 * 1024 * 1024
#: Ports the app may never take (the agent daemon's).
RESERVED_PORTS = frozenset({8765})
_NAME_OK = set("abcdefghijklmnopqrstuvwxyz0123456789-_")


class AppSpecError(ValueError):
    """A spec the worker refuses; the sentence names the field."""


@dataclass(frozen=True)
class AppSpec:
    name: str
    argv: tuple[str, ...]
    cwd: str
    port: int
    env: dict[str, str] = field(default_factory=dict)
    #: How long a stop waits for the app after SIGTERM before SIGKILL (the host may say).
    stop_grace_seconds: float = 15.0

    def digest(self) -> str:
        raw = json.dumps(
            {"name": self.name, "argv": list(self.argv), "cwd": self.cwd, "port": self.port, "env": self.env},
            sort_keys=True,
        )
        return hashlib.sha256(raw.encode()).hexdigest()[:24]


def parse_spec(raw: Any, *, home: str) -> AppSpec:
    """The host's spec, checked: a name, an argv of strings, a folder inside the home, a
    loopback port the daemon does not hold, and an env of name -> string."""
    if not isinstance(raw, dict):
        raise AppSpecError("the app spec must be an object")
    name = str(raw.get("name") or "")
    if not name or len(name) > 40 or not set(name) <= _NAME_OK:
        raise AppSpecError("name must be 1-40 lowercase letters, digits, '-' or '_'")
    argv = raw.get("argv")
    if not isinstance(argv, list) or not argv or not all(isinstance(a, str) and a for a in argv):
        raise AppSpecError("argv must be a non-empty list of strings")
    home_path = Path(home).resolve()
    cwd = Path(str(raw.get("cwd") or home)).expanduser()
    if not cwd.is_absolute():
        cwd = home_path / cwd
    cwd = cwd.resolve()
    if cwd != home_path and not cwd.is_relative_to(home_path):
        raise AppSpecError("cwd must be inside the machine's home")
    port = raw.get("port")
    if not isinstance(port, int) or isinstance(port, bool) or not 1024 <= port <= 65535 or port in RESERVED_PORTS:
        raise AppSpecError("port must be a free loopback port 1024-65535 (not the agent daemon's)")
    env = raw.get("env") or {}
    if not isinstance(env, dict) or not all(isinstance(k, str) and k and isinstance(v, str) for k, v in env.items()):
        raise AppSpecError("env must be an object of name -> string")
    spec = AppSpec(name=name, argv=tuple(argv), cwd=str(cwd), port=port, env=dict(env))
    grace = raw.get("stop_grace_seconds")
    if grace is not None:
        if not isinstance(grace, (int, float)) or isinstance(grace, bool) or not 0 < grace <= 300:
            raise AppSpecError("stop_grace_seconds must be a number of seconds, 0-300")
        spec = AppSpec(**{**spec.__dict__, "stop_grace_seconds": float(grace)})
    return spec


class MachineApp:
    """The one supervised app on this machine (none until the host asks)."""

    def __init__(self, home: str) -> None:
        self.home = home
        self.spec: AppSpec | None = None
        self.restarts = 0
        self.last_exit: int | None = None
        self.started_at: float | None = None
        self._proc: asyncio.subprocess.Process | None = None
        self._task: asyncio.Task[None] | None = None
        self._stopping = False

    # ── what the process gets ───────────────────────────────────────────────
    def base_env(self) -> dict[str, str]:
        return {
            "PATH": f"{self.home}/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
            "HOME": self.home,
            "LANG": "C.UTF-8",
        }

    def env_for(self, spec: AppSpec) -> dict[str, str]:
        """The minimal base + the spec's names. Never the worker's launch environment."""
        return {**self.base_env(), **spec.env}

    def log_path(self, spec: AppSpec) -> Path:
        return Path(self.home) / APP_LOG_DIR / f"{spec.name}.log"

    @property
    def running(self) -> bool:
        return self._proc is not None and self._proc.returncode is None

    @property
    def pid(self) -> int | None:
        """The running app's pid (its process-group root), or None."""
        return self._proc.pid if self.running and self._proc is not None else None

    @property
    def port(self) -> int | None:
        return self.spec.port if self.spec is not None else None

    # ── lifecycle ───────────────────────────────────────────────────────────
    async def apply(self, spec: AppSpec) -> dict[str, Any]:
        """Run ``spec``. The same spec already supervised is left alone (idempotent); a
        different one replaces it (the old process is stopped first)."""
        if self.spec is not None and self.spec.digest() == spec.digest() and self._task is not None and not self._task.done():
            return {**self.status(), "changed": False}
        await self.stop()
        self.spec = spec
        self.restarts = 0
        self.last_exit = None
        self._stopping = False
        self._task = asyncio.create_task(self._run_forever(spec), name=f"machine-app-{spec.name}")
        return {**self.status(), "changed": True}

    async def stop(self) -> None:
        """End the app and its supervision. Safe to call when nothing runs."""
        self._stopping = True
        await self._terminate()
        if self._task is not None:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError, Exception):
                await self._task
        self._task = None

    async def _terminate(self) -> None:
        proc = self._proc
        if proc is None or proc.returncode is not None:
            return
        grace = self.spec.stop_grace_seconds if self.spec is not None else 15.0
        with contextlib.suppress(ProcessLookupError, PermissionError):
            os.killpg(proc.pid, signal.SIGTERM)
        try:
            await asyncio.wait_for(proc.wait(), grace)
        except TimeoutError:
            with contextlib.suppress(ProcessLookupError, PermissionError):
                os.killpg(proc.pid, signal.SIGKILL)
            await proc.wait()

    def _open_log(self, spec: AppSpec):  # noqa: ANN202
        path = self.log_path(spec)
        path.parent.mkdir(parents=True, exist_ok=True)
        with contextlib.suppress(OSError):
            if path.stat().st_size > APP_LOG_MAX_BYTES:
                path.replace(path.with_name(path.name + ".1"))
        return open(path, "ab", buffering=0)  # noqa: SIM115 - handed to the child

    async def _run_forever(self, spec: AppSpec) -> None:
        loop = asyncio.get_running_loop()
        delay = 1.0
        while not self._stopping:
            log = self._open_log(spec)
            try:
                log.write(f"\n[machine-app] starting {spec.name} (restart {self.restarts})\n".encode())
                self._proc = await asyncio.create_subprocess_exec(
                    *spec.argv, cwd=spec.cwd, env=self.env_for(spec),
                    stdout=log, stderr=asyncio.subprocess.STDOUT, stdin=asyncio.subprocess.DEVNULL,
                    start_new_session=True,
                )
            except OSError as exc:
                log.write(f"[machine-app] could not start: {exc}\n".encode())
                log.close()
                self.last_exit = -1
                logger.error("machine app %s could not start: %s", spec.name, exc)
            else:
                log.close()
                self.started_at = loop.time()
                self.last_exit = await self._proc.wait()
                if self._stopping:
                    return
                logger.warning("machine app %s exited %s; restarting in %.0fs", spec.name, self.last_exit, delay)
            self.restarts += 1
            await asyncio.sleep(delay)
            delay = min(delay * 2, 30.0)

    async def wait_listening(self, timeout: float) -> bool:
        """True once the app accepts on its loopback port, False after ``timeout``."""
        if self.spec is None:
            return False
        loop = asyncio.get_running_loop()
        deadline = loop.time() + timeout
        while True:
            try:
                _, writer = await asyncio.open_connection("127.0.0.1", self.spec.port)
            except OSError:
                if loop.time() >= deadline:
                    return False
                await asyncio.sleep(0.2)
                continue
            writer.close()
            with contextlib.suppress(Exception):
                await writer.wait_closed()
            return True

    def status(self) -> dict[str, Any]:
        spec = self.spec
        return {
            "configured": spec is not None,
            "name": spec.name if spec else None,
            "port": spec.port if spec else None,
            "cwd": spec.cwd if spec else None,
            "spec_digest": spec.digest() if spec else None,
            "running": self.running,
            "restarts": self.restarts,
            "last_exit": self.last_exit,
            "log": str(self.log_path(spec)) if spec else None,
            # Names only, never a value.
            "env_names": sorted(spec.env) if spec else [],
        }


__all__ = ["APP_LOG_DIR", "AppSpec", "AppSpecError", "MachineApp", "parse_spec"]
