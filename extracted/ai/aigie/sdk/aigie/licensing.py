"""
License validation module for Aigie SDK.

Validates license keys with the Kytte licensing server and
reports usage telemetry from self-hosted installations.
"""

import asyncio
import contextlib
import logging
import platform
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx

from .diagnostics import A004, R005, format_diagnostic

logger = logging.getLogger(__name__)


class LicenseError(Exception):
    """Raised when license validation fails."""

    pass


class LicenseExpiredError(LicenseError):
    """Raised when license has expired."""

    pass


class LicenseRevokedError(LicenseError):
    """Raised when license has been revoked."""

    pass


class LicenseLimitExceededError(LicenseError):
    """Raised when license limits are exceeded."""

    pass


@dataclass
class LicenseInfo:
    """License information returned from validation."""

    valid: bool
    tier: str | None = None
    max_seats: int = 0
    max_traces_per_month: int = 0
    max_projects: int = 0
    features: dict[str, bool] = field(default_factory=dict)
    expires_at: datetime | None = None
    error: str | None = None

    @property
    def is_unlimited(self) -> bool:
        """Check if license has unlimited limits (enterprise)."""
        return self.max_traces_per_month < 0


@dataclass
class UsageSummary:
    """Current usage summary."""

    traces_this_month: int = 0
    traces_remaining: int = -1
    spans_this_month: int = 0
    active_users: int = 0
    api_calls_this_month: int = 0


@dataclass
class UsageMetrics:
    """Usage metrics to report."""

    traces_count: int = 0
    spans_count: int = 0
    active_users: int = 0
    api_calls: int = 0


@dataclass
class ErrorInfo:
    """Error information for reporting."""

    error_type: str
    count: int = 1
    message: str | None = None


class FeatureTracker:
    """
    Tracks which SDK features are being used.

    Features are automatically tracked when used and reported
    in heartbeats to help understand SDK adoption.
    """

    KNOWN_FEATURES = [
        "tracing",  # Basic tracing (trace/span)
        "auto_instrument",  # Auto-instrumentation
        "langchain",  # LangChain integration
        "langgraph",  # LangGraph integration
        "cost_tracking",  # Cost tracking
        "evaluation",  # Evaluation/scoring
        "datasets",  # Dataset management
        "experiments",  # A/B experiments
        "sessions",  # Session tracking
        "annotations",  # Human annotations
        "prompts",  # Prompt management
        "streaming",  # Streaming support
        "playground",  # Playground features
        "rules",  # Rules engine
        "alerting",  # Alerting
        "drift",  # Drift detection
        "remediation",  # Auto-remediation
        "judge",  # LLM-as-Judge
        "realtime",  # Real-time features
    ]

    def __init__(self):
        self._features_used: set[str] = set()

    def track(self, feature: str):
        """Track a feature as used."""
        self._features_used.add(feature)

    def get_features(self) -> list[str]:
        """Get list of features that have been used."""
        return list(self._features_used)

    def clear(self):
        """Clear tracked features."""
        self._features_used.clear()


class ErrorCollector:
    """
    Collects errors encountered during SDK operation.

    Errors are aggregated and reported in heartbeats to help
    identify common issues across installations.
    """

    MAX_ERRORS = 100  # Max errors to keep in memory

    def __init__(self):
        self._errors: dict[str, ErrorInfo] = {}

    def record(self, error_type: str, message: str | None = None):
        """Record an error occurrence."""
        if error_type in self._errors:
            self._errors[error_type].count += 1
            if message:
                self._errors[error_type].message = message
        elif len(self._errors) < self.MAX_ERRORS:
            self._errors[error_type] = ErrorInfo(
                error_type=error_type,
                count=1,
                message=message,
            )

    def get_errors(self) -> list[dict[str, Any]]:
        """Get error summary for reporting."""
        return [
            {
                "type": e.error_type,
                "count": e.count,
                "message": e.message,
            }
            for e in self._errors.values()
        ]

    def clear(self):
        """Clear collected errors."""
        self._errors.clear()


# Global feature tracker and error collector
_feature_tracker = FeatureTracker()
_error_collector = ErrorCollector()


def track_feature(feature: str):
    """Track a feature as used (called by SDK components)."""
    _feature_tracker.track(feature)


def record_error(error_type: str, message: str | None = None):
    """Record an error (called by SDK components)."""
    _error_collector.record(error_type, message)


def _sanitize_error(e: Exception) -> str:
    """Summarize an error for customer-facing logs WITHOUT leaking internal URLs.

    str(httpx errors) embeds the full request URL (our internal licensing
    service) and MDN links. Customers should only ever see the status code
    or the error class.
    """
    status = getattr(getattr(e, "response", None), "status_code", None)
    if status is not None:
        return f"HTTP {status}"
    return type(e).__name__


class LicenseValidator:
    """
    Validates Aigie tokens with the Aigie licensing server.

    Usage:
        validator = LicenseValidator(
            aigie_token="kytte_lic_pro_xxx"
        )
        license_info = await validator.validate()
        if not license_info.valid:
            raise LicenseError(license_info.error)

    Or simply set AIGIE_TOKEN environment variable and use the SDK.
    """

    DEFAULT_LICENSE_SERVER = "https://portal.aigie.io/api"
    CACHE_TTL = 3600  # 1 hour cache for valid licenses
    HEARTBEAT_INTERVAL = 3600  # 1 hour between heartbeats
    USAGE_REPORT_INTERVAL = 86400  # 24 hours between usage reports

    def __init__(
        self,
        aigie_token: str,
        license_server_url: str | None = None,
        installation_id: str | None = None,
        enable_telemetry: bool = True,
        # Backwards compatibility
        license_key: str | None = None,
    ):
        """
        Initialize the license validator.

        Args:
            aigie_token: Your Aigie token (get one at https://app.aigie.io)
            license_server_url: URL of the licensing server (uses default if not provided)
            installation_id: Unique ID for this installation (auto-generated if not provided)
            enable_telemetry: Whether to report usage telemetry
            license_key: Deprecated, use aigie_token instead
        """
        # Support both aigie_token and legacy license_key
        self.aigie_token = aigie_token or license_key
        if not self.aigie_token:
            raise ValueError("aigie_token is required")
        self.license_server_url = (license_server_url or self.DEFAULT_LICENSE_SERVER).rstrip("/")
        self.installation_id = installation_id or self._generate_installation_id()
        self.enable_telemetry = enable_telemetry

        # Cached license info
        self._license_info: LicenseInfo | None = None
        self._usage_summary: UsageSummary | None = None
        self._cache_expires_at: datetime | None = None

        # Background tasks
        self._heartbeat_task: asyncio.Task | None = None
        self._usage_report_task: asyncio.Task | None = None

        # Usage tracking
        self._local_usage = UsageMetrics()

        # HTTP client
        self._client: httpx.AsyncClient | None = None

    def _generate_installation_id(self) -> str:
        """Generate a unique installation ID."""
        # Use a combination of machine info and random UUID
        try:
            machine_id = platform.node()
        except Exception:
            machine_id = "unknown"
        return f"{machine_id}-{uuid.uuid4().hex[:8]}"

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=30.0,
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": self.aigie_token,
                },
            )
        return self._client

    async def close(self):
        """Close the validator and stop background tasks."""
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._heartbeat_task

        if self._usage_report_task:
            self._usage_report_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._usage_report_task

        if self._client:
            await self._client.aclose()
            self._client = None

    async def validate(self, force: bool = False) -> LicenseInfo:
        """
        Validate the license key with the licensing server.

        Args:
            force: Force validation even if cached

        Returns:
            LicenseInfo with validation result

        Raises:
            LicenseError: If license is invalid
            LicenseExpiredError: If license has expired
            LicenseRevokedError: If license has been revoked
        """
        # Check cache
        if not force and self._is_cache_valid():
            return self._license_info

        client = await self._get_client()

        try:
            response = await client.post(
                f"{self.license_server_url}/v1/licenses/validate",
                json={
                    "license_key": self.aigie_token,
                    "installation_id": self.installation_id,
                },
            )
            response.raise_for_status()
            data = response.json()

            if not data.get("valid"):
                error = data.get("error", "License validation failed")
                if "expired" in error.lower():
                    raise LicenseExpiredError(error)
                if "revoked" in error.lower():
                    raise LicenseRevokedError(error)
                raise LicenseError(error)

            # Parse license info
            license_data = data.get("license", {})
            expires_at = None
            if license_data.get("expires_at"):
                with contextlib.suppress(Exception):
                    expires_at = datetime.fromisoformat(
                        license_data["expires_at"].replace("Z", "+00:00")
                    )

            self._license_info = LicenseInfo(
                valid=True,
                tier=license_data.get("tier"),
                max_seats=license_data.get("max_seats", 0),
                max_traces_per_month=license_data.get("max_traces_per_month", 0),
                max_projects=license_data.get("max_projects", 0),
                features=license_data.get("features", {}),
                expires_at=expires_at,
            )

            # Parse usage summary
            usage_data = data.get("usage", {})
            self._usage_summary = UsageSummary(
                traces_this_month=usage_data.get("traces_this_month", 0),
                traces_remaining=usage_data.get("traces_remaining", -1),
                spans_this_month=usage_data.get("spans_this_month", 0),
                active_users=usage_data.get("active_users", 0),
                api_calls_this_month=usage_data.get("api_calls_this_month", 0),
            )

            # Update cache
            self._cache_expires_at = datetime.now(timezone.utc) + timedelta(seconds=self.CACHE_TTL)

            logger.info(f"License validated: tier={self._license_info.tier}")
            return self._license_info

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 402:
                raise LicenseExpiredError("License expired or payment required") from e
            if e.response.status_code == 404:
                raise LicenseError(
                    "License validation service unavailable. Contact support@aigie.io"
                ) from e
            raise LicenseError(f"License validation failed (HTTP {e.response.status_code})") from e
        except (httpx.RequestError, httpx.TimeoutException) as e:
            # Network error - check if we have cached info
            if self._license_info and self._license_info.valid:
                logger.warning(format_diagnostic(A004, extra=_sanitize_error(e)))
                return self._license_info
            raise LicenseError(
                "Unable to reach license validation service. "
                "Check your network connection or contact support@aigie.io"
            ) from e

    def _is_cache_valid(self) -> bool:
        """Check if cached license info is still valid."""
        if not self._license_info or not self._cache_expires_at:
            return False
        return datetime.now(timezone.utc) < self._cache_expires_at

    async def check_feature(self, feature: str) -> bool:
        """
        Check if a feature is available in the current license.

        Args:
            feature: Feature name to check

        Returns:
            True if feature is available
        """
        if not self._license_info:
            await self.validate()

        return self._license_info.features.get(feature, False)

    def is_within_limits(self, metric: str, value: int) -> bool:
        """
        Check if a usage metric is within license limits.

        Args:
            metric: Metric name (e.g., "traces", "seats", "projects")
            value: Current value

        Returns:
            True if within limits
        """
        if not self._license_info:
            return False

        limits = {
            "traces": self._license_info.max_traces_per_month,
            "seats": self._license_info.max_seats,
            "projects": self._license_info.max_projects,
        }

        limit = limits.get(metric, 0)
        if limit < 0:  # Unlimited
            return True

        return value <= limit

    def track_usage(
        self,
        traces: int = 0,
        spans: int = 0,
        api_calls: int = 0,
    ):
        """
        Track local usage for periodic reporting.

        Args:
            traces: Number of traces created
            spans: Number of spans created
            api_calls: Number of API calls made
        """
        self._local_usage.traces_count += traces
        self._local_usage.spans_count += spans
        self._local_usage.api_calls += api_calls

    async def report_usage(self) -> bool:
        """
        Report accumulated usage to the licensing server.

        Returns:
            True if report was successful
        """
        if not self.enable_telemetry:
            return True

        if (
            self._local_usage.traces_count == 0
            and self._local_usage.spans_count == 0
            and self._local_usage.api_calls == 0
        ):
            return True

        client = await self._get_client()

        try:
            response = await client.post(
                f"{self.license_server_url}/v1/licenses/usage",
                json={
                    "license_key": self.aigie_token,
                    "installation_id": self.installation_id,
                    "metrics": {
                        "traces_count": self._local_usage.traces_count,
                        "spans_count": self._local_usage.spans_count,
                        "active_users": self._local_usage.active_users,
                        "api_calls": self._local_usage.api_calls,
                    },
                    "sdk_version": self._get_sdk_version(),
                    "python_version": platform.python_version(),
                },
            )
            response.raise_for_status()

            # Reset local usage after successful report
            self._local_usage = UsageMetrics()
            logger.debug("Usage report sent successfully")
            return True

        except Exception as e:
            logger.debug(format_diagnostic(R005, extra=_sanitize_error(e)))
            return False

    async def send_heartbeat(self) -> bool:
        """
        Send enhanced heartbeat to licensing server.

        Includes feature usage, session metrics, and errors.

        Returns:
            True if heartbeat was successful
        """
        client = await self._get_client()

        try:
            # Build enhanced heartbeat payload
            payload = {
                "license_key": self.aigie_token,
                "installation_id": self.installation_id,
                "sdk_version": self._get_sdk_version(),
                "python_version": platform.python_version(),
                "platform": platform.system(),
                # Feature usage
                "features_used": _feature_tracker.get_features(),
                # Session metrics
                "session_traces": self._local_usage.traces_count,
                "session_tokens": 0,  # TODO: Track tokens in SDK
                "session_cost": 0.0,  # TODO: Track cost in SDK
                # Errors
                "errors": _error_collector.get_errors(),
            }

            response = await client.post(
                f"{self.license_server_url}/v1/telemetry/heartbeat",
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

            status = data.get("status")
            if status == "revoked":
                raise LicenseRevokedError("License has been revoked")
            if status == "expired":
                raise LicenseExpiredError("License has expired")
            if status == "invalid":
                raise LicenseError(data.get("message", "Invalid license key"))

            # Update features and limits from heartbeat response
            if self._license_info:
                self._license_info.features = data.get("features", self._license_info.features)
                # Update limits
                limits = data.get("limits", {})
                if limits:
                    self._license_info.max_seats = limits.get(
                        "max_seats", self._license_info.max_seats
                    )
                    self._license_info.max_traces_per_month = limits.get(
                        "max_traces_per_month", self._license_info.max_traces_per_month
                    )
                    self._license_info.max_projects = limits.get(
                        "max_projects", self._license_info.max_projects
                    )

            # Clear tracked data after successful heartbeat
            _feature_tracker.clear()
            _error_collector.clear()

            logger.debug("Enhanced heartbeat sent successfully")
            return True

        except (LicenseRevokedError, LicenseExpiredError, LicenseError):
            raise
        except Exception as e:
            logger.debug(format_diagnostic(R005, extra=_sanitize_error(e)))
            # Record the heartbeat failure as an error for next time
            _error_collector.record("heartbeat_failed", str(e))
            return False

    async def start_background_tasks(self):
        """Start background tasks for heartbeat and usage reporting."""
        if self._heartbeat_task is None:
            self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())

        if self._usage_report_task is None and self.enable_telemetry:
            self._usage_report_task = asyncio.create_task(self._usage_report_loop())

    async def _heartbeat_loop(self):
        """Background loop for sending heartbeats."""
        while True:
            try:
                await self.send_heartbeat()
                await asyncio.sleep(self.HEARTBEAT_INTERVAL)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.debug(format_diagnostic(R005, extra=_sanitize_error(e)))
                await asyncio.sleep(self.HEARTBEAT_INTERVAL)

    async def _usage_report_loop(self):
        """Background loop for reporting usage."""
        while True:
            try:
                await asyncio.sleep(self.USAGE_REPORT_INTERVAL)
                await self.report_usage()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.debug(format_diagnostic(R005, extra=_sanitize_error(e)))

    def _get_sdk_version(self) -> str:
        """Get the SDK version."""
        try:
            from . import __version__

            return __version__
        except Exception:
            return "unknown"

    @property
    def license_info(self) -> LicenseInfo | None:
        """Get cached license info."""
        return self._license_info

    @property
    def usage_summary(self) -> UsageSummary | None:
        """Get cached usage summary."""
        return self._usage_summary

    @property
    def tier(self) -> str | None:
        """Get license tier."""
        return self._license_info.tier if self._license_info else None

    @property
    def features(self) -> dict[str, bool]:
        """Get available features."""
        return self._license_info.features if self._license_info else {}
