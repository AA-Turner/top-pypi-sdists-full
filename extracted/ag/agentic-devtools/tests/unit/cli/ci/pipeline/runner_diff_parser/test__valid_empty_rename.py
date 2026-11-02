"""Tests for validating empty pure renames."""

from agentic_devtools.cli.ci.pipeline.runner_diff_parser import _valid_empty_rename


def test_accepts_supported_similarity_and_mode_change_metadata() -> None:
    similarity = "similarity index 100%"
    assert _valid_empty_rename([similarity, "rename from old.py", "rename to new.py"], similarity)
    assert _valid_empty_rename(
        ["old mode 100644", "new mode 100755", similarity, "rename from old.py", "rename to new.py"],
        similarity,
    )


def test_rejects_unmodified_mode_or_malformed_metadata() -> None:
    similarity = "similarity index 100%"
    assert not _valid_empty_rename(
        ["old mode 100644", "new mode 100644", similarity, "rename from old.py", "rename to new.py"], similarity
    )
