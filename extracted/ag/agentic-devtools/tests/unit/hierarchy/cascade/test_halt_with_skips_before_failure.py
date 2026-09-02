"""Tests for halt-on-failure with preceding skips (FR-004 + FR-005 combined)."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.hierarchy.cascade import CascadeAction, CascadeProcessor


class TestHaltWithSkipsBeforeFailure:
    """Tests that skip comment is posted before halt comment when both conditions apply."""

    def test_trigger_first_child_skips_then_halts(self, tmp_path: Path) -> None:
        """Epic cascade: skip #101 (speckit:skip) then halt on #102 (speckit:failed)."""
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text(
            "level: epic\n"
            "parent: null\n"
            "children:\n"
            "  - number: 101\n"
            "    title: Skipped Feature\n"
            "    order: 1\n"
            "  - number: 102\n"
            "    title: Failed Feature\n"
            "    order: 2\n"
            "  - number: 103\n"
            "    title: Good Feature\n"
            "    order: 3\n"
            "informational_children: []\n"
        )

        processor = CascadeProcessor(owner="org", repo="repo")

        def mock_state(issue_number: int) -> dict:
            if issue_number == 101:
                return {"state": "open", "labels": [{"name": "speckit:skip"}]}
            if issue_number == 102:
                return {"state": "open", "labels": [{"name": "speckit:failed"}]}
            return {"state": "open", "labels": []}

        posted_comments: list[tuple[int, str]] = []

        def mock_post(issue: int, body: str) -> bool:
            posted_comments.append((issue, body))
            return True

        with (
            patch.object(processor, "_get_issue_state", side_effect=mock_state),
            patch.object(processor, "_apply_label") as mock_label,
            patch.object(processor, "_post_comment", side_effect=mock_post),
        ):
            result = processor.trigger_first_child(100, yml_path)

        assert result.action == CascadeAction.HALTED
        assert result.skipped_issues == [101]
        # Two comments posted: skip notice then halt
        assert len(posted_comments) == 2
        assert "Skip Notice" in posted_comments[0][1]
        assert "#101" in posted_comments[0][1]
        assert "halted" in posted_comments[1][1].lower()
        mock_label.assert_not_called()

    def test_trigger_next_sibling_skips_then_halts(self, tmp_path: Path) -> None:
        """Sibling cascade: skip #202 (speckit:skip) then halt on #203 (speckit:failed)."""
        yml_path = tmp_path / "hierarchy.yml"
        yml_path.write_text(
            "level: feature\n"
            "parent: 50\n"
            "children:\n"
            "  - number: 201\n"
            "    title: Completed Task\n"
            "    order: 1\n"
            "  - number: 202\n"
            "    title: Skipped Task\n"
            "    order: 2\n"
            "  - number: 203\n"
            "    title: Failed Task\n"
            "    order: 3\n"
            "  - number: 204\n"
            "    title: Good Task\n"
            "    order: 4\n"
            "informational_children: []\n"
        )

        processor = CascadeProcessor(owner="org", repo="repo")

        def mock_state(issue_number: int) -> dict:
            if issue_number == 202:
                return {"state": "open", "labels": [{"name": "speckit:skip"}]}
            if issue_number == 203:
                return {"state": "open", "labels": [{"name": "speckit:failed"}]}
            return {"state": "open", "labels": []}

        posted_comments: list[tuple[int, str]] = []

        def mock_post(issue: int, body: str) -> bool:
            posted_comments.append((issue, body))
            return True

        with (
            patch.object(processor, "_get_issue_state", side_effect=mock_state),
            patch.object(processor, "_apply_label") as mock_label,
            patch.object(processor, "_post_comment", side_effect=mock_post),
        ):
            result = processor.trigger_next_sibling(201, yml_path)

        assert result.action == CascadeAction.HALTED
        assert result.skipped_issues == [202]
        # Three comments: skip notice to completed child, halt to completed child,
        # halt also to parent (issue 50 from metadata.parent) so the parent is notified.
        assert len(posted_comments) == 3
        assert "Skip Notice" in posted_comments[0][1]
        assert "#202" in posted_comments[0][1]
        assert posted_comments[0][0] == 201
        assert "halted" in posted_comments[1][1].lower()
        assert posted_comments[1][0] == 201
        assert "halted" in posted_comments[2][1].lower()
        assert posted_comments[2][0] == 50
        mock_label.assert_not_called()
