"""
Health Monitor - Backend Degradation Awareness.

This module provides health monitoring capabilities to track backend
degradation state and adjust SDK behavior accordingly.

Health Levels:
- HEALTHY: Backend operating normally
- WARNING: Minor issues, monitoring recommended
- DEGRADED: Reduced functionality, use local fallbacks
- CRITICAL: Severe issues, minimal functionality

Features:
- Query backend degradation status
- Adjust SDK behavior based on backend health
- Automatic fallback to local-only mode when backend degraded
- Health check caching to reduce backend load

Usage:
    from aigie import HealthMonitor, DegradationLevel

    # Initialize health monitor
    monitor = HealthMonitor(api_url=api_url, api_key=api_key)

    # Check backend health
    level = await monitor.get_degradation_level()

    if monitor.is_backend_healthy():
        # Normal operation
        pass
    elif monitor.should_use_local_fallback():
        # Use local-only mode
        pass
"""

import asyncio
import contextlib
import logging
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger("aigie.health")


class DegradationLevel(str, Enum):
    """Backend degradation levels."""

    HEALTHY = "healthy"  # All systems operational
    WARNING = "warning"  # Minor issues, monitoring
    DEGRADED = "degraded"  # Reduced functionality
    CRITICAL = "critical"  # Severe issues
    UNKNOWN = "unknown"  # Unable to determine


class ServiceStatus(str, Enum):
    """Status of individual backend services."""

    UP = "up"
    DOWN = "down"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


@dataclass
class ServiceHealth:
    """Health status of a backend service."""

    service_name: str
    status: ServiceStatus
    latency_ms: float | None = None
    error_rate: float = 0.0
    last_check: datetime = field(default_factory=datetime.utcnow)
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "service_name": self.service_name,
            "status": self.status.value,
            "latency_ms": self.latency_ms,
            "error_rate": self.error_rate,
            "last_check": self.last_check.isoformat(),
            "details": self.details,
        }


@dataclass
class HealthStatus:
    """Overall health status of the backend."""

    level: DegradationLevel
    message: str = ""
    services: list[ServiceHealth] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)

    # Thresholds
    error_budget_remaining: float = 1.0  # 0-1, how much error budget left
    rate_limit_remaining: int | None = None
    queue_depth: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "level": self.level.value,
            "message": self.message,
            "services": [s.to_dict() for s in self.services],
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "error_budget_remaining": self.error_budget_remaining,
            "rate_limit_remaining": self.rate_limit_remaining,
            "queue_depth": self.queue_depth,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HealthStatus":
        services = []
        for svc_data in data.get("services", []):
            services.append(
                ServiceHealth(
                    service_name=svc_data.get("service_name", ""),
                    status=ServiceStatus(svc_data.get("status", "unknown")),
                    latency_ms=svc_data.get("latency_ms"),
                    error_rate=svc_data.get("error_rate", 0.0),
                    details=svc_data.get("details", {}),
                )
            )

        return cls(
            level=DegradationLevel(data.get("level", "unknown")),
            message=data.get("message", ""),
            services=services,
            metadata=data.get("metadata", {}),
            error_budget_remaining=data.get("error_budget_remaining", 1.0),
            rate_limit_remaining=data.get("rate_limit_remaining"),
            queue_depth=data.get("queue_depth"),
        )


@dataclass
class HealthConfig:
    """Configuration for health monitoring."""

    # Check intervals
    check_interval_sec: float = 30.0
    cache_ttl_sec: float = 10.0

    # Thresholds for degradation levels
    warning_error_rate: float = 0.05  # 5% error rate -> WARNING
    degraded_error_rate: float = 0.10  # 10% error rate -> DEGRADED
    critical_error_rate: float = 0.25  # 25% error rate -> CRITICAL

    warning_latency_ms: float = 200.0  # 200ms -> WARNING
    degraded_latency_ms: float = 500.0  # 500ms -> DEGRADED
    critical_latency_ms: float = 1000.0  # 1000ms -> CRITICAL

    # Fallback behavior
    fallback_on_degraded: bool = True
    fallback_on_critical: bool = True
    fallback_on_unknown: bool = False

    # Callbacks
    on_status_change: Callable[[DegradationLevel, DegradationLevel], Awaitable[None]] | None = None


@dataclass
class HealthMetrics:
    """Metrics for health monitoring."""

    checks_performed: int = 0
    checks_successful: int = 0
    checks_failed: int = 0
    cache_hits: int = 0
    status_changes: int = 0
    avg_latency_ms: float = 0.0
    _latency_samples: list[float] = field(default_factory=list)

    def record_check(self, success: bool, latency_ms: float):
        self.checks_performed += 1
        if success:
            self.checks_successful += 1
            self._latency_samples.append(latency_ms)
            if len(self._latency_samples) > 100:
                self._latency_samples.pop(0)
            self.avg_latency_ms = sum(self._latency_samples) / len(self._latency_samples)
        else:
            self.checks_failed += 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "checks_performed": self.checks_performed,
            "checks_successful": self.checks_successful,
            "checks_failed": self.checks_failed,
            "cache_hits": self.cache_hits,
            "status_changes": self.status_changes,
            "avg_latency_ms": self.avg_latency_ms,
        }


class HealthMonitor:
    """
    Monitor backend health and adjust SDK behavior.

    Provides degradation awareness by periodically checking backend
    health and adjusting SDK behavior accordingly. When the backend
    is degraded, the SDK can fall back to local-only operation.

    Features:
    - Periodic health checks
    - Cached health status
    - Automatic fallback detection
    - Status change callbacks
    """

    def __init__(
        self,
        kytte_url: str | None = None,
        kytte_token: str | None = None,
        config: HealthConfig | None = None,
    ):
        """
        Initialize the health monitor.

        Args:
            kytte_url: Kytte platform URL
            kytte_token: Kytte authentication token
            config: Health monitoring configuration
        """
        self._api_url = kytte_url
        self._api_key = kytte_token
        self._config = config or HealthConfig()

        # Current status
        self._current_status: HealthStatus | None = None
        self._last_check: datetime | None = None
        self._previous_level: DegradationLevel | None = None

        # Background task
        self._check_task: asyncio.Task | None = None

        # Metrics
        self._metrics = HealthMetrics()

        # Lock for thread safety
        self._lock = asyncio.Lock()

        # Persistent HTTP session (lazily initialized)
        self._session = None

    async def get_degradation_level(self, force_refresh: bool = False) -> DegradationLevel:
        """
        Get the current backend degradation level.

        Args:
            force_refresh: Force a fresh check, ignoring cache

        Returns:
            Current DegradationLevel
        """
        # Check cache
        if not force_refresh and self._is_cache_valid():
            self._metrics.cache_hits += 1
            return self._current_status.level if self._current_status else DegradationLevel.UNKNOWN

        # Perform health check
        status = await self._check_health()
        return status.level

    async def get_health_status(self, force_refresh: bool = False) -> HealthStatus:
        """
        Get the full health status.

        Args:
            force_refresh: Force a fresh check, ignoring cache

        Returns:
            Current HealthStatus
        """
        if not force_refresh and self._is_cache_valid() and self._current_status:
            self._metrics.cache_hits += 1
            return self._current_status

        return await self._check_health()

    def is_backend_healthy(self) -> bool:
        """
        Check if the backend is currently healthy.

        Returns:
            True if backend is HEALTHY or WARNING level
        """
        if not self._current_status:
            return True  # Assume healthy if no status yet

        return self._current_status.level in (
            DegradationLevel.HEALTHY,
            DegradationLevel.WARNING,
        )

    def is_backend_degraded(self) -> bool:
        """
        Check if the backend is currently degraded.

        Returns:
            True if backend is DEGRADED or CRITICAL level
        """
        if not self._current_status:
            return False

        return self._current_status.level in (
            DegradationLevel.DEGRADED,
            DegradationLevel.CRITICAL,
        )

    def should_use_local_fallback(self) -> bool:
        """
        Check if SDK should use local fallback mode.

        Based on configuration and current degradation level.

        Returns:
            True if local fallback should be used
        """
        if not self._current_status:
            return self._config.fallback_on_unknown

        level = self._current_status.level

        if level == DegradationLevel.CRITICAL:
            return self._config.fallback_on_critical

        if level == DegradationLevel.DEGRADED:
            return self._config.fallback_on_degraded

        if level == DegradationLevel.UNKNOWN:
            return self._config.fallback_on_unknown

        return False

    def get_recommended_timeout_ms(self) -> float:
        """
        Get recommended timeout based on backend health.

        Returns higher timeouts when backend is degraded to
        avoid premature timeouts.

        Returns:
            Recommended timeout in milliseconds
        """
        base_timeout = 100.0  # 100ms base

        if not self._current_status:
            return base_timeout

        multipliers = {
            DegradationLevel.HEALTHY: 1.0,
            DegradationLevel.WARNING: 1.5,
            DegradationLevel.DEGRADED: 2.0,
            DegradationLevel.CRITICAL: 3.0,
            DegradationLevel.UNKNOWN: 1.5,
        }

        multiplier = multipliers.get(self._current_status.level, 1.0)
        return base_timeout * multiplier

    def get_recommended_retry_count(self) -> int:
        """
        Get recommended retry count based on backend health.

        Returns:
            Recommended number of retries
        """
        if not self._current_status:
            return 3

        retry_counts = {
            DegradationLevel.HEALTHY: 3,
            DegradationLevel.WARNING: 2,
            DegradationLevel.DEGRADED: 1,
            DegradationLevel.CRITICAL: 0,  # Don't retry when critical
            DegradationLevel.UNKNOWN: 2,
        }

        return retry_counts.get(self._current_status.level, 3)

    async def _check_health(self) -> HealthStatus:
        """Perform a health check against the backend."""
        start_time = time.perf_counter()

        # If no API URL, return unknown status
        if not self._api_url:
            status = HealthStatus(
                level=DegradationLevel.UNKNOWN,
                message="No API URL configured",
            )
            self._update_status(status)
            return status

        try:
            import aiohttp

            if self._session is None:
                headers = {}
                if self._api_key:
                    headers["Authorization"] = f"Bearer {self._api_key}"
                self._session = aiohttp.ClientSession(
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=5),
                )

            async with self._session.get(
                f"{self._api_url}/v1/health",
            ) as response:
                latency_ms = (time.perf_counter() - start_time) * 1000

                if response.status == 200:
                    data = await response.json()
                    status = HealthStatus.from_dict(data)

                    # If backend doesn't provide level, calculate it
                    if status.level == DegradationLevel.UNKNOWN:
                        status.level = self._calculate_level_from_metrics(
                            latency_ms=latency_ms,
                            error_rate=data.get("error_rate", 0.0),
                        )

                    self._metrics.record_check(True, latency_ms)
                else:
                    status = HealthStatus(
                        level=DegradationLevel.DEGRADED,
                        message=f"Health check returned {response.status}",
                    )
                    self._metrics.record_check(False, latency_ms)

        except ImportError:
            status = HealthStatus(
                level=DegradationLevel.UNKNOWN,
                message="aiohttp not installed",
            )
            self._metrics.record_check(False, 0)

        except asyncio.TimeoutError:
            latency_ms = (time.perf_counter() - start_time) * 1000
            status = HealthStatus(
                level=DegradationLevel.DEGRADED,
                message="Health check timed out",
            )
            self._metrics.record_check(False, latency_ms)

        except Exception as e:
            latency_ms = (time.perf_counter() - start_time) * 1000
            status = HealthStatus(
                level=DegradationLevel.UNKNOWN,
                message=f"Health check failed: {e!s}",
            )
            self._metrics.record_check(False, latency_ms)
            logger.warning(f"Health check failed: {e}")

        self._update_status(status)
        return status

    def _calculate_level_from_metrics(
        self,
        latency_ms: float,
        error_rate: float,
    ) -> DegradationLevel:
        """Calculate degradation level from metrics."""
        # Check error rate first (more important)
        if error_rate >= self._config.critical_error_rate:
            return DegradationLevel.CRITICAL
        if error_rate >= self._config.degraded_error_rate:
            return DegradationLevel.DEGRADED
        if error_rate >= self._config.warning_error_rate:
            return DegradationLevel.WARNING

        # Check latency
        if latency_ms >= self._config.critical_latency_ms:
            return DegradationLevel.CRITICAL
        if latency_ms >= self._config.degraded_latency_ms:
            return DegradationLevel.DEGRADED
        if latency_ms >= self._config.warning_latency_ms:
            return DegradationLevel.WARNING

        return DegradationLevel.HEALTHY

    def _update_status(self, status: HealthStatus) -> None:
        """Update current status and trigger callbacks if changed."""
        old_level = self._current_status.level if self._current_status else None
        new_level = status.level

        self._current_status = status
        self._last_check = datetime.utcnow()

        # Check for status change
        if old_level != new_level and old_level is not None:
            self._metrics.status_changes += 1
            logger.info(f"Backend health changed: {old_level} -> {new_level}")

            # Trigger callback
            if self._config.on_status_change:
                asyncio.create_task(self._safe_callback(old_level, new_level))

    async def _safe_callback(
        self,
        old_level: DegradationLevel,
        new_level: DegradationLevel,
    ) -> None:
        """Safely call the status change callback."""
        try:
            await self._config.on_status_change(old_level, new_level)
        except Exception as e:
            logger.warning(f"Status change callback error: {e}")

    def _is_cache_valid(self) -> bool:
        """Check if cached status is still valid."""
        if not self._last_check or not self._current_status:
            return False

        age = (datetime.utcnow() - self._last_check).total_seconds()
        return age < self._config.cache_ttl_sec

    async def start_monitoring(self) -> None:
        """Start background health monitoring."""
        if self._check_task is None or self._check_task.done():
            self._check_task = asyncio.create_task(self._monitoring_loop())
            logger.info("Started background health monitoring")

    async def stop_monitoring(self) -> None:
        """Stop background health monitoring."""
        if self._check_task and not self._check_task.done():
            self._check_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._check_task
            logger.info("Stopped background health monitoring")

        # Close persistent session
        if self._session:
            await self._session.close()
            self._session = None

    async def _monitoring_loop(self) -> None:
        """Background loop for periodic health checks."""
        while True:
            try:
                await asyncio.sleep(self._config.check_interval_sec)
                await self._check_health()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.warning(f"Health monitoring error: {e}")

    def get_metrics(self) -> HealthMetrics:
        """Get health monitoring metrics."""
        return self._metrics

    def get_stats(self) -> dict[str, Any]:
        """Get health monitor statistics."""
        return {
            **self._metrics.to_dict(),
            "current_level": self._current_status.level.value
            if self._current_status
            else "unknown",
            "is_healthy": self.is_backend_healthy(),
            "should_fallback": self.should_use_local_fallback(),
            "last_check": self._last_check.isoformat() if self._last_check else None,
            "recommended_timeout_ms": self.get_recommended_timeout_ms(),
            "recommended_retry_count": self.get_recommended_retry_count(),
        }

    @property
    def current_level(self) -> DegradationLevel:
        """Get current degradation level without checking."""
        return self._current_status.level if self._current_status else DegradationLevel.UNKNOWN


# Convenience function for global health monitor
_global_monitor: HealthMonitor | None = None


def get_health_monitor() -> HealthMonitor | None:
    """Get the global health monitor instance."""
    return _global_monitor


def set_health_monitor(monitor: HealthMonitor) -> None:
    """Set the global health monitor instance."""
    global _global_monitor
    _global_monitor = monitor
