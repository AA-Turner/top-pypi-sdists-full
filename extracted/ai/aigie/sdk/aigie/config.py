"""
Configuration management for Aigie SDK.

Enhanced with:
- Logging verbosity control
- Query API configuration
"""

import logging
import os
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from aigie._grpc import data_path_grpc_target

if TYPE_CHECKING:
    from aigie.telemetry._config import TelemetryConfig


# License server URL (Aigie's licensing server).
LICENSE_SERVER_URL: str = os.getenv("AIGIE_LICENSE_SERVER", "https://portal.aigie.io/api")


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

    # Logging Configuration
    log_level: str = "WARNING"

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

    # Skip license validation (offline/CI escape hatch). When set, license
    # validation no-ops gracefully so the SDK works without reaching the
    # licensing server.
    skip_license_validation: bool = field(
        default_factory=lambda: (
            os.getenv("AIGIE_SKIP_LICENSE_VALIDATION", "false").lower() == "true"
        )
    )

    # =========================================================================
    # Internal — derived, not part of the public/config surface
    # =========================================================================

    # Derived from aigie_url in __post_init__ (host + gRPC port 50051). When
    # set, finalized spans (SPAN_UPDATE) are sent over gRPC to
    # kytte.ingest.v1.IngestService; other event types stay on HTTP.
    kytte_grpc_url: str | None = field(default=None, init=False)
    # Derived from aigie_url's scheme in __post_init__: https → TLS (gRPC rides
    # the TLS front), http → plaintext (in-cluster traffic).
    kytte_grpc_use_tls: bool = field(default=False, init=False)
    # Derived from aigie_url in __post_init__ (host + decision gRPC port 50052).
    kytte_decision_grpc_url: str | None = field(default=None, init=False)

    # Auto-derived unique installation ID (off the config surface).
    installation_id: str | None = field(
        default_factory=lambda: os.getenv("AIGIE_INSTALLATION_ID"), init=False
    )

    # Internal OTel telemetry configuration (driven from TelemetryConfig.from_env()).
    internal_telemetry: "TelemetryConfig" = field(
        default_factory=_make_default_telemetry_config, init=False
    )

    def __post_init__(self):
        """Normalize configuration values and derive internal targets."""
        from aigie._grpc import _DEFAULT_DECISION_GRPC_PORT, grpc_uses_tls

        # Ensure API URL doesn't end with /
        self.aigie_url = self.aigie_url.rstrip("/")

        # https → gRPC over TLS on the shared front; http → in-cluster plaintext.
        self.kytte_grpc_use_tls = grpc_uses_tls(self.aigie_url)

        if not self.kytte_grpc_url and self.aigie_url:
            self.kytte_grpc_url = data_path_grpc_target(self.aigie_url) or None

        # Decision Orchestrator target (Determine Error MVP): same host, fixed
        # decision port (or the shared TLS front for https).
        if not self.kytte_decision_grpc_url and self.aigie_url:
            self.kytte_decision_grpc_url = (
                data_path_grpc_target(self.aigie_url, default_port=_DEFAULT_DECISION_GRPC_PORT)
                or None
            )

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
        """Get the authentication token for API calls."""
        return self.aigie_token or None

    @property
    def license_server_url(self) -> str:
        """License server URL (module constant)."""
        return LICENSE_SERVER_URL

    def validate_self_hosted(self) -> list[str]:
        """
        Validate configuration for self-hosted deployments.

        Returns:
            List of validation warnings/errors (empty if valid)
        """
        warnings = []

        # Check for HTTP (not HTTPS) in non-localhost URLs
        if self.aigie_url.startswith("http://"):
            is_local = any(
                host in self.aigie_url
                for host in ["localhost", "127.0.0.1", "0.0.0.0"]  # noqa: S104 — URL substring check, not a bind address
            )
            if not is_local:
                warnings.append(
                    f"API URL uses HTTP instead of HTTPS: {self.aigie_url}. "
                    "This is insecure for production deployments."
                )

        # Check license server URL security
        if self.license_server_url.startswith("http://"):
            is_local = any(
                host in self.license_server_url
                for host in ["localhost", "127.0.0.1", "0.0.0.0"]  # noqa: S104 — URL substring check, not a bind address
            )
            if not is_local:
                warnings.append(
                    f"License server URL uses HTTP instead of HTTPS: {self.license_server_url}. "
                    "This is insecure for production deployments."
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
