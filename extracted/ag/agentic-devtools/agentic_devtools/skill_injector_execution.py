"""Execute a planned kind and roll back newly created files on write failure."""

from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path

from agentic_devtools.skill_injector_execution_copy import _copy_origin, _describe_origin
from agentic_devtools.skill_injector_markdown import _generate_readme
from agentic_devtools.skill_injector_models import InjectionPlan
from agentic_devtools.skill_injector_paths import (
    _LEGACY_AGDT_ENTRY,
    _MANAGED_README,
    _SKILLS_KIND,
    _resolve_skill_target_path,
)


def _remove_legacy_directory(plan: InjectionPlan, target_dir: Path) -> None:
    """Remove a previous .agdt directory or symlink when migration is planned."""
    if _LEGACY_AGDT_ENTRY not in plan.deleted:
        return
    old_agdt = target_dir / ".agdt"
    if old_agdt.is_symlink():
        old_agdt.unlink()
    elif old_agdt.is_dir():
        shutil.rmtree(old_agdt)


def _remove_stale_entries(plan: InjectionPlan, target_dir: Path) -> None:
    """Remove planned stale paths and any newly empty skill directory."""
    for stale_name in plan.deleted:
        if stale_name == _LEGACY_AGDT_ENTRY:
            continue
        stale_path = (
            _resolve_skill_target_path(target_dir, stale_name) if plan.kind == _SKILLS_KIND else target_dir / stale_name
        )
        stale_path.unlink()
        stale_parent = stale_path.parent
        if stale_parent != target_dir and not any(stale_parent.iterdir()):
            stale_parent.rmdir()


def _write_manifest(target_dir: Path, manifest: list[tuple[str, str]], kind: str) -> None:
    """Atomically replace the managed manifest for one kind."""
    readme_path = target_dir / _MANAGED_README
    if kind == _SKILLS_KIND and readme_path.is_symlink():  # pragma: no cover
        raise OSError(f"Refusing to write skills manifest through symlink: {readme_path!s}")
    readme_content = _generate_readme(manifest, kind)
    tmp_fd, tmp_name = tempfile.mkstemp(dir=target_dir, prefix=".agdt.README.", suffix=".tmp")
    tmp_replaced = False
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as fh:
            fh.write(readme_content)
        os.replace(tmp_name, readme_path)
        tmp_replaced = True
    finally:
        if not tmp_replaced:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass


def _rollback_new_files(newly_created: list[Path], target_dir: Path) -> None:
    """Remove files created by a failed injection and prune their empty folders."""
    for new_file in newly_created:
        try:
            new_file.unlink()
        except OSError:
            # Best-effort rollback: ignore missing/inaccessible files and continue cleanup.
            pass
        stale_parent = new_file.parent
        while stale_parent != target_dir:
            try:
                stale_parent.rmdir()
            except OSError:
                break
            stale_parent = stale_parent.parent


def _execute_plan(
    plan: InjectionPlan,
    target_dir: Path,
    origins: dict[str, Path],
    fm_cache: dict[Path, dict[str, object]],
) -> bool:
    """Write one planned kind, returning false only for non-UTF-8 descriptions."""
    kind = plan.kind
    target_dir.mkdir(parents=True, exist_ok=True)
    _remove_legacy_directory(plan, target_dir)
    case_rename_new_to_old = {new: old for old, new in plan.case_renames}
    newly_created: list[Path] = []
    overall_success = True
    try:
        manifest: list[tuple[str, str]] = []
        for flat_name, src in origins.items():
            _copy_origin(
                kind,
                target_dir,
                flat_name,
                src,
                case_rename_new_to_old.get(flat_name),
                newly_created,
            )
            desc, readable = _describe_origin(src, kind, fm_cache)
            overall_success = readable and overall_success
            manifest.append((flat_name, desc))

        _remove_stale_entries(plan, target_dir)
        _write_manifest(target_dir, manifest, kind)
    except OSError:
        _rollback_new_files(newly_created, target_dir)
        raise
    return overall_success
