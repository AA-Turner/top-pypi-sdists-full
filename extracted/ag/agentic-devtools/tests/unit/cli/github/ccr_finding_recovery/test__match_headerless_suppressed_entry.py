"""Tests for headerless legacy suppressed-entry matching."""

import agentic_devtools.cli.github.ccr_review_format as ccr_review_format
from agentic_devtools.cli.github.ccr_finding_recovery import _match_headerless_suppressed_entry, _SuppressedBlock


def _block(ordered_headers: list[tuple[int, tuple[str, int, bool]]]) -> _SuppressedBlock:
    return _SuppressedBlock(
        block="legacy text",
        block_offset=0,
        declared_count=None,
        structured_spans=(),
        parsed_entries=[],
        masked_block="legacy text",
        ordered_headers=ordered_headers,
        boundary_ends={},
        legacy_occurrences=(),
    )


def test_returns_none_for_unknown_path_when_structured_headers_exist() -> None:
    assert (
        _match_headerless_suppressed_entry(_block([(0, ("src/a.py", 10, False))]), "(unknown file)", "legacy text")
        is None
    )


def test_returns_none_for_known_path_without_structured_headers() -> None:
    assert _match_headerless_suppressed_entry(_block([]), "src/a.py", "legacy text") is None


def test_legacy_headerless_fallback_is_recovered_from_each_supported_block() -> None:
    body = (
        "<details><summary>Suppressed comments (1)</summary>\n"
        "First headerless finding\n"
        "</details>\n"
        "<details><summary>Suppressed comments (1)</summary>\n"
        "Second headerless finding\n"
        "</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.title, finding.ordinal) for finding in result.findings] == [
        ("(unknown file)", "First headerless finding", 1),
        ("(unknown file)", "Second headerless finding", 2),
    ]
    assert result.shortfalls == ()


def test_unstructured_legacy_text_without_a_count_is_recovered_as_unknown_file() -> None:
    body = (
        "<details><summary>Comments suppressed due to low confidence</summary>\n\n"
        "```text\nquoted excerpt\n```\n\n"
        "Unstructured text\n</details>"
    )

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.title, finding.body) for finding in result.findings] == [
        ("(unknown file)", "Unstructured text", "Unstructured text")
    ]
    assert result.shortfalls == ()


def test_fallback_suppressed_text_counts_as_a_recovered_declared_entry() -> None:
    body = "<details><summary>Suppressed comments (1)</summary>\nNo supported entry header is present.\n</details>"

    result = ccr_review_format.extract_ccr_findings(body)

    assert [(finding.path, finding.title) for finding in result.findings] == [
        ("(unknown file)", "No supported entry header is present.")
    ]
    assert result.shortfalls == ()
