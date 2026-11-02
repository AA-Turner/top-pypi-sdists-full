"""End-to-end mapping recovery and relationship reconciliation tests."""

from __future__ import annotations

import json
import subprocess

import pytest

import agentic_devtools.cli.jira.creation_pipeline as cp
from agentic_devtools.adapters.issue_provider import InMemoryIssueProvider
from agentic_devtools.cli.workflows.create_epic.records import (
    atomic_write_mapping_document,
    initialize_mapping_document,
)


@pytest.fixture
def patched_provider(monkeypatch, tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True, shell=False)
    monkeypatch.chdir(tmp_path)
    provider_ref = InMemoryIssueProvider("github")
    provider_ref.owner_repo = "owner/repo"
    monkeypatch.setattr(cp, "resolve_provider_name", lambda repo, *, provider=None: "github")
    monkeypatch.setattr(cp, "resolve_provider_target", lambda repo, provider_name: "owner/repo")
    monkeypatch.setattr(cp, "get_issue_provider", lambda repo, *, provider=None: provider_ref)
    return provider_ref


def _make_repo(tmp_path, doc, name="tree.json"):
    repo = tmp_path / "repo"
    repo.mkdir(exist_ok=True)
    file_path = repo / name
    file_path.write_text(json.dumps(doc), encoding="utf-8")
    return repo, file_path


def _tree_doc() -> dict:
    return {
        "schemaVersion": "2.0",
        "treeId": "12345678-1234-5678-1234-567812345678",
        "epic": {
            "ref": "e1",
            "title": "Epic",
            "body": "b",
            "features": [
                {
                    "ref": "f1",
                    "title": "F1",
                    "body": "b",
                    "subtasks": [
                        {"ref": "s1", "title": "S1", "body": "b", "blockedBy": ["s2"]},
                        {"ref": "s2", "title": "S2", "body": "b"},
                    ],
                }
            ],
        },
    }


def _mapping_path(tmp_path, monkeypatch):
    path = tmp_path / "mapping.json"
    monkeypatch.setattr(cp, "resolve_mapping_path", lambda tree, *, create=False: path)
    return path


def test_schema_v1_plan_rerun_is_idempotent_and_distinct_plans_do_not_collide(tmp_path, patched_provider, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    first_path = repo / "first.json"
    second_path = repo / "second.json"
    first_doc = {
        "schemaVersion": "1.0",
        "epic": {"ref": "e1", "title": "Epic", "body": "b", "features": []},
    }
    second_doc = json.loads(json.dumps(first_doc))
    second_doc["epic"]["title"] = "A separate epic"
    first_path.write_text(json.dumps(first_doc), encoding="utf-8")
    second_path.write_text(json.dumps(second_doc), encoding="utf-8")

    first = cp.run_creation_pipeline(repo, first_path)
    rerun = cp.run_creation_pipeline(repo, first_path)

    assert all(operation.status == "created" for operation in first.create_operations)
    assert all(operation.status == "existing" for operation in rerun.create_operations)
    assert len(patched_provider.issues) == 1

    second = cp.run_creation_pipeline(repo, second_path)

    assert all(operation.status == "created" for operation in second.create_operations)
    assert len(patched_provider.issues) == 2
    assert json.loads(first_path.read_text(encoding="utf-8"))["schemaVersion"] == "2.0"


def test_completed_rerun_skips_all_issues(tmp_path, patched_provider, monkeypatch):
    tree = _tree_doc()
    mapping_path = _mapping_path(tmp_path, monkeypatch)
    repo, file_path = _make_repo(tmp_path, tree)
    atomic_write_mapping_document(
        mapping_path,
        initialize_mapping_document(tree["treeId"], "github", "owner/repo"),
    )

    first = cp.run_creation_pipeline(repo, file_path)
    second = cp.run_creation_pipeline(repo, file_path)

    assert len(first.create_operations) == 4
    assert len(second.create_operations) == 4
    assert all(operation.status == "existing" for operation in second.create_operations)
    assert second.created_issue_count == 0
    assert second.skipped_issue_count == 4
    assert len(patched_provider.issues) == 4


def test_partial_mapping_creates_missing_items_and_reconciles_links(tmp_path, patched_provider, monkeypatch):
    tree = _tree_doc()
    mapping_path = _mapping_path(tmp_path, monkeypatch)
    repo, file_path = _make_repo(tmp_path, tree)
    atomic_write_mapping_document(
        mapping_path,
        initialize_mapping_document(tree["treeId"], "github", "owner/repo"),
    )

    first = cp.run_creation_pipeline(repo, file_path)
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    mapping["entries"]["s1"] = {
        "status": "created",
        "provider_id": mapping["entries"]["s1"]["provider_id"],
    }
    patched_provider._parent_child.clear()
    patched_provider._blocked_by.clear()
    mapping_path.write_text(json.dumps(mapping), encoding="utf-8")

    rerun = cp.run_creation_pipeline(repo, file_path)

    assert all(operation.status == "existing" for operation in rerun.create_operations)
    assert rerun.skipped_issue_count == 4
    assert patched_provider.parent_child_links
    assert patched_provider.blocked_by_links
    assert len(first.create_operations) == 4


def test_v2_tree_without_mapping_remains_supported(tmp_path, patched_provider, monkeypatch):
    tree = _tree_doc()
    mapping_path = _mapping_path(tmp_path, monkeypatch)
    repo, file_path = _make_repo(tmp_path, tree)

    plan = cp.run_creation_pipeline(repo, file_path)

    assert plan.created_issue_count == 4
    assert plan.check_existing is False
    assert mapping_path.is_file()
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    assert mapping["entries"]["link_subissue:e1:f1"]["status"] == "confirmed"
    assert mapping["entries"]["add_blocked_by:s1:s2"]["status"] == "confirmed"


def test_start_from_resumes_at_requested_reference(tmp_path, patched_provider, monkeypatch):
    tree = _tree_doc()
    mapping_path = _mapping_path(tmp_path, monkeypatch)
    repo, file_path = _make_repo(tmp_path, tree)
    atomic_write_mapping_document(
        mapping_path,
        initialize_mapping_document(tree["treeId"], "github", "owner/repo"),
    )

    cp.run_creation_pipeline(repo, file_path)
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    mapping["entries"].pop("s1")
    mapping_path.write_text(json.dumps(mapping), encoding="utf-8")

    resumed = cp.run_creation_pipeline(repo, file_path, start_from="s1")

    assert [operation.refs[0] for operation in resumed.create_operations if operation.status == "existing"] == ["s1"]
    assert all(operation.refs[0] != "e1" for operation in resumed.create_operations)


def test_reconciliation_normalizes_all_malformed_pending_relationship_timestamps(
    tmp_path, patched_provider, monkeypatch
):
    tree = _tree_doc()
    mapping_path = _mapping_path(tmp_path, monkeypatch)
    repo, file_path = _make_repo(tmp_path, tree)
    atomic_write_mapping_document(
        mapping_path,
        initialize_mapping_document(tree["treeId"], "github", "owner/repo"),
    )
    cp.run_creation_pipeline(repo, file_path)
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    mapping["entries"]["link_subissue:e1:f1"]["status"] = "pending"
    mapping["entries"]["link_subissue:e1:f1"].pop("confirmed_at")
    mapping["entries"]["link_subissue:e1:f1"].pop("result")
    mapping["entries"]["link_subissue:e1:f1"]["pending_since"] = "not-a-timestamp"
    mapping["entries"]["add_blocked_by:s1:s2"]["status"] = "pending"
    mapping["entries"]["add_blocked_by:s1:s2"].pop("confirmed_at")
    mapping["entries"]["add_blocked_by:s1:s2"].pop("result")
    mapping["entries"]["add_blocked_by:s1:s2"]["pending_since"] = "not-a-timestamp"
    mapping_path.write_text(json.dumps(mapping), encoding="utf-8")

    cp.run_creation_pipeline(repo, file_path)

    repaired = json.loads(mapping_path.read_text(encoding="utf-8"))["entries"]
    assert repaired["link_subissue:e1:f1"]["status"] == "confirmed"
    assert repaired["add_blocked_by:s1:s2"]["status"] == "confirmed"
    assert repaired["link_subissue:e1:f1"]["confirmed_at"].endswith("Z")
    assert repaired["add_blocked_by:s1:s2"]["confirmed_at"].endswith("Z")


def test_missing_pending_node_timestamp_requires_force_resume(tmp_path, patched_provider, monkeypatch):
    tree = _tree_doc()
    mapping_path = _mapping_path(tmp_path, monkeypatch)
    repo, file_path = _make_repo(tmp_path, tree)
    mapping = initialize_mapping_document(tree["treeId"], "github", "owner/repo")
    mapping["entries"]["e1"] = {"status": "pending"}
    mapping_path.write_text(json.dumps(mapping), encoding="utf-8")

    with pytest.raises(cp.PipelineValidationError, match="--force-resume"):
        cp.run_creation_pipeline(repo, file_path)

    assert patched_provider.issues == {}


def test_malformed_pending_node_timestamp_recovers_with_force_resume(tmp_path, patched_provider, monkeypatch):
    tree = _tree_doc()
    mapping_path = _mapping_path(tmp_path, monkeypatch)
    repo, file_path = _make_repo(tmp_path, tree)
    mapping = initialize_mapping_document(tree["treeId"], "github", "owner/repo")
    mapping["entries"]["e1"] = {"status": "pending", "pending_since": "not-a-timestamp"}
    mapping_path.write_text(json.dumps(mapping), encoding="utf-8")

    plan = cp.run_creation_pipeline(repo, file_path, force_resume=True)

    assert plan.created_issue_count == 4
    assert len(patched_provider.issues) == 4
    persisted = json.loads(mapping_path.read_text(encoding="utf-8"))
    assert persisted["entries"]["e1"] == {"status": "created", "provider_id": "1"}
