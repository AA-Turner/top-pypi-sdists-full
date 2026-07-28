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
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, List, Optional, Set, Tuple

from packaging.version import InvalidVersion, Version

from abstra_internals.logger import AbstraLogger
from abstra_internals.utils.file_lock import try_file_lock

VERSIONS_DIRNAME = "abstra-versions"

# Cross-process guard file (on the shared EFS user base). Serializes slot
# mutations across processes — the update can be triggered from the editor
# process (button) and the linter sidecar child. See utils/file_lock.
UPDATE_LOCK_FILENAME = ".abstra-update.lock"

# Set by the pod boot shim (cloud-api webEditor/webEditorWorker specs). Its
# presence means the process was launched through the shim, so a flipped slot
# will actually be activated on the next restart. Without it — a pod still on a
# pre-shim spec revision, or any launch that bypasses the shim — flipping a slot
# would silently do nothing (the new version would never be exported onto
# PYTHONPATH), so we must fall back to the legacy in-place upgrade instead.
SHIM_MARKER_ENV = "ABSTRA_SLOT_SHIM"


def _get_python_tag() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}"


def shim_active() -> bool:
    return bool(os.getenv(SHIM_MARKER_ENV))


def get_userbase() -> Optional[Path]:
    userbase = os.getenv("PYTHONUSERBASE")
    return Path(userbase) if userbase else None


def get_update_lock_path(userbase: Path) -> Path:
    return userbase / UPDATE_LOCK_FILENAME


# Intra-process guard for slot mutations. The file lock above (fcntl) only
# serializes across PROCESSES — it is a no-op between threads of the SAME
# process, so it does NOT stop the editor's own threads (boot lint, on-connect
# version check, periodic checker, the update button) from racing into stage()
# and clobbering the shared `.staging-<v>` dir. This thread lock closes that
# gap; every slot-mutating entry point takes both via try_update_lock.
_mutation_lock = threading.Lock()


@contextmanager
def try_update_lock(userbase: Optional[Path]) -> Iterator[bool]:
    """Serialize a slot mutation both intra-process (thread lock) and
    cross-process (fcntl file lock on the shared user base). Non-blocking:
    yields False when another thread OR process is already mutating, so the
    caller bails instead of racing. When there is no user base (desktop /
    non-slotted) only the thread lock applies — there is no shared FS to guard.

    Do NOT nest: the fcntl lock is released when any fd to the lock file closes,
    so an inner acquire would drop the outer lock (see stage_and_prune_locked)."""
    if not _mutation_lock.acquire(blocking=False):
        yield False
        return
    try:
        if userbase is None:
            yield True
        else:
            with try_file_lock(str(get_update_lock_path(userbase))) as acquired:
                yield acquired
    finally:
        _mutation_lock.release()


def get_current_pointer(userbase: Path) -> Path:
    return userbase / f"abstra-current-py{_get_python_tag()}"


def _get_slot_site_packages(slot: Path) -> Path:
    return slot / "lib" / f"python{_get_python_tag()}" / "site-packages"


def _get_slot_dir_of_site(site_packages: Path) -> Path:
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

        site_packages = _get_slot_site_packages(staging)
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
    pointer = get_current_pointer(userbase)
    previous: Optional[Path] = None
    if pointer.is_symlink():
        target = Path(os.readlink(pointer))
        if target.is_absolute():
            previous = _get_slot_dir_of_site(target)

    tmp = pointer.with_name(pointer.name + ".tmp")
    if tmp.is_symlink() or tmp.exists():
        tmp.unlink()
    os.symlink(_get_slot_site_packages(slot), tmp)
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


def _list_slots(userbase: Path) -> List[Tuple[Version, Path]]:
    """Version-sorted list of materialized slots (ignores hidden staging dirs
    and any non-version-named entry)."""
    versions_dir = userbase / VERSIONS_DIRNAME
    if not versions_dir.is_dir():
        return []
    slots: List[Tuple[Version, Path]] = []
    for entry in versions_dir.iterdir():
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        try:
            slots.append((Version(entry.name), entry))
        except InvalidVersion:
            continue
    return sorted(slots, key=lambda item: item[0])


def _get_current_target_slot(userbase: Path) -> Optional[Path]:
    pointer = get_current_pointer(userbase)
    if pointer.is_symlink():
        target = Path(os.readlink(pointer))
        if target.is_absolute():
            return _get_slot_dir_of_site(target)
    return None


def get_pending_version(userbase: Path) -> Optional[str]:
    """The version of a staged slot that is NOT the active pointer target, or
    None when the pointer already points at the newest slot (nothing pending).

    Derived purely from disk (the slot dirs + the pointer), so a
    staged-but-not-flipped update survives a crash / scale-to-zero between the
    stage and the deferred flip — the same slot is still there to activate.
    Because slots only exist once `stage()` renames the hidden staging dir into
    place, this never reports a half-built slot.
    """
    slots = _list_slots(userbase)
    if not slots:
        return None
    newest_version, newest_slot = slots[-1]
    current = _get_current_target_slot(userbase)
    if current is not None and current.resolve() == newest_slot.resolve():
        return None
    return str(newest_version)


def stage_and_prune_locked(userbase: Path, version: str) -> bool:
    """Stage <version> into an inactive slot (deferred update: no flip) and
    prune stale staged slots, keeping the active version (pointer target) and
    the newly staged one. Idempotent: a no-op returning False when <version> is
    already the pending slot.

    MUST be called while already holding the update file lock — it does NOT
    acquire it, because fcntl locks are released when ANY fd to the lock file is
    closed, so a nested acquire here would drop the caller's lock.

    Pruning keeps {active, new}: intermediate slots staged across deferred
    releases (the user updated but hasn't restarted) don't accumulate, and the
    running version is never removed because the pointer target is kept."""
    if get_pending_version(userbase) == version:
        return False
    slot = stage(userbase, version)
    active = _get_current_target_slot(userbase)
    keep = {slot} if active is None else {slot, active}
    prune(userbase, keep)
    AbstraLogger.warning(f"[SelfUpdate] Staged pending abstra=={version} at {slot}")
    return True


def activate_pending_update() -> Optional[str]:
    """Flip the pointer to the pending staged slot and prune, under the update
    lock. Returns the activated version, or None when there is nothing pending
    or another update holds the lock. Does NOT restart — the caller does."""
    userbase = get_userbase()
    if userbase is None:
        return None

    with try_update_lock(userbase) as acquired:
        if not acquired:
            AbstraLogger.warning(
                "[SelfUpdate] Another update in progress; skipping activation"
            )
            return None
        version = get_pending_version(userbase)
        if version is None:
            return None
        slot = userbase / VERSIONS_DIRNAME / version
        previous = flip(userbase, slot)
        keep = {slot} if previous is None else {slot, previous}
        prune(userbase, keep)
        AbstraLogger.warning(f"[SelfUpdate] Activated pending slot abstra=={version}")
        return version


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
