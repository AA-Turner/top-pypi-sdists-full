from __future__ import annotations

import json
from dataclasses import replace

import pytest

import agentic_devtools.cli.jira.creation_pipeline as cp
from agentic_devtools.adapters.issue_provider import ProviderIssueResult, ProviderLinkResult
from agentic_devtools.adapters.operation_plan import OperationPlan
from agentic_devtools.cli.workflows.create_epic.records import initialize_mapping_document

from .conftest import make_context


def test_link_operations_persists_provider_returned_ids(tmp_path, monkeypatch) -> None:
    base_context = make_context()
    tree = cp.EpicTree(
        schemaVersion="2.0",
        treeId="12345678-1234-5678-1234-567812345678",
        epic=base_context.tree.epic,
    )
    mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
    mapping_path = tmp_path / "mapping.json"
    context = cp._PreflightContext(
        tree=tree,
        provider=base_context.provider,
        provider_name="github",
        provider_target="owner/repo",
        node_index=cp._build_node_index(tree),
        mapping_document=mapping_document,
        mapping_path=mapping_path,
    )

    def link_subissue(parent_id, child_id, *, dry_run=False):
        return ProviderLinkResult(f"normalized-{parent_id}", f"normalized-{child_id}", "linked")

    monkeypatch.setattr(context.provider, "link_subissue", link_subissue)

    cp._link_operations(context, {"e1": "parent", "f1": "child", "s1": "one", "s2": "two"})

    relationship = mapping_document["entries"]["link_subissue:e1:f1"]
    assert relationship["source_provider_id"] == "normalized-parent"
    assert relationship["target_provider_id"] == "normalized-child"
    persisted = json.loads(mapping_path.read_text(encoding="utf-8"))
    assert persisted["entries"]["link_subissue:e1:f1"]["source_provider_id"] == "normalized-parent"
    assert persisted["entries"]["link_subissue:e1:f1"]["target_provider_id"] == "normalized-child"


def test_link_operations_reconciles_existing_hierarchy_links() -> None:
    context = make_context()
    ordered_refs = cp._build_execution_order(context)
    ref_to_id, create_operations = cp._create_issue_operations(context, ordered_refs)
    existing_operations = tuple(
        replace(
            operation,
            status="existing",
            result=(
                replace(operation.result, status="existing", hierarchy_link_result=None)
                if isinstance(operation.result, ProviderIssueResult)
                else operation.result
            ),
        )
        for operation in create_operations
    )
    context.provider._parent_child.clear()

    linked = cp._link_operations(context, ref_to_id, prior_operations=existing_operations)
    preview = cp._link_operations(context, ref_to_id, dry_run=True, prior_operations=existing_operations)

    assert len(linked) == 3
    assert all(operation.status == "linked" for operation in linked)
    assert all(operation.status == "dry-run" for operation in preview)


def test_link_operations_skips_children_created_with_parent_link() -> None:
    context = make_context()
    ordered_refs = cp._build_execution_order(context)
    ref_to_id, create_operations = cp._create_issue_operations(context, ordered_refs)

    linked = cp._link_operations(context, ref_to_id, prior_operations=tuple(create_operations))

    assert linked == []


def test_link_operations_skips_relationships_already_reconciled() -> None:
    context = make_context()
    ordered_refs = cp._build_execution_order(context)
    ref_to_id, _ = cp._create_issue_operations(context, ordered_refs)
    completed = cp.OperationDescriptor(
        operation_type="link_subissue",
        orchestration_key="completed",
        refs=("e1", "f1"),
        status="linked",
        provider_params={},
    )

    linked = cp._link_operations(context, ref_to_id, prior_operations=(completed,))

    assert ("e1", "f1") not in [operation.refs for operation in linked]


def test_link_operations_dry_run_describes_links_without_resolved_ids() -> None:
    context = make_context()

    preview = cp._link_operations(context, {}, dry_run=True)

    assert [operation.refs for operation in preview] == [("e1", "f1"), ("f1", "s1"), ("f1", "s2")]
    assert all(operation.status == "dry-run" for operation in preview)


def test_link_operations_live_skips_links_without_resolved_ids() -> None:
    context = make_context()

    linked = cp._link_operations(context, {"e1": "1"}, dry_run=False)

    assert linked == []


class _FailingLinkProvider:
    def __init__(self) -> None:
        self._next_id = 0

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
        self._next_id += 1
        identifier = str(self._next_id)
        hierarchy_link_result = ProviderLinkResult(parent_id, identifier, "linked") if parent_id is not None else None
        return ProviderIssueResult(
            identifier=identifier,
            url=f"u/{self._next_id}",
            status="created",
            hierarchy_link_result=hierarchy_link_result,
        )

    def link_subissue(self, parent_id, child_id, *, dry_run=False):
        raise RuntimeError("link failed")


def test_link_operations_wraps_provider_failures_in_pipeline_error() -> None:
    context = make_context()
    provider = _FailingLinkProvider()
    context = context.__class__(
        tree=context.tree,
        provider=provider,
        provider_name=context.provider_name,
        node_index=context.node_index,
    )
    ordered_refs = cp._build_execution_order(context)
    ref_to_id, create_operations = cp._create_issue_operations(context, ordered_refs)
    existing_operations = tuple(
        replace(
            operation,
            status="existing",
            result=(
                replace(operation.result, status="existing", hierarchy_link_result=None)
                if isinstance(operation.result, ProviderIssueResult)
                else operation.result
            ),
        )
        for operation in create_operations
    )

    with pytest.raises(cp.PipelineExecutionError) as exc_info:
        cp._link_operations(context, ref_to_id, prior_operations=existing_operations)

    assert exc_info.value.operation_type == "link_subissue"
    assert exc_info.value.refs == ("e1", "f1")
    assert [operation.operation_type for operation in exc_info.value.partial_plan.operations] == [
        "create_issue",
        "create_issue",
        "create_issue",
        "create_issue",
    ]


class _PipelineErrorLinkProvider(_FailingLinkProvider):
    def link_subissue(self, parent_id, child_id, *, dry_run=False):
        raise cp.PipelineExecutionError(
            cause=RuntimeError("nested"),
            operation_type="create_issue",
            refs=("nested",),
            stage="create_issue",
            created_result=None,
            partial_plan=OperationPlan(operations=(), dry_run=False, check_existing=False),
        )


def test_link_operations_preserves_provider_pipeline_errors() -> None:
    context = make_context()
    provider = _PipelineErrorLinkProvider()
    context = context.__class__(
        tree=context.tree,
        provider=provider,
        provider_name=context.provider_name,
        node_index=context.node_index,
    )
    ordered_refs = cp._build_execution_order(context)
    ref_to_id, create_operations = cp._create_issue_operations(context, ordered_refs)
    existing_operations = tuple(
        replace(
            operation,
            status="existing",
            result=(
                replace(operation.result, status="existing", hierarchy_link_result=None)
                if isinstance(operation.result, ProviderIssueResult)
                else operation.result
            ),
        )
        for operation in create_operations
    )

    with pytest.raises(cp.PipelineExecutionError) as exc_info:
        cp._link_operations(context, ref_to_id, prior_operations=existing_operations)

    assert exc_info.value.operation_type == "create_issue"
    assert exc_info.value.refs == ("nested",)
