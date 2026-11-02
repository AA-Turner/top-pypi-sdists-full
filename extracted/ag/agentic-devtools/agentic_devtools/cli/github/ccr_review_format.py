"""Canonical parsers for Copilot Code Review (CCR) review bodies.

This module is the **single source of truth** for extracting structured
information from a Copilot Code Review body. It understands legacy suppressed
formats, the private-preview verdict format, and ``ccr-overview-v2`` missed
sections:

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

**CCR overview-v2 format** — the ``<!-- ccr-overview-v2 -->`` marker may accompany
a ``Previously missed (N)`` section. Its declared count is authoritative even
when the overview summary reports zero open findings.

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
from dataclasses import dataclass

from agentic_devtools.cli.github.ccr_finding_content import (
    _finding_content_key as _finding_content_key,
)
from agentic_devtools.cli.github.ccr_finding_content import (
    _finding_start_matches as _finding_start_matches,
)
from agentic_devtools.cli.github.ccr_finding_content import (
    _is_explanatory_standalone_location as _is_explanatory_standalone_location,
)
from agentic_devtools.cli.github.ccr_finding_recovery import (
    _find_suppressed_block as _find_suppressed_block,
)
from agentic_devtools.cli.github.ccr_finding_recovery import (
    _find_suppressed_block_with_offset as _find_suppressed_block_with_offset,
)
from agentic_devtools.cli.github.ccr_finding_recovery import (
    _finding_is_explicitly_resolved as _finding_is_explicitly_resolved,
)
from agentic_devtools.cli.github.ccr_finding_recovery import (
    _independent_legacy_spans as _independent_legacy_spans,
)
from agentic_devtools.cli.github.ccr_finding_recovery import (
    _mask_spans as _mask_spans,
)
from agentic_devtools.cli.github.ccr_finding_recovery import (
    _parse_missed_section_entries as _parse_missed_section_entries,
)
from agentic_devtools.cli.github.ccr_finding_recovery import (
    extract_ccr_findings as extract_ccr_findings,
)
from agentic_devtools.cli.github.ccr_finding_recovery import (
    extract_suppressed_comment_entries as extract_suppressed_comment_entries,
)
from agentic_devtools.cli.github.ccr_reported_comment_count import (
    parse_reported_comment_count as parse_reported_comment_count,
)
from agentic_devtools.cli.github.ccr_review_format_markdown import (
    _FENCE_DELIM_RE as _FENCE_DELIM_RE,
)
from agentic_devtools.cli.github.ccr_review_format_markdown import (
    _INLINE_CODE_COMPARISON_RE as _INLINE_CODE_COMPARISON_RE,
)
from agentic_devtools.cli.github.ccr_review_format_markdown import (
    _INLINE_CODE_RE as _INLINE_CODE_RE,
)
from agentic_devtools.cli.github.ccr_review_format_markdown import (
    _mask_fenced_blocks as _mask_fenced_blocks,
)
from agentic_devtools.cli.github.ccr_review_format_markdown import (
    _mask_inline_code as _mask_inline_code,
)
from agentic_devtools.cli.github.ccr_review_format_signals import (
    parse_suppressed_count as parse_suppressed_count,
)
from agentic_devtools.cli.github.ccr_review_format_signals import (
    parse_verdict as parse_verdict,
)
from agentic_devtools.cli.github.ccr_review_format_signals import (
    unrecovered_suppression_signal as unrecovered_suppression_signal,
)

__all__ = [
    "CCRFinding",
    "CCRFindingRecovery",
    "UNKNOWN_FILE",
    "VERDICT_APPROVE",
    "VERDICT_NOT_APPROVE",
    "ccr_path_match_key",
    "extract_ccr_findings",
    "extract_suppressed_comment_entries",
    "parse_reported_comment_count",
    "parse_suppressed_count",
    "parse_verdict",
    "unrecovered_suppression_signal",
    "_FENCE_DELIM_RE",
    "_CCR_SECTION_DECLARATION_RE",
    "_ENTRY_HEADER_INLINE_RE",
    "_ENTRY_HEADER_ONLY_RE",
    "_EXPLICITLY_RESOLVED_RE",
    "_INLINE_CODE_COMPARISON_RE",
    "_INLINE_CODE_RE",
    "_FILE_FIELD_START_RE",
    "_FILE_LOCATION_RE",
    "_FINDING_START_RE",
    "_GENERATED_NONE_RE",
    "_GENERATED_N_RE",
    "_HEADING_RE",
    "_LEGACY_SUPPRESSED_BLOCK_RE",
    "_LINE_LOCATION_RE",
    "_LOW_CONFIDENCE_COUNT_RE",
    "_METRICS_GENERATED_RE",
    "_SEVERITY_PREFIX_RE",
    "_SEVERITY_RE",
    "_STANDALONE_FILE_LOCATION_RE",
    "_SUPPRESSED_ANCHOR_RE",
    "_SUPPRESSED_BLOCK_END_RE",
    "_SUPPRESSED_COUNT_RE",
    "_UNANCHORED_LOW_CONFIDENCE_COUNT_RE",
    "_UNANCHORED_SUPPRESSED_COUNT_RE",
    "_find_suppressed_block",
    "_find_suppressed_block_with_offset",
    "_finding_content_key",
    "_is_inline_code_header",
    "_finding_is_explicitly_resolved",
    "_finding_start_matches",
    "_independent_legacy_spans",
    "_is_explanatory_standalone_location",
    "_mask_fenced_blocks",
    "_mask_inline_code",
    "_mask_spans",
    "_parse_missed_section_entries",
    "_unescape_markdown_path",
]

# ---------------------------------------------------------------------------
# Public constants
# ---------------------------------------------------------------------------

#: Verdict returned when the new-format heading blocks approval.
VERDICT_NOT_APPROVE = "not_approve"

#: Verdict returned when the new-format heading approves.
VERDICT_APPROVE = "approve"

#: Placeholder path used when a suppressed comment cannot be attributed to a file.
UNKNOWN_FILE = "(unknown file)"


def ccr_path_match_key(path: str) -> str:
    """Return a path key that ignores CCR's zero-width artifact after separators."""
    return re.sub(r"/\u200b+", "/", path)


def _unescape_markdown_path(path: str) -> str:
    """Decode escaped backslashes and underscores outside inline code spans."""
    return re.sub(r"\\([\\_])", r"\1", path)


@dataclass(frozen=True)
class CCRFinding:
    """One recoverable occurrence from a CCR missed or suppressed section."""

    section: str
    ordinal: int
    severity: str
    title: str
    body: str
    path: str
    line: int | None
    source_review_id: int = 0
    source_review_url: str = ""
    explicitly_resolved: bool = False


@dataclass(frozen=True)
class CCRFindingRecovery:
    """Findings and declaration shortfalls recovered from a CCR review body."""

    findings: tuple[CCRFinding, ...]
    shortfalls: tuple[tuple[str, int, int], ...] = ()


# ---------------------------------------------------------------------------
# Verdict heading
# ---------------------------------------------------------------------------

#: Matches any ``###``-level (or deeper) heading line; the heading text is captured.
_HEADING_RE = re.compile(r"^#{3,}\s+(.+?)\s*$", re.MULTILINE)


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
#: ``Suppressed comment(s) (N)`` and ``Suppressed finding(s) (N)`` spellings.
#: Word boundaries still reject look-alikes like ``Unsuppressed comments (N)``
#: and ``Suppressed commentary (N)``.
_SUPPRESSED_DECLARATION = r"[^\n<]*?\bsuppressed\b(?:\s*|[^.(\n<]*\b(?:comments?|findings?)\b[^.(\n<]*)\((\d+)\)"

#: The "… low confidence … (N)" fallback declaration, without its anchor.
_LOW_CONFIDENCE_DECLARATION = r"[^\n<]*?low confidence[^.(\n<]*\((\d+)\)"

#: "… suppressed … (N)" anchored to a markdown heading or a ``<summary>`` element
#: so that prose mentioning "Suppressed comment (1)" is never counted.
_SUPPRESSED_COUNT_RE = re.compile(_ANCHOR + _SUPPRESSED_DECLARATION, re.IGNORECASE | re.MULTILINE)

#: "… low confidence … (N)" fallback, anchored the same way.
_LOW_CONFIDENCE_COUNT_RE = re.compile(_ANCHOR + _LOW_CONFIDENCE_DECLARATION, re.IGNORECASE | re.MULTILINE)


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


def _is_inline_code_header(text: str, match: re.Match[str]) -> bool:
    """Return whether a parsed path header is enclosed in inline code."""
    return "`" in text[match.start() : match.start(1)]


_CCR_SECTION_DECLARATION_RE = re.compile(
    r"(?:<summary>\s*(?:<strong>\s*)?|^[ \t]{0,3}#{1,6}[ \t]+)"
    r"(?:Previously\s+missed\s*\((\d+)\)|" + _SUPPRESSED_DECLARATION + r"|" + _LOW_CONFIDENCE_DECLARATION + r")",
    re.IGNORECASE | re.MULTILINE,
)
_FINDING_START_RE = re.compile(
    r"^[ \t]{0,3}(?:<summary>\s*<picture\b.*?</summary>|"
    r"#{1,6}[ \t]+(?!(?:Previously missed|.*\bsuppressed\b)).+|"
    r"[-*][ \t]+(?:(?:\*\*)?\[(?:P[0-4]|critical|high|medium|low)\](?:\*\*)?[ \t]*|"
    r"\*\*Severity:\*\*[ \t]*)\S.*)$",
    re.IGNORECASE | re.MULTILINE,
)


_FILE_LOCATION_RE = re.compile(
    r"(?:\*\*(?:file|path):\*\*|(?:file|path):)[ \t]*"
    r"(?:`+([^`\n]+)`+|([^\s`*]+))",
    re.IGNORECASE,
)
_FILE_FIELD_START_RE = re.compile(
    r"^[ \t]{0,3}(?:\*\*(?:file|path):\*\*|(?:file|path):)",
    re.IGNORECASE | re.MULTILINE,
)
_STANDALONE_FILE_LOCATION_RE = re.compile(r"^[ \t]{0,3}`+([^`\n]+:\d+)`+[ \t]*$", re.MULTILINE)
_LINE_LOCATION_RE = re.compile(
    r"(?:\*\*lines?:\*\*|lines?:)[ \t]*(\d+)(?:[ \t]*[-–][ \t]*\d+)?",
    re.IGNORECASE,
)
_SEVERITY_RE = re.compile(r"\b(P[0-4]|critical|high|medium|low)\b", re.IGNORECASE)
_SEVERITY_PREFIX_RE = re.compile(
    r"^[ \t]*(?:\[(P[0-4]|critical|high|medium|low)\]|"
    r"(P[0-4])(?=[ \t:*-])|(critical|high|medium|low)(?=:))",
    re.IGNORECASE,
)
_EXPLICITLY_RESOLVED_RE = re.compile(
    r"^[ \t]*(?:[-*][ \t]+)?resolved\s+since\s+(?:the\s+)?(?:last|previous)\s+review\.?[ \t]*$",
    re.IGNORECASE | re.MULTILINE,
)


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
