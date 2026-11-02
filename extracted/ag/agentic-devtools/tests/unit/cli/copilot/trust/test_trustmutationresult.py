"""Tests for TrustMutationResult."""

from agentic_devtools.cli.copilot.trust import TrustMutationResult


class TestTrustMutationResult:
    """Tests for TrustMutationResult."""

    def test_defaults(self):
        """added defaults to False when not provided."""
        result = TrustMutationResult(succeeded=True)
        assert result.succeeded is True
        assert result.added is False

    def test_explicit_fields(self):
        """Both fields are set when provided explicitly."""
        result = TrustMutationResult(succeeded=True, added=True)
        assert result.succeeded is True
        assert result.added is True

    def test_failed_with_ownership(self):
        """succeeded=False with added=True represents a write-succeeded-but-verify-failed state."""
        result = TrustMutationResult(succeeded=False, added=True)
        assert result.succeeded is False
        assert result.added is True

    def test_equality(self):
        """Two instances with the same field values are equal."""
        assert TrustMutationResult(True, True) == TrustMutationResult(True, True)
        assert TrustMutationResult(True) == TrustMutationResult(True, False)
        assert TrustMutationResult(False, True) != TrustMutationResult(True, True)

    def test_immutable(self):
        """Frozen dataclass rejects field mutation."""
        import pytest

        result = TrustMutationResult(succeeded=True, added=True)
        with pytest.raises(Exception):
            result.succeeded = False  # type: ignore[misc]
