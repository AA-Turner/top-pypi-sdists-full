"""
alert_instance_utils.py

PRODUCTION-READY VERSION
Robust JSON parsing with fallback handling.
"""

from __future__ import annotations

import json
import logging
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class AlertConfig:
    """Represents an instant alert configuration."""

    instant_alert_id: str
    camera_id: str
    app_deployment_id: str
    application_id: str
    alert_name: str
    detection_config: Dict[str, Any]
    severity_level: str
    is_active: bool
    action: str
    timestamp: str
    last_updated: float = field(default_factory=time.time)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AlertConfig":
        """Create AlertConfig from dictionary."""
        # Handle is_active as string (e.g., "True" or "true" -> True)
        is_active_raw = data.get("is_active", True)
        if isinstance(is_active_raw, str):
            is_active = is_active_raw.lower() in ("true", "1", "yes")
        else:
            is_active = bool(is_active_raw)

        return cls(
            instant_alert_id=data.get("instant_alert_id", ""),
            camera_id=data.get("camera_id", ""),
            app_deployment_id=data.get("app_deployment_id", ""),
            application_id=data.get("application_id", ""),
            alert_name=data.get("alert_name", ""),
            detection_config=data.get("detection_config", {}),
            severity_level=data.get("severity_level", "medium"),
            is_active=is_active,
            action=data.get("action", "create"),
            timestamp=data.get("timestamp", datetime.now(timezone.utc).isoformat()),
            last_updated=time.time(),
        )


class ALERT_INSTANCE:
    """
    Manages instant alert configurations and evaluates detection events.

    This class handles:
    - Polling alert configs from Redis/Kafka every polling_interval seconds
    - Maintaining in-memory alert state
    - Evaluating detection events against alert criteria
    - Publishing trigger messages when matches occur

    Transport Priority:
    - Redis is primary for both config reading and trigger publishing
    - Kafka is fallback when Redis operations fail
    """

    def __init__(
        self,
        redis_client: Optional[Any] = None,
        kafka_client: Optional[Any] = None,
        config_topic: str = "alert_instant_config_request",
        trigger_topic: str = "alert_instant_triggered",
        polling_interval: int = 10,
        logger: Optional[logging.Logger] = None,
        app_deployment_id: Optional[str] = None,
    ):
        """
        Initialize ALERT_INSTANCE.

        Args:
            redis_client: MatriceStream instance configured for Redis (primary transport)
            kafka_client: MatriceStream instance configured for Kafka (fallback transport)
            config_topic: Topic/stream name for receiving alert configs
            trigger_topic: Topic/stream name for publishing triggers
            polling_interval: Seconds between config polling
            logger: Python logger instance
            app_deployment_id: App deployment ID to filter incoming alerts (only process alerts matching this ID)
        """
        self.redis_client = redis_client
        self.kafka_client = kafka_client
        self.config_topic = config_topic
        self.trigger_topic = trigger_topic
        self.polling_interval = polling_interval
        self.logger = logger or logging.getLogger(__name__)
        self.app_deployment_id = app_deployment_id

        # In-memory alert storage: {instant_alert_id: AlertConfig}
        self._alerts: Dict[str, AlertConfig] = {}
        self._alerts_lock = threading.Lock()

        # Cooldown tracking: {(instant_alert_id, detection_key): last_trigger_timestamp}
        # detection_key = plateNumber for LPR, objectClass for count/intrusion, "fire_smoke" for fire/smoke
        self._cooldown_cache: Dict[tuple, float] = {}
        self._cooldown_lock = threading.Lock()
        self._cooldown_seconds = 5  # 5 second cooldown per alert+detection combination

        # Polling thread control
        self._polling_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._running = False

        self.logger.info(
            f"Initialized ALERT_INSTANCE with config_topic={config_topic}, "
            f"trigger_topic={trigger_topic}, polling_interval={polling_interval}s, "
            f"cooldown={self._cooldown_seconds}s, app_deployment_id={app_deployment_id}"
        )

    def start(self):
        """Start the background polling thread for config updates."""
        if self._running:
            self.logger.warning("ALERT_INSTANCE already running")
            return

        self._running = True
        self._stop_event.clear()
        self._polling_thread = threading.Thread(target=self._polling_loop, daemon=True, name="AlertConfigPoller")
        self._polling_thread.start()
        self.logger.info("Started alert config polling thread")

    def stop(self):
        """Stop the background polling thread gracefully."""
        if not self._running:
            return

        self.logger.info("Stopping ALERT_INSTANCE...")
        self._running = False
        self._stop_event.set()

        if self._polling_thread and self._polling_thread.is_alive():
            self._polling_thread.join(timeout=5)

        self.logger.info("ALERT_INSTANCE stopped")

    def _polling_loop(self):
        """Background thread that polls for config updates every polling_interval seconds."""
        self.logger.info(f"Alert config polling loop started (interval: {self.polling_interval}s)")

        while not self._stop_event.is_set():
            try:
                self._fetch_and_update_configs()
            except Exception as e:
                self.logger.error(f"Error in polling loop: {e}", exc_info=True)

            # Sleep in small increments to allow quick shutdown
            for _ in range(self.polling_interval):
                if self._stop_event.is_set():
                    break
                time.sleep(1)

        self.logger.info("Alert config polling loop exited")

    def _fetch_and_update_configs(self):
        """Fetch config messages from Redis (primary) or Kafka (fallback)."""
        configs = []

        # Try Redis first (primary)
        if self.redis_client:
            try:
                self.logger.debug(f"Fetching configs from Redis stream: {self.config_topic}")
                configs = self._read_from_redis(self.config_topic)
                if configs:
                    self.logger.info(f"Fetched {len(configs)} config(s) from Redis")
            except Exception as e:
                self.logger.error(f"Redis config fetch failed: {e}", exc_info=True)

        # Fallback to Kafka if Redis failed or no client
        if not configs and self.kafka_client:
            try:
                self.logger.debug(f"Falling back to Kafka topic: {self.config_topic}")
                configs = self._read_from_kafka(self.config_topic)
                if configs:
                    self.logger.info(f"Fetched {len(configs)} config(s) from Kafka")
            except Exception as e:
                self.logger.error(f"Kafka config fetch failed: {e}", exc_info=True)

        # Update in-memory alert configs
        for config_data in configs:
            try:
                self._handle_config_message(config_data)
            except Exception as e:
                self.logger.error(f"Error handling config message: {e}", exc_info=True)

    def _read_from_redis(self, topic: str, max_messages: int = 100) -> List[Dict[str, Any]]:
        """
        Read messages from Redis stream.

        Args:
            topic: Redis stream name
            max_messages: Maximum messages to fetch

        Returns:
            List of parsed message dictionaries
        """
        messages = []
        try:
            self.logger.debug(f"[ALERT_DEBUG] Reading from Redis topic: {topic}, max_messages: {max_messages}")
            for msg_count in range(max_messages):
                msg = self.redis_client.get_message(timeout=0.1)
                if not msg:
                    self.logger.debug(f"[ALERT_DEBUG] No more messages from Redis after {msg_count} messages")
                    break

                self.logger.debug(f"[ALERT_DEBUG] Raw message #{msg_count + 1} received: {msg}")
                value = msg.get("value") or msg.get("data") or msg.get("message")
                if value:
                    self.logger.debug(
                        f"[ALERT_DEBUG] Extracted value type: {type(value)}, length: {len(value) if hasattr(value, '__len__') else 'N/A'}"
                    )

                    # Handle case where value is already a dict (Redis stream format)
                    if isinstance(value, dict):
                        self.logger.debug(f"[ALERT_DEBUG] Value is already a dict, keys: {list(value.keys())}")
                        # Check if there's a nested 'data' key (common Redis stream pattern)
                        if "data" in value and isinstance(value["data"], dict):
                            parsed = value["data"]
                            self.logger.info(f"[ALERT_DEBUG] Extracted nested 'data' dict: {parsed}")
                            messages.append(parsed)
                        else:
                            # Use the dict directly
                            self.logger.info(f"[ALERT_DEBUG] Using dict directly: {value}")
                            messages.append(value)
                        continue

                    if isinstance(value, bytes):
                        value = value.decode("utf-8")
                        self.logger.debug(f"[ALERT_DEBUG] Decoded bytes to string: {value[:200]}...")
                    if isinstance(value, str):
                        self.logger.debug(f"[ALERT_DEBUG] Raw JSON string: {value}")
                        # Robust JSON parsing with error handling
                        try:
                            parsed = json.loads(value)
                            self.logger.info(f"[ALERT_DEBUG] Successfully parsed JSON: {parsed}")
                            messages.append(parsed)
                        except json.JSONDecodeError as e:
                            self.logger.error(f"[ALERT_DEBUG] JSON parse error: {e}")
                            self.logger.error(f"[ALERT_DEBUG] Invalid JSON (first 500 chars): {value[:500]}")
                            # Try to fix common issues
                            try:
                                # Replace Python booleans with JSON booleans
                                self.logger.debug("[ALERT_DEBUG] Attempting to fix Python-style formatting...")
                                fixed = value

                                # Fix Python booleans (True/False -> true/false)
                                fixed = fixed.replace(": True", ": true").replace(": False", ": false")
                                fixed = fixed.replace(":True", ":true").replace(":False", ":false")
                                fixed = fixed.replace(" True,", " true,").replace(" False,", " false,")
                                fixed = fixed.replace(" True}", " true}").replace(" False}", " false}")
                                fixed = fixed.replace("{True", "{true").replace("{False", "{false")

                                # Fix Python None (None -> null)
                                fixed = fixed.replace(": None", ": null").replace(":None", ":null")
                                fixed = fixed.replace(" None,", " null,").replace(" None}", " null}")

                                # Fix single quotes (Python dict style) -> double quotes (JSON style)
                                # This is a simple replacement that works for most cases
                                if "'" in fixed and '"' not in fixed:
                                    self.logger.debug(
                                        "[ALERT_DEBUG] Detected single quotes, replacing with double quotes"
                                    )
                                    fixed = fixed.replace("'", '"')

                                self.logger.debug(f"[ALERT_DEBUG] Fixed JSON string: {fixed[:500]}...")
                                parsed = json.loads(fixed)
                                self.logger.info(f"[ALERT_DEBUG] Successfully fixed and parsed JSON: {parsed}")
                                messages.append(parsed)
                            except Exception as fix_error:
                                self.logger.error(f"[ALERT_DEBUG] Could not fix JSON: {fix_error}, skipping message")
                                continue
                else:
                    self.logger.warning(f"[ALERT_DEBUG] Message has no value/data/message field: {msg}")
        except Exception as e:
            self.logger.error(f"[ALERT_DEBUG] Error reading from Redis: {e}", exc_info=True)
            raise

        self.logger.info(f"[ALERT_DEBUG] Total messages parsed from Redis: {len(messages)}")
        return messages

    def _read_from_kafka(self, topic: str, max_messages: int = 100) -> List[Dict[str, Any]]:
        """
        Read messages from Kafka topic.

        Args:
            topic: Kafka topic name
            max_messages: Maximum messages to fetch

        Returns:
            List of parsed message dictionaries
        """
        messages = []
        try:
            self.logger.debug(f"[ALERT_DEBUG] Reading from Kafka topic: {topic}, max_messages: {max_messages}")
            for msg_count in range(max_messages):
                msg = self.kafka_client.get_message(timeout=0.1)
                if not msg:
                    self.logger.debug(f"[ALERT_DEBUG] No more messages from Kafka after {msg_count} messages")
                    break

                self.logger.debug(f"[ALERT_DEBUG] Raw Kafka message #{msg_count + 1} received: {msg}")
                value = msg.get("value") or msg.get("data") or msg.get("message")
                if value:
                    self.logger.debug(
                        f"[ALERT_DEBUG] Extracted value type: {type(value)}, length: {len(value) if hasattr(value, '__len__') else 'N/A'}"
                    )

                    # Handle case where value is already a dict (Kafka message format)
                    if isinstance(value, dict):
                        self.logger.debug(f"[ALERT_DEBUG] Value is already a dict, keys: {list(value.keys())}")
                        # Check if there's a nested 'data' key (common Kafka message pattern)
                        if "data" in value and isinstance(value["data"], dict):
                            parsed = value["data"]
                            self.logger.info(f"[ALERT_DEBUG] Extracted nested 'data' dict: {parsed}")
                            messages.append(parsed)
                        else:
                            # Use the dict directly
                            self.logger.info(f"[ALERT_DEBUG] Using dict directly: {value}")
                            messages.append(value)
                        continue

                    if isinstance(value, bytes):
                        value = value.decode("utf-8")
                        self.logger.debug(f"[ALERT_DEBUG] Decoded bytes to string: {value[:200]}...")
                    if isinstance(value, str):
                        self.logger.debug(f"[ALERT_DEBUG] Raw JSON string: {value}")
                        try:
                            parsed = json.loads(value)
                            self.logger.info(f"[ALERT_DEBUG] Successfully parsed Kafka JSON: {parsed}")
                            messages.append(parsed)
                        except json.JSONDecodeError as e:
                            self.logger.error(f"[ALERT_DEBUG] Kafka JSON parse error: {e}")
                            self.logger.error(f"[ALERT_DEBUG] Invalid JSON (first 500 chars): {value[:500]}")
                            # Try to fix common issues
                            try:
                                self.logger.debug("[ALERT_DEBUG] Attempting to fix Python-style formatting...")
                                fixed = value

                                # Fix Python booleans (True/False -> true/false)
                                fixed = fixed.replace(": True", ": true").replace(": False", ": false")
                                fixed = fixed.replace(":True", ":true").replace(":False", ":false")
                                fixed = fixed.replace(" True,", " true,").replace(" False,", " false,")
                                fixed = fixed.replace(" True}", " true}").replace(" False}", " false}")
                                fixed = fixed.replace("{True", "{true").replace("{False", "{false")

                                # Fix Python None (None -> null)
                                fixed = fixed.replace(": None", ": null").replace(":None", ":null")
                                fixed = fixed.replace(" None,", " null,").replace(" None}", " null}")

                                # Fix single quotes (Python dict style) -> double quotes (JSON style)
                                # This is a simple replacement that works for most cases
                                if "'" in fixed and '"' not in fixed:
                                    self.logger.debug(
                                        "[ALERT_DEBUG] Detected single quotes, replacing with double quotes"
                                    )
                                    fixed = fixed.replace("'", '"')

                                self.logger.debug(f"[ALERT_DEBUG] Fixed JSON string: {fixed[:500]}...")
                                parsed = json.loads(fixed)
                                self.logger.info(f"[ALERT_DEBUG] Successfully fixed and parsed Kafka JSON: {parsed}")
                                messages.append(parsed)
                            except Exception as fix_error:
                                self.logger.error(
                                    f"[ALERT_DEBUG] Could not fix Kafka JSON: {fix_error}, skipping message"
                                )
                                continue
                else:
                    self.logger.warning(f"[ALERT_DEBUG] Kafka message has no value/data/message field: {msg}")
        except Exception as e:
            self.logger.error(f"[ALERT_DEBUG] Error reading from Kafka: {e}", exc_info=True)
            raise

        self.logger.info(f"[ALERT_DEBUG] Total messages parsed from Kafka: {len(messages)}")
        return messages

    def _handle_config_message(self, config_data: Dict[str, Any]):
        """
        Handle a single config message (create/update/delete).

        Args:
            config_data: Alert configuration dictionary
        """
        try:
            self.logger.info("[ALERT_DEBUG] ========== HANDLING CONFIG MESSAGE ==========")
            self.logger.info(f"[ALERT_DEBUG] Raw config_data type: {type(config_data)}")
            self.logger.info(
                f"[ALERT_DEBUG] Raw config_data keys: {list(config_data.keys()) if isinstance(config_data, dict) else 'N/A'}"
            )
            self.logger.info(f"[ALERT_DEBUG] Raw config_data: {config_data}")

            # Skip if this is a wrapper with 'raw' key (from failed JSON parse)
            if "raw" in config_data and len(config_data) == 1:
                self.logger.warning("[ALERT_DEBUG] Skipping malformed config with 'raw' key only")
                return

            # Log detection_service field (informational only, no filtering)
            detection_service = config_data.get("detection_service", "")
            self.logger.info(f"[ALERT_DEBUG] detection_service: '{detection_service}'")

            # Filter by app_deployment_id - only process alerts that match our app_deployment_id
            incoming_app_deployment_id = config_data.get("app_deployment_id", "")
            if self.app_deployment_id:
                if incoming_app_deployment_id != self.app_deployment_id:
                    self.logger.info(
                        f"[ALERT_DEBUG] Skipping alert - app_deployment_id mismatch: "
                        f"incoming='{incoming_app_deployment_id}', ours='{self.app_deployment_id}'"
                    )
                    return
                else:
                    self.logger.info(f"[ALERT_DEBUG] ✓ app_deployment_id match: '{incoming_app_deployment_id}'")
            else:
                self.logger.warning(
                    f"[ALERT_DEBUG] No app_deployment_id filter set, processing all alerts. "
                    f"Incoming app_deployment_id: '{incoming_app_deployment_id}'"
                )

            # Log individual fields before creating AlertConfig
            self.logger.debug("[ALERT_DEBUG] Extracted fields from config_data:")
            self.logger.debug(f"[ALERT_DEBUG]   - instant_alert_id: '{config_data.get('instant_alert_id', 'MISSING')}'")
            self.logger.debug(f"[ALERT_DEBUG]   - camera_id: '{config_data.get('camera_id', 'MISSING')}'")
            self.logger.debug(
                f"[ALERT_DEBUG]   - app_deployment_id: '{config_data.get('app_deployment_id', 'MISSING')}'"
            )
            self.logger.debug(f"[ALERT_DEBUG]   - application_id: '{config_data.get('application_id', 'MISSING')}'")
            self.logger.debug(f"[ALERT_DEBUG]   - alert_name: '{config_data.get('alert_name', 'MISSING')}'")
            self.logger.debug(f"[ALERT_DEBUG]   - detection_config: {config_data.get('detection_config', 'MISSING')}")
            self.logger.debug(f"[ALERT_DEBUG]   - severity_level: '{config_data.get('severity_level', 'MISSING')}'")
            self.logger.debug(f"[ALERT_DEBUG]   - is_active: {config_data.get('is_active', 'MISSING')}")
            self.logger.debug(f"[ALERT_DEBUG]   - action: '{config_data.get('action', 'MISSING')}'")
            self.logger.debug(f"[ALERT_DEBUG]   - timestamp: '{config_data.get('timestamp', 'MISSING')}'")

            alert_config = AlertConfig.from_dict(config_data)

            self.logger.info("[ALERT_DEBUG] AlertConfig created successfully")
            self.logger.info("[ALERT_DEBUG] AlertConfig fields:")
            self.logger.info(f"[ALERT_DEBUG]   - instant_alert_id: '{alert_config.instant_alert_id}'")
            self.logger.info(f"[ALERT_DEBUG]   - camera_id: '{alert_config.camera_id}'")
            self.logger.info(f"[ALERT_DEBUG]   - app_deployment_id: '{alert_config.app_deployment_id}'")
            self.logger.info(f"[ALERT_DEBUG]   - application_id: '{alert_config.application_id}'")
            self.logger.info(f"[ALERT_DEBUG]   - alert_name: '{alert_config.alert_name}'")
            self.logger.info(f"[ALERT_DEBUG]   - detection_config: {alert_config.detection_config}")
            self.logger.info(f"[ALERT_DEBUG]   - severity_level: '{alert_config.severity_level}'")
            self.logger.info(f"[ALERT_DEBUG]   - is_active: {alert_config.is_active}")
            self.logger.info(f"[ALERT_DEBUG]   - action: '{alert_config.action}'")
            self.logger.info(f"[ALERT_DEBUG]   - timestamp: '{alert_config.timestamp}'")

            action = alert_config.action.lower()
            alert_id = alert_config.instant_alert_id

            self.logger.info(f"[ALERT_DEBUG] Action (lowercase): '{action}'")
            self.logger.info(f"[ALERT_DEBUG] Alert ID: '{alert_id}'")

            # Validate required fields
            if not alert_id:
                self.logger.error("[ALERT_DEBUG] ❌ VALIDATION FAILED: Missing 'instant_alert_id'")
                self.logger.error(f"[ALERT_DEBUG] Full config data: {config_data}")
                return
            if not alert_config.camera_id:
                self.logger.warning(
                    f"[ALERT_DEBUG] camera_id missing for alert '{alert_id}', defaulting to empty and proceeding"
                )

            self.logger.info("[ALERT_DEBUG] ✓ Validation passed")

            with self._alerts_lock:
                if action == "create":
                    if alert_id in self._alerts:
                        self.logger.info(f"[ALERT_DEBUG] Alert {alert_id} already exists, treating as update")
                    self._alerts[alert_id] = alert_config
                    self.logger.info(f"[ALERT_DEBUG] ✓ Created/Updated alert: {alert_id} ({alert_config.alert_name})")
                    self.logger.info(f"[ALERT_DEBUG] Total active alerts now: {len(self._alerts)}")

                elif action == "update":
                    self._alerts[alert_id] = alert_config
                    self.logger.info(f"[ALERT_DEBUG] ✓ Updated alert: {alert_id} ({alert_config.alert_name})")
                    self.logger.info(f"[ALERT_DEBUG] Total active alerts now: {len(self._alerts)}")

                elif action == "delete":
                    if alert_id in self._alerts:
                        del self._alerts[alert_id]
                        self.logger.info(f"[ALERT_DEBUG] ✓ Deleted alert: {alert_id}")
                        self.logger.info(f"[ALERT_DEBUG] Total active alerts now: {len(self._alerts)}")
                    else:
                        self.logger.warning(f"[ALERT_DEBUG] Delete requested for non-existent alert: {alert_id}")

                # Also deactivate if is_active is False
                if not alert_config.is_active and alert_id in self._alerts:
                    del self._alerts[alert_id]
                    self.logger.info(f"[ALERT_DEBUG] ✓ Deactivated alert: {alert_id}")
                    self.logger.info(f"[ALERT_DEBUG] Total active alerts now: {len(self._alerts)}")

            self.logger.info("[ALERT_DEBUG] ========== CONFIG MESSAGE HANDLED ==========")

        except Exception as e:
            self.logger.error(
                f"[ALERT_DEBUG] ❌ EXCEPTION in _handle_config_message: {e}",
                exc_info=True,
            )
            self.logger.error(f"[ALERT_DEBUG] Failed config_data: {config_data}")

    def process_detection_event(
        self,
        detection_payload: Dict[str, Any],
        stream_info: Optional[Dict[str, Any]] = None,
    ):
        """
        Process a detection event and evaluate against active alerts.

        Args:
            detection_payload: Detection event data
            stream_info: Stream metadata containing stream_time and other info
        """
        try:
            self.logger.info("[ALERT_DEBUG] ========== PROCESSING DETECTION EVENT ==========")
            self.logger.info(f"[ALERT_DEBUG] Detection payload: {detection_payload}")

            camera_id = detection_payload.get("camera_id")
            self.logger.debug(f"[ALERT_DEBUG] Camera ID: '{camera_id}'")

            if not camera_id:
                self.logger.warning(
                    "[ALERT_DEBUG] Detection event missing camera_id; defaulting to empty and evaluating against all active alerts"
                )
                camera_id = ""

            # Get all active alerts for this camera
            matching_alerts = self._get_alerts_for_camera(camera_id)

            # Fallback: if no alerts found for this camera (or camera_id missing), evaluate against all active alerts
            if not matching_alerts:
                self.logger.info(
                    f"[ALERT_DEBUG] No camera-specific alerts for '{camera_id}'. Evaluating against all active alerts."
                )
                with self._alerts_lock:
                    matching_alerts = [a for a in self._alerts.values() if a.is_active]

            self.logger.info(f"[ALERT_DEBUG] Found {len(matching_alerts)} active alert(s) for camera '{camera_id}'")
            for i, alert in enumerate(matching_alerts):
                self.logger.debug(f"[ALERT_DEBUG] Alert #{i + 1}: ID={alert.instant_alert_id}, Name={alert.alert_name}")

            if not matching_alerts:
                self.logger.debug(f"[ALERT_DEBUG] No active alerts for camera: {camera_id}")
                self.logger.debug(f"[ALERT_DEBUG] Total alerts in system: {len(self._alerts)}")
                with self._alerts_lock:
                    all_camera_ids = [a.camera_id for a in self._alerts.values()]
                    self.logger.debug(f"[ALERT_DEBUG] All camera IDs in alert system: {all_camera_ids}")
                # return

            # Evaluate each alert
            for alert in matching_alerts:
                try:
                    self.logger.info(f"[ALERT_DEBUG] Evaluating alert: {alert.instant_alert_id} ({alert.alert_name})")

                    # First check if alert criteria match
                    if self._evaluate_alert(alert, detection_payload):
                        # Extract detection key for cooldown check
                        detection_key = self._get_detection_key(detection_payload)

                        # Atomically acquire cooldown slot (check+set)
                        acquired, prev_time = self._try_acquire_cooldown(alert.instant_alert_id, detection_key)
                        if acquired:
                            self.logger.info(
                                "[ALERT_DEBUG] ✓ Alert matched and cooldown acquired, publishing trigger..."
                            )
                            publish_ok = self._publish_trigger(alert, detection_payload, stream_info)
                            if not publish_ok:
                                # Rollback cooldown if publish failed
                                self._rollback_cooldown(alert.instant_alert_id, detection_key, prev_time)
                                self.logger.warning(
                                    f"[ALERT_DEBUG] Publish failed, cooldown rolled back: "
                                    f"alert={alert.instant_alert_id}, detection_key={detection_key}"
                                )
                        else:
                            # Cooldown active, skip publish
                            self.logger.info(
                                f"[ALERT_DEBUG] ⏱️ Alert matched but in cooldown period, skipping: "
                                f"alert={alert.instant_alert_id}, detection_key={detection_key}"
                            )
                    else:
                        self.logger.debug("[ALERT_DEBUG] ✗ Alert did not match criteria")
                except Exception as e:
                    self.logger.error(
                        f"[ALERT_DEBUG] ❌ Error evaluating alert {alert.instant_alert_id}: {e}",
                        exc_info=True,
                    )

            self.logger.info("[ALERT_DEBUG] ========== DETECTION EVENT PROCESSED ==========")

        except Exception as e:
            self.logger.error(f"[ALERT_DEBUG] ❌ Error processing detection event: {e}", exc_info=True)

    def _get_alerts_for_camera(self, camera_id: str) -> List[AlertConfig]:
        """Get all active alerts for a specific camera."""
        with self._alerts_lock:
            return [alert for alert in self._alerts.values() if alert.camera_id == camera_id and alert.is_active]

    def _get_detection_key(self, detection: Dict[str, Any]) -> str:
        """
        Extract the unique detection key based on detection type.

        Returns:
            - plateNumber for license_plate
            - objectClass for object_count/intrusion
            - "fire_smoke" for fire_smoke detection
        """
        detection_type = detection.get("detectionType", "").lower()

        if detection_type == "license_plate":
            return detection.get("plateNumber", "").upper().strip()
        elif detection_type in ["object_count", "intrusion"]:
            return detection.get("objectClass", "unknown")
        elif detection_type == "fire_smoke":
            return "fire_smoke"
        else:
            return "unknown"

    def _check_cooldown(self, alert_id: str, detection_key: str) -> bool:
        """
        Check if alert+detection is in cooldown period.

        Args:
            alert_id: instant_alert_id
            detection_key: plateNumber, objectClass, or detection type

        Returns:
            True if allowed to trigger (not in cooldown), False if in cooldown
        """
        cooldown_key = (alert_id, detection_key)
        current_time = time.time()

        with self._cooldown_lock:
            last_trigger_time = self._cooldown_cache.get(cooldown_key, 0)
            time_since_last = current_time - last_trigger_time

            if time_since_last < self._cooldown_seconds:
                remaining = self._cooldown_seconds - time_since_last
                self.logger.debug(
                    f"[ALERT_DEBUG] ⏱️ COOLDOWN ACTIVE: alert={alert_id}, key={detection_key}, "
                    f"remaining={remaining:.1f}s"
                )
                return False

            return True

    def _update_cooldown(self, alert_id: str, detection_key: str):
        """
        Update the cooldown timestamp for alert+detection combination.

        Args:
            alert_id: instant_alert_id
            detection_key: plateNumber, objectClass, or detection type
        """
        cooldown_key = (alert_id, detection_key)
        current_time = time.time()

        with self._cooldown_lock:
            self._cooldown_cache[cooldown_key] = current_time
            self.logger.debug(
                f"[ALERT_DEBUG] ⏱️ COOLDOWN SET: alert={alert_id}, key={detection_key}, "
                f"duration={self._cooldown_seconds}s"
            )

            # Clean up old entries (older than 2x cooldown period)
            cleanup_threshold = current_time - (self._cooldown_seconds * 2)
            keys_to_remove = [key for key, timestamp in self._cooldown_cache.items() if timestamp < cleanup_threshold]
            for key in keys_to_remove:
                del self._cooldown_cache[key]

            if keys_to_remove:
                self.logger.debug(f"[ALERT_DEBUG] Cleaned up {len(keys_to_remove)} old cooldown entries")

    def _try_acquire_cooldown(self, alert_id: str, detection_key: str) -> tuple[bool, float]:
        """
        Atomically check and set cooldown.

        Returns:
            (acquired, prev_timestamp)
            - acquired: True if cooldown slot acquired (allowed to publish)
            - prev_timestamp: previous timestamp to support rollback if publish fails
        """
        cooldown_key = (alert_id, detection_key)
        current_time = time.time()

        with self._cooldown_lock:
            prev_timestamp = self._cooldown_cache.get(cooldown_key, 0)
            time_since_last = current_time - prev_timestamp

            if time_since_last < self._cooldown_seconds:
                remaining = self._cooldown_seconds - time_since_last
                self.logger.debug(
                    f"[ALERT_DEBUG] ⏱️ COOLDOWN ACTIVE (acquire failed): alert={alert_id}, key={detection_key}, "
                    f"remaining={remaining:.1f}s"
                )
                return False, prev_timestamp

            # Acquire slot by setting to now
            self._cooldown_cache[cooldown_key] = current_time
            self.logger.debug(
                f"[ALERT_DEBUG] ⏱️ COOLDOWN ACQUIRED: alert={alert_id}, key={detection_key}, "
                f"timestamp={current_time:.3f}"
            )
            return True, prev_timestamp

    def _rollback_cooldown(self, alert_id: str, detection_key: str, prev_timestamp: float):
        """Rollback cooldown to the previous timestamp (used when publish fails)."""
        cooldown_key = (alert_id, detection_key)
        with self._cooldown_lock:
            if prev_timestamp == 0:
                # Remove key entirely if there was no previous value
                self._cooldown_cache.pop(cooldown_key, None)
            else:
                self._cooldown_cache[cooldown_key] = prev_timestamp
            self.logger.debug(
                f"[ALERT_DEBUG] ⏱️ COOLDOWN ROLLBACK: alert={alert_id}, key={detection_key}, "
                f"restored_timestamp={prev_timestamp:.3f}"
            )

    def _evaluate_alert(self, alert: AlertConfig, detection: Dict[str, Any]) -> bool:
        """Evaluate if a detection matches alert criteria."""
        detection_type = detection.get("detectionType", "").lower()
        config = alert.detection_config

        if detection_type == "license_plate":
            return self._evaluate_lpr_alert(alert, detection, config)
        elif detection_type == "object_count":
            return self._evaluate_count_alert(alert, detection, config)
        elif detection_type == "fire_smoke":
            return self._evaluate_fire_smoke_alert(alert, detection, config)
        elif detection_type == "intrusion":
            return self._evaluate_intrusion_alert(alert, detection, config)
        else:
            self.logger.warning(f"Unknown detection type: {detection_type}")
            return False

    def _evaluate_lpr_alert(self, alert: AlertConfig, detection: Dict[str, Any], config: Dict[str, Any]) -> bool:
        """
        Evaluate license plate detection against alert criteria.

        Supports two alert conditions:
        - "in_list" (BLACKLIST): Alert ONLY when detected plate IS in targetPlates list
        - "not_in_list" (WHITELIST): Alert when detected plate is NOT in targetPlates list
        """
        self.logger.debug("[ALERT_DEBUG] ========== EVALUATING LPR ALERT ==========")
        self.logger.debug(f"[ALERT_DEBUG] Alert ID: {alert.instant_alert_id}")
        self.logger.debug(f"[ALERT_DEBUG] Alert Name: {alert.alert_name}")
        self.logger.debug(f"[ALERT_DEBUG] Detection config: {config}")
        self.logger.debug(f"[ALERT_DEBUG] Detection data: {detection}")

        target_plates = config.get("targetPlates", [])
        min_confidence = config.get("minConfidence", 0.0)
        # Get alertCondition: "in_list" (blacklist) or "not_in_list" (whitelist)
        alert_condition = config.get("alertCondition", "in_list")

        self.logger.debug(f"[ALERT_DEBUG] Target plates: {target_plates}")
        self.logger.debug(f"[ALERT_DEBUG] Min confidence: {min_confidence}")
        self.logger.info(
            f"[ALERT_DEBUG] Alert condition: '{alert_condition}' (in_list=blacklist, not_in_list=whitelist)"
        )

        plate_number = detection.get("plateNumber", "").upper().strip()
        confidence = detection.get("confidence", 0.0)

        self.logger.debug(f"[ALERT_DEBUG] Detected plate (normalized): '{plate_number}'")
        self.logger.debug(f"[ALERT_DEBUG] Detection confidence: {confidence}")

        # Skip empty plate numbers
        if not plate_number:
            self.logger.debug("[ALERT_DEBUG] ✗ Empty plate number, skipping")
            return False

        # Check if plate matches target list (case-insensitive)
        normalized_targets = [str(t).upper().strip() for t in target_plates]
        plate_in_list = plate_number in normalized_targets

        self.logger.debug(f"[ALERT_DEBUG] Normalized target plates: {normalized_targets}")
        self.logger.debug(f"[ALERT_DEBUG] Plate '{plate_number}' in list: {plate_in_list}")

        # Check confidence threshold (minimum 0.05)
        min_confidence = max(0.05, min_confidence)
        confidence_match = confidence >= min_confidence

        self.logger.debug(
            f"[ALERT_DEBUG] Confidence match result: {confidence_match} ({confidence} >= {min_confidence})"
        )

        # Determine if alert should trigger based on alertCondition
        should_trigger = False

        if alert_condition == "in_list":
            # BLACKLIST: Alert only when plate IS in the target list
            if plate_in_list and confidence_match:
                should_trigger = True
                self.logger.info(
                    f"[ALERT_DEBUG] ✓ LPR BLACKLIST ALERT TRIGGERED: {alert.alert_name} - "
                    f"Plate: {plate_number} IS in blacklist, Confidence: {confidence:.2f}"
                )
            else:
                self.logger.debug(
                    f"[ALERT_DEBUG] ✗ LPR blacklist alert NOT triggered: {alert.alert_name} - "
                    f"Plate '{plate_number}' in_list={plate_in_list}, confidence_match={confidence_match}"
                )

        elif alert_condition == "not_in_list":
            # WHITELIST: Alert when plate is NOT in the target list
            if not plate_in_list and confidence_match:
                should_trigger = True
                self.logger.info(
                    f"[ALERT_DEBUG] ✓ LPR WHITELIST ALERT TRIGGERED: {alert.alert_name} - "
                    f"Plate: {plate_number} is NOT in whitelist, Confidence: {confidence:.2f}"
                )
            else:
                self.logger.debug(
                    f"[ALERT_DEBUG] ✗ LPR whitelist alert NOT triggered: {alert.alert_name} - "
                    f"Plate '{plate_number}' in_list={plate_in_list} (whitelisted), confidence_match={confidence_match}"
                )

        else:
            # Unknown condition, default to blacklist behavior for backward compatibility
            self.logger.warning(
                f"[ALERT_DEBUG] Unknown alertCondition '{alert_condition}', defaulting to 'in_list' (blacklist) behavior"
            )
            if plate_in_list and confidence_match:
                should_trigger = True
                self.logger.info(
                    f"[ALERT_DEBUG] ✓ LPR ALERT TRIGGERED (default): {alert.alert_name} - "
                    f"Plate: {plate_number}, Confidence: {confidence:.2f}"
                )

        return should_trigger

    def _evaluate_count_alert(self, alert: AlertConfig, detection: Dict[str, Any], config: Dict[str, Any]) -> bool:
        """Evaluate object count against threshold."""
        threshold_count = config.get("thresholdCount", 0)
        current_count = detection.get("currentCount", 0)

        if current_count >= threshold_count:
            self.logger.info(
                f"Count alert triggered: {alert.alert_name} - Count: {current_count}, Threshold: {threshold_count}"
            )
            return True

        return False

    def _evaluate_fire_smoke_alert(
        self, alert: AlertConfig, detection: Dict[str, Any], _config: Dict[str, Any]
    ) -> bool:
        """Evaluate fire/smoke detection."""
        _ = _config
        confidence = detection.get("confidence", 0.0)

        fire_detected = detection.get("fireDetected", False)
        smoke_detected = detection.get("smokeDetected", False)
        min_confidence = 0.05

        if (fire_detected or smoke_detected) and confidence >= min_confidence:
            self.logger.info(
                f"Fire/Smoke alert triggered: {alert.alert_name} - "
                f"Fire: {fire_detected}, Smoke: {smoke_detected}, Confidence: {confidence:.2f}"
            )
            return True

        return False

    def _evaluate_intrusion_alert(self, alert: AlertConfig, detection: Dict[str, Any], _config: Dict[str, Any]) -> bool:
        """Evaluate intrusion detection."""
        _ = _config
        confidence = detection.get("confidence", 0.0)
        min_confidence = 0.05

        if confidence >= min_confidence:
            self.logger.info(f"Intrusion alert triggered: {alert.alert_name} - Confidence: {confidence:.2f}")
            return True

        return False

    def _publish_trigger(
        self,
        alert: AlertConfig,
        detection: Dict[str, Any],
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Publish trigger message to backend. Returns True if published successfully."""
        self.logger.info("[ALERT_DEBUG] ========== PUBLISHING TRIGGER ==========")
        self.logger.info(f"[ALERT_DEBUG] Alert ID: {alert.instant_alert_id}")
        self.logger.info(f"[ALERT_DEBUG] Alert Name: {alert.alert_name}")

        trigger_message = self._build_trigger_message(alert, detection, stream_info)

        self.logger.info(f"[ALERT_DEBUG] Built trigger message: {trigger_message}")

        # Publish via Redis (primary) or Kafka (fallback)
        success = False

        if self.redis_client:
            try:
                self.logger.debug(f"[ALERT_DEBUG] Publishing trigger to Redis stream: {self.trigger_topic}")
                self._publish_to_redis(self.trigger_topic, trigger_message)
                self.logger.info(f"[ALERT_DEBUG] ✓ Trigger published to Redis for alert: {alert.instant_alert_id}")
                success = True
            except Exception as e:
                self.logger.error(f"[ALERT_DEBUG] ❌ Redis publish failed: {e}", exc_info=True)

        if not success and self.kafka_client:
            try:
                self.logger.debug(f"[ALERT_DEBUG] Falling back to Kafka topic: {self.trigger_topic}")
                self._publish_to_kafka(self.trigger_topic, trigger_message)
                self.logger.info(f"[ALERT_DEBUG] ✓ Trigger published to Kafka for alert: {alert.instant_alert_id}")
                success = True
            except Exception as e:
                self.logger.error(f"[ALERT_DEBUG] ❌ Kafka publish failed: {e}", exc_info=True)

        if success:
            self.logger.info("[ALERT_DEBUG] ========== TRIGGER PUBLISHED ==========")
        else:
            self.logger.error("[ALERT_DEBUG] ❌ TRIGGER NOT PUBLISHED (both transports failed) ==========")
        return success

    def _build_trigger_message(
        self,
        alert: AlertConfig,
        detection: Dict[str, Any],
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Build trigger message in exact format specified in documentation."""
        detection_type_raw = detection.get("detectionType", "").lower()
        triggered_at = datetime.now(timezone.utc).isoformat()

        # Extract stream_time from stream_info
        stream_time = ""
        if stream_info:
            stream_time = stream_info.get("stream_time", "")
            if not stream_time:
                # Try alternative paths
                input_settings = stream_info.get("input_settings", {})
                if isinstance(input_settings, dict):
                    stream_time = input_settings.get("stream_time", "")

        context_data = {
            "detectionType": detection_type_raw,
            "confidence": detection.get("confidence", 0.0),
            "coordinates": detection.get("coordinates", {}),
            "cameraName": detection.get("cameraName", ""),
            "locationName": detection.get("locationName", ""),
        }

        # Add type-specific fields
        if detection_type_raw == "license_plate":
            context_data.update(
                {
                    "plateNumber": detection.get("plateNumber", ""),
                    # "vehicleType": detection.get("vehicleType", ""),
                    # "vehicleColor": detection.get("vehicleColor", "")
                }
            )
        elif detection_type_raw == "object_count":
            context_data.update(
                {
                    "objectClass": detection.get("objectClass", "person"),
                    "currentCount": detection.get("currentCount", 0),
                    "thresholdCount": alert.detection_config.get("thresholdCount", 0),
                }
            )
        elif detection_type_raw == "fire_smoke":
            context_data.update(
                {
                    "fireDetected": detection.get("fireDetected", False),
                    "smokeDetected": detection.get("smokeDetected", False),
                    "severity": alert.severity_level,
                }
            )
        elif detection_type_raw == "intrusion":
            context_data.update(
                {
                    "objectClass": detection.get("objectClass", "person"),
                    "zoneName": detection.get("zoneName", ""),
                    "personCount": detection.get("personCount", 1),
                }
            )

        # Build contextData with bbox, conf, timestamp, type for enhanced alert info
        # Extract bbox from coordinates or detection's bounding_box
        bbox = []
        coordinates = detection.get("coordinates", {})
        if isinstance(coordinates, dict) and coordinates:
            # Convert from x,y,width,height format to [x1,y1,x2,y2] format
            x = coordinates.get("x", 0)
            y = coordinates.get("y", 0)
            width = coordinates.get("width", 0)
            height = coordinates.get("height", 0)
            bbox = [x, y, x + width, y + height]
        elif detection.get("bounding_box"):
            bb = detection.get("bounding_box", {})
            if isinstance(bb, dict):
                if "xmin" in bb:
                    bbox = [
                        bb.get("xmin", 0),
                        bb.get("ymin", 0),
                        bb.get("xmax", 0),
                        bb.get("ymax", 0),
                    ]
                elif "x" in bb:
                    x, y = bb.get("x", 0), bb.get("y", 0)
                    w, h = bb.get("width", 0), bb.get("height", 0)
                    bbox = [x, y, x + w, y + h]
            elif isinstance(bb, list) and len(bb) >= 4:
                bbox = list(bb[:4])

        context_data_enhanced = {
            "bbox": bbox,
            "conf": float(detection.get("confidence", 0.0)),
            "timestamp": detection.get("timestamp", triggered_at),
            "type": detection_type_raw,
            "plateNumber": detection.get("plateNumber", "") if detection_type_raw == "license_plate" else "",
            "cameraName": detection.get("cameraName", ""),
            "locationName": detection.get("locationName", ""),
        }

        # Prefer detection-level IDs, then fallback to stream_info IDs when available.
        frame_id = detection.get("frame_id", "")
        rtp_number = detection.get("rtp_number", "")
        if stream_info:
            input_settings = (
                stream_info.get("input_settings", {}) if isinstance(stream_info.get("input_settings", {}), dict) else {}
            )
            if not frame_id:
                frame_id = (
                    stream_info.get("frame_id", "")
                    or stream_info.get("frameId", "")
                    or input_settings.get("frame_id", "")
                    or input_settings.get("frameId", "")
                    or ""
                )
            if not rtp_number:
                rtp_number = (
                    stream_info.get("rtp_number", "")
                    or stream_info.get("rtpNumber", "")
                    or input_settings.get("rtp_number", "")
                    or input_settings.get("rtpNumber", "")
                    or ""
                )

        trigger_message = {
            "instant_alert_id": alert.instant_alert_id,
            "camera_id": alert.camera_id,
            "application_id": alert.application_id,
            "frame_id": frame_id,
            "rtp_number": rtp_number,
            "triggered_at": triggered_at,
            "stream_time": stream_time,  # Add stream_time from stream_info
            "context_data": context_data,
            "contextData": context_data_enhanced,  # Enhanced contextData with bbox, conf, timestamp, type
        }

        return trigger_message

    def _publish_to_redis(self, topic: str, message: Dict[str, Any]):
        """Publish message to Redis stream."""
        try:
            self.redis_client.add_message(
                topic_or_channel=topic,
                message=json.dumps(message),
                key=message.get("instant_alert_id", ""),
            )
        except Exception as e:
            self.logger.error(f"Redis publish error: {e}")
            raise

    def _publish_to_kafka(self, topic: str, message: Dict[str, Any]):
        """Publish message to Kafka topic."""
        try:
            self.kafka_client.add_message(
                topic_or_channel=topic,
                message=json.dumps(message),
                key=message.get("instant_alert_id", ""),
            )
        except Exception as e:
            self.logger.error(f"Kafka publish error: {e}")
            raise

    def get_active_alerts_count(self) -> int:
        """Get count of active alerts."""
        with self._alerts_lock:
            return len(self._alerts)

    def get_alerts_for_camera(self, camera_id: str) -> List[Dict[str, Any]]:
        """Get all active alerts for a camera (for debugging/monitoring)."""
        with self._alerts_lock:
            return [
                {
                    "instant_alert_id": alert.instant_alert_id,
                    "alert_name": alert.alert_name,
                    "severity_level": alert.severity_level,
                    "detection_config": alert.detection_config,
                }
                for alert in self._alerts.values()
                if alert.camera_id == camera_id and alert.is_active
            ]
