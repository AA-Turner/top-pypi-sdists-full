"""Authoritative end-to-end tests for the topological creation pipeline (T032).

These integration tests exercise the *real* internal helpers of
``run_creation_pipeline`` — preflight, ordering, issue creation, and blocking —
using an in-memory adapter double (never mocked helpers).  They cover the
complete happy path for epic, feature, subtask, and blocking creation (US1,
FR-001 through FR-009), including a complementary-declaration deduplication
scenario.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import agentic_devtools.cli.jira.creation_pipeline as cp
from agentic_devtools.adapters.issue_provider import InMemoryIssueProvider
from agentic_devtools.cli.jira.creation_pipeline import run_creation_pipeline


@pytest.fixture
def in_memory_github(monkeypatch):
    """Bind the pipeline to a fresh in-memory GitHub-style provider."""
    _provider_ref = InMemoryIssueProvider("github")
    monkeypatch.setattr(cp, "resolve_provider_name", lambda repo, *, provider=None: "github")
    monkeypatch.setattr(cp, "get_issue_provider", lambda repo, *, provider=None: _provider_ref)
    return _provider_ref


def _write_repo(tmp_path: Path, doc: dict) -> tuple[Path, Path]:
    repo = tmp_path / "repo"
    repo.mkdir()
    file_path = repo / "epic-tree.json"
    file_path.write_text(json.dumps(doc), encoding="utf-8")
    return repo, file_path


def _full_tree_doc() -> dict:
    return {
        "schemaVersion": "1.0",
        "epic": {
            "ref": "epic",
            "title": "Epic",
            "body": "epic body",
            "features": [
                {
                    "ref": "feat-a",
                    "title": "Feature A",
                    "body": "b",
                    "subtasks": [
                        {"ref": "s1", "title": "S1", "body": "b", "blockedBy": ["s2"]},
                        {"ref": "s2", "title": "S2", "body": "b"},
                    ],
                },
                {
                    "ref": "feat-b",
                    "title": "Feature B",
                    "body": "b",
                    "subtasks": [{"ref": "s3", "title": "S3", "body": "b"}],
                },
            ],
        },
    }


class TestValidTreeExecutionHappyPath:
    def test_all_nodes_created_with_hierarchy(self, tmp_path, in_memory_github):
        repo, file_path = _write_repo(tmp_path, _full_tree_doc())
        plan = run_creation_pipeline(repo, file_path)

        # Every node was created exactly once.
        create_refs = sorted(op.refs[0] for op in plan.operations if op.operation_type == "create_issue")
        assert create_refs == ["epic", "feat-a", "feat-b", "s1", "s2", "s3"]
        assert len(in_memory_github._issues) == 6

        # Hierarchy links established during creation.
        by_title = {rec["title"]: rec for rec in in_memory_github._issues.values()}
        assert by_title["Feature A"]["parent_id"] is not None
        assert by_title["S1"]["parent_id"] == _id_of(in_memory_github, "Feature A")
        assert by_title["S3"]["parent_id"] == _id_of(in_memory_github, "Feature B")

    def test_blocking_edge_created_after_creates(self, tmp_path, in_memory_github):
        repo, file_path = _write_repo(tmp_path, _full_tree_doc())
        plan = run_creation_pipeline(repo, file_path)

        block_ops = [op for op in plan.operations if op.operation_type == "add_blocked_by"]
        assert len(block_ops) == 1
        assert block_ops[0].refs == ("s1", "s2")
        assert len(in_memory_github._blocked_by) == 1

        # s2 (the blocker) is created before s1 (the blocked).
        order = [op.refs[0] for op in plan.operations if op.operation_type == "create_issue"]
        assert order.index("s2") < order.index("s1")


class TestValidTreeComplementaryDeduplication:
    """A ``blocks``/``blockedBy`` complementary pair collapses to one edge."""

    def test_complementary_declaration_dedupes(self, tmp_path, in_memory_github):
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "epic",
                "title": "Epic",
                "body": "b",
                "features": [
                    {
                        "ref": "feat-a",
                        "title": "Feature A",
                        "body": "b",
                        "subtasks": [
                            {"ref": "s1", "title": "S1", "body": "b", "blockedBy": ["s2"]},
                            {"ref": "s2", "title": "S2", "body": "b", "blocks": ["s1"]},
                        ],
                    }
                ],
            },
        }
        repo, file_path = _write_repo(tmp_path, doc)
        plan = run_creation_pipeline(repo, file_path)

        block_ops = [op for op in plan.operations if op.operation_type == "add_blocked_by"]
        assert len(block_ops) == 1
        assert block_ops[0].refs == ("s1", "s2")
        assert len(in_memory_github._blocked_by) == 1


def _id_of(provider: InMemoryIssueProvider, title: str) -> str:
    for identifier, rec in provider._issues.items():
        if rec["title"] == title:
            return identifier
    raise AssertionError(f"issue with title {title!r} not found")
