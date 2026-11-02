"""Tests for GitHubProvider."""

from __future__ import annotations

import json
import subprocess

import pytest

from agentic_devtools.adapters.github_provider import GitHubProvider
from agentic_devtools.adapters.issue_provider import (
    DefinitiveCreationFailure,
    PreCreateLookup,
    ProviderIssueResult,
)
from agentic_devtools.adapters.retry import TransientError
from tests.unit.adapters.github_provider._fixtures import _make_run_mock


class TestGitHubProviderCreateIssue:
    """Tests for GitHubProvider.create_issue."""

    def test_create_issue_success(self):
        response = json.dumps(
            {
                "number": 42,
                "html_url": "https://github.com/org/repo/issues/42",
                "id": 123456,
                "node_id": "I_kwDO123456",
            }
        )
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout=response))
        result = provider.create_issue("Title", "Body", "task", dry_run=False)
        assert isinstance(result, ProviderIssueResult)
        assert result.identifier == "42"
        assert result.status == "created"
        assert result.metadata["database_id"] == 123456
        assert result.metadata["node_id"] == "I_kwDO123456"

    def test_create_issue_does_not_pass_repo_flag_to_gh_api(self):
        """`gh api` rejects --repo; the repository comes from the endpoint path."""
        response = json.dumps(
            {
                "number": 42,
                "html_url": "https://github.com/org/repo/issues/42",
                "id": 123456,
                "node_id": "I_kwDO123456",
            }
        )
        captured_calls: list[list[str]] = []

        def mock_run(*args, **kwargs):
            captured_calls.append(list(args[0]))
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=response, stderr="")

        GitHubProvider(owner_repo="org/repo", run_command=mock_run).create_issue("Title", "Body", "task", dry_run=False)

        api_calls = [call for call in captured_calls if len(call) >= 2 and call[0] == "gh" and call[1] == "api"]
        assert api_calls
        for call in api_calls:
            assert "--repo" not in call

    def test_create_issue_dry_run(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        result = provider.create_issue("Title", "Body", "task", dry_run=True)
        assert result.status == "dry-run"
        assert result.identifier == ""

    def test_create_issue_error(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stderr="not found", returncode=1))
        with pytest.raises(RuntimeError, match="Failed to create issue"):
            provider.create_issue("Title", "Body", "task", dry_run=False)

    def test_create_issue_transient_error(self):
        """create_issue raises TransientError on 429/502/503 during POST."""
        provider = GitHubProvider(
            owner_repo="org/repo", run_command=_make_run_mock(stderr="HTTP 429 rate limited", returncode=1)
        )
        with pytest.raises(TransientError):
            provider.create_issue("Title", "Body", "task", dry_run=False)

    def test_create_issue_empty_type_raises(self):
        """create_issue rejects empty issue_type values."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(DefinitiveCreationFailure, match="issue_type must be a non-empty string"):
            provider.create_issue("Title", "Body", "", dry_run=False)

    def test_create_issue_unsupported_type_raises(self):
        """create_issue with sub-task type raises IssueTypeMappingError."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(DefinitiveCreationFailure, match="sub-task"):
            provider.create_issue("Title", "Body", "sub-task", dry_run=False)

    def test_create_issue_unknown_type_raises(self):
        """create_issue with unknown type raises IssueTypeMappingError."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(DefinitiveCreationFailure, match="no GitHub label mapping"):
            provider.create_issue("Title", "Body", "story", dry_run=False)

    def test_create_issue_dry_run_unknown_type_raises(self):
        """create_issue dry-run validates unknown type mappings."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(DefinitiveCreationFailure, match="no GitHub label mapping"):
            provider.create_issue("Title", "Body", "story", dry_run=True)

    def test_create_issue_empty_title_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(DefinitiveCreationFailure, match="title must be a non-empty string"):
            provider.create_issue("  ", "Body", "task", dry_run=False)

    def test_create_issue_empty_parent_id_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(DefinitiveCreationFailure, match="parent_id must be a non-empty string"):
            provider.create_issue("Title", "Body", "task", parent_id="  ", dry_run=False)

    def test_create_issue_malformed_parent_id_raises_before_create(self):
        """A non-numeric parent_id fails fast without creating an orphaned issue."""
        calls: list[list[str]] = []

        def mock_run(*args, **kwargs):
            calls.append(list(args[0]))
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout="{}", stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(DefinitiveCreationFailure, match="parent_id must be a numeric GitHub issue number"):
            provider.create_issue("Title", "Body", "task", parent_id="1/comments", dry_run=False)
        assert calls == [], "No provider call should be issued when parent_id is invalid"

    def test_create_issue_includes_caller_labels(self):
        response = json.dumps({"number": 12, "html_url": "u", "id": 120, "node_id": "I_x"})
        captured: dict[str, object] = {}

        def mock_run(*args, **kwargs):
            captured["input"] = kwargs.get("input")
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.create_issue("Title", "Body", "task", labels=["extra", "task", ""], dry_run=False)
        assert result.status == "created"
        payload = json.loads(captured["input"])
        assert payload["labels"] == ["task", "extra"]

    def test_create_issue_normalizes_caller_labels_case_insensitively(self):
        """create_issue trims and deduplicates caller-provided labels case-insensitively."""
        response = json.dumps({"number": 12, "html_url": "u", "id": 120, "node_id": "I_x"})
        captured: dict[str, object] = {}

        def mock_run(*args, **kwargs):
            captured["input"] = kwargs.get("input")
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        # " TASK " duplicates the derived "task" label; " extra " should be trimmed;
        # "EXTRA" duplicates the trimmed "extra" (case-insensitive).
        result = provider.create_issue("Title", "Body", "task", labels=[" TASK ", " extra ", "EXTRA"], dry_run=False)
        assert result.status == "created"
        payload = json.loads(captured["input"])
        assert payload["labels"] == ["task", "extra"]

    def test_create_issue_embeds_key_and_caches_success(self, monkeypatch):
        key = "a" * 64
        captured: dict[str, str] = {}
        response = json.dumps({"number": 12, "html_url": "u", "id": 120, "node_id": "I_x"})
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout=response))
        monkeypatch.setattr(provider, "_lookup_existing_for_creation", lambda *_args: None)

        def create_with_recovery(_args, payload, lookup_key):
            captured["body"] = payload["body"]
            captured["lookup_key"] = lookup_key
            return (
                subprocess.CompletedProcess(args=["gh"], returncode=0, stdout=response, stderr=""),
                None,
            )

        monkeypatch.setattr(provider, "_create_issue_with_recovery", create_with_recovery)

        result = provider.create_issue("Title", "Body", "task", idempotency_key=key)

        assert result.status == "created"
        assert f"<!-- agdt-orch-key:{key} -->" in captured["body"]
        assert captured["lookup_key"] == key
        assert provider._idempotency_cache[key].identifier == result.identifier

    def test_create_issue_returns_precreate_match(self, monkeypatch):
        key = "b" * 64
        existing = ProviderIssueResult(identifier="44", url="u/44", status="existing")
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        monkeypatch.setattr(provider, "_lookup_existing_for_creation", lambda *_args: existing)

        result = provider.create_issue("Title", "Body", "task", idempotency_key=key)

        assert result is existing

    def test_create_issue_returns_recovered_match_and_caches_it(self, monkeypatch):
        key = "c" * 64
        recovered = ProviderIssueResult(identifier="45", url="u/45", status="existing")
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        monkeypatch.setattr(provider, "_lookup_existing_for_creation", lambda *_args: None)
        monkeypatch.setattr(provider, "_create_issue_with_recovery", lambda *_args: (None, recovered))

        result = provider.create_issue("Title", "Body", "task", idempotency_key=key)

        assert result.identifier == recovered.identifier
        assert result.status == "existing"
        assert provider._idempotency_cache[key] is result

    def test_create_issue_with_precreate_lookup_delegates(self, monkeypatch):
        result = ProviderIssueResult(identifier="46", url="u/46", status="existing")
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        monkeypatch.setattr(provider, "create_issue", lambda *_args, **_kwargs: result)

        assert (
            provider.create_issue_with_precreate_lookup(
                "Title",
                "Body",
                "task",
                precreate_lookup=PreCreateLookup(orchestration_key="d" * 64, issue=None),
            )
            is result
        )


class TestGitHubProviderContractGaps:
    """GitHub-specific gap tests complementing the shared contract suite."""

    def test_create_issue_happy_path_captures_correct_cli_args_and_stdin_payload(self):
        """create_issue issues the expected gh api POST with a JSON stdin payload (T012)."""
        captured: dict[str, object] = {}

        def capturing_run(args, **kwargs):
            captured["args"] = list(args)
            captured["input"] = kwargs.get("input")
            captured["shell"] = kwargs.get("shell")
            return subprocess.CompletedProcess(
                args=args,
                returncode=0,
                stdout=json.dumps(
                    {"number": 7, "html_url": "https://github.com/org/repo/issues/7", "id": 700, "node_id": "I_kwDO700"}
                ),
                stderr="",
            )

        provider = GitHubProvider(owner_repo="org/repo", run_command=capturing_run)
        result = provider.create_issue("My Title", "My Body", "task", dry_run=False)

        assert result.status == "created"
        args = captured["args"]
        assert "gh" in args and "api" in args
        assert "/repos/org/repo/issues" in args
        assert args[args.index("--method") + 1] == "POST"
        assert captured["shell"] is False
        payload = json.loads(captured["input"])
        assert payload["title"] == "My Title"
        assert payload["body"] == "My Body"
        assert payload["labels"] == ["task"]

    def test_create_issue_malformed_response_not_dict_raises_value_error(self):
        """create_issue raises ValueError when API returns a non-dict (e.g. a list)."""

        def list_run(args, **kwargs):
            return subprocess.CompletedProcess(args=args, returncode=0, stdout=json.dumps([{"number": 1}]), stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=list_run)
        with pytest.raises(ValueError, match="Unexpected response type from GitHub API"):
            provider.create_issue("T", "B", "task", dry_run=False)

    def test_create_issue_missing_number_raises_value_error(self):
        """create_issue raises ValueError when API returns a dict without a valid issue number."""

        def empty_run(args, **kwargs):
            return subprocess.CompletedProcess(args=args, returncode=0, stdout=json.dumps({}), stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=empty_run)
        with pytest.raises(ValueError, match="did not include a valid issue number"):
            provider.create_issue("T", "B", "task", dry_run=False)

    def test_create_issue_retry_exhaustion_raises_transient_error(self, monkeypatch):
        """create_issue retries transient failures and eventually raises (T013).

        With DEFAULT_MAX_RETRIES=3, the run_command is invoked 4 times total
        (1 initial + 3 retries) before the TransientError propagates.
        """
        from agentic_devtools.adapters.retry import DEFAULT_MAX_RETRIES

        monkeypatch.setattr("agentic_devtools.adapters.retry.time.sleep", lambda *a, **k: None)
        call_count = {"n": 0}

        def failing_run(args, **kwargs):
            call_count["n"] += 1
            return subprocess.CompletedProcess(args=args, returncode=1, stdout="", stderr="HTTP 503 unavailable")

        provider = GitHubProvider(owner_repo="org/repo", run_command=failing_run)
        with pytest.raises(TransientError):
            provider.create_issue("Title", "Body", "task", dry_run=False)
        assert call_count["n"] == DEFAULT_MAX_RETRIES + 1 == 4
