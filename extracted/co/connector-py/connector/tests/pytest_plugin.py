"""
Pytest plugin registered as a pytest11 entry point in the connector SDK.

Provides shared fixtures for all connector tests without requiring a conftest.py
in the projects/connectors/python/ directory.
"""

from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def suppress_rate_limit_state_passthrough():
    """Suppress rate limit state collection during tests.

    RateLimiter.get_current_state() returns a snapshot whose values depend on
    the connector's RateLimitConfig/state (requests_per_window, window_seconds, etc.).
    This makes the 'rate_limit' field in every response non-deterministic across
    connectors, which would require every test case to explicitly set an expected
    rate_limit value.

    Patching get_current_state to return None causes BaseIntegrationClient.__aexit__
    to write None into RATE_LIMIT_RESULT_CONTEXT, so the executor never populates
    response.rate_limit — leaving it as the model default (None) for all responses.

    Note:
    Keep the import inside the fixture to not load it before pytest/cov starts collection,
    otherwise you will see coverage discrepancies.
    """
    from connector.utils.rate_limiting import RateLimiter

    with patch.object(RateLimiter, "get_current_state", return_value=None):
        yield
