"""uv, which locks the project: the Dockerfile builds from `uv.lock`, so the first commit must carry it."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

INSTALL_DOCS_URL = "https://docs.astral.sh/uv/getting-started/installation/"


class UvError(Exception):
    """A uv command failed. `output` is what it printed."""

    def __init__(self, message: str, output: str = "") -> None:
        super().__init__(message)
        self.output = output


def find() -> str | None:
    return shutil.which("uv")


def install_command() -> list[str]:
    """Astral's installer, as https://docs.astral.sh/uv/getting-started/installation/ gives it."""
    if sys.platform == "win32":
        return [
            "powershell",
            "-ExecutionPolicy",
            "ByPass",
            "-c",
            "irm https://astral.sh/uv/install.ps1 | iex",
        ]
    return ["sh", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"]


def install() -> str:
    """Install uv with Astral's installer, and return its path.

    The installer adds its folder to the PATH of new shells, not of this process, so uv is looked up where
    the installer puts it.
    """
    try:
        completed = subprocess.run(install_command(), check=False)  # noqa: S603 - a fixed command
    except OSError as exc:
        raise UvError(f"Could not run the uv installer: {exc}") from exc
    if completed.returncode != 0:
        raise UvError(f"The uv installer failed (exit code {completed.returncode}).")
    found = find() or next((str(path) for path in _install_locations() if path.is_file()), None)
    if found is None:
        raise UvError(
            "The uv installer finished, but uv was not found. Open a new terminal and run `agents init` again."
        )
    return found


def _install_locations() -> list[Path]:
    # Where the installer puts uv, in its order: UV_INSTALL_DIR, then XDG_BIN_HOME, then ~/.local/bin.
    executable = "uv.exe" if sys.platform == "win32" else "uv"
    folders = [os.environ.get("UV_INSTALL_DIR"), os.environ.get("XDG_BIN_HOME")]
    candidates = [Path(folder) for folder in folders if folder]
    candidates.append(Path.home() / ".local" / "bin")
    return [folder / executable for folder in candidates]


def lock(folder: Path, uv: str) -> None:
    """Write the project's `uv.lock`."""
    try:
        completed = subprocess.run(  # noqa: S603 - uv, found on the PATH or just installed
            [uv, "lock", "--directory", str(folder)],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        raise UvError(f"Could not run uv: {exc}") from exc
    if completed.returncode != 0:
        raise UvError("`uv lock` failed.", output=(completed.stderr or completed.stdout).strip())
