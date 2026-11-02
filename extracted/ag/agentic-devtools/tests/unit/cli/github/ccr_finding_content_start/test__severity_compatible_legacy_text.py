"""Tests for severity reconciliation between structured and legacy findings."""

import pytest

import agentic_devtools.cli.github.ccr_review_format as ccr_review_format
from agentic_devtools.cli.github.ccr_finding_content_start import _severity_compatible_legacy_text


@pytest.mark.parametrize(
    ("structured_start", "legacy_text", "expected_compatible", "expected_text"),
    (
        (None, "[P2] Guard the response", True, " Guard the response"),
        ("- [P1] Guard the response", "[P2] Guard the response", False, "[P2] Guard the response"),
        ("- [P1] Guard the response", "- [P2] Guard the response", False, "- [P2] Guard the response"),
        (
            '<summary><picture><img alt="High severity"></picture>Guard the response</summary>',
            "[P2] Guard the response",
            False,
            "[P2] Guard the response",
        ),
        ("- [P1] Guard the response", "[P1] Guard the response", True, " Guard the response"),
        ("- [P1] Guard the response", "- [P1] Guard the response", True, "-  Guard the response"),
        (
            '<summary><picture><img alt="High severity"></picture>Guard the response</summary>',
            "[HIGH] Guard the response",
            True,
            " Guard the response",
        ),
        ("- [High] Guard the response", "[P1] Guard the response", True, " Guard the response"),
        ("- [High] Guard the response", "[P2] Guard the response", False, "[P2] Guard the response"),
        ("### [P1] Guard the response", "[P2] Guard the response", False, "[P2] Guard the response"),
        ("### Guard the response", "[P2] Guard the response", True, " Guard the response"),
        (
            "<summary><picture>Guard the response</picture></summary>",
            "[P2] Guard the response",
            True,
            " Guard the response",
        ),
        ("### [P1] Guard the response", "Guard the response", True, "Guard the response"),
    ),
)
def test_structured_severity_is_reconciled_with_legacy_severity(
    structured_start: str | None,
    legacy_text: str,
    expected_compatible: bool,
    expected_text: str,
) -> None:
    structured_match = (
        ccr_review_format._FINDING_START_RE.match(structured_start) if structured_start is not None else None
    )

    compatible, normalized_text = _severity_compatible_legacy_text(structured_match, legacy_text)

    assert compatible is expected_compatible
    assert normalized_text == expected_text


@pytest.mark.parametrize(
    "structured_start",
    (
        "- [P1] Guard the response",
        '<summary><picture alt="P1"></picture>Guard the response</summary>',
    ),
)
def test_declared_missed_count_keeps_mismatched_severity_and_excludes_explanation_heading(
    structured_start: str,
) -> None:
    body = (
        "<details><summary>Previously missed (2)</summary>\n"
        f"{structured_start}\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "Guard the response.\n"
        "**src/a.py:10** [P2] Guard the response\n"
        "Guard the response.\n"
        "### Why this fails\n"
        "The missing guard can raise.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.severity, finding.title) for finding in result.findings] == [
        ("P1", "Guard the response"),
        ("P2", "Guard the response"),
    ]
    assert result.shortfalls == ()


@pytest.mark.parametrize("newline", ("\n", "\r\n"))
def test_independent_severity_bullet_after_legacy_entry_is_recovered(newline: str) -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "**src/a.py:10**: First finding.\n\n"
        "- [P1] Second finding\n"
        "The second finding has no file metadata.\n"
        "</details>"
    ).replace("\n", newline)

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.severity, finding.title, finding.path, finding.line) for finding in result.findings] == [
        ("", "First finding.", "src/a.py", 10),
        ("P1", "Second finding", ccr_review_format.UNKNOWN_FILE, None),
    ]
    assert result.shortfalls == ()


def test_independent_severity_bullet_after_legacy_entry_needs_no_blank_line() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "**src/a.py:10**: First finding.\n"
        "- [P1] Second finding\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.severity, finding.title, finding.path, finding.line) for finding in result.findings] == [
        ("", "First finding.", "src/a.py", 10),
        ("P1", "Second finding", ccr_review_format.UNKNOWN_FILE, None),
    ]
    assert result.shortfalls == ()


def test_first_severity_bullet_remains_attached_to_header_only_legacy_entry() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "**src/a.py:10**\n"
        "* [P1] First finding\n"
        "- [P2] Second finding\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.severity, finding.title, finding.path, finding.line) for finding in result.findings] == [
        ("P1", "[P1] First finding", "src/a.py", 10),
        ("P2", "Second finding", ccr_review_format.UNKNOWN_FILE, None),
    ]
    assert result.shortfalls == ()


def test_blank_separated_first_severity_bullet_keeps_legacy_path() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n**src/a.py:10**\n\n* [P1] Guard against None.\n</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.severity, finding.title, finding.path, finding.line) for finding in result.findings] == [
        ("P1", "Guard against None.", "src/a.py", 10)
    ]
    assert result.shortfalls == ()


def test_path_without_severity_and_separate_line_metadata_is_recovered() -> None:
    body = (
        "<details><summary>Previously missed (1)</summary>\n"
        "**File:** `src/path.py`\n"
        "**Line:** 13\n"
        "This finding has no severity heading.\n"
        "</details>"
    )

    finding = ccr_review_format.extract_ccr_findings(body).findings[0]

    assert finding.title == "This finding has no severity heading."
    assert finding.path == "src/path.py"
    assert finding.line == 13
    assert finding.severity == ""


def test_severity_is_read_from_picture_alt_or_a_leading_token_only() -> None:
    body = (
        "<details><summary>Previously missed (2)</summary>\n"
        "### Preserve low values\n"
        "**File:** `src/values.py`\n"
        "A title containing low is not a severity label.\n"
        '<summary><picture><img alt="Low severity"></picture>Low threshold behavior</summary>\n'
        "`src/threshold.py:12`\n"
        "The title starts with Low but should remain unchanged.\n"
        "</details>"
    )

    findings = ccr_review_format.extract_ccr_findings(body).findings

    assert [(finding.severity, finding.title) for finding in findings] == [
        ("", "Preserve low values"),
        ("LOW", "Low threshold behavior"),
    ]


def test_legacy_explanation_keeps_severity_bullet_and_subheading() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "**src/a.py:10**\n"
        "* [P1] Guard against None.\n"
        "#### Why this fails\n"
        "The value is unchecked.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert len(result.findings) == 1
    finding = result.findings[0]
    assert (finding.path, finding.line) == ("src/a.py", 10)
    assert finding.body == "[P1] Guard against None.\n#### Why this fails\nThe value is unchecked."
    assert result.shortfalls == ()


@pytest.mark.parametrize(
    ("legacy_severity", "expected_count"),
    (("P1", 1), ("P2", 2)),
)
def test_legacy_severity_prefix_only_deduplicates_matching_structured_severity(
    legacy_severity: str,
    expected_count: int,
) -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "### [P1] Guard against None.\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "Guard against None.\n"
        f"**src/a.py:10**: [{legacy_severity}] Guard against None.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert len(result.findings) == expected_count
    assert result.shortfalls == (() if expected_count == 1 else (("suppressed", 1, 2),))
    assert result.findings[0].body.endswith(f"**src/a.py:10**: [{legacy_severity}] Guard against None.")
    if expected_count == 2:
        assert result.findings[1].body == f"[{legacy_severity}] Guard against None."


def test_matching_legacy_severity_does_not_consume_metadata_free_finding_count() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Guard against None.\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "Guard against None.\n"
        "**src/a.py:10**: [P1] Guard against None.\n"
        "### Second finding\n"
        "Resolved since the previous review.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.severity, finding.title, finding.explicitly_resolved) for finding in result.findings] == [
        ("P1", "Guard against None.", False),
        ("", "Second finding", True),
    ]
    assert result.shortfalls == ()


def test_legacy_severity_duplicate_matches_structured_finding_without_severity() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "### Guard against None.\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "Guard against None.\n"
        "**src/a.py:10**: [P1] Guard against None.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.title, finding.path, finding.line) for finding in result.findings] == [
        ("Guard against None.", "src/a.py", 10)
    ]
    assert result.shortfalls == ()


def test_leading_bullets_match_between_structured_and_legacy_findings() -> None:
    for bullet in ("*", "-"):
        for indentation in ("", "  "):
            body = (
                "<details><summary>Suppressed comments (1)</summary>\n"
                "### [P1] Structured occurrence\n"
                "**File:** `src/repeated.py`\n"
                "**Line:** 10\n"
                f"{indentation}{bullet} Repeated finding body.\n"
                f"**src/repeated.py:10**: {indentation}{bullet} Repeated finding body.\n"
                "</details>"
            )

            result = ccr_review_format.extract_ccr_findings(body)

            assert len(result.findings) == 1
            assert result.shortfalls == ()
