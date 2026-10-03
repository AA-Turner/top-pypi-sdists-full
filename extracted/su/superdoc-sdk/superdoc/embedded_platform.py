from __future__ import annotations

import os
import platform
import stat
from importlib import resources
from pathlib import Path
from typing import Optional


TARGET_TO_COMPANION_MODULE = {
    'darwin-arm64': 'superdoc_sdk_cli_darwin_arm64',
    'darwin-x64': 'superdoc_sdk_cli_darwin_x64',
    'linux-x64': 'superdoc_sdk_cli_linux_x64',
    'linux-arm64': 'superdoc_sdk_cli_linux_arm64',
    'windows-x64': 'superdoc_sdk_cli_windows_x64',
}


def _normalized_machine(value: str) -> str:
    normalized = value.strip().lower()
    if normalized in {'x86_64', 'amd64'}:
        return 'x64'
    if normalized in {'aarch64', 'arm64'}:
        return 'arm64'
    return normalized


def resolve_embedded_target() -> Optional[str]:
    system = platform.system().lower()
    machine = _normalized_machine(platform.machine())

    if system == 'darwin' and machine == 'arm64':
        return 'darwin-arm64'
    if system == 'darwin' and machine == 'x64':
        return 'darwin-x64'
    if system == 'linux' and machine == 'x64':
        return 'linux-x64'
    if system == 'linux' and machine == 'arm64':
        return 'linux-arm64'
    if system == 'windows' and machine == 'x64':
        return 'windows-x64'

    return None


def resolve_companion_binary(target: str, binary_name: str) -> Optional[str]:
    module_name = TARGET_TO_COMPANION_MODULE.get(target)
    if module_name is None:
        return None

    try:
        module = __import__(module_name)
        binary = resources.files(module).joinpath('bin', binary_name)
        path = Path(str(binary))
    except (ImportError, FileNotFoundError, ModuleNotFoundError):
        return None

    return str(path) if path.is_file() else None


def ensure_executable(path: str) -> None:
    if os.name == 'nt':
        return
    # AIDEV-NOTE: Never chmod a binary this process can already execute. Every
    # client construction lands here, and on overlayfs any metadata write to a
    # file in a read-only image layer copies the whole binary (over 100 MB)
    # into the container layer. Mirrors ensureEmbeddedExecutable in the Node SDK.
    if os.access(path, os.X_OK):
        return
    try:
        mode = stat.S_IMODE(os.stat(path).st_mode) | 0o111
    except OSError:
        # Unreadable mode is not a reason to skip the repair.
        mode = 0o755
    try:
        os.chmod(path, mode)
    except OSError:
        # Non-fatal: launching the host reports the actionable error.
        pass
