"""Tests for _collect_extra_test_targets."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.cli.checks.changed_files import DiffUnavailableError
from agentic_devtools.cli.checks.commands import _collect_extra_test_targets

MODULE = "agentic_devtools.cli.checks.commands"


class TestCollectExtraTestTargets:
    """Tests for _collect_extra_test_targets."""

    @patch(f"{MODULE}.get_changed_files", return_value=[])
    @patch(f"{MODULE}._find_test_path", return_value=None)
    def test_uncovered_changed_test_returned(self, _ftp, _gcf, tmp_path):
        result = _collect_extra_test_targets(["tests/unit/other/test_bar.py"], [], tmp_path)
        assert result == ["tests/unit/other/test_bar.py"]

    @patch(f"{MODULE}.get_changed_files", return_value=[])
    def test_covered_by_test_file_excluded(self, _gcf, tmp_path):
        covered = "tests/unit/foo/test_foo.py"
        with patch(f"{MODULE}._find_test_path", return_value=str(tmp_path / covered)):
            result = _collect_extra_test_targets([covered], ["agentic_devtools/foo.py"], tmp_path)
        assert result == []

    @patch(f"{MODULE}.get_changed_files", return_value=[])
    def test_covered_by_directory_excluded(self, _gcf, tmp_path):
        covered_dir = tmp_path / "tests" / "unit" / "foo"
        with patch(f"{MODULE}._find_test_path", return_value=str(covered_dir)):
            result = _collect_extra_test_targets(["tests/unit/foo/test_bar.py"], ["agentic_devtools/foo.py"], tmp_path)
        assert result == []

    @patch(f"{MODULE}.get_changed_files", return_value=[])
    def test_covered_directory_equal_candidate_excluded(self, _gcf, tmp_path):
        covered_dir = tmp_path / "tests" / "unit" / "foo"
        with patch(f"{MODULE}._find_test_path", return_value=str(covered_dir)):
            result = _collect_extra_test_targets(["tests/unit/foo"], ["agentic_devtools/foo.py"], tmp_path)
        assert result == []

    @patch(f"{MODULE}.find_consumer_test_paths", return_value=["tests/unit/adapters/github_provider/test_x.py"])
    @patch(f"{MODULE}.get_changed_files", return_value=["tests/unit/adapters/issue_provider/_c.py"])
    @patch(f"{MODULE}._find_test_path", return_value=None)
    def test_support_file_consumer_added(self, _ftp, _gcf, _fctp, tmp_path):
        result = _collect_extra_test_targets([], [], tmp_path)
        assert result == ["tests/unit/adapters/github_provider/test_x.py"]

    @patch(f"{MODULE}.find_consumer_test_paths", return_value=["tests/unit/other/test_bar.py"])
    @patch(f"{MODULE}.get_changed_files", return_value=["tests/conftest.py"])
    @patch(f"{MODULE}._find_test_path", return_value=None)
    def test_support_consumer_not_duplicated(self, _ftp, _gcf, _fctp, tmp_path):
        result = _collect_extra_test_targets(["tests/unit/other/test_bar.py"], [], tmp_path)
        assert result == ["tests/unit/other/test_bar.py"]

    @patch(f"{MODULE}.find_consumer_test_paths", return_value=["tests/unit/foo/test_bar.py"])
    @patch(f"{MODULE}.get_changed_files", return_value=["tests/conftest.py"])
    def test_support_consumer_already_covered_excluded(self, _gcf, _fctp, tmp_path):
        covered_dir = tmp_path / "tests" / "unit" / "foo"
        with patch(f"{MODULE}._find_test_path", return_value=str(covered_dir)):
            result = _collect_extra_test_targets([], ["agentic_devtools/foo.py"], tmp_path)
        assert result == []

    @patch(f"{MODULE}.find_consumer_test_paths")
    @patch(f"{MODULE}.get_changed_files", side_effect=DiffUnavailableError("no git"))
    @patch(f"{MODULE}._find_test_path", return_value=None)
    def test_diff_unavailable_skips_support_mapping(self, _ftp, _gcf, mock_fctp, tmp_path):
        result = _collect_extra_test_targets(["tests/unit/other/test_bar.py"], [], tmp_path)
        assert result == ["tests/unit/other/test_bar.py"]
        mock_fctp.assert_not_called()
