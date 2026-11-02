"""Tests for GitHubProvider."""

from __future__ import annotations

import json
import subprocess

import pytest

from agentic_devtools.adapters.github_provider import GitHubProvider
from agentic_devtools.adapters.retry import TransientError
from tests.unit.adapters.github_provider._fixtures import _make_run_mock


class TestGitHubProviderApplyLabels:
    """Tests for GitHubProvider.apply_labels."""

    def test_apply_new_label(self):
        responses = [json.dumps([]), json.dumps([{"name": "epic"}])]
        call_idx = {"i": 0}

        def mock_run(*args, **kwargs):
            resp = responses[call_idx["i"]] if call_idx["i"] < len(responses) else ""
            call_idx["i"] += 1
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=resp, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.apply_labels("42", ["epic"], dry_run=False)
        assert result.status == "updated"
        assert result.identifier == "42"
        assert result.metadata["labels"] == ["epic"]

    def test_apply_new_label_merges_with_existing(self):
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stdout=json.dumps([{"name": "bug"}])),
        )
        result = provider.apply_labels("42", ["epic"], dry_run=False)
        assert result.status == "updated"
        assert result.metadata["labels"] == ["bug", "epic"]

    def test_apply_existing_label_case_insensitive_returns_no_op(self):
        """apply_labels treats 'Bug' and 'bug' as the same label (no-op, no redundant POST)."""
        call_count = {"n": 0}

        def mock_run(*args, **kwargs):
            call_count["n"] += 1
            # Only the GET labels page should be called; POST must not be called.
            return subprocess.CompletedProcess(
                args=args[0], returncode=0, stdout=json.dumps([{"name": "Bug"}]), stderr=""
            )

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.apply_labels("42", ["bug"], dry_run=False)
        assert result.status == "no-op"
        # Only 1 call (GET labels page); POST must not have been issued.
        assert call_count["n"] == 1

    def test_apply_existing_label_returns_no_op(self):
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stdout=json.dumps([{"name": "bug"}])),
        )
        result = provider.apply_labels("42", ["bug"], dry_run=False)
        assert result.status == "no-op"
        assert result.metadata["labels"] == ["bug"]

    def test_apply_labels_fetches_all_pages_for_no_op_detection(self):
        captured_calls: list[list[str]] = []
        first_page = [{"name": f"label-{i}"} for i in range(100)]
        responses = [
            json.dumps(first_page),
            json.dumps([{"name": "epic"}]),
        ]
        call_idx = {"i": 0}

        def mock_run(*args, **kwargs):
            captured_calls.append(list(args[0]))
            resp = responses[call_idx["i"]] if call_idx["i"] < len(responses) else ""
            call_idx["i"] += 1
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=resp, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.apply_labels("42", ["epic"], dry_run=False)

        assert result.status == "no-op"
        assert any("page=1" in arg for arg in captured_calls[0])
        assert any("page=2" in arg for arg in captured_calls[1])

    def test_apply_empty_labels_returns_no_op(self):
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stdout=json.dumps([{"name": "bug"}])),
        )
        result = provider.apply_labels("42", [], dry_run=False)
        assert result.status == "no-op"
        assert result.metadata["labels"] == ["bug"]

    def test_apply_labels_empty_identifier_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="non-empty"):
            provider.apply_labels("  ", ["bug"], dry_run=False)

    def test_apply_labels_rejects_non_numeric_identifier(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="numeric GitHub issue number"):
            provider.apply_labels("42/labels", ["bug"], dry_run=True)

    def test_apply_label_dry_run(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        result = provider.apply_labels("42", ["b-label", "a-label"], dry_run=True)
        assert result.status == "dry-run"
        assert result.metadata["labels"] == ["a-label", "b-label"]
        # Dry-run should record the intended mutation in the manifest
        assert len(provider._dry_run_deps) == 1
        assert provider._dry_run_deps[0]["type"] == "label"
        assert provider._dry_run_deps[0]["status"] == "dry-run"

    def test_apply_label_transient_error(self):
        """apply_labels raises TransientError on 503 during POST."""
        responses = [json.dumps([]), ""]  # GET labels ok, POST fails
        call_idx = {"i": 0}

        def mock_run(*args, **kwargs):
            idx = call_idx["i"]
            call_idx["i"] += 1
            if idx == 0:
                return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=responses[0], stderr="")
            return subprocess.CompletedProcess(
                args=args[0], returncode=1, stdout="", stderr="HTTP 503 service unavailable"
            )

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(TransientError):
            provider.apply_labels("42", ["epic"], dry_run=False)

    def test_apply_label_generic_error(self):
        """apply_labels raises RuntimeError on non-transient failure during POST."""
        responses = [json.dumps([]), ""]  # GET labels ok, POST fails
        call_idx = {"i": 0}

        def mock_run(*args, **kwargs):
            idx = call_idx["i"]
            call_idx["i"] += 1
            if idx == 0:
                return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=responses[0], stderr="")
            return subprocess.CompletedProcess(args=args[0], returncode=1, stdout="", stderr="permission denied")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(RuntimeError, match="Failed to apply labels"):
            provider.apply_labels("42", ["epic"], dry_run=False)

    def test_apply_labels_404_raises_value_error(self):
        """apply_labels raises ValueError when the issue is not found (HTTP 404)."""
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stderr="gh: Not Found (HTTP 404)", returncode=1),
        )
        with pytest.raises(ValueError, match="not found"):
            provider.apply_labels("999", ["bug"], dry_run=False)

    def test_apply_labels_non_404_labels_fetch_error_propagates(self):
        """apply_labels re-raises non-404 RuntimeError from the label-fetch GET."""
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stderr="gh: Server Error (HTTP 500)", returncode=1),
        )
        with pytest.raises(RuntimeError, match="gh command failed"):
            provider.apply_labels("42", ["bug"], dry_run=False)

    def test_apply_labels_normalizes_requested_labels(self):
        """apply_labels trims whitespace and deduplicates case-insensitively."""
        posted: list[list[str]] = []

        def mock_run(*args, **kwargs):
            argv = list(args[0])
            if "--method" in argv and argv[argv.index("--method") + 1] == "POST":
                posted.append(argv)
                return subprocess.CompletedProcess(
                    args=argv, returncode=0, stdout=json.dumps([{"name": "bug"}, {"name": "epic"}]), stderr=""
                )
            # GET labels — issue has no labels yet
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=json.dumps([]), stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        # " epic ", "Epic" → "epic"; "bug", " BUG " → "bug" (4 inputs → 2 unique labels)
        result = provider.apply_labels("42", [" epic ", "Epic", "bug", " BUG "], dry_run=False)
        assert result.status == "updated"
        # Exactly one POST (not one per normalized label)
        assert len(posted) == 1
        # Labels in metadata are sorted and contain only the 2 deduplicated normalized labels
        assert result.metadata["labels"] == ["bug", "epic"]

    def test_apply_labels_dry_run_trims_and_deduplicates(self):
        """apply_labels dry-run normalizes labels before returning metadata."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        result = provider.apply_labels("42", [" a-label ", "A-LABEL", "b-label"], dry_run=True)
        assert result.status == "dry-run"
        # "a-label" (trimmed first occurrence) and "b-label" — "A-LABEL" is a duplicate
        assert result.metadata["labels"] == ["a-label", "b-label"]
