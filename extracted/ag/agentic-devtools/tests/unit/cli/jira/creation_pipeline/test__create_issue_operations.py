"""Tests for ``_create_issue_operations`` (T028, T046)."""

from __future__ import annotations

import json

import pytest

import agentic_devtools.cli.jira.creation_pipeline as cp
from agentic_devtools.adapters.exceptions import HierarchyLinkError
from agentic_devtools.adapters.issue_provider import DefinitiveCreationFailure, ProviderIssueResult, ProviderLinkResult
from agentic_devtools.adapters.orchestration_key import generate_orchestration_key
from agentic_devtools.cli.workflows.create_epic.records import initialize_mapping_document

from .conftest import make_context, make_tree


class TestCreateIssueOperationsOrchestrationKeyScoping:
    """Provider-visible idempotency keys must be scoped by treeId."""

    def test_new_ref_key_is_scoped_by_tree_id(self):
        tree_id = "12345678-1234-5678-1234-567812345678"
        tree = cp.EpicTree(schemaVersion="2.0", treeId=tree_id, epic=make_tree().epic)
        ctx = make_context(tree)
        order = cp._build_execution_order(ctx)
        _, descriptors = cp._create_issue_operations(ctx, order, dry_run=False)
        create_ops = {d.refs[0]: d for d in descriptors if d.operation_type == "create_issue"}
        unscoped_key = generate_orchestration_key("create_issue", "e1")
        scoped_key = generate_orchestration_key("create_issue", tree_id, "e1")
        assert create_ops["e1"].orchestration_key == scoped_key
        assert create_ops["e1"].orchestration_key != unscoped_key

    def test_same_ref_in_different_trees_yields_different_keys(self):
        tree_id_a = "12345678-1234-5678-1234-567812345678"
        tree_id_b = "87654321-4321-8765-4321-876543218765"
        tree_a = cp.EpicTree(schemaVersion="2.0", treeId=tree_id_a, epic=make_tree().epic)
        tree_b = cp.EpicTree(schemaVersion="2.0", treeId=tree_id_b, epic=make_tree().epic)
        ctx_a = make_context(tree_a)
        ctx_b = make_context(tree_b)
        _, descriptors_a = cp._create_issue_operations(ctx_a, cp._build_execution_order(ctx_a), dry_run=False)
        _, descriptors_b = cp._create_issue_operations(ctx_b, cp._build_execution_order(ctx_b), dry_run=False)
        key_a = next(d.orchestration_key for d in descriptors_a if d.refs == ("e1",))
        key_b = next(d.orchestration_key for d in descriptors_b if d.refs == ("e1",))
        assert key_a != key_b

    def test_schema_v1_tree_without_tree_id_keeps_unscoped_key(self):
        # The operation descriptor retains the fallback key, but providers do
        # not receive it because it is not scoped to a tree identity.
        tree = make_tree()
        assert tree.treeId is None
        ctx = make_context(tree)
        order = cp._build_execution_order(ctx)
        _, descriptors = cp._create_issue_operations(ctx, order, dry_run=False)
        create_ops = {d.refs[0]: d for d in descriptors if d.operation_type == "create_issue"}
        assert create_ops["e1"].orchestration_key == generate_orchestration_key("create_issue", "e1")
        assert ctx.provider._idempotency_keys == {}


class TestCreateIssueOperationsHappyPath:
    def test_relationship_mapping_entries_are_not_treated_as_node_entries(self):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        base_context = make_context(tree)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["link_subissue:e1:f1"] = {
            "status": "pending",
            "operation_type": "link_subissue",
            "source_ref": "e1",
            "target_ref": "f1",
            "source_provider_id": "1",
            "target_provider_id": None,
            "pending_since": "2026-01-01T00:00:00Z",
        }
        context = cp._PreflightContext(
            tree=tree,
            provider=base_context.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=base_context.node_index,
            mapping_document=mapping_document,
        )

        _, operations = cp._create_issue_operations(context, cp._build_execution_order(context))

        assert [operation.refs for operation in operations] == [("e1",), ("f1",), ("s1",), ("s2",)]

    def test_creates_all_nodes_in_order_with_parent_links(self, in_memory_context):
        order = cp._build_execution_order(in_memory_context)
        ref_to_id, descriptors = cp._create_issue_operations(in_memory_context, order, dry_run=False)
        # Every ordered ref got an id and a descriptor.
        assert set(ref_to_id) == set(order)
        assert [d.refs for d in descriptors] == [(ref,) for ref in order]
        assert all(d.operation_type == "create_issue" for d in descriptors)
        assert all(d.status == "created" for d in descriptors)

    def test_child_receives_parent_identifier(self):
        tree = make_tree(with_blocking=False)
        ctx = make_context(tree)
        order = cp._build_execution_order(ctx)
        ref_to_id, _ = cp._create_issue_operations(ctx, order, dry_run=False)
        provider = ctx.provider
        f1_record = provider._issues[ref_to_id["f1"]]
        assert f1_record["parent_id"] == ref_to_id["e1"]
        s1_record = provider._issues[ref_to_id["s1"]]
        assert s1_record["parent_id"] == ref_to_id["f1"]

    def test_issue_creation_and_execution_require_constructed_provider(self):
        base_context = make_context(make_tree(with_blocking=False))
        context = cp._PreflightContext(
            tree=base_context.tree,
            provider=None,
            provider_name=base_context.provider_name,
            node_index=base_context.node_index,
        )

        with pytest.raises(cp.PipelineValidationError, match="Provider construction was not completed"):
            cp._create_issue_operations(context, cp._build_execution_order(context))
        with pytest.raises(cp.PipelineValidationError, match="Provider construction was not completed"):
            cp._execute_creation_plan(context, dry_run=False)
        with pytest.raises(cp.PipelineValidationError, match="Provider construction was not completed"):
            cp._link_operations(context, {})
        with pytest.raises(cp.PipelineValidationError, match="Provider construction was not completed"):
            cp._blocking_operations(context, {})

    def test_legacy_string_mapping_entry_is_reused_without_dry_run_mutation(self):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        existing = ctx.provider.create_issue("Existing", "body", "epic")
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = existing.identifier
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
        )

        cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=True)

        assert len(ctx.provider.issues) == 1
        assert mapping_document["entries"]["e1"] == existing.identifier

    @pytest.mark.parametrize("status", ["created", "trusted-match"])
    def test_created_mapping_status_requires_identifier_before_mutation(self, status):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {"status": status}
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
        )

        with pytest.raises(cp.PipelineValidationError, match=f"status {status!r} requires a provider identifier"):
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert ctx.provider.issues == {}


class TestCreateIssueOperationsDryRun:
    def test_dry_run_creates_nothing_and_leaves_ids_empty(self, in_memory_context):
        order = cp._build_execution_order(in_memory_context)
        ref_to_id, descriptors = cp._create_issue_operations(in_memory_context, order, dry_run=True)
        assert ref_to_id == {}
        assert all(d.status == "dry-run" for d in descriptors)
        assert all(d.result is None for d in descriptors)
        # No issues persisted in the provider store.
        assert in_memory_context.provider._issues == {}

    def test_initializes_mapping_before_first_live_mutation(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree().epic,
        )
        ctx = make_context(tree)
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_path=tmp_path / "mapping.json",
        )

        cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        document = json.loads((tmp_path / "mapping.json").read_text(encoding="utf-8"))
        assert document["provider"] == {"name": "github", "target": "owner/repo"}
        assert set(document["entries"]) == {
            "e1",
            "f1",
            "s1",
            "s2",
            "link_subissue:e1:f1",
            "link_subissue:f1:s1",
            "link_subissue:f1:s2",
        }

    def test_pending_mapping_entry_reuses_existing_issue_via_orchestration_key(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        key = generate_orchestration_key("create_issue", tree.treeId, "e1")
        existing = ctx.provider.create_issue("Epic", "b", "epic", idempotency_key=key)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {
            "status": "pending",
            "pending_since": "2026-01-01T00:00:00Z",
        }
        mapping_path = tmp_path / "mapping.json"
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=mapping_path,
        )

        ref_to_id, descriptors = cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert ref_to_id["e1"] == existing.identifier
        assert descriptors[0].status == "existing"
        assert descriptors[0].orchestration_key == key
        assert len(ctx.provider.issues) == 4
        persisted = json.loads(mapping_path.read_text(encoding="utf-8"))
        assert persisted["entries"]["e1"]["provider_id"] == existing.identifier

    def test_start_from_counts_skipped_prefix_nodes(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        for ref in ("e1", "f1", "s1", "s2"):
            issue = ctx.provider.create_issue(ref, "body", "task")
            mapping_document["entries"][ref] = {"provider_id": issue.identifier, "status": "created"}
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            start_from="s2",
            mapping_document=mapping_document,
            mapping_path=tmp_path / "mapping.json",
        )

        _, descriptors = cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert len(descriptors) == 6
        assert [descriptor.operation_type for descriptor in descriptors] == [
            "resume_skip",
            "resume_skip",
            "resume_skip",
            "link_subissue",
            "link_subissue",
            "create_issue",
        ]

    @pytest.mark.parametrize("dry_run", [False, True])
    def test_start_from_requires_mapped_identifiers_for_skipped_prerequisites(self, tmp_path, dry_run):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree().epic,
        )
        ctx = make_context(tree)
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            node_index=ctx.node_index,
            start_from="s1",
            mapping_path=tmp_path / "mapping.json",
        )

        with pytest.raises(cp.PipelineValidationError, match="skipped prerequisite refs: e1, f1"):
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=dry_run)
        assert ctx.mapping_path is not None
        assert not ctx.mapping_path.exists()


class TestCreateIssueOperationsMappingResolution:
    """Comment 2 (PR #4200 review): not-found vs. indeterminate resolve_identifier failures."""

    @pytest.mark.parametrize(
        ("call_outcome", "expected_status"),
        [("created", "created"), ("existing", "trusted-match")],
    )
    def test_promotes_pending_identifier_before_reusing_it(self, tmp_path, call_outcome, expected_status):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        existing = ctx.provider.create_issue("Epic", "b", "epic")
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {
            "status": "pending",
            "provider_id": existing.identifier,
            "call_outcome": call_outcome,
            "pending_since": "2026-01-01T00:00:00Z",
        }
        mapping_path = tmp_path / "mapping.json"
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=mapping_path,
        )

        ref_to_id, descriptors = cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert ref_to_id["e1"] == existing.identifier
        assert next(d for d in descriptors if d.refs == ("e1",)).status == "existing"
        assert mapping_document["entries"]["e1"] == {
            "provider_id": existing.identifier,
            "status": expected_status,
            **({"match_basis": "create-existing-response"} if expected_status == "trusted-match" else {}),
        }
        assert json.loads(mapping_path.read_text(encoding="utf-8"))["entries"]["e1"]["status"] == expected_status

    def test_dry_run_does_not_persist_pending_mapping_promotion(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        existing = ctx.provider.create_issue("Epic", "b", "epic")
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {
            "status": "pending",
            "provider_id": existing.identifier,
            "call_outcome": "created",
            "pending_since": "2026-01-01T00:00:00Z",
        }
        mapping_path = tmp_path / "mapping.json"
        mapping_path.write_text(json.dumps(mapping_document), encoding="utf-8")
        original = mapping_path.read_bytes()
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=mapping_path,
        )

        cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=True)

        assert mapping_path.read_bytes() == original
        assert mapping_document["entries"]["e1"]["status"] == "created"

    def test_rejects_unrecognized_mapping_status(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        existing = ctx.provider.create_issue("Unrelated", "b", "epic")
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {"identifier": existing.identifier, "status": "invalid"}
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=tmp_path / "mapping.json",
        )

        with pytest.raises(cp.PipelineValidationError, match="unrecognized status 'invalid'"):
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert len(ctx.provider.issues) == 1

    def test_failed_mapping_status_allows_fresh_creation(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {"status": "failed"}
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=tmp_path / "mapping.json",
        )

        ref_to_id, descriptors = cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert ref_to_id["e1"]
        assert next(d for d in descriptors if d.refs == ("e1",)).status == "created"

    def test_failed_mapping_uses_precreate_lookup_for_uncertain_retry(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        key = generate_orchestration_key("create_issue", tree.treeId, "e1")
        lookup_calls: list[str] = []
        create_lookups = []
        original_create = ctx.provider.create_issue

        def find_existing_issue(orchestration_key):
            lookup_calls.append(orchestration_key)
            return None

        def create_issue(title, *args, **kwargs):
            create_lookups.append(kwargs.get("precreate_lookup"))
            return original_create(title, *args, **kwargs)

        ctx.provider.find_existing_issue = find_existing_issue  # type: ignore[attr-defined]
        ctx.provider.create_issue = create_issue
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {"status": "failed", "error": "previous failure"}
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=tmp_path / "mapping.json",
        )

        cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert key in lookup_calls
        lookup = next(item for item in create_lookups if item is not None and item.node_ref == "e1")
        assert lookup.issue is None
        assert lookup.orchestration_key == key
        assert lookup.legacy_orchestration_key == generate_orchestration_key("create_issue", "e1")
        assert lookup.legacy_adoption_permitted is False

    def test_provider_without_precreate_lookup_capability_keeps_original_create_contract(self):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        lookups: list[str] = []
        original_create = ctx.provider.create_issue

        def find_existing_issue(orchestration_key):
            lookups.append(orchestration_key)
            return None

        def legacy_create_issue(
            title,
            body,
            issue_type,
            *,
            parent_id=None,
            labels=None,
            idempotency_key=None,
            dry_run=False,
        ):
            return original_create(
                title,
                body,
                issue_type,
                parent_id=parent_id,
                labels=labels,
                idempotency_key=idempotency_key,
                dry_run=dry_run,
            )

        ctx.provider.find_existing_issue = find_existing_issue  # type: ignore[attr-defined]
        ctx.provider.create_issue = legacy_create_issue
        ctx.provider.create_issue_with_precreate_lookup = None  # type: ignore[attr-defined]
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=initialize_mapping_document(tree, "github", "owner/repo"),
        )

        ref_to_id, _ = cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert lookups
        assert ref_to_id["e1"]

    def test_does_not_reuse_pending_identifier_without_call_outcome(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        existing = ctx.provider.create_issue("Unrelated", "b", "epic")
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {"identifier": existing.identifier, "status": "pending"}
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_path=tmp_path / "mapping.json",
            mapping_document=mapping_document,
        )

        ref_to_id, descriptors = cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert ref_to_id["e1"] != existing.identifier
        assert next(d for d in descriptors if d.refs == ("e1",)).status == "created"

    def test_promotes_pending_identifier_in_memory_without_mapping_path(self):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        existing = ctx.provider.create_issue("Epic", "b", "epic")
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {
            "identifier": existing.identifier,
            "status": "pending",
            "call_outcome": "created",
        }
        for ref in ("f1", "s1", "s2"):
            issue = ctx.provider.create_issue(ref, "b", "task")
            mapping_document["entries"][ref] = {"provider_id": issue.identifier, "status": "created"}
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
        )

        cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert mapping_document["entries"]["e1"]["status"] == "created"

    def test_reuses_verified_mapped_result_without_second_lookup(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        existing = ctx.provider.create_issue("Epic", "b", "epic")
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {"provider_id": existing.identifier, "status": "created"}
        resolve_calls: list[tuple[str, bool]] = []
        original_resolve = ctx.provider.resolve_identifier

        def _track_resolve(identifier: str, *, dry_run: bool = False) -> ProviderIssueResult:
            resolve_calls.append((identifier, dry_run))
            return original_resolve(identifier, dry_run=dry_run)

        ctx.provider.resolve_identifier = _track_resolve  # type: ignore[method-assign]
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=tmp_path / "mapping.json",
        )

        ref_to_id, descriptors = cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert resolve_calls == [(existing.identifier, False)]
        assert ref_to_id["e1"] == existing.identifier
        descriptor = next(d for d in descriptors if d.refs == ("e1",))
        assert descriptor.status == "existing"
        assert descriptor.result is not None
        assert descriptor.result.identifier == existing.identifier

    def test_not_found_mapping_fails_closed_without_recreating(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {"identifier": "does-not-exist"}
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=tmp_path / "mapping.json",
        )

        with pytest.raises(cp.PipelineValidationError, match="no longer exists"):
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)
        assert len(ctx.provider.issues) == 0

    def test_indeterminate_lookup_failure_propagates(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {"identifier": "e-1"}

        error = ValueError("Unexpected response type from provider API: list")

        def _raise_malformed(identifier: str, *, dry_run: bool = False) -> object:
            raise error

        ctx.provider.resolve_identifier = _raise_malformed  # type: ignore[method-assign]
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=tmp_path / "mapping.json",
        )

        with pytest.raises(cp.PipelineValidationError, match="Could not resolve mapped provider issue") as exc_info:
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)
        assert exc_info.value.cause is error

    def test_malformed_lookup_result_is_wrapped_as_validation_error(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {"identifier": "e-1"}
        ctx.provider.resolve_identifier = lambda identifier, *, dry_run=False: None  # type: ignore[method-assign]
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=tmp_path / "mapping.json",
        )

        with pytest.raises(cp.PipelineValidationError, match="Could not resolve mapped provider issue") as exc_info:
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)
        assert isinstance(exc_info.value.cause, TypeError)

    @pytest.mark.parametrize(
        ("resolved_identifier", "normalized_identifier"),
        [("", "canonical-id"), ("e-1", "")],
    )
    def test_empty_lookup_identifiers_are_wrapped_as_validation_errors(
        self, tmp_path, resolved_identifier, normalized_identifier
    ):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {"identifier": "e-1"}
        ctx.provider.resolve_identifier = lambda *_args, **_kwargs: ProviderIssueResult(
            identifier=resolved_identifier,
            url="",
            status="existing",
        )  # type: ignore[method-assign]
        ctx.provider.normalize_identifier = lambda _identifier: normalized_identifier  # type: ignore[method-assign]
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=tmp_path / "mapping.json",
        )

        with pytest.raises(cp.PipelineValidationError, match="Could not resolve mapped provider issue") as exc_info:
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)
        assert isinstance(exc_info.value.cause, ValueError)

    def test_recovers_pending_entry_by_key_before_creating(self, tmp_path, monkeypatch):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        key = generate_orchestration_key("create_issue", tree.treeId, "e1")
        existing = ctx.provider.create_issue("Existing", "body", "epic")
        calls: list[str] = []

        def find_existing_issue(orchestration_key):
            calls.append(orchestration_key)
            return existing if calls.count(key) == 3 and orchestration_key == key else None

        ctx.provider.find_existing_issue = find_existing_issue  # type: ignore[attr-defined]
        monkeypatch.setattr(cp.time, "sleep", lambda _seconds: None)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {"status": "pending", "pending_since": "2026-01-01T00:00:00Z"}
        mapping_path = tmp_path / "mapping.json"
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=mapping_path,
        )

        ref_to_id, descriptors = cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert calls.count(key) == 3
        assert ref_to_id["e1"] == "1"
        assert next(d for d in descriptors if d.refs == ("e1",)).status == "existing"
        assert mapping_document["entries"]["e1"] == {
            "provider_id": "1",
            "status": "trusted-match",
            "match_basis": "pending-confirmation-unresolved",
        }

    def test_unresolved_pending_entry_fails_closed_without_creating(self, tmp_path, monkeypatch):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        ctx.provider.find_existing_issue = lambda _key: None  # type: ignore[attr-defined]
        monkeypatch.setattr(cp.time, "sleep", lambda _seconds: None)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {"status": "pending", "pending_since": "2026-01-01T00:00:00Z"}
        original = json.loads(json.dumps(mapping_document))
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=tmp_path / "mapping.json",
        )

        with pytest.raises(cp.PipelineValidationError, match="--force-resume"):
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert ctx.provider.issues == {}
        assert mapping_document == original

    @pytest.mark.parametrize("dry_run", [False, True])
    def test_fresh_pending_entry_does_not_allow_forced_retry(self, tmp_path, monkeypatch, dry_run):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        key = generate_orchestration_key("create_issue", tree.treeId, "e1")
        lookup_calls = []

        def find_existing_issue(orchestration_key):
            lookup_calls.append(orchestration_key)
            return None

        ctx.provider.find_existing_issue = find_existing_issue  # type: ignore[attr-defined]
        monkeypatch.setattr(cp.time, "sleep", lambda _seconds: None)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {
            "status": "pending",
            "pending_since": cp._utc_timestamp(),
            "orchestrationKey": key,
        }
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
        )
        original = json.loads(json.dumps(mapping_document))

        with pytest.raises(cp.PipelineValidationError, match="No issue was created"):
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=dry_run, force_resume=True)

        assert lookup_calls == [key] * cp._PENDING_RECOVERY_ATTEMPTS
        assert ctx.provider.issues == {}
        assert mapping_document == original

    @pytest.mark.parametrize("threshold", ["0", "invalid"])
    def test_invalid_stale_threshold_fails_closed(self, tmp_path, monkeypatch, threshold):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        key = generate_orchestration_key("create_issue", tree.treeId, "e1")
        ctx.provider.find_existing_issue = lambda _key: None  # type: ignore[attr-defined]
        monkeypatch.setattr(cp.time, "sleep", lambda _seconds: None)
        monkeypatch.setenv("AGDT_STALE_LOCK_THRESHOLD_MINUTES", threshold)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {
            "status": "pending",
            "pending_since": "2000-01-01T00:00:00Z",
            "orchestrationKey": key,
        }
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
        )

        with pytest.raises(cp.PipelineValidationError, match="AGDT_STALE_LOCK_THRESHOLD_MINUTES"):
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx))

        assert ctx.provider.issues == {}

    def test_stale_pending_lookup_exception_fails_without_creating(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        key = generate_orchestration_key("create_issue", tree.treeId, "e1")

        def find_existing_issue(_key):
            raise RuntimeError("lookup unavailable")

        ctx.provider.find_existing_issue = find_existing_issue  # type: ignore[attr-defined]
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {
            "status": "pending",
            "pending_since": "2000-01-01T00:00:00Z",
            "orchestrationKey": key,
        }
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
        )

        with pytest.raises(cp.PipelineValidationError, match="Could not reconcile"):
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx), force_resume=True)

        assert ctx.provider.issues == {}

    @pytest.mark.parametrize(
        "pending_since",
        ["2000-01-01T00:00:00Z", "invalidZ", "2099-01-01T00:00:00Z", "2026-01-01Z", None],
    )
    @pytest.mark.parametrize("dry_run", [False, True])
    def test_stale_pending_entry_requires_force_resume_after_settling(
        self, tmp_path, monkeypatch, pending_since, dry_run
    ):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        key = generate_orchestration_key("create_issue", tree.treeId, "e1")
        lookup_calls: list[str] = []

        def find_existing_issue(orchestration_key):
            lookup_calls.append(orchestration_key)
            return None

        ctx.provider.find_existing_issue = find_existing_issue  # type: ignore[attr-defined]
        monkeypatch.setattr(cp.time, "sleep", lambda _seconds: None)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        pending_entry = {
            "status": "pending",
            "orchestrationKey": key,
        }
        if pending_since is not None:
            pending_entry["pending_since"] = pending_since
        mapping_document["entries"]["e1"] = pending_entry
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=tmp_path / "mapping.json",
        )
        original = json.loads(json.dumps(mapping_document))

        with pytest.raises(cp.PipelineValidationError, match="--force-resume"):
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=dry_run)

        assert lookup_calls == [key] * cp._PENDING_RECOVERY_ATTEMPTS
        assert ctx.provider.issues == {}
        assert mapping_document == original

    @pytest.mark.parametrize("pending_since", ["2000-01-01T00:00:00Z", "2026-01-01Z"])
    def test_force_resume_retries_stale_pending_entry_once(self, tmp_path, monkeypatch, pending_since):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        key = generate_orchestration_key("create_issue", tree.treeId, "e1")
        lookup_calls: list[str] = []
        create_calls: list[str] = []
        create_lookups = []
        original_create = ctx.provider.create_issue

        def find_existing_issue(orchestration_key):
            lookup_calls.append(orchestration_key)
            return None

        def create_issue(title, *args, **kwargs):
            create_calls.append(title)
            create_lookups.append((title, kwargs.get("precreate_lookup")))
            return original_create(title, *args, **kwargs)

        ctx.provider.find_existing_issue = find_existing_issue  # type: ignore[attr-defined]
        ctx.provider.create_issue = create_issue
        monkeypatch.setattr(cp.time, "sleep", lambda _seconds: None)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {
            "status": "pending",
            "pending_since": pending_since,
            "orchestrationKey": key,
        }
        mapping_path = tmp_path / "mapping.json"
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=mapping_path,
        )

        ref_to_id, _ = cp._create_issue_operations(
            ctx, cp._build_execution_order(ctx), dry_run=False, force_resume=True
        )

        assert lookup_calls.count(key) == cp._PENDING_RECOVERY_ATTEMPTS
        assert create_calls.count("Epic") == 1
        lookup = next(item for title, item in create_lookups if title == "Epic")
        assert lookup.issue is None
        assert ref_to_id["e1"]
        assert json.loads(mapping_path.read_text(encoding="utf-8"))["entries"]["e1"] == {
            "provider_id": ref_to_id["e1"],
            "status": "created",
        }

    def test_dry_run_force_resume_previews_stale_pending_entry_without_mutations(self, tmp_path, monkeypatch):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        key = generate_orchestration_key("create_issue", tree.treeId, "e1")
        lookup_calls = []
        ctx.provider.find_existing_issue = lambda orchestration_key: lookup_calls.append(orchestration_key)  # type: ignore[attr-defined]
        monkeypatch.setattr(cp.time, "sleep", lambda _seconds: None)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {
            "status": "pending",
            "pending_since": "invalid",
            "orchestrationKey": key,
        }
        original = json.loads(json.dumps(mapping_document))
        mapping_path = tmp_path / "mapping.json"
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=mapping_path,
        )

        _, descriptors = cp._create_issue_operations(
            ctx, cp._build_execution_order(ctx), dry_run=True, force_resume=True
        )

        assert lookup_calls == [key] * cp._PENDING_RECOVERY_ATTEMPTS
        assert all(descriptor.status == "dry-run" for descriptor in descriptors)
        assert ctx.provider.issues == {}
        assert mapping_document == original
        assert not mapping_path.exists()

    def test_force_resume_normalizes_multiple_bad_timestamps_before_prefix_reconciliation(self, tmp_path, monkeypatch):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        existing_epic = ctx.provider.create_issue("Epic", "b", "epic")
        existing_feature = ctx.provider.create_issue("Feature", "b", "feature")
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {"provider_id": existing_epic.identifier, "status": "created"}
        mapping_document["entries"]["f1"] = {"provider_id": existing_feature.identifier, "status": "created"}
        mapping_document["entries"]["s1"] = {"status": "pending", "pending_since": "invalid"}
        mapping_document["entries"]["s2"] = {"status": "pending"}
        mapping_path = tmp_path / "mapping.json"
        writes = []
        original_write = cp.atomic_write_mapping_document

        def write_mapping(path, document):
            writes.append(json.loads(json.dumps(document)))
            return original_write(path, document)

        monkeypatch.setattr(cp, "atomic_write_mapping_document", write_mapping)
        ctx.provider.find_existing_issue = lambda _key: None  # type: ignore[attr-defined]
        monkeypatch.setattr(cp.time, "sleep", lambda _seconds: None)
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            start_from="s1",
            mapping_document=mapping_document,
            mapping_path=mapping_path,
        )

        cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False, force_resume=True)

        assert writes
        assert all(
            isinstance(entry.get("pending_since"), str) and entry["pending_since"].endswith("Z")
            for document in writes
            for entry in document["entries"].values()
            if isinstance(entry, dict) and entry.get("status") == "pending"
        )

    def test_unmapped_node_settles_before_creation(self, tmp_path, monkeypatch):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        key = generate_orchestration_key("create_issue", tree.treeId, "e1")
        events: list[str] = []
        delays: list[float] = []
        original_create = ctx.provider.create_issue

        def find_existing_issue(orchestration_key):
            if orchestration_key == key:
                events.append("lookup")
            return None

        def create_issue(title, *args, **kwargs):
            if title == "Epic":
                events.append("create")
                lookup = kwargs.get("precreate_lookup")
                assert lookup.orchestration_key == key
                assert lookup.issue is None
            return original_create(title, *args, **kwargs)

        ctx.provider.find_existing_issue = find_existing_issue  # type: ignore[attr-defined]
        ctx.provider.create_issue = create_issue
        monkeypatch.setattr(cp.time, "sleep", delays.append)
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=initialize_mapping_document(tree, "github", "owner/repo"),
            mapping_path=tmp_path / "mapping.json",
        )

        cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert events == ["lookup"] * cp._PRECREATE_SETTLING_ATTEMPTS + ["create"]
        assert delays[:4] == pytest.approx([0.1, 0.2, 0.4, 0.8])

    def test_unmapped_node_stops_settling_when_lookup_finds_issue(self, tmp_path, monkeypatch):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        existing = ctx.provider.create_issue("Epic", "body", "epic")
        key = generate_orchestration_key("create_issue", tree.treeId, "e1")
        lookups: list[str] = []

        def find_existing_issue(orchestration_key):
            if orchestration_key == key:
                lookups.append(orchestration_key)
                return existing if len(lookups) == 3 else None
            return None

        delays: list[float] = []
        ctx.provider.find_existing_issue = find_existing_issue  # type: ignore[attr-defined]
        monkeypatch.setattr(cp.time, "sleep", delays.append)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=tmp_path / "mapping.json",
        )

        ref_to_id, descriptors = cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert lookups == [key] * 3
        assert delays[:2] == pytest.approx([0.1, 0.2])
        assert ref_to_id["e1"] == existing.identifier
        assert sum(issue["title"] == "Epic" for issue in ctx.provider.issues.values()) == 1
        assert mapping_document["entries"]["e1"] == {
            "provider_id": existing.identifier,
            "status": "trusted-match",
            "match_basis": "pre-create-guard",
        }
        assert next(descriptor for descriptor in descriptors if descriptor.refs == ("e1",)).status == "existing"

    def test_prefix_relationship_failure_precedes_suffix_creation(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        mapped_ids = {ref: ctx.provider.create_issue(ref, "body", "epic").identifier for ref in ("e1", "f1")}
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"].update(
            {ref: {"provider_id": identifier, "status": "created"} for ref, identifier in mapped_ids.items()}
        )

        def fail_link(parent_id, child_id, *, dry_run=False):
            raise RuntimeError("prefix link failed")

        ctx.provider.link_subissue = fail_link  # type: ignore[method-assign]
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=tmp_path / "mapping.json",
            start_from="s1",
        )

        with pytest.raises(cp.PipelineExecutionError, match="prefix link failed"):
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert set(ctx.provider.issues) == set(mapped_ids.values())

    def test_unmapped_node_persists_precreate_match_without_creating_it(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        key = generate_orchestration_key("create_issue", tree.treeId, "e1")
        existing = ctx.provider.create_issue("Epic", "body", "epic", idempotency_key=key)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_path = tmp_path / "mapping.json"
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=mapping_path,
        )

        ref_to_id, descriptors = cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert ref_to_id["e1"] == existing.identifier
        assert next(d for d in descriptors if d.refs == ("e1",)).status == "existing"
        assert mapping_document["entries"]["e1"] == {
            "provider_id": existing.identifier,
            "status": "trusted-match",
            "match_basis": "pre-create-guard",
        }
        persisted = json.loads(mapping_path.read_text(encoding="utf-8"))
        assert persisted["entries"]["e1"] == mapping_document["entries"]["e1"]

    def test_unmapped_node_match_updates_in_memory_mapping_without_path(self):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        key = generate_orchestration_key("create_issue", tree.treeId, "e1")
        existing = ctx.provider.create_issue("Epic", "body", "epic", idempotency_key=key)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        for ref in ("f1", "s1", "s2"):
            mapped = ctx.provider.create_issue(ref, "body", "task")
            mapping_document["entries"][ref] = {
                "provider_id": mapped.identifier,
                "status": "created",
            }
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
        )

        ref_to_id, _ = cp._create_issue_operations(ctx, cp._build_execution_order(ctx))

        assert ref_to_id["e1"] == existing.identifier
        assert mapping_document["entries"]["e1"] == {
            "provider_id": existing.identifier,
            "status": "trusted-match",
            "match_basis": "pre-create-guard",
        }

    def test_unmapped_node_match_rejects_mapped_identifier_collision(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        key = generate_orchestration_key("create_issue", tree.treeId, "f1")
        existing = ctx.provider.create_issue("Existing", "body", "epic", idempotency_key=key)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {
            "provider_id": existing.identifier,
            "status": "created",
        }
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=tmp_path / "mapping.json",
        )

        with pytest.raises(cp.PipelineValidationError, match="same provider identifier"):
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx))

        assert "f1" not in mapping_document["entries"]
        assert len(ctx.provider.issues) == 1

    def test_existing_create_response_persists_canonical_terminal_entry(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        result_ids = iter(("epic-1", "feature-1", "subtask-1", "subtask-2"))

        def create_existing(*args, **kwargs):
            identifier = next(result_ids)
            parent_id = kwargs.get("parent_id")
            hierarchy_link_result = (
                ProviderLinkResult(parent_id, identifier, "already-linked") if parent_id is not None else None
            )
            return ProviderIssueResult(
                identifier=identifier,
                url=f"https://issues/{identifier}",
                status="existing",
                hierarchy_link_result=hierarchy_link_result,
            )

        ctx.provider.create_issue = create_existing
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=tmp_path / "mapping.json",
        )

        cp._create_issue_operations(ctx, cp._build_execution_order(ctx))

        assert mapping_document["entries"]["e1"] == {
            "provider_id": "epic-1",
            "status": "trusted-match",
            "match_basis": "create-existing-response",
        }
        assert mapping_document["entries"]["f1"] == {
            "provider_id": "feature-1",
            "status": "trusted-match",
            "match_basis": "create-existing-response",
        }
        assert mapping_document["entries"]["link_subissue:e1:f1"]["status"] == "confirmed"
        assert mapping_document["entries"]["link_subissue:e1:f1"]["result"] == "already-linked"

    def test_unmapped_node_lookup_failure_fails_closed(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        ctx.provider.find_existing_issue = None  # type: ignore[attr-defined]
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=tmp_path / "mapping.json",
        )

        with pytest.raises(cp.PipelineValidationError, match="cannot safely check"):
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx))

        assert ctx.provider.issues == {}

    def test_unmapped_node_lookup_error_fails_closed(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)

        def fail_lookup(_key):
            raise RuntimeError("lookup unavailable")

        ctx.provider.find_existing_issue = fail_lookup  # type: ignore[attr-defined]
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=initialize_mapping_document(tree, "github", "owner/repo"),
            mapping_path=tmp_path / "mapping.json",
        )

        with pytest.raises(cp.PipelineValidationError, match="Could not check whether"):
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx))

        assert ctx.provider.issues == {}

    def test_pending_entry_without_stored_key_uses_deterministic_recovery_key(self, tmp_path, monkeypatch):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        key = generate_orchestration_key("create_issue", tree.treeId, "e1")
        calls = []

        def find_existing_issue(orchestration_key):
            calls.append(orchestration_key)
            return None

        ctx.provider.find_existing_issue = find_existing_issue  # type: ignore[attr-defined]
        monkeypatch.setattr(cp.time, "sleep", lambda _seconds: None)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {
            "status": "pending",
            "pending_since": cp._utc_timestamp(),
        }
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=tmp_path / "mapping.json",
        )

        with pytest.raises(cp.PipelineValidationError, match="after 5 attempts"):
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert calls == [key] * 5
        assert ctx.provider.issues == {}

    def test_pending_entry_without_lookup_capability_fails_closed(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        ctx.provider.find_existing_issue = None  # type: ignore[attr-defined]
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {
            "status": "pending",
            "pending_since": cp._utc_timestamp(),
        }
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=tmp_path / "mapping.json",
        )

        with pytest.raises(cp.PipelineValidationError, match="safely recoverable"):
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert ctx.provider.issues == {}

    def test_pending_recovery_failure_fails_closed(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        key = generate_orchestration_key("create_issue", tree.treeId, "e1")

        def find_existing_issue(_key):
            raise RuntimeError("lookup unavailable")

        ctx.provider.find_existing_issue = find_existing_issue  # type: ignore[attr-defined]
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {"status": "pending", "orchestrationKey": key}
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=tmp_path / "mapping.json",
        )

        with pytest.raises(cp.PipelineValidationError, match="Could not reconcile"):
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert ctx.provider.issues == {}

    def test_rejects_mapping_identifier_collision_before_creation(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        ctx = make_context(tree)
        existing = ctx.provider.create_issue("Existing", "body", "epic")
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_document["entries"]["e1"] = {"provider_id": existing.identifier, "status": "created"}
        mapping_document["entries"]["f1"] = {"provider_id": existing.identifier, "status": "created"}
        original = json.loads(json.dumps(mapping_document))
        ctx = cp._PreflightContext(
            tree=tree,
            provider=ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=tmp_path / "mapping.json",
        )

        with pytest.raises(cp.PipelineValidationError, match="same provider identifier"):
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert len(ctx.provider.issues) == 1
        assert mapping_document == original


class TestCreateIssueOperationsPartialLink:
    """T046 — a partial hierarchy-link failure yields a ``partial-created`` op."""

    class _PartialLinkProvider:
        def __init__(self):
            self._n = 0

        def normalize_identifier(self, identifier):
            return identifier

        def find_existing_issue(self, _orchestration_key):
            return None

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
        order = cp._build_execution_order(ctx)
        with pytest.raises(cp.PipelineExecutionError) as exc_info:
            cp._create_issue_operations(ctx, order, dry_run=False)
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

    def test_partial_created_dry_run_does_not_promote_mapping(self):
        tree = make_tree(with_blocking=False)
        base_ctx = make_context(tree)
        mapping_document = initialize_mapping_document(
            "12345678-1234-5678-1234-567812345678",
            "github",
            "owner/repo",
        )
        ctx = cp._PreflightContext(
            tree=tree,
            provider=self._PartialLinkProvider(),
            provider_name="github",
            provider_target="owner/repo",
            node_index=base_ctx.node_index,
            mapping_document=mapping_document,
        )

        with pytest.raises(cp.PipelineExecutionError):
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=True)

        assert mapping_document["entries"] == {}

    def test_partial_created_identifier_is_persisted_before_raise(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        base_ctx = make_context(tree)
        ctx = cp._PreflightContext(
            tree=tree,
            provider=self._PartialLinkProvider(),
            provider_name="github",
            provider_target="owner/repo",
            node_index=base_ctx.node_index,
            mapping_document=initialize_mapping_document(tree, "github", "owner/repo"),
            mapping_path=tmp_path / "mapping.json",
        )

        with pytest.raises(cp.PipelineExecutionError):
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        persisted = json.loads((tmp_path / "mapping.json").read_text(encoding="utf-8"))
        assert persisted["entries"]["e1"] == {"provider_id": "1", "status": "created"}
        assert persisted["entries"]["f1"] == {"provider_id": "2", "status": "created"}
        assert persisted["entries"]["link_subissue:e1:f1"] == {
            "status": "pending",
            "operation_type": "link_subissue",
            "source_ref": "e1",
            "target_ref": "f1",
            "source_provider_id": "1",
            "target_provider_id": "2",
            "pending_since": persisted["entries"]["link_subissue:e1:f1"]["pending_since"],
        }
        assert persisted["entries"]["link_subissue:e1:f1"]["pending_since"].endswith("Z")

    def test_recovered_existing_identifier_is_persisted_as_trusted_match(self, tmp_path):
        class _RecoveredExistingLinkProvider(self._PartialLinkProvider):
            def create_issue(self, title, body, issue_type, **kwargs):
                if title == "F1":
                    recovered = ProviderIssueResult(identifier="2", url="u/2", status="existing")
                    raise HierarchyLinkError(
                        "parent link failed",
                        created_result=recovered,
                        stage="link_subissue",
                        cause=RuntimeError("link failed"),
                    )
                return super().create_issue(title, body, issue_type, **kwargs)

        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        base_ctx = make_context(tree)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_path = tmp_path / "mapping.json"
        context = cp._PreflightContext(
            tree=tree,
            provider=_RecoveredExistingLinkProvider(),
            provider_name="github",
            provider_target="owner/repo",
            node_index=base_ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=mapping_path,
        )

        with pytest.raises(cp.PipelineExecutionError):
            cp._create_issue_operations(context, cp._build_execution_order(context), dry_run=False)

        trusted_entry = {
            "provider_id": "2",
            "status": "trusted-match",
            "match_basis": "create-existing-response",
        }
        assert mapping_document["entries"]["f1"] == trusted_entry
        persisted = json.loads(mapping_path.read_text(encoding="utf-8"))
        assert persisted["entries"]["f1"] == trusted_entry

    def test_partial_created_identifier_collision_preserves_pending_entry(self, tmp_path):
        class _CollidingPartialLinkProvider(self._PartialLinkProvider):
            def create_issue(self, title, body, issue_type, **kwargs):
                if title == "F1":
                    partial = ProviderIssueResult(identifier="1", url="u/1", status="partial-created")
                    raise HierarchyLinkError(
                        "sub-issue link failed",
                        created_result=partial,
                        stage="link_subissue",
                        cause=RuntimeError("link failed"),
                    )
                return super().create_issue(title, body, issue_type, **kwargs)

        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        base_ctx = make_context(tree)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_path = tmp_path / "mapping.json"
        ctx = cp._PreflightContext(
            tree=tree,
            provider=_CollidingPartialLinkProvider(),
            provider_name="github",
            provider_target="owner/repo",
            node_index=base_ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=mapping_path,
        )

        with pytest.raises(cp.PipelineExecutionError, match="same provider identifier") as exc_info:
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert exc_info.value.created_result.identifier == "1"
        assert mapping_document["entries"]["f1"]["status"] == "pending"
        persisted = json.loads(mapping_path.read_text(encoding="utf-8"))
        assert persisted["entries"]["f1"]["status"] == "pending"

    def test_promotes_embedded_link_using_provider_link_result(self, tmp_path, monkeypatch):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        base_ctx = make_context(tree)
        next_id = 0

        def create_with_link_result(title, body, issue_type, *, parent_id=None, **kwargs):
            nonlocal next_id
            next_id += 1
            identifier = str(next_id)
            hierarchy_link_result = (
                ProviderLinkResult(parent_id, identifier, "already-linked") if parent_id is not None else None
            )
            return ProviderIssueResult(
                identifier=identifier,
                url=f"https://issues/{identifier}",
                status="created",
                hierarchy_link_result=hierarchy_link_result,
            )

        base_ctx.provider.create_issue = create_with_link_result
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")
        mapping_path = tmp_path / "mapping.json"
        ctx = cp._PreflightContext(
            tree=tree,
            provider=base_ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=base_ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=mapping_path,
        )

        original_write = cp.atomic_write_mapping_document
        persisted_link_states: list[tuple[str, object]] = []

        def track_mapping_write(path, document):
            relationship = document["entries"].get("link_subissue:e1:f1")
            if isinstance(relationship, dict):
                persisted_link_states.append((relationship["status"], relationship["target_provider_id"]))
            original_write(path, document)

        monkeypatch.setattr(cp, "atomic_write_mapping_document", track_mapping_write)
        cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        link = mapping_document["entries"]["link_subissue:e1:f1"]
        assert link["status"] == "confirmed"
        assert link["result"] == "already-linked"
        assert link["source_provider_id"] == "1"
        assert link["target_provider_id"] == "2"
        assert ("pending", None) in persisted_link_states
        assert ("pending", "2") in persisted_link_states
        assert ("confirmed", "2") in persisted_link_states
        assert persisted_link_states.index(("pending", "2")) < persisted_link_states.index(("confirmed", "2"))

    @pytest.mark.parametrize("persist_mapping", [True, False])
    @pytest.mark.parametrize(
        "hierarchy_link_result",
        [
            None,
            ProviderLinkResult("wrong-parent", "2", "linked"),
            ProviderLinkResult("1", "wrong-child", "linked"),
            ProviderLinkResult("1", "2", "unknown"),
        ],
    )
    def test_invalid_embedded_link_result_keeps_relationship_pending(
        self, tmp_path, hierarchy_link_result, persist_mapping
    ):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        base_ctx = make_context(tree)
        next_id = 0

        def create_with_invalid_link_result(title, body, issue_type, *, parent_id=None, **kwargs):
            nonlocal next_id
            next_id += 1
            identifier = str(next_id)
            return ProviderIssueResult(
                identifier=identifier,
                url=f"https://issues/{identifier}",
                status="created",
                hierarchy_link_result=hierarchy_link_result if parent_id is not None else None,
            )

        base_ctx.provider.create_issue = create_with_invalid_link_result
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo") if persist_mapping else None
        mapping_path = tmp_path / "mapping.json" if persist_mapping else None
        ctx = cp._PreflightContext(
            tree=tree,
            provider=base_ctx.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=base_ctx.node_index,
            mapping_document=mapping_document,
            mapping_path=mapping_path,
        )

        with pytest.raises(cp.PipelineExecutionError, match="no valid hierarchy link result") as exc_info:
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        assert exc_info.value.created_result is not None
        assert exc_info.value.created_result.identifier == "2"
        if persist_mapping:
            assert mapping_path is not None
            persisted = json.loads(mapping_path.read_text(encoding="utf-8"))
            assert persisted["entries"]["f1"] == {"provider_id": "2", "status": "created"}
            assert persisted["entries"]["link_subissue:e1:f1"]["status"] == "pending"
        else:
            assert not (tmp_path / "mapping.json").exists()

    def test_partial_root_identifier_is_persisted_before_raise(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        base_ctx = make_context(tree)

        class RootPartialProvider(self._PartialLinkProvider):
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
                if title == "Epic":
                    partial = ProviderIssueResult(identifier="root", url="u", status="partial-created")
                    raise HierarchyLinkError(
                        "root link failed",
                        created_result=partial,
                        stage="link_subissue",
                        cause=RuntimeError("gh api 500"),
                    )
                return super().create_issue(
                    title,
                    body,
                    issue_type,
                    parent_id=parent_id,
                    labels=labels,
                    idempotency_key=idempotency_key,
                    precreate_lookup=precreate_lookup,
                    dry_run=dry_run,
                )

        ctx = cp._PreflightContext(
            tree=tree,
            provider=RootPartialProvider(),
            provider_name="github",
            provider_target="owner/repo",
            node_index=base_ctx.node_index,
            mapping_document=initialize_mapping_document(tree, "github", "owner/repo"),
            mapping_path=tmp_path / "mapping.json",
        )

        with pytest.raises(cp.PipelineExecutionError):
            cp._create_issue_operations(ctx, cp._build_execution_order(ctx), dry_run=False)

        persisted = json.loads((tmp_path / "mapping.json").read_text(encoding="utf-8"))
        assert persisted["entries"]["e1"]["provider_id"] == "root"


class _FailingCreateProvider:
    """Fake provider that fails on a specific create call."""

    def __init__(self, fail_on_ref_title: str, error: Exception):
        self._fail_title = fail_on_ref_title
        self._error = error
        self.create_calls: list[str] = []
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
        with pytest.raises(cp.PipelineExecutionError) as exc_info:
            cp._create_issue_operations(ctx, order, dry_run=False)
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
        with pytest.raises(cp.PipelineExecutionError) as exc_info:
            cp._create_issue_operations(ctx, order, dry_run=False)
        plan = exc_info.value.partial_plan
        # Epic succeeded and was captured; the failed create is not a descriptor.
        assert [op.refs for op in plan.operations] == [("e1",)]
        assert plan.check_existing is False

    def test_definitive_failure_persists_redacted_failed_mapping_entry(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        context = make_context(tree)
        mapping_path = tmp_path / "mapping.json"

        def fail_create(*args, **kwargs):
            raise DefinitiveCreationFailure("invalid token=do-not-persist")

        context.provider.create_issue = fail_create
        context = cp._PreflightContext(
            tree=tree,
            provider=context.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=context.node_index,
            mapping_path=mapping_path,
        )

        with pytest.raises(cp.PipelineExecutionError):
            cp._create_issue_operations(context, cp._build_execution_order(context), dry_run=False)

        persisted = json.loads(mapping_path.read_text(encoding="utf-8"))
        assert persisted["entries"]["e1"]["status"] == "failed"
        assert persisted["entries"]["e1"] == {
            "error": "invalid [REDACTED]",
            "status": "failed",
        }
        assert "do-not-persist" not in mapping_path.read_text(encoding="utf-8")

    def test_definitive_failure_without_mapping_keeps_pipeline_error(self):
        context = make_context(make_tree(with_blocking=False))

        def fail_create(*args, **kwargs):
            raise DefinitiveCreationFailure("invalid request")

        context.provider.create_issue = fail_create

        with pytest.raises(cp.PipelineExecutionError):
            cp._create_issue_operations(context, cp._build_execution_order(context), dry_run=False)

    def test_definitive_failure_updates_in_memory_mapping_without_path(self):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        context = make_context(tree)
        mapping_document = initialize_mapping_document(tree, "github", "owner/repo")

        def fail_create(*args, **kwargs):
            raise DefinitiveCreationFailure("invalid request")

        context.provider.create_issue = fail_create
        context = cp._PreflightContext(
            tree=tree,
            provider=context.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=context.node_index,
            mapping_document=mapping_document,
        )

        with pytest.raises(cp.PipelineExecutionError):
            cp._create_issue_operations(context, cp._build_execution_order(context), dry_run=False)

        assert mapping_document["entries"]["e1"]["status"] == "failed"

    def test_create_result_collision_is_rejected_before_mapping_promotion(self, tmp_path):
        tree = cp.EpicTree(
            schemaVersion="2.0",
            treeId="12345678-1234-5678-1234-567812345678",
            epic=make_tree(with_blocking=False).epic,
        )
        context = make_context(tree)
        mapping_path = tmp_path / "mapping.json"

        def duplicate_create(*args, **kwargs):
            return ProviderIssueResult(identifier="same-id", url="u/same-id", status="existing")

        context.provider.create_issue = duplicate_create
        context = cp._PreflightContext(
            tree=tree,
            provider=context.provider,
            provider_name="github",
            provider_target="owner/repo",
            node_index=context.node_index,
            mapping_path=mapping_path,
        )

        with pytest.raises(cp.PipelineExecutionError, match="resolve to the same provider identifier") as exc_info:
            cp._create_issue_operations(context, cp._build_execution_order(context), dry_run=False)

        assert isinstance(exc_info.value.cause, RuntimeError)
        assert not isinstance(exc_info.value.cause, cp.PipelineValidationError)
        assert exc_info.value.created_result is not None
        assert exc_info.value.partial_plan.operations[-1].refs == ("f1",)
        persisted = json.loads(mapping_path.read_text(encoding="utf-8"))
        assert persisted["entries"]["e1"]["provider_id"] == "same-id"
        assert persisted["entries"]["f1"]["status"] == "pending"
        assert "provider_id" not in persisted["entries"]["f1"]
