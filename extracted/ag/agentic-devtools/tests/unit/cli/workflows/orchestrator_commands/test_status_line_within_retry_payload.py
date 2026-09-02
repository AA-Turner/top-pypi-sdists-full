"""Tests for _status_line_within_retry_payload."""

from agentic_devtools.cli.workflows.orchestrator_commands import _status_line_within_retry_payload


def test_status_line_within_retry_payload_accepts_non_rename_changes_inside_prefix() -> None:
    assert _status_line_within_retry_payload(" M .agdt/scratch/slug/file.txt", ".agdt/scratch/slug")


def test_status_line_within_retry_payload_rejects_malformed_short_lines() -> None:
    assert not _status_line_within_retry_payload("??", ".agdt/scratch/slug")


def test_status_line_within_retry_payload_validates_both_sides_of_rename() -> None:
    assert _status_line_within_retry_payload(
        "R  .agdt/scratch/slug/old.txt -> .agdt/scratch/slug/new.txt",
        ".agdt/scratch/slug",
    )
    assert not _status_line_within_retry_payload(
        "R  .agdt/scratch/slug/old.txt -> outside/new.txt",
        ".agdt/scratch/slug",
    )
