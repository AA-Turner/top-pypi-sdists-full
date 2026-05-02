"""Run terminal commands (PowerShell/cmd) and return output."""

from __future__ import annotations

import asyncio
import sys

# Commands that should NEVER be executed
BLOCKED_COMMANDS = {
    # Destructive file operations
    "format",
    "del /s",
    "rm -rf",
    "rmdir /s",
    "del c:\\",
    "erase",
    "rd /s",
    # System modification
    "shutdown",
    "restart",
    "taskkill /f /im explorer",
    "reg delete",
    "reg add",
    "bcdedit",
    "diskpart",
    "sfc /scannow",
    "dism",
    # Network manipulation
    "netsh",
    "route add",
    "route delete",
    # Package/service manipulation
    "sc delete",
    "sc stop",
    "net stop",
    # PowerShell dangerous patterns
    "remove-item -recurse -force c:",
    "set-executionpolicy",
    "invoke-webrequest",
    "iwr",
    "wget",
    "curl",
}


def is_blocked(command: str) -> bool:
    """Check if a command is in the blocklist."""
    cmd_lower = command.lower().strip()
    return any(blocked in cmd_lower for blocked in BLOCKED_COMMANDS)


async def run_command(
    command: str,
    timeout: float = 30.0,
    cwd: str | None = None,
) -> dict[str, str | int | None]:
    """Execute a shell command and return structured output.

    Returns:
        {"stdout": str, "stderr": str, "returncode": int, "error": str | None}
    """
    if is_blocked(command):
        return {
            "stdout": "",
            "stderr": "",
            "returncode": -1,
            "error": f"Blocked command: {command}",
        }

    # Use PowerShell on Windows, bash on others
    if sys.platform == "win32":
        shell = ["powershell", "-NoProfile", "-Command", command]
    else:
        shell = ["bash", "-c", command]

    try:
        proc = await asyncio.create_subprocess_exec(
            *shell,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)

        return {
            "stdout": stdout.decode("utf-8", errors="replace").strip(),
            "stderr": stderr.decode("utf-8", errors="replace").strip(),
            "returncode": proc.returncode or 0,
            "error": None,
        }
    except TimeoutError:
        proc.kill()
        return {
            "stdout": "",
            "stderr": "",
            "returncode": -1,
            "error": f"Command timed out after {timeout}s",
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": "",
            "returncode": -1,
            "error": str(e),
        }
