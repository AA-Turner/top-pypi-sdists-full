"""Tests for cascade_trigger_command CLI entry point."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.hierarchy.cascade import (
    CascadeAction,
    CascadeApiRetryExhaustedError,
    CascadeResult,
)
from agentic_devtools.hierarchy.models import CascadeDirection, CascadeEvent


class TestCascadeTriggerCommand:
    """Tests for agdt-cascade-trigger CLI command."""

    def test_first_child_mode(self, tmp_path: Path, capsys) -> None:
        from agentic_devtools.cli.hierarchy.commands import cascade_trigger_command

        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text("level: epic\nparent: null\nchildren: []\n")

        mock_result = CascadeResult(
            action=CascadeAction.TRIGGERED,
            event=CascadeEvent(
                source_issue=100,
                target_issue=101,
                direction=CascadeDirection.PARENT_TO_CHILD,
            ),
            comment="Triggered",
        )

        with (
            patch(
                "sys.argv",
                [
                    "cmd",
                    "--issue",
                    "100",
                    "--owner",
                    "org",
                    "--repo",
                    "repo",
                    "--hierarchy-yml",
                    str(yml_path),
                    "--mode",
                    "first-child",
                ],
            ),
            patch("agentic_devtools.cli.hierarchy.commands.CascadeProcessor") as mock_cls,
        ):
            mock_processor = MagicMock()
            mock_processor.trigger_first_child.return_value = mock_result
            mock_cls.return_value = mock_processor

            cascade_trigger_command()

        captured = capsys.readouterr()
        assert '"action": "triggered"' in captured.out
        assert '"target_issue": 101' in captured.out

    def test_next_sibling_mode(self, tmp_path: Path, capsys) -> None:
        from agentic_devtools.cli.hierarchy.commands import cascade_trigger_command

        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text("level: epic\nparent: null\nchildren: []\n")

        mock_result = CascadeResult(
            action=CascadeAction.CASCADE_COMPLETE,
            comment="All done",
        )

        with (
            patch(
                "sys.argv",
                [
                    "cmd",
                    "--issue",
                    "101",
                    "--owner",
                    "org",
                    "--repo",
                    "repo",
                    "--hierarchy-yml",
                    str(yml_path),
                    "--mode",
                    "next-sibling",
                ],
            ),
            patch("agentic_devtools.cli.hierarchy.commands.CascadeProcessor") as mock_cls,
        ):
            mock_processor = MagicMock()
            mock_processor.trigger_next_sibling.return_value = mock_result
            mock_cls.return_value = mock_processor

            cascade_trigger_command()

        captured = capsys.readouterr()
        assert '"action": "cascade_complete"' in captured.out

    def test_pipeline_failed_rejected_for_first_child_mode(self, tmp_path: Path, capsys) -> None:
        from agentic_devtools.cli.hierarchy.commands import cascade_trigger_command

        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text("level: epic\nparent: null\nchildren: []\n")

        with patch(
            "sys.argv",
            [
                "cmd",
                "--issue",
                "100",
                "--owner",
                "org",
                "--repo",
                "repo",
                "--hierarchy-yml",
                str(yml_path),
                "--mode",
                "first-child",
                "--pipeline-failed",
            ],
        ):
            with pytest.raises(SystemExit) as exc_info:
                cascade_trigger_command()

        assert exc_info.value.code == 2
        captured = capsys.readouterr()
        assert "--pipeline-failed is only valid with --mode next-sibling" in captured.err

    def test_retry_exhaustion_exits_non_zero(self, tmp_path: Path, capsys) -> None:
        from agentic_devtools.cli.hierarchy.commands import cascade_trigger_command

        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text("level: epic\nparent: null\nchildren: []\n")

        with (
            patch(
                "sys.argv",
                [
                    "cmd",
                    "--issue",
                    "100",
                    "--owner",
                    "org",
                    "--repo",
                    "repo",
                    "--hierarchy-yml",
                    str(yml_path),
                    "--mode",
                    "first-child",
                ],
            ),
            patch("agentic_devtools.cli.hierarchy.commands.CascadeProcessor") as mock_cls,
            pytest.raises(SystemExit) as exc_info,
        ):
            mock_processor = MagicMock()
            mock_processor.trigger_first_child.side_effect = CascadeApiRetryExhaustedError("boom")
            mock_cls.return_value = mock_processor
            cascade_trigger_command()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Retry exhausted" in captured.err or "boom" in captured.err
