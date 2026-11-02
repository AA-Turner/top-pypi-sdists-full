"""Tests for classify_pr_diff_evidence."""

from collections.abc import Sequence
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.models import PRMetadata
from agentic_devtools.cli.ci.pipeline.delivery import PRDiffEvidence, classify_pr_diff_evidence
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


def _metadata(
    base_branch: str = "main",
    head_sha: str = "head",
    changed_files: int = 0,
) -> PRMetadata:
    return PRMetadata(
        number=1,
        title="change",
        head_branch="feature",
        head_sha=head_sha,
        base_branch=base_branch,
        changed_files=changed_files,
    )


def _provider(
    *,
    metadata: Sequence[object] = (_metadata(), _metadata()),
    base_shas: Sequence[str] = ("base", "base"),
    files: list[str] | None = None,
) -> Mock:
    provider = Mock()
    provider.get_pr_metadata.side_effect = metadata
    provider.get_ref_sha.side_effect = base_shas
    provider.list_pr_files_complete.return_value = [] if files is None else files
    return provider


@pytest.mark.parametrize(
    ("files", "expected", "changed_files"),
    [
        ([], PRDiffEvidence.ZERO_DIFF, 0),
        (["src/main.py"], PRDiffEvidence.NON_ZERO_DIFF, 1),
    ],
)
def test_classifies_complete_inventory(files: list[str], expected: PRDiffEvidence, changed_files: int) -> None:
    metadata = _metadata(changed_files=changed_files)
    provider = _provider(metadata=(metadata, metadata), files=files)

    result = classify_pr_diff_evidence(provider, 1)

    assert isinstance(result, PRDiffEvidence)
    assert result is expected
    assert provider.get_pr_metadata.call_count == 2
    assert provider.get_ref_sha.call_args_list[0].args == ("main",)
    assert provider.get_ref_sha.call_args_list[1].args == ("main",)
    assert provider.list_pr_files_complete.call_args.args == (1, changed_files)


@pytest.mark.parametrize(
    ("metadata", "base_shas"),
    [
        ((_metadata(), _metadata(head_sha="advanced")), ("base", "base")),
        ((_metadata(), _metadata(base_branch="release")), ("base", "base")),
        ((_metadata(), _metadata()), ("base", "changed-base")),
    ],
)
def test_returns_unknown_when_base_or_head_changes_during_inventory(
    metadata: Sequence[PRMetadata], base_shas: Sequence[str]
) -> None:
    metadata = tuple(_metadata(item.base_branch, item.head_sha, changed_files=1) for item in metadata)
    provider = _provider(metadata=metadata, base_shas=base_shas, files=["src/main.py"])

    assert classify_pr_diff_evidence(provider, 1) is PRDiffEvidence.UNKNOWN


@pytest.mark.parametrize(
    "setup",
    [
        "metadata",
        "base",
        "inventory",
        "malformed_inventory",
    ],
)
def test_returns_unknown_when_fresh_evidence_is_unavailable_or_incomplete(setup: str) -> None:
    provider = _provider()
    if setup == "metadata":
        provider.get_pr_metadata.side_effect = RuntimeError("metadata unavailable")
    elif setup == "base":
        provider.get_ref_sha.side_effect = ["", "base"]
    elif setup == "inventory":
        provider.list_pr_files_complete.side_effect = RuntimeError("file inventory unavailable")
    else:
        provider.get_pr_metadata.side_effect = (_metadata(changed_files=1), _metadata(changed_files=1))
        provider.list_pr_files_complete.return_value = [SimpleNamespace(filename="src/main.py")]

    assert classify_pr_diff_evidence(provider, 1) is PRDiffEvidence.UNKNOWN


def test_returns_unknown_when_file_count_does_not_match_complete_inventory() -> None:
    provider = _provider(files=[])
    provider.get_pr_metadata.side_effect = (
        _metadata(changed_files=1),
        _metadata(changed_files=1),
    )

    assert classify_pr_diff_evidence(provider, 1) is PRDiffEvidence.UNKNOWN


def test_returns_unknown_when_provider_cannot_prove_inventory_completeness() -> None:
    provider = _provider()
    del provider.list_pr_files_complete

    assert classify_pr_diff_evidence(provider, 1) is PRDiffEvidence.UNKNOWN


@pytest.mark.parametrize("failure_step", ["metadata", "inventory"])
def test_propagates_rate_limit_errors(failure_step: str) -> None:
    provider = _provider()
    error = ProviderRateLimitError(30, provider="github")
    if failure_step == "metadata":
        provider.get_pr_metadata.side_effect = error
    else:
        provider.list_pr_files_complete.side_effect = error

    with pytest.raises(ProviderRateLimitError) as exc_info:
        classify_pr_diff_evidence(provider, 1)

    assert exc_info.value is error


def test_logs_unavailable_inventory_before_returning_unknown(caplog: pytest.LogCaptureFixture) -> None:
    provider = _provider()
    provider.list_pr_files_complete.side_effect = RuntimeError("inventory unavailable")

    assert classify_pr_diff_evidence(provider, 1) is PRDiffEvidence.UNKNOWN
    assert "Unable to verify PR diff evidence for #1" in caplog.text


def test_logs_non_rate_limit_provider_error_and_returns_unknown(caplog: pytest.LogCaptureFixture) -> None:
    provider = _provider()
    provider.list_pr_files_complete.side_effect = ProviderRateLimitError(is_rate_limit=False)

    assert classify_pr_diff_evidence(provider, 1) is PRDiffEvidence.UNKNOWN
    assert "Provider rate limit exhausted" in caplog.text


def test_returns_unknown_when_metadata_or_base_sha_is_malformed() -> None:
    provider = _provider(metadata=(SimpleNamespace(base_branch="", head_sha="head"), _metadata()))

    assert classify_pr_diff_evidence(provider, 1) is PRDiffEvidence.UNKNOWN


@pytest.mark.parametrize("pr_number", [True, 0, None])
def test_invalid_pr_number_raises_value_error(pr_number: object) -> None:
    with pytest.raises(ValueError, match="pr_number must be a positive integer"):
        classify_pr_diff_evidence(Mock(), pr_number)  # type: ignore[arg-type]
