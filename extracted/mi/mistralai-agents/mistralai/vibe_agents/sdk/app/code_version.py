"""The code that declares an agent's configuration, so that a restart of the same code keeps its agent.

`AGENTS_SDK_CODE_VERSION` names it when the operator sets it, for example to the commit an image was
built from. Otherwise the SDK hashes the project: the files git lists (tracked, and untracked but not
ignored), or every file except virtual environments and caches when the project is not in git. The files
of each local skill are hashed wherever they live. Code outside the project, such as an installed
package, is not seen.

Any doubt gives no code version, and the control plane then stores a new snapshot at every start: a
missing version only costs a snapshot, while a wrong one would hide a code change.
"""

import base64
import hashlib
import logging
import os
import shutil
import subprocess
import time
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from mistralai.vibe_agents.sdk.app import config
from mistralai.vibe_agents.sdk.app.loader import AgentApp

logger = logging.getLogger(__name__)

_MAX_FILES = 20_000
_MAX_BYTES = 256 * 1024 * 1024
_MAX_SECONDS = 10.0
_CHUNK_BYTES = 1024 * 1024
# The longest code version the control plane takes.
_MAX_VERSION_LENGTH = 255
_GIT_TIMEOUT_SECONDS = 5.0
_SKIPPED_DIRECTORIES = frozenset(
    {".git", ".venv", "venv", "__pycache__", "node_modules", ".mypy_cache", ".pytest_cache", ".ruff_cache", ".tox"}
)
_SKIPPED_SUFFIXES = (".pyc", ".pyo")


@dataclass(frozen=True, slots=True)
class CodeIdentity:
    version: str
    source: Literal["explicit", "computed"]


class _NotComputedError(Exception):
    pass


def code_identity(app: AgentApp) -> CodeIdentity | None:
    """The code version to send with the agent's configuration, or None when it is not known."""
    explicit = config.ControlPlaneSettings().code_version.strip()
    if len(explicit) > _MAX_VERSION_LENGTH:
        logger.warning(
            "AGENTS_SDK_CODE_VERSION holds %d characters, more than the %d the control plane takes. "
            "No code version is sent, so each start stores a new snapshot.",
            len(explicit),
            _MAX_VERSION_LENGTH,
        )
        return None
    if explicit:
        return CodeIdentity(version=explicit, source="explicit")
    try:
        digest = _project_digest(Path(app.root), _local_skill_files(app.harness))
    except (_NotComputedError, OSError, subprocess.SubprocessError, ValueError) as exc:
        logger.warning(
            "The code version of the project was not computed (%s), so each start stores a new snapshot. "
            "Set AGENTS_SDK_CODE_VERSION, for example to the commit the image is built from.",
            exc,
        )
        return None
    return CodeIdentity(version=f"sha256:{digest}", source="computed")


def _project_digest(root: Path, skill_files: list[tuple[str, bytes]]) -> str:
    if not root.is_dir():
        raise _NotComputedError(f"{root} is not a directory")
    deadline = time.monotonic() + _MAX_SECONDS
    hasher = hashlib.sha256()
    total_bytes = 0
    for relative in sorted(_project_files(root, deadline)):
        _check_deadline(deadline)
        path = root / relative
        # A file git still tracks may be deleted, and a submodule is listed as a directory.
        if not path.is_file():
            continue
        # The limits apply before a file is read, so one large file cannot exhaust the worker's memory.
        size = path.stat().st_size
        total_bytes += size
        if total_bytes > _MAX_BYTES:
            raise _NotComputedError(f"the project holds more than {_MAX_BYTES} bytes")
        _add_file(hasher, relative, path, size, deadline)
    for name, content in skill_files:
        _add(hasher, "skill", name, content)
    return hasher.hexdigest()


def _add(hasher: "hashlib._Hash", kind: str, name: str, content: bytes) -> None:
    # Length-prefixed, so that two different file sets never hash the same bytes.
    hasher.update(f"{kind}\0{name}\0{len(content)}\0".encode())
    hasher.update(content)


def _add_file(hasher: "hashlib._Hash", name: str, path: Path, size: int, deadline: float) -> None:
    """Hash the file as ``_add`` would hash its content, in chunks of constant memory."""
    hasher.update(f"project\0{name}\0{size}\0".encode())
    # One byte past ``size`` shows a file that grew after its size was read.
    remaining = size + 1
    with path.open("rb") as file:
        while remaining and (chunk := file.read(min(_CHUNK_BYTES, remaining))):
            _check_deadline(deadline)
            remaining -= len(chunk)
            hasher.update(chunk)
    if remaining != 1:
        raise _NotComputedError(f"{name} changed while the project was hashed")


def _check_deadline(deadline: float) -> None:
    if time.monotonic() > deadline:
        raise _NotComputedError(f"hashing the project took more than {_MAX_SECONDS:.0f}s")


def _project_files(root: Path, deadline: float) -> list[str]:
    listed = _git_files(root)
    files = list(_walked_files(root, deadline)) if listed is None else [p for p in listed if not _is_skipped(p)]
    if len(files) > _MAX_FILES:
        raise _NotComputedError(f"the project holds more than {_MAX_FILES} files")
    return files


def _git_files(root: Path) -> list[str] | None:
    """The files git lists under ``root``, relative to it, or None when ``root`` is not in a git checkout."""
    git = shutil.which("git")
    if git is None:
        return None
    inside = subprocess.run(  # noqa: S603 - fixed arguments, no shell
        [git, "-C", str(root), "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
        check=False,
        timeout=_GIT_TIMEOUT_SECONDS,
    )
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        return None
    listed = subprocess.run(  # noqa: S603 - fixed arguments, no shell
        [git, "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", "."],
        capture_output=True,
        check=True,
        timeout=_GIT_TIMEOUT_SECONDS,
    )
    # A path git lists twice, staged and modified, is one file. A project that git ignores lists nothing,
    # and is walked like one outside git.
    files = sorted({path for path in listed.stdout.decode("utf-8", "surrogateescape").split("\0") if path})
    return files or None


def _walked_files(root: Path, deadline: float) -> Iterator[str]:
    count = 0
    for directory, subdirectories, files in os.walk(root):
        subdirectories[:] = [name for name in subdirectories if name not in _SKIPPED_DIRECTORIES]
        for name in files:
            if name.endswith(_SKIPPED_SUFFIXES):
                continue
            count += 1
            if count > _MAX_FILES:
                raise _NotComputedError(f"the project holds more than {_MAX_FILES} files")
            if time.monotonic() > deadline:
                raise _NotComputedError(f"listing the project took more than {_MAX_SECONDS:.0f}s")
            yield Path(directory, name).relative_to(root).as_posix()


def _is_skipped(relative: str) -> bool:
    parts = relative.split("/")
    return any(part in _SKIPPED_DIRECTORIES for part in parts[:-1]) or parts[-1].endswith(_SKIPPED_SUFFIXES)


def _local_skill_files(harness: object) -> list[tuple[str, bytes]]:
    from mistralai.vibe_agents.sdk.authoring.contracts import LocalSkillBundle  # noqa: PLC0415

    files: list[tuple[str, bytes]] = []
    for index, bundle in enumerate(getattr(harness, "skills", ())):
        if not isinstance(bundle, LocalSkillBundle):
            continue
        files.extend((f"{index}/{file.path}", base64.b64decode(file.content_base64)) for file in bundle.files)
    return sorted(files)
