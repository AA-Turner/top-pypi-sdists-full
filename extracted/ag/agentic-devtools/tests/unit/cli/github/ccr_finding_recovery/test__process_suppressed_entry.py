"""Tests for processing legacy suppressed entries."""

import agentic_devtools.cli.github.ccr_review_format as ccr_review_format


def test_structured_suppressed_finding_unescapes_unquoted_markdown_path() -> None:
    body = (
        "### Low confidence comments (1)\n"
        "- [P1] Keep the unquoted source path\n"
        r"**File:** src/foo\_bar.py"
        "\n**Line:** 42\n"
        "The finding belongs to the underscored file."
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.section, finding.path, finding.line) for finding in result.findings] == [
        ("suppressed", "src/foo_bar.py", 42)
    ]
    assert result.shortfalls == ()


def test_inline_file_line_and_unknown_path_are_supported() -> None:
    body = (
        "<details><summary>Previously missed (2)</summary>\n"
        "### [P0] First finding\n"
        "**File:** `src/inline.py:22`\n"
        "Description.\n"
        "### Second finding\n"
        "No file metadata was supplied.\n"
        "</details>"
    )

    findings = ccr_review_format.extract_ccr_findings(body).findings

    assert findings[0].path == "src/inline.py"
    assert findings[0].line == 22
    assert findings[1].path == "(unknown file)"
    assert findings[1].title == "Second finding"
