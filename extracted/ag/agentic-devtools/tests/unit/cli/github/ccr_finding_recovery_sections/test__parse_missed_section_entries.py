"""Tests for the private missed-section entry parser."""

import pytest

import agentic_devtools.cli.github.ccr_review_format as ccr_review_format
from agentic_devtools.cli.github.ccr_finding_recovery import _parse_missed_section_entries


@pytest.mark.parametrize(
    "entries",
    [
        (
            '<summary><picture alt="P1"></picture>Guard the response</summary>\n'
            "`src/\u200ba.py:10`\n"
            "The response must be guarded.\n"
            "**src/a.py:10** [P1] Guard the response\n"
            "The response must be guarded.\n"
            "**src/other.py:20** [P1] Preserve the other response\n"
            "The other response remains useful."
        ),
        (
            "**src/other.py:20** [P1] Preserve the other response\n"
            "The other response remains useful.\n"
            '<summary><picture alt="P1"></picture>Guard the response</summary>\n'
            "`src/\u200ba.py:10`\n"
            "The response must be guarded.\n"
            "**src/a.py:10** [P1] Guard the response\n"
            "The response must be guarded."
        ),
    ],
)
def test_reconciles_path_aliases_independently_of_entry_order(entries: str) -> None:
    findings = _parse_missed_section_entries(
        entries,
        "previously_missed",
        declared_count=2,
        source_review_id=8420,
        source_review_url="https://github.com/example/repo/pull/4#pullrequestreview-8420",
    )

    assert len(findings) == 2
    assert {finding.title for _, finding in findings} == {
        "Guard the response",
        "Preserve the other response",
    }


def test_parses_finding_metadata_from_a_section() -> None:
    findings = _parse_missed_section_entries(
        "### [P1] Guard the response\n**File:** `src/client.py`\n**Line:** 42\nThe response may be missing.",
        "previously_missed",
        source_review_id=8420,
        source_review_url="https://github.com/example/repo/pull/4#pullrequestreview-8420",
    )

    assert len(findings) == 1
    offset, finding = findings[0]
    assert offset == 0
    assert finding.section == "previously_missed"
    assert finding.severity == "P1"
    assert finding.title == "Guard the response"
    assert finding.path == "src/client.py"
    assert finding.line == 42
    assert finding.source_review_id == 8420
    assert finding.source_review_url == "https://github.com/example/repo/pull/4#pullrequestreview-8420"


def test_returns_no_findings_when_section_has_no_entry_headers() -> None:
    assert (
        _parse_missed_section_entries(
            "No entries were found.",
            "suppressed",
            source_review_id=0,
            source_review_url="",
        )
        == []
    )


def test_parses_multiple_metadata_only_occurrences() -> None:
    findings = _parse_missed_section_entries(
        "**File:** `src/first.py`\nFirst finding description.\n\n"
        "**File:** `src/second.py`\nSecond finding description.",
        "previously_missed",
        source_review_id=8420,
        source_review_url="https://github.com/example/repo/pull/4#pullrequestreview-8420",
    )

    assert len(findings) == 2
    assert [finding.path for _, finding in findings] == ["src/first.py", "src/second.py"]
    assert [finding.title for _, finding in findings] == ["First finding description.", "Second finding description."]


def test_coalesces_legacy_entry_duplicate_of_picture_finding() -> None:
    findings = _parse_missed_section_entries(
        '<summary><picture alt="P1"></picture>Guard the response</summary>\n'
        r"`src/foo\_bar.py:10`"
        "\n"
        "The response must be guarded.\n"
        r"**`src/foo\_bar.py:10`** [P1] Guard the response"
        "\n"
        "The response must be guarded.",
        "previously_missed",
        declared_count=1,
        source_review_id=8420,
        source_review_url="https://github.com/example/repo/pull/4#pullrequestreview-8420",
    )

    assert len(findings) == 1
    _, finding = findings[0]
    assert finding.title == "Guard the response"
    assert finding.severity == "P1"
    assert finding.path == r"src/foo\_bar.py"
    assert finding.line == 10


def test_coalesces_picture_and_legacy_path_alias_when_declared_count_is_one() -> None:
    findings = _parse_missed_section_entries(
        '<summary><picture alt="P1"></picture>Guard the response</summary>\n'
        "`src/\u200ba.py:10`\n"
        "The response may be missing.\n"
        "**src/a.py:10** [P1] Guard the response\n"
        "The response may be missing.",
        "previously_missed",
        declared_count=1,
        source_review_id=8420,
        source_review_url="https://github.com/example/repo/pull/4#pullrequestreview-8420",
    )

    assert [(finding.path, finding.line) for _, finding in findings] == [("src/\u200ba.py", 10)]


def test_crlf_explanation_heading_does_not_create_phantom_picture_legacy_finding() -> None:
    findings = _parse_missed_section_entries(
        '<summary><picture alt="P1"></picture>Guard the response</summary>\n'
        "`src/a.py:10`\n"
        "The response may be missing.\n"
        "### Why this fails\r\n"
        "The response may be missing.\n"
        "**src/a.py:10** [P1] Guard the response\n"
        "The response may be missing.\n"
        "### Why this fails\r\n"
        "The response may be missing.",
        "previously_missed",
        declared_count=1,
        source_review_id=8420,
        source_review_url="https://github.com/example/repo/pull/4#pullrequestreview-8420",
    )

    assert [(finding.title, finding.path, finding.line) for _, finding in findings] == [
        ("Guard the response", "src/a.py", 10)
    ]


def test_preserves_independent_legacy_finding_at_same_location_and_severity() -> None:
    findings = _parse_missed_section_entries(
        '<summary><picture alt="P1"></picture>Guard the response</summary>\n'
        "`src/a.py:10`\n"
        "The response may be missing.\n"
        "**src/a.py:10** [P1] Preserve the original exception\n"
        "The original error is useful.",
        "previously_missed",
        declared_count=2,
        source_review_id=8420,
        source_review_url="https://github.com/example/repo/pull/4#pullrequestreview-8420",
    )

    assert [(finding.title, finding.path, finding.line) for _, finding in findings] == [
        ("Guard the response", "src/a.py", 10),
        ("Preserve the original exception", "src/a.py", 10),
    ]


def test_preserves_normalized_only_path_match_when_count_allows_two_findings() -> None:
    findings = _parse_missed_section_entries(
        '<summary><picture alt="P1"></picture>Guard the response</summary>\n'
        "`src/\u200ba.py:10`\n"
        "The response may be missing.\n"
        "**src/a.py:10** [P1] Guard the response\n"
        "The response may be missing.",
        "previously_missed",
        declared_count=2,
        source_review_id=8420,
        source_review_url="https://github.com/example/repo/pull/4#pullrequestreview-8420",
    )

    assert [(finding.path, finding.line) for _, finding in findings] == [
        ("src/\u200ba.py", 10),
        ("src/a.py", 10),
    ]


def test_duplicate_legacy_resolution_status_is_preserved_for_path_alias() -> None:
    findings = _parse_missed_section_entries(
        '<summary><picture alt="P1"></picture>Guard the response</summary>\n'
        "`src/\u200ba.py:10`\n"
        "The response must be guarded.\n"
        "**src/a.py:10** [P1] Guard the response\n"
        "The response must be guarded.\n"
        "Resolved since the previous review.",
        "previously_missed",
        declared_count=1,
        source_review_id=8420,
        source_review_url="https://github.com/example/repo/pull/4#pullrequestreview-8420",
    )

    assert len(findings) == 1
    _, finding = findings[0]
    assert finding.path == "src/\u200ba.py"
    assert finding.explicitly_resolved is True


def test_duplicate_legacy_resolution_status_is_preserved_for_exact_path() -> None:
    findings = _parse_missed_section_entries(
        '<summary><picture alt="P1"></picture>Guard the response</summary>\n'
        "`src/a.py:10`\n"
        "The response must be guarded.\n"
        "**src/a.py:10** [P1] Guard the response\n"
        "The response must be guarded.\n"
        "Resolved since the previous review.",
        "previously_missed",
        declared_count=1,
        source_review_id=8420,
        source_review_url="https://github.com/example/repo/pull/4#pullrequestreview-8420",
    )

    assert len(findings) == 1
    _, finding = findings[0]
    assert finding.path == "src/a.py"
    assert finding.explicitly_resolved is True


def test_preserves_unrelated_legacy_severity_entry_after_structured_finding() -> None:
    findings = _parse_missed_section_entries(
        "### [P1] Guard the response\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "The response may be missing.\n"
        "**src/b.py** [P2] Preserve the original exception\n"
        "The original error is useful.\n",
        "previously_missed",
        declared_count=2,
        source_review_id=8420,
        source_review_url="https://github.com/example/repo/pull/4#pullrequestreview-8420",
    )

    assert [(finding.title, finding.path, finding.line) for _, finding in findings] == [
        ("Guard the response", "src/a.py", 10),
        ("Preserve the original exception", "src/b.py", None),
    ]


def test_headerless_fallback_before_structured_finding_is_retained() -> None:
    body = (
        "<details><summary>Comments suppressed due to low confidence</summary>\n"
        "First independent finding.\n"
        "### [P1] Second finding\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "The structured finding has file metadata.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.title, finding.path) for finding in result.findings] == [
        ("First independent finding.", "(unknown file)"),
        ("Second finding", "src/a.py"),
    ]
    assert result.shortfalls == ()


def test_positive_missed_count_without_entries_is_a_shortfall() -> None:
    body = "<details><summary>Previously missed (2)</summary>\nNo entries were recovered.\n</details>"

    result = ccr_review_format.extract_ccr_findings(body)

    assert result.findings == ()
    assert result.shortfalls == (("previously_missed", 2, 0),)


def test_missed_summary_without_details_does_not_consume_following_heading() -> None:
    body = (
        "<summary>Previously missed (1)</summary>\n"
        "### Unrelated historical summary\n"
        "**File:** `src/unrelated.py`\n"
        "This is not a missed finding."
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert result.findings == ()
    assert result.shortfalls == (("previously_missed", 1, 0),)


def test_heading_only_missed_section_does_not_consume_following_summary() -> None:
    body = (
        "<details><summary>Review details</summary>\n"
        "### Previously missed (1)\n"
        "### Summary\n"
        "No missed findings here.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert result.findings == ()
    assert result.shortfalls == (("previously_missed", 1, 0),)


def test_missed_and_suppressed_sections_are_preserved_in_document_order() -> None:
    body = (
        "<details>\n"
        "<summary>Previously missed (1)</summary>\n"
        "### [P1] First occurrence\n"
        "**File:** `src/first.py`\n"
        "First body.\n"
        "<summary>Suppressed comments (1)</summary>\n"
        "### [P2] Second occurrence\n"
        "**File:** `src/second.py`\n"
        "Second body.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.section, finding.title) for finding in result.findings] == [
        ("previously_missed", "First occurrence"),
        ("suppressed", "Second occurrence"),
    ]
    assert result.shortfalls == ()
