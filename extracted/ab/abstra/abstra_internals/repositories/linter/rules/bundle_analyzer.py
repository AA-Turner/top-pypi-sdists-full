import sys
from pathlib import Path
from typing import List

from abstra_internals.consts.filepaths import GITIGNORE_FILEPATH
from abstra_internals.repositories.linter.models import (
    LinterFix,
    LinterIssue,
    LinterRule,
)
from abstra_internals.services.fs import FileSystemService
from abstra_internals.settings import Settings


def _has_root_env_entry(gitignore_file: Path) -> bool:
    if not gitignore_file.exists():
        return False
    try:
        lines = gitignore_file.read_text().splitlines()
    except (IOError, UnicodeDecodeError):
        return False
    return any(line.strip() in (".env", "/.env") for line in lines)


def get_root_and_prefix_path():
    prefix_path = Path(sys.prefix).resolve().as_posix()
    root_path = Settings.root_path.resolve().as_posix()

    return root_path, prefix_path


def running_under_virtualenv() -> bool:
    # pip._internal.utils.virtualenv._running_under_venv
    if sys.prefix != getattr(sys, "base_prefix", sys.prefix):
        return True

    # pip._internal.utils.virtualenv._running_under_legacy_virtualenv
    if hasattr(sys, "real_prefix"):
        return True

    return False


def virtualenv_inside_project() -> bool:
    root_path, prefix_path = get_root_and_prefix_path()
    return prefix_path.startswith(root_path)


def virtualenv_ignored() -> bool:
    root_path, prefix_path = get_root_and_prefix_path()
    venv_folder = prefix_path.replace(root_path, "").lstrip("/")
    # Use absolute path to ensure git check-ignore works correctly
    absolute_venv_path = Settings.root_path / venv_folder
    return FileSystemService.is_ignored(absolute_venv_path)


class UntrackEnv(LinterFix):
    label = "Untrack and ignore .env"

    def fix(self):
        env_file = Settings.root_path / ".env"
        gitignore_file = Settings.root_path / GITIGNORE_FILEPATH

        if not _has_root_env_entry(gitignore_file):
            with gitignore_file.open("a") as file:
                file.write("\n.env")

        FileSystemService.untrack_path_from_git(env_file)


class UntrackVenv(LinterFix):
    label = "Add virtual env to git ignore"

    def fix(self):
        root_path, prefix_path = get_root_and_prefix_path()
        venv_folder = prefix_path.replace(root_path, "").lstrip("/")

        if virtualenv_inside_project() and not virtualenv_ignored():
            gitignore_file = Settings.root_path / GITIGNORE_FILEPATH
            with gitignore_file.open("a") as file:
                file.write("\n")
                file.write(venv_folder)

        FileSystemService.untrack_path_from_git(Path(venv_folder))


class EnvInBundleFound(LinterIssue):
    title = "You can't add .env to the bundle"
    type = "error"

    def __init__(self) -> None:
        self.label = "Your .env file is exposed to git"
        self.fixes = [UntrackEnv()]


class VenvInBundleFound(LinterIssue):
    title = "You can't add virtual env to the bundle"
    type = "error"

    def __init__(self) -> None:
        self.label = "You have not ignored the virtualenv folder"
        self.fixes = [UntrackVenv()]


def _env_in_bundle_issues() -> List[LinterIssue]:
    env_file = Settings.root_path / ".env"

    if not env_file.exists():
        return []

    if FileSystemService.is_ignored(env_file):
        return []

    return [EnvInBundleFound()]


def _venv_in_bundle_issues() -> List[LinterIssue]:
    if not running_under_virtualenv():
        return []

    if not virtualenv_inside_project():
        return []

    if virtualenv_ignored():
        return []

    return [VenvInBundleFound()]


class BundleAnalyzer(LinterRule):
    """Files that must never ship in the bundle / git tree, in one pass:
    a .env exposed to git and a virtualenv folder that isn't ignored."""

    label = "Bundle analysis"

    def find_issues(self) -> List[LinterIssue]:
        return [
            *_env_in_bundle_issues(),
            *_venv_in_bundle_issues(),
        ]
