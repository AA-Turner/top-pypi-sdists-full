"""Source discovery and managed-skill manifest reading."""

from __future__ import annotations

import warnings
from pathlib import Path

from agentic_devtools.skill_classification import parse_classification, should_inject
from agentic_devtools.skill_injector_markdown import _parse_frontmatter
from agentic_devtools.skill_injector_paths import (
    _MANAGED_README,
    _MANIFEST_ROW_RE,
    _SHARED_SKILL_RESOURCES,
    _SKILL_ENTRY_FILE,
    _SKILLS_MANIFEST_MARKER,
    _is_managed_skill_relative_path,
    _is_supported_skill_resource_name,
)


def _list_md_files(source_dir: Path, kind: str) -> list[Path]:
    """Return the ``.md`` files that should be injected for *kind*.

    Uses ``rglob`` so that future subdirectory structures are preserved.

    * ``agents`` → all non-hidden ``*.md`` files (excluding hidden files/dirs).
    * ``prompts`` → only ``*.prompt.md`` files (excluding hidden files/dirs).
    """
    if kind == "agents":
        return sorted(
            p
            for p in source_dir.rglob("*.md")
            if p.is_file() and not any(part.startswith(".") for part in p.relative_to(source_dir).parts)
        )
    # prompts
    return sorted(
        p
        for p in source_dir.rglob("*.prompt.md")
        if p.is_file() and not any(part.startswith(".") for part in p.relative_to(source_dir).parts)
    )


def _should_include_skill(
    entry: Path,
    *,
    filtering: bool,
    issue_adapter: str | None,
    code_hosting: str | None,
    fm_cache: dict[Path, dict[str, object]],
) -> bool:
    """Return whether a skill passes classification filtering."""
    if not filtering:
        return True
    try:
        content = entry.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return True
    fm = _parse_frontmatter(content)
    if not should_inject(
        parse_classification(fm),
        issue_adapter=issue_adapter,
        code_hosting=code_hosting,
    ):
        return False
    fm_cache[entry] = fm
    return True


def _find_resource_name_collision(resources: list[Path]) -> tuple[str, str] | None:
    """Return prior and current names when resources collide by case-folding."""
    seen_cf: dict[str, str] = {_SKILL_ENTRY_FILE.casefold(): _SKILL_ENTRY_FILE}
    for resource in resources:
        folded_name = resource.name.casefold()
        if folded_name in seen_cf:
            return seen_cf[folded_name], resource.name
        seen_cf[folded_name] = resource.name
    return None


def _select_skill_sources(
    source_dir: Path,
    *,
    issue_adapter: str | None,
    code_hosting: str | None,
) -> tuple[dict[str, Path], dict[Path, dict[str, object]], int]:
    """Select the skill files to mirror from *source_dir*.

    A skill is a non-hidden directory directly under *source_dir* that holds a
    ``SKILL.md`` entry file.  Its entry file plus every non-hidden file one
    level deep inside it are mirrored.  Explicitly supported shared resources
    at the source root are mirrored as well.  Directory names are preserved
    verbatim — never flattened — because a dot in a skill name makes the skill
    silently fail to load.

    The classification filter runs over each skill's ``SKILL.md`` exactly as it
    runs over the flat kinds, and prunes the **whole** skill (entry file and
    resources) when the declared axes do not match the consumer.  Filtering is
    skipped entirely when neither axis is resolved (legacy inject-all).

    Args:
        source_dir: The packaged/checked-out skills tree.
        issue_adapter: Resolved issue adapter, or ``None`` when unrestricted.
        code_hosting: Resolved code hosting platform, or ``None`` when unrestricted.

    Returns:
        A ``(origins, fm_cache, pruned)`` tuple where *origins* maps the
        repo-relative POSIX destination path (e.g. ``my-skill/SKILL.md``) to its
        source file, *fm_cache* holds already-parsed ``SKILL.md`` front-matter,
        and *pruned* counts the skills removed by the classification filter.
    """
    origins: dict[str, Path] = {}
    fm_cache: dict[Path, dict[str, object]] = {}
    pruned = 0
    filtering = issue_adapter is not None or code_hosting is not None

    skill_dirs = sorted(
        p
        for p in source_dir.iterdir()
        if p.is_dir() and not p.name.startswith(".") and (p / _SKILL_ENTRY_FILE).is_file()
    )
    for skill_dir in skill_dirs:
        entry = skill_dir / _SKILL_ENTRY_FILE
        if not _should_include_skill(
            entry,
            filtering=filtering,
            issue_adapter=issue_adapter,
            code_hosting=code_hosting,
            fm_cache=fm_cache,
        ):
            pruned += 1
            continue

        resources = sorted(
            p
            for p in skill_dir.iterdir()
            if p.is_file() and p.name != _SKILL_ENTRY_FILE and _is_supported_skill_resource_name(p.name)
        )
        # Detect case-fold collisions among resources (e.g. Guide.md vs guide.md).
        # On a case-insensitive filesystem both would resolve to the same destination,
        # silently overwriting one.  Skip the entire skill to prevent silent data loss.
        collision = _find_resource_name_collision(resources)
        if collision is not None:
            prior_name, collision_name = collision
            warnings.warn(
                f"agentic-devtools: skipping skill '{skill_dir.name}' — "
                "resource name collision on a case-insensitive filesystem: "
                f"'{prior_name}' vs '{collision_name}'",
                RuntimeWarning,
            )
            continue
        for src in (entry, *resources):
            origins[src.relative_to(source_dir).as_posix()] = src

    for resource_name in sorted(_SHARED_SKILL_RESOURCES):
        resource = source_dir / resource_name
        if resource.is_file():
            origins[resource_name] = resource

    return origins, fm_cache, pruned


def _read_managed_skill_manifest(target_dir: Path) -> set[str]:
    """Return the skill paths recorded in *target_dir*'s managed manifest.

    The generated ``agdt.README.md`` is the record of what a previous injection
    wrote, so it is the only basis for stale cleanup of the directory-shaped
    kind: skills the consumer authored themselves are never listed there and
    therefore can never be deleted.  Only a *missing* manifest yields an empty
    set (first-run state); unreadable/non-UTF-8 or untrusted manifest content
    raises :class:`OSError` so callers abort without mutating files.

    Entries that do not have the shape ``<skill-name>/<resource>`` are ignored,
    which also rejects absolute paths and ``..`` segments.
    """
    manifest_path = target_dir / _MANAGED_README
    try:
        content = manifest_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return set()
    except (UnicodeDecodeError, OSError) as exc:
        raise OSError(f"Unreadable managed skills manifest: {manifest_path!s}") from exc
    if _SKILLS_MANIFEST_MARKER not in content:
        raise OSError(f"Refusing untrusted skills manifest without managed marker: {manifest_path!s}")
    return {
        match.group(1)
        for line in content.splitlines()
        if (match := _MANIFEST_ROW_RE.match(line)) and _is_managed_skill_relative_path(match.group(1))
    }
