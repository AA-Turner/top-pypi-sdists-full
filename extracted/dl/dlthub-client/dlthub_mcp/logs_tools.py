"""Read-only tools over what a run printed.

Both read the run's *stored* log, which the platform consolidates once the run
ends, so neither answers for a run still in flight.
"""

from __future__ import annotations

# Python internals
from collections import deque
from dataclasses import dataclass
from typing import Optional

# Other libraries
from dlt.common.typing import Annotated

# Current package
from dlthub_mcp._access import CONTEXT_READ
from dlthub_mcp._client import tool, workspace
from dlthub_mcp._log_search import MAX_MATCHES, LogSearchResult, search

#: Trailing lines returned when the caller does not say, and the ceiling.
LOG_LINES = 200
MAX_LOG_LINES = 5_000


@dataclass(frozen=True)
class RunLogTail:
    """The end of a run's log.

    Attributes:
        run_id: The run the lines came from.
        lines: The trailing lines, oldest first.
        first_line_number: The 1-based position of ``lines[0]`` in the whole
            log, so a quote can be placed. ``None`` when the log is empty.
        total_lines: How many lines the log holds.
        truncated: Whether earlier lines exist above ``lines``.
    """

    run_id: str
    lines: tuple[str, ...]
    first_line_number: int | None
    total_lines: int
    truncated: bool


@tool
def dlthub_get_run_logs(
    run_id: str, max_lines: int = LOG_LINES
) -> Annotated[RunLogTail, CONTEXT_READ]:
    """The tail of what a run printed, where a traceback usually is.

    Reach for this to quote an actual error instead of reporting that something
    failed. Returns the LAST lines; ``truncated`` says whether earlier ones
    exist, and ``dlthub_grep_run_logs`` searches the whole log when they do. An
    empty result means the run stored nothing, which is worth reporting rather
    than guessing around.

    Only stored logs: the platform consolidates a run's log after it ends, so
    this reports the run as having no log until then.

    Args:
        run_id: The run's uuid, from ``dlthub_list_runs``.
        max_lines: How many trailing lines to return, at most 5000. Raise it
            when a traceback looks cut off at the top.

    Returns:
        The trailing lines, where they sit in the log, and whether more precede
        them.

    Raises:
        Exception: A ``ToolError`` when the run has no stored log yet.
    """
    limit = max(1, min(max_lines, MAX_LOG_LINES))
    kept: deque[str] = deque(maxlen=limit)
    total = 0
    for line in workspace().job_runs.get(id=run_id).logs():
        kept.append(line.content)
        total += 1
    return RunLogTail(
        run_id=run_id,
        lines=tuple(kept),
        first_line_number=total - len(kept) + 1 if kept else None,
        total_lines=total,
        truncated=total > len(kept),
    )


@tool
def dlthub_grep_run_logs(
    run_id: str,
    pattern: str,
    ignore_case: bool = False,
    invert: bool = False,
    word: bool = False,
    line_regexp: bool = False,
    fixed: bool = False,
    count_only: bool = False,
    context: int = 0,
    before: Optional[int] = None,
    after: Optional[int] = None,
    max_matches: int = MAX_MATCHES,
) -> Annotated[LogSearchResult, CONTEXT_READ]:
    r"""Search a run's WHOLE log, not just the tail ``dlthub_get_run_logs`` returns.

    Reach for this when a log is long and you know roughly what you are after —
    an exception type, a table name, a load id. Matches carry 1-based line
    numbers, so a position can be quoted, and ``match_count`` is exact even when
    the matches themselves were capped.

    The options are grep's, by their grep names: ``ignore_case`` is ``-i``,
    ``context`` is ``-C``, and so on. The pattern is not grep's, though — it is
    a Python regular expression, so ``\d`` and ``\w`` work, and a POSIX class
    like ``[[:digit:]]`` is refused rather than quietly matching nothing.

    Args:
        run_id: The run's uuid, from ``dlthub_list_runs``.
        pattern: A Python regular expression, or a literal string when
            ``fixed``.
        ignore_case: Match regardless of case.
        invert: Return the lines that did *not* match.
        word: Require whole-word matches, so ``run`` does not match ``running``.
        line_regexp: Require the pattern to match the entire line.
        fixed: Treat the pattern as a literal string. Reach for this when the
            text contains regex characters you mean literally.
        count_only: Report how many lines matched and return none of them.
            Cheapest way to ask whether something appears at all.
        context: Lines of context on both sides of each match, at most 50.
        before: Lines of context above each match, overriding ``context``.
        after: Lines of context below each match, overriding ``context``. Pass
            0 to suppress the side ``context`` would have set.
        max_matches: Cap on matches returned, at most 2000.

    Returns:
        The matches with their line numbers and any context asked for, plus the
        exact total.

    Raises:
        Exception: A ``ToolError`` when the pattern is unusable or too slow to
            finish, or the run has no stored log yet.
    """
    lines = [line.content for line in workspace().job_runs.get(id=run_id).logs()]
    return search(
        run_id,
        lines,
        pattern,
        ignore_case=ignore_case,
        invert=invert,
        word=word,
        line_regexp=line_regexp,
        fixed=fixed,
        count_only=count_only,
        before=context if before is None else before,
        after=context if after is None else after,
        max_matches=max_matches,
    )


__tools__ = (dlthub_get_run_logs, dlthub_grep_run_logs)
