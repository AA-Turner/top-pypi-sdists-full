"""Version-check helpers shared by CLI startup and explicit commands."""

from __future__ import annotations

import asyncio
import re
import sys
from dataclasses import dataclass
from enum import Enum
from string import Formatter

from packaging.version import InvalidVersion, Version

DEFAULT_UPDATE_CHECK_MESSAGE = "Update available: {current} -> {latest} -- pip install --upgrade anteroom"


class VersionCheckStatus(str, Enum):
    UPDATE_AVAILABLE = "update_available"
    CURRENT = "current"
    NOT_NEWER = "not_newer"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class VersionCheckResult:
    current: str
    latest: str | None
    status: VersionCheckStatus
    source: str
    reason: str | None = None


def format_update_message(template: str, current: str, latest: str) -> str:
    """Format the configured update message without allowing startup crashes."""
    if template == "":
        return ""

    values = {
        "current": current,
        "latest": latest,
        "upgrade_command": "pip install --upgrade anteroom",
    }
    try:
        for _, field_name, _, _ in Formatter().parse(template):
            if field_name and field_name not in values:
                return DEFAULT_UPDATE_CHECK_MESSAGE.format(**values)
        return template.format(**values)
    except Exception:
        return DEFAULT_UPDATE_CHECK_MESSAGE.format(**values)


def _first_non_empty_line(output: str) -> str:
    for line in output.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _parse_latest_version(output: str, *, command: str) -> str | None:
    if command:
        return _first_non_empty_line(output)

    match = re.search(r"anteroom\s*\(([^)]+)\)", output)
    if not match:
        return None
    return match.group(1).strip()


async def check_for_update(current: str, *, command: str = "", timeout: float = 5.0) -> VersionCheckResult:
    """Check for a newer Anteroom version.

    Failures return ``UNAVAILABLE`` rather than pretending the installed
    version is current. Startup callers can stay silent on that status, while
    explicit commands can report it confidently.
    """
    source = "custom command" if command else "pip index"
    proc = None
    try:
        if command:
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        else:
            proc = await asyncio.create_subprocess_exec(
                sys.executable,
                "-m",
                "pip",
                "index",
                "versions",
                "anteroom",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

        try:
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except TimeoutError:
            if proc.returncode is None:
                proc.kill()
                await proc.wait()
            return VersionCheckResult(current, None, VersionCheckStatus.UNAVAILABLE, source, "check timed out")

        if proc.returncode != 0:
            return VersionCheckResult(current, None, VersionCheckStatus.UNAVAILABLE, source, "checker exited non-zero")

        latest = _parse_latest_version(stdout.decode(errors="replace").strip(), command=command)
        if not latest:
            return VersionCheckResult(
                current,
                None,
                VersionCheckStatus.UNAVAILABLE,
                source,
                "checker returned no version",
            )

        try:
            latest_version = Version(latest)
            current_version = Version(current)
        except InvalidVersion:
            return VersionCheckResult(
                current,
                latest,
                VersionCheckStatus.UNAVAILABLE,
                source,
                "checker returned invalid version",
            )

        if latest_version > current_version:
            return VersionCheckResult(current, latest, VersionCheckStatus.UPDATE_AVAILABLE, source)
        if latest_version == current_version:
            return VersionCheckResult(current, latest, VersionCheckStatus.CURRENT, source)
        return VersionCheckResult(current, latest, VersionCheckStatus.NOT_NEWER, source)
    except Exception as exc:
        if proc and proc.returncode is None:
            try:
                proc.kill()
                await proc.wait()
            except Exception:
                pass
        return VersionCheckResult(current, None, VersionCheckStatus.UNAVAILABLE, source, type(exc).__name__)
