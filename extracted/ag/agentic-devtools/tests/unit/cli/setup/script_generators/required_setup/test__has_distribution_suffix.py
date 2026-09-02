"""Tests for _has_distribution_suffix."""

from agentic_devtools.cli.setup.script_generators.required_setup import _has_distribution_suffix


class TestHasDistributionSuffix:
    """Tests for _has_distribution_suffix."""

    def test_accepts_valid_release_and_dev_local_suffixes(self) -> None:
        """Release and dev/local suffix shapes are accepted."""
        assert _has_distribution_suffix(".dist-info") is True
        assert _has_distribution_suffix("-1.2.3.dist-info") is True
        assert _has_distribution_suffix("-0.2.9.dev1+g1234abc.dist-info") is True
        assert _has_distribution_suffix("-1.2.3") is True

    def test_rejects_invalid_or_unrelated_suffixes(self) -> None:
        """Unrelated package-name remainders stay rejected."""
        assert _has_distribution_suffix("") is False
        assert _has_distribution_suffix(".egg-info") is False
        assert _has_distribution_suffix("extra-1.0.0.dist-info") is False
        assert _has_distribution_suffix("-extra-1.0.0.dist-info") is False
        assert _has_distribution_suffix("-2-extra-1.0.dist-info") is False
        assert _has_distribution_suffix("-0.2.9_dev1.dist-info") is False
