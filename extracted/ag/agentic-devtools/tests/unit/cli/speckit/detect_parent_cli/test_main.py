"""Tests for detect_parent_cli.main()."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.speckit.detect_parent_cli import main
from agentic_devtools.cli.speckit.hierarchy import HierarchyLevel

_DETECTOR_PATH = "agentic_devtools.cli.speckit.hierarchy_detector.GitHubHierarchyDetector"


class TestMainSuccess:
    """Tests for successful hierarchy detection."""

    @patch(_DETECTOR_PATH)
    def test_success_output_format(self, mock_detector_cls, capsys, monkeypatch):
        """Outputs line-oriented key=value format on success."""
        monkeypatch.setattr("sys.argv", ["prog", "--issue", "200", "--repo", "owner/repo"])

        mock_detector = MagicMock()
        mock_detector.get_parent.return_value = 100
        mock_level = MagicMock()
        mock_level.value = "feature"
        mock_detector.get_level.return_value = mock_level
        mock_detector._fetch_issue_title.return_value = "Add webhook support"
        mock_detector_cls.return_value = mock_detector

        main()

        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert lines[0] == "status=ok"
        assert lines[1] == "parent=100"
        assert lines[2] == "level=feature"
        assert lines[3] == "title=Add webhook support"

    @patch(_DETECTOR_PATH)
    def test_null_parent(self, mock_detector_cls, capsys, monkeypatch):
        """Outputs parent=null and a concrete level when no parent detected."""
        monkeypatch.setattr("sys.argv", ["prog", "--issue", "100", "--repo", "owner/repo"])

        mock_detector = MagicMock()
        mock_detector.get_parent.return_value = None
        mock_detector.get_level.return_value = HierarchyLevel.TASK
        mock_detector._fetch_issue_title.return_value = "Epic feature"
        mock_detector_cls.return_value = mock_detector

        main()

        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert lines[0] == "status=ok"
        assert lines[1] == "parent=null"
        assert lines[2] == "level=task"
        assert lines[3] == "title=Epic feature"

    @patch(_DETECTOR_PATH)
    def test_title_with_hash_normalized(self, mock_detector_cls, capsys, monkeypatch):
        """Title 'Issue #200' is normalized to 'Issue 200'."""
        monkeypatch.setattr("sys.argv", ["prog", "--issue", "200", "--repo", "owner/repo"])

        mock_detector = MagicMock()
        mock_detector.get_parent.return_value = None
        mock_detector.get_level.return_value = HierarchyLevel.TASK
        mock_detector._fetch_issue_title.return_value = "Issue #200"
        mock_detector_cls.return_value = mock_detector

        main()

        captured = capsys.readouterr()
        assert "title=Issue 200" in captured.out


class TestMainInvalidArgs:
    """Tests for argument validation errors."""

    def test_invalid_repo_format(self, capsys, monkeypatch):
        """Exits 1 with status=error when repo has no slash."""
        monkeypatch.setattr("sys.argv", ["prog", "--issue", "200", "--repo", "noslash"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "status=error" in captured.out
        assert "parent=null" in captured.out

    def test_invalid_repo_extra_slash(self, capsys, monkeypatch):
        """Exits 1 with status=error when repo has extra path segment."""
        monkeypatch.setattr("sys.argv", ["prog", "--issue", "200", "--repo", "owner/repo/extra"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "status=error" in captured.out

    def test_invalid_repo_trailing_slash(self, capsys, monkeypatch):
        """Exits 1 with status=error when repo segment is empty (trailing slash)."""
        monkeypatch.setattr("sys.argv", ["prog", "--issue", "200", "--repo", "owner/"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "status=error" in captured.out

    def test_invalid_repo_leading_slash(self, capsys, monkeypatch):
        """Exits 1 with status=error when owner segment is empty (leading slash)."""
        monkeypatch.setattr("sys.argv", ["prog", "--issue", "200", "--repo", "/repo"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "status=error" in captured.out

    def test_missing_required_args_exits_1(self, capsys, monkeypatch):
        """Exits 1 (not 2) with status=error when required args are missing."""
        monkeypatch.setattr("sys.argv", ["prog"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "status=error" in captured.out
        assert "parent=null" in captured.out

    def test_missing_repo_arg_exits_1(self, capsys, monkeypatch):
        """Exits 1 (not 2) with status=error when --repo is missing."""
        monkeypatch.setattr("sys.argv", ["prog", "--issue", "200"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "status=error" in captured.out

    def test_issue_zero_exits_1(self, capsys, monkeypatch):
        """Exits 1 with status=error when --issue 0 (not a positive integer)."""
        monkeypatch.setattr("sys.argv", ["prog", "--issue", "0", "--repo", "owner/repo"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "status=error" in captured.out
        assert "parent=null" in captured.out

    def test_issue_negative_exits_1(self, capsys, monkeypatch):
        """Exits 1 with status=error when --issue is negative."""
        monkeypatch.setattr("sys.argv", ["prog", "--issue", "-1", "--repo", "owner/repo"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "status=error" in captured.out
        assert "parent=null" in captured.out


class TestMainDetectorFailure:
    """Tests for when the detector raises an exception."""

    @patch(_DETECTOR_PATH)
    def test_exception_outputs_error(self, mock_detector_cls, capsys, monkeypatch):
        """Outputs status=error and exits 1 when detector raises."""
        monkeypatch.setattr("sys.argv", ["prog", "--issue", "200", "--repo", "owner/repo"])

        mock_detector_cls.side_effect = RuntimeError("Network error")

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "status=error" in captured.out
        assert "parent=null" in captured.out
        assert "Network error" in captured.err


class TestMainNoSigalrm:
    """Tests for platforms where SIGALRM is unavailable (e.g., Windows)."""

    @patch(_DETECTOR_PATH)
    def test_success_without_sigalrm(self, mock_detector_cls, capsys, monkeypatch):
        """Succeeds without SIGALRM (covers lines 86->90 and 106->110)."""
        monkeypatch.setattr("sys.argv", ["prog", "--issue", "200", "--repo", "owner/repo"])
        monkeypatch.delattr("signal.SIGALRM", raising=False)

        mock_detector = MagicMock()
        mock_detector.get_parent.return_value = 100
        mock_level = MagicMock()
        mock_level.value = "feature"
        mock_detector.get_level.return_value = mock_level
        mock_detector._fetch_issue_title.return_value = "Add webhook support"
        mock_detector_cls.return_value = mock_detector

        main()

        captured = capsys.readouterr()
        assert "status=ok" in captured.out
        assert "parent=100" in captured.out

    @patch(_DETECTOR_PATH)
    def test_exception_without_sigalrm(self, mock_detector_cls, capsys, monkeypatch):
        """Error path without SIGALRM (covers line 119->122)."""
        monkeypatch.setattr("sys.argv", ["prog", "--issue", "200", "--repo", "owner/repo"])
        monkeypatch.delattr("signal.SIGALRM", raising=False)

        mock_detector_cls.side_effect = RuntimeError("Network error")

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "status=error" in captured.out


class TestMainSigalrmSetupFailure:
    """Tests for SIGALRM arming failures being normalised into status=error."""

    def test_signal_signal_raises_outputs_error(self, capsys, monkeypatch):
        """If signal.signal() raises (e.g. called from non-main thread), exits 1 with status=error."""
        import signal as _signal

        monkeypatch.setattr("sys.argv", ["prog", "--issue", "200", "--repo", "owner/repo"])

        # Ensure SIGALRM appears present so the arming block is entered on all platforms
        if not hasattr(_signal, "SIGALRM"):
            monkeypatch.setattr(_signal, "SIGALRM", 14)

        def _bad_signal(signum, handler):  # noqa: ANN001
            raise OSError("signal only works in main thread")

        # signal.alarm is never reached because signal.signal raises first
        monkeypatch.setattr("signal.signal", _bad_signal)

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "status=error" in captured.out
        assert "parent=null" in captured.out
        assert "main thread" in captured.err


class TestMainCustomTimeout:
    """Tests for custom --timeout flag propagating to _timeout_secs."""

    @patch(_DETECTOR_PATH)
    def test_custom_timeout_sets_module_variable(self, mock_detector_cls, monkeypatch):
        """--timeout N updates the module-level _timeout_secs before arming SIGALRM."""
        import agentic_devtools.cli.speckit.detect_parent_cli as _mod

        # Register the current value so monkeypatch restores it after this test.
        monkeypatch.setattr(_mod, "_timeout_secs", _mod._timeout_secs)
        monkeypatch.setattr("sys.argv", ["prog", "--issue", "200", "--repo", "owner/repo", "--timeout", "30"])
        monkeypatch.delattr("signal.SIGALRM", raising=False)

        mock_detector = MagicMock()
        mock_detector.get_parent.return_value = None
        mock_detector.get_level.return_value = HierarchyLevel.TASK
        mock_detector._fetch_issue_title.return_value = "Title"
        mock_detector_cls.return_value = mock_detector

        main()

        assert _mod._timeout_secs == 30

    def test_timeout_zero_exits_1(self, capsys, monkeypatch):
        """--timeout 0 exits 1 with status=error (zero is not a positive integer)."""
        monkeypatch.setattr("sys.argv", ["prog", "--issue", "200", "--repo", "owner/repo", "--timeout", "0"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "status=error" in captured.out
        assert "parent=null" in captured.out

    def test_timeout_negative_exits_1(self, capsys, monkeypatch):
        """--timeout -5 exits 1 with status=error (negative is not a positive integer)."""
        monkeypatch.setattr("sys.argv", ["prog", "--issue", "200", "--repo", "owner/repo", "--timeout", "-5"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "status=error" in captured.out
        assert "parent=null" in captured.out

    def test_timeout_non_integer_exits_1(self, capsys, monkeypatch):
        """--timeout abc exits 1 with status=error (non-integer value)."""
        monkeypatch.setattr("sys.argv", ["prog", "--issue", "200", "--repo", "owner/repo", "--timeout", "abc"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "status=error" in captured.out
        assert "parent=null" in captured.out
