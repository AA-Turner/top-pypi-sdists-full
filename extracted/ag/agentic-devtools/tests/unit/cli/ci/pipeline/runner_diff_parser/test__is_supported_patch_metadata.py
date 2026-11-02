"""Tests for supported patch metadata classification."""

from agentic_devtools.cli.ci.pipeline.runner_diff_parser import _is_supported_patch_metadata


def test_accepts_supported_metadata_and_rejects_unknown_lines() -> None:
    assert _is_supported_patch_metadata("index 0123456..abcdef0")
    assert _is_supported_patch_metadata("rename from old.py")
    assert not _is_supported_patch_metadata("unsupported metadata")
