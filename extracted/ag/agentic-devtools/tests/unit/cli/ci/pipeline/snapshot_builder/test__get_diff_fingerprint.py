"""Tests for _get_diff_fingerprint."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.pipeline.snapshot_builder import _get_diff_fingerprint


def test_returns_supported_fingerprint(monkeypatch) -> None:
    """A non-empty string from a capable provider is available."""
    provider = MagicMock()
    provider.compute_diff_hash.return_value = "fingerprint"
    monkeypatch.setattr("agentic_devtools.cli.ci.pipeline.snapshot_builder._supports_diff_fingerprint", lambda _p: True)

    assert _get_diff_fingerprint(provider, 7, "main", "head", {}) == ("fingerprint", True, True)


def test_unavailable_fingerprint_is_not_treated_as_failure(monkeypatch) -> None:
    """An empty provider result leaves the optional fingerprint unavailable."""
    provider = MagicMock()
    provider.compute_diff_hash.return_value = ""
    monkeypatch.setattr("agentic_devtools.cli.ci.pipeline.snapshot_builder._supports_diff_fingerprint", lambda _p: True)

    assert _get_diff_fingerprint(provider, 7, "main", "head", {}) == ("", True, False)


def test_unsupported_provider_skips_fingerprint_lookup(monkeypatch) -> None:
    """Providers without fingerprint support return the unsupported state."""
    provider = MagicMock()
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.pipeline.snapshot_builder._supports_diff_fingerprint", lambda _p: False
    )

    assert _get_diff_fingerprint(provider, 7, "main", "head", {}) == ("", False, False)
    provider.compute_diff_hash.assert_not_called()
