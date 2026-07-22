import asyncio
import base64
import json
import logging
import os
import time
from typing import Any, Dict, List, Optional

from kafka import KafkaProducer
from matrice_common.session import Session

from matrice_inference.server.stream.deployment_refresh_listener import (
    DeploymentRefreshListener,
)
from matrice_inference.server.stream.utils import CameraConfig


class AppDeployment:
    """Handles app deployment configuration and camera setup for streaming pipeline."""

    def __init__(
        self,
        session: Session,
        app_deployment_id: str,
        deployment_instance_id: Optional[str] = None,
        instance_id: Optional[str] = None,
        connection_timeout: int = 1200,
        action_id: Optional[str] = None,
        instance_string_id: Optional[str] = None,
    ):  # Increased from 300 to 1200
        self.app_deployment_id = app_deployment_id
        self.deployment_instance_id = deployment_instance_id
        self.instance_id = instance_id
        self.instance_string_id = instance_string_id or instance_id
        self.rpc = session.rpc
        self.session = session
        self.connection_timeout = connection_timeout
        self.action_id = action_id
        self.logger = logging.getLogger(__name__)

        self.logger.info(
            "AppDeployment initialized: instance_id=%s, deployment_instance_id=%s, "
            "app_deployment_id=%s, instance_string_id=%s, action_id=%s",
            instance_id,
            deployment_instance_id,
            app_deployment_id,
            self.instance_string_id,
            action_id,
        )
        if not instance_id:
            self.logger.error(
                "AppDeployment created with instance_id=None. "
                "All get_consuming_topics_by_instance calls will fail. "
                "Root cause: _idComputeInstance missing from outer action record."
            )

        # Refresh listener for dynamic topic updates (initialized separately)
        self.refresh_listener: Optional[DeploymentRefreshListener] = None
        self.streaming_pipeline = None  # Reference to pipeline (set externally)
        self.event_loop = None  # Event loop reference for async operations

        # Heartbeat reporter for sending app deployment status
        self.heartbeat_producer: Optional[KafkaProducer] = None
        self.heartbeat_topic = "app_deployment_heartbeat"
        self.heartbeat_timeout = 5.0
        self._init_heartbeat_producer()

        # Server info cache with 10 minute expiration
        self._server_info_cache: Dict[str, Dict[str, Any]] = {}  # Key: f"{server_type}:{server_id}"
        self._cache_expiration = 600  # 10 minutes in seconds

    def get_consuming_topics_by_instance(self) -> List[Dict]:
        """Get all consuming topics (input+output) for this instance in a single API call.

        Only available when instance_id is set.

        Returns:
            List of CameraStreamTopicResponse dicts
        """
        if not self.instance_id:
            self.logger.error(
                "get_consuming_topics_by_instance called without instance_id. "
                "Ensure _idComputeInstance is present in the outer action record "
                "(not inside actionDetails). Without it, no cameras can be loaded."
            )
            return []
        api_url = f"/v1/inference/get_app_deployment_consuming_topics/{self.instance_id}"
        self.logger.info("Fetching consuming topics: GET %s", api_url)
        try:
            response = self.rpc.get(api_url)
            self.logger.debug("get_consuming_topics_by_instance raw response: %s", response)
            if response.get("success", False):
                topics = response.get("data", [])
                self.logger.info(
                    "Got %d consuming topics for instance %s (camera_ids: %s)",
                    len(topics),
                    self.instance_id,
                    [t.get("cameraId") for t in topics] if topics else "[]",
                )
                return topics
            self.logger.error(
                "Failed to get consuming topics from %s: %s (full response: %s)",
                api_url,
                response.get("message", "Unknown error"),
                response,
            )
            return []
        except Exception as e:
            self.logger.error(
                "Exception getting consuming topics from %s: %s",
                api_url,
                e,
                exc_info=True,
            )
            return []

    def get_output_topics_by_instance(self, app_deployment_id: str) -> List[Dict]:
        """Get output topics filtered by app deployment + instance.

        Args:
            app_deployment_id: App deployment ID to filter by

        Returns:
            List of output topic dicts
        """
        if not self.instance_id:
            self.logger.error(
                "get_output_topics_by_instance called without instance_id. "
                "Ensure instance_id is passed to AppDeployment constructor."
            )
            return []
        try:
            response = self.rpc.get(
                f"/v1/inference/get_output_topics_by_app_deployment_and_instance/{app_deployment_id}/{self.instance_id}"
            )
            if response.get("success", False):
                return response.get("data", [])
            self.logger.error(f"Failed to get output topics by instance: {response.get('message', 'Unknown error')}")
            return []
        except Exception as e:
            self.logger.error(f"Exception getting output topics by instance: {e}")
            return []

    def get_redis_connection_by_instance(self, max_retries: int = 3) -> Optional[Dict]:
        """Get Redis connection info by instance ID, with retry and Sentinel support.

        Args:
            max_retries: Number of retry attempts with exponential backoff

        Returns:
            Connection info dict or None
        """
        if not self.instance_id:
            return None

        for attempt in range(max_retries):
            try:
                response = self.rpc.get(f"/v1/actions/get_redis_server_by_instance_id/{self.instance_string_id}")
                if response.get("success", False):
                    data = response.get("data")
                    if data and data.get("status") == "running":
                        redis_password = data.get("password") or None
                        if not redis_password:
                            self.logger.warning(
                                "Redis endpoint %s:%s returned no password; connecting without authentication",
                                data.get("host") or "localhost",
                                data.get("port"),
                            )
                        conn = {
                            "host": data.get("host") or "localhost",
                            "port": int(data["port"]),
                            # Default to None (not "") so downstream treats a
                            # missing credential as "no auth" explicitly.
                            "password": redis_password,
                            "username": data.get("username"),
                            "db": data.get("db", 0),
                            "connection_timeout": 120,
                        }
                        # Sentinel support — sentinelConfig is a nested object
                        sentinel_cfg = data.get("sentinelConfig") or {}
                        if sentinel_cfg.get("sentinelHosts"):
                            conn["sentinel_hosts"] = [(h, 26379) for h in sentinel_cfg["sentinelHosts"]]
                            conn["master_name"] = sentinel_cfg.get("masterName")
                            self.logger.info(
                                "Redis Sentinel detected: master=%s, sentinels=%d",
                                conn["master_name"],
                                len(conn["sentinel_hosts"]),
                            )
                        return conn
            except Exception as e:
                self.logger.warning(f"Redis API call attempt {attempt + 1}/{max_retries} failed: {e}")

            if attempt < max_retries - 1:
                delay = 2**attempt
                self.logger.info(f"Retrying Redis config fetch in {delay}s...")
                time.sleep(delay)

        self.logger.error(f"All {max_retries} attempts to get Redis config failed for instance {self.instance_id}")
        return None

    def get_camera_configs(self) -> Dict[str, CameraConfig]:
        """
        Get camera configurations for the streaming pipeline.

        Tries the app-deployment-specific endpoint first
        (get_output_topics_by_app_deployment_and_instance), then falls back
        to the SG endpoint (get_app_deployment_consuming_topics) on failure.

        Returns:
            Dict[str, CameraConfig]: Dictionary mapping camera_id to CameraConfig
        """
        self.logger.info(
            "get_camera_configs called: instance_id=%s, app_deployment_id=%s",
            self.instance_id,
            self.app_deployment_id,
        )

        topics = []
        primary_ok = False

        # Primary: app-deployment-specific endpoint. An EMPTY result here is a
        # VALID answer — this deployment simply owns 0 cameras right now — NOT a
        # failure. It must NOT trigger the instance-wide fallback, or a scaled-to-
        # zero deployment would adopt EVERY camera on the host (cross-deployment
        # leak: mask-detection processing FR/PC/weapon cams). See ANALYTICS incident.
        if self.app_deployment_id:
            try:
                topics = self.get_output_topics_by_instance(self.app_deployment_id)
                primary_ok = True
                self.logger.info(
                    "Got %d topics from app-deployment endpoint (primary)",
                    len(topics),
                )
            except Exception as e:
                self.logger.warning("App-deployment endpoint failed: %s, falling back to SG endpoint", e)
                topics = []
                primary_ok = False

        # Fallback: SG instance-wide endpoint — ONLY when the deployment-scoped
        # query could not be made or errored (no app_deployment_id / exception),
        # never on a successful-but-empty result.
        if not primary_ok:
            self.logger.info("Falling back to SG consuming-topics endpoint (deployment-scoped query unavailable)")
            topics = self.get_consuming_topics_by_instance()
            # Defense-in-depth: if we know our deployment, never adopt another
            # deployment's cameras from the instance-wide list.
            if self.app_deployment_id and topics:
                dep = str(self.app_deployment_id)
                before = len(topics)
                topics = [t for t in topics if str(t.get("appDeploymentId") or "") in ("", dep)]
                if len(topics) != before:
                    self.logger.warning(
                        "Filtered instance-wide topics to app_deployment_id=%s: %d -> %d",
                        dep,
                        before,
                        len(topics),
                    )

        configs = self._build_camera_configs_from_streaming_topics(topics)
        self.logger.info(
            "get_camera_configs result: %d topics -> %d camera configs",
            len(topics),
            len(configs),
        )
        return configs

    def _get_cached_server_info(self, server_type: str, server_id: str) -> Optional[Dict]:
        """Get server info from cache if available and not expired.

        Args:
            server_type: Type of server (kafka/redis)
            server_id: Server ID

        Returns:
            Cached connection info if available and valid, None otherwise
        """
        cache_key = f"{server_type}:{server_id}"

        if cache_key in self._server_info_cache:
            cached_entry = self._server_info_cache[cache_key]
            cached_time = cached_entry.get("timestamp", 0)
            current_time = time.time()

            # Check if cache is still valid (within 10 minutes)
            if current_time - cached_time < self._cache_expiration:
                self.logger.debug(
                    f"Using cached {server_type} server info for {server_id} (age: {current_time - cached_time:.1f}s)"
                )
                return cached_entry.get("data")
            # Cache expired, remove it
            self.logger.debug(f"Cache expired for {server_type} server {server_id}, will fetch fresh data")
            del self._server_info_cache[cache_key]

        return None

    def _cache_server_info(self, server_type: str, server_id: str, connection_info: Dict) -> None:
        """Cache server connection info with timestamp.

        Args:
            server_type: Type of server (kafka/redis)
            server_id: Server ID
            connection_info: Connection info to cache
        """
        cache_key = f"{server_type}:{server_id}"
        self._server_info_cache[cache_key] = {
            "timestamp": time.time(),
            "data": connection_info,
        }
        self.logger.debug(f"Cached {server_type} server info for {server_id}")

    def _get_kafka_connection_info(self, server_id: str) -> Optional[Dict]:
        """Query the Kafka server endpoint and return connection info, or ``None``.

        Behavior mirrors the previous nested ``_get_kafka_connection_info`` closure
        exactly (same completeness checks, logging, and exception handling).
        """
        try:
            response = self.rpc.get(f"/v1/actions/get_kafka_server/{server_id}")
            if response.get("success", False):
                data = response.get("data")
                if data and data.get("ipAddress") and data.get("port") and data.get("status") == "running":
                    return {
                        "bootstrap_servers": f"{data['ipAddress']}:{data['port']}",
                        "sasl_mechanism": "SCRAM-SHA-256",
                        "sasl_username": os.environ.get("KAFKA_SASL_USERNAME"),
                        "sasl_password": os.environ.get("KAFKA_SASL_PASSWORD"),
                        # SASL_PLAINTEXT (no TLS) is an accepted, documented
                        # dependency on the machine-wide private-only firewall
                        # posture: the broker is only reachable on the trusted
                        # private segment. Do not silently regress to exposing
                        # this on an untrusted network without moving to SASL_SSL.
                        "security_protocol": "SASL_PLAINTEXT",
                    }
                self.logger.debug("Kafka connection information is not complete, waiting...")
                return None
            self.logger.debug(
                "Failed to get Kafka connection information: %s",
                response.get("message", "Unknown error"),
            )
            return None
        except Exception as exc:
            self.logger.debug("Exception getting Kafka connection info: %s", str(exc))
            return None

    def _get_redis_connection_info(self, server_id: str) -> Optional[Dict]:
        """Resolve Redis connection info (instance API, then per-server API), or ``None``.

        Behavior mirrors the previous nested ``_get_redis_connection_info`` closure
        exactly (Sentinel support, fallthrough order, logging, exception handling).
        """
        # Try instance-level Redis endpoint first (supports Sentinel)
        try:
            conn = self.get_redis_connection_by_instance()
            if conn:
                self.logger.info("Got Redis connection info via instance-based API")
                return conn
            self.logger.debug("Instance-based Redis API returned no data, falling through to per-server API")
        except Exception as exc:
            self.logger.debug("Instance-based Redis API failed: %s, falling through", str(exc))

        # Try per-server-id API, fall back to hardcoded config if API fails
        try:
            # Build URL with actionId query parameter if available
            url = f"/v1/actions/redis_servers/{server_id}"
            if self.action_id:
                url += f"?actionId={self.action_id}"
            response = self.rpc.get(url)
            if response.get("success", False):
                data = response.get("data")
                if (
                    data
                    # and data.get("host")
                    and data.get("port")
                    and data.get("status") == "running"
                ):
                    conn = {
                        "host": data.get("host") or "localhost",
                        "port": int(data["port"]),
                        "password": data.get("password", ""),  # Empty string for passwordless Redis
                        "username": data.get("username"),  # None if not provided
                        "db": data.get("db", 0),
                        "connection_timeout": 120,  # Increased from 30 to 120
                    }
                    # Sentinel support — sentinelConfig is a nested object
                    sentinel_cfg = data.get("sentinelConfig") or {}
                    if sentinel_cfg.get("sentinelHosts"):
                        conn["sentinel_hosts"] = [(h, 26379) for h in sentinel_cfg["sentinelHosts"]]
                        conn["master_name"] = sentinel_cfg.get("masterName")
                        self.logger.info(
                            "Redis Sentinel detected (fallback path): master=%s, sentinels=%d",
                            conn["master_name"],
                            len(conn["sentinel_hosts"]),
                        )
                    return conn
        except Exception as exc:
            self.logger.debug("Exception getting Redis connection info from API: %s", str(exc))

        # No hardcoded fallback — return None so caller can skip/retry
        self.logger.error(
            "REDIS API CALL FAILED FOR SERVER ID: %s — no fallback, caller should retry or skip camera",
            server_id,
        )
        return None

    def get_and_wait_for_connection_info(self, server_type: str, server_id: str) -> Optional[Dict]:
        """Get the connection information for the streaming gateway."""
        # Check cache first
        cached_info = self._get_cached_server_info(server_type, server_id)
        if cached_info:
            return cached_info

        start_time = time.time()
        last_log_time = 0

        while True:
            current_time = time.time()

            # Get connection info based on server type
            connection_info = None
            if server_type == "kafka":
                connection_info = self._get_kafka_connection_info(server_id)
            elif server_type == "redis":
                connection_info = self._get_redis_connection_info(server_id)
            else:
                raise ValueError(f"Unsupported server type: {server_type}")

            # If we got valid connection info, cache it and return
            if connection_info:
                self.logger.info("Successfully retrieved %s connection information", server_type)
                self._cache_server_info(server_type, server_id, connection_info)
                return connection_info

            # Check timeout
            if current_time - start_time > self.connection_timeout:
                error_msg = (
                    f"Timeout waiting for {server_type} connection information after {self.connection_timeout} seconds"
                )
                self.logger.error(error_msg)

                # Log the last response for debugging
                try:
                    if server_type == "kafka":
                        response = self.rpc.get(f"/v1/actions/get_kafka_server/{server_id}")
                    else:
                        url = f"/v1/actions/redis_servers/{server_id}"
                        if self.action_id:
                            url += f"?actionId={self.action_id}"
                        response = self.rpc.get(url)
                    self.logger.error("Last response received: %s", response)
                except Exception as exc:
                    self.logger.error("Failed to get last response for debugging: %s", str(exc))

                return None  # Return None instead of raising exception to allow graceful handling

            # Log waiting message every 10 seconds to avoid spam
            if current_time - last_log_time >= 10:
                elapsed = current_time - start_time
                remaining = self.connection_timeout - elapsed
                self.logger.info(
                    "Waiting for %s connection information... (%.1fs elapsed, %.1fs remaining)",
                    server_type,
                    elapsed,
                    remaining,
                )
                last_log_time = current_time

            time.sleep(1)

    def _init_heartbeat_producer(self):
        """Initialize Kafka producer for heartbeats."""
        try:
            # Get Kafka configuration
            response = self.rpc.get("/v1/actions/get_kafka_info")

            if not response or "data" not in response:
                self.logger.error("Failed to get Kafka info for heartbeat reporter")
                return

            data = response.get("data", {})

            # Decode connection info
            ip = base64.b64decode(data["ip"]).decode("utf-8")
            port = base64.b64decode(data["port"]).decode("utf-8")
            bootstrap_servers = f"{ip}:{port}"

            # Create Kafka producer config
            kafka_config = {
                "bootstrap_servers": bootstrap_servers,
                "value_serializer": lambda v: json.dumps(v).encode("utf-8"),
                "key_serializer": lambda k: k.encode("utf-8") if k else None,
                "acks": 1,  # Wait for leader acknowledgment
                "retries": 3,
                "max_in_flight_requests_per_connection": 1,
            }

            # Add SASL authentication if available
            if "username" in data and "password" in data:
                username = base64.b64decode(data["username"]).decode("utf-8")
                password = base64.b64decode(data["password"]).decode("utf-8")

                kafka_config.update(
                    {
                        # SASL_PLAINTEXT (no TLS) is accepted and mitigated by the
                        # machine-wide private-only firewall posture (broker on the
                        # trusted private segment). Do not regress to an untrusted
                        # network without switching to SASL_SSL.
                        "security_protocol": "SASL_PLAINTEXT",
                        "sasl_mechanism": "SCRAM-SHA-256",
                        "sasl_plain_username": username,
                        "sasl_plain_password": password,
                    }
                )

            # Create producer
            self.heartbeat_producer = KafkaProducer(**kafka_config)
            self.logger.info(
                f"Kafka heartbeat producer initialized: {bootstrap_servers}, topic: {self.heartbeat_topic}"
            )

        except Exception as e:
            self.logger.error(f"Failed to initialize Kafka heartbeat producer: {e}", exc_info=True)
            self.heartbeat_producer = None

    def send_heartbeat(self, camera_configs: Dict[str, Any]) -> bool:
        """
        Send heartbeat to Kafka topic with current camera configurations.

        Handles both CameraConfig objects and plain dicts.

        Args:
            camera_configs: Dictionary of camera_id -> CameraConfig or dict

        Returns:
            True if successful, False otherwise
        """
        if not self.heartbeat_producer:
            self._init_heartbeat_producer()
        if not self.heartbeat_producer:
            return False

        try:
            # Build camera config payload — handle both CameraConfig objects and dicts
            cameras = []
            for camera_id, config in camera_configs.items():
                if isinstance(config, dict):
                    input_topic = config.get("input_topic")
                    output_topic = config.get("output_topic")
                    stream_type = (
                        config.get("stream_config", {}).get("stream_type", "unknown")
                        if isinstance(config.get("stream_config"), dict)
                        else config.get("stream_type", "unknown")
                    )
                    enabled = config.get("enabled", True)
                else:
                    input_topic = config.input_topic
                    output_topic = config.output_topic
                    stream_type = config.stream_config.get("stream_type", "unknown")
                    enabled = config.enabled
                camera_data = {
                    "camera_id": camera_id,
                    "input_topic": input_topic,
                    "output_topic": output_topic,
                    "stream_type": stream_type,
                    "enabled": enabled,
                    "management_type": "refresh",
                }
                cameras.append(camera_data)

            # Build heartbeat message
            heartbeat = {
                "app_deployment_id": self.app_deployment_id,
                "deployment_instance_id": self.deployment_instance_id,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "camera_count": len(cameras),
                "cameras": cameras,
            }

            # Send to Kafka
            future = self.heartbeat_producer.send(self.heartbeat_topic, value=heartbeat, key=self.app_deployment_id)

            # Wait for send to complete with timeout
            future.get(timeout=self.heartbeat_timeout)

            self.logger.debug(f"Heartbeat sent: {len(cameras)} cameras")
            return True

        except Exception as e:
            self.logger.error(f"Failed to send heartbeat to Kafka: {e}", exc_info=True)
            # Force reconnect on next attempt
            try:
                self.heartbeat_producer.close(timeout=2)
            except Exception as close_exc:
                self.logger.error(f"Error closing Kafka producer after send failure: {close_exc}")
            self.heartbeat_producer = None
            return False

    def close_heartbeat_producer(self):
        """Close Kafka heartbeat producer."""
        if self.heartbeat_producer:
            try:
                self.heartbeat_producer.close(timeout=5)
                self.logger.info("Kafka heartbeat producer closed")
            except Exception as e:
                self.logger.error(f"Error closing Kafka heartbeat producer: {e}")

    def initialize_refresh_listener(self, streaming_pipeline=None, event_loop=None, camera_config_monitor=None) -> bool:
        """Initialize and start the deployment refresh listener.

        Args:
            streaming_pipeline: Reference to the StreamingPipeline instance
            event_loop: Event loop for scheduling async tasks
            camera_config_monitor: Reference to CameraConfigMonitor for notifications

        Returns:
            bool: True if successfully initialized and started
        """
        try:
            if not self.deployment_instance_id and not self.instance_id:
                self.logger.error("No deployment_instance_id or instance_id provided, cannot start refresh listener")
                return False

            if self.refresh_listener and self.refresh_listener.is_listening:
                self.logger.warning("Refresh listener already running")
                return False

            self.streaming_pipeline = streaming_pipeline
            self.camera_config_monitor = camera_config_monitor

            # Get or store event loop
            if event_loop:
                self.event_loop = event_loop
            else:
                try:
                    self.event_loop = asyncio.get_running_loop()
                except RuntimeError:
                    self.logger.warning("No running event loop found, async operations may not work")
                    self.event_loop = None

            # Create refresh listener
            self.refresh_listener = DeploymentRefreshListener(
                session=self.session,
                deployment_instance_id=self.deployment_instance_id,
                on_refresh=self._trigger_api_refresh,
                instance_id=self.instance_id,
            )

            # Start listening
            success = self.refresh_listener.start()
            if success:
                self.logger.info(
                    f"Deployment refresh listener started for instance {self.deployment_instance_id} "
                    f"(PRIMARY source of truth)"
                )
            else:
                self.logger.error("Failed to start deployment refresh listener")

            return success

        except Exception as e:
            self.logger.error(f"Error initializing refresh listener: {e}", exc_info=True)
            return False

    def stop_refresh_listener(self):
        """Stop the deployment refresh listener."""
        if self.refresh_listener:
            self.refresh_listener.stop()
            self.refresh_listener = None
            self.logger.info("Deployment refresh listener stopped")

    def _trigger_api_refresh(self):
        """Trigger a full API refresh and reconcile cameras.

        Called by the refresh listener on any Kafka event or periodic timer.
        Always fetches the latest state from the API (never uses event data).
        """
        try:
            self.logger.info("API refresh triggered - fetching latest camera configs")

            new_camera_configs = self.get_camera_configs()

            if new_camera_configs is None:
                self.logger.error("API returned None - skipping refresh")
                raise RuntimeError("API returned None for camera configs")

            if not new_camera_configs:
                current_count = len(self.streaming_pipeline.camera_configs) if self.streaming_pipeline else 0
                if current_count > 0:
                    self.logger.warning(f"API returned empty configs - will remove all {current_count} cameras")

            if not self.streaming_pipeline:
                self.logger.error("No streaming pipeline - cannot reconcile")
                raise RuntimeError("No streaming pipeline reference")

            if not self.event_loop or self.event_loop.is_closed() or not self.event_loop.is_running():
                self.logger.error("Event loop not available - cannot reconcile")
                raise RuntimeError("Event loop not available")

            timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

            future = asyncio.run_coroutine_threadsafe(
                self._reconcile_cameras(new_camera_configs, timestamp), self.event_loop
            )

            def log_result(fut):
                try:
                    success = fut.result(timeout=300)
                    if success:
                        self.logger.info("API refresh reconciliation completed successfully")
                    else:
                        self.logger.error("API refresh reconciliation failed")
                except Exception as e:
                    self.logger.error(f"Exception during API refresh reconciliation: {e}")

            future.add_done_callback(log_result)

        except Exception as e:
            self.logger.error(f"Error in API refresh: {e}", exc_info=True)
            raise  # Let refresh listener track via circuit breaker

    def _log_empty_refresh_event(self) -> None:
        """Log the appropriate message for an empty-data refresh event.

        Warns when cameras will be removed, otherwise logs a no-op info line.
        Behavior mirrors the previous inline block exactly.
        """
        current_camera_count = len(self.streaming_pipeline.camera_configs) if self.streaming_pipeline else 0
        if current_camera_count > 0:
            self.logger.warning(
                f"Refresh event has EMPTY data array - this will remove ALL {current_camera_count} cameras from this instance. "
                f"This is expected during scale-down or rebalancing."
            )
        else:
            self.logger.info("Refresh event has empty data and no cameras currently configured - no action needed")

    def _event_loop_ready_for_reconcile(self) -> bool:
        """Return ``True`` when the pipeline + event loop can schedule reconciliation.

        Emits the same error logs as the previous inline guard checks for each
        failure mode (missing pipeline, missing/closed/not-running event loop).
        """
        if not self.streaming_pipeline:
            self.logger.error("No streaming pipeline reference, cannot reconcile cameras")
            return False

        if not self.event_loop:
            self.logger.error("No event loop reference, cannot schedule async operation")
            return False

        # Check event loop state comprehensively
        if self.event_loop.is_closed():
            self.logger.error("Event loop is closed, cannot schedule async operation")
            return False

        if not self.event_loop.is_running():
            self.logger.error("Event loop is not running, cannot schedule async operation")
            return False

        return True

    def _handle_refresh_event(self, event: Dict[str, Any]):
        """Handle refresh event containing full camera configuration snapshot.

        This event is sent by the backend when the deployment needs to be
        scaled or rebalanced. The backend distributes camera topics across
        deployment instances based on FPS requirements to ensure even load
        distribution.

        Backend Logic:
        1. Gets total required FPS for all cameras in the app deployment
        2. Gets all running deployment instances
        3. Calculates FPS per instance (total_fps / num_instances)
        4. Sorts output topics by camera FPS (ascending)
        5. Assigns topics to instances to balance FPS load
        6. Sends refresh event to each instance with its assigned topics

        Args:
            event: Refresh event dict with structure:
                {
                    "eventType": "refresh",
                    "streamingGatewayId": "...",  # NOTE: Key name is wrong, this is deployInstanceId
                    "timestamp": "...",
                    "data": [CameraStreamTopicResponse]
                }

                Where each CameraStreamTopicResponse contains:
                {
                    "id": "...",
                    "accountNumber": "...",
                    "cameraId": "...",
                    "streamingGatewayId": "...",
                    "serverId": "...",
                    "serverType": "redis" | "kafka",
                    "appDeploymentId": "...",
                    "topicName": "...",
                    "topicType": "input" | "output",
                    "ipAddress": "...",
                    "port": 123,
                    "consumingAppsDeploymentIds": [...],
                    "cameraFPS": 30,
                    "deployInstanceId": "..."
                }

                NOTE: Backend sends "streamingGatewayId" but the value is actually
                the deployment instance ID. The key name is incorrect in the backend.
        """
        try:
            timestamp = event.get("timestamp", "unknown")
            streaming_topics = event.get("data", [])

            self.logger.warning(
                f"Refresh event received: timestamp={timestamp}, streaming_topics={len(streaming_topics)}"
            )

            # CRITICAL: Validate that streaming_topics is not None and is a list
            if streaming_topics is None:
                self.logger.warning(
                    "Refresh event has None data - treating as empty assignment. "
                    "This will remove all cameras from this instance."
                )
                streaming_topics = []

            # Empty refresh event is VALID - it means this instance should handle NO cameras
            # This is intentional during scale-down or rebalancing
            if len(streaming_topics) == 0:
                self._log_empty_refresh_event()

            # Build camera configs from streaming topics
            new_camera_configs = self._build_camera_configs_from_streaming_topics(streaming_topics)

            self.logger.info(
                f"Built {len(new_camera_configs)} camera configs from refresh event "
                f"(from {len(streaming_topics)} streaming topics)"
            )

            # Validate we have cameras if streaming_topics was not empty
            if len(streaming_topics) > 0 and len(new_camera_configs) == 0:
                self.logger.error(
                    f"Failed to build any camera configs from {len(streaming_topics)} streaming topics - "
                    f"skipping refresh to avoid accidental removal of all cameras"
                )
                return

            # Check pipeline + event loop availability/state comprehensively
            if not self._event_loop_ready_for_reconcile():
                return

            # Schedule reconciliation on event loop with error handling
            self.logger.warning("Scheduling camera reconciliation on event loop...")
            try:
                future = asyncio.run_coroutine_threadsafe(
                    self._reconcile_cameras(new_camera_configs, timestamp),
                    self.event_loop,
                )
            except RuntimeError as e:
                self.logger.error(f"Failed to schedule reconciliation - event loop may have closed: {e}")
                return

            # Add callback to log result with timeout protection
            def log_result(fut):
                try:
                    # Use timeout to prevent indefinite blocking
                    success = fut.result(timeout=300)  # 5 minute timeout
                    if success:
                        self.logger.info("✓ Refresh reconciliation completed successfully")
                    else:
                        self.logger.error("✗ Refresh reconciliation failed")
                except TimeoutError:
                    self.logger.error("✗ Refresh reconciliation timed out after 300 seconds")
                except Exception as e:
                    self.logger.error(f"✗ Exception during refresh reconciliation: {e}", exc_info=True)

            future.add_done_callback(log_result)

        except Exception as e:
            self.logger.error(f"Error handling refresh event: {e}\nEvent: {event}", exc_info=True)

    def _build_camera_configs_from_streaming_topics(
        self, streaming_topics: List[Dict[str, Any]]
    ) -> Dict[str, CameraConfig]:
        """Build camera configurations from streaming topics data.

        Args:
            streaming_topics: List of StreamingTopics from refresh event

        Returns:
            Dict mapping camera_id to CameraConfig
        """
        camera_configs = {}

        try:
            # Group streaming topics by camera_id
            topics_by_camera = {}
            for topic in streaming_topics:
                camera_id = topic.get("cameraId")
                if not camera_id:
                    self.logger.warning(f"Streaming topic missing cameraId: {topic}")
                    continue

                if camera_id not in topics_by_camera:
                    topics_by_camera[camera_id] = {"input": None, "output": None}

                topic_type = topic.get("topicType", "").lower()
                # Default unknown/missing topicType to "output"
                if topic_type not in ("input", "output"):
                    topic_type = "output"
                topics_by_camera[camera_id][topic_type] = topic

            # Build camera config for each camera
            for camera_id, topics in topics_by_camera.items():
                try:
                    input_topic = topics.get("input")
                    output_topic = topics.get("output")

                    # Use any available topic — prefer output, fall back to input
                    source_topic = output_topic or input_topic
                    if not source_topic:
                        self.logger.warning(f"Camera {camera_id} has no topics, skipping")
                        continue
                    server_id = source_topic.get("serverId")
                    server_type = source_topic.get("serverType", "redis").lower()

                    # Get connection info: per-topic server or instance-level Redis fallback
                    connection_info = None
                    _zero_id = "000000000000000000000000"
                    if server_id and server_id != _zero_id:
                        # Validate server type
                        valid_server_types = ["redis", "kafka"]
                        if server_type not in valid_server_types:
                            self.logger.error(
                                f"Invalid server type '{server_type}' for camera {camera_id} "
                                f"(valid types: {valid_server_types}), skipping"
                            )
                            continue

                        try:
                            connection_info = self.get_and_wait_for_connection_info(server_type, server_id)
                        except Exception as e:
                            self.logger.error(
                                f"Exception getting connection info for camera {camera_id}: {e}, skipping",
                                exc_info=True,
                            )
                            continue
                    else:
                        # No per-topic server — use instance-level Redis
                        self.logger.info(f"Camera {camera_id}: no per-topic serverId, using instance Redis")
                        server_type = "redis"
                        connection_info = self.get_redis_connection_by_instance()

                    if not connection_info:
                        self.logger.error(f"Could not get connection info for camera {camera_id}, skipping")
                        continue

                    # Create stream config
                    stream_config = connection_info.copy()
                    stream_config["stream_type"] = server_type

                    # Store camera metadata for stream_info reconstruction
                    stream_config["camera_name"] = source_topic.get("cameraName", camera_id)
                    stream_config["camera_group"] = source_topic.get("cameraGroup", camera_id)
                    stream_config["location"] = source_topic.get("locationId", "Unknown Location")

                    # Validate stream_config
                    if not stream_config or "stream_type" not in stream_config:
                        self.logger.error(f"Invalid stream_config for camera {camera_id}: {stream_config}, skipping")
                        continue

                    # Log the configuration
                    input_topic_name = input_topic.get("topicName") if input_topic else None
                    output_topic_name = output_topic.get("topicName") if output_topic else None
                    self.logger.info(
                        f"Created camera config for {camera_id}: "
                        f"stream_type={server_type}, "
                        f"input_topic={input_topic_name}, "
                        f"output_topic={output_topic_name}"
                    )

                    # Create camera config
                    camera_config = CameraConfig(
                        camera_id=camera_id,
                        input_topic=input_topic_name,
                        output_topic=output_topic_name,
                        stream_config=stream_config,
                        enabled=True,
                    )

                    camera_configs[camera_id] = camera_config

                except Exception as e:
                    self.logger.error(
                        f"Error creating config for camera {camera_id}: {e}",
                        exc_info=True,
                    )
                    continue

            # Log summary of cameras and total FPS
            if camera_configs:
                camera_ids = list(camera_configs.keys())
                self.logger.info(f"Successfully built camera configs: {', '.join(camera_ids)}")

            return camera_configs

        except Exception as e:
            self.logger.error(
                f"Error building camera configs from streaming topics: {e}",
                exc_info=True,
            )
            return {}

    async def _reconcile_cameras(self, new_camera_configs: Dict[str, CameraConfig], event_timestamp: str) -> bool:
        """Reconcile pipeline cameras with new configuration snapshot.

        Performs full replacement: cameras in new_camera_configs become the
        complete set of active cameras.

        Args:
            new_camera_configs: New camera configuration dict (full snapshot)
            event_timestamp: Timestamp from refresh event

        Returns:
            bool: True if reconciliation succeeded
        """
        try:
            # Get current camera IDs
            current_ids = set(self.streaming_pipeline.camera_configs.keys()) if self.streaming_pipeline else set()
            new_ids = set(new_camera_configs.keys())

            # Determine changes
            to_remove = current_ids - new_ids
            to_add = new_ids - current_ids
            to_maybe_update = new_ids & current_ids

            # Log reconciliation plan
            self.logger.warning(
                f"Refresh reconciliation plan: "
                f"+{len(to_add)} adds, ~{len(to_maybe_update)} potential updates, "
                f"-{len(to_remove)} removes (event_timestamp={event_timestamp})"
            )

            # Execute full reconciliation on pipeline
            if self.streaming_pipeline:
                result = await self.streaming_pipeline.reconcile_camera_configs(new_camera_configs)

                if result.get("success"):
                    self.logger.info(
                        f"✓ Refresh reconciliation completed: {result['total_cameras']} cameras active "
                        f"(+{result['added']}, ~{result['updated']}, -{result['removed']})"
                    )

                    return True
                errors = result.get("errors", [])
                self.logger.error(
                    f"✗ Refresh reconciliation failed: {len(errors)} errors\n"
                    f"Errors: {errors}\n"
                    f"Keeping current configuration"
                )
                return False
            self.logger.error("No streaming pipeline available for reconciliation")
            return False

        except Exception as e:
            self.logger.error(
                f"✗ Exception during camera reconciliation: {e}\n"
                f"Event timestamp: {event_timestamp}\n"
                f"New cameras: {len(new_camera_configs)}\n"
                f"Current cameras: {len(current_ids)}\n"
                f"Keeping current configuration",
                exc_info=True,
            )
            return False
