"""The Dockerfile `agents deploy` writes for a project that has none.

The platform builds the image from the pushed commit, so the file has to be committed before it can be
built: once the user agrees, the deploy writes it and stops, and the user commits and pushes it. From then
on it is the project's own file, and later deploys build it as it is. The same goes for the
`.python-version` it builds with.
"""

from __future__ import annotations

from importlib import resources
from pathlib import Path

# The project's uv.lock is the single source of the SDK version and of every other dependency, so the
# template pins neither. uv is pinned to a minor version, which still gets its patch releases, so a new uv
# cannot change the image the user tested. The sync is --frozen, not --locked: --locked also compares the
# lock with the uv settings of the machine that wrote it, such as a global exclude-newer, which the build
# does not have.
TEMPLATE = resources.files(__package__).joinpath("agent.Dockerfile")

PYTHON_VERSION_FILE = ".python-version"
# Without the file, uv in the build installs the newest Python the project allows, which can be newer
# than its dependencies have wheels for. The oldest Python the SDK supports has the widest choice.
DEFAULT_PYTHON_VERSION = "3.12"

# What the template builds from, and how to get it.
_REQUIRED_FILES = {
    "pyproject.toml": "Run `uv init`",
    "uv.lock": "Run `uv lock`",
}


def generation_issues(project: Path) -> list[str]:
    """Say why the Dockerfile cannot be written for this project, one line per missing file."""
    return [
        f"No Dockerfile was found, and `agents deploy` can only write one for a uv project: {name} is missing. "
        f"{hint}, or add your own Dockerfile."
        for name, hint in _REQUIRED_FILES.items()
        if not (project / name).is_file()
    ]


def write(target: Path) -> None:
    target.write_text(TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")


def missing(project: Path, dockerfile_name: str) -> list[str]:
    """Name the files the deploy can write for the project: the Dockerfile, and the `.python-version` a
    generated one builds with, when the project lacks them.
    """
    names: list[str] = []
    dockerfile = project / dockerfile_name
    has_dockerfile = dockerfile.is_file()
    if not has_dockerfile:
        names.append(dockerfile_name)
    if (not has_dockerfile or build_inputs(dockerfile)) and not (project / PYTHON_VERSION_FILE).is_file():
        names.append(PYTHON_VERSION_FILE)
    return names


def write_missing(project: Path, dockerfile_name: str) -> list[str]:
    """Write the files `missing` names, and return their names."""
    names = missing(project, dockerfile_name)
    if dockerfile_name in names:
        write(project / dockerfile_name)
    if PYTHON_VERSION_FILE in names:
        (project / PYTHON_VERSION_FILE).write_text(f"{DEFAULT_PYTHON_VERSION}\n", encoding="utf-8")
    return names


def build_inputs(dockerfile: Path) -> list[str]:
    """The project files a Dockerfile written from the template builds from; none for any other Dockerfile.

    The file is recognised by its first line, which an edit to the rest of the file keeps.
    """
    header = TEMPLATE.read_text(encoding="utf-8").partition("\n")[0]
    with dockerfile.open(encoding="utf-8") as file:
        written = file.readline().rstrip("\n") == header
    return [*_REQUIRED_FILES, PYTHON_VERSION_FILE] if written else []
