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
import contextlib
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
#: The machine's own services on its loopback — worker control (8002), the Selkies stream (8080)
#: and the agent daemon — which a port preview never opens (AI Dream's ``cloud_computer_preview``
#: reads this set too). The worker adds its configured ``BROWSER_WORKER_PORT``.
MACHINE_SERVICE_PORTS: frozenset[int] = frozenset({8002, 8080, AGENT_PORT})
#: Env the daemon must never inherit (its own replica would race ours).
_STRIPPED_ENV = ("MATRX_CLOUD_FILES_TOKEN", "MATRX_AIDREAM_SERVICE_TOKEN", "MATRX_AIDREAM_URL")

# ── git on the machine authenticates with the owner's GitHub (machines plan phase 3) ──
#: The vault-env name AI Dream pushes the owner's GitHub connection token under; the Vault's own
#: ``GITHUB_TOKEN`` is the fallback.
GIT_TOKEN_ENV = "MATRX_GITHUB_GIT_TOKEN"
#: Where the live token sits: tmpfs (memory), never the home (EFS, backed up). Replaced at every
#: vault push, removed when the push carries none, gone when the machine stops.
GIT_TOKEN_FILE = "/dev/shm/matrx-git/github-token"
#: The env-only credential helper for github.com (no file in the home, no value in the config):
#: every git the daemon runs — its git door, recipe clones, agent commands, the terminal — reads
#: the token file at the moment git asks.
GIT_CREDENTIAL_HELPER = (
    '!f() { test "$1" = get || exit 0; t=$(cat "$MATRX_GIT_TOKEN_FILE" 2>/dev/null) || exit 0; '
    'test -n "$t" || exit 0; echo username=x-access-token; echo "password=$t"; }; f'
)


# ── the terminal sees the owner's Vault too (machines plan 4b part 2) ──
#: tmpfs (memory) JSON of the owner's Vault env, rewritten at every vault push; the daemon's
#: ``/pty`` merges it into each new shell (``MATRX_AGENT_PTY_ENV_FILE``). Never the home.
PTY_ENV_FILE = "/dev/shm/matrx-vault/pty-env.json"


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
        #: The owner's Vault values AI Dream pushed at the last binding
        #: (``apply_vault_env``). Memory only — never the home (EFS, backed up),
        #: never a log line; merged into every agent ``exec``.
        self.vault_env: dict[str, str] = {}
        self.vault_version: str | None = None
        #: The tmpfs file git's credential helper reads (``GIT_TOKEN_FILE``).
        self.git_token_path = GIT_TOKEN_FILE
        #: The tmpfs file the daemon's terminal reads the Vault env from (``PTY_ENV_FILE``).
        self.pty_env_path = PTY_ENV_FILE
        self._proc: asyncio.subprocess.Process | None = None

    @property
    def available(self) -> bool:
        return os.access(self.python, os.X_OK)

    @property
    def base_url(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    async def wait_listening(self, timeout: float) -> bool:
        """True once the daemon accepts on its loopback port, False after ``timeout``.

        The worker answers ``/health`` before the daemon's uvicorn binds, so a wake's
        first agent call landed in that gap and got 503 (2026-11-01, task
        06d55a36: ``/health`` 200, then ``/agent/exec`` 503 0.2 s later). Every agent
        call waits here first; a daemon that is not installed answers at once."""
        if not self.available:
            return False
        loop = asyncio.get_running_loop()
        deadline = loop.time() + timeout
        while True:
            try:
                _, writer = await asyncio.open_connection("127.0.0.1", self.port)
            except OSError:
                if loop.time() >= deadline:
                    return False
                await asyncio.sleep(0.1)
                continue
            writer.close()
            with contextlib.suppress(Exception):
                await writer.wait_closed()
            return True

    def _env(self) -> dict[str, str]:
        env = {k: v for k, v in self.launch_env.items() if k not in _STRIPPED_ENV}
        env.update(
            MATRX_AGENT_TOKEN=self.token,
            MATRX_WORKSPACE_ROOT=self.home,
            HOT_PATH=self.home,
            HOME=self.home,
            MATRX_GIT_TOKEN_FILE=self.git_token_path,
            MATRX_AGENT_PTY_ENV_FILE=self.pty_env_path,
            GIT_CONFIG_COUNT="1",
            GIT_CONFIG_KEY_0="credential.https://github.com.helper",
            GIT_CONFIG_VALUE_0=GIT_CREDENTIAL_HELPER,
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
            # Names only, never a value.
            "vault_env_names": sorted(self.vault_env),
            "vault_version": self.vault_version,
        }


def write_git_token(path: str, token: str | None) -> None:
    """Put the live GitHub token where the credential helper reads it (tmpfs, 0600), or remove
    it. A failure is logged by name, never fatal: git then answers GitHub's own refusal."""
    try:
        if not token:
            if os.path.exists(path):
                os.remove(path)
            return
        os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
        tmp = f"{path}.{os.getpid()}.tmp"
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as handle:
            handle.write(token)
        os.replace(tmp, path)
    except OSError as exc:
        logger.error("git credential token not placed at %s: %s", path, type(exc).__name__)


def write_pty_env(path: str, env: Mapping[str, str]) -> None:
    """Put the owner's Vault env where a new terminal shell reads it (tmpfs JSON, 0600), or
    remove it when empty. A failure is logged by name, never fatal: the terminal then opens
    without the Vault (exec still carries it)."""
    import json

    try:
        if not env:
            if os.path.exists(path):
                os.remove(path)
            return
        os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
        tmp = f"{path}.{os.getpid()}.tmp"
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as handle:
            json.dump(dict(env), handle)
        os.replace(tmp, path)
    except OSError as exc:
        logger.error("terminal vault env not placed at %s: %s", path, type(exc).__name__)


def vault_version(env: Mapping[str, str]) -> str:
    """A digest of the whole name/value set; values hashed, never kept in it
    (the same digest the sandbox orchestrator stamps, ``vault_env_refresh``)."""
    import hashlib

    digest = hashlib.sha256()
    for name in sorted(env):
        digest.update(name.encode())
        digest.update(b"\0")
        digest.update(hashlib.sha256(env[name].encode()).digest())
    return digest.hexdigest()[:32]


def apply_vault_env(daemon: AgentDaemon, env: Mapping[str, Any]) -> dict[str, Any]:
    """Replace the machine's Vault env with ``env`` (the owner's vault truth at
    this binding). A name the vault no longer has leaves; a rotated value lands.
    Answers NAMES only — added, removed, present — never a value."""
    clean = {
        str(k): str(v) for k, v in env.items()
        if isinstance(k, str) and k and v is not None and k not in _STRIPPED_ENV
    }
    before = set(daemon.vault_env)
    daemon.vault_env = clean
    daemon.vault_version = vault_version(clean)
    write_git_token(daemon.git_token_path, clean.get(GIT_TOKEN_ENV) or clean.get("GITHUB_TOKEN"))
    write_pty_env(daemon.pty_env_path, clean)
    return {
        "added": sorted(set(clean) - before),
        "removed": sorted(before - set(clean)),
        "present": sorted(clean),
        "version": daemon.vault_version,
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


def daemon_refusal(resp: Any) -> str:
    """The daemon's own refusal sentence (FastAPI ``{"detail": ...}``), else its body."""
    try:
        detail = resp.json().get("detail")
    except (ValueError, AttributeError):
        detail = None
    if isinstance(detail, str) and detail:
        return detail
    return (resp.text or f"agent daemon answered {resp.status_code}")[:500]


async def run_exec(daemon: AgentDaemon, body: dict[str, Any], *, timeout: float) -> dict[str, Any]:
    """``POST /exec`` for the sandbox proxy, run through the daemon's streaming exec."""
    import httpx

    request = {k: body[k] for k in ("command", "env", "stdin", "timeout") if body.get(k) is not None}
    # The owner's Vault rides every command; a value the caller passed on purpose wins.
    caller_env = request.get("env") if isinstance(request.get("env"), dict) else {}
    if daemon.vault_env or caller_env:
        request["env"] = {**daemon.vault_env, **caller_env}
    request["cwd"] = body.get("cwd") or daemon.home
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(
            f"{daemon.base_url}/exec/stream", json=request,
            headers={"x-matrx-agent-token": daemon.token},
        )
    resp.raise_for_status()
    return parse_exec_stream(resp.text, cwd=request["cwd"])
