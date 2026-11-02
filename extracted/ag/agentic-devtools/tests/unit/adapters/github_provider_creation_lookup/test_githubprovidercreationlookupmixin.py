"""Tests for GitHubProvider."""

from __future__ import annotations

import hashlib
import json
import subprocess

import pytest

from agentic_devtools.adapters.github_provider import GitHubProvider
from agentic_devtools.adapters.issue_provider import (
    DefinitiveCreationFailure,
    PreCreateLookup,
    ProviderIssueResult,
    ProviderLinkResult,
)
from tests.unit.adapters.github_provider._fixtures import _make_run_mock


class TestGitHubProviderCreateIssue:
    """Tests for GitHubProvider.create_issue."""

    def test_create_issue_with_orchestration_key_finds_existing(self):
        search_response = json.dumps(
            {"items": [{"number": 99, "html_url": "https://github.com/org/repo/issues/99", "id": 999}]}
        )
        captured_calls: list[list[str]] = []

        def mock_run(*args, **kwargs):
            captured_calls.append(list(args[0]))
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=search_response, stderr="")

        body = "Content\n\n<!-- agdt-orch-key:" + "a" * 64 + " -->"
        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.create_issue("Title", body, "task", dry_run=False)
        assert result.status == "existing"
        assert result.identifier == "99"
        # T015: an orchestration-key hit must short-circuit before any create POST.
        create_posts = [
            call
            for call in captured_calls
            if "--method" in call
            and call[call.index("--method") + 1] == "POST"
            and any(a.endswith("/issues") for a in call)
        ]
        assert create_posts == [], "create_issue must not POST a new issue when an existing one is found"

    def test_create_issue_orch_key_search_returns_empty(self):
        """create_issue with orch key that doesn't match creates a new issue."""
        responses = [
            json.dumps({"items": []}),  # search returns empty
            json.dumps({"number": 55, "html_url": "https://github.com/org/repo/issues/55", "id": 550}),
        ]
        call_idx = {"i": 0}

        def mock_run(*args, **kwargs):
            resp = responses[call_idx["i"]] if call_idx["i"] < len(responses) else "{}"
            call_idx["i"] += 1
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=resp, stderr="")

        body = "Content\n\n<!-- agdt-orch-key:" + "b" * 64 + " -->"
        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.create_issue("Title", body, "task", dry_run=False)
        assert result.status == "created"
        assert result.identifier == "55"

    def test_create_issue_reuses_precreate_lookup_miss(self, monkeypatch):
        key = "d" * 64
        response = json.dumps({"number": 55, "html_url": "https://github.com/org/repo/issues/55", "id": 550})
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout=response))
        monkeypatch.setattr(
            provider,
            "_find_by_orchestration_key",
            lambda _key: pytest.fail("pre-create lookup miss must not be searched again"),
        )

        result = provider.create_issue_with_precreate_lookup(
            "Title",
            "Body",
            "task",
            idempotency_key=key,
            precreate_lookup=PreCreateLookup(orchestration_key=key, issue=None),
        )

        assert result.status == "created"
        assert result.identifier == "55"

    def test_create_issue_finds_legacy_raw_orchestration_key(self):
        key = "legacy-key"
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
        calls = []

        def mock_run(*args, **kwargs):
            argv = args[0]
            calls.append(argv)
            query = argv[argv.index("-f") + 1]
            items = (
                [{"number": 55, "html_url": "https://github.com/org/repo/issues/55", "id": 550}]
                if f"agdt-orch-key:{key}" in query
                else []
            )
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=json.dumps({"items": items}), stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)

        result = provider.create_issue("Title", "Body", "task", idempotency_key=key)

        assert result.status == "existing"
        assert result.identifier == "55"
        assert f"agdt-orch-key:{digest}" in calls[0][calls[0].index("-f") + 1]
        assert f"agdt-orch-key:{key}" in calls[1][calls[1].index("-f") + 1]
        assert len(calls) == 2

    def test_create_issue_reuses_precreate_lookup_match(self, monkeypatch):
        key = "e" * 64
        existing = ProviderIssueResult(identifier="99", url="u/99", status="existing")
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        monkeypatch.setattr(
            provider,
            "_find_by_orchestration_key",
            lambda _key: pytest.fail("pre-create lookup match must be reused"),
        )

        result = provider.create_issue(
            "Title",
            "Body",
            "task",
            idempotency_key=key,
            precreate_lookup=PreCreateLookup(orchestration_key=key, issue=existing),
        )

        assert result.status == "existing"
        assert result.identifier == "99"

    def test_create_issue_rejects_mismatched_precreate_lookup_key(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())

        with pytest.raises(DefinitiveCreationFailure, match="must match"):
            provider.create_issue(
                "Title",
                "Body",
                "task",
                idempotency_key="key-1",
                precreate_lookup=PreCreateLookup(orchestration_key="key-2", issue=None),
            )

    def test_create_issue_rejects_unverified_legacy_match(self, monkeypatch):
        tree_key = "a" * 64
        legacy_key = "b" * 64
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        monkeypatch.setattr(
            provider,
            "_find_by_orchestration_key",
            lambda key: (
                ProviderIssueResult(identifier="99", url="u/99", status="existing") if key == legacy_key else None
            ),
        )

        with pytest.raises(DefinitiveCreationFailure, match="(?i)unverified legacy.*e1"):
            provider.create_issue(
                "Title",
                "Body",
                "task",
                idempotency_key=tree_key,
                precreate_lookup=PreCreateLookup(
                    orchestration_key=tree_key,
                    issue=None,
                    legacy_orchestration_key=legacy_key,
                    node_ref="e1",
                ),
            )

    def test_create_issue_reuses_verified_legacy_match(self, monkeypatch):
        tree_key = "e" * 64
        legacy_key = "f" * 64
        existing = ProviderIssueResult(identifier="99", url="u/99", status="existing")
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        monkeypatch.setattr(
            provider,
            "_find_by_orchestration_key",
            lambda key: existing if key == legacy_key else None,
        )

        result = provider.create_issue(
            "Title",
            "Body",
            "task",
            idempotency_key=tree_key,
            precreate_lookup=PreCreateLookup(
                orchestration_key=tree_key,
                issue=None,
                legacy_orchestration_key=legacy_key,
                legacy_adoption_permitted=True,
                node_ref="e1",
            ),
        )

        assert result.status == "existing"
        assert result.identifier == existing.identifier

    def test_create_issue_accepts_same_match_for_both_keys(self, monkeypatch):
        tree_key = "a" * 64
        legacy_key = "b" * 64
        existing = ProviderIssueResult(identifier="99", url="u/99", status="existing")
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        monkeypatch.setattr(provider, "_find_by_orchestration_key", lambda _key: existing)

        result = provider.create_issue(
            "Title",
            "Body",
            "task",
            idempotency_key=tree_key,
            precreate_lookup=PreCreateLookup(
                orchestration_key=tree_key,
                issue=existing,
                legacy_orchestration_key=legacy_key,
                node_ref="e1",
            ),
        )

        assert result.status == "existing"
        assert result.identifier == existing.identifier

    @pytest.mark.parametrize(
        ("legacy_key", "node_ref", "permitted"),
        [("", "e1", False), ("b" * 64, None, False), ("b" * 64, "e1", 1)],
    )
    def test_create_issue_rejects_invalid_legacy_lookup(self, legacy_key, node_ref, permitted):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())

        with pytest.raises(DefinitiveCreationFailure, match="legacy candidate is invalid"):
            provider.create_issue(
                "Title",
                "Body",
                "task",
                idempotency_key="a" * 64,
                precreate_lookup=PreCreateLookup(
                    orchestration_key="a" * 64,
                    issue=None,
                    legacy_orchestration_key=legacy_key,
                    legacy_adoption_permitted=permitted,
                    node_ref=node_ref,
                ),
            )

    def test_create_issue_rejects_precreate_match_conflicting_with_cache(self):
        tree_key = "a" * 64
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        provider._idempotency_cache[tree_key] = ProviderIssueResult(identifier="98", url="u/98", status="existing")

        with pytest.raises(DefinitiveCreationFailure, match="Ambiguous tree-scoped lookup"):
            provider.create_issue(
                "Title",
                "Body",
                "task",
                idempotency_key=tree_key,
                precreate_lookup=PreCreateLookup(
                    orchestration_key=tree_key,
                    issue=ProviderIssueResult(identifier="99", url="u/99", status="existing"),
                ),
            )

    def test_create_issue_accepts_precreate_match_matching_cache(self):
        tree_key = "a" * 64
        existing = ProviderIssueResult(identifier="98", url="u/98", status="existing")
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        provider._idempotency_cache[tree_key] = existing

        result = provider.create_issue(
            "Title",
            "Body",
            "task",
            idempotency_key=tree_key,
            precreate_lookup=PreCreateLookup(orchestration_key=tree_key, issue=existing),
        )

        assert result.status == "existing"
        assert result.identifier == existing.identifier

    def test_create_issue_rejects_ambiguous_tree_and_legacy_matches(self, monkeypatch):
        tree_key = "c" * 64
        legacy_key = "d" * 64
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        monkeypatch.setattr(
            provider,
            "_find_by_orchestration_key",
            lambda key: (
                ProviderIssueResult(identifier="99", url="u/99", status="existing") if key == legacy_key else None
            ),
        )

        with pytest.raises(DefinitiveCreationFailure, match="(?i)ambiguous.*e1"):
            provider.create_issue(
                "Title",
                "Body",
                "task",
                idempotency_key=tree_key,
                precreate_lookup=PreCreateLookup(
                    orchestration_key=tree_key,
                    issue=ProviderIssueResult(identifier="98", url="u/98", status="existing"),
                    legacy_orchestration_key=legacy_key,
                    node_ref="e1",
                ),
            )

    def test_create_issue_idempotency_cache_short_circuits_search(self):
        """Second call with same orch key returns cached result without a search-API round-trip."""
        issue_response = json.dumps({"number": 42, "html_url": "u", "id": 420, "node_id": "I_x"})
        search_calls: list[list[str]] = []

        def mock_run(*args, **kwargs):
            argv = args[0]
            if "/search/issues" in " ".join(argv):
                search_calls.append(list(argv))
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=issue_response, stderr="")

        orch_body = "Body\n\n<!-- agdt-orch-key:" + "b" * 64 + " -->"
        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        # First call: orchestration-key search returns no match → POST creates issue
        result1 = provider.create_issue("Title", orch_body, "task", dry_run=False)
        assert result1.status == "created"
        first_search_count = len(search_calls)
        # Second call: instance cache hit — no new search or create
        result2 = provider.create_issue("Title", orch_body, "task", dry_run=False)
        assert result2.identifier == result1.identifier
        assert len(search_calls) == first_search_count  # no additional search call issued

    def test_create_issue_cache_hit_returns_embedded_parent_link_result(self, monkeypatch):
        key = "e" * 64
        cached = ProviderIssueResult(identifier="42", url="u/42", status="existing")
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        provider._idempotency_cache[key] = cached
        monkeypatch.setattr(
            provider,
            "link_subissue",
            lambda parent_id, child_id, *, dry_run=False: ProviderLinkResult(parent_id, child_id, "already-linked"),
        )

        result = provider.create_issue("Title", "Body", "task", parent_id="1", idempotency_key=key)

        assert result.status == "existing"
        assert result.hierarchy_link_result == ProviderLinkResult("1", "42", "already-linked")
