"""Tests for classify_initial_delivery_with_head."""

from collections.abc import Sequence
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.models import PRMetadata
from agentic_devtools.cli.ci.pipeline.delivery import InitialDeliveryOutcome, classify_initial_delivery_with_head
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


def _provider(*, files: list[str], head_shas: Sequence[str] = ("initial-head", "initial-head")) -> Mock:
    provider = Mock()
    provider.get_pr_metadata.side_effect = [
        PRMetadata(
            number=1,
            title="change",
            head_branch="feature",
            head_sha=sha,
            base_branch="main",
            changed_files=len(files),
        )
        for sha in head_shas
    ]
    provider.get_ref_sha.side_effect = ["base", "base"]
    provider.list_pr_files_complete.return_value = files
    return provider


@pytest.mark.parametrize(
    ("files", "head_sha", "initial_plan_sha", "expected"),
    [
        (["src/main.py"], "initial-head", "initial-head", InitialDeliveryOutcome.DELIVERED),
        (["src/main.py"], "advanced", "initial-head", InitialDeliveryOutcome.DELIVERED),
        ([], "initial-head", "initial-head", InitialDeliveryOutcome.NO_DELIVERY),
        ([], "initial-head", None, InitialDeliveryOutcome.UNKNOWN),
        ([], "initial-head", "", InitialDeliveryOutcome.UNKNOWN),
        ([], "initial-head", "  ", InitialDeliveryOutcome.UNKNOWN),
        ([], "advanced", "initial-head", InitialDeliveryOutcome.UNKNOWN),
        ([], "initial-head", 1, InitialDeliveryOutcome.UNKNOWN),
        ([], " head ", " head ", InitialDeliveryOutcome.NO_DELIVERY),
    ],
)
def test_returns_exact_classified_head_from_one_inventory(
    files: list[str], head_sha: str, initial_plan_sha: object, expected: InitialDeliveryOutcome
) -> None:
    provider = _provider(files=files, head_shas=(head_sha, head_sha))

    assert classify_initial_delivery_with_head(
        provider,
        1,
        completion_confirmed=True,
        initial_plan_sha=initial_plan_sha,  # type: ignore[arg-type]
    ) == (head_sha, expected)
    assert provider.get_pr_metadata.call_count == 2
    assert provider.get_ref_sha.call_count == 2
    provider.list_pr_files_complete.assert_called_once_with(1, len(files))


@pytest.mark.parametrize("completion_confirmed", [False, None, 1, "true"])
@pytest.mark.parametrize("pr_number", [0, -1, True, "1", None])
def test_unconfirmed_completion_neither_observes_nor_validates(completion_confirmed: object, pr_number: object) -> None:
    provider = Mock()

    assert classify_initial_delivery_with_head(
        provider,
        pr_number,  # type: ignore[arg-type]
        completion_confirmed=completion_confirmed,  # type: ignore[arg-type]
        initial_plan_sha="initial-head",
    ) == ("", InitialDeliveryOutcome.UNKNOWN)
    assert provider.mock_calls == []


@pytest.mark.parametrize("pr_number", [0, -1, True, "1", None])
def test_confirmed_invalid_pr_number_raises(pr_number: object) -> None:
    provider = Mock()

    with pytest.raises(ValueError, match="pr_number must be a positive integer"):
        classify_initial_delivery_with_head(
            provider,
            pr_number,  # type: ignore[arg-type]
            completion_confirmed=True,
            initial_plan_sha=None,
        )
    assert provider.mock_calls == []


@pytest.mark.parametrize("head_shas", [("initial-head", "advanced"), ("initial-head", "")])
def test_head_change_or_missing_after_identity_returns_no_head(head_shas: Sequence[str]) -> None:
    provider = _provider(files=["src/main.py"], head_shas=head_shas)

    assert classify_initial_delivery_with_head(
        provider, 1, completion_confirmed=True, initial_plan_sha="initial-head"
    ) == ("", InitialDeliveryOutcome.UNKNOWN)
    assert provider.get_pr_metadata.call_count == 2
    provider.list_pr_files_complete.assert_called_once_with(1, 1)


@pytest.mark.parametrize("failure_step", ["metadata", "base", "inventory"])
@pytest.mark.parametrize("error", [RuntimeError("unavailable"), ProviderRateLimitError(is_rate_limit=False)])
def test_unavailable_observation_returns_no_head(failure_step: str, error: Exception) -> None:
    provider = _provider(files=["src/main.py"])
    method = {
        "metadata": provider.get_pr_metadata,
        "base": provider.get_ref_sha,
        "inventory": provider.list_pr_files_complete,
    }[failure_step]
    method.side_effect = error

    assert classify_initial_delivery_with_head(
        provider, 1, completion_confirmed=True, initial_plan_sha="initial-head"
    ) == ("", InitialDeliveryOutcome.UNKNOWN)


def test_incomplete_inventory_returns_no_head() -> None:
    provider = _provider(files=["src/main.py"])
    provider.list_pr_files_complete.return_value = []

    assert classify_initial_delivery_with_head(
        provider, 1, completion_confirmed=True, initial_plan_sha="initial-head"
    ) == ("", InitialDeliveryOutcome.UNKNOWN)
    assert provider.get_pr_metadata.call_count == 1
    provider.list_pr_files_complete.assert_called_once_with(1, 1)


@pytest.mark.parametrize("failure_step", ["metadata", "inventory"])
def test_rate_limit_error_propagates(failure_step: str) -> None:
    provider = _provider(files=[])
    error = ProviderRateLimitError(30, provider="github")
    method = provider.get_pr_metadata if failure_step == "metadata" else provider.list_pr_files_complete
    method.side_effect = error

    with pytest.raises(ProviderRateLimitError) as exc_info:
        classify_initial_delivery_with_head(provider, 1, completion_confirmed=True, initial_plan_sha=None)
    assert exc_info.value is error
