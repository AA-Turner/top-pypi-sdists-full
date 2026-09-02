"""Tests for the public ``run_creation_pipeline`` entry point.

Covers helper call-sequencing (T026), end-to-end happy path via an in-memory
provider (T040), dry-run semantics (T042), the returned ``OperationPlan``
contract (T044), preflight-failure propagation (T050), execution-failure
propagation (T052), and deterministic operation ordering (T054).
"""

from __future__ import annotations

import json
from typing import cast

import pytest

import agentic_devtools.cli.jira.creation_pipeline as cp
from agentic_devtools.adapters.issue_provider import (
    InMemoryIssueProvider,
    ProviderIssueResult,
    ProviderLinkResult,
)
from agentic_devtools.adapters.operation_plan import OperationPlan
from agentic_devtools.adapters.orchestration_key import generate_orchestration_key
from agentic_devtools.cli.jira.creation_pipeline import (
    PipelineExecutionError,
    PipelineValidationError,
    run_creation_pipeline,
)

from .conftest import make_context, make_tree, valid_tree_doc


@pytest.fixture
def patched(monkeypatch):
    fake = InMemoryIssueProvider("github")
    monkeypatch.setattr(cp, "resolve_provider_name", lambda repo, *, provider=None: "github")
    monkeypatch.setattr(cp, "get_issue_provider", lambda repo, *, provider=None: fake)
    return fake


def _make_repo(tmp_path, doc, name="tree.json"):
    repo = tmp_path / "repo"
    repo.mkdir(exist_ok=True)
    file_path = repo / name
    file_path.write_text(json.dumps(doc), encoding="utf-8")
    return repo, file_path


class TestRunCreationPipelineHelperSequencing:
    """T026 — the entry point orchestrates the four helpers in order."""

    def test_helpers_called_in_dependency_order(self, tmp_path, monkeypatch):
        calls: list[str] = []
        ctx = make_context(make_tree(with_blocking=True))

        def fake_preflight(repo, file, *, provider=None, start_from=None):
            calls.append("preflight")
            return ctx

        def fake_order(context):
            calls.append("order")
            assert context is ctx
            return ["e1", "f1", "s2", "s1"]

        def fake_create(context, ordered_refs, *, dry_run=False):
            calls.append("create")
            assert ordered_refs == ["e1", "f1", "s2", "s1"]
            return {"e1": "1"}, []

        def fake_blocking(context, ref_to_id, *, dry_run=False, prior_operations=()):
            calls.append("blocking")
            assert ref_to_id == {"e1": "1"}
            return []

        monkeypatch.setattr(cp, "_run_preflight", fake_preflight)
        monkeypatch.setattr(cp, "_build_execution_order", fake_order)
        monkeypatch.setattr(cp, "_create_issue_operations", fake_create)
        monkeypatch.setattr(cp, "_blocking_operations", fake_blocking)

        plan = run_creation_pipeline(tmp_path, tmp_path / "f.json")
        assert calls == ["preflight", "order", "create", "blocking"]
        assert isinstance(plan, OperationPlan)


class TestRunCreationPipelineEndToEnd:
    """T040 — full happy path through a real in-memory provider."""

    def test_creates_all_issues_and_blocking_edges(self, tmp_path, patched):
        repo, file_path = _make_repo(tmp_path, valid_tree_doc(with_blocking=True))
        plan = run_creation_pipeline(repo, file_path)
        assert plan.dry_run is False
        assert plan.check_existing is False
        create_ops = [op for op in plan.operations if op.operation_type == "create_issue"]
        block_ops = [op for op in plan.operations if op.operation_type == "add_blocked_by"]
        assert {op.refs[0] for op in create_ops} == {"e1", "f1", "s1", "s2"}
        assert len(block_ops) == 1
        # Provider actually created 4 issues and 1 blocking edge.
        assert len(patched._issues) == 4
        assert len(patched._blocked_by) == 1

    def test_accepts_tree_with_zero_features(self, tmp_path, patched):
        repo, file_path = _make_repo(
            tmp_path,
            {"schemaVersion": "1.0", "epic": {"ref": "e1", "title": "Epic", "body": "b", "features": []}},
        )
        plan = run_creation_pipeline(repo, file_path)
        assert [op.operation_type for op in plan.operations] == ["create_issue"]
        assert [op.refs for op in plan.operations] == [("e1",)]
        assert len(patched._issues) == 1
        assert len(patched._blocked_by) == 0

    def test_supports_cross_subtree_blocking_edge(self, tmp_path, patched):
        tree_doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "b",
                "features": [
                    {
                        "ref": "f1",
                        "title": "F1",
                        "body": "b",
                        "subtasks": [{"ref": "s1", "title": "S1", "body": "b", "blockedBy": ["s2"]}],
                    },
                    {"ref": "f2", "title": "F2", "body": "b", "subtasks": [{"ref": "s2", "title": "S2", "body": "b"}]},
                ],
            },
        }
        repo, file_path = _make_repo(tmp_path, tree_doc)
        plan = run_creation_pipeline(repo, file_path)
        create_refs = [op.refs[0] for op in plan.operations if op.operation_type == "create_issue"]
        assert create_refs.index("s2") < create_refs.index("s1")
        block_ops = [op for op in plan.operations if op.operation_type == "add_blocked_by"]
        assert len(block_ops) == 1
        assert block_ops[0].refs == ("s1", "s2")
        assert len(patched._blocked_by) == 1


class TestRunCreationPipelineDryRun:
    """T042 — dry-run runs full preflight but performs no mutation."""

    def test_dry_run_produces_plan_without_mutation(self, tmp_path, patched):
        repo, file_path = _make_repo(tmp_path, valid_tree_doc(with_blocking=True))
        plan = run_creation_pipeline(repo, file_path, dry_run=True)
        assert plan.dry_run is True
        assert all(op.status == "dry-run" for op in plan.operations)
        assert all(op.result is None for op in plan.operations)
        assert patched._issues == {}
        assert patched._blocked_by == set()


class TestRunCreationPipelinePlanContract:
    """T044 — the returned OperationPlan captures every operation in order."""

    def test_creates_precede_blocking_and_check_existing_false(self, tmp_path, patched):
        repo, file_path = _make_repo(tmp_path, valid_tree_doc(with_blocking=True))
        plan = run_creation_pipeline(repo, file_path)
        types = [op.operation_type for op in plan.operations]
        last_create = max(i for i, t in enumerate(types) if t == "create_issue")
        first_block = min(i for i, t in enumerate(types) if t == "add_blocked_by")
        assert last_create < first_block
        assert plan.check_existing is False
        assert all(
            op.orchestration_key == generate_orchestration_key(op.operation_type, *op.refs) for op in plan.operations
        )

        create_ops = [op for op in plan.operations if op.operation_type == "create_issue"]
        block_ops = [op for op in plan.operations if op.operation_type == "add_blocked_by"]
        create_id_by_ref: dict[str, str] = {}
        for op in create_ops:
            result = cast(ProviderIssueResult, op.result)
            create_id_by_ref[op.refs[0]] = result.identifier
            assert result.identifier

        for op in block_ops:
            result = cast(ProviderLinkResult, op.result)
            assert result.target_id == create_id_by_ref[op.refs[0]]
            assert result.source_id == create_id_by_ref[op.refs[1]]


class TestRunCreationPipelineFailurePropagation:
    def test_preflight_failure_propagates(self, tmp_path, patched):
        # start_from is unsupported -> PipelineValidationError before any mutation.
        repo, file_path = _make_repo(tmp_path, valid_tree_doc())
        with pytest.raises(PipelineValidationError):
            run_creation_pipeline(repo, file_path, start_from="s1")
        assert patched._issues == {}

    def test_execution_failure_propagates(self, tmp_path, monkeypatch):
        class _FailingProvider(InMemoryIssueProvider):
            def create_issue(self, title, body, issue_type, **kwargs):
                if title == "F1":
                    raise RuntimeError("boom")
                return super().create_issue(title, body, issue_type, **kwargs)

        fake = _FailingProvider("github")
        monkeypatch.setattr(cp, "resolve_provider_name", lambda repo, *, provider=None: "github")
        monkeypatch.setattr(cp, "get_issue_provider", lambda repo, *, provider=None: fake)
        repo, file_path = _make_repo(tmp_path, valid_tree_doc())
        with pytest.raises(PipelineExecutionError) as exc_info:
            run_creation_pipeline(repo, file_path)
        assert exc_info.value.operation_type == "create_issue"
        assert exc_info.value.refs == ("f1",)


class TestRunCreationPipelineDeterminism:
    """T054 — operation order stays stable across provider identities."""

    def test_operation_refs_are_stable_across_github_and_jira(self, tmp_path, monkeypatch):
        def _fresh_provider(repo, *, provider=None):
            return InMemoryIssueProvider(provider or "github")

        monkeypatch.setattr(cp, "resolve_provider_name", lambda repo, *, provider=None: provider or "github")
        monkeypatch.setattr(cp, "get_issue_provider", _fresh_provider)
        repo, file_path = _make_repo(tmp_path, valid_tree_doc(with_blocking=True))
        github_refs = [op.refs for op in run_creation_pipeline(repo, file_path, provider="github").operations]
        jira_refs = [op.refs for op in run_creation_pipeline(repo, file_path, provider="jira").operations]
        assert github_refs == jira_refs

    def test_operation_refs_are_stable_across_repeated_runs(self, tmp_path, monkeypatch):
        monkeypatch.setattr(cp, "resolve_provider_name", lambda repo, *, provider=None: "github")
        monkeypatch.setattr(cp, "get_issue_provider", lambda repo, *, provider=None: InMemoryIssueProvider("github"))
        repo, file_path = _make_repo(tmp_path, valid_tree_doc(with_blocking=True))
        first = [op.refs for op in run_creation_pipeline(repo, file_path).operations]
        second = [op.refs for op in run_creation_pipeline(repo, file_path).operations]
        assert first == second
