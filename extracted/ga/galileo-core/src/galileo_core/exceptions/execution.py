from typing import Optional

from galileo_core.exceptions.base import BaseGalileoException


class ExecutionError(BaseGalileoException):
    """Raised when there is an issue with the execution of a task or process."""

    error_type: Optional[str] = None


class MetricNotFoundError(ExecutionError):
    """Raised when attempting to access a metric that doesn't exist in the Metrics object."""

    def __init__(self, metric_name: str, extra: Optional[dict] = None):
        message = (
            f"Metric '{metric_name}' does not exist. "
            f"The metric you have attempted to retrieve is either not in the required metrics, "
            f"or you have used an incorrect name."
        )
        super().__init__(message, extra)
        self.metric_name = metric_name


class MetricStatusError(ExecutionError):
    """Base class for errors when a metric has a non-success status."""

    def __init__(self, metric_name: str, status: str, extra: Optional[dict] = None):
        message = f"Metric '{metric_name}' has status '{status}'."
        super().__init__(message, extra)
        self.metric_name = metric_name
        self.status = status


class MetricFailedError(MetricStatusError):
    """Raised when attempting to access a metric that has 'failed' status."""

    def __init__(self, metric_name: str, extra: Optional[dict] = None):
        super().__init__(metric_name, "failed", extra)


class MetricErrorError(MetricStatusError):
    """Raised when attempting to access a metric that has 'error' status."""

    def __init__(self, metric_name: str, extra: Optional[dict] = None):
        super().__init__(metric_name, "error", extra)


class MetricNotComputedError(MetricStatusError):
    """Raised when attempting to access a metric that has 'not_computed' status."""

    def __init__(self, metric_name: str, extra: Optional[dict] = None):
        super().__init__(metric_name, "not_computed", extra)


class MetricNotApplicableError(MetricStatusError):
    """Raised when attempting to access a metric that has 'not_applicable' status."""

    def __init__(self, metric_name: str, extra: Optional[dict] = None):
        super().__init__(metric_name, "not_applicable", extra)


class MetricPendingError(MetricStatusError):
    """Raised when attempting to access a metric that has 'pending' status (still queued)."""

    def __init__(self, metric_name: str, extra: Optional[dict] = None):
        super().__init__(metric_name, "pending", extra)


class MetricComputingError(MetricStatusError):
    """Raised when attempting to access a metric that has 'computing' status (still in progress)."""

    def __init__(self, metric_name: str, extra: Optional[dict] = None):
        super().__init__(metric_name, "computing", extra)
