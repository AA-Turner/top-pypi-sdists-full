"""Unit tests for spec_queue -- review inbox and approval queue (#1015)."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from anteroom.services.spec_queue import (
    ReviewQueue,
    get_review_queue,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_artifact(
    fqn: str,
    phases: dict[str, str],
    *,
    artifact_id: str = "art-1",
    updated_at: str = "2025-01-01T00:00:00",
    created_at: str = "2025-01-01T00:00:00",
) -> dict[str, Any]:
    """Build a mock artifact dict matching artifact_storage.list_artifacts output."""
    meta_phases = {}
    for name, status in phases.items():
        meta_phases[name] = {
            "status": status,
            "approved_at": "2025-01-01T00:00:00" if status == "approved" else None,
            "approved_by": "user" if status == "approved" else None,
        }
    return {
        "id": artifact_id,
        "fqn": fqn,
        "type": "spec",
        "namespace": "ns",
        "name": fqn.split("/")[-1],
        "metadata": {"phases": meta_phases},
        "updated_at": updated_at,
        "created_at": created_at,
    }


def _blocked_run(run_id: str = "run-1", spec_fqn: str = "@ns/spec/x") -> dict[str, Any]:
    return {
        "id": run_id,
        "workflow_id": "wf-1",
        "status": "blocked",
        "stop_reason": "spec_gate",
        "current_step_id": "step-1",
        "created_at": "2025-01-02T00:00:00",
    }


def _run_queue(
    artifacts: list[dict[str, Any]],
    blocked_runs: list[dict[str, Any]] | None = None,
    stale_reason: str | None = None,
    *,
    space_id: str | None = None,
    project_path: str | None = None,
) -> ReviewQueue:
    """Run get_review_queue with mocked dependencies."""
    with (
        patch("anteroom.services.artifact_storage.list_artifacts", return_value=artifacts),
        patch("anteroom.services.workflow_storage.list_spec_blocked_runs", return_value=blocked_runs or []),
        patch("anteroom.services.spec_diff.derive_stale_reason", return_value=stale_reason),
    ):
        return get_review_queue(MagicMock(), space_id=space_id, project_path=project_path)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestEmptyQueue:
    def test_empty_queue(self) -> None:
        """No specs -> empty ReviewQueue."""
        result = _run_queue([])
        assert result.total == 0
        assert result.needs_review == []
        assert result.stale == []
        assert result.blocked == []


class TestNeedsReviewAllDraft:
    def test_all_draft_in_needs_review(self) -> None:
        """New spec with all phases draft appears in needs_review."""
        art = _make_artifact(
            "@ns/spec/feature-a",
            {"requirements": "draft", "design": "draft", "tasks": "draft"},
        )
        result = _run_queue([art])

        assert result.total == 1
        assert len(result.needs_review) == 1
        item = result.needs_review[0]
        assert item.fqn == "@ns/spec/feature-a"
        assert item.category == "needs_review"
        assert all(v == "draft" for v in item.phases.values())
        assert item.stale_reasons == {}
        assert item.blocked_runs == []
        assert result.stale == []
        assert result.blocked == []


class TestNeedsReviewPartialApproval:
    def test_partial_approval_in_needs_review(self) -> None:
        """Spec with requirements approved, design still draft -> needs_review."""
        art = _make_artifact(
            "@ns/spec/feature-b",
            {"requirements": "approved", "design": "draft", "tasks": "draft"},
        )
        result = _run_queue([art])

        assert result.total == 1
        assert len(result.needs_review) == 1
        item = result.needs_review[0]
        assert item.phases["requirements"] == "approved"
        assert item.phases["design"] == "draft"


class TestStaleDetection:
    def test_stale_in_both_lists(self) -> None:
        """Spec with stale phase appears in both stale and needs_review."""
        art = _make_artifact(
            "@ns/spec/feature-c",
            {"requirements": "stale", "design": "approved", "tasks": "draft"},
        )
        result = _run_queue([art], stale_reason="requirements changed since approval")

        assert result.total == 1
        assert len(result.needs_review) == 1
        assert len(result.stale) == 1
        assert result.stale[0].fqn == "@ns/spec/feature-c"
        assert result.stale[0].stale_reasons["requirements"] == "requirements changed since approval"


class TestBlockedSpecGateOnly:
    def test_blocked_at_spec_gate(self) -> None:
        """Run blocked at spec gate appears in blocked list."""
        art = _make_artifact(
            "@ns/spec/feature-d",
            {"requirements": "approved", "design": "approved", "tasks": "approved"},
        )
        run = _blocked_run("run-1", "@ns/spec/feature-d")
        result = _run_queue([art], blocked_runs=[run])

        # All phases approved -> not in needs_review
        assert result.total == 0
        assert len(result.needs_review) == 0
        # But has blocked runs -> in blocked
        assert len(result.blocked) == 1
        assert result.blocked[0].blocked_runs == [run]


class TestBlockedNonSpecGateExcluded:
    def test_non_spec_gate_not_in_blocked(self) -> None:
        """Run blocked at a non-spec gate does not appear (list_spec_blocked_runs returns [])."""
        art = _make_artifact(
            "@ns/spec/feature-e",
            {"requirements": "approved", "design": "approved", "tasks": "approved"},
        )
        result = _run_queue([art])

        assert result.blocked == []
        assert result.needs_review == []


class TestAllApprovedNotInQueue:
    def test_fully_approved_excluded(self) -> None:
        """Fully approved specs with no blocked runs excluded from all lists."""
        art = _make_artifact(
            "@ns/spec/feature-f",
            {"requirements": "approved", "design": "approved", "tasks": "approved"},
        )
        result = _run_queue([art])

        assert result.total == 0
        assert result.needs_review == []
        assert result.stale == []
        assert result.blocked == []


class TestQueueSorting:
    def test_most_recent_first(self) -> None:
        """Items sorted by updated_at descending (most recent first)."""
        art_old = _make_artifact(
            "@ns/spec/old",
            {"requirements": "draft", "design": "draft", "tasks": "draft"},
            artifact_id="art-old",
            updated_at="2025-01-01T00:00:00",
        )
        art_new = _make_artifact(
            "@ns/spec/new",
            {"requirements": "draft", "design": "draft", "tasks": "draft"},
            artifact_id="art-new",
            updated_at="2025-06-01T00:00:00",
        )
        result = _run_queue([art_old, art_new])

        assert result.total == 2
        assert result.needs_review[0].fqn == "@ns/spec/new"
        assert result.needs_review[1].fqn == "@ns/spec/old"


class TestListSpecBlockedRunsJoin:
    """Direct test of the storage query using a real SQLite DB."""

    @pytest.fixture()
    def db(self, tmp_path: Path) -> Any:
        from anteroom.db import init_db

        return init_db(tmp_path / "test.db")

    def test_returns_blocked_spec_gate_runs(self, db: Any) -> None:
        from anteroom.services.workflow_storage import (
            create_workflow_run,
            create_workflow_step,
            list_spec_blocked_runs,
            update_workflow_run,
            update_workflow_step,
        )

        run = create_workflow_run(
            db,
            workflow_id="wf-1",
            workflow_version="1",
            target_kind="spec",
            target_ref="feature-x",
            inputs={"spec_fqn": "@ns/spec/feature-x", "task_id": "t1"},
        )
        step = create_workflow_step(
            db,
            run_id=run["id"],
            step_id="gate-1",
            step_type="gate",
        )
        update_workflow_run(db, run["id"], status="blocked", stop_reason="spec_gate")
        update_workflow_step(
            db,
            step["id"],
            status="completed",
            result_status="blocked",
            result_summary="Phase requirements not approved",
        )

        results = list_spec_blocked_runs(db, "@ns/spec/feature-x")
        assert len(results) == 1
        assert results[0]["id"] == run["id"]
        assert results[0]["status"] == "blocked"

    def test_excludes_non_gate_blocked_runs(self, db: Any) -> None:
        from anteroom.services.workflow_storage import (
            create_workflow_run,
            create_workflow_step,
            list_spec_blocked_runs,
            update_workflow_run,
            update_workflow_step,
        )

        run = create_workflow_run(
            db,
            workflow_id="wf-2",
            workflow_version="1",
            target_kind="spec",
            target_ref="feature-y",
            inputs={"spec_fqn": "@ns/spec/feature-y", "task_id": "t1"},
        )
        step = create_workflow_step(
            db,
            run_id=run["id"],
            step_id="run-1",
            step_type="runner",
        )
        update_workflow_run(db, run["id"], status="blocked")
        update_workflow_step(
            db,
            step["id"],
            status="completed",
            result_status="blocked",
            result_summary="Some other block",
        )

        results = list_spec_blocked_runs(db, "@ns/spec/feature-y")
        assert results == []

    def test_excludes_non_spec_fqn_runs(self, db: Any) -> None:
        from anteroom.services.workflow_storage import (
            create_workflow_run,
            create_workflow_step,
            list_spec_blocked_runs,
            update_workflow_run,
            update_workflow_step,
        )

        run = create_workflow_run(
            db,
            workflow_id="wf-3",
            workflow_version="1",
            target_kind="spec",
            target_ref="other",
            inputs={"spec_fqn": "@ns/spec/other", "task_id": "t1"},
        )
        step = create_workflow_step(
            db,
            run_id=run["id"],
            step_id="gate-2",
            step_type="gate",
        )
        update_workflow_run(db, run["id"], status="blocked", stop_reason="spec_gate")
        update_workflow_step(
            db,
            step["id"],
            status="completed",
            result_status="blocked",
            result_summary="Phase design not approved",
        )

        results = list_spec_blocked_runs(db, "@ns/spec/feature-z")
        assert results == []


class TestAttachmentFiltering:
    def test_passes_attachment_context(self) -> None:
        """When space_id/project_path provided, list_artifacts called with attached_only=True."""
        art = _make_artifact(
            "@ns/spec/feature-g",
            {"requirements": "draft", "design": "draft", "tasks": "draft"},
        )
        with (
            patch("anteroom.services.artifact_storage.list_artifacts", return_value=[art]) as mock_list,
            patch("anteroom.services.workflow_storage.list_spec_blocked_runs", return_value=[]),
            patch("anteroom.services.spec_diff.derive_stale_reason", return_value=None),
        ):
            get_review_queue(MagicMock(), space_id="sp-1", project_path="/some/path")

        mock_list.assert_called_once()
        call_kwargs = mock_list.call_args
        assert call_kwargs.kwargs.get("attached_only") is True or call_kwargs[1].get("attached_only") is True
        kw = call_kwargs.kwargs if call_kwargs.kwargs else call_kwargs[1]
        assert kw["space_id"] == "sp-1"
        assert kw["project_path"] == "/some/path"

    def test_no_context_scans_all(self) -> None:
        """When no space/project context, list_artifacts called with attached_only=False."""
        with (
            patch("anteroom.services.artifact_storage.list_artifacts", return_value=[]) as mock_list,
            patch("anteroom.services.workflow_storage.list_spec_blocked_runs", return_value=[]),
            patch("anteroom.services.spec_diff.derive_stale_reason", return_value=None),
        ):
            get_review_queue(MagicMock())

        mock_list.assert_called_once()
        call_kwargs = mock_list.call_args
        kw = call_kwargs.kwargs if call_kwargs.kwargs else call_kwargs[1]
        assert kw.get("attached_only") is False
