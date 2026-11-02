"""A Python client for forge-dashboard's REST API
(github.com/alrayyes/forge-dashboard), generated from its OpenAPI spec
with openapi-python-client.

Every operation except ``get_version`` and the two webhook receivers
requires an authenticated session -- see :class:`ForgeDashboardClient` for
the bearer-token auth story.
"""

from .client import API_TOKEN_ENV_VAR, ForgeDashboardClient
from .errors import APIError, decode_error
from .retry import DEFAULT_RETRY_CONFIG, AsyncRetryTransport, RetryConfig, RetryTransport

__all__ = [
    "API_TOKEN_ENV_VAR",
    "DEFAULT_RETRY_CONFIG",
    "APIError",
    "AsyncRetryTransport",
    "ForgeDashboardClient",
    "RetryConfig",
    "RetryTransport",
    "decode_error",
]
