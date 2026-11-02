"""Tests for _is_explanatory_standalone_location."""

import pytest

import agentic_devtools.cli.github.ccr_review_format as ccr_review_format
from agentic_devtools.cli.github.ccr_finding_content import _is_explanatory_standalone_location


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Explanation.\n`src/input.py:5`\n", True),
        ("Explanation.\n`src/input.py:5`\n* Finding text.\n", False),
        ("`src/input.py:5`\n", False),
        ("Explanation.\n\n`src/input.py:5`\n", False),
        ("Explanation.\n  \t\n`src/input.py:5`\n", False),
        ("Explanation.\r\n\r\n`src/input.py:5`\r\n", False),
        ("### [P1] Finding\n`src/input.py:5`\n", False),
        ("**File:** `src/review.py`\n`src/input.py:5`\n", False),
        ("**Line:** 23\n`src/input.py:5`\n", False),
        ("</summary>\n`src/input.py:5`\n", False),
        ("<summary>Review details\n`src/input.py:5`\n", False),
    ],
)
def test_classifies_standalone_locations_by_preceding_content(text: str, expected: bool) -> None:
    match = ccr_review_format._ENTRY_HEADER_ONLY_RE.search(text)

    assert match is not None
    assert _is_explanatory_standalone_location(text, match) is expected


def test_explanatory_standalone_locations_keep_structured_and_legacy_findings_distinct() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** `src/\u200breview.py`\n"
        "**Line:** 23\n"
        "Identical prose.\n"
        "``src/input.py:5``\n"
        "**src/review.py:23**: Identical prose.\n"
        "``src/output.py:6``\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert len(result.findings) == 2
    assert "``src/input.py:5``" in result.findings[0].body
    assert "``src/output.py:6``" in result.findings[1].body
    assert result.shortfalls == ()


def test_single_backticked_explanatory_locations_keep_findings_distinct() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** `src/\u200breview.py`\n"
        "**Line:** 23\n"
        "Identical prose.\n"
        "`src/input.py:5`\n"
        "**src/review.py:23**: Identical prose.\n"
        "`src/output.py:6`\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert len(result.findings) == 2
    assert "`src/input.py:5`" in result.findings[0].body
    assert "`src/output.py:6`" in result.findings[1].body
    assert result.shortfalls == ()


def test_standalone_explanatory_location_after_prose_is_preserved() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** src/a.py\n"
        "Guard the response.\n"
        "`src/a.py:42`\n"
        "**src/a.py:42**: Guard the response.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert len(result.findings) == 2
    assert result.shortfalls == ()


def test_crlf_standalone_location_is_excluded_from_structured_finding_body() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\r\n"
        "### [P1] Guard the response\r\n"
        "**File:** `src/a.py`\r\n"
        "**Line:** 42\r\n"
        "``src/a.py:42``\r\n"
        "The response may be missing.\r\n"
        "**src/a.py:42**: The response may be missing.\r\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.line, finding.title) for finding in result.findings] == [
        ("src/a.py", 42, "Guard the response")
    ]
    assert result.shortfalls == ()
