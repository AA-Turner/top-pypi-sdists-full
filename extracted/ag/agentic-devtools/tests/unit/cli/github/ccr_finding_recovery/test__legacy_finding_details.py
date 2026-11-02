"""Tests for metadata derived from a recovered legacy finding."""

from agentic_devtools.cli.github.ccr_finding_recovery import (
    _FindingRecoveryState,
    _legacy_finding_details,
    _LegacyEntry,
    _SuppressedBlock,
)


def test_severity_bullet_and_blank_separation_normalize_title_and_comparison() -> None:
    state = _FindingRecoveryState(body="", source_review_id=1, source_review_url="")
    block = _SuppressedBlock(
        block="",
        block_offset=0,
        declared_count=None,
        structured_spans=(),
        parsed_entries=[],
        masked_block="",
        ordered_headers=[],
        boundary_ends={},
        legacy_occurrences=(),
    )
    entry = _LegacyEntry(
        offset=0,
        occurrence="",
        body="[P1] Guard the response.",
        candidate_body="\n\n- [P1] Guard the response.",
        finding_occurrences=(),
    )

    details = _legacy_finding_details(state, block, entry, "src/client.py:42", "[P1] Guard the response.")

    assert (details.path, details.line, details.severity, details.title) == (
        "src/client.py",
        42,
        "P1",
        "Guard the response.",
    )
    assert details.comparison_content == (("fenced", ""), ("prose", "Guard the response."))
