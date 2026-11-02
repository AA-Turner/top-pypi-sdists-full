"""Tests for removal of appended legacy spans."""

import agentic_devtools.cli.github.ccr_review_format as ccr_review_format


def test_double_backticked_structured_location_deduplicates_with_legacy_entry() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "### [P1] Reconcile the report\n"
        "``src/a.py:42``\n"
        "Reconcile the generated report before promotion.\n"
        "**src/a.py:42**\n"
        "* Reconcile the generated report before promotion.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.line) for finding in result.findings] == [("src/a.py", 42)]
    assert result.shortfalls == ()


def test_source_metadata_after_explanation_is_excluded_from_deduplication() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** src/a.py\n"
        "Guard the response.\n"
        "**Line:** 42\n"
        "**src/a.py:42**: Guard the response.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert len(result.findings) == 1
    assert result.shortfalls == ()


def test_whitespace_padded_line_metadata_is_excluded_from_deduplication() -> None:
    for line_metadata in ("  **Line:** 42", "**Line:** 42  "):
        body = (
            "<details><summary>Suppressed comments (1)</summary>\n"
            "### [P1] Structured occurrence\n"
            "**File:** src/a.py\n"
            f"{line_metadata}\n"
            "Guard the response.\n"
            "**src/a.py:42**: Guard the response.\n"
            "</details>"
        )

        result = ccr_review_format.extract_ccr_findings(body)

        assert len(result.findings) == 1
        assert result.shortfalls == ()
