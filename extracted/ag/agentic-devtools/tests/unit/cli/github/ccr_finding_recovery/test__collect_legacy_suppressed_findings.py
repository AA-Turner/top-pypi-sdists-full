"""Tests for legacy suppressed-finding collection."""

import agentic_devtools.cli.github.ccr_review_format as ccr_review_format


def test_crlf_and_legacy_suppressed_findings_remain_supported() -> None:
    body = (
        "<details>\r\n"
        "<summary>Comments suppressed due to low confidence (1)</summary>\r\n"
        "\r\n"
        "**src/legacy.py**: Retain the existing fallback behavior\r\n"
        "\r\n</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert len(result.findings) == 1
    assert result.findings[0].section == "suppressed"
    assert result.findings[0].path == "src/legacy.py"
    assert "Retain the existing fallback behavior" in result.findings[0].body
    assert result.shortfalls == ()


def test_mixed_structured_and_legacy_suppressed_entries_are_recovered() -> None:
    body = (
        "<details><summary>Suppressed comments (3)</summary>\n"
        "### [P1] Structured occurrence\n"
        "**File:** `src/structured.py`\n"
        "Structured finding body.\n"
        "**src/structured.py**: Structured finding body.\n"
        "**src/legacy.py**: Legacy finding body.\n"
        "**src/legacy-only.py:19**\n"
        "- Legacy header-only body.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.title) for finding in result.findings] == [
        ("src/structured.py", "Structured occurrence"),
        ("src/legacy.py", "Legacy finding body."),
        ("src/legacy-only.py", "Legacy header-only body."),
    ]
    assert result.findings[2].line == 19
    assert result.shortfalls == ()


def test_consecutive_structured_and_legacy_entries_keep_their_boundaries() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Guard the first response\n"
        "**File:** `src/a.py`\n"
        "**Line:** 10\n"
        "Guard A.\n"
        "**src/a.py:10**\n"
        "* Guard A.\n"
        "### [P2] Guard the second response\n"
        "**File:** `src/b.py`\n"
        "**Line:** 20\n"
        "Guard B.\n"
        "**src/b.py:20**\n"
        "* Guard B.\n"
        "</details>"
    )

    entries = ccr_review_format.extract_suppressed_comment_entries(body)
    result = ccr_review_format.extract_ccr_findings(body)

    assert entries == [("src/a.py:10", "Guard A."), ("src/b.py:20", "Guard B.")]
    assert [(finding.path, finding.line) for finding in result.findings] == [
        ("src/a.py", 10),
        ("src/b.py", 20),
    ]
    assert result.shortfalls == ()


def test_hybrid_structured_and_legacy_entry_uses_legacy_explanation_once() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "### [P1] Preserve the explanation\n"
        "**File:** `src/review.py`\n"
        "**Line:** 23\n"
        "**src/review.py:23**\n"
        "The explanation appears only after the legacy header.\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert len(result.findings) == 1
    assert result.findings[0].title == "Preserve the explanation"
    assert result.shortfalls == ()


def test_hybrid_entry_and_independent_legacy_entry_recover_declared_count() -> None:
    body = (
        "<details><summary>Suppressed comments (2)</summary>\n"
        "### [P1] Preserve the explanation\n"
        "**File:** `src/review.py`\n"
        "**Line:** 23\n"
        "**src/review.py:23**\n"
        "The explanation appears only after the legacy header.\n"
        "**src/other.py:10**: Other finding\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.title) for finding in result.findings] == [
        ("src/review.py", "Preserve the explanation"),
        ("src/other.py", "Other finding"),
    ]
    assert result.shortfalls == ()


def test_long_preamble_preserves_order_for_mixed_suppressed_entries() -> None:
    body = (
        "Review preamble: " + "x" * 1000 + "\n<details><summary>Suppressed comments (3)</summary>\n"
        "### [P1] First structured occurrence\n"
        "**File:** `src/first.py`\n"
        "First finding body.\n"
        "### [P2] Second structured occurrence\n"
        "**File:** `src/second.py`\n"
        "Second finding body.\n"
        "**src/legacy.py**: Later legacy finding body.\n"
        "</details>"
    )

    findings = ccr_review_format.extract_ccr_findings(body).findings

    assert [(finding.path, finding.ordinal) for finding in findings] == [
        ("src/first.py", 1),
        ("src/second.py", 2),
        ("src/legacy.py", 3),
    ]


def test_empty_legacy_extraction_keeps_the_declared_shortfall(monkeypatch) -> None:
    body = "<details><summary>Suppressed comments (1)</summary>\nPlain section\n</details>"
    monkeypatch.setattr(ccr_review_format, "extract_suppressed_comment_entries", lambda _body, **_kwargs: [])

    result = ccr_review_format.extract_ccr_findings(body)

    assert result.findings == ()
    assert result.shortfalls == (("suppressed", 1, 0),)


def test_unmappable_legacy_entry_is_not_added_as_a_finding(monkeypatch) -> None:
    body = "<details><summary>Comments suppressed due to low confidence</summary>\nActual body\n</details>"
    monkeypatch.setattr(
        ccr_review_format,
        "extract_suppressed_comment_entries",
        lambda _body, **_kwargs: [("(unknown file)", "Synthetic entry")],
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert result.findings == ()
    assert result.shortfalls == ()
