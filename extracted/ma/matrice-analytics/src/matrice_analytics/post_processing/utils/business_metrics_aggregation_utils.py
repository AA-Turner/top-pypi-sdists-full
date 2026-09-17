"""
business_metrics_aggregation_utils.py

Manages business metrics aggregation and publishing to Redis/Kafka.
Aggregates metrics for 5 minutes (300 seconds) and pushes to output topic.
Supports aggregation types: mean (default), min, max, sum.

Split out of ``business_metrics_manager_utils`` (SG-6/F02b): aggregation and
the control-plane construction that produces a manager share nothing but the
class they hand back, and together they carried the module past the org
file-size cap. ``business_metrics_manager_utils`` keeps the factory and
re-exports everything here, so importers are unaffected -- and the dependency
runs one way, from the factory to this module.

PRODUCTION-READY VERSION
"""

import json
import logging
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

from .location_name_cache import LocationNameCache

if TYPE_CHECKING:  # pragma: no cover - resolved by the type checker only
    # One-way dependency: the factory module imports this one at runtime, so the
    # reverse reference exists for annotations and nothing else.
    from .business_metrics_manager_utils import BusinessMetricsManagerFactory

# Default aggregation interval in seconds (5 minutes)
DEFAULT_AGGREGATION_INTERVAL = 300

# Supported aggregation types
AGGREGATION_TYPES = ["mean", "min", "max", "sum"]

# Cache for location names to avoid repeated API calls
_location_name_cache = LocationNameCache()

# Default metrics configuration with aggregation type
DEFAULT_METRICS_CONFIG = {
    "customer_to_staff_ratio": "mean",
    "service_coverage": "mean",
    "interaction_rate": "mean",
    "staff_utilization": "mean",
    "area_utilization": "mean",
    "service_quality_score": "mean",
    "attention_score": "mean",
    "overall_performance": "mean",
}


@dataclass
class MetricAggregator:
    """Stores aggregated values for a single metric."""

    values: List[float] = field(default_factory=list)
    agg_type: str = "mean"

    def add_value(self, value: float):
        """Add a value to the aggregator."""
        if value is not None and isinstance(value, (int, float)):
            self.values.append(float(value))

    def get_aggregated_value(self) -> Optional[float]:
        """Get the aggregated value based on aggregation type."""
        if not self.values:
            return None

        if self.agg_type == "mean":
            return sum(self.values) / len(self.values)
        elif self.agg_type == "min":
            return min(self.values)
        elif self.agg_type == "max":
            return max(self.values)
        elif self.agg_type == "sum":
            return sum(self.values)
        else:
            # Default to mean if unknown type
            return sum(self.values) / len(self.values)

    def reset(self):
        """Reset the aggregator values."""
        self.values = []

    def has_values(self) -> bool:
        """Check if aggregator has any values."""
        return len(self.values) > 0


@dataclass
class CameraMetricsState:
    """Stores metrics state for a camera."""

    camera_id: str
    camera_name: str = ""
    app_deployment_id: str = ""
    application_id: str = ""
    location_id: str = ""
    location_name: str = ""
    stream_time: str = ""  # Store most recent stream_time
    metrics: Dict[str, MetricAggregator] = field(default_factory=dict)
    last_push_time: float = field(default_factory=time.time)
    """Wall clock of the last push. **Reported, never measured against.**

    It is published raw in ``get_camera_state``/``get_all_camera_states``, where an epoch
    is what a reader wants, so it stays a wall clock.
    """

    last_push_at: float = field(default_factory=time.monotonic)
    """``time.monotonic()`` of the last push -- the one the interval arithmetic uses.

    The publish decision is ``elapsed >= aggregation_interval``, so it is control logic:
    an NTP correction backwards makes ``elapsed`` negative and stalls publishing for that
    camera until the clock catches up, which on an edge device booting with a dead RTC is
    a routine step, not an edge case. The two fields are set together and never diverge;
    keeping both means the diagnostics stay readable without the cadence depending on a
    clock that can move.
    """

    def add_metric_value(self, metric_name: str, value: float, agg_type: str = "mean"):
        """Add a value for a specific metric."""
        if metric_name not in self.metrics:
            self.metrics[metric_name] = MetricAggregator(agg_type=agg_type)
        self.metrics[metric_name].add_value(value)

    def get_aggregated_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Get all aggregated metrics in output format."""
        result = {}
        for metric_name, aggregator in self.metrics.items():
            if aggregator.has_values():
                agg_value = aggregator.get_aggregated_value()
                if agg_value is not None:
                    result[metric_name] = {
                        "data": round(agg_value, 4),
                        "agg_type": aggregator.agg_type,
                    }
        return result

    def reset_metrics(self):
        """Reset all metric aggregators."""
        for aggregator in self.metrics.values():
            aggregator.reset()
        self.last_push_time = time.time()
        self.last_push_at = time.monotonic()

    def has_metrics(self) -> bool:
        """Check if any metrics have values."""
        return any(agg.has_values() for agg in self.metrics.values())


class BUSINESS_METRICS_MANAGER:
    """
    Manages business metrics aggregation and publishing.

    Key behaviors:
    - Aggregates business metrics for configurable interval (default 5 minutes)
    - Publishes aggregated metrics to Redis/Kafka topic
    - Supports multiple aggregation types (mean, min, max, sum)
    - Resets all values after publishing
    - Thread-safe operations

    Usage:
        manager = BUSINESS_METRICS_MANAGER(redis_client=..., kafka_client=...)
        manager.start()  # Start aggregation timer
        manager.process_metrics(camera_id, metrics_data, stream_info)
        manager.stop()   # Stop on shutdown
    """

    OUTPUT_TOPIC = "business_metrics"

    def __init__(
        self,
        redis_client: Optional[Any] = None,
        kafka_client: Optional[Any] = None,
        output_topic: str = "business_metrics",
        aggregation_interval: int = DEFAULT_AGGREGATION_INTERVAL,
        metrics_config: Optional[Dict[str, str]] = None,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize BUSINESS_METRICS_MANAGER.

        Args:
            redis_client: MatriceStream instance configured for Redis
            kafka_client: MatriceStream instance configured for Kafka
            output_topic: Topic/stream name for publishing metrics
            aggregation_interval: Interval in seconds for aggregation (default 300 = 5 minutes)
            metrics_config: Dict of metric_name -> aggregation_type
            logger: Python logger instance
        """
        self.redis_client = redis_client
        self.kafka_client = kafka_client
        self.output_topic = output_topic
        self.aggregation_interval = aggregation_interval
        self.metrics_config = metrics_config or DEFAULT_METRICS_CONFIG.copy()
        self.logger = logger or logging.getLogger(__name__)

        # Per-camera metrics state tracking: {camera_id: CameraMetricsState}
        self._camera_states: Dict[str, CameraMetricsState] = {}
        self._states_lock = threading.Lock()

        # Timer thread control
        self._timer_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._running = False

        # Store factory reference for fetching camera info
        self._factory_ref: Optional["BusinessMetricsManagerFactory"] = None

        self.logger.info(
            f"[BUSINESS_METRICS_MANAGER] Initialized with output_topic={output_topic}, "
            f"aggregation_interval={aggregation_interval}s"
        )

    def set_factory_ref(self, factory: "BusinessMetricsManagerFactory"):
        """Set reference to factory for accessing deployment info."""
        self._factory_ref = factory

    def start(self):
        """Start the background timer thread for periodic publishing."""
        if self._running:
            self.logger.warning("[BUSINESS_METRICS_MANAGER] Already running")
            return

        self._running = True
        self._stop_event.clear()
        self._timer_thread = threading.Thread(
            target=self._timer_loop, daemon=True, name="BusinessMetricsTimer"
        )
        self._timer_thread.start()
        self.logger.info("[BUSINESS_METRICS_MANAGER] ✓ Started timer thread")

    def stop(self):
        """Stop the background timer thread gracefully."""
        if not self._running:
            return

        self.logger.info("[BUSINESS_METRICS_MANAGER] Stopping...")
        self._running = False
        self._stop_event.set()

        if self._timer_thread and self._timer_thread.is_alive():
            self._timer_thread.join(timeout=5)

        self.logger.info("[BUSINESS_METRICS_MANAGER] ✓ Stopped")

    def _timer_loop(self):
        """Background thread that checks and publishes metrics periodically."""
        self.logger.info(
            f"[BUSINESS_METRICS_MANAGER] Timer loop started (interval: {self.aggregation_interval}s, check_every: 10s)"
        )

        loop_count = 0
        while not self._stop_event.is_set():
            loop_count += 1
            try:
                self.logger.debug(f"[BUSINESS_METRICS_MANAGER] Timer loop iteration #{loop_count}")
                self._check_and_publish_all()
            except Exception as e:
                self.logger.error(
                    f"[BUSINESS_METRICS_MANAGER] Error in timer loop: {e}",
                    exc_info=True,
                )

            # Sleep in small increments to allow quick shutdown
            for _ in range(min(10, self.aggregation_interval)):
                if self._stop_event.is_set():
                    break
                time.sleep(1)

        self.logger.info("[BUSINESS_METRICS_MANAGER] Timer loop exited")

    def _check_and_publish_all(self):
        """Check all cameras and publish metrics if interval has passed."""
        current_time = time.monotonic()
        cameras_to_publish = []

        with self._states_lock:
            num_cameras = len(self._camera_states)
            if num_cameras > 0:
                self.logger.debug(
                    f"[BUSINESS_METRICS_MANAGER] _check_and_publish_all: checking {num_cameras} camera(s)"
                )

            for camera_id, state in self._camera_states.items():
                elapsed = current_time - state.last_push_at
                has_metrics = state.has_metrics()
                metrics_count = sum(len(agg.values) for agg in state.metrics.values())

                self.logger.debug(
                    f"[BUSINESS_METRICS_MANAGER] Camera {camera_id}: elapsed={elapsed:.1f}s, "
                    f"interval={self.aggregation_interval}s, has_metrics={has_metrics}, count={metrics_count}"
                )

                if elapsed >= self.aggregation_interval and has_metrics:
                    cameras_to_publish.append(camera_id)
                    self.logger.info(
                        f"[BUSINESS_METRICS_MANAGER] ✓ Camera {camera_id} ready for publish "
                        f"(elapsed={elapsed:.1f}s >= {self.aggregation_interval}s)"
                    )

        if cameras_to_publish:
            self.logger.info(
                f"[BUSINESS_METRICS_MANAGER] Publishing metrics for {len(cameras_to_publish)} camera(s)"
            )

        for camera_id in cameras_to_publish:
            try:
                success = self._publish_camera_metrics(camera_id)
                if success:
                    self.logger.info(
                        f"[BUSINESS_METRICS_MANAGER] ✓ Successfully published metrics for camera: {camera_id}"
                    )
                else:
                    self.logger.warning(
                        f"[BUSINESS_METRICS_MANAGER] ❌ Failed to publish metrics for camera: {camera_id}"
                    )
            except Exception as e:
                self.logger.error(
                    f"[BUSINESS_METRICS_MANAGER] Error publishing metrics for camera {camera_id}: {e}",
                    exc_info=True,
                )

    def _camera_info_sources(
        self, stream_info: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
        """Return the three dicts camera fields can arrive in.

        ``(camera_info, input_settings, input_camera_info)`` -- the direct
        ``camera_info`` block, the ``input_settings`` block, and the nested
        camera block, which the ``input_streams`` array overrides when present.
        """
        # Path 1: Direct camera_info in stream_info (most common for streaming)
        camera_info = stream_info.get("camera_info", {}) or {}
        self.logger.debug(f"[BUSINESS_METRICS_MANAGER] Direct camera_info = {camera_info}")

        # Path 2: From input_settings -> input_stream pattern
        input_settings = stream_info.get("input_settings", {}) or {}
        input_stream = input_settings.get("input_stream", {}) or {}
        input_camera_info = input_stream.get("camera_info", {}) or {}

        # Path 3: From input_streams array
        input_streams = stream_info.get("input_streams", [])
        if input_streams and len(input_streams) > 0:
            input_data = input_streams[0] if isinstance(input_streams[0], dict) else {}
            input_stream_inner = input_data.get("input_stream", input_data)
            input_camera_info = input_stream_inner.get("camera_info", {}) or input_camera_info

        return camera_info, input_settings, input_camera_info

    def _camera_id_from_topic(self, stream_info: Dict[str, Any]) -> str:
        """Camera id carried by the input topic name, or empty.

        Path 4: the topic is named ``<camera_id>_input_topic``, which in the
        streaming flow is the only place the id appears at all.
        """
        topic = stream_info.get("topic", "")
        if topic and "_input_topic" in topic:
            camera_id_from_topic = topic.replace("_input_topic", "").strip()
            self.logger.debug(
                f"[BUSINESS_METRICS_MANAGER] Extracted camera_id from topic: {camera_id_from_topic}"
            )
            return camera_id_from_topic
        return ""

    def _pick_camera_identity(
        self,
        camera_id_from_topic: str,
        stream_info: Dict[str, Any],
        camera_info: Dict[str, Any],
        input_camera_info: Dict[str, Any],
        input_settings: Dict[str, Any],
    ) -> Tuple[str, str]:
        """``(camera_name, camera_id)``, first non-empty across the sources.

        The topic-derived id wins over every declared one: it is the id the
        frames actually arrived under.
        """
        camera_name = (
            camera_info.get("camera_name", "")
            or input_camera_info.get("camera_name", "")
            or stream_info.get("camera_name", "")
            or input_settings.get("camera_name", "")
            or ""
        )
        camera_id = (
            camera_id_from_topic
            or camera_info.get("camera_id", "")
            or input_camera_info.get("camera_id", "")
            or stream_info.get("camera_id", "")
            or input_settings.get("camera_id", "")
            or camera_info.get("cameraId", "")
            or input_camera_info.get("cameraId", "")
            or ""
        )
        return camera_name, camera_id

    def _pick_deployment_ids(
        self,
        stream_info: Dict[str, Any],
        camera_info: Dict[str, Any],
        input_settings: Dict[str, Any],
    ) -> Tuple[str, str]:
        """``(app_deployment_id, application_id)``, snake_case preferred over camelCase."""
        app_deployment_id = (
            stream_info.get("app_deployment_id", "")
            or stream_info.get("appDeploymentId", "")
            or input_settings.get("app_deployment_id", "")
            or input_settings.get("appDeploymentId", "")
            or camera_info.get("app_deployment_id", "")
            or ""
        )
        application_id = (
            stream_info.get("application_id", "")
            or stream_info.get("applicationId", "")
            or input_settings.get("application_id", "")
            or input_settings.get("applicationId", "")
            or camera_info.get("application_id", "")
            or ""
        )
        return app_deployment_id, application_id

    def _pick_location_id(
        self,
        stream_info: Dict[str, Any],
        camera_info: Dict[str, Any],
        input_camera_info: Dict[str, Any],
    ) -> str:
        """Location id: explicit id fields first, else a resolvable ``location`` label.

        ``location`` doubles as a human label and as an ObjectId depending on the
        producer, so it is only promoted to an id when it actually looks like one.
        """
        from .post_processing_config_client import (
            is_resolvable_location_id,
            normalize_location_id,
        )

        location_from_label = ""
        for candidate in (
            camera_info.get("location"),
            input_camera_info.get("location"),
        ):
            text = str(candidate or "").strip()
            if is_resolvable_location_id(text):
                location_from_label = text
                break

        return normalize_location_id(
            camera_info.get("location_id", "")
            or camera_info.get("locationId", "")
            or input_camera_info.get("location_id", "")
            or input_camera_info.get("locationId", "")
            or stream_info.get("location_id", "")
            or stream_info.get("locationId", "")
            or location_from_label
            or ""
        )

    def _extract_camera_info_from_stream(
        self, stream_info: Optional[Dict[str, Any]]
    ) -> Dict[str, str]:
        """
        Extract camera info from stream_info.

        Stream info structure example:
        {
            'broker': 'localhost:9092',
            'topic': '692d7bde42582ffde3611908_input_topic',  # camera_id is here!
            'stream_time': '2025-12-02-05:09:53.914224 UTC',
            'camera_info': {
                'camera_name': 'cusstomer-cam-1',
                'camera_group': 'staging-customer-1',
                'location': '<location ObjectId>'
            },
            'frame_id': '...'
        }

        Args:
            stream_info: Stream metadata from usecase

        Returns:
            Dict with camera_id, camera_name, app_deployment_id, application_id, location_id
        """
        result = {
            "camera_id": "",
            "camera_name": "",
            "app_deployment_id": "",
            "application_id": "",
            "location_id": "",
        }

        if not stream_info:
            self.logger.debug(
                "[BUSINESS_METRICS_MANAGER] _extract_camera_info_from_stream: stream_info is None/empty"
            )
            return result

        self.logger.debug(
            f"[BUSINESS_METRICS_MANAGER] _extract_camera_info_from_stream: stream_info keys = {list(stream_info.keys())}"
        )

        try:
            # Try multiple paths to get camera info; merge them preferring non-empty values.
            camera_info, input_settings, input_camera_info = self._camera_info_sources(stream_info)
            camera_id_from_topic = self._camera_id_from_topic(stream_info)

            result["camera_name"], result["camera_id"] = self._pick_camera_identity(
                camera_id_from_topic, stream_info, camera_info, input_camera_info, input_settings
            )
            result["app_deployment_id"], result["application_id"] = self._pick_deployment_ids(
                stream_info, camera_info, input_settings
            )
            result["location_id"] = self._pick_location_id(
                stream_info, camera_info, input_camera_info
            )

            self.logger.debug(f"[BUSINESS_METRICS_MANAGER] Extracted camera info: {result}")

        except Exception as e:
            self.logger.error(
                f"[BUSINESS_METRICS_MANAGER] Error extracting camera info: {e}",
                exc_info=True,
            )

        return result

    def _fetch_location_name(self, location_id: str) -> str:
        """
        Fetch location name from API using location_id.

        Args:
            location_id: The location ID to look up

        Returns:
            Location name string, or 'Entry Reception' as default if API fails
        """
        global _location_name_cache
        default_location = "Entry Reception"

        from .post_processing_config_client import is_null_object_id, is_resolvable_location_id

        if (
            not location_id
            or is_null_object_id(location_id)
            or not is_resolvable_location_id(location_id)
        ):
            self.logger.debug(
                f"[BUSINESS_METRICS_MANAGER] No resolvable location_id, using default: '{default_location}'"
            )
            return default_location

        # Check cache first
        cached_name = _location_name_cache.resolved(location_id)
        if cached_name is not None:
            self.logger.debug(
                f"[BUSINESS_METRICS_MANAGER] Using cached location name for '{location_id}': '{cached_name}'"
            )
            return cached_name

        # Need factory reference with session to make API call
        if not self._factory_ref or not self._factory_ref._session:
            self.logger.warning(
                f"[BUSINESS_METRICS_MANAGER] No session available for location API, using default: '{default_location}'"
            )
            return default_location

        # A recent failure suppresses the request for a cool-off, but no longer forever:
        # caching the failure pinned the placeholder onto every row for this location
        # for the life of the process, and the API recovering changed nothing (INC-2606).
        if not _location_name_cache.should_fetch(location_id):
            return default_location

        try:
            endpoint = f"/v1/inference/get_location/{location_id}"
            self.logger.info(
                f"[BUSINESS_METRICS_MANAGER] Fetching location name from API: {endpoint}"
            )

            response = self._factory_ref._session.rpc.get(
                endpoint, timeout=3, raise_exception=False
            )

            if response and isinstance(response, dict):
                success = response.get("success", False)
                if success:
                    data = response.get("data", {})
                    location_name = data.get("locationName", default_location)
                    self.logger.info(
                        f"[BUSINESS_METRICS_MANAGER] ✓ Fetched location name: '{location_name}' for location_id: '{location_id}'"
                    )

                    # Cache the result
                    _location_name_cache.store(location_id, location_name)
                    return location_name
                else:
                    self.logger.warning(
                        f"[BUSINESS_METRICS_MANAGER] API returned success=false for location_id '{location_id}': "
                        f"{response.get('message', 'Unknown error')}"
                    )
            else:
                self.logger.warning(
                    f"[BUSINESS_METRICS_MANAGER] Invalid response format from API: {response}"
                )

        except Exception as e:
            self.logger.error(
                f"[BUSINESS_METRICS_MANAGER] Error fetching location name for '{location_id}': {e}",
                exc_info=True,
            )

        # Use default on any failure
        self.logger.info(
            f"[BUSINESS_METRICS_MANAGER] Using default location name: '{default_location}'"
        )
        _location_name_cache.note_failure(location_id)
        return default_location

    def _resolve_metrics_identity(
        self, camera_id: str, stream_info: Optional[Dict[str, Any]]
    ) -> Dict[str, str]:
        """Settle the camera/deployment identity this batch of metrics belongs to.

        Precedence is ``stream_info`` over the factory's jobParams values, then
        the ``camera_id`` the caller passed. The location NAME is resolved here
        too, because it is an API lookup keyed on the id this method settles.
        """
        camera_info = self._extract_camera_info_from_stream(stream_info)
        self.logger.debug(f"[BUSINESS_METRICS_MANAGER] Extracted camera_info: {camera_info}")

        # Get factory app_deployment_id and application_id if available (from jobParams)
        factory_app_deployment_id = ""
        factory_application_id = ""
        if self._factory_ref:
            factory_app_deployment_id = self._factory_ref._app_deployment_id or ""
            factory_application_id = self._factory_ref._application_id or ""
            self.logger.debug(
                f"[BUSINESS_METRICS_MANAGER] Factory values - "
                f"app_deployment_id: {factory_app_deployment_id}, application_id: {factory_application_id}"
            )

        resolved = {
            "camera_id": camera_info.get("camera_id") or camera_id or "",
            "camera_name": camera_info.get("camera_name") or "",
            "app_deployment_id": camera_info.get("app_deployment_id")
            or factory_app_deployment_id
            or "",
            "application_id": camera_info.get("application_id") or factory_application_id or "",
            "location_id": camera_info.get("location_id") or "",
            "stream_time": self._extract_stream_time(stream_info),
        }
        # Fetch location_name from API using location_id
        resolved["location_name"] = self._fetch_location_name(resolved["location_id"])

        self.logger.info(
            f"[BUSINESS_METRICS_MANAGER] Final values - camera_id={resolved['camera_id']}, "
            f"camera_name={resolved['camera_name']}, app_deployment_id={resolved['app_deployment_id']}, "
            f"application_id={resolved['application_id']}, location_id={resolved['location_id']}, "
            f"location_name={resolved['location_name']}"
        )
        return resolved

    def _extract_stream_time(self, stream_info: Optional[Dict[str, Any]]) -> str:
        """The frame's stream_time, top level first then nested under input_settings."""
        if not stream_info:
            return ""
        stream_time = stream_info.get("stream_time", "")
        if not stream_time:
            # Try alternative paths
            input_settings = stream_info.get("input_settings", {})
            if isinstance(input_settings, dict):
                stream_time = input_settings.get("stream_time", "")
        return stream_time

    def _upsert_camera_state(self, resolved: Dict[str, str]) -> CameraMetricsState:
        """Get or create this camera's state, back-filling identity fields.

        Identity fields are only ever filled in, never overwritten: the first
        non-empty value wins for the life of the state, because a later frame
        arriving without camera_info must not blank a name already published.
        ``stream_time`` is the exception -- it is the frame clock, so it always
        takes the newest value.
        """
        with self._states_lock:
            if resolved["camera_id"] not in self._camera_states:
                self._camera_states[resolved["camera_id"]] = CameraMetricsState(
                    camera_id=resolved["camera_id"],
                    camera_name=resolved["camera_name"],
                    app_deployment_id=resolved["app_deployment_id"],
                    application_id=resolved["application_id"],
                    location_id=resolved["location_id"],
                    location_name=resolved["location_name"],
                    stream_time=resolved["stream_time"],
                )
                self.logger.info(
                    f"[BUSINESS_METRICS_MANAGER] ✓ Created new state for camera: {resolved['camera_id']}"
                )

            state = self._camera_states[resolved["camera_id"]]

            # Update camera info if we have better values
            for attr in (
                "camera_name",
                "app_deployment_id",
                "application_id",
                "location_id",
                "location_name",
            ):
                if resolved[attr] and not getattr(state, attr):
                    setattr(state, attr, resolved[attr])
                    self.logger.debug(
                        f"[BUSINESS_METRICS_MANAGER] Updated {attr} to: {resolved[attr]}"
                    )
            # Always update stream_time with most recent value
            if resolved["stream_time"]:
                state.stream_time = resolved["stream_time"]
                self.logger.debug(
                    f"[BUSINESS_METRICS_MANAGER] Updated stream_time to: {resolved['stream_time']}"
                )

        return state

    def _ingest_metric_values(self, state: CameraMetricsState, metrics_data: Dict[str, Any]) -> int:
        """Feed each numeric metric into its aggregator; return how many landed.

        ``area_utilization`` arrives as a per-area dict and is collapsed to the
        mean across areas first. Non-numeric payloads (``peak_areas``,
        ``optimization_opportunities``, strings, nested objects) are dropped --
        there is no aggregation defined for them.
        """
        metrics_added = 0
        for metric_name, raw_value in metrics_data.items():
            # Skip non-numeric fields and complex objects
            if metric_name in ["peak_areas", "optimization_opportunities"]:
                continue

            value = raw_value
            # Handle area_utilization which is a dict
            if metric_name == "area_utilization" and isinstance(value, dict):
                # Average all area utilization values
                area_values = [v for v in value.values() if isinstance(v, (int, float))]
                if area_values:
                    value = sum(area_values) / len(area_values)
                else:
                    continue

            # Only process numeric values
            if isinstance(value, (int, float)):
                agg_type = self.metrics_config.get(metric_name, "mean")
                with self._states_lock:
                    state.add_metric_value(metric_name, value, agg_type)
                    metrics_added += 1

        self.logger.debug(
            f"[BUSINESS_METRICS_MANAGER] Added {metrics_added} metric values to aggregator"
        )
        return metrics_added

    def _publish_interval_elapsed(self, state: CameraMetricsState) -> bool:
        """True when this camera is both due and has something to publish."""
        current_time = time.monotonic()

        with self._states_lock:
            elapsed = current_time - state.last_push_at
            has_metrics = state.has_metrics()
            metrics_count = sum(len(agg.values) for agg in state.metrics.values())

            self.logger.debug(
                f"[BUSINESS_METRICS_MANAGER] Publish check - elapsed={elapsed:.1f}s, "
                f"interval={self.aggregation_interval}s, has_metrics={has_metrics}, "
                f"total_values_count={metrics_count}"
            )

            if elapsed >= self.aggregation_interval and has_metrics:
                self.logger.info(
                    f"[BUSINESS_METRICS_MANAGER] ✓ PUBLISH CONDITION MET! "
                    f"elapsed={elapsed:.1f}s >= interval={self.aggregation_interval}s"
                )
                return True

            remaining = self.aggregation_interval - elapsed
            self.logger.debug(
                f"[BUSINESS_METRICS_MANAGER] Not publishing yet. "
                f"Remaining time: {remaining:.1f}s, metrics_count={metrics_count}"
            )
            return False

    def process_metrics(
        self,
        camera_id: str,
        metrics_data: Dict[str, Any],
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Process business metrics and add to aggregation.

        This method:
        1. Extracts camera info from stream_info
        2. Adds each metric value to the appropriate aggregator
        3. Checks if aggregation interval has passed and publishes if so

        Args:
            camera_id: Unique camera identifier
            metrics_data: Business metrics dictionary from usecase
            stream_info: Stream metadata

        Returns:
            True if metrics were published, False otherwise
        """
        try:
            self.logger.debug("[BUSINESS_METRICS_MANAGER] ===== process_metrics START =====")
            self.logger.debug(f"[BUSINESS_METRICS_MANAGER] Input camera_id param: {camera_id}")
            self.logger.debug(
                f"[BUSINESS_METRICS_MANAGER] metrics_data keys: {list(metrics_data.keys()) if metrics_data else 'None'}"
            )

            if not metrics_data or not isinstance(metrics_data, dict):
                self.logger.debug(
                    "[BUSINESS_METRICS_MANAGER] Empty or invalid metrics data, skipping"
                )
                return False

            resolved = self._resolve_metrics_identity(camera_id, stream_info)
            state = self._upsert_camera_state(resolved)
            self._ingest_metric_values(state, metrics_data)

            # Check if we should publish (interval elapsed)
            if self._publish_interval_elapsed(state):
                self.logger.info(
                    f"[BUSINESS_METRICS_MANAGER] Triggering publish for camera: {resolved['camera_id']}"
                )
                return self._publish_camera_metrics(resolved["camera_id"])

            self.logger.debug(
                "[BUSINESS_METRICS_MANAGER] ===== process_metrics END (no publish) ====="
            )
            return False

        except Exception as e:
            self.logger.error(
                f"[BUSINESS_METRICS_MANAGER] Error processing metrics: {e}",
                exc_info=True,
            )
            return False

    def _publish_camera_metrics(self, camera_id: str) -> bool:
        """
        Publish aggregated metrics for a specific camera.

        Args:
            camera_id: Camera identifier

        Returns:
            True if published successfully, False otherwise
        """
        self.logger.info("[BUSINESS_METRICS_MANAGER] ========== PUBLISHING METRICS ==========")

        try:
            with self._states_lock:
                if camera_id not in self._camera_states:
                    self.logger.warning(
                        f"[BUSINESS_METRICS_MANAGER] No state found for camera: {camera_id}"
                    )
                    return False

                state = self._camera_states[camera_id]

                if not state.has_metrics():
                    self.logger.debug(
                        f"[BUSINESS_METRICS_MANAGER] No metrics to publish for camera: {camera_id}"
                    )
                    return False

                # Build the message
                aggregated_metrics = state.get_aggregated_metrics()

                # Get application_id from factory if not in state (fallback)
                final_application_id = state.application_id
                if not final_application_id and self._factory_ref:
                    final_application_id = self._factory_ref._application_id or ""

                message = {
                    "camera_id": state.camera_id,
                    "camera_name": state.camera_name,
                    "app_deployment_id": state.app_deployment_id,
                    "application_id": final_application_id,  # Ensure application_id is included
                    "location_name": state.location_name,
                    "stream_time": state.stream_time,  # Add stream_time from state
                    "business_metrics": aggregated_metrics,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "aggregation_interval_seconds": self.aggregation_interval,
                }

                # Reset metrics after building message (inside lock)
                state.reset_metrics()

            self.logger.info(
                f"[BUSINESS_METRICS_MANAGER] Built metrics message: {json.dumps(message, default=str)[:500]}..."
            )

            success = False

            # Try Redis first (primary)
            if self.redis_client:
                try:
                    self.logger.debug(
                        f"[BUSINESS_METRICS_MANAGER] Publishing to Redis stream: {self.output_topic}"
                    )
                    self._publish_to_redis(self.output_topic, message)
                    self.logger.info("[BUSINESS_METRICS_MANAGER] ✓ Metrics published to Redis")
                    success = True
                except Exception as e:
                    self.logger.error(
                        f"[BUSINESS_METRICS_MANAGER] ❌ Redis publish failed: {e}",
                        exc_info=True,
                    )

            # Fallback to Kafka if Redis failed or no Redis client
            if not success and self.kafka_client:
                try:
                    self.logger.debug(
                        f"[BUSINESS_METRICS_MANAGER] Publishing to Kafka topic: {self.output_topic}"
                    )
                    self._publish_to_kafka(self.output_topic, message)
                    self.logger.info("[BUSINESS_METRICS_MANAGER] ✓ Metrics published to Kafka")
                    success = True
                except Exception as e:
                    self.logger.error(
                        f"[BUSINESS_METRICS_MANAGER] ❌ Kafka publish failed: {e}",
                        exc_info=True,
                    )

            if success:
                self.logger.info(
                    "[BUSINESS_METRICS_MANAGER] ========== METRICS PUBLISHED =========="
                )
            else:
                self.logger.error(
                    "[BUSINESS_METRICS_MANAGER] ❌ METRICS NOT PUBLISHED (both transports failed)"
                )

            return success

        except Exception as e:
            self.logger.error(
                f"[BUSINESS_METRICS_MANAGER] Error publishing metrics: {e}",
                exc_info=True,
            )
            return False

    def _publish_to_redis(self, topic: str, message: Dict[str, Any]):
        """Publish message to Redis stream."""
        try:
            self.redis_client.add_message(
                topic_or_channel=topic,
                message=json.dumps(message),
                key=message.get("camera_id", ""),
            )
        except Exception as e:
            self.logger.error(f"[BUSINESS_METRICS_MANAGER] Redis publish error: {e}")
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
            self.logger.error(f"[BUSINESS_METRICS_MANAGER] Kafka publish error: {e}")
            raise

    def reset_camera_state(self, camera_id: str):
        """Reset metrics state for a specific camera."""
        with self._states_lock:
            if camera_id in self._camera_states:
                self._camera_states[camera_id].reset_metrics()
                self.logger.info(f"[BUSINESS_METRICS_MANAGER] Reset state for camera: {camera_id}")

    def get_camera_state(self, camera_id: str) -> Optional[Dict[str, Any]]:
        """Get current metrics state for a camera (for debugging)."""
        with self._states_lock:
            state = self._camera_states.get(camera_id)
            if state:
                return {
                    "camera_id": state.camera_id,
                    "camera_name": state.camera_name,
                    "app_deployment_id": state.app_deployment_id,
                    "application_id": state.application_id,
                    "location_id": state.location_id,
                    "location_name": state.location_name,
                    "metrics_count": {name: len(agg.values) for name, agg in state.metrics.items()},
                    "last_push_time": state.last_push_time,
                    "seconds_since_push": time.monotonic() - state.last_push_at,
                }
            return None

    def get_all_camera_states(self) -> Dict[str, Dict[str, Any]]:
        """Get all camera states for debugging/monitoring."""
        with self._states_lock:
            return {
                cam_id: {
                    "camera_id": state.camera_id,
                    "camera_name": state.camera_name,
                    "location_name": state.location_name,
                    "metrics_count": {name: len(agg.values) for name, agg in state.metrics.items()},
                    "last_push_time": state.last_push_time,
                    "seconds_since_push": time.monotonic() - state.last_push_at,
                }
                for cam_id, state in self._camera_states.items()
            }

    def force_publish_all(self) -> int:
        """Force publish all cameras with pending metrics. Returns count published."""
        published_count = 0
        # Collect camera IDs with pending metrics without holding the lock during publish
        with self._states_lock:
            camera_ids = [
                cam_id for cam_id, state in self._camera_states.items() if state.has_metrics()
            ]
        for camera_id in camera_ids:
            if self._publish_camera_metrics(camera_id):
                published_count += 1
        return published_count

    def set_metrics_config(self, metrics_config: Dict[str, str]):
        """
        Set aggregation type configuration for metrics.

        Args:
            metrics_config: Dict of metric_name -> aggregation_type
        """
        self.metrics_config = metrics_config
        self.logger.info(f"[BUSINESS_METRICS_MANAGER] Updated metrics config: {metrics_config}")

    def set_aggregation_interval(self, interval_seconds: int):
        """
        Set the aggregation interval.

        Args:
            interval_seconds: New interval in seconds
        """
        self.aggregation_interval = interval_seconds
        self.logger.info(
            f"[BUSINESS_METRICS_MANAGER] Updated aggregation interval to {interval_seconds}s"
        )
