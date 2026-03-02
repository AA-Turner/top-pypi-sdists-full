"""
business_metrics_manager_utils.py

Manages business metrics aggregation and publishing to Redis/Kafka.
Aggregates metrics for 5 minutes (300 seconds) and pushes to output topic.
Supports aggregation types: mean (default), min, max, sum.

PRODUCTION-READY VERSION
"""

import json
import time
import threading
import logging
import os
import urllib.request
import base64
import re
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timezone
from dataclasses import dataclass, field
from pathlib import Path


# Default aggregation interval in seconds (5 minutes)
DEFAULT_AGGREGATION_INTERVAL = 300

# Supported aggregation types
AGGREGATION_TYPES = ["mean", "min", "max", "sum"]

# Cache for location names to avoid repeated API calls
_location_name_cache: Dict[str, str] = {}

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
                        "agg_type": aggregator.agg_type
                    }
        return result
    
    def reset_metrics(self):
        """Reset all metric aggregators."""
        for aggregator in self.metrics.values():
            aggregator.reset()
        self.last_push_time = time.time()
    
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
        logger: Optional[logging.Logger] = None
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
        self._factory_ref: Optional['BusinessMetricsManagerFactory'] = None
        
        self.logger.info(
            f"[BUSINESS_METRICS_MANAGER] Initialized with output_topic={output_topic}, "
            f"aggregation_interval={aggregation_interval}s"
        )
    
    def set_factory_ref(self, factory: 'BusinessMetricsManagerFactory'):
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
            target=self._timer_loop,
            daemon=True,
            name="BusinessMetricsTimer"
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
            f"[BUSINESS_METRICS_MANAGER] Timer loop started "
            f"(interval: {self.aggregation_interval}s, check_every: 10s)"
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
                    exc_info=True
                )
            
            # Sleep in small increments to allow quick shutdown
            for _ in range(min(10, self.aggregation_interval)):
                if self._stop_event.is_set():
                    break
                time.sleep(1)
        
        self.logger.info("[BUSINESS_METRICS_MANAGER] Timer loop exited")
    
    def _check_and_publish_all(self):
        """Check all cameras and publish metrics if interval has passed."""
        current_time = time.time()
        cameras_to_publish = []
        
        with self._states_lock:
            num_cameras = len(self._camera_states)
            if num_cameras > 0:
                self.logger.debug(f"[BUSINESS_METRICS_MANAGER] _check_and_publish_all: checking {num_cameras} camera(s)")
            
            for camera_id, state in self._camera_states.items():
                elapsed = current_time - state.last_push_time
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
            self.logger.info(f"[BUSINESS_METRICS_MANAGER] Publishing metrics for {len(cameras_to_publish)} camera(s)")
        
        for camera_id in cameras_to_publish:
            try:
                success = self._publish_camera_metrics(camera_id)
                if success:
                    self.logger.info(f"[BUSINESS_METRICS_MANAGER] ✓ Successfully published metrics for camera: {camera_id}")
                else:
                    self.logger.warning(f"[BUSINESS_METRICS_MANAGER] ❌ Failed to publish metrics for camera: {camera_id}")
            except Exception as e:
                self.logger.error(
                    f"[BUSINESS_METRICS_MANAGER] Error publishing metrics for "
                    f"camera {camera_id}: {e}", 
                    exc_info=True
                )
    
    def _extract_camera_info_from_stream(
        self, 
        stream_info: Optional[Dict[str, Any]]
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
                'location': '6908756db129880c34f2e09a'
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
            "location_id": ""
        }
        
        if not stream_info:
            self.logger.debug("[BUSINESS_METRICS_MANAGER] _extract_camera_info_from_stream: stream_info is None/empty")
            return result
        
        self.logger.debug(f"[BUSINESS_METRICS_MANAGER] _extract_camera_info_from_stream: stream_info keys = {list(stream_info.keys())}")
        
        try:
            # Try multiple paths to get camera info
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
            
            # Path 4: Extract camera_id from topic field (e.g., "692d7bde42582ffde3611908_input_topic")
            topic = stream_info.get("topic", "")
            camera_id_from_topic = ""
            if topic and "_input_topic" in topic:
                camera_id_from_topic = topic.replace("_input_topic", "").strip()
                self.logger.debug(f"[BUSINESS_METRICS_MANAGER] Extracted camera_id from topic: {camera_id_from_topic}")
            
            # Merge all sources, preferring non-empty values
            # camera_name - prefer camera_info.camera_name
            result["camera_name"] = (
                camera_info.get("camera_name", "") or
                input_camera_info.get("camera_name", "") or
                stream_info.get("camera_name", "") or
                input_settings.get("camera_name", "") or
                ""
            )
            
            # camera_id - try topic extraction first, then other sources
            result["camera_id"] = (
                camera_id_from_topic or
                camera_info.get("camera_id", "") or
                input_camera_info.get("camera_id", "") or
                stream_info.get("camera_id", "") or
                input_settings.get("camera_id", "") or
                camera_info.get("cameraId", "") or
                input_camera_info.get("cameraId", "") or
                ""
            )
            
            # app_deployment_id
            result["app_deployment_id"] = (
                stream_info.get("app_deployment_id", "") or
                stream_info.get("appDeploymentId", "") or
                input_settings.get("app_deployment_id", "") or
                input_settings.get("appDeploymentId", "") or
                camera_info.get("app_deployment_id", "") or
                ""
            )
            
            # application_id
            result["application_id"] = (
                stream_info.get("application_id", "") or
                stream_info.get("applicationId", "") or
                input_settings.get("application_id", "") or
                input_settings.get("applicationId", "") or
                camera_info.get("application_id", "") or
                ""
            )
            
            # location_id - from camera_info.location
            result["location_id"] = (
                camera_info.get("location", "") or
                camera_info.get("location_id", "") or
                camera_info.get("locationId", "") or
                input_camera_info.get("location", "") or
                input_camera_info.get("location_id", "") or
                ""
            )
            
            self.logger.debug(f"[BUSINESS_METRICS_MANAGER] Extracted camera info: {result}")
            
        except Exception as e:
            self.logger.error(f"[BUSINESS_METRICS_MANAGER] Error extracting camera info: {e}", exc_info=True)
        
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
        
        if not location_id:
            self.logger.debug(f"[BUSINESS_METRICS_MANAGER] No location_id provided, using default: '{default_location}'")
            return default_location
        
        # Check cache first
        if location_id in _location_name_cache:
            cached_name = _location_name_cache[location_id]
            self.logger.debug(f"[BUSINESS_METRICS_MANAGER] Using cached location name for '{location_id}': '{cached_name}'")
            return cached_name
        
        # Need factory reference with session to make API call
        if not self._factory_ref or not self._factory_ref._session:
            self.logger.warning(f"[BUSINESS_METRICS_MANAGER] No session available for location API, using default: '{default_location}'")
            return default_location
        
        try:
            endpoint = f"/v1/inference/get_location/{location_id}"
            self.logger.info(f"[BUSINESS_METRICS_MANAGER] Fetching location name from API: {endpoint}")
            
            response = self._factory_ref._session.rpc.get(endpoint)
            
            if response and isinstance(response, dict):
                success = response.get("success", False)
                if success:
                    data = response.get("data", {})
                    location_name = data.get("locationName", default_location)
                    self.logger.info(f"[BUSINESS_METRICS_MANAGER] ✓ Fetched location name: '{location_name}' for location_id: '{location_id}'")
                    
                    # Cache the result
                    _location_name_cache[location_id] = location_name
                    return location_name
                else:
                    self.logger.warning(
                        f"[BUSINESS_METRICS_MANAGER] API returned success=false for location_id '{location_id}': "
                        f"{response.get('message', 'Unknown error')}"
                    )
            else:
                self.logger.warning(f"[BUSINESS_METRICS_MANAGER] Invalid response format from API: {response}")
                
        except Exception as e:
            self.logger.error(f"[BUSINESS_METRICS_MANAGER] Error fetching location name for '{location_id}': {e}", exc_info=True)
        
        # Use default on any failure
        self.logger.info(f"[BUSINESS_METRICS_MANAGER] Using default location name: '{default_location}'")
        _location_name_cache[location_id] = default_location
        return default_location
    
    def process_metrics(
        self,
        camera_id: str,
        metrics_data: Dict[str, Any],
        stream_info: Optional[Dict[str, Any]] = None
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
            self.logger.debug(f"[BUSINESS_METRICS_MANAGER] ===== process_metrics START =====")
            self.logger.debug(f"[BUSINESS_METRICS_MANAGER] Input camera_id param: {camera_id}")
            self.logger.debug(f"[BUSINESS_METRICS_MANAGER] metrics_data keys: {list(metrics_data.keys()) if metrics_data else 'None'}")
            
            if not metrics_data or not isinstance(metrics_data, dict):
                self.logger.debug("[BUSINESS_METRICS_MANAGER] Empty or invalid metrics data, skipping")
                return False
            
            # Extract camera info from stream_info
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
            
            # Use extracted or fallback values
            # Priority: stream_info > factory (from jobParams)
            final_camera_id = camera_info.get("camera_id") or camera_id or ""
            final_camera_name = camera_info.get("camera_name") or ""
            final_app_deployment_id = camera_info.get("app_deployment_id") or factory_app_deployment_id or ""
            final_application_id = camera_info.get("application_id") or factory_application_id or ""
            final_location_id = camera_info.get("location_id") or ""
            
            # Extract stream_time from stream_info
            final_stream_time = ""
            if stream_info:
                final_stream_time = stream_info.get("stream_time", "")
                if not final_stream_time:
                    # Try alternative paths
                    input_settings = stream_info.get("input_settings", {})
                    if isinstance(input_settings, dict):
                        final_stream_time = input_settings.get("stream_time", "")
            
            # Fetch location_name from API using location_id
            final_location_name = self._fetch_location_name(final_location_id)
            
            self.logger.info(
                f"[BUSINESS_METRICS_MANAGER] Final values - camera_id={final_camera_id}, "
                f"camera_name={final_camera_name}, app_deployment_id={final_app_deployment_id}, "
                f"application_id={final_application_id}, location_id={final_location_id}, "
                f"location_name={final_location_name}"
            )
            
            with self._states_lock:
                # Get or create state for this camera
                if final_camera_id not in self._camera_states:
                    self._camera_states[final_camera_id] = CameraMetricsState(
                        camera_id=final_camera_id,
                        camera_name=final_camera_name,
                        app_deployment_id=final_app_deployment_id,
                        application_id=final_application_id,
                        location_id=final_location_id,
                        location_name=final_location_name,
                        stream_time=final_stream_time
                    )
                    self.logger.info(
                        f"[BUSINESS_METRICS_MANAGER] ✓ Created new state for camera: {final_camera_id}"
                    )
                
                state = self._camera_states[final_camera_id]
                
                # Update camera info if we have better values
                if final_camera_name and not state.camera_name:
                    state.camera_name = final_camera_name
                    self.logger.debug(f"[BUSINESS_METRICS_MANAGER] Updated camera_name to: {final_camera_name}")
                if final_app_deployment_id and not state.app_deployment_id:
                    state.app_deployment_id = final_app_deployment_id
                    self.logger.debug(f"[BUSINESS_METRICS_MANAGER] Updated app_deployment_id to: {final_app_deployment_id}")
                if final_application_id and not state.application_id:
                    state.application_id = final_application_id
                    self.logger.debug(f"[BUSINESS_METRICS_MANAGER] Updated application_id to: {final_application_id}")
                if final_location_id and not state.location_id:
                    state.location_id = final_location_id
                    self.logger.debug(f"[BUSINESS_METRICS_MANAGER] Updated location_id to: {final_location_id}")
                if final_location_name and not state.location_name:
                    state.location_name = final_location_name
                    self.logger.debug(f"[BUSINESS_METRICS_MANAGER] Updated location_name to: {final_location_name}")
                # Always update stream_time with most recent value
                if final_stream_time:
                    state.stream_time = final_stream_time
                    self.logger.debug(f"[BUSINESS_METRICS_MANAGER] Updated stream_time to: {final_stream_time}")
            
            # Add each metric value to aggregator
            metrics_added = 0
            for metric_name, value in metrics_data.items():
                # Skip non-numeric fields and complex objects
                if metric_name in ["peak_areas", "optimization_opportunities"]:
                    continue
                
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
            
            self.logger.debug(f"[BUSINESS_METRICS_MANAGER] Added {metrics_added} metric values to aggregator")
            
            # Check if we should publish (interval elapsed)
            current_time = time.time()
            should_publish = False
            elapsed = 0.0
            metrics_count = 0
            
            with self._states_lock:
                elapsed = current_time - state.last_push_time
                has_metrics = state.has_metrics()
                metrics_count = sum(len(agg.values) for agg in state.metrics.values())
                
                self.logger.debug(
                    f"[BUSINESS_METRICS_MANAGER] Publish check - elapsed={elapsed:.1f}s, "
                    f"interval={self.aggregation_interval}s, has_metrics={has_metrics}, "
                    f"total_values_count={metrics_count}"
                )
                
                if elapsed >= self.aggregation_interval and has_metrics:
                    should_publish = True
                    self.logger.info(
                        f"[BUSINESS_METRICS_MANAGER] ✓ PUBLISH CONDITION MET! "
                        f"elapsed={elapsed:.1f}s >= interval={self.aggregation_interval}s"
                    )
                else:
                    remaining = self.aggregation_interval - elapsed
                    self.logger.debug(
                        f"[BUSINESS_METRICS_MANAGER] Not publishing yet. "
                        f"Remaining time: {remaining:.1f}s, metrics_count={metrics_count}"
                    )
            
            if should_publish:
                self.logger.info(f"[BUSINESS_METRICS_MANAGER] Triggering publish for camera: {final_camera_id}")
                return self._publish_camera_metrics(final_camera_id)
            
            self.logger.debug(f"[BUSINESS_METRICS_MANAGER] ===== process_metrics END (no publish) =====")
            return False
            
        except Exception as e:
            self.logger.error(
                f"[BUSINESS_METRICS_MANAGER] Error processing metrics: {e}", 
                exc_info=True
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
        self.logger.info(f"[BUSINESS_METRICS_MANAGER] ========== PUBLISHING METRICS ==========")
        
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
                    "aggregation_interval_seconds": self.aggregation_interval
                }
                
                # Reset metrics after building message (inside lock)
                state.reset_metrics()
            
            self.logger.info(
                f"[BUSINESS_METRICS_MANAGER] Built metrics message: "
                f"{json.dumps(message, default=str)[:500]}..."
            )
            
            success = False
            
            # Try Redis first (primary)
            if self.redis_client:
                try:
                    self.logger.debug(
                        f"[BUSINESS_METRICS_MANAGER] Publishing to Redis stream: {self.output_topic}"
                    )
                    self._publish_to_redis(self.output_topic, message)
                    self.logger.info(
                        f"[BUSINESS_METRICS_MANAGER] ✓ Metrics published to Redis"
                    )
                    success = True
                except Exception as e:
                    self.logger.error(
                        f"[BUSINESS_METRICS_MANAGER] ❌ Redis publish failed: {e}", 
                        exc_info=True
                    )
            
            # Fallback to Kafka if Redis failed or no Redis client
            if not success and self.kafka_client:
                try:
                    self.logger.debug(
                        f"[BUSINESS_METRICS_MANAGER] Publishing to Kafka topic: {self.output_topic}"
                    )
                    self._publish_to_kafka(self.output_topic, message)
                    self.logger.info(
                        f"[BUSINESS_METRICS_MANAGER] ✓ Metrics published to Kafka"
                    )
                    success = True
                except Exception as e:
                    self.logger.error(
                        f"[BUSINESS_METRICS_MANAGER] ❌ Kafka publish failed: {e}", 
                        exc_info=True
                    )
            
            if success:
                self.logger.info(f"[BUSINESS_METRICS_MANAGER] ========== METRICS PUBLISHED ==========")
            else:
                self.logger.error(
                    f"[BUSINESS_METRICS_MANAGER] ❌ METRICS NOT PUBLISHED (both transports failed)"
                )
            
            return success
            
        except Exception as e:
            self.logger.error(
                f"[BUSINESS_METRICS_MANAGER] Error publishing metrics: {e}", 
                exc_info=True
            )
            return False
    
    def _publish_to_redis(self, topic: str, message: Dict[str, Any]):
        """Publish message to Redis stream."""
        try:
            self.redis_client.add_message(
                topic_or_channel=topic,
                message=json.dumps(message),
                key=message.get("camera_id", "")
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
                key=message.get("camera_id", "")
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
                    "metrics_count": {
                        name: len(agg.values) 
                        for name, agg in state.metrics.items()
                    },
                    "last_push_time": state.last_push_time,
                    "seconds_since_push": time.time() - state.last_push_time
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
                    "metrics_count": {
                        name: len(agg.values) 
                        for name, agg in state.metrics.items()
                    },
                    "last_push_time": state.last_push_time,
                    "seconds_since_push": time.time() - state.last_push_time
                }
                for cam_id, state in self._camera_states.items()
            }
    
    def force_publish_all(self) -> int:
        """Force publish all cameras with pending metrics. Returns count published."""
        published_count = 0
        # Collect camera IDs with pending metrics without holding the lock during publish
        with self._states_lock:
            camera_ids = [cam_id for cam_id, state in self._camera_states.items() if state.has_metrics()]
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


class BusinessMetricsManagerFactory:
    """
    Factory class for creating BUSINESS_METRICS_MANAGER instances.
    
    Handles session initialization and Redis/Kafka client creation
    following the same pattern as IncidentManagerFactory.
    """
    
    ACTION_ID_PATTERN = re.compile(r"^[0-9a-f]{8,}$", re.IGNORECASE)
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        self._initialized = False
        self._business_metrics_manager: Optional[BUSINESS_METRICS_MANAGER] = None
        
        # Store these for later access
        self._session = None
        self._action_id: Optional[str] = None
        self._instance_id: Optional[str] = None
        self._deployment_id: Optional[str] = None
        self._app_deployment_id: Optional[str] = None
        self._application_id: Optional[str] = None  # Store application_id from jobParams
        self._external_ip: Optional[str] = None
    
    def initialize(
        self, 
        config: Any,
        aggregation_interval: int = DEFAULT_AGGREGATION_INTERVAL,
        metrics_config: Optional[Dict[str, str]] = None
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
            from matrice_common.stream.matrice_stream import MatriceStream, StreamType
            from matrice_common.session import Session
            
            self.logger.info("[BUSINESS_METRICS_MANAGER_FACTORY] ===== STARTING INITIALIZATION =====")
            
            # Get or create session
            self._session = getattr(config, 'session', None)
            if not self._session:
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
                
                self._session = Session(
                    account_number=account_number,
                    access_key=access_key_id,
                    secret_key=secret_key,
                    project_id=project_id,
                )
                self.logger.info("[BUSINESS_METRICS_MANAGER_FACTORY] ✓ Created session from environment")
            else:
                self.logger.info("[BUSINESS_METRICS_MANAGER_FACTORY] ✓ Using session from config")
            
            rpc = self._session.rpc
            
            # Discover action_id
            self._action_id = self._discover_action_id()
            if not self._action_id:
                self.logger.error("[BUSINESS_METRICS_MANAGER_FACTORY] ❌ Could not discover action_id")
                print("----- BUSINESS METRICS MANAGER ACTION DISCOVERY -----")
                print("action_id: NOT FOUND")
                print("------------------------------------------------------")
                self._initialized = True
                return None
            
            self.logger.info(f"[BUSINESS_METRICS_MANAGER_FACTORY] ✓ Discovered action_id: {self._action_id}")
            
            # Fetch action details
            action_details = {}
            try:
                action_url = f"/v1/actions/action/{self._action_id}/details"
                action_resp = rpc.get(action_url)
                if not (action_resp and action_resp.get("success", False)):
                    raise RuntimeError(
                        action_resp.get("message", "Unknown error") 
                        if isinstance(action_resp, dict) else "Unknown error"
                    )
                action_doc = action_resp.get("data", {}) if isinstance(action_resp, dict) else {}
                action_details = action_doc.get("actionDetails", {}) if isinstance(action_doc, dict) else {}
                
                # IMPORTANT: jobParams contains application_id
                # Structure: response['data']['jobParams']['application_id']
                job_params = action_doc.get("jobParams", {}) if isinstance(action_doc, dict) else {}
                
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
                
                # Store identifiers
                self._deployment_id = action_details.get("_idDeployment") or action_details.get("deployment_id")
                
                # app_deployment_id: check actionDetails first, then jobParams
                self._app_deployment_id = (
                    action_details.get("app_deployment_id") or
                    action_details.get("appDeploymentId") or
                    action_details.get("app_deploymentId") or
                    job_params.get("app_deployment_id") or
                    job_params.get("appDeploymentId") or
                    job_params.get("app_deploymentId") or
                    ""
                )
                
                # application_id: PRIMARILY from jobParams (this is where it lives!)
                # response['data']['jobParams'].get('application_id', '')
                self._application_id = (
                    job_params.get("application_id") or
                    job_params.get("applicationId") or
                    job_params.get("app_id") or
                    job_params.get("appId") or
                    action_details.get("application_id") or
                    action_details.get("applicationId") or
                    ""
                )
                
                self._instance_id = action_details.get("instanceID") or action_details.get("instanceId")
                self._external_ip = action_details.get("externalIP") or action_details.get("externalIp")
                
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
                self.logger.debug(f"[BUSINESS_METRICS_MANAGER_FACTORY] actionDetails keys: {list(action_details.keys())}")
                self.logger.debug(f"[BUSINESS_METRICS_MANAGER_FACTORY] jobParams keys: {list(job_params.keys()) if job_params else []}")
                
            except Exception as e:
                self.logger.error(
                    f"[BUSINESS_METRICS_MANAGER_FACTORY] ❌ Failed to fetch action details: {e}", 
                    exc_info=True
                )
                print("----- BUSINESS METRICS MANAGER ACTION DETAILS ERROR -----")
                print(f"action_id: {self._action_id}")
                print(f"error: {e}")
                print("---------------------------------------------------------")
                self._initialized = True
                return None
            
            # Determine localhost vs cloud using externalIP from action_details
            is_localhost = False
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
            
            localhost_indicators = ["localhost", "127.0.0.1", "0.0.0.0"]
            if server_host in localhost_indicators:
                is_localhost = True
                self.logger.info(
                    f"[BUSINESS_METRICS_MANAGER_FACTORY] Detected Localhost environment "
                    f"(Public IP={public_ip}, Server IP={server_host})"
                )
            else:
                is_localhost = False
                self.logger.info(
                    f"[BUSINESS_METRICS_MANAGER_FACTORY] Detected Cloud environment "
                    f"(Public IP={public_ip}, Server IP={server_host})"
                )
            
            redis_client = None
            kafka_client = None

            # Force localhost and Redis always
            is_localhost = True

            # STRICT SWITCH: Only Redis if localhost, Only Kafka if cloud
            if is_localhost:
                # Initialize Redis client (ONLY) using instance_id
                if not self._instance_id:
                    self.logger.error(
                        "[BUSINESS_METRICS_MANAGER_FACTORY] ❌ Localhost mode but instance_id missing"
                    )
                else:
                    try:
                        url = f"/v1/actions/get_redis_server_by_instance_id/{self._instance_id}"
                        self.logger.info(
                            f"[BUSINESS_METRICS_MANAGER_FACTORY] Fetching Redis server info "
                            f"for instance: {self._instance_id}"
                        )
                        response = rpc.get(url)
                        
                        if isinstance(response, dict) and response.get("success", False):
                            data = response.get("data", {})
                            host = data.get("host")
                            port = data.get("port")
                            username = data.get("username")
                            password = data.get("password", "")
                            db_index = data.get("db", 0)
                            conn_timeout = data.get("connection_timeout", 120)
                            
                            print("----- BUSINESS METRICS MANAGER REDIS SERVER PARAMS -----")
                            print(f"instance_id: {self._instance_id}")
                            print(f"host: {host}")
                            print(f"port: {port}")
                            print(f"username: {username}")
                            print(f"password: {'*' * len(password) if password else ''}")
                            print(f"db: {db_index}")
                            print(f"connection_timeout: {conn_timeout}")
                            print("--------------------------------------------------------")
                            
                            self.logger.info(
                                f"[BUSINESS_METRICS_MANAGER_FACTORY] Redis params - "
                                f"host={host}, port={port}, user={username}"
                            )
                            
                            redis_client = MatriceStream(
                                StreamType.REDIS,
                                host=host,
                                port=int(port),
                                password=password,
                                username=username,
                                db=db_index,
                                connection_timeout=conn_timeout
                            )
                            # Setup for metrics publishing
                            redis_client.setup("business_metrics")
                            self.logger.info("[BUSINESS_METRICS_MANAGER_FACTORY] ✓ Redis client initialized")
                        else:
                            self.logger.warning(
                                f"[BUSINESS_METRICS_MANAGER_FACTORY] Failed to fetch Redis server info: "
                                f"{response.get('message', 'Unknown error') if isinstance(response, dict) else 'Unknown error'}"
                            )
                    except Exception as e:
                        self.logger.warning(
                            f"[BUSINESS_METRICS_MANAGER_FACTORY] Redis initialization failed: {e}"
                        )
            
            else:
                # Initialize Kafka client (ONLY) using global info endpoint
                try:
                    url = f"/v1/actions/get_kafka_info"
                    self.logger.info(
                        "[BUSINESS_METRICS_MANAGER_FACTORY] Fetching Kafka server info for Cloud mode"
                    )
                    response = rpc.get(url)
                    
                    if isinstance(response, dict) and response.get("success", False):
                        data = response.get("data", {})
                        enc_ip = data.get("ip")
                        enc_port = data.get("port")
                        
                        # Decode base64 encoded values
                        ip_addr = None
                        port = None
                        try:
                            ip_addr = base64.b64decode(str(enc_ip)).decode("utf-8")
                        except Exception:
                            ip_addr = enc_ip
                        try:
                            port = base64.b64decode(str(enc_port)).decode("utf-8")
                        except Exception:
                            port = enc_port
                        
                        print("----- BUSINESS METRICS MANAGER KAFKA SERVER PARAMS -----")
                        print(f"ipAddress: {ip_addr}")
                        print(f"port: {port}")
                        print("--------------------------------------------------------")
                        
                        self.logger.info(
                            f"[BUSINESS_METRICS_MANAGER_FACTORY] Kafka params - ip={ip_addr}, port={port}"
                        )
                        
                        bootstrap_servers = f"{ip_addr}:{port}"
                        kafka_client = MatriceStream(
                            StreamType.KAFKA,
                            bootstrap_servers=bootstrap_servers,
                            sasl_mechanism="SCRAM-SHA-256",
                            sasl_username=os.environ.get("KAFKA_SASL_USERNAME"),
                            sasl_password=os.environ.get("KAFKA_SASL_PASSWORD"),
                            security_protocol="SASL_PLAINTEXT"
                        )
                        # Setup for metrics publishing (producer-only; no consumer group needed)
                        kafka_client.setup("business_metrics")
                        self.logger.info(
                            f"[BUSINESS_METRICS_MANAGER_FACTORY] ✓ Kafka client initialized "
                            f"(servers={bootstrap_servers})"
                        )
                    else:
                        self.logger.warning(
                            f"[BUSINESS_METRICS_MANAGER_FACTORY] Failed to fetch Kafka server info: "
                            f"{response.get('message', 'Unknown error') if isinstance(response, dict) else 'Unknown error'}"
                        )
                except Exception as e:
                    self.logger.warning(
                        f"[BUSINESS_METRICS_MANAGER_FACTORY] Kafka initialization failed: {e}"
                    )
            
            # Create business metrics manager if we have at least one transport
            if redis_client or kafka_client:
                self._business_metrics_manager = BUSINESS_METRICS_MANAGER(
                    redis_client=redis_client,
                    kafka_client=kafka_client,
                    output_topic="business_metrics",
                    aggregation_interval=aggregation_interval,
                    metrics_config=metrics_config or DEFAULT_METRICS_CONFIG.copy(),
                    logger=self.logger
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
            else:
                self.logger.warning(
                    f"[BUSINESS_METRICS_MANAGER_FACTORY] No {'Redis' if is_localhost else 'Kafka'} client available, "
                    f"business metrics manager not created"
                )
            
            self._initialized = True
            self.logger.info("[BUSINESS_METRICS_MANAGER_FACTORY] ===== INITIALIZATION COMPLETE =====")
            return self._business_metrics_manager
            
        except ImportError as e:
            self.logger.error(f"[BUSINESS_METRICS_MANAGER_FACTORY] Import error: {e}")
            self._initialized = True
            return None
        except Exception as e:
            self.logger.error(
                f"[BUSINESS_METRICS_MANAGER_FACTORY] Initialization failed: {e}", 
                exc_info=True
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
            except Exception:
                pass
            
            try:
                usr_src = Path("/usr/src")
                if usr_src.exists():
                    for child in usr_src.iterdir():
                        if child.is_dir():
                            candidates.append(child.name)
            except Exception:
                pass
            
            for candidate in candidates:
                if candidate and len(candidate) >= 8 and self.ACTION_ID_PATTERN.match(candidate):
                    return candidate
        except Exception:
            pass
        return None
    
    def _get_public_ip(self) -> str:
        """Get the public IP address of this machine."""
        self.logger.info("[BUSINESS_METRICS_MANAGER_FACTORY] Fetching public IP address...")
        try:
            public_ip = urllib.request.urlopen(
                "https://v4.ident.me", timeout=120
            ).read().decode("utf8").strip()
            self.logger.debug(f"[BUSINESS_METRICS_MANAGER_FACTORY] Public IP: {public_ip}")
            return public_ip
        except Exception as e:
            self.logger.warning(f"[BUSINESS_METRICS_MANAGER_FACTORY] Error fetching public IP: {e}")
            return "localhost"
    
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
    def business_metrics_manager(self) -> Optional[BUSINESS_METRICS_MANAGER]:
        return self._business_metrics_manager


# Module-level factory instance for convenience
_default_factory: Optional[BusinessMetricsManagerFactory] = None


def get_business_metrics_manager(
    config: Any, 
    logger: Optional[logging.Logger] = None,
    aggregation_interval: int = DEFAULT_AGGREGATION_INTERVAL,
    metrics_config: Optional[Dict[str, str]] = None
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
        config, 
        aggregation_interval=aggregation_interval,
        metrics_config=metrics_config
    )

