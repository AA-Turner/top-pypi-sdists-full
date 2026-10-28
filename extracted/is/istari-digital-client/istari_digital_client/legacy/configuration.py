import os
import logging
from pathlib import Path
from dataclasses import field, dataclass
from typing import TypedDict, Literal, Optional, Union, cast

from istari_digital_client.legacy.env import (
    env_bool,
    env_bool_aliased,
    env_bool_aliased_optional,
    env_int,
    env_str,
    env_cache_root,
)
from istari_digital_client.identity.auth.identity_service import (
    IdentityApiVersion,
    IdentityApiVersionLike,
    IdentityServiceClient,
    RetryPolicy,
    parse_identity_api_version,
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


logger = logging.getLogger(__name__)


class _FromEnv:
    """Default for a credential field the caller omitted; resolved from the environment."""

    def __repr__(self) -> str:
        return "<from environment>"


_FROM_ENV = _FromEnv()

_CREDENTIAL_ENV_VARS = (
    ("registry_auth_token", "ISTARI_REGISTRY_AUTH_TOKEN"),
    ("identity_service_secret", "ISTARI_CLIENT_IDENTITY_SERVICE_SECRET"),
    ("identity_service_secret_file", "ISTARI_CLIENT_IDENTITY_SERVICE_SECRET_FILE"),
)


def _is_int(value: object) -> bool:
    # int() would silently truncate 16.9 or -0.5 past the bounds checks; bool is an int subclass
    return isinstance(value, int) and not isinstance(value, bool)


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
        default=cast(Optional[str], _FROM_ENV)  # omitted: read from ISTARI_REGISTRY_AUTH_TOKEN
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

    # === Transfer (data-plane) config fields ===
    transfer_concurrency: Optional[int] = field(
        default_factory=env_int("ISTARI_CLIENT_TRANSFER_CONCURRENCY", default=4)
    )
    """Parallel part uploads / range downloads per transfer, 1..16. Every transfer
    the client runs at once multiplies this, so a caller with its own upload pool
    opens ``pool_size x transfer_concurrency`` data-plane connections per host."""
    transfer_retry_deadline_secs: Optional[int] = field(
        default_factory=env_int("ISTARI_CLIENT_TRANSFER_RETRY_DEADLINE_SECS", default=300)
    )
    """Retry window for transfer registry calls and each part/range request.
    The window starts on the first retryable failure, not during healthy initial
    transfer time. Only new download offsets renew an active window. Backoff and
    jitter use ``retry_*``; disabling retries permits exactly one attempt.
    Socket inactivity/request timeouts bound silent attempts separately; this is
    not a strict transfer wall-clock deadline or cancellable DNS guarantee."""
    transfer_read_timeout_secs: Optional[int] = field(
        default_factory=env_int("ISTARI_CLIENT_TRANSFER_READ_TIMEOUT_SECS", default=120)
    )
    """Data-plane socket idle timeout (per read, not wall-clock). Connect uses
    ``http_request_timeout_secs``, or 30 s when that is unset."""
    filesystem_cache_max_size: Optional[int] = field(
        default_factory=env_int(
            "ISTARI_CLIENT_FILESYSTEM_CACHE_MAX_SIZE", default=2 * 1024 * 1024 * 1024
        )
    )
    """Largest content (bytes) written to the filesystem cache; bigger downloads
    bypass it so a second full copy is never written."""

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
        default_factory=env_bool_aliased_optional(
            [
                "ISTARI_DIGITAL_IDENTITY_SERVICE_ENABLED",
                "ISTARI_CLIENT_IDENTITY_SERVICE_ENABLED",
            ]
        )
    )
    """When True, authenticate to the registry with an auto-refreshed JWT obtained
    from the Identity Service (RFC 7523 private_key_jwt) instead of a fixed PAT.
    Requires ``digital_api_url`` (gateway) or ``identity_url`` (direct); the
    Identity Service base URL is derived from these (see ``_identity_service_base_url``).

    Read from the shared, cross-client ``ISTARI_DIGITAL_IDENTITY_SERVICE_ENABLED``
    (preferred) or the service-prefixed ``ISTARI_CLIENT_IDENTITY_SERVICE_ENABLED``
    (alias); the shared var wins when both are set, so one platform value can
    enable identity-service auth across every Istari client.

    Left unset (the default), it resolves to True when an identity-service secret or secret
    file is configured and a gateway or ``identity_url`` resolves, and to False otherwise
    (logging a warning when a secret is configured but no URL resolves); a PAT does not turn it
    on. An explicit False (the argument, or whichever toggle variable takes effect) wins unless
    ``identity_service_required`` is set. When True without a configured secret, a client that
    has a PAT uses the PAT instead. A PAT passed as an argument also wins over a secret read
    from the environment. Both of those PAT rules yield to ``identity_service_required``."""
    identity_service_secret: Optional[str] = field(
        default=cast(Optional[str], _FROM_ENV),  # omitted: read from ISTARI_CLIENT_IDENTITY_SERVICE_SECRET
        repr=False,
    )
    """Inline credentials: a base64-encoded JSON blob {clientId, keyId, key}
    where key is a PEM-encoded ECDSA P-384 private key."""
    identity_service_secret_file: Optional[Union[str, Path]] = field(
        default=cast(Optional[Union[str, Path]], _FROM_ENV),  # omitted: read from ISTARI_CLIENT_IDENTITY_SERVICE_SECRET_FILE
        repr=False,
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

    identity_url: Optional[str] = field(
        default_factory=env_str("ISTARI_IDENTITY_URL", default=None)
    )
    """Direct base URL of the identity-service, used when no gateway is set. The
    gateway derivation ``<digital_api_url>/identity`` wins when ``digital_api_url``
    is set, mirroring how ``registry_url`` yields to the gateway."""
    identity_api_version: IdentityApiVersionLike = field(
        default_factory=env_str("ISTARI_IDENTITY_API_VERSION", default=IdentityApiVersion.AUTO)
    )
    """Which identity-service API this client uses: ``"auto"`` (the default), ``"v2"`` or ``"v1"``.

    Pass an :class:`IdentityApiVersion` member or its string; the attribute holds the
    member once the configuration is constructed.

    * ``"v2"``: the bearer token is issued at ``/api/v2/oauth2/token`` and
      carries ``principal_kind``; ``IstariAdmin.identity`` (tenants,
      memberships, principals, keys, roles, OAuth) works.
    * ``"v1"``: the bearer token is issued at ``/oauth2/token``;
      ``IstariAdmin.identity`` raises.
    * ``"auto"``: the first token fetch tries the v2 endpoint and settles on v1
      when the identity-service does not serve ``/api/v2``; nothing is sent when
      the configuration is constructed. :meth:`resolved_identity_api_version` reports
      the outcome.

    The deprecated key surface (``IstariAdmin.keys``, ``client.keys`` on the legacy
    clients, and the ``istari_digital_client.identity.v1`` helpers) works under any
    setting. Read from ``ISTARI_IDENTITY_API_VERSION`` when the argument is
    omitted; an explicit argument wins over the environment variable. Any other
    value raises :class:`ConfigurationError` when the configuration is constructed."""

    identity_service_required: bool = field(
        default_factory=env_bool_aliased(
            [
                "ISTARI_DIGITAL_IDENTITY_SERVICE_REQUIRED",
                "ISTARI_CLIENT_IDENTITY_SERVICE_REQUIRED",
            ],
            default=False,
        )
    )
    """When True, identity-service auth is mandatory: it is enabled whatever
    ``identity_service_enabled`` says, and a missing secret raises
    :class:`ConfigurationError` instead of falling back to the PAT. Read from
    ``ISTARI_DIGITAL_IDENTITY_SERVICE_REQUIRED`` (preferred) or the
    ``ISTARI_CLIENT_IDENTITY_SERVICE_REQUIRED`` alias. Defaults to False."""

    # === Date and time formats ===
    datetime_format: str = field(init=False, default="%Y-%m-%dT%H:%M:%S.%f%z")
    date_format: str = field(init=False, default="%Y-%m-%d")

    # Holds the live Identity Service token state when identity_service_enabled. Hidden from
    # init/repr/equality.
    _identity_service_client: Optional[IdentityServiceClient] = field(
        init=False, default=None, repr=False, compare=False
    )
    # Credential fields filled from the environment rather than passed as arguments.
    _credentials_from_env: frozenset[str] = field(
        init=False, default=frozenset(), repr=False, compare=False
    )

    def __post_init__(self) -> None:
        self._read_credentials_from_env()
        if self.s3_direct_upload_enabled and not self.s3_bucket_name:
            raise ConfigurationError(
                "ISTARI_CLIENT_S3_BUCKET_NAME must be set when ISTARI_CLIENT_S3_DIRECT_UPLOAD is enabled"
            )

        self._validate_transfer_settings()
        self._configure_logging()
        self._configure_identity_service()

    def _validate_transfer_settings(self) -> None:
        """Reject out-of-range transfer knobs at construction."""
        concurrency = self.transfer_concurrency
        if not _is_int(concurrency) or not 1 <= concurrency <= 16:
            raise ConfigurationError(
                "ISTARI_CLIENT_TRANSFER_CONCURRENCY must be an integer between 1 and 16"
            )
        for name in ("transfer_retry_deadline_secs", "filesystem_cache_max_size"):
            value = getattr(self, name)
            if not _is_int(value) or value < 0:
                raise ConfigurationError(f"{name} must be a non-negative integer")
        # urllib3 rejects a read timeout of 0, so it would fail every transfer.
        timeout = self.transfer_read_timeout_secs
        if not _is_int(timeout) or timeout <= 0:
            raise ConfigurationError("transfer_read_timeout_secs must be a positive integer")

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

    def _read_credentials_from_env(self) -> None:
        """Fill omitted credential fields from the environment, recording which ones it supplied."""
        from_env = set()
        for name, env_var in _CREDENTIAL_ENV_VARS:
            if getattr(self, name) is _FROM_ENV:
                value = os.environ.get(env_var)
                setattr(self, name, value)
                if value is not None:
                    from_env.add(name)
        self._credentials_from_env = frozenset(from_env)

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

    def resolved_identity_api_version(self) -> IdentityApiVersion:
        """The identity-service API version in force: ``IdentityApiVersion.V1`` or ``V2``.

        Settles ``"auto"`` on first use through the identity-service client, which
        fetches a token; without identity-service auth ``"auto"`` reads as ``"v2"``.

        :raises IdentityServiceError: If settling ``"auto"`` fails.
        """
        if self._identity_service_client is not None:
            return self._identity_service_client.api_version
        version = parse_identity_api_version(self.identity_api_version)
        return IdentityApiVersion.V2 if version is IdentityApiVersion.AUTO else version

    def _identity_service_base_url(self) -> Optional[str]:
        """Identity-service base URL: the gateway derivation, else ``identity_url``, else None."""
        if self.digital_api_url:
            return self.digital_api_url.rstrip("/") + "/identity"
        if self.identity_url:
            return self.identity_url.rstrip("/")
        return None

    def _configure_identity_service(self) -> None:
        """Validate Identity Service config and construct the token client when Identity Service is enabled."""
        try:
            self.identity_api_version = parse_identity_api_version(self.identity_api_version)
        except ValueError as e:
            raise ConfigurationError(str(e)) from None

        has_secret = bool(self.identity_service_secret or self.identity_service_secret_file)
        explicit_secret = any(
            getattr(self, name) and name not in self._credentials_from_env
            for name in ("identity_service_secret", "identity_service_secret_file")
        )
        explicit_pat = bool(self.registry_auth_token) and (
            "registry_auth_token" not in self._credentials_from_env
        )
        # Unset: a secret turns it on when an identity-service URL resolves; a PAT never does.
        if self.identity_service_enabled is None:
            has_url = bool(self._identity_service_base_url())
            self.identity_service_enabled = has_secret and has_url
            if (
                has_secret
                and not has_url
                and not self.identity_service_required
                and not (explicit_pat and not explicit_secret)
            ):
                logger.warning(
                    "An identity-service secret is configured but identity-service auth stays off: "
                    "set ISTARI_DIGITAL_API_URL (gateway) or ISTARI_IDENTITY_URL (direct) to use it"
                )
        if self.identity_service_required:
            self.identity_service_enabled = True
        elif self.identity_service_enabled and has_secret and explicit_pat and not explicit_secret:
            logger.debug(
                "The personal access token passed to Configuration takes precedence over the "
                "identity-service secret read from ISTARI_CLIENT_IDENTITY_SERVICE_SECRET(_FILE)"
            )
            self.identity_service_enabled = False
        elif self.identity_service_enabled and not has_secret and self.registry_auth_token:
            logger.debug(
                "No identity-service secret is configured, so the client authenticates with its "
                "personal access token; set ISTARI_DIGITAL_IDENTITY_SERVICE_REQUIRED=true to refuse it"
            )
            self.identity_service_enabled = False
        elif self.identity_service_enabled and not has_secret:
            raise ConfigurationError(
                "No credentials are configured: set ISTARI_REGISTRY_AUTH_TOKEN to authenticate "
                "with a personal access token, or ISTARI_CLIENT_IDENTITY_SERVICE_SECRET or "
                "ISTARI_CLIENT_IDENTITY_SERVICE_SECRET_FILE to authenticate through identity-service"
            )
        if not self.identity_service_enabled:
            return

        identity_service_url = self._identity_service_base_url()
        if not identity_service_url:
            raise ConfigurationError(
                "ISTARI_DIGITAL_API_URL (gateway) or ISTARI_IDENTITY_URL (direct) must be set when "
                "identity-service auth is enabled (ISTARI_DIGITAL_IDENTITY_SERVICE_ENABLED) or "
                "required (ISTARI_DIGITAL_IDENTITY_SERVICE_REQUIRED)"
            )

        # Prefer the file-based secret if configured; fall back to the inline secret.
        secret = self.identity_service_secret
        if self.identity_service_secret_file:
            secret = str(self.identity_service_secret_file)

        if not secret:
            raise ConfigurationError(
                "ISTARI_CLIENT_IDENTITY_SERVICE_SECRET or "
                "ISTARI_CLIENT_IDENTITY_SERVICE_SECRET_FILE must be set when "
                "identity-service auth is enabled (ISTARI_DIGITAL_IDENTITY_SERVICE_ENABLED) "
                "or required (ISTARI_DIGITAL_IDENTITY_SERVICE_REQUIRED)"
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
            api_version=self.identity_api_version,
        )

    def _configure_logging(self) -> None:
        """Configures logging based on the configuration settings."""
        log_level_str = (self.log_level or "INFO").upper()
        log_level = getattr(logging, log_level_str, logging.INFO)

        if not isinstance(log_level, int):
            raise ValueError(f"Invalid log level: {self.log_level}")

        pkg_logger = logging.getLogger("istari_digital_client")
        pkg_logger.setLevel(log_level)

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
        for existing in list(pkg_logger.handlers):
            pkg_logger.removeHandler(existing)
            existing.close()

        for handler in handlers:
            pkg_logger.addHandler(handler)

        pkg_logger.propagate = False

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
