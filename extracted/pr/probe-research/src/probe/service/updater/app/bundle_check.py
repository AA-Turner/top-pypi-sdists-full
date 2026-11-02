"""check a staged bundle is Probe at the version asked for, signed by the Probe team."""

from __future__ import annotations
import os
import stat
import subprocess
from pathlib import Path

from . import locate as appupdate
from probe.service.updater.app.errors import InstallError
from probe.service.updater.app.manifest import same_version

BUNDLE_ID = appupdate.BUNDLE_ID
CODESIGN = "/usr/bin/codesign"
CODESIGN_TIMEOUT_S = 120.0
#: The Developer ID team that signs every Probe release: the certificate in
#: prbe-ai/desktop release.yml's `APPLE_CERTIFICATE` secret, "Developer ID
#: Application: Richard Wei (2HDWBQ9P3D)" (desktop CLAUDE.md, Releases; `spctl`
#: reports it as the origin of 0.1.53 and 0.1.54 on agent-os-matrix's macOS
#: job). Also pinned in desktop `probe-swap.rs` `TEAM_ID`: a new team is a new
#: constant in both, in the same release.
TEAM_ID = "2HDWBQ9P3D"
#: Developer ID only: Apple's Developer ID CA as the intermediate, a Developer
#: ID Application leaf, the team. The same text in desktop `probe-swap.rs`
#: `team_requirement` and release.yml's signature check.
TEAM_REQUIREMENT = (
    "=anchor apple generic and certificate 1[field.1.2.840.113635.100.6.2.6] exists"
    " and certificate leaf[field.1.2.840.113635.100.6.1.13] exists"
    f' and certificate leaf[subject.OU] = "{TEAM_ID}"'
)


def bundle_info(bundle: Path) -> dict:
    """The bundle's Info.plist (at most 1 MB), or InstallError."""
    import plistlib

    path = bundle / "Contents" / "Info.plist"
    try:
        if not stat.S_ISREG(os.lstat(path).st_mode) or os.lstat(path).st_size > 1024 * 1024:
            raise InstallError("the bundle's Info.plist is not a file")
        with open(path, "rb") as handle:
            data = plistlib.load(handle)
    except (OSError, ValueError, plistlib.InvalidFileException) as exc:
        raise InstallError(f"the bundle's Info.plist cannot be read: {exc}") from exc
    if not isinstance(data, dict):
        raise InstallError("the bundle's Info.plist is not a dictionary")
    return data


def check_bundle(bundle: Path, version: str) -> None:
    """The staged bundle is Probe at `version`, with its executable."""
    info = bundle_info(bundle)
    if info.get("CFBundleIdentifier") != BUNDLE_ID:
        raise InstallError(f"the update's bundle id is {info.get('CFBundleIdentifier')!r}, not {BUNDLE_ID}")
    found = info.get("CFBundleShortVersionString")
    if not isinstance(found, str) or not same_version(found, version):
        raise InstallError(f"the update's bundle is version {found!r}, not {version}")
    executable = info.get("CFBundleExecutable")
    if not isinstance(executable, str) or not executable or "/" in executable or executable in (".", ".."):
        raise InstallError("the update's bundle names no executable")
    path = bundle / "Contents" / "MacOS" / executable
    try:
        mode = os.lstat(path).st_mode
    except OSError as exc:
        raise InstallError(f"the update's executable {executable} is missing") from exc
    if not stat.S_ISREG(mode) or not mode & 0o100:
        raise InstallError(f"the update's executable {executable} is not an executable file")


def codesign_verify(bundle: Path, what: str = "the update") -> str:
    """`codesign --verify --deep --strict -R=<the Probe team>` on the staged
    bundle: integrity AND who signed it (an ad-hoc or another team's signature
    is refused; the service runs this bundle's helper next). "verified", or
    "unavailable" where there is no codesign (not macOS). InstallError otherwise
    (`what` names the bundle in its message)."""
    if not os.path.exists(CODESIGN):
        return "unavailable"
    try:
        done = subprocess.run(
            # `-R` and the requirement as two arguments: "=" then the text (attached,
            # `-R==…`, codesign reads an invalid requirement).
            [CODESIGN, "--verify", "--deep", "--strict", "-R", TEAM_REQUIREMENT, str(bundle)],
            capture_output=True,
            text=True,
            timeout=CODESIGN_TIMEOUT_S,
            stdin=subprocess.DEVNULL,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise InstallError(f"codesign could not run: {exc}") from exc
    if done.returncode != 0:
        raise InstallError(f"codesign refused {what}: {(done.stderr or done.stdout).strip()[:300]}")
    return "verified"


def app_broken(app: Path) -> str | None:
    """Why the installed app fails `codesign_verify`, or None when it passes
    (or there is no codesign to ask)."""
    try:
        codesign_verify(app, what="the installed app")
    except InstallError as exc:
        return str(exc)
    return None
