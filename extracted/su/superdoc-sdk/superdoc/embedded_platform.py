from __future__ import annotations

import os
import platform
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
    try:
        mode = os.stat(path).st_mode
        os.chmod(path, mode | 0o111)
    except OSError:
        pass
