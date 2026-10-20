"""Agent shell/filesystem tools on the person's Cloud Computer.

The machine runs the SAME sandbox daemon every Matrx Sandbox runs
(``matrx_agent``, from matrx-sandbox, installed in the image at
``/opt/matrx-agent``) on loopback only. This module is the one door to it:

* ``/agent/{path}`` on the worker forwards to the daemon after verifying the
  ``X-Sandbox-Access-Token`` the platform's sandbox proxy already sends
  (matrx-ai ``tools/_sandbox_proxy.py``). The token is AI Dream's ES256 worker
  token for THIS machine (``aud=worker:<id>``, ``mtx_op=machine_agent``),
  reusable until it expires — a tool loop sends many calls with one binding.
* Before forwarding, a read of a Cloud stub or a shell command that names one
  fetches it first (fetch-on-open), so agents never see a placeholder.

The daemon's own cloud-files replica stays OFF (no bridge env reaches it): the
``Cloud`` folder is owned by ``cloud_files_sync``.
"""

from __future__ import annotations

import asyncio
import logging
import os
import secrets
from collections.abc import Mapping
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

AGENT_PYTHON = "/opt/matrx-agent/bin/python"
AGENT_PORT = 8765
AGENT_OP = "machine_agent"
#: Env the daemon must never inherit (its own replica would race ours).
_STRIPPED_ENV = ("MATRX_CLOUD_FILES_TOKEN", "MATRX_AIDREAM_SERVICE_TOKEN", "MATRX_AIDREAM_URL")


class AgentDaemon:
    """The loopback ``matrx_agent`` process, restarted if it exits."""

    def __init__(
        self, home: str, *, launch_env: Mapping[str, str], python: str = AGENT_PYTHON, port: int = AGENT_PORT
    ) -> None:
        self.home = home
        #: The worker's process environment, handed in by the entrypoint (server.py).
        self.launch_env = dict(launch_env)
        self.python = python
        self.port = port
        self.token = secrets.token_urlsafe(32)
        self.restarts = 0
        self.last_exit: int | None = None
        self._proc: asyncio.subprocess.Process | None = None

    @property
    def available(self) -> bool:
        return os.access(self.python, os.X_OK)

    @property
    def base_url(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    def _env(self) -> dict[str, str]:
        env = {k: v for k, v in self.launch_env.items() if k not in _STRIPPED_ENV}
        env.update(
            MATRX_AGENT_TOKEN=self.token,
            MATRX_WORKSPACE_ROOT=self.home,
            HOT_PATH=self.home,
            HOME=self.home,
        )
        return env

    async def run_forever(self) -> None:
        if not self.available:
            logger.warning("agent daemon not installed at %s; agent tools are off", self.python)
            return
        delay = 1.0
        while True:
            self._proc = await asyncio.create_subprocess_exec(
                self.python, "-m", "uvicorn", "matrx_agent.api.main:app",
                "--host", "127.0.0.1", "--port", str(self.port), "--log-level", "warning",
                cwd=self.home, env=self._env(),
            )
            self.last_exit = await self._proc.wait()
            self.restarts += 1
            logger.warning("agent daemon exited %s; restarting in %.0fs", self.last_exit, delay)
            await asyncio.sleep(delay)
            delay = min(delay * 2, 30.0)

    def status(self) -> dict[str, Any]:
        return {
            "installed": self.available,
            "running": self._proc is not None and self._proc.returncode is None,
            "restarts": self.restarts,
            "last_exit": self.last_exit,
        }


def stub_paths_named(command: str, sync: Any, cwd: str | None) -> list[str]:
    """Cloud stubs a shell command names (by cloud path or file name) — fetched first."""
    if sync is None or not command:
        return []
    named = []
    for rel, entry in list(sync.entries.items()):
        if entry.stub and (rel in command or os.path.basename(rel) in command):
            named.append(rel)
    return named


async def hydrate_for_request(method: str, path: str, params: dict[str, str], body: Any, sync: Any) -> list[str]:
    """The open hook: fetch every stub this agent call is about to read."""
    if sync is None:
        return []
    wanted: list[str] = []
    if method == "GET" and path in ("fs/read", "fs/download"):
        rel = sync.rel_for(params.get("path", ""))
        if rel and sync.is_stub(rel):
            wanted.append(rel)
    elif method == "POST" and path == "exec" and isinstance(body, dict):
        wanted = stub_paths_named(str(body.get("command") or ""), sync, body.get("cwd"))
    fetched = []
    for rel in wanted:
        try:
            if await sync.hydrate(rel):
                fetched.append(rel)
        except Exception:  # noqa: BLE001 - the command still runs; the stub says what it is
            logger.exception("fetch-on-open failed for %s", rel)
    return fetched


def home_dir() -> str:
    return str(Path.home())


def parse_exec_stream(raw: str, *, cwd: str) -> dict[str, Any]:
    """The daemon's ``/exec/stream`` SSE -> the orchestrator ``ExecResponse`` shape
    (``{exit_code, stdout, stderr, cwd}``) the sandbox proxy's ``/exec`` returns."""
    import json

    out: dict[str, list[str]] = {"stdout": [], "stderr": []}
    result: dict[str, Any] = {"exit_code": -1, "cwd": cwd}
    for block in raw.split("\n\n"):
        event, data = "", ""
        for line in block.splitlines():
            if line.startswith("event:"):
                event = line[6:].strip()
            elif line.startswith("data:"):
                data += line[5:].strip()
        if not event or not data:
            continue
        payload = json.loads(data)
        if event in out:
            out[event].append(str(payload.get("data", "")))
        elif event == "exit":
            result.update(exit_code=payload.get("exit_code", -1), cwd=payload.get("cwd") or cwd,
                          duration_ms=payload.get("duration_ms"))
    result["stdout"] = "".join(out["stdout"])
    result["stderr"] = "".join(out["stderr"])
    return result


async def run_exec(daemon: AgentDaemon, body: dict[str, Any], *, timeout: float) -> dict[str, Any]:
    """``POST /exec`` for the sandbox proxy, run through the daemon's streaming exec."""
    import httpx

    request = {k: body[k] for k in ("command", "env", "stdin", "timeout") if body.get(k) is not None}
    request["cwd"] = body.get("cwd") or daemon.home
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(
            f"{daemon.base_url}/exec/stream", json=request,
            headers={"x-matrx-agent-token": daemon.token},
        )
    resp.raise_for_status()
    return parse_exec_stream(resp.text, cwd=request["cwd"])
