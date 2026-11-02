"""Tests for GitHubProvider."""

from __future__ import annotations

import json
import subprocess

import pytest

from agentic_devtools.adapters.github_provider import GitHubProvider
from agentic_devtools.adapters.retry import TransientError
from tests.unit.adapters.github_provider._fixtures import _make_run_mock


class TestGitHubProviderNormalizeFormatIdentifier:
    """Tests for GitHubProvider.normalize_identifier and format_identifier."""

    def test_normalize_strips_hash_prefix(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        assert provider.normalize_identifier("#42") == "42"
        assert provider.normalize_identifier(" 42 ") == "42"

    def test_normalize_empty_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="non-empty string"):
            provider.normalize_identifier("  ")

    def test_normalize_hash_only_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="after normalization"):
            provider.normalize_identifier("#")

    def test_format_adds_hash_prefix(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        assert provider.format_identifier("42") == "#42"
        assert provider.format_identifier("#42") == "#42"

    def test_format_empty_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="non-empty string"):
            provider.format_identifier("  ")


class TestGitHubProviderHelpers:
    """Tests for internal helper methods."""

    def test_owner_repo_property(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        assert provider.owner_repo == "org/repo"

    @pytest.mark.parametrize(
        ("identifier", "field_name", "expected"),
        [
            (" 42 ", "issue_id", "42"),
            (" ", "issue_id", "non-empty string"),
            ("abc", "issue_id", "numeric GitHub issue number"),
        ],
    )
    def test_normalize_issue_number(self, identifier, field_name, expected):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        if expected.isdigit():
            assert provider._normalize_issue_number(identifier, field_name) == expected
        else:
            with pytest.raises(ValueError, match=expected):
                provider._normalize_issue_number(identifier, field_name)

    def test_normalize_identifier_hash_only_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="after normalization"):
            provider.normalize_identifier("#")

    def test_format_identifier_rejects_empty_value(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="non-empty string"):
            provider.format_identifier(" ")

    def test_format_identifier_preserves_existing_hash(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        assert provider.format_identifier(" #42 ") == "#42"

    def test_format_identifier_adds_hash(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        assert provider.format_identifier("42") == "#42"

    def test_exec_gh_transient_error(self):
        """_exec_gh detects transient HTTP error codes in stderr."""
        provider = GitHubProvider(
            owner_repo="org/repo", run_command=_make_run_mock(stderr="HTTP 429 rate limited", returncode=1)
        )
        with pytest.raises(TransientError, match="429"):
            provider._exec_gh(["gh", "api", "/test"])

    def test_exec_gh_no_false_positive_on_embedded_digit(self):
        """_exec_gh does NOT treat 'error code 1429' as a transient 429."""
        provider = GitHubProvider(
            owner_repo="org/repo", run_command=_make_run_mock(stderr="error code 1429 detail", returncode=1)
        )
        with pytest.raises(RuntimeError, match="gh command failed"):
            provider._exec_gh(["gh", "api", "/test"])

    def test_exec_gh_non_transient_error(self):
        """_exec_gh raises RuntimeError for non-transient failures."""
        provider = GitHubProvider(
            owner_repo="org/repo", run_command=_make_run_mock(stderr="401 unauthorized", returncode=1)
        )
        with pytest.raises(RuntimeError, match="gh command failed"):
            provider._exec_gh(["gh", "api", "/test"])

    def test_parse_json_invalid(self):
        """_parse_json raises RuntimeError on invalid JSON."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(RuntimeError, match="Failed to parse gh output"):
            provider._parse_json("not json {")

    def test_fetch_issue_label_names_non_list_response_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout=json.dumps({"name": "bug"})))
        with pytest.raises(RuntimeError, match="Expected label list response"):
            provider._fetch_issue_label_names("42")

    def test_fetch_issue_label_names_translates_not_found(self):
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stderr="gh: Not Found (HTTP 404)", returncode=1),
        )

        with pytest.raises(ValueError, match="GitHub issue '42' not found"):
            provider._fetch_issue_label_names("42")

    def test_fetch_issue_label_names_propagates_other_runtime_errors(self):
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stderr="HTTP 500 internal error", returncode=1),
        )

        with pytest.raises(RuntimeError, match="gh command failed"):
            provider._fetch_issue_label_names("42")

    def test_fetch_issue_label_names_fetches_all_pages(self):
        first_page = json.dumps([{"name": f"label-{index}"} for index in range(100)])
        responses = [first_page, json.dumps([{"name": "final"}])]
        calls = {"count": 0}

        def mock_run(*args, **kwargs):
            stdout = responses[calls["count"]]
            calls["count"] += 1
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=stdout, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)

        labels = provider._fetch_issue_label_names("42")

        assert calls["count"] == 2
        assert len(labels) == 101
        assert "final" in labels

    def test_fetch_issue_label_names_ignores_invalid_entries(self):
        responses = [
            json.dumps([{"name": "bug"}, {"name": ""}, {"name": None}, {}, "not-a-dict"]),
        ]
        call_idx = {"i": 0}

        def mock_run(*args, **kwargs):
            resp = responses[call_idx["i"]] if call_idx["i"] < len(responses) else "[]"
            call_idx["i"] += 1
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=resp, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        assert provider._fetch_issue_label_names("42") == {"bug"}


class TestGitHubProviderContractGaps:
    """GitHub-specific gap tests complementing the shared contract suite."""

    def test_exec_gh_no_false_positive_on_50200(self):
        """_exec_gh does NOT treat 'HTTP 50200' as a transient 502 (T025)."""
        provider = GitHubProvider(
            owner_repo="org/repo", run_command=_make_run_mock(stderr="HTTP 50200 weird", returncode=1)
        )
        with pytest.raises(RuntimeError, match="gh command failed"):
            provider._exec_gh(["gh", "api", "/test"])

    def test_exec_gh_no_false_positive_on_adjacent_digit_prefix(self):
        """_exec_gh does NOT treat '4290' (adjacent trailing digit) as transient 429 (T025)."""
        provider = GitHubProvider(
            owner_repo="org/repo", run_command=_make_run_mock(stderr="status 4290 detail", returncode=1)
        )
        with pytest.raises(RuntimeError, match="gh command failed"):
            provider._exec_gh(["gh", "api", "/test"])

    def test_exec_gh_no_false_positive_on_standalone_status_code(self):
        """_exec_gh does NOT treat 'processed 429 rows' (no HTTP prefix) as transient (T025)."""
        provider = GitHubProvider(
            owner_repo="org/repo", run_command=_make_run_mock(stderr="processed 429 rows", returncode=1)
        )
        with pytest.raises(RuntimeError, match="gh command failed"):
            provider._exec_gh(["gh", "api", "/test"])

    def test_exec_gh_detects_http_prefixed_transient_case_insensitively(self):
        """_exec_gh treats a lowercase 'http 503' token as a transient error (T025)."""
        provider = GitHubProvider(
            owner_repo="org/repo", run_command=_make_run_mock(stderr="http 503 service unavailable", returncode=1)
        )
        with pytest.raises(TransientError):
            provider._exec_gh(["gh", "api", "/test"])

    def test_exec_gh_detects_bare_transient_status_with_reason_phrase(self):
        """_exec_gh treats bare transient provider stderr as a transient error (T025)."""
        provider = GitHubProvider(
            owner_repo="org/repo", run_command=_make_run_mock(stderr="503 service unavailable", returncode=1)
        )
        with pytest.raises(TransientError):
            provider._exec_gh(["gh", "api", "/test"])
