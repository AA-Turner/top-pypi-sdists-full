"""Tests for _get_head_author."""

from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.pipeline.snapshot_builder import _get_head_author
from agentic_devtools.cli.ci.retry import ProviderRateLimitError


def test_returns_string_author_and_defaults_invalid_or_failed_lookups() -> None:
    """Invalid provider values and ordinary lookup errors produce an empty login."""
    provider = MagicMock()
    provider.get_commit_author_login.return_value = "author"
    assert _get_head_author(provider, "head") == "author"

    provider.get_commit_author_login.return_value = None
    assert _get_head_author(provider, "head") == ""

    provider.get_commit_author_login.side_effect = RuntimeError("lookup failed")
    assert _get_head_author(provider, "head") == ""


def test_propagates_provider_rate_limit() -> None:
    """Rate limits are not swallowed by the best-effort author lookup."""
    provider = MagicMock()
    provider.get_commit_author_login.side_effect = ProviderRateLimitError(is_rate_limit=True)

    with pytest.raises(ProviderRateLimitError):
        _get_head_author(provider, "head")


def test_swallows_rate_limit_error_not_marked_as_rate_limit() -> None:
    """A provider error without the rate-limit flag follows ordinary fail-open behavior."""
    provider = MagicMock()
    provider.get_commit_author_login.side_effect = ProviderRateLimitError(is_rate_limit=False)

    assert _get_head_author(provider, "head") == ""
