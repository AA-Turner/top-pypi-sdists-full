"""Offline capability collection tests."""

import json
from dataclasses import replace
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.approver_preflight import (
    EvidenceStatus,
    collect_approver_preflight,
)
from agentic_devtools.cli.ci.github_api_error import GitHubApiError
from agentic_devtools.cli.ci.models import ReviewInfo
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError
from tests.unit.cli.ci.pipeline._snapshot_fixtures import _current_review_provider


def test_identity_visibility_and_role_do_not_prove_review_eligibility() -> None:
    request = Mock(side_effect=[json.dumps({"login": "bot"}), json.dumps({"permissions": {"push": True}})])

    result = collect_approver_preflight(request, "base/repository", "credential")

    assert result.identity.value == "bot"
    assert result.repository_visibility.status is EvidenceStatus.VERIFIED
    assert result.repository_role.value == "write"
    assert result.review_eligibility.status is EvidenceStatus.UNKNOWN
    assert result.blocking_capability == "review_eligibility"
    assert [call.args[0] for call in request.call_args_list] == ["/user", "/repos/base/repository"]
    assert all(call.kwargs["method"] == "GET" for call in request.call_args_list)


def test_underscored_authenticated_approver_is_recognized_on_exact_head() -> None:
    login = "Albert-Marsnik_swica"
    request = Mock(
        side_effect=[
            json.dumps({"login": login}),
            json.dumps({"permissions": {"push": True}}),
        ]
    )
    preflight = collect_approver_preflight(request, "actual/base", "credential")

    assert preflight.identity.status is EvidenceStatus.VERIFIED
    assert preflight.identity.value == login
    assert preflight.repository_visibility.status is EvidenceStatus.VERIFIED
    assert preflight.repository_role.value == "write"

    provider = _current_review_provider([], {})
    provider.get_pr_metadata.return_value = replace(
        provider.get_pr_metadata.return_value,
        base_repo_full_name="actual/base",
    )
    provider.get_approver_preflight = Mock(return_value=preflight)
    provider.list_reviews.return_value = [
        ReviewInfo(id=1, user=login, state="APPROVED", commit_sha="head-sha"),
    ]

    snapshot = build_pr_state_snapshot(provider, 1)

    provider.get_approver_preflight.assert_called_once_with("actual/base")
    assert snapshot.approver_preflight is preflight
    assert snapshot.approver_login == login
    assert snapshot.has_approver_approval_on_head is True


@pytest.mark.parametrize("token", ["", "   "])
def test_missing_token_blocks_identity_without_requests(token: str) -> None:
    request = Mock()
    result = collect_approver_preflight(request, "o/r", token.strip())
    assert result.identity.status is EvidenceStatus.MISSING
    assert result.blocking_capability == "identity"
    request.assert_not_called()


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"login": ""},
        {"login": 3},
        {"login": "raw token\n"},
        {"login": "invalid login"},
        {"login": "invalid;login"},
        [],
    ],
)
def test_unresolvable_identity_cannot_become_a_login_bypass(payload: object) -> None:
    request = Mock(return_value=json.dumps(payload))
    result = collect_approver_preflight(request, "o/r", "credential")
    assert result.blocking_capability == "identity"
    assert result.identity.value is None
    assert request.call_count == 1


@pytest.mark.parametrize(
    "failure",
    [
        GitHubApiError(401),
        GitHubApiError(403),
        GitHubApiError(None),
        RuntimeError("credential raw private response"),
        ValueError("credential"),
    ],
)
def test_identity_denials_and_lookup_failures_are_safe_and_not_retried(failure: Exception) -> None:
    request = Mock(side_effect=failure)
    result = collect_approver_preflight(request, "o/r", "credential")
    assert result.blocking_capability == "identity"
    assert "credential" not in repr(result)
    assert "raw private response" not in repr(result)
    assert request.call_count == 1


def test_repository_404_is_unavailable_not_an_access_only_diagnosis() -> None:
    request = Mock(side_effect=['{"login": "bot"}', GitHubApiError(404)])
    result = collect_approver_preflight(request, "o/r", "credential")
    assert result.blocking_capability == "repository_visibility"
    assert result.repository_visibility.status is EvidenceStatus.UNAVAILABLE
    assert result.repository_visibility.http_status == 404
    assert result.identity.value == "bot"
    assert result.repository_role.status is EvidenceStatus.UNKNOWN
    assert request.call_count == 2


@pytest.mark.parametrize("repository", ["", "o/r/extra", "../repo", "o/r?token=secret", "o/\n", "o/.", "o/.."])
def test_unresolvable_base_repository_never_requests_a_different_target(repository: str) -> None:
    request = Mock(return_value='{"login": "bot"}')
    result = collect_approver_preflight(request, repository, "credential")
    assert result.blocking_capability == "repository_visibility"
    assert request.call_count == 1


@pytest.mark.parametrize(
    "failure",
    [
        RetryableError(
            "limited",
            retry_after=45,
            reset_timestamp=100,
            remaining=0,
            provider="github",
            credential_identity="AGDT_PR_APPROVER_PAT",
            source="retry-after",
            is_rate_limit=True,
        ),
        ProviderRateLimitError(
            retry_after_seconds=45,
            reset_timestamp=100,
            remaining=0,
            provider="github",
            credential_identity="AGDT_PR_APPROVER_PAT",
            source="retry-after",
        ),
    ],
)
def test_rate_limit_metadata_is_preserved_without_retry_loop(failure: Exception) -> None:
    request = Mock(side_effect=failure)
    with pytest.raises(ProviderRateLimitError) as caught:
        collect_approver_preflight(request, "o/r", "credential")
    error = caught.value
    assert (error.retry_after_seconds, error.reset_timestamp, error.remaining) == (45, 100, 0)
    assert (error.provider, error.credential_identity, error.source) == (
        "github",
        "AGDT_PR_APPROVER_PAT",
        "retry-after",
    )
    assert request.call_count == 1


def test_unrelated_transient_failure_remains_retryable() -> None:
    error = RetryableError("server error", is_rate_limit=False)
    with pytest.raises(RetryableError) as caught:
        collect_approver_preflight(Mock(side_effect=error), "o/r", "credential")
    assert caught.value is error
