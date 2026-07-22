"""Staged (slotted) self-update of the abstra package.

In web-editor pods the running environment must never be mutated in place: pip swaps
files on disk while the old process still imports modules lazily and serves
the bundled JS assets per request, so frontend and backend skew (see
editor_update.py). Instead, each update is installed into an isolated slot
under $PYTHONUSERBASE/abstra-versions/<version>/ and activated by atomically
flipping the $PYTHONUSERBASE/abstra-current-py<X.Y> symlink, which the pod
boot shim (cloud-api webEditor/webEditorWorker specs) exports as PYTHONPATH.
The running slot is never touched; the new version only becomes visible on
the restart that follows the flip, python and JS assets together.

The pointer targets the slot's site-packages dir directly so the shim doesn't
need to know the layout, and its name encodes the python minor version: a pod
rebuilt on a newer python ignores pointers staged under the old ABI and falls
back to the image's abstra.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional, Set

from abstra_internals.logger import AbstraLogger

VERSIONS_DIRNAME = "abstra-versions"

# Set by the pod boot shim (cloud-api webEditor/webEditorWorker specs). Its
# presence means the process was launched through the shim, so a flipped slot
# will actually be activated on the next restart. Without it — a pod still on a
# pre-shim spec revision, or any launch that bypasses the shim — flipping a slot
# would silently do nothing (the new version would never be exported onto
# PYTHONPATH), so we must fall back to the legacy in-place upgrade instead.
SHIM_MARKER_ENV = "ABSTRA_SLOT_SHIM"


def _python_tag() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}"


def shim_active() -> bool:
    return bool(os.getenv(SHIM_MARKER_ENV))


def get_userbase() -> Optional[Path]:
    userbase = os.getenv("PYTHONUSERBASE")
    return Path(userbase) if userbase else None


def current_pointer(userbase: Path) -> Path:
    return userbase / f"abstra-current-py{_python_tag()}"


def _slot_site_packages(slot: Path) -> Path:
    return slot / "lib" / f"python{_python_tag()}" / "site-packages"


def _slot_dir_of_site(site_packages: Path) -> Path:
    # <slot>/lib/pythonX.Y/site-packages -> <slot>
    return site_packages.parents[2]


def stage(userbase: Path, version: str) -> Path:
    """Install abstra==<version> into a fresh slot and return the slot dir.

    The install targets a hidden staging dir renamed into place only on
    success, so a crash mid-install never leaves a half-usable slot behind.

    The slot is kept lean (abstra + its bundled statics, ~50MB) instead of
    self-contained (~420MB) by installing in two pip passes and letting deps
    resolve from the ambient environment at runtime.
    """
    versions_dir = userbase / VERSIONS_DIRNAME
    versions_dir.mkdir(parents=True, exist_ok=True)
    staging = versions_dir / f".staging-{version}"
    slot = versions_dir / version
    if staging.exists():
        shutil.rmtree(staging)

    # PYTHONUSERBASE routes both `--user` passes into the staging dir; PYTHONPATH
    # is dropped so a previously active slot can't interfere with resolution.
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    env["PYTHONUSERBASE"] = str(staging)

    def pip_install(*args: str) -> None:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--user",
                *args,
                f"abstra=={version}",
            ],
            env=env,
        )

    try:
        # Pass 1 — force abstra itself (and its bundled statics) into the slot.
        # The editor image bakes abstra into the global site-packages, which
        # stays on pip's path, so a plain install would treat the target as
        # "already satisfied" and copy nothing whenever the target version is
        # <= the image's (e.g. right after a release). --ignore-installed
        # forces it in regardless; --no-deps keeps the ~370MB of dependencies
        # out of the slot.
        pip_install("--ignore-installed", "--no-deps", "--no-warn-script-location")
        # Pass 2 — resolve abstra's dependencies against the ambient
        # environment (global image + user site) and copy only the ones not
        # already satisfied into the slot. On a normal patch upgrade this
        # installs nothing; it only kicks in when a new abstra bumps a dep.
        pip_install("--no-warn-script-location")

        site_packages = _slot_site_packages(staging)
        if not (site_packages / "abstra").is_dir():
            raise RuntimeError(
                f"Staged install of abstra=={version} produced no package at {site_packages}"
            )
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise

    if slot.exists():
        shutil.rmtree(slot)
    staging.rename(slot)
    return slot


def flip(userbase: Path, slot: Path) -> Optional[Path]:
    """Atomically point the current-version symlink at the slot.

    Returns the previously active slot dir, if any. os.replace over the
    temporary symlink is a rename(2), atomic on the same EFS directory, so
    readers (pod boot shims) always see either the old or the new target.
    """
    pointer = current_pointer(userbase)
    previous: Optional[Path] = None
    if pointer.is_symlink():
        target = Path(os.readlink(pointer))
        if target.is_absolute():
            previous = _slot_dir_of_site(target)

    tmp = pointer.with_name(pointer.name + ".tmp")
    if tmp.is_symlink() or tmp.exists():
        tmp.unlink()
    os.symlink(_slot_site_packages(slot), tmp)
    os.replace(tmp, pointer)
    return previous


def prune(userbase: Path, keep: Set[Path]) -> None:
    """Remove slots (and stale staging dirs) other than the ones to keep.

    Keeping the previous slot alongside the new one allows a cheap manual
    rollback: flip the pointer back and restart.
    """
    versions_dir = userbase / VERSIONS_DIRNAME
    if not versions_dir.is_dir():
        return
    keep_resolved = {path.resolve() for path in keep}
    for entry in versions_dir.iterdir():
        if entry.resolve() in keep_resolved:
            continue
        try:
            shutil.rmtree(entry)
        except Exception as e:
            AbstraLogger.warning(f"[SelfUpdate] Failed to prune slot {entry}: {e}")


def perform_staged_update(version: str) -> bool:
    """Stage abstra==<version> in a new slot and flip the active pointer.

    Returns False when the environment can't support slots (no boot shim, or
    no PYTHONUSERBASE), letting the caller fall back to the legacy in-place
    upgrade. Any failure while staging raises before the pointer is touched, so
    the running version stays fully intact.
    """
    if not shim_active():
        return False

    userbase = get_userbase()
    if userbase is None:
        return False

    slot = stage(userbase, version)
    previous = flip(userbase, slot)
    keep = {slot} if previous is None else {slot, previous}
    prune(userbase, keep)
    AbstraLogger.warning(
        f"[SelfUpdate] Staged abstra=={version} at {slot} and flipped the active pointer"
        + (f" (previous: {previous})" if previous else "")
    )
    return True
