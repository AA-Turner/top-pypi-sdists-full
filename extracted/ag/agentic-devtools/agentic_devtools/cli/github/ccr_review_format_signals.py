"""CCR verdict and suppression signal parsing."""

from __future__ import annotations

import agentic_devtools.cli.github.ccr_review_format as _format


def parse_verdict(body: str) -> str | None:
    """Parse the review verdict from a new-style CCR heading.

    Scans for ``###``-level headings introduced by the new CCR private-preview
    format (e.g. ``### 🟡 Not ready to approve``, ``### ✅ Ready to approve``)
    and returns the verdict from the first heading that expresses one.

    ``"not ready to approve"`` is checked before ``"ready to approve"`` so the
    substring match cannot mis-classify a blocking heading as approving.

    Args:
        body: Full review body text.

    Returns:
        :data:`VERDICT_NOT_APPROVE` when a blocking verdict heading is found,
        :data:`VERDICT_APPROVE` when an approving verdict heading is found, or
        ``None`` when no recognised CCR verdict heading is present (in which
        case callers should fall back to their existing logic).
    """
    if not body:
        return None
    for match in _format._HEADING_RE.finditer(body):
        heading_text = match.group(1).strip().lower()
        if "not ready to approve" in heading_text:
            return _format.VERDICT_NOT_APPROVE
        if "ready to approve" in heading_text:
            return _format.VERDICT_APPROVE
    return None


def parse_suppressed_count(body: str) -> int:
    """Parse the suppressed / low-confidence comment count from *body*.

    Matches ``… suppressed … (N)`` — and, as a fallback, ``… low confidence …
    (N)`` — but only when the count is anchored to a markdown heading (``###
    Suppressed comments (N)``, at any level h1–h6) or a ``<summary>`` element
    (``<summary>Comments suppressed due to low confidence (N)</summary>``).
    Counts appearing in ordinary prose, or inside a fenced code block, are
    ignored so review narrative cannot fabricate a suppressed count.

    Both pattern families are scanned for a nonzero value before committing
    to zero.  This means a body that contains ``### Suppressed comments (0)``
    followed by ``### Low confidence (1)`` returns ``1`` — the zero declaration
    does not short-circuit the search for a nonzero sibling declaration.

    Args:
        body: Full review body text.

    Returns:
        The first nonzero count found across all anchored suppressed-count
        patterns, or ``0`` when every match is zero or no match exists.
        See :func:`unrecovered_suppression_signal` for the fail-closed
        backstop that covers an unanchored count naming real findings.
    """
    if not body:
        return 0
    masked = _format._mask_inline_code(_format._mask_fenced_blocks(body))
    # Scan *all* pattern families before committing to zero: a body that contains
    # "### Suppressed comments (0)" followed by "### Low confidence (1)" must
    # return 1 so that extraction and the sentinel are not suppressed by the
    # earlier zero declaration.
    for pattern in (_format._SUPPRESSED_COUNT_RE, _format._LOW_CONFIDENCE_COUNT_RE):
        for m in pattern.finditer(masked):
            n = int(m.group(1))
            if n:
                return n
    # No nonzero declaration found; return 0 whether or not a zero appeared.
    return 0


def unrecovered_suppression_signal(body: str) -> bool:
    """Return ``True`` when *body* advertises a suppressed count the parser lost.

    The structured parser is deliberately strict: it only counts a suppressed
    total that is anchored to a heading or a ``<summary>``.  This sentinel is the
    fail-closed backstop for that strictness — it fires when an *unanchored*
    count is present, the structured parser recovered nothing, and entry-shaped
    lines follow that count.  Callers must treat a firing sentinel as "cannot
    conclude clean" rather than returning a clean verdict.

    Firing blocks the merge without dispatching a repair agent, so the two probes
    are kept deliberately narrow to avoid blocking a genuinely clean review:

    - The count is read from a copy with both fenced blocks and inline code spans
      masked, so a review that merely *quotes* ``\u0060Suppressed comments (3)\u0060``
      in its narrative does not trip the sentinel.
    - A supported entry header must appear *after* a nonzero unanchored count, as
      in a real suppressed section, so an earlier zero declaration does not block
      a clean review.  That probe runs on the fence-masked (not inline-masked)
      copy so backticked ``\u0060path\u0060`` and legacy inline ``**path**: body``
      entries still count; both copies preserve offsets, so the positions are
      interchangeable.

    Args:
        body: Full review body text.

    Returns:
        ``True`` when an unanchored suppressed count is followed by entry-shaped
        lines while the structured parser yielded neither count nor entries;
        ``False`` otherwise.
    """
    if not body:
        return False
    if parse_suppressed_count(body) or _format.extract_suppressed_comment_entries(body):
        return False
    fence_masked = _format._mask_fenced_blocks(body)
    both_masked = _format._mask_inline_code(fence_masked)
    for count_pattern in (_format._UNANCHORED_SUPPRESSED_COUNT_RE, _format._UNANCHORED_LOW_CONFIDENCE_COUNT_RE):
        for count in count_pattern.finditer(both_masked):
            if int(count.group(1)) == 0:
                continue
            if _format._ENTRY_HEADER_ONLY_RE.search(
                fence_masked, count.end()
            ) or _format._ENTRY_HEADER_INLINE_RE.search(fence_masked, count.end()):
                return True
    return False
