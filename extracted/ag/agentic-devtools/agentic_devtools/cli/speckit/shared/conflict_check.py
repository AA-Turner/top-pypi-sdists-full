"""Target path conflict detection for speckit migration commands.

Detects existing target paths that would be overwritten by a migration
or retro-spec placement, enabling abort-before-write behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Move:
    """Represents a directory move operation.

    Attributes:
        source: Absolute or relative path of the source directory.
        target: Absolute or relative path of the target directory.
        issue_number: The issue number associated with this spec.
    """

    source: Path
    target: Path
    issue_number: int


def check_target_conflicts(moves: list[Move]) -> list[str]:
    """Detect existing target paths that would conflict with planned moves.

    Args:
        moves: List of planned directory move operations.

    Returns:
        List of conflicting target path strings. Empty if no conflicts.
    """
    conflicts: list[str] = []
    for move in moves:
        if move.target.exists():
            conflicts.append(str(move.target))
    return conflicts
