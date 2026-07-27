"""T2 — Diff preview before applying batched FILE: writes.

Shows a unified diff of every pending change so the user can confirm or
reject the entire batch in one keypress, instead of discovering five turns
later that Sage wrote prose into pets.js.

Decision logic:
  - All clean + small batch → auto-apply
  - Any validator failure → require confirm (block auto)
  - Large batch (>200 lines or >5 files) → require confirm
"""

from __future__ import annotations

import difflib
from dataclasses import dataclass, field

from sage.core.content_validator import validate_content

__all__ = [
    "PendingChange",
    "ApplyDecision",
    "render_diff",
    "render_batch_summary",
    "should_auto_apply",
]


@dataclass
class PendingChange:
    filepath: str
    before: str | None    # None = file doesn't exist yet
    after: str | None     # None = file is being deleted

    @property
    def kind(self) -> str:
        if self.before is None and self.after is not None:
            return "new"
        if self.before is not None and self.after is None:
            return "delete"
        if self.before == self.after:
            return "noop"
        return "modify"

    @property
    def added_lines(self) -> int:
        return len((self.after or "").splitlines())

    @property
    def removed_lines(self) -> int:
        return len((self.before or "").splitlines())


@dataclass
class ApplyDecision:
    auto: bool
    reason: str = ""
    rejected: list[str] = field(default_factory=list)


def render_diff(*, filepath: str, before: str | None, after: str | None) -> str:
    """Unified diff for a single change."""
    if before is None and after is not None:
        body = "\n".join(f"+ {l}" for l in after.splitlines())
        return f"--- {filepath} (new file)\n{body}"
    if before is not None and after is None:
        body = "\n".join(f"- {l}" for l in before.splitlines())
        return f"--- {filepath} (deleted)\n{body}"
    diff = difflib.unified_diff(
        (before or "").splitlines(keepends=False),
        (after or "").splitlines(keepends=False),
        fromfile=f"a/{filepath}",
        tofile=f"b/{filepath}",
        lineterm="",
        n=3,
    )
    return "\n".join(diff)


def render_batch_summary(changes: list[PendingChange]) -> str:
    """One-screen summary of an entire pending batch."""
    if not changes:
        return "(no pending changes)"
    n_new = sum(1 for c in changes if c.kind == "new")
    n_mod = sum(1 for c in changes if c.kind == "modify")
    n_del = sum(1 for c in changes if c.kind == "delete")
    total_added = sum(c.added_lines for c in changes)
    total_removed = sum(c.removed_lines for c in changes if c.kind != "new")
    lines = [
        f"Pending: {len(changes)} change(s) "
        f"({n_new} new, {n_mod} modified, {n_del} deleted) "
        f"+{total_added}/-{total_removed} lines",
        "",
    ]
    for c in changes:
        marker = {"new": "+", "modify": "~", "delete": "-", "noop": "="}[c.kind]
        lines.append(f"  {marker} {c.filepath} (+{c.added_lines}/-{c.removed_lines})")
    return "\n".join(lines)


def should_auto_apply(
    changes: list[PendingChange],
    *,
    auto_threshold_lines: int = 200,
    auto_threshold_files: int = 5,
) -> ApplyDecision:
    """Decide whether to auto-apply or require user confirmation.

    Auto-apply requires ALL of:
      - Every change passes content validator
      - Total lines ≤ threshold
      - File count ≤ threshold
    Any failure → require confirm with a clear reason.
    """
    rejected: list[str] = []
    for c in changes:
        if c.after is None:
            continue
        result = validate_content(c.filepath, c.after)
        if not result.ok:
            rejected.append(f"{c.filepath}: {result.signal}")
    if rejected:
        return ApplyDecision(
            auto=False,
            reason=f"validator rejected {len(rejected)} file(s): {'; '.join(rejected[:3])}",
            rejected=rejected,
        )

    total_lines = sum(c.added_lines + c.removed_lines for c in changes)
    if total_lines > auto_threshold_lines:
        return ApplyDecision(
            auto=False,
            reason=f"large batch: {total_lines} total lines exceeds {auto_threshold_lines}",
        )
    if len(changes) > auto_threshold_files:
        return ApplyDecision(
            auto=False,
            reason=f"large batch: {len(changes)} files exceeds {auto_threshold_files}",
        )

    return ApplyDecision(auto=True, reason="all clean and small")
