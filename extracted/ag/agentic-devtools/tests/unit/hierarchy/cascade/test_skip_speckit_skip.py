"""Tests for speckit:skip label skip logic."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.hierarchy.cascade import CascadeAction, CascadeProcessor


class TestSkipSpeckitSkip:
    """Tests that issues with speckit:skip label are skipped."""

    def test_skips_skip_labeled_child(self, tmp_path: Path) -> None:
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text(
            "level: epic\n"
            "parent: null\n"
            "children:\n"
            "  - number: 101\n"
            "    title: Skip Me\n"
            "    order: 1\n"
            "  - number: 102\n"
            "    title: Process Me\n"
            "    order: 2\n"
            "informational_children: []\n"
        )

        processor = CascadeProcessor(owner="org", repo="repo")

        def mock_state(issue_number: int) -> dict:
            if issue_number == 101:
                return {"state": "open", "labels": [{"name": "speckit:skip"}]}
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
