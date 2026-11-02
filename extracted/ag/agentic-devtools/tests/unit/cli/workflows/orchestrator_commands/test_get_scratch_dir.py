"""Tests for _get_scratch_dir."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.workflows.orchestrator_commands import _get_scratch_dir


@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_feature_slug")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
def test_get_scratch_dir_uses_repo_root_when_available(mock_get_repo_root, mock_get_feature_slug, tmp_path) -> None:
    mock_get_repo_root.return_value = tmp_path
    mock_get_feature_slug.return_value = "demo"

    assert _get_scratch_dir() == tmp_path / ".agdt" / "scratch" / "demo"


@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_feature_slug")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_repo_root")
def test_get_scratch_dir_falls_back_to_cwd(mock_get_repo_root, mock_get_feature_slug, tmp_path) -> None:
    mock_get_repo_root.return_value = None
    mock_get_feature_slug.return_value = "demo"

    with patch.object(Path, "cwd", return_value=tmp_path):
        assert _get_scratch_dir() == tmp_path / ".agdt" / "scratch" / "demo"
