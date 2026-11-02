"""Tests for preparing structured and legacy suppressed entries."""

import agentic_devtools.cli.github.ccr_review_format as ccr_review_format


def test_structured_finding_text_is_preserved_in_uncounted_mixed_wrapper() -> None:
    body = (
        "<details><summary>Comments suppressed due to low confidence</summary>\n"
        "**src/a.py:10**: First finding.\n"
        "### [P1] Independent structured finding\n"
        "**File:** `src/b.py`\n"
        "The second issue.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.body) for finding in result.findings] == [
        ("src/a.py", "First finding."),
        (
            "src/b.py",
            "### [P1] Independent structured finding\n**File:** `src/b.py`\nThe second issue.",
        ),
    ]
    assert result.shortfalls == ()


def test_purely_structured_findings_in_uncounted_wrapper_are_recovered() -> None:
    body = (
        "<details><summary>Comments suppressed due to low confidence</summary>\n"
        "### [P1] First structured finding\n"
        "**File:** `src/a.py`\n"
        "The first issue.\n"
        "### [P2] Second structured finding\n"
        "**File:** `src/b.py`\n"
        "The second issue.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.severity) for finding in result.findings] == [
        ("src/a.py", "P1"),
        ("src/b.py", "P2"),
    ]
    assert result.shortfalls == ()


def test_structured_finding_followed_by_independent_legacy_in_uncounted_wrapper() -> None:
    body = (
        "<details><summary>Comments suppressed due to low confidence</summary>\n"
        "### [P1] First finding\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "First finding body.\n\n"
        "**src/b.py:20**: Second finding.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.line) for finding in result.findings] == [
        ("src/a.py", 10),
        ("src/b.py", 20),
    ]
    assert result.shortfalls == ()


def test_later_suppressed_count_does_not_split_an_uncounted_wrapper() -> None:
    body = (
        "<details><summary>Comments suppressed due to low confidence</summary>\n"
        "**src/a.py:10**: Guard the response.\n"
        "### Why this fails\n"
        "The implementation can fail when the value is missing.\n"
        "</details>\n"
        "<details><summary>Suppressed comments (2)</summary>\n"
        "**src/b.py:20**: Preserve the response.\n"
        "**src/c.py:30**: Preserve the request.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert result.findings[0].body == (
        "Guard the response.\n### Why this fails\nThe implementation can fail when the value is missing."
    )


def test_heading_only_suppressed_declaration_records_unrecovered_count() -> None:
    body = "### Suppressed findings (1)\n### Other section\n"

    result = ccr_review_format.extract_ccr_findings(body)

    assert result.findings == ()
    assert ("suppressed", 1, 0) in result.shortfalls


def test_suppressed_declaration_without_following_section_has_shortfall() -> None:
    result = ccr_review_format.extract_ccr_findings("### Suppressed findings (1)\n")

    assert result.shortfalls == (("suppressed", 1, 0),)


def test_legacy_suppressed_count_shortfall_is_reported() -> None:
    body = "<details><summary>Suppressed comments (2)</summary>\n**src/one.py**: One recoverable entry\n</details>"

    result = ccr_review_format.extract_ccr_findings(body)

    assert len(result.findings) == 1
    assert result.shortfalls == (("suppressed", 2, 1),)


def test_legacy_recovery_does_not_clear_another_suppressed_declaration_shortfall() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "**src/legacy.py**: Recover this entry\n"
        "</details>\n"
        "<details><summary>Low confidence (1)</summary>\n"
        "This entry cannot be recovered.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.title) for finding in result.findings] == [("src/legacy.py", "Recover this entry")]
    assert result.shortfalls == (("suppressed", 1, 0),)


def test_legacy_entries_without_count_declarations_do_not_create_shortfalls() -> None:
    body = (
        "<details><summary>Comments suppressed due to low confidence</summary>\n"
        "**src/legacy.py**: Recover this entry\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert len(result.findings) == 1
    assert result.findings[0].path == "src/legacy.py"
    assert result.shortfalls == ()


def test_legacy_entries_are_recovered_from_each_suppressed_declaration() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "**src/first.py**: First legacy finding\n"
        "</details>\n"
        "<details><summary>Low confidence (1)</summary>\n"
        "**src/second.py**: Second legacy finding\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.title, finding.ordinal) for finding in result.findings] == [
        ("src/first.py", "First legacy finding", 1),
        ("src/second.py", "Second legacy finding", 2),
    ]
    assert result.shortfalls == ()


def test_final_legacy_declaration_without_closing_wrapper_is_recovered() -> None:
    body = "<summary>Suppressed comments (1)</summary>\n**src/final.py**: Final legacy finding"

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.title) for finding in result.findings] == [("src/final.py", "Final legacy finding")]
    assert result.shortfalls == ()


def test_unmatched_legacy_entry_does_not_satisfy_a_later_declaration() -> None:
    body = (
        "<details><summary>Comments suppressed due to low confidence</summary>\n"
        "**src/legacy.py**: Earlier entry\n"
        "</details>\n"
        "<details><summary>Low confidence (1)</summary>\n"
        "No recoverable entry.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert len(result.findings) == 1
    assert result.findings[0].path == "src/legacy.py"
    assert result.shortfalls == (("suppressed", 1, 0),)


def test_nested_empty_summary_does_not_recover_an_unrelated_sibling_finding() -> None:
    body = (
        "<details>\n"
        "<summary>Review details</summary>\n"
        "<details>\n"
        "<summary>Previously missed (1)</summary>\n"
        "</details>\n"
        "### [P1] Unrelated historical finding\n"
        "**File:** `src/unrelated.py`\n"
        "**Line:** 12\n"
        "This finding is outside the nested declaration.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert result.findings == ()
    assert result.shortfalls == (("previously_missed", 1, 0),)
