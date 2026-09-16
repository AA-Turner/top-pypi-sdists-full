"""Tests for _supports_diff_fingerprint."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.pipeline.snapshot import _supports_diff_fingerprint
from agentic_devtools.cli.ci.provider import CIPlatformProvider


class TestSupportsDiffFingerprint:
    """Unit tests for diff-fingerprint capability detection."""

    def test_returns_false_when_provider_has_no_callable_method(self) -> None:
        provider = MagicMock()
        provider.compute_diff_hash = None

        assert _supports_diff_fingerprint(provider) is False

    def test_returns_true_for_overridden_callable_method(self) -> None:
        provider = MagicMock()

        def compute_diff_hash(*, base_branch: str, sha: str) -> str:
            return f"{base_branch}:{sha}"

        provider.compute_diff_hash = compute_diff_hash

        assert _supports_diff_fingerprint(provider) is True

    def test_returns_false_for_inherited_base_provider_method(self) -> None:
        provider = MagicMock()
        provider.compute_diff_hash = CIPlatformProvider.compute_diff_hash.__get__(provider, MagicMock)

        assert _supports_diff_fingerprint(provider) is False
