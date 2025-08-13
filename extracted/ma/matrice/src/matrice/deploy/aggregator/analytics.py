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

        # Stats
        self.stats = {
            "start_time": None,
            "summaries_published": 0,
            "messages_ingested": 0,
            "errors": 0,
            "last_error": None,
            "last_error_time": None,
            "last_flush_time": None,
        }

    def _setup_kafka_producer(self):
        path = "/v1/actions/get_kafka_info"

        response = self.session.get(path=path, raise_exception=True)

        if not response or not response.get("success"):
            raise ValueError(f"Failed to fetch Kafka config: {response.get('message', 'No response')}")

        # Decode base64 fields
        encoded_ip = response["data"]["ip"]
        encoded_port = response["data"]["port"]
        ip = base64.b64decode(encoded_ip).decode("utf-8")
        port = base64.b64decode(encoded_port).decode("utf-8")
        bootstrap_servers = f"{ip}:{port}"
        
        
        # Kafka handler for summaries (reuse pipeline server topic)
        kafka_producer = Producer({
            "bootstrap.servers": bootstrap_servers,
            "acks": "all",
            "retries": 3,
            "retry.backoff.ms": 1000,
            "request.timeout.ms": 30000,
            "max.in.flight.requests.per.connection": 1,
            "linger.ms": 10,
            "batch.size": 4096,
            "queue.buffering.max.ms": 50,
            "log_level": 0,
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
            # Reset buffers after copying references
            self._buffers = {}

        for (camera_group, camera_name), buf in items:
            try:
                camera_info = buf.get("camera_info", {})
                start_time = buf.get("window_start", end_time)
                messages = buf.get("messages", 0)

                agg_apps_output: List[Dict[str, Any]] = []
                for app_key, app_buf in buf.get("apps", {}).items():
                    # Convert counts dicts to lists
                    current_list = [
                        {"category": cat, "count": cnt}
                        for cat, cnt in app_buf.get("current_counts", {}).items()
                    ]
                    total_list = [
                        {"category": cat, "count": cnt}
                        for cat, cnt in app_buf.get("total_counts", {}).items()
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

                # Publish via Kafka (JSON bytes)
                self.kafka_producer.produce(
                    topic="Analytics-Inference-Pipeline",
                    key=str(camera_name).encode("utf-8"),
                    value=json.dumps(summary_payload, separators=(",", ":")).encode("utf-8"),
                )
                self.stats["summaries_published"] += 1
                logging.debug(
                    f"Published 5-min summary for camera {camera_group}/{camera_name} with {len(agg_apps_output)} apps"
                )
            except Exception as exc:
                self._record_error(f"Failed to publish summary for {camera_group}/{camera_name}: {exc}")
        # Brief flush for delivery
        try:
            self.kafka_producer.poll(0)
            self.kafka_producer.flush(5)
        except Exception:
            pass

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
        try:
            if hasattr(self, "kafka_producer") and self.kafka_producer is not None:
                self.kafka_producer.flush(5)
        except Exception as exc:
            logging.error(f"Error flushing analytics kafka producer: {exc}")
        logging.info("Analytics summarizer cleanup completed")


