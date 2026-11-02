"""Tests for the public CCR review-format finding extractor."""

import pytest

import agentic_devtools.cli.github.ccr_review_format as ccr_review_format


def test_strips_inline_line_suffix_when_reconciling_duplicate_location() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] First finding\n"
        "**File:** `src/a.py:10`\n"
        "First finding body.\n"
        "**src/a.py:10**: First finding body.\n"
        "### Second finding\n"
        "The second finding has no file metadata.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.title, finding.path, finding.line) for finding in result.findings] == [
        ("First finding", "src/a.py", 10),
        ("Second finding", ccr_review_format.UNKNOWN_FILE, None),
    ]
    assert result.shortfalls == ()


@pytest.mark.parametrize("legacy_header", ("**src/a.py:10**", "**`src/a.py:10`**"))
def test_reports_shortfall_for_ambiguous_normalized_duplicate_paths(legacy_header: str) -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] First finding\n"
        "**File:** `src/\u200ba.py`\n"
        "**Line:** 10\n"
        "First finding body.\n"
        f"{legacy_header}: First finding body.\n"
        "### Second finding\n"
        "The second finding has no file metadata.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert result.shortfalls == (("suppressed", 2, 1),)


def test_distinct_normalized_paths_with_explicit_heading_metadata_are_recovered() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] First finding\n"
        "**File:** `src/\u200ba.py`\n"
        "**Line:** 10\n"
        "First finding body.\n"
        "**src/a.py:10**: First finding body.\n"
        "### Second finding\n"
        "**File:** `src/b.py`\n"
        "**Line:** 20\n"
        "The second finding has file metadata.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.title, finding.path, finding.line) for finding in result.findings] == [
        ("First finding", "src/\u200ba.py", 10),
        ("Second finding", "src/b.py", 20),
    ]
    assert result.shortfalls == ()


def test_preserves_second_finding_after_duplicate_with_explanatory_locations() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] First finding\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "First explanation.\n"
        "`src/input.py:5`\n"
        "**src/a.py:10**: First explanation.\n"
        "`src/input.py:5`\n"
        "### Second finding\n"
        "No file metadata was supplied.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.title, finding.path) for finding in result.findings] == [
        ("First finding", "src/a.py"),
        ("Second finding", ccr_review_format.UNKNOWN_FILE),
    ]
    assert result.findings[1].body == "### Second finding\nNo file metadata was supplied."
    assert result.shortfalls == ()


def test_reports_shortfall_for_ambiguous_literal_paths_before_explanation_heading() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] First finding\n"
        "**File:** `src/\u200ba.py`\n"
        "**Line:** 10\n"
        "First explanation.\n"
        "**src/a.py:10**: First explanation.\n"
        "### Why this fails\n"
        "The explanation heading is not a finding.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.title, finding.path, finding.line) for finding in result.findings] == [
        ("First finding", "src/\u200ba.py", 10),
        ("First explanation.", "src/a.py", 10),
    ]
    assert result.shortfalls == (("suppressed", 2, 1),)


@pytest.mark.parametrize(
    "structured_start",
    (
        "- [P1] Guard the response.\n",
        '<summary><picture><img alt="High severity"></picture>Guard the response</summary>\n',
    ),
)
def test_reconciles_severity_starts_before_legacy_duplicate_and_explanation(
    structured_start: str,
) -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "**src/a.py:10**\n"
        f"{structured_start}"
        "**src/a.py:10**\n"
        "[P2] Guard the response.\n"
        "### Why this fails\n"
        "The implementation can fail when the value is missing.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert len(result.findings) == 2
    assert all(finding.title != "Why this fails" for finding in result.findings)
    assert result.shortfalls == ()


@pytest.mark.parametrize(
    ("picture_severity", "legacy_severity", "expected_picture_severity"),
    (
        ("Medium severity", "P2", "MEDIUM"),
        ("P2", "Medium", "P2"),
        ("P2", "P2", "P2"),
    ),
)
def test_reconciles_picture_and_legacy_entries_before_explanation_headings(
    picture_severity: str,
    legacy_severity: str,
    expected_picture_severity: str,
) -> None:
    body = (
        "<details><summary>Previously missed (2)</summary>\n"
        "<details>\n"
        f'<summary><picture><img src="x.png" alt="{picture_severity}"></picture>'
        "Guard the nullable response</summary>\n"
        "`src/a.py:10`\n"
        "### Why this fails\n"
        "The response may be missing.\n"
        "</details>\n"
        f"**src/a.py:10** [{legacy_severity}] Guard the nullable response\n"
        "### Why this fails\n"
        "The response may be missing.\n"
        "**src/b.py:20** [P1] Second\n"
        "### Why this fails\n"
        "Because.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.severity, finding.title, finding.path, finding.line) for finding in result.findings] == [
        (expected_picture_severity, "Guard the nullable response", "src/a.py", 10),
        ("P1", "Second", "src/b.py", 20),
    ]
    assert result.shortfalls == ()


def test_reconciles_duplicate_location_when_only_legacy_line_is_known() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Guard the response\n"
        "**File:** `src/a.py`\n"
        "Guard against None.\n"
        "**src/a.py:10**: Guard against None.\n"
        "### Independent finding\n"
        "This is a separate finding.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.title, finding.path, finding.line) for finding in result.findings] == [
        ("Guard the response", "src/a.py", None),
        ("Independent finding", ccr_review_format.UNKNOWN_FILE, None),
    ]
    assert result.shortfalls == ()


def test_duplicate_comparison_stops_at_next_legacy_entry_header() -> None:
    body = (
        "<details><summary>Suppressed comments (3)</summary>\n"
        "### [P1] First structured finding\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "First finding explanation.\n"
        "**src/a.py:10**: First finding explanation.\n"
        "**src/b.py:20**: Independent legacy finding.\n"
        "### Third finding\n"
        "The third finding has no file metadata.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.title, finding.path, finding.line) for finding in result.findings] == [
        ("First structured finding", "src/a.py", 10),
        ("Independent legacy finding.", "src/b.py", 20),
        ("Third finding", ccr_review_format.UNKNOWN_FILE, None),
    ]
    assert result.shortfalls == ()


def test_duplicate_comparison_normalizes_leading_bullets() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Guard the response\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "* Guard the response.\n"
        "**src/a.py:10**\n"
        "Guard the response.\n"
        "### Second finding\n"
        "The second finding has no file metadata.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.title, finding.path) for finding in result.findings] == [
        ("Guard the response", "src/a.py"),
        ("Second finding", ccr_review_format.UNKNOWN_FILE),
    ]
    assert result.shortfalls == ()


def test_different_whitespace_in_inline_code_keeps_findings_distinct() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** `src/review.py`\n"
        "**Line:** 23\n"
        "Handle the input `a  b` correctly.\n"
        "**src/review.py:23**: Handle the input `a b` correctly.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert len(result.findings) == 2
    assert result.shortfalls == ()


def test_single_backtick_code_span_with_triple_backticks_keeps_findings_distinct() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** `src/review.py`\n"
        "**Line:** 23\n"
        "Handle `a ``` b  c` carefully.\n"
        "**src/review.py:23**: Handle `a ``` b c` carefully.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert len(result.findings) == 2
    assert result.shortfalls == ()


def test_multiline_inline_code_keeps_findings_distinct() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** `src/review.py`\n"
        "**Line:** 23\n"
        "Handle the input `a\n  b` correctly.\n"
        "**src/review.py:23**: Handle the input `a b` correctly.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert len(result.findings) == 2
    assert result.shortfalls == ()


def test_multiline_inline_code_with_indented_continuation_keeps_findings_distinct() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** src/a.py\n"
        "**Line:** 42\n"
        "Handle `a  b\n"
        "    c` carefully.\n"
        "**src/a.py:42**: Handle `a b\n"
        "    c` carefully.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert len(result.findings) == 2
    assert result.shortfalls == ()


def test_wrapper_like_lines_inside_multiline_inline_code_keep_findings_distinct() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** src/a.py\n"
        "**Line:** 42\n"
        "Preserve `begin\n"
        "<details>\n"
        "end` as literal.\n"
        "**src/a.py:42**: Preserve `begin\n"
        "<details open>\n"
        "end` as literal.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert len(result.findings) == 2
    assert result.shortfalls == ()


def test_line_metadata_inside_multiline_inline_code_is_preserved_for_deduplication() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** src/a.py\n"
        "**Line:** 23\n"
        "Check `begin\n"
        "line: 42\n"
        "end`.\n"
        "**src/a.py:23**: Check `begin\n"
        "line: 43\n"
        "end`.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert len(result.findings) == 2
    assert result.shortfalls == ()


def test_hybrid_code_only_indented_legacy_entry_deduplicates() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "### [P1] Code-only cleanup\n"
        "**File:** `src/cleanup.py`\n"
        "**Line:** 1\n"
        "\n"
        "    if should_cleanup:\n"
        "        cleanup()\n"
        "**src/cleanup.py:1**\n"
        "\n"
        "    if should_cleanup:\n"
        "        cleanup()\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert len(result.findings) == 1
    assert result.findings[0].path == "src/cleanup.py"
    assert result.shortfalls == ()


def test_backticked_legacy_suppressed_path_keeps_literal_escape() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        r"`src/foo\_bar.py`: Legacy finding body."
        "\n</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.title) for finding in result.findings] == [
        (r"src/foo\_bar.py", "Legacy finding body.")
    ]
    assert result.shortfalls == ()


def test_leading_whitespace_only_line_does_not_prevent_legacy_deduplication() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "### [P1] Guard the response\n"
        "**File:** `src/a.py`\n"
        "**Line:** 42\n"
        "    \n"
        "* Guard the response.\n"
        "**src/a.py:42**: * Guard the response.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [
        (finding.section, finding.path, finding.line, finding.title, finding.ordinal) for finding in result.findings
    ] == [("suppressed", "src/a.py", 42, "Guard the response", 1)]
    assert result.shortfalls == ()
