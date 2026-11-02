"""Tests for reading a patch's hunk and rename metadata."""

from agentic_devtools.cli.ci.pipeline.runner_diff_parser import _read_patch_metadata


def test_returns_named_metadata_for_a_complete_patch() -> None:
    metadata = _read_patch_metadata(["@@ -1 +1 @@", "-old", "+new"])

    assert metadata is not None
    assert metadata.hunk_count == 1
    assert metadata.changed_line_count == 2
    assert metadata.rename_from == ""
    assert metadata.rename_to == ""


def test_rejects_unrecognized_patch_metadata() -> None:
    assert _read_patch_metadata(["unsupported metadata"]) is None
