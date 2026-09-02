"""Tests for plan_manifest() orchestrator function."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.issue_provider import InMemoryIssueProvider, ProviderIssueResult
from agentic_devtools.adapters.orchestration_key import embed_orchestration_key, generate_orchestration_key
from agentic_devtools.adapters.plan_manifest import plan_manifest


def _make_16_node_manifest() -> dict:
    """Create a 16-node manifest (1 epic, 3 features, 12 subtasks)."""
    nodes = []
    # Epic
    nodes.append(
        {
            "ref": "epic-1",
            "title": "Epic 1",
            "body": "Epic description",
            "issue_type": "epic",
        }
    )
    # 3 features under the epic
    for i in range(1, 4):
        nodes.append(
            {
                "ref": f"feature-{i}",
                "title": f"Feature {i}",
                "body": f"Feature {i} description",
                "issue_type": "feature",
                "parent_ref": "epic-1",
            }
        )
    # 4 subtasks under each feature = 12 subtasks
    for fi in range(1, 4):
        for si in range(1, 5):
            nodes.append(
                {
                    "ref": f"subtask-{fi}-{si}",
                    "title": f"Subtask {fi}-{si}",
                    "body": f"Subtask {fi}-{si} description",
                    "issue_type": "subtask",
                    "parent_ref": f"feature-{fi}",
                }
            )
    return {"nodes": nodes}


def _make_dependency_manifest() -> dict:
    """Create a manifest with blocked_by dependencies."""
    return {
        "nodes": [
            {
                "ref": "task-A",
                "title": "Task A",
                "body": "A body",
                "issue_type": "task",
            },
            {
                "ref": "task-B",
                "title": "Task B",
                "body": "B body",
                "issue_type": "task",
                "blocked_by": ["task-A"],
            },
        ]
    }


class TestPlanManifestDryRun:
    """US1: Dry-run preview of full epic creation."""

    def test_16_node_manifest_produces_correct_operation_counts(self):
        """US1-AC1: 16 creates + 15 links, all status=dry-run, zero provider calls."""
        manifest = _make_16_node_manifest()
        provider = InMemoryIssueProvider()

        plan = plan_manifest(manifest, provider, dry_run=True, check_existing=False)

        assert len(plan.create_operations) == 16
        assert len(plan.link_operations) == 15
        assert all(op.status == "dry-run" for op in plan.operations)
        # No issues created in provider (zero mutations)
        assert len(provider.issues) == 0

    def test_descriptors_include_provider_params(self):
        """US1-AC2: Each descriptor includes provider-specific parameters."""
        manifest = {
            "nodes": [
                {"ref": "f1", "title": "Feature 1", "body": "Body", "issue_type": "feature"},
            ]
        }
        provider = InMemoryIssueProvider()

        plan = plan_manifest(manifest, provider, dry_run=True, check_existing=False)

        desc = plan.create_operations[0]
        assert desc.provider_params["title"] == "Feature 1"
        assert desc.provider_params["issue_type"] == "feature"
        assert desc.orchestration_key
        assert desc.refs == ("f1",)

    def test_dependency_safe_ordering(self):
        """US1-AC3: Create A before B when B is blocked-by A."""
        manifest = _make_dependency_manifest()
        provider = InMemoryIssueProvider()

        plan = plan_manifest(manifest, provider, dry_run=True, check_existing=False)

        creates = plan.create_operations
        create_refs = [op.refs[0] for op in creates]
        # A must come before B
        assert create_refs.index("task-A") < create_refs.index("task-B")

        # add_blocked_by operations come after both creates
        deps = plan.dependency_operations
        assert len(deps) == 1
        all_ops = list(plan.operations)
        dep_idx = all_ops.index(deps[0])
        create_a_idx = next(
            i for i, op in enumerate(all_ops) if op.operation_type == "create_issue" and op.refs[0] == "task-A"
        )
        create_b_idx = next(
            i for i, op in enumerate(all_ops) if op.operation_type == "create_issue" and op.refs[0] == "task-B"
        )
        assert dep_idx > create_a_idx
        assert dep_idx > create_b_idx

    def test_check_existing_without_query_provider_raises(self):
        """FR-010: check_existing=True without query_provider raises ValueError."""
        manifest = {"nodes": []}
        provider = InMemoryIssueProvider()

        with pytest.raises(ValueError, match="check_existing=True requires a query_provider"):
            plan_manifest(manifest, provider, dry_run=True, check_existing=True)

    def test_check_existing_with_dry_run_false_raises(self):
        """FR-010: check_existing=True with dry_run=False raises ValueError."""
        manifest = {"nodes": []}
        provider = InMemoryIssueProvider()

        with pytest.raises(ValueError, match="check_existing=True is only valid with dry_run=True"):
            plan_manifest(manifest, provider, dry_run=False, check_existing=True, query_provider=provider)

    def test_check_existing_with_non_protocol_query_provider_raises(self):
        """check_existing=True with an object that does not implement IdempotencyQueryProvider raises ValueError."""
        manifest = {"nodes": []}
        provider = InMemoryIssueProvider()

        with pytest.raises(ValueError, match="query_provider must implement the IdempotencyQueryProvider protocol"):
            plan_manifest(manifest, provider, dry_run=True, check_existing=True, query_provider=object())

    def test_zero_provider_api_io_in_planning_mode(self):
        """FR-001: dry-run planning-only makes zero mutations."""
        manifest = _make_16_node_manifest()
        provider = InMemoryIssueProvider()

        plan_manifest(manifest, provider, dry_run=True, check_existing=False)

        # Verify no state was mutated
        assert len(provider.issues) == 0
        assert len(provider.parent_child_links) == 0
        assert len(provider.blocked_by_links) == 0

    def test_planning_mode_does_not_call_create_issue(self):
        """FR-001: planning-only dry-run does not call provider.create_issue."""

        class _TrackingProvider(InMemoryIssueProvider):
            def __init__(self) -> None:
                super().__init__()
                self.create_issue_calls = 0

            def create_issue(
                self,
                title: str,
                body: str,
                issue_type: str,
                *,
                parent_id: str | None = None,
                labels: list[str] | None = None,
                idempotency_key: str | None = None,
                dry_run: bool = False,
            ) -> ProviderIssueResult:
                self.create_issue_calls += 1
                return super().create_issue(
                    title,
                    body,
                    issue_type,
                    parent_id=parent_id,
                    labels=labels,
                    idempotency_key=idempotency_key,
                    dry_run=dry_run,
                )

        provider = _TrackingProvider()
        manifest = {
            "nodes": [
                {"ref": "task-1", "title": "Task 1", "body": "Body 1", "issue_type": "task"},
            ]
        }

        plan = plan_manifest(manifest, provider, dry_run=True, check_existing=False)

        assert provider.create_issue_calls == 0
        assert plan.create_operations[0].result is None


class TestPlanManifestExecution:
    """US2: Idempotent re-run via orchestrator."""

    def test_4_issues_2_existing(self):
        """US2-AC1: 4-issue manifest where 2 exist → 2 existing + 2 created."""
        provider = InMemoryIssueProvider()

        # Pre-create 2 issues with orchestration keys
        key0 = generate_orchestration_key("create_issue", "node-0")
        key1 = generate_orchestration_key("create_issue", "node-1")
        body0 = embed_orchestration_key("Body 0", key0)
        body1 = embed_orchestration_key("Body 1", key1)
        provider.create_issue("Node 0", body0, "task", idempotency_key=key0)
        provider.create_issue("Node 1", body1, "task", idempotency_key=key1)

        manifest = {
            "nodes": [
                {"ref": "node-0", "title": "Node 0", "body": "Body 0", "issue_type": "task"},
                {"ref": "node-1", "title": "Node 1", "body": "Body 1", "issue_type": "task"},
                {"ref": "node-2", "title": "Node 2", "body": "Body 2", "issue_type": "task"},
                {"ref": "node-3", "title": "Node 3", "body": "Body 3", "issue_type": "task"},
            ]
        }

        plan = plan_manifest(manifest, provider, dry_run=False)

        statuses = [op.status for op in plan.create_operations]
        assert statuses.count("existing") == 2
        assert statuses.count("created") == 2

    def test_pre_linked_parent_child(self):
        """US2-AC2: pre-linked parent-child re-execute → already-linked."""
        provider = InMemoryIssueProvider()

        # Pre-create parent and child, and link them
        key_p = generate_orchestration_key("create_issue", "parent")
        key_c = generate_orchestration_key("create_issue", "child")
        body_p = embed_orchestration_key("Parent body", key_p)
        body_c = embed_orchestration_key("Child body", key_c)
        r_p = provider.create_issue("Parent", body_p, "feature", idempotency_key=key_p)
        r_c = provider.create_issue("Child", body_c, "subtask", idempotency_key=key_c)
        provider.link_subissue(r_p.identifier, r_c.identifier)

        manifest = {
            "nodes": [
                {"ref": "parent", "title": "Parent", "body": "Parent body", "issue_type": "feature"},
                {
                    "ref": "child",
                    "title": "Child",
                    "body": "Child body",
                    "issue_type": "subtask",
                    "parent_ref": "parent",
                },
            ]
        }

        plan = plan_manifest(manifest, provider, dry_run=False)

        link_ops = plan.link_operations
        assert len(link_ops) == 1
        assert link_ops[0].status == "already-linked"

    def test_pre_existing_blocking_dependency(self):
        """US2-AC3: pre-existing blocking dependency → already-linked."""
        provider = InMemoryIssueProvider()

        # Pre-create issues and add blocking relationship
        key_a = generate_orchestration_key("create_issue", "task-A")
        key_b = generate_orchestration_key("create_issue", "task-B")
        body_a = embed_orchestration_key("A body", key_a)
        body_b = embed_orchestration_key("B body", key_b)
        r_a = provider.create_issue("Task A", body_a, "task", idempotency_key=key_a)
        r_b = provider.create_issue("Task B", body_b, "task", idempotency_key=key_b)
        provider.add_blocked_by(r_b.identifier, r_a.identifier)

        manifest = _make_dependency_manifest()

        plan = plan_manifest(manifest, provider, dry_run=False)

        dep_ops = plan.dependency_operations
        assert len(dep_ops) == 1
        assert dep_ops[0].status == "already-linked"


class TestPlanManifestCheckExisting:
    """Dry-run with existence checks (Mode 2)."""

    def test_check_existing_finds_existing_issues(self):
        """check_existing=True reports existing/dry-run correctly."""
        provider = InMemoryIssueProvider()

        # Pre-create one issue
        key0 = generate_orchestration_key("create_issue", "node-0")
        body0 = embed_orchestration_key("Body 0", key0)
        provider.create_issue("Node 0", body0, "task", idempotency_key=key0)

        manifest = {
            "nodes": [
                {"ref": "node-0", "title": "Node 0", "body": "Body 0", "issue_type": "task"},
                {"ref": "node-1", "title": "Node 1", "body": "Body 1", "issue_type": "task"},
            ]
        }

        plan = plan_manifest(manifest, provider, dry_run=True, check_existing=True, query_provider=provider)

        creates = plan.create_operations
        statuses = {op.refs[0]: op.status for op in creates}
        assert statuses["node-0"] == "existing"
        assert statuses["node-1"] == "dry-run"

    def test_network_error_propagates(self):
        """FR-009: network error during existence check fails entire plan."""

        class _FailingQueryProvider:
            def find_existing_issue(self, orchestration_key: str):
                raise RuntimeError("Network error")

            def find_existing_link(self, parent_provider_id: str, child_provider_id: str):
                return None

            def find_existing_dependency(self, issue_provider_id: str, blocked_by_provider_id: str):
                return None

        provider = InMemoryIssueProvider()
        manifest = {
            "nodes": [
                {"ref": "node-0", "title": "Node 0", "body": "Body 0", "issue_type": "task"},
            ]
        }

        with pytest.raises(RuntimeError, match="Network error"):
            plan_manifest(manifest, provider, dry_run=True, check_existing=True, query_provider=_FailingQueryProvider())

    def test_check_existing_does_not_call_create_issue_for_missing_issue(self):
        """FR-001: query-only dry-run does not call provider.create_issue."""

        class _TrackingProvider(InMemoryIssueProvider):
            def __init__(self) -> None:
                super().__init__()
                self.create_issue_calls = 0

            def create_issue(
                self,
                title: str,
                body: str,
                issue_type: str,
                *,
                parent_id: str | None = None,
                labels: list[str] | None = None,
                idempotency_key: str | None = None,
                dry_run: bool = False,
            ) -> ProviderIssueResult:
                self.create_issue_calls += 1
                return super().create_issue(
                    title,
                    body,
                    issue_type,
                    parent_id=parent_id,
                    labels=labels,
                    idempotency_key=idempotency_key,
                    dry_run=dry_run,
                )

        provider = _TrackingProvider()
        manifest = {
            "nodes": [
                {"ref": "node-1", "title": "Node 1", "body": "Body 1", "issue_type": "task"},
            ]
        }

        plan = plan_manifest(manifest, provider, dry_run=True, check_existing=True, query_provider=provider)

        assert provider.create_issue_calls == 0
        assert plan.create_operations[0].result is None


class TestPlanManifestMixedState:
    """US5: Mixed state detection on re-run."""

    def test_mixed_state_correct_statuses(self):
        """US5-AC1: Partial pre-populated state → correct mixed statuses."""
        provider = InMemoryIssueProvider()

        # Node 1 exists with link to parent
        key_p = generate_orchestration_key("create_issue", "parent")
        key_1 = generate_orchestration_key("create_issue", "child-1")
        body_p = embed_orchestration_key("Parent", key_p)
        body_1 = embed_orchestration_key("Child 1", key_1)
        r_p = provider.create_issue("Parent", body_p, "feature", idempotency_key=key_p)
        r_1 = provider.create_issue("Child 1", body_1, "subtask", idempotency_key=key_1)
        provider.link_subissue(r_p.identifier, r_1.identifier)

        manifest = {
            "nodes": [
                {"ref": "parent", "title": "Parent", "body": "Parent", "issue_type": "feature"},
                {
                    "ref": "child-1",
                    "title": "Child 1",
                    "body": "Child 1",
                    "issue_type": "subtask",
                    "parent_ref": "parent",
                },
                {
                    "ref": "child-2",
                    "title": "Child 2",
                    "body": "Child 2",
                    "issue_type": "subtask",
                    "parent_ref": "parent",
                },
            ]
        }

        plan = plan_manifest(manifest, provider, dry_run=False)

        create_statuses = {op.refs[0]: op.status for op in plan.create_operations}
        assert create_statuses["parent"] == "existing"
        assert create_statuses["child-1"] == "existing"
        assert create_statuses["child-2"] == "created"

        link_statuses = {op.refs[1]: op.status for op in plan.link_operations}
        assert link_statuses["child-1"] == "already-linked"
        assert link_statuses["child-2"] == "linked"


class TestPlanManifestCheckExistingLinks:
    """Coverage for check_existing mode with links and dependencies."""

    def test_check_existing_link_already_linked(self):
        """check_existing=True detects pre-existing parent-child links."""
        provider = InMemoryIssueProvider()
        key_p = generate_orchestration_key("create_issue", "parent")
        key_c = generate_orchestration_key("create_issue", "child")
        body_p = embed_orchestration_key("Parent", key_p)
        body_c = embed_orchestration_key("Child", key_c)
        r_p = provider.create_issue("Parent", body_p, "feature", idempotency_key=key_p)
        r_c = provider.create_issue("Child", body_c, "subtask", idempotency_key=key_c)
        provider.link_subissue(r_p.identifier, r_c.identifier)

        manifest = {
            "nodes": [
                {"ref": "parent", "title": "Parent", "body": "Parent", "issue_type": "feature"},
                {
                    "ref": "child",
                    "title": "Child",
                    "body": "Child",
                    "issue_type": "subtask",
                    "parent_ref": "parent",
                },
            ]
        }

        plan = plan_manifest(manifest, provider, dry_run=True, check_existing=True, query_provider=provider)
        links = plan.link_operations
        assert len(links) == 1
        assert links[0].status == "already-linked"

    def test_check_existing_link_not_found(self):
        """check_existing=True with no pre-existing link → dry-run status."""
        provider = InMemoryIssueProvider()
        key_p = generate_orchestration_key("create_issue", "parent")
        key_c = generate_orchestration_key("create_issue", "child")
        body_p = embed_orchestration_key("Parent", key_p)
        body_c = embed_orchestration_key("Child", key_c)
        provider.create_issue("Parent", body_p, "feature", idempotency_key=key_p)
        provider.create_issue("Child", body_c, "subtask", idempotency_key=key_c)
        # Do NOT link them

        manifest = {
            "nodes": [
                {"ref": "parent", "title": "Parent", "body": "Parent", "issue_type": "feature"},
                {
                    "ref": "child",
                    "title": "Child",
                    "body": "Child",
                    "issue_type": "subtask",
                    "parent_ref": "parent",
                },
            ]
        }

        plan = plan_manifest(manifest, provider, dry_run=True, check_existing=True, query_provider=provider)
        links = plan.link_operations
        assert len(links) == 1
        assert links[0].status == "dry-run"

    def test_check_existing_link_unresolved_ref_bindings(self):
        """check_existing=True with unresolved ref bindings → dry-run."""
        provider = InMemoryIssueProvider()
        # Don't create any issues — ref_bindings will be empty
        manifest = {
            "nodes": [
                {"ref": "parent", "title": "P", "body": "P", "issue_type": "feature"},
                {
                    "ref": "child",
                    "title": "C",
                    "body": "C",
                    "issue_type": "subtask",
                    "parent_ref": "parent",
                },
            ]
        }

        plan = plan_manifest(manifest, provider, dry_run=True, check_existing=True, query_provider=provider)
        links = plan.link_operations
        assert len(links) == 1
        assert links[0].status == "dry-run"

    def test_check_existing_dependency_already_linked(self):
        """check_existing=True detects pre-existing blocking dependencies."""
        provider = InMemoryIssueProvider()
        key_a = generate_orchestration_key("create_issue", "task-A")
        key_b = generate_orchestration_key("create_issue", "task-B")
        body_a = embed_orchestration_key("A", key_a)
        body_b = embed_orchestration_key("B", key_b)
        r_a = provider.create_issue("A", body_a, "task", idempotency_key=key_a)
        r_b = provider.create_issue("B", body_b, "task", idempotency_key=key_b)
        provider.add_blocked_by(r_a.identifier, r_b.identifier)

        manifest = {
            "nodes": [
                {"ref": "task-A", "title": "A", "body": "A", "issue_type": "task", "blocked_by": ["task-B"]},
                {"ref": "task-B", "title": "B", "body": "B", "issue_type": "task"},
            ],
        }

        plan = plan_manifest(manifest, provider, dry_run=True, check_existing=True, query_provider=provider)
        deps = plan.dependency_operations
        assert len(deps) == 1
        assert deps[0].status == "already-linked"

    def test_check_existing_dependency_not_found(self):
        """check_existing=True with no pre-existing dep → dry-run status."""
        provider = InMemoryIssueProvider()
        key_a = generate_orchestration_key("create_issue", "task-A")
        key_b = generate_orchestration_key("create_issue", "task-B")
        body_a = embed_orchestration_key("A", key_a)
        body_b = embed_orchestration_key("B", key_b)
        provider.create_issue("A", body_a, "task", idempotency_key=key_a)
        provider.create_issue("B", body_b, "task", idempotency_key=key_b)
        # Do NOT add blocked_by

        manifest = {
            "nodes": [
                {"ref": "task-A", "title": "A", "body": "A", "issue_type": "task", "blocked_by": ["task-B"]},
                {"ref": "task-B", "title": "B", "body": "B", "issue_type": "task"},
            ],
        }

        plan = plan_manifest(manifest, provider, dry_run=True, check_existing=True, query_provider=provider)
        deps = plan.dependency_operations
        assert len(deps) == 1
        assert deps[0].status == "dry-run"

    def test_check_existing_dependency_unresolved_refs(self):
        """check_existing=True with unresolved dep ref bindings → dry-run."""
        provider = InMemoryIssueProvider()
        manifest = {
            "nodes": [
                {"ref": "task-A", "title": "A", "body": "A", "issue_type": "task", "blocked_by": ["task-B"]},
                {"ref": "task-B", "title": "B", "body": "B", "issue_type": "task"},
            ],
        }

        plan = plan_manifest(manifest, provider, dry_run=True, check_existing=True, query_provider=provider)
        deps = plan.dependency_operations
        assert len(deps) == 1
        assert deps[0].status == "dry-run"

    def test_labels_included_in_provider_params(self):
        """Labels from manifest are included in provider_params."""
        provider = InMemoryIssueProvider()
        manifest = {
            "nodes": [
                {
                    "ref": "task-1",
                    "title": "Task",
                    "body": "Body",
                    "issue_type": "task",
                    "labels": ["bug", "critical"],
                },
            ]
        }
        plan = plan_manifest(manifest, provider, dry_run=True)
        creates = plan.create_operations
        assert creates[0].provider_params["labels"] == ["bug", "critical"]

    def test_external_blocker_ref_not_in_nodes(self):
        """Refs in blocked_by that are not manifest nodes are skipped gracefully."""
        provider = InMemoryIssueProvider()
        manifest = {
            "nodes": [
                {
                    "ref": "task-A",
                    "title": "A",
                    "body": "A",
                    "issue_type": "task",
                    "blocked_by": ["external-ref"],
                },
            ]
        }
        plan = plan_manifest(manifest, provider, dry_run=True)
        # Should have 1 create and 1 blocked_by operation (for task-A)
        assert len(plan.create_operations) == 1
        assert len(plan.dependency_operations) == 1
        # external-ref doesn't become a create operation
        assert all(op.refs[0] == "task-A" for op in plan.create_operations)

    def test_real_execution_with_external_blocker_ref_raises_value_error(self):
        """Real execution rejects blocked_by refs that are not manifest nodes."""
        provider = InMemoryIssueProvider()
        manifest = {
            "nodes": [
                {
                    "ref": "task-A",
                    "title": "A",
                    "body": "A",
                    "issue_type": "task",
                    "blocked_by": ["external-ref"],
                },
            ]
        }

        with pytest.raises(
            ValueError,
            match=r"blocked_by ref 'external-ref' for manifest ref 'task-A' could not be resolved",
        ):
            plan_manifest(manifest, provider, dry_run=False)
        assert len(provider.issues) == 0


class TestPlanManifestValidation:
    """Upfront manifest structure validation."""

    def test_manifest_not_a_dict_raises(self):
        """Non-dict manifest raises ValueError before any field access."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="manifest must be a dict"):
            plan_manifest(["not-a-dict"], provider, dry_run=True)

    def test_nodes_not_a_list_raises(self):
        """manifest['nodes'] must be a list."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="manifest\\['nodes'\\] must be a list"):
            plan_manifest({"nodes": "not-a-list"}, provider, dry_run=True)

    def test_node_not_a_dict_raises(self):
        """Each element of manifest['nodes'] must be a dict."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="manifest\\['nodes'\\]\\[0\\] must be a dict"):
            plan_manifest({"nodes": ["not-a-dict"]}, provider, dry_run=True)

    def test_node_missing_ref_raises(self):
        """Node missing 'ref' key raises ValueError."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="missing required key 'ref'"):
            plan_manifest(
                {"nodes": [{"title": "T", "issue_type": "task"}]},
                provider,
                dry_run=True,
            )

    def test_node_missing_title_raises(self):
        """Node missing 'title' key raises ValueError."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="missing required key 'title'"):
            plan_manifest(
                {"nodes": [{"ref": "r1", "issue_type": "task"}]},
                provider,
                dry_run=True,
            )

    def test_node_missing_issue_type_raises(self):
        """Node missing 'issue_type' key raises ValueError."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="missing required key 'issue_type'"):
            plan_manifest(
                {"nodes": [{"ref": "r1", "title": "T"}]},
                provider,
                dry_run=True,
            )

    def test_duplicate_ref_raises(self):
        """Duplicate refs in manifest['nodes'] raise ValueError."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="Duplicate ref 'task-1'"):
            plan_manifest(
                {
                    "nodes": [
                        {"ref": "task-1", "title": "T1", "issue_type": "task"},
                        {"ref": "task-1", "title": "T2", "issue_type": "task"},
                    ]
                },
                provider,
                dry_run=True,
            )

    def test_unresolvable_parent_ref_raises_in_real_execution(self):
        """Real execution raises ValueError when parent_ref cannot be resolved."""
        provider = InMemoryIssueProvider()
        manifest = {
            "nodes": [
                {
                    "ref": "valid-task",
                    "title": "Valid Task",
                    "body": "Valid",
                    "issue_type": "task",
                },
                {
                    "ref": "child",
                    "title": "Child",
                    "body": "Child",
                    "issue_type": "subtask",
                    "parent_ref": "external-parent",
                },
            ]
        }

        with pytest.raises(
            ValueError,
            match=r"parent_ref 'external-parent' for manifest ref 'child' could not be resolved",
        ):
            plan_manifest(manifest, provider, dry_run=False)
        assert len(provider.issues) == 0

    def test_empty_ref_raises(self):
        """Node with an empty string 'ref' raises ValueError."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="must be a non-empty string"):
            plan_manifest(
                {"nodes": [{"ref": "", "title": "T", "issue_type": "task"}]},
                provider,
                dry_run=True,
            )

    def test_none_ref_raises(self):
        """Node with None 'ref' raises ValueError."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="must be a non-empty string"):
            plan_manifest(
                {"nodes": [{"ref": None, "title": "T", "issue_type": "task"}]},
                provider,
                dry_run=True,
            )

    def test_empty_title_raises(self):
        """Node with an empty string 'title' raises ValueError."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="must be a non-empty string"):
            plan_manifest(
                {"nodes": [{"ref": "r1", "title": "", "issue_type": "task"}]},
                provider,
                dry_run=True,
            )

    def test_empty_issue_type_raises(self):
        """Node with an empty string 'issue_type' raises ValueError."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="must be a non-empty string"):
            plan_manifest(
                {"nodes": [{"ref": "r1", "title": "T", "issue_type": ""}]},
                provider,
                dry_run=True,
            )

    def test_issue_type_is_normalized_before_planning(self):
        """Mixed-case issue_type is normalized before provider params are built."""
        provider = InMemoryIssueProvider()

        plan = plan_manifest(
            {"nodes": [{"ref": "r1", "title": "T", "issue_type": " Feature "}]},
            provider,
            dry_run=True,
        )

        assert plan.create_operations[0].provider_params["issue_type"] == "feature"

    def test_ref_is_stripped_and_used_as_canonical_identifier(self):
        """Whitespace-padded ref is stripped; stripped value is used for orchestration key and cross-refs."""
        provider = InMemoryIssueProvider()

        plan = plan_manifest(
            {
                "nodes": [
                    {"ref": " epic-1 ", "title": "Epic", "issue_type": "epic"},
                    {"ref": " task-1 ", "title": "Task", "issue_type": "task", "parent_ref": " epic-1 "},
                ]
            },
            provider,
            dry_run=True,
        )

        create_refs = [op.refs[0] for op in plan.create_operations]
        assert create_refs == ["epic-1", "task-1"]
        link_ops = plan.link_operations
        assert len(link_ops) == 1
        assert link_ops[0].refs == ("epic-1", "task-1")

    def test_title_is_stripped_and_stored_in_provider_params(self):
        """Whitespace-padded title is stripped before being stored in provider_params."""
        provider = InMemoryIssueProvider()

        plan = plan_manifest(
            {"nodes": [{"ref": "r1", "title": "  My Title  ", "issue_type": "task"}]},
            provider,
            dry_run=True,
        )

        assert plan.create_operations[0].provider_params["title"] == "My Title"

    def test_parent_ref_is_stripped_and_resolves_cross_ref(self):
        """Whitespace-padded parent_ref is stripped; stripped value resolves the parent node ref."""
        provider = InMemoryIssueProvider()

        plan = plan_manifest(
            {
                "nodes": [
                    {"ref": "epic-1", "title": "Epic", "issue_type": "epic"},
                    {"ref": "task-1", "title": "Task", "issue_type": "task", "parent_ref": " epic-1 "},
                ]
            },
            provider,
            dry_run=True,
        )

        link_ops = plan.link_operations
        assert len(link_ops) == 1
        assert link_ops[0].provider_params["parent_ref"] == "epic-1"
        assert link_ops[0].refs == ("epic-1", "task-1")

    def test_blocked_by_elements_are_stripped(self):
        """Whitespace-padded blocked_by elements are stripped; stripped values resolve cross-refs."""
        provider = InMemoryIssueProvider()

        plan = plan_manifest(
            {
                "nodes": [
                    {"ref": "task-A", "title": "A", "issue_type": "task"},
                    {"ref": "task-B", "title": "B", "issue_type": "task", "blocked_by": [" task-A "]},
                ]
            },
            provider,
            dry_run=True,
        )

        dep_ops = plan.dependency_operations
        assert len(dep_ops) == 1
        assert dep_ops[0].refs == ("task-B", "task-A")

    def test_labels_elements_are_stripped(self):
        """Whitespace-padded labels elements are stripped before being stored in provider_params."""
        provider = InMemoryIssueProvider()

        plan = plan_manifest(
            {"nodes": [{"ref": "r1", "title": "T", "issue_type": "task", "labels": [" bug ", "  enhancement  "]}]},
            provider,
            dry_run=True,
        )

        assert plan.create_operations[0].provider_params["labels"] == ["bug", "enhancement"]

    def test_unsupported_issue_type_raises_before_execution(self):
        """Unsupported issue_type raises before real execution mutates provider state."""
        provider = InMemoryIssueProvider()

        with pytest.raises(ValueError, match="Unsupported issue_type 'unknown'"):
            plan_manifest(
                {"nodes": [{"ref": "r1", "title": "T", "issue_type": "unknown"}]},
                provider,
                dry_run=False,
            )

        assert len(provider.issues) == 0

    def test_blocked_by_as_string_raises(self):
        """Node with 'blocked_by' as a string raises ValueError (must be a list)."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="'blocked_by'\\] must be a list"):
            plan_manifest(
                {
                    "nodes": [
                        {"ref": "task-A", "title": "A", "issue_type": "task"},
                        {
                            "ref": "task-B",
                            "title": "B",
                            "issue_type": "task",
                            "blocked_by": "task-A",  # string instead of list
                        },
                    ]
                },
                provider,
                dry_run=True,
            )

    def test_blocked_by_none_raises(self):
        """Node with 'blocked_by' set to None raises ValueError (must be a list)."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="'blocked_by'\\] must be a list"):
            plan_manifest(
                {"nodes": [{"ref": "r1", "title": "T", "issue_type": "task", "blocked_by": None}]},
                provider,
                dry_run=True,
            )

    def test_labels_as_string_raises(self):
        """Node with 'labels' as a string raises ValueError (must be a list)."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="'labels'\\] must be a list"):
            plan_manifest(
                {
                    "nodes": [
                        {
                            "ref": "r1",
                            "title": "T",
                            "issue_type": "task",
                            "labels": "my-label",  # string instead of list
                        }
                    ]
                },
                provider,
                dry_run=True,
            )

    def test_blocked_by_element_not_string_raises(self):
        """Non-string element in 'blocked_by' raises ValueError."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="'blocked_by'\\]\\[0\\] must be a non-empty string"):
            plan_manifest(
                {
                    "nodes": [
                        {"ref": "task-A", "title": "A", "issue_type": "task"},
                        {
                            "ref": "task-B",
                            "title": "B",
                            "issue_type": "task",
                            "blocked_by": [None],  # None instead of string
                        },
                    ]
                },
                provider,
                dry_run=True,
            )

    def test_blocked_by_element_empty_string_raises(self):
        """Empty string element in 'blocked_by' raises ValueError."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="'blocked_by'\\]\\[0\\] must be a non-empty string"):
            plan_manifest(
                {
                    "nodes": [
                        {"ref": "task-A", "title": "A", "issue_type": "task"},
                        {
                            "ref": "task-B",
                            "title": "B",
                            "issue_type": "task",
                            "blocked_by": [""],  # empty string
                        },
                    ]
                },
                provider,
                dry_run=True,
            )

    def test_blocked_by_element_int_raises(self):
        """Integer element in 'blocked_by' raises ValueError."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="'blocked_by'\\]\\[0\\] must be a non-empty string"):
            plan_manifest(
                {
                    "nodes": [
                        {
                            "ref": "task-A",
                            "title": "A",
                            "issue_type": "task",
                            "blocked_by": [42],  # int instead of string
                        }
                    ]
                },
                provider,
                dry_run=True,
            )

    def test_labels_element_not_string_raises(self):
        """Non-string element in 'labels' raises ValueError."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="'labels'\\]\\[0\\] must be a non-empty string"):
            plan_manifest(
                {
                    "nodes": [
                        {
                            "ref": "r1",
                            "title": "T",
                            "issue_type": "task",
                            "labels": [123],  # int instead of string
                        }
                    ]
                },
                provider,
                dry_run=True,
            )

    def test_labels_element_empty_string_raises(self):
        """Empty string element in 'labels' raises ValueError."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="'labels'\\]\\[0\\] must be a non-empty string"):
            plan_manifest(
                {
                    "nodes": [
                        {
                            "ref": "r1",
                            "title": "T",
                            "issue_type": "task",
                            "labels": [""],  # empty string
                        }
                    ]
                },
                provider,
                dry_run=True,
            )

    def test_required_string_field_whitespace_only_raises(self):
        """Whitespace-only required string fields raise ValueError."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="\\['ref'\\] must be a non-empty string"):
            plan_manifest(
                {
                    "nodes": [
                        {
                            "ref": "   ",
                            "title": "T",
                            "issue_type": "task",
                        }
                    ]
                },
                provider,
                dry_run=True,
            )

    def test_parent_ref_whitespace_only_raises(self):
        """Whitespace-only parent_ref raises ValueError."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="'parent_ref'\\] must be a non-empty string"):
            plan_manifest(
                {
                    "nodes": [
                        {
                            "ref": "child",
                            "title": "T",
                            "issue_type": "task",
                            "parent_ref": "   ",
                        }
                    ]
                },
                provider,
                dry_run=True,
            )

    def test_blocked_by_element_whitespace_only_raises(self):
        """Whitespace-only blocked_by element raises ValueError."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="'blocked_by'\\]\\[0\\] must be a non-empty string"):
            plan_manifest(
                {
                    "nodes": [
                        {"ref": "task-A", "title": "A", "issue_type": "task"},
                        {
                            "ref": "task-B",
                            "title": "B",
                            "issue_type": "task",
                            "blocked_by": ["   "],
                        },
                    ]
                },
                provider,
                dry_run=True,
            )

    def test_body_null_is_treated_as_empty_string(self):
        """Null body is normalized to an empty string before key embedding."""
        provider = InMemoryIssueProvider()

        plan = plan_manifest(
            {
                "nodes": [
                    {
                        "ref": "task-1",
                        "title": "Task 1",
                        "body": None,
                        "issue_type": "task",
                    }
                ]
            },
            provider,
            dry_run=True,
        )

        assert isinstance(plan.create_operations[0].provider_params["body"], str)

    def test_body_non_string_raises(self):
        """Non-string non-null body raises ValueError."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="\\['body'\\] must be a string or null"):
            plan_manifest(
                {
                    "nodes": [
                        {
                            "ref": "task-1",
                            "title": "Task 1",
                            "body": 42,
                            "issue_type": "task",
                        }
                    ]
                },
                provider,
                dry_run=True,
            )

    def test_parent_ref_not_string_raises(self):
        """Non-string 'parent_ref' raises ValueError."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="'parent_ref'\\] must be a non-empty string"):
            plan_manifest(
                {
                    "nodes": [
                        {
                            "ref": "r1",
                            "title": "T",
                            "issue_type": "task",
                            "parent_ref": 42,  # int instead of string
                        }
                    ]
                },
                provider,
                dry_run=True,
            )

    def test_parent_ref_empty_string_raises(self):
        """Empty string 'parent_ref' raises ValueError."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="'parent_ref'\\] must be a non-empty string"):
            plan_manifest(
                {
                    "nodes": [
                        {
                            "ref": "r1",
                            "title": "T",
                            "issue_type": "task",
                            "parent_ref": "",  # empty string
                        }
                    ]
                },
                provider,
                dry_run=True,
            )

    def test_parent_ref_none_raises(self):
        """None 'parent_ref' raises ValueError (must be non-empty string when present)."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="'parent_ref'\\] must be a non-empty string"):
            plan_manifest(
                {
                    "nodes": [
                        {
                            "ref": "r1",
                            "title": "T",
                            "issue_type": "task",
                            "parent_ref": None,  # None — explicit null from JSON
                        }
                    ]
                },
                provider,
                dry_run=True,
            )

    def test_cycle_raises_value_error(self):
        """A circular dependency in manifest nodes raises ValueError, not CycleDetectedError."""
        provider = InMemoryIssueProvider()
        with pytest.raises(ValueError, match="Circular dependency detected"):
            plan_manifest(
                {
                    "nodes": [
                        {
                            "ref": "task-A",
                            "title": "A",
                            "issue_type": "task",
                            "blocked_by": ["task-B"],
                        },
                        {
                            "ref": "task-B",
                            "title": "B",
                            "issue_type": "task",
                            "blocked_by": ["task-A"],
                        },
                    ]
                },
                provider,
                dry_run=True,
            )
