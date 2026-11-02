"""Tests for parsing Git index blob hashes."""

from agentic_devtools.cli.ci.pipeline.runner_diff_parser import _parse_index_hashes


def test_parses_equal_length_blob_hashes() -> None:
    hashes = _parse_index_hashes("index 0000000..e69de29")

    assert hashes is not None
    assert hashes.old_hash == "0000000"
    assert hashes.new_hash == "e69de29"


def test_rejects_malformed_or_mismatched_hashes() -> None:
    assert _parse_index_hashes("index malformed") is None
    assert _parse_index_hashes("index 0000000..e69de29abcdef") is None
