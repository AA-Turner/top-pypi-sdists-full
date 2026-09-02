"""Tests for OperationPlan (FR-006)."""

from __future__ import annotations

import json

from agentic_devtools.adapters.operation_plan import OperationDescriptor, OperationPlan


class TestOperationPlan:
    """Verify OperationPlan construction, filtering, and serialization."""

    def _make_plan(self) -> OperationPlan:
        ops = (
            OperationDescriptor(
                operation_type="create_issue",
                orchestration_key="a" * 64,
                refs=("ref-1",),
                status="dry-run",
                provider_params={"title": "Issue 1"},
            ),
            OperationDescriptor(
                operation_type="create_issue",
                orchestration_key="b" * 64,
                refs=("ref-2",),
                status="dry-run",
                provider_params={"title": "Issue 2"},
            ),
            OperationDescriptor(
                operation_type="link_subissue",
                orchestration_key="c" * 64,
                refs=("ref-1", "ref-2"),
                status="dry-run",
                provider_params={"parent_id": "ref-1", "child_id": "ref-2"},
            ),
            OperationDescriptor(
                operation_type="add_blocked_by",
                orchestration_key="d" * 64,
                refs=("ref-2", "ref-1"),
                status="dry-run",
                provider_params={"issue_id": "ref-2", "blocked_by_id": "ref-1"},
            ),
        )
        return OperationPlan(operations=ops, dry_run=True, check_existing=False)

    def test_construction(self):
        plan = self._make_plan()
        assert len(plan.operations) == 4
        assert plan.dry_run is True
        assert plan.check_existing is False

    def test_create_operations(self):
        plan = self._make_plan()
        creates = plan.create_operations
        assert len(creates) == 2
        assert all(op.operation_type == "create_issue" for op in creates)

    def test_link_operations(self):
        plan = self._make_plan()
        links = plan.link_operations
        assert len(links) == 1
        assert links[0].operation_type == "link_subissue"

    def test_dependency_operations(self):
        plan = self._make_plan()
        deps = plan.dependency_operations
        assert len(deps) == 1
        assert deps[0].operation_type == "add_blocked_by"

    def test_to_dict_json_serializable(self):
        plan = self._make_plan()
        d = plan.to_dict()
        serialized = json.dumps(d)
        assert serialized
        assert d["dry_run"] is True
        assert d["check_existing"] is False
        assert d["summary"]["total"] == 4
        assert d["summary"]["creates"] == 2
        assert d["summary"]["links"] == 1
        assert d["summary"]["dependencies"] == 1

    def test_empty_plan(self):
        plan = OperationPlan(operations=(), dry_run=True, check_existing=False)
        assert len(plan.operations) == 0
        assert len(plan.create_operations) == 0
        assert len(plan.link_operations) == 0
        assert len(plan.dependency_operations) == 0
        d = plan.to_dict()
        assert d["summary"]["total"] == 0
