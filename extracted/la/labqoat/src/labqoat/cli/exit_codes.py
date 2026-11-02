"""Process exit codes for CLI commands."""

from __future__ import annotations


class ExitCodes:
    """Stable exit values for scripting."""

    SUCCESS = 0
    DOMAIN_FAILURE = 1
    USAGE_ERROR = 2
    AUTH_FAILURE = 1
    TRANSPORT_FAILURE = 1
    DEADLINE_EXCEEDED = 1
    WAIT_TIMEOUT = 3
    INTERRUPTED = 130
