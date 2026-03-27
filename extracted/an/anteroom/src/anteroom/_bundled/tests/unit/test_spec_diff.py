"""Unit tests for spec_diff — diffing, invalidation rules, stale reason derivation."""

from __future__ import annotations

from anteroom.services.spec_diff import (
    apply_invalidations,
    diff_spec_versions,
    evaluate_invalidation_rules,
)
from anteroom.services.spec_schema import (
    SpecContent,
    SpecPhaseStatus,
    SpecTask,
    default_phase_metadata,
    set_phase_status,
)


def _spec(
    req: str = "requirements text",
    design: str = "design text",
    tasks: list[SpecTask] | None = None,
) -> SpecContent:
    return SpecContent(
        requirements=req,
        design=design,
        tasks=tasks or [SpecTask(id="t1", summary="task one")],
    )


# ---------------------------------------------------------------------------
# diff_spec_versions
# ---------------------------------------------------------------------------


class TestDiffSpecVersions:
    def test_no_changes_returns_empty_diff(self) -> None:
        spec = _spec()
        diff = diff_spec_versions(spec, spec, version_from=1, version_to=2)
        assert all(not pc.content_changed for pc in diff.phase_changes)
        assert diff.task_changes == []

    def test_requirements_changed(self) -> None:
        old = _spec(req="old requirements")
        new = _spec(req="new requirements")
        diff = diff_spec_versions(old, new)
        req_change = next(pc for pc in diff.phase_changes if pc.phase == "requirements")
        assert req_change.content_changed is True
        assert req_change.content_diff is not None
        assert "old requirements" in req_change.content_diff
        assert "new requirements" in req_change.content_diff

    def test_design_changed(self) -> None:
        old = _spec(design="old design")
        new = _spec(design="new design")
        diff = diff_spec_versions(old, new)
        design_change = next(pc for pc in diff.phase_changes if pc.phase == "design")
        assert design_change.content_changed is True

    def test_task_added(self) -> None:
        old = _spec()
        new = _spec(tasks=[SpecTask(id="t1", summary="task one"), SpecTask(id="t2", summary="new task")])
        diff = diff_spec_versions(old, new)
        added = [tc for tc in diff.task_changes if tc.change_type == "added"]
        assert len(added) == 1
        assert added[0].task_id == "t2"
        assert added[0].summary_after == "new task"

    def test_task_removed(self) -> None:
        old = _spec(tasks=[SpecTask(id="t1", summary="task one"), SpecTask(id="t2", summary="removed")])
        new = _spec()
        diff = diff_spec_versions(old, new)
        removed = [tc for tc in diff.task_changes if tc.change_type == "removed"]
        assert len(removed) == 1
        assert removed[0].task_id == "t2"

    def test_task_modified(self) -> None:
        old = _spec(tasks=[SpecTask(id="t1", summary="old summary")])
        new = _spec(tasks=[SpecTask(id="t1", summary="new summary")])
        diff = diff_spec_versions(old, new)
        modified = [tc for tc in diff.task_changes if tc.change_type == "modified"]
        assert len(modified) == 1
        assert modified[0].summary_before == "old summary"
        assert modified[0].summary_after == "new summary"

    def test_tasks_phase_changed_when_list_differs(self) -> None:
        old = _spec()
        new = _spec(tasks=[SpecTask(id="t1", summary="task one"), SpecTask(id="t2", summary="extra")])
        diff = diff_spec_versions(old, new)
        tasks_phase = next(pc for pc in diff.phase_changes if pc.phase == "tasks")
        assert tasks_phase.content_changed is True

    def test_version_numbers_in_diff(self) -> None:
        diff = diff_spec_versions(_spec(), _spec(), version_from=3, version_to=5)
        assert diff.version_from == 3
        assert diff.version_to == 5


# ---------------------------------------------------------------------------
# evaluate_invalidation_rules
# ---------------------------------------------------------------------------


class TestEvaluateInvalidationRules:
    def test_no_changes_no_invalidations(self) -> None:
        spec = _spec()
        meta = set_phase_status(default_phase_metadata(), "design", SpecPhaseStatus.APPROVED)
        result = evaluate_invalidation_rules(spec, spec, meta)
        assert result == []

    def test_req_changed_design_approved_invalidates_design(self) -> None:
        old = _spec(req="old")
        new = _spec(req="new")
        meta = set_phase_status(default_phase_metadata(), "design", SpecPhaseStatus.APPROVED)
        result = evaluate_invalidation_rules(old, new, meta)
        phases = [r[0] for r in result]
        assert "design" in phases

    def test_req_changed_tasks_approved_invalidates_tasks(self) -> None:
        old = _spec(req="old")
        new = _spec(req="new")
        meta = set_phase_status(default_phase_metadata(), "tasks", SpecPhaseStatus.APPROVED)
        result = evaluate_invalidation_rules(old, new, meta)
        phases = [r[0] for r in result]
        assert "tasks" in phases

    def test_design_changed_tasks_approved_invalidates_tasks(self) -> None:
        old = _spec(design="old")
        new = _spec(design="new")
        meta = set_phase_status(default_phase_metadata(), "tasks", SpecPhaseStatus.APPROVED)
        result = evaluate_invalidation_rules(old, new, meta)
        phases = [r[0] for r in result]
        assert "tasks" in phases

    def test_req_changed_design_draft_no_invalidation(self) -> None:
        old = _spec(req="old")
        new = _spec(req="new")
        meta = default_phase_metadata()  # all draft
        result = evaluate_invalidation_rules(old, new, meta)
        assert result == []

    def test_req_changed_design_already_stale_no_invalidation(self) -> None:
        old = _spec(req="old")
        new = _spec(req="new")
        meta = set_phase_status(default_phase_metadata(), "design", SpecPhaseStatus.STALE)
        result = evaluate_invalidation_rules(old, new, meta)
        phases = [r[0] for r in result]
        assert "design" not in phases

    def test_both_req_and_design_changed_tasks_approved(self) -> None:
        old = _spec(req="old req", design="old design")
        new = _spec(req="new req", design="new design")
        meta = set_phase_status(default_phase_metadata(), "tasks", SpecPhaseStatus.APPROVED)
        result = evaluate_invalidation_rules(old, new, meta)
        # tasks should be invalidated once, not twice
        task_invalidations = [r for r in result if r[0] == "tasks"]
        assert len(task_invalidations) == 1

    def test_req_changed_both_design_and_tasks_approved(self) -> None:
        old = _spec(req="old")
        new = _spec(req="new")
        meta = default_phase_metadata()
        meta = set_phase_status(meta, "design", SpecPhaseStatus.APPROVED)
        meta = set_phase_status(meta, "tasks", SpecPhaseStatus.APPROVED)
        result = evaluate_invalidation_rules(old, new, meta)
        phases = [r[0] for r in result]
        assert "design" in phases
        assert "tasks" in phases

    def test_missing_phases_key_in_metadata(self) -> None:
        old = _spec(req="old")
        new = _spec(req="new")
        result = evaluate_invalidation_rules(old, new, {})
        assert result == []


# ---------------------------------------------------------------------------
# apply_invalidations
# ---------------------------------------------------------------------------


class TestApplyInvalidations:
    def test_empty_invalidations_returns_original(self) -> None:
        meta = default_phase_metadata()
        result = apply_invalidations(meta, [])
        assert result is meta

    def test_marks_phase_stale(self) -> None:
        meta = set_phase_status(default_phase_metadata(), "design", SpecPhaseStatus.APPROVED, approved_by="troy")
        result = apply_invalidations(meta, [("design", "req changed")])
        assert result["phases"]["design"]["status"] == "stale"
        assert result["phases"]["design"]["approved_by"] == "troy"

    def test_preserves_approved_at_version(self) -> None:
        meta = set_phase_status(
            default_phase_metadata(),
            "design",
            SpecPhaseStatus.APPROVED,
            approved_by="troy",
            approved_at_version=3,
        )
        result = apply_invalidations(meta, [("design", "req changed")])
        assert result["phases"]["design"]["status"] == "stale"
        assert result["phases"]["design"]["approved_at_version"] == 3

    def test_multiple_invalidations(self) -> None:
        meta = default_phase_metadata()
        meta = set_phase_status(meta, "design", SpecPhaseStatus.APPROVED)
        meta = set_phase_status(meta, "tasks", SpecPhaseStatus.APPROVED)
        result = apply_invalidations(meta, [("design", "r1"), ("tasks", "r2")])
        assert result["phases"]["design"]["status"] == "stale"
        assert result["phases"]["tasks"]["status"] == "stale"
