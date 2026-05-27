"""Shared SSH and subprocess helpers.

Consolidates duplicated SSH command building and subprocess execution
used across the runtime and CLI modules.
"""

from __future__ import annotations

import asyncio
import logging
import re
import shlex
from pathlib import Path

logger = logging.getLogger(__name__)

#: Shell snippet that sets PATH to include the pre-baked venv and common install
#: locations.  Use in any SSH command that needs to find SDK entry-points
#: (plato-agent-runner, plato-world-runner, plato-git-ops-server, etc.).
VM_PATH_EXPORT = 'export PATH="/opt/plato-venv/bin:/root/.local/bin:/usr/local/bin:$PATH"'

#: Canonical Python interpreter inside Plato world/agent VM images.
VM_VENV_PYTHON = "/opt/plato-venv/bin/python"


def _close_subprocess(proc: asyncio.subprocess.Process) -> None:
    """Explicitly close subprocess transport pipes to prevent 'Event loop is closed' noise.

    Python's asyncio subprocess transports print RuntimeError tracebacks to
    stderr when they're garbage-collected after the event loop closes. Closing
    the transport eagerly after wait() prevents this.
    """
    transport = getattr(proc, "_transport", None)
    if transport and not transport.is_closing():
        transport.close()


SSH_OPTS: list[tuple[str, str]] = [
    ("StrictHostKeyChecking", "no"),
    ("UserKnownHostsFile", "/dev/null"),
    ("LogLevel", "ERROR"),
    ("ConnectTimeout", "15"),
    ("ServerAliveInterval", "10"),
    ("ServerAliveCountMax", "3"),
    # Connection multiplexing: first SSH to a host opens a master socket,
    # subsequent calls reuse it (sub-100ms vs. full TCP+KEX+auth handshake).
    # Massive win when many agent installs/probes run in parallel.
    ("ControlMaster", "auto"),
    ("ControlPath", "/tmp/plato-ssh-%C"),
    ("ControlPersist", "60s"),
]


_SENSITIVE_ENV_KEY_PATTERN = re.compile(
    r"(?:token|secret|pass|password|key|credential|session|cookie|auth|aws)",
    re.IGNORECASE,
)
_ENV_ASSIGNMENT_PATTERN = re.compile(
    r"(?P<prefix>\bexport\s+)?(?P<key>[A-Za-z_][A-Za-z0-9_]*)=" r"(?P<value>'[^']*'|\"[^\"]*\"|[^\s;|&]+)"
)


def _sanitize_command_for_logs(command: str) -> str:
    """Redact sensitive env values before logging SSH commands."""

    def _replace(match: re.Match[str]) -> str:
        prefix = match.group("prefix") or ""
        key = match.group("key")
        value = match.group("value")
        if _SENSITIVE_ENV_KEY_PATTERN.search(key):
            return f"{prefix}{key}=<redacted>"
        return f"{prefix}{key}={value}"

    return _ENV_ASSIGNMENT_PATTERN.sub(_replace, command)


async def run_local(command: str, timeout: int = 60) -> tuple[int, str, str]:
    """Run a command locally as a subprocess."""
    proc = await asyncio.create_subprocess_exec(
        "bash",
        "-c",
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    except TimeoutError:
        try:
            proc.kill()
        except ProcessLookupError:
            pass  # Process already exited between timeout and kill
        await proc.wait()
        _close_subprocess(proc)
        raise RuntimeError(f"Command timed out after {timeout}s: {command[:100]}")
    _close_subprocess(proc)
    return proc.returncode or 0, stdout.decode(), stderr.decode()


async def run_ssh(
    ssh_key: Path,
    hostname: str,
    command: str,
    user: str = "root",
    timeout: int = 300,
    extra_opts: list[tuple[str, str]] | None = None,
) -> tuple[int, str, str]:
    """Run a command on a remote host via SSH and return (exit_code, stdout, stderr)."""
    if user != "root":
        command = f"sudo -u {shlex.quote(user)} -- bash -c {shlex.quote(command)}"
    ssh_cmd = build_ssh_command(ssh_key, hostname, extra_opts=extra_opts)
    ssh_cmd.append(command)
    log_command = _sanitize_command_for_logs(command)

    logger.debug("SSH running command on %s: %s", hostname, log_command)

    proc = await asyncio.create_subprocess_exec(
        *ssh_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    except TimeoutError:
        try:
            proc.kill()
        except ProcessLookupError:
            pass  # Process already exited between timeout and kill
        await proc.wait()
        _close_subprocess(proc)
        raise RuntimeError(f"SSH command timed out after {timeout}s: {command[:100]}")
    _close_subprocess(proc)

    exit_code = proc.returncode or 0
    stdout_str = stdout.decode("utf-8", errors="replace")
    stderr_str = stderr.decode("utf-8", errors="replace")

    if exit_code != 0:
        logger.warning(
            "SSH command failed on %s: exit_code=%s command=%s",
            hostname,
            exit_code,
            log_command,
        )
        if stdout_str:
            logger.warning(f"SSH stdout: {stdout_str}")
        if stderr_str:
            logger.warning(f"SSH stderr: {stderr_str}")
    else:
        logger.debug("SSH command finished on %s: exit_code=%s", hostname, exit_code)

    return exit_code, stdout_str, stderr_str


async def run_ssh_streaming(
    ssh_key: Path,
    hostname: str,
    command: str,
    user: str = "root",
    extra_opts: list[tuple[str, str]] | None = None,
) -> int:
    """Run a command via SSH with real-time output streaming. Returns exit code."""
    if user != "root":
        command = f"sudo -u {shlex.quote(user)} -- bash -c {shlex.quote(command)}"
    ssh_cmd = build_ssh_command(ssh_key, hostname, extra_opts=extra_opts)
    ssh_cmd.append(command)
    log_command = _sanitize_command_for_logs(command)

    logger.debug("SSH streaming command on %s: %s", hostname, log_command)

    process = await asyncio.create_subprocess_exec(
        *ssh_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )

    output_lines: list[str] = []
    if process.stdout:
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            decoded_line = line.decode("utf-8", errors="replace").rstrip()
            output_lines.append(decoded_line)

    await process.wait()
    _close_subprocess(process)

    exit_code = process.returncode or 0

    if output_lines and exit_code != 0:
        output_block = "\n".join(output_lines)
        logger.error(f"SSH output ({len(output_lines)} lines):\n{output_block}")

    logger.debug("SSH command finished on %s: exit_code=%s", hostname, exit_code)
    return exit_code


async def scp_content_to_vm(
    ssh_key: Path,
    hostname: str,
    remote_path: str,
    content: bytes,
    *,
    extra_opts: list[tuple[str, str]] | None = None,
    timeout: float = 30,
) -> None:
    """Write content to a remote file via scp.

    Writes content to a local temp file, scp's it to the VM, then cleans up.
    Avoids shell argument expansion that causes E2BIG with large payloads.
    """
    import tempfile

    cmd = ["scp", "-i", str(ssh_key)]
    all_opts = list(SSH_OPTS)
    if extra_opts:
        all_opts.extend(extra_opts)
    for name, value in all_opts:
        cmd.extend(["-o", f"{name}={value}"])

    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        tmp.write(content)
        tmp.flush()
        cmd.extend([tmp.name, f"root@{hostname}:{remote_path}"])
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            _, err = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except TimeoutError:
            try:
                proc.kill()
            except ProcessLookupError:
                pass
            await proc.wait()
            _close_subprocess(proc)
            raise RuntimeError(f"scp to {hostname}:{remote_path} timed out after {timeout}s")
        _close_subprocess(proc)
        if proc.returncode != 0:
            raise RuntimeError(f"scp to {hostname}:{remote_path} failed (exit {proc.returncode}): {err.decode()}")


def build_ssh_command(
    ssh_key: Path,
    hostname: str,
    extra_opts: list[tuple[str, str]] | None = None,
    *,
    multiplex: bool = True,
) -> list[str]:
    """Build an SSH command list with standard options.

    Args:
        ssh_key: Path to SSH private key.
        hostname: Remote hostname or IP.
        extra_opts: Additional SSH -o options (e.g., ProxyCommand).
        multiplex: If False, skip the ControlMaster/ControlPath/ControlPersist
            options. Required for long-lived foreground SSH commands like
            ``ssh -L … -N`` port forwards: with multiplexing on, the second
            and later SSH calls to a host hand their request to the master
            and exit immediately (rc=0), which makes the foreground process
            die before its caller can attach.

    Returns:
        SSH command as a list of strings (without the remote command).
    """
    cmd = ["ssh", "-i", str(ssh_key)]
    if multiplex:
        all_opts = list(SSH_OPTS)
    else:
        all_opts = [(name, value) for name, value in SSH_OPTS if not name.startswith("Control")]
    if extra_opts:
        all_opts.extend(extra_opts)
    for name, value in all_opts:
        cmd.extend(["-o", f"{name}={value}"])
    cmd.append(f"root@{hostname}")
    return cmd
