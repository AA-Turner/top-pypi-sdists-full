"""
business_metrics_manager_utils.py

Builds the BUSINESS_METRICS_MANAGER: discovers this action, reads its details
off the control plane, and opens the Redis stream the aggregated metrics go out
on.

The aggregation half -- the two dataclasses and ``BUSINESS_METRICS_MANAGER``
itself -- moved to ``business_metrics_aggregation_utils`` under SG-6/F02b, where
the two together had carried this module past the org file-size cap. They are
re-exported below, so ``from ...business_metrics_manager_utils import
BUSINESS_METRICS_MANAGER`` keeps working and no importer had to change.
"""

import logging
import os
from typing import Any, Dict, Optional

from ...clients import identity
from ...clients.analytics_client import AnalyticsClient
from ...clients.bootstrap import get_action_id
from .business_metrics_aggregation_utils import (
    AGGREGATION_TYPES,
    BUSINESS_METRICS_MANAGER,
    DEFAULT_AGGREGATION_INTERVAL,
    DEFAULT_METRICS_CONFIG,
    CameraMetricsState,
    MetricAggregator,
)
from .public_ip import resolve_public_ip_once

__all__ = [
    "AGGREGATION_TYPES",
    "BUSINESS_METRICS_MANAGER",
    "DEFAULT_AGGREGATION_INTERVAL",
    "DEFAULT_METRICS_CONFIG",
    "BusinessMetricsManagerFactory",
    "CameraMetricsState",
    "MetricAggregator",
    "get_business_metrics_manager",
]


class BusinessMetricsManagerFactory:
    """
    Factory class for creating BUSINESS_METRICS_MANAGER instances.

    Handles session initialization and Redis/Kafka client creation
    following the same pattern as IncidentManagerFactory.
    """

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        client: Optional[AnalyticsClient] = None,
    ):
        """
        Args:
            logger: Python logger instance.
            client: The platform client to make calls through. Absent one, a client is built
                on the session this factory already resolves, so a caller that passes nothing
                sends exactly the requests it sent before.
        """
        self.logger = logger or logging.getLogger(__name__)
        self._initialized = False
        self._client = client
        self._business_metrics_manager: Optional[BUSINESS_METRICS_MANAGER] = None

        # Store these for later access
        self._session = None
        self._action_id: Optional[str] = None
        self._instance_id: Optional[str] = None
        self._deployment_id: Optional[str] = None
        self._app_deployment_id: Optional[str] = None
        self._application_id: Optional[str] = None  # Store application_id from jobParams
        self._external_ip: Optional[str] = None

    def _platform(self) -> AnalyticsClient:
        """The client every platform call in this factory goes through.

        The caller's when one was injected, otherwise one riding the session resolved above --
        so the requests are the same either way.
        """
        if self._client is None:
            self._client = AnalyticsClient(session=self._session)
        return self._client

    def _resolve_session(self, config: Any, session_cls: Any) -> Any:
        """The session to make control-plane calls with: config's, else one from env."""
        session = getattr(config, "session", None)
        if session:
            self.logger.info("[BUSINESS_METRICS_MANAGER_FACTORY] ✓ Using session from config")
            return session

        self.logger.info(
            "[BUSINESS_METRICS_MANAGER_FACTORY] No session in config, creating from environment..."
        )
        account_number = os.getenv("MATRICE_ACCOUNT_NUMBER", "")
        access_key_id = os.getenv("MATRICE_ACCESS_KEY_ID", "")
        secret_key = os.getenv("MATRICE_SECRET_ACCESS_KEY", "")
        project_id = os.getenv("MATRICE_PROJECT_ID", "")

        self.logger.debug(
            f"[BUSINESS_METRICS_MANAGER_FACTORY] Env vars - "
            f"account: {'SET' if account_number else 'NOT SET'}, "
            f"access_key: {'SET' if access_key_id else 'NOT SET'}, "
            f"secret: {'SET' if secret_key else 'NOT SET'}"
        )

        session = session_cls(
            account_number=account_number,
            access_key=access_key_id,
            secret_key=secret_key,
            project_id=project_id,
        )
        self.logger.info("[BUSINESS_METRICS_MANAGER_FACTORY] ✓ Created session from environment")
        return session

    def _store_action_identifiers(
        self, action_details: Dict[str, Any], job_params: Dict[str, Any]
    ) -> None:
        """Pull the deployment/application identifiers out of the action document.

        The per-field search order is the resolvers' and is not symmetric:
        ``application_id`` is read from ``jobParams`` before ``actionDetails`` because that is
        where the control plane writes it, and ``app_deployment_id`` the other way round. The
        two slices disagree, so reading either in the other's order answers with the wrong id.

        The camelCase spellings this used to try are gone. The action record carries
        ``application_id`` and ``app_deployment_id`` and no other form of either, confirmed
        with the platform, so those branches never fired.
        """
        self._deployment_id = action_details.get("_idDeployment") or action_details.get(
            "deployment_id"
        )

        record = {"actionDetails": action_details, "jobParams": job_params}
        self._app_deployment_id = identity.resolve_app_deployment_id(action_record=lambda: record)
        self._application_id = identity.resolve_application_id(action_record=lambda: record)

        self._instance_id = action_details.get("instanceID") or action_details.get("instanceId")
        self._external_ip = action_details.get("externalIP") or action_details.get("externalIp")

    def _load_action_details(self) -> Optional[Dict[str, Any]]:
        """Fetch this action's details and store its identifiers.

        Returns the ``actionDetails`` sub-document, or ``None`` when the call
        failed -- which the caller treats as "no metrics transport is possible".
        """
        try:
            record = self._platform().actions.get_action_details(self._action_id)
            action_details = record.action_details
            job_params = record.job_params

            # Extract server details
            server_id = (
                action_details.get("serverId")
                or action_details.get("server_id")
                or action_details.get("serverID")
                or action_details.get("redis_server_id")
                or action_details.get("kafka_server_id")
            )
            server_type = (
                action_details.get("serverType")
                or action_details.get("server_type")
                or action_details.get("type")
            )

            self._store_action_identifiers(action_details, job_params)

            print("----- BUSINESS METRICS MANAGER ACTION DETAILS -----")
            print(f"action_id: {self._action_id}")
            print(f"server_type: {server_type}")
            print(f"server_id: {server_id}")
            print(f"deployment_id: {self._deployment_id}")
            print(f"app_deployment_id: {self._app_deployment_id}")
            print(f"application_id: {self._application_id}")
            print(f"instance_id: {self._instance_id}")
            print(f"external_ip: {self._external_ip}")
            print(f"jobParams keys: {list(job_params.keys()) if job_params else []}")
            print("----------------------------------------------------")

            self.logger.info(
                f"[BUSINESS_METRICS_MANAGER_FACTORY] Action details - server_type={server_type}, "
                f"instance_id={self._instance_id}, "
                f"app_deployment_id={self._app_deployment_id}, application_id={self._application_id}"
            )

            # Log all available keys for debugging
            self.logger.debug(
                f"[BUSINESS_METRICS_MANAGER_FACTORY] actionDetails keys: {list(action_details.keys())}"
            )
            self.logger.debug(
                f"[BUSINESS_METRICS_MANAGER_FACTORY] jobParams keys: {list(job_params.keys()) if job_params else []}"
            )
            return action_details

        except Exception as e:
            self.logger.error(
                f"[BUSINESS_METRICS_MANAGER_FACTORY] ❌ Failed to fetch action details: {e}",
                exc_info=True,
            )
            print("----- BUSINESS METRICS MANAGER ACTION DETAILS ERROR -----")
            print(f"action_id: {self._action_id}")
            print(f"error: {e}")
            print("---------------------------------------------------------")
            return None

    def _detect_localhost(self, action_details: Dict[str, Any]) -> bool:
        """Whether the action's server host is a loopback address.

        Diagnostic only: ``initialize`` overwrites the result (see the comment
        at the call site), so this decides nothing but the log line.
        """
        public_ip = self._get_public_ip()

        # Get server host from action_details
        server_host = (
            action_details.get("externalIP")
            or action_details.get("external_IP")
            or action_details.get("externalip")
            or action_details.get("external_ip")
            or action_details.get("externalIp")
            or action_details.get("external_Ip")
        )
        print(f"server_host: {server_host}")
        self.logger.info(f"[BUSINESS_METRICS_MANAGER_FACTORY] DEBUG - server_host: {server_host}")

        localhost_indicators = ["localhost", "127.0.0.1", "0.0.0.0"]  # nosec B104
        if server_host in localhost_indicators:
            self.logger.info(
                f"[BUSINESS_METRICS_MANAGER_FACTORY] Detected Localhost environment "
                f"(Public IP={public_ip}, Server IP={server_host})"
            )
            return True

        self.logger.info(
            f"[BUSINESS_METRICS_MANAGER_FACTORY] Detected Cloud environment "
            f"(Public IP={public_ip}, Server IP={server_host})"
        )
        return False

    def _redis_stream_kwargs(self, server: Any) -> Dict[str, Any]:
        """Turn the instance's Redis server record into MatriceStream kwargs.

        Sentinel fields are only added when the record carries a sentinel
        config, because MatriceStream switches to HA discovery on their presence.

        ``username``, ``db`` and ``connection_timeout`` are stated rather than read. The
        producer's published schema for this route declares none of the three, so the reads
        they replace (``data.get("username")``, ``.get("db", 0)``,
        ``.get("connection_timeout", 120)``) resolved to exactly these values on every call.
        """
        password = server.password

        # Sentinel HA support
        sentinel_hosts = None
        master_name = None
        sentinel_cfg = server.sentinel_config or {}
        if sentinel_cfg.get("sentinelHosts"):
            sentinel_hosts = [(h, 26379) for h in sentinel_cfg["sentinelHosts"]]
            master_name = sentinel_cfg.get("masterName")

        sentinel_str = (
            f"yes, master={master_name}, nodes={len(sentinel_hosts)}" if sentinel_hosts else "no"
        )

        print("----- BUSINESS METRICS MANAGER REDIS SERVER PARAMS -----")
        print(f"instance_id: {self._instance_id}")
        print(f"host: {server.host}")
        print(f"port: {server.port}")
        print(f"username: {None}")
        print(f"password: {'*' * len(password) if password else ''}")
        print(f"db: {0}")
        print(f"connection_timeout: {120}")
        print(f"sentinel: {sentinel_str}")
        print("--------------------------------------------------------")

        self.logger.info(
            f"[BUSINESS_METRICS_MANAGER_FACTORY] Redis params - "
            f"host={server.host}, port={server.port}, "
            f"user={None}, sentinel={sentinel_str}"
        )

        stream_kwargs = dict(
            host=server.host,
            port=int(server.port),
            password=password,
            username=None,
            db=0,
            connection_timeout=120,
        )
        if sentinel_hosts and master_name:
            stream_kwargs["sentinel_hosts"] = sentinel_hosts
            stream_kwargs["master_name"] = master_name
        return stream_kwargs

    def _build_redis_client(self, stream_cls: Any, stream_type: Any) -> Optional[Any]:
        """Look up this instance's Redis server and open a stream on it.

        Returns ``None`` -- never raises -- when the instance id is unknown, the
        lookup fails, or the connection cannot be made: business metrics are
        best-effort telemetry and must not take the analytics process down.
        """
        if not self._instance_id:
            self.logger.error(
                "[BUSINESS_METRICS_MANAGER_FACTORY] ❌ Localhost mode but instance_id missing"
            )
            return None

        try:
            self.logger.info(
                f"[BUSINESS_METRICS_MANAGER_FACTORY] Fetching Redis server info for instance: {self._instance_id}"
            )
            server = self._platform().actions.fetch_redis_server(self._instance_id)

            if server is None:
                self.logger.warning(
                    "[BUSINESS_METRICS_MANAGER_FACTORY] Failed to fetch Redis server info: "
                    f"no record for instance {self._instance_id}"
                )
                return None

            stream_kwargs = self._redis_stream_kwargs(server)
            redis_client = stream_cls(stream_type.REDIS, **stream_kwargs)
            # Setup for metrics publishing
            redis_client.setup("business_metrics")
            self.logger.info("[BUSINESS_METRICS_MANAGER_FACTORY] ✓ Redis client initialized")
            return redis_client
        except Exception as e:  # noqa: BLE001 - the failure surface here spans the control-plane
            # RPC, int()/dict parsing of an untrusted server document, redis-py's own error
            # tree and a TCP connect; every one of them means "no Redis transport", and this
            # runs during analytics startup, where raising would take the whole process down
            # over optional telemetry.
            self.logger.warning(
                f"[BUSINESS_METRICS_MANAGER_FACTORY] Redis initialization failed: {e}"
            )
            return None

    def _start_manager(
        self,
        redis_client: Optional[Any],
        kafka_client: Optional[Any],
        aggregation_interval: int,
        metrics_config: Optional[Dict[str, str]],
    ) -> None:
        """Build the manager over the available transport and start its timer."""
        self._business_metrics_manager = BUSINESS_METRICS_MANAGER(
            redis_client=redis_client,
            kafka_client=kafka_client,
            output_topic="business_metrics",
            aggregation_interval=aggregation_interval,
            metrics_config=metrics_config or DEFAULT_METRICS_CONFIG.copy(),
            logger=self.logger,
        )
        # Set factory reference for accessing deployment info
        self._business_metrics_manager.set_factory_ref(self)
        # Start the timer thread
        self._business_metrics_manager.start()

        transport = "Redis" if redis_client else "Kafka"
        self.logger.info(
            f"[BUSINESS_METRICS_MANAGER_FACTORY] ✓ Business metrics manager created with {transport}"
        )
        print(f"----- BUSINESS METRICS MANAGER INITIALIZED ({transport}) -----")

    def initialize(
        self,
        config: Any,
        aggregation_interval: int = DEFAULT_AGGREGATION_INTERVAL,
        metrics_config: Optional[Dict[str, str]] = None,
    ) -> Optional[BUSINESS_METRICS_MANAGER]:
        """
        Initialize and return BUSINESS_METRICS_MANAGER with Redis/Kafka clients.

        This follows the same pattern as IncidentManagerFactory for
        session initialization and Redis/Kafka client creation.

        Args:
            config: Configuration object with session, server_id, etc.
            aggregation_interval: Interval in seconds for aggregation (default 300)
            metrics_config: Dict of metric_name -> aggregation_type

        Returns:
            BUSINESS_METRICS_MANAGER instance or None if initialization failed
        """
        if self._initialized and self._business_metrics_manager is not None:
            self.logger.debug(
                "[BUSINESS_METRICS_MANAGER_FACTORY] Already initialized, returning existing instance"
            )
            return self._business_metrics_manager

        try:
            # Import required modules
            from matrice_common.session import Session
            from matrice_streaming.databus.matrice_stream import MatriceStream, StreamType

            self.logger.info(
                "[BUSINESS_METRICS_MANAGER_FACTORY] ===== STARTING INITIALIZATION ====="
            )

            self._session = self._resolve_session(config, Session)

            # Discover action_id
            self._action_id = get_action_id()
            if not self._action_id:
                self.logger.error(
                    "[BUSINESS_METRICS_MANAGER_FACTORY] ❌ Could not discover action_id"
                )
                print("----- BUSINESS METRICS MANAGER ACTION DISCOVERY -----")
                print("action_id: NOT FOUND")
                print("------------------------------------------------------")
                self._initialized = True
                return None

            self.logger.info(
                f"[BUSINESS_METRICS_MANAGER_FACTORY] ✓ Discovered action_id: {self._action_id}"
            )

            action_details = self._load_action_details()
            if action_details is None:
                self._initialized = True
                return None

            # Determine localhost vs cloud using externalIP from action_details
            is_localhost = self._detect_localhost(action_details)

            # Historical deployment behavior: always initialize via Redis (instance API), not Kafka.
            is_localhost = True

            redis_client = None
            kafka_client = None

            # STRICT SWITCH: Only Redis if localhost, Only Kafka if cloud
            if is_localhost:
                # Initialize Redis client (ONLY) using instance_id
                redis_client = self._build_redis_client(MatriceStream, StreamType)

            # Create business metrics manager if we have at least one transport
            if redis_client or kafka_client:
                self._start_manager(
                    redis_client, kafka_client, aggregation_interval, metrics_config
                )
            else:
                self.logger.warning(
                    f"[BUSINESS_METRICS_MANAGER_FACTORY] No {'Redis' if is_localhost else 'Kafka'} client available, "
                    f"business metrics manager not created"
                )

            self._initialized = True
            self.logger.info(
                "[BUSINESS_METRICS_MANAGER_FACTORY] ===== INITIALIZATION COMPLETE ====="
            )
            return self._business_metrics_manager

        except ImportError as e:
            self.logger.error(f"[BUSINESS_METRICS_MANAGER_FACTORY] Import error: {e}")
            self._initialized = True
            return None
        except Exception as e:
            self.logger.error(
                f"[BUSINESS_METRICS_MANAGER_FACTORY] Initialization failed: {e}",
                exc_info=True,
            )
            self._initialized = True
            return None

    def _get_public_ip(self) -> str:
        """This host's public IP; see :func:`.public_ip.resolve_public_ip_once`.

        ANA-18: this used ``timeout=120`` and ran uncached from ``initialize()``,
        i.e. on the first frame. The value never reaches a decision -- the
        localhost-vs-cloud branch below is computed from ``server_host`` and then
        unconditionally overwritten with ``is_localhost = True`` -- so the whole
        cost bought two log f-strings.
        """
        self.logger.info("[BUSINESS_METRICS_MANAGER_FACTORY] Fetching public IP address...")
        public_ip = resolve_public_ip_once(self.logger)
        self.logger.debug(f"[BUSINESS_METRICS_MANAGER_FACTORY] Public IP: {public_ip}")
        return public_ip

    @property
    def is_initialized(self) -> bool:
        return self._initialized

    @property
    def business_metrics_manager(self) -> Optional[BUSINESS_METRICS_MANAGER]:
        return self._business_metrics_manager


# Module-level factory instance for convenience
_default_factory: Optional[BusinessMetricsManagerFactory] = None


def get_business_metrics_manager(
    config: Any,
    logger: Optional[logging.Logger] = None,
    aggregation_interval: int = DEFAULT_AGGREGATION_INTERVAL,
    metrics_config: Optional[Dict[str, str]] = None,
) -> Optional[BUSINESS_METRICS_MANAGER]:
    """
    Get or create BUSINESS_METRICS_MANAGER instance.

    This is a convenience function that uses a module-level factory.
    For more control, use BusinessMetricsManagerFactory directly.

    Args:
        config: Configuration object with session, server_id, etc.
        logger: Logger instance
        aggregation_interval: Interval in seconds for aggregation (default 300)
        metrics_config: Dict of metric_name -> aggregation_type

    Returns:
        BUSINESS_METRICS_MANAGER instance or None
    """
    global _default_factory

    if _default_factory is None:
        _default_factory = BusinessMetricsManagerFactory(logger=logger)

    return _default_factory.initialize(
        config, aggregation_interval=aggregation_interval, metrics_config=metrics_config
    )
