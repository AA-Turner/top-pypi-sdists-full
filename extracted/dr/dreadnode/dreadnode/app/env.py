"""Runtime env var resolution with deprecation warnings for legacy names.

Centralizes reads of the ``DREADNODE_RUNTIME_*`` family so legacy aliases (which
collided with the platform ``DREADNODE_SERVER`` var or lived under the narrow
``SANDBOX_`` prefix) can be honored during the deprecation window without
duplicating warning bookkeeping at every call site.
"""

import os
import platform
import shutil
import subprocess
import sys
import threading
import typing as t
import warnings
from pathlib import Path

from loguru import logger

__all__ = [
    "read_env_with_deprecation",
    "resolve_python_executable",
]

_ALREADY_WARNED: set[str] = set()
# Guard the check-then-add on ``_ALREADY_WARNED`` so concurrent threads
# racing on startup (SDK + TUI + worker manager) still produce exactly one
# warning per legacy name.
_WARN_LOCK = threading.Lock()


def resolve_python_executable() -> str:
    """Resolve the Python executable for dreadnode, never using sys.executable.

    Finds the correct Python that has dreadnode SDK installed by checking:
    1. Dreadnode installation paths
    2. UV tool environments
    3. Virtual environments
    4. PATH with validation

    Returns:
        Path to the Python executable that should be used for subprocess execution.

    Raises:
        ValueError: If no Python with dreadnode SDK is found.
    """
    # 1. Try dreadnode installation detection
    installation_python = _get_dreadnode_installation_python()
    if installation_python and _validate_python_has_dreadnode(installation_python):
        logger.debug(f"Using dreadnode installation Python: {installation_python}")
        return installation_python

    # 2. Try UV tool environment
    uv_python = _get_uv_tool_python()
    if uv_python and _validate_python_has_dreadnode(uv_python):
        logger.debug(f"Using UV tool Python: {uv_python}")
        return uv_python

    # 3. Try virtual environment
    venv_python = _get_venv_python()
    if venv_python and _validate_python_has_dreadnode(venv_python):
        logger.debug(f"Using virtual environment Python: {venv_python}")
        return venv_python

    # 4. Try PATH with validation
    for python_name in ["python3", "python"]:
        python_from_path = shutil.which(python_name)
        if python_from_path and _validate_python_has_dreadnode(python_from_path):
            logger.debug(f"Using PATH Python: {python_from_path}")
            return python_from_path

    # 5. FAIL FAST - no sys.executable fallback
    raise ValueError(
        "Dreadnode installation not found. No Python executable found with dreadnode SDK installed. "
        "Please install following the documentation: https://docs.dreadnode.io/getting-started/quickstart/"
    )


def _get_platform_uv_tool_paths() -> list[Path]:
    """Get platform-specific UV tool installation paths for dreadnode."""
    paths = []

    if platform.system() == "Windows":
        # Windows UV tool paths
        if os.environ.get("LOCALAPPDATA"):
            paths.append(
                Path(os.environ["LOCALAPPDATA"])
                / "uv"
                / "tools"
                / "dreadnode"
                / "Scripts"
                / "python.exe"
            )
        if os.environ.get("APPDATA"):
            paths.append(
                Path(os.environ["APPDATA"])
                / "uv"
                / "tools"
                / "dreadnode"
                / "Scripts"
                / "python.exe"
            )
        # Fallback for Windows with Unix-style paths (WSL, Git Bash, etc.)
        paths.append(
            Path.home()
            / ".local"
            / "share"
            / "uv"
            / "tools"
            / "dreadnode"
            / "Scripts"
            / "python.exe"
        )
    else:
        # Unix-like systems (Linux, macOS)
        paths.extend(
            [
                Path.home() / ".local" / "share" / "uv" / "tools" / "dreadnode" / "bin" / "python3",
                Path.home() / ".local" / "share" / "uv" / "tools" / "dreadnode" / "bin" / "python",
            ]
        )

    return paths


def _get_dreadnode_installation_python() -> str | None:
    """Find Python from dreadnode installation directory."""
    # Method 1: Derive from current executable location
    current_executable = sys.argv[0]
    if current_executable:
        executable_path = Path(current_executable).resolve()

        # UV tool pattern: ~/.local/share/uv/tools/dreadnode/bin/dreadnode
        if "uv/tools/dreadnode" in str(executable_path):
            # UV tool installation - Python is in same directory
            if platform.system() == "Windows":
                potential_python = executable_path.parent / "python.exe"
            else:
                potential_python = executable_path.parent / "python3"
            if potential_python.exists():
                return str(potential_python)
            if platform.system() != "Windows":
                potential_python = executable_path.parent / "python"
                if potential_python.exists():
                    return str(potential_python)

        # Check for other common installation patterns:
        # ~/.local/bin/dn -> ~/.local/bin/python3
        # ~/.dreadnode/bin/dn -> ~/.dreadnode/bin/python3
        # /usr/local/bin/dn -> /usr/local/bin/python3
        if platform.system() == "Windows":
            potential_python = executable_path.parent / "python.exe"
        else:
            potential_python = executable_path.parent / "python3"
        if potential_python.exists():
            return str(potential_python)

    # Method 2: Check standard installation locations
    installation_paths = []

    # UV tool installation (highest priority) - platform-aware
    installation_paths.extend(_get_platform_uv_tool_paths())

    # Other standard locations
    if platform.system() == "Windows":
        installation_paths.extend(
            [
                Path.home() / ".dreadnode" / "Scripts" / "python.exe",
                Path.home() / "AppData" / "Local" / "Programs" / "Python" / "python.exe",
            ]
        )
    else:
        installation_paths.extend(
            [
                Path.home() / ".dreadnode" / "bin" / "python3",
                Path.home() / ".local" / "bin" / "python3",
                Path("/usr/local/bin/python3"),
            ]
        )

    for python_path in installation_paths:
        if python_path.exists():
            return str(python_path)

    return None


def _get_uv_tool_python() -> str | None:
    """Find Python from UV tool installation."""
    # Check if current executable is in a UV tool path
    current_executable = sys.argv[0]
    if current_executable:
        executable_path = Path(current_executable).resolve()

        # UV tool pattern: ~/.local/share/uv/tools/dreadnode/bin/dreadnode
        if "uv/tools" in str(executable_path):
            # Extract the tool directory and find Python
            tool_parts = str(executable_path).split("uv/tools/")
            if len(tool_parts) == 2:
                tool_base = tool_parts[0] + "uv/tools/" + tool_parts[1].split("/")[0]
                if platform.system() == "Windows":
                    uv_python = Path(tool_base) / "Scripts" / "python.exe"
                    if uv_python.exists():
                        return str(uv_python)
                else:
                    uv_python = Path(tool_base) / "bin" / "python3"
                    if uv_python.exists():
                        return str(uv_python)
                    # Try without the '3' suffix
                    uv_python = Path(tool_base) / "bin" / "python"
                    if uv_python.exists():
                        return str(uv_python)

    # Fallback: check platform-specific standard UV tool locations for dreadnode
    platform_paths = _get_platform_uv_tool_paths()
    for python_path in platform_paths:
        if python_path.exists():
            return str(python_path)

    return None


def _get_venv_python() -> str | None:
    """Find Python from virtual environment."""
    virtual_env = os.environ.get("VIRTUAL_ENV")
    if virtual_env:
        venv_python = Path(virtual_env) / "bin" / "python3"
        if venv_python.exists():
            return str(venv_python)

    return None


def _validate_python_has_dreadnode(python_path: str) -> bool:
    """Verify this Python can import dreadnode SDK."""
    try:
        result = subprocess.run(  # noqa: S603
            [python_path, "-c", "import dreadnode; import dreadnode.app; print('OK')"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,  # We handle returncode ourselves
        )
        if result.returncode == 0 and "OK" in result.stdout:
            return True
    except Exception as e:
        logger.debug(f"Python validation failed for {python_path}: {e}")
    return False


@t.overload
def read_env_with_deprecation(canonical: str, legacy: str) -> str | None: ...


@t.overload
def read_env_with_deprecation(canonical: str, legacy: str, default: str) -> str: ...


def read_env_with_deprecation(
    canonical: str,
    legacy: str,
    default: str | None = None,
) -> str | None:
    """Return the value of ``canonical`` if set, else ``legacy`` (warning once), else ``default``.

    The ``DeprecationWarning`` fires at most once per legacy name per process,
    so repeated reads during startup don't flood logs. The mirrored
    ``logger.warning`` ensures the message is visible even when warnings are
    filtered out of the user's environment.
    """
    canonical_value = os.environ.get(canonical)
    if canonical_value is not None:
        return canonical_value

    legacy_value = os.environ.get(legacy)
    if legacy_value is not None:
        with _WARN_LOCK:
            should_warn = legacy not in _ALREADY_WARNED
            if should_warn:
                _ALREADY_WARNED.add(legacy)
        if should_warn:
            msg = (
                f"{legacy} is deprecated and will be removed in a future release. "
                f"Use {canonical} instead."
            )
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            logger.warning(msg)
        return legacy_value

    return default
