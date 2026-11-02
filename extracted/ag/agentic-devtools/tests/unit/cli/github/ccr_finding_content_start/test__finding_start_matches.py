"""Tests for the private structured finding-boundary selector."""

import pytest

import agentic_devtools.cli.github.ccr_review_format as ccr_review_format
from agentic_devtools.cli.github.ccr_finding_content import _finding_start_matches


def test_legacy_explanation_bullets_and_subheadings_are_not_finding_starts() -> None:
    text = "**src/a.py:10**\n* [P1] Guard against None.\n#### Why this fails\nThe value is unchecked."

    assert _finding_start_matches(text) == []


def test_independent_structured_heading_after_legacy_header_is_a_finding_start() -> None:
    text = "**src/a.py:10**\nLegacy explanation.\n### [P1] Independent structured finding\n**File:** `src/b.py`\n"

    assert [match.group(0) for match in _finding_start_matches(text)] == ["### [P1] Independent structured finding"]


def test_inline_quoted_location_does_not_make_an_explanation_heading_a_finding_start() -> None:
    text = "**src/a.py:10**: First finding.\n### Why this fails\nExample: `src/b.py:20`.\n"

    matches = _finding_start_matches(ccr_review_format._mask_inline_code(text), metadata_text=text)

    assert matches == []


def test_unmatched_legacy_header_offset_is_counted_as_a_distinct_occurrence() -> None:
    text = "Legacy context\n### Second finding\n"

    matches = _finding_start_matches(text, legacy_header_offsets={0}, declared_count=2)

    assert [match.group(0) for match in matches] == ["### Second finding"]


def test_duplicate_legacy_header_matches_backticked_structured_location() -> None:
    text = (
        "### [P1] First finding\n"
        "`src/a.py:10`\n"
        "First finding body.\n"
        "**src/a.py:10**: First finding body.\n"
        "### Second finding\n"
    )
    legacy_header_offsets = {text.index("**src/a.py:10**")}

    matches = _finding_start_matches(
        ccr_review_format._mask_inline_code(text),
        metadata_text=text,
        legacy_header_offsets=legacy_header_offsets,
        declared_count=2,
    )

    assert [match.group(0) for match in matches] == ["### [P1] First finding", "### Second finding"]


@pytest.mark.parametrize(
    ("structured_path", "legacy_path"),
    (
        ("src/foo_bar.py", r"src/foo\_bar.py"),
        (r"src/foo\_bar.py", "src/foo_bar.py"),
    ),
)
def test_duplicate_legacy_header_normalizes_markdown_escaped_path(structured_path: str, legacy_path: str) -> None:
    text = (
        "### [P1] First finding\n"
        f"**File:** {structured_path}\n"
        "**Line:** 10\n"
        "Use `key` carefully.\n"
        f"**{legacy_path}:10**: Use `key` carefully.\n"
        "### Second finding\n"
    )

    matches = _finding_start_matches(
        ccr_review_format._mask_inline_code(text),
        metadata_text=text,
        legacy_header_offsets={text.index(f"**{legacy_path}:10**")},
        declared_count=2,
    )

    assert [match.group(0) for match in matches] == ["### [P1] First finding", "### Second finding"]


def test_duplicate_legacy_header_does_not_unescape_backticked_path() -> None:
    text = (
        "### [P1] First finding\n"
        "**File:** `src/foo_bar.py`\n"
        "**Line:** 10\n"
        "First finding body.\n"
        "**`src/foo\\_bar.py:10`**: First finding body.\n"
        "### Second finding\n"
    )

    matches = _finding_start_matches(
        ccr_review_format._mask_inline_code(text),
        metadata_text=text,
        legacy_header_offsets={text.index("**`src/foo\\_bar.py:10`**")},
        declared_count=2,
    )

    assert [match.group(0) for match in matches] == ["### [P1] First finding"]


def test_duplicate_legacy_explanation_compares_inline_code_from_original_text() -> None:
    text = (
        "### [P1] First finding\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "Use `key` carefully.\n"
        "**src/a.py:10**: Use `key` carefully.\n"
        "### Second finding\n"
    )

    matches = _finding_start_matches(
        ccr_review_format._mask_inline_code(text),
        metadata_text=text,
        legacy_header_offsets={text.index("**src/a.py:10**")},
        declared_count=2,
    )

    assert [match.group(0) for match in matches] == ["### [P1] First finding", "### Second finding"]


def test_location_metadata_is_scoped_to_each_candidate() -> None:
    text = (
        "**src/a.py:10**: First finding.\n"
        "### Why this fails\n"
        "The response may be missing.\n"
        "### Second finding\n"
        "`src/b.py:20`\n"
    )

    matches = _finding_start_matches(
        ccr_review_format._mask_inline_code(text),
        metadata_text=text,
        declared_count=2,
    )

    assert [match.group(0) for match in matches] == ["### Second finding"]


@pytest.mark.parametrize(
    ("location_metadata", "legacy_header"),
    (
        (
            "**File:** `src/a.py`\n**Line:** 10\n",
            "**src/a.py:10**: Different body.\n",
        ),
        (
            "**File:** `src/a.py`\n**Line:** 10\n",
            "**src/b.py:10**: Different path.\n",
        ),
        ("", "**src/a.py:10**: Missing structured location.\n"),
    ),
)
def test_nonduplicate_legacy_header_does_not_reduce_the_declared_count(
    location_metadata: str, legacy_header: str
) -> None:
    text = f"### [P1] First finding\n{location_metadata}First finding body.\n{legacy_header}### Second finding\n"

    matches = _finding_start_matches(
        ccr_review_format._mask_inline_code(text),
        metadata_text=text,
        legacy_header_offsets={text.index(legacy_header)},
        declared_count=2,
    )

    assert [match.group(0) for match in matches] == ["### [P1] First finding"]


def test_explanatory_location_offsets_do_not_hide_an_independent_heading() -> None:
    text = (
        "### [P1] First finding\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "First explanation.\n"
        "`src/input.py:5`\n"
        "**src/a.py:10**: First explanation.\n"
        "`src/input.py:5`\n"
        "### Second finding\n"
    )
    supplied_offsets = {
        match.start()
        for pattern in (ccr_review_format._ENTRY_HEADER_INLINE_RE, ccr_review_format._ENTRY_HEADER_ONLY_RE)
        for match in pattern.finditer(text)
    }

    matches = _finding_start_matches(
        ccr_review_format._mask_inline_code(text),
        metadata_text=text,
        legacy_header_offsets=supplied_offsets,
        declared_count=2,
    )

    assert [match.group(0) for match in matches] == ["### [P1] First finding", "### Second finding"]


def test_mismatched_legacy_severity_keeps_following_heading_counted() -> None:
    text = (
        "### [P1] First finding\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "Guard against None.\n"
        "**src/a.py:10**: [P2] Guard against None.\n"
        "### Second finding\n"
    )
    legacy_header_offsets = {text.index("**src/a.py:10**")}

    matches = _finding_start_matches(
        ccr_review_format._mask_inline_code(text),
        metadata_text=text,
        legacy_header_offsets=legacy_header_offsets,
        declared_count=3,
    )

    assert [match.group(0) for match in matches] == ["### [P1] First finding", "### Second finding"]


def test_empty_legacy_explanation_keeps_following_heading_counted() -> None:
    text = (
        "### [P1] First finding\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "Guard against None.\n"
        "**src/a.py:10**\n"
        "### Second finding\n"
    )
    legacy_header_offsets = {text.index("**src/a.py:10**")}

    matches = _finding_start_matches(
        ccr_review_format._mask_inline_code(text),
        metadata_text=text,
        legacy_header_offsets=legacy_header_offsets,
        declared_count=3,
    )

    assert [match.group(0) for match in matches] == ["### [P1] First finding", "### Second finding"]


def test_nonduplicate_zero_width_path_alias_is_not_recorded_as_ambiguous() -> None:
    text = (
        "### [P1] First finding\n"
        "**File:** `src/\u200ba.py`\n"
        "**Line:** 10\n"
        "First explanation.\n"
        "**src/a.py:10**: Different legacy explanation.\n"
        "### Why this fails\n"
        "The explanation heading is not another finding.\n"
    )
    aliases: set[int] = set()

    matches = _finding_start_matches(
        ccr_review_format._mask_inline_code(text),
        metadata_text=text,
        content_text=text,
        legacy_header_offsets={text.index("**src/a.py:10**")},
        declared_count=2,
        ambiguous_path_aliases=aliases,
    )

    assert [match.group(0) for match in matches] == ["### [P1] First finding"]
    assert aliases == set()


def test_normalized_only_path_match_does_not_free_a_heading_count_slot() -> None:
    text = (
        "### [P1] First finding\n"
        "**File:** `src/\u200ba.py`\n"
        "**Line:** 10\n"
        "First explanation.\n"
        "**src/a.py:10**: First explanation.\n"
        "### Why this fails\n"
    )
    supplied_offsets = {
        match.start()
        for pattern in (ccr_review_format._ENTRY_HEADER_INLINE_RE, ccr_review_format._ENTRY_HEADER_ONLY_RE)
        for match in pattern.finditer(text)
    }

    matches = _finding_start_matches(
        ccr_review_format._mask_inline_code(text),
        metadata_text=text,
        legacy_header_offsets=supplied_offsets,
        declared_count=2,
    )

    assert [match.group(0) for match in matches] == ["### [P1] First finding"]


@pytest.mark.parametrize(
    ("suffix", "expected_titles"),
    (
        ("", ["### [P1] First finding"]),
        (
            "\n### Why this fails\n"
            "```md\n"
            "**File:** `src/note.py`\n"
            "```\n"
            "### [P1] Second finding\n"
            "**File:** `src/b.py`\n",
            ["### [P1] First finding", "### [P1] Second finding"],
        ),
    ),
)
def test_normalized_alias_scan_stops_at_next_structured_occurrence(suffix: str, expected_titles: list[str]) -> None:
    content = (
        "### [P1] First finding\n"
        "**File:** `src/\u200ba.py`\n"
        "**Line:** 10\n"
        "First explanation.\n"
        "**src/a.py:10**: First explanation."
        f"{suffix}"
    )
    metadata_text = ccr_review_format._mask_fenced_blocks(content)
    ambiguous_path_aliases: set[int] = set()

    matches = _finding_start_matches(
        ccr_review_format._mask_inline_code(metadata_text),
        metadata_text=metadata_text,
        content_text=content,
        legacy_header_offsets={content.index("**src/a.py:10**")},
        declared_count=2,
        ambiguous_path_aliases=ambiguous_path_aliases,
    )

    assert [match.group(0) for match in matches] == expected_titles
    assert ambiguous_path_aliases == set()


@pytest.mark.parametrize(
    ("structured_start", "expected_severity"),
    (
        ("- [P1] Guard the response\n**File:** `src/a.py`\n**Line:** 10\n", "P1"),
        (
            '<summary><picture><img alt="High severity"></picture>Guard the response</summary>\n`src/a.py:10`\n',
            "HIGH",
        ),
    ),
)
def test_explanation_heading_does_not_count_after_severity_mismatch(
    structured_start: str,
    expected_severity: str,
) -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        f"{structured_start}"
        "The guard is missing.\n"
        "**src/a.py:10**: [P2] Guard the response\n"
        "### Why this fails\n"
        "The missing guard permits an invalid response.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.severity, finding.path) for finding in result.findings] == [
        (expected_severity, "src/a.py"),
        ("P2", "src/a.py"),
    ]
    assert result.shortfalls == ()


def test_h3_explanation_is_preserved_in_uncounted_suppressed_wrapper() -> None:
    body = (
        "<details><summary>Comments suppressed due to low confidence</summary>\n"
        "**src/a.py:10**: Guard the response.\n"
        "### Why this fails\n"
        "The implementation can fail when the value is missing.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.line, finding.body) for finding in result.findings] == [
        (
            "src/a.py",
            10,
            "Guard the response.\n### Why this fails\nThe implementation can fail when the value is missing.",
        )
    ]
    assert result.shortfalls == ()


def test_h3_explanation_is_preserved_when_structured_finding_satisfies_count() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "**src/a.py:10**: Guard the response.\n"
        "### Why this fails\n"
        "The implementation can fail when the value is missing.\n"
        "### [P1] Independent structured finding\n"
        "**File:** `src/b.py`\n"
        "The second issue.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.title, finding.path, finding.body) for finding in result.findings] == [
        (
            "Guard the response.",
            "src/a.py",
            "Guard the response.\n### Why this fails\nThe implementation can fail when the value is missing.",
        ),
        (
            "Independent structured finding",
            "src/b.py",
            "### [P1] Independent structured finding\n**File:** `src/b.py`\nThe second issue.",
        ),
    ]
    assert result.shortfalls == ()


def test_picture_summary_after_structured_and_legacy_entry_is_a_boundary() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] First finding\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "First finding body.\n"
        "**src/a.py:10**: First finding body.\n\n"
        "<details>\n"
        '<summary><picture><img alt="Medium severity"></picture>Second finding</summary>\n'
        "`src/b.py:20`\n"
        "Second finding body.\n"
        "</details>\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.severity, finding.title, finding.path, finding.line) for finding in result.findings] == [
        ("P1", "First finding", "src/a.py", 10),
        ("MEDIUM", "Second finding", "src/b.py", 20),
    ]
    assert result.shortfalls == ()
