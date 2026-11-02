"""Tests for finding-local resolution status."""

import pytest

import agentic_devtools.cli.github.ccr_review_format as ccr_review_format
from agentic_devtools.cli.github.ccr_finding_recovery import _finding_is_explicitly_resolved


def test_independent_legacy_resolution_does_not_resolve_structured_finding() -> None:
    body = (
        "### [P1] Outstanding structured finding\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "The issue still needs a fix.\n\n"
        "**src/b.py:20**: Independent legacy finding.\n"
        "Resolved since the previous review."
    )

    wrapper = "<details><summary>Comments suppressed due to low confidence</summary>\n" + body + "\n</details>"
    result = ccr_review_format.extract_ccr_findings(wrapper)

    assert [(finding.path, finding.explicitly_resolved) for finding in result.findings] == [
        ("src/a.py", False),
        ("src/b.py", True),
    ]
    assert result.shortfalls == ()
    assert _finding_is_explicitly_resolved(body, "src/a.py", 10) is False


def test_hybrid_legacy_resolution_remains_attached_to_its_structured_finding() -> None:
    body = (
        "### [P1] Hybrid finding\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "The same finding.\n"
        "**src/a.py:10**: The same finding.\n"
        "Resolved since the previous review."
    )

    assert _finding_is_explicitly_resolved(body, "src/a.py", 10) is True


@pytest.mark.parametrize("indent", ["    ", "\t"])
def test_indented_severity_like_code_preserves_duplicate_resolution_status(indent: str) -> None:
    body = (
        "### [P1] Finding\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        f"{indent}[P1] literal code\n"
        "**src/a.py:10**:\n"
        f"{indent}[P1] literal code\n"
        "Resolved since the previous review."
    )

    assert _finding_is_explicitly_resolved(body, "src/a.py", 10) is True


def test_normalized_path_alias_does_not_resolve_structured_finding() -> None:
    body = (
        "### [P1] Outstanding structured finding\n"
        "**File:** `src/\u200ba.py`\n"
        "**Line:** 10\n"
        "The open issue still needs a fix.\n"
        "**src/a.py:10**: A different resolved finding.\n"
        "Resolved since the previous review."
    )

    assert _finding_is_explicitly_resolved(body, "src/\u200ba.py", 10) is False


def test_same_location_with_different_content_does_not_resolve_structured_finding() -> None:
    body = (
        "### [P1] Outstanding structured finding\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "The open issue still needs a fix.\n"
        "**src/a.py:10**: A different resolved finding.\n"
        "Resolved since the previous review."
    )

    assert _finding_is_explicitly_resolved(body, "src/a.py", 10) is False


def test_prose_status_is_not_resolution() -> None:
    assert _finding_is_explicitly_resolved("Not resolved since the previous review.", "src/a.py", 10) is False


def test_explicitly_resolved_entry_is_marked_for_promotion_filtering() -> None:
    body = (
        "<details><summary>Previously missed (1)</summary>\n"
        "### [P1] Already fixed\n"
        "**File:** `src/fixed.py`\n"
        "**Line:** 8\n"
        "Resolved since the previous review.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert len(result.findings) == 1
    assert result.findings[0].explicitly_resolved is True
    assert result.shortfalls == ()


def test_resolved_occurrence_does_not_renumber_outstanding_occurrences() -> None:
    body = (
        "<details><summary>Previously missed (2)</summary>\n"
        "### [P1] Already fixed\n"
        "**File:** `src/fixed.py`\n"
        "Resolved since the previous review.\n"
        "### [P1] Still outstanding\n"
        "**File:** `src/open.py`\n"
        "Needs a fix.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert len(result.findings) == 2
    assert result.findings[0].explicitly_resolved is True
    assert result.findings[1].title == "Still outstanding"
    assert result.findings[1].ordinal == 2


def test_only_a_standalone_resolved_status_marks_a_finding_resolved() -> None:
    body = (
        "<details><summary>Previously missed (4)</summary>\n"
        "### Actionable prose\n"
        "**File:** `src/prose.py`\n"
        "This is not resolved since the previous review.\n"
        "### Inline code status\n"
        "**File:** `src/inline.py`\n"
        "`Resolved since the previous review.` is quoted text.\n"
        "### Fenced code status\n"
        "**File:** `src/fenced.py`\n"
        "```text\nResolved since the previous review.\n```\n"
        "### Actual status\n"
        "**File:** `src/resolved.py`\n"
        "Resolved since the previous review.\n"
        "</details>"
    )

    findings = ccr_review_format.extract_ccr_findings(body).findings

    assert [finding.explicitly_resolved for finding in findings] == [False, False, False, True]


def test_picture_summary_location_does_not_hide_its_resolution_status() -> None:
    body = (
        '<summary><picture alt="P1"></picture>Already resolved</summary>\n'
        "`src/a.py:10`\n"
        "Resolved since the previous review."
    )

    assert _finding_is_explicitly_resolved(body, "src/a.py", 10) is True


def test_structured_heading_location_does_not_hide_its_resolution_status() -> None:
    body = "### [P1] Already resolved\n`src/a.py:10`\nResolved since the previous review."

    assert _finding_is_explicitly_resolved(body, "src/a.py", 10) is True


@pytest.mark.parametrize("heading", ["### [P1] Guard", '<summary><picture alt="P1"></picture>Guard</summary>'])
def test_standalone_location_and_matching_continuation_preserve_resolution_status(heading: str) -> None:
    body = (
        f"{heading}\n"
        "`src/a.py:10`\n"
        "Guard the response.\n"
        "**src/a.py:10**: Guard the response.\n"
        "Resolved since the previous review."
    )

    assert _finding_is_explicitly_resolved(body, "src/a.py", 10) is True
