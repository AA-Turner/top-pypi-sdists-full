"""Health indicator protocol, base class, and built-in implementations."""

import inspect
import logging
import shutil
from typing import Any, Protocol

logger = logging.getLogger(__name__)


class HealthIndicator(Protocol):
    """Contract for health indicators contributing to ``/actuator/health``.

    Each indicator reports its own status and optional details.
    """

    def health(self) -> dict[str, Any]:
        """Return health status for this indicator.

        Returns:
            Dict with at minimum ``{"status": "UP"|"DOWN"|...}``.
            May include a ``"details"`` key with arbitrary metadata.
        """


class BaseHealthIndicator:
    """Exception-safe base class for health indicators.

    Subclass and override ``_check()`` to implement the health logic.
    ``health()`` wraps ``_check()`` in a try/except so exceptions never
    leak — a failing indicator returns ``{"status": "DOWN"}`` instead of
    crashing the entire health endpoint.

    Both sync and async ``_check()`` implementations are supported::

        class MyIndicator(BaseHealthIndicator):
            _name = "myService"

            def _check(self) -> dict[str, Any]:
                return {"status": "UP"}

        class MyAsyncIndicator(BaseHealthIndicator):
            _name = "myAsyncService"

            async def _check(self) -> dict[str, Any]:
                result = await some_client.ping()
                return {"status": "UP", "details": result}
    """

    _name: str = "unknown"

    def _check(self) -> dict[str, Any]:
        """Override to perform the actual health check."""
        raise NotImplementedError

    def health(self) -> dict[str, Any]:
        """Execute ``_check`` and catch any exception.

        Returns a well-formed health dict in every case.  For async
        ``_check`` implementations, returns a coroutine that the plugin's
        ``_evaluate_indicator`` will ``await`` — the wrapper coroutine
        still catches exceptions internally.
        """
        try:
            result = self._check()
            if inspect.iscoroutine(result):
                return self._await_check(result)  # type: ignore[return-value]
            return result
        except Exception:
            logger.exception("Health indicator '%s' raised unexpectedly", self._name)
            return {"status": "DOWN", "details": {"error": "Health check failed"}}

    async def _await_check(self, coro) -> dict[str, Any]:  # type: ignore[override]
        """Await an async ``_check`` with the same exception safety."""
        try:
            result = await coro
            return dict(result)
        except Exception:
            logger.exception("Health indicator '%s' raised unexpectedly", self._name)
            return {"status": "DOWN", "details": {"error": "Health check failed"}}


class PingHealthIndicator(BaseHealthIndicator):
    """Always-UP indicator confirming the process is alive."""

    _name = "ping"

    def _check(self) -> dict[str, Any]:
        return {"status": "UP"}


class LivenessIndicator(BaseHealthIndicator):
    """Kubernetes liveness probe — UP while the process is running."""

    _name = "livenessState"

    def _check(self) -> dict[str, Any]:
        return {"status": "UP"}


class ReadinessIndicator(BaseHealthIndicator):
    """Kubernetes readiness probe — UP when the service can accept traffic."""

    _name = "readinessState"

    def _check(self) -> dict[str, Any]:
        return {"status": "UP"}


class DiskSpaceHealthIndicator(BaseHealthIndicator):
    """Reports disk space availability.

    Args:
        path: Filesystem path to check (default ``"."``).
        threshold: Minimum free bytes before status becomes DOWN
            (default 10 MB, matching Spring Boot).
    """

    _name = "diskSpace"

    def __init__(self, path: str = ".", threshold: int = 10_485_760) -> None:
        self._path = path
        self._threshold = threshold

    def _check(self) -> dict[str, Any]:
        usage = shutil.disk_usage(self._path)
        status = "UP" if usage.free >= self._threshold else "DOWN"
        return {
            "status": status,
            "details": {
                "total": usage.total,
                "free": usage.free,
                "threshold": self._threshold,
                "path": self._path,
                "exists": True,
            },
        }
