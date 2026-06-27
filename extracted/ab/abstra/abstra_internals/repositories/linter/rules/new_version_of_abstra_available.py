import webbrowser
from importlib.metadata import PackageNotFoundError
from pathlib import Path
from typing import List, Optional

from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.linter.models import (
    LinterFix,
    LinterIssue,
    PathScopedLinterRule,
)
from abstra_internals.repositories.linter.process_actions import (
    restart_editor_and_workers,
)
from abstra_internals.utils.platform import is_windows
from abstra_internals.version import PackageVersionManager, VersionStatus

RELEASE_NOTES_URL = "https://github.com/abstra-app/abstra-lib/releases"


def _update_lib_version():
    import subprocess
    import sys

    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "abstra"]
        )
        # The restart must happen in the EDITOR process. Under the linter
        # sidecar this fix runs in the child, where os._exit/os.execv would
        # restart the wrong process — the process-action hook routes it to
        # the editor (and executes immediately on the in-process path).
        restart_editor_and_workers("[UpdateAbstra]")
    except Exception as e:
        AbstraLogger.error(f"[UpdateAbstra] Failed to update Abstra: {e}")


class UpdateAbstraVersion(LinterFix):
    def __init__(self) -> None:
        self.label = "Update Abstra Editor version"

    def fix(self):
        _update_lib_version()


class OpenChangeLog(LinterFix):
    def __init__(self) -> None:
        self.label = "Open the release notes"

    def fix(self):
        webbrowser.open(RELEASE_NOTES_URL)


class NewVersionOfAbstraAvailableFound(LinterIssue):
    def __init__(self) -> None:
        package_version = PackageVersionManager("abstra")
        self.label = f"Latest version is {package_version.cached_latest_version}, but you have {package_version.current_local_version}. Updating may take up to 2 minutes."
        if is_windows():
            self.fixes = [OpenChangeLog()]
        else:
            self.fixes = [UpdateAbstraVersion()]


class NewVersionOfAbstraAvailable(PathScopedLinterRule):
    label = "A new version of Abstra Editor is available"
    type = "warning"

    def find_issues(self, path: Optional[Path] = None) -> List[LinterIssue]:
        # A file save cannot change the published Abstra version, and the check
        # hits PyPI (cached 4h). Skip it on scoped (save) runs; the existing
        # project-global banner is preserved by the scoped merge. The check
        # still runs on full passes (boot/refresh/deploy).
        if path is not None:
            return []
        try:
            package_version = PackageVersionManager("abstra")
        except PackageNotFoundError:
            return []
        version_status = package_version.get_version_status()
        is_there_a_new_version = version_status == VersionStatus.OUT_OF_DATE

        if is_there_a_new_version is True:
            return [NewVersionOfAbstraAvailableFound()]
        else:
            return []
