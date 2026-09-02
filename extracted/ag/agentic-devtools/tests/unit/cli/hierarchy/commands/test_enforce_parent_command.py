"""Tests for enforce_parent_command CLI entry point."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.hierarchy.enforcement import EnforcementAction, EnforcementResult
from agentic_devtools.hierarchy.models import HierarchyLevel, HierarchyMetadata


class TestEnforceParentCommand:
    """Tests for agdt-enforce-parent CLI command."""

    def test_allows_when_parent_specked(self, tmp_path, capsys) -> None:
        from agentic_devtools.cli.hierarchy.commands import enforce_parent_command

        mock_meta = HierarchyMetadata(level=HierarchyLevel.STANDALONE)

        with (
            patch(
                "sys.argv",
                ["cmd", "--issue", "100", "--owner", "org", "--repo", "repo", "--specs-root", str(tmp_path / "specs")],
            ),
            patch("agentic_devtools.cli.hierarchy.commands.GitHubHierarchyDetector") as mock_cls,
            patch("agentic_devtools.cli.hierarchy.commands.enforce_parent_specked") as mock_enforce,
        ):
            mock_detector = MagicMock()
            mock_detector.build_metadata.return_value = mock_meta
            mock_cls.return_value = mock_detector
            mock_enforce.return_value = EnforcementResult(
                action=EnforcementAction.ALLOW,
                reason="Standalone issue",
            )

            enforce_parent_command()

        captured = capsys.readouterr()
        assert '"action": "allow"' in captured.out

    def test_exits_1_on_rejection(self, tmp_path, capsys) -> None:
        from agentic_devtools.cli.hierarchy.commands import enforce_parent_command

        mock_meta = HierarchyMetadata(level=HierarchyLevel.FEATURE, parent=100)

        with (
            patch(
                "sys.argv",
                ["cmd", "--issue", "101", "--owner", "org", "--repo", "repo", "--specs-root", str(tmp_path / "specs")],
            ),
            patch("agentic_devtools.cli.hierarchy.commands.GitHubHierarchyDetector") as mock_cls,
            patch("agentic_devtools.cli.hierarchy.commands.enforce_parent_specked") as mock_enforce,
            pytest.raises(SystemExit) as exc_info,
        ):
            mock_detector = MagicMock()
            mock_detector.build_metadata.return_value = mock_meta
            mock_cls.return_value = mock_detector
            mock_enforce.return_value = EnforcementResult(
                action=EnforcementAction.REJECT,
                reason="Parent not specked",
                parent_issue=100,
            )

            enforce_parent_command()

        assert exc_info.value.code == 1

    def test_passes_parent_ancestor_chain(self, tmp_path) -> None:
        from agentic_devtools.cli.hierarchy.commands import enforce_parent_command

        mock_meta = HierarchyMetadata(level=HierarchyLevel.TASK, parent=101)

        with (
            patch(
                "sys.argv",
                ["cmd", "--issue", "110", "--owner", "org", "--repo", "repo", "--specs-root", str(tmp_path / "specs")],
            ),
            patch("agentic_devtools.cli.hierarchy.commands.GitHubHierarchyDetector") as mock_cls,
            patch("agentic_devtools.cli.hierarchy.commands.enforce_parent_specked") as mock_enforce,
        ):
            mock_detector = MagicMock()
            mock_detector.build_metadata.return_value = mock_meta
            mock_detector.detect_parent.side_effect = [101, 100, None]
            mock_cls.return_value = mock_detector
            mock_enforce.return_value = EnforcementResult(
                action=EnforcementAction.ALLOW,
                reason="Parent specked",
                parent_issue=101,
            )

            enforce_parent_command()

        mock_enforce.assert_called_once_with(
            110,
            mock_meta,
            tmp_path / "specs",
            ancestors=[100],
        )

    def test_rejection_posts_comment_and_removes_label(self, tmp_path) -> None:
        from agentic_devtools.cli.hierarchy.commands import enforce_parent_command

        mock_meta = HierarchyMetadata(level=HierarchyLevel.FEATURE, parent=100)
        success = MagicMock(returncode=0, stdout="", stderr="")

        with (
            patch(
                "sys.argv",
                ["cmd", "--issue", "101", "--owner", "org", "--repo", "repo", "--specs-root", str(tmp_path / "specs")],
            ),
            patch("agentic_devtools.cli.hierarchy.commands.GitHubHierarchyDetector") as mock_cls,
            patch("agentic_devtools.cli.hierarchy.commands.enforce_parent_specked") as mock_enforce,
            patch("agentic_devtools.cli.hierarchy.commands.run_safe", side_effect=[success, success]) as mock_run_safe,
            pytest.raises(SystemExit),
        ):
            mock_detector = MagicMock()
            mock_detector.build_metadata.return_value = mock_meta
            mock_detector.detect_parent.side_effect = [100, None]
            mock_cls.return_value = mock_detector
            mock_enforce.return_value = EnforcementResult(
                action=EnforcementAction.REJECT,
                reason="Parent not specked",
                parent_issue=100,
            )

            enforce_parent_command()

        assert mock_run_safe.call_count == 2
        comment_call = mock_run_safe.call_args_list[0]
        remove_label_call = mock_run_safe.call_args_list[1]
        assert comment_call.args[0][:4] == ["gh", "issue", "comment", "101"]
        assert "--body" in comment_call.args[0]
        assert remove_label_call.args[0][:4] == ["gh", "issue", "edit", "101"]
        assert "--remove-label" in remove_label_call.args[0]

    def test_rejection_warns_on_comment_failure(self, tmp_path, capsys) -> None:
        from agentic_devtools.cli.hierarchy.commands import enforce_parent_command

        mock_meta = HierarchyMetadata(level=HierarchyLevel.FEATURE, parent=100)
        failure = MagicMock(returncode=1, stdout="", stderr="auth error")
        success = MagicMock(returncode=0, stdout="", stderr="")

        with (
            patch(
                "sys.argv",
                ["cmd", "--issue", "101", "--owner", "org", "--repo", "repo", "--specs-root", str(tmp_path / "specs")],
            ),
            patch("agentic_devtools.cli.hierarchy.commands.GitHubHierarchyDetector") as mock_cls,
            patch("agentic_devtools.cli.hierarchy.commands.enforce_parent_specked") as mock_enforce,
            patch("agentic_devtools.cli.hierarchy.commands.run_safe", side_effect=[failure, success]),
            pytest.raises(SystemExit) as exc_info,
        ):
            mock_detector = MagicMock()
            mock_detector.build_metadata.return_value = mock_meta
            mock_detector.detect_parent.side_effect = [100, None]
            mock_cls.return_value = mock_detector
            mock_enforce.return_value = EnforcementResult(
                action=EnforcementAction.REJECT,
                reason="Parent not specked",
                parent_issue=100,
            )

            enforce_parent_command()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Warning" in captured.err
        assert "rejection comment" in captured.err

    def test_rejection_warns_on_label_removal_failure(self, tmp_path, capsys) -> None:
        from agentic_devtools.cli.hierarchy.commands import enforce_parent_command

        mock_meta = HierarchyMetadata(level=HierarchyLevel.FEATURE, parent=100)
        success = MagicMock(returncode=0, stdout="", stderr="")
        failure = MagicMock(returncode=1, stdout="", stderr="label error")

        with (
            patch(
                "sys.argv",
                ["cmd", "--issue", "101", "--owner", "org", "--repo", "repo", "--specs-root", str(tmp_path / "specs")],
            ),
            patch("agentic_devtools.cli.hierarchy.commands.GitHubHierarchyDetector") as mock_cls,
            patch("agentic_devtools.cli.hierarchy.commands.enforce_parent_specked") as mock_enforce,
            patch("agentic_devtools.cli.hierarchy.commands.run_safe", side_effect=[success, failure]),
            pytest.raises(SystemExit) as exc_info,
        ):
            mock_detector = MagicMock()
            mock_detector.build_metadata.return_value = mock_meta
            mock_detector.detect_parent.side_effect = [100, None]
            mock_cls.return_value = mock_detector
            mock_enforce.return_value = EnforcementResult(
                action=EnforcementAction.REJECT,
                reason="Parent not specked",
                parent_issue=100,
            )

            enforce_parent_command()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Warning" in captured.err
        assert "speckit" in captured.err

    def test_rejection_warns_when_comment_command_missing(self, tmp_path, capsys) -> None:
        from agentic_devtools.cli.hierarchy.commands import enforce_parent_command

        mock_meta = HierarchyMetadata(level=HierarchyLevel.FEATURE, parent=100)
        success = MagicMock(returncode=0, stdout="", stderr="")

        with (
            patch(
                "sys.argv",
                ["cmd", "--issue", "101", "--owner", "org", "--repo", "repo", "--specs-root", str(tmp_path / "specs")],
            ),
            patch("agentic_devtools.cli.hierarchy.commands.GitHubHierarchyDetector") as mock_cls,
            patch("agentic_devtools.cli.hierarchy.commands.enforce_parent_specked") as mock_enforce,
            patch("agentic_devtools.cli.hierarchy.commands.run_safe", side_effect=[FileNotFoundError("gh"), success]),
            pytest.raises(SystemExit) as exc_info,
        ):
            mock_detector = MagicMock()
            mock_detector.build_metadata.return_value = mock_meta
            mock_detector.detect_parent.side_effect = [100, None]
            mock_cls.return_value = mock_detector
            mock_enforce.return_value = EnforcementResult(
                action=EnforcementAction.REJECT,
                reason="Parent not specked",
                parent_issue=100,
            )

            enforce_parent_command()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "failed to post rejection comment" in captured.err

    def test_rejection_warns_when_label_command_missing(self, tmp_path, capsys) -> None:
        from agentic_devtools.cli.hierarchy.commands import enforce_parent_command

        mock_meta = HierarchyMetadata(level=HierarchyLevel.FEATURE, parent=100)
        success = MagicMock(returncode=0, stdout="", stderr="")

        with (
            patch(
                "sys.argv",
                ["cmd", "--issue", "101", "--owner", "org", "--repo", "repo", "--specs-root", str(tmp_path / "specs")],
            ),
            patch("agentic_devtools.cli.hierarchy.commands.GitHubHierarchyDetector") as mock_cls,
            patch("agentic_devtools.cli.hierarchy.commands.enforce_parent_specked") as mock_enforce,
            patch("agentic_devtools.cli.hierarchy.commands.run_safe", side_effect=[success, FileNotFoundError("gh")]),
            pytest.raises(SystemExit) as exc_info,
        ):
            mock_detector = MagicMock()
            mock_detector.build_metadata.return_value = mock_meta
            mock_detector.detect_parent.side_effect = [100, None]
            mock_cls.return_value = mock_detector
            mock_enforce.return_value = EnforcementResult(
                action=EnforcementAction.REJECT,
                reason="Parent not specked",
                parent_issue=100,
            )

            enforce_parent_command()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "failed to remove 'speckit' label" in captured.err
