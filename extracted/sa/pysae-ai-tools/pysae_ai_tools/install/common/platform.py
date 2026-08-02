"""Detect the current operating system and CPU architecture."""

import platform
from dataclasses import dataclass
from enum import StrEnum


class OS(StrEnum):
    LINUX = "linux"
    DARWIN = "darwin"
    WINDOWS = "windows"


class Arch(StrEnum):
    X86_64 = "x86_64"
    ARM64 = "arm64"


@dataclass(frozen=True)
class Platform:
    """Normalized platform identifier used by all install-* skills."""

    os: OS
    arch: Arch

    @property
    def os_capitalized(self) -> str:
        """OS with first letter capitalized (e.g. 'Linux', 'Darwin')."""
        return self.os.value.capitalize()

    @property
    def is_linux(self) -> bool:
        return self.os is OS.LINUX

    @property
    def is_macos(self) -> bool:
        return self.os is OS.DARWIN

    @property
    def is_windows(self) -> bool:
        return self.os is OS.WINDOWS

    def to_dict(self) -> dict[str, str]:
        return {"os": self.os.value, "arch": self.arch.value}


_OS_MAP: dict[str, OS] = {
    "linux": OS.LINUX,
    "darwin": OS.DARWIN,
    "windows": OS.WINDOWS,
}

_ARCH_MAP: dict[str, Arch] = {
    "x86_64": Arch.X86_64,
    "amd64": Arch.X86_64,
    "aarch64": Arch.ARM64,
    "arm64": Arch.ARM64,
}


def detect() -> Platform:
    """Detect the current platform.

    Raises ValueError on unsupported OS or architecture.
    """
    raw_os = platform.system().lower()
    raw_arch = platform.machine().lower()

    os = _OS_MAP.get(raw_os)
    if os is None:
        raise ValueError(f"Unsupported OS: {raw_os!r}")

    arch = _ARCH_MAP.get(raw_arch)
    if arch is None:
        raise ValueError(f"Unsupported architecture: {raw_arch!r}")

    return Platform(os=os, arch=arch)
