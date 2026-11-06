"""The skills shipped in the wheel, under `bundled/`, and how `agents skills add` copies one into a project."""

from __future__ import annotations

import enum
from collections.abc import Iterator
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path, PurePosixPath

# The name `agents skills add` takes, and the folder under `bundled/` it installs. The folder is the skill's
# name, which coding agents and the Harness accept only as letters, digits and hyphens: no dot.
SKILLS = {"migrate-1.1": "migrate-1-1"}

# The project skills folder that Codex and Mistral Vibe read.
SKILLS_DIR = Path(".agents") / "skills"

_BUNDLED = resources.files(__package__).joinpath("bundled")


class Outcome(enum.Enum):
    ADDED = "added"
    UPDATED = "updated"
    UNCHANGED = "unchanged"


def install(name: str) -> tuple[Path, Outcome]:
    """Copy the shipped skill `name` into `./.agents/skills/<skill>/`. Returns that folder and what changed.

    The shipped files replace the installed ones, so a run after an SDK upgrade brings the skill up to date.
    A file the user added beside them stays.
    """
    folder = SKILLS[name]
    target = SKILLS_DIR / folder
    existed = (target / "SKILL.md").exists()
    changed = False
    for relative, content in _files(_BUNDLED.joinpath(folder), PurePosixPath()):
        path = target.joinpath(*relative.parts)
        if path.is_file() and path.read_bytes() == content:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        changed = True
    if not existed:
        return target, Outcome.ADDED
    return target, Outcome.UPDATED if changed else Outcome.UNCHANGED


def _files(folder: Traversable, relative: PurePosixPath) -> Iterator[tuple[PurePosixPath, bytes]]:
    for entry in sorted(folder.iterdir(), key=lambda entry: entry.name):
        if entry.is_dir():
            yield from _files(entry, relative / entry.name)
        elif entry.is_file():
            yield relative / entry.name, entry.read_bytes()
