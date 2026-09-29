"""Timestamped archive folders, kept for a fixed window then pruned.

One rule for the two archives the CLI keeps: a workspace's `.innoday/archive/`
(prior `project.yml` / `CLAUDE.md`) and `~/.innoday/archive/` (a config.json
that could not be parsed, PF-467). Entries are named `<name>.<UTC stamp>`; the
stamp is what pruning reads, so a file without one is never deleted.
"""

from datetime import datetime, timedelta, timezone
from pathlib import Path

ARCHIVE_RETENTION_DAYS = 30
STAMP_FORMAT = "%Y%m%d-%H%M%S"


def archive_stamp() -> str:
    return datetime.now(timezone.utc).strftime(STAMP_FORMAT)


def prune_archive(archive_dir: Path, days: int = ARCHIVE_RETENTION_DAYS) -> None:
    """Delete entries whose stamp is older than `days`. Unstamped files stay."""
    if not archive_dir.is_dir():
        return
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    for entry in archive_dir.iterdir():
        stamp = entry.name.rsplit(".", 1)[-1]
        # A same-second collision gets a "-N" suffix; the stamp is before it.
        stamp = "-".join(stamp.split("-")[:2])
        try:
            when = datetime.strptime(stamp, STAMP_FORMAT).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        if when < cutoff:
            entry.unlink(missing_ok=True)
