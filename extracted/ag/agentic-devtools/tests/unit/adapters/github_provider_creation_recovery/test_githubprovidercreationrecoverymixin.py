"""Tests for GitHubProvider."""

from __future__ import annotations

import json
import subprocess

import pytest

from agentic_devtools.adapters.github_provider import GitHubProvider
from agentic_devtools.adapters.issue_provider import (
    PreCreateLookup,
    ProviderIssueResult,
)
from agentic_devtools.adapters.retry import TransientError
from tests.unit.adapters.github_provider._fixtures import _make_run_mock


class TestGitHubProviderCreateIssue:
    """Tests for GitHubProvider.create_issue."""

    def test_recovery_returns_match_found_after_transient_create(self, monkeypatch):
        recovered = ProviderIssueResult(identifier="55", url="u/55", status="existing")
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stderr="HTTP 503 Service unavailable", returncode=1),
        )
        monkeypatch.setattr(provider, "_find_by_orchestration_key", lambda _key: recovered)

        result, recovery_result = provider._create_issue_with_recovery(["gh"], {}, "key")

        assert result is None
        assert recovery_result is recovered

    def test_recovery_propagates_transient_create_without_lookup_key(self):
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stderr="HTTP 503 Service unavailable", returncode=1),
        )

        with pytest.raises(TransientError):
            provider._create_issue_with_recovery(["gh"], {}, "")

    def test_recovery_raises_runtime_error_for_non_transient_failure(self):
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stderr="HTTP 401 unauthorized", returncode=1),
        )

        with pytest.raises(RuntimeError, match="Failed to create issue"):
            provider._create_issue_with_recovery(["gh"], {}, "key")

    def test_create_issue_without_idempotency_key_skips_lookup_retry(self):
        response = json.dumps({"number": 7, "html_url": "https://github.com/org/repo/issues/7"})
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout=response))

        result = provider.create_issue("Title", "Body", "task")

        assert result.identifier == "7"
        assert result.status == "created"

    def test_create_issue_recovers_committed_create_after_transient_response(self):
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
            (0, json.dumps({"items": []}), ""),
            (0, search_response, ""),
        ]
        calls = []

        def mock_run(*args, **kwargs):
            calls.append(args[0])
            returncode, stdout, stderr = responses[len(calls) - 1]
            return subprocess.CompletedProcess(args=args[0], returncode=returncode, stdout=stdout, stderr=stderr)

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)

        result = provider.create_issue(
            "Title",
            "Body",
            "task",
            idempotency_key=key,
            precreate_lookup=PreCreateLookup(orchestration_key=key, issue=None),
        )

        assert result.status == "existing"
        assert result.identifier == "55"
        assert len(calls) == 3
        assert calls[0][calls[0].index("--method") + 1] == "POST"
        assert calls[1][calls[1].index("--method") + 1] == "GET"
        assert calls[2][calls[2].index("--method") + 1] == "GET"

    @pytest.mark.parametrize(
        ("lookup_error", "expected_create_attempts"),
        [
            (None, 1),
            (RuntimeError("search unavailable"), 1),
            (TransientError("search unavailable", status_code=503), 1),
        ],
    )
    def test_create_issue_stops_after_unresolved_transient_create(
        self, monkeypatch, lookup_error, expected_create_attempts
    ):
        monkeypatch.setattr("agentic_devtools.adapters.retry.time.sleep", lambda *_args, **_kwargs: None)
        key = "a" * 64
        create_calls = {"count": 0}

        def run(*args, **kwargs):
            create_calls["count"] += 1
            return _make_run_mock(stderr="HTTP 503 Service unavailable", returncode=1)(*args, **kwargs)

        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=run,
        )
        if lookup_error is None:

            def lookup(_key):
                return None
        else:

            def lookup(_key):
                raise lookup_error

        monkeypatch.setattr(provider, "_find_by_orchestration_key", lookup)

        with pytest.raises(RuntimeError, match="outcome is uncertain"):
            provider.create_issue(
                "Title",
                "Body",
                "task",
                idempotency_key=key,
                precreate_lookup=PreCreateLookup(orchestration_key=key, issue=None),
            )
        assert create_calls["count"] == expected_create_attempts

    def test_create_issue_retries_when_recovery_lookup_is_transient(self, monkeypatch):
        monkeypatch.setattr("agentic_devtools.adapters.retry.time.sleep", lambda *_args, **_kwargs: None)
        key = "a" * 64
        create_calls = []
        recovered = ProviderIssueResult(identifier="55", url="u/55", status="existing")
        lookups = iter([TransientError("search unavailable", status_code=503), recovered])

        def mock_run(*args, **kwargs):
            create_calls.append(args[0])
            return subprocess.CompletedProcess(
                args=args[0], returncode=1, stdout="", stderr="HTTP 503 Service unavailable"
            )

        def lookup(_key):
            result = next(lookups)
            if isinstance(result, TransientError):
                raise result
            return result

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        monkeypatch.setattr(provider, "_find_by_orchestration_key", lookup)

        result = provider.create_issue(
            "Title",
            "Body",
            "task",
            idempotency_key=key,
            precreate_lookup=PreCreateLookup(orchestration_key=key, issue=None),
        )

        assert result.status == "existing"
        assert len(create_calls) == 1

    def test_create_issue_rechecks_after_transient_recovery_lookup(self, monkeypatch):
        monkeypatch.setattr("agentic_devtools.adapters.retry.time.sleep", lambda *_args, **_kwargs: None)
        key = "a" * 64
        create_calls = []
        recovered = ProviderIssueResult(identifier="55", url="u/55", status="existing")
        lookups = iter([None, TransientError("search unavailable", status_code=503), recovered])

        def mock_run(*args, **kwargs):
            create_calls.append(args[0])
            return subprocess.CompletedProcess(
                args=args[0], returncode=1, stdout="", stderr="HTTP 503 Service unavailable"
            )

        def lookup(_key):
            result = next(lookups)
            if isinstance(result, TransientError):
                raise result
            return result

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        monkeypatch.setattr(provider, "_find_by_orchestration_key", lookup)

        result = provider.create_issue(
            "Title",
            "Body",
            "task",
            idempotency_key=key,
            precreate_lookup=PreCreateLookup(orchestration_key=key, issue=None),
        )

        assert result.status == "existing"
        assert len(create_calls) == 1

    def test_create_issue_stops_when_retry_lookup_fails(self, monkeypatch):
        monkeypatch.setattr("agentic_devtools.adapters.retry.time.sleep", lambda *_args, **_kwargs: None)
        key = "a" * 64
        create_calls = []
        lookups = iter([None, RuntimeError("search unavailable")])

        def mock_run(*args, **kwargs):
            create_calls.append(args[0])
            return subprocess.CompletedProcess(
                args=args[0], returncode=1, stdout="", stderr="HTTP 503 Service unavailable"
            )

        def lookup(_key):
            result = next(lookups)
            if isinstance(result, Exception):
                raise result
            return result

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        monkeypatch.setattr(provider, "_find_by_orchestration_key", lookup)

        with pytest.raises(RuntimeError, match="outcome is uncertain"):
            provider.create_issue(
                "Title",
                "Body",
                "task",
                idempotency_key=key,
                precreate_lookup=PreCreateLookup(orchestration_key=key, issue=None),
            )

        assert len(create_calls) == 1
