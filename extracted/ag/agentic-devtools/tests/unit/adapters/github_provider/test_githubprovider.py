"""Tests for GitHubProvider."""

from __future__ import annotations

import inspect
import subprocess

import pytest

from agentic_devtools.adapters.github_provider import GitHubProvider
from tests.unit.adapters.conftest import build_github_contract_provider  # noqa: E402
from tests.unit.adapters.github_provider._fixtures import _make_run_mock
from tests.unit.adapters.issue_provider import _contract_scenarios as contract  # noqa: E402


class TestGitHubProviderInit:
    """Tests for GitHubProvider.__init__."""

    @pytest.mark.parametrize("owner_repo", ["", " ", "repo-only", "org/repo/extra", "/repo", "org/"])
    def test_init_rejects_invalid_owner_repo(self, owner_repo):
        with pytest.raises(ValueError, match="owner/repo"):
            GitHubProvider(owner_repo=owner_repo, run_command=_make_run_mock())

    def test_init_normalizes_owner_repo_whitespace(self):
        provider = GitHubProvider(owner_repo=" org/repo ", run_command=_make_run_mock())
        assert provider.owner_repo == "org/repo"


class TestGitHubProviderFacadeContract:
    def test_public_identity_signatures_and_subclassing(self):
        assert GitHubProvider.__module__ == "agentic_devtools.adapters.github_provider"
        init_parameters = inspect.signature(GitHubProvider.__init__).parameters
        assert list(init_parameters) == ["self", "owner_repo", "run_command"]
        assert init_parameters["run_command"].default is None

        create_parameters = inspect.signature(GitHubProvider.create_issue).parameters
        assert list(create_parameters) == [
            "self",
            "title",
            "body",
            "issue_type",
            "parent_id",
            "labels",
            "idempotency_key",
            "precreate_lookup",
            "dry_run",
        ]
        assert create_parameters["parent_id"].default is None
        assert create_parameters["labels"].default is None
        assert create_parameters["idempotency_key"].default is None
        assert create_parameters["precreate_lookup"].default is None
        assert create_parameters["dry_run"].default is False

        class SpecializedGitHubProvider(GitHubProvider):
            pass

        assert issubclass(SpecializedGitHubProvider, GitHubProvider)
        assert isinstance(SpecializedGitHubProvider("org/repo"), GitHubProvider)


class TestGitHubProviderDryRunManifest:
    """Tests for dry-run manifest accumulation."""

    def test_dry_run_accumulates_issues(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        provider.create_issue("Title 1", "Body", "epic", dry_run=True)
        provider.create_issue("Title 2", "Body", "feature", parent_id="1", dry_run=True)
        manifest = provider.get_dry_run_manifest()
        assert len(manifest["issues"]) == 2
        assert manifest["issues"][0]["title"] == "Title 1"
        assert manifest["issues"][1]["parent_id"] == "1"

    def test_dry_run_accumulates_dependencies(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        provider.link_subissue("1", "2", dry_run=True)
        provider.add_blocked_by("3", "4", dry_run=True)
        manifest = provider.get_dry_run_manifest()
        assert len(manifest["dependencies"]) == 2
        assert manifest["dependencies"][0]["type"] == "sub-issue"
        assert manifest["dependencies"][1]["type"] == "blocks"


class TestGitHubProviderContractGaps:
    """GitHub-specific gap tests complementing the shared contract suite."""

    def test_init_accepts_valid_owner_repo(self):
        """__init__ accepts a well-formed owner/repo slug (T023)."""
        provider = GitHubProvider(owner_repo="octocat/hello-world", run_command=_make_run_mock())
        assert provider.owner_repo == "octocat/hello-world"


def _failing_github_provider(stderr: str) -> GitHubProvider:
    """Return a GitHubProvider whose gh calls always fail with *stderr*."""

    def failing_run(args, **kwargs):
        return subprocess.CompletedProcess(args=args, returncode=1, stdout="", stderr=stderr)

    return GitHubProvider(owner_repo="org/repo", run_command=failing_run)


class TestGitHubContract(
    contract.TestContractCreateIssue,
    contract.TestContractCreateIssueDryRun,
    contract.TestContractCreateIssueIdempotent,
    contract.TestContractSetIssueType,
    contract.TestContractSetIssueTypeTransition,
    contract.TestContractSetIssueTypeDryRun,
    contract.TestContractLinkSubissue,
    contract.TestContractLinkSubissueDryRun,
    contract.TestContractIdempotentRelink,
    contract.TestContractAddBlockedBy,
    contract.TestContractAddBlockedByDryRun,
    contract.TestContractIdempotentBlockedBy,
    contract.TestContractApplyLabels,
    contract.TestContractApplyLabelsDryRun,
    contract.TestContractApplyLabelsIdempotent,
    contract.TestContractResolveIdentifier,
    contract.TestContractResolveIdentifierDryRun,
    contract.TestContractNormalizeIdentifier,
    contract.TestContractFormatIdentifier,
    contract.TestContractTransientError,
    contract.TestContractNonTransientApiFailure,
):
    """Runs the shared contract suite directly against the production GitHubProvider."""

    sample_identifier = "#1"
    non_transient_exc_type = RuntimeError

    @pytest.fixture()
    def provider(self):
        provider, backend = build_github_contract_provider()
        self._backend = backend
        return provider

    def boundary_calls(self, provider):
        return self._backend.call_count

    def seed_issue(self, provider):
        return provider.create_issue("Seed", "Seed body", "task").identifier

    def seed_two_issues(self, provider):
        first = provider.create_issue("First", "first body", "task").identifier
        second = provider.create_issue("Second", "second body", "task").identifier
        return first, second

    def make_transient_create_provider(self):
        return _failing_github_provider("HTTP 503 unavailable")

    def make_non_transient_create_provider(self):
        return _failing_github_provider("404 not found")
