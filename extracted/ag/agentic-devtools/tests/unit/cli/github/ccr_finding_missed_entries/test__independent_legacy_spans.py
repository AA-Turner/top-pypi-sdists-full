"""Tests for isolating independent legacy entries from structured findings."""

import pytest

from agentic_devtools.cli.github.ccr_finding_missed_entries import _independent_legacy_spans


def test_inline_code_legacy_path_is_not_unescaped_as_an_independent_entry() -> None:
    block = "**`src/other.py:20`**: Independent legacy finding."

    assert _independent_legacy_spans(block, structured_path="src/current.py", structured_line=10) == ((0, len(block)),)


def test_no_legacy_entry_headers_returns_no_spans() -> None:
    block = "### [P1] Structured finding\nNo legacy entries."

    assert _independent_legacy_spans(block, structured_path="src/current.py", structured_line=10) == ()


@pytest.mark.parametrize("legacy_path", ["src/a.py:10", "src/\u200ba.py:10"])
def test_same_location_different_legacy_content_is_independent(legacy_path: str) -> None:
    block = (
        "### [P1] Open finding\n"
        "**File:** `src/\u200ba.py`\n"
        "**Line:** 10\n"
        "Open explanation.\n"
        f"**{legacy_path}**: Different resolved finding.\n"
        "Resolved since the previous review."
    )
    start = block.index("**" + legacy_path)

    assert _independent_legacy_spans(block, structured_path="src/\u200ba.py", structured_line=10) == (
        (start, len(block)),
    )


def test_same_location_and_content_is_not_an_independent_legacy_entry() -> None:
    block = (
        "### [P1] Open finding\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "Open explanation.\n"
        "**src/a.py:10**: Open explanation.\n"
        "Resolved since the previous review."
    )

    assert _independent_legacy_spans(block, structured_path="src/a.py", structured_line=10) == ()


@pytest.mark.parametrize("indent", ["    ", "\t"])
def test_indented_severity_like_code_does_not_make_duplicate_independent(indent: str) -> None:
    block = (
        "### [P1] Finding\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        f"{indent}[P1] literal code\n"
        "**src/a.py:10**:\n"
        f"{indent}[P1] literal code\n"
        "Resolved since the previous review."
    )

    assert _independent_legacy_spans(block, structured_path="src/a.py", structured_line=10) == ()


def test_resolution_status_inside_code_does_not_hide_an_independent_legacy_entry() -> None:
    block = (
        "### [P1] Finding\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "Finding details.\n"
        "```text\n"
        "Resolved since the previous review.\n"
        "```\n"
        "**src/a.py:10**: Finding details.\n"
        "```text\n"
        "\n"
        "```\n"
        "Resolved since the previous review."
    )

    start = block.index("**src/a.py:10**")

    assert _independent_legacy_spans(block, structured_path="src/a.py", structured_line=10) == ((start, len(block)),)


def test_picture_summary_location_is_metadata_before_later_independent_entry() -> None:
    block = (
        '<summary><picture alt="P1"></picture>Finding</summary>\n'
        "`src/a.py:10`\n"
        "Resolved since the previous review.\n"
        "**src/b.py:20**: Independent finding.\n"
        "Resolved since the previous review."
    )
    start = block.index("**src/b.py:20**")

    assert _independent_legacy_spans(block, structured_path="src/a.py", structured_line=10) == ((start, len(block)),)


@pytest.mark.parametrize("heading", ["### [P1] Guard", '<summary><picture alt="P1"></picture>Guard</summary>'])
def test_standalone_location_and_matching_continuation_are_not_independent(heading: str) -> None:
    block = (
        f"{heading}\n"
        "`src/a.py:10`\n"
        "Guard the response.\n"
        "**src/a.py:10**: Guard the response.\n"
        "Resolved since the previous review."
    )

    assert _independent_legacy_spans(block, structured_path="src/a.py", structured_line=10) == ()
