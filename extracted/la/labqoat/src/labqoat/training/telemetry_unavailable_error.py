"""Retryable experiment telemetry transport failure."""


class TelemetryUnavailableError(RuntimeError):
    """The experiment backend is temporarily unavailable."""
