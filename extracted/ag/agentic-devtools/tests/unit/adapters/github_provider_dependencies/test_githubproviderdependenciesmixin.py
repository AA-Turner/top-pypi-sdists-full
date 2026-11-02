"""Tests for GitHubProvider."""

from __future__ import annotations

import json
import subprocess

import pytest

from agentic_devtools.adapters.github_provider import GitHubProvider
from agentic_devtools.adapters.retry import TransientError
from tests.unit.adapters.github_provider._fixtures import _make_run_mock


class TestGitHubProviderAddBlockedBy:
    """Tests for GitHubProvider.add_blocked_by."""

    def test_add_blocked_by_success(self):
        """add_blocked_by POSTs to the REST dependencies endpoint and returns linked."""
        resolve_response = json.dumps(
            {"id": 2000, "node_id": "I_kwDOblocker", "html_url": "https://github.com/org/repo/issues/2"}
        )
        post_response = json.dumps({})

        def mock_run(*args, **kwargs):
            argv = args[0]
            if "--method" in argv and "POST" in argv:
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout=post_response, stderr="")
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.add_blocked_by("1", "2", dry_run=False)
        assert result.status == "linked"
        assert result.source_id == "2"
        assert result.target_id == "1"

    def test_add_blocked_by_resolves_numeric_identifiers_to_db_ids(self):
        """add_blocked_by resolves blocked_by_id to its integer database ID before POSTing."""
        calls: list[tuple[list[str], str | None]] = []
        responses = {
            "/repos/org/repo/issues/1": json.dumps(
                {"id": 1001, "node_id": "I_kwDOblocker", "html_url": "https://github.com/org/repo/issues/1"}
            ),
        }
        post_response = json.dumps({})

        def mock_run(*args, **kwargs):
            argv = args[0]
            calls.append((argv, kwargs.get("input")))
            if "--method" in argv and "POST" in argv:
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout=post_response, stderr="")
            endpoint = argv[-1]
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=responses[endpoint], stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.add_blocked_by("2", "1", dry_run=False)
        assert result.status == "linked"

        # Last call is the POST; its input body must carry the integer database ID.
        post_call = next(c for c in calls if "--method" in c[0] and "POST" in c[0])
        assert post_call[1] is not None
        body = json.loads(post_call[1])
        assert body == {"issue_id": 1001}

        # The POST endpoint must be the REST dependencies path for the issue number.
        post_path = next(a for a in post_call[0] if a.startswith("/repos/"))
        assert post_path == "/repos/org/repo/issues/2/dependencies/blocked_by"

        # Result preserves the original method arguments.
        assert result.source_id == "1"
        assert result.target_id == "2"

    def test_add_blocked_by_raises_when_blocker_has_no_database_id(self):
        """add_blocked_by raises RuntimeError when blocked_by_id resolves without a database ID."""
        responses = {
            "/repos/org/repo/issues/1": json.dumps({"id": 0, "html_url": "https://github.com/org/repo/issues/1"}),
        }

        def mock_run(*args, **kwargs):
            argv = args[0]
            endpoint = argv[-1]
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=responses[endpoint], stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(RuntimeError, match="integer database ID"):
            provider.add_blocked_by("2", "1", dry_run=False)

    def test_add_blocked_by_rejects_non_numeric_issue_id(self):
        """add_blocked_by raises ValueError for a non-numeric issue_id (first arg)."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout="{}"))
        with pytest.raises(ValueError, match="issue_id must be a numeric GitHub issue number"):
            provider.add_blocked_by("not-a-number", "2", dry_run=False)

    def test_add_blocked_by_rejects_non_numeric_blocked_by_id(self):
        """add_blocked_by raises ValueError for a non-numeric blocked_by_id (second arg)."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout="{}"))
        with pytest.raises(ValueError, match="blocked_by_id must be a numeric GitHub issue number"):
            provider.add_blocked_by("2", "not-a-number", dry_run=False)

    def test_add_blocked_by_rejects_path_fragment_issue_id(self):
        """add_blocked_by rejects path-traversal-style identifiers before any provider call."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout="{}"))
        with pytest.raises(ValueError, match="issue_id must be a numeric GitHub issue number"):
            provider.add_blocked_by("1/comments", "2", dry_run=False)

    def test_add_blocked_by_dry_run_rejects_path_fragment_issue_id(self):
        """add_blocked_by dry-run rejects path-traversal-style identifiers."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout="{}"))
        with pytest.raises(ValueError, match="issue_id must be a numeric GitHub issue number"):
            provider.add_blocked_by("1/comments", "2", dry_run=True)

    def test_add_blocked_by_dry_run_rejects_path_fragment_blocked_by_id(self):
        """add_blocked_by dry-run rejects path-traversal-style blocked_by_id."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout="{}"))
        with pytest.raises(ValueError, match="blocked_by_id must be a numeric GitHub issue number"):
            provider.add_blocked_by("1", "2/labels", dry_run=True)

    def test_add_blocked_by_rejects_empty_identifier(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout="{}"))
        with pytest.raises(ValueError, match="must be non-empty"):
            provider.add_blocked_by("", "2", dry_run=False)

    def test_add_blocked_by_rejects_empty_blocker_identifier(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout="{}"))
        with pytest.raises(ValueError, match="blocked_by_id must be non-empty"):
            provider.add_blocked_by("1", "   ", dry_run=False)

    def test_add_blocked_by_dry_run_rejects_empty_identifier(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout="{}"))
        with pytest.raises(ValueError, match="must be non-empty"):
            provider.add_blocked_by("  ", "2", dry_run=True)

    def test_add_blocked_by_rejects_self_blocking(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout="{}"))
        with pytest.raises(ValueError, match="an issue cannot block itself"):
            provider.add_blocked_by("1", "1", dry_run=False)

    def test_add_blocked_by_dry_run_rejects_self_blocking(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout="{}"))
        with pytest.raises(ValueError, match="an issue cannot block itself"):
            provider.add_blocked_by("1", "1", dry_run=True)

    def test_add_blocked_by_dry_run(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        result = provider.add_blocked_by("2", "1", dry_run=True)
        assert result.status == "dry-run"

    def test_add_blocked_by_dry_run_operation_name_uses_rest_path(self):
        """add_blocked_by dry-run operation string names the REST endpoint."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        provider.add_blocked_by("2", "1", dry_run=True)
        dep = provider._dry_run_deps[-1]
        assert "dependencies/blocked_by" in dep["operation"]
        assert "/graphql" not in dep["operation"]

    def test_add_blocked_by_error(self):
        """add_blocked_by raises RuntimeError for non-idempotent failures."""
        resolve_response = json.dumps({"id": 999, "node_id": "I_x", "html_url": "u"})

        def mock_run(*args, **kwargs):
            argv = args[0]
            if "--method" in argv and "POST" in argv:
                return subprocess.CompletedProcess(args=argv, returncode=1, stdout="", stderr="server error")
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(RuntimeError, match="Failed to add blocked_by"):
            provider.add_blocked_by("1", "2", dry_run=False)

    def test_add_blocked_by_transient_error(self):
        """add_blocked_by raises TransientError on 429."""
        resolve_response = json.dumps({"id": 999, "node_id": "I_x", "html_url": "u"})

        def mock_run(*args, **kwargs):
            argv = args[0]
            if "--method" in argv and "POST" in argv:
                return subprocess.CompletedProcess(
                    args=argv, returncode=1, stdout="", stderr="HTTP 429 too many requests"
                )
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(TransientError):
            provider.add_blocked_by("1", "2", dry_run=False)

    def test_add_blocked_by_idempotent_already_exists(self):
        """add_blocked_by returns already-linked when REST API signals the dependency already exists."""
        resolve_response = json.dumps({"id": 999, "node_id": "I_x", "html_url": "u"})

        def mock_run(*args, **kwargs):
            argv = args[0]
            if "--method" in argv and "POST" in argv:
                msg = json.dumps({"message": "Dependency already exists"})
                return subprocess.CompletedProcess(args=argv, returncode=1, stdout=msg, stderr=msg)
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.add_blocked_by("1", "2", dry_run=False)
        assert result.status == "already-linked"

    def test_add_blocked_by_uses_shell_false(self):
        """add_blocked_by passes shell=False to the run callable."""
        resolve_response = json.dumps({"id": 999, "node_id": "I_x", "html_url": "u"})
        captured_kwargs: list[dict] = []

        def mock_run(*args, **kwargs):
            captured_kwargs.append(kwargs)
            argv = args[0]
            if "--method" in argv and "POST" in argv:
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="{}", stderr="")
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        provider.add_blocked_by("1", "2", dry_run=False)
        assert all(kw.get("shell") is False for kw in captured_kwargs)

    def test_add_blocked_by_404_raises_value_error(self):
        """add_blocked_by raises ValueError when GitHub returns HTTP 404."""
        resolve_response = json.dumps({"id": 999, "node_id": "I_x", "html_url": "u"})

        def mock_run(*args, **kwargs):
            argv = args[0]
            if "--method" in argv and "POST" in argv:
                return subprocess.CompletedProcess(args=argv, returncode=1, stdout="", stderr="HTTP 404 Not Found")
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(ValueError, match="HTTP 404/422"):
            provider.add_blocked_by("1", "2", dry_run=False)

    def test_add_blocked_by_422_raises_value_error(self):
        """add_blocked_by raises ValueError when GitHub returns HTTP 422."""
        resolve_response = json.dumps({"id": 999, "node_id": "I_x", "html_url": "u"})

        def mock_run(*args, **kwargs):
            argv = args[0]
            if "--method" in argv and "POST" in argv:
                return subprocess.CompletedProcess(
                    args=argv, returncode=1, stdout="", stderr="HTTP 422 Unprocessable Entity"
                )
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(ValueError, match="HTTP 404/422"):
            provider.add_blocked_by("1", "2", dry_run=False)

    def test_add_blocked_by_blocker_not_found_raises_value_error(self):
        """add_blocked_by raises ValueError when the blocker issue does not exist (404 on resolve)."""

        def mock_run(*args, **kwargs):
            argv = args[0]
            # Simulate 404 during _to_db_id resolve of blocked_by_id
            return subprocess.CompletedProcess(args=argv, returncode=1, stdout="", stderr="gh: Not Found (HTTP 404)")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(ValueError, match="not found"):
            provider.add_blocked_by("1", "2", dry_run=False)


class TestGitHubProviderHelpers:
    """Tests for internal helper methods."""

    def test_to_db_id_strips_whitespace_from_numeric_identifier(self):
        """_to_db_id normalizes a whitespace-padded numeric identifier before resolving."""
        resolve_response = json.dumps(
            {"number": 42, "id": 4200, "node_id": "I_kwDOnorm", "html_url": "https://github.com/org/repo/issues/42"}
        )
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout=resolve_response))
        db_id = provider._to_db_id(" 42 ")
        assert db_id == 4200

    def test_to_db_id_rejects_empty_after_strip(self):
        """_to_db_id raises RuntimeError when identifier is whitespace-only."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(RuntimeError, match="must not be empty"):
            provider._to_db_id("   ")

    def test_to_db_id_rejects_non_numeric_identifier(self):
        """_to_db_id raises RuntimeError for a non-numeric non-empty identifier."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(RuntimeError, match="Expected a numeric GitHub issue number"):
            provider._to_db_id("abc")

    def test_to_db_id_raises_when_database_id_not_castable(self):
        """_to_db_id raises RuntimeError when resolved metadata has a non-integer database_id."""
        resolve_response = json.dumps(
            {"number": 5, "id": None, "node_id": "I_kwDOx", "html_url": "https://github.com/org/repo/issues/5"}
        )
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout=resolve_response))
        with pytest.raises(RuntimeError, match="integer database ID"):
            provider._to_db_id("5")
