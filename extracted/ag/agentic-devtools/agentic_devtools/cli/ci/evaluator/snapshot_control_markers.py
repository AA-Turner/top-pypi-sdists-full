"""Trusted control markers that must not be synthesized by comment repair."""

from __future__ import annotations

import re

from ..guards import (
    CYCLE_TRACKER_MARKER,
    DEDUP_MARKER_PATTERN,
    REPAIR_SATISFIED_MARKER,
    REVIEW_ID_MARKER_RE,
    THREAD_EVALUATED_MARKER,
)
from .lock import _LOCK_MARKER as _EVALUATOR_LOCK_MARKER

_SENTINEL_MARKER = "<!-- copilot-agent-result -->"

# Issue-comment control markers whose exact spelling the HTML-comment balancer
# could synthesize by inserting a closing ``-->`` into a truncated opener (e.g.
# ``<!-- ai-pr-loop:repair-satisfied`` at end of a quoted line becomes the
# canonical marker). If a sanitized rewrite would introduce one of these trusted
# signals — or a ``review-id`` marker — that was not already present, the rewrite
# must not be persisted back to the provider: a later evaluator run would
# otherwise treat the synthesized marker as a genuine Copilot signal (for
# example incorrectly clearing a suppressed-comments block).
_SYNTHESIZABLE_CONTROL_MARKERS = (
    _SENTINEL_MARKER,
    REPAIR_SATISFIED_MARKER,
    THREAD_EVALUATED_MARKER,
    CYCLE_TRACKER_MARKER,
    _EVALUATOR_LOCK_MARKER,
)

# Variable-content dedup/dispatch markers the balancer could likewise synthesize
# by closing a truncated opener. Their embedded fields (review id, SHAs, ISO-8601
# timestamp) mean a fixed-string ``.count`` check is insufficient, so the full
# ordered list of complete markers is compared instead (as with ``review-id``):
#
# * ``<!-- copilot-trigger:{review_id}[:{iso8601_utc}] -->`` — scanned by
#   :func:`is_duplicate_trigger`; a synthesized marker with an unparseable
#   timestamp is treated as a non-expiring duplicate, permanently suppressing a
#   legitimate re-dispatch.
# * ``<!-- repair-dispatch:{sha}:{count}:{writer_token} -->`` — parsed by
#   :data:`DEDUP_MARKER_PATTERN` in :func:`check_deduplication`; a synthesized
#   marker can shadow the real dedup-tracking comment and skew the dispatch
#   count or redirect the next update into a Copilot-authored comment.
# * ``<!-- agdt:conflict-repair:{base}:{head}:{iso8601_utc} -->`` — located by
#   ``find_comment(CONFLICT_REPAIR_MARKER_PREFIX)`` on behalf of
#   :class:`~agentic_devtools.cli.ci.pipeline.actions.dispatch_conflict_resolution.DispatchConflictResolutionAction`.
#   Both ``should_dispatch_conflict_repair`` and ``count_conflict_repair_dispatches``
#   are identity-scoped to the PR-token login (``dispatch_login``), so neither a
#   verbatim quote nor a synthesized marker in a Copilot-authored comment can
#   affect deduplication or the attempt count — they are equally inert.
#   The escaping here is therefore defense in depth rather than a load-bearing
#   protection.
#
# Each pattern requires the closing ``-->`` (which the balancer inserts), so a
# truncated opener present in the original body does not match until it has been
# balanced — the resulting mismatch blocks persistence.
_COPILOT_TRIGGER_MARKER_RE = re.compile(r"<!--\s*copilot-trigger:[^>]*?-->")
_REPAIR_ACCOUNTING_MARKER_RE = re.compile(r"<!--\s*repair-dispatch:(?:v2|work|exhausted):[^>]*?-->")
_CONFLICT_REPAIR_MARKER_RE = re.compile(r"<!--\s*agdt:conflict-repair:[^>]*?-->")
_SYNTHESIZABLE_CONTROL_MARKER_PATTERNS = (
    REVIEW_ID_MARKER_RE,
    _COPILOT_TRIGGER_MARKER_RE,
    DEDUP_MARKER_PATTERN,
    _REPAIR_ACCOUNTING_MARKER_RE,
    _CONFLICT_REPAIR_MARKER_RE,
)


def _neutralize_synthesized_control_markers(body: str, inserted_positions: tuple[int, ...]) -> str:
    """Escape any trusted marker whose closing ``-->`` was synthesized by balancing."""
    opener_positions: set[int] = set()
    for pos in inserted_positions:
        open_idx = body.rfind("<!--", 0, pos)
        if open_idx == -1:
            continue
        candidate = body[open_idx : pos + 4]
        if candidate in _SYNTHESIZABLE_CONTROL_MARKERS or any(
            pattern.fullmatch(candidate) for pattern in _SYNTHESIZABLE_CONTROL_MARKER_PATTERNS
        ):
            opener_positions.add(open_idx)
    if not opener_positions:
        return body
    pieces: list[str] = []
    prev = 0
    for open_idx in sorted(opener_positions):
        pieces.append(body[prev:open_idx])
        pieces.append("&lt;!--")
        prev = open_idx + 4
    pieces.append(body[prev:])
    return "".join(pieces)


def _introduces_control_marker(original: str, sanitized: str) -> bool:
    """Return True when *sanitized* gains a trusted control marker absent in *original*.

    The HTML-comment balancer inserts a closing ``-->`` into a truncated
    ``<!--`` opener. That can synthesize the *exact* spelling of a trusted
    issue-comment control marker (e.g. :data:`REPAIR_SATISFIED_MARKER` or a
    ``review-id`` marker) that a later evaluator run would accept as a genuine
    Copilot signal. Persistence paths neutralize those synthesized markers
    first; this helper remains the final safety check that no trusted signal
    absent in the original body survives the rewrite.

    Presence alone is insufficient: a comment may already carry one legitimate
    marker while balancing forges a *second* one (e.g. an earlier truncated
    ``<!-- review-id:999`` alongside a valid ``<!-- review-id:123 -->``). A
    later run reading the first regex match would then trust the wrong signal.
    Compare marker *counts* and the complete ordered list of matches — for the
    ``review-id`` marker as well as the variable-content ``copilot-trigger``
    dedup marker, ``repair-dispatch`` dedup marker, and
    ``agdt:conflict-repair`` dispatch marker — so any newly synthesized trusted
    signal blocks persistence.
    """
    for marker in _SYNTHESIZABLE_CONTROL_MARKERS:
        if sanitized.count(marker) > original.count(marker):
            return True
    for pattern in _SYNTHESIZABLE_CONTROL_MARKER_PATTERNS:
        if pattern.findall(sanitized) != pattern.findall(original):
            return True
    return False
