"""Build flat-kind source selections and plans before any writes."""

from __future__ import annotations

import warnings
from collections.abc import Callable
from pathlib import Path

from agentic_devtools.skill_classification import parse_classification, should_inject
from agentic_devtools.skill_injector_discovery import _list_md_files
from agentic_devtools.skill_injector_markdown import _parse_frontmatter
from agentic_devtools.skill_injector_models import InjectionPlan
from agentic_devtools.skill_injector_paths import _MANAGED_PREFIX, _MANAGED_README, _SPECKIT_PREFIX, _flatten_filename
from agentic_devtools.skill_injector_planning import _plan_kind


def _prepare_flat_kind(
    kind: str,
    source_dir: Path,
    target_dir: Path,
    *,
    issue_adapter: str | None,
    code_hosting: str | None,
    on_counts: Callable[[int, int], None] | None = None,
) -> tuple[InjectionPlan, dict[str, Path], dict[Path, dict[str, object]], int]:
    """Select, filter, and plan the flat agent/prompt resources for one kind."""
    source_files = _list_md_files(source_dir, kind)
    source_files = [p for p in source_files if p.relative_to(source_dir) != Path(_MANAGED_README)]
    source_files = [p for p in source_files if not p.name.startswith(_SPECKIT_PREFIX)]
    source_files = [p for p in source_files if p.name.startswith(_MANAGED_PREFIX)]

    fm_cache: dict[Path, dict[str, object]] = {}
    pruned = 0
    if issue_adapter is not None or code_hosting is not None:
        pre_filter_count = len(source_files)
        filtered: list[Path] = []
        for src in source_files:
            try:
                content = src.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                filtered.append(src)
                continue
            fm = _parse_frontmatter(content)
            if should_inject(parse_classification(fm), issue_adapter=issue_adapter, code_hosting=code_hosting):
                fm_cache[src] = fm
                filtered.append(src)
        source_files = filtered
        pruned = pre_filter_count - len(source_files)
    if on_counts is not None:
        on_counts(0, pruned)

    source_rel_names: set[str] = set()
    flat_name_origins: dict[str, Path] = {}
    casefold_to_flat: dict[str, str] = {}
    for src in source_files:
        flat_name = _flatten_filename(src.relative_to(source_dir))
        key = flat_name.casefold()
        prev_flat = casefold_to_flat.get(key)
        if prev_flat is not None and prev_flat != flat_name:
            warnings.warn(
                f"agentic-devtools: duplicate flat filename {flat_name!r} "
                f"(case-insensitive match of {prev_flat!r}) "
                f"from {src!s} (first seen from {flat_name_origins[prev_flat]!s}); "
                "only the last source will be injected on case-insensitive filesystems.",
                RuntimeWarning,
            )
            flat_name_origins.pop(prev_flat, None)
            source_rel_names.discard(prev_flat)
        elif flat_name in flat_name_origins:
            warnings.warn(
                f"agentic-devtools: duplicate flat filename {flat_name!r} "
                f"from {src!s} (first seen from {flat_name_origins[flat_name]!s}); "
                "only the last source will be injected.",
                RuntimeWarning,
            )
        casefold_to_flat[key] = flat_name
        flat_name_origins[flat_name] = src
        source_rel_names.add(flat_name)

    if on_counts is not None:
        on_counts(len(flat_name_origins), 0)
    plan = _plan_kind(kind, target_dir, flat_name_origins)
    return plan, flat_name_origins, fm_cache, pruned
