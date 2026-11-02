"""The project's git repository: `agents deploy` builds the commit you push, so the first commit deploys."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

COMMIT_MESSAGE = "Create the agent with agents init"


class GitError(Exception):
    """A git command failed. `command` finishes the setup by hand; `output` is what git printed."""

    def __init__(self, message: str, *, command: str, output: str) -> None:
        super().__init__(message)
        self.command = command
        self.output = output


class GitState(Enum):
    NO_GIT = "no-git"
    IN_REPOSITORY = "in-repository"
    CAN_INIT = "can-init"


@dataclass(frozen=True)
class GitContext:
    state: GitState
    git: str | None = None


def context(folder: Path) -> GitContext:
    """Whether the project can get a repository of its own.

    A project inside an existing repository, such as a monorepo checkout, is committed there: a nested
    repository is almost always a mistake.
    """
    git = shutil.which("git")
    if git is None:
        return GitContext(GitState.NO_GIT)
    completed = subprocess.run(  # noqa: S603 - git, found on the PATH
        [git, "-C", str(folder), "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode == 0 and completed.stdout.strip() == "true":
        return GitContext(GitState.IN_REPOSITORY, git)
    return GitContext(GitState.CAN_INIT, git)


def init(folder: Path, git: str) -> None:
    """Create the project's repository and commit every file in it, so the next `agents deploy` takes one step."""
    _run(folder, git, ["init", "--quiet"], command=f"git -C {folder} init")
    _run(folder, git, ["add", "--all"], command=f"git -C {folder} add --all")
    _run(
        folder,
        git,
        ["commit", "--quiet", "--message", COMMIT_MESSAGE],
        command=f'git -C {folder} commit -m "{COMMIT_MESSAGE}"',
    )


def _run(folder: Path, git: str, args: list[str], *, command: str) -> None:
    completed = subprocess.run(  # noqa: S603 - git, found on the PATH
        [git, "-C", str(folder), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise GitError(
            f"`git {args[0]}` failed.", command=command, output=(completed.stderr or completed.stdout).strip()
        )
