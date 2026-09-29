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

Copies sit beside the config, except when the config's directory is reached
through a symlink (``~/.claude -> ~/dotfiles/claude``): a linked directory is
usually a git working tree, and a copy of ``settings.json`` can carry the API
key the routing writer just blanked, so those copies go to
``~/.runlayer/config-backups/<dir relative to home>/`` instead (ENG-6814). In
user scope, copies older CLIs left beside the link are moved there on the next
prune before retention runs, so nothing is lost for having sat in the tree.
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
    resolve_within_home,
)

BACKUP_KEEP = 5
BACKUP_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S_%f"
BACKUP_ROOT = Path(".runlayer") / "config-backups"

# ``YYYYMMDD_HHMMSS`` (legacy second precision) with an optional ``_ffffff``
# microsecond tail. Zero-padded digits sort lexicographically in time order, and
# a second-only name sorts before the same second's microsecond names.
_TIMESTAMP_PATTERN = r"\d{8}_\d{6}(?:_\d{6})?"


def _reached_through_link(directory: Path, anchor: Path, *, gated: bool) -> bool:
    """Whether *directory* (under *anchor*) is only reachable through a symlink.

    *gated* means *anchor* is a console-home trust boundary, so the answer
    comes from the same in-home resolution the writer used (an unresolvable
    chain counts as linked: nothing of ours belongs in there). Otherwise the
    running user owns the tree and a plain ``realpath`` comparison is enough.
    """
    if gated:
        return resolve_within_home(anchor, directory) != directory
    canonical_anchor = Path(os.path.realpath(anchor))
    return Path(os.path.realpath(directory)) != canonical_anchor.joinpath(
        *directory.relative_to(anchor).parts
    )


def backup_dir_for(path: Path, *, home: Path | None) -> Path:
    """Directory that holds the recovery copies of *path*.

    The config's own directory, unless that directory is reached through a
    link, in which case ``<home>/.runlayer/config-backups/<relative dir>``.
    *home* is the console-home anchor for root MDM writes; ``None`` means the
    running user's own home. A config outside the home (or directly in it)
    keeps its copies beside itself.
    """
    anchor = home if home is not None else Path.home()
    directory = path.parent
    try:
        relative = directory.relative_to(anchor)
    except ValueError:
        return directory
    if not relative.parts:
        return directory
    if not _reached_through_link(directory, anchor, gated=home is not None):
        return directory
    return anchor / BACKUP_ROOT / relative


def backup_path_for(
    path: Path, *, home: Path | None, now: datetime | None = None
) -> Path:
    """Recovery-copy path for *path* stamped with *now* (see ``backup_dir_for``)."""
    stamp = (now or datetime.now()).strftime(BACKUP_TIMESTAMP_FORMAT)
    return backup_dir_for(path, home=home) / f"{path.stem}.backup_{stamp}{path.suffix}"


def _backup_name_pattern(path: Path) -> regex_safe.Pattern:
    return regex_safe.compile(
        rf"^{regex_safe.escape(path.stem)}\.backup_({_TIMESTAMP_PATTERN})"
        rf"{regex_safe.escape(path.suffix)}$"
    )


def _recognized_backups(path: Path, directory: Path) -> list[Path]:
    """Regular files in *directory* named as backups of *path*, oldest first."""
    pattern = _backup_name_pattern(path)
    stamped: list[tuple[str, Path]] = []
    try:
        with os.scandir(directory) as entries:
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


def _adopt_legacy_siblings(path: Path, directory: Path) -> None:
    """Move copies an older CLI left beside *path* into *directory* (user scope).

    Released CLIs wrote the copy beside the link, i.e. inside the linked tree
    relocation now keeps it out of. The user owns that tree, so the copies
    move — same name, so the stamp keeps ordering them — and the single
    retention pass over *directory* then decides which survive. Best-effort:
    a copy that cannot be moved (``EXDEV``, permissions, race) stays in place
    rather than being lost.
    """
    legacy = _recognized_backups(path, path.parent)
    if not legacy:
        return
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except OSError:
        return
    for copy in legacy:
        try:
            os.replace(copy, directory / copy.name)
        except OSError:
            continue


def prune_backups(
    path: Path, *, home: Path | None, keep: int = BACKUP_KEEP
) -> list[Path]:
    """Delete all but the newest *keep* recognized backups of *path*.

    Scans the directory ``backup_dir_for`` names for *path*, so copies
    relocated out of a linked tree drain too. In user scope, copies an older
    CLI left *beside* a linked config are first moved into that directory
    (``_adopt_legacy_siblings``), so one retention pass keeps the newest
    *keep* across both origins. Under a console-home anchor the linked tree
    is never touched: root never wrote there and must not modify inside the
    user's link. Best-effort: a candidate that cannot be removed (permission,
    race, link swapped in underneath) is skipped rather than failing the
    caller's install. With *home* set, removal is the link-safe descriptor
    walk from that anchor. On Windows a candidate that is or sits under a
    reparse point is skipped. Returns the paths that were removed.
    """
    directory = backup_dir_for(path, home=home)
    if home is None and directory != path.parent:
        _adopt_legacy_siblings(path, directory)
    candidates = _recognized_backups(path, directory)
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
    "BACKUP_ROOT",
    "BACKUP_TIMESTAMP_FORMAT",
    "backup_dir_for",
    "backup_path_for",
    "prune_backups",
]
