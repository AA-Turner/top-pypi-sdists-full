from __future__ import annotations


class ExperimentError(RuntimeError):
    """Base error for scientist workflow failures."""


class ExperimentFingerprintMismatchError(ExperimentError):
    """Raised when a run directory is reused for a different request."""


class ExperimentUnsupportedOperationError(ExperimentError):
    """Raised when a workflow operation is not supported for a run type."""
