"""Abstra editor self-update.

Extracted from the linter: "a new abstra version is available" is an
environment/platform concern, not a check on the user's project code. It hits
PyPI (cached 15 min) and only makes sense on full passes, so the result is
cached here and refreshed on boot / explicit refresh, then surfaced to the
editor via the linter-events payload and triggered via a dedicated route.
"""

import threading
import webbrowser
from importlib.metadata import PackageNotFoundError
from typing import Optional, Tuple, TypedDict

from abstra_internals.environment import EDITOR_MODE
from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.linter.process_actions import (
    restart_editor_and_workers,
)
from abstra_internals.services.self_update import (
    get_userbase,
    shim_active,
    stage_and_prune_locked,
    try_update_lock,
)
from abstra_internals.utils.platform import is_windows
from abstra_internals.version import PackageVersionManager, VersionStatus

RELEASE_NOTES_URL = "https://github.com/abstra-app/abstra-lib/releases"


class UpdateState(TypedDict):
    available: bool
    label: str
    # Whether clicking update restarts the editor IMMEDIATELY. False on Windows
    # (opens release notes) and on the deferred staged path (web + boot shim:
    # the click only stages a slot; the restart happens later via "Restart
    # now"). True for the legacy immediate in-place upgrade (desktop, or web
    # pods still on a pre-shim spec).
    restarts: bool
    # Whether updates go through the deferred staged flow (web + boot shim):
    # auto-staged in the background, applied on a user-triggered restart — so
    # the frontend shows no manual update button. False elsewhere.
    deferred: bool


def _defers_restart() -> bool:
    """The staged path installs into an inactive slot without restarting; the
    user applies it later via EditorRestartController. Only web pods with the
    boot shim marker take this path (see editor_update._do_update)."""
    return EDITOR_MODE == "web" and shim_active()


def _latest_known_version() -> Optional[str]:
    try:
        return str(PackageVersionManager("abstra").cached_latest_version)
    except PackageNotFoundError:
        return None


def _do_update() -> None:
    import subprocess
    import sys

    try:
        if _defers_restart():
            # Deferred staged path: install the new version into an INACTIVE
            # slot but do NOT flip or restart. The running version (python AND
            # its bundled JS assets) stays untouched; the new one activates only
            # when the user triggers "Restart now" (EditorRestartController),
            # which flips the pointer and restarts. restart_status(abstra) is
            # then derived from disk (the staged slot). Requires the boot shim
            # marker + PYTHONUSERBASE.
            userbase = get_userbase()
            target = _latest_known_version()
            if userbase is not None and target is not None:
                # Runs under _update_lib_version's file lock (do NOT acquire it
                # again — see stage_and_prune_locked). Idempotent: a no-op when
                # the latest is already staged.
                stage_and_prune_locked(userbase, target)
                AbstraLogger.warning(
                    f"[UpdateAbstra] Ensured abstra=={target} staged; awaiting user restart"
                )
                return
            AbstraLogger.warning(
                "[UpdateAbstra] Staged update unavailable; upgrading in place"
            )

        # Legacy immediate upgrade: web pods still on a pre-shim spec (a flipped
        # slot would never activate) and desktop. Mutates in place, restarts now.
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "abstra"]
        )
        # The restart must happen in the EDITOR process. Under the linter
        # sidecar this runs in the child, where os._exit/os.execv would restart
        # the wrong process — the process-action hook routes it to the editor.
        restart_editor_and_workers("[UpdateAbstra]")
    except Exception as e:
        AbstraLogger.error(f"[UpdateAbstra] Failed to update Abstra: {e}")


def _update_lib_version() -> None:
    # Serialize the whole update (staged AND in-place) against every other
    # slot-mutating path — the update button, the linter-fix trigger, and the
    # background auto-stage all share try_update_lock's thread + file locks.
    # Bailing on a held lock must NOT fall through to an in-place pip: another
    # thread or process is already updating this pod.
    with try_update_lock(get_userbase()) as acquired:
        if not acquired:
            AbstraLogger.warning(
                "[UpdateAbstra] Another update already in progress; skipping"
            )
            return
        _do_update()


class EditorUpdateController:
    _lock = threading.Lock()
    _available = False
    _label = ""
    _restarts = False

    @classmethod
    def _compute(cls, revalidate: bool) -> Tuple[bool, str, bool]:
        try:
            package_version = PackageVersionManager("abstra", revalidate=revalidate)
        except PackageNotFoundError:
            return False, "", False

        if package_version.get_version_status() != VersionStatus.OUT_OF_DATE:
            return False, "", False

        label = (
            f"Latest version is {package_version.cached_latest_version}, but you "
            f"have {package_version.current_local_version}. "
            f"Updating may take up to 2 minutes."
        )
        restarts_immediately = not is_windows() and not _defers_restart()
        return True, label, restarts_immediately

    @classmethod
    def refresh(cls, revalidate: bool = False) -> None:
        """Recompute update availability. Runs only on full passes (boot /
        explicit refresh) to avoid hitting the version cache on every broadcast."""
        available, label, restarts = cls._compute(revalidate)
        with cls._lock:
            cls._available = available
            cls._label = label
            cls._restarts = restarts

    @classmethod
    def state(cls) -> UpdateState:
        with cls._lock:
            return UpdateState(
                available=cls._available,
                label=cls._label,
                restarts=cls._restarts,
                deferred=_defers_restart(),
            )

    @classmethod
    def auto_stage_if_needed(cls) -> bool:
        """Deferred path only (web + boot shim): pre-stage the latest version
        into an inactive slot in the background so the user's "Restart editor"
        is instant. No-op when not on the deferred path, no update is available,
        or the latest is already staged. Returns whether it staged fresh."""
        if not _defers_restart():
            return False
        with cls._lock:
            available = cls._available
        if not available:
            return False
        userbase = get_userbase()
        target = _latest_known_version()
        if userbase is None or target is None:
            return False
        try:
            # try_update_lock serializes against the update button / linter-fix
            # trigger AND against the editor's other auto-stage threads (boot
            # lint, on-connect check, periodic checker) — the fcntl file lock
            # alone would NOT, since it is a no-op between same-process threads.
            with try_update_lock(userbase) as acquired:
                if not acquired:
                    return False
                return stage_and_prune_locked(userbase, target)
        except Exception as e:
            AbstraLogger.error(f"[UpdateAbstra] Auto-stage failed: {e}")
            return False

    @classmethod
    def trigger_update(cls) -> None:
        if is_windows():
            webbrowser.open(RELEASE_NOTES_URL)
            return
        # No separate intra-process lock here: _update_lib_version's
        # try_update_lock already serializes concurrent clicks (the editor pod
        # is shared by the project's users) against each other and against the
        # background auto-stage.
        _update_lib_version()
