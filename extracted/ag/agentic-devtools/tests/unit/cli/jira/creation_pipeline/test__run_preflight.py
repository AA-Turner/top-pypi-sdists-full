"""Tests for ``_run_preflight`` (T034, T036).

The preflight gate is mutation-free.  Provider construction is patched to an
in-memory double so no live credential or network access is required.
"""

from __future__ import annotations

import json

import pytest

import agentic_devtools.cli.jira.creation_pipeline as cp
from agentic_devtools.adapters.issue_provider import InMemoryIssueProvider
from agentic_devtools.cli.jira.creation_pipeline import PipelineValidationError, _run_preflight

from .conftest import valid_tree_doc


@pytest.fixture
def patched_provider(monkeypatch):
    """Patch provider resolution/construction to an in-memory double."""
    fake = InMemoryIssueProvider("github")
    monkeypatch.setattr(cp, "resolve_provider_name", lambda repo, *, provider=None: "github")
    monkeypatch.setattr(cp, "get_issue_provider", lambda repo, *, provider=None: fake)
    return fake


def _make_repo(tmp_path, doc):
    repo = tmp_path / "repo"
    repo.mkdir()
    file_path = repo / "tree.json"
    file_path.write_text(json.dumps(doc), encoding="utf-8")
    return repo, file_path


class TestRunPreflightHappyPath:
    def test_returns_context_with_full_node_index(self, tmp_path, patched_provider):
        repo, file_path = _make_repo(tmp_path, valid_tree_doc(with_blocking=True))
        ctx = _run_preflight(repo, file_path)
        assert ctx.provider_name == "github"
        assert ctx.provider is patched_provider
        assert set(ctx.node_index) == {"e1", "f1", "s1", "s2"}

    def test_no_provider_mutation_during_preflight(self, tmp_path, patched_provider):
        repo, file_path = _make_repo(tmp_path, valid_tree_doc())
        _run_preflight(repo, file_path)
        assert patched_provider._issues == {}


class TestRunPreflightValidationFailures:
    def test_start_from_is_rejected(self, tmp_path, patched_provider):
        repo, file_path = _make_repo(tmp_path, valid_tree_doc())
        with pytest.raises(PipelineValidationError) as exc_info:
            _run_preflight(repo, file_path, start_from="s1")
        assert "start_from" in str(exc_info.value)

    def test_missing_repo_root_raises(self, tmp_path, patched_provider):
        repo, file_path = _make_repo(tmp_path, valid_tree_doc())
        with pytest.raises(PipelineValidationError):
            _run_preflight(tmp_path / "does-not-exist", file_path)

    def test_missing_definition_file_raises(self, tmp_path, patched_provider):
        repo, _ = _make_repo(tmp_path, valid_tree_doc())
        with pytest.raises(PipelineValidationError):
            _run_preflight(repo, repo / "missing.json")

    def test_path_traversal_is_rejected(self, tmp_path, patched_provider):
        repo, _ = _make_repo(tmp_path, valid_tree_doc())
        outside = tmp_path / "outside.json"
        outside.write_text(json.dumps(valid_tree_doc()), encoding="utf-8")
        with pytest.raises(PipelineValidationError) as exc_info:
            _run_preflight(repo, outside)
        assert "traversal" in str(exc_info.value).lower()

    def test_missing_hierarchy_capability_raises(self, tmp_path, monkeypatch):
        repo, file_path = _make_repo(tmp_path, valid_tree_doc())

        class _NoCapabilityProvider:
            pass

        monkeypatch.setattr(cp, "resolve_provider_name", lambda repo, *, provider=None: "github")
        monkeypatch.setattr(cp, "get_issue_provider", lambda repo, *, provider=None: _NoCapabilityProvider())
        with pytest.raises(PipelineValidationError) as exc_info:
            _run_preflight(repo, file_path)
        assert "hierarchy validation" in str(exc_info.value).lower()

    def test_repo_root_not_a_directory_raises(self, tmp_path, patched_provider):
        # A file (not a directory) passed as the repo root.
        repo, file_path = _make_repo(tmp_path, valid_tree_doc())
        not_a_dir = tmp_path / "afile"
        not_a_dir.write_text("x", encoding="utf-8")
        with pytest.raises(PipelineValidationError) as exc_info:
            _run_preflight(not_a_dir, file_path)
        assert "not a directory" in str(exc_info.value).lower()

    def test_malformed_definition_raises_validation_error(self, tmp_path, patched_provider):
        repo = tmp_path / "repo"
        repo.mkdir(exist_ok=True)
        bad = repo / "bad.json"
        bad.write_text("{ not valid json", encoding="utf-8")
        with pytest.raises(PipelineValidationError) as exc_info:
            _run_preflight(repo, bad)
        assert "load epic-tree" in str(exc_info.value).lower()
        assert exc_info.value.cause is not None

    def test_definition_path_directory_raises_validation_error(self, tmp_path, patched_provider):
        repo = tmp_path / "repo"
        repo.mkdir(exist_ok=True)
        as_dir = repo / "tree.json"
        as_dir.mkdir()
        with pytest.raises(PipelineValidationError) as exc_info:
            _run_preflight(repo, as_dir)
        assert "load epic-tree" in str(exc_info.value).lower()
        assert isinstance(exc_info.value.cause, OSError)

    def test_invalid_issue_type_raises(self, tmp_path, monkeypatch):
        doc = valid_tree_doc()
        doc["epic"]["issueType"] = "Nonsense"
        repo, file_path = _make_repo(tmp_path, doc)
        fake = InMemoryIssueProvider("github")
        monkeypatch.setattr(cp, "resolve_provider_name", lambda repo, *, provider=None: "github")
        monkeypatch.setattr(cp, "get_issue_provider", lambda repo, *, provider=None: fake)
        with pytest.raises(PipelineValidationError):
            _run_preflight(repo, file_path)

    def test_provider_resolution_error_wrapped_as_validation(self, tmp_path, monkeypatch):
        repo, file_path = _make_repo(tmp_path, valid_tree_doc())

        def _raise_provider_resolution(*args, **kwargs):
            raise cp.ConfigError("config.json", "provider", "missing provider")

        monkeypatch.setattr(cp, "resolve_provider_name", _raise_provider_resolution)
        monkeypatch.setattr(cp, "get_issue_provider", lambda repo, *, provider=None: InMemoryIssueProvider("github"))

        with pytest.raises(PipelineValidationError) as exc_info:
            _run_preflight(repo, file_path)
        assert "provider resolution failed" in str(exc_info.value).lower()
        assert isinstance(exc_info.value.cause, cp.ConfigError)

    def test_provider_construction_error_wrapped_as_validation(self, tmp_path, monkeypatch):
        repo, file_path = _make_repo(tmp_path, valid_tree_doc())
        monkeypatch.setattr(cp, "resolve_provider_name", lambda repo, *, provider=None: "github")

        def _raise_provider_construction(*args, **kwargs):
            raise cp.ConfigError("config.json", "provider", "missing coordinates")

        monkeypatch.setattr(cp, "get_issue_provider", _raise_provider_construction)
        with pytest.raises(PipelineValidationError) as exc_info:
            _run_preflight(repo, file_path)
        assert "provider construction failed" in str(exc_info.value).lower()
        assert isinstance(exc_info.value.cause, cp.ConfigError)

    def test_invalid_hierarchy_pair_is_rejected_without_mutation(self, tmp_path, monkeypatch):
        doc = valid_tree_doc()
        doc["epic"]["features"][0]["subtasks"][0]["issueType"] = "Task"
        repo, file_path = _make_repo(tmp_path, doc)
        fake = InMemoryIssueProvider("github")
        monkeypatch.setattr(cp, "resolve_provider_name", lambda repo, *, provider=None: "github")
        monkeypatch.setattr(cp, "get_issue_provider", lambda repo, *, provider=None: fake)

        with pytest.raises(PipelineValidationError, match="Invalid hierarchy pair"):
            _run_preflight(repo, file_path)

        assert fake._issues == {}

    def test_jira_native_issue_types_are_normalized_for_validation(self, tmp_path, monkeypatch):
        doc = valid_tree_doc()
        doc["epic"]["issueType"] = "Initiative"
        doc["epic"]["features"][0]["issueType"] = "Story"
        doc["epic"]["features"][0]["subtasks"][0]["issueType"] = "Sub-task"
        repo, file_path = _make_repo(tmp_path, doc)
        fake = InMemoryIssueProvider("jira")
        monkeypatch.setattr(cp, "resolve_provider_name", lambda repo, *, provider=None: "jira")
        monkeypatch.setattr(cp, "get_issue_provider", lambda repo, *, provider=None: fake)

        context = _run_preflight(repo, file_path)

        assert {meta.issue_type for meta in context.node_index.values()} == {"epic", "feature", "subtask"}
