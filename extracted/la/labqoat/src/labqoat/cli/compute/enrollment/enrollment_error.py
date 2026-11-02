"""Connected-host bootstrap failure carrying only observed, nonsecret evidence."""

from __future__ import annotations


class EnrollmentError(RuntimeError):
    """A preflight, transfer, installation or readiness step did not succeed."""
