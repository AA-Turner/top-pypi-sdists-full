"""Tests for _get_changed_files_between_commits."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.azure_devops.review_prompt_tracking import _get_changed_files_between_commits


def test_returns_normalized_paths_from_git_diff() -> None:
    with patch(
        "agentic_devtools.cli.azure_devops.review_prompt_tracking.run_safe",
        return_value=MagicMock(returncode=0, stdout="src/a.py\n\nsrc/b.py\n"),
    ) as run_safe:
        result = _get_changed_files_between_commits("old", "new", lambda path: path.lower())

    assert result == {"src/a.py", "src/b.py"}
    run_safe.assert_called_once()
