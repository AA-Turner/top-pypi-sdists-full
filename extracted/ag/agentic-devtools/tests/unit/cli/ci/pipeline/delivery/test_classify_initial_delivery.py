"""Tests for classify_initial_delivery."""

from collections.abc import Sequence
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.models import PRMetadata
from agentic_devtools.cli.ci.pipeline.delivery import InitialDeliveryOutcome, classify_initial_delivery
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


def _metadata(head_sha: str = "initial-head", changed_files: int = 0) -> PRMetadata:
    return PRMetadata(
        number=1,
        title="change",
        head_branch="feature",
        head_sha=head_sha,
        base_branch="main",
        changed_files=changed_files,
    )


def _provider(*, files: list[str], head_shas: Sequence[str] = ("initial-head", "initial-head")) -> Mock:
    provider = Mock()
    changed_files = len(files)
    provider.get_pr_metadata.side_effect = [_metadata(sha, changed_files) for sha in head_shas]
    provider.get_ref_sha.side_effect = ["base", "base"]
    provider.list_pr_files_complete.return_value = files
    return provider


def test_returns_no_delivery_only_for_confirmed_empty_diff_at_initial_head() -> None:
    provider = _provider(files=[])

    assert (
        classify_initial_delivery(
            provider,
            1,
            completion_confirmed=True,
            initial_plan_sha="initial-head",
        )
        is InitialDeliveryOutcome.NO_DELIVERY
    )


@pytest.mark.parametrize("head_shas", [("initial-head", "initial-head"), ("advanced", "advanced")])
def test_non_empty_diff_is_delivered_at_unchanged_or_advanced_head(head_shas: Sequence[str]) -> None:
    provider = _provider(files=["src/main.py"], head_shas=head_shas)

    assert (
        classify_initial_delivery(
            provider,
            1,
            completion_confirmed=True,
            initial_plan_sha="initial-head",
        )
        is InitialDeliveryOutcome.DELIVERED
    )


@pytest.mark.parametrize(
    ("completion_confirmed", "files", "head_sha", "initial_plan_sha"),
    [
        (False, ["src/main.py"], "initial-head", "initial-head"),
        (True, [], "initial-head", None),
        (True, [], "advanced", "initial-head"),
    ],
)
def test_missing_completion_or_authoritative_identity_fails_closed(
    completion_confirmed: bool,
    files: list[str],
    head_sha: str,
    initial_plan_sha: str | None,
) -> None:
    provider = _provider(files=files, head_shas=(head_sha, head_sha))

    assert (
        classify_initial_delivery(
            provider,
            1,
            completion_confirmed=completion_confirmed,
            initial_plan_sha=initial_plan_sha,
        )
        is InitialDeliveryOutcome.UNKNOWN
    )


def test_unknown_diff_evidence_cannot_authorize_delivery() -> None:
    provider = _provider(files=[])
    provider.list_pr_files_complete.side_effect = RuntimeError("incomplete inventory")

    assert (
        classify_initial_delivery(
            provider,
            1,
            completion_confirmed=True,
            initial_plan_sha="initial-head",
        )
        is InitialDeliveryOutcome.UNKNOWN
    )


def test_returns_outcome_only_from_one_observation() -> None:
    provider = _provider(files=["src/main.py"])

    result = classify_initial_delivery(provider, 1, completion_confirmed=True, initial_plan_sha=None)

    assert isinstance(result, InitialDeliveryOutcome)
    assert result is InitialDeliveryOutcome.DELIVERED
    assert provider.get_pr_metadata.call_count == 2
    provider.list_pr_files_complete.assert_called_once_with(1, 1)


@pytest.mark.parametrize("pr_number", [0, -1, True, "1", None])
def test_confirmed_invalid_pr_number_raises(pr_number: object) -> None:
    with pytest.raises(ValueError, match="pr_number must be a positive integer"):
        classify_initial_delivery(
            Mock(),
            pr_number,  # type: ignore[arg-type]
            completion_confirmed=True,
            initial_plan_sha=None,
        )


@pytest.mark.parametrize("completion_confirmed", [False, 1])
def test_unconfirmed_completion_does_not_observe_or_validate(completion_confirmed: object) -> None:
    provider = Mock()

    assert (
        classify_initial_delivery(
            provider,
            0,
            completion_confirmed=completion_confirmed,  # type: ignore[arg-type]
            initial_plan_sha=None,
        )
        is InitialDeliveryOutcome.UNKNOWN
    )
    assert provider.mock_calls == []


def test_rate_limit_error_propagates() -> None:
    provider = _provider(files=[])
    error = ProviderRateLimitError(30, provider="github")
    provider.list_pr_files_complete.side_effect = error

    with pytest.raises(ProviderRateLimitError) as exc_info:
        classify_initial_delivery(provider, 1, completion_confirmed=True, initial_plan_sha=None)
    assert exc_info.value is error
