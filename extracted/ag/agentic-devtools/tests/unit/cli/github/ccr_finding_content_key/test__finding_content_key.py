"""Tests for normalized finding-content comparison keys."""

from agentic_devtools.cli.github.ccr_finding_content_key import _finding_content_key


def test_normalizes_leading_bullet_and_finding_metadata() -> None:
    structured = "### [P1] Guard the response\n**File:** `src/a.py`\n**Line:** 10\n* Guard the response.\n"

    assert _finding_content_key(structured) == _finding_content_key("Guard the response.\n")


def test_preserves_whitespace_inside_inline_code() -> None:
    assert _finding_content_key("Use `a  b` as written.") != _finding_content_key("Use `a b` as written.")


def test_preserves_content_after_unicode_line_separator_inside_inline_code() -> None:
    first = "Use `input\u2028alpha`."
    second = "Use `input\u2028beta`."

    assert _finding_content_key(first) != _finding_content_key(second)


def test_does_not_detect_fences_inside_inline_code() -> None:
    first = "Use ``a  b\u2028```\u2028end``."
    second = "Use ``a b\u2028```\u2028end``."

    assert _finding_content_key(first) != _finding_content_key(second)


def test_preserves_resolution_status_inside_code_blocks() -> None:
    fenced_status = "```text\nResolved since the previous review.\n```"
    indented_status = "    Resolved since the previous review."

    assert _finding_content_key(fenced_status) != _finding_content_key("```text\n```")
    assert _finding_content_key(indented_status) != _finding_content_key("    ")


def test_preserves_resolution_status_inside_multiline_inline_code() -> None:
    status_code = "Example: ``\nResolved since the previous review.\n``"
    blank_code = "Example: ``\n\n``"

    assert _finding_content_key(status_code) != _finding_content_key(blank_code)


def test_ignores_standalone_resolution_status_during_comparison() -> None:
    body = "Finding body.\nResolved since the previous review.\nResolved since the last review.\n"

    assert _finding_content_key(body) == _finding_content_key("Finding body.\n")


def test_normalizes_fenced_and_indented_code_blocks() -> None:
    body = (
        "Opening prose.\n"
        "</details>\n"
        "    first code line\n"
        "    \n"
        "Between code blocks.\n"
        "    second code line\n"
        "\n"
        "Closing prose.\n"
    )

    assert _finding_content_key(body) == (
        ("prose", "Opening prose."),
        ("indented", "    first code line"),
        ("prose", "Between code blocks."),
        ("indented", "    second code line"),
        ("fenced", ""),
        ("prose", "Closing prose."),
    )


def test_fenced_code_requires_a_matching_closing_delimiter() -> None:
    body = "Before.\n`````python\n```\n~~~\n````` trailing text\n`````\nAfter.\n"

    assert _finding_content_key(body) == (
        ("prose", "Before."),
        ("fenced", "`````python\n```\n~~~\n````` trailing text\n`````"),
        ("fenced", ""),
        ("prose", "After."),
    )


def test_ignores_out_of_range_appended_legacy_spans() -> None:
    body = "The original finding."

    assert _finding_content_key(body, ((len(body) + 1, len(body) + 3),)) == _finding_content_key(body)


def test_empty_body_has_no_prose_content() -> None:
    assert _finding_content_key("") == (("fenced", ""),)


def test_leading_blank_line_is_normalized_before_prose_content() -> None:
    assert _finding_content_key("\nBody.") == (("fenced", ""), ("prose", "Body."))
