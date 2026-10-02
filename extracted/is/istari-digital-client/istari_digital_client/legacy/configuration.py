import logging
from pathlib import Path
from dataclasses import field, dataclass
from typing import TypedDict, Literal, Optional, Union

from istari_digital_client.legacy.env import (
    env_bool,
    env_bool_aliased,
    env_int,
    env_str,
    env_cache_root,
)
from istari_digital_client.legacy.auth.identity_service import (
    IdentityServiceClient,
    RetryPolicy,
    validate_credentials_file,
    validate_inline_credentials,
)

BearerAuthSetting = TypedDict(
    "BearerAuthSetting",
    {
        "type": Literal["bearer"],
        "in": Literal["header"],
        "key": Literal["Authorization"],
        "value": str,
    },
)

AuthSettings = TypedDict(
    "AuthSettings",
    {
        "RequestAuthenticator": BearerAuthSetting,
    },
    total=False,
)


@dataclass
class Configuration:
    """
    Client configuration for the Istari Digital SDK.

    This class provides runtime configuration options for the SDK, including registry
    connection settings, retry policies, filesystem cache behavior, logging options,
    and multipart upload settings. Values are loaded from environment variables and
    can be overridden at runtime.

    Most configuration values are optional. Defaults are applied via helper functions
    that read from environment variables with appropriate fallbacks.
    """

    registry_url: Optional[str] = field(
        default_factory=env_str("ISTARI_REGISTRY_URL", default=None)
    )
    digital_api_url: Optional[str] = field(
        default_factory=env_str("ISTARI_DIGITAL_API_URL", default=None)
    )
    """Base URL of the Istari service-router gateway. When set, registry
    traffic is routed through the gateway at ``<digital_api_url>/registry/...``
    and this value wins over ``registry_url``; unset (the default) keeps
    today's direct registry addressing. The trailing slash is optional and is
    normalized where the URL is built.

    The same gateway also fronts the Identity Service: when
    ``identity_service_enabled`` is True, Identity Service traffic is routed to
    ``<digital_api_url>/identity/...`` (see ``_identity_service_base_url``), so
    this single URL is all that is needed to reach both services.
    """
    registry_auth_token: Optional[str] = field(
        default_factory=env_str("ISTARI_REGISTRY_AUTH_TOKEN")
    )
    http_request_timeout_secs: Optional[int] = field(
        default_factory=env_int("ISTARI_CLIENT_HTTP_REQUEST_TIMEOUT_SECS"),
    )
    # === Retry config fields ===
    retry_enabled: Optional[bool] = field(
        default_factory=env_bool("ISTARI_CLIENT_RETRY_ENABLED", default=True)
    )
    retry_max_attempts: Optional[int] = field(
        default_factory=env_int("ISTARI_CLIENT_RETRY_MAX_ATTEMPTS")
    )
    retry_min_interval_millis: Optional[int] = field(
        default_factory=env_int("ISTARI_CLIENT_RETRY_MIN_INTERVAL_MILLIS")
    )
    retry_max_interval_millis: Optional[int] = field(
        default_factory=env_int("ISTARI_CLIENT_RETRY_MAX_INTERVAL_MILLIS")
    )
    # === Filesystem cache config fields ===
    filesystem_cache_enabled: Optional[bool] = field(
        default_factory=env_bool("ISTARI_CLIENT_FILESYSTEM_CACHE_ENABLED", default=True)
    )
    filesystem_cache_root: Path = field(
        default_factory=env_cache_root("ISTARI_CLIENT_FILESYSTEM_CACHE_ROOT")
    )
    filesystem_cache_clean_on_exit: Optional[bool] = field(
        default_factory=env_bool(
            "ISTARI_CLIENT_FILESYSTEM_CACHE_CLEAN_BEFORE_EXIT", default=True
        )
    )
    retry_jitter_enabled: Optional[bool] = field(
        default_factory=env_bool("ISTARI_CLIENT_RETRY_JITTER_ENABLED", default=True)
    )
    # === Multipart upload config fields ===
    multipart_chunksize: Optional[int] = field(
        default_factory=lambda: (
            val if (val := env_int("ISTARI_CLIENT_MULTIPART_CHUNKSIZE")()) is not None
            else 128 * 1024 * 1024
        )
    )

    multipart_threshold: Optional[int] = field(
        default_factory=lambda: (
            val if (val := env_int("ISTARI_CLIENT_MULTIPART_THRESHOLD")()) is not None
            else 2 * 1024 * 1024 * 1024
        )
    )

    # === Direct S3 upload config fields ===
    s3_direct_upload_enabled: Optional[bool] = field(
        default_factory=env_bool("ISTARI_CLIENT_S3_DIRECT_UPLOAD", default=False)
    )
    s3_bucket_name: Optional[str] = field(
        default_factory=env_str("ISTARI_CLIENT_S3_BUCKET_NAME", default=None)
    )

    # === Logging config fields ===
    log_level: Optional[str] = field(
        default_factory=env_str("ISTARI_CLIENT_LOG_LEVEL", default="INFO")
    )
    log_to_file: Optional[bool] = field(
        default_factory=env_bool("ISTARI_CLIENT_LOG_TO_FILE", default=False)
    )
    log_file_path: Optional[str] = field(
        default_factory=env_str("ISTARI_CLIENT_LOG_FILE_PATH", default=None)
    )

    # === Identity Service auth config fields ===
    identity_service_enabled: Optional[bool] = field(
        default_factory=env_bool_aliased(
            [
                "ISTARI_DIGITAL_IDENTITY_SERVICE_ENABLED",
                "ISTARI_CLIENT_IDENTITY_SERVICE_ENABLED",
            ],
            default=False,
        )
    )
    """When True, authenticate to the registry with an auto-refreshed JWT obtained
    from the Identity Service (RFC 7523 private_key_jwt) instead of a fixed PAT.
    Requires ``digital_api_url`` to be set; the Identity Service base URL is
    derived from it (see ``_identity_service_base_url``).

    Read from the shared, cross-client ``ISTARI_DIGITAL_IDENTITY_SERVICE_ENABLED``
    (preferred) or the service-prefixed ``ISTARI_CLIENT_IDENTITY_SERVICE_ENABLED``
    (alias); the shared var wins when both are set, so one platform value can
    enable identity-service auth across every Istari client. Defaults to False."""
    identity_service_secret: Optional[str] = field(
        default_factory=env_str("ISTARI_CLIENT_IDENTITY_SERVICE_SECRET", default=None)
    )
    """Inline credentials: a base64-encoded JSON blob {clientId, keyId, key}
    where key is a PEM-encoded ECDSA P-384 private key."""
    identity_service_secret_file: Optional[Union[str, Path]] = field(
        default_factory=env_str(
            "ISTARI_CLIENT_IDENTITY_SERVICE_SECRET_FILE", default=None
        )
    )
    """Path to a raw JSON credentials file, as a str or Path. Preferred over
    the inline secret when both are set."""

    # === Compatibility config fields ===
    tags: Optional[list[str]] = field(default=None)
    """Endpoint tags this client uses (e.g., ["Agent", "Model"]).

    When set, the SDK sends only the hashes for these tags in the
    X-Istari-Client-Api-Hashes header. When None, all known hashes are sent.
    """

    # === Outbound proxy / TLS trust config fields ===
    proxy_url: Optional[str] = field(
        default_factory=env_str("ISTARI_CLIENT_PROXY_URL", default=None),
        repr=False,  # may embed proxy credentials: keep out of repr/str/logs
    )
    """Forward proxy for outbound HTTP(S) traffic (e.g. ``http://proxy.corp:8080``).
    When set, it overrides the ``HTTP_PROXY``/``HTTPS_PROXY``/``ALL_PROXY``
    environment variables; ``NO_PROXY`` is still honored. Credentials may be
    embedded (``http://<user>:<password>@proxy:8080``) and are sent as a
    ``Proxy-Authorization`` header. Unset (the default), the conventional proxy
    environment variables apply. SOCKS proxies are not supported."""
    ca_bundle: Optional[str] = field(
        default_factory=env_str("ISTARI_CLIENT_CA_BUNDLE", default=None)
    )
    """Path to a PEM CA bundle used to verify TLS server certificates, for
    networks whose proxy terminates and re-signs TLS. Overrides the
    ``REQUESTS_CA_BUNDLE`` and ``SSL_CERT_FILE`` environment variables; unset,
    those are honored in that order. Certificate verification stays required
    either way."""
    trust_env: Optional[bool] = field(
        default_factory=env_bool("ISTARI_CLIENT_TRUST_ENV", default=True)
    )
    """When False, ignore the proxy and CA-bundle environment variables
    (``HTTP_PROXY``, ``HTTPS_PROXY``, ``ALL_PROXY``, ``NO_PROXY``,
    ``REQUESTS_CA_BUNDLE``, ``SSL_CERT_FILE``). The explicit ``proxy_url`` and
    ``ca_bundle`` settings still apply. Defaults to True."""

    # === Date and time formats ===
    datetime_format: str = field(init=False, default="%Y-%m-%dT%H:%M:%S.%f%z")
    date_format: str = field(init=False, default="%Y-%m-%d")

    # Holds the live Identity Service token state when identity_service_enabled. Hidden from
    # init/repr/equality.
    _identity_service_client: Optional[IdentityServiceClient] = field(
        init=False, default=None, repr=False, compare=False
    )

    def __post_init__(self) -> None:
        if self.s3_direct_upload_enabled and not self.s3_bucket_name:
            raise ConfigurationError(
                "ISTARI_CLIENT_S3_BUCKET_NAME must be set when ISTARI_CLIENT_S3_DIRECT_UPLOAD is enabled"
            )

        self._configure_identity_service()
        self._configure_logging()

    def _retry_policy(self) -> RetryPolicy:
        """Build a RetryPolicy for the Identity Service token fetch from the SDK's retry_* knobs."""
        return RetryPolicy(
            enabled=bool(self.retry_enabled),
            max_attempts=(
                int(self.retry_max_attempts)
                if self.retry_max_attempts is not None
                else RetryPolicy.max_attempts
            ),
            min_interval_millis=(
                int(self.retry_min_interval_millis)
                if self.retry_min_interval_millis is not None
                else RetryPolicy.min_interval_millis
            ),
            max_interval_millis=(
                int(self.retry_max_interval_millis)
                if self.retry_max_interval_millis is not None
                else RetryPolicy.max_interval_millis
            ),
            jitter_enabled=bool(self.retry_jitter_enabled),
        )

    def _registry_base_url(self) -> Optional[str]:
        """Derive the gateway-fronted registry base URL from ``digital_api_url``.

        Returns ``<digital_api_url>/registry`` when the service-router gateway is
        configured, mirroring ``_identity_service_base_url``. Returns None when
        ``digital_api_url`` is unset, signalling that the registry is addressed
        directly via ``registry_url`` instead.
        """
        if not self.digital_api_url:
            return None
        return self.digital_api_url.rstrip("/") + "/registry"

    def _identity_service_base_url(self) -> Optional[str]:
        """Derive the Identity Service base URL from ``digital_api_url``.

        The service-router gateway fronts the Identity Service under ``<digital_api_url>/identity``,
        mirroring how the registry is served under ``<digital_api_url>/registry`` (see
        ``_registry_base_url``). Returns None when ``digital_api_url`` is unset.
        """
        if not self.digital_api_url:
            return None
        return self.digital_api_url.rstrip("/") + "/identity"

    def _configure_identity_service(self) -> None:
        """Validate Identity Service config and construct the token client when Identity Service is enabled."""
        if not self.identity_service_enabled:
            return

        identity_service_url = self._identity_service_base_url()
        if not identity_service_url:
            raise ConfigurationError(
                "ISTARI_DIGITAL_API_URL must be set when identity-service auth "
                "is enabled (ISTARI_DIGITAL_IDENTITY_SERVICE_ENABLED)"
            )

        # Prefer the file-based secret if configured; fall back to the inline secret.
        secret = self.identity_service_secret
        if self.identity_service_secret_file:
            secret = str(self.identity_service_secret_file)

        if not secret:
            raise ConfigurationError(
                "ISTARI_CLIENT_IDENTITY_SERVICE_SECRET or "
                "ISTARI_CLIENT_IDENTITY_SERVICE_SECRET_FILE must be set when "
                "identity-service auth is enabled "
                "(ISTARI_DIGITAL_IDENTITY_SERVICE_ENABLED)"
            )

        # Validate credentials on load.
        try:
            if self.identity_service_secret_file:
                validate_credentials_file(Path(self.identity_service_secret_file))
            else:
                validate_inline_credentials(secret)
        except (ValueError, TypeError) as e:
            raise ConfigurationError(f"Invalid Identity Service credentials: {e}") from e

        self._identity_service_client = IdentityServiceClient(
            identity_service_url,
            secret,
            retry_policy=self._retry_policy(),
        )

    def _configure_logging(self) -> None:
        """Configures logging based on the configuration settings."""
        log_level_str = (self.log_level or "INFO").upper()
        log_level = getattr(logging, log_level_str, logging.INFO)

        if not isinstance(log_level, int):
            raise ValueError(f"Invalid log level: {self.log_level}")

        logger = logging.getLogger("istari_digital_client")
        logger.setLevel(log_level)

        formatter = logging.Formatter(
            "%(asctime)s -  %(name)s:%(funcName)s:%(lineno)d - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        handlers: list[logging.Handler] = []

        if self.log_to_file:
            if not self.log_file_path:
                raise ConfigurationError(
                    "ISTARI_CLIENT_LOG_FILE_PATH must be set when ISTARI_CLIENT_LOG_TO_FILE=true"
                )

            log_dir = Path(self.log_file_path).parent
            if not log_dir.exists():
                raise ConfigurationError(
                    f"Directory does not exist for log file: {log_dir}"
                )

            file_handler = logging.FileHandler(self.log_file_path)
            file_handler.setFormatter(formatter)
            handlers.append(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        handlers.append(stream_handler)

        # Reset existing handlers first. _configure_logging runs on every
        # Configuration construction; without this, each new instance stacks
        # another handler on the shared "istari_digital_client" logger and every
        # record is emitted once per accumulated handler.
        for existing in list(logger.handlers):
            logger.removeHandler(existing)
            existing.close()

        for handler in handlers:
            logger.addHandler(handler)

        logger.propagate = False

    def auth_settings(self) -> AuthSettings:
        """Gets Auth Settings dict for api client.

        When the Identity Service is enabled, the bearer value is a live JWT
        obtained (and proactively refreshed) from the Identity Service; otherwise it is the
        fixed registry auth token (PAT).

        :return: The Auth Settings information dict.
        """
        auth: AuthSettings = {}
        bearer_value: Optional[str] = None

        if self._identity_service_client is not None:
            bearer_value = "Bearer " + self._identity_service_client.get_token()
        elif self.registry_auth_token is not None:
            bearer_value = "Bearer " + self.registry_auth_token

        if bearer_value is not None:
            auth["RequestAuthenticator"] = {
                "type": "bearer",
                "in": "header",
                "key": "Authorization",
                "value": bearer_value,
            }
        return auth

    def _invalidate_managed_auth(self) -> bool:
        """Drop any cached, refreshable auth so the next `auth_settings()` re-fetches.

        Returns `True` if there was a refreshable token to clear, or `False`
        for static credentials (e.g. a PAT), which have nothing to drop.
        """
        if self._identity_service_client is None:
            return False
        self._identity_service_client.invalidate()
        return True


class ConfigurationError(ValueError):
    pass
