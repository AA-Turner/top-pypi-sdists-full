"""Tests for provider rate-limit propagation."""

import pytest

from agentic_devtools.cli.ci.pipeline.snapshot_utils import _raise_if_rate_limit
from agentic_devtools.cli.ci.retry import ProviderRateLimitError


def test_reraises_provider_rate_limits() -> None:
    error = ProviderRateLimitError(provider="github", is_rate_limit=True)

    try:
        raise error
    except ProviderRateLimitError as caught:
        with pytest.raises(ProviderRateLimitError):
            _raise_if_rate_limit(caught)


def test_ignores_non_rate_limit_provider_errors() -> None:
    _raise_if_rate_limit(ProviderRateLimitError(provider="github", is_rate_limit=False))


def test_ignores_other_exception_types() -> None:
    _raise_if_rate_limit(RuntimeError("ordinary failure"))
