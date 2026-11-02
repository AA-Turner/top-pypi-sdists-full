"""Tests for get_exact_diff_fingerprint."""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.pipeline.runner_diff_fingerprint import get_exact_diff_fingerprint
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

_VALID_DIFF = "diff --git a/file.py b/file.py\n@@ -1 +1 @@\n-old\n+new\n"


def test_fetches_and_validates_a_pinned_exact_diff() -> None:
    """A valid provider patch is fingerprinted using its pinned base and inventory."""
    provider = MagicMock()
    provider.get_commit_range_diff_bytes.return_value = _VALID_DIFF.encode()
    provider.get_commit_range_diff_change_counts.return_value = {"file.py": 2}

    fingerprint = get_exact_diff_fingerprint(
        provider,
        base_sha="base",
        head_sha="head",
        expected_files=["file.py"],
        pr_number=42,
    )

    assert fingerprint.startswith("exact-diff-sha256:")
    provider.get_commit_range_diff_bytes.assert_called_once_with("base", "head")
    provider.get_commit_range_diff_change_counts.assert_called_once_with("base", "head")


@pytest.mark.parametrize("invalid_byte", [b"\x80", b"\x81"])
def test_fails_closed_for_distinct_invalid_utf8_diff_payloads(invalid_byte: bytes) -> None:
    """Distinct invalid UTF-8 patch bytes cannot produce an exact fingerprint."""
    provider = GitHubActionsProvider(repo="owner/repo")
    exact_diff = b"diff --git a/file.py b/file.py\n@@ -1 +1 @@\n-old\n+new" + invalid_byte + b"\n"
    mock_run_safe_results = [
        SimpleNamespace(returncode=0, stdout=exact_diff, stderr=b""),
        SimpleNamespace(
            returncode=0,
            stdout='{"files":[{"filename":"file.py","changes":2}]}',
            stderr="",
        ),
    ]

    with patch(
        "agentic_devtools.cli.ci.github_provider.run_safe",
        side_effect=mock_run_safe_results,
    ):
        fingerprint = get_exact_diff_fingerprint(
            provider,
            base_sha="base",
            head_sha="head",
            expected_files=["file.py"],
            pr_number=42,
        )

    assert fingerprint == ""


@pytest.mark.parametrize(
    ("base_sha", "expected_files"),
    [
        ("", ["file.py"]),
        ("base", []),
    ],
    ids=("no-base", "no-inventory"),
)
def test_skips_fetch_without_pinned_base_or_inventory(base_sha: str, expected_files: list[str]) -> None:
    """Missing prerequisites prevent an API lookup."""
    provider = MagicMock()

    assert (
        get_exact_diff_fingerprint(
            provider,
            base_sha=base_sha,
            head_sha="head",
            expected_files=expected_files,
            pr_number=42,
        )
        == ""
    )
    provider.get_commit_range_diff_bytes.assert_not_called()


def test_skips_provider_without_exact_diff_support() -> None:
    """A provider that does not implement exact diff retrieval fails closed."""
    provider = MagicMock()
    provider.get_commit_range_diff_bytes = None

    assert (
        get_exact_diff_fingerprint(
            provider,
            base_sha="base",
            head_sha="head",
            expected_files=["file.py"],
            pr_number=42,
        )
        == ""
    )


def test_skips_provider_without_completeness_evidence() -> None:
    """A diff without provider-reported change totals cannot authorize a fingerprint."""
    provider = MagicMock()
    provider.get_commit_range_diff_bytes.return_value = _VALID_DIFF.encode()
    provider.get_commit_range_diff_change_counts = None

    assert (
        get_exact_diff_fingerprint(
            provider,
            base_sha="base",
            head_sha="head",
            expected_files=["file.py"],
            pr_number=42,
        )
        == ""
    )
    provider.get_commit_range_diff_bytes.assert_not_called()


def test_rejects_non_mapping_change_counts() -> None:
    """Change totals must be a mapping before the parser can trust them."""
    provider = MagicMock()
    provider.get_commit_range_diff_bytes.return_value = _VALID_DIFF.encode()
    provider.get_commit_range_diff_change_counts.return_value = []

    assert (
        get_exact_diff_fingerprint(
            provider,
            base_sha="base",
            head_sha="head",
            expected_files=["file.py"],
            pr_number=42,
        )
        == ""
    )


def test_skips_unimplemented_base_diff_method() -> None:
    """The abstract provider implementation is not treated as patch evidence."""

    class _BaseMethod:
        __func__ = CIPlatformProvider.get_commit_range_diff_bytes

        def __call__(self, base_sha: str, head_sha: str) -> bytes:
            raise AssertionError("base provider method should not be called")

    provider = MagicMock()
    provider.get_commit_range_diff_bytes = _BaseMethod()

    assert (
        get_exact_diff_fingerprint(
            provider,
            base_sha="base",
            head_sha="head",
            expected_files=["file.py"],
            pr_number=42,
        )
        == ""
    )


def test_rejects_non_string_and_invalid_diff_responses() -> None:
    """Non-string and structurally invalid provider responses are not fingerprinted."""
    provider = MagicMock()
    provider.get_commit_range_diff_bytes.return_value = object()
    provider.get_commit_range_diff_change_counts.return_value = {"file.py": 2}
    assert (
        get_exact_diff_fingerprint(
            provider,
            base_sha="base",
            head_sha="head",
            expected_files=["file.py"],
            pr_number=42,
        )
        == ""
    )

    provider.get_commit_range_diff_bytes.return_value = b"diff --git a/file.py b/file.py\n"
    assert (
        get_exact_diff_fingerprint(
            provider,
            base_sha="base",
            head_sha="head",
            expected_files=["file.py"],
            pr_number=42,
        )
        == ""
    )


def test_returns_empty_and_logs_for_non_rate_limit_provider_error(caplog: pytest.LogCaptureFixture) -> None:
    """Ordinary comparison failures are logged and fail closed."""
    provider = MagicMock()
    provider.get_commit_range_diff_bytes.side_effect = RuntimeError("comparison unavailable")

    assert (
        get_exact_diff_fingerprint(
            provider,
            base_sha="base",
            head_sha="head",
            expected_files=["file.py"],
            pr_number=42,
        )
        == ""
    )
    assert "Failed to compute exact diff for head" in caplog.text


def test_reraises_rate_limit_provider_error() -> None:
    """Provider rate limits propagate instead of being converted to missing evidence."""
    provider = MagicMock()
    provider.get_commit_range_diff_bytes.side_effect = ProviderRateLimitError(
        provider="github",
        credential_identity="DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
    )

    with pytest.raises(ProviderRateLimitError):
        get_exact_diff_fingerprint(
            provider,
            base_sha="base",
            head_sha="head",
            expected_files=["file.py"],
            pr_number=42,
        )
