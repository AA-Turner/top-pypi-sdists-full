"""System (OS-level) dependency provisioning, decoupled from tool installers.

A tool declares the OS dependencies it needs at run time via ``system_deps``
(a list of :class:`SystemDep`); the install framework ensures them **before** the
tool's own installer runs. This keeps OS dependencies — shared across tools
(several AppImages need libfuse2) and distro-specific — out of each tool's
``do_install``.

Every :class:`SystemDep` carries its own **probe** (a check that returns whether
the dependency is already satisfied). The probe is the guard used *before*
touching any package manager (skip if already present) and the verification used
*after* each install attempt (confirm it actually worked). It also decouples the
check from the install: the package that provides a dependency differs by distro
*and* release (e.g. Ubuntu 24.04+/Debian trixie renamed ``libfuse2`` →
``libfuse2t64``), so candidates are tried in order and each is verified via the
probe rather than trusting a package name.
"""

import shutil
import subprocess
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path

# Package-manager binary -> install command prefix, in preference order.
_MANAGERS: list[tuple[str, list[str]]] = [
    ("apt-get", ["sudo", "apt-get", "install", "-y"]),
    ("dnf", ["sudo", "dnf", "install", "-y"]),
    ("yum", ["sudo", "yum", "install", "-y"]),
    ("zypper", ["sudo", "zypper", "--non-interactive", "install"]),
    ("pacman", ["sudo", "pacman", "-S", "--noconfirm"]),
    ("apk", ["sudo", "apk", "add", "--no-cache"]),
]

_LIB_DIRS = (
    "/usr/lib/x86_64-linux-gnu",
    "/usr/lib/aarch64-linux-gnu",
    "/lib/x86_64-linux-gnu",
    "/usr/lib64",
    "/usr/lib",
    "/lib",
)


@dataclass(frozen=True)
class SystemDep:
    """An OS dependency, its per-manager candidate packages, and how to detect it.

    - ``name``: human label for reporting.
    - ``packages``: manager binary (``apt-get``, ``dnf``, …) -> ordered candidate
      package names to try for that manager.
    - ``probe``: returns ``True`` when the dependency is already satisfied. Called
      before any install (short-circuit) and after each candidate (verify).
    """

    name: str
    packages: dict[str, tuple[str, ...]]
    probe: Callable[[], bool]

    def present(self) -> bool:
        return self.probe()


def library_present(soname: str) -> bool:
    """Whether a shared library ``soname`` (e.g. ``libfuse.so.2``) is available."""
    try:
        r = subprocess.run(
            ["ldconfig", "-p"], capture_output=True, text=True, encoding="utf-8", errors="replace", check=False
        )
        if r.returncode == 0 and soname in (r.stdout or ""):
            return True
    except FileNotFoundError:
        pass
    return any((Path(d) / soname).exists() for d in _LIB_DIRS)


def library_dep(soname: str, packages: dict[str, tuple[str, ...]], label: str = "") -> SystemDep:
    """Build a :class:`SystemDep` for a shared library, probed via :func:`library_present`."""
    return SystemDep(name=label or soname, packages=packages, probe=lambda: library_present(soname))


def command_dep(command: str, packages: dict[str, tuple[str, ...]], label: str = "") -> SystemDep:
    """Build a :class:`SystemDep` for a CLI on PATH, probed via ``shutil.which``."""
    return SystemDep(name=label or command, packages=packages, probe=lambda: shutil.which(command) is not None)


def ensure_dep(dep: SystemDep) -> str:
    """Ensure ``dep`` is satisfied, reporting the outcome for the caller to act on.

    Returns ``present`` (probe already true — no package manager touched),
    ``installed`` (a candidate made the probe true), ``missing`` (a manager
    exists but no candidate satisfied the probe), or ``unsupported`` (no known
    package manager, or none has a candidate for this dep — e.g. macOS/Windows).
    The caller treats ``missing``/``unsupported`` as a hard failure.
    """
    if dep.present():
        return "present"
    manager = next(((name, cmd) for name, cmd in _MANAGERS if shutil.which(name)), None)
    if manager is None:
        return "unsupported"
    name, install_cmd = manager
    candidates = dep.packages.get(name)
    if not candidates:
        return "unsupported"
    if name == "apt-get":
        subprocess.run(
            ["sudo", "apt-get", "update"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdin=subprocess.DEVNULL,
            check=False,
        )
    for pkg in candidates:
        try:
            # stdin=DEVNULL so a sudo password prompt fails fast instead of hanging
            # invisibly (output is captured, so a prompt would never be seen).
            subprocess.run(
                [*install_cmd, pkg],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                stdin=subprocess.DEVNULL,
                check=False,
            )
        except FileNotFoundError:
            continue
        if dep.present():
            return "installed"
    return "missing"


def ensure_all(deps: Iterable[SystemDep]) -> dict[str, str]:
    """Ensure every declared dependency. Returns {name: status}."""
    return {dep.name: ensure_dep(dep) for dep in deps}


# --- Common, reusable dependencies -----------------------------------------

LIBFUSE2 = library_dep(
    "libfuse.so.2",
    {
        "apt-get": ("libfuse2t64", "libfuse2"),
        "dnf": ("fuse-libs",),
        "yum": ("fuse-libs",),
        "zypper": ("libfuse2",),
        "pacman": ("fuse2",),
        "apk": ("fuse",),
    },
    label="libfuse2",
)
