"""Validated server fit authority mapped conservatively onto the worker's monotonic clock."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
import math

from labqoat.json_document import JsonDocument


@dataclass(frozen=True)
class FitGrant:
    """Retain immutable server identity and an expiry that includes all request and replay latency."""

    id: str
    run_id: str
    attempt_id: str
    fence: int
    duration_ms: int
    starts_at: datetime
    expires_at: datetime
    not_before: float
    deadline: float

    @classmethod
    def capture(cls, value: JsonDocument, requested_at: float, received_at: float) -> "FitGrant":
        """Reject closed, malformed and already expired grants before granting physical authority."""
        now = cls._timestamp(value, "server_now")
        starts, expires = cls._timestamp(value, "starts_at"), cls._timestamp(value, "expires_at")
        duration, fence = cls._integer(value, "duration_ms"), cls._integer(value, "fence")
        not_before = received_at + max(0.0, (starts - now).total_seconds())
        deadline = requested_at + (expires - now).total_seconds()
        valid_clock = math.isfinite(requested_at) and math.isfinite(received_at) and received_at >= requested_at
        if not valid_clock or value["status"] != "open" or deadline <= not_before:
            raise ValueError("Fit grant is closed, expired or has no safely executable interval")
        if not 1 <= duration <= 30_000 or (expires - starts).total_seconds() != duration / 1000 or fence < 0:
            raise ValueError("Fit grant has invalid bounds")
        return cls(
            cls._identity(value, "id"),
            cls._identity(value, "run_id"),
            cls._identity(value, "attempt_id"),
            fence,
            duration,
            starts,
            expires,
            not_before,
            deadline,
        )

    @staticmethod
    def _timestamp(value: JsonDocument, key: str) -> datetime:
        """Require a timezone-aware server timestamp rather than trusting the worker's wall clock."""
        timestamp = datetime.fromisoformat(JsonDocument.expect_scalar(value[key], str))
        if timestamp.tzinfo is None:
            raise ValueError("Fit timestamps must include their timezone")
        return timestamp

    @staticmethod
    def _integer(value: JsonDocument, key: str) -> int:
        """Reject booleans and coercion in execution-authority counters."""
        number = value[key]
        if type(number) is not int:
            raise ValueError("Fit counters must be integers")
        return number

    @staticmethod
    def _identity(value: JsonDocument, key: str) -> str:
        """Require canonical UUIDs before composing scoped resource paths."""
        return str(UUID(JsonDocument.expect_scalar(value[key], str)))
