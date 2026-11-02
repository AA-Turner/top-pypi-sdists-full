"""Install a robot's optional dependency bundle the first time its setup runs.

`dreamscale robots <robot> setup` calls `ensure_extras` before touching hardware, so a
plain `pip install dreamscale` (or `uv tool install dreamscale`) is the whole install
story. Requirements come from dreamscale's own package metadata, the installer matches
how dreamscale itself was installed, and the command re-executes once the new packages
are in place so they import cleanly.
"""

from __future__ import annotations

import importlib.util
import json
import os
import platform
import re
import shlex
import shutil
import subprocess
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path

from packaging.requirements import InvalidRequirement, Requirement

from dreamscale import errors

DISTRIBUTION = "dreamscale"
# Set across the re-exec so a still-missing dependency fails instead of looping.
REEXEC_ENV = "DREAMSCALE_EXTRAS_INSTALLED"

# Python ranges narrower than the SDK's own, as [low, high). LeRobot 0.6.1 requires
# 3.12 and its dependency stack has no 3.14 wheels yet; pyrealsense2 stops at 3.13 (not
# on aarch64 Linux, where dreamscale-pyrealsense2 covers every SDK Python), hud at 3.12.
_PYTHON_RANGE: dict[str, tuple[tuple[int, int], tuple[int, int]]] = {
    "so101": ((3, 12), (3, 14)),
    "realsense": ((3, 9), (3, 14)),
    "hud": ((3, 11), (3, 13)),
}
# Where a uv tool install moves when its Python is out of range: the version each
# stack is qualified on, if it fits every extra; otherwise the range's oldest Python.
_PYTHON_TARGET: dict[str, tuple[int, int]] = {
    "so101": (3, 12),
    "realsense": (3, 13),
}
# Commands an extra's package provides that a uv tool install should put on PATH too.
_TOOL_EXECUTABLES: dict[str, str] = {
    "inspect-robots": "inspect-robots",
}

_REQUIREMENT = re.compile(
    r"^\s*(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)\s*(?:\[(?P<extras>[^\]]*)\])?"
    r"\s*(?P<spec>[^;]*?)\s*(?:;\s*(?P<marker>.*))?$"
)
_EXTRA_MARKER = re.compile(r"""extra\s*==\s*['"]([^'"]+)['"]""")


@dataclass(frozen=True)
class InstallPlan:
    command: list[str]
    cwd: Path | None = None


def so101_extras() -> list[str]:
    return ["so101"]


def yam_extras() -> list[str]:
    """YAM driver and cameras, plus RealSense wherever it can be installed."""
    extras = ["yam", "cameras"]
    if realsense_installable():
        extras.append("realsense")
    return extras


def franka_extras() -> list[str]:
    """franky (libfranka in C++) and cameras, plus RealSense wherever it can be installed."""
    extras = ["franka", "cameras"]
    if realsense_installable():
        extras.append("realsense")
    return extras


def ur_extras() -> list[str]:
    """ur_rtde (RTDE and External Control) and cameras, plus RealSense wherever it can be
    installed."""
    extras = ["ur", "cameras"]
    if realsense_installable():
        extras.append("realsense")
    return extras


def xarm7_extras() -> list[str]:
    """xarm-python-sdk and cameras, plus RealSense wherever it can be installed."""
    extras = ["xarm7", "cameras"]
    if realsense_installable():
        extras.append("realsense")
    return extras


def realsense_installable() -> bool:
    """A RealSense wheel exists for this Python, or a uv tool install can move to one.

    pyrealsense2's wheels cover x86_64 Linux and Windows, up to Python 3.13. On aarch64
    Linux the extra installs dreamscale-pyrealsense2, built for every SDK Python.
    """
    if _rsusb_platform():
        return True
    if sys.platform not in {"linux", "win32"}:
        return False
    if platform.machine().lower() not in {"x86_64", "amd64"}:
        return False
    return sys.version_info[:2] < _PYTHON_RANGE["realsense"][1] or _uv_tool()


def _rsusb_platform() -> bool:
    """aarch64 Linux, where the realsense extra installs dreamscale-pyrealsense2."""
    return sys.platform == "linux" and platform.machine() == "aarch64"


def _uv_tool() -> bool:
    return (Path(sys.prefix) / "uv-receipt.toml").exists()


def missing_requirements(extras: Sequence[str]) -> list[str]:
    """Requirements of `extras` that are absent or off their exact pin."""
    missing: list[str] = []
    for extra in extras:
        for requirement in _requirements(DISTRIBUTION, extra):
            if not _satisfied(requirement) and requirement not in missing:
                missing.append(requirement)
    return missing


def installed_extras() -> list[str]:
    """Extras whose requirements are all present, so a reinstall keeps them."""
    try:
        provided = metadata.metadata(DISTRIBUTION).get_all("Provides-Extra") or []
    except metadata.PackageNotFoundError:
        return []
    return [
        extra for extra in provided
        if _requirements(DISTRIBUTION, extra) and not missing_requirements([extra])
    ]


def ensure_extras(
    extras: Sequence[str],
    *,
    label: str,
    setup_command: str,
    print_fn: Callable[[str], None] = print,
    run: Callable[..., subprocess.CompletedProcess] = subprocess.run,
    execv: Callable[[str, list[str]], object] = os.execv,
) -> None:
    """Install whatever `extras` still needs, then restart the current command."""
    if not missing_requirements(extras):
        return
    if os.environ.get(REEXEC_ENV):
        raise errors.catalog(
            "extra_install_failed",
            label=label,
            command=_manual_command(extras),
            detail="the install finished but the packages still do not import here",
            retry_command=setup_command,
        )
    plan = install_plan(extras, label=label, setup_command=setup_command)
    print_fn(f"Installing {label} support (one time): {shlex.join(plan.command)}")
    result = run(plan.command, cwd=plan.cwd, check=False)
    if result.returncode:
        raise errors.catalog(
            "extra_install_failed",
            label=label,
            command=shlex.join(plan.command),
            detail=f"the installer exited with status {result.returncode} (output above)",
            retry_command=setup_command,
        )
    print_fn(f"✓ {label} support installed")
    sys.stdout.flush()
    os.environ[REEXEC_ENV] = "1"
    execv(sys.executable, [sys.executable, *sys.orig_argv[1:]])


def install_plan(extras: Sequence[str], *, label: str, setup_command: str) -> InstallPlan:
    """The command that adds `extras` to the environment running dreamscale."""
    version = metadata.version(DISTRIBUTION)
    prefix = Path(sys.prefix)
    current = sys.version_info[:2]
    python = _python_for(extras, current)

    if _uv_tool():
        # `uv tool install --force` rebuilds the tool environment from its arguments, so
        # name every extra this install already has, and pick a Python that suits all of
        # them. A lower bound, not an exact pin, so `uv tool upgrade dreamscale` works.
        merged = _merge(installed_extras(), extras)
        python = _python_for(merged, current)
        executables = [
            arg for extra in merged if extra in _TOOL_EXECUTABLES
            for arg in ("--with-executables-from", _TOOL_EXECUTABLES[extra])
        ]
        return InstallPlan([
            _require_uv(extras, label), "tool", "install", "--force",
            "--python", ".".join(map(str, python or current)),
            *executables,
            f"{DISTRIBUTION}[{','.join(merged)}]>={version}",
        ])

    if python is not None:
        raise errors.catalog(
            "extra_python_unsupported",
            label=label,
            python_version=platform.python_version(),
            supported=_describe_range(extras),
            command=_tool_command(extras, version, python),
            retry_command=setup_command,
        )

    source = _editable_source()
    if source is not None:
        return InstallPlan(_pip_install(extras, label, "-e", f"{source}[{','.join(extras)}]"))

    project = prefix.parent
    if (
        prefix.name == ".venv"
        and (project / "pyproject.toml").exists()
        and (project / "uv.lock").exists()
        and _uv() is not None
    ):
        # A `uv pip install` here would vanish on the next `uv sync`; record it instead.
        merged = _merge(installed_extras(), extras)
        return InstallPlan(
            [_uv(), "add", f"{DISTRIBUTION}[{','.join(merged)}]=={version}"],
            cwd=project,
        )

    return InstallPlan(
        _pip_install(extras, label, f"{DISTRIBUTION}[{','.join(extras)}]=={version}")
    )


def _requirements(distribution: str, extra: str) -> list[str]:
    """`extra`'s requirements that apply to this platform, without their markers."""
    try:
        requires = metadata.requires(distribution) or []
    except metadata.PackageNotFoundError:
        return []
    return [
        requirement.split(";", 1)[0].strip()
        for requirement in requires
        if extra in _EXTRA_MARKER.findall(requirement.partition(";")[2])
        and _applies(requirement, extra)
    ]


def _applies(requirement: str, extra: str) -> bool:
    try:
        marker = Requirement(requirement).marker
    except InvalidRequirement:
        return True
    # This module's view of the platform, so tests can stand in for another one.
    return marker is None or marker.evaluate({
        "extra": extra, "sys_platform": sys.platform, "platform_machine": platform.machine(),
    })


def _satisfied(requirement: str) -> bool:
    match = _REQUIREMENT.match(requirement)
    if match is None:
        return False
    name, spec = match["name"], match["spec"].replace(" ", "")
    try:
        version = metadata.version(name)
    except metadata.PackageNotFoundError:
        return False
    if spec.startswith("==") and "," not in spec and "*" not in spec:
        if version != spec[2:]:
            return False
    # One level of nested extras, e.g. `lerobot[feetech]` needs the Feetech SDK.
    nested = [extra.strip() for extra in (match["extras"] or "").split(",") if extra.strip()]
    return all(
        _installed(inner)
        for extra in nested
        for inner in _requirements(name, extra)
    )


def _installed(requirement: str) -> bool:
    match = _REQUIREMENT.match(requirement)
    if match is None:
        return False
    try:
        metadata.version(match["name"])
    except metadata.PackageNotFoundError:
        return False
    return True


def _python_for(extras: Sequence[str], current: tuple[int, int]) -> tuple[int, int] | None:
    """None when `current` suits every extra, else the Python to move to."""
    low, high = _range(extras)
    if low <= current < high:
        return None
    targets = [
        target for extra in extras
        if (target := _PYTHON_TARGET.get(extra)) is not None and low <= target < high
    ]
    return min(targets) if targets else low


def _range(extras: Sequence[str]) -> tuple[tuple[int, int], tuple[int, int]]:
    low, high = (3, 0), (4, 0)
    for extra in extras:
        if extra in _PYTHON_RANGE and not (extra == "realsense" and _rsusb_platform()):
            extra_low, extra_high = _PYTHON_RANGE[extra]
            low, high = max(low, extra_low), min(high, extra_high)
    return low, high


def _describe_range(extras: Sequence[str]) -> str:
    (low_major, low_minor), (high_major, high_minor) = _range(extras)
    last = f"{high_major}.{high_minor - 1}" if high_minor else f"{high_major - 1}.x"
    return f"Python {low_major}.{low_minor} through {last}"


def _merge(installed: Sequence[str], requested: Sequence[str]) -> list[str]:
    return sorted({*installed, *requested})


def _editable_source() -> Path | None:
    try:
        raw = metadata.distribution(DISTRIBUTION).read_text("direct_url.json")
    except metadata.PackageNotFoundError:
        return None
    try:
        direct = json.loads(raw or "{}")
    except ValueError:
        return None
    url = direct.get("url", "")
    if not direct.get("dir_info", {}).get("editable") or not url.startswith("file://"):
        return None
    return Path(url.removeprefix("file://"))


def _uv() -> str | None:
    """uv from $UV or PATH, else where uv's installer puts it: a uv tool install often
    runs from a shell whose PATH lacks ~/.local/bin (ssh, cron, systemd)."""
    found = os.environ.get("UV") or shutil.which("uv")
    if found:
        return found
    home = Path.home()
    candidates = [
        os.environ.get("UV_INSTALL_DIR"), os.environ.get("XDG_BIN_HOME"),
        home / ".local" / "bin", home / ".cargo" / "bin",
    ]
    for directory in filter(None, candidates):
        uv = Path(directory) / "uv"
        if uv.is_file() and os.access(uv, os.X_OK):
            return str(uv)
    return None


def _require_uv(extras: Sequence[str], label: str) -> str:
    uv = _uv()
    if uv is None:
        raise errors.catalog(
            "extra_install_failed",
            label=label,
            command=_manual_command(extras),
            detail="this uv tool install needs `uv` on PATH to add packages",
        )
    return uv


def _pip_install(extras: Sequence[str], label: str, *args: str) -> list[str]:
    uv = _uv()
    if uv is not None:
        return [uv, "pip", "install", "--python", sys.executable, *args]
    if importlib.util.find_spec("pip") is not None:
        return [sys.executable, "-m", "pip", "install", *args]
    raise errors.catalog(
        "extra_install_failed",
        label=label,
        command=_manual_command(extras),
        detail="this environment has neither uv nor pip to install packages with",
    )


def _tool_command(extras: Sequence[str], version: str, python: tuple[int, int]) -> str:
    return (
        f'uv tool install --python {python[0]}.{python[1]} '
        f'"{DISTRIBUTION}[{",".join(extras)}]>={version}"'
    )


def _manual_command(extras: Sequence[str]) -> str:
    try:
        version = metadata.version(DISTRIBUTION)
    except metadata.PackageNotFoundError:
        version = ""
    pin = f"=={version}" if version else ""
    return f'uv pip install "{DISTRIBUTION}[{",".join(extras)}]{pin}"'
