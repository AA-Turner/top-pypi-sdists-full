"""Tests for GitHubProvider."""

from __future__ import annotations

import json
import subprocess

import pytest

from agentic_devtools.adapters.exceptions import (
    HierarchyLinkError,
)
from agentic_devtools.adapters.github_provider import GitHubProvider
from agentic_devtools.adapters.issue_provider import (
    PreCreateLookup,
    ProviderIssueResult,
    ProviderLinkResult,
)
from tests.unit.adapters.github_provider._fixtures import _make_run_mock


class TestGitHubProviderCreateIssue:
    """Tests for GitHubProvider.create_issue."""

    def test_link_created_issue_without_parent_preserves_result(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        issue = ProviderIssueResult(identifier="7", url="u/7", status="created")

        result = provider._link_created_issue(issue, None, newly_created=True)

        assert result is issue

    def test_create_issue_returns_recovered_issue_with_parent_link(self, monkeypatch):
        key = "f" * 64
        search_response = json.dumps(
            {
                "items": [
                    {
                        "number": 55,
                        "html_url": "https://github.com/org/repo/issues/55",
                        "id": 550,
                    }
                ]
            }
        )
        responses = [
            (1, "", "HTTP 503 Service unavailable"),
            (0, search_response, ""),
        ]
        calls = []

        def mock_run(*args, **kwargs):
            calls.append(args[0])
            returncode, stdout, stderr = responses[len(calls) - 1]
            return subprocess.CompletedProcess(args=args[0], returncode=returncode, stdout=stdout, stderr=stderr)

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        link_result = ProviderLinkResult("1", "55", "linked")
        monkeypatch.setattr(provider, "link_subissue", lambda *_args, **_kwargs: link_result)

        create_issue = getattr(provider.create_issue, "__wrapped__")
        result = create_issue(
            provider,
            "Title",
            "Body",
            "task",
            parent_id="1",
            idempotency_key=key,
            precreate_lookup=PreCreateLookup(orchestration_key=key, issue=None),
        )

        assert result.status == "existing"
        assert result.identifier == "55"
        assert result.hierarchy_link_result == link_result
        assert provider._idempotency_cache[key].hierarchy_link_result == link_result
        assert len(calls) == 2

    def test_create_issue_recovery_wraps_parent_link_failure(self, monkeypatch):
        key = "f" * 64
        search_response = json.dumps(
            {
                "items": [
                    {
                        "number": 55,
                        "html_url": "https://github.com/org/repo/issues/55",
                        "id": 550,
                    }
                ]
            }
        )
        responses = [
            (1, "", "HTTP 503 Service unavailable"),
            (0, search_response, ""),
        ]
        calls = []

        def mock_run(*args, **kwargs):
            calls.append(args[0])
            returncode, stdout, stderr = responses[len(calls) - 1]
            return subprocess.CompletedProcess(args=args[0], returncode=returncode, stdout=stdout, stderr=stderr)

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)

        def fail_link(*_args, **_kwargs):
            raise RuntimeError("link failed")

        monkeypatch.setattr(provider, "link_subissue", fail_link)
        create_issue = getattr(provider.create_issue, "__wrapped__")

        with pytest.raises(HierarchyLinkError, match="already exists") as exc_info:
            create_issue(
                provider,
                "Title",
                "Body",
                "task",
                parent_id="1",
                idempotency_key=key,
                precreate_lookup=PreCreateLookup(orchestration_key=key, issue=None),
            )

        assert exc_info.value.created_result.identifier == "55"
        assert exc_info.value.stage == "link_subissue"
        assert len(calls) == 2

    def test_create_issue_precreate_match_wraps_parent_link_failure(self, monkeypatch):
        key = "f" * 64
        existing = ProviderIssueResult(identifier="99", url="u/99", status="existing")
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        monkeypatch.setattr(
            provider,
            "link_subissue",
            lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError("link failed")),
        )

        with pytest.raises(HierarchyLinkError) as exc_info:
            provider.create_issue(
                "Title",
                "Body",
                "task",
                parent_id="12",
                idempotency_key=key,
                precreate_lookup=PreCreateLookup(orchestration_key=key, issue=existing),
            )

        assert exc_info.value.created_result is existing
        assert exc_info.value.stage == "link_subissue"
        assert str(exc_info.value.cause) == "link failed"

    def test_create_issue_cache_hit_wraps_parent_link_failure(self, monkeypatch):
        key = "f" * 64
        cached = ProviderIssueResult(identifier="42", url="u/42", status="existing")
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        provider._idempotency_cache[key] = cached

        def fail_link(parent_id, child_id, *, dry_run=False):
            raise RuntimeError("link failed")

        monkeypatch.setattr(provider, "link_subissue", fail_link)

        with pytest.raises(HierarchyLinkError, match="already exists.*sub-issue linking.*failed") as exc_info:
            provider.create_issue("Title", "Body", "task", parent_id="1", idempotency_key=key)

        assert exc_info.value.created_result == cached
        assert exc_info.value.stage == "link_subissue"
        assert isinstance(exc_info.value.cause, RuntimeError)

    def test_create_issue_with_parent_id_links_child_to_parent(self):
        """create_issue calls link_subissue to attach the new issue to its parent."""
        issue_response = json.dumps({"number": 7, "html_url": "u", "id": 70, "node_id": "I_x"})
        resolve_response = json.dumps({"id": 70, "node_id": "I_x", "html_url": "u"})
        calls: list[list[str]] = []

        def mock_run(*args, **kwargs):
            argv = list(args[0])
            calls.append(argv)
            # POST to sub_issues: success
            if (
                "--method" in argv
                and argv[argv.index("--method") + 1] == "POST"
                and any(a.endswith("/sub_issues") for a in argv)
            ):
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="{}", stderr="")
            # GET sub_issues: empty list (idempotency pre-check inside link_subissue)
            if any(a.endswith("/sub_issues") for a in argv):
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="[]", stderr="")
            # POST /issues (create)
            if "--method" in argv and argv[argv.index("--method") + 1] == "POST":
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout=issue_response, stderr="")
            # GET /issues/{n} (resolve child database ID inside link_subissue)
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.create_issue("Title", "Body", "task", parent_id="1", dry_run=False)
        assert result.status == "created"
        assert result.identifier == "7"
        assert result.hierarchy_link_result is not None
        assert result.hierarchy_link_result.source_id == "1"
        assert result.hierarchy_link_result.target_id == "7"
        assert result.hierarchy_link_result.status == "linked"
        sub_posts = [
            c
            for c in calls
            if "--method" in c and c[c.index("--method") + 1] == "POST" and any(a.endswith("/sub_issues") for a in c)
        ]
        assert len(sub_posts) == 1, "Expected exactly one sub_issues POST for parent_id linking"

    def test_create_issue_with_parent_id_partial_failure_raises_runtime_error(self):
        """create_issue raises HierarchyLinkError describing the partial success when linking fails."""
        issue_response = json.dumps({"number": 7, "html_url": "u", "id": 70, "node_id": "I_x"})
        resolve_response = json.dumps({"id": 70, "node_id": "I_x", "html_url": "u"})

        def mock_run(*args, **kwargs):
            argv = list(args[0])
            if (
                "--method" in argv
                and argv[argv.index("--method") + 1] == "POST"
                and any(a.endswith("/sub_issues") for a in argv)
            ):
                return subprocess.CompletedProcess(args=argv, returncode=1, stdout="", stderr="sub-issues API error")
            if any(a.endswith("/sub_issues") for a in argv):
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="[]", stderr="")
            if "--method" in argv and argv[argv.index("--method") + 1] == "POST":
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout=issue_response, stderr="")
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(HierarchyLinkError, match="was created.*sub-issue linking.*failed") as exc_info:
            provider.create_issue("Title", "Body", "task", parent_id="1", dry_run=False)

        # FR-007: the typed error carries the partial created result, stage, and cause.
        err = exc_info.value
        assert err.created_result is not None
        assert err.created_result.identifier == "7"
        assert err.created_result.status == "created"
        assert err.stage == "link_subissue"
        assert err.cause is not None

    def test_create_issue_existing_remote_with_parent_reconciles_link(self):
        """create_issue with existing remote match and parent_id calls link_subissue."""
        search_response = json.dumps({"items": [{"number": 42, "html_url": "https://github.com/org/repo/issues/42"}]})
        resolve_response = json.dumps(
            {"id": 420, "node_id": "I_kwDO42", "html_url": "https://github.com/org/repo/issues/42"}
        )
        sub_posts: list[list[str]] = []

        def mock_run(*args, **kwargs):
            argv = list(args[0])
            if "/search/issues" in " ".join(argv):
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout=search_response, stderr="")
            if (
                "--method" in argv
                and argv[argv.index("--method") + 1] == "POST"
                and any(a.endswith("/sub_issues") for a in argv)
            ):
                sub_posts.append(argv)
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="{}", stderr="")
            if any(a.endswith("/sub_issues") for a in argv):
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="[]", stderr="")
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        orch_body = "Body\n\n<!-- agdt-orch-key:" + "c" * 64 + " -->"
        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.create_issue("Title", orch_body, "task", parent_id="1", dry_run=False)
        assert result.identifier == "42"
        assert result.hierarchy_link_result is not None
        assert result.hierarchy_link_result.source_id == "1"
        assert result.hierarchy_link_result.target_id == "42"
        assert len(sub_posts) == 1, "Expected exactly one sub_issues POST for parent reconciliation"

    def test_create_issue_existing_remote_with_parent_link_failure_raises(self):
        """create_issue preserves the existing issue result when parent linking fails."""
        search_response = json.dumps({"items": [{"number": 42, "html_url": "https://github.com/org/repo/issues/42"}]})
        resolve_response = json.dumps(
            {"id": 420, "node_id": "I_kwDO42", "html_url": "https://github.com/org/repo/issues/42"}
        )

        def mock_run(*args, **kwargs):
            argv = list(args[0])
            if "/search/issues" in " ".join(argv):
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout=search_response, stderr="")
            if (
                "--method" in argv
                and argv[argv.index("--method") + 1] == "POST"
                and any(a.endswith("/sub_issues") for a in argv)
            ):
                return subprocess.CompletedProcess(args=argv, returncode=1, stdout="", stderr="link error")
            if any(a.endswith("/sub_issues") for a in argv):
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="[]", stderr="")
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        orch_body = "Body\n\n<!-- agdt-orch-key:" + "d" * 64 + " -->"
        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(HierarchyLinkError, match="already exists.*sub-issue linking.*failed") as exc_info:
            provider.create_issue("Title", orch_body, "task", parent_id="1", dry_run=False)
        assert exc_info.value.created_result.identifier == "42"
        assert exc_info.value.stage == "link_subissue"
