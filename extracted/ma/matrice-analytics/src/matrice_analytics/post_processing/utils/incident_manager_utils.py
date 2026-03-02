"""
incident_manager_utils.py

Manages incident publishing to Redis/Kafka when severity levels change.
Implements consecutive-frame validation before publishing:
- 5 consecutive frames for medium/significant/critical
- 10 consecutive frames for low (stricter)
- 101 consecutive empty frames to send 'info' (incident ended)

Polls 'incident_modification_config' topic for dynamic threshold settings.
Publishes to 'incident_res' topic.

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
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timezone
from dataclasses import dataclass, field
from pathlib import Path


# Severity level ordering for comparison (none = no incident)
SEVERITY_LEVELS = ["none", "info", "low", "medium", "significant", "critical"]

# Default thresholds if none provided (same as fire_detection.py defaults)
DEFAULT_THRESHOLDS = [
    {"level": "low", "percentage": 0.0001},
    {"level": "medium", "percentage": 3},
    {"level": "significant", "percentage": 13},
    {"level": "critical", "percentage": 30}
]

# Cache for location names to avoid repeated API calls
_location_name_cache: Dict[str, str] = {}


@dataclass
class IncidentState:
    """Tracks the current incident state for a camera/usecase."""
    current_level: str = "none"        # Current confirmed severity level
    pending_level: str = "none"        # Level being validated (needs consecutive frames)
    consecutive_count: int = 0         # Consecutive frames with pending_level
    last_published_level: str = "none" # Last level that was published (for spam prevention)
    incident_cycle_id: int = 1         # Starts at 1, incremented when cycle resets (after info sent)
    empty_frames_count: int = 0        # Consecutive empty incident frames (for "info" detection)
    current_incident_id: str = ""      # Current incident_id for this cycle (managed per camera)
    incident_active: bool = False      # Whether an incident is currently active in this cycle


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
      - 101 empty frames to send "info" (incident ended)
    - Supports both Redis and Kafka transports
    - Thread-safe operations
    
    Usage:
        manager = INCIDENT_MANAGER(redis_client=..., kafka_client=...)
        manager.start()  # Start config polling
        manager.process_incident(camera_id, incident_data, stream_info)
        manager.stop()   # Stop polling on shutdown
    """
    
    # Frame thresholds for different severity levels
    CONSECUTIVE_FRAMES_DEFAULT = 5       # For medium, significant, critical
    CONSECUTIVE_FRAMES_LOW = 10          # For low level (stricter)
    CONSECUTIVE_FRAMES_EMPTY = 101       # For sending "info" after no detections
    
    CONFIG_POLLING_INTERVAL = 10  # Poll every 10 seconds
    CONFIG_TOPIC = "incident_modification_config"
    INCIDENT_TOPIC = "incident_res"
    
    def __init__(
        self,
        redis_client: Optional[Any] = None,
        kafka_client: Optional[Any] = None,
        incident_topic: str = "incident_res",
        config_topic: str = "incident_modification_config",
        logger: Optional[logging.Logger] = None
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
        self._factory_ref: Optional['IncidentManagerFactory'] = None
        
        self.logger.info(
            f"[INCIDENT_MANAGER] Initialized with incident_topic={incident_topic}, "
            f"config_topic={config_topic}, "
            f"low_frames={self.CONSECUTIVE_FRAMES_LOW}, "
            f"default_frames={self.CONSECUTIVE_FRAMES_DEFAULT}, "
            f"empty_frames_for_info={self.CONSECUTIVE_FRAMES_EMPTY}, "
            f"polling_interval={self.CONFIG_POLLING_INTERVAL}s"
        )
    
    def set_factory_ref(self, factory: 'IncidentManagerFactory'):
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
            target=self._config_polling_loop,
            daemon=True,
            name="IncidentConfigPoller"
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
        self.logger.info(f"[INCIDENT_MANAGER] Config polling loop started (interval: {self.CONFIG_POLLING_INTERVAL}s)")
        
        while not self._stop_event.is_set():
            try:
                self._fetch_and_update_configs()
            except Exception as e:
                self.logger.error(f"[INCIDENT_MANAGER] Error in config polling loop: {e}", exc_info=True)
            
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
                self.logger.debug(f"[INCIDENT_MANAGER] Fetching configs from Redis: {self.config_topic}")
                configs = self._read_configs_from_redis(max_messages=100)
                if configs:
                    self.logger.info(f"[INCIDENT_MANAGER] Fetched {len(configs)} config(s) from Redis")
            except Exception as e:
                self.logger.debug(f"[INCIDENT_MANAGER] Redis config fetch: {e}")
        
        # Fallback to Kafka if Redis failed or no messages
        if not configs and self.kafka_client:
            try:
                self.logger.debug(f"[INCIDENT_MANAGER] Fetching configs from Kafka: {self.config_topic}")
                configs = self._read_configs_from_kafka(max_messages=100)
                if configs:
                    self.logger.info(f"[INCIDENT_MANAGER] Fetched {len(configs)} config(s) from Kafka")
            except Exception as e:
                self.logger.debug(f"[INCIDENT_MANAGER] Kafka config fetch: {e}")
        
        # Update in-memory threshold configs
        for config_data in configs:
            try:
                self._handle_config_message(config_data)
            except Exception as e:
                self.logger.error(f"[INCIDENT_MANAGER] Error handling config message: {e}", exc_info=True)
    
    def _read_configs_from_redis(self, max_messages: int = 100) -> List[Dict[str, Any]]:
        """Read config messages from Redis stream."""
        messages = []
        try:
            for msg_count in range(max_messages):
                msg = self.redis_client.get_message(timeout=0.1)
                if not msg:
                    break
                
                value = msg.get('value') or msg.get('data') or msg.get('message')
                if value:
                    parsed = self._parse_message_value(value)
                    if parsed:
                        messages.append(parsed)
        except Exception as e:
            self.logger.debug(f"[INCIDENT_MANAGER] Error reading from Redis: {e}")
        
        return messages
    
    def _read_configs_from_kafka(self, max_messages: int = 100) -> List[Dict[str, Any]]:
        """Read config messages from Kafka topic."""
        messages = []
        try:
            for msg_count in range(max_messages):
                msg = self.kafka_client.get_message(timeout=0.1)
                if not msg:
                    break
                
                value = msg.get('value') or msg.get('data') or msg.get('message')
                if value:
                    parsed = self._parse_message_value(value)
                    if parsed:
                        messages.append(parsed)
        except Exception as e:
            self.logger.debug(f"[INCIDENT_MANAGER] Error reading from Kafka: {e}")
        
        return messages
    
    def _parse_message_value(self, value: Any) -> Optional[Dict[str, Any]]:
        """Parse message value into a dictionary."""
        try:
            # Already a dict
            if isinstance(value, dict):
                if 'data' in value and isinstance(value['data'], dict):
                    return value['data']
                return value
            
            # Bytes to string
            if isinstance(value, bytes):
                value = value.decode('utf-8')
            
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
        except Exception as e:
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
                {"level": "low", "percentage": 0.0001},
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
                self.logger.debug(f"[INCIDENT_MANAGER] Using default thresholds for camera: {camera_id}")
            else:
                # Validate each threshold has required fields
                # Also map "high" -> "significant" (backend uses "high", we use "significant")
                valid_thresholds = []
                for t in thresholds:
                    if isinstance(t, dict) and "level" in t and "percentage" in t:
                        level = t.get("level", "").lower().strip()
                        # Map "high" to "significant" when receiving from backend
                        if level == "high":
                            self.logger.debug(f"[INCIDENT_MANAGER] Mapping level 'high' -> 'significant' for camera {camera_id}")
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
                    camera_name=camera_name
                )
            
            self.logger.info(
                f"[INCIDENT_MANAGER] ✓ Updated thresholds for camera: {camera_id}, "
                f"thresholds: {thresholds}"
            )
            
        except Exception as e:
            self.logger.error(f"[INCIDENT_MANAGER] Error handling config message: {e}", exc_info=True)
    
    def _get_thresholds_for_camera(self, camera_id: str) -> Tuple[List[Dict[str, Any]], Optional[ThresholdConfig]]:
        """
        Get thresholds for a specific camera, or defaults if not configured.
        
        Returns:
            Tuple of (thresholds list, ThresholdConfig or None)
        """
        with self._config_lock:
            config = self._threshold_configs.get(camera_id)
            if config:
                return config.thresholds, config
            return DEFAULT_THRESHOLDS, None
    
    def _calculate_severity_from_quant(
        self, 
        incident_quant: float, 
        thresholds: List[Dict[str, Any]]
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
        self, 
        stream_info: Optional[Dict[str, Any]]
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
                'location': '6908756db129880c34f2e09a'
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
            "location_id": ""
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
                camera_info.get("camera_name", "") or
                camera_info.get("cameraName", "") or
                input_camera_info.get("camera_name", "") or
                input_camera_info.get("cameraName", "") or
                stream_info.get("camera_name", "") or
                stream_info.get("cameraName", "") or
                input_settings.get("camera_name", "") or
                input_settings.get("cameraName", "") or
                ""
            )
            
            # camera_id - check direct fields first
            result["camera_id"] = (
                camera_info.get("camera_id", "") or
                camera_info.get("cameraId", "") or
                input_camera_info.get("camera_id", "") or
                input_camera_info.get("cameraId", "") or
                stream_info.get("camera_id", "") or
                stream_info.get("cameraId", "") or
                input_settings.get("camera_id", "") or
                input_settings.get("cameraId", "") or
                ""
            )
            
            # If camera_id still not found, extract from topic
            # Topic format: {camera_id}_input_topic (e.g., "692d7bde42582ffde3611908_input_topic")
            if not result["camera_id"]:
                topic = stream_info.get("topic", "")
                if topic:
                    extracted_camera_id = ""
                    if topic.endswith("_input_topic"):
                        extracted_camera_id = topic[: -len("_input_topic")]
                        self.logger.debug(f"[INCIDENT_MANAGER] Extracted camera_id from topic (underscore): {extracted_camera_id}")
                    elif topic.endswith("_input-topic"):
                        extracted_camera_id = topic[: -len("_input-topic")]
                        self.logger.debug(f"[INCIDENT_MANAGER] Extracted camera_id from topic (hyphen): {extracted_camera_id}")
                    else:
                        if "_input_topic" in topic:
                            extracted_camera_id = topic.split("_input_topic")[0]
                            self.logger.debug(f"[INCIDENT_MANAGER] Extracted camera_id from topic split (underscore): {extracted_camera_id}")
                        elif "_input-topic" in topic:
                            extracted_camera_id = topic.split("_input-topic")[0]
                            self.logger.debug(f"[INCIDENT_MANAGER] Extracted camera_id from topic split (hyphen): {extracted_camera_id}")
                    if extracted_camera_id:
                        result["camera_id"] = extracted_camera_id
            
            # app_deployment_id
            result["app_deployment_id"] = (
                stream_info.get("app_deployment_id", "") or
                stream_info.get("appDeploymentId", "") or
                stream_info.get("app_deploymentId", "") or
                input_settings.get("app_deployment_id", "") or
                input_settings.get("appDeploymentId", "") or
                camera_info.get("app_deployment_id", "") or
                camera_info.get("appDeploymentId", "") or
                ""
            )
            
            # application_id
            result["application_id"] = (
                stream_info.get("application_id", "") or
                stream_info.get("applicationId", "") or
                stream_info.get("app_id", "") or
                stream_info.get("appId", "") or
                input_settings.get("application_id", "") or
                input_settings.get("applicationId", "") or
                camera_info.get("application_id", "") or
                camera_info.get("applicationId", "") or
                ""
            )
            
            # frame_id - at top level of stream_info
            result["frame_id"] = (
                stream_info.get("frame_id", "") or
                stream_info.get("frameId", "") or
                input_settings.get("frame_id", "") or
                input_settings.get("frameId", "") or
                ""
            )

            # rtp_number - for media server frame retrieval (replaces frame_id for new flow)
            result["rtp_number"] = (
                stream_info.get("rtp_number", "") or
                stream_info.get("rtpNumber", "") or
                input_settings.get("rtp_number", "") or
                input_settings.get("rtpNumber", "") or
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
            
            self.logger.debug(
                f"[INCIDENT_MANAGER] Extracted from stream_info - "
                f"camera_id={result['camera_id']}, camera_name={result['camera_name']}, "
                f"app_deployment_id={result['app_deployment_id']}, application_id={result['application_id']}, "
                f"frame_id={result['frame_id']}, rtp_number={result['rtp_number']}, location_id={result['location_id']}"
            )
            
        except Exception as e:
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
            self.logger.debug(f"[INCIDENT_MANAGER] No location_id provided, using default: '{default_location}'")
            return default_location
        
        # Check cache first
        if location_id in _location_name_cache:
            cached_name = _location_name_cache[location_id]
            self.logger.debug(f"[INCIDENT_MANAGER] Using cached location name for '{location_id}': '{cached_name}'")
            return cached_name
        
        # Need factory reference with session to make API call
        if not self._factory_ref or not self._factory_ref._session:
            self.logger.warning(f"[INCIDENT_MANAGER] No session available for location API, using default: '{default_location}'")
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
                    self.logger.info(f"[INCIDENT_MANAGER] ✓ Fetched location name: '{location_name}' for location_id: '{location_id}'")
                    
                    # Cache the result
                    _location_name_cache[location_id] = location_name
                    return location_name
                else:
                    self.logger.warning(
                        f"[INCIDENT_MANAGER] API returned success=false for location_id '{location_id}': "
                        f"{response.get('message', 'Unknown error')}"
                    )
            else:
                self.logger.warning(f"[INCIDENT_MANAGER] Invalid response format from API: {response}")
                
        except Exception as e:
            self.logger.error(f"[INCIDENT_MANAGER] Error fetching location name for '{location_id}': {e}", exc_info=True)
        
        # Use default on any failure
        self.logger.info(f"[INCIDENT_MANAGER] Using default location name: '{default_location}'")
        _location_name_cache[location_id] = default_location
        return default_location
    
    def _generate_incident_id(self, camera_id: str, cycle_id: int) -> str:
        """Generate a unique incident_id for a camera's cycle."""
        return f"incident_{camera_id}_{cycle_id}"
    
    def process_incident(
        self,
        camera_id: str,
        incident_data: Dict[str, Any],
        stream_info: Optional[Dict[str, Any]] = None
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
        5. Tracks empty incidents and publishes "info" after 101 consecutive empty frames
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
                    new_state.current_incident_id = self._generate_incident_id(camera_id, new_state.incident_cycle_id)
                    self._incident_states[camera_id] = new_state
                    self.logger.info(
                        f"[INCIDENT_MANAGER] Created new state for camera: {camera_id}, "
                        f"initial incident_id: {new_state.current_incident_id}"
                    )
                
                state = self._incident_states[camera_id]
                
                # Ensure incident_id is set (for existing states that may not have it)
                if not state.current_incident_id:
                    state.current_incident_id = self._generate_incident_id(camera_id, state.incident_cycle_id)
                    self.logger.info(f"[INCIDENT_MANAGER] Generated incident_id for existing state: {state.current_incident_id}")
            
            # Handle empty incident data - track for "info" level
            is_empty_incident = (not incident_data or incident_data == {})
            
            if is_empty_incident:
                self.logger.debug("[INCIDENT_MANAGER] Empty incident data, tracking for info level")
                return self._handle_empty_incident(camera_id, state, stream_info)
            
            # Step 1: Get thresholds for this camera
            thresholds, threshold_config = self._get_thresholds_for_camera(camera_id)
            
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
            
            # We have a real detection (severity != none), reset empty frame counter
            with self._states_lock:
                state.empty_frames_count = 0
            
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
                        f"[INCIDENT_MANAGER] Same pending level, "
                        f"consecutive_count now: {state.consecutive_count}"
                    )
                else:
                    # Different level, reset counter
                    state.pending_level = severity_level
                    state.consecutive_count = 1
                    self.logger.debug(
                        f"[INCIDENT_MANAGER] New pending level: {severity_level}, "
                        f"reset consecutive_count to 1"
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
                            new_level != "none" and
                            new_level != state.last_published_level
                        )
                        
                        self.logger.info(
                            f"[INCIDENT_MANAGER] Level changed: {old_level} -> {new_level}, "
                            f"should_publish={should_publish} "
                            f"(last_published={state.last_published_level})"
                        )
                        
                        if should_publish:
                            # Mark incident as active for this cycle
                            state.incident_active = True
                            
                            # Use the managed incident_id for this cycle
                            incident_data["incident_id"] = state.current_incident_id
                            
                            # Publish the incident
                            success = self._publish_incident(
                                camera_id, incident_data, stream_info
                            )
                            if success:
                                state.last_published_level = new_level
                                self.logger.info(
                                    f"[INCIDENT_MANAGER] ✓ Published incident for level: {new_level}, "
                                    f"incident_id: {state.current_incident_id}"
                                )
                            return success
                        else:
                            self.logger.debug(
                                f"[INCIDENT_MANAGER] Skipping publish - "
                                f"level={new_level}, already published"
                            )
                    else:
                        self.logger.debug(
                            f"[INCIDENT_MANAGER] No level change, staying at: {state.current_level}"
                        )
                
                return False
            
        except Exception as e:
            self.logger.error(
                f"[INCIDENT_MANAGER] Error processing incident: {e}", 
                exc_info=True
            )
            return False
    
    def _handle_empty_incident(
        self, 
        camera_id: str, 
        state: IncidentState,
        stream_info: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Handle empty incident (no detection).
        
        After 101 consecutive empty frames, send "info" level if an incident was active.
        Info uses the SAME incident_id as the current cycle, then starts a new cycle.
        
        Args:
            camera_id: Camera identifier
            state: Current incident state
            stream_info: Stream metadata
            
        Returns:
            True if "info" incident was published, False otherwise
        """
        with self._states_lock:
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
                should_send_info = (
                    state.incident_active and 
                    state.last_published_level not in ("info", "none")
                )
                
                if should_send_info:
                    self.logger.info(
                        f"[INCIDENT_MANAGER] {self.CONSECUTIVE_FRAMES_EMPTY} consecutive empty frames for camera {camera_id}, "
                        f"sending 'info' level to close incident cycle "
                        f"(last_published={state.last_published_level}, incident_id={state.current_incident_id})"
                    )
                    
                    # Get incident_type from threshold config if available
                    incident_type = "fire_smoke_detection"  # Default
                    with self._config_lock:
                        config = self._threshold_configs.get(camera_id)
                        if config and config.incident_type:
                            incident_type = config.incident_type
                    
                    # Create info incident data - USE THE SAME incident_id from this cycle!
                    info_incident = {
                        "incident_id": state.current_incident_id,  # Same incident_id for this cycle
                        "incident_type": incident_type,
                        "severity_level": "info",
                        "human_text": "Incident ended"
                    }
                    
                    # Update state BEFORE publishing
                    state.current_level = "info"
                    state.empty_frames_count = 0  # Reset counter
                    
                    # Publish info incident
                    success = self._publish_incident(camera_id, info_incident, stream_info)
                    if success:
                        state.last_published_level = "info"
                        
                        # END THIS CYCLE - Start a new cycle for future incidents
                        old_cycle_id = state.incident_cycle_id
                        old_incident_id = state.current_incident_id
                        
                        state.incident_cycle_id += 1  # Increment cycle
                        state.current_incident_id = self._generate_incident_id(camera_id, state.incident_cycle_id)
                        state.incident_active = False  # No active incident in new cycle yet
                        state.current_level = "none"  # Reset level for new cycle
                        state.pending_level = "none"
                        state.consecutive_count = 0
                        # Note: We keep last_published_level as "info" to prevent duplicate info sends
                        
                        self.logger.info(
                            f"[INCIDENT_MANAGER] ✓ Published 'info' for camera {camera_id}, "
                            f"closed incident_id={old_incident_id} (cycle {old_cycle_id}), "
                            f"started new cycle {state.incident_cycle_id} with incident_id={state.current_incident_id}"
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
        stream_info: Optional[Dict[str, Any]] = None
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
        self.logger.info(f"[INCIDENT_MANAGER] ========== PUBLISHING INCIDENT ==========")
        
        try:
            # Build the incident message
            message = self._build_incident_message(camera_id, incident_data, stream_info)
            
            self.logger.info(f"[INCIDENT_MANAGER] Built incident message: {json.dumps(message, default=str)[:500]}...")
            
            success = False
            
            # Try Redis first (primary)
            if self.redis_client:
                try:
                    self.logger.debug(
                        f"[INCIDENT_MANAGER] Publishing to Redis stream: {self.incident_topic}"
                    )
                    self._publish_to_redis(self.incident_topic, message)
                    self.logger.info(
                        f"[INCIDENT_MANAGER] ✓ Incident published to Redis"
                    )
                    success = True
                except Exception as e:
                    self.logger.error(
                        f"[INCIDENT_MANAGER] ❌ Redis publish failed: {e}", 
                        exc_info=True
                    )
            
            # Fallback to Kafka if Redis failed or no Redis client
            if not success and self.kafka_client:
                try:
                    self.logger.debug(
                        f"[INCIDENT_MANAGER] Publishing to Kafka topic: {self.incident_topic}"
                    )
                    self._publish_to_kafka(self.incident_topic, message)
                    self.logger.info(
                        f"[INCIDENT_MANAGER] ✓ Incident published to Kafka"
                    )
                    success = True
                except Exception as e:
                    self.logger.error(
                        f"[INCIDENT_MANAGER] ❌ Kafka publish failed: {e}", 
                        exc_info=True
                    )
            
            if success:
                self.logger.info(f"[INCIDENT_MANAGER] ========== INCIDENT PUBLISHED ==========")
            else:
                self.logger.error(
                    f"[INCIDENT_MANAGER] ❌ INCIDENT NOT PUBLISHED (both transports failed)"
                )
            
            return success
            
        except Exception as e:
            self.logger.error(
                f"[INCIDENT_MANAGER] Error publishing incident: {e}", 
                exc_info=True
            )
            return False
    
    def _build_incident_message(
        self,
        camera_id: str,
        incident_data: Dict[str, Any],
        stream_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Build the incident message in the required format.
        
        Output format (STRICT):
        {
            "camera_id": "...",
            "app_deployment_id": "...",
            "application_id": "...",
            "camera_name": "...",
            "frame_id": "...",
            "location_name": "...",
            "incidents": [{
                "incident_id": "...",
                "incident_type": "...",
                "severity_level": "...",
                "human_text": "..."
            }]
        }
        
        Keys to REMOVE: "alerts", "alert_settings", "duration", "incident_quant", 
                        "start_time", "end_time", "camera_info", "level_settings"
        """
        
        # Extract camera info from multiple sources
        stream_camera_info = self._extract_camera_info_from_stream(stream_info)
        
        # Get IDs from threshold config (if available - set by config polling)
        config_camera_id = incident_data.get("_config_camera_id", "")
        config_application_id = incident_data.get("_config_application_id", "")
        config_app_deployment_id = incident_data.get("_config_app_deployment_id", "")
        config_camera_name = incident_data.get("_config_camera_name", "")
        
        # Get IDs from factory (from action_details)
        factory_app_deployment_id = ""
        factory_application_id = ""
        if self._factory_ref:
            factory_app_deployment_id = self._factory_ref._app_deployment_id or ""
            factory_application_id = self._factory_ref._application_id or ""
        
        # Priority: stream_info > threshold_config > factory > camera_id param
        final_camera_id = (
            stream_camera_info.get("camera_id") or 
            config_camera_id or 
            camera_id or 
            ""
        )
        
        final_camera_name = (
            stream_camera_info.get("camera_name") or 
            config_camera_name or 
            ""
        )
        
        final_app_deployment_id = (
            stream_camera_info.get("app_deployment_id") or 
            config_app_deployment_id or 
            factory_app_deployment_id or 
            ""
        )
        
        final_application_id = (
            stream_camera_info.get("application_id") or 
            config_application_id or 
            factory_application_id or 
            ""
        )
        
        # Extract frame_id and rtp_number from stream_info
        final_frame_id = stream_camera_info.get("frame_id", "")
        final_rtp_number = stream_camera_info.get("rtp_number", "")

        # Extract stream_time from stream_info
        stream_time = ""
        if stream_info:
            stream_time = stream_info.get("stream_time", "")
            if not stream_time:
                # Try alternative paths
                input_settings = stream_info.get("input_settings", {})
                if isinstance(input_settings, dict):
                    stream_time = input_settings.get("stream_time", "")

        # Guard against pre-Y2K timestamps from relative RTP values
        if stream_time:
            try:
                ts_clean = stream_time.replace(" UTC", "").strip()
                if ts_clean[:4].isdigit() and int(ts_clean[:4]) < 2000:
                    stream_time = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            except (ValueError, IndexError):
                pass
        
        # Fetch location_name from API using location_id
        location_id = stream_camera_info.get("location_id", "")
        final_location_name = self._fetch_location_name(location_id)
        
        self.logger.info(
            f"[INCIDENT_MANAGER] Building message with - "
            f"camera_id={final_camera_id}, camera_name={final_camera_name}, "
            f"app_deployment_id={final_app_deployment_id}, application_id={final_application_id}, "
            f"frame_id={final_frame_id}, rtp_number={final_rtp_number}, location_name={final_location_name}"
        )
        
        # Build incident - ONLY include required fields
        # Map "significant" -> "high" for backend (we use "significant" internally, backend expects "high")
        severity_level = incident_data.get("severity_level", "")
        if severity_level.lower().strip() == "significant":
            severity_level = "high"
            self.logger.debug(f"[INCIDENT_MANAGER] Mapped severity_level 'significant' -> 'high' for publishing")
        
        incident = {
            "incident_id": incident_data.get("incident_id", ""),
            "incident_type": incident_data.get("incident_type", "fire_smoke_detection"),
            "severity_level": severity_level,
            "human_text": incident_data.get("human_text", "")
        }
        
        # Build final message with all required fields
        message = {
            "camera_id": final_camera_id,
            "app_deployment_id": final_app_deployment_id,
            "application_id": final_application_id,
            "camera_name": final_camera_name,
            "frame_id": final_frame_id,
            "rtp_number": final_rtp_number,
            "location_name": final_location_name,
            "stream_time": stream_time,
            "incidents": [incident]
        }
        
        return message
    
    def _publish_to_redis(self, topic: str, message: Dict[str, Any]):
        """Publish message to Redis stream."""
        try:
            self.redis_client.add_message(
                topic_or_channel=topic,
                message=json.dumps(message),
                key=message.get("camera_id", "")
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
                key=message.get("camera_id", "")
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
                    "incident_active": state.incident_active
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
                    "incident_active": state.incident_active
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
                    "camera_name": config.camera_name
                }
            return None
    
    def set_thresholds_for_camera(
        self, 
        camera_id: str, 
        thresholds: List[Dict[str, Any]],
        application_id: str = "",
        app_deployment_id: str = "",
        incident_type: str = "",
        camera_name: str = ""
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
                        self.logger.debug(f"[INCIDENT_MANAGER] Mapped threshold level 'high' -> 'significant'")
                    mapped_thresholds.append(t)
        
        with self._config_lock:
            self._threshold_configs[camera_id] = ThresholdConfig(
                camera_id=camera_id,
                application_id=application_id,
                app_deployment_id=app_deployment_id,
                incident_type=incident_type,
                thresholds=mapped_thresholds if mapped_thresholds else DEFAULT_THRESHOLDS.copy(),
                last_updated=time.time(),
                camera_name=camera_name
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
    
    def initialize(self, config: Any) -> Optional[INCIDENT_MANAGER]:
        """
        Initialize and return INCIDENT_MANAGER with Redis/Kafka clients.
        
        This follows the same pattern as license_plate_monitoring.py for
        session initialization and Redis/Kafka client creation.
        
        Args:
            config: Configuration object with session, server_id, etc.
            
        Returns:
            INCIDENT_MANAGER instance or None if initialization failed
        """
        if self._initialized and self._incident_manager is not None:
            self.logger.debug("[INCIDENT_MANAGER_FACTORY] Already initialized, returning existing instance")
            return self._incident_manager
        
        try:
            # Import required modules
            from matrice_common.stream.matrice_stream import MatriceStream, StreamType
            from matrice_common.session import Session
            
            self.logger.info("[INCIDENT_MANAGER_FACTORY] ===== STARTING INITIALIZATION =====")
            
            # Get or create session
            self._session = getattr(config, 'session', None)
            if not self._session:
                self.logger.info("[INCIDENT_MANAGER_FACTORY] No session in config, creating from environment...")
                account_number = os.getenv("MATRICE_ACCOUNT_NUMBER", "")
                access_key_id = os.getenv("MATRICE_ACCESS_KEY_ID", "")
                secret_key = os.getenv("MATRICE_SECRET_ACCESS_KEY", "")
                project_id = os.getenv("MATRICE_PROJECT_ID", "")
                
                self.logger.debug(f"[INCIDENT_MANAGER_FACTORY] Env vars - account: {'SET' if account_number else 'NOT SET'}, "
                                  f"access_key: {'SET' if access_key_id else 'NOT SET'}, "
                                  f"secret: {'SET' if secret_key else 'NOT SET'}")
                
                
                self._session = Session(
                    account_number=account_number,
                    access_key=access_key_id,
                    secret_key=secret_key,
                    project_id=project_id,
                )
                self.logger.info("[INCIDENT_MANAGER_FACTORY] ✓ Created session from environment")
            else:
                self.logger.info("[INCIDENT_MANAGER_FACTORY] ✓ Using session from config")
            
            rpc = self._session.rpc
            
            # Discover action_id
            self._action_id = self._discover_action_id()
            if not self._action_id:
                self.logger.error("[INCIDENT_MANAGER_FACTORY] ❌ Could not discover action_id")
                print("----- INCIDENT MANAGER ACTION DISCOVERY -----")
                print("action_id: NOT FOUND")
                print("---------------------------------------------")
                self._initialized = True
                return None
            
            self.logger.info(f"[INCIDENT_MANAGER_FACTORY] ✓ Discovered action_id: {self._action_id}")
            
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
                
                print("----- INCIDENT MANAGER ACTION DETAILS -----")
                print(f"action_id: {self._action_id}")
                print(f"server_type: {server_type}")
                print(f"server_id: {server_id}")
                print(f"deployment_id: {self._deployment_id}")
                print(f"app_deployment_id: {self._app_deployment_id}")
                print(f"application_id: {self._application_id}")
                print(f"instance_id: {self._instance_id}")
                print(f"external_ip: {self._external_ip}")
                print(f"jobParams keys: {list(job_params.keys()) if job_params else []}")
                print("--------------------------------------------")
                
                self.logger.info(
                    f"[INCIDENT_MANAGER_FACTORY] Action details - server_type={server_type}, "
                    f"instance_id={self._instance_id}, "
                    f"app_deployment_id={self._app_deployment_id}, application_id={self._application_id}"
                )
                
                # Log all available keys for debugging
                self.logger.debug(f"[INCIDENT_MANAGER_FACTORY] actionDetails keys: {list(action_details.keys())}")
                self.logger.debug(f"[INCIDENT_MANAGER_FACTORY] jobParams keys: {list(job_params.keys()) if job_params else []}")
                
            except Exception as e:
                self.logger.error(f"[INCIDENT_MANAGER_FACTORY] ❌ Failed to fetch action details: {e}", exc_info=True)
                print("----- INCIDENT MANAGER ACTION DETAILS ERROR -----")
                print(f"action_id: {self._action_id}")
                print(f"error: {e}")
                print("-------------------------------------------------")
                self._initialized = True
                return None
            
            # Determine localhost vs cloud using externalIP from action_details
            is_localhost = False
            public_ip = self._get_public_ip()
            
            # Get server host from action_details (user's method - no dependency on server_id)
            server_host = (
                action_details.get("externalIP")
                or action_details.get("external_IP")
                or action_details.get("externalip")
                or action_details.get("external_ip")
                or action_details.get("externalIp")
                or action_details.get("external_Ip")
            )
            print(f"server_host: {server_host}")
            self.logger.info(f"[INCIDENT_MANAGER_FACTORY] DEBUG - server_host: {server_host}")
            
            localhost_indicators = ["localhost", "127.0.0.1", "0.0.0.0"]
            if server_host in localhost_indicators:
                is_localhost = True
                self.logger.info(
                    f"[INCIDENT_MANAGER_FACTORY] Detected Localhost environment "
                    f"(Public IP={public_ip}, Server IP={server_host})"
                )
            else:
                is_localhost = False
                self.logger.info(
                    f"[INCIDENT_MANAGER_FACTORY] Detected Cloud environment "
                    f"(Public IP={public_ip}, Server IP={server_host})"
                )
            # Force localhost and Redis always
            is_localhost = True
            redis_client = None
            kafka_client = None
            
            # STRICT SWITCH: Only Redis if localhost, Only Kafka if cloud
            if is_localhost:
                # Initialize Redis client (ONLY) using instance_id
                if not self._instance_id:
                    self.logger.error("[INCIDENT_MANAGER_FACTORY] ❌ Localhost mode but instance_id missing")
                else:
                    try:
                        url = f"/v1/actions/get_redis_server_by_instance_id/{self._instance_id}"
                        self.logger.info(f"[INCIDENT_MANAGER_FACTORY] Fetching Redis server info for instance: {self._instance_id}")
                        response = rpc.get(url)
                        
                        if isinstance(response, dict) and response.get("success", False):
                            data = response.get("data", {})
                            host = data.get("host")
                            port = data.get("port")
                            username = data.get("username")
                            password = data.get("password", "")
                            db_index = data.get("db", 0)
                            conn_timeout = data.get("connection_timeout", 120)
                            
                            print("----- INCIDENT MANAGER REDIS SERVER PARAMS -----")
                            print(f"instance_id: {self._instance_id}")
                            print(f"host: {host}")
                            print(f"port: {port}")
                            print(f"username: {username}")
                            print(f"password: {'*' * len(password) if password else ''}")
                            print(f"db: {db_index}")
                            print(f"connection_timeout: {conn_timeout}")
                            print("------------------------------------------------")
                            
                            self.logger.info(
                                f"[INCIDENT_MANAGER_FACTORY] Redis params - host={host}, port={port}, user={username}"
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
                            # Setup for both config polling and incident publishing
                            redis_client.setup("incident_modification_config")
                            self.logger.info("[INCIDENT_MANAGER_FACTORY] ✓ Redis client initialized")
                        else:
                            self.logger.warning(
                                f"[INCIDENT_MANAGER_FACTORY] Failed to fetch Redis server info: "
                                f"{response.get('message', 'Unknown error') if isinstance(response, dict) else 'Unknown error'}"
                            )
                    except Exception as e:
                        self.logger.warning(f"[INCIDENT_MANAGER_FACTORY] Redis initialization failed: {e}")
            
            else:
                # Initialize Kafka client (ONLY) using global info endpoint
                try:
                    url = f"/v1/actions/get_kafka_info"
                    self.logger.info("[INCIDENT_MANAGER_FACTORY] Fetching Kafka server info for Cloud mode")
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
                        
                        print("----- INCIDENT MANAGER KAFKA SERVER PARAMS -----")
                        print(f"ipAddress: {ip_addr}")
                        print(f"port: {port}")
                        print("------------------------------------------------")
                        
                        self.logger.info(f"[INCIDENT_MANAGER_FACTORY] Kafka params - ip={ip_addr}, port={port}")
                        
                        bootstrap_servers = f"{ip_addr}:{port}"
                        kafka_client = MatriceStream(
                            StreamType.KAFKA,
                            bootstrap_servers=bootstrap_servers,
                            sasl_mechanism="SCRAM-SHA-256",
                            sasl_username=os.environ.get("KAFKA_SASL_USERNAME"),
                            sasl_password=os.environ.get("KAFKA_SASL_PASSWORD"),
                            security_protocol="SASL_PLAINTEXT"
                        )
                        # Setup for both config polling and incident publishing
                        kafka_client.setup("incident_modification_config", consumer_group_id="py_analytics_incidents")
                        self.logger.info(f"[INCIDENT_MANAGER_FACTORY] ✓ Kafka client initialized (servers={bootstrap_servers})")
                    else:
                        self.logger.warning(
                            f"[INCIDENT_MANAGER_FACTORY] Failed to fetch Kafka server info: "
                            f"{response.get('message', 'Unknown error') if isinstance(response, dict) else 'Unknown error'}"
                        )
                except Exception as e:
                    self.logger.warning(f"[INCIDENT_MANAGER_FACTORY] Kafka initialization failed: {e}")
            
            # Create incident manager if we have at least one transport
            if redis_client or kafka_client:
                self._incident_manager = INCIDENT_MANAGER(
                    redis_client=redis_client,
                    kafka_client=kafka_client,
                    incident_topic="incident_res",
                    config_topic="incident_modification_config",
                    logger=self.logger
                )
                # Set factory reference for accessing deployment info
                self._incident_manager.set_factory_ref(self)
                # Start the config polling thread
                self._incident_manager.start()
                
                transport = "Redis" if redis_client else "Kafka"
                self.logger.info(f"[INCIDENT_MANAGER_FACTORY] ✓ Incident manager created with {transport}")
                print(f"----- INCIDENT MANAGER INITIALIZED ({transport}) -----")
            else:
                self.logger.warning(
                    f"[INCIDENT_MANAGER_FACTORY] No {'Redis' if is_localhost else 'Kafka'} client available, "
                    f"incident manager not created"
                )
            
            self._initialized = True
            self.logger.info("[INCIDENT_MANAGER_FACTORY] ===== INITIALIZATION COMPLETE =====")
            return self._incident_manager
            
        except ImportError as e:
            self.logger.error(f"[INCIDENT_MANAGER_FACTORY] Import error: {e}")
            self._initialized = True
            return None
        except Exception as e:
            self.logger.error(f"[INCIDENT_MANAGER_FACTORY] Initialization failed: {e}", exc_info=True)
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
        self.logger.info("[INCIDENT_MANAGER_FACTORY] Fetching public IP address...")
        try:
            public_ip = urllib.request.urlopen(
                "https://v4.ident.me", timeout=120
            ).read().decode("utf8").strip()
            self.logger.debug(f"[INCIDENT_MANAGER_FACTORY] Public IP: {public_ip}")
            return public_ip
        except Exception as e:
            self.logger.warning(f"[INCIDENT_MANAGER_FACTORY] Error fetching public IP: {e}")
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
    def incident_manager(self) -> Optional[INCIDENT_MANAGER]:
        return self._incident_manager


# Module-level factory instance for convenience
_default_factory: Optional[IncidentManagerFactory] = None


def get_incident_manager(config: Any, logger: Optional[logging.Logger] = None) -> Optional[INCIDENT_MANAGER]:
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
