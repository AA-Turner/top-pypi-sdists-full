"""Tests for DecisionRequired and decision gate persistence."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.orchestration.execution.decision_gate import (
    DecisionRequired,
    read_pending_decisions,
    resolve_decision,
    write_pending_decision,
)


class TestDecisionRequired:
    """Tests for DecisionRequired frozen dataclass."""

    def test_create_factory(self) -> None:
        """create() produces a valid pending decision."""
        decision = DecisionRequired.create(
            action_name="git_push",
            arguments={"branch": "main"},
            node_name="push_node",
            run_id="run-abc",
        )
        assert decision.action_name == "git_push"
        assert decision.status == "pending"
        assert decision.run_id == "run-abc"
        assert len(decision.decision_id) == 32  # UUID hex

    def test_frozen(self) -> None:
        """DecisionRequired is frozen."""
        d = DecisionRequired.create(action_name="x")
        with pytest.raises(AttributeError):
            d.status = "approved"  # type: ignore[misc]


class TestWritePendingDecision:
    """Tests for write/read/resolve decision persistence."""

    def test_write_and_read_roundtrip(self, tmp_path: Path) -> None:
        """Written decisions can be read back."""
        decision = DecisionRequired.create(
            action_name="deploy",
            node_name="deploy_node",
            run_id="run1",
        )
        write_pending_decision(tmp_path, "run1", decision)

        decisions = read_pending_decisions(tmp_path, "run1")
        assert len(decisions) == 1
        assert decisions[0].action_name == "deploy"
        assert decisions[0].decision_id == decision.decision_id

    def test_multiple_decisions(self, tmp_path: Path) -> None:
        """Multiple decisions accumulate."""
        d1 = DecisionRequired.create(action_name="action1", run_id="run1")
        d2 = DecisionRequired.create(action_name="action2", run_id="run1")

        write_pending_decision(tmp_path, "run1", d1)
        write_pending_decision(tmp_path, "run1", d2)

        decisions = read_pending_decisions(tmp_path, "run1")
        assert len(decisions) == 2

    def test_read_empty_run(self, tmp_path: Path) -> None:
        """Reading from a non-existent run returns empty list."""
        decisions = read_pending_decisions(tmp_path, "nonexistent")
        assert decisions == []


class TestResolveDecision:
    """Tests for resolve_decision()."""

    def test_approve_decision(self, tmp_path: Path) -> None:
        """Approving updates status to 'approved'."""
        decision = DecisionRequired.create(action_name="push", run_id="run1")
        write_pending_decision(tmp_path, "run1", decision)

        resolved = resolve_decision(tmp_path, "run1", decision.decision_id, approved=True)
        assert resolved.status == "approved"

    def test_deny_decision(self, tmp_path: Path) -> None:
        """Denying updates status to 'denied'."""
        decision = DecisionRequired.create(action_name="push", run_id="run1")
        write_pending_decision(tmp_path, "run1", decision)

        resolved = resolve_decision(tmp_path, "run1", decision.decision_id, approved=False)
        assert resolved.status == "denied"

    def test_resolve_nonexistent_raises(self, tmp_path: Path) -> None:
        """Resolving unknown decision_id raises ValueError."""
        with pytest.raises(ValueError, match="Decision not found"):
            resolve_decision(tmp_path, "run1", "nonexistent_id", approved=True)

    def test_resolve_second_decision_in_list(self, tmp_path: Path) -> None:
        """Resolving the second decision iterates past the first."""
        d1 = DecisionRequired.create(action_name="action1", run_id="run1")
        d2 = DecisionRequired.create(action_name="action2", run_id="run1")
        write_pending_decision(tmp_path, "run1", d1)
        write_pending_decision(tmp_path, "run1", d2)

        resolved = resolve_decision(tmp_path, "run1", d2.decision_id, approved=True)
        assert resolved.status == "approved"
        assert resolved.action_name == "action2"


class TestLoadDecisionsRaw:
    """Tests for _load_decisions_raw edge cases."""

    def test_empty_file_returns_empty_list(self, tmp_path: Path) -> None:
        """File with only whitespace returns empty list."""
        from agentic_devtools.orchestration.execution.decision_gate import _get_decisions_path

        path = _get_decisions_path(tmp_path, "run1")
        path.write_text("   \n  ")

        decisions = read_pending_decisions(tmp_path, "run1")
        assert decisions == []

    def test_non_list_json_returns_empty_list(self, tmp_path: Path) -> None:
        """File containing a JSON object (not a list) returns empty list."""
        from agentic_devtools.orchestration.execution.decision_gate import _get_decisions_path

        path = _get_decisions_path(tmp_path, "run1")
        path.write_text('{"key": "value"}')

        decisions = read_pending_decisions(tmp_path, "run1")
        assert decisions == []

    def test_invalid_json_returns_empty_list(self, tmp_path: Path) -> None:
        """File containing invalid JSON returns empty list."""
        from agentic_devtools.orchestration.execution.decision_gate import _get_decisions_path

        path = _get_decisions_path(tmp_path, "run1")
        path.write_text("not valid json {{{}}")

        decisions = read_pending_decisions(tmp_path, "run1")
        assert decisions == []

    def test_oserror_on_locked_read_returns_empty_list(self, tmp_path: Path) -> None:
        """OSError during locked_file read returns empty list gracefully."""
        from unittest.mock import patch

        from agentic_devtools.orchestration.execution.decision_gate import (
            _get_decisions_path,
            _load_decisions_raw,
        )

        path = _get_decisions_path(tmp_path, "run1")
        path.write_text("[]")

        with patch("agentic_devtools.file_locking.locked_file", side_effect=OSError("permission denied")):
            result = _load_decisions_raw(path)

        assert result == []


class TestRunIdValidation:
    """Tests that persistence helpers reject path-like run IDs."""

    @pytest.mark.parametrize("run_id", ["../escape", r"..\\escape", "/tmp/escape", "C:\\temp\\escape", "   "])
    def test_write_pending_decision_rejects_invalid_run_id(self, tmp_path: Path, run_id: str) -> None:
        """write_pending_decision rejects path-like run IDs at the persistence boundary."""
        decision = DecisionRequired.create(action_name="deploy", run_id="run1")
        with pytest.raises(ValueError, match="run_id"):
            write_pending_decision(tmp_path, run_id, decision)

    @pytest.mark.parametrize("run_id", ["../escape", r"..\\escape", "/tmp/escape", "C:\\temp\\escape", "   "])
    def test_read_pending_decisions_rejects_invalid_run_id(self, tmp_path: Path, run_id: str) -> None:
        """read_pending_decisions rejects path-like run IDs at the persistence boundary."""
        with pytest.raises(ValueError, match="run_id"):
            read_pending_decisions(tmp_path, run_id)

    @pytest.mark.parametrize("run_id", ["../escape", r"..\\escape", "/tmp/escape", "C:\\temp\\escape", "   "])
    def test_resolve_decision_rejects_invalid_run_id(self, tmp_path: Path, run_id: str) -> None:
        """resolve_decision rejects path-like run IDs at the persistence boundary."""
        with pytest.raises(ValueError, match="run_id"):
            resolve_decision(tmp_path, run_id, "decision-id", approved=True)


class TestNonDictEntryGracefulDegradation:
    """Tests that non-dict list entries are skipped without raising."""

    def _write_raw(self, tmp_path: Path, run_id: str, content: str) -> None:
        from agentic_devtools.orchestration.execution.decision_gate import _get_decisions_path

        path = _get_decisions_path(tmp_path, run_id)
        path.write_text(content)

    def test_read_skips_non_dict_entries(self, tmp_path: Path) -> None:
        """Non-dict list entries (strings, ints) are skipped by read_pending_decisions."""
        self._write_raw(tmp_path, "run1", '["not_a_dict", 42, null]')
        decisions = read_pending_decisions(tmp_path, "run1")
        assert decisions == []

    def test_read_skips_non_dict_entries_mixed(self, tmp_path: Path) -> None:
        """Valid dict entries are returned; non-dict entries are silently skipped."""
        decision = DecisionRequired.create(action_name="deploy", run_id="run1")
        import json
        from dataclasses import asdict

        content = json.dumps(["not_a_dict", asdict(decision), None])
        self._write_raw(tmp_path, "run1", content)

        decisions = read_pending_decisions(tmp_path, "run1")
        assert len(decisions) == 1
        assert decisions[0].action_name == "deploy"

    def test_read_skips_dict_entries_missing_required_fields(self, tmp_path: Path) -> None:
        """Partially corrupt dict entries are skipped without breaking valid ones."""
        decision = DecisionRequired.create(action_name="deploy", run_id="run1")
        import json
        from dataclasses import asdict

        content = json.dumps([{"action_name": "missing_id"}, asdict(decision)])
        self._write_raw(tmp_path, "run1", content)

        decisions = read_pending_decisions(tmp_path, "run1")
        assert len(decisions) == 1
        assert decisions[0].decision_id == decision.decision_id

    def test_resolve_skips_non_dict_entries(self, tmp_path: Path) -> None:
        """resolve_decision skips non-dict entries when searching for decision_id."""
        decision = DecisionRequired.create(action_name="push", run_id="run1")
        import json
        from dataclasses import asdict

        content = json.dumps(["corrupted_entry", asdict(decision)])
        self._write_raw(tmp_path, "run1", content)

        resolved = resolve_decision(tmp_path, "run1", decision.decision_id, approved=True)
        assert resolved.status == "approved"

    def test_resolve_corrupt_dict_with_matching_id_raises_value_error(self, tmp_path: Path) -> None:
        """Corrupt dict with matching decision_id but missing required fields raises ValueError."""
        import json

        corrupt_entry = {"decision_id": "target-id-999"}  # missing action_name etc.
        self._write_raw(tmp_path, "run1", json.dumps([corrupt_entry]))

        with pytest.raises(ValueError, match="Corrupt decision entry"):
            resolve_decision(tmp_path, "run1", "target-id-999", approved=True)
