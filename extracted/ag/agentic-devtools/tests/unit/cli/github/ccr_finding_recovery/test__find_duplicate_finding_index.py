"""Tests for duplicate recovered-finding selection."""

import pytest

import agentic_devtools.cli.github.ccr_review_format as ccr_review_format


def test_normalized_path_duplicate_before_next_structured_finding_is_reconciled() -> None:
    body = (
        "<details><summary>Suppressed comments (3)</summary>\n"
        "### [P1] First finding\n"
        "**File:** `src/\u200ba.py`\n"
        "**Line:** 10\n"
        "Same explanation.\n"
        "**src/a.py:10**: Same explanation.\n"
        "### [P1] Second finding\n"
        "**File:** `src/b.py`\n"
        "**Line:** 20\n"
        "Second explanation.\n"
        "### Third finding\n"
        "No file metadata was supplied.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.title, finding.path) for finding in result.findings] == [
        ("First finding", "src/\u200ba.py"),
        ("Second finding", "src/b.py"),
        ("Third finding", ccr_review_format.UNKNOWN_FILE),
    ]
    assert result.shortfalls == ()


def test_normalized_path_findings_remain_distinct_without_declared_count() -> None:
    body = (
        "<details><summary>Comments suppressed due to low confidence</summary>\n"
        "### [P1] First finding\n"
        "**File:** `src/\u200ba.py`\n"
        "**Line:** 10\n"
        "Same explanation.\n"
        "`src/a.py:10`\n"
        "* Same explanation.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.title, finding.path, finding.line) for finding in result.findings] == [
        ("First finding", "src/\u200ba.py", 10),
        ("Same explanation.", "src/a.py", 10),
    ]
    assert result.shortfalls == ()


def test_legacy_duplicate_after_another_structured_finding_is_not_deduplicated() -> None:
    body = (
        "<details><summary>Suppressed comments (3)</summary>\n"
        "### [P1] First structured finding\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "First finding explanation.\n"
        "### [P2] Second structured finding\n"
        "**File:** `src/b.py`\n"
        "**Line:** 20\n"
        "Second finding explanation.\n"
        "**src/a.py:10**\n"
        "* First finding explanation.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.line) for finding in result.findings] == [
        ("src/a.py", 10),
        ("src/b.py", 20),
        ("src/a.py", 10),
    ]
    assert result.shortfalls == ()


def test_escaped_legacy_suppressed_entry_deduplicates_with_structured_finding() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** `src/foo_bar.py`\n"
        "Legacy finding body.\n"
        r"**src/foo\_bar.py**: Legacy finding body."
        "\n</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.title) for finding in result.findings] == [
        ("src/foo_bar.py", "Structured occurrence")
    ]
    assert result.shortfalls == ()


def test_repeated_legacy_suppressed_occurrences_are_not_deduplicated() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "**src/repeated.py:10**: Repeated finding\n"
        "**src/repeated.py:10**: Repeated finding\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.line, finding.title) for finding in result.findings] == [
        ("src/repeated.py", 10, "Repeated finding"),
        ("src/repeated.py", 10, "Repeated finding"),
    ]
    assert result.shortfalls == ()


def test_distinct_mixed_format_findings_with_normalized_paths_are_not_deduplicated() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** `src/\u200brepeated.py`\n"
        "**Line:** 10\n"
        "Structured finding text.\n"
        "**src/repeated.py:20**: Different legacy finding text.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.line, finding.title) for finding in result.findings] == [
        ("src/\u200brepeated.py", 10, "Structured occurrence"),
        ("src/repeated.py", 20, "Different legacy finding text."),
    ]
    assert result.shortfalls == ()


def test_nested_suppressed_finding_deduplicates_structured_and_legacy_entries() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "<details>\n"
        '<summary><picture alt="P1"></picture>Nested finding</summary>\n'
        "`src/client.py:42`\n"
        "The explanation appears once.\n"
        "</details>\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.line, finding.title) for finding in result.findings] == [
        ("src/client.py", 42, "Nested finding")
    ]
    assert result.shortfalls == ()


def test_legacy_example_does_not_interfere_with_hybrid_deduplication() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Finding A\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "Finding A explanation.\n"
        "Example:\n"
        "```markdown\n"
        "**src/b.py:20**: Finding B explanation.\n"
        "```\n"
        "**src/a.py:10**: Finding A explanation.\n"
        "Example:\n"
        "```markdown\n"
        "**src/b.py:20**: Finding B explanation.\n"
        "```\n"
        "**src/b.py:20**: Finding B explanation.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.title) for finding in result.findings] == [
        ("src/a.py", "Finding A"),
        ("src/b.py", "Finding B explanation."),
    ]
    assert result.shortfalls == ()


def test_repeated_preamble_prose_is_not_promoted_as_a_second_suppressed_finding() -> None:
    body = "Repeated finding sentence.\n\n### Suppressed comments (1)\n\nRepeated finding sentence.\n"

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.body, finding.ordinal) for finding in result.findings] == [("Repeated finding sentence.", 1)]
    assert result.shortfalls == ()


def test_identical_legacy_entries_in_separate_declarations_remain_distinct() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** `src/repeated.py`\n"
        "Repeated legacy finding\n"
        "**src/repeated.py**: Repeated legacy finding\n"
        "</details>\n"
        "<details><summary>Low confidence (1)</summary>\n"
        "**src/repeated.py**: Repeated legacy finding\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.title, finding.ordinal) for finding in result.findings] == [
        ("src/repeated.py", "Structured occurrence", 1),
        ("src/repeated.py", "Repeated legacy finding", 2),
    ]
    assert result.shortfalls == ()


def test_only_one_identical_legacy_entry_is_deduplicated_against_a_structured_finding() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** `src/repeated.py`\n"
        "Repeated legacy finding\n"
        "**src/repeated.py**: Repeated legacy finding\n"
        "**src/repeated.py**: Repeated legacy finding\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.title, finding.ordinal) for finding in result.findings] == [
        ("src/repeated.py", "Structured occurrence", 1),
        ("src/repeated.py", "Repeated legacy finding", 2),
    ]
    assert result.shortfalls == ()


def test_deferred_normalized_duplicate_reserves_structured_occurrence() -> None:
    body = (
        "<details><summary>Suppressed comments (3)</summary>\n"
        "### [P1] Structured A\n"
        "**File:** `src/\u200ba.py`\n"
        "**Line:** 10\n"
        "Finding A.\n"
        "**src/a.py:10**: Finding A.\n"
        "**src/b.py:20**: Finding B.\n"
        "**src/a.py:10**: Finding A.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.title, finding.ordinal) for finding in result.findings] == [
        ("src/\u200ba.py", "Structured A", 1),
        ("src/b.py", "Finding B.", 2),
        ("src/a.py", "Finding A.", 3),
    ]
    assert result.shortfalls == ()


@pytest.mark.parametrize(
    "legacy_entries",
    [
        "**src/a.py:10**: Same explanation.\n**src/b.py:20**: Independent B.",
        "**src/b.py:20**: Independent B.\n**src/a.py:10**: Same explanation.",
    ],
)
def test_normalized_duplicate_reconciliation_is_independent_of_legacy_entry_order(legacy_entries: str) -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** `src/\u200ba.py`\n"
        "**Line:** 10\n"
        "Same explanation.\n"
        f"{legacy_entries}\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.line, finding.title) for finding in result.findings] == [
        ("src/\u200ba.py", 10, "Structured occurrence"),
        ("src/b.py", 20, "Independent B."),
    ]
    assert result.shortfalls == ()
