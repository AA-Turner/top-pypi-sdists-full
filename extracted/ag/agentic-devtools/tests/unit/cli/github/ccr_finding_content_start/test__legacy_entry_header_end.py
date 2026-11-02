"""Tests for _legacy_entry_header_end()."""

import agentic_devtools.cli.github.ccr_review_format as ccr_review_format
from agentic_devtools.cli.github.ccr_finding_content_start import (
    _FindingStartContext,
    _legacy_entry_header_end,
)


def test_uses_match_start_when_no_previous_header_or_separator_exists() -> None:
    text = "### Finding"
    context = _FindingStartContext(
        text=text,
        location_text=text,
        comparison_text=text,
        header_matches={},
        legacy_header_offsets=set(),
        candidates=[],
        structured_occurrences=set(),
        declared_count=None,
        ambiguous_path_aliases=None,
    )

    assert _legacy_entry_header_end(context, len(text), []) == (len(text), None, None)


def test_backticked_location_metadata_allows_heading_boundary_without_unmasking_quotes() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] First finding\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "First finding body.\n"
        "**src/a.py:10**: First finding body.\n"
        "### Second finding\n"
        "`src/b.py:20`\n"
        "The second finding has a source location.\n"
        "The prose quotes `src/quoted.py:30` as an example.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.title, finding.path, finding.line) for finding in result.findings] == [
        ("First finding", "src/a.py", 10),
        ("Second finding", "src/b.py", 20),
    ]
    assert result.shortfalls == ()


def test_consecutive_legacy_headers_keep_metadata_with_their_findings() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "`src/a.py:10`\n"
        "* [P1] First finding.\n"
        "`src/b.py:20`\n"
        "* [P1] Second finding.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.line) for finding in result.findings] == [
        ("src/a.py", 10),
        ("src/b.py", 20),
    ]
    assert result.shortfalls == ()


def test_different_fenced_snippets_do_not_split_legacy_explanation_heading() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** `src/review.py`\n"
        "**Line:** 23\n"
        "Identical prose.\n"
        "```yaml\n"
        "path: input\n"
        "```\n"
        "**src/review.py:23**: Identical prose.\n"
        "```yaml\n"
        "path: output\n"
        "```\n"
        "### Why this fails\n"
        "The output path is not accepted.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.title, finding.path) for finding in result.findings] == [
        ("Structured occurrence", "src/review.py"),
        ("Identical prose.", "src/review.py"),
    ]
    assert result.findings[1].body == (
        "Identical prose.\n```yaml\npath: output\n```\n### Why this fails\nThe output path is not accepted."
    )
    assert result.shortfalls == ()


def test_adjacent_legacy_header_only_entries_are_both_recovered() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "`src/a.py:10`\n"
        "* First finding.\n"
        "`src/b.py:20`\n"
        "\n"
        "* Second finding.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.line, finding.title) for finding in result.findings] == [
        ("src/a.py", 10, "First finding."),
        ("src/b.py", 20, "Second finding."),
    ]
    assert result.shortfalls == ()


def test_backticked_legacy_header_does_not_split_structured_boundaries() -> None:
    body = (
        "### Suppressed comments (1)\n\n"
        "`src/a.py:10`\n"
        "* [P1] Guard against None.\n"
        "#### Why this fails\n"
        "The value is unchecked.\n"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.title) for finding in result.findings] == [("src/a.py", "[P1] Guard against None.")]
    assert result.shortfalls == ()


def test_unmatched_legacy_header_does_not_prevent_a_later_match(monkeypatch) -> None:
    body = "<details><summary>Suppressed comments (1)</summary>\n**src/a.py**: Recover this entry\n</details>"
    monkeypatch.setattr(
        ccr_review_format,
        "extract_suppressed_comment_entries",
        lambda _body, **_kwargs: [("src/missing.py", "Not present"), ("src/a.py", "Recover this entry")],
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.title) for finding in result.findings] == [("src/a.py", "Recover this entry")]
    assert result.shortfalls == ()
