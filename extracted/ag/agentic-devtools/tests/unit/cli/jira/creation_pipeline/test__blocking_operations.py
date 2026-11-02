"""Tests for ``_blocking_operations`` (T030)."""

from __future__ import annotations

import pytest

import agentic_devtools.cli.jira.creation_pipeline as cp
from agentic_devtools.adapters.issue_provider import ProviderIssueResult, ProviderLinkResult
from agentic_devtools.cli.jira.creation_pipeline import (
    PipelineExecutionError,
    _blocking_operations,
    _build_execution_order,
    _create_issue_operations,
)
from agentic_devtools.cli.workflows.create_epic.records import initialize_mapping_document
from agentic_devtools.epic_tree.models import EpicNode, EpicTree, FeatureNode, SubtaskNode

from .conftest import make_context, make_tree


def _tree_with_complementary_declaration() -> EpicTree:
    """s1 declares blockedBy s2; s2 declares blocks s1 (same edge)."""
    s1 = SubtaskNode(ref="s1", title="S1", body="b", issueType="Subtask", blockedBy=("s2",))
    s2 = SubtaskNode(ref="s2", title="S2", body="b", issueType="Subtask", blocks=("s1",))
    f1 = FeatureNode(ref="f1", title="F1", body="b", issueType="Feature", subtasks=(s1, s2))
    epic = EpicNode(ref="e1", title="Epic", body="b", issueType="Epic", features=(f1,))
    return EpicTree(schemaVersion="1.0", epic=epic)


class TestBlockingOperationsHappyPath:
    def test_single_edge_creates_one_descriptor(self):
        tree = make_tree(with_blocking=True)
        ctx = make_context(tree)
        order = _build_execution_order(ctx)
        ref_to_id, _ = _create_issue_operations(ctx, order, dry_run=False)
        ops = _blocking_operations(ctx, ref_to_id, dry_run=False)
        assert len(ops) == 1
        op = ops[0]
        assert op.operation_type == "add_blocked_by"
        # Canonical refs recorded as (blocked_ref, blocker_ref).
        assert op.refs == ("s1", "s2")
        assert op.status == "linked"

    def test_complementary_declaration_dedupes_to_one_call(self):
        tree = _tree_with_complementary_declaration()
        ctx = make_context(tree)
        order = _build_execution_order(ctx)
        ref_to_id, _ = _create_issue_operations(ctx, order, dry_run=False)
        ops = _blocking_operations(ctx, ref_to_id, dry_run=False)
        assert len(ops) == 1
        assert ops[0].refs == ("s1", "s2")
        # Exactly one edge persisted in the provider store.
        assert len(ctx.provider._blocked_by) == 1

    def test_confirmation_persists_provider_returned_dependency_ids(self, tmp_path):
        base_tree = make_tree(with_blocking=True)
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=base_tree.epic,
        )
        ctx = make_context(tree)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")

        def add_blocked_by(_blocked_id, _blocker_id, *, dry_run=False):
            return ProviderLinkResult("normalized-blocker", "normalized-blocked", "linked")

        ctx.provider.add_blocked_by = add_blocked_by
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=tmp_path / "mapping.json",
        )
        order = _build_execution_order(ctx)
        ref_to_id, _ = _create_issue_operations(ctx, order, dry_run=False)

        _blocking_operations(ctx, ref_to_id, dry_run=False)

        relationship = mapping_document["entries"]["add_blocked_by:s1:s2"]
        assert relationship["source_provider_id"] == "normalized-blocked"
        assert relationship["target_provider_id"] == "normalized-blocker"


class TestBlockingOperationsDryRun:
    def test_dry_run_plans_without_provider_call(self):
        tree = make_tree(with_blocking=True)
        ctx = make_context(tree)
        order = _build_execution_order(ctx)
        ref_to_id, _ = _create_issue_operations(ctx, order, dry_run=True)
        ops = _blocking_operations(ctx, ref_to_id, dry_run=True)
        assert len(ops) == 1
        assert ops[0].status == "dry-run"
        assert ops[0].result is None
        assert ctx.provider._blocked_by == set()


class TestBlockingOperationsDeterministicOrder:
    def test_edges_sorted_lexicographically(self):
        # Two independent blocking edges: (s2 blocks s1) and (s3 blocks s4).
        s1 = SubtaskNode(ref="s1", title="S1", body="b", issueType="Subtask", blockedBy=("s2",))
        s2 = SubtaskNode(ref="s2", title="S2", body="b", issueType="Subtask")
        s3 = SubtaskNode(ref="s3", title="S3", body="b", issueType="Subtask")
        s4 = SubtaskNode(ref="s4", title="S4", body="b", issueType="Subtask", blockedBy=("s3",))
        f1 = FeatureNode(ref="f1", title="F1", body="b", issueType="Feature", subtasks=(s1, s2, s3, s4))
        epic = EpicNode(ref="e1", title="Epic", body="b", issueType="Epic", features=(f1,))
        tree = EpicTree(schemaVersion="1.0", epic=epic)
        ctx = make_context(tree)
        order = _build_execution_order(ctx)
        ref_to_id, _ = _create_issue_operations(ctx, order, dry_run=False)
        ops = _blocking_operations(ctx, ref_to_id, dry_run=False)
        refs = [op.refs for op in ops]
        # blocker order: s2 (< s3) first -> blocked/blocker pairs.
        assert refs == [("s1", "s2"), ("s4", "s3")]


class TestBlockingOperationsUnresolvedPrefixEdges:
    """Edges entirely within an unmapped, skipped ``start_from`` prefix are skipped."""

    def test_edge_with_both_refs_missing_from_ref_to_id_is_skipped(self):
        # s2 -> s1 edge exists in the tree, but neither ref is present in
        # ref_to_id (e.g. both were skipped by --start-from and were never
        # previously mapped). Reconciliation must skip the edge rather than
        # raising a KeyError.
        tree = make_tree(with_blocking=True)
        ctx = make_context(tree)
        ref_to_id = {"e1": "1", "f1": "2"}
        ops = _blocking_operations(ctx, ref_to_id, dry_run=False)
        assert ops == []
        assert ctx.provider._blocked_by == set()


def test_blocking_operations_skip_relationships_already_reconciled() -> None:
    tree = make_tree(with_blocking=True)
    ctx = make_context(tree)
    order = _build_execution_order(ctx)
    ref_to_id, _ = _create_issue_operations(ctx, order, dry_run=False)
    completed = cp.OperationDescriptor(
        operation_type="add_blocked_by",
        orchestration_key="completed",
        refs=("s1", "s2"),
        status="linked",
        provider_params={},
    )

    ops = _blocking_operations(ctx, ref_to_id, prior_operations=(completed,))

    assert ops == []


def test_blocking_operations_respects_only_refs_filter() -> None:
    context = make_context()
    ordered_refs = _build_execution_order(context)
    ref_to_id, _ = _create_issue_operations(context, ordered_refs)

    operations = _blocking_operations(context, ref_to_id, only_refs={"s1"})

    assert operations == []


def test_edge_with_only_one_ref_missing_is_skipped() -> None:
    tree = make_tree(with_blocking=True)
    ctx = make_context(tree)
    ref_to_id = {"e1": "1", "f1": "2", "s2": "3"}
    ops = _blocking_operations(ctx, ref_to_id, dry_run=False)
    assert ops == []
    assert ctx.provider._blocked_by == set()


class _FailingBlockProvider:
    def __init__(self, error: Exception):
        self._error = error
        self._n = 0

    def normalize_identifier(self, identifier: str) -> str:
        return identifier

    def create_issue(
        self,
        title,
        body,
        issue_type,
        *,
        parent_id=None,
        labels=None,
        idempotency_key=None,
        precreate_lookup=None,
        dry_run=False,
    ):
        self._n += 1
        identifier = str(self._n)
        hierarchy_link_result = ProviderLinkResult(parent_id, identifier, "linked") if parent_id is not None else None
        return ProviderIssueResult(
            identifier=identifier,
            url=f"u/{self._n}",
            status="created",
            hierarchy_link_result=hierarchy_link_result,
        )

    def add_blocked_by(self, issue_id, blocked_by_id, *, dry_run=False):
        raise self._error


class TestBlockingFailurePropagation:
    def test_blocking_failure_includes_prior_create_ops(self):
        tree = make_tree(with_blocking=True)
        provider = _FailingBlockProvider(RuntimeError("link failed"))
        ctx = cp._PreflightContext(
            tree=tree,
            provider=provider,
            provider_name="github",
            node_index=cp._build_node_index(tree),
        )
        order = _build_execution_order(ctx)
        ref_to_id, create_ops = _create_issue_operations(ctx, order, dry_run=False)
        with pytest.raises(PipelineExecutionError) as exc_info:
            _blocking_operations(ctx, ref_to_id, dry_run=False, prior_operations=tuple(create_ops))
        err = exc_info.value
        assert err.operation_type == "add_blocked_by"
        assert err.refs == ("s1", "s2")
        # Partial plan carries every prior create descriptor (no rollback).
        create_refs = [op.refs for op in err.partial_plan.operations]
        assert ("e1",) in create_refs and ("f1",) in create_refs
