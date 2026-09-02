"""Tests that cascade halts on non-404 API errors instead of silently skipping."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.hierarchy.cascade import CascadeAction, CascadeProcessor, IssueStateError


class TestHaltOnApiError:
    """IssueStateError from _get_issue_state must halt the cascade."""

    def _write_two_child_yml(self, tmp_path: Path) -> Path:
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text(
            "level: epic\n"
            "parent: null\n"
            "children:\n"
            "  - number: 101\n"
            "    title: First Child\n"
            "    order: 1\n"
            "  - number: 102\n"
            "    title: Second Child\n"
            "    order: 2\n"
            "informational_children: []\n"
        )
        return yml_path

    def test_trigger_first_child_halts_on_api_error(self, tmp_path: Path) -> None:
        """When _get_issue_state raises IssueStateError, trigger_first_child returns HALTED."""
        yml_path = self._write_two_child_yml(tmp_path)
        processor = CascadeProcessor(owner="org", repo="repo")

        with (
            patch.object(processor, "_get_issue_state", side_effect=IssueStateError("502 Bad Gateway")),
            patch.object(processor, "_post_comment") as mock_comment,
        ):
            mock_comment.return_value = True
            result = processor.trigger_first_child(100, yml_path)

        assert result.action == CascadeAction.HALTED
        assert "Could not retrieve issue state" in result.comment
        assert "502 Bad Gateway" in result.comment
        mock_comment.assert_called_once()

    def test_trigger_next_sibling_halts_on_api_error(self, tmp_path: Path) -> None:
        """When _get_issue_state raises IssueStateError, trigger_next_sibling returns HALTED."""
        # Write the parent's hierarchy.yml (containing two children: 101 and 102)
        parent_dir = tmp_path / "10"
        parent_dir.mkdir()
        yml_path = parent_dir / "hierarchy.yml"
        yml_path.write_text(
            "level: epic\n"
            "parent: null\n"
            "children:\n"
            "  - number: 101\n"
            "    title: First Child\n"
            "    order: 1\n"
            "  - number: 102\n"
            "    title: Second Child\n"
            "    order: 2\n"
            "informational_children: []\n"
        )
        processor = CascadeProcessor(owner="org", repo="repo")

        with (
            patch.object(processor, "_get_issue_state", side_effect=IssueStateError("auth failure")),
            patch.object(processor, "_post_comment") as mock_comment,
        ):
            mock_comment.return_value = True
            # completed_child=101; should try to fetch 102 and hit the error
            result = processor.trigger_next_sibling(101, yml_path)

        assert result.action == CascadeAction.HALTED
        assert "Could not retrieve issue state" in result.comment
        assert "auth failure" in result.comment
        mock_comment.assert_called_once()

    def test_first_child_deleted_second_child_api_error_halts(self, tmp_path: Path) -> None:
        """404 for first child is skipped; API error on second child halts (not skipped)."""
        yml_path = self._write_two_child_yml(tmp_path)
        processor = CascadeProcessor(owner="org", repo="repo")

        call_count = 0

        def side_effect_404_then_api_error(issue_number: int) -> dict | None:
            nonlocal call_count
            call_count += 1
            if issue_number == 101:
                return None  # 404 — skip
            raise IssueStateError("transient error")

        with (
            patch.object(processor, "_get_issue_state", side_effect=side_effect_404_then_api_error),
            patch.object(processor, "_post_comment") as mock_comment,
        ):
            mock_comment.return_value = True
            result = processor.trigger_first_child(100, yml_path)

        assert result.action == CascadeAction.HALTED
        assert "transient error" in result.comment
        # Both children were inspected
        assert call_count == 2
