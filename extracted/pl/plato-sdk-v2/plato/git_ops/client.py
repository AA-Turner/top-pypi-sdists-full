"""Typed remote client for git ops over a persistent SSH stdio session."""

from __future__ import annotations

import asyncio
from pathlib import Path

from plato.git_ops.models import GitOpRequest, GitOpResult
from plato.utils.subprocess import _close_subprocess, build_ssh_command


class RemoteGitClient:
    """Long-lived SSH-backed stdio client for git ops."""

    def __init__(self, ssh_key_path: Path, hostname: str) -> None:
        self._ssh_key_path = ssh_key_path
        self._hostname = hostname
        self._proc: asyncio.subprocess.Process | None = None
        self._lock = asyncio.Lock()
        self._stderr_task: asyncio.Task[None] | None = None
        self._stderr_lines: list[str] = []

    async def run(self, request: GitOpRequest, *, timeout: int) -> GitOpResult:
        async with self._lock:
            await self._ensure_started()
            proc = self._proc
            if proc is None or proc.stdin is None or proc.stdout is None:
                raise RuntimeError(f"Git ops server unavailable on {self._hostname}")
            proc.stdin.write(request.model_dump_json().encode("utf-8") + b"\n")
            await proc.stdin.drain()
            try:
                line = await asyncio.wait_for(proc.stdout.readline(), timeout=timeout)
            except asyncio.TimeoutError as exc:
                await self.close()
                raise RuntimeError(
                    f"Timed out waiting for git operation {request.operation} on {self._hostname}"
                ) from exc
            if not line:
                stderr = "\n".join(self._stderr_lines[-20:]).strip()
                await self.close()
                raise RuntimeError(stderr or f"Git ops server exited unexpectedly on {self._hostname}")
            return GitOpResult.model_validate_json(line.decode("utf-8"))

    async def close(self) -> None:
        proc = self._proc
        stderr_task = self._stderr_task
        self._proc = None
        self._stderr_task = None
        self._stderr_lines.clear()
        if proc is None:
            return
        if proc.stdin is not None:
            proc.stdin.close()
        if proc.returncode is None:
            proc.terminate()
            try:
                await asyncio.wait_for(proc.wait(), timeout=5)
            except asyncio.TimeoutError:
                proc.kill()
                await proc.wait()
        _close_subprocess(proc)
        if stderr_task is not None:
            try:
                await stderr_task
            except Exception:
                pass

    async def _ensure_started(self) -> None:
        if self._proc is not None and self._proc.returncode is None:
            return
        self._stderr_lines.clear()
        command = 'export PATH="/root/.local/bin:/usr/local/bin:$PATH"; exec plato-git-ops-server'
        ssh_cmd = build_ssh_command(self._ssh_key_path, self._hostname)
        ssh_cmd.append(command)
        self._proc = await asyncio.create_subprocess_exec(
            *ssh_cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        self._stderr_task = asyncio.create_task(self._consume_stderr())

    async def _consume_stderr(self) -> None:
        proc = self._proc
        if proc is None or proc.stderr is None:
            return
        while True:
            line = await proc.stderr.readline()
            if not line:
                return
            self._stderr_lines.append(line.decode("utf-8", errors="replace").rstrip())
            if len(self._stderr_lines) > 200:
                del self._stderr_lines[:100]
