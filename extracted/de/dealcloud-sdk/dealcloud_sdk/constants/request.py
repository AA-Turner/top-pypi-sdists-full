"""
Request constants with DealCloud API best practices.

Note: These constants are used by our custom HTTPX retry transport.
Unlike the requests library (which uses urllib3.Retry), HTTPX doesn't
have built-in retry. We implement our own retry logic.

See: https://api.docs.dealcloud.com/docs - Rate Limits section
"""

# =============================================================================
# Retry Configuration
# =============================================================================

# Default max retries for status codes not in RETRY_COUNT_BY_STATUS
MAX_RETRIES_DEFAULT = 5

# Status codes that should trigger a retry
# - 429: Rate limited (most common with DealCloud)
# - 500: Internal server error (transient)
# - 502/503/504: Gateway/service errors (transient)
RETRYABLE_STATUS_CODES = (429, 500, 502, 503, 504)

# Per-status retry counts (from .NET SDK best practices)
# 429 gets more retries since rate limits are expected and temporary
RETRY_COUNT_BY_STATUS = {
    429: 5,   # Rate limits: more retries with backoff
    500: 2,   # Internal server error: fewer retries
    502: 2,   # Bad gateway
    503: 2,   # Service unavailable
    504: 2,   # Gateway timeout
}

# Exponential backoff multiplier: wait = backoff_factor^attempt
# Higher factor = longer waits = fewer requests = gentler on API
BACKOFF_FACTOR = 2.0

# Maximum wait time between retries (seconds)
MAX_BACKOFF_SECONDS = 300.0  # 5 minutes cap

# =============================================================================
# Timeout Configuration
# =============================================================================

# Default request timeout in seconds
DEFAULT_TIMEOUT_SECONDS = 120

# =============================================================================
# Rate Limit Handling
# =============================================================================

# Honor Retry-After header from 429 responses
# DealCloud returns this header to indicate when to retry
RESPECT_RETRY_AFTER_HEADER = True


