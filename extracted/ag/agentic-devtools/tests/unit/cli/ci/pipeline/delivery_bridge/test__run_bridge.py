"""Offline delivery bridge behavior and authority delegation."""

from unittest.mock import Mock, patch

import pytest

from agentic_devtools.cli.ci.models import PRMetadata
from agentic_devtools.cli.ci.pipeline.delivery import InitialDeliveryOutcome
from agentic_devtools.cli.ci.pipeline.delivery_bridge import _run_bridge
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

MODULE = "agentic_devtools.cli.ci.pipeline.delivery_bridge"
SHA = "ab" * 20


@pytest.mark.parametrize(
    ("observed", "outcome", "delivered"),
    [
        (SHA, InitialDeliveryOutcome.DELIVERED, True),
        (SHA.upper(), InitialDeliveryOutcome.DELIVERED, True),
        ("cd" * 20, InitialDeliveryOutcome.DELIVERED, False),
        ("", InitialDeliveryOutcome.DELIVERED, False),
        (SHA, InitialDeliveryOutcome.NO_DELIVERY, False),
        (SHA, InitialDeliveryOutcome.UNKNOWN, False),
    ],
)
def test_delegates_once_and_binds_result_to_requested_head(
    observed: str, outcome: InitialDeliveryOutcome, delivered: bool
) -> None:
    with (
        patch(f"{MODULE}.GitHubActionsProvider") as provider,
        patch(f"{MODULE}.classify_initial_delivery_with_head", return_value=(observed, outcome)) as classify,
    ):
        result = _run_bridge("owner/repo", 42, SHA.upper())

    provider.assert_called_once_with(repo="owner/repo", token=None)
    classify.assert_called_once_with(provider.return_value, 42, completion_confirmed=True, initial_plan_sha=None)
    assert result == {
        "repository": "owner/repo",
        "prNumber": 42,
        "headSha": SHA,
        "outcome": "DELIVERED" if delivered else "UNKNOWN",
        "complete": delivered,
        "diffEvidence": "NON_ZERO_DIFF" if delivered else "UNKNOWN",
    }


def test_normalizes_mixed_case_requested_head() -> None:
    with (
        patch(f"{MODULE}.GitHubActionsProvider"),
        patch(f"{MODULE}.classify_initial_delivery_with_head", return_value=(SHA, InitialDeliveryOutcome.DELIVERED)),
    ):
        result = _run_bridge("owner/repo", 42, "aB" * 20)

    assert result["headSha"] == SHA
    assert result["complete"] is True


@pytest.mark.parametrize("failure_step", ["provider", "classification"])
def test_bridge_does_not_swallow_exceptions(failure_step: str) -> None:
    error = RuntimeError("unavailable")
    with (
        patch(f"{MODULE}.GitHubActionsProvider") as provider,
        patch(f"{MODULE}.classify_initial_delivery_with_head") as classify,
    ):
        failing = provider if failure_step == "provider" else classify
        failing.side_effect = error

        with pytest.raises(RuntimeError) as exc:
            _run_bridge("owner/repo", 42, SHA)

    assert exc.value is error


@pytest.mark.parametrize(
    ("files", "count", "heads", "delivered"),
    [
        (["src/main.py"], 1, [SHA, SHA], True),
        (["src/main.py"], 1, [SHA.upper(), SHA.upper()], True),
        ([], 0, [SHA, SHA], False),
        ([], 1, [SHA, SHA], False),
        (["src/main.py"], 2, [SHA, SHA], False),
        (["src/main.py"], 1, [SHA, "cd" * 20], False),
        (["src/main.py"], 1, ["cd" * 20, "cd" * 20], False),
    ],
)
def test_actual_authority_requires_complete_stable_nonempty_inventory(
    files: list[str], count: int, heads: list[str], delivered: bool
) -> None:
    provider = Mock()
    provider.get_pr_metadata.side_effect = [
        PRMetadata(
            number=42,
            title="change",
            head_branch="feature",
            head_sha=head,
            base_branch="main",
            changed_files=count,
        )
        for head in heads
    ]
    provider.get_ref_sha.return_value = "ef" * 20
    provider.list_pr_files_complete.return_value = files

    with patch(f"{MODULE}.GitHubActionsProvider", return_value=provider):
        result = _run_bridge("owner/repo", 42, SHA.upper())

    assert result == {
        "repository": "owner/repo",
        "prNumber": 42,
        "headSha": SHA,
        "outcome": "DELIVERED" if delivered else "UNKNOWN",
        "complete": delivered,
        "diffEvidence": "NON_ZERO_DIFF" if delivered else "UNKNOWN",
    }
    provider.list_pr_files_complete.assert_called_once_with(42, count)


@pytest.mark.parametrize("error", [RuntimeError("provider unavailable"), ProviderRateLimitError(is_rate_limit=False)])
def test_actual_authority_normalizes_nonrate_provider_errors(error: Exception) -> None:
    provider = Mock()
    provider.get_pr_metadata.side_effect = error

    with patch(f"{MODULE}.GitHubActionsProvider", return_value=provider):
        result = _run_bridge("owner/repo", 42, SHA)

    assert result["outcome"] == "UNKNOWN"
    assert result["complete"] is False
    assert result["diffEvidence"] == "UNKNOWN"
    assert result["repository"] == "owner/repo"
    assert result["prNumber"] == 42
    assert result["headSha"] == SHA


def test_actual_authority_propagates_rate_limits() -> None:
    error = ProviderRateLimitError(30, provider="github")
    provider = Mock()
    provider.get_pr_metadata.side_effect = error

    with patch(f"{MODULE}.GitHubActionsProvider", return_value=provider):
        with pytest.raises(ProviderRateLimitError) as exc:
            _run_bridge("owner/repo", 42, SHA)

    assert exc.value is error
