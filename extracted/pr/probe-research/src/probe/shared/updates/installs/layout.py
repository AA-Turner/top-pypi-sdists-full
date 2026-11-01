"""where version envs live on disk: uv's tool dir, version folders, generations."""

from __future__ import annotations
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

DIST = "probe-research"
VERSIONS_DIRNAME = "probe-versions"
_VERSION = re.compile(r"^[0-9][0-9A-Za-z.+!_-]{0,63}$")
_UV_TIMEOUT_S = 15


def tool_dir() -> Path:
    """uv's tool folder: `UV_TOOL_DIR`, else `uv tool dir`, else the default."""
    override = os.environ.get("UV_TOOL_DIR")
    if override:
        return Path(override)
    uv = shutil.which("uv")
    if uv:
        try:
            out = subprocess.run(
                [uv, "tool", "dir"], capture_output=True, text=True, timeout=_UV_TIMEOUT_S, check=False
            )
            line = (out.stdout or "").strip().splitlines()
            if out.returncode == 0 and line and os.path.isabs(line[-1]):
                return Path(line[-1])
        except (OSError, subprocess.SubprocessError):
            pass
    base = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    return Path(base) / "uv" / "tools"


def tool_env(tools: Path | None = None) -> Path:
    """The tool path: `<uv tool dir>/probe-research`."""
    return (tools or tool_dir()) / DIST


def versions_root(tools: Path | None = None) -> Path:
    """`<uv tool dir>/../probe-versions`: beside uv's tools, on the same filesystem."""
    return (tools or tool_dir()).parent / VERSIONS_DIRNAME


def version_env(version: str, tools: Path | None = None) -> Path:
    if not _VERSION.match(version):
        raise ValueError(f"not a version: {version!r}")
    return versions_root(tools) / version / DIST


#: `<version>+g<N>`: a rebuild of `<version>` beside the folder in use. `-<digits>`:
#: an older release's migration leftover (`<version>-<unix time>`).
_FOLDER = re.compile(r"^(?P<version>.+?)(?:\+g(?P<generation>[0-9]{1,6}))?(?:-(?P<stamp>[0-9]{6,}))?$")


def folder_parts(name: str) -> tuple[str, int, bool]:
    """`(version, generation, leftover)` of a version folder's name:
    `0.3.1` -> ("0.3.1", 1, False), `0.3.1+g2` -> ("0.3.1", 2, False),
    `0.3.1-1730000000` -> ("0.3.1", 1, True). Only a NAME: the version an env
    holds is its dist-info's (`env_version`)."""
    found = _FOLDER.match(name)
    if not found:
        return name, 1, False
    generation = int(found.group("generation") or 1)
    return found.group("version"), max(generation, 1), found.group("stamp") is not None


def generation_env(version: str, generation: int, tools: Path | None = None) -> Path:
    """`probe-versions/<version>/probe-research` for generation 1, else
    `probe-versions/<version>+g<N>/probe-research`."""
    if generation <= 1:
        return version_env(version, tools)
    return version_env(f"{version}+g{int(generation)}", tools)


def _folders(tools: Path | None = None) -> list[Path]:
    try:
        return [p for p in versions_root(tools).iterdir() if p.is_dir() and not p.name.startswith(".")]
    except OSError:
        return []


def next_generation(version: str, tools: Path | None = None) -> int:
    """The generation a rebuild of `version` gets: one past every folder of it."""
    highest = 1
    for folder in _folders(tools):
        name, generation, _leftover = folder_parts(folder.name)
        if name == version:
            highest = max(highest, generation)
    return highest + 1


def envs_of(version: str, tools: Path | None = None) -> list[Path]:
    """Every generation's env of `version` that has an interpreter, newest
    generation first (leftovers last). Their dist-info decides what they hold."""
    found = []
    for folder in _folders(tools):
        name, generation, leftover = folder_parts(folder.name)
        env = folder / DIST
        if name == version and env_python(env).exists():
            found.append((not leftover, generation, env))
    return [env for *_key, env in sorted(found, key=lambda item: (item[0], item[1]), reverse=True)]


def same_filesystem(tools: Path | None = None) -> bool:
    """Can the tool path be switched by rename onto the versions folder?"""
    tools = tools or tool_dir()
    try:
        root = versions_root(tools)
        root.mkdir(parents=True, exist_ok=True)
        return os.stat(root).st_dev == os.stat(tools).st_dev
    except OSError:
        return False


def usable(tools: Path | None = None) -> bool:
    """Is the side-by-side layout usable here: a uv tool env (a folder or our
    symlink) at the tool path, and the versions folder on its filesystem?"""
    if os.name == "nt":
        # Not yet: the first switch moves the folder the running CLI (and the
        # service) run from, which Windows refuses while they run. Windows
        # updates in place, through the CLI's own updater, as before.
        return False
    tools = tools or tool_dir()
    env = tool_env(tools)
    return (is_link(env) or env.is_dir()) and same_filesystem(tools)


def running_from_versions(prefix: str | None = None) -> bool:
    """Does this interpreter run from a version env (`probe-versions/<v>/...`)?"""
    text = (prefix if prefix is not None else sys.prefix).replace(os.sep, "/")
    return f"/{VERSIONS_DIRNAME}/" in text


def versions_root_of(prefix: str | None = None) -> Path | None:
    """The versions folder this interpreter runs from (`probe-versions/<v>/probe-research`'s
    grandparent), or None when it does not run from a version env. No `uv` asked."""
    path = Path(prefix if prefix is not None else sys.prefix)
    if not running_from_versions(str(path)):
        return None
    for parent in path.parents:
        if parent.name == VERSIONS_DIRNAME:
            return parent
    return None
from probe.shared.updates.installs.link import env_python, is_link  # noqa: E402 -- pieces need each other; the front door loads this one first
