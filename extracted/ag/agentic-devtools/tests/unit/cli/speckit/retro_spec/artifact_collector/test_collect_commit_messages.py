"""Tests for collect_commit_messages in retro_spec/artifact_collector.py."""

from __future__ import annotations

import subprocess
from unittest.mock import patch

from agentic_devtools.cli.speckit.retro_spec.artifact_collector import collect_commit_messages


class TestCollectCommitMessages:
    """Tests for the collect_commit_messages function."""

    def test_returns_empty_when_command_fails(self) -> None:
        """Test that failures return an empty list."""
        with patch(
            "agentic_devtools.cli.speckit.retro_spec.artifact_collector.subprocess.run",
            return_value=subprocess.CompletedProcess([], 1, "", "boom"),
        ):
            assert collect_commit_messages("owner", "repo", 42) == []

    def test_returns_empty_when_os_error_raised(self) -> None:
        """Test that an OSError (e.g., gh missing) degrades to an empty list."""
        with patch(
            "agentic_devtools.cli.speckit.retro_spec.artifact_collector.subprocess.run",
            side_effect=OSError("No such file or directory"),
        ):
            assert collect_commit_messages("owner", "repo", 42) == []

    def test_filters_blank_lines_from_commit_output(self) -> None:
        """Test that empty output lines are removed."""
        with patch(
            "agentic_devtools.cli.speckit.retro_spec.artifact_collector.subprocess.run",
            return_value=subprocess.CompletedProcess([], 0, "feat: add thing\n\nfix: tidy\n", ""),
        ):
            assert collect_commit_messages("owner", "repo", 42) == ["feat: add thing", "fix: tidy"]
