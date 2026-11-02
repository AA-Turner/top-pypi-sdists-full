"""Manifest diff and safety planning for flat and directory-shaped resources."""

from __future__ import annotations

import warnings
from pathlib import Path

from agentic_devtools.skill_injector_discovery import _read_managed_skill_manifest
from agentic_devtools.skill_injector_models import InjectionPlan
from agentic_devtools.skill_injector_paths import (
    _LEGACY_AGDT_ENTRY,
    _MANAGED_PREFIX,
    _MANAGED_README,
    _SKILLS_KIND,
    _resolve_skill_target_path,
    _validate_skills_target_dir,
)


def _normalize_platform_arg(
    value: str | None,
    arg_name: str,
    valid_values: frozenset[str],
) -> str | None:
    """Normalize a platform argument to ``None`` if empty, whitespace, or unknown.

    Empty strings and whitespace-only strings are silently normalized to ``None``
    (unresolved / inject-all for that axis).

    Unknown (non-allowlist) values emit a :class:`RuntimeWarning` and are also
    normalized to ``None``, matching the "unresolved ⇒ inject-all" contract.
    This prevents callers that accidentally pass a stale or mis-spelled platform
    value from silently excluding or deleting constrained skill files.
    """
    if value is None:
        return None
    stripped = value.strip()
    if not stripped:
        return None
    if stripped not in valid_values:
        warnings.warn(
            f"inject_skills: unknown {arg_name} value {value!r}; "
            f"valid options are {sorted(valid_values)}. "
            "Treating as unresolved (inject-all for this axis).",
            RuntimeWarning,
            stacklevel=3,
        )
        return None
    return stripped


def _diff_against_target(
    target_dir: Path,
    origins: dict[str, Path],
) -> tuple[list[str], list[str]]:
    """Split *origins* into the entries to add and the entries to overwrite.

    An entry is an *add* when no file exists at the destination, and an
    *overwrite* when one exists with different bytes.  Identical bytes are
    reported as neither.
    """
    added: list[str] = []
    overwritten: list[str] = []
    for name, src in origins.items():
        dest = target_dir / name
        if not dest.is_file():
            added.append(name)
        elif src.read_bytes() != dest.read_bytes():
            overwritten.append(name)
    return added, overwritten


def _plan_kind(
    kind: str,
    target_dir: Path,
    flat_name_origins: dict[str, Path],
) -> InjectionPlan:
    """Compute the manifest diff for *kind* without writing anything.

    Args:
        kind: ``"agents"`` or ``"prompts"``.
        target_dir: Destination directory in the target repository.  It does
            not need to exist yet.
        flat_name_origins: Mapping of flattened destination filename → source
            file, as resolved by the selection and classification phases.

    Returns:
        An :class:`InjectionPlan` whose three lists are sorted for stable output.
    """
    added, overwritten = _diff_against_target(target_dir, flat_name_origins)

    deleted: list[str] = []
    managed_names_exact = set(flat_name_origins.keys())
    managed_name_casefolds = {name.casefold(): name for name in managed_names_exact}
    if target_dir.is_dir():
        for existing in target_dir.iterdir():
            if (
                existing.is_file()
                and existing.name.startswith(_MANAGED_PREFIX)
                and existing.name != _MANAGED_README
                and existing.name not in managed_names_exact
            ):
                # A case-only variant whose casefold matches a source name is
                # only suppressed when the target filesystem actually resolves
                # both spellings to the same file (i.e. case-insensitive).  On
                # case-sensitive filesystems the candidate path won't exist, so
                # stat() raises OSError and the variant is planned as stale.
                casefolded = existing.name.casefold()
                if casefolded in managed_name_casefolds:
                    source_spelling = managed_name_casefolds[casefolded]
                    suppressed = False
                    try:
                        existing_stat = existing.stat()
                        cand_stat = (target_dir / source_spelling).stat()
                        if cand_stat.st_ino == existing_stat.st_ino and cand_stat.st_dev == existing_stat.st_dev:
                            suppressed = True
                    except OSError:
                        # Expected when the alternate-cased candidate path does not
                        # resolve (e.g., case-sensitive filesystems) or metadata
                        # cannot be read; keep suppressed=False so this entry is
                        # treated as stale and planned for deletion.
                        suppressed = False
                    if suppressed:
                        continue
                deleted.append(existing.name)
    old_agdt = target_dir / ".agdt"
    if old_agdt.is_symlink() or old_agdt.is_dir():
        deleted.append(_LEGACY_AGDT_ENTRY)

    return InjectionPlan(
        kind=kind,
        added=tuple(sorted(added)),
        overwritten=tuple(sorted(overwritten)),
        deleted=tuple(sorted(deleted)),
    )


def _plan_skills_kind(target_dir: Path, origins: dict[str, Path]) -> InjectionPlan:
    """Plan adds/overwrites and manifest-authorized stale deletions for skills."""
    # Validate that target_dir, its parent, and the manifest are not symlinks.
    # Extracted into _validate_skills_target_dir so the same guard runs before
    # the early manifest read in the planning loop.
    _validate_skills_target_dir(target_dir)
    added: list[str] = []
    overwritten: list[str] = []
    for name, src in origins.items():
        dest = _resolve_skill_target_path(target_dir, name)
        if not dest.is_file():
            added.append(name)
        elif src.read_bytes() != dest.read_bytes():
            overwritten.append(name)

    # Build a casefold → exact-key map so that case-only renames on
    # case-insensitive filesystems (e.g. macOS, Windows) can be detected.
    origins_casefolds = {name.casefold(): name for name in origins}
    deleted: list[str] = []
    case_renames: list[tuple[str, str]] = []
    for name in _read_managed_skill_manifest(target_dir):
        if name in origins:
            continue
        dest = _resolve_skill_target_path(target_dir, name)
        if not dest.is_file():
            continue
        # Detect case-only renames: when the same inode is reachable via the
        # new spelling, the file is being renamed rather than deleted.  On a
        # case-sensitive filesystem the new path either does not exist or is a
        # distinct file, so stat() will raise OSError or return a different
        # inode and the entry remains a deletion candidate.
        name_cf = name.casefold()
        if name_cf in origins_casefolds:
            new_name = origins_casefolds[name_cf]
            try:
                new_dest = _resolve_skill_target_path(target_dir, new_name)
                old_st = dest.stat()
                new_st = new_dest.stat()
                if old_st.st_ino == new_st.st_ino and old_st.st_dev == new_st.st_dev:
                    # Same inode: this is a case rename on a case-insensitive FS.
                    # Record it so the execution phase can update the directory-
                    # entry casing via a two-step rename; do NOT add to deleted.
                    case_renames.append((name, new_name))
                    continue
            except OSError:
                # If either stat fails, this is not a confirmed same-inode
                # case-only rename; keep the entry as a deletion candidate.
                pass
        deleted.append(name)
    return InjectionPlan(
        kind=_SKILLS_KIND,
        added=tuple(sorted(added)),
        overwritten=tuple(sorted(overwritten)),
        deleted=tuple(sorted(deleted)),
        case_renames=tuple(sorted(case_renames)),
    )
