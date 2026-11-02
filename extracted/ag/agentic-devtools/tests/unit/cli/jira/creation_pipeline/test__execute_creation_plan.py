"""Tests for ``_execute_creation_plan``.

Covers the ordering/create/link/blocking call sequence and the
``OperationPlan`` contract it assembles, independent of the lock/preflight
concerns owned by ``run_creation_pipeline`` itself.
"""

from __future__ import annotations

from agentic_devtools.adapters.operation_plan import OperationPlan
from agentic_devtools.cli.jira.creation_pipeline import _execute_creation_plan

from .conftest import make_context, make_tree


class TestExecuteCreationPlanHappyPath:
    def test_builds_plan_with_every_operation_type(self):
        ctx = make_context(make_tree(with_blocking=True))
        plan = _execute_creation_plan(ctx, dry_run=False)
        assert isinstance(plan, OperationPlan)
        assert plan.dry_run is False
        assert plan.check_existing is False
        op_types = {op.operation_type for op in plan.operations}
        assert op_types == {"create_issue", "add_blocked_by"}

    def test_dry_run_plans_without_provider_mutation(self):
        ctx = make_context(make_tree(with_blocking=True))
        plan = _execute_creation_plan(ctx, dry_run=True)
        assert plan.dry_run is True
        assert all(op.status == "dry-run" for op in plan.operations)
        assert ctx.provider._issues == {}  # type: ignore[attr-defined]

    def test_check_existing_reflects_prior_mapping_document(self, tmp_path):
        from agentic_devtools.cli.jira.creation_pipeline import EpicTree, _PreflightContext
        from agentic_devtools.cli.workflows.create_epic.records import initialize_mapping_document

        base_tree = make_tree()
        tree = EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=base_tree.epic,
        )
        base_ctx = make_context(tree)
        ctx = _PreflightContext(
            tree=tree,
            provider=base_ctx.provider,
            provider_name=base_ctx.provider_name,
            node_index=base_ctx.node_index,
            mapping_document=initialize_mapping_document(tree, "github", "owner/repo"),
            mapping_path=tmp_path / "mapping.json",
        )
        plan = _execute_creation_plan(ctx, dry_run=False)
        assert plan.check_existing is True
