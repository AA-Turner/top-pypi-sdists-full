"""Tests for the throttle's first-rate-limit notification hook."""

from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.dispatcher_policy import _notify_rate_limit
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


@pytest.mark.parametrize("is_rate_limit", [False, True])
@pytest.mark.parametrize("configured", [False, True])
def test_notifies_only_confirmed_limits_with_a_configured_producer(is_rate_limit, configured):
    callback = Mock()
    error = ProviderRateLimitError(7200, is_rate_limit=is_rate_limit)
    _notify_rate_limit(error, callback if configured else None)
    if configured and is_rate_limit:
        callback.assert_called_once_with(error)
    else:
        callback.assert_not_called()
