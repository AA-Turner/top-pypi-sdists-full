# abstract_paths/content_utils/src/diff_engine.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Iterable, Optional
import logging

# re-use your existing primitives
from .find_content import findContentAndEdit
from .diff_utils import apply_replacements_to_lines, write_text_atomic
from ..file_handlers import read_any_file

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────────────
# Data models
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class Hunk:
    """One contiguous diff 'block': a set of '-' lines, '+' lines, and matches found in the repo."""
    subs: List[str] = field(default_factory=list)   # lines without leading '-'
    adds: List[str] = field(default_factory=list)   # lines without leading '+'
    content: List[Dict[str, Any]] = field(default_factory=list)  # [{file_path, lines:[{line,content},...]}]

    def is_multiline(self) -> bool:
        return len(self.subs) > 1 or len(self.adds) > 1


@dataclass
class ApplyReport:
    changed_files: List[str] = field(default_factory=list)
    skipped_files: List[str] = field(default_factory=list)
    hunks_applied: int = 0
    hunks_skipped: int = 0

    def extend_changed(self, path: str):
        if path not in self.changed_files:
            self.changed_files.append(path)

    def extend_skipped(self, path: str):
        if path not in self.skipped_files:
            self.skipped_files.append(path)


# ──────────────────────────────────────────────────────────────────────────────
# Parser
# ──────────────────────────────────────────────────────────────────────────────

def parse_unified_diff(diff_text: str) -> List[Hunk]:
    """
    Parse a minimal unified-ish diff:
      - Lines starting with '-' go to subs (without the prefix)
      - Lines starting with '+' go to adds (without the prefix)
      - Blank/other lines delimit hunks
    """
    hunks: List[Hunk] = []
    current = Hunk()
    open_block = False

    def close():
        nonlocal current, open_block
        if open_block and (current.subs or current.adds):
            hunks.append(current)
        current = Hunk()
        open_block = False

    for raw in diff_text.splitlines():
        if raw.startswith('-'):
            if not open_block:
                open_block = True
            current.subs.append(raw[1:])
        elif raw.startswith('+'):
            if not open_block:
                open_block = True
            current.adds.append(raw[1:])
        else:
            # delimiter
            if open_block:
                close()

    # trailing block
    if open_block:
        close()

    return hunks


# ──────────────────────────────────────────────────────────────────────────────
# Finder
# ──────────────────────────────────────────────────────────────────────────────


def resolve_hunk_targets(
    hunk: Hunk,
    *,
    directory: str,
    # NEW: pass-through filters (same surface as FinderTab)
    allowed_exts: Optional[set] = False,
    unallowed_exts: Optional[set] = False,
    exclude_types: Optional[set] = False,
    exclude_dirs: Optional[list] = False,
    exclude_patterns: Optional[list] = False,
    add: bool = False,
    recursive: bool = True,
) -> Hunk:
    matches = findContentAndEdit(
        directory=directory,
        allowed_exts=allowed_exts,
        unallowed_exts=unallowed_exts,
        exclude_types=exclude_types,
        exclude_dirs=exclude_dirs,
        exclude_patterns=exclude_patterns,
        add=add,
        recursive=recursive,
        strings=hunk.subs,
        edit_lines=False,
        diffs=True,
        get_lines=True,
    ) or []
    hunk.content = matches
    return hunk

# ──────────────────────────────────────────────────────────────────────────────
# Applier
# ──────────────────────────────────────────────────────────────────────────────

def _safe_apply_to_file(
    file_path: str,
    matches: List[Dict[str, Any]],
    adds: List[str],
    *,
    verify: bool = False,
) -> bool:
    """
    Apply one hunk to a single file in memory and persist atomically.
    Returns True if file changed.
    """
    before = read_any_file(file_path)
    og_lines = before.split("\n")

    if verify and not matches:
        return False

    new_lines = apply_replacements_to_lines(og_lines, matches, adds)

    if new_lines is og_lines or new_lines == og_lines:
        return False

    # Write back atomically
    write_text_atomic(file_path, "\n".join(new_lines))
    return True


def apply_hunks(
    hunks: List[Hunk],
    *,
    directory: str,
    exclude_dirs: Optional[Iterable[str]] = None,
    verify_before_replace: bool = False,
) -> ApplyReport:
    """
    For each hunk:
      1) Resolve targets (files + line hits)
      2) Apply replacements deterministically
      3) Write per file atomically
    """
    report = ApplyReport()
    exclude_dirs = list(exclude_dirs or [])

    last_file: Optional[str] = None
    inmem_lines: Optional[List[str]] = None  # not used here because we write per file immediately

    for hunk in hunks:
        # 1) find targets
        hunk = resolve_hunk_targets(hunk, directory=directory, exclude_dirs=exclude_dirs)
        contents = hunk.content or []
        if not contents:
            report.hunks_skipped += 1
            logger.debug("No matches for hunk; subs=%s", hunk.subs)
            continue

        # 2) apply to each file that matched this hunk
        any_applied = False
        for entry in contents:
            file_path = entry["file_path"]
            matches = entry.get("lines") or []

            changed = _safe_apply_to_file(
                file_path,
                matches,
                hunk.adds or [],
                verify=verify_before_replace,
            )
            if changed:
                any_applied = True
                report.extend_changed(file_path)
            else:
                report.extend_skipped(file_path)

        if any_applied:
            report.hunks_applied += 1
        else:
            report.hunks_skipped += 1

    return report


# ──────────────────────────────────────────────────────────────────────────────
# Public one-shot API
# ──────────────────────────────────────────────────────────────────────────────

def apply_diff_text(
    diff_text: str,
    *,
    directory: str,
    exclude_dirs: Optional[Iterable[str]] = None,
    verify_before_replace: bool = False,
) -> ApplyReport:
    """
    High-level convenience: parse, find, apply, report.
    """
    hunks = parse_unified_diff(diff_text)
    logger.info("Parsed %d hunks", len(hunks))
    return apply_hunks(
        hunks,
        directory=directory,
        exclude_dirs=exclude_dirs,
        verify_before_replace=verify_before_replace,
    )


def plan_previews(
    diff_text: str,
    *,
    directory: str,
    # NEW: same pass-through filters
    allowed_exts: Optional[set] = False,
    unallowed_exts: Optional[set] = False,
    exclude_types: Optional[set] = False,
    exclude_dirs: Optional[list] = False,
    exclude_patterns: Optional[list] = False,
    add: bool = False,
    recursive: bool = True,
) -> Dict[str, str]:
    hunks = parse_unified_diff(diff_text)
    plan: Dict[str, List[Tuple[List[Dict[str, Any]], List[str]]]] = {}

    for h in hunks:
        matches = findContentAndEdit(
            directory=directory,
            allowed_exts=allowed_exts,
            unallowed_exts=unallowed_exts,
            exclude_types=exclude_types,
            exclude_dirs=exclude_dirs,
            exclude_patterns=exclude_patterns,
            add=add,
            recursive=recursive,
            strings=h.subs,
            edit_lines=False,
            diffs=True,
            get_lines=True,
        ) or []
        for entry in matches:
            fp = entry["file_path"]
            plan.setdefault(fp, []).append((entry.get("lines") or [], h.adds or []))

    previews: Dict[str, str] = {}
    for fp, steps in plan.items():
        before = read_any_file(fp)
        og_lines = before.split("\n")
        for lines_hit, adds in steps:
            og_lines = apply_replacements_to_lines(og_lines, lines_hit, adds)
        txt = "\n".join(og_lines)
        if not txt.endswith("\n"):
            txt += "\n"
        previews[fp] = txt
    return previews


def apply_custom_diff(original_lines: List[str], diff_lines: List[str]) -> str:
    # Skip file path if present
    if diff_lines and '/' in diff_lines[0]:
        diff_lines = diff_lines[1:]
    # Split into hunks at ...
    hunks = []
    current_hunk = []
    for line in diff_lines:
        stripped = line.strip()
        if stripped == '...':
            if current_hunk:
                hunks.append(current_hunk)
            current_hunk = []
        else:
            current_hunk.append(line)
    if current_hunk:
        hunks.append(current_hunk)
    patched = list(original_lines)  # copy
    offset = 0
    for hunk in hunks:
        old_hunk = []
        new_hunk = []
        for line in hunk:
            if line.startswith('-'):
                old_hunk.append(line[1:])
            elif line.startswith('+'):
                new_hunk.append(line[1:])
            else:
                old_hunk.append(line)
                new_hunk.append(line)
        hunk_len = len(old_hunk)
        found = False
        for k in range(offset, len(patched) - hunk_len + 1):
            if all(patched[k + m] == old_hunk[m] for m in range(hunk_len)):
                # Replace
                del patched[k : k + hunk_len]
                patched[k:k] = new_hunk
                offset = k + len(new_hunk)
                found = True
                break
        if not found:
            raise ValueError(f"Hunk not found: {hunk}")
    return '\n'.join(patched)
