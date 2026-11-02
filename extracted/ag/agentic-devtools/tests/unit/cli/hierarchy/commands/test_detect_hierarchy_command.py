"""Tests for detect_hierarchy_command CLI entry point."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.hierarchy.models import ChildInfo, HierarchyLevel, HierarchyMetadata


class TestDetectHierarchyCommand:
    """Tests for agdt-detect-hierarchy CLI command."""

    def test_detects_and_outputs_json(self, tmp_path, capsys) -> None:
        from agentic_devtools.cli.hierarchy.commands import detect_hierarchy_command

        mock_meta = HierarchyMetadata(
            level=HierarchyLevel.EPIC,
            children=[ChildInfo(number=101, title="Feature A")],
        )

        with (
            patch(
                "sys.argv",
                ["cmd", "--issue", "100", "--owner", "org", "--repo", "repo", "--specs-root", str(tmp_path / "specs")],
            ),
            patch("agentic_devtools.cli.hierarchy.commands.GitHubHierarchyDetector") as mock_cls,
            patch("agentic_devtools.cli.hierarchy.commands.write_hierarchy_yml") as mock_write,
        ):
            mock_detector = MagicMock()
            mock_detector.build_metadata.return_value = mock_meta
            mock_cls.return_value = mock_detector
            mock_write.return_value = True

            detect_hierarchy_command()

        captured = capsys.readouterr()
        assert '"level": "epic"' in captured.out
        assert '"issue": 100' in captured.out

    def test_passes_ancestor_chain_to_path_resolution(self, tmp_path) -> None:
        from agentic_devtools.cli.hierarchy.commands import detect_hierarchy_command

        mock_meta = HierarchyMetadata(
            level=HierarchyLevel.TASK,
            parent=101,
        )
        resolved_path = tmp_path / "specs" / "100" / "101" / "110"

        with (
            patch(
                "sys.argv",
                ["cmd", "--issue", "110", "--owner", "org", "--repo", "repo", "--specs-root", str(tmp_path / "specs")],
            ),
            patch("agentic_devtools.cli.hierarchy.commands.GitHubHierarchyDetector") as mock_cls,
            patch(
                "agentic_devtools.cli.hierarchy.commands.resolve_spec_path",
                return_value=resolved_path,
            ) as mock_resolve,
            patch("agentic_devtools.cli.hierarchy.commands.write_hierarchy_yml", return_value=True),
        ):
            mock_detector = MagicMock()
            mock_detector.build_metadata.return_value = mock_meta
            mock_detector.detect_parent.side_effect = [101, 100, None]
            mock_cls.return_value = mock_detector

            detect_hierarchy_command()

        mock_resolve.assert_called_once_with(
            110,
            mock_meta,
            tmp_path / "specs",
            ancestors=[100, 101],
        )

    def test_standalone_does_not_create_spec_dir(self, tmp_path, capsys) -> None:
        from agentic_devtools.cli.hierarchy.commands import detect_hierarchy_command

        mock_meta = HierarchyMetadata(level=HierarchyLevel.STANDALONE)
        specs_root = tmp_path / "specs"

        with (
            patch(
                "sys.argv",
                ["cmd", "--issue", "42", "--owner", "org", "--repo", "repo", "--specs-root", str(specs_root)],
            ),
            patch("agentic_devtools.cli.hierarchy.commands.GitHubHierarchyDetector") as mock_cls,
        ):
            mock_detector = MagicMock()
            mock_detector.build_metadata.return_value = mock_meta
            mock_detector.detect_parent.return_value = None
            mock_cls.return_value = mock_detector

            detect_hierarchy_command()

        captured = capsys.readouterr()
        assert '"hierarchy_yml_written": false' in captured.out
        # The spec dir must NOT have been created on disk
        assert not any(specs_root.rglob("*")) if specs_root.exists() else True

    def test_exits_with_error_when_owner_repo_cannot_be_resolved(self) -> None:
        from agentic_devtools.cli.hierarchy.commands import detect_hierarchy_command

        with (
            patch("sys.argv", ["cmd", "--issue", "100"]),
            patch(
                "agentic_devtools.cli.hierarchy.commands.resolve_owner_repo", side_effect=ValueError("Cannot resolve")
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            detect_hierarchy_command()

        assert exc_info.value.code == 1

    def test_skips_mkdir_and_write_when_enforcement_rejects(self, tmp_path, capsys) -> None:
        """Enforcement check runs before mkdir; a rejected child must not create directories."""
        from agentic_devtools.cli.hierarchy.commands import detect_hierarchy_command
        from agentic_devtools.hierarchy.enforcement import EnforcementAction, EnforcementResult

        mock_meta = HierarchyMetadata(
            level=HierarchyLevel.FEATURE,
            parent=10,
        )
        specs_root = tmp_path / "specs"
        resolved_path = specs_root / "10" / "101"

        rejected = EnforcementResult(
            action=EnforcementAction.REJECT,
            reason="Parent #10 has not been specked yet.",
            parent_issue=10,
        )

        with (
            patch(
                "sys.argv",
                ["cmd", "--issue", "101", "--owner", "org", "--repo", "repo", "--specs-root", str(specs_root)],
            ),
            patch("agentic_devtools.cli.hierarchy.commands.GitHubHierarchyDetector") as mock_cls,
            patch(
                "agentic_devtools.cli.hierarchy.commands.resolve_spec_path",
                return_value=resolved_path,
            ),
            patch(
                "agentic_devtools.cli.hierarchy.commands.enforce_parent_specked",
                return_value=rejected,
            ) as mock_enforce,
            patch("agentic_devtools.cli.hierarchy.commands.write_hierarchy_yml") as mock_write,
        ):
            mock_detector = MagicMock()
            mock_detector.build_metadata.return_value = mock_meta
            mock_detector.detect_parent.return_value = None
            mock_cls.return_value = mock_detector

            detect_hierarchy_command()

        # Directory must NOT be created on disk (neither the target nor its parent)
        assert not resolved_path.exists()
        assert not (specs_root / "10").exists()
        # write_hierarchy_yml must NOT be called
        mock_write.assert_not_called()
        # enforce_parent_specked must have been called
        mock_enforce.assert_called_once()
        # JSON output must reflect the rejection
        captured = capsys.readouterr()
        assert '"hierarchy_yml_written": false' in captured.out
        assert '"enforcement_rejected": true' in captured.out
