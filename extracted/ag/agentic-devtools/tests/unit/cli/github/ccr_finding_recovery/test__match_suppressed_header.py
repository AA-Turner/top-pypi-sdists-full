"""Tests for matching a legacy header to a structured finding."""

from agentic_devtools.cli.github.ccr_finding_recovery import _match_suppressed_header, _SuppressedBlock


def test_mismatched_legacy_header_is_skipped_before_a_later_match() -> None:
    text = "**src/a.py:10**\nFirst finding.\n**src/b.py:20**\n- Second finding.\n"
    first_header_end = len("**src/a.py:10**")
    second_header = text.index("**src/b.py:20**")
    second_header_end = second_header + len("**src/b.py:20**")
    block = _SuppressedBlock(
        block=text,
        block_offset=0,
        declared_count=2,
        structured_spans=(),
        parsed_entries=[],
        masked_block=text,
        ordered_headers=[
            (0, ("src/a.py:10", first_header_end, False)),
            (second_header, ("src/b.py:20", second_header_end, False)),
        ],
        boundary_ends={0: second_header, second_header: len(text)},
        legacy_occurrences=(),
    )

    result = _match_suppressed_header(block, "src/b.py:20", "Second finding.")

    assert result is not None
    assert result.offset == second_header
    assert result.body == "Second finding."
    assert second_header in block.matched_header_offsets
