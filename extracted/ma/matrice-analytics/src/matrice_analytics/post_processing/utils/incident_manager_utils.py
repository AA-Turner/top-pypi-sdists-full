"""
incident_manager_utils.py

Manages incident publishing to Redis/Kafka when severity levels change.
Implements consecutive-frame validation before publishing:
- 5 consecutive frames for medium/significant/critical
- 10 consecutive frames for low (stricter)
- 50 consecutive empty frames to send 'info' (incident ended)

Polls 'incident_modification_config' topic for dynamic threshold settings.
Publishes to 'incident_res' topic.

PRODUCTION-READY VERSION
"""

import json
import logging
import os
import random
import re
import string
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .location_name_cache import LocationNameCache

# Severity level ordering for comparison (none = no incident)
SEVERITY_LEVELS = ["none", "info", "low", "medium", "significant", "critical"]

# Default thresholds if none provided (fire-style incident_quant / coverage %).
# low was previously 0.0001 (effectively any non-zero); keep it tight but
# above noise so tiny freckles do not open after CONSECUTIVE_FRAMES_LOW.
DEFAULT_THRESHOLDS = [
    {"level": "low", "percentage": 1},
    {"level": "medium", "percentage": 3},
    {"level": "significant", "percentage": 13},
    {"level": "critical", "percentage": 30},
]

# Weapon detection: incident_quant is max confidence % (not fire area intensity)
WEAPON_DEFAULT_THRESHOLDS = [
    {"level": "low", "percentage": 27},
    {"level": "medium", "percentage": 40},
    {"level": "critical", "percentage": 70},
]

# Loitering: incident_quant is zone occupancy % (loiterers / threshold * 100)
LOITERING_DEFAULT_THRESHOLDS = [
    {"level": "low", "percentage": 1},
    {"level": "medium", "percentage": 5},
    {"level": "significant", "percentage": 15},
    {"level": "critical", "percentage": 25},
]

# Overcrowding: incident_quant is zone occupancy % (count / capacity * 100), and
# overcrowding_detection.py only ever computes/emits it while a zone is already
# flagged "overcrowded" -- which its own state machine never sets below 100%
# (high_severity_percent). It escalates to "critical" at 120% (critical_severity_percent).
# Without this table, incident_quant (typically 100-200+) fell through to
# DEFAULT_THRESHOLDS -- calibrated for fire's coverage-% scale, critical at just 30% --
# so every overcrowding incident silently reported "critical", discarding the app's own
# "high" grading below 120%. Two rungs only: intermediate ones would be dead code, since
# incident_quant can't land below 100 on this app's normal active path.
OVERCROWDING_DEFAULT_THRESHOLDS = [
    {"level": "significant", "percentage": 100},
    {"level": "critical", "percentage": 120},
]

# Cache for location names to avoid repeated API calls
_location_name_cache = LocationNameCache()


@dataclass
class IncidentState:
    """Tracks the current incident state for a camera/usecase."""

    current_level: str = "none"  # Current confirmed severity level
    pending_level: str = "none"  # Level being validated (needs consecutive frames)
    consecutive_count: int = 0  # Consecutive frames with pending_level
    last_published_level: str = "none"  # Last level that was published (for spam prevention)
    incident_cycle_id: int = 1  # Starts at 1, incremented when cycle resets (after info sent)
    empty_frames_count: int = 0  # Consecutive empty incident frames (for "info" detection)
    current_incident_id: str = ""  # Current incident_id for this cycle (managed per camera)
    incident_active: bool = False  # Whether an incident is currently active in this cycle
    active_incident_type: str = ""  # incident_type from the open event in this cycle
    start_time: str = ""  # ISO-8601 UTC set on first publish in this cycle
    last_detection_at: float = 0.0
    """``time.monotonic()`` of the last real detection frame; 0.0 = none yet.

    Monotonic, and named for it. This field was read through ``time.time()`` to decide
    when to close an idle incident -- the exact "wall clock as CONTROL LOGIC" case the
    central rule singles out. An edge device that boots with a dead RTC and steps its
    clock once the network arrives makes the delta negative, and a negative idle time
    never reaches ``IDLE_CLOSE_SEC``, so the incident stays open forever; a forward step
    closes one that is still live. Renamed rather than merely retyped, so nobody reseeds
    it from a wall clock later.
    """

    # --- Rolling-window close logic (replaces consecutive-empty-frames check) ---
    # We close the cycle when, over the most recent `window_size` frames, at most
    # `noise_threshold` had a real detection (severity != none). This makes the
    # close immune to spurious 1-frame flickers between long quiet stretches.
    # window_size and noise_threshold are derived from the stream's fps:
    #   window_size     = int(5 * fps)   (~5 seconds of stream)
    #   noise_threshold = int(0.3 * fps) (~0.3 seconds worth of detections)
    fps: float = 10.0
    window_size: int = 50
    noise_threshold: int = 3
    detection_window: deque = field(default_factory=lambda: deque(maxlen=50))


@dataclass
class ThresholdConfig:
    """Stores threshold configuration for a camera."""

    camera_id: str
    application_id: str = ""
    app_deployment_id: str = ""
    incident_type: str = ""
    thresholds: List[Dict[str, Any]] = field(default_factory=lambda: DEFAULT_THRESHOLDS.copy())
    last_updated: float = field(default_factory=time.time)
    camera_name: str = ""  # Store camera_name from config


class INCIDENT_MANAGER:
    """
    Manages incident severity level tracking and publishing.

    Key behaviors:
    - Polls 'incident_modification_config' topic for dynamic threshold settings
    - Calculates severity_level from incident_quant using thresholds
    - Publishes incidents ONLY when severity level changes
    - Requires different consecutive frames based on level:
      - 5 frames for medium/significant/critical
      - 10 frames for low (stricter to avoid false positives)
      - 50 empty frames to send "info" (incident ended)
    - Supports both Redis and Kafka transports
    - Thread-safe operations

    Usage:
        manager = INCIDENT_MANAGER(redis_client=..., kafka_client=...)
        manager.start()  # Start config polling
        manager.process_incident(camera_id, incident_data, stream_info)
        manager.stop()   # Stop polling on shutdown
    """

    # Frame thresholds for different severity levels
    CONSECUTIVE_FRAMES_DEFAULT = 5  # For medium, significant, critical
    CONSECUTIVE_FRAMES_LOW = 10  # For low level (stricter)
    CONSECUTIVE_FRAMES_EMPTY = 50  # For sending "info" after no detections
    # Slightly above 1s to cut open/close churn on brief tracker misses, but
    # kept short so looped test clips with distinct events still separate.
    IDLE_CLOSE_SEC = 2.5

    CONFIG_POLLING_INTERVAL = 10  # Poll every 10 seconds
    CONFIG_TOPIC = "incident_modification_config"
    INCIDENT_TOPIC = "incident_res"

    def __init__(
        self,
        redis_client: Optional[Any] = None,
        kafka_client: Optional[Any] = None,
        incident_topic: str = "incident_res",
        config_topic: str = "incident_modification_config",
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize INCIDENT_MANAGER.

        Args:
            redis_client: MatriceStream instance configured for Redis
            kafka_client: MatriceStream instance configured for Kafka
            incident_topic: Topic/stream name for publishing incidents
            config_topic: Topic/stream name for receiving threshold configs
            logger: Python logger instance
        """
        self.redis_client = redis_client
        self.kafka_client = kafka_client
        self.incident_topic = incident_topic
        self.config_topic = config_topic
        self.logger = logger or logging.getLogger(__name__)

        # Per-camera incident state tracking: {camera_id: IncidentState}
        self._incident_states: Dict[str, IncidentState] = {}
        self._states_lock = threading.Lock()

        # Per-camera threshold configuration: {camera_id: ThresholdConfig}
        self._threshold_configs: Dict[str, ThresholdConfig] = {}
        self._config_lock = threading.Lock()

        # Config polling thread control
        self._polling_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._running = False

        # Store factory reference for fetching camera info
        self._factory_ref: Optional["IncidentManagerFactory"] = None

        self.logger.info(
            f"[INCIDENT_MANAGER] Initialized with incident_topic={incident_topic}, "
            f"config_topic={config_topic}, "
            f"low_frames={self.CONSECUTIVE_FRAMES_LOW}, "
            f"default_frames={self.CONSECUTIVE_FRAMES_DEFAULT}, "
            f"empty_frames_for_info={self.CONSECUTIVE_FRAMES_EMPTY}, "
            f"polling_interval={self.CONFIG_POLLING_INTERVAL}s"
        )

    def set_factory_ref(self, factory: "IncidentManagerFactory"):
        """Set reference to factory for accessing deployment info."""
        self._factory_ref = factory

    def start(self):
        """Start the background config polling thread."""
        if self._running:
            self.logger.warning("[INCIDENT_MANAGER] Already running")
            return

        self._running = True
        self._stop_event.clear()
        self._polling_thread = threading.Thread(
            target=self._config_polling_loop, daemon=True, name="IncidentConfigPoller"
        )
        self._polling_thread.start()
        self.logger.info("[INCIDENT_MANAGER] ✓ Started config polling thread")

    def stop(self):
        """Stop the background polling thread gracefully."""
        if not self._running:
            return

        self.logger.info("[INCIDENT_MANAGER] Stopping...")
        self._running = False
        self._stop_event.set()

        if self._polling_thread and self._polling_thread.is_alive():
            self._polling_thread.join(timeout=5)

        self.logger.info("[INCIDENT_MANAGER] ✓ Stopped")

    def _config_polling_loop(self):
        """Background thread that polls for config updates every CONFIG_POLLING_INTERVAL seconds."""
        self.logger.info(
            f"[INCIDENT_MANAGER] Config polling loop started (interval: {self.CONFIG_POLLING_INTERVAL}s)"
        )

        while not self._stop_event.is_set():
            try:
                self._fetch_and_update_configs()
            except Exception as e:
                self.logger.error(
                    f"[INCIDENT_MANAGER] Error in config polling loop: {e}",
                    exc_info=True,
                )

            # Sleep in small increments to allow quick shutdown
            for _ in range(self.CONFIG_POLLING_INTERVAL):
                if self._stop_event.is_set():
                    break
                time.sleep(1)

        self.logger.info("[INCIDENT_MANAGER] Config polling loop exited")

    def _fetch_and_update_configs(self):
        """Fetch config messages from Redis (primary) or Kafka (fallback)."""
        configs = []

        # Try Redis first (primary)
        if self.redis_client:
            try:
                self.logger.debug(
                    f"[INCIDENT_MANAGER] Fetching configs from Redis: {self.config_topic}"
                )
                configs = self._read_configs_from_redis(max_messages=100)
                if configs:
                    self.logger.info(
                        f"[INCIDENT_MANAGER] Fetched {len(configs)} config(s) from Redis"
                    )
            except Exception as e:  # noqa: BLE001 - Redis is a fallback source; any failure just skips it
                self.logger.debug(f"[INCIDENT_MANAGER] Redis config fetch: {e}")

        # Fallback to Kafka if Redis failed or no messages
        if not configs and self.kafka_client:
            try:
                self.logger.debug(
                    f"[INCIDENT_MANAGER] Fetching configs from Kafka: {self.config_topic}"
                )
                configs = self._read_configs_from_kafka(max_messages=100)
                if configs:
                    self.logger.info(
                        f"[INCIDENT_MANAGER] Fetched {len(configs)} config(s) from Kafka"
                    )
            except Exception as e:  # noqa: BLE001 - Kafka is a fallback source; any failure just skips it
                self.logger.debug(f"[INCIDENT_MANAGER] Kafka config fetch: {e}")

        # Update in-memory threshold configs
        for config_data in configs:
            try:
                self._handle_config_message(config_data)
            except Exception as e:
                self.logger.error(
                    f"[INCIDENT_MANAGER] Error handling config message: {e}",
                    exc_info=True,
                )

    def _read_configs_from_redis(self, max_messages: int = 100) -> List[Dict[str, Any]]:
        """Read config messages from Redis stream."""
        messages = []
        try:
            for _msg_count in range(max_messages):
                msg = self.redis_client.get_message(timeout=0.1)
                if not msg:
                    break

                value = msg.get("value") or msg.get("data") or msg.get("message")
                if value:
                    parsed = self._parse_message_value(value)
                    if parsed:
                        messages.append(parsed)
        except Exception as e:  # noqa: BLE001 - a bad/partial poll must not kill the polling loop
            self.logger.debug(f"[INCIDENT_MANAGER] Error reading from Redis: {e}")

        return messages

    def _read_configs_from_kafka(self, max_messages: int = 100) -> List[Dict[str, Any]]:
        """Read config messages from Kafka topic."""
        messages = []
        try:
            for _msg_count in range(max_messages):
                msg = self.kafka_client.get_message(timeout=0.1)
                if not msg:
                    break

                value = msg.get("value") or msg.get("data") or msg.get("message")
                if value:
                    parsed = self._parse_message_value(value)
                    if parsed:
                        messages.append(parsed)
        except Exception as e:  # noqa: BLE001 - a bad/partial poll must not kill the polling loop
            self.logger.debug(f"[INCIDENT_MANAGER] Error reading from Kafka: {e}")

        return messages

    def _parse_message_value(self, value: Any) -> Optional[Dict[str, Any]]:
        """Parse message value into a dictionary."""
        try:
            # Already a dict
            if isinstance(value, dict):
                if "data" in value and isinstance(value["data"], dict):
                    return value["data"]
                return value

            # Bytes to string
            if isinstance(value, bytes):
                value = value.decode("utf-8")

            # Parse JSON string
            if isinstance(value, str):
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    # Try fixing Python-style formatting
                    fixed = value
                    fixed = fixed.replace(": True", ": true").replace(": False", ": false")
                    fixed = fixed.replace(":True", ":true").replace(":False", ":false")
                    fixed = fixed.replace(": None", ": null").replace(":None", ":null")
                    if "'" in fixed and '"' not in fixed:
                        fixed = fixed.replace("'", '"')
                    return json.loads(fixed)
        except Exception as e:  # noqa: BLE001 - malformed message; report and return None
            self.logger.debug(f"[INCIDENT_MANAGER] Failed to parse message: {e}")

        return None

    def _handle_config_message(self, config_data: Dict[str, Any]):
        """
        Handle a threshold config message.

        Expected format:
        {
            "camera_id": "68f9d95cfaff6151c774e0e7",
            "application_id": "...",
            "app_deployment_id": "...",
            "incident_type": "fire",
            "camera_name": "camera_1",
            "thresholds": [
                {"level": "low", "percentage": 1},
                {"level": "medium", "percentage": 3},
                {"level": "significant", "percentage": 13},
                {"level": "critical", "percentage": 30}
            ]
        }
        """
        try:
            camera_id = config_data.get("camera_id", "")
            if not camera_id:
                self.logger.debug("[INCIDENT_MANAGER] Config message missing camera_id, skipping")
                return

            # Extract fields with defaults
            application_id = config_data.get("application_id", "")
            app_deployment_id = config_data.get("app_deployment_id", "")
            incident_type = config_data.get("incident_type", "")
            camera_name = config_data.get("camera_name", "")
            thresholds = config_data.get("thresholds", [])

            # Validate thresholds - use defaults if invalid
            if not thresholds or not isinstance(thresholds, list):
                thresholds = DEFAULT_THRESHOLDS.copy()
                self.logger.debug(
                    f"[INCIDENT_MANAGER] Using default thresholds for camera: {camera_id}"
                )
            else:
                # Validate each threshold has required fields
                # Also map "high" -> "significant" (backend uses "high", we use "significant")
                valid_thresholds = []
                for t in thresholds:
                    if isinstance(t, dict) and "level" in t and "percentage" in t:
                        level = t.get("level", "").lower().strip()
                        # Map "high" to "significant" when receiving from backend
                        if level == "high":
                            self.logger.debug(
                                f"[INCIDENT_MANAGER] Mapping level 'high' -> 'significant' for camera {camera_id}"
                            )
                            t = dict(t)  # Make a copy to avoid modifying original
                            t["level"] = "significant"
                        valid_thresholds.append(t)

                if not valid_thresholds:
                    thresholds = DEFAULT_THRESHOLDS.copy()
                else:
                    thresholds = valid_thresholds

            # Create or update threshold config
            with self._config_lock:
                self._threshold_configs[camera_id] = ThresholdConfig(
                    camera_id=camera_id,
                    application_id=application_id,
                    app_deployment_id=app_deployment_id,
                    incident_type=incident_type,
                    thresholds=thresholds,
                    last_updated=time.time(),
                    camera_name=camera_name,
                )

            self.logger.info(
                f"[INCIDENT_MANAGER] ✓ Updated thresholds for camera: {camera_id}, thresholds: {thresholds}"
            )

        except Exception as e:
            self.logger.error(
                f"[INCIDENT_MANAGER] Error handling config message: {e}", exc_info=True
            )

    def _get_thresholds_for_camera(
        self,
        camera_id: str,
        incident_type: Optional[str] = None,
    ) -> Tuple[List[Dict[str, Any]], Optional[ThresholdConfig]]:
        """
        Get thresholds for a specific camera, or defaults if not configured.

        Returns:
            Tuple of (thresholds list, ThresholdConfig or None)
        """
        with self._config_lock:
            config = self._threshold_configs.get(camera_id)
            if config:
                return config.thresholds, config
            if incident_type in ("weapon_detection", "violence_detection"):
                return WEAPON_DEFAULT_THRESHOLDS, None
            if incident_type in ("loitering_detection", "loitering"):
                return LOITERING_DEFAULT_THRESHOLDS, None
            if incident_type in ("overcrowding_detection", "overcrowding"):
                return OVERCROWDING_DEFAULT_THRESHOLDS, None
            return DEFAULT_THRESHOLDS, None

    def _calculate_severity_from_quant(
        self, incident_quant: float, thresholds: List[Dict[str, Any]]
    ) -> str:
        """
        Calculate severity level from incident_quant using thresholds.

        Args:
            incident_quant: The quantitative value (e.g., intensity percentage)
            thresholds: List of threshold configs sorted by percentage

        Returns:
            Severity level string (none, low, medium, significant, critical)
        """
        if incident_quant is None or incident_quant < 0:
            return "none"

        # Sort thresholds by percentage (ascending)
        sorted_thresholds = sorted(thresholds, key=lambda x: float(x.get("percentage", 0)))

        # Find the highest level where percentage threshold is met
        severity = "none"
        for t in sorted_thresholds:
            level = t.get("level", "").lower()
            percentage = float(t.get("percentage", 0))

            if incident_quant >= percentage:
                severity = level
            else:
                break  # Since sorted ascending, no need to check further

        # Validate severity
        if severity not in SEVERITY_LEVELS:
            severity = "none"

        return severity

    def _get_frames_required_for_level(self, level: str) -> int:
        """
        Get the number of consecutive frames required to confirm a level.

        Args:
            level: Severity level string

        Returns:
            Number of consecutive frames required
        """
        if level == "low":
            return self.CONSECUTIVE_FRAMES_LOW  # 10 frames for low (stricter)
        return self.CONSECUTIVE_FRAMES_DEFAULT  # 5 frames for others

    def _extract_camera_info_from_stream(
        self, stream_info: Optional[Dict[str, Any]]
    ) -> Dict[str, str]:
        """
        Extract camera info from stream_info (similar to ResultsIngestor pattern).

        Stream info structure example:
        {
            'broker': 'localhost:9092',
            'topic': '692d7bde42582ffde3611908_input_topic',  # camera_id is prefix before _input_topic
            'stream_time': '2025-12-02-05:09:53.914224 UTC',
            'camera_info': {
                'camera_name': 'cusstomer-cam-1',
                'camera_group': 'staging-customer-1',
                'location': '<location ObjectId>'
            },
            'frame_id': '7b94e2f668fb456f95b73c3084e17f8a'
        }

        Args:
            stream_info: Stream metadata from usecase

        Returns:
            Dict with camera_id, camera_name, app_deployment_id, application_id, frame_id, location_id
        """
        result = {
            "camera_id": "",
            "camera_name": "",
            "app_deployment_id": "",
            "application_id": "",
            "frame_id": "",
            "rtp_number": "",
            "location": "",
            "location_id": "",
        }

        if not stream_info:
            return result

        try:
            # Try multiple paths to get camera info (like ResultsIngestor)
            # Path 1: Direct camera_info in stream_info
            camera_info = stream_info.get("camera_info", {}) or {}

            # Path 2: From input_settings -> input_stream pattern
            input_settings = stream_info.get("input_settings", {}) or {}
            input_stream = input_settings.get("input_stream", {}) or {}
            input_camera_info = input_stream.get("camera_info", {}) or {}

            # Path 3: From input_streams array (like ResultsIngestor)
            input_streams = stream_info.get("input_streams", [])
            if input_streams and len(input_streams) > 0:
                input_data = input_streams[0] if isinstance(input_streams[0], dict) else {}
                input_stream_inner = input_data.get("input_stream", input_data)
                input_camera_info = input_stream_inner.get("camera_info", {}) or input_camera_info

            # Merge all sources, preferring non-empty values
            # camera_name - check all possible locations
            result["camera_name"] = (
                camera_info.get("camera_name", "")
                or camera_info.get("cameraName", "")
                or input_camera_info.get("camera_name", "")
                or input_camera_info.get("cameraName", "")
                or stream_info.get("camera_name", "")
                or stream_info.get("cameraName", "")
                or input_settings.get("camera_name", "")
                or input_settings.get("cameraName", "")
                or ""
            )

            # camera_id - check direct fields first
            result["camera_id"] = (
                camera_info.get("camera_id", "")
                or camera_info.get("cameraId", "")
                or input_camera_info.get("camera_id", "")
                or input_camera_info.get("cameraId", "")
                or stream_info.get("camera_id", "")
                or stream_info.get("cameraId", "")
                or input_settings.get("camera_id", "")
                or input_settings.get("cameraId", "")
                or ""
            )

            # If camera_id still not found, extract from topic
            # Topic format: {camera_id}_input_topic (e.g., "692d7bde42582ffde3611908_input_topic")
            if not result["camera_id"]:
                topic = stream_info.get("topic", "")
                if topic:
                    extracted_camera_id = ""
                    if topic.endswith("_input_topic"):
                        extracted_camera_id = topic[: -len("_input_topic")]
                        self.logger.debug(
                            f"[INCIDENT_MANAGER] Extracted camera_id from topic (underscore): {extracted_camera_id}"
                        )
                    elif topic.endswith("_input-topic"):
                        extracted_camera_id = topic[: -len("_input-topic")]
                        self.logger.debug(
                            f"[INCIDENT_MANAGER] Extracted camera_id from topic (hyphen): {extracted_camera_id}"
                        )
                    else:
                        if "_input_topic" in topic:
                            extracted_camera_id = topic.split("_input_topic")[0]
                            self.logger.debug(
                                f"[INCIDENT_MANAGER] Extracted camera_id from topic split (underscore): {extracted_camera_id}"
                            )
                        elif "_input-topic" in topic:
                            extracted_camera_id = topic.split("_input-topic")[0]
                            self.logger.debug(
                                f"[INCIDENT_MANAGER] Extracted camera_id from topic split (hyphen): {extracted_camera_id}"
                            )
                    if extracted_camera_id:
                        result["camera_id"] = extracted_camera_id

            # app_deployment_id
            result["app_deployment_id"] = (
                stream_info.get("app_deployment_id", "")
                or stream_info.get("appDeploymentId", "")
                or stream_info.get("app_deploymentId", "")
                or input_settings.get("app_deployment_id", "")
                or input_settings.get("appDeploymentId", "")
                or camera_info.get("app_deployment_id", "")
                or camera_info.get("appDeploymentId", "")
                or ""
            )

            # application_id
            result["application_id"] = (
                stream_info.get("application_id", "")
                or stream_info.get("applicationId", "")
                or stream_info.get("app_id", "")
                or stream_info.get("appId", "")
                or input_settings.get("application_id", "")
                or input_settings.get("applicationId", "")
                or camera_info.get("application_id", "")
                or camera_info.get("applicationId", "")
                or ""
            )

            # frame_id - at top level of stream_info
            result["frame_id"] = (
                stream_info.get("frame_id", "")
                or stream_info.get("frameId", "")
                or input_settings.get("frame_id", "")
                or input_settings.get("frameId", "")
                or ""
            )

            # rtp_number - for media server frame retrieval (replaces frame_id for new flow)
            result["rtp_number"] = (
                stream_info.get("rtp_number", "")
                or stream_info.get("rtpNumber", "")
                or input_settings.get("rtp_number", "")
                or input_settings.get("rtpNumber", "")
                or ""
            )

            # location display name (human-readable label from stream metadata)
            from .post_processing_config_client import (
                is_null_object_id,
                is_resolvable_location_id,
                looks_like_object_id,
                normalize_location_id,
            )

            for candidate in (
                camera_info.get("location"),
                camera_info.get("locationName"),
                input_camera_info.get("location"),
                input_camera_info.get("locationName"),
                stream_info.get("location"),
                stream_info.get("locationName"),
            ):
                text = str(candidate or "").strip()
                if text and not is_null_object_id(text) and not looks_like_object_id(text):
                    result["location"] = text
                    break

            # location_id - prefer explicit id fields over the display label
            location_from_label = ""
            for candidate in (
                camera_info.get("location"),
                input_camera_info.get("location"),
            ):
                text = str(candidate or "").strip()
                if is_resolvable_location_id(text):
                    location_from_label = text
                    break

            result["location_id"] = normalize_location_id(
                camera_info.get("location_id", "")
                or camera_info.get("locationId", "")
                or input_camera_info.get("location_id", "")
                or input_camera_info.get("locationId", "")
                or stream_info.get("location_id", "")
                or stream_info.get("locationId", "")
                or location_from_label
                or ""
            )

            self.logger.debug(
                f"[INCIDENT_MANAGER] Extracted from stream_info - "
                f"camera_id={result['camera_id']}, camera_name={result['camera_name']}, "
                f"app_deployment_id={result['app_deployment_id']}, application_id={result['application_id']}, "
                f"frame_id={result['frame_id']}, rtp_number={result['rtp_number']}, "
                f"location={result['location']}, location_id={result['location_id']}"
            )

        except Exception as e:  # noqa: BLE001 - best-effort extraction; partial `result` is still usable
            self.logger.debug(f"[INCIDENT_MANAGER] Error extracting camera info: {e}")

        return result

    def _map_level_from_backend(self, level: str) -> str:
        """Map level from backend terminology to internal terminology.

        Backend uses 'high', we use 'significant' internally.
        """
        if level and level.lower().strip() == "high":
            return "significant"
        return level

    def _map_level_to_backend(self, level: str) -> str:
        """Map level from internal terminology to backend terminology.

        We use 'significant' internally, backend expects 'high'.
        """
        if level and level.lower().strip() == "significant":
            return "high"
        return level

    def _fetch_location_name(self, location_id: str, stream_location: str = "") -> str:
        """
        Fetch location name from API using location_id.

        Args:
            location_id: The location ID to look up
            stream_location: Human-readable location already present on stream_info

        Returns:
            Location name string, or stream/default fallback if lookup is skipped
        """
        from .post_processing_config_client import is_null_object_id, is_resolvable_location_id

        global _location_name_cache
        stream_label = str(stream_location or "").strip()
        default_location = stream_label or "Entry Reception"

        if not location_id or is_null_object_id(location_id):
            self.logger.debug(
                f"[INCIDENT_MANAGER] Skipping location API for unset location_id, using '{default_location}'"
            )
            return default_location

        if not is_resolvable_location_id(location_id):
            return default_location

        # Check cache first
        cached_name = _location_name_cache.resolved(location_id)
        if cached_name is not None:
            self.logger.debug(
                f"[INCIDENT_MANAGER] Using cached location name for '{location_id}': '{cached_name}'"
            )
            return cached_name

        # Need factory reference with session to make API call
        if not self._factory_ref or not self._factory_ref._session:
            self.logger.warning(
                f"[INCIDENT_MANAGER] No session available for location API, using default: '{default_location}'"
            )
            return default_location

        # A recent failure suppresses the request for a cool-off, but no longer forever:
        # caching the failure pinned the placeholder onto every row for this location
        # for the life of the process, and the API recovering changed nothing (INC-2606).
        if not _location_name_cache.should_fetch(location_id):
            return default_location

        try:
            endpoint = f"/v1/inference/get_location/{location_id}"
            self.logger.info(f"[INCIDENT_MANAGER] Fetching location name from API: {endpoint}")

            response = self._factory_ref._session.rpc.get(endpoint)

            if response and isinstance(response, dict):
                success = response.get("success", False)
                if success:
                    data = response.get("data", {})
                    location_name = data.get("locationName", default_location)
                    self.logger.info(
                        f"[INCIDENT_MANAGER] ✓ Fetched location name: '{location_name}' for location_id: '{location_id}'"
                    )

                    # Cache the result
                    _location_name_cache.store(location_id, location_name)
                    return location_name
                else:
                    self.logger.warning(
                        f"[INCIDENT_MANAGER] API returned success=false for location_id '{location_id}': "
                        f"{response.get('message', 'Unknown error')}"
                    )
            else:
                self.logger.warning(
                    f"[INCIDENT_MANAGER] Invalid response format from API: {response}"
                )

        except Exception as e:
            self.logger.error(
                f"[INCIDENT_MANAGER] Error fetching location name for '{location_id}': {e}",
                exc_info=True,
            )

        # Use fallback on any failure and cache it to avoid repeated blocking calls.
        self.logger.info(f"[INCIDENT_MANAGER] Using fallback location name: '{default_location}'")
        _location_name_cache.note_failure(location_id)
        return default_location

    def _generate_incident_id(self, camera_id: str, cycle_id: int) -> str:
        """Generate a compact random incident_id (max 8 chars).

        Format: 2 uppercase letters + 6 digits (e.g. ``AB482193``). Being
        random, it rarely collides across concurrent applications on the same
        camera or across restarts (which reset ``cycle_id``). ``camera_id`` and
        ``cycle_id`` are accepted for signature compatibility but are not
        embedded. Regenerated only when a new cycle begins, so it stays stable
        across frames within a single incident.
        """
        _ = (camera_id, cycle_id)
        letters = "".join(random.choices(string.ascii_uppercase, k=2))
        digits = f"{random.randint(0, 999_999):06d}"
        return f"{letters}{digits}"

    def _sync_window_config(
        self,
        state: IncidentState,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Sync the per-camera rolling-window config to the stream's fps.

        Window size = 4 * fps frames (~4 sec of stream).
        Noise threshold = 0.5 * fps detections (~0.5 sec).
        If fps changes (or first time), resize the rolling deque so the
        sliding window stays roughly time-bounded across streams.
        """
        fps_in = state.fps
        if stream_info:
            try:
                v = stream_info.get("fps") or stream_info.get("original_fps")
                if v:
                    fps_in = float(v)
            except (TypeError, ValueError):
                pass
        if fps_in <= 0:
            fps_in = state.fps  # fall back to whatever was cached
        new_window_size = max(1, int(round(5 * fps_in)))
        new_noise_threshold = max(1, int(round(0.3 * fps_in)))
        if (
            new_window_size != state.window_size
            or new_noise_threshold != state.noise_threshold
            or state.detection_window.maxlen != new_window_size
        ):
            state.fps = fps_in
            state.window_size = new_window_size
            state.noise_threshold = new_noise_threshold
            state.detection_window = deque(state.detection_window, maxlen=new_window_size)

    def _record_detection_in_window(self, state: IncidentState, had_detection: bool) -> None:
        """Append the current frame's status (True = real detection, False = none)
        into the per-camera rolling window."""
        state.detection_window.append(bool(had_detection))

    def _resolve_close_incident_type(self, camera_id: str, state: IncidentState) -> str:
        """Resolve incident_type for the closing ``info`` event.

        Prefer the type recorded when the cycle opened (e.g. ``weapon_detection``).
        Fall back to polled threshold config, then the historical fire default.
        """
        if state.active_incident_type:
            return state.active_incident_type
        with self._config_lock:
            config = self._threshold_configs.get(camera_id)
            if config and config.incident_type:
                return config.incident_type
        return "fire_smoke_detection"

    def _publish_close_cycle(
        self,
        camera_id: str,
        state: IncidentState,
        stream_info: Optional[Dict[str, Any]],
        *,
        end_time: str,
        incident_type: Optional[str] = None,
    ) -> bool:
        """Publish a closing ``info`` event and rotate to the next incident cycle."""
        from .incident_res_format import utc_now_iso_z

        resolved_type = incident_type or self._resolve_close_incident_type(camera_id, state)
        info_incident = {
            "incident_id": state.current_incident_id,
            "incident_type": resolved_type,
            "severity_level": "info",
            "human_text": "Incident ended",
            "start_time": state.start_time,
            "end_time": end_time or utc_now_iso_z(),
        }

        state.current_level = "info"
        state.empty_frames_count = 0

        success = self._publish_incident(camera_id, info_incident, stream_info)
        if not success:
            return False

        old_incident_id = state.current_incident_id
        old_cycle_id = state.incident_cycle_id

        state.last_published_level = "info"
        state.incident_cycle_id += 1
        state.current_incident_id = self._generate_incident_id(camera_id, state.incident_cycle_id)
        state.incident_active = False
        state.current_level = "none"
        state.pending_level = "none"
        state.consecutive_count = 0
        state.active_incident_type = ""
        state.start_time = ""
        state.last_detection_at = 0.0
        state.detection_window.clear()

        self.logger.info(
            f"[INCIDENT_MANAGER] Closed incident cycle for camera {camera_id}: "
            f"incident_id={old_incident_id} (cycle {old_cycle_id}) → "
            f"new incident_id={state.current_incident_id} (cycle {state.incident_cycle_id})"
        )
        return True

    def _maybe_close_on_idle(
        self,
        camera_id: str,
        state: IncidentState,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Close an active incident after ``IDLE_CLOSE_SEC`` without detections."""
        if not state.incident_active or state.last_published_level in ("info", "none"):
            return False
        if state.last_detection_at <= 0:
            return False
        idle_for = time.monotonic() - state.last_detection_at
        if idle_for < self.IDLE_CLOSE_SEC:
            return False

        self.logger.info(
            f"[INCIDENT_MANAGER] Idle close for camera {camera_id}: "
            f"no detections for {idle_for:.2f}s "
            f"(threshold={self.IDLE_CLOSE_SEC}s, incident_id={state.current_incident_id})"
        )
        from .incident_res_format import utc_now_iso_z

        incident_type = self._resolve_close_incident_type(camera_id, state)
        return self._publish_close_cycle(
            camera_id,
            state,
            stream_info,
            end_time=utc_now_iso_z(),
            incident_type=incident_type,
        )

    def _try_publish_usecase_close(
        self,
        camera_id: str,
        state: IncidentState,
        incident_data: Dict[str, Any],
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Publish when a use case emits an explicit close (``info`` or real ``end_time``)."""
        from .incident_res_format import (
            is_valid_incident_end_time,
            normalize_incident_timestamp,
            utc_now_iso_z,
        )

        raw_severity = str(incident_data.get("severity_level", "")).lower().strip()
        end_raw = incident_data.get("end_time")
        is_explicit_info = raw_severity == "info"
        has_valid_end = is_valid_incident_end_time(end_raw)

        if not is_explicit_info and not has_valid_end:
            return False
        if not state.incident_active or state.last_published_level in ("info", "none"):
            return False

        end_time = normalize_incident_timestamp(end_raw) if has_valid_end else utc_now_iso_z()
        open_type = str(incident_data.get("incident_type", "") or "").strip()
        return self._publish_close_cycle(
            camera_id,
            state,
            stream_info,
            end_time=end_time,
            incident_type=open_type or None,
        )

    def _track_frame_and_maybe_close(
        self,
        camera_id: str,
        state: IncidentState,
        had_detection: bool,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Record this frame in the rolling window and close if the stream is quiet."""
        self._record_detection_in_window(state, had_detection)
        if not self._maybe_close_cycle_via_window(camera_id, state, stream_info):
            return False

        detection_count = sum(state.detection_window)
        self.logger.info(
            f"[INCIDENT_MANAGER] ROLLING-WINDOW close for camera {camera_id}: "
            f"{detection_count}/{state.window_size} detections <= "
            f"{state.noise_threshold} threshold."
        )
        return True

    def _maybe_close_cycle_via_window(
        self,
        camera_id: str,
        state: IncidentState,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """If, over the most recent ``window_size`` frames, the number of
        frames with a real detection is at or below ``noise_threshold``,
        AND an incident is currently active, send the closing 'info' event
        and rotate the cycle (so the next real incident gets a fresh
        incident_id).

        This is the canonical close-the-cycle path. It supersedes the older
        ``empty_frames_count >= CONSECUTIVE_FRAMES_EMPTY`` check, which was
        susceptible to a single spurious detection resetting the counter
        indefinitely (BUG: same incident_id reused across days).
        """
        if len(state.detection_window) < state.window_size:
            # Not enough samples yet — wait until the window is full.
            return False

        detection_count = sum(state.detection_window)
        if detection_count > state.noise_threshold:
            return False  # still genuinely active — keep the cycle open

        # Only emit a closing 'info' when there was something to close.
        if not (state.incident_active and state.last_published_level not in ("info", "none")):
            return False

        from .incident_res_format import utc_now_iso_z

        incident_type = self._resolve_close_incident_type(camera_id, state)
        return self._publish_close_cycle(
            camera_id,
            state,
            stream_info,
            end_time=utc_now_iso_z(),
            incident_type=incident_type,
        )

    def process_incident(
        self,
        camera_id: str,
        incident_data: Dict[str, Any],
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Process an incident and publish if severity level changed.

        This method:
        1. Gets incident_quant from incident_data
        2. Calculates severity_level using dynamic thresholds for this camera
        3. Updates incident_data with new severity_level
        4. Tracks level changes with consecutive-frame validation:
           - 5 frames for medium/significant/critical
           - 10 frames for low (stricter)
        5. Tracks empty incidents and publishes "info" after 50 consecutive empty frames
        6. Publishes on level change
        7. Manages incident_id per camera per cycle (increments after info is sent)

        Args:
            camera_id: Unique camera identifier
            incident_data: Incident dictionary from usecase (must include incident_quant)
            stream_info: Stream metadata

        Returns:
            True if incident was published, False otherwise
        """
        try:
            self.logger.debug(f"[INCIDENT_MANAGER] Processing incident for camera: {camera_id}")

            # Get or create state for this camera
            with self._states_lock:
                if camera_id not in self._incident_states:
                    new_state = IncidentState()
                    # Initialize incident_id for new camera
                    new_state.current_incident_id = self._generate_incident_id(
                        camera_id, new_state.incident_cycle_id
                    )
                    self._incident_states[camera_id] = new_state
                    self.logger.info(
                        f"[INCIDENT_MANAGER] Created new state for camera: {camera_id}, "
                        f"initial incident_id: {new_state.current_incident_id}"
                    )

                state = self._incident_states[camera_id]

                # Ensure incident_id is set (for existing states that may not have it)
                if not state.current_incident_id:
                    state.current_incident_id = self._generate_incident_id(
                        camera_id, state.incident_cycle_id
                    )
                    self.logger.info(
                        f"[INCIDENT_MANAGER] Generated incident_id for existing state: {state.current_incident_id}"
                    )

                # Sync rolling-window config to this stream's fps (used by the
                # noise-tolerant close path that replaces the old consecutive-empty check).
                self._sync_window_config(state, stream_info)

            # Handle empty incident data - track for "info" level
            is_empty_incident = not incident_data or incident_data == {}

            if is_empty_incident:
                self.logger.debug("[INCIDENT_MANAGER] Empty incident data, tracking for info level")
                with self._states_lock:
                    if self._maybe_close_on_idle(camera_id, state, stream_info):
                        return True
                return self._handle_empty_incident(camera_id, state, stream_info)

            with self._states_lock:
                if self._maybe_close_on_idle(camera_id, state, stream_info):
                    return True
                if self._try_publish_usecase_close(camera_id, state, incident_data, stream_info):
                    return True

            # Step 1: Get thresholds for this camera
            incident_type = incident_data.get("incident_type", "")
            thresholds, threshold_config = self._get_thresholds_for_camera(
                camera_id, incident_type=incident_type
            )

            # Step 2: Get incident_quant and calculate severity level dynamically
            incident_quant = incident_data.get("incident_quant")

            if incident_quant is not None:
                # Calculate severity from quant using dynamic thresholds
                severity_level = self._calculate_severity_from_quant(incident_quant, thresholds)

                # Update incident_data with new severity level
                incident_data["severity_level"] = severity_level

                self.logger.debug(
                    f"[INCIDENT_MANAGER] Calculated severity from incident_quant={incident_quant}: "
                    f"severity_level={severity_level}"
                )
            else:
                # Fallback to existing severity_level in incident_data
                severity_level = incident_data.get("severity_level", "none")
                if not severity_level or severity_level == "":
                    severity_level = "none"

            # Store threshold config info in incident_data for output message
            if threshold_config:
                incident_data["_config_camera_id"] = threshold_config.camera_id
                incident_data["_config_application_id"] = threshold_config.application_id
                incident_data["_config_app_deployment_id"] = threshold_config.app_deployment_id
                incident_data["_config_camera_name"] = threshold_config.camera_name

            severity_level = severity_level.lower().strip()

            self.logger.debug(f"[INCIDENT_MANAGER] Final severity_level: '{severity_level}'")

            # Validate severity level
            if severity_level not in SEVERITY_LEVELS:
                self.logger.warning(
                    f"[INCIDENT_MANAGER] Unknown severity level '{severity_level}', treating as 'none'"
                )
                severity_level = "none"

            # If level is "none", treat as empty incident (DO NOT reset empty_frames_count here!)
            if severity_level == "none":
                return self._handle_empty_incident(camera_id, state, stream_info)

            # We have a real detection (severity != none) — reset the empty-frame
            # counter. The incident ends only after CONSECUTIVE_FRAMES_EMPTY
            # consecutive frames with no weapon/detection.
            with self._states_lock:
                state.empty_frames_count = 0
                state.last_detection_at = time.monotonic()

            with self._states_lock:
                self.logger.debug(
                    f"[INCIDENT_MANAGER] Current state - "
                    f"current_level={state.current_level}, "
                    f"pending_level={state.pending_level}, "
                    f"consecutive_count={state.consecutive_count}, "
                    f"last_published_level={state.last_published_level}, "
                    f"incident_id={state.current_incident_id}, "
                    f"cycle_id={state.incident_cycle_id}, "
                    f"incident_active={state.incident_active}"
                )

                # Check if this is a new pending level or continuation
                if severity_level == state.pending_level:
                    # Same level, increment counter
                    state.consecutive_count += 1
                    self.logger.debug(
                        f"[INCIDENT_MANAGER] Same pending level, consecutive_count now: {state.consecutive_count}"
                    )
                else:
                    # Different level, reset counter
                    state.pending_level = severity_level
                    state.consecutive_count = 1
                    self.logger.debug(
                        f"[INCIDENT_MANAGER] New pending level: {severity_level}, reset consecutive_count to 1"
                    )

                # Get required frames for this level
                frames_required = self._get_frames_required_for_level(severity_level)

                # Check if we've reached the threshold for confirmation
                if state.consecutive_count >= frames_required:
                    # Level is confirmed after required consecutive frames
                    old_level = state.current_level
                    new_level = state.pending_level

                    self.logger.info(
                        f"[INCIDENT_MANAGER] Level confirmed after {state.consecutive_count} frames "
                        f"(required: {frames_required}): {old_level} -> {new_level}"
                    )

                    # Check if level actually changed
                    if new_level != state.current_level:
                        state.current_level = new_level

                        # Check if we should publish
                        # 1. Don't publish "none" level (no incident)
                        # 2. Don't publish same level again (spam prevention)
                        should_publish = (
                            new_level != "none" and new_level != state.last_published_level
                        )

                        self.logger.info(
                            f"[INCIDENT_MANAGER] Level changed: {old_level} -> {new_level}, "
                            f"should_publish={should_publish} "
                            f"(last_published={state.last_published_level})"
                        )

                        if should_publish:
                            # Mark incident as active for this cycle
                            state.incident_active = True
                            open_type = str(incident_data.get("incident_type", "") or "").strip()
                            if open_type:
                                state.active_incident_type = open_type

                            # Use the managed incident_id for this cycle
                            incident_data["incident_id"] = state.current_incident_id

                            from .incident_res_format import utc_now_iso_z

                            if not state.start_time:
                                state.start_time = utc_now_iso_z()
                            incident_data["start_time"] = state.start_time
                            if new_level != "info":
                                incident_data["end_time"] = ""

                            # Publish the incident
                            success = self._publish_incident(camera_id, incident_data, stream_info)
                            if success:
                                state.last_published_level = new_level
                                self.logger.info(
                                    f"[INCIDENT_MANAGER] ✓ Published incident for level: {new_level}, "
                                    f"incident_id: {state.current_incident_id}"
                                )
                            if self._track_frame_and_maybe_close(
                                camera_id, state, True, stream_info
                            ):
                                return True
                            return success
                        else:
                            self.logger.debug(
                                f"[INCIDENT_MANAGER] Skipping publish - level={new_level}, already published"
                            )
                    else:
                        self.logger.debug(
                            f"[INCIDENT_MANAGER] No level change, staying at: {state.current_level}"
                        )

                if self._track_frame_and_maybe_close(camera_id, state, True, stream_info):
                    return True
                return False

        except Exception as e:
            self.logger.error(f"[INCIDENT_MANAGER] Error processing incident: {e}", exc_info=True)
            return False

    def _handle_empty_incident(
        self,
        camera_id: str,
        state: IncidentState,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Handle empty incident (no detection).

        After 50 consecutive empty frames, send "info" level if an incident was active.
        Info uses the SAME incident_id as the current cycle, then starts a new cycle.

        Args:
            camera_id: Camera identifier
            state: Current incident state
            stream_info: Stream metadata

        Returns:
            True if "info" incident was published, False otherwise
        """
        with self._states_lock:
            if self._maybe_close_on_idle(camera_id, state, stream_info):
                return True
            if self._track_frame_and_maybe_close(camera_id, state, False, stream_info):
                return True

            state.empty_frames_count += 1

            self.logger.debug(
                f"[INCIDENT_MANAGER] Empty frame count for camera {camera_id}: "
                f"{state.empty_frames_count}/{self.CONSECUTIVE_FRAMES_EMPTY}, "
                f"incident_active={state.incident_active}, "
                f"current_incident_id={state.current_incident_id}"
            )

            # Reset pending level tracking when empty
            if state.pending_level not in ("none", "info"):
                state.pending_level = "none"
                state.consecutive_count = 0

            # Check if we should send "info" (incident ended)
            if state.empty_frames_count >= self.CONSECUTIVE_FRAMES_EMPTY:
                # Only send "info" if:
                # 1. An incident was actually active in this cycle (we published something)
                # 2. Last published level was NOT "info" (don't send duplicate info)
                should_send_info = state.incident_active and state.last_published_level not in (
                    "info",
                    "none",
                )

                if should_send_info:
                    self.logger.info(
                        f"[INCIDENT_MANAGER] {self.CONSECUTIVE_FRAMES_EMPTY} consecutive empty frames for camera {camera_id}, "
                        f"sending 'info' level to close incident cycle "
                        f"(last_published={state.last_published_level}, incident_id={state.current_incident_id})"
                    )

                    incident_type = self._resolve_close_incident_type(camera_id, state)

                    from .incident_res_format import utc_now_iso_z

                    success = self._publish_close_cycle(
                        camera_id,
                        state,
                        stream_info,
                        end_time=utc_now_iso_z(),
                        incident_type=incident_type,
                    )
                    if success:
                        self.logger.info(
                            f"[INCIDENT_MANAGER] ✓ Published 'info' for camera {camera_id} after "
                            f"{self.CONSECUTIVE_FRAMES_EMPTY} consecutive empty frames"
                        )
                    return success
                else:
                    # No active incident or already sent info
                    if not state.incident_active:
                        self.logger.debug(
                            f"[INCIDENT_MANAGER] Skipping 'info' for camera {camera_id} - "
                            f"no incident was active in this cycle"
                        )
                    else:
                        self.logger.debug(
                            f"[INCIDENT_MANAGER] Skipping 'info' for camera {camera_id} - "
                            f"last_published is already '{state.last_published_level}'"
                        )

                    # Reset empty frame counter if we decide not to send info
                    # to avoid repeated checks every frame after 101
                    state.empty_frames_count = 0

            return False

    def _publish_incident(
        self,
        camera_id: str,
        incident_data: Dict[str, Any],
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Publish incident to Redis/Kafka topic.

        Args:
            camera_id: Camera identifier
            incident_data: Incident dictionary
            stream_info: Stream metadata

        Returns:
            True if published successfully, False otherwise
        """
        self.logger.info("[INCIDENT_MANAGER] ========== PUBLISHING INCIDENT ==========")

        try:
            # Build the incident message
            message = self._build_incident_message(camera_id, incident_data, stream_info)

            self.logger.info(
                f"[INCIDENT_MANAGER] Built incident message: {json.dumps(message, default=str)[:500]}..."
            )

            success = False

            # Try Redis first (primary)
            if self.redis_client:
                try:
                    self.logger.debug(
                        f"[INCIDENT_MANAGER] Publishing to Redis stream: {self.incident_topic}"
                    )
                    self._publish_to_redis(self.incident_topic, message)
                    self.logger.info("[INCIDENT_MANAGER] ✓ Incident published to Redis")
                    success = True
                except Exception as e:
                    self.logger.error(
                        f"[INCIDENT_MANAGER] ❌ Redis publish failed: {e}",
                        exc_info=True,
                    )

            # Fallback to Kafka if Redis failed or no Redis client
            if not success and self.kafka_client:
                try:
                    self.logger.debug(
                        f"[INCIDENT_MANAGER] Publishing to Kafka topic: {self.incident_topic}"
                    )
                    self._publish_to_kafka(self.incident_topic, message)
                    self.logger.info("[INCIDENT_MANAGER] ✓ Incident published to Kafka")
                    success = True
                except Exception as e:
                    self.logger.error(
                        f"[INCIDENT_MANAGER] ❌ Kafka publish failed: {e}",
                        exc_info=True,
                    )

            if success:
                self.logger.info("[INCIDENT_MANAGER] ========== INCIDENT PUBLISHED ==========")
            else:
                self.logger.error(
                    "[INCIDENT_MANAGER] ❌ INCIDENT NOT PUBLISHED (both transports failed)"
                )

            return success

        except Exception as e:
            self.logger.error(f"[INCIDENT_MANAGER] Error publishing incident: {e}", exc_info=True)
            return False

    def _build_incident_message(
        self,
        camera_id: str,
        incident_data: Dict[str, Any],
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Build the incident message in the canonical ``IncidentMessage`` wire format
        (same envelope as the new AnalyticsEngine flow).
        """
        from .incident_res_format import _pick_str, build_incident_res_message

        stream_camera_info = self._extract_camera_info_from_stream(stream_info)

        config_camera_id = incident_data.get("_config_camera_id", "")
        config_application_id = incident_data.get("_config_application_id", "")
        config_app_deployment_id = incident_data.get("_config_app_deployment_id", "")

        factory_app_deployment_id = ""
        factory_application_id = ""
        if self._factory_ref:
            factory_app_deployment_id = self._factory_ref._app_deployment_id or ""
            factory_application_id = self._factory_ref._application_id or ""

        final_camera_id = stream_camera_info.get("camera_id") or config_camera_id or camera_id or ""
        final_frame_id = stream_camera_info.get("frame_id", "")
        final_rtp_number = stream_camera_info.get("rtp_number", "")

        stream_time = ""
        if stream_info:
            stream_time = stream_info.get("stream_time", "")
            if not stream_time:
                input_settings = stream_info.get("input_settings", {})
                if isinstance(input_settings, dict):
                    stream_time = input_settings.get("stream_time", "")

        if stream_time:
            try:
                ts_clean = stream_time.replace(" UTC", "").strip()
                if ts_clean[:4].isdigit() and int(ts_clean[:4]) < 2000:
                    stream_time = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            except (ValueError, IndexError):
                pass

        # DRIFT-005: env-gated wall-clock override (truthy MATRICE_FORCE_WALLCLOCK_STREAM_TIME).
        # Default OFF preserves the frame/RTP-derived stream_time above.
        from .stream_time_utils import (
            force_wallclock_stream_time,
            wallclock_incident_stream_time,
        )

        if force_wallclock_stream_time():
            stream_time = wallclock_incident_stream_time()

        location_id = stream_camera_info.get("location_id", "")
        final_location_name = self._fetch_location_name(
            location_id,
            stream_location=stream_camera_info.get("location", ""),
        )

        from ...analytics.engine_session import resolve_camera_fields_from_stream_info

        cam_fields = resolve_camera_fields_from_stream_info(stream_info)
        final_camera_name = _pick_str(
            cam_fields.get("camera_name"),
            stream_camera_info.get("camera_name"),
            incident_data.get("_config_camera_name"),
        )

        # stream_info often lacks application_name; factory only carries ids.
        # Fall back to the legacy profile display name (e.g. weapon_detection →
        # "Weapon Detection") so incident_res matches the legacy/new-flow envelopes.
        si = stream_info or {}
        inp = si.get("input_settings") if isinstance(si.get("input_settings"), dict) else {}
        threshold_configs = getattr(self, "_threshold_configs", None) or {}
        threshold_cfg = threshold_configs.get(final_camera_id) if final_camera_id else None
        incident_type = _pick_str(
            incident_data.get("incident_type"),
            getattr(threshold_cfg, "incident_type", None),
        )
        default_app_name = ""
        if incident_type:
            try:
                from .legacy_analytics_bridge import get_legacy_profile

                profile = get_legacy_profile(incident_type)
                if profile and profile.default_application_name:
                    default_app_name = profile.default_application_name
            except Exception:  # noqa: BLE001 - profile lookup is cosmetic; fall back to a titleized name
                default_app_name = ""
            if not default_app_name:
                default_app_name = incident_type.replace("_", " ").title()

        final_application_name = _pick_str(
            si.get("application_name"),
            si.get("app_name"),
            inp.get("application_name") if isinstance(inp, dict) else None,
            inp.get("app_name") if isinstance(inp, dict) else None,
            default_app_name,
        )

        message = build_incident_res_message(
            incident_data,
            stream_info,
            camera_id=final_camera_id,
            camera_name=final_camera_name,
            location_name=final_location_name,
            application_name=final_application_name,
            factory_app_deployment_id=config_app_deployment_id or factory_app_deployment_id,
            factory_application_id=config_application_id or factory_application_id,
            frame_id=final_frame_id,
            stream_time=stream_time,
        )
        if final_rtp_number:
            message["rtp_number"] = final_rtp_number

        self.logger.info(
            f"[INCIDENT_MANAGER] Building message with - "
            f"camera_id={message.get('camera_id')}, camera_name={message.get('camera_name')}, "
            f"app_deployment_id={message.get('app_deployment_id')}, application_id={message.get('application_id')}, "
            f"frame_id={message.get('frame_id')}, rtp_number={message.get('rtp_number')}, "
            f"location_name={message.get('location_name')}"
        )
        return message

    def _publish_to_redis(self, topic: str, message: Dict[str, Any]):
        """Publish message to Redis stream."""
        try:
            self.redis_client.add_message(
                topic_or_channel=topic,
                message=json.dumps(message),
                key=message.get("camera_id", ""),
            )
        except Exception as e:
            self.logger.error(f"[INCIDENT_MANAGER] Redis publish error: {e}")
            raise

    def _publish_to_kafka(self, topic: str, message: Dict[str, Any]):
        """Publish message to Kafka topic."""
        try:
            self.kafka_client.add_message(
                topic_or_channel=topic,
                message=json.dumps(message),
                key=message.get("camera_id", ""),
            )
        except Exception as e:
            self.logger.error(f"[INCIDENT_MANAGER] Kafka publish error: {e}")
            raise

    def reset_camera_state(self, camera_id: str):
        """Reset incident state for a specific camera."""
        with self._states_lock:
            if camera_id in self._incident_states:
                self._incident_states[camera_id] = IncidentState()
                self.logger.info(f"[INCIDENT_MANAGER] Reset state for camera: {camera_id}")

    def get_camera_state(self, camera_id: str) -> Optional[Dict[str, Any]]:
        """Get current incident state for a camera (for debugging)."""
        with self._states_lock:
            state = self._incident_states.get(camera_id)
            if state:
                return {
                    "current_level": state.current_level,
                    "pending_level": state.pending_level,
                    "consecutive_count": state.consecutive_count,
                    "last_published_level": state.last_published_level,
                    "incident_cycle_id": state.incident_cycle_id,
                    "empty_frames_count": state.empty_frames_count,
                    "current_incident_id": state.current_incident_id,
                    "incident_active": state.incident_active,
                    "fps": state.fps,
                    "window_size": state.window_size,
                    "noise_threshold": state.noise_threshold,
                    "detection_window_count": sum(state.detection_window),
                    "detection_window_len": len(state.detection_window),
                }
            return None

    def get_all_camera_states(self) -> Dict[str, Dict[str, Any]]:
        """Get all camera states for debugging/monitoring."""
        with self._states_lock:
            return {
                cam_id: {
                    "current_level": state.current_level,
                    "pending_level": state.pending_level,
                    "consecutive_count": state.consecutive_count,
                    "last_published_level": state.last_published_level,
                    "incident_cycle_id": state.incident_cycle_id,
                    "empty_frames_count": state.empty_frames_count,
                    "current_incident_id": state.current_incident_id,
                    "incident_active": state.incident_active,
                    "fps": state.fps,
                    "window_size": state.window_size,
                    "noise_threshold": state.noise_threshold,
                    "detection_window_count": sum(state.detection_window),
                    "detection_window_len": len(state.detection_window),
                }
                for cam_id, state in self._incident_states.items()
            }

    def get_threshold_config(self, camera_id: str) -> Optional[Dict[str, Any]]:
        """Get threshold configuration for a camera (for debugging)."""
        with self._config_lock:
            config = self._threshold_configs.get(camera_id)
            if config:
                return {
                    "camera_id": config.camera_id,
                    "application_id": config.application_id,
                    "app_deployment_id": config.app_deployment_id,
                    "incident_type": config.incident_type,
                    "thresholds": config.thresholds,
                    "last_updated": config.last_updated,
                    "camera_name": config.camera_name,
                }
            return None

    def set_thresholds_for_camera(
        self,
        camera_id: str,
        thresholds: List[Dict[str, Any]],
        application_id: str = "",
        app_deployment_id: str = "",
        incident_type: str = "",
        camera_name: str = "",
    ):
        """
        Manually set thresholds for a camera (useful for testing or direct config).

        Args:
            camera_id: Camera identifier
            thresholds: List of threshold configs
            application_id: Application ID
            app_deployment_id: App deployment ID
            incident_type: Incident type (e.g., "fire")
            camera_name: Camera name
        """
        # Map "high" -> "significant" in thresholds (backend uses "high", we use "significant")
        mapped_thresholds = []
        if thresholds:
            for t in thresholds:
                if isinstance(t, dict):
                    level = t.get("level", "").lower().strip()
                    if level == "high":
                        t = dict(t)  # Copy to avoid modifying original
                        t["level"] = "significant"
                        self.logger.debug(
                            "[INCIDENT_MANAGER] Mapped threshold level 'high' -> 'significant'"
                        )
                    mapped_thresholds.append(t)

        with self._config_lock:
            self._threshold_configs[camera_id] = ThresholdConfig(
                camera_id=camera_id,
                application_id=application_id,
                app_deployment_id=app_deployment_id,
                incident_type=incident_type,
                thresholds=mapped_thresholds if mapped_thresholds else DEFAULT_THRESHOLDS.copy(),
                last_updated=time.time(),
                camera_name=camera_name,
            )
        self.logger.info(f"[INCIDENT_MANAGER] Manually set thresholds for camera: {camera_id}")


class IncidentManagerFactory:
    """
    Factory class for creating INCIDENT_MANAGER instances.

    Handles session initialization and Redis/Kafka client creation
    following the same pattern as license_plate_monitoring.py.
    """

    ACTION_ID_PATTERN = re.compile(r"^[0-9a-f]{8,}$", re.IGNORECASE)

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        self._initialized = False
        self._incident_manager: Optional[INCIDENT_MANAGER] = None

        # Store these for later access
        self._session = None
        self._action_id: Optional[str] = None
        self._instance_id: Optional[str] = None
        self._deployment_id: Optional[str] = None
        self._app_deployment_id: Optional[str] = None
        self._application_id: Optional[str] = None  # Store application_id from action_details
        self._external_ip: Optional[str] = None

    def _get_or_create_session(self, config: Any):
        """Get session from config or create one from environment variables."""
        try:
            from matrice_common.session import Session
        except ImportError:
            Session = None

        self._session = getattr(config, "session", None)
        if self._session:
            self.logger.info("[INCIDENT_MANAGER_FACTORY] Using session from config")
            return

        self.logger.info(
            "[INCIDENT_MANAGER_FACTORY] No session in config, creating from environment..."
        )
        account_number = os.getenv("MATRICE_ACCOUNT_NUMBER", "")
        access_key_id = os.getenv("MATRICE_ACCESS_KEY_ID", "")
        secret_key = os.getenv("MATRICE_SECRET_ACCESS_KEY", "")
        project_id = os.getenv("MATRICE_PROJECT_ID", "")

        self.logger.debug(
            f"[INCIDENT_MANAGER_FACTORY] Env vars - account: {'SET' if account_number else 'NOT SET'}, "
            f"access_key: {'SET' if access_key_id else 'NOT SET'}, "
            f"secret: {'SET' if secret_key else 'NOT SET'}"
        )

        self._session = Session(
            account_number=account_number,
            access_key=access_key_id,
            secret_key=secret_key,
            project_id=project_id,
        )
        self.logger.info("[INCIDENT_MANAGER_FACTORY] Created session from environment")

    def _fetch_and_store_action_details(self, rpc: Any) -> Optional[dict]:
        """Fetch action details from API and store identifiers. Returns action_details or None on failure."""
        try:
            action_url = f"/v1/actions/action/{self._action_id}/details"
            action_resp = rpc.get(action_url)
            if not (action_resp and action_resp.get("success", False)):
                raise RuntimeError(
                    action_resp.get("message", "Unknown error")
                    if isinstance(action_resp, dict)
                    else "Unknown error"
                )
            action_doc = action_resp.get("data", {}) if isinstance(action_resp, dict) else {}
            action_details = (
                action_doc.get("actionDetails", {}) if isinstance(action_doc, dict) else {}
            )
            job_params = action_doc.get("jobParams", {}) if isinstance(action_doc, dict) else {}

            self._deployment_id = action_details.get("_idDeployment") or action_details.get(
                "deployment_id"
            )
            self._app_deployment_id = (
                action_details.get("app_deployment_id")
                or action_details.get("appDeploymentId")
                or action_details.get("app_deploymentId")
                or job_params.get("app_deployment_id")
                or job_params.get("appDeploymentId")
                or job_params.get("app_deploymentId")
                or ""
            )
            self._application_id = (
                job_params.get("application_id")
                or job_params.get("applicationId")
                or job_params.get("app_id")
                or job_params.get("appId")
                or action_details.get("application_id")
                or action_details.get("applicationId")
                or ""
            )
            self._instance_id = action_details.get("instanceID") or action_details.get("instanceId")
            self._external_ip = action_details.get("externalIP") or action_details.get("externalIp")

            self.logger.info(
                f"[INCIDENT_MANAGER_FACTORY] Action details - "
                f"instance_id={self._instance_id}, "
                f"app_deployment_id={self._app_deployment_id}, application_id={self._application_id}"
            )
            self.logger.debug(
                f"[INCIDENT_MANAGER_FACTORY] actionDetails keys: {list(action_details.keys())}"
            )
            self.logger.debug(
                f"[INCIDENT_MANAGER_FACTORY] jobParams keys: {list(job_params.keys()) if job_params else []}"
            )
            return action_details

        except Exception as e:
            self.logger.error(
                f"[INCIDENT_MANAGER_FACTORY] Failed to fetch action details: {e}",
                exc_info=True,
            )
            print(
                f"----- INCIDENT MANAGER ACTION DETAILS ERROR -----\naction_id: {self._action_id}\nerror: {e}\n-------------------------------------------------"
            )
            return None

    def _create_redis_client(self, rpc: Any):
        """Create and return a Redis MatriceStream client, or None on failure."""
        try:
            from matrice_common.stream.matrice_stream import MatriceStream, StreamType
        except ImportError:
            MatriceStream = None
            StreamType = None

        if not self._instance_id:
            self.logger.error("[INCIDENT_MANAGER_FACTORY] Localhost mode but instance_id missing")
            return None
        try:
            url = f"/v1/actions/get_redis_server_by_instance_id/{self._instance_id}"
            self.logger.info(
                f"[INCIDENT_MANAGER_FACTORY] Fetching Redis server info for instance: {self._instance_id}"
            )
            response = rpc.get(url)

            if not (isinstance(response, dict) and response.get("success", False)):
                msg = (
                    response.get("message", "Unknown error")
                    if isinstance(response, dict)
                    else "Unknown error"
                )
                self.logger.warning(
                    f"[INCIDENT_MANAGER_FACTORY] Failed to fetch Redis server info: {msg}"
                )
                return None

            data = response.get("data", {})
            host = data.get("host")
            port = data.get("port")
            password = data.get("password", "")

            sentinel_cfg = data.get("sentinelConfig") or {}
            sentinel_hosts = (
                [(h, 26379) for h in sentinel_cfg["sentinelHosts"]]
                if sentinel_cfg.get("sentinelHosts")
                else None
            )
            master_name = sentinel_cfg.get("masterName") if sentinel_hosts else None

            self.logger.info(f"[INCIDENT_MANAGER_FACTORY] Redis params - host={host}, port={port}")

            stream_kwargs = dict(
                host=host,
                port=int(port),
                password=password,
                username=data.get("username"),
                db=data.get("db", 0),
                connection_timeout=data.get("connection_timeout", 120),
            )
            if sentinel_hosts and master_name:
                stream_kwargs["sentinel_hosts"] = sentinel_hosts
                stream_kwargs["master_name"] = master_name
            redis_client = MatriceStream(StreamType.REDIS, **stream_kwargs)
            redis_client.setup("incident_modification_config")
            self.logger.info("[INCIDENT_MANAGER_FACTORY] Redis client initialized")
            return redis_client
        except Exception as e:  # noqa: BLE001 - unreachable Redis is not fatal; caller treats None as "no client"
            self.logger.warning(f"[INCIDENT_MANAGER_FACTORY] Redis initialization failed: {e}")
            return None

    def initialize(self, config: Any) -> Optional[INCIDENT_MANAGER]:
        """
        Initialize and return INCIDENT_MANAGER with Redis/Kafka clients.

        Args:
            config: Configuration object with session, server_id, etc.

        Returns:
            INCIDENT_MANAGER instance or None if initialization failed
        """
        if self._initialized and self._incident_manager is not None:
            self.logger.debug(
                "[INCIDENT_MANAGER_FACTORY] Already initialized, returning existing instance"
            )
            return self._incident_manager

        try:
            self.logger.info("[INCIDENT_MANAGER_FACTORY] ===== STARTING INITIALIZATION =====")
            self._get_or_create_session(config)
            rpc = self._session.rpc

            self._action_id = self._discover_action_id()
            if not self._action_id:
                self.logger.error("[INCIDENT_MANAGER_FACTORY] Could not discover action_id")
                self._initialized = True
                return None

            self.logger.info(f"[INCIDENT_MANAGER_FACTORY] Discovered action_id: {self._action_id}")

            action_details = self._fetch_and_store_action_details(rpc)
            if action_details is None:
                self._initialized = True
                return None

            # Historical deployment behavior: always initialize via Redis
            redis_client = self._create_redis_client(rpc)

            if redis_client:
                self._incident_manager = INCIDENT_MANAGER(
                    redis_client=redis_client,
                    kafka_client=None,
                    incident_topic="incident_res",
                    config_topic="incident_modification_config",
                    logger=self.logger,
                )
                self._incident_manager.set_factory_ref(self)
                self._incident_manager.start()
                self.logger.info("[INCIDENT_MANAGER_FACTORY] Incident manager created with Redis")
            else:
                self.logger.warning(
                    "[INCIDENT_MANAGER_FACTORY] No Redis client available, incident manager not created"
                )

            self._initialized = True
            self.logger.info("[INCIDENT_MANAGER_FACTORY] ===== INITIALIZATION COMPLETE =====")
            return self._incident_manager

        except ImportError as e:
            self.logger.error(f"[INCIDENT_MANAGER_FACTORY] Import error: {e}")
            self._initialized = True
            return None
        except Exception as e:
            self.logger.error(
                f"[INCIDENT_MANAGER_FACTORY] Initialization failed: {e}", exc_info=True
            )
            self._initialized = True
            return None

    def _discover_action_id(self) -> Optional[str]:
        """Discover action_id from current working directory name (and parents)."""
        try:
            candidates: List[str] = []

            try:
                cwd = Path.cwd()
                candidates.append(cwd.name)
                for parent in cwd.parents:
                    candidates.append(parent.name)
            except Exception:  # noqa: BLE001 - cwd is only one of several action_id candidate sources
                self.logger.debug(
                    "[INCIDENT_MANAGER] cwd scan for action_id candidates failed", exc_info=True
                )

            try:
                usr_src = Path("/usr/src")
                if usr_src.exists():
                    for child in usr_src.iterdir():
                        if child.is_dir():
                            candidates.append(child.name)
            except Exception:  # noqa: BLE001 - /usr/src is absent outside the container image
                self.logger.debug(
                    "[INCIDENT_MANAGER] /usr/src scan for action_id candidates failed",
                    exc_info=True,
                )

            for candidate in candidates:
                if candidate and len(candidate) >= 8 and self.ACTION_ID_PATTERN.match(candidate):
                    return candidate
        except Exception:  # noqa: BLE001 - callers treat an unresolved action_id as "not discoverable"
            self.logger.debug("[INCIDENT_MANAGER] action_id discovery failed", exc_info=True)
        return None

    def _get_backend_base_url(self) -> str:
        """Resolve backend base URL based on ENV variable."""
        env = os.getenv("ENV", "prod").strip().lower()
        if env in ("prod", "production"):
            host = "prod.backend.app.matrice.ai"
        elif env in ("dev", "development"):
            host = "dev.backend.app.matrice.ai"
        else:
            host = "staging.backend.app.matrice.ai"
        return f"https://{host}"

    @property
    def is_initialized(self) -> bool:
        return self._initialized

    @property
    def incident_manager(self) -> Optional[INCIDENT_MANAGER]:
        return self._incident_manager


# Module-level factory instance for convenience
_default_factory: Optional[IncidentManagerFactory] = None


def get_incident_manager(
    config: Any, logger: Optional[logging.Logger] = None
) -> Optional[INCIDENT_MANAGER]:
    """
    Get or create INCIDENT_MANAGER instance.

    This is a convenience function that uses a module-level factory.
    For more control, use IncidentManagerFactory directly.

    Args:
        config: Configuration object with session, server_id, etc.
        logger: Logger instance

    Returns:
        INCIDENT_MANAGER instance or None
    """
    global _default_factory

    if _default_factory is None:
        _default_factory = IncidentManagerFactory(logger=logger)

    return _default_factory.initialize(config)
