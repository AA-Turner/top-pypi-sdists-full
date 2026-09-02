"""Canonical parsers for Copilot Code Review (CCR) review bodies.

This module is the **single source of truth** for extracting structured
information from a Copilot Code Review body.  It understands two body formats:

**Legacy format** — prose summary with:

- ``"generated N comment(s)"`` / ``"generated no comments"`` phrasing.
- ``Suppressed (N)`` / ``Low confidence (N)`` counts, in a ``<summary>`` element.
- A ``<details><summary>… suppressed due to low confidence …</summary>…</details>``
  block (or the newer bare ``<details><summary>Suppressed comments (N)</summary>…``
  block) whose entries are ``**path**: body`` / ``` `path`: body ``` lines, or the
  new format's ``**path:line**`` header followed by a ``* body`` bullet.

**New CCR private-preview format** — a ``### <emoji> <verdict>`` heading
(``### 🟡 Not ready to approve`` / ``### ✅ Ready to approve``) followed by a
``<details><summary>Review details</summary>`` block containing:

- A markdown heading naming the suppressed set with a parenthesised count —
  observed as both ``### Comments suppressed due to low confidence (N)`` and
  ``### Suppressed comments (N)`` — whose entries are ``**path:line**`` on one
  line followed by a ``* body`` bullet (and, often, a fenced code block).
- A metrics footer (``- **Files reviewed:** …``, ``- **Comments generated:** N``,
  ``- **Review effort level:** …``).

The suppressed-comment format is an unpublished contract that has already used
several anchor spellings, so the block anchor is deliberately format-agnostic
(any ``suppressed … (N)`` heading at levels h1–h6, or a ``<summary>``) rather
than a list of literal headings.  Fenced code excerpts are masked before any
block/entry/count matching so CCR's embedded snippets cannot fabricate block
boundaries or entries.

Centralising this logic keeps every consumer in the AI PR loop consistent:

- :mod:`agentic_devtools.cli.ci.pipeline.gate_verdict` (approval/merge gate)
- :mod:`agentic_devtools.cli.ci.github_provider` (suppressed-comment recovery
  for repair dispatch)
- :mod:`agentic_devtools.cli.github.copilot_review_status` (poll-ready
  review-status classification)

Public API
----------
- :data:`VERDICT_NOT_APPROVE`, :data:`VERDICT_APPROVE` — verdict constants.
- :data:`UNKNOWN_FILE` — placeholder path for unattributed suppressed comments.
- :func:`parse_verdict` — new-format ``### <verdict>`` heading → verdict.
- :func:`parse_reported_comment_count` — self-reported posted-comment count.
- :func:`parse_suppressed_count` — self-reported suppressed/low-confidence count.
- :func:`extract_suppressed_comment_entries` — ``(path, body)`` pairs for every
  recoverable suppressed comment (both formats).
- :func:`unrecovered_suppression_signal` — fail-closed sentinel for a suppressed
  count the structured parser could not recover.
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# Public constants
# ---------------------------------------------------------------------------

#: Verdict returned when the new-format heading blocks approval.
VERDICT_NOT_APPROVE = "not_approve"

#: Verdict returned when the new-format heading approves.
VERDICT_APPROVE = "approve"

#: Placeholder path used when a suppressed comment cannot be attributed to a file.
UNKNOWN_FILE = "(unknown file)"

# ---------------------------------------------------------------------------
# Verdict heading
# ---------------------------------------------------------------------------

#: Matches any ``###``-level (or deeper) heading line; the heading text is captured.
_HEADING_RE = re.compile(r"^#{3,}\s+(.+?)\s*$", re.MULTILINE)


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
    for match in _HEADING_RE.finditer(body):
        heading_text = match.group(1).strip().lower()
        if "not ready to approve" in heading_text:
            return VERDICT_NOT_APPROVE
        if "ready to approve" in heading_text:
            return VERDICT_APPROVE
    return None


# ---------------------------------------------------------------------------
# Reported comment count
# ---------------------------------------------------------------------------

#: Legacy "generated no [new] comments" phrasing → count 0.
_GENERATED_NONE_RE = re.compile(r"generated no( new)? comments", re.IGNORECASE)

#: Legacy "generated N comment(s)" phrasing → count N.
_GENERATED_N_RE = re.compile(r"generated (\d+) comment", re.IGNORECASE)

#: New CCR metrics-footer "**Comments generated:** N [new]" → count N.
#: The trailing "new" qualifier is optional — some reviews report a bare count
#: (``**Comments generated:** 4``) while re-reviews report ``0 new``.
_METRICS_GENERATED_RE = re.compile(
    r"Comments generated[^:\n]*:\s*\*{0,2}\s*(\d+)(?:\s+new)?\b",
    re.IGNORECASE,
)


def parse_reported_comment_count(body: str) -> int | None:
    """Parse Copilot's self-reported posted-comment count from *body*.

    Matches, in priority order:

    - ``"generated no comments"`` / ``"generated no new comments"`` → ``0``
    - ``"generated N comment(s)"`` → ``N``
    - ``"**Comments generated:** N [new]"`` (new CCR metrics footer) → ``N``

    Args:
        body: Full review body text.

    Returns:
        An integer count, or ``None`` when no recognised count pattern is
        present (callers fail closed on ``None``).
    """
    if not body:
        return None
    if _GENERATED_NONE_RE.search(body):
        return 0
    match = _GENERATED_N_RE.search(body)
    if match:
        return int(match.group(1))
    match = _METRICS_GENERATED_RE.search(body)
    if match:
        return int(match.group(1))
    return None


# ---------------------------------------------------------------------------
# Fenced-code masking
# ---------------------------------------------------------------------------

#: Opening/closing delimiter of a fenced code block (``` or ~~~), with up to
#: three leading spaces of indentation as allowed by CommonMark.
_FENCE_DELIM_RE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})")


def _mask_fenced_blocks(text: str) -> str:
    """Return *text* with every fenced-code line replaced by equal-length spaces.

    Offsets are preserved so a match found on the masked text can be used to
    slice the original.  CCR embeds a fenced code excerpt under each suppressed
    comment; that excerpt frequently contains markdown headings and ``**bold**``
    runs which must never be mistaken for block or entry boundaries.

    Args:
        text: Markdown text to mask.

    Returns:
        A string of the same length as *text* in which every line belonging to a
        fenced code block (including its delimiter lines) is blanked out.
    """
    masked: list[str] = []
    open_delim: str | None = None
    for line in text.split("\n"):
        match = _FENCE_DELIM_RE.match(line)
        if open_delim is None:
            if match:
                if match.group(1).startswith("`") and "`" in line[match.end() :]:
                    masked.append(line)
                    continue
                open_delim = match.group(1)
                masked.append(" " * len(line))
                continue
            masked.append(line)
            continue
        if (
            match
            and match.group(1)[0] == open_delim[0]
            and len(match.group(1)) >= len(open_delim)
            and line[match.end() :].strip() == ""
        ):
            open_delim = None
        masked.append(" " * len(line))
    return "\n".join(masked)


#: An inline code span (``` `text` ```). The closing run must match the opening
#: run length exactly, while still remaining single-line so an unmatched
#: backtick cannot swallow the rest of the body.
_INLINE_CODE_RE = re.compile(r"(?P<ticks>`+)[^\n]*?(?P=ticks)")


def _mask_inline_code(text: str) -> str:
    """Return *text* with every inline code span replaced by equal-length spaces.

    Offsets are preserved, exactly as in :func:`_mask_fenced_blocks`, so results
    from either masking can be compared or used to slice the original.  A review
    that quotes a count in backticks is narrating, not declaring, so the span is
    blanked before the unanchored-count probe runs.

    Args:
        text: Markdown text to mask.

    Returns:
        A string of the same length as *text* with inline code spans blanked out.
    """
    return _INLINE_CODE_RE.sub(lambda match: " " * len(match.group(0)), text)


# ---------------------------------------------------------------------------
# Suppressed / low-confidence count
# ---------------------------------------------------------------------------

#: Heading-or-``<summary>`` anchor shared by every declaration pattern below.
#: Keeping one definition is what makes the count and the block anchor
#: structurally identical; see :data:`_SUPPRESSED_ANCHOR_RE`.
_ANCHOR = r"(?:^[ \t]{0,3}#{1,6}[ \t]+|<summary>)"

#: The suppressed declaration itself, without its anchor.
#:
#: Supports both the legacy bare form ``Suppressed (N)`` and the newer
#: ``Suppressed comment(s) (N)`` spelling.  Word boundaries still reject
#: look-alikes like ``Unsuppressed comments (N)`` and
#: ``Suppressed commentary (N)``.
_SUPPRESSED_DECLARATION = r"[^\n<]*?\bsuppressed\b(?:\s*|[^.(\n<]*\bcomments?\b[^.(\n<]*)\((\d+)\)"

#: The "… low confidence … (N)" fallback declaration, without its anchor.
_LOW_CONFIDENCE_DECLARATION = r"[^\n<]*?low confidence[^.(\n<]*\((\d+)\)"

#: "… suppressed … (N)" anchored to a markdown heading or a ``<summary>`` element
#: so that prose mentioning "Suppressed comment (1)" is never counted.
_SUPPRESSED_COUNT_RE = re.compile(_ANCHOR + _SUPPRESSED_DECLARATION, re.IGNORECASE | re.MULTILINE)

#: "… low confidence … (N)" fallback, anchored the same way.
_LOW_CONFIDENCE_COUNT_RE = re.compile(_ANCHOR + _LOW_CONFIDENCE_DECLARATION, re.IGNORECASE | re.MULTILINE)


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
    masked = _mask_inline_code(_mask_fenced_blocks(body))
    # Scan *all* pattern families before committing to zero: a body that contains
    # "### Suppressed comments (0)" followed by "### Low confidence (1)" must
    # return 1 so that extraction and the sentinel are not suppressed by the
    # earlier zero declaration.
    for pattern in (_SUPPRESSED_COUNT_RE, _LOW_CONFIDENCE_COUNT_RE):
        for m in pattern.finditer(masked):
            n = int(m.group(1))
            if n:
                return n
    # No nonzero declaration found; return 0 whether or not a zero appeared.
    return 0


# ---------------------------------------------------------------------------
# Suppressed block location
# ---------------------------------------------------------------------------

#: Legacy/bare-summary ``<details>`` block whose ``<summary>`` names the
#: suppressed set.  Matches both the older ``… suppressed due to low confidence
#: …`` summary and the newer bare ``Suppressed comments (N)`` summary.  Anchoring
#: on ``suppressed`` followed by either ``comment(s)`` or ``low confidence``
#: (rather than a bare ``suppressed``) keeps the match specific to
#: suppressed-comment blocks and avoids matching unrelated ``<details>`` sections.
#: Both halves of that phrase are word-bounded so a summary that merely *contains*
#: the substrings — ``Unsuppressed comments``, ``Suppressed commentary`` — is not
#: mistaken for a suppressed-comment block and handed to the repair agent.
#: Attributes on the ``<details>`` tag (``<details open>``) are tolerated.
_LEGACY_SUPPRESSED_BLOCK_RE = re.compile(
    r"<details(?:\s[^>]*)?>\s*<summary>([^<]*\bsuppressed\b[^<]*\b(?:comments?|low confidence)\b[^<]*)</summary>"
    r"(.*?)</details>",
    re.DOTALL | re.IGNORECASE,
)

#: Opens an anchored suppressed block.  This is deliberately the union of the two
#: count patterns, so the block anchor and the count can never disagree: every
#: declaration :func:`parse_suppressed_count` reads also opens a block.  That
#: makes the "declared N > 0 but zero entries recovered" stall structurally
#: impossible to reintroduce via a heading level, a heading tail, a CRLF body, a
#: ``<summary>`` outside a recognised ``<details>``, or a future anchor spelling.
_SUPPRESSED_ANCHOR_RE = re.compile(
    _ANCHOR + r"(?:" + _SUPPRESSED_DECLARATION + r"|" + _LOW_CONFIDENCE_DECLARATION + r")",
    re.IGNORECASE | re.MULTILINE,
)

#: Terminates an anchored suppressed block: the next heading, the metrics footer,
#: or the close of the enclosing ``<details>``.
_SUPPRESSED_BLOCK_END_RE = re.compile(
    r"^[ \t]{0,3}#{1,6}[ \t]"
    r"|^[ \t]*[-*][ \t]+\*\*(?:Files reviewed|Comments generated|Review effort)"
    r"|</details>",
    re.IGNORECASE | re.MULTILINE,
)


def _find_suppressed_block(body: str) -> str | None:
    """Return the suppressed-comment block content for either format, or ``None``.

    Prefers the ``<details><summary>`` block (legacy ``… suppressed due to low
    confidence …`` or the newer bare ``Suppressed comments (N)`` summary); falls
    back to any anchored ``suppressed … (N)`` declaration — a markdown heading at
    any level, or a ``<summary>`` — whose section starts on the line after the
    declaration and runs until the next heading, the metrics footer, or the
    enclosing ``</details>``.  Zero-valued declarations (``(0)`` headings) are
    skipped outright so a ``(0)`` section with nonempty text (e.g. "No findings.")
    cannot mask a later nonzero declaration that carries the real findings.
    Anchors, fences, and inline code spans are located on masked copies so an
    embedded code excerpt or a literal ``</details>`` inside inline code can
    neither open nor close a block; the returned content is sliced from the
    original text so excerpts are preserved verbatim.

    Args:
        body: Full review body text.

    Returns:
        The block's inner content, or ``None`` when neither format is present or
        every located block is empty.
    """
    masked = _mask_fenced_blocks(body)
    double_masked = _mask_inline_code(masked)
    for legacy in _LEGACY_SUPPRESSED_BLOCK_RE.finditer(double_masked):
        summary = legacy.group(1)
        count_match = re.search(r"\((\d+)\)", summary)
        if count_match and int(count_match.group(1)) == 0:
            continue
        start, end = legacy.span(2)
        content = body[start:end].strip()
        if content:
            return content

    # Use the doubly-masked copy (fenced + inline) for boundary detection so
    # that ``</details>`` or a heading inside an inline code span cannot
    # terminate the block prematurely. Offsets are still valid against both
    # masked and body.
    for anchor in _SUPPRESSED_ANCHOR_RE.finditer(double_masked):
        # group(1) is the count from the suppressed alternative; group(2) from the
        # low-confidence alternative.  Exactly one will be non-None.
        # Skip zero-valued anchors so a ``(0)`` heading with nonempty text
        # (e.g. "No findings.") does not mask a later nonzero declaration.
        if int(anchor.group(1) or anchor.group(2)) == 0:
            continue
        newline = double_masked.find("\n", anchor.end())
        if newline == -1:
            continue  # Declaration on the last line — no content can follow it.
        end_match = _SUPPRESSED_BLOCK_END_RE.search(double_masked, newline + 1)
        end = end_match.start() if end_match else len(body)
        content = body[newline + 1 : end].strip()
        if content:
            return content
    return None


# ---------------------------------------------------------------------------
# Suppressed comment entries
# ---------------------------------------------------------------------------

#: New format: a bold/code file path alone on its line (``**path:line**``).
#: Also used by :func:`unrecovered_suppression_signal` as the "entry-shaped
#: line" probe — an entry-shaped line is exactly a header-only entry line.
#: ``\r`` is accepted before the end anchor so CRLF bodies — which GitHub
#: returns verbatim — still yield entries rather than the "count > 0, entries
#: = 0" stall.
_ENTRY_HEADER_ONLY_RE = re.compile(
    r"^[ \t]{0,3}(?:\*\*`?|`)([^`*\n]+?)(?:`?\*\*|`)[ \t]*:?[ \t\r]*$",
    re.MULTILINE,
)

#: Legacy format: a bold/code file path followed by ": body" on the same line.
_ENTRY_HEADER_INLINE_RE = re.compile(
    r"^[ \t]{0,3}(?:\*\*`?|`)([^`*\n]+?)(?:`?\*\*|`)[ \t]*:[ \t]*(?=\S)",
    re.MULTILINE,
)


def extract_suppressed_comment_entries(body: str) -> list[tuple[str, str]]:
    """Extract ``(path, body)`` pairs for suppressed comments in *body*.

    Handles both the legacy ``<details>`` block and any anchored ``suppressed …
    (N)`` declaration section — see :func:`_find_suppressed_block`.  Entry
    headers are located on a fence-masked copy
    of the block so that bold runs inside CCR's embedded code excerpts cannot be
    mistaken for entries; the comment bodies are then sliced from the original
    text so the excerpts are preserved verbatim.  When a structured entry has no
    file path, :data:`UNKNOWN_FILE` is used.  When the block contains no
    structured entries at all, each non-blank line becomes a standalone
    ``(UNKNOWN_FILE, line)`` fallback comment.

    Args:
        body: Full review body text (may contain HTML/Markdown).

    Returns:
        A list of ``(path, comment_body)`` tuples in document order.  Empty when
        no suppressed block is found or the block yields no non-empty content.
    """
    if not body:
        return []

    block = _find_suppressed_block(body)
    if not block:
        return []

    masked_block = _mask_fenced_blocks(block)

    # Entry headers keyed by their offset in the block, so an inline header
    # (``**path**: body``) always wins over a header-only one (``**path:line**``)
    # should both ever match the same line.  ``setdefault`` keeps that precedence
    # explicit instead of leaving it to iteration order.
    starts: dict[int, tuple[str, int]] = {}
    for match in _ENTRY_HEADER_INLINE_RE.finditer(masked_block):
        starts.setdefault(match.start(), (match.group(1).strip(), match.end()))
    for match in _ENTRY_HEADER_ONLY_RE.finditer(masked_block):
        starts.setdefault(match.start(), (match.group(1).strip(), match.end()))
    ordered = sorted(starts.items())

    entries: list[tuple[str, str]] = []
    for index, (_offset, (path, header_end)) in enumerate(ordered):
        next_offset = ordered[index + 1][0] if index + 1 < len(ordered) else len(block)
        text = block[header_end:next_offset].strip()
        # The new CCR format renders each comment as a markdown bullet
        # (``* comment``); strip a single leading bullet marker so the recovered
        # comment text is clean.  Legacy bodies carry no bullet, so this is a
        # no-op for them.
        if text[:2] in ("* ", "- "):
            text = text[2:].strip()
        if not text:
            continue
        entries.append((path or UNKNOWN_FILE, text))

    # Block matched but produced no structured entries — fail open, one comment
    # per non-blank, non-fenced line.
    if not entries:
        for original_line, masked_line in zip(block.split("\n"), masked_block.split("\n"), strict=False):
            if not masked_line.strip():
                continue
            entries.append((UNKNOWN_FILE, original_line.strip()))

    return entries


# ---------------------------------------------------------------------------
# Fail-closed sentinel  (this is NOT optional hardening)
# ---------------------------------------------------------------------------

#: The pre-fix count pattern, minus the heading/``<summary>`` anchor and scoped
#: to a single line (matching the anchored patterns' ``[^.(\n<]*`` class).  After
#: the fix, a count matching only this — neither in a heading nor a
#: ``<summary>`` — parses to 0.  That is the intended prose-false-positive
#: correction, but it is also the channel through which a real suppressed block
#: in an unrecognised wrapper could silently become "clean".
#:
#: Word-bounded identically to :data:`_SUPPRESSED_DECLARATION` so that known
#: look-alike labels (``Unsuppressed comments (2)``, ``Suppressed commentary
#: (2)``) are rejected here just as they are rejected by the structured parser.
#: Genuine unknown wrappers — e.g. ``suppressed (2)`` bare or ``suppressed
#: comments (2)`` in prose — still fire the sentinel, preserving fail-closed
#: behaviour for novel CCR body spellings.
_UNANCHORED_SUPPRESSED_COUNT_RE = re.compile(
    r"\bsuppressed\b(?:\s*|[^.(\n<]*\bcomments?\b[^.(\n<]*)\((\d+)\)", re.IGNORECASE
)

#: Unanchored "… low confidence … (N)" declaration used by the fail-closed sentinel.
_UNANCHORED_LOW_CONFIDENCE_COUNT_RE = re.compile(r"low confidence[^.(\n<]*\((\d+)\)", re.IGNORECASE)


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
    if parse_suppressed_count(body) or extract_suppressed_comment_entries(body):
        return False
    fence_masked = _mask_fenced_blocks(body)
    both_masked = _mask_inline_code(fence_masked)
    for count_pattern in (_UNANCHORED_SUPPRESSED_COUNT_RE, _UNANCHORED_LOW_CONFIDENCE_COUNT_RE):
        for count in count_pattern.finditer(both_masked):
            if int(count.group(1)) == 0:
                continue
            if _ENTRY_HEADER_ONLY_RE.search(fence_masked, count.end()) or _ENTRY_HEADER_INLINE_RE.search(
                fence_masked, count.end()
            ):
                return True
    return False
