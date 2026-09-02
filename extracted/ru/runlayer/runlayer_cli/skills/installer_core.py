"""Anyio-free filesystem + lockfile primitives for skill installation.

Split from ``installer.py`` so the ``aiwatch`` PyInstaller bundle (which
excludes ``anyio``) can reconcile managed skills via ``device_sync.py``.
``installer.py`` keeps the anyio orchestration (``install_skills`` /
``update_skills`` / ``uninstall_skill``) and re-exports everything here, so
existing importers are unaffected.

Import closure contract: stdlib + ``yaml`` + ``pydantic`` only (plus the
stdlib-only ``skills.frontmatter`` sibling). No ``anyio``, no
``metrics_flush``, no ``api``.
"""

from __future__ import annotations

import datetime
import glob
import os
import shutil
import stat
import tempfile
import time
from collections.abc import Callable, Sequence
from pathlib import Path, PurePosixPath
from typing import Protocol, TypeVar

import yaml
from pydantic import BaseModel, ValidationError

from runlayer_cli.skills.frontmatter import rewrite_skill_frontmatter_name
from runlayer_cli.skills.marker import (
    CANONICAL_BASE,
    INSTALLED_MARKER,
    SKILLS_DIR_MAP,
)

LOCKFILE = "skill-lock.yml"


class SkillFilePayload(Protocol):
    """Any file object with a relative title and full content."""

    title: str
    content: str


def _sanitize_name(name: str) -> str:
    """Validate that *name* is a safe relative path component.

    Rejects absolute paths, ``..`` traversal, and empty/dot-only values.
    Returns *name* unchanged when valid.
    """
    p = PurePosixPath(name)
    if (
        not name
        or p.is_absolute()
        or ".." in p.parts
        or p == PurePosixPath(".")
        or "\\" in name
    ):
        raise ValueError(f"invalid skill path component: {name!r}")
    return name


class LockEntry(BaseModel):
    name: str
    id: str
    namespace: str | None = None
    updated_at: datetime.datetime | None = None
    identifier: str | None = None
    client: str = "claude_code"


def resolve_dirs(
    client_name: str, global_install: bool, cwd: Path
) -> tuple[Path, Path, Path]:
    project_rel, global_rel = SKILLS_DIR_MAP[client_name]
    if global_install:
        home = Path.home()
        canonical = home / CANONICAL_BASE
        editor = home / global_rel
        lockfile = home / ".runlayer" / LOCKFILE
    else:
        canonical = cwd / CANONICAL_BASE
        editor = cwd / project_rel
        lockfile = cwd / ".runlayer" / LOCKFILE
    return canonical, editor, lockfile


LockEntryT = TypeVar("LockEntryT", bound=BaseModel)


def read_lock_entries(
    path: Path,
    model: type[LockEntryT],
    *,
    preprocess: Callable[[dict], dict] | None = None,
) -> list[LockEntryT]:
    """Shared YAML lock-list parser for the user and managed lockfiles."""
    if not path.exists():
        return []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (yaml.YAMLError, OSError) as e:
        raise ValueError(f"invalid lockfile YAML: {e}") from e
    if not data or "skills" not in data:
        return []
    raw_entries = data["skills"]
    if not isinstance(raw_entries, list):
        raise ValueError("invalid lockfile format: 'skills' must be a list")

    parsed: list[LockEntryT] = []
    for i, item in enumerate(raw_entries):
        if not isinstance(item, dict):
            raise ValueError(f"invalid lockfile entry at index {i}: expected mapping")
        if preprocess is not None:
            item = preprocess(item)
        try:
            parsed.append(model.model_validate(item))
        except ValidationError as e:
            raise ValueError(f"invalid lockfile entry at index {i}: {e}") from e
    return parsed


def write_lock_entries(
    path: Path, entries: Sequence[BaseModel], *, header: str
) -> None:
    """Atomically write a lock-list (torn writes would orphan install state).

    The tmp file is unique per writer: overlapping reconciles (manual sync vs
    launchd tick) must not truncate each other's staging mid-``os.replace``.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "skills": [e.model_dump(mode="json") for e in entries],
    }
    fd, tmp_name = tempfile.mkstemp(
        prefix=f"{path.name}.", suffix=".tmp", dir=path.parent
    )
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(f"# managed by: {header}\n" + yaml.dump(data, sort_keys=False))
        os.replace(tmp, path)
    except OSError:
        tmp.unlink(missing_ok=True)
        raise


def _legacy_default_client(item: dict) -> dict:
    if "client" not in item:
        return {**item, "client": "claude_code"}
    return item


def read_lockfile(path: Path) -> list[LockEntry]:
    return read_lock_entries(path, LockEntry, preprocess=_legacy_default_client)


def _write_lockfile(path: Path, entries: list[LockEntry]) -> None:
    write_lock_entries(path, entries, header="runlayer skills add")


def _is_junction(path: Path) -> bool:
    """Windows junction (or any non-symlink reparse point) at *path*.

    A junction has ``is_symlink() == False``, yet file access *follows* the
    reparse point into the target: reading ``<path>/.installed`` on a junction
    aimed at the canonical skill dir returns the canonical managed marker, so
    marker-based ownership checks would misclassify the junction as our
    copy-mode entry — and ``shutil.rmtree`` on it (pre-3.13) can recurse
    through into the canonical tree and delete it. Such entries are foreign:
    never read markers through them, never remove or refresh them, never copy
    through them. Always ``False`` off Windows (``st_file_attributes`` doesn't
    exist there).
    """
    try:
        path_stat = os.lstat(path)
    except OSError:
        return False
    attributes = getattr(path_stat, "st_file_attributes", 0)
    has_reparse_point = bool(
        attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    )
    return has_reparse_point and not stat.S_ISLNK(path_stat.st_mode)


def _links_and_junctions(dirpath: str, names: list[str]) -> set[str]:
    """``shutil.copytree`` ignore callable: skip symlinks and junctions.

    copytree follows file symlinks (default ``symlinks=False``) and descends
    junction dirs, so a link planted inside a managed skill dir would pull
    its target's content into the editor copy — leaking foreign files and
    making the copy hash drift from the install-time baseline (restore
    thrash). Managed installs are written from wire content and never contain
    links, so anything link-shaped is foreign and skipped. Must mirror the
    walk-skip in ``device_sync._compute_dir_identifier`` so a clean copy
    hashes identical to its canonical dir.
    """
    skipped: set[str] = set()
    for name in names:
        p = Path(dirpath) / name
        if p.is_symlink() or _is_junction(p):
            skipped.add(name)
    return skipped


_COPY_STAGING_INFIX = ".rl-copy-"
# Staging siblings younger than this are presumed to belong to a live
# concurrent run (manual sync overlapping a packaged scheduler tick)
# and are left alone; older ones are crashed-run leftovers.
_COPY_STAGING_MAX_AGE_SECONDS = 3600.0


def link_or_copy_skill_dir(src: Path, dest: Path) -> None:
    """Symlink ``dest`` -> ``src``; fall back to an atomic full copy.

    Windows non-elevated users without Developer Mode can't create symlinks
    (the norm on managed fleets). The copy is staged into a temp sibling and
    renamed into place so a killed process can never leave a partial dir at
    ``dest`` — a partial without its marker would look user-owned to the
    reconciler and be skipped forever. ``dest`` must not exist. Updates
    re-run remove+write+link, so the lockfile identifier still drives drift
    detection and the copy is refreshed on every update.
    """
    rel = os.path.relpath(src, dest.parent)
    try:
        dest.symlink_to(rel, target_is_directory=True)
        return
    except OSError:
        pass
    # Stale staging siblings are ours by construction (reserved infix), but
    # only clear crashed-run leftovers — a recent sibling may be a live
    # concurrent run's in-flight copy (same age-gate model as the canonical
    # reconcile staging).
    now = time.time()
    for stale in dest.parent.glob(f".{glob.escape(dest.name)}{_COPY_STAGING_INFIX}*"):
        try:
            if now - stale.stat().st_mtime > _COPY_STAGING_MAX_AGE_SECONDS:
                shutil.rmtree(stale, ignore_errors=True)
        except OSError:
            continue
    staging = Path(
        tempfile.mkdtemp(prefix=f".{dest.name}{_COPY_STAGING_INFIX}", dir=dest.parent)
    )
    try:
        staged = staging / dest.name
        shutil.copytree(src, staged, ignore=_links_and_junctions)
        os.rename(staged, dest)
    finally:
        shutil.rmtree(staging, ignore_errors=True)


def _symlink_skill(canonical_dir: Path, editor_dir: Path, skill_name: str) -> None:
    _sanitize_name(skill_name)
    src = canonical_dir / skill_name
    dest = editor_dir / skill_name
    if src == dest:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_symlink():
        dest.unlink()
    elif dest.exists():
        if dest.is_dir():
            shutil.rmtree(dest)
        else:
            dest.unlink()
    link_or_copy_skill_dir(src, dest)


def _write_skill_files(
    canonical_dir: Path, skill_name: str, files: Sequence[SkillFilePayload]
) -> None:
    _sanitize_name(skill_name)
    skill_dir = canonical_dir / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / INSTALLED_MARKER).write_text("", encoding="utf-8")
    for f in files:
        _sanitize_name(f.title)
        fpath = skill_dir / PurePosixPath(f.title)
        fpath.parent.mkdir(parents=True, exist_ok=True)
        content = f.content
        if f.title == "SKILL.md":
            content = rewrite_skill_frontmatter_name(
                content,
                skill_name,
                fallback_description="Runlayer skill.",
            )
        fpath.write_text(content, encoding="utf-8")


def _remove_skill_files(
    canonical_dir: Path,
    editor_dir: Path,
    skill_name: str,
    *,
    remove_canonical: bool = True,
) -> None:
    _sanitize_name(skill_name)
    if remove_canonical:
        skill_dir = canonical_dir / skill_name
        if skill_dir.exists():
            shutil.rmtree(skill_dir)

    if canonical_dir != editor_dir:
        link = editor_dir / skill_name
        if link.is_symlink():
            link.unlink()
        elif link.exists():
            shutil.rmtree(link)
