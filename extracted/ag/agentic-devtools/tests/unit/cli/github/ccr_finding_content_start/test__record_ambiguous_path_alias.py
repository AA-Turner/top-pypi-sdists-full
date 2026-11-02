"""Tests for _record_ambiguous_path_alias()."""

import agentic_devtools.cli.github.ccr_review_format as ccr_review_format
from agentic_devtools.cli.github.ccr_finding_content_start import (
    _FindingStartContext,
    _record_ambiguous_path_alias,
)


def _context(
    text: str,
    *,
    structured_occurrences: set[int],
    ambiguous_path_aliases: set[int] | None,
) -> _FindingStartContext:
    return _FindingStartContext(
        text=text,
        location_text=text,
        comparison_text=text,
        header_matches={},
        legacy_header_offsets=set(),
        candidates=[],
        structured_occurrences=structured_occurrences,
        declared_count=None,
        ambiguous_path_aliases=ambiguous_path_aliases,
    )


def test_returns_when_alias_collection_is_not_requested() -> None:
    _record_ambiguous_path_alias(
        _context("### Finding\n", structured_occurrences=set(), ambiguous_path_aliases=None),
        0,
    )


def test_stops_before_a_heading_after_the_next_structured_occurrence() -> None:
    aliases: set[int] = set()
    context = _context("x\n### Later heading\n", structured_occurrences={1}, ambiguous_path_aliases=aliases)

    _record_ambiguous_path_alias(context, 0)

    assert aliases == set()


def test_records_alias_when_following_heading_has_no_location_metadata() -> None:
    aliases: set[int] = set()
    context = _context("x\n### Unlocated heading\n", structured_occurrences=set(), ambiguous_path_aliases=aliases)

    _record_ambiguous_path_alias(context, 0)

    assert aliases == {0}


def test_stops_after_location_metadata_on_the_next_occurrence() -> None:
    text = "x\n### Next finding\nFile: src/a.py\n"
    aliases: set[int] = set()
    context = _context(
        text,
        structured_occurrences={text.index("### Next finding")},
        ambiguous_path_aliases=aliases,
    )

    _record_ambiguous_path_alias(context, 0)

    assert aliases == set()


def test_file_metadata_without_inline_code_is_found_and_missing_line_stays_unknown() -> None:
    body = (
        "<details><summary>Previously missed (1)</summary>\n"
        "### Finding title\n"
        "**File:** src/no-line.py\n"
        "No source line was supplied.\n"
        "</details>"
    )

    finding = ccr_review_format.extract_ccr_findings(body).findings[0]

    assert finding.title == "Finding title"
    assert finding.path == "src/no-line.py"
    assert finding.line is None


def test_unquoted_file_metadata_unescapes_markdown_underscore() -> None:
    body = (
        "<details><summary>Previously missed (1)</summary>\n"
        "### Finding title\n"
        r"**File:** src/foo\_bar.py"
        "\nThe path uses a Markdown escape.\n</details>"
    )

    finding = ccr_review_format.extract_ccr_findings(body).findings[0]

    assert finding.path == "src/foo_bar.py"


def test_backticked_file_metadata_keeps_literal_backslash() -> None:
    body = (
        "<details><summary>Previously missed (1)</summary>\n"
        r"**File:** `src/foo\_bar.py`"
        "\nThe code-span path is literal.\n</details>"
    )

    finding = ccr_review_format.extract_ccr_findings(body).findings[0]

    assert finding.path == r"src/foo\_bar.py"


def test_legacy_suppressed_entry_unescapes_path_without_shortfall() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        r"**src/foo\_bar.py**: Legacy finding body."
        "\n</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.title) for finding in result.findings] == [
        ("src/foo_bar.py", "Legacy finding body.")
    ]
    assert result.shortfalls == ()


def test_escaped_backslashes_and_underscores_match_in_structured_and_legacy_paths() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "### [P1] Structured occurrence\n"
        r"**File:** src/foo\\\_bar.py"
        "\n**Line:** 42\n"
        "The structured and legacy paths refer to the same file.\n"
        r"**src/foo\\\_bar.py:42**: The structured and legacy paths refer to the same file."
        "\n</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.line) for finding in result.findings] == [(r"src/foo\_bar.py", 42)]
    assert result.shortfalls == ()


def test_line_range_metadata_matches_legacy_entry() -> None:
    for separator in ("-", "–"):
        body = (
            "<details><summary>Suppressed comments (1)</summary>\n"
            "### [P1] Guard the response\n"
            "**File:** src/a.py\n"
            f"**Lines:** 42{separator}44\n"
            "Guard the response.\n"
            "**src/a.py:42**: Guard the response.\n"
            "</details>"
        )

        result = ccr_review_format.extract_ccr_findings(body)

        assert [(finding.path, finding.line) for finding in result.findings] == [("src/a.py", 42)]
        assert result.shortfalls == ()


def test_legacy_entry_with_zero_width_path_artifact_deduplicates_with_structured_finding() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** `src/\u200brepeated.py`\n"
        "Repeated legacy finding\n"
        "**src/repeated.py**: Repeated legacy finding\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.title) for finding in result.findings] == [
        ("src/\u200brepeated.py", "Structured occurrence")
    ]
    assert result.shortfalls == ()


def test_distinct_literal_paths_are_not_deduplicated_by_normalized_path() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** `src/\u200ba.py`\n"
        "**Line:** 10\n"
        "Same explanation.\n"
        "**src/a.py:10**: Same explanation.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.line) for finding in result.findings] == [
        ("src/\u200ba.py", 10),
        ("src/a.py", 10),
    ]
    assert result.shortfalls == ()
