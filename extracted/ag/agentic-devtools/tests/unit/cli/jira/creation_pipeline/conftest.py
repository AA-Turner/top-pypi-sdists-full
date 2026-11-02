"""Shared fixtures and helpers for creation-pipeline unit tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from agentic_devtools.adapters.issue_provider import InMemoryIssueProvider
from agentic_devtools.epic_tree.models import EpicNode, EpicTree, FeatureNode, SubtaskNode


def make_tree(*, with_blocking: bool = False, empty_feature: bool = False) -> EpicTree:
    """Build a small valid epic tree for pipeline tests."""
    subtasks_f1 = (
        SubtaskNode(
            ref="s1",
            title="S1",
            body="b",
            issueType="Subtask",
            blockedBy=("s2",) if with_blocking else (),
        ),
        SubtaskNode(ref="s2", title="S2", body="b", issueType="Subtask"),
    )
    features = [
        FeatureNode(ref="f1", title="F1", body="b", issueType="Feature", subtasks=subtasks_f1),
    ]
    if empty_feature:
        features.append(FeatureNode(ref="f2", title="F2", body="b", issueType="Feature", subtasks=()))
    epic = EpicNode(ref="e1", title="Epic", body="b", issueType="Epic", features=tuple(features))
    return EpicTree(schemaVersion="1.0", epic=epic)


def make_context(tree: EpicTree | None = None, *, style: str = "github"):
    """Build a ``_PreflightContext`` bound to an in-memory provider."""
    import agentic_devtools.cli.jira.creation_pipeline as cp

    tree = tree if tree is not None else make_tree(with_blocking=True)
    provider = InMemoryIssueProvider(style)
    return cp._PreflightContext(
        tree=tree,
        provider=provider,
        provider_name="github" if style == "github" else "jira",
        node_index=cp._build_node_index(tree),
    )


@pytest.fixture
def in_memory_context():
    return make_context()


def write_repo_with_tree(
    tmp_path: Path, tree_doc: dict, *, adapter: str = "github", filename: str = "tree.json"
) -> tuple[Path, Path]:
    """Create a repo dir with a config and a definition file; return (repo, file)."""
    repo = tmp_path / "repo"
    (repo / ".github").mkdir(parents=True)
    (repo / ".github" / "agdt-config.json").write_text(
        json.dumps({"platform": {"issue_adapter": adapter}}), encoding="utf-8"
    )
    (repo / ".git").mkdir()
    file_path = repo / filename
    file_path.write_text(json.dumps(tree_doc), encoding="utf-8")
    return repo, file_path


def valid_tree_doc(*, with_blocking: bool = False) -> dict:
    """Return a JSON-serializable valid epic-tree document."""
    s1: dict = {"ref": "s1", "title": "S1", "body": "b"}
    if with_blocking:
        s1["blockedBy"] = ["s2"]
    return {
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
                    "subtasks": [s1, {"ref": "s2", "title": "S2", "body": "b"}],
                }
            ],
        },
    }
