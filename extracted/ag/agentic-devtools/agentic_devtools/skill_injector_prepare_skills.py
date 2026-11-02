"""Build the directory-shaped skill selection and plan."""

from __future__ import annotations

import warnings
from collections.abc import Callable
from pathlib import Path, PurePosixPath

from agentic_devtools.skill_injector_discovery import _read_managed_skill_manifest, _select_skill_sources
from agentic_devtools.skill_injector_models import InjectionPlan
from agentic_devtools.skill_injector_paths import (
    _SHARED_SKILL_RESOURCES,
    _SKILL_ENTRY_FILE,
    _resolve_skill_target_path,
    _validate_skills_target_dir,
)


def _prepare_skills_kind(
    source_dir: Path,
    target_dir: Path,
    *,
    issue_adapter: str | None,
    code_hosting: str | None,
    plan_skills_kind: Callable[[Path, dict[str, Path]], InjectionPlan],
    on_counts: Callable[[int, int], None] | None = None,
) -> tuple[InjectionPlan, dict[str, Path], dict[Path, dict[str, object]], int, int, bool]:
    """Select skills, protect consumer content, and plan the skill tree."""
    skill_origins, skill_fm_cache, skill_pruned = _select_skill_sources(
        source_dir, issue_adapter=issue_adapter, code_hosting=code_hosting
    )
    if on_counts is not None:
        on_counts(0, skill_pruned)
    _validate_skills_target_dir(target_dir)
    managed_before = _read_managed_skill_manifest(target_dir)
    managed_skills = {PurePosixPath(name).parts[0] for name in managed_before if len(PurePosixPath(name).parts) == 2}
    managed_before_casefolds = {name.casefold(): name for name in managed_before}
    colliding_skills = _find_colliding_skills(
        target_dir,
        skill_origins,
        managed_before,
        managed_skills,
        managed_before_casefolds,
    )
    skill_origins, skill_fm_cache, selected_skill_count, shared_resource_collision = _filter_colliding_skills(
        target_dir,
        skill_origins,
        skill_fm_cache,
        managed_before,
        colliding_skills,
    )
    if on_counts is not None:
        on_counts(selected_skill_count, 0)
    plan = plan_skills_kind(target_dir, skill_origins)
    return plan, skill_origins, skill_fm_cache, selected_skill_count, skill_pruned, shared_resource_collision


def _find_colliding_skills(
    target_dir: Path,
    skill_origins: dict[str, Path],
    managed_before: set[str],
    managed_skills: set[str],
    managed_before_casefolds: dict[str, str],
) -> set[str]:
    """Find skill names whose target paths contain unmanaged consumer content."""
    colliding_skills: set[str] = set()
    for name in skill_origins:
        if len(PurePosixPath(name).parts) == 1:
            dest = _resolve_skill_target_path(target_dir, name)
            if name not in managed_before and dest.exists():
                colliding_skills.add(name)
            continue
        skill_name = PurePosixPath(name).parts[0]
        dest = _resolve_skill_target_path(target_dir, name)
        not_in_manifest = name not in managed_before
        if not_in_manifest:
            name_cf = name.casefold()
            if name_cf in managed_before_casefolds:
                prior_spelling = managed_before_casefolds[name_cf]
                try:
                    prior_dest = _resolve_skill_target_path(target_dir, prior_spelling)
                    ds = dest.stat()
                    ps = prior_dest.stat()
                    if ds.st_ino == ps.st_ino and ds.st_dev == ps.st_dev:
                        not_in_manifest = False
                except OSError:
                    # If either path cannot be stat'ed (e.g., removed concurrently or inaccessible),
                    # we cannot prove inode-equivalence; keep the conservative default.
                    pass
        if (skill_name not in managed_skills and dest.parent.exists()) or (not_in_manifest and dest.exists()):
            colliding_skills.add(skill_name)
    return colliding_skills


def _filter_colliding_skills(
    target_dir: Path,
    skill_origins: dict[str, Path],
    skill_fm_cache: dict[Path, dict[str, object]],
    managed_before: set[str],
    colliding_skills: set[str],
) -> tuple[dict[str, Path], dict[Path, dict[str, object]], int, bool]:
    """Exclude consumer-colliding bundled skills and preserve their managed files."""
    if not colliding_skills:
        selected_count = _count_selected_skills(skill_origins)
        return skill_origins, skill_fm_cache, selected_count, False

    shared_collisions = colliding_skills & _SHARED_SKILL_RESOURCES
    if shared_collisions and any(len(PurePosixPath(name).parts) > 1 for name in skill_origins):
        warnings.warn(
            "agentic-devtools: refusing to inject bundled skills because "
            "a shared resource collides with a consumer-authored file: "
            f"{', '.join(sorted(shared_collisions))}",
            RuntimeWarning,
        )
        selected_count = _count_selected_skills(skill_origins)
        return skill_origins, skill_fm_cache, selected_count, True

    warnings.warn(
        "agentic-devtools: skipping bundled skills that collide with "
        "consumer-authored files not listed in the previous managed "
        f"manifest: {', '.join(sorted(colliding_skills))}",
        RuntimeWarning,
    )
    skill_origins = {
        name: src for name, src in skill_origins.items() if PurePosixPath(name).parts[0] not in colliding_skills
    }
    allowed_sources = set(skill_origins.values())
    skill_fm_cache = {src: fm for src, fm in skill_fm_cache.items() if src in allowed_sources}
    selected_count = _count_selected_skills(skill_origins)
    for managed_name in sorted(managed_before):
        if PurePosixPath(managed_name).parts[0] not in colliding_skills:
            continue
        managed_dest = _resolve_skill_target_path(target_dir, managed_name)
        if managed_dest.is_file():
            skill_origins[managed_name] = managed_dest

    return skill_origins, skill_fm_cache, selected_count, False


def _count_selected_skills(skill_origins: dict[str, Path]) -> int:
    """Count selected skill entries before preserving prior managed files."""
    return len({PurePosixPath(name).parts[0] for name, src in skill_origins.items() if src.name == _SKILL_ENTRY_FILE})
