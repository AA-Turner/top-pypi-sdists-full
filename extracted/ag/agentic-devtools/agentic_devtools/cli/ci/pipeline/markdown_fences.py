"""Stateless Markdown fence-line candidate classification."""

from dataclasses import dataclass


@dataclass(frozen=True)
class FenceLineCandidate:
    """Syntax facts about one candidate fence delimiter line."""

    line_number: int
    marker: str
    run_length: int
    can_open: bool
    can_close: bool


def classify_fence_line(line: str, line_number: int) -> FenceLineCandidate | None:
    """Classify one physical line without tracking Markdown fence state."""
    if line_number <= 0:
        raise ValueError("line_number must be positive")

    marker_start = 0
    while marker_start < len(line) and marker_start < 3 and line[marker_start] == " ":
        marker_start += 1
    if marker_start == len(line) or line[marker_start] not in ("`", "~"):
        return None

    marker = line[marker_start]
    run_end = marker_start
    while run_end < len(line) and line[run_end] == marker:
        run_end += 1
    run_length = run_end - marker_start
    if run_length < 3:
        return None

    info = line[run_end:]
    return FenceLineCandidate(
        line_number=line_number,
        marker=marker,
        run_length=run_length,
        can_open=marker != "`" or "`" not in info,
        can_close=not info.strip(),
    )
