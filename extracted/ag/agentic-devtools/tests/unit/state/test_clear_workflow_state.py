"""Tests for agentic_devtools.state.clear_workflow_state."""

import json
from unittest.mock import MagicMock, patch

from agentic_devtools import state
from agentic_devtools.state import PIN_FILENAME


def test_clear_workflow_state(temp_state_dir):
    """Test clearing workflow state."""
    state.set_workflow_state(name="test-workflow", status="in-progress")
    assert state.get_workflow_state() is not None

    state.clear_workflow_state()
    assert state.get_workflow_state() is None


def test_clear_workflow_state_force_delete_removes_hierarchy_retention(temp_state_dir):
    """force_delete=True removes retained hierarchy traces with the workflow."""
    registry = temp_state_dir / "orchestration" / "hierarchy" / "retention-registry.ndjson"
    trace = temp_state_dir / "orchestration" / "hierarchy" / "run-1" / "trace.ndjson"
    trace.parent.mkdir(parents=True)
    trace.write_text("encrypted", encoding="utf-8")
    registry.write_text(
        json.dumps(
            {
                "run_id": "run-1",
                "trace_path": str(trace),
                "expires_at": "2099-01-01T00:00:00+00:00",
                "timestamp": "2026-01-01T00:00:00+00:00",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    mock_storage = MagicMock()
    mock_storage.delete.side_effect = lambda: trace.unlink() or True
    with (
        patch("agentic_devtools.orchestration.hierarchy.aggregation.resolve_master_key", return_value=b"x" * 32),
        patch(
            "agentic_devtools.orchestration.hierarchy.aggregation.resolve_authorized_principals",
            return_value=frozenset({"test-principal"}),
        ),
        patch("agentic_devtools.orchestration.hierarchy.aggregation.ProtectedStorage", return_value=mock_storage),
    ):
        state.clear_workflow_state(force_delete=True)

    assert not trace.exists()
    assert not registry.exists()


class TestClearWorkflowStatePinCleanup:
    """Tests for pin file cleanup during clear_workflow_state."""

    def test_force_delete_unconditionally_deletes_pin(self, tmp_path, temp_state_dir):
        """force_delete=True deletes pin file regardless of workflow field."""
        agdt_dir = tmp_path / ".agdt"
        agdt_dir.mkdir(parents=True)
        pin_path = agdt_dir / PIN_FILENAME
        pin_path.write_text(
            json.dumps({"state_dir": "/tmp", "workflow": "other-workflow", "created_utc": "x", "ttl_hours": 24}),
            encoding="utf-8",
        )

        state.set_workflow_state(name="test", status="active")
        with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
            state.clear_workflow_state(force_delete=True)

        assert not pin_path.exists()

    def test_completing_workflow_deletes_matching_pin(self, tmp_path, temp_state_dir):
        """completing_workflow deletes pin only when workflow field matches."""
        agdt_dir = tmp_path / ".agdt"
        agdt_dir.mkdir(parents=True)
        pin_path = agdt_dir / PIN_FILENAME
        pin_path.write_text(
            json.dumps({"state_dir": "/tmp", "workflow": "pull-request-review", "created_utc": "x", "ttl_hours": 24}),
            encoding="utf-8",
        )

        state.set_workflow_state(name="test", status="active")
        with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
            state.clear_workflow_state(completing_workflow="pull-request-review")

        assert not pin_path.exists()

    def test_completing_workflow_preserves_non_matching_pin(self, tmp_path, temp_state_dir):
        """completing_workflow preserves pin when workflow field doesn't match."""
        agdt_dir = tmp_path / ".agdt"
        agdt_dir.mkdir(parents=True)
        pin_path = agdt_dir / PIN_FILENAME
        pin_path.write_text(
            json.dumps({"state_dir": "/tmp", "workflow": "pull-request-review", "created_utc": "x", "ttl_hours": 24}),
            encoding="utf-8",
        )

        state.set_workflow_state(name="test", status="active")
        with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
            state.clear_workflow_state(completing_workflow="other-workflow")

        assert pin_path.exists()

    def test_completing_workflow_without_pin_file(self, tmp_path, temp_state_dir):
        """Conditional pin cleanup no-ops when pin file does not exist."""
        state.set_workflow_state(name="test", status="active")
        with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
            state.clear_workflow_state(completing_workflow="pull-request-review")
        assert state.get_workflow_state() is None

    def test_no_pin_cleanup_when_no_flags(self, tmp_path, temp_state_dir):
        """Default call (no flags) does not delete pin file."""
        agdt_dir = tmp_path / ".agdt"
        agdt_dir.mkdir(parents=True)
        pin_path = agdt_dir / PIN_FILENAME
        pin_path.write_text(json.dumps({"workflow": "pull-request-review"}), encoding="utf-8")

        state.set_workflow_state(name="test", status="active")
        with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
            state.clear_workflow_state()

        assert pin_path.exists()

    def test_pin_cleanup_ignores_read_exceptions_on_conditional_delete(self, tmp_path, temp_state_dir):
        """Ignores OSError, ValueError, and JSONDecodeError on conditional delete."""
        agdt_dir = tmp_path / ".agdt"
        agdt_dir.mkdir(parents=True)
        pin_path = agdt_dir / PIN_FILENAME

        # Test JSONDecodeError by writing invalid json
        pin_path.write_text("invalid json", encoding="utf-8")
        with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
            state.clear_workflow_state(completing_workflow="test-workflow")
        assert pin_path.exists()

        # Test OSError by patching read_text
        pin_path.write_text(json.dumps({"workflow": "test-workflow"}), encoding="utf-8")
        with patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path):
            with patch("pathlib.Path.read_text", side_effect=OSError("mock read error")):
                state.clear_workflow_state(completing_workflow="test-workflow")
        assert pin_path.exists()

    def test_pin_cleanup_skipped_when_no_git_root(self, temp_state_dir):
        """Pin cleanup is skipped when not in a git repo."""
        state.set_workflow_state(name="test", status="active")
        with patch("agentic_devtools.state._get_git_repo_root", return_value=None):
            state.clear_workflow_state(force_delete=True)
        # No error raised — gracefully returns
