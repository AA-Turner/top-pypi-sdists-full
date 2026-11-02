"""The files `agents init` writes: every file the first `agents deploy` builds from, so one commit deploys.

`agents deploy` can write a Dockerfile, but not a `pyproject.toml`: it cannot know the project's
dependencies. A new project has none yet, so `init` can write them all.
"""

from __future__ import annotations

import re
from importlib import resources
from importlib.metadata import version
from pathlib import Path
from string import Template

from packaging.version import InvalidVersion, Version

from mistralai.vibe_agents.sdk.app import dockerfile

DISTRIBUTION = "mistralai-agents"
# Every extra, so each quickstart step works on the project. `cli` is left out: it only keeps an old
# spelling resolving, and adds nothing the package does not already install.
EXTRAS = ("bashkit", "sessions-client", "koyeb")
REQUIRES_PYTHON = ">=3.12,<3.15"
# The packages a user's uv `exclude-newer` cutoff can hide on the day of a release: the SDK, and the
# harness it pins exactly. Keep this in step with the `mistralai-vibe-harness==` pin in pyproject.toml.
EXCLUDE_NEWER_EXEMPT = (DISTRIBUTION, "mistralai-vibe-harness")

DOCS_URL = "https://docs-internal-frameworks.mistral.ai/agents-sdk"

# The control plane's agent name rule (AGENT_NAME_PATTERN in agents_controller), which a folder and a
# Python project name also accept: lowercase letters, digits and hyphens, a letter or digit at both ends.
_NAME = re.compile(r"^[a-z0-9](?:[-a-z0-9]*[a-z0-9])?$")
_NAME_MAX_LENGTH = 63
# Windows reserves these names for devices, in any case, so it cannot create a folder with one.
_WINDOWS_DEVICE_NAMES = frozenset(
    ["con", "prn", "aux", "nul", *(f"com{n}" for n in range(1, 10)), *(f"lpt{n}" for n in range(1, 10))]
)

_TEMPLATES = resources.files(__package__).joinpath("templates")


class ProjectError(Exception):
    """`init` cannot create the project. Nothing has been written."""


def check_name(name: str) -> None:
    if len(name) > _NAME_MAX_LENGTH or not _NAME.match(name):
        raise ProjectError(
            f"{name!r} cannot name an agent. Use 1 to {_NAME_MAX_LENGTH} lowercase letters, digits and hyphens (-), "
            "starting and ending with a letter or digit."
        )
    if name in _WINDOWS_DEVICE_NAMES:
        raise ProjectError(f"{name!r} names a device on Windows, so it cannot name a folder. Choose another name.")


def check_folder(folder: Path) -> None:
    if folder.exists() and not folder.is_dir():
        raise ProjectError(f"{folder} exists and is not a folder. Choose another name.")
    if folder.is_dir() and any(folder.iterdir()):
        raise ProjectError(f"{folder} is not empty. `agents init` only creates a new project; choose another name.")


def sdk_version() -> str:
    """The released SDK version the project pins: the one running `init`, so the CLI and the project match.

    A dev or local build is not on PyPI, so a project pinning it could not be locked.
    """
    installed = version(DISTRIBUTION)
    try:
        parsed = Version(installed)
    except InvalidVersion:
        parsed = None
    if parsed is None or parsed.is_devrelease or parsed.local is not None:
        raise ProjectError(
            f"{DISTRIBUTION} {installed} is not a released version, so a project cannot pin it. "
            f"Run `agents init` from a release: `uvx --from {DISTRIBUTION} agents init`."
        )
    return installed


def pyproject_toml(name: str, sdk: str, *, exempt_from_exclude_newer: bool) -> str:
    lines = [
        "[project]",
        f'name = "{name}"',
        'version = "0.1.0"',
        f'requires-python = "{REQUIRES_PYTHON}"',
        f'dependencies = ["{DISTRIBUTION}[{",".join(EXTRAS)}]=={sdk}"]',
    ]
    uv: list[str] = []
    if Version(sdk).is_prerelease:
        uv += [
            "# A release candidate is a prerelease, so it is opt-in. Setting it here rather than passing",
            "# --prerelease=allow keeps `uv run` from re-resolving the lockfile on every command.",
            'prerelease = "allow"',
        ]
    if exempt_from_exclude_newer:
        exempt = ", ".join(f"{package} = false" for package in EXCLUDE_NEWER_EXEMPT)
        uv += [
            "# Your uv `exclude-newer` cutoff would hide a release published after it. Drop this line",
            f"# once the cutoff is past the day {DISTRIBUTION} {sdk} was released.",
            f"exclude-newer-package = {{ {exempt} }}",
        ]
    if uv:
        lines += ["", "[tool.uv]", *uv]
    lines += [
        "",
        "# The project is a workspace of its own, so `uv lock` writes its uv.lock here even inside another",
        "# uv workspace, such as a monorepo checkout.",
        "[tool.uv.workspace]",
    ]
    return "\n".join(lines) + "\n"


def _template(template: str, **values: str) -> str:
    return Template(_TEMPLATES.joinpath(template).read_text(encoding="utf-8")).substitute(values)


def write(folder: Path, name: str, sdk: str, *, exempt_from_exclude_newer: bool) -> list[str]:
    """Write the project's files in `folder`, which `check_folder` accepted, and return their names."""
    files = {
        "pyproject.toml": pyproject_toml(name, sdk, exempt_from_exclude_newer=exempt_from_exclude_newer),
        dockerfile.PYTHON_VERSION_FILE: f"{dockerfile.DEFAULT_PYTHON_VERSION}\n",
        "main.py": _template("main.py.tmpl", name=name),
        ".gitignore": _template("gitignore.tmpl"),
        "README.md": _template("README.md.tmpl", name=name, docs_url=DOCS_URL),
    }
    folder.mkdir(parents=True, exist_ok=True)
    for file_name, content in files.items():
        (folder / file_name).write_text(content, encoding="utf-8")
    dockerfile.write(folder / "Dockerfile")
    return [*files, "Dockerfile"]
