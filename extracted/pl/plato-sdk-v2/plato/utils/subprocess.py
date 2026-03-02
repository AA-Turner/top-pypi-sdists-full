"""Shared SSH and subprocess helpers.

Consolidates duplicated SSH command building and subprocess execution
used across the runtime and CLI modules.
"""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

SSH_OPTS: list[tuple[str, str]] = [
    ("StrictHostKeyChecking", "no"),
    ("UserKnownHostsFile", "/dev/null"),
    ("LogLevel", "ERROR"),
]


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
    except asyncio.TimeoutError:
        proc.kill()
        raise RuntimeError(f"Command timed out after {timeout}s: {command[:100]}")
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
        escaped_cmd = command.replace("\\", "\\\\").replace('"', '\\"')
        command = f'su - {user} -c "{escaped_cmd}"'

    ssh_cmd = build_ssh_command(ssh_key, hostname, extra_opts=extra_opts)
    ssh_cmd.append(command)

    logger.debug(f"SSH running command as {user}: {command[:200]}...")

    proc = await asyncio.create_subprocess_exec(
        *ssh_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    except asyncio.TimeoutError:
        proc.kill()
        raise RuntimeError(f"SSH command timed out after {timeout}s: {command[:100]}")

    exit_code = proc.returncode or 0
    stdout_str = stdout.decode("utf-8", errors="replace")
    stderr_str = stderr.decode("utf-8", errors="replace")

    if exit_code != 0:
        logger.warning(f"SSH command failed: exit_code={exit_code}")
        if stdout_str:
            logger.warning(f"SSH stdout: {stdout_str}")
        if stderr_str:
            logger.warning(f"SSH stderr: {stderr_str}")
    else:
        logger.debug(f"SSH command finished: exit_code={exit_code}")

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
        escaped_cmd = command.replace("\\", "\\\\").replace('"', '\\"')
        command = f'su - {user} -c "{escaped_cmd}"'

    ssh_cmd = build_ssh_command(ssh_key, hostname, extra_opts=extra_opts)
    ssh_cmd.append(command)

    logger.debug(f"SSH streaming command as {user}: {command[:200]}...")

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
            output_lines.append(line.decode("utf-8", errors="replace").rstrip())

    await process.wait()

    exit_code = process.returncode or 0

    if output_lines and exit_code != 0:
        output_block = "\n".join(output_lines)
        logger.error(f"SSH output ({len(output_lines)} lines):\n{output_block}")

    logger.debug(f"SSH command finished: exit_code={exit_code}")
    return exit_code


def build_ssh_command(
    ssh_key: Path,
    hostname: str,
    extra_opts: list[tuple[str, str]] | None = None,
) -> list[str]:
    """Build an SSH command list with standard options.

    Args:
        ssh_key: Path to SSH private key.
        hostname: Remote hostname or IP.
        extra_opts: Additional SSH -o options (e.g., ProxyCommand).

    Returns:
        SSH command as a list of strings (without the remote command).
    """
    cmd = ["ssh", "-i", str(ssh_key)]
    all_opts = list(SSH_OPTS)
    if extra_opts:
        all_opts.extend(extra_opts)
    for name, value in all_opts:
        cmd.extend(["-o", f"{name}={value}"])
    cmd.append(f"root@{hostname}")
    return cmd
