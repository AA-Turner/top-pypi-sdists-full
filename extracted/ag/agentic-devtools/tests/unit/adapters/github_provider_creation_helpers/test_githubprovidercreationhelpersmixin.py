"""Tests for GitHub issue-creation preparation and result helpers."""

from __future__ import annotations

import json

import pytest

from agentic_devtools.adapters.github_provider import GitHubProvider
from agentic_devtools.adapters.issue_provider import DefinitiveCreationFailure, ProviderIssueResult
from tests.unit.adapters.github_provider._fixtures import _make_run_mock


def _provider() -> GitHubProvider:
    return GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())


class TestGitHubProviderCreationHelpers:
    def test_prepare_creation_context_normalizes_parent_and_key(self):
        key = "a" * 64
        context = _provider()._prepare_creation_context("Title", "Body", "task", " #12 ", key, None)

        assert context.parent_id == "12"
        assert context.type_label == "task"
        assert context.orchestration_key == key
        assert context.lookup_key == key
        assert f"<!-- agdt-orch-key:{key} -->" in context.body

    @pytest.mark.parametrize("title", ["", "  ", None])
    def test_validate_creation_title_rejects_invalid_values(self, title):
        with pytest.raises(DefinitiveCreationFailure, match="title must be a non-empty string"):
            _provider()._validate_creation_title(title)

    def test_normalize_creation_parent_accepts_none(self):
        assert _provider()._normalize_creation_parent(None) is None

    def test_normalize_creation_parent_rejects_invalid_value(self):
        with pytest.raises(DefinitiveCreationFailure, match="numeric GitHub issue number"):
            _provider()._normalize_creation_parent("12/comments")

    @pytest.mark.parametrize(
        ("issue_type", "expected"),
        [
            ("task", "task"),
            ("sub-task", "cannot be mapped"),
            ("unknown", "no GitHub label mapping"),
            (" ", "issue_type must be a non-empty string"),
            (None, "issue_type must be a non-empty string"),
        ],
    )
    def test_resolve_creation_type(self, issue_type, expected):
        if expected == "task":
            assert _provider()._resolve_creation_type(issue_type) == expected
        else:
            with pytest.raises(DefinitiveCreationFailure, match=expected):
                _provider()._resolve_creation_type(issue_type)

    def test_embed_creation_key_without_key(self):
        assert _provider()._embed_creation_key("Body", None) == ("Body", None)

    def test_embed_creation_key_with_key(self):
        key = "b" * 64
        body, embedded_key = _provider()._embed_creation_key("Body", key)
        assert embedded_key == key
        assert f"<!-- agdt-orch-key:{key} -->" in body

    def test_dry_run_creation_result_records_manifest_entry(self):
        provider = _provider()
        context = provider._prepare_creation_context("Title", "Body", "task", None, None, None)

        result = provider._dry_run_creation_result(context)

        assert result.status == "dry-run"
        assert provider.get_dry_run_manifest()["issues"][0]["title"] == "Title"

    def test_find_existing_creation_skips_without_key(self):
        provider = _provider()
        context = provider._prepare_creation_context("Title", "Body", "task", None, None, None)
        assert provider._find_existing_creation(context) is None

    def test_find_existing_creation_uses_lookup_result(self, monkeypatch):
        provider = _provider()
        context = provider._prepare_creation_context("Title", "Body", "task", None, "c" * 64, None)
        existing = ProviderIssueResult(identifier="7", url="u/7", status="existing")
        monkeypatch.setattr(provider, "_lookup_existing_for_creation", lambda *_args: existing)

        assert provider._find_existing_creation(context) is existing

    def test_creation_labels_trims_and_deduplicates(self):
        assert GitHubProvider._creation_labels("task", [" TASK ", " extra ", "EXTRA", ""]) == ["task", "extra"]
        assert GitHubProvider._creation_labels("task", None) == ["task"]

    def test_recovered_creation_result_links_and_caches(self):
        provider = _provider()
        context = provider._prepare_creation_context("Title", "Body", "task", None, "d" * 64, None)
        recovered = ProviderIssueResult(identifier="8", url="u/8", status="existing")

        result = provider._recovered_creation_result(recovered, context)

        assert result.status == "existing"
        assert provider._idempotency_cache[context.orchestration_key] is result

    @pytest.mark.parametrize(
        ("stdout", "expected"),
        [
            (json.dumps({"number": 12, "html_url": "u", "id": 120, "node_id": "I_x"}), "12"),
            (json.dumps([]), "Unexpected response type"),
            (json.dumps({"number": 0}), "valid issue number"),
        ],
    )
    def test_created_issue_result(self, stdout, expected):
        if expected == "12":
            assert _provider()._created_issue_result(stdout, ["task"]).identifier == expected
        else:
            with pytest.raises(ValueError, match=expected):
                _provider()._created_issue_result(stdout, ["task"])

    def test_cache_created_issue_skips_missing_key(self):
        provider = _provider()
        issue = ProviderIssueResult(identifier="9", url="u/9", status="created")
        provider._cache_created_issue(issue, None)
        assert provider._idempotency_cache == {}

    def test_cache_created_issue_stores_existing_status(self):
        provider = _provider()
        issue = ProviderIssueResult(identifier="9", url="u/9", status="created")

        provider._cache_created_issue(issue, "key")

        assert provider._idempotency_cache["key"].status == "existing"
