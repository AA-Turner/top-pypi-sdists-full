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
from typing import Tuple, TypedDict

from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.linter.process_actions import (
    restart_editor_and_workers,
)
from abstra_internals.utils.platform import is_windows
from abstra_internals.version import PackageVersionManager, VersionStatus

RELEASE_NOTES_URL = "https://github.com/abstra-app/abstra-lib/releases"


class UpdateState(TypedDict):
    available: bool
    label: str
    # Whether triggering the update restarts the editor. False on Windows,
    # where we open the release notes instead of upgrading in place.
    restarts: bool


def _update_lib_version() -> None:
    import subprocess
    import sys

    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "abstra"]
        )
        # The restart must happen in the EDITOR process. Under the linter
        # sidecar this runs in the child, where os._exit/os.execv would restart
        # the wrong process — the process-action hook routes it to the editor
        # (web defers the restart to the user; desktop restarts in place).
        restart_editor_and_workers("[UpdateAbstra]")
    except Exception as e:
        AbstraLogger.error(f"[UpdateAbstra] Failed to update Abstra: {e}")


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
        return True, label, not is_windows()

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
                available=cls._available, label=cls._label, restarts=cls._restarts
            )

    @classmethod
    def trigger_update(cls) -> None:
        if is_windows():
            webbrowser.open(RELEASE_NOTES_URL)
        else:
            _update_lib_version()
