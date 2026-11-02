"""Headline parsing and semantic fast paths for CCR overview-v2 reviews."""

from __future__ import annotations

import re

from .ccr_code_masking import mask_fenced_blocks, mask_inline_code

# CCR overview-v2 headline
# ---------------------------------------------------------------------------

_CCR_OVERVIEW_MARKER_RE = re.compile(r"^[ \t]*<!-- ccr-overview-v2 -->[ \t]*\r?$", re.MULTILINE)
_CCR_OVERVIEW_ZERO_RE = re.compile(
    r"[ \t]*(?:\*\*)?(?:no open (?:issues|findings)|0 open findings)(?:\*\*)?(?:[ \t]+[^\r\n]*)?",
    re.IGNORECASE,
)
_CCR_OVERVIEW_HEADING_RE = re.compile(r"^[ \t]{0,3}#{1,6}[ \t]+[^\r\n]+", re.MULTILINE)
_APPROVAL_WORTHY_HEADLINE_RE = re.compile(
    r"^(?:(?:this )?(?:pr|pull request) is )?"
    r"(?:ready(?: for (?:human )?approval(?:/merge)?| to merge)?"
    r"|only needs? (?:human )?(?:review|approval(?:/merge)?|merge)"
    r"|only needs? (?:a )?final human (?:review|approval)"
    r"|awaiting (?:human )?(?:review|approval|merge))[\s.!]*$",
    re.IGNORECASE,
)
_CRITIQUE_HEADLINE_RE = re.compile(
    r"\b(?:bug|broken|defect|fail(?:ed|ing|ure)?|finding|insecure|issue|loss|lose|loses|"
    r"missing|regression|risk|unsafe|unresolved|vulnerab)\w*\b",
    re.IGNORECASE,
)


def parse_ccr_overview_summary(body: str) -> tuple[bool, str | None] | None:
    """Parse the zero-open-findings signal and headline sentence from CCR overview-v2.

    The headline is the first non-empty paragraph after the first Markdown
    heading following the overview marker. A missing or structurally unparseable
    headline is returned as ``None`` while preserving the parsed zero-findings
    signal, allowing callers to log the incomplete summary without changing
    their existing behavior.

    Args:
        body: Full review body text.

    Returns:
        ``(zero_open_findings, headline)`` for an overview-v2 body, or ``None``
        when the marker is absent.
    """
    if not body:
        return None
    masked = mask_inline_code(mask_fenced_blocks(body))
    marker = _CCR_OVERVIEW_MARKER_RE.search(masked)
    if marker is None:
        return None

    overview = masked[marker.end() :]
    zero_open_findings = any(
        _CCR_OVERVIEW_ZERO_RE.fullmatch(line.strip()) is not None for line in overview.splitlines()
    )
    heading = _CCR_OVERVIEW_HEADING_RE.search(overview)
    if heading is None:
        return zero_open_findings, None

    raw_overview = body[marker.end() :]
    lines = raw_overview[heading.end() :].splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines or not lines[0].strip() or lines[0].lstrip().startswith(("#", "<")):
        return zero_open_findings, None
    paragraph: list[str] = []
    for line in lines:
        if not line.strip():
            break
        paragraph.append(line.strip())
    headline = " ".join(paragraph).strip()
    if headline.startswith("**") and headline.endswith("**"):
        headline = headline[2:-2].strip()
    if not headline or _CCR_OVERVIEW_ZERO_RE.fullmatch(headline) is not None:
        return zero_open_findings, None
    return zero_open_findings, headline


def is_approval_worthy_ccr_headline(headline: str) -> bool:
    """Return whether a headline is an unambiguous human-approval-only fast-path match.

    A false result means semantic classification is still needed; it does not
    establish that the headline is a critique.
    """
    if not isinstance(headline, str) or not headline.strip():
        return False
    normalized = headline.strip()
    return (
        _APPROVAL_WORTHY_HEADLINE_RE.fullmatch(normalized) is not None
        and _CRITIQUE_HEADLINE_RE.search(normalized) is None
    )


# ---------------------------------------------------------------------------
