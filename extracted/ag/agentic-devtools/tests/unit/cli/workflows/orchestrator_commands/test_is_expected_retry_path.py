"""Tests for _is_expected_retry_path."""

from agentic_devtools.cli.workflows.orchestrator_commands import _is_expected_retry_path


def test_is_expected_retry_path_accepts_exact_prefix_match() -> None:
    assert _is_expected_retry_path(".agdt/scratch/slug", ".agdt/scratch/slug")


def test_is_expected_retry_path_accepts_child_paths_only() -> None:
    assert _is_expected_retry_path(".agdt/scratch/slug/file.txt", ".agdt/scratch/slug")
    assert not _is_expected_retry_path(".agdt/scratch/slug-other/file.txt", ".agdt/scratch/slug")
