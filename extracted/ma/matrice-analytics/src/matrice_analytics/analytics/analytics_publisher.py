"""
Analytics Publisher Worker - Aggregates and publishes tracking statistics.

Flow: Post-Processing -> Output Queue -> Producer -> Analytics Publisher
      Analytics Publisher reads from output queue and publishes aggregated stats to Redis/Kafka
"""

import asyncio
import json
import logging
import os
import queue
import threading
import time
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

from matrice_common.stream.matrice_stream import MatriceStream, StreamType


class AnalyticsPublisher:
    """
    Publishes aggregated analytics to Redis (localhost) and Kafka internal streams.

    Monitors output queue and aggregates tracking statistics over 5-minute windows.
    Publishes to 'results-agg' topic on both Redis and Kafka.

    Output structure (zone-keyed: tracking_stats maps zone_id -> stats; the old
    non-zone-aware flow uses the single "global" zone):
        tracking_stats: {
            "global": {
                "input_timestamp": "2026-06-14T06:30:00Z",                  # RFC3339 UTC event time
                "current_counts": [{"category": "person", "count": 2}],         # NEW people in this publish window (delta)
                "total_current_counts": [{"category": "person", "count": 7}],   # ALL people in frame right now
                "total_counts": [{"category": "person", "count": 15}]           # Cumulative unique since reset
            }
        }
    """

    DEFAULT_AGGREGATION_INTERVAL = 300  # 5 minutes in seconds
    DEFAULT_PUBLISH_INTERVAL = 60  # Publish every 60 seconds
    ANALYTICS_TOPIC = "results-agg"
    # Minimum seconds between "queue full" warnings; the drop COUNT is exact
    # regardless, only the logging is throttled.
    _DROP_LOG_INTERVAL_S = 30.0
    # Zone id for the non-zone-aware old post-processing flow. tracking_stats is published as
    # {ANALYTICS_ZONE_GLOBAL: {...}} to satisfy the zone-keyed results-agg consumer.
    ANALYTICS_ZONE_GLOBAL = "global"

    def __init__(
        self,
        # camera_id -> camera config. Accepts BOTH a CameraConfig-like object
        # (with a .stream_config attribute) and an engine dict of the form
        # {"stream_config": {...}}; _build_analytics_message reads metadata from
        # either form. The engine-dict form is what ml-codebases deploy.py passes.
        camera_configs: Dict[str, Any],
        aggregation_interval: int = DEFAULT_AGGREGATION_INTERVAL,
        publish_interval: int = DEFAULT_PUBLISH_INTERVAL,
        app_deployment_id: Optional[str] = None,
        inference_pipeline_id: Optional[str] = None,
        deployment_instance_id: Optional[str] = None,
        app_id: Optional[str] = None,
        app_name: Optional[str] = None,
        app_version: Optional[str] = None,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_password: Optional[str] = None,
        redis_username: Optional[str] = None,
        redis_db: int = 0,
        sentinel_hosts: Optional[List] = None,
        master_name: Optional[str] = None,
        kafka_bootstrap_servers: Optional[str] = None,
        enable_kafka: bool = False,
    ):
        self.camera_configs = camera_configs
        self._camera_configs_lock = threading.Lock()
        self.aggregation_interval = aggregation_interval
        self.publish_interval = publish_interval
        self.app_deployment_id = app_deployment_id
        self.inference_pipeline_id = inference_pipeline_id
        self.deployment_instance_id = deployment_instance_id
        self.app_id = app_id
        self.app_name = app_name or "Unknown Application"
        self.app_version = app_version or "1.0"

        # Redis connection params
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_password = redis_password
        self.redis_username = redis_username
        self.redis_db = redis_db
        self.sentinel_hosts = sentinel_hosts
        self.master_name = master_name

        # Optional callback to get fresh Redis config from API (for retry scenarios)
        self._redis_config_provider: Optional[Callable[[], Optional[Dict[str, Any]]]] = None

        # Kafka connection params
        self.enable_kafka = enable_kafka
        self.kafka_bootstrap_servers = kafka_bootstrap_servers

        self.running = False
        self.logger = logging.getLogger(f"{__name__}.analytics_publisher")

        # Analytics aggregation storage (per camera)
        # Structure: {camera_id: {category: {"current": count, "total": count, "last_reset": timestamp}}}
        self.analytics_store: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(lambda: defaultdict(dict))
        self.reset_timestamps: Dict[str, str] = {}  # {camera_id: reset_timestamp}

        # Track previous total_counts per (camera_id, category) for computing deltas
        # Used to compute per-window deltas for current_counts at publish time
        self._prev_total_counts: Dict[str, Dict[str, int]] = defaultdict(dict)

        # Frame counter per camera for debugging (tracks frames per publish window)
        self._frame_counts: Dict[str, int] = defaultdict(int)

        # Carry into next 60s window: last-frame in-frame occupancy (from
        # tracking_stats.total_current_counts) of the previous published window.
        # Empty on first publish after start so total_current_counts == current_counts.
        self._prev_window_last_frame_current: Dict[str, Dict[str, int]] = defaultdict(dict)
        # Latest in-frame occupancy seen this window (overwritten every frame).
        self._last_frame_current: Dict[str, Dict[str, int]] = defaultdict(dict)

        # Hysteresis tracking for reset detection (prevents false positives from fluctuations)
        # Structure: {camera_id: {category: consecutive_drop_count}}
        self._consecutive_drops: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self._reset_drop_threshold = 0.5  # 50% drop triggers potential reset
        self._reset_consecutive_required = 3  # Require 3 consecutive drops to confirm reset

        # Internal queue for receiving analytics data from producer
        # Bounded at 8000 (was 1000) to absorb bursts without dropping frames at enqueue.
        self.analytics_queue: queue.Queue = queue.Queue(maxsize=8000)

        # Enqueue-drop accounting. Drops are silent data loss by design (see
        # enqueue_analytics_data), so they are counted and surfaced in
        # get_metrics(); the warning log is throttled to one per interval.
        self._dropped_messages: int = 0
        self._last_drop_log_monotonic: float = -self._DROP_LOG_INTERVAL_S

        # Stream connections
        self.redis_stream: Optional[MatriceStream] = None
        self.kafka_stream: Optional[MatriceStream] = None

    def start(self) -> threading.Thread:
        """Start the analytics publisher in a separate thread."""
        self.running = True
        thread = threading.Thread(target=self._run, name="AnalyticsPublisher", daemon=False)
        thread.start()
        self.logger.info("Started Analytics Publisher")
        return thread

    def stop(self):
        """Stop the analytics publisher."""
        self.running = False
        self.logger.info("Stopping Analytics Publisher")

    def set_redis_config_provider(self, provider: Callable[[], Optional[Dict[str, Any]]]) -> None:
        """Set a callback that provides fresh Redis connection config for retries.

        The provider should return a dict with keys:
        host, port, password, username, sentinel_hosts, master_name
        """
        self._redis_config_provider = provider

    def update_camera_configs(self, camera_configs: Dict[str, Any]) -> None:
        """Update camera configurations thread-safely."""
        with self._camera_configs_lock:
            self.camera_configs = camera_configs
        self.logger.info("Updated camera_configs: %d cameras", len(camera_configs))

    def _run(self) -> None:
        """Main analytics publisher loop with proper resource management."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Initialize streams
            loop.run_until_complete(self._initialize_streams())

            # Start processing and publishing
            self._process_and_publish_loop(loop)

        except Exception as e:
            self.logger.error(f"Fatal error in analytics publisher: {e}", exc_info=True)
        finally:
            self._cleanup_resources(loop)

    async def _initialize_streams(self) -> None:
        """Initialize Redis and optionally Kafka streams for publishing.

        If no Redis password is available, defers initialization — the main loop
        will retry periodically until credentials become available.
        """
        if not self.redis_password:
            self.logger.warning(
                "No Redis password provided — deferring Redis stream init. "
                "Analytics will be unavailable until credentials are set."
            )
            self.redis_stream = None
            return

        # Initialize Redis stream
        # IMPORTANT: Disable batching for analytics - we want immediate delivery
        try:
            stream_kwargs = dict(
                host=self.redis_host,
                port=self.redis_port,
                password=self.redis_password,
                username=self.redis_username,
                db=self.redis_db,
                enable_batching=False,  # Disable batching for real-time analytics
                pool_max_connections=10,  # Lower pool size for analytics
            )
            if self.sentinel_hosts and self.master_name:
                stream_kwargs["sentinel_hosts"] = self.sentinel_hosts
                stream_kwargs["master_name"] = self.master_name
            self.redis_stream = MatriceStream(StreamType.REDIS, **stream_kwargs)
            await self.redis_stream.async_setup(self.ANALYTICS_TOPIC)
            sentinel_info = f", sentinel=yes, master={self.master_name}" if self.sentinel_hosts else ""
            self.logger.info(
                f"Initialized Redis stream for analytics on {self.redis_host}:{self.redis_port} (batching disabled{sentinel_info})"
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize Redis analytics stream: {e}", exc_info=True)
            self.redis_stream = None  # degrade gracefully instead of crash

        # Initialize Kafka stream (optional)
        if self.enable_kafka and self.kafka_bootstrap_servers:
            try:
                # Transport security is configurable so a deployment on an
                # untrusted network can require TLS without a code change. The
                # default stays SASL_PLAINTEXT to preserve existing private-broker
                # behaviour byte-for-byte; set KAFKA_SECURITY_PROTOCOL=SASL_SSL
                # once the broker terminates TLS.
                security_protocol = os.environ.get("KAFKA_SECURITY_PROTOCOL", "SASL_PLAINTEXT")
                sasl_mechanism = os.environ.get("KAFKA_SASL_MECHANISM", "SCRAM-SHA-256")
                sasl_username = os.environ.get("KAFKA_SASL_USERNAME")
                sasl_password = os.environ.get("KAFKA_SASL_PASSWORD")

                # Passing sasl_username/password=None explicitly does NOT fall back
                # to the library defaults -- it defeats the upstream
                # `if mechanism and username and password:` guard, which silently
                # drops the SASL block *and* security_protocol along with it, so the
                # producer connects unauthenticated over cleartext PLAINTEXT while
                # this code appears to have requested SASL. Only forward the
                # credential kwargs when both are actually present, and say so
                # loudly when they are not, rather than downgrading in silence.
                kafka_kwargs: Dict[str, Any] = {
                    "bootstrap_servers": self.kafka_bootstrap_servers,
                    "security_protocol": security_protocol,
                }
                if sasl_username and sasl_password:
                    kafka_kwargs["sasl_username"] = sasl_username
                    kafka_kwargs["sasl_password"] = sasl_password
                    kafka_kwargs["sasl_mechanism"] = sasl_mechanism
                else:
                    self.logger.warning(
                        "KAFKA_SASL_USERNAME/KAFKA_SASL_PASSWORD not set -- the analytics "
                        "Kafka producer will connect WITHOUT SASL authentication. Set both "
                        "to enable %s over %s.",
                        sasl_mechanism,
                        security_protocol,
                    )

                self.kafka_stream = MatriceStream(StreamType.KAFKA, **kafka_kwargs)
                await self.kafka_stream.async_setup(self.ANALYTICS_TOPIC)
                self.logger.info(f"Initialized Kafka stream for analytics on {self.kafka_bootstrap_servers}")
            except Exception as e:
                self.logger.warning(f"Failed to initialize Kafka analytics stream (non-fatal): {e}")
                self.kafka_stream = None
        else:
            self.logger.info("Kafka analytics publishing disabled")

    def _process_and_publish_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        """Main loop: consume from analytics queue, aggregate, and publish periodically."""
        last_publish_time = time.time()
        last_redis_retry = 0.0

        while self.running:
            try:
                # Lazy retry: if redis_stream is None, refresh config from API every 30s
                current_time = time.time()
                if self.redis_stream is None and current_time - last_redis_retry > 30:
                    last_redis_retry = current_time

                    # Refresh config from API provider if available
                    if self._redis_config_provider:
                        try:
                            fresh = self._redis_config_provider()
                            if fresh:
                                self.redis_host = fresh.get("host", self.redis_host)
                                self.redis_port = int(fresh.get("port", self.redis_port))
                                self.redis_password = fresh.get("password", self.redis_password)
                                self.redis_username = fresh.get("username", self.redis_username)
                                self.sentinel_hosts = fresh.get("sentinel_hosts")
                                self.master_name = fresh.get("master_name")
                                self.logger.info(
                                    "Redis config refreshed from API: host=%s, port=%d, sentinel=%s",
                                    self.redis_host,
                                    self.redis_port,
                                    f"yes, master={self.master_name}" if self.sentinel_hosts else "no",
                                )
                        except Exception as e:
                            self.logger.warning(f"Redis config provider failed: {e}")

                    if self.redis_password:
                        self.logger.info(
                            "Retrying Redis connection (host=%s, port=%d, sentinel=%s)...",
                            self.redis_host,
                            self.redis_port,
                            "yes" if self.sentinel_hosts else "no",
                        )
                        try:
                            loop.run_until_complete(self._initialize_streams())
                        except Exception as e:
                            self.logger.warning(f"Redis retry failed: {e}")

                # Drain ALL available messages from queue (batch processing)
                messages_processed = self._drain_analytics_queue()

                # Check if it's time to publish
                if current_time - last_publish_time >= self.publish_interval:
                    loop.run_until_complete(self._publish_analytics())
                    last_publish_time = current_time

                # Sleep longer if no messages to prevent CPU spinning
                # Sleep shorter if messages were processed to keep up with load
                if messages_processed == 0:
                    time.sleep(0.1)  # No messages, sleep longer
                else:
                    time.sleep(0.001)  # Messages processed, re-check quickly to keep drain ahead of enqueue

            except Exception as e:
                self.logger.error(f"Error in process/publish loop: {e}", exc_info=True)
                time.sleep(1.0)

    def enqueue_analytics_data(self, task_data: Dict[str, Any]) -> None:
        """
        Enqueue analytics data from producer for processing.
        Called by ProducerWorker after sending messages.

        Args:
            task_data: Task data from output queue containing analytics info
        """
        try:
            self.analytics_queue.put_nowait(task_data)
        except queue.Full:
            # Drop, never block: this runs on the per-frame producer path, so
            # applying backpressure here would let a Redis/Kafka stall propagate
            # into post-processing and stall the pipeline. Analytics is a side
            # channel and must never take down inference.
            #
            # The drop is counted (surfaced via get_metrics()["dropped_messages"])
            # so silent analytics loss is visible to monitoring, and the log is
            # rate-limited -- the previous unconditional warning emitted one record
            # per dropped message per camera, which turned a publish stall into a
            # log flood on exactly the path that was already overloaded.
            self._dropped_messages += 1
            now = time.monotonic()
            if now - self._last_drop_log_monotonic >= self._DROP_LOG_INTERVAL_S:
                self.logger.warning(
                    "Analytics queue full, dropping messages (%d dropped since start, queue maxsize=%d)",
                    self._dropped_messages,
                    self.analytics_queue.maxsize,
                )
                self._last_drop_log_monotonic = now
        except Exception as e:
            self.logger.error(f"Error enqueueing analytics data: {e}")

    def _drain_analytics_queue(self) -> int:
        """Drain ALL available messages from analytics queue and update analytics store.

        This uses batch processing to prevent queue overflow. Instead of processing
        one message at a time with timeouts, it drains all available messages as fast
        as possible, enabling the system to handle high input rates.

        Returns:
            int: Number of messages processed
        """
        messages_processed = 0
        max_batch_size = 500  # Process max 500 messages per iteration to prevent blocking

        try:
            # Process messages in batch until queue is empty or batch limit reached
            while messages_processed < max_batch_size:
                try:
                    # Non-blocking get - returns immediately if queue is empty
                    task_data = self.analytics_queue.get_nowait()

                    # Extract analytics data
                    self._extract_and_aggregate_analytics(task_data)
                    messages_processed += 1

                except queue.Empty:
                    # Queue is empty, done processing
                    break

        except Exception as e:
            self.logger.error(f"Error draining analytics queue: {e}", exc_info=True)

        # Log if we processed a significant batch
        if messages_processed > 0:
            self.logger.debug(f"Processed {messages_processed} analytics messages from queue")

        return messages_processed

    def _extract_agg_summary(self, task_data: Dict[str, Any]) -> tuple:
        """Extract and validate agg_summary from task data.

        Returns:
            Tuple of (camera_id, agg_summary) or (None, None) if extraction fails.
        """
        camera_id = task_data.get("camera_id")
        if not camera_id:
            self.logger.warning(f"[ANALYTICS_SKIP] No camera_id in task_data. Available keys: {list(task_data.keys())}")
            return None, None

        data = task_data.get("data", {})
        if not data:
            self.logger.warning(
                f"[ANALYTICS_SKIP] camera={camera_id} - 'data' field is empty or missing. "
                f"task_data keys: {list(task_data.keys())}"
            )
            return None, None

        post_processing_result = data.get("post_processing_result", {})
        if not post_processing_result:
            self.logger.warning(
                f"[ANALYTICS_SKIP] camera={camera_id} - 'post_processing_result' is empty or missing. "
                f"data keys: {list(data.keys())}"
            )
            return None, None

        # Check for agg_summary at top level (current format after flattening)
        # or nested in data field (legacy format for backward compatibility)
        agg_summary = post_processing_result.get("agg_summary")
        if agg_summary is None and "data" in post_processing_result:
            agg_summary = post_processing_result.get("data", {}).get("agg_summary")
            if agg_summary:
                self.logger.debug(f"Found agg_summary in legacy nested format for camera {camera_id}")

        if not agg_summary or not isinstance(agg_summary, dict):
            pp_keys = list(post_processing_result.keys()) if post_processing_result else "empty"
            self.logger.warning(
                f"[ANALYTICS_SKIP] camera={camera_id} - No valid agg_summary. "
                f"post_processing_result keys: {pp_keys}. "
                f"Expected 'agg_summary' dict but got: {type(agg_summary).__name__}"
            )
            return None, None

        return camera_id, agg_summary

    def _validated_count_list(self, raw_value: Any, field_name: str, camera_id: str, frame_id: str) -> list:
        """Validate and return a count list, logging issues and defaulting to [].

        Args:
            raw_value: The raw value from tracking_stats.
            field_name: Name of the field (for logging).
            camera_id: Camera ID (for logging).
            frame_id: Frame ID (for logging).

        Returns:
            A validated list (empty list if the value was missing or wrong type).
        """
        if raw_value is None:
            self.logger.debug(
                f"[ANALYTICS_MISSING] camera={camera_id}, frame={frame_id}: "
                f"{field_name} missing or null from app, assuming []"
            )
            return []
        if not isinstance(raw_value, list):
            self.logger.debug(
                f"[ANALYTICS_MISSING] camera={camera_id}, frame={frame_id}: {field_name} not a list, assuming []"
            )
            return []
        return raw_value

    def _extract_and_aggregate_analytics(self, task_data: Dict[str, Any]) -> None:
        """Extract tracking stats from task data and aggregate."""
        try:
            camera_id, agg_summary = self._extract_agg_summary(task_data)
            if camera_id is None:
                return

            self.logger.debug(
                f"[ANALYTICS_FOUND] camera={camera_id} - Processing agg_summary with {len(agg_summary)} frame(s)"
            )

            # Process each frame in agg_summary
            frames_with_tracking = 0
            for frame_id, frame_data in agg_summary.items():
                tracking_stats = frame_data.get("tracking_stats", {})

                if not tracking_stats:
                    self.logger.warning(
                        f"[ANALYTICS_SKIP_FRAME] camera={camera_id}, frame={frame_id} - "
                        f"tracking_stats is empty. frame_data keys: {list(frame_data.keys())}"
                    )
                    continue

                current_counts = self._validated_count_list(
                    tracking_stats.get("current_counts"), "current_counts", camera_id, frame_id
                )
                current_new_counts = self._validated_count_list(
                    tracking_stats.get("current_new_counts"), "current_new_counts", camera_id, frame_id
                )
                total_counts = self._validated_count_list(
                    tracking_stats.get("total_counts"), "total_counts", camera_id, frame_id
                )
                total_current_counts = self._validated_count_list(
                    tracking_stats.get("total_current_counts"), "total_current_counts", camera_id, frame_id
                )
                reset_timestamp = tracking_stats.get("reset_timestamp") or ""

                if not current_counts and not total_counts and not current_new_counts:
                    self.logger.warning(
                        f"[ANALYTICS_SKIP_FRAME] camera={camera_id}, frame={frame_id} - "
                        f"All counts are empty. "
                        f"tracking_stats keys: {list(tracking_stats.keys())}"
                    )
                    continue

                frames_with_tracking += 1
                self.logger.debug(
                    f"[ANALYTICS_AGGREGATING] camera={camera_id}, frame={frame_id} - "
                    f"current_counts={current_counts}, current_new_counts={current_new_counts}, total_counts={total_counts}"
                )

                # Update analytics store
                self._update_analytics_store(
                    camera_id,
                    current_counts,
                    current_new_counts,
                    total_counts,
                    total_current_counts,
                    reset_timestamp,
                )

            if frames_with_tracking == 0:
                self.logger.warning(
                    f"[ANALYTICS_NO_DATA] camera={camera_id} - "
                    f"Processed {len(agg_summary)} frames but none had valid tracking_stats"
                )

        except Exception as e:
            self.logger.error(f"[ANALYTICS_ERROR] Error extracting analytics: {e}", exc_info=True)

    @staticmethod
    def _safe_count(val: Any) -> int:
        """Return count as int; treat None or invalid values as 0 to avoid crashes."""
        if val is None:
            return 0
        try:
            return int(val)
        except (TypeError, ValueError):
            return 0

    def _update_analytics_store(
        self,
        camera_id: str,
        current_counts: List[Dict],
        current_new_counts: List[Dict],
        total_counts: List[Dict],
        total_current_counts: List[Dict],
        reset_timestamp: str,
    ) -> None:
        """Update the analytics store with new counts.

        Aggregation logic:
        - current (from current_counts): retained for compatibility / window bookkeeping
        - current_new (from current_new_counts): SUM/ACCUMULATE - new arrivals only
        - total_current_counts: tracked as latest in-frame occupancy for prev-window carry
        - total (from total_counts): LATEST value - cumulative unique since reset

        All window accumulators are RESET to 0 after publish.
        """
        try:
            # Increment frame counter for this camera
            self._frame_counts[camera_id] += 1
            frame_num = self._frame_counts[camera_id]

            # Log each frame's contribution for debugging (DEBUG level to reduce noise)
            self.logger.debug(
                f"[ANALYTICS_FRAME] camera={camera_id} frame#{frame_num}: "
                f"current_counts={current_counts}, current_new_counts={current_new_counts}, "
                f"total_current_counts={total_current_counts}, total_counts={total_counts}"
            )

            # WARN only if current_new_counts field is MISSING entirely (not just zero)
            # Zero is expected when same people stay in frame - no new arrivals
            has_detections = any(self._safe_count(c.get("count")) > 0 for c in current_counts)
            field_missing = not current_new_counts  # Field is missing/empty list
            if field_missing and has_detections:
                self.logger.warning(
                    f"[ANALYTICS_WARN] camera={camera_id} frame#{frame_num}: current_new_counts field is MISSING "
                    f"but has {sum(self._safe_count(c.get('count')) for c in current_counts)} detections! "
                    f"Tracker may not be providing new counts."
                )

            # Log INFO when new arrivals actually occur (helps diagnose inflated counts)
            for count_item in current_new_counts:
                new_count = self._safe_count(count_item.get("count"))
                if new_count > 0:
                    self.logger.info(
                        f"[NEW_ARRIVAL] camera={camera_id} frame#{frame_num}: "
                        f"category={count_item.get('category')}, new_count={new_count}"
                    )

            # Input validation - check for suspicious values
            for count_item in current_new_counts:
                count = self._safe_count(count_item.get("count"))
                category = count_item.get("category") or "unknown"
                if count < 0:
                    self.logger.error(
                        f"[ANALYTICS_INVALID] camera={camera_id}: negative count={count} for current_new_counts category={category}! "
                        f"This should never happen."
                    )
                elif count > 50:  # Suspiciously high for single frame
                    self.logger.warning(
                        f"[ANALYTICS_SUSPICIOUS] camera={camera_id}: high count={count} for current_new_counts category={category} in single frame. "
                        f"Check if tracker is creating too many new IDs."
                    )

            # Update reset timestamp if changed
            if reset_timestamp and (
                camera_id not in self.reset_timestamps or self.reset_timestamps[camera_id] != reset_timestamp
            ):
                self.reset_timestamps[camera_id] = reset_timestamp
                # Reset analytics for this camera
                self.analytics_store[camera_id] = defaultdict(dict)
                self._frame_counts[camera_id] = 1  # Reset frame counter too
                self.logger.info(f"Reset analytics for camera {camera_id}")

            current_time = time.time()

            # Update current counts - use FIRST value in window as baseline (total at window start)
            # total_current_counts at publish = baseline + sum(current_new_counts)
            # We only set baseline once per window; never overwrite until reset after publish
            for count_item in current_counts:
                category = count_item.get("category")
                count = self._safe_count(count_item.get("count"))

                if not category:
                    continue

                # Initialize or update category data
                if category not in self.analytics_store[camera_id]:
                    self.analytics_store[camera_id][category] = {
                        "current": count,  # BASELINE: first total in scene this window
                        "current_new": 0,  # SUM: new arrivals only
                        "total": 0,  # LATEST: cumulative unique
                        "last_update": current_time,
                    }
                else:
                    # Set baseline only when not yet set (first frame after reset)
                    existing = self.analytics_store[camera_id][category]["current"]
                    if existing == 0:
                        self.analytics_store[camera_id][category]["current"] = count
                    self.analytics_store[camera_id][category]["last_update"] = current_time

            # Update current_new counts - SUM/ACCUMULATE (new arrivals only)
            # This becomes "current_counts" when publishing
            for count_item in current_new_counts:
                category = count_item.get("category")
                count = self._safe_count(count_item.get("count"))

                if not category or count == 0:
                    continue

                if category not in self.analytics_store[camera_id]:
                    self.analytics_store[camera_id][category] = {
                        "current": 0,
                        "current_new": count,  # Start accumulating
                        "total": 0,
                        "last_update": current_time,
                    }
                else:
                    # ACCUMULATE new arrivals (SUM)
                    self.analytics_store[camera_id][category]["current_new"] += count
                    self.analytics_store[camera_id][category]["last_update"] = current_time

            # Track latest in-frame occupancy (total_current_counts); fall back to
            # current_counts for legacy apps that omit the field. Overwrite each
            # frame — this becomes the next window's prev-window carry on publish.
            frame_total_current = total_current_counts or current_counts
            last_frame: Dict[str, int] = {}
            for count_item in frame_total_current:
                category = count_item.get("category")
                count = self._safe_count(count_item.get("count"))
                if not category:
                    continue
                last_frame[category] = count
            if last_frame:
                self._last_frame_current[camera_id] = last_frame

            # Update total counts - use LATEST value (cumulative unique)
            for count_item in total_counts:
                category = count_item.get("category")
                count = self._safe_count(count_item.get("count"))

                if not category:
                    continue

                if category not in self.analytics_store[camera_id]:
                    self.analytics_store[camera_id][category] = {
                        "current": 0,
                        "current_new": 0,
                        "total": count,
                        "last_update": current_time,
                    }
                else:
                    # DETECT TRACKER RESET with hysteresis: Require sustained significant drops
                    # This prevents false positives from normal fluctuations
                    previous_total = self.analytics_store[camera_id][category]["total"]

                    # Check for significant drop (> threshold)
                    is_significant_drop = previous_total > 0 and count < previous_total * self._reset_drop_threshold

                    if is_significant_drop:
                        # Increment consecutive drop counter
                        self._consecutive_drops[camera_id][category] += 1
                        drop_count = self._consecutive_drops[camera_id][category]

                        if drop_count >= self._reset_consecutive_required:
                            # Confirmed reset after sustained drops
                            self.logger.warning(
                                f"[TRACKER_RESET_CONFIRMED] camera={camera_id} category={category}: "
                                f"total decreased from {previous_total} to {count} "
                                f"({drop_count} consecutive drops). "
                                f"Resetting current_new accumulator to prevent inflation."
                            )
                            self.analytics_store[camera_id][category]["current_new"] = 0
                            self.analytics_store[camera_id][category]["current"] = 0
                            # Reset the drop counter after confirmed reset
                            self._consecutive_drops[camera_id][category] = 0
                        else:
                            self.logger.debug(
                                f"[TRACKER_RESET_PENDING] camera={camera_id} category={category}: "
                                f"drop detected ({drop_count}/{self._reset_consecutive_required}), "
                                f"waiting for confirmation"
                            )
                    elif count < previous_total:
                        # Minor drop (not significant) - log but don't track for reset
                        self.logger.debug(
                            f"[TRACKER_MINOR_DROP] camera={camera_id} category={category}: "
                            f"total decreased from {previous_total} to {count} (minor, ignoring)"
                        )
                        # Reset consecutive counter since this isn't a significant drop
                        self._consecutive_drops[camera_id][category] = 0
                    else:
                        # No drop - reset consecutive counter
                        self._consecutive_drops[camera_id][category] = 0

                    # Use LATEST value
                    self.analytics_store[camera_id][category]["total"] = count

            # Log current aggregation state after update
            for category, data in self.analytics_store[camera_id].items():
                self.logger.debug(
                    f"[ANALYTICS_STATE] camera={camera_id} category={category}: "
                    f"current(baseline)={data.get('current', 0)}, "
                    f"current_new(SUM)={data.get('current_new', 0)}, "
                    f"total(LATEST)={data.get('total', 0)}"
                )

            # SANITY CHECK & CORRECTION: current_new should not exceed total
            # If it does, clamp it to prevent publishing invalid data
            for category, data in self.analytics_store[camera_id].items():
                if not isinstance(data, dict):
                    continue
                current_new = self._safe_count(data.get("current_new"))
                total = self._safe_count(data.get("total"))
                if current_new > total:
                    if total == 0 and current_new > 0:
                        # Some use cases (e.g., LPR) don't provide total_counts.
                        # Instead of clamping current_new to 0 (which drops all counts),
                        # auto-correct total to match current_new.
                        self.logger.warning(
                            f"[ANALYTICS_AUTOCORRECT] camera={camera_id} category={category}: "
                            f"current_new({current_new}) but total=0. "
                            f"Auto-setting total=current_new (use case may not track total_counts)."
                        )
                        self.analytics_store[camera_id][category]["total"] = current_new
                    else:
                        self.logger.warning(
                            f"[ANALYTICS_SANITY_FAIL] camera={camera_id} category={category}: "
                            f"current_new({current_new}) > total({total})! "
                            f"This indicates tracker instability. Clamping current_new to total."
                        )
                        # Clamp current_new to total to maintain invariant
                        self.analytics_store[camera_id][category]["current_new"] = total

            self.logger.debug(
                f"Updated analytics store for camera {camera_id}: {len(self.analytics_store[camera_id])} categories"
            )

        except Exception as e:
            self.logger.error(f"Error updating analytics store: {e}", exc_info=True)

    async def _publish_analytics(self) -> None:
        """Publish aggregated analytics to Redis and optionally Kafka."""
        try:
            if not self.analytics_store:
                self.logger.warning(
                    "[ANALYTICS_PUBLISH_SKIP] analytics_store is empty - nothing to publish. "
                    "Check if tracking_stats are being extracted correctly."
                )
                return

            self.logger.info(f"Publishing analytics for {len(self.analytics_store)} camera(s) to results-agg")

            # Publish analytics for each camera
            for camera_id, analytics_data in self.analytics_store.items():
                if not analytics_data:
                    self.logger.debug(f"No analytics data for camera {camera_id}, skipping")
                    continue

                # Log publish summary with frame count
                frame_count = self._frame_counts.get(camera_id, 0)
                self.logger.info(
                    f"[ANALYTICS_PUBLISH] camera={camera_id}: "
                    f"aggregated {frame_count} frames over {self.publish_interval}s window"
                )

                # Log per-category details before publishing
                for category, data in analytics_data.items():
                    if not isinstance(data, dict):
                        continue
                    incoming = self._safe_count(data.get("current_new"))
                    prev_last = self._safe_count(self._prev_window_last_frame_current.get(camera_id, {}).get(category))
                    self.logger.info(
                        f"[ANALYTICS_PUBLISH] camera={camera_id} category={category}: "
                        f"publishing current_counts(new)={incoming}, "
                        f"total_current_counts(prev_last+incoming)={prev_last + incoming}, "
                        f"total_counts={self._safe_count(data.get('total'))}"
                    )

                # Build analytics message
                message = self._build_analytics_message(camera_id, analytics_data)

                if not message:
                    self.logger.warning(f"Failed to build analytics message for camera {camera_id}")
                    continue

                # Publish to Redis (required)
                await self._publish_to_redis(message, camera_id)

                # Publish to Kafka (optional)
                if self.kafka_stream:
                    await self._publish_to_kafka(message, camera_id)

                # Carry last-frame occupancy into the next window, then reset.
                self._prev_window_last_frame_current[camera_id] = dict(self._last_frame_current.get(camera_id, {}))
                self._last_frame_current[camera_id] = {}
                for cat_data in analytics_data.values():
                    if isinstance(cat_data, dict):
                        cat_data["current"] = 0  # Reset total objects in scene
                        cat_data["current_new"] = 0  # Reset new arrivals accumulator

            # Reset frame counts after publish (start fresh for next window)
            self._frame_counts = defaultdict(int)

        except Exception as e:
            self.logger.error(f"Error publishing analytics: {e}", exc_info=True)

    def _build_analytics_message(self, camera_id: str, analytics_data: Dict) -> Optional[Dict[str, Any]]:
        """Build analytics message in expected format.

        Output mapping:
        - current_counts = accumulated current_new (NEW arrivals in this window)
        - total_current_counts = prev window last-frame current + incoming_sum
          (first publish after start: prev carry is 0 → equals current_counts)
        - total_counts = cumulative unique since reset
        """
        try:
            # Get camera config (thread-safe read)
            with self._camera_configs_lock:
                camera_config = self.camera_configs.get(camera_id)
            if not camera_config:
                self.logger.warning(f"No camera config found for {camera_id}")
                return None

            # Extract camera info from stream_config. Accept BOTH forms of the
            # camera config: a CameraConfig-like object (.stream_config attribute,
            # what the SDK passed) and an engine dict ({"stream_config": {...}},
            # what ml-codebases deploy.py passes). Previously only the object form
            # was read, so the engine-dict form silently fell back to {} and lost
            # all camera metadata.
            if hasattr(camera_config, "stream_config"):
                stream_config = camera_config.stream_config or {}
            elif isinstance(camera_config, dict):
                stream_config = camera_config.get("stream_config", {}) or {}
            else:
                stream_config = {}

            # Log stream config for debugging
            self.logger.debug(
                f"Building analytics for camera {camera_id}: "
                f"stream_type={stream_config.get('stream_type', 'MISSING')}, "
                f"config_keys={list(stream_config.keys())}"
            )

            # Camera metadata from stream_config (mirrors the worker's stream_info
            # mapping in workers.py); fall back to stable defaults / camera_id.
            camera_name = stream_config.get("camera_name") or camera_id
            camera_group = stream_config.get("camera_group") or "default_group"
            location = stream_config.get("location") or "Unknown Location"
            location_id = stream_config.get("location_id") or stream_config.get("locationId") or ""

            # Build output counts from store
            current_counts = []  # NEW arrivals in this window (from current_new - ACCUMULATED)
            total_current_counts = []  # prev last-frame occupancy + new arrivals
            total_counts = []  # Cumulative unique since reset (from total - LATEST)
            prev_carry = self._prev_window_last_frame_current.get(camera_id, {})

            for category, data in analytics_data.items():
                if not isinstance(data, dict):
                    continue
                # current_new = accumulated NEW arrivals in window (incoming_sum); fallback 0 if missing
                new_arrivals = self._safe_count(data.get("current_new"))
                prev_last = self._safe_count(prev_carry.get(category))
                # total = cumulative unique; fallback 0 if missing
                cumulative_total = self._safe_count(data.get("total"))

                # current_counts = NEW arrivals (accumulated current_new_counts)
                current_counts.append({"category": category, "count": new_arrivals})

                # total_current_counts = prev window last-frame + this window's new
                total_current_counts.append({"category": category, "count": prev_last + new_arrivals})

                # total_counts = cumulative unique since reset
                total_counts.append({"category": category, "count": cumulative_total})

            # Get timestamps.
            # input_timestamp is RFC3339/ISO-8601 UTC so the zone-keyed be-inference-tracker
            # consumer parses it as the event time (Go time.Parse(time.RFC3339, ...)); a time-only
            # string fails that parse and the consumer silently falls back to ingest time.
            current_time = datetime.now(timezone.utc)
            input_timestamp = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")  # RFC3339, e.g. 2026-06-14T06:30:00Z
            reset_timestamp = self.reset_timestamps.get(camera_id, "00:00:00")

            # Per-zone tracking stats keyed by zone id.
            # - current_counts: NEW arrivals in this window (accumulated)
            # - total_current_counts: prev last-frame + incoming_sum
            # - total_counts: Cumulative unique since reset
            zone_stats = {
                "input_timestamp": input_timestamp,
                "reset_timestamp": reset_timestamp,
                "current_counts": current_counts,
                "total_current_counts": total_current_counts,
                "total_counts": total_counts,
            }
            # The old post-processing flow is not zone-aware, so everything goes under a single
            # "global" zone. This matches the AnalyticsEngine convention (no-polygon case) and the
            # zone-keyed results-agg contract required by be-inference-tracker's
            # mappers.ParseKafkaAnalyticsMessageFromJSON (tracking_stats = {zone_id: {stats}}).
            tracking_stats = {self.ANALYTICS_ZONE_GLOBAL: zone_stats}

            # Build complete message
            message = {
                "camera_name": camera_name,
                "inferencePipelineId": self.inference_pipeline_id or "",
                "camera_id": camera_id,
                "app_deployment_id": self.app_deployment_id or "",
                "deployment_instance_id": self.deployment_instance_id or "",
                "app_id": self.app_id or "",
                "camera_group": camera_group,
                "locationId": location_id,
                "location": location,
                "application_name": self.app_name,
                "application_key_name": self.app_name.lower().replace(" ", "_") if self.app_name else "unknown_app",
                "application_version": self.app_version,
                "tracking_stats": tracking_stats,
            }

            self.logger.debug(
                f"Built analytics message for camera {camera_id}: "
                f"current(new)={current_counts}, total_current={total_current_counts}, total={total_counts}"
            )

            return message

        except Exception as e:
            self.logger.error(f"Error building analytics message for {camera_id}: {e}", exc_info=True)
            return None

    async def _publish_to_redis(self, message: Dict[str, Any], camera_id: str) -> None:
        """Publish analytics message to Redis stream."""
        try:
            if not self.redis_stream:
                self.logger.warning("Redis stream not initialized, skipping publish")
                return

            message_json = json.dumps(message)
            await self.redis_stream.async_add_message(self.ANALYTICS_TOPIC, message_json, key=camera_id)

            # Log at info level so we can see when data is being published
            # (tracking_stats is zone-keyed; read the global zone for the summary line)
            tracking_stats = message.get("tracking_stats", {})
            zone_stats = tracking_stats.get(self.ANALYTICS_ZONE_GLOBAL, {})
            current_counts = zone_stats.get("current_counts", [])
            total_counts = zone_stats.get("total_counts", [])
            self.logger.info(
                f"Published analytics to Redis '{self.ANALYTICS_TOPIC}' for camera {camera_id}: "
                f"current={current_counts}, total={total_counts}"
            )

        except Exception as e:
            self.logger.error(f"Error publishing to Redis for {camera_id}: {e}", exc_info=True)

    async def _publish_to_kafka(self, message: Dict[str, Any], camera_id: str) -> None:
        """Publish analytics message to Kafka stream."""
        try:
            if not self.kafka_stream:
                self.logger.warning("Kafka stream not initialized, skipping publish")
                return

            message_json = json.dumps(message)
            await self.kafka_stream.async_add_message(self.ANALYTICS_TOPIC, message_json, key=camera_id)

            self.logger.debug(f"Published analytics to Kafka for camera {camera_id}")

        except Exception as e:
            self.logger.error(f"Error publishing to Kafka for {camera_id}: {e}", exc_info=True)

    def _cleanup_resources(self, loop: asyncio.AbstractEventLoop) -> None:
        """Clean up stream connections and event loop."""
        # Close Redis stream
        if self.redis_stream:
            try:
                loop.run_until_complete(self.redis_stream.async_close())
                self.logger.info("Closed Redis analytics stream")
            except Exception as e:
                self.logger.error(f"Error closing Redis stream: {e}")

        # Close Kafka stream
        if self.kafka_stream:
            try:
                loop.run_until_complete(self.kafka_stream.async_close())
                self.logger.info("Closed Kafka analytics stream")
            except Exception as e:
                self.logger.error(f"Error closing Kafka stream: {e}")

        # Close event loop
        try:
            loop.close()
        except Exception as e:
            self.logger.error(f"Error closing event loop: {e}")

        self.logger.info("Analytics Publisher stopped")

    def get_metrics(self) -> Dict[str, Any]:
        """Get analytics publisher metrics."""
        metrics = {
            "running": self.running,
            "cameras_tracked": len(self.analytics_store),
            "aggregation_interval_sec": self.aggregation_interval,
            "publish_interval_sec": self.publish_interval,
            "queue_size": self.analytics_queue.qsize(),
            "queue_maxsize": self.analytics_queue.maxsize,
            # Cumulative analytics records lost at enqueue because the queue was
            # full. Non-zero means the publisher could not keep up and analytics
            # data (including alert-bearing records) was silently discarded.
            "dropped_messages": self._dropped_messages,
            "streams": {
                "redis": {
                    "enabled": True,
                    "connected": self.redis_stream is not None,
                    "host": f"{self.redis_host}:{self.redis_port}",
                },
                "kafka": {
                    "enabled": self.enable_kafka,
                    "connected": self.kafka_stream is not None,
                },
            },
            "camera_analytics": {},
        }

        # Add per-camera metrics with actual count data
        for camera_id, analytics_data in self.analytics_store.items():
            camera_metrics = {
                "categories_tracked": len(analytics_data),
                "categories": list(analytics_data.keys()),
                "counts": {},
            }
            for category, data in analytics_data.items():
                camera_metrics["counts"][category] = {
                    "current": data.get("current", 0),
                    "total": data.get("total", 0),
                }
            metrics["camera_analytics"][camera_id] = camera_metrics

        return metrics
