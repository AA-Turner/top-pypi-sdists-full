"""Cross-reference detection and update for the nest command.

Scans migrated spec artifacts for relative path references that need
updating after directory moves, and applies the updates in-place.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

from agentic_devtools.cli.speckit.shared.conflict_check import Move


@dataclass
class CrossRefUpdate:
    """Represents a cross-reference path replacement.

    Attributes:
        file_path: Post-migration path of the file containing the reference
            (the file's new location after the directory move).
        old_ref: The full matched path reference string as it appears in the
            file before migration (e.g. ``../100-auth/``).
        new_ref: The correctly recomputed replacement path reference string
            (e.g. ``../`` for a relative ref, or ``specs/100/`` for a
            ``specs/``-prefixed ref).
        line_number: The 1-indexed line number where the reference was found.
    """

    file_path: Path
    old_ref: str
    new_ref: str
    line_number: int


# Regex to detect relative path references to other spec directories
# Matches patterns like: ../100-auth-module/, ../../specs/100-auth-module/,
# specs/100-auth-module/, ./100-auth-module/, specs/100-auth-module (no trailing
# slash — common in markdown links), and bare directory names with a trailing
# slash (e.g., 100-auth/).  Bare names without a path prefix and without a
# trailing slash (prose such as "Issue 100-auth …") are intentionally excluded.
_PATH_REF_PATTERN = re.compile(r"(?:\.\.?/|specs/)[\w\-/]*\d+[\w\-]*/?|\d+[\w\-]+/")


def scan_crossrefs(moves: list[Move], specs_root: str | Path) -> list[CrossRefUpdate]:
    """Scan every markdown file under specs/ for references to moved directories.

    The scan walks the **entire** ``specs/`` tree recursively — not only the
    ``move.source`` directories — so references living in unmoved or standalone
    specs are updated too.  Each update stores:

    * ``file_path`` — the **post-migration** path of the referencing file so
      that :func:`apply_crossref_updates` can open it after all directories
      have been moved.
    * ``old_ref`` / ``new_ref`` — the full matched path reference string and
      the correctly recomputed replacement, accounting for the change in
      nesting depth of both the referencing file and the referenced directory.

    Args:
        moves: List of planned directory moves.
        specs_root: Path to the specs/ directory.

    Returns:
        List of CrossRefUpdate objects describing needed replacements.
    """
    specs_path = Path(specs_root)
    updates: list[CrossRefUpdate] = []

    if not specs_path.is_dir():
        return updates

    # Build: old directory name → (new absolute target path, specs-root-relative path)
    target_map: dict[str, tuple[Path, str]] = {}
    for move in moves:
        target_map[move.source.name] = (move.target, move.target.relative_to(specs_path).as_posix())

    if not target_map:
        return updates

    scanned_files: set[Path] = set()
    for old_file_path in sorted(specs_path.rglob("*.md")):
        if old_file_path in scanned_files:
            continue
        scanned_files.add(old_file_path)
        _scan_file(old_file_path, _post_migration_path(old_file_path, moves), target_map, updates)

    return updates


def _post_migration_path(old_file_path: Path, moves: list[Move]) -> Path:
    """Return where a file will live once all planned moves have been applied.

    Files inside a moved directory follow their directory to the new location;
    files outside every moved directory keep their current path.
    """
    for move in moves:
        try:
            rel_within_dir = old_file_path.relative_to(move.source)
        except ValueError:
            continue
        return move.target / rel_within_dir
    return old_file_path


def _scan_file(
    old_file_path: Path,
    new_file_path: Path,
    target_map: dict[str, tuple[Path, str]],
    updates: list[CrossRefUpdate],
) -> None:
    """Scan a single file for cross-references matching moved directories.

    Args:
        old_file_path: Current (pre-migration) path; used for reading content.
        new_file_path: Post-migration path; stored in each CrossRefUpdate so
            that apply_crossref_updates opens the correct file after the move.
        target_map: Mapping from old directory name to
            ``(new_target_path, new_rel_from_specs)``.
        updates: List to append discovered CrossRefUpdate objects to.
    """
    try:
        content = old_file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise OSError(
            f"Cannot read '{old_file_path}' during cross-reference scan: {exc}. "
            "Resolve the read error before running nest migration."
        ) from exc

    for line_num, line in enumerate(content.splitlines(), start=1):
        # Collect all path references on this line first so we only flag
        # old_names that appear inside a genuine path reference context,
        # never in bare prose (e.g., "Issue 100-auth …").
        path_matches = list(_PATH_REF_PATTERN.finditer(line))
        # A single line may contain several *distinct* reference forms to the
        # same moved directory (e.g. both "../100-auth/" and "specs/100-auth").
        # Each distinct form has a different old_ref and a different recomputed
        # new_ref, so we must emit one update per distinct old_ref. seen_refs is
        # scoped to the whole line (not per old_name) so that a single old_ref
        # which happens to contain more than one moved directory name is never
        # turned into conflicting updates that replace the same string two
        # different ways. Identical repeats are deduplicated because
        # apply_crossref_updates uses str.replace (which replaces every
        # occurrence), making duplicate updates redundant.
        seen_refs: set[str] = set()
        for old_name, (new_target, new_rel) in target_map.items():
            for match in path_matches:
                old_full_ref = match.group(0)
                if old_full_ref in seen_refs:
                    continue
                if not _path_ref_contains_dir(old_full_ref, old_name):
                    continue
                seen_refs.add(old_full_ref)
                new_full_ref = _compute_new_path_ref(
                    old_full_ref,
                    old_name,
                    new_rel,
                    new_file_path.parent,
                    new_target,
                )
                updates.append(
                    CrossRefUpdate(
                        file_path=new_file_path,
                        old_ref=old_full_ref,
                        new_ref=new_full_ref,
                        line_number=line_num,
                    )
                )


def _path_ref_contains_dir(path_ref: str, directory_name: str) -> bool:
    """Return True when directory_name appears as an exact segment in raw path_ref text."""
    return any(segment == directory_name for segment in path_ref.split("/") if segment and segment not in {".", ".."})


def _compute_new_path_ref(
    old_path_ref: str,
    old_dir_name: str,
    new_rel_from_specs: str,
    new_file_parent: Path,
    new_target_dir: Path,
) -> str:
    """Compute the replacement path reference string.

    For relative references (starting with ``../`` or ``./``), recomputes the
    full relative path from the new file location to the new target directory
    using :func:`os.path.relpath`, which correctly accounts for nesting-depth
    changes in both the referencing file and the referenced directory.

    For ``specs/``-prefixed and bare-name references, performs a segment
    substitution so the ``specs/`` prefix is preserved.

    Args:
        old_path_ref: Full matched path reference string (e.g. ``../100-auth/``).
        old_dir_name: Old directory name being replaced (e.g. ``100-auth``).
        new_rel_from_specs: New directory path relative to the specs root
            (e.g. ``100`` or ``100/101``).
        new_file_parent: Directory of the referencing file after migration.
        new_target_dir: New absolute path of the referenced directory.

    Returns:
        The replacement path reference string.
    """
    has_trailing_slash = old_path_ref.endswith("/")

    if old_path_ref.startswith(("../", "./")):
        # Relative reference: recompute using relpath so that depth changes in
        # both the referencing file and the referenced directory are handled.
        try:
            rel = Path(os.path.relpath(str(new_target_dir), str(new_file_parent))).as_posix()
        except ValueError:
            # Fallback for environments where relpath fails (e.g. cross-drive
            # on Windows); use segment substitution instead.
            return _segment_replace(old_path_ref, old_dir_name, new_rel_from_specs)
        return rel + ("/" if has_trailing_slash else "")

    # specs/-prefixed or bare-name: segment substitution preserves the prefix.
    return _segment_replace(old_path_ref, old_dir_name, new_rel_from_specs)


def _segment_replace(path_ref: str, old_name: str, new_rel: str) -> str:
    """Replace old directory name segment with the new relative path fragment.

    Handles the case where ``new_rel`` contains path separators
    (e.g. ``100/101``), expanding a single segment into multiple segments.

    Args:
        path_ref: The path reference string (e.g. ``specs/100-auth/``).
        old_name: The segment to replace (e.g. ``100-auth``).
        new_rel: The replacement, which may contain ``/`` (e.g. ``100/101``).

    Returns:
        The updated path reference string.
    """
    parts = path_ref.split("/")
    new_parts: list[str] = []
    for part in parts:
        if part == old_name:
            new_parts.extend(new_rel.split("/"))
        else:
            new_parts.append(part)
    return "/".join(new_parts)


def apply_crossref_updates(updates: list[CrossRefUpdate]) -> None:
    """Apply cross-reference path replacements in-place within spec artifacts.

    Each update's ``file_path`` must be the **post-migration** location of the
    file (as produced by :func:`scan_crossrefs`), so this function must be
    called after all directory moves have been completed.

    Missing-file, read, and write failures are **raised**, never downgraded to
    warnings, so the caller's rollback boundary is triggered instead of
    committing a partial migration with stale links.

    Args:
        updates: List of CrossRefUpdate objects describing replacements.

    Raises:
        FileNotFoundError: If a referenced file does not exist after migration.
        OSError: If a file cannot be read or written.
        UnicodeDecodeError: If a file is not valid UTF-8.
    """
    file_updates: dict[Path, list[CrossRefUpdate]] = {}
    for update in updates:
        file_updates.setdefault(update.file_path, []).append(update)

    for file_path, file_refs in file_updates.items():
        if not file_path.exists():
            raise FileNotFoundError(f"cross-reference update failed: file not found after migration: {file_path}")

        content = file_path.read_text(encoding="utf-8")

        lines = content.splitlines(keepends=True)
        refs_by_line: dict[int, list[CrossRefUpdate]] = {}
        for ref in file_refs:
            refs_by_line.setdefault(ref.line_number, []).append(ref)

        for line_number, line_refs in refs_by_line.items():
            line_index = line_number - 1
            if line_index < 0 or line_index >= len(lines):
                continue
            for ref in line_refs:
                lines[line_index] = lines[line_index].replace(ref.old_ref, ref.new_ref)

        file_path.write_text("".join(lines), encoding="utf-8")
