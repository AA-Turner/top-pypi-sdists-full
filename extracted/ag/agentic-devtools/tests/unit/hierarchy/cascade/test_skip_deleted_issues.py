"""Tests for deleted issue (404) skip logic."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.hierarchy.cascade import CascadeAction, CascadeProcessor


class TestSkipDeletedIssues:
    """Tests that deleted issues (404) are skipped."""

    def test_skips_deleted_child(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text(
            "level: epic\n"
            "parent: null\n"
            "children:\n"
            "  - number: 101\n"
            "    title: Deleted Issue\n"
            "    order: 1\n"
            "  - number: 102\n"
            "    title: Existing Issue\n"
            "    order: 2\n"
            "informational_children: []\n"
        )

        processor = CascadeProcessor(owner="org", repo="repo")

        def mock_state(issue_number: int) -> dict | None:
            if issue_number == 101:
                return None  # 404
            return {"state": "open", "labels": []}

        with (
            patch.object(processor, "_get_issue_state", side_effect=mock_state),
            patch.object(processor, "_apply_label") as mock_label,
            patch.object(processor, "_post_comment") as mock_comment,
        ):
            mock_label.return_value = True
            mock_comment.return_value = True
            result = processor.trigger_first_child(100, yml_path)

        assert result.action == CascadeAction.TRIGGERED
        assert result.event is not None
        assert result.event.target_issue == 102
        assert 101 in result.skipped_issues
