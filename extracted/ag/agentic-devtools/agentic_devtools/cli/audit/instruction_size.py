"""Length cap for repository instruction files.

GitHub documents a best practice of limiting any single instruction file to about
1,000 lines, and lists over-length as the first cause of instructions being
ignored. The audit workflow appends findings to instruction files, so without a
cap it steadily pushes them past that limit.

This module provides the cap and the check the audit apply step runs before it
opens an instruction-update pull request. The check **fails loudly**: an
oversized proposal aborts the batch rather than silently dropping the finding.
"""

from __future__ import annotations

from collections.abc import Iterable

# Hard cap applied to every instruction file the audit workflow may write.
# Deliberately below GitHub's ~1,000-line guidance so there is headroom before
# the guidance itself is breached. Raising this value is not the fix for a
# violation — move content into a path-scoped instruction file or into docs/.
MAX_INSTRUCTION_FILE_LINES = 900


class InstructionFileTooLongError(RuntimeError):
    """Raised when a proposed instruction file exceeds the line cap."""


def find_oversized_instruction_files(candidates: Iterable[tuple[str, str]]) -> list[tuple[str, int]]:
    """Return ``(path, line_count)`` for every candidate over the cap.

    Uses logical-line counting (``str.splitlines()``): a trailing newline does
    not add an extra line, but an unterminated final line is still counted.

    Args:
        candidates: Pairs of repo-relative path and proposed file content.

    Returns:
        Violations in input order. Empty when every candidate is within the cap.
    """
    violations: list[tuple[str, int]] = []
    for path, content in candidates:
        line_count = len(content.splitlines())
        if line_count > MAX_INSTRUCTION_FILE_LINES:
            violations.append((path, line_count))
    return violations


def check_instruction_file_sizes(candidates: Iterable[tuple[str, str]]) -> None:
    """Raise :class:`InstructionFileTooLongError` when any candidate is oversized.

    Args:
        candidates: Pairs of repo-relative path and proposed file content.

    Raises:
        InstructionFileTooLongError: When at least one candidate exceeds
            :data:`MAX_INSTRUCTION_FILE_LINES`. The message names every
            offending file, its line count, and the remediation.
    """
    violations = find_oversized_instruction_files(candidates)
    if not violations:
        return
    detail = "; ".join(f"{path} would be {lines} lines" for path, lines in violations)
    raise InstructionFileTooLongError(
        f"Instruction file line cap exceeded ({detail}); the cap is "
        f"{MAX_INSTRUCTION_FILE_LINES} lines. Consolidate the file or move content into a "
        "path-scoped .github/instructions/*.instructions.md file or into docs/ — "
        "do not raise the cap."
    )
