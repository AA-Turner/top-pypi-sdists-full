from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from matrice_common.session import Session

from .constants import (
    DEFAULT_CAMERA_FPS,
    DEFAULT_CAMERA_HEIGHT,
    DEFAULT_CAMERA_QUALITY,
    DEFAULT_CAMERA_WIDTH,
    DEFAULT_OUTPUT_FPS_CAP,
    DEFAULT_STREAM_WH,
)

logger = logging.getLogger(__name__)

UNKNOWN_CAMERA = "Unknown Camera"
UNKNOWN_CAMERA_GROUP = "Unknown Camera Group"
UNKNOWN_CAMERA_LOCATION = "Unknown Camera Location"


class ConnectionAuthError(RuntimeError):
    """Raised when the control plane permanently rejects a connection-info
    request with an auth error (HTTP 401/403).

    Distinguishing this from a transient outage lets the pollers fail closed
    on revoked/invalid credentials instead of silently retrying until timeout
    (which masks the real, security-relevant reason for the failure).
    """


def _raise_if_auth_rejected(response: dict, what: str) -> None:
    """Fail closed on a permanent auth rejection in an RPC response dict.

    The RPC layer already retries 401/403 with a fresh token internally; a
    401/403 that still reaches us is a durable credential problem, not a
    transient one, so surface it immediately rather than polling to timeout.
    """
    if isinstance(response, dict) and response.get("status_code") in (401, 403):
        raise ConnectionAuthError(
            f"{what}: control plane rejected request with {response.get('status_code')} (auth); not retrying"
        )


@dataclass
class InputStream:
    """Configuration for input sources."""

    source: Union[int, str]  # Camera index, file path, or stream URL
    fps: float = DEFAULT_CAMERA_FPS  # F08: supports fractional min_fps (e.g. 2.5)
    quality: int = DEFAULT_CAMERA_QUALITY
    width: Optional[int] = DEFAULT_CAMERA_WIDTH  # 0 = native by default; inference owns preprocess
    height: Optional[int] = DEFAULT_CAMERA_HEIGHT  # 0 = native by default; inference owns preprocess
    camera_id: Optional[str] = None
    camera_key: Optional[str] = UNKNOWN_CAMERA
    camera_group_key: Optional[str] = UNKNOWN_CAMERA_GROUP
    camera_location: Optional[str] = UNKNOWN_CAMERA_LOCATION
    camera_input_topic: Optional[str] = None
    camera_connection_info: Optional[dict] = None
    simulate_video_file_stream: bool = False
    # NOTE: Default codec is h264 — matches majority of deployed RTSP cameras.
    # Accepts any case/alias (H265, HEVC, avc, etc.) — normalized downstream by StreamConfig.
    codec: str = "h264"  # "h264" or "h265"


def _mediamtx_host_is_authoritative() -> bool:
    """True when MEDIAMTX_HOST must override per-camera instance IPs (F17).

    Set by py_compute only for a managed-cluster install, where the media-server has
    no host network and is therefore reachable solely through its Kubernetes Service
    — making the compute-instance IPs from ``camera_instance_ips`` dead addresses.

    Read at call time so the flag can be flipped on a running deployment without a
    rebuilt image. Only the literal "true" counts: this suppresses a working
    resolution path, so a half-remembered truthy spelling must not silently disable
    per-camera routing on an appliance where those IPs are correct.

    KNOWN LIMITATION: the host injected today is the namespace-wide ``media-server``
    Service, whose selector matches every node's media-server, so on a MULTI-node
    managed cluster it round-robins instead of reaching the node holding the camera.
    Correct for the single-node managed clusters this targets; multi-node needs the
    per-instance Service (F17-04) wired in first.
    """
    return os.getenv("MEDIAMTX_HOST_AUTHORITATIVE", "").strip().lower() == "true"


def _parse_resolution(value: object) -> tuple[int, int]:
    """Parse a "<width>x<height>" demand string into a ``(w, h)`` int tuple.

    Returns ``(0, 0)`` for anything unusable (None, empty, malformed, or a
    non-positive dimension) so callers can treat "no valid resolution" uniformly
    and fall back to the streaming default. Case-insensitive on the ``x``.
    """
    if not value:
        return (0, 0)
    try:
        w_str, h_str = str(value).lower().split("x", 1)
        w, h = int(w_str), int(h_str)
    except (ValueError, AttributeError):
        logger.warning("[F08] Ignoring malformed resolution demand: %r", value)
        return (0, 0)
    if w <= 0 or h <= 0:
        logger.warning("[F08] Ignoring non-positive resolution demand: %r", value)
        return (0, 0)
    return (w, h)


def _coerce_fps(value: object, what: str) -> float:
    """Parse an FPS-ish field to a non-negative float; 0.0 means "unusable".

    Returns 0.0 for None, empty, non-numeric, negative, and NaN/inf so every
    caller can treat "no usable value" uniformly. ``what`` names the field in the
    warning so a malformed ``minFps`` is distinguishable from a malformed
    ``cameraFPS`` in the logs.
    """
    if value is None or value == "":
        return 0.0
    try:
        fps = float(value)
    except (TypeError, ValueError):
        logger.warning("[F08] Ignoring malformed %s: %r", what, value)
        return 0.0
    # NaN fails every comparison, so an explicit self-equality check is needed;
    # inf would otherwise sail through `> 0` and become an infinite publish rate.
    if fps != fps or fps in (float("inf"), float("-inf")) or fps <= 0:
        if fps != 0:
            logger.warning("[F08] Ignoring non-positive/non-finite %s: %r", what, value)
        return 0.0
    return fps


def resolve_operator_default_fps() -> float:
    """Resolve the operator-facing default publish rate, in FPS.

    ``MATRICE_OUTPUT_FPS`` overrides ``DEFAULT_OUTPUT_FPS_CAP`` (10). A value of
    ``0`` (or negative) means "cap disabled" and is returned as ``0.0`` —
    callers must treat 0 as "no ceiling", matching
    ``nvdec._resolve_output_interval_ns``, which returns interval 0 for the same
    input. A missing or malformed value falls back to the default rather than
    silently disabling the cap.
    """
    raw = os.environ.get("MATRICE_OUTPUT_FPS")
    if raw is None or raw.strip() == "":
        return DEFAULT_OUTPUT_FPS_CAP
    try:
        fps = float(raw)
    except ValueError:
        logger.warning(
            "[F08] Malformed MATRICE_OUTPUT_FPS=%r — falling back to %.1f fps",
            raw,
            DEFAULT_OUTPUT_FPS_CAP,
        )
        return DEFAULT_OUTPUT_FPS_CAP
    if fps <= 0:
        return 0.0  # cap explicitly disabled
    return fps


def resolve_publish_fps(demand_fps: float, camera_fps: float) -> float:
    """Resolve a camera's PUBLISH rate from app demand and the camera's rate.

    The rule, single-sourced here so no code path can drift:

    * ``demand_fps > 0`` — the aggregated ``max(minFps)`` across the apps
      consuming this camera wins outright, even when it exceeds the operator
      default. That is the F08 contract: an app that declares it needs 15 fps
      gets 15 fps.
    * otherwise (no demand declared, malformed, or the lookup failed) —
      ``min(operator_default, camera_fps)``. Falling back to ``camera_fps``
      alone is what broke the cap; falling back to the operator default alone
      would "cap" a 5 fps camera at 10, which is a no-op.

    ``camera_fps <= 0`` (unknown source rate) yields the operator default.
    A disabled cap (``MATRICE_OUTPUT_FPS=0``) yields ``camera_fps``, i.e. publish
    every decoded frame, and ``0.0`` when the source rate is also unknown —
    which the publish gate reads as "cap disabled".
    """
    demand = _coerce_fps(demand_fps, "minFps demand")
    if demand > 0:
        return demand

    source = _coerce_fps(camera_fps, "cameraFPS")
    operator_default = resolve_operator_default_fps()
    if operator_default <= 0:
        # Cap disabled: publish at the source rate (0.0 == unknown == no gate).
        return source
    if source <= 0:
        return operator_default
    return min(operator_default, source)


def _aggregate_camera_demand(topics: List[dict]) -> Dict[str, dict]:
    """Reduce per-(app, camera) consuming-topic rows to one demand per camera.

    The consuming-topics API returns one row per (app, camera) with the app's
    ``minFps`` and ``cameraResolution`` (its ``min_resolution``). F08 runs each
    camera at the floor that still serves its most-demanding app, so we take
    ``max(min_fps)`` and the element-wise ``max`` of ``min_resolution`` across
    the apps consuming that camera (replacing the old first-row dedup).

    ``minFps`` does NOT fall back to ``cameraFPS``. ``cameraFPS`` is the camera's
    SOURCE rate, not a demand — using it as one set every camera's publish target
    to its own source rate, which made the publish cap a no-op (the phase
    accumulator passes every frame when ``source_fps <= target_fps``). It is
    aggregated separately as ``camera_fps`` and used only as the ceiling of the
    no-demand fallback in :func:`resolve_publish_fps`.

    Returns ``{camera_id: {"fps", "camera_fps", "w", "h", "base"}}`` where
    ``base`` is the first row seen for that camera (used for codec/name/topic
    fields). ``fps``/``w``/``h`` are the raw aggregated maxima (0 = undeclared)
    and ``camera_fps`` is the max reported source rate; the caller applies the
    fallback and the clamp-to-camera.
    """
    by_cam: Dict[str, dict] = {}
    for t in topics:
        cid = t.get("cameraId")
        if not cid:
            continue
        agg = by_cam.get(cid)
        if agg is None:
            agg = {"fps": 0.0, "camera_fps": 0.0, "w": 0, "h": 0, "base": t}
            by_cam[cid] = agg
        # Two SEPARATE quantities, deliberately not collapsed into one:
        #   fps        = declared app demand (max minFps). 0 when undeclared.
        #   camera_fps = the camera's own source rate (cameraFPS).
        # cameraFPS is still very much used — most cameras declare no minFps, and
        # for those resolve_publish_fps() falls back to
        # min(MATRICE_OUTPUT_FPS, camera_fps), so cameraFPS is the CEILING of the
        # fallback (a 4 fps camera publishes 4, never a pointless "cap" at 10).
        # What it must never be again is the demand VALUE: `minFps or cameraFPS`
        # made every camera's publish target equal its own source rate, so
        # _should_publish_frame's `source_fps <= target_fps` passed every frame and
        # the cap dropped nothing.
        agg["fps"] = max(agg["fps"], _coerce_fps(t.get("minFps"), "minFps demand"))
        agg["camera_fps"] = max(agg["camera_fps"], _coerce_fps(t.get("cameraFPS"), "cameraFPS"))
        w, h = _parse_resolution(t.get("cameraResolution"))
        agg["w"], agg["h"] = max(agg["w"], w), max(agg["h"], h)
    return by_cam


def _resolve_stream_demand(agg: dict) -> tuple[float, int, int]:
    """Apply the F08 fallbacks to a raw aggregated demand.

    - FPS: ``max(minFps)`` when declared, else ``min(operator default,
      cameraFPS)`` — see :func:`resolve_publish_fps`. Previously an undeclared
      demand fell through to a bare ``DEFAULT_STREAM_FPS``, but
      ``_aggregate_camera_demand`` was promoting ``cameraFPS`` to a demand, so in
      practice the target became the source rate and the cap never fired.
    - Resolution: undeclared or partial -> NATIVE (``DEFAULT_STREAM_WH`` = (0, 0),
      i.e. the SG performs no resize). The app always letterboxes to its model
      input size, so an undeclared camera streams native and each consumer
      downscales itself.

    Clamp-to-camera happens downstream where native/source dims are known.
    """
    fps = resolve_publish_fps(agg.get("fps", 0.0), agg.get("camera_fps", 0.0))
    w, h = (agg["w"], agg["h"]) if agg["w"] > 0 and agg["h"] > 0 else DEFAULT_STREAM_WH
    return fps, w, h


class StreamingGatewayUtil:
    def __init__(
        self,
        session: Session,
        streaming_gateway_id: str,
        server_id: Optional[str] = None,
        action_id: Optional[str] = None,
    ):
        self.session = session
        self.streaming_gateway_id = streaming_gateway_id
        self.server_id = server_id
        self.action_id = action_id
        if not self.server_id and self.streaming_gateway_id:
            self.server_id = self.get_streaming_gateway_by_id().get("serverId")

        # Initialize heartbeat reporter for Kafka
        self._heartbeat_reporter = None
        self._init_heartbeat_reporter()

    def _init_heartbeat_reporter(self):
        """Initialize the Kafka heartbeat reporter."""
        try:
            from .metrics_reporter import HeartbeatReporter

            self._heartbeat_reporter = HeartbeatReporter(  # type: ignore[assignment]
                self.session,
                self.streaming_gateway_id,
                topic="streaming_gateway_heartbeat",
            )
            logger.info("Heartbeat reporter initialized for streaming gateway")
        except Exception as e:
            logger.warning(f"Failed to initialize heartbeat reporter: {e}")

    def _parse_response(self, resp: dict):
        if resp.get("success"):
            return resp.get("data")
        logger.error("Request failed with payload: %s", resp, exc_info=True)
        return None

    def get_streaming_gateway_by_id(self):
        if not self.streaming_gateway_id:
            raise ValueError("Streaming gateway ID is required")
        return self._parse_response(
            self.session.rpc.get(f"/v1/inference/get_streaming_gateways/{self.streaming_gateway_id}")
        )

    #     {'id': '68c43cee7b628ecd0d44c0ca',  # pragma: allowlist secret
    #   'accountNumber': '2276842692221978464767135',
    #   'accountType': 'enterprise',
    #   'gatewayName': 'Test_App_Deployment',
    #   'description': 'Testing',
    #   'status': 'created',
    #   'actionRecordID': '000000000000000000000000',
    #   'startTime': '0001-01-01T00:00:00Z',
    #   'lastStreamTime': '0001-01-01T00:00:00Z',
    #   'serverId': '68c43ceed0e26ec0da43eb3a',  # pragma: allowlist secret
    #   'serverType': 'redis',
    #   'networkSettings': {'IPAddress': '0.0.0.0',
    #    'port': 80,
    #    'accessScale': 'regional',
    #    'region': 'US'},
    #   'userID': '6819bdda7481e811e530a84a',  # pragma: allowlist secret
    #   'createdAt': '2025-09-12T15:31:58.359Z',
    #   'updatedAt': '2025-09-12T15:31:59.298Z'}

    def start_streaming(self) -> Optional[Dict]:
        """
        Start the streaming gateway.

        Returns:
            Dict: API response data or None if failed
        """
        path = f"/v1/inference/start_streaming_gateway/{self.streaming_gateway_id}"

        resp = self.session.rpc.post(path=path, payload={})

        return self._parse_response(resp)

    def stop_streaming(self) -> Optional[Dict]:
        """
        Stop the streaming gateway.

        Returns:
            Dict: API response data or None if failed
        """
        path = f"/v1/inference/stop_streaming_gateway/{self.streaming_gateway_id}"

        resp = self.session.rpc.post(path=path, payload={})

        return self._parse_response(resp)

    def update_status(self, status: str) -> Optional[Dict]:
        """
        Update the status of the streaming gateway.

        Args:
            status: New status (active, inactive, starting, stopped, etc.)

        Returns:
            Dict: API response data or None if failed
        """
        if not status:
            logger.error("Status is required", exc_info=True)
            return None

        # Use PUT endpoint with status in query params
        path = f"/v1/inference/update_streaming_gateway_status/{self.streaming_gateway_id}?status={status}"

        resp = self.session.rpc.put(path=path, payload={})

        logger.info(f"Updated streaming gateway status to: {status}")
        return self._parse_response(resp)

    def get_and_wait_for_connection_info(
        self,
        server_type: Optional[str] = None,
        server_id: Optional[str] = None,
        connection_timeout: int = 300,
    ) -> Dict:
        """Get and wait for connection information for the streaming gateway.

        Args:
            server_type: Type of server ('kafka' or 'redis'). Required.
            server_id: ID of the server. If not provided, uses self.server_id.
            connection_timeout: Timeout in seconds to wait for connection info (default: 300).

        Returns:
            Dict: Connection configuration

        Raises:
            ValueError: If server_type or server_id is not provided
            RuntimeError: If timeout is reached while waiting for connection info
        """
        # Use provided server_id or fall back to instance server_id
        server_id = server_id or self.server_id

        if not server_id:
            raise ValueError("Server ID is required (provide server_id parameter or set self.server_id)")
        if not server_type:
            raise ValueError("Server type is required")

        def _get_kafka_connection_info():
            try:
                response = self.session.rpc.get(f"/v1/actions/get_kafka_server/{server_id}")
                if response.get("success", False):
                    data = response.get("data")
                    if data and data.get("ipAddress") and data.get("port") and data.get("status") == "running":
                        # SECURITY: SASL_PLAINTEXT gives no channel encryption.
                        # Accepted, documented dependency on the machine-wide
                        # private-only firewall posture (broker reachable only
                        # over the trusted/localhost subnet). Do not silently
                        # regress to a public bind without SASL_SSL + CA verify.
                        return {
                            "bootstrap_servers": f"{data['ipAddress']}:{data['port']}",
                            "sasl_mechanism": "SCRAM-SHA-256",
                            "sasl_username": os.environ.get("KAFKA_SASL_USERNAME"),
                            "sasl_password": os.environ.get("KAFKA_SASL_PASSWORD"),
                            "security_protocol": "SASL_PLAINTEXT",
                        }
                    logger.debug("Kafka connection information is not complete, waiting...")
                    return None
                _raise_if_auth_rejected(response, "Kafka connection info")
                logger.debug(
                    "Failed to get Kafka connection information: %s",
                    response.get("message", "Unknown error"),
                )
                return None
            except ConnectionAuthError:
                raise
            except Exception as exc:
                logger.debug("Exception getting Kafka connection info: %s", str(exc))
                return None

        def _get_redis_connection_info():
            try:
                # Build URL with actionId query parameter if available
                url = f"/v1/actions/redis_servers/{server_id}"
                if self.action_id:
                    url += f"?actionId={self.action_id}"
                response = self.session.rpc.get(url)
                if response.get("success", False):
                    data = response.get("data")
                    if (
                        data
                        # TODO: Check why BE is giving host as empty while in the DB it is localhost
                        and data.get("port")
                        and data.get("status") == "running"
                    ):
                        return {
                            "host": data.get("host") or "localhost",
                            "port": int(data["port"]),
                            "password": data.get("password", ""),
                            "username": data.get("username"),
                            "db": data.get("db", 0),
                            "connection_timeout": 30,
                        }
                    logger.debug("Redis connection information is not complete, waiting...")
                    return None
                _raise_if_auth_rejected(response, "Redis connection info")
                logger.debug(
                    "Failed to get Redis connection information: %s",
                    response.get("message", "Unknown error"),
                )
                return None
            except ConnectionAuthError:
                raise
            except Exception as exc:
                logger.debug("Exception getting Redis connection info: %s", str(exc))
                return None

        start_time = time.time()
        last_log_time = 0.0
        poll_interval = 0.5
        max_poll_interval = 10.0

        while True:
            current_time = time.time()

            # Get connection info based on server type
            connection_info = None
            if server_type == "kafka":
                connection_info = _get_kafka_connection_info()
            elif server_type == "redis":
                connection_info = _get_redis_connection_info()
            else:
                raise ValueError(f"Unsupported server type: {server_type}")

            # If we got valid connection info, return it
            if connection_info:
                logger.info("Successfully retrieved %s connection information", server_type)
                return connection_info

            # Check timeout
            if current_time - start_time > connection_timeout:
                error_msg = (
                    f"Timeout waiting for {server_type} connection information after {connection_timeout} seconds"
                )
                logger.error(error_msg)

                # Log the last response for debugging
                try:
                    if server_type == "kafka":
                        response = self.session.rpc.get(f"/v1/actions/get_kafka_server/{server_id}")
                    else:
                        url = f"/v1/actions/redis_servers/{server_id}"
                        if self.action_id:
                            url += f"?actionId={self.action_id}"
                        response = self.session.rpc.get(url)
                    logger.error("Last response received: %s", response)
                except Exception as exc:
                    logger.exception("Failed to get last response for debugging: %s", str(exc))

                raise RuntimeError(error_msg)

            # Log waiting message every 10 seconds to avoid spam
            if current_time - last_log_time >= 10:
                elapsed = current_time - start_time
                remaining = connection_timeout - elapsed
                logger.info(
                    "Waiting for %s connection information... (%.1fs elapsed, %.1fs remaining)",
                    server_type,
                    elapsed,
                    remaining,
                )
                last_log_time = current_time

            time.sleep(poll_interval)
            poll_interval = min(max_poll_interval, poll_interval * 1.5)

    def send_heartbeat(self, camera_config: Optional[Dict] = None) -> bool:
        """
        Send a heartbeat to the streaming gateway via Kafka.

        Args:
            camera_config: Camera configuration data to include in heartbeat
                           Should contain 'cameras' list and 'stats' dict

        Returns:
            bool: True if heartbeat sent successfully, False otherwise
        """
        if not self.streaming_gateway_id:
            raise ValueError("Streaming gateway ID is required")

        if not self._heartbeat_reporter:
            logger.warning("Heartbeat reporter not initialized, cannot send heartbeat")
            return False

        # Use provided camera_config or empty structure
        config = camera_config or {"cameras": [], "stats": {}}

        # Send via Kafka
        try:
            success = self._heartbeat_reporter.send_heartbeat(config)
            return success
        except Exception as e:
            logger.exception(f"Failed to send heartbeat: {e}")
            return False


def input_stream_to_camera_config(input_stream: InputStream) -> Dict:
    """Convert InputStream dataclass to camera_config dict for WorkerManager.

    This adapter function converts the InputStream configuration format used by
    StreamingGateway to the dictionary format expected by WorkerManager and
    AsyncCameraWorker.

    Args:
        input_stream: InputStream dataclass instance

    Returns:
        Dict compatible with WorkerManager/AsyncCameraWorker
    """
    return {
        "stream_key": input_stream.camera_key or f"camera_{input_stream.camera_id}",
        "camera_id": input_stream.camera_id,
        "source": input_stream.source,
        "topic": input_stream.camera_input_topic or f"{input_stream.camera_id}_input_topic",
        "fps": input_stream.fps,
        "quality": input_stream.quality,
        "width": input_stream.width,
        "height": input_stream.height,
        "camera_location": input_stream.camera_location or "Unknown",
        "stream_group_key": input_stream.camera_group_key or "default",
        "simulate_video_file_stream": input_stream.simulate_video_file_stream,
        "codec": input_stream.codec,
    }


class InstanceStreamingGatewayUtil:
    """Instance-based streaming gateway utility.

    Uses compute instance_id as the primary key for all API calls,
    replacing the old streaming_gateway_id-based flow. A single
    get_consuming_topics() call replaces the old cameras + groups + topics calls.
    """

    def __init__(
        self,
        session: Session,
        instance_id: str,
        action_id: Optional[str] = None,
        instance_string_id: Optional[str] = None,
    ):
        self.session = session
        self.instance_id = instance_id
        self.action_id = action_id
        self.instance_string_id = instance_string_id or instance_id
        self._cached_consuming_topics: Optional[List[dict]] = None

    def _parse_response(self, resp: dict):
        if resp.get("success"):
            return resp.get("data")
        logger.error("Request failed with payload: %s", resp, exc_info=True)
        return None

    def get_consuming_topics(self) -> List[dict]:
        """Get all consuming topics (input+output) for this instance in a single API call.

        Returns:
            List of CameraStreamTopicResponse dicts with keys:
            cameraId, topicName, appDeploymentId, serverId, serverType,
            ipAddress, port, cameraFPS, streamingGatewayId, topicType, isActive
        """
        try:
            data = self._parse_response(
                self.session.rpc.get(f"/v1/inference/get_app_deployment_consuming_topics/{self.instance_id}")
            )
            result = data if data else []
            self._cached_consuming_topics = result
            return result
        except Exception as e:
            logger.exception(f"Failed to get consuming topics for instance {self.instance_id}: {e}")
            return []

    def get_output_topics_by_app_deployment(self, app_deployment_id: str) -> List[dict]:
        """Get output topics filtered by app deployment + instance."""
        try:
            data = self._parse_response(
                self.session.rpc.get(
                    f"/v1/inference/get_output_topics_by_app_deployment_and_instance/{app_deployment_id}/{self.instance_id}"
                )
            )
            return data if data else []
        except Exception as e:
            logger.exception(f"Failed to get output topics for app deployment {app_deployment_id}: {e}")
            return []

    def get_camera_instance_ips(self, camera_ids: List[str]) -> Dict[str, str]:
        """Resolve camera IDs to their hosting instance IPs.

        Args:
            camera_ids: List of camera IDs to resolve

        Returns:
            Dict mapping camera_id to instance IP address
        """
        try:
            data = self._parse_response(
                self.session.rpc.post(
                    "/v1/inference/camera_instance_ips",
                    payload={"cameraIds": camera_ids},
                )
            )
            return data if data else {}
        except Exception as e:
            logger.exception(f"Failed to get camera instance IPs: {e}")
            return {}

    def _resolve_camera_ips(self, camera_ids: List[str], fallback_host: str) -> Dict[str, str]:
        """Resolve camera IDs to MediaMTX instance IPs with fallback.

        Calls the camera_instance_ips API to get per-camera private IPs.
        Falls back to fallback_host for any camera that fails to resolve.

        Args:
            camera_ids: List of camera IDs to resolve
            fallback_host: Fallback hostname if resolution fails

        Returns:
            Dict mapping camera_id to resolved IP (or fallback_host)
        """
        if not camera_ids:
            return {}

        # F17: on a cluster that forbids host networking, the per-camera addresses
        # from camera_instance_ips are unusable. They are compute-instance (node)
        # IPs, and the media-server no longer binds the node — it is reachable only
        # through its Service. Worse, they would WIN over MEDIAMTX_HOST below, so
        # injecting the Service DNS alone is silently defeated and every camera
        # produces no frames with no error anywhere.
        #
        # MEDIAMTX_HOST_AUTHORITATIVE makes the injected host win. Set by py_compute
        # only in managed-cluster mode; unset everywhere else, so VM mode and the
        # appliance keep resolving per-camera IPs exactly as before (which is
        # correct there — the node IP is where the media-server actually binds).
        if _mediamtx_host_is_authoritative():
            logger.info(
                f"[Instance] MEDIAMTX_HOST is authoritative ({fallback_host}); "
                f"skipping camera_instance_ips for all {len(camera_ids)} cameras"
            )
            return {cid: fallback_host for cid in camera_ids}

        try:
            camera_ips = self.get_camera_instance_ips(camera_ids)
            if camera_ips:
                resolved = {cid for cid, ip in camera_ips.items() if ip}
                unresolved = set(camera_ids) - resolved
                if unresolved:
                    logger.warning(
                        f"[Instance] {len(unresolved)} cameras could not resolve instance IP, "
                        f"falling back to {fallback_host}: {list(unresolved)[:5]}"
                    )
                logger.info(f"[Instance] Resolved MediaMTX IPs for {len(resolved)}/{len(camera_ids)} cameras")
                # Fill in fallback for unresolved or empty IPs
                for cid in camera_ids:
                    if not camera_ips.get(cid):
                        camera_ips[cid] = fallback_host
                return camera_ips
            logger.warning(
                f"[Instance] camera_instance_ips API returned empty, "
                f"falling back to {fallback_host} for all {len(camera_ids)} cameras"
            )
            return {cid: fallback_host for cid in camera_ids}
        except Exception as e:
            logger.warning(
                f"[Instance] Failed to resolve camera instance IPs: {e}, "
                f"falling back to {fallback_host} for all {len(camera_ids)} cameras"
            )
            return {cid: fallback_host for cid in camera_ids}

    def get_and_wait_for_redis_connection_info(self, connection_timeout: int = 300) -> Dict:
        """Get Redis connection info by instance ID, polling until ready.

        Supports Redis Sentinel — if the API response includes sentinelHosts,
        the returned dict will contain sentinel_hosts and master_name.

        Args:
            connection_timeout: Timeout in seconds (default: 300)

        Returns:
            Dict with host, port, password, username, db, connection_timeout,
            and optionally sentinel_hosts and master_name

        Raises:
            RuntimeError: If timeout is reached
        """
        start_time = time.time()
        last_log_time = 0.0

        while True:
            current_time = time.time()

            try:
                url = f"/v1/actions/get_redis_server_by_instance_id/{self.instance_string_id}"
                if self.action_id:
                    url += f"?actionId={self.action_id}"
                response = self.session.rpc.get(url)
                _raise_if_auth_rejected(response, "Redis connection info")
                if response.get("success", False):
                    data = response.get("data")
                    if data and data.get("port") and data.get("status") == "running":
                        conn = {
                            "host": data.get("host") or "localhost",
                            "port": int(data["port"]),
                            "password": data.get("password", ""),
                            "username": data.get("username"),
                            "db": data.get("db", 0),
                            "connection_timeout": 30,
                        }
                        # Sentinel support — sentinelConfig is a nested object
                        sentinel_cfg = data.get("sentinelConfig") or {}
                        if sentinel_cfg.get("sentinelHosts"):
                            conn["sentinel_hosts"] = [(h, 26379) for h in sentinel_cfg["sentinelHosts"]]
                            conn["master_name"] = sentinel_cfg.get("masterName")
                            logger.info(
                                "Redis Sentinel detected for instance %s: master=%s, sentinels=%d",
                                self.instance_id,
                                conn["master_name"],
                                len(conn["sentinel_hosts"]),
                            )
                        logger.info(
                            "Successfully retrieved Redis connection info for instance %s",
                            self.instance_id,
                        )
                        return conn
            except ConnectionAuthError:
                raise
            except Exception as exc:
                logger.debug("Exception getting Redis connection info: %s", str(exc))

            # Check timeout
            if current_time - start_time > connection_timeout:
                error_msg = (
                    f"Timeout waiting for Redis connection info for instance "
                    f"{self.instance_id} after {connection_timeout} seconds"
                )
                logger.error(error_msg)
                raise RuntimeError(error_msg)

            # Log every 10 seconds
            if current_time - last_log_time >= 10:
                elapsed = current_time - start_time
                remaining = connection_timeout - elapsed
                logger.info(
                    "Waiting for Redis connection info (instance %s)... (%.1fs elapsed, %.1fs remaining)",
                    self.instance_id,
                    elapsed,
                    remaining,
                )
                last_log_time = current_time

            time.sleep(1)

    def get_input_streams(
        self,
        mediamtx_host: str = "localhost",
        mediamtx_port: int = 8554,
    ) -> List[InputStream]:
        """Get camera input streams from consuming topics for this instance.

        Args:
            mediamtx_host: MediaMTX RTSP server hostname (fallback if IP resolution fails)
            mediamtx_port: MediaMTX RTSP server port

        Returns:
            List[InputStream] configurations
        """
        start = time.time()
        topics = self.get_consuming_topics()
        elapsed = time.time() - start
        logger.info(f"[Instance] Fetched {len(topics)} consuming topics in {elapsed:.3f}s")

        if not topics:
            logger.warning("[Instance] No consuming topics found for instance %s", self.instance_id)
            return []

        # F08: aggregate per-(app, camera) rows to one demand per camera —
        # target_fps = max(min_fps), target_resolution = max(min_resolution) —
        # replacing the old first-row-wins dedup. Fallbacks when undeclared:
        # FPS -> 10, resolution -> native (no SG resize).
        by_cam = _aggregate_camera_demand(topics)
        logger.info(f"[Instance] {len(topics)} raw topics -> {len(by_cam)} unique cameras")

        # Resolve per-camera instance IPs for cross-instance streaming
        fallback_host = os.getenv("MEDIAMTX_HOST", mediamtx_host)
        camera_ips = self._resolve_camera_ips(list(by_cam.keys()), fallback_host)

        input_streams = []
        for camera_id, agg in by_cam.items():
            topic = agg["base"]
            fps, width, height = _resolve_stream_demand(agg)

            camera_host = camera_ips.get(camera_id, fallback_host)
            source = f"rtsp://{camera_host}:{mediamtx_port}/{camera_id}"

            input_stream = InputStream(
                source=source,
                fps=fps,
                quality=DEFAULT_CAMERA_QUALITY,
                width=width,
                height=height,
                camera_id=camera_id,
                camera_key=topic.get("cameraName", UNKNOWN_CAMERA),
                camera_group_key=topic.get("cameraGroup", UNKNOWN_CAMERA_GROUP),
                camera_location=topic.get("locationId", UNKNOWN_CAMERA_LOCATION),
                camera_input_topic=topic.get("topicName"),
                camera_connection_info=topic,
                simulate_video_file_stream=False,
            )
            input_streams.append(input_stream)

        logger.info(f"[Instance] Created {len(input_streams)} input streams for instance {self.instance_id}")
        return input_streams

    def get_nvdec_input_streams(
        self,
        mediamtx_host: str = "localhost",
        mediamtx_port: int = 8554,
    ) -> List[InputStream]:
        """Get camera input streams with codec detection for NVDEC hardware decode.

        Same as get_input_streams() but adds per-camera codec detection.

        Args:
            mediamtx_host: MediaMTX RTSP server hostname (fallback if IP resolution fails)
            mediamtx_port: MediaMTX RTSP server port

        Returns:
            List[InputStream] configurations with codec info
        """
        start = time.time()
        topics = self.get_consuming_topics()
        elapsed = time.time() - start
        logger.info(f"[Instance/NVDEC] Fetched {len(topics)} consuming topics in {elapsed:.3f}s")

        if not topics:
            logger.warning(
                "[Instance/NVDEC] No consuming topics found for instance %s",
                self.instance_id,
            )
            return []

        from matrice_streaming.streaming_gateway.camera_streamer.codec_detect import (
            normalize_codec,
        )

        # F08: aggregate per-(app, camera) rows to one demand per camera —
        # target_fps = max(min_fps), target_resolution = max(min_resolution) —
        # replacing the old first-row-wins dedup. Fallbacks when undeclared:
        # FPS -> 10, resolution -> native (no SG resize).
        by_cam = _aggregate_camera_demand(topics)
        logger.info(f"[Instance/NVDEC] {len(topics)} raw topics -> {len(by_cam)} unique cameras")

        # Resolve per-camera instance IPs for cross-instance streaming
        fallback_host = os.getenv("MEDIAMTX_HOST", mediamtx_host)
        camera_ips = self._resolve_camera_ips(list(by_cam.keys()), fallback_host)

        input_streams = []
        for camera_id, agg in by_cam.items():
            topic = agg["base"]
            fps, width, height = _resolve_stream_demand(agg)

            camera_host = camera_ips.get(camera_id, fallback_host)
            source = f"rtsp://{camera_host}:{mediamtx_port}/{camera_id}"

            # Field-name precedence matches build_nvdec_camera_config in
            # dynamic_camera_manager.py: cameraCodec (canonical v1 API field)
            # → videoCodec (legacy) → video_codec (snake-case fallback).
            cam_codec = normalize_codec(topic.get("cameraCodec") or topic.get("videoCodec") or topic.get("video_codec"))

            input_stream = InputStream(
                source=source,
                fps=fps,
                quality=DEFAULT_CAMERA_QUALITY,
                width=width,
                height=height,
                camera_id=camera_id,
                camera_key=topic.get("cameraName", UNKNOWN_CAMERA),
                camera_group_key=topic.get("cameraGroup", UNKNOWN_CAMERA_GROUP),
                camera_location=topic.get("locationId", UNKNOWN_CAMERA_LOCATION),
                camera_input_topic=topic.get("topicName"),
                camera_connection_info=topic,
                simulate_video_file_stream=False,
                codec=cam_codec,
            )
            input_streams.append(input_stream)

        logger.info(f"[Instance/NVDEC] Created {len(input_streams)} input streams for instance {self.instance_id}")
        return input_streams

    # Lifecycle methods — delegate to existing gateway-id endpoints
    # The streamingGatewayId comes from the consuming topics response

    def start_streaming(self, gateway_id: str) -> Optional[Dict]:
        """Start the streaming gateway by gateway ID."""
        path = f"/v1/inference/start_streaming_gateway/{gateway_id}"
        resp = self.session.rpc.post(path=path, payload={})
        return self._parse_response(resp)

    def stop_streaming(self, gateway_id: str) -> Optional[Dict]:
        """Stop the streaming gateway by gateway ID."""
        path = f"/v1/inference/stop_streaming_gateway/{gateway_id}"
        resp = self.session.rpc.post(path=path, payload={})
        return self._parse_response(resp)

    def update_status(self, gateway_id: str, status: str) -> Optional[Dict]:
        """Update the status of the streaming gateway by gateway ID."""
        if not status:
            logger.error("Status is required", exc_info=True)
            return None
        path = f"/v1/inference/update_streaming_gateway_status/{gateway_id}?status={status}"
        resp = self.session.rpc.put(path=path, payload={})
        logger.info(f"Updated streaming gateway {gateway_id} status to: {status}")
        return self._parse_response(resp)


def build_stream_config_for_instance(
    instance_util: InstanceStreamingGatewayUtil,
    service_id: str,
    stream_maxlen: Optional[int] = None,
) -> Dict:
    """Build stream_config dict from instance-based Redis connection info.

    Args:
        instance_util: InstanceStreamingGatewayUtil instance
        service_id: Streaming gateway ID (used as service_id)
        stream_maxlen: Maximum entries per Redis stream (approximate mode)

    Returns:
        Dict with connection configuration for WorkerManager
    """
    conn = instance_util.get_and_wait_for_redis_connection_info()
    stream_config = {
        **conn,
        "service_id": service_id,
    }
    # Sentinel hosts are already parsed as tuples by get_and_wait_for_redis_connection_info
    stream_config.update(
        {
            "pool_max_connections": 500,
            "enable_batching": True,
            "batch_size": 10,
            "batch_timeout": 0.01,
            "stream_maxlen": stream_maxlen,
        }
    )
    return stream_config
