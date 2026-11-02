"""Tests for consuming rename and similarity metadata."""

from agentic_devtools.cli.ci.pipeline.runner_diff_parser import _consume_patch_metadata


def test_returns_named_rename_metadata_state() -> None:
    state = _consume_patch_metadata("rename from old.py", "", "", "")

    assert state is not None
    assert state.rename_from == "old.py"
    assert state.rename_to == ""
    assert state.similarity_index == ""


def test_rejects_binary_duplicate_and_unsupported_metadata() -> None:
    assert _consume_patch_metadata("GIT binary patch", "", "", "") is None
    assert _consume_patch_metadata("rename from old.py", "already-set", "", "") is None
    assert _consume_patch_metadata("unknown", "", "", "") is None
