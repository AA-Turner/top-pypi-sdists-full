"""Tool-result density helpers for CLI rendering (#1367).

Pure helpers — no I/O, no Rich console writes. The renderer imports
``densify_output`` and ``collapse_diff_hunks`` and uses them to decide *what*
to show for a tool call's end-of-call body. Keeping these as pure functions
lets unit tests assert exact string output without a terminal.

Defaults are *byte-identical* to the pre-#1367 behaviour: density ``NORMAL``
returns inputs untouched. Other modes are opt-in via ``cli.density.mode`` /
``AI_CHAT_CLI_DENSITY_MODE`` / the ``/density`` slash command.
"""

from __future__ import annotations

from enum import Enum
from typing import Iterable, Sequence


class ToolResultDensity(Enum):
    """Four levels of tool-result density, narrow → wide.

    * ``MINIMAL`` — hide body entirely, show only the one-line tool summary.
    * ``COMPACT`` — head/tail slice of the body with a ``[+N lines]`` hint.
    * ``NORMAL`` — byte-identical to pre-#1367 rendering. This is the default.
    * ``DETAILED`` — expand the body fully (with a very high safety cap).
    """

    MINIMAL = "minimal"
    COMPACT = "compact"
    NORMAL = "normal"
    DETAILED = "detailed"


# Absolute ceiling on how many body lines ``DETAILED`` will print before
# adding a truncation marker. Prevents a pathological 10_000-line payload
# from flooding the terminal even when the user asks for "detailed".
_DETAILED_LINE_CAP = 200


def parse_density(value: str | None) -> ToolResultDensity:
    """Parse a density string (case-insensitive) into a ``ToolResultDensity``.

    Unknown or empty values fall back to ``NORMAL`` — the fail-safe default.
    """
    if not value:
        return ToolResultDensity.NORMAL
    lowered = value.strip().lower()
    for member in ToolResultDensity:
        if member.value == lowered:
            return member
    return ToolResultDensity.NORMAL


def densify_output(
    output: str,
    density: ToolResultDensity,
    *,
    head_lines: int,
    tail_lines: int,
) -> str:
    """Return a density-aware rendering of ``output``.

    The helper does *not* emit Rich markup — it returns plain text that the
    renderer then escapes / styles as usual.

    Contract:
        - ``NORMAL`` returns ``output`` byte-identical.
        - ``MINIMAL`` returns an empty string (caller hides the body row entirely).
        - ``COMPACT`` keeps the first ``head_lines`` and last ``tail_lines``,
          replacing the middle with a single ``"... [+N lines]"`` marker when
          the payload has more lines than ``head+tail``.
        - ``DETAILED`` returns the full payload, capped at ``_DETAILED_LINE_CAP``
          lines to avoid terminal floods.
    """
    if density == ToolResultDensity.NORMAL:
        return output

    if density == ToolResultDensity.MINIMAL:
        return ""

    if density == ToolResultDensity.DETAILED:
        if not output:
            return ""
        lines = output.split("\n")
        if len(lines) <= _DETAILED_LINE_CAP:
            return output
        kept = lines[:_DETAILED_LINE_CAP]
        omitted = len(lines) - _DETAILED_LINE_CAP
        kept.append(f"... [+{omitted} lines truncated]")
        return "\n".join(kept)

    # COMPACT
    if not output:
        return ""
    head_lines = max(0, head_lines)
    tail_lines = max(0, tail_lines)
    lines = output.split("\n")
    if len(lines) <= head_lines + tail_lines:
        return output
    omitted = len(lines) - head_lines - tail_lines
    parts: list[str] = []
    if head_lines:
        parts.extend(lines[:head_lines])
    parts.append(f"... [+{omitted} lines]")
    if tail_lines:
        parts.extend(lines[-tail_lines:])
    return "\n".join(parts)


_CONTEXT_MARKER_TAG = "~"


def collapse_diff_hunks(
    hunk_lines: Iterable[tuple[str, str]],
    *,
    context_lines: int,
    density: ToolResultDensity,
) -> Sequence[tuple[str, str]]:
    """Return hunk lines with middle context runs collapsed per density.

    ``hunk_lines`` is a sequence of ``(tag, content)`` pairs where ``tag`` is
    one of ``" "`` (unchanged), ``"+"`` (added), or ``"-"`` (removed). The
    helper preserves every change line (``+``/``-``) and collapses long runs
    of unchanged context. Marker rows use the tag ``"~"`` so the renderer can
    display them differently (e.g. ``…``).

    Modes:
        - ``NORMAL`` / ``DETAILED``: pass-through.
        - ``COMPACT``: runs of unchanged lines longer than
          ``2 * context_lines + 1`` keep ``context_lines`` at each end and
          insert a single marker ``("~", "[N unchanged lines]")`` between them.
        - ``MINIMAL``: drop every unchanged line, keep only ``+``/``-``.
    """
    hunk_list = list(hunk_lines)

    if density in (ToolResultDensity.NORMAL, ToolResultDensity.DETAILED):
        return hunk_list

    if density == ToolResultDensity.MINIMAL:
        return [pair for pair in hunk_list if pair[0] in ("+", "-")]

    # COMPACT: collapse long runs of context.
    context_lines = max(0, context_lines)
    # Threshold: only collapse a run when hiding at least one context line
    # would shorten the output. That means runs strictly longer than
    # 2 * context_lines + 1 (leaving head + tail + ≥1 collapsed row).
    threshold = 2 * context_lines + 1

    result: list[tuple[str, str]] = []
    i = 0
    n = len(hunk_list)
    while i < n:
        tag, content = hunk_list[i]
        if tag == " ":
            # Find the length of this context run.
            j = i
            while j < n and hunk_list[j][0] == " ":
                j += 1
            run_len = j - i
            if run_len > threshold:
                # Keep head context, marker, tail context.
                if context_lines:
                    result.extend(hunk_list[i : i + context_lines])
                omitted = run_len - 2 * context_lines
                result.append((_CONTEXT_MARKER_TAG, f"[{omitted} unchanged lines]"))
                if context_lines:
                    result.extend(hunk_list[j - context_lines : j])
            else:
                result.extend(hunk_list[i:j])
            i = j
        else:
            result.append((tag, content))
            i += 1

    return result
