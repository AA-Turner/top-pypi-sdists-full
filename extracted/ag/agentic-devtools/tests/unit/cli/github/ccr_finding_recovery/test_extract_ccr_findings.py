"""Tests for structured extraction of hidden CCR findings."""

import agentic_devtools.cli.github.ccr_finding_recovery as ccr_finding_recovery
import agentic_devtools.cli.github.ccr_review_format as ccr_review_format


def test_extracts_previously_missed_findings_despite_zero_open_summary() -> None:
    body = (
        "<!-- ccr-overview-v2 -->\n"
        "0 open findings\n"
        "<details>\n"
        "<summary><strong>Previously missed (2)</strong></summary>\n"
        "### [P1] Guard the nullable response\n"
        "**File:** `src/client.py`\n"
        "**Line:** 42\n"
        "The response may be missing.\n"
        "### [P2] Preserve the original exception\n"
        "**File:** `src/retry.py`\n"
        "**Line:** 17\n"
        "The retry wrapper loses the traceback.\n"
        "</details>"
    )

    result = ccr_finding_recovery.extract_ccr_findings(
        body,
        source_review_id=8420,
        source_review_url="https://github.com/example/repo/pull/4#pullrequestreview-8420",
    )

    assert result.shortfalls == ()
    assert [(finding.severity, finding.title, finding.path, finding.line) for finding in result.findings] == [
        ("P1", "Guard the nullable response", "src/client.py", 42),
        ("P2", "Preserve the original exception", "src/retry.py", 17),
    ]
    assert [finding.ordinal for finding in result.findings] == [1, 2]
    assert all(finding.section == "previously_missed" for finding in result.findings)
    assert all(finding.source_review_id == 8420 for finding in result.findings)
    assert all(
        finding.source_review_url == "https://github.com/example/repo/pull/4#pullrequestreview-8420"
        for finding in result.findings
    )


def test_previously_missed_entry_with_backticked_path_and_severity_bullet_is_recovered() -> None:
    body = (
        "<details><summary>Previously missed (1)</summary>\n"
        "`src/a.py:10`\n"
        "* [P1] Guard the nullable response\n"
        "</details>"
    )

    result = ccr_finding_recovery.extract_ccr_findings(body)

    assert result.shortfalls == ()
    assert [(finding.severity, finding.title) for finding in result.findings] == [("P1", "Guard the nullable response")]


def test_extracts_findings_from_strong_wrapped_overview_v2_declaration() -> None:
    body = (
        "<!-- ccr-overview-v2 -->\n"
        "0 open findings\n"
        "<details open>\n"
        "<summary><strong>Previously missed (2)</strong></summary>\n"
        "\n"
        "### [P1] Preserve the authenticated author\n"
        "**File:** `agentic_devtools/cli/ci/github_provider.py`\n"
        "**Line:** 3975\n"
        "A marker comment from another author must not be trusted.\n"
        "\n"
        "### [P1] Select the current replacement line\n"
        "**File:** `agentic_devtools/cli/ci/review_thread_promotion.py`\n"
        "**Line:** 97\n"
        "Prefer the RIGHT-side anchor over a deleted LEFT-side line.\n"
        "</details>"
    )

    result = ccr_finding_recovery.extract_ccr_findings(body, source_review_id=5460509463)

    assert result.shortfalls == ()
    assert [(finding.title, finding.path, finding.line) for finding in result.findings] == [
        ("Preserve the authenticated author", "agentic_devtools/cli/ci/github_provider.py", 3975),
        ("Select the current replacement line", "agentic_devtools/cli/ci/review_thread_promotion.py", 97),
    ]
    assert [finding.source_review_id for finding in result.findings] == [5460509463, 5460509463]


def test_extracts_nested_overview_v2_findings_and_standalone_path_anchors() -> None:
    body = (
        "<!-- ccr-overview-v2 -->\n"
        "0 open findings\n"
        "<details open>\n"
        "<summary><strong>Previously missed (2)</strong></summary>\n"
        "<details>\n"
        '<summary><picture><source media="(prefers-color-scheme: dark)" '
        'srcset="low-v2-dark.svg"><source media="(prefers-color-scheme: light)" '
        'srcset="low-v2-light.svg"><img src="low-v2-light.png" alt="Low severity" '
        'width="62" height="18" align="texttop"></picture>Preserve the original exception</summary>\n'
        "`agentic_devtools/cli/ci/github_provider.py:3975`\n"
        "A marker comment from another author must not be trusted.\n"
        "</details>\n"
        "<details>\n"
        '<summary><picture><source media="(prefers-color-scheme: dark)" '
        'srcset="low-v2-dark.svg"><source media="(prefers-color-scheme: light)" '
        'srcset="low-v2-light.svg"><img src="low-v2-light.png" alt="Low severity" '
        'width="62" height="18" align="texttop"></picture>Select the current replacement line</summary>\n'
        "`agentic_devtools/cli/ci/review_thread_promotion.py:97`\n"
        "Prefer the RIGHT-side anchor over a deleted LEFT-side line.\n"
        "</details>\n"
        "</details>"
    )

    result = ccr_finding_recovery.extract_ccr_findings(body, source_review_id=5460509463)

    assert result.shortfalls == ()
    assert [(finding.severity, finding.title, finding.path, finding.line) for finding in result.findings] == [
        ("LOW", "Preserve the original exception", "agentic_devtools/cli/ci/github_provider.py", 3975),
        ("LOW", "Select the current replacement line", "agentic_devtools/cli/ci/review_thread_promotion.py", 97),
    ]
    assert all(finding.source_review_id == 5460509463 for finding in result.findings)


def test_coalesces_picture_duplicate_with_markdown_escaped_legacy_path() -> None:
    body = (
        "<details><summary>Previously missed (1)</summary>\n"
        "<details>\n"
        '<summary><picture alt="P1"></picture>Guard the response</summary>\n'
        "`src/foo_bar.py:10`\n"
        "The response must be guarded.\n"
        "</details>\n"
        r"**src/foo\_bar.py:10** [P1] Guard the response"
        "\nThe response must be guarded."
        "\n</details>"
    )

    result = ccr_finding_recovery.extract_ccr_findings(body)

    assert result.shortfalls == ()
    assert [(finding.severity, finding.title, finding.path, finding.line) for finding in result.findings] == [
        ("P1", "Guard the response", "src/foo_bar.py", 10)
    ]


def test_preserves_distinct_picture_and_legacy_findings_with_normalized_path_matches() -> None:
    body = (
        "<details><summary>Previously missed (2)</summary>\n"
        '<summary><picture alt="P1"></picture>Guard the response</summary>\n'
        "`src/\u200ba.py:10`\n"
        "The response may be missing.\n"
        "**src/a.py:10** [P1] Preserve the original exception\n"
        "The original error is useful.\n"
        "</details>"
    )

    result = ccr_finding_recovery.extract_ccr_findings(body)

    assert [(finding.title, finding.path, finding.line) for finding in result.findings] == [
        ("Guard the response", "src/\u200ba.py", 10),
        ("Preserve the original exception", "src/a.py", 10),
    ]
    assert result.shortfalls == ()


def test_empty_missed_section_has_no_shortfall() -> None:
    body = "<!-- ccr-overview-v2 -->\n<details><summary>Previously missed (0)</summary>\n</details>"

    assert ccr_finding_recovery.extract_ccr_findings(body).findings == ()
    assert ccr_finding_recovery.extract_ccr_findings(body).shortfalls == ()


def test_ignores_suppressed_commentary_declaration() -> None:
    body = (
        "### Suppressed commentary (1)\n\n"
        "- [P1] Historical finding\n"
        "**File:** `src/historical.py`\n"
        "**Line:** 12\n"
        "This is unrelated historical prose."
    )

    result = ccr_finding_recovery.extract_ccr_findings(body)

    assert result.findings == ()
    assert result.shortfalls == ()


def test_reconciles_low_confidence_comments_declaration() -> None:
    body = (
        "### Low confidence comments (2)\n\n"
        "- [P1] Guard the response\n"
        "**File:** `src/client.py`\n"
        "**Line:** 42\n"
        "The response may be missing."
    )

    result = ccr_finding_recovery.extract_ccr_findings(body)

    assert [(finding.section, finding.title, finding.path, finding.line) for finding in result.findings] == [
        ("suppressed", "Guard the response", "src/client.py", 42)
    ]
    assert result.shortfalls == (("suppressed", 2, 1),)


def test_metadata_free_heading_after_legacy_entry_is_recovered_as_unknown_file() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "**src/a.py:10**: First finding.\n"
        "### Second finding\n"
        "No file metadata was supplied.\n"
        "</details>"
    )

    result = ccr_finding_recovery.extract_ccr_findings(body)

    assert [(finding.title, finding.path) for finding in result.findings] == [
        ("First finding.", "src/a.py"),
        ("Second finding", ccr_review_format.UNKNOWN_FILE),
    ]
    assert result.shortfalls == ()


def test_h3_explanation_does_not_split_single_legacy_entry() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "**src/a.py:10**: First finding.\n"
        "### Why this fails\n"
        "The implementation can fail when the value is missing.\n"
        "</details>"
    )

    result = ccr_finding_recovery.extract_ccr_findings(body)

    assert [(finding.title, finding.path, finding.body) for finding in result.findings] == [
        (
            "First finding.",
            "src/a.py",
            "First finding.\n### Why this fails\nThe implementation can fail when the value is missing.",
        )
    ]
    assert result.shortfalls == ()


def test_fenced_legacy_explanation_does_not_swallow_severity_finding() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "**src/a.py:10**\n"
        "```python\n"
        'value = "src/a.py"\n'
        "```\n"
        "\n"
        "- [P1] Second finding\n"
        "</details>"
    )

    result = ccr_finding_recovery.extract_ccr_findings(body)

    assert len(result.findings) == 2
    assert result.findings[0].path == "src/a.py"
    assert result.findings[0].body == '```python\nvalue = "src/a.py"\n```'
    assert (result.findings[1].title, result.findings[1].path) == (
        "Second finding",
        ccr_review_format.UNKNOWN_FILE,
    )
    assert result.shortfalls == ()


def test_reconciles_duplicate_legacy_entry_before_counting_heading_boundaries() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] First finding\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "First finding body.\n"
        "**src/a.py:10**: First finding body.\n"
        "### Second finding\n"
        "The second finding has no file metadata.\n"
        "</details>"
    )

    result = ccr_finding_recovery.extract_ccr_findings(body)

    assert [(finding.title, finding.path) for finding in result.findings] == [
        ("First finding", "src/a.py"),
        ("Second finding", ccr_review_format.UNKNOWN_FILE),
    ]
    assert result.shortfalls == ()


def test_duplicate_comparison_preserves_inline_code_whitespace() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Preserve exact code\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "Use `a  b` as written.\n"
        "**src/a.py:10**\n"
        "Use `a b` as written.\n\n"
        "### Why this fails\n"
        "The literal spacing changes the result.\n"
        "</details>"
    )

    result = ccr_finding_recovery.extract_ccr_findings(body)

    assert [(finding.title, finding.path) for finding in result.findings] == [
        ("Preserve exact code", "src/a.py"),
        ("Use `a b` as written.", "src/a.py"),
    ]
    assert result.shortfalls == ()


def test_different_fenced_code_snippets_keep_structured_and_legacy_findings_distinct() -> None:
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
        "</details>"
    )

    result = ccr_finding_recovery.extract_ccr_findings(body)

    assert len(result.findings) == 2
    assert "path: input" in result.findings[0].body
    assert "path: output" in result.findings[1].body
    assert result.findings[1].body == "Identical prose.\n```yaml\npath: output\n```"
    assert result.shortfalls == ()


def test_identical_fenced_code_snippets_deduplicate_structured_and_legacy_findings() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** `src/review.py`\n"
        "**Line:** 23\n"
        "Identical prose.\n"
        "```yaml\n"
        "path: input\n"
        "```\n"
        "**src/review.py:23**: Identical prose.\n"
        "```yaml\n"
        "path: input\n"
        "```\n"
        "</details>"
    )

    result = ccr_finding_recovery.extract_ccr_findings(body)

    assert len(result.findings) == 1
    assert result.findings[0].title == "Structured occurrence"
    assert "path: input" in result.findings[0].body
    assert result.shortfalls == ()


def test_deduplicates_resolved_aliases_but_keeps_different_severity_levels() -> None:
    cases = (("P1", "", True, 1), ("High", "P1", False, 1), ("High", "P2", False, 2))
    for structured_severity, legacy_severity, resolved, expected_count in cases:
        status = "Resolved since the previous review.\n" if resolved else ""
        legacy_label = f"[{legacy_severity}] " if legacy_severity else ""
        body = (
            f"<details><summary>Suppressed comments (1)</summary>\n### [{structured_severity}] Guard the response\n"
            "**File:** `src/a.py`\n**Line:** 10\nThe response must be guarded.\n"
            f"**src/a.py:10**: {legacy_label}The response must be guarded.\n{status}</details>"
        )
        result = ccr_finding_recovery.extract_ccr_findings(body)
        assert len(result.findings) == expected_count
        assert result.shortfalls == (() if expected_count == 1 else (("suppressed", 1, 2),))
        finding = result.findings[0]
        assert (finding.severity, finding.explicitly_resolved) == (structured_severity.upper(), resolved)
        assert ("Resolved since the previous review." in result.findings[0].body) is resolved


def test_indentation_sensitive_fenced_snippets_keep_findings_distinct() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** `src/review.py`\n"
        "**Line:** 23\n"
        "Identical prose.\n"
        "```python\n"
        "if should_cleanup:\n"
        "    cleanup()\n"
        "```\n"
        "**src/review.py:23**: Identical prose.\n"
        "```python\n"
        "if should_cleanup:\n"
        "cleanup()\n"
        "```\n"
        "</details>"
    )

    result = ccr_finding_recovery.extract_ccr_findings(body)

    assert len(result.findings) == 2
    assert "    cleanup()" in result.findings[0].body
    assert "\ncleanup()" in result.findings[1].body
    assert result.shortfalls == ()


def test_indentation_sensitive_indented_snippets_keep_findings_distinct() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** `src/review.py`\n"
        "**Line:** 23\n"
        "Identical prose.\n"
        "    if should_cleanup:\n"
        "        cleanup()\n"
        "The snippet comes from the caller.\n"
        "**src/review.py:23**: Identical prose.\n"
        "    if should_cleanup:\n"
        "    cleanup()\n"
        "The snippet comes from the caller.\n"
        "</details>"
    )

    result = ccr_finding_recovery.extract_ccr_findings(body)

    assert len(result.findings) == 2
    assert "        cleanup()" in result.findings[0].body
    assert "    cleanup()" in result.findings[1].body
    assert result.shortfalls == ()


def test_identical_indented_snippets_deduplicate_structured_and_legacy_findings() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** `src/review.py`\n"
        "**Line:** 23\n"
        "Identical prose.\n"
        "    if should_cleanup:\n"
        "        cleanup()\n"
        "**src/review.py:23**: Identical prose.\n"
        "    if should_cleanup:\n"
        "        cleanup()\n"
        "</details>"
    )

    result = ccr_finding_recovery.extract_ccr_findings(body)

    assert len(result.findings) == 1
    assert "        cleanup()" in result.findings[0].body
    assert result.shortfalls == ()


def test_trailing_whitespace_only_indented_line_does_not_block_deduplication() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** `src/review.py`\n"
        "**Line:** 23\n"
        "Identical prose.\n"
        "    if should_cleanup:\n"
        "        cleanup()\n"
        "    \n"
        "**src/review.py:23**: Identical prose.\n"
        "    if should_cleanup:\n"
        "        cleanup()\n"
        "</details>"
    )

    result = ccr_finding_recovery.extract_ccr_findings(body)

    assert len(result.findings) == 1
    assert result.findings[0].path == "src/review.py"
    assert result.shortfalls == ()


def test_whitespace_only_indented_chunk_does_not_affect_deduplication() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** `src/review.py`\n"
        "**Line:** 23\n"
        "Identical prose.\n"
        "    \n"
        "Boundary note.\n"
        "**src/review.py:23**: Identical prose.\n"
        "    \n"
        "Boundary note.\n"
        "</details>"
    )

    result = ccr_finding_recovery.extract_ccr_findings(body)

    assert len(result.findings) == 1
    assert result.shortfalls == ()


def test_empty_body_and_unrelated_body_have_no_findings() -> None:
    assert ccr_finding_recovery.extract_ccr_findings("").findings == ()
    assert ccr_finding_recovery.extract_ccr_findings("No hidden review sections.").shortfalls == ()
