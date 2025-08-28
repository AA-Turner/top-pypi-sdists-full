import logging
import threading
import time
import base64
import json
from typing import Dict, Any, Optional, List, Tuple

from matrice.session import Session
from confluent_kafka import Producer

class AnalyticsSummarizer:
    """
    Buffers aggregated camera_results and emits 5-minute rollups per camera
    focusing on tracking_stats per application.

    Output structure example per camera:
        {
          "camera_name": "camera_1",
          "inferencePipelineId": "pipeline-xyz",
          "camera_group": "group_a",
          "location": "Lobby",
          "agg_apps": [
            {
              "application_name": "People Counting",
              "application_key_name": "People_Counting",
              "application_version": "1.3",
              "tracking_stats": {
                "input_timestamp": "00:00:09.9",          # last seen
                "reset_timestamp": "00:00:00",             # earliest seen in window
                "current_counts": [{"category": "person", "count": 4}],  # last seen
                "total_counts": [{"category": "person", "count": 37}]   # max seen in window
              }
            }
          ],
          "summary_metadata": {
            "window_seconds": 300,
            "messages_aggregated": 123,
            "start_time": 1710000000.0,
            "end_time": 1710000300.0
          }
        }
    """

    def __init__(
        self,
        session: Session,
        inference_pipeline_id: str,
        flush_interval_seconds: int = 300,
    ) -> None:
        self.session = session
        self.inference_pipeline_id = inference_pipeline_id
        self.flush_interval_seconds = flush_interval_seconds

        self.kafka_producer = self._setup_kafka_producer()

        # Threading
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._is_running = False
        self._lock = threading.RLock()

        # Ingestion queue
        self._ingest_queue: List[Dict[str, Any]] = []

        # Aggregation buffers keyed by (camera_group, camera_name)
        # Each value holds:
        #   {
        #       "window_start": float,
        #       "last_seen": float,
        #       "camera_info": dict,
        #       "messages": int,
        #       "apps": {
        #           application_key_name: {
        #               "meta": {name, key_name, version},
        #               "last_input_timestamp": str,
        #               "earliest_reset_timestamp": str | None,
        #               "current_counts": {category: last_value},
        #               "total_counts": {category: max_value}
        #           }
        #       }
        #   }
        #
        self._buffers: Dict[Tuple[str, str], Dict[str, Any]] = {}

        # Track previous total_counts per (camera_group, camera_name, application_key_name)
        # Used to compute per-window deltas for current_counts at flush time
        self._prev_total_counts: Dict[Tuple[str, str, str], Dict[str, int]] = {}

        # Location aggregation buffers keyed by (camera_group, location)
        # Each value holds similar structure to camera buffers but aggregated by location
        self._location_buffers: Dict[Tuple[str, str], Dict[str, Any]] = {}
        
        # Track previous location total_counts per (camera_group, location, application_key_name)
        self._prev_location_total_counts: Dict[Tuple[str, str, str], Dict[str, int]] = {}

        # Incident tracking buffers keyed by (camera_group, camera_name, application_key_name)
        # Each value holds incidents for immediate publishing
        self._incident_buffers: Dict[Tuple[str, str, str], List[Dict[str, Any]]] = {}

        # Stats
        self.stats = {
            "start_time": None,
            "summaries_published": 0,
            "location_summaries_published": 0,
            "incidents_published": 0,
            "messages_ingested": 0,
            "errors": 0,
            "last_error": None,
            "last_error_time": None,
            "last_flush_time": None,
        }

    def _setup_kafka_producer(self):
        path = "/v1/actions/get_kafka_info"

        response = self.session.rpc.get(path=path, raise_exception=True)

        if not response or not response.get("success"):
            raise ValueError(f"Failed to fetch Kafka config: {response.get('message', 'No response')}")

        # Decode base64 fields
        encoded_ip = response["data"]["ip"]
        encoded_port = response["data"]["port"]
        ip = base64.b64decode(encoded_ip).decode("utf-8")
        port = base64.b64decode(encoded_port).decode("utf-8")
        bootstrap_servers = f"{ip}:{port}"
        
        
        # Kafka handler for summaries (non-blocking configuration)
        kafka_producer = Producer({
            "bootstrap.servers": bootstrap_servers,
            "acks": "all",  # Changed from "all" to reduce blocking
            "retries": 2,  # Reduced retries for faster failure
            "retry.backoff.ms": 500,  # Reduced backoff time
            "request.timeout.ms": 15000,  # Reduced timeout
            "max.in.flight.requests.per.connection": 5,  # Increased for better throughput
            "linger.ms": 5,  # Reduced linger time
            "batch.size": 8192,  # Increased batch size
            "queue.buffering.max.ms": 100,  # Increased buffer time
            "log_level": 0,
            "delivery.timeout.ms": 30000,  # Add delivery timeout
            "enable.idempotence": True,  # Ensure exactly-once delivery
        })
        return kafka_producer
    
    def start(self) -> bool:
        if self._is_running:
            logging.warning("Analytics summarizer already running")
            return True
        try:
            self._stop.clear()
            self._is_running = True
            self.stats["start_time"] = time.time()
            self.stats["last_flush_time"] = time.time()
            self._thread = threading.Thread(
                target=self._run, name=f"AnalyticsSummarizer-{self.inference_pipeline_id}", daemon=True
            )
            self._thread.start()
            logging.info("Analytics summarizer started")
            return True
        except Exception as exc:
            self._record_error(f"Failed to start analytics summarizer: {exc}")
            self.stop()
            return False

    def stop(self) -> None:
        if not self._is_running:
            logging.info("Analytics summarizer not running")
            return
        logging.info("Stopping analytics summarizer...")
        self._is_running = False
        self._stop.set()
        try:
            if self._thread and self._thread.is_alive():
                self._thread.join(timeout=5.0)
        except Exception as exc:
            logging.error(f"Error joining analytics summarizer thread: {exc}")
        self._thread = None
        logging.info("Analytics summarizer stopped")

    def ingest_result(self, aggregated_result: Dict[str, Any]) -> None:
        """
        Receive a single aggregated camera_results payload for buffering.
        This is intended to be called by the publisher after successful publish.
        """
        try:
            with self._lock:
                self._ingest_queue.append(aggregated_result)
                self.stats["messages_ingested"] += 1
        except Exception as exc:
            self._record_error(f"Failed to ingest result: {exc}")

    def _run(self) -> None:
        logging.info("Analytics summarizer worker started")
        while not self._stop.is_set():
            try:
                # Drain ingestion queue
                self._drain_ingest_queue()

                # Time-based flush
                current_time = time.time()
                last_flush = self.stats.get("last_flush_time") or current_time
                if current_time - last_flush >= self.flush_interval_seconds:
                    self._flush_all(current_time)
                    self.stats["last_flush_time"] = current_time

                # Prevent busy loop
                time.sleep(0.5)

            except Exception as exc:
                if not self._stop.is_set():
                    self._record_error(f"Error in summarizer loop: {exc}")
                    time.sleep(0.2)
        # Final flush on stop
        try:
            self._flush_all(time.time())
        except Exception as exc:
            logging.error(f"Error during final analytics flush: {exc}")
        logging.info("Analytics summarizer worker stopped")

    def _drain_ingest_queue(self) -> None:
        local_batch: List[Dict[str, Any]] = []
        with self._lock:
            if self._ingest_queue:
                local_batch = self._ingest_queue
                self._ingest_queue = []

        for result in local_batch:
            try:
                self._add_to_buffers(result)
            except Exception as exc:
                self._record_error(f"Failed buffering result: {exc}")

    def _add_to_buffers(self, result: Dict[str, Any]) -> None:
        camera_info = result.get("camera_info", {}) or {}
        camera_name = camera_info.get("camera_name") or "unknown"
        camera_group = camera_info.get("camera_group") or "default_group"
        location = camera_info.get("location")

        key = (camera_group, camera_name)
        now = time.time()
        buffer = self._buffers.get(key)
        if not buffer:
            buffer = {
                "window_start": now,
                "last_seen": now,
                "camera_info": {
                    "camera_name": camera_name,
                    "camera_group": camera_group,
                    "location": location,
                },
                "messages": 0,
                "apps": {},
            }
            self._buffers[key] = buffer
        else:
            buffer["last_seen"] = now
            # Update location if provided
            if location:
                buffer["camera_info"]["location"] = location

        buffer["messages"] += 1
        
        # Also update location buffer
        if location:
            self._add_to_location_buffer(camera_group, location, result, now)

        # Process each app
        agg_apps = result.get("agg_apps", []) or []
        for app in agg_apps:
            app_name = app.get("application_name") or app.get("app_name") or "unknown"
            app_key = app.get("application_key_name") or app.get("application_key") or app_name
            app_ver = app.get("application_version") or app.get("version") or ""

            app_buf = buffer["apps"].get(app_key)
            if not app_buf:
                app_buf = {
                    "meta": {
                        "application_name": app_name,
                        "application_key_name": app_key,
                        "application_version": app_ver,
                    },
                    "last_input_timestamp": None,
                    "reset_timestamp": None,
                    "current_counts": {},
                    "total_counts": {},
                }
                buffer["apps"][app_key] = app_buf

            # Extract tracking_stats from app
            tracking_stats = self._extract_tracking_stats_from_app(app)
            if not tracking_stats:
                continue

            input_ts = tracking_stats.get("input_timestamp")
            reset_ts = tracking_stats.get("reset_timestamp")
            current_counts = tracking_stats.get("current_counts") or []
            total_counts = tracking_stats.get("total_counts") or []

            if input_ts:
                app_buf["last_input_timestamp"] = input_ts
            if reset_ts is not None:
                # Simplify: keep last seen reset timestamp only
                app_buf["reset_timestamp"] = reset_ts

            # Update current counts (take last observed)
            for item in current_counts:
                cat = item.get("category")
                cnt = item.get("count")
                if cat is not None and cnt is not None:
                    app_buf["current_counts"][cat] = cnt

            # Update total counts (take max observed to avoid double-counting cumulative totals)
            for item in total_counts:
                cat = item.get("category")
                cnt = item.get("count")
                if cat is None or cnt is None:
                    continue
                existing = app_buf["total_counts"].get(cat)
                if existing is None or cnt > existing:
                    app_buf["total_counts"][cat] = cnt

        # Extract and process incidents from the main buffer processing
        self._extract_and_process_incidents(camera_group, camera_name, app, camera_info)

    def _add_to_location_buffer(self, camera_group: str, location: str, result: Dict[str, Any], now: float) -> None:
        """Add result to location aggregation buffer."""
        key = (camera_group, location)
        buffer = self._location_buffers.get(key)
        
        if not buffer:
            buffer = {
                "window_start": now,
                "last_seen": now,
                "camera_group": camera_group,
                "location": location,
                "messages": 0,
                "cameras": {},  # Track individual cameras in this location
                "apps": {},  # Aggregated app data for this location
            }
            self._location_buffers[key] = buffer
        else:
            buffer["last_seen"] = now

        buffer["messages"] += 1
        
        # Track camera data within location
        camera_info = result.get("camera_info", {}) or {}
        camera_name = camera_info.get("camera_name") or "unknown"
        
        if camera_name not in buffer["cameras"]:
            buffer["cameras"][camera_name] = {
                "camera_name": camera_name,
                "camera_group": camera_group,
                "location": location,
                "messages": 0,
                "apps": {},
            }
        
        camera_buffer = buffer["cameras"][camera_name]
        camera_buffer["messages"] += 1
        
        # Process each app for both camera-level and location-level aggregation
        agg_apps = result.get("agg_apps", []) or []
        for app in agg_apps:
            app_name = app.get("application_name") or app.get("app_name") or "unknown"
            app_key = app.get("application_key_name") or app.get("application_key") or app_name
            app_ver = app.get("application_version") or app.get("version") or ""
            
            # Update camera-level app data
            if app_key not in camera_buffer["apps"]:
                camera_buffer["apps"][app_key] = {
                    "meta": {
                        "application_name": app_name,
                        "application_key_name": app_key,
                        "application_version": app_ver,
                    },
                    "last_input_timestamp": None,
                    "reset_timestamp": None,
                    "current_counts": {},
                    "total_counts": {},
                }
            
            # Update location-level app data
            if app_key not in buffer["apps"]:
                buffer["apps"][app_key] = {
                    "meta": {
                        "application_name": app_name,
                        "application_key_name": app_key,
                        "application_version": app_ver,
                    },
                    "last_input_timestamp": None,
                    "reset_timestamp": None,
                    "current_counts": {},
                    "total_counts": {},
                }
            
            # Extract tracking stats and update both levels
            tracking_stats = self._extract_tracking_stats_from_app(app)
            if tracking_stats:
                self._update_app_buffer_with_tracking_stats(camera_buffer["apps"][app_key], tracking_stats)
                self._update_location_app_buffer_with_tracking_stats(buffer["apps"][app_key], tracking_stats)
            
            # Extract and process incidents from the app
            self._extract_and_process_incidents(camera_group, camera_name, app, camera_info)

    def _update_app_buffer_with_tracking_stats(self, app_buf: Dict[str, Any], tracking_stats: Dict[str, Any]) -> None:
        """Update app buffer with tracking stats - shared logic."""
        input_ts = tracking_stats.get("input_timestamp")
        reset_ts = tracking_stats.get("reset_timestamp")
        current_counts = tracking_stats.get("current_counts") or []
        total_counts = tracking_stats.get("total_counts") or []

        if input_ts:
            app_buf["last_input_timestamp"] = input_ts
        if reset_ts is not None:
            app_buf["reset_timestamp"] = reset_ts

        # Update current counts (take last observed)
        for item in current_counts:
            cat = item.get("category")
            cnt = item.get("count")
            if cat is not None and cnt is not None:
                app_buf["current_counts"][cat] = cnt

        # Update total counts (take max observed)
        for item in total_counts:
            cat = item.get("category")
            cnt = item.get("count")
            if cat is None or cnt is None:
                continue
            existing = app_buf["total_counts"].get(cat)
            if existing is None or cnt > existing:
                app_buf["total_counts"][cat] = cnt

    def _update_location_app_buffer_with_tracking_stats(self, app_buf: Dict[str, Any], tracking_stats: Dict[str, Any]) -> None:
        """Update location app buffer with tracking stats - aggregated across cameras."""
        input_ts = tracking_stats.get("input_timestamp")
        reset_ts = tracking_stats.get("reset_timestamp")
        current_counts = tracking_stats.get("current_counts") or []
        total_counts = tracking_stats.get("total_counts") or []

        # For location aggregation, take the latest timestamp
        if input_ts:
            current_ts = app_buf.get("last_input_timestamp")
            if not current_ts or input_ts > current_ts:
                app_buf["last_input_timestamp"] = input_ts
        
        if reset_ts is not None:
            current_reset = app_buf.get("reset_timestamp")
            if not current_reset or reset_ts < current_reset:
                app_buf["reset_timestamp"] = reset_ts

        # Aggregate current counts (sum across cameras)
        for item in current_counts:
            cat = item.get("category")
            cnt = item.get("count")
            if cat is not None and cnt is not None:
                existing = app_buf["current_counts"].get(cat, 0)
                app_buf["current_counts"][cat] = existing + cnt

        # Aggregate total counts (sum across cameras)
        for item in total_counts:
            cat = item.get("category")
            cnt = item.get("count")
            if cat is None or cnt is None:
                continue
            existing = app_buf["total_counts"].get(cat, 0)
            app_buf["total_counts"][cat] = existing + cnt

    def _extract_and_process_incidents(self, camera_group: str, camera_name: str, app: Dict[str, Any], camera_info: Dict[str, Any]) -> None:
        """Extract incidents from app data and publish them immediately to incident_res topic."""
        try:
            app_name = app.get("application_name") or app.get("app_name") or "unknown"
            app_key = app.get("application_key_name") or app.get("application_key") or app_name
            app_ver = app.get("application_version") or app.get("version") or ""
            
            # Extract incidents from various possible locations in the app data
            incidents = []
            
            # Check direct incidents in app
            if "incidents" in app and isinstance(app["incidents"], list):
                incidents.extend(app["incidents"])
            
            # Check incidents in agg_summary
            agg_summary = app.get("agg_summary", {})
            if isinstance(agg_summary, dict):
                # Look through frame-based structure
                for frame_key, frame_data in agg_summary.items():
                    if isinstance(frame_data, dict) and "incidents" in frame_data:
                        frame_incidents = frame_data["incidents"]
                        if isinstance(frame_incidents, list):
                            incidents.extend(frame_incidents)
                        elif isinstance(frame_incidents, dict):
                            # If incidents is a dict, treat values as incidents
                            for incident_data in frame_incidents.values():
                                if isinstance(incident_data, dict):
                                    incidents.append(incident_data)
            
            # Check incidents in tracking_stats
            tracking_stats = self._extract_tracking_stats_from_app(app)
            if tracking_stats and "incidents" in tracking_stats:
                if isinstance(tracking_stats["incidents"], list):
                    incidents.extend(tracking_stats["incidents"])
            
            # If we found incidents, publish them immediately
            if incidents:
                self._publish_incidents_immediately(
                    camera_name, camera_group, camera_info.get("location"),
                    app_name, app_key, app_ver, incidents
                )
                
        except Exception as exc:
            self._record_error(f"Failed to extract incidents from app {app_name}: {exc}")

    def _publish_incidents_immediately(self, camera_name: str, camera_group: str, location: str,
                                     app_name: str, app_key: str, app_version: str, 
                                     incidents: List[Dict[str, Any]]) -> None:
        """Publish incidents immediately to incident_res topic."""
        try:
            # Create incident payload according to the specified structure
            incident_payload = {
                "camera_name": camera_name,
                "inferencePipelineId": self.inference_pipeline_id,
                "camera_group": camera_group,
                "location": location or "Unknown Location",
                "application_name": app_name,
                "application_key_name": app_key,
                "application_version": app_version,
                "incidents": []
            }
            
            # Process each incident to ensure proper structure
            for incident in incidents:
                if not isinstance(incident, dict):
                    continue
                
                # Ensure required incident fields with defaults
                processed_incident = {
                    "incident_id": incident.get("incident_id", f"inc_{int(time.time())}"),
                    "incident_type": incident.get("incident_type", "unknown"),
                    "severity_level": incident.get("severity_level", "low"),
                    "human_text": incident.get("human_text", "Incident detected"),
                    "start_time": incident.get("start_time", time.strftime("%Y-%m-%dT%H:%M:%SZ")),
                    "end_time": incident.get("end_time", ""),
                    "camera_info": incident.get("camera_info", f"Camera at {location}"),
                    "level_settings": incident.get("level_settings", "Level 1"),
                    "content": incident.get("content", ""),  # Base64 image content if available
                    "alerts": incident.get("alerts", []),
                    "alert_settings": incident.get("alert_settings", [])
                }
                
                incident_payload["incidents"].append(processed_incident)
            
            # Only publish if we have valid incidents
            if incident_payload["incidents"]:
                # Publish incident data via Kafka - non-blocking with robust error handling
                try:
                    # Use callback for non-blocking operation
                    def incident_delivery_callback(err, msg):
                        if err:
                            self._record_error(f"Failed to deliver incident message: {err}")
                        else:
                            logging.debug(f"Incident message delivered to {msg.topic()} [{msg.partition()}]")
                    
                    self.kafka_producer.produce(
                        topic="incident_res",
                        key=f"{camera_name}_{app_key}".encode("utf-8"),
                        value=json.dumps(incident_payload, separators=(",", ":")).encode("utf-8"),
                        callback=incident_delivery_callback
                    )
                    
                    # Non-blocking poll to process delivery callbacks
                    self.kafka_producer.poll(0)
                    
                    self.stats["incidents_published"] += 1
                    logging.debug(
                        f"Published {len(incident_payload['incidents'])} incidents for camera {camera_name}, app {app_name}"
                    )
                except Exception as kafka_exc:
                    self._record_error(f"Failed to produce incident message to Kafka: {kafka_exc}")
                    # Continue processing - don't fail the entire analytics flow for incident issues
                    
        except Exception as exc:
            self._record_error(f"Failed to publish incidents for {camera_name}/{app_name}: {exc}")

    def _extract_tracking_stats_from_app(self, app: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # Prefer direct 'tracking_stats' if present
        if isinstance(app.get("tracking_stats"), dict):
            return app["tracking_stats"]

        # Otherwise, try agg_summary structure: pick latest by key order
        agg_summary = app.get("agg_summary")
        if isinstance(agg_summary, dict) and agg_summary:
            # Keys might be frame numbers as strings -> choose max numerically
            try:
                latest_key = max(agg_summary.keys(), key=lambda k: int(str(k)))
            except Exception:
                latest_key = sorted(agg_summary.keys())[-1]
            entry = agg_summary.get(latest_key) or {}
            ts = entry.get("tracking_stats")
            if isinstance(ts, dict):
                return ts
        return None

    def _flush_all(self, end_time: float) -> None:
        # Build and publish summaries per camera
        with self._lock:
            items = list(self._buffers.items())
            location_items = list(self._location_buffers.items())
            # Reset buffers after copying references
            self._buffers = {}
            self._location_buffers = {}

        for (camera_group, camera_name), buf in items:
            try:
                camera_info = buf.get("camera_info", {})
                start_time = buf.get("window_start", end_time)
                messages = buf.get("messages", 0)

                agg_apps_output: List[Dict[str, Any]] = []
                for app_key, app_buf in buf.get("apps", {}).items():
                    # Compute per-window delta for current_counts using previous total_counts
                    curr_total_dict = app_buf.get("total_counts", {}) or {}
                    prev_key = (camera_group, camera_name, app_key)
                    prev_total_dict = self._prev_total_counts.get(prev_key, {}) or {}

                    # Delta = max(curr_total - prev_total, 0) per category
                    window_delta_dict: Dict[str, int] = {}
                    for cat, curr_cnt in curr_total_dict.items():
                        try:
                            prev_cnt = int(prev_total_dict.get(cat, 0))
                            curr_cnt_int = int(curr_cnt)
                            delta = curr_cnt_int - prev_cnt
                            if delta < 0:
                                # Counter reset detected; treat current as delta for this window
                                delta = curr_cnt_int
                            window_delta_dict[cat] = delta
                        except Exception:
                            # Fallback: if parsing fails, emit current as-is
                            window_delta_dict[cat] = curr_cnt

                    # Convert dicts to lists for output
                    current_list = [
                        {"category": cat, "count": cnt}
                        for cat, cnt in window_delta_dict.items()
                    ]
                    total_list = [
                        {"category": cat, "count": cnt}
                        for cat, cnt in curr_total_dict.items()
                    ]

                    agg_apps_output.append(
                        {
                            **app_buf["meta"],
                            "tracking_stats": {
                                "input_timestamp": app_buf.get("last_input_timestamp"),
                                "reset_timestamp": app_buf.get("reset_timestamp"),
                                "current_counts": current_list,
                                "total_counts": total_list,
                            },
                        }
                    )

                    # Update previous totals baseline for next window
                    self._prev_total_counts[prev_key] = dict(curr_total_dict)

                summary_payload = {
                    "camera_name": camera_info.get("camera_name", camera_name),
                    "inferencePipelineId": self.inference_pipeline_id,
                    "camera_group": camera_info.get("camera_group", camera_group),
                    "location": camera_info.get("location"),
                    "agg_apps": agg_apps_output,
                    "summary_metadata": {
                        "window_seconds": self.flush_interval_seconds,
                        "messages_aggregated": messages,
                    },
                }

                # Publish via Kafka (JSON bytes) - non-blocking with robust error handling
                try:
                    # Use callback for non-blocking operation
                    def delivery_callback(err, msg):
                        if err:
                            self._record_error(f"Failed to deliver analytics message: {err}")
                        else:
                            logging.debug(f"Analytics message delivered to {msg.topic()} [{msg.partition()}]")
                    
                    self.kafka_producer.produce(
                        topic="results-agg",
                        key=str(camera_name).encode("utf-8"),
                        value=json.dumps(summary_payload, separators=(",", ":")).encode("utf-8"),
                        callback=delivery_callback
                    )
                    
                    # Non-blocking poll to process delivery callbacks
                    self.kafka_producer.poll(0)
                    
                    self.stats["summaries_published"] += 1
                    logging.debug(
                        f"Published 5-min summary for camera {camera_group}/{camera_name} with {len(agg_apps_output)} apps"
                    )
                except Exception as kafka_exc:
                    self._record_error(f"Failed to produce analytics message to Kafka: {kafka_exc}")
                    # Continue processing other cameras even if one fails
            except Exception as exc:
                self._record_error(f"Failed to publish summary for {camera_group}/{camera_name}: {exc}")
        
        # Flush location aggregation data
        self._flush_location_data(location_items, end_time)
        
        # Brief non-blocking flush for delivery
        try:
            # Non-blocking poll to handle any pending callbacks
            self.kafka_producer.poll(0)
            # Short flush timeout to avoid blocking
            self.kafka_producer.flush(timeout=2)
        except Exception as flush_exc:
            logging.warning(f"Analytics kafka flush error (non-critical): {flush_exc}")
            pass

    def _flush_location_data(self, location_items: List[Tuple[Tuple[str, str], Dict[str, Any]]], end_time: float) -> None:
        """Flush location aggregation data to location_raw topic."""
        for (camera_group, location), buf in location_items:
            try:
                start_time = buf.get("window_start", end_time)
                messages = buf.get("messages", 0)
                cameras_data = buf.get("cameras", {})
                location_apps = buf.get("apps", {})

                # Build camera stats array
                camera_stats = []
                for camera_name, camera_data in cameras_data.items():
                    camera_apps = []
                    for app_key, app_buf in camera_data.get("apps", {}).items():
                        # Convert dicts to lists for camera output
                        current_list = [
                            {"category": cat, "count": cnt}
                            for cat, cnt in app_buf.get("current_counts", {}).items()
                        ]
                        total_list = [
                            {"category": cat, "count": cnt}
                            for cat, cnt in app_buf.get("total_counts", {}).items()
                        ]

                        camera_apps.append({
                            **app_buf["meta"],
                            "tracking_stats": {
                                "input_timestamp": app_buf.get("last_input_timestamp"),
                                "reset_timestamp": app_buf.get("reset_timestamp"),
                                "current_counts": current_list,
                                "total_counts": total_list,
                            },
                        })

                    camera_stats.append({
                        "camera_name": camera_name,
                        "inferencePipelineId": self.inference_pipeline_id,
                        "camera_group": camera_group,
                        "location": location,
                        "agg_apps": camera_apps,
                        "summary_metadata": {
                            "window_seconds": self.flush_interval_seconds,
                            "messages_aggregated": camera_data.get("messages", 0),
                        },
                    })

                # Build location-level app stats
                apps_stats = []
                for app_key, app_buf in location_apps.items():
                    # For location aggregation, compute per-window delta using previous location totals
                    curr_total_dict = app_buf.get("total_counts", {}) or {}
                    prev_key = (camera_group, location, app_key)
                    prev_total_dict = self._prev_location_total_counts.get(prev_key, {}) or {}

                    # Delta = max(curr_total - prev_total, 0) per category
                    window_delta_dict: Dict[str, int] = {}
                    for cat, curr_cnt in curr_total_dict.items():
                        try:
                            prev_cnt = int(prev_total_dict.get(cat, 0))
                            curr_cnt_int = int(curr_cnt)
                            delta = curr_cnt_int - prev_cnt
                            if delta < 0:
                                # Counter reset detected; treat current as delta for this window
                                delta = curr_cnt_int
                            window_delta_dict[cat] = delta
                        except Exception:
                            # Fallback: if parsing fails, emit current as-is
                            window_delta_dict[cat] = curr_cnt

                    # Convert dicts to lists for output
                    current_list = [
                        {"category": cat, "count": cnt}
                        for cat, cnt in window_delta_dict.items()
                    ]
                    total_list = [
                        {"category": cat, "count": cnt}
                        for cat, cnt in curr_total_dict.items()
                    ]

                    apps_stats.append({
                        **app_buf["meta"],
                        "tracking_stats": {
                            "input_timestamp": app_buf.get("last_input_timestamp"),
                            "reset_timestamp": app_buf.get("reset_timestamp"),
                            "current_counts": current_list,
                            "total_counts": total_list,
                        },
                    })

                    # Update previous totals baseline for next window
                    self._prev_location_total_counts[prev_key] = dict(curr_total_dict)

                # Build location payload
                location_payload = {
                    "message": "success",
                    "inferencePipelineId": self.inference_pipeline_id,
                    "camera_group_name": camera_group,
                    "camera_group_location": location,
                    "camera_stats": camera_stats,
                    "apps_stats": apps_stats,
                }

                # Publish location data via Kafka - non-blocking with robust error handling
                try:
                    # Use callback for non-blocking operation
                    def location_delivery_callback(err, msg):
                        if err:
                            self._record_error(f"Failed to deliver location analytics message: {err}")
                        else:
                            logging.debug(f"Location analytics message delivered to {msg.topic()} [{msg.partition()}]")
                    
                    self.kafka_producer.produce(
                        topic="location_raw",
                        key=f"{camera_group}_{location}".encode("utf-8"),
                        value=json.dumps(location_payload, separators=(",", ":")).encode("utf-8"),
                        callback=location_delivery_callback
                    )
                    
                    # Non-blocking poll to process delivery callbacks
                    self.kafka_producer.poll(0)
                    
                    self.stats["location_summaries_published"] += 1
                    logging.debug(
                        f"Published location summary for {camera_group}/{location} with {len(camera_stats)} cameras and {len(apps_stats)} apps"
                    )
                except Exception as kafka_exc:
                    self._record_error(f"Failed to produce location analytics message to Kafka: {kafka_exc}")
                    # Continue processing other locations even if one fails

            except Exception as exc:
                self._record_error(f"Failed to publish location summary for {camera_group}/{location}: {exc}")

    def _record_error(self, error_message: str) -> None:
        with self._lock:
            self.stats["errors"] += 1
            self.stats["last_error"] = error_message
            self.stats["last_error_time"] = time.time()
        logging.error(f"Analytics summarizer error: {error_message}")

    def get_stats(self) -> Dict[str, Any]:
        with self._lock:
            stats = dict(self.stats)
        if stats.get("start_time"):
            stats["uptime_seconds"] = time.time() - stats["start_time"]
        return stats

    def get_health_status(self) -> Dict[str, Any]:
        health = {
            "status": "healthy",
            "is_running": self._is_running,
            "errors": self.stats["errors"],
            "summaries_published": self.stats["summaries_published"],
            "messages_ingested": self.stats["messages_ingested"],
        }
        if (
            self.stats.get("last_error_time")
            and (time.time() - self.stats["last_error_time"]) < 60
        ):
            health["status"] = "degraded"
            health["reason"] = f"Recent error: {self.stats.get('last_error')}"
        if not self._is_running:
            health["status"] = "unhealthy"
            health["reason"] = "Summarizer is not running"
        return health

    def cleanup(self) -> None:
        try:
            self.stop()
        except Exception:
            pass
        with self._lock:
            self._ingest_queue = []
            self._buffers = {}
            self._location_buffers = {}
            self._prev_location_total_counts = {}
            self._incident_buffers = {}
        try:
            if hasattr(self, "kafka_producer") and self.kafka_producer is not None:
                # Non-blocking cleanup with timeout
                self.kafka_producer.poll(0)  # Process any pending callbacks
                self.kafka_producer.flush(timeout=3)  # Short timeout for cleanup
        except Exception as exc:
            logging.warning(f"Analytics kafka producer cleanup error (non-critical): {exc}")
        logging.info("Analytics summarizer cleanup completed")


