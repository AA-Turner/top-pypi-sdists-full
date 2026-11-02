"""Copy planned injection sources and derive manifest descriptions."""

from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path

from agentic_devtools.skill_injector_markdown import _extract_description, _parse_frontmatter
from agentic_devtools.skill_injector_paths import _SKILL_ENTRY_FILE, _SKILLS_KIND, _resolve_skill_target_path


def _copy_destination(src: Path, dest: Path, newly_created: list[Path]) -> None:
    """Copy a source file and remember destinations created by this operation."""
    existed_before = dest.exists()
    if not existed_before:
        newly_created.append(dest)
    shutil.copy2(src, dest)


def _copy_case_renamed_source(
    target_dir: Path,
    old_name: str,
    src: Path,
    dest: Path,
    newly_created: list[Path],
) -> None:
    """Use a temporary path for a case-only rename on case-insensitive filesystems."""
    old_path = _resolve_skill_target_path(target_dir, old_name)
    if not old_path.is_file() or old_path.is_symlink():
        _copy_destination(src, dest, newly_created)
        return

    tmp_cr_fd, tmp_cr_name = tempfile.mkstemp(dir=old_path.parent)
    os.close(tmp_cr_fd)
    os.replace(old_path, tmp_cr_name)
    try:
        shutil.copy2(src, dest)
    except Exception:
        try:
            os.replace(tmp_cr_name, old_path)
        except OSError:
            # Best-effort rollback: preserve and re-raise the original copy failure.
            pass
        raise
    else:
        try:
            os.unlink(tmp_cr_name)
        except OSError:  # pragma: no cover
            pass


def _copy_origin(
    kind: str,
    target_dir: Path,
    flat_name: str,
    src: Path,
    case_rename_old_name: str | None,
    newly_created: list[Path],
) -> None:
    """Copy one planned source unless it already resolves to its destination."""
    dest = _resolve_skill_target_path(target_dir, flat_name) if kind == _SKILLS_KIND else target_dir / flat_name
    dest.parent.mkdir(parents=True, exist_ok=True)
    if src.resolve() == dest.resolve():
        return
    if kind == _SKILLS_KIND and case_rename_old_name is not None:
        _copy_case_renamed_source(target_dir, case_rename_old_name, src, dest, newly_created)
    else:
        _copy_destination(src, dest, newly_created)


def _describe_origin(
    src: Path,
    kind: str,
    fm_cache: dict[Path, dict[str, object]],
) -> tuple[str, bool]:
    """Return the manifest description and whether source text was readable."""
    if src in fm_cache:
        return _extract_description(fm_cache[src], kind), True
    if kind == _SKILLS_KIND and src.name != _SKILL_ENTRY_FILE:
        return src.name, True
    try:
        content = src.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return "Non-UTF-8 source; description unavailable.", False
    return _extract_description(_parse_frontmatter(content), kind), True
