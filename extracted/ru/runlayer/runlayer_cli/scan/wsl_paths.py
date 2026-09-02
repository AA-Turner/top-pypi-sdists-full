"""Parse Windows-host WSL UNC paths without host-OS path semantics."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import PurePosixPath, PureWindowsPath


@dataclass(frozen=True)
class ParsedWSLPath:
    """Identity and Linux path represented by a WSL UNC path."""

    distro: str
    user: str | None
    linux_path: str


def parse_wsl_unc_path(
    value: str | os.PathLike[str] | None,
) -> ParsedWSLPath | None:
    """Parse ``\\wsl.localhost`` and legacy ``\\wsl$`` share paths.

    ``PureWindowsPath`` is intentional: scans and tests can inspect Windows UNC
    strings while running on any host OS. The WSL username is knowable only for
    paths rooted below ``/home/<user>``.
    """
    if value is None:
        return None

    try:
        raw_path = os.fspath(value)
    except TypeError:
        return None
    if isinstance(raw_path, bytes):
        raw_path = os.fsdecode(raw_path)

    windows_path = PureWindowsPath(raw_path)
    drive = windows_path.drive
    if not drive.startswith("\\\\"):
        return None

    share_parts = drive[2:].split("\\", maxsplit=1)
    if len(share_parts) != 2:
        return None
    server, distro = share_parts
    if server.casefold() not in {"wsl.localhost", "wsl$"} or not distro:
        return None

    relative_parts = windows_path.parts[1:]
    linux_path = PurePosixPath("/", *relative_parts).as_posix()
    user: str | None = None
    if relative_parts and relative_parts[0] == "root":
        user = "root"
    elif (
        len(relative_parts) >= 2
        and relative_parts[0] == "home"
        and relative_parts[1] not in {"", ".", ".."}
    ):
        user = relative_parts[1]
    return ParsedWSLPath(
        distro=distro,
        user=user,
        linux_path=linux_path,
    )
