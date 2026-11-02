"""Tests for observation watermark decoding."""

from __future__ import annotations

from agentic_devtools.cli.ci.github_provider import _decode_observation_watermark


def test_decode_observation_watermark_uses_valid_values() -> None:
    """Decode persisted review, comment, and commit watermarks."""
    assert _decode_observation_watermark('{"review":4,"comment":7,"commit":"sha"}') == (4, 7, "sha")


def test_decode_observation_watermark_rejects_non_mapping() -> None:
    """Treat a valid non-object JSON watermark as a legacy value."""
    assert _decode_observation_watermark("[]") == (0, 0, "[]")
