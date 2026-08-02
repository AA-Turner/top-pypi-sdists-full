"""Inspect installed binaries: presence, version, path."""

import re
import shutil
import subprocess
from dataclasses import dataclass

from ...common import winpath


@dataclass
class BinaryStatus:
    """State of a binary on the current machine."""

    name: str
    path: str = ""
    version: str = ""
    installed: bool = False

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "installed": self.installed,
            "path": self.path,
            "version": self.version,
        }


def which(name: str) -> str:
    """Return the absolute path to a binary, or '' if not found.

    On Windows, transparently merges the user-scope registry PATH into
    the process PATH on first use — winget-installed binaries from a
    previous run only sit in the registry, so a stale process PATH would
    make us think the binary is missing and re-trigger the install on
    every CLI invocation. The merge is cached per-process; ``which`` is
    free after the first call.
    """
    winpath.refresh_process_path_from_registry()
    return shutil.which(name) or ""


_VERSION_RE = re.compile(r"v?(\d+\.\d+(?:\.\d+)?)")


def extract_version(text: str) -> str:
    """Extract the first semver-like token from a string."""
    match = _VERSION_RE.search(text)
    return match.group(1) if match else ""


def get_version(name: str, version_arg: str = "--version", timeout: int = 5) -> str:
    """Run `<name> <version_arg>` and extract a semver from the output.

    ``version_arg`` is split on whitespace, so multi-flag invocations like
    ``"version --client=true"`` are supported.

    Returns '' if the binary is missing or the command fails.
    """
    binary = which(name)
    if not binary:
        return ""
    try:
        result = subprocess.run(
            [binary, *version_arg.split()],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return extract_version(result.stdout) or extract_version(result.stderr)


def status(name: str, version_arg: str = "--version", timeout: int = 5) -> BinaryStatus:
    """Full BinaryStatus for a named binary."""
    path = which(name)
    if not path:
        return BinaryStatus(name=name)
    return BinaryStatus(
        name=name,
        path=path,
        version=get_version(name, version_arg=version_arg, timeout=timeout),
        installed=True,
    )


def needs_update(current: str, latest: str) -> bool:
    """Return True when latest is at least one minor version ahead of current.

    Uses lexicographic comparison on tuples of int components. Missing
    components default to 0. Returns False if either string is unparseable.
    """
    if not current or not latest:
        return bool(latest)

    def parse(v: str) -> tuple[int, ...]:
        parts = v.lstrip("v").split(".")
        out: list[int] = []
        for part in parts:
            try:
                out.append(int(part.split("-")[0]))
            except ValueError:
                return ()
        return tuple(out)

    c = parse(current)
    l = parse(latest)  # noqa: E741
    if not c or not l:
        return False
    # Pad to same length
    n = max(len(c), len(l))
    c = c + (0,) * (n - len(c))
    l = l + (0,) * (n - len(l))  # noqa: E741
    return l > c
