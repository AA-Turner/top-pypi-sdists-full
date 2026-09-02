"""Tests for ``_create_issue_operations`` (T028, T046)."""

from __future__ import annotations

import pytest

import agentic_devtools.cli.jira.creation_pipeline as cp
from agentic_devtools.adapters.exceptions import HierarchyLinkError
from agentic_devtools.adapters.issue_provider import ProviderIssueResult
from agentic_devtools.cli.jira.creation_pipeline import (
    PipelineExecutionError,
    _build_execution_order,
    _create_issue_operations,
)

from .conftest import make_context, make_tree


class TestCreateIssueOperationsHappyPath:
    def test_creates_all_nodes_in_order_with_parent_links(self, in_memory_context):
        order = _build_execution_order(in_memory_context)
        ref_to_id, descriptors = _create_issue_operations(in_memory_context, order, dry_run=False)
        # Every ordered ref got an id and a descriptor.
        assert set(ref_to_id) == set(order)
        assert [d.refs for d in descriptors] == [(ref,) for ref in order]
        assert all(d.operation_type == "create_issue" for d in descriptors)
        assert all(d.status == "created" for d in descriptors)

    def test_child_receives_parent_identifier(self):
        tree = make_tree(with_blocking=False)
        ctx = make_context(tree)
        order = _build_execution_order(ctx)
        ref_to_id, _ = _create_issue_operations(ctx, order, dry_run=False)
        provider = ctx.provider
        f1_record = provider._issues[ref_to_id["f1"]]
        assert f1_record["parent_id"] == ref_to_id["e1"]
        s1_record = provider._issues[ref_to_id["s1"]]
        assert s1_record["parent_id"] == ref_to_id["f1"]


class TestCreateIssueOperationsDryRun:
    def test_dry_run_creates_nothing_and_leaves_ids_empty(self, in_memory_context):
        order = _build_execution_order(in_memory_context)
        ref_to_id, descriptors = _create_issue_operations(in_memory_context, order, dry_run=True)
        assert ref_to_id == {}
        assert all(d.status == "dry-run" for d in descriptors)
        assert all(d.result is None for d in descriptors)
        # No issues persisted in the provider store.
        assert in_memory_context.provider._issues == {}


class TestCreateIssueOperationsPartialLink:
    """T046 — a partial hierarchy-link failure yields a ``partial-created`` op."""

    class _PartialLinkProvider:
        def __init__(self):
            self._n = 0

        def create_issue(self, title, body, issue_type, *, parent_id=None, labels=None, dry_run=False):
            self._n += 1
            if title == "F1":
                partial = ProviderIssueResult(identifier=str(self._n), url="u", status="partial-created")
                raise HierarchyLinkError(
                    "sub-issue link failed",
                    created_result=partial,
                    stage="link_subissue",
                    cause=RuntimeError("gh api 500"),
                )
            return ProviderIssueResult(identifier=str(self._n), url=f"u/{self._n}", status="created")

    def test_partial_created_descriptor_captured_before_raise(self):
        tree = make_tree(with_blocking=False)
        ctx = make_context(tree)
        ctx = cp._PreflightContext(
            tree=tree,
            provider=self._PartialLinkProvider(),
            provider_name="github",
            node_index=ctx.node_index,
        )
        order = _build_execution_order(ctx)
        with pytest.raises(PipelineExecutionError) as exc_info:
            _create_issue_operations(ctx, order, dry_run=False)
        err = exc_info.value
        assert err.stage == "link_subissue"
        assert err.created_result is not None
        assert err.created_result.status == "partial-created"
        # Partial plan ends with the partial-created descriptor for f1.
        last = err.partial_plan.operations[-1]
        assert last.refs == ("f1",)
        assert last.status == "partial-created"
        assert last.is_partial_created is True
        # Underlying cause propagated (not the HierarchyLinkError wrapper).
        assert isinstance(err.cause, RuntimeError)


class _FailingCreateProvider:
    """Fake provider that fails on a specific create call."""

    def __init__(self, fail_on_ref_title: str, error: Exception):
        self._fail_title = fail_on_ref_title
        self._error = error
        self.create_calls: list[str] = []
        self._n = 0

    def create_issue(self, title, body, issue_type, *, parent_id=None, labels=None, dry_run=False):
        self.create_calls.append(title)
        if title == self._fail_title:
            raise self._error
        self._n += 1
        return ProviderIssueResult(identifier=str(self._n), url=f"u/{self._n}", status="created")


class TestCreateFailurePropagation:
    def test_first_failure_stops_and_suppresses_later_ops(self):
        tree = make_tree(with_blocking=False)
        ctx = make_context(tree)
        provider = _FailingCreateProvider("F1", RuntimeError("create failed"))
        ctx = cp._PreflightContext(tree=tree, provider=provider, provider_name="github", node_index=ctx.node_index)
        order = cp._build_execution_order(ctx)
        with pytest.raises(PipelineExecutionError) as exc_info:
            _create_issue_operations(ctx, order, dry_run=False)
        err = exc_info.value
        assert err.operation_type == "create_issue"
        assert err.refs == ("f1",)
        # Only Epic ("Epic") and the failing "F1" were attempted; subtasks suppressed.
        assert provider.create_calls == ["Epic", "F1"]

    def test_partial_plan_contains_successful_ops_only(self):
        tree = make_tree(with_blocking=False)
        ctx = make_context(tree)
        provider = _FailingCreateProvider("F1", RuntimeError("create failed"))
        ctx = cp._PreflightContext(tree=tree, provider=provider, provider_name="github", node_index=ctx.node_index)
        order = cp._build_execution_order(ctx)
        with pytest.raises(PipelineExecutionError) as exc_info:
            _create_issue_operations(ctx, order, dry_run=False)
        plan = exc_info.value.partial_plan
        # Epic succeeded and was captured; the failed create is not a descriptor.
        assert [op.refs for op in plan.operations] == [("e1",)]
        assert plan.check_existing is False
