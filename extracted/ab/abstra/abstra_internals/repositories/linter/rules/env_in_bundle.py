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


class UntrackEnv(LinterFix):
    label = "Untrack and ignore .env"

    def fix(self):
        env_file = Settings.root_path / ".env"
        gitignore_file = Settings.root_path / GITIGNORE_FILEPATH

        if not _has_root_env_entry(gitignore_file):
            with gitignore_file.open("a") as file:
                file.write("\n.env")

        FileSystemService.untrack_path_from_git(env_file)


class EnvInBundleFound(LinterIssue):
    def __init__(self) -> None:
        self.label = "Your .env file is exposed to git"
        self.fixes = [UntrackEnv()]


class EnvInBundle(LinterRule):
    label = "You can't add .env to the bundle"
    type = "security"

    def find_issues(self) -> List[LinterIssue]:
        env_file = Settings.root_path / ".env"

        if not env_file.exists():
            return []

        if FileSystemService.is_ignored(env_file):
            return []

        return [EnvInBundleFound()]
