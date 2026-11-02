"""read the release manifest as tauri-plugin-updater does: semver compare, targets, this machine's entry."""

from __future__ import annotations
import contextlib
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from probe.service.updater.app.errors import InstallError


def supported() -> bool:
    """The desktop app exists on macOS only."""
    return sys.platform == "darwin"


# -- versions (the semver crate's, as tauri-plugin-updater compares them) ------

_SEMVER = re.compile(
    r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
)


def parse_version(text: object) -> tuple | None:
    """`(major, minor, patch, pre)` of a semver string (a leading `v` dropped,
    as the updater's `parse_version` does), or None."""
    if not isinstance(text, str):
        return None
    found = _SEMVER.fullmatch(text[1:] if text.startswith("v") else text)
    if found is None:
        return None
    pre = tuple(int(p) if p.isdigit() else p for p in found.group(4).split(".")) if found.group(4) else ()
    return int(found.group(1)), int(found.group(2)), int(found.group(3)), pre


def _pre_key(pre: tuple) -> tuple:
    # Semver precedence: no pre-release ranks above any; numeric below alphanumeric.
    if not pre:
        return (1,)
    return (0, tuple((0, p, "") if isinstance(p, int) else (1, 0, p) for p in pre))


def newer(version: str, than: str) -> bool:
    """Is `version` strictly newer than `than`? False when either is not semver."""
    a, b = parse_version(version), parse_version(than)
    if a is None or b is None:
        return False
    return (a[:3], _pre_key(a[3])) > (b[:3], _pre_key(b[3]))


def _build(text: str) -> str | None:
    return text.split("+", 1)[1] if "+" in text else None


def same_version(a: str, b: str) -> bool:
    """The signed-version check's equality: the semver crate's, `v` dropped,
    build metadata compared literally (`0.1.54+x` is not `0.1.54`); else the
    literal text."""
    pa, pb = parse_version(a), parse_version(b)
    if pa is not None and pb is not None:
        return pa == pb and _build(a) == _build(b)
    return a == b


# -- the manifest ------------------------------------------------------------------


@dataclass(frozen=True)
class Release:
    version: str
    url: str
    signature: str
    target: str  # the manifest key it came from ("" for a dynamic answer)


_RFC3339 = re.compile(r"\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}:\d{2}(\.\d+)?([Zz]|[+-]\d{2}:\d{2})")


def arch() -> str:
    """The architecture the app's updater names (`updater_arch`, its own build's
    `target_arch`): the universal app runs native, so the machine's, even when
    this Python runs under Rosetta."""
    machine = os.uname().machine
    if machine in ("arm64", "aarch64"):
        return "aarch64"
    if supported():
        with contextlib.suppress(OSError, subprocess.SubprocessError):
            done = subprocess.run(
                ["/usr/sbin/sysctl", "-n", "hw.optional.arm64"], capture_output=True, text=True, timeout=5
            )
            if done.stdout.strip() == "1":
                return "aarch64"
    return "x86_64" if machine in ("x86_64", "amd64") else machine


def targets(machine_arch: str | None = None) -> list[str]:
    """`get_urls`'s lookup order for a macOS `.app`: `{os}-{arch}-{installer}`, `{os}-{arch}`."""
    a = machine_arch or arch()
    return [f"darwin-{a}-app", f"darwin-{a}"]


def parse_manifest(data: object, machine_arch: str | None = None) -> tuple[str, dict | None]:
    """`(version, entry)` of a manifest as the updater deserializes it: a
    static one's `platforms[...]` for the first target it has, or a dynamic
    one's own `url`/`signature`. `entry` is None when no target matches."""
    if not isinstance(data, dict):
        raise InstallError("the manifest is not a JSON object")
    version = data.get("version", data.get("name"))
    if parse_version(version) is None:
        raise InstallError(f"the manifest's version {version!r} is not a version")
    pub_date = data.get("pub_date")
    if pub_date is not None and (not isinstance(pub_date, str) or not _RFC3339.fullmatch(pub_date)):
        raise InstallError("the manifest's pub_date is not an RFC 3339 date")
    platforms = data.get("platforms")
    if platforms is not None:
        if not isinstance(platforms, dict):
            raise InstallError("the manifest's platforms is not an object")
        for target in targets(machine_arch):
            entry = platforms.get(target)
            if isinstance(entry, dict) and isinstance(entry.get("url"), str) and isinstance(entry.get("signature"), str):
                return version, {**entry, "target": target}
        return version, None
    if not isinstance(data.get("url"), str) or not isinstance(data.get("signature"), str):
        raise InstallError("the manifest has neither platforms nor a url and signature")
    return version, {"url": data["url"], "signature": data["signature"], "target": ""}
