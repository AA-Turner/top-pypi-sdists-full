"""A grep-shaped search over a run's log lines.

No external process: the CLI supports Windows, where there is no ``grep``, and
shelling out nothing removes the command-injection surface rather than trying
to sanitise it. The options are the flags a caller would reach for, taken as
typed arguments — an MCP caller reads a schema, so an unsupported option cannot
be expressed and there is nothing to refuse.

``regex`` rather than ``re``, for its ``timeout``. The pattern is agent-written
and a backtracking one cannot be interrupted out of ``re``: signals reach only
the main thread, and an MCP server runs its sync tools off it. Unbounded, one
such pattern wedges the whole server rather than the single call.
"""

from __future__ import annotations

# Python internals
import time
from dataclasses import dataclass
from typing import Iterable

# Other libraries
import regex

#: Matches returned when the caller does not say, and the ceiling it may ask for.
MAX_MATCHES = 200
MAX_MATCHES_CAP = 2_000
#: Context lines either side of a match, and the longest pattern accepted.
MAX_CONTEXT_LINES = 50
MAX_PATTERN_LENGTH = 1_000
#: Seconds of matching the whole search shares out. Spending it does not end
#: the search, it only holds every remaining line to `_SPENT`.
SEARCH_TIMEOUT = 5.0
#: Handed to `regex` once the budget is gone, so it gives up rather than reading
#: a non-positive timeout as no timeout at all.
_SPENT = 0.001
#: A POSIX class. `regex` honours it, but the pattern is documented as a Python
#: regular expression, so it stays refused rather than working by engine luck.
_POSIX_CLASS = regex.compile(r"\[:[a-z]+:\]")


class LogSearchError(ValueError):
    """An unusable pattern. A ValueError, so `tool` reports it to the agent."""


@dataclass(frozen=True)
class LogMatch:
    """One line that matched, and the lines around it when asked for.

    Attributes:
        line_number: Its 1-based position in the whole log.
        line: What the line said.
        context_before: Lines immediately above, when ``before`` asked for any.
        context_after: Lines immediately below, when ``after`` asked for any.
    """

    line_number: int
    line: str
    context_before: tuple[str, ...] = ()
    context_after: tuple[str, ...] = ()


@dataclass(frozen=True)
class LogSearchResult:
    """What a search over one run's log found.

    Attributes:
        run_id: The run that was searched.
        pattern: The pattern it was searched for.
        matches: The matches, capped at what the caller allowed.
        match_count: How many lines matched in total. Exact even when
            ``matches`` was capped, and all ``count_only`` returns.
        searched_lines: How many lines the log holds.
        truncated: Whether ``match_count`` exceeds the matches returned.
    """

    run_id: str
    pattern: str
    matches: tuple[LogMatch, ...]
    match_count: int
    searched_lines: int
    truncated: bool


def _compile(
    pattern: str,
    *,
    ignore_case: bool,
    word: bool,
    line_regexp: bool,
    fixed: bool,
) -> regex.Pattern[str]:
    """Build the pattern the options describe.

    Args:
        pattern: The caller's pattern, a Python regular expression.
        ignore_case: Match regardless of case.
        word: Require whole-word matches.
        line_regexp: Require the pattern to match the entire line.
        fixed: Treat the pattern as a literal string.

    Returns:
        The compiled pattern.

    Raises:
        LogSearchError: The pattern is empty, over length, carries a POSIX
            class, or is not a valid regex.
    """
    if not pattern:
        raise LogSearchError("a search pattern is required")
    if len(pattern) > MAX_PATTERN_LENGTH:
        raise LogSearchError(f"pattern is longer than {MAX_PATTERN_LENGTH} characters")
    if not fixed and _POSIX_CLASS.search(pattern):
        raise LogSearchError(
            "invalid pattern: POSIX classes such as [[:digit:]] are not supported. "
            "The pattern is a Python regular expression, so use \\d, \\w or \\s, "
            "or pass fixed=True to search for the text literally."
        )
    body = regex.escape(pattern) if fixed else pattern
    if line_regexp:
        body = rf"\A(?:{body})\Z"
    elif word:
        body = rf"\b(?:{body})\b"
    try:
        return regex.compile(body, regex.IGNORECASE if ignore_case else 0)
    except regex.error as e:
        raise LogSearchError(f"invalid pattern: {e}") from e


def search(
    run_id: str,
    lines: Iterable[str],
    pattern: str,
    *,
    ignore_case: bool = False,
    invert: bool = False,
    word: bool = False,
    line_regexp: bool = False,
    fixed: bool = False,
    count_only: bool = False,
    before: int = 0,
    after: int = 0,
    max_matches: int = MAX_MATCHES,
) -> LogSearchResult:
    """Search a run's log, line by line.

    Args:
        run_id: The run the lines came from, echoed back on the result.
        lines: Every line of the log, oldest first.
        pattern: A Python regular expression, or a literal when ``fixed``.
        ignore_case: Match regardless of case.
        invert: Return the lines that did *not* match.
        word: Require whole-word matches.
        line_regexp: Require the pattern to match the entire line.
        fixed: Treat the pattern as a literal string, not a regex.
        count_only: Report ``match_count`` and return no matches.
        before: Lines of context above each match, capped at 50.
        after: Lines of context below each match, capped at 50.
        max_matches: Cap on matches returned. ``match_count`` stays exact.

    Returns:
        The matches, and how many there were in total.

    Raises:
        LogSearchError: The pattern was refused, or was still slow once
            :data:`SEARCH_TIMEOUT` had been spent.
    """
    compiled = _compile(
        pattern,
        ignore_case=ignore_case,
        word=word,
        line_regexp=line_regexp,
        fixed=fixed,
    )
    limit = max(1, min(max_matches or MAX_MATCHES, MAX_MATCHES_CAP))
    above = max(0, min(before, MAX_CONTEXT_LINES))
    below = max(0, min(after, MAX_CONTEXT_LINES))

    # Kept whole because `before` needs lines already passed and `after` lines
    # not yet read.
    body = list(lines)
    found: list[LogMatch] = []
    count = 0
    # One budget shared across the lines, not one per line. Spending it leaves
    # each remaining line `_SPENT`, so only a still-slow pattern trips.
    deadline = time.monotonic() + SEARCH_TIMEOUT
    for position, line in enumerate(body):
        try:
            hit = compiled.search(
                line, timeout=max(_SPENT, deadline - time.monotonic())
            )
        except TimeoutError as e:
            raise LogSearchError(
                f"the search gave up after {SEARCH_TIMEOUT:g}s at line "
                f"{position + 1} of {len(body)}. The pattern is too slow on this "
                "log — anchor it, drop a nested repetition such as (a+)+, or pass "
                "fixed=True to search for the text literally."
            ) from e
        if (hit is not None) is invert:
            continue
        count += 1
        if count_only or len(found) >= limit:
            continue
        found.append(
            LogMatch(
                line_number=position + 1,
                line=line,
                context_before=tuple(body[max(0, position - above) : position]),
                context_after=tuple(body[position + 1 : position + 1 + below]),
            )
        )

    return LogSearchResult(
        run_id=run_id,
        pattern=pattern,
        matches=tuple(found),
        match_count=count,
        searched_lines=len(body),
        truncated=count > len(found) and not count_only,
    )


__all__ = [
    "MAX_CONTEXT_LINES",
    "MAX_MATCHES",
    "MAX_MATCHES_CAP",
    "MAX_PATTERN_LENGTH",
    "SEARCH_TIMEOUT",
    "LogMatch",
    "LogSearchError",
    "LogSearchResult",
    "search",
]
