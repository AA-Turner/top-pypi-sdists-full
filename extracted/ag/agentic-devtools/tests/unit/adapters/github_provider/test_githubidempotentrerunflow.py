"""Tests for GitHubProvider idempotent re-run flow."""

from __future__ import annotations

import json
import subprocess

import pytest

from agentic_devtools.adapters.exceptions import HierarchyLinkError
from agentic_devtools.adapters.github_provider import GitHubProvider
from agentic_devtools.adapters.orchestration_key import embed_orchestration_key, generate_orchestration_key


class TestGitHubIdempotentRerunFlow:
    """Verify idempotent re-run creates 0 duplicates for GitHub provider."""

    def test_github_rerun_finds_existing(self):
        """Second run finds all issues via orchestration key search."""
        orch_key = generate_orchestration_key("create_issue", "epic.features[0]")

        def mock_run(*args, **kwargs):
            cmd = args[0] if args else []
            # Search calls return existing issue
            if "/search/issues" in str(cmd):
                data = {"items": [{"number": 42, "html_url": "https://github.com/org/repo/issues/42", "id": 9999}]}
                return subprocess.CompletedProcess(args=cmd, returncode=0, stdout=json.dumps(data), stderr="")
            return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="{}", stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        body = embed_orchestration_key("Issue body", orch_key)

        # "Re-run" — should find existing
        result = provider.create_issue("Title", body, "task", dry_run=False)
        assert result.status == "existing"
        assert result.identifier == "42"

    def test_github_partial_failure_recovery(self):
        """3 of 5 exist, re-run creates only 2 missing."""
        keys = [generate_orchestration_key("create_issue", f"epic.features[{i}]") for i in range(5)]
        existing_keys = set(keys[:3])  # First 3 already exist
        create_counter = {"n": 0}

        def mock_run(*args, **kwargs):
            cmd = args[0] if args else []
            _ = kwargs.get("input", "")
            # Search calls
            if "/search/issues" in str(cmd):
                # Check if the query contains an existing key
                for ek in existing_keys:
                    if ek in str(cmd) or ek in str(kwargs):
                        data = {"items": [{"number": 99, "html_url": "http://x/99", "id": 9900}]}
                        return subprocess.CompletedProcess(args=cmd, returncode=0, stdout=json.dumps(data), stderr="")
                return subprocess.CompletedProcess(args=cmd, returncode=0, stdout='{"items": []}', stderr="")
            # Create calls
            if "POST" in str(cmd) and "/issues" in str(cmd) and "sub_issues" not in str(cmd):
                create_counter["n"] += 1
                n = create_counter["n"]
                data = {
                    "number": 100 + n,
                    "html_url": f"http://x/{100 + n}",
                    "id": 5000 + n,
                }
                return subprocess.CompletedProcess(args=cmd, returncode=0, stdout=json.dumps(data), stderr="")
            return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="{}", stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)

        results = []
        for i, key in enumerate(keys):
            body = embed_orchestration_key(f"Body {i}", key)
            result = provider.create_issue(f"Issue {i}", body, "task", dry_run=False)
            results.append(result)

        existing_count = sum(1 for r in results if r.status == "existing")
        created_count = sum(1 for r in results if r.status == "created")
        assert existing_count == 3
        assert created_count == 2

    def test_find_by_orchestration_key_raises_on_multiple_matches(self):
        """Ambiguous search (>1 result) must raise RuntimeError, not silently pick first."""
        orch_key = generate_orchestration_key("create_issue", "epic.features[0]")

        def mock_run(*args, **kwargs):
            cmd = args[0] if args else []
            if "/search/issues" in str(cmd):
                data = {
                    "items": [
                        {"number": 10, "html_url": "http://x/10", "id": 1000, "node_id": "A"},
                        {"number": 11, "html_url": "http://x/11", "id": 1001, "node_id": "B"},
                    ]
                }
                return subprocess.CompletedProcess(args=cmd, returncode=0, stdout=json.dumps(data), stderr="")
            return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="{}", stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        body = embed_orchestration_key("Issue body", orch_key)
        with pytest.raises(RuntimeError, match="Ambiguous idempotency-key search"):
            provider.create_issue("Title", body, "task", dry_run=False)

    def test_idempotency_cache_not_populated_on_link_failure(self):
        """Idempotency cache must not be set when parent linking fails."""
        orch_key = generate_orchestration_key("create_issue", "epic.features[0]")
        issue_response = json.dumps({"number": 7, "html_url": "u", "id": 70, "node_id": "I_x"})
        resolve_response = json.dumps({"id": 70, "node_id": "I_x", "html_url": "u"})

        def mock_run(*args, **kwargs):
            argv = list(args[0])
            # Simulate search returning no existing issue
            if "/search/issues" in str(argv):
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout='{"items": []}', stderr="")
            # Fail sub-issue POST
            if (
                "--method" in argv
                and argv[argv.index("--method") + 1] == "POST"
                and any(a.endswith("/sub_issues") for a in argv)
            ):
                return subprocess.CompletedProcess(args=argv, returncode=1, stdout="", stderr="link API error")
            # Sub-issues GET — empty list
            if any(a.endswith("/sub_issues") for a in argv):
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="[]", stderr="")
            # Issue create POST succeeds
            if "--method" in argv and argv[argv.index("--method") + 1] == "POST":
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout=issue_response, stderr="")
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        body = embed_orchestration_key("Issue body", orch_key)

        # First call: create succeeds but linking fails
        with pytest.raises(HierarchyLinkError, match="sub-issue linking.*failed"):
            provider.create_issue("Title", body, "task", parent_id="1", dry_run=False)

        # Cache must be empty — the key must NOT be in the idempotency cache
        assert orch_key not in provider._idempotency_cache
