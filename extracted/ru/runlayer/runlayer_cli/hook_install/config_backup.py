"""Naming and bounded retention for ``<stem>.backup_<timestamp><suffix>`` copies.

Every writer that rewrites a third-party client config keeps the previous
content beside it as a recovery copy. Reconciliation runs hourly (macOS
LaunchDaemon) or every 15 minutes (Windows task), so an unbounded pile of
backups is what a customer eventually sees in ``~/.claude`` (ENG-6770).
``prune_backups`` caps that pile per config file at ``BACKUP_KEEP`` newest
copies, ordered by the timestamp embedded in the file name so retention never
depends on ``mtime`` (which a copy/restore can rewrite).

Only names that match the exact shape this module produces — or the legacy
second-precision shape older CLIs produced — are ever candidates; the active
config, ``*.local.*`` siblings, and any user-named file are never touched.
Deletion is descriptor-relative under a console-home anchor (root MDM writes
into a user-controlled home) and skips anything that is not a regular file.
"""

from __future__ import annotations

import os
import platform
from datetime import datetime
from pathlib import Path

from runlayer_cli import regex_safe
from runlayer_cli.hook_install.safe_fs import (
    maybe_safe_unlink,
    path_has_link_or_reparse_point,
)

BACKUP_KEEP = 5
BACKUP_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S_%f"

# ``YYYYMMDD_HHMMSS`` (legacy second precision) with an optional ``_ffffff``
# microsecond tail. Zero-padded digits sort lexicographically in time order, and
# a second-only name sorts before the same second's microsecond names.
_TIMESTAMP_PATTERN = r"\d{8}_\d{6}(?:_\d{6})?"


def backup_path_for(path: Path, now: datetime | None = None) -> Path:
    """Sibling path for a recovery copy of *path* stamped with *now*."""
    stamp = (now or datetime.now()).strftime(BACKUP_TIMESTAMP_FORMAT)
    return path.with_name(f"{path.stem}.backup_{stamp}{path.suffix}")


def _backup_name_pattern(path: Path) -> regex_safe.Pattern:
    return regex_safe.compile(
        rf"^{regex_safe.escape(path.stem)}\.backup_({_TIMESTAMP_PATTERN})"
        rf"{regex_safe.escape(path.suffix)}$"
    )


def _recognized_backups(path: Path) -> list[Path]:
    """Regular-file siblings named as backups of *path*, oldest first."""
    pattern = _backup_name_pattern(path)
    stamped: list[tuple[str, Path]] = []
    try:
        with os.scandir(path.parent) as entries:
            for entry in entries:
                matched = pattern.match(entry.name)
                if matched is None:
                    continue
                try:
                    if not entry.is_file(follow_symlinks=False):
                        continue
                except OSError:
                    continue
                stamped.append((matched.group(1), Path(entry.path)))
    except OSError:
        return []
    stamped.sort(key=lambda item: item[0])
    return [candidate for _, candidate in stamped]


def prune_backups(
    path: Path, *, home: Path | None, keep: int = BACKUP_KEEP
) -> list[Path]:
    """Delete all but the newest *keep* recognized backups of *path*.

    Best-effort: a candidate that cannot be removed (permission, race, link
    swapped in underneath) is skipped rather than failing the caller's install.
    With *home* set, removal is the link-safe descriptor walk from that anchor;
    on Windows a candidate that is or sits under a reparse point is skipped.
    Returns the paths that were removed.
    """
    candidates = _recognized_backups(path)
    surplus = candidates[: max(len(candidates) - keep, 0)]
    windows = platform.system() == "Windows"
    removed: list[Path] = []
    for candidate in surplus:
        if windows and path_has_link_or_reparse_point(candidate):
            continue
        try:
            if maybe_safe_unlink(candidate, home=home):
                removed.append(candidate)
        except OSError:
            continue
    return removed


__all__ = [
    "BACKUP_KEEP",
    "BACKUP_TIMESTAMP_FORMAT",
    "backup_path_for",
    "prune_backups",
]
