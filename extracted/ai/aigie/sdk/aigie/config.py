"""
Configuration management for Aigie SDK.

Enhanced with:
- Data masking support for PII protection
- Debug mode with detailed logging
- I/O capture control defaults
- Query API configuration
"""

import logging
import os
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from aigie.telemetry._config import TelemetryConfig


def _make_default_telemetry_config() -> "TelemetryConfig":
    from aigie.telemetry._config import TelemetryConfig
    return TelemetryConfig.from_env()


@dataclass
class Config:
    """
    Configuration for Aigie SDK.

    Usage:
        config = Config(
            aigie_url="https://portal.aigie.io/api",
            aigie_token="your-token",  # Required for data to be sent
            batch_size=100,
            flush_interval=5.0
        )
        aigie = Aigie(config=config)

    Authentication:
        The aigie_token is REQUIRED for data to be sent to the platform.
        Without a valid token, traces will not be sent (security measure).
        Set via AIGIE_TOKEN environment variable or pass directly.
    """

    # API Configuration
    # aigie_url is the primary URL field for the Aigie API
    aigie_url: str = field(
        default_factory=lambda: os.getenv(
            "KYTTE_URL", os.getenv("AIGIE_URL", os.getenv("AIGIE_API_URL", ""))
        )
    )

    # DEPRECATED: Use aigie_url instead. Kept for backward compatibility.
    api_url: str = field(default_factory=lambda: "")

    # DEPRECATED: Use aigie_token instead. Kept for backward compatibility.
    api_key: str = field(default_factory=lambda: os.getenv("AIGIE_API_KEY", ""))

    # Buffering Configuration
    enable_buffering: bool = True
    batch_size: int = 100
    flush_interval: float = 5.0  # seconds

    # Retry Configuration
    max_retries: int = 3
    retry_delay: float = 1.0  # base delay in seconds
    exponential_backoff: bool = True

    # HTTP Configuration
    timeout: float = 30.0
    connect_timeout: float = 5.0  # TCP connect timeout — fail fast on unreachable backends
    max_connections: int = 10

    # OpenTelemetry Configuration
    enable_otel: bool = False
    otel_service_name: str | None = None

    # Logging Configuration
    log_level: str = "INFO"
    enable_debug: bool = False

    # Advanced Configuration
    enable_circuit_breaker: bool = True
    circuit_breaker_threshold: int = 5  # failures before opening
    circuit_breaker_timeout: float = 60.0  # seconds before retry

    # Compression Configuration
    enable_compression: bool = field(
        default_factory=lambda: os.getenv("AIGIE_ENABLE_COMPRESSION", "true").lower() == "true"
    )
    compression_algorithm: str = field(
        default_factory=lambda: os.getenv("AIGIE_COMPRESSION_ALGORITHM", "zstd")
    )
    compression_level: int | None = field(
        default_factory=lambda: (
            int(os.getenv("AIGIE_COMPRESSION_LEVEL", "1"))
            if os.getenv("AIGIE_COMPRESSION_LEVEL")
            else 1
        )
    )

    # Sampling Configuration
    sampling_rate: float | None = field(
        default_factory=lambda: (
            float(os.getenv("AIGIE_SAMPLING_RATE")) if os.getenv("AIGIE_SAMPLING_RATE") else None
        )
    )

    # Auto-Instrumentation Configuration
    enable_auto_instrument: bool = field(
        default_factory=lambda: (
            os.getenv("AIGIE_AUTO_INSTRUMENT", "true").lower() not in ("false", "0", "no")
        )
    )
    disable_auto_instrument: bool = field(
        default_factory=lambda: (
            os.getenv("AIGIE_DISABLE_AUTO_INSTRUMENT", "false").lower() in ("true", "1", "yes")
        )
    )

    # Data Masking Configuration
    # Function to mask sensitive data before sending to API
    mask: Callable[[dict[str, Any]], dict[str, Any]] | None = None

    # =========================================================================
    # Sensitive Data Scrubbing Configuration
    # =========================================================================
    # Automatic scrubbing of API keys, passwords, tokens from traces/spans
    # Enabled by default for security - set to False only for debugging

    # Enable/disable automatic sensitive data scrubbing
    scrubbing_enabled: bool = field(
        default_factory=lambda: os.getenv("AIGIE_SCRUBBING_ENABLED", "true").lower() == "true"
    )

    # Custom regex patterns to scrub (in addition to defaults)
    scrubbing_custom_patterns: list[str] = field(default_factory=list)

    # Custom field names to always scrub (in addition to defaults)
    scrubbing_custom_fields: list[str] = field(default_factory=list)

    # Character to use for masking (default: *)
    scrubbing_mask_char: str = field(
        default_factory=lambda: os.getenv("AIGIE_SCRUBBING_MASK_CHAR", "*")
    )

    # Default I/O Capture Control
    # Can be overridden per-decorator
    default_capture_input: bool = field(
        default_factory=lambda: os.getenv("AIGIE_CAPTURE_INPUT", "true").lower() == "true"
    )
    default_capture_output: bool = field(
        default_factory=lambda: os.getenv("AIGIE_CAPTURE_OUTPUT", "true").lower() == "true"
    )

    # Debug Mode
    debug: bool = field(
        default_factory=lambda: os.getenv("AIGIE_DEBUG", "false").lower() in ("true", "1", "yes")
    )

    # Blocked Instrumentation Scopes
    # List of instrumentation scope names to exclude from tracing
    blocked_instrumentation_scopes: list[str] = field(default_factory=list)

    # NEW: User/Session Defaults
    default_user_id: str | None = field(default_factory=lambda: os.getenv("AIGIE_DEFAULT_USER_ID"))
    default_session_id: str | None = field(
        default_factory=lambda: os.getenv("AIGIE_DEFAULT_SESSION_ID")
    )

    # NEW: Environment/Release Configuration
    environment: str | None = field(
        default_factory=lambda: os.getenv("AIGIE_ENVIRONMENT") or os.getenv("ENVIRONMENT")
    )
    release: str | None = field(
        default_factory=lambda: os.getenv("AIGIE_RELEASE") or os.getenv("RELEASE")
    )

    # =========================================================================
    # Autonomous Runtime — ONE toggle for everything autonomous
    # =========================================================================
    #
    # `autonomous` is the single source of truth. When True (default), the SDK
    # creates the interceptor chain, installs framework adapters, binds the
    # autonomous runtime hook, and routes LLM errors through the chain so
    # interventions like RetryIntervention can fire end-to-end.
    #
    # `enable_interception` is kept as a derived, read-only property for
    # backwards-compatible internal callers. Do NOT set it directly.
    #
    # Legacy `AIGIE_AUTONOMOUS_DISABLE=1` env var is honored as a kill-switch
    # (BC shim). A one-line deprecation log fires once at config build time.
    autonomous: bool = field(
        default_factory=lambda: os.environ.get("AIGIE_AUTONOMOUS_DISABLE") != "1"
    )

    @property
    def enable_interception(self) -> bool:
        """Derived from `autonomous`. Kept for backwards compatibility — do not set directly."""
        return self.autonomous

    @enable_interception.setter
    def enable_interception(self, value: bool) -> None:  # pragma: no cover - BC shim only
        # Allow legacy code paths (and platform mode responses) to flip the
        # autonomous toggle through the old name. Logging is intentionally
        # absent here to avoid noise on every set.
        self.autonomous = bool(value)

    # Timeout for local hook execution (milliseconds)
    local_decision_timeout_ms: float = field(
        default_factory=lambda: float(os.getenv("AIGIE_LOCAL_DECISION_TIMEOUT_MS", "5"))
    )

    # Timeout for backend consultation (milliseconds)
    backend_consultation_timeout_ms: float = field(
        default_factory=lambda: float(os.getenv("AIGIE_BACKEND_CONSULTATION_TIMEOUT_MS", "500"))
    )

    # Cost limit per trace (None = no limit)
    cost_limit_per_trace: float | None = field(
        default_factory=lambda: (
            float(os.getenv("AIGIE_COST_LIMIT_PER_TRACE"))
            if os.getenv("AIGIE_COST_LIMIT_PER_TRACE")
            else None
        )
    )

    # Cost limit per request (None = no limit)
    cost_limit_per_request: float | None = field(
        default_factory=lambda: (
            float(os.getenv("AIGIE_COST_LIMIT_PER_REQUEST"))
            if os.getenv("AIGIE_COST_LIMIT_PER_REQUEST")
            else None
        )
    )

    # Token limit per request (None = no limit)
    token_limit_per_request: int | None = field(
        default_factory=lambda: (
            int(os.getenv("AIGIE_TOKEN_LIMIT_PER_REQUEST"))
            if os.getenv("AIGIE_TOKEN_LIMIT_PER_REQUEST")
            else None
        )
    )

    # Drift detection threshold (0.0-1.0, higher = more sensitive)
    drift_threshold: float = field(
        default_factory=lambda: float(os.getenv("AIGIE_DRIFT_THRESHOLD", "0.7"))
    )

    # Enable automatic drift detection
    enable_drift_detection: bool = field(
        default_factory=lambda: os.getenv("AIGIE_ENABLE_DRIFT_DETECTION", "false").lower() == "true"
    )

    # Blocked patterns (regex patterns to block in requests)
    blocked_patterns: list[str] = field(default_factory=list)

    # Rate limit per minute (None = no limit)
    rate_limit_per_minute: int | None = field(
        default_factory=lambda: (
            int(os.getenv("AIGIE_RATE_LIMIT_PER_MINUTE"))
            if os.getenv("AIGIE_RATE_LIMIT_PER_MINUTE")
            else None
        )
    )

    # Enable automatic fix application from backend
    enable_auto_fix: bool = field(
        default_factory=lambda: os.getenv("AIGIE_ENABLE_AUTO_FIX", "false").lower() == "true"
    )

    # Maximum retry attempts for auto-fix
    auto_fix_max_retries: int = field(
        default_factory=lambda: int(os.getenv("AIGIE_AUTO_FIX_MAX_RETRIES", "2"))
    )

    # =========================================================================
    # Aigie Token Configuration (PRIMARY AUTHENTICATION)
    # =========================================================================
    # IMPORTANT: Token is REQUIRED for data to be sent to the platform.
    # Without a valid token, no data will be transmitted (security measure
    # to prevent unauthorized data injection to the platform).

    # Aigie token for authentication - REQUIRED
    # Set via AIGIE_TOKEN environment variable or pass directly
    aigie_token: str | None = field(
        default_factory=lambda: os.getenv("KYTTE_TOKEN", os.getenv("AIGIE_TOKEN"))
    )

    # License server URL (defaults to Aigie's licensing server)
    license_server_url: str = field(
        default_factory=lambda: os.getenv("AIGIE_LICENSE_SERVER", "https://portal.aigie.io/api")
    )

    # Unique installation ID (auto-generated if not provided)
    installation_id: str | None = field(default_factory=lambda: os.getenv("AIGIE_INSTALLATION_ID"))

    # Enable usage telemetry reporting to license server
    enable_usage_telemetry: bool = field(
        default_factory=lambda: os.getenv("AIGIE_USAGE_TELEMETRY", "true").lower() == "true"
    )

    # Skip license validation (for development/testing)
    skip_license_validation: bool = field(
        default_factory=lambda: (
            os.getenv("AIGIE_SKIP_LICENSE_VALIDATION", "false").lower() == "true"
        )
    )

    # Internal OTel telemetry configuration
    internal_telemetry: "TelemetryConfig" = field(
        default_factory=_make_default_telemetry_config
    )

    def __post_init__(self):
        """Normalize configuration values."""
        # One-line deprecation notice for legacy autonomous kill-switch env var.
        if os.environ.get("AIGIE_AUTONOMOUS_DISABLE") is not None:
            logging.getLogger("aigie").warning(
                "[AIGIE] AIGIE_AUTONOMOUS_DISABLE is deprecated; "
                "set Config(autonomous=False) instead."
            )

        # URL consolidation: if api_url is set but aigie_url uses default, use api_url
        # This provides backward compatibility for users still using api_url
        if self.api_url and self.api_url != "" and not self.aigie_url:
            self.aigie_url = self.api_url
            logging.getLogger("aigie").debug(
                "[AIGIE] Using api_url as aigie_url (api_url is deprecated, use KYTTE_URL instead)"
            )

        # Ensure API URL doesn't end with /
        self.aigie_url = self.aigie_url.rstrip("/")
        # Keep api_url in sync for backward compatibility
        self.api_url = self.aigie_url

        # Token consolidation: if api_key is set but aigie_token is not, use api_key
        # This provides backward compatibility for users still using api_key
        if self.api_key and not self.aigie_token:
            self.aigie_token = self.api_key
            logging.getLogger("aigie").debug(
                "[AIGIE] Using api_key as aigie_token (api_key is deprecated, use AIGIE_TOKEN instead)"
            )

        # Validate batch size
        self.batch_size = max(self.batch_size, 1)
        self.batch_size = min(self.batch_size, 1000)

        # Validate flush interval
        self.flush_interval = max(self.flush_interval, 0.1)
        self.flush_interval = min(self.flush_interval, 60)

        # Configure logging based on debug mode
        if self.debug:
            logging.getLogger("aigie").setLevel(logging.DEBUG)
            # Also set global debug mode for decorators
            from . import decorators_v3

            decorators_v3.set_debug_mode(True)

        # Set global mask function if provided
        if self.mask:
            from . import decorators_v3

            decorators_v3.set_global_mask_fn(self.mask)

    @property
    def is_authenticated(self) -> bool:
        """
        Check if the SDK has a valid authentication token.

        Returns:
            True if aigie_token is set, False otherwise.

        Note:
            Without authentication, no data will be sent to the platform.
            This is a security measure to prevent unauthorized data injection.
        """
        return bool(self.aigie_token)

    def get_auth_token(self) -> str | None:
        """
        Get the authentication token for API calls.

        Returns the aigie_token if set, falls back to api_key for backward compatibility.

        Returns:
            The authentication token, or None if not configured.
        """
        return self.aigie_token or self.api_key or None

    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables."""
        # Parse blocked scopes from comma-separated env var
        blocked_scopes_str = os.getenv("AIGIE_BLOCKED_INSTRUMENTATION_SCOPES", "")
        blocked_scopes = [s.strip() for s in blocked_scopes_str.split(",") if s.strip()]

        return cls(
            aigie_url=os.getenv(
                "KYTTE_URL", os.getenv("AIGIE_URL", os.getenv("AIGIE_API_URL", ""))
            ),
            api_key=os.getenv("AIGIE_API_KEY", ""),
            enable_buffering=os.getenv("AIGIE_ENABLE_BUFFERING", "true").lower() == "true",
            batch_size=int(os.getenv("AIGIE_BATCH_SIZE", "100")),
            flush_interval=float(os.getenv("AIGIE_FLUSH_INTERVAL", "5.0")),
            max_retries=int(os.getenv("AIGIE_MAX_RETRIES", "3")),
            connect_timeout=float(os.getenv("AIGIE_CONNECT_TIMEOUT", "5.0")),
            log_level=os.getenv("AIGIE_LOG_LEVEL", "INFO"),
            enable_debug=os.getenv("AIGIE_DEBUG", "false").lower() == "true",
            # New fields
            debug=os.getenv("AIGIE_DEBUG", "false").lower() in ("true", "1", "yes"),
            default_capture_input=os.getenv("AIGIE_CAPTURE_INPUT", "true").lower() == "true",
            default_capture_output=os.getenv("AIGIE_CAPTURE_OUTPUT", "true").lower() == "true",
            blocked_instrumentation_scopes=blocked_scopes,
            default_user_id=os.getenv("AIGIE_DEFAULT_USER_ID"),
            default_session_id=os.getenv("AIGIE_DEFAULT_SESSION_ID"),
            environment=os.getenv("AIGIE_ENVIRONMENT") or os.getenv("ENVIRONMENT"),
            release=os.getenv("AIGIE_RELEASE") or os.getenv("RELEASE"),
        )

    def validate_self_hosted(self) -> list[str]:
        """
        Validate configuration for self-hosted deployments.

        Returns:
            List of validation warnings/errors (empty if valid)
        """
        warnings = []

        # Check for HTTP (not HTTPS) in non-localhost URLs
        if self.aigie_url.startswith("http://"):
            is_local = any(host in self.aigie_url for host in ["localhost", "127.0.0.1", "0.0.0.0"])
            if not is_local:
                warnings.append(
                    f"API URL uses HTTP instead of HTTPS: {self.aigie_url}. "
                    "This is insecure for production deployments."
                )

        # Check license server URL security
        if self.license_server_url.startswith("http://"):
            is_local = any(
                host in self.license_server_url for host in ["localhost", "127.0.0.1", "0.0.0.0"]
            )
            if not is_local:
                warnings.append(
                    f"License server URL uses HTTP instead of HTTPS: {self.license_server_url}. "
                    "This is insecure for production deployments."
                )

        # Check for sampling rate validity
        if self.sampling_rate is not None and not (0.0 <= self.sampling_rate <= 1.0):
            warnings.append(
                f"Invalid sampling_rate: {self.sampling_rate}. Must be between 0.0 and 1.0."
            )

        return warnings

    def validate_and_warn(self) -> None:
        """
        Validate configuration and log warnings.

        Call this during initialization to get early feedback on configuration issues.
        """
        warnings = self.validate_self_hosted()
        if warnings:
            for warning in warnings:
                logging.getLogger("aigie").warning(f"Configuration warning: {warning}")

    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary (excluding sensitive data)."""
        return {
            "aigie_url": self.aigie_url,
            "api_url": self.api_url,  # Deprecated, kept for backward compatibility
            "enable_buffering": self.enable_buffering,
            "batch_size": self.batch_size,
            "flush_interval": self.flush_interval,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "log_level": self.log_level,
            "enable_debug": self.enable_debug,
            # New fields
            "debug": self.debug,
            "default_capture_input": self.default_capture_input,
            "default_capture_output": self.default_capture_output,
            "blocked_instrumentation_scopes": self.blocked_instrumentation_scopes,
            "environment": self.environment,
            "release": self.release,
            "has_mask_fn": self.mask is not None,
            # Autonomous (interception derives from this)
            "autonomous": self.autonomous,
            "enable_interception": self.enable_interception,
            "local_decision_timeout_ms": self.local_decision_timeout_ms,
            "backend_consultation_timeout_ms": self.backend_consultation_timeout_ms,
            "cost_limit_per_trace": self.cost_limit_per_trace,
            "cost_limit_per_request": self.cost_limit_per_request,
            "token_limit_per_request": self.token_limit_per_request,
            "drift_threshold": self.drift_threshold,
            "enable_drift_detection": self.enable_drift_detection,
            "rate_limit_per_minute": self.rate_limit_per_minute,
            "enable_auto_fix": self.enable_auto_fix,
            "auto_fix_max_retries": self.auto_fix_max_retries,
            # Token fields (mask the token)
            "has_aigie_token": self.aigie_token is not None,
            "license_server_url": self.license_server_url,
            "enable_usage_telemetry": self.enable_usage_telemetry,
            "skip_license_validation": self.skip_license_validation,
        }
