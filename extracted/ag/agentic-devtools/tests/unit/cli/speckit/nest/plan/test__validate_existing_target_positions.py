"""Tests for _validate_existing_target_positions in nest/plan.py."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.cli.speckit.nest.discovery import ChildRef
from agentic_devtools.cli.speckit.nest.plan import _validate_existing_target_positions


class TestValidateExistingTargetPositions:
    """Tests for _validate_existing_target_positions."""

    def test_passes_when_no_existing_children(self) -> None:
        """No error when no children are in existing_targets."""
        hierarchy_files = {
            "/specs/1": [ChildRef(number=2, title="Issue #2", order=0)],
        }
        existing: dict[int, Path] = {}
        _validate_existing_target_positions(hierarchy_files, existing)  # no error

    def test_passes_when_child_at_canonical_position(self) -> None:
        """No error when existing child is exactly at parent_dir/child_number."""
        parent_path = Path("/specs/1")
        hierarchy_files = {
            str(parent_path): [ChildRef(number=2, title="Issue #2", order=0)],
        }
        existing = {2: parent_path / "2"}
        _validate_existing_target_positions(hierarchy_files, existing)  # no error

    def test_raises_when_child_at_wrong_position(self) -> None:
        """ValueError raised when existing child is not under its parent directory."""
        parent_path = Path("/specs/1")
        hierarchy_files = {
            str(parent_path): [ChildRef(number=2, title="Issue #2", order=0)],
        }
        # child 2 is at the flat root, not under parent 1
        existing = {2: Path("/specs/2")}
        with pytest.raises(ValueError, match="Existing target #2 is at"):
            _validate_existing_target_positions(hierarchy_files, existing)

    def test_error_message_names_expected_and_actual_paths(self) -> None:
        """Error message includes both the actual and expected paths."""
        parent_path = Path("/specs/1")
        hierarchy_files = {
            str(parent_path): [ChildRef(number=2, title="Issue #2", order=0)],
        }
        existing = {2: Path("/specs/2")}
        with pytest.raises(ValueError) as exc_info:
            _validate_existing_target_positions(hierarchy_files, existing)
        msg = str(exc_info.value)
        assert "/specs/2" in msg
        assert "/specs/1/2" in msg

    def test_passes_with_multiple_children_all_canonical(self) -> None:
        """No error when multiple existing children are all correctly nested."""
        parent_path = Path("/specs/1")
        hierarchy_files = {
            str(parent_path): [
                ChildRef(number=2, title="Issue #2", order=0),
                ChildRef(number=3, title="Issue #3", order=1),
            ],
        }
        existing = {
            2: parent_path / "2",
            3: parent_path / "3",
        }
        _validate_existing_target_positions(hierarchy_files, existing)  # no error

    def test_raises_on_first_mismatch_among_multiple_children(self) -> None:
        """Raises as soon as a misplaced child is encountered."""
        parent_path = Path("/specs/1")
        hierarchy_files = {
            str(parent_path): [
                ChildRef(number=2, title="Issue #2", order=0),
                ChildRef(number=3, title="Issue #3", order=1),
            ],
        }
        existing = {
            2: parent_path / "2",  # correct
            3: Path("/specs/3"),  # wrong — should be /specs/1/3
        }
        with pytest.raises(ValueError, match="Existing target #3 is at"):
            _validate_existing_target_positions(hierarchy_files, existing)

    def test_passes_when_hierarchy_files_empty(self) -> None:
        """No error when there are no hierarchy files to validate."""
        _validate_existing_target_positions({}, {1: Path("/specs/1")})  # no error
