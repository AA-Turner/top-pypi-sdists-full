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
from typing import Any, Dict, List, Optional

from matrice_common.stream.matrice_stream import MatriceStream, StreamType


class AnalyticsPublisher:
    """
    Publishes aggregated analytics to Redis (localhost) and Kafka internal streams.
    
    Monitors output queue and aggregates tracking statistics over 5-minute windows.
    Publishes to 'results-agg' topic on both Redis and Kafka.
    
    Output structure:
        tracking_stats: {
            "current_counts": [{"category": "person", "count": 2}],         # NEW people in this publish window (delta)
            "total_current_counts": [{"category": "person", "count": 7}],   # ALL people in frame right now
            "total_counts": [{"category": "person", "count": 15}]           # Cumulative unique since reset
        }
    """

    DEFAULT_AGGREGATION_INTERVAL = 300  # 5 minutes in seconds
    DEFAULT_PUBLISH_INTERVAL = 60  # Publish every 60 seconds
    ANALYTICS_TOPIC = "results-agg"

    def __init__(
        self,
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
        kafka_bootstrap_servers: Optional[str] = None,
        enable_kafka: bool = False,
    ):
        self.camera_configs = camera_configs
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

        # Hysteresis tracking for reset detection (prevents false positives from fluctuations)
        # Structure: {camera_id: {category: consecutive_drop_count}}
        self._consecutive_drops: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self._reset_drop_threshold = 0.5  # 50% drop triggers potential reset
        self._reset_consecutive_required = 3  # Require 3 consecutive drops to confirm reset

        # Internal queue for receiving analytics data from producer
        self.analytics_queue: queue.Queue = queue.Queue(maxsize=1000)
        
        # Stream connections
        self.redis_stream: Optional[MatriceStream] = None
        self.kafka_stream: Optional[MatriceStream] = None

    def start(self) -> threading.Thread:
        """Start the analytics publisher in a separate thread."""
        self.running = True
        thread = threading.Thread(
            target=self._run,
            name="AnalyticsPublisher",
            daemon=False
        )
        thread.start()
        self.logger.info("Started Analytics Publisher")
        return thread

    def stop(self):
        """Stop the analytics publisher."""
        self.running = False
        self.logger.info("Stopping Analytics Publisher")

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
            self.redis_stream = MatriceStream(
                StreamType.REDIS,
                host=self.redis_host,
                port=self.redis_port,
                password=self.redis_password,
                username=self.redis_username,
                db=self.redis_db,
                enable_batching=False,  # Disable batching for real-time analytics
                pool_max_connections=10,  # Lower pool size for analytics
            )
            await self.redis_stream.async_setup(self.ANALYTICS_TOPIC)
            self.logger.info(f"Initialized Redis stream for analytics on {self.redis_host}:{self.redis_port} (batching disabled)")
        except Exception as e:
            self.logger.error(f"Failed to initialize Redis analytics stream: {e}", exc_info=True)
            self.redis_stream = None  # degrade gracefully instead of crash

        # Initialize Kafka stream (optional)
        if self.enable_kafka and self.kafka_bootstrap_servers:
            try:
                self.kafka_stream = MatriceStream(
                    StreamType.KAFKA,
                    bootstrap_servers=self.kafka_bootstrap_servers,
                    sasl_username=os.environ.get("KAFKA_SASL_USERNAME"),
                    sasl_password=os.environ.get("KAFKA_SASL_PASSWORD"),
                    sasl_mechanism="SCRAM-SHA-256",
                    security_protocol="SASL_PLAINTEXT"
                )
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
                # Lazy retry: if redis_stream is None, re-check env var every 30s
                current_time = time.time()
                if self.redis_stream is None and current_time - last_redis_retry > 30:
                    last_redis_retry = current_time
                    pw = os.environ.get("REDIS_PASSWORD") or self.redis_password
                    if pw:
                        self.redis_password = pw
                        self.logger.info("Redis password now available, attempting connection...")
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
                    time.sleep(0.01)  # Messages processed, check again quickly

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
            # Drop message if queue is full (analytics is non-critical)
            self.logger.warning("Analytics queue full, dropping message")
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

    def _extract_and_aggregate_analytics(self, task_data: Dict[str, Any]) -> None:
        """Extract tracking stats from task data and aggregate."""
        try:
            camera_id = task_data.get("camera_id")
            if not camera_id:
                self.logger.warning(
                    "[ANALYTICS_SKIP] No camera_id in task_data. "
                    f"Available keys: {list(task_data.keys())}"
                )
                return

            data = task_data.get("data", {})
            if not data:
                self.logger.warning(
                    f"[ANALYTICS_SKIP] camera={camera_id} - 'data' field is empty or missing. "
                    f"task_data keys: {list(task_data.keys())}"
                )
                return

            post_processing_result = data.get("post_processing_result", {})
            if not post_processing_result:
                self.logger.warning(
                    f"[ANALYTICS_SKIP] camera={camera_id} - 'post_processing_result' is empty or missing. "
                    f"data keys: {list(data.keys())}"
                )
                return

            # Check for agg_summary at top level (current format after flattening)
            # or nested in data field (legacy format for backward compatibility)
            agg_summary = post_processing_result.get("agg_summary")
            if agg_summary is None and "data" in post_processing_result:
                # Legacy format: agg_summary nested in data field
                agg_summary = post_processing_result.get("data", {}).get("agg_summary")
                if agg_summary:
                    self.logger.debug(f"Found agg_summary in legacy nested format for camera {camera_id}")

            # Skip if no agg_summary found
            if not agg_summary or not isinstance(agg_summary, dict):
                self.logger.warning(
                    f"[ANALYTICS_SKIP] camera={camera_id} - No valid agg_summary. "
                    f"post_processing_result keys: {list(post_processing_result.keys()) if post_processing_result else 'empty'}. "
                    f"Expected 'agg_summary' dict but got: {type(agg_summary).__name__}"
                )
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

                # Extract counts from tracking_stats (fallback to [] if missing/null to avoid crashes)
                # - current_counts: TOTAL objects in scene (existing + new)
                # - current_new_counts: NEW arrivals only in this frame
                # - total_counts: Cumulative unique since reset
                if "current_counts" not in tracking_stats or tracking_stats.get("current_counts") is None:
                    self.logger.debug(
                        f"[ANALYTICS_MISSING] camera={camera_id}, frame={frame_id}: "
                        "current_counts missing or null from app, assuming []"
                    )
                if "current_new_counts" not in tracking_stats or tracking_stats.get("current_new_counts") is None:
                    self.logger.debug(
                        f"[ANALYTICS_MISSING] camera={camera_id}, frame={frame_id}: "
                        "current_new_counts missing or null from app, assuming []"
                    )
                if "total_counts" not in tracking_stats or tracking_stats.get("total_counts") is None:
                    self.logger.debug(
                        f"[ANALYTICS_MISSING] camera={camera_id}, frame={frame_id}: "
                        "total_counts missing or null from app, assuming []"
                    )
                current_counts = tracking_stats.get("current_counts") or []
                current_new_counts = tracking_stats.get("current_new_counts") or []
                total_counts = tracking_stats.get("total_counts") or []
                if not isinstance(current_counts, list):
                    self.logger.debug(f"[ANALYTICS_MISSING] camera={camera_id}, frame={frame_id}: current_counts not a list, assuming []")
                    current_counts = []
                if not isinstance(current_new_counts, list):
                    self.logger.debug(f"[ANALYTICS_MISSING] camera={camera_id}, frame={frame_id}: current_new_counts not a list, assuming []")
                    current_new_counts = []
                if not isinstance(total_counts, list):
                    self.logger.debug(f"[ANALYTICS_MISSING] camera={camera_id}, frame={frame_id}: total_counts not a list, assuming []")
                    total_counts = []
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
                    reset_timestamp
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
        reset_timestamp: str
    ) -> None:
        """Update the analytics store with new counts.

        Aggregation logic:
        - current (from current_counts): BASELINE - first total in scene at window start
        - current_new (from current_new_counts): SUM/ACCUMULATE - new arrivals only
        - total (from total_counts): LATEST value - cumulative unique since reset

        All values are RESET to 0 after publish.
        """
        try:
            # Increment frame counter for this camera
            self._frame_counts[camera_id] += 1
            frame_num = self._frame_counts[camera_id]

            # Log each frame's contribution for debugging (DEBUG level to reduce noise)
            self.logger.debug(
                f"[ANALYTICS_FRAME] camera={camera_id} frame#{frame_num}: "
                f"current_counts={current_counts}, current_new_counts={current_new_counts}, total_counts={total_counts}"
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
            if reset_timestamp and (camera_id not in self.reset_timestamps or
                                   self.reset_timestamps[camera_id] != reset_timestamp):
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
                        "current": count,      # BASELINE: first total in scene this window
                        "current_new": 0,      # SUM: new arrivals only
                        "total": 0,            # LATEST: cumulative unique
                        "last_update": current_time
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
                        "last_update": current_time
                    }
                else:
                    # ACCUMULATE new arrivals (SUM)
                    self.analytics_store[camera_id][category]["current_new"] += count
                    self.analytics_store[camera_id][category]["last_update"] = current_time
            
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
                        "last_update": current_time
                    }
                else:
                    # DETECT TRACKER RESET with hysteresis: Require sustained significant drops
                    # This prevents false positives from normal fluctuations
                    previous_total = self.analytics_store[camera_id][category]["total"]

                    # Check for significant drop (> threshold)
                    is_significant_drop = (
                        previous_total > 0 and
                        count < previous_total * self._reset_drop_threshold
                    )

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
                        self.logger.warning(
                            f"[ANALYTICS_SANITY_FAIL] camera={camera_id} category={category}: "
                            f"current_new({current_new}) but total=0! "
                            f"This indicates total_counts is not being sent correctly from post-processing. "
                            f"Clamping current_new to 0."
                        )
                        # Clamp to 0 since total is 0
                        self.analytics_store[camera_id][category]["current_new"] = 0
                    else:
                        self.logger.warning(
                            f"[ANALYTICS_SANITY_FAIL] camera={camera_id} category={category}: "
                            f"current_new({current_new}) > total({total})! "
                            f"This indicates tracker instability. Clamping current_new to total."
                        )
                        # Clamp current_new to total to maintain invariant
                        self.analytics_store[camera_id][category]["current_new"] = total

            self.logger.debug(
                f"Updated analytics store for camera {camera_id}: "
                f"{len(self.analytics_store[camera_id])} categories"
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

            self.logger.info(
                f"Publishing analytics for {len(self.analytics_store)} camera(s) to results-agg"
            )

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
                    baseline = self._safe_count(data.get("current"))
                    incoming = self._safe_count(data.get("current_new"))
                    self.logger.info(
                        f"[ANALYTICS_PUBLISH] camera={camera_id} category={category}: "
                        f"publishing current_counts(new)={incoming}, "
                        f"total_current_counts(baseline+incoming)={baseline + incoming}, "
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

                # RESET current and current_new to 0 after successful publish
                # This ensures next aggregation window starts fresh
                for cat_data in analytics_data.values():
                    if isinstance(cat_data, dict):
                        cat_data["current"] = 0       # Reset total objects in scene
                        cat_data["current_new"] = 0   # Reset new arrivals accumulator

            # Reset frame counts after publish (start fresh for next window)
            self._frame_counts = defaultdict(int)

        except Exception as e:
            self.logger.error(f"Error publishing analytics: {e}", exc_info=True)

    def _build_analytics_message(self, camera_id: str, analytics_data: Dict) -> Optional[Dict[str, Any]]:
        """Build analytics message in expected format.
        
        Output mapping:
        - current_counts = accumulated current_new (NEW arrivals in this window)
        - total_current_counts = baseline + incoming_sum (unique present in window)
        - total_counts = cumulative unique since reset
        """
        try:
            # Get camera config
            camera_config = self.camera_configs.get(camera_id)
            if not camera_config:
                self.logger.warning(f"No camera config found for {camera_id}")
                return None
            
            # Extract camera info from stream_config
            stream_config = camera_config.stream_config if hasattr(camera_config, 'stream_config') else {}
            
            # Log stream config for debugging
            self.logger.debug(
                f"Building analytics for camera {camera_id}: "
                f"stream_type={stream_config.get('stream_type', 'MISSING')}, "
                f"config_keys={list(stream_config.keys())}"
            )
            
            # Get camera metadata (try to extract from various sources)
            camera_name = camera_id  # Default to camera_id
            camera_group = "default_group"
            location = "Unknown Location"
            location_id = ""
            
            # Try to get from camera config
            if hasattr(camera_config, 'camera_id'):
                camera_name = getattr(camera_config, 'camera_id', camera_id)
            
            # Build output counts from store
            current_counts = []       # NEW arrivals in this window (from current_new - ACCUMULATED)
            total_current_counts = [] # ALL objects in scene (from current - LATEST)
            total_counts = []         # Cumulative unique since reset (from total - LATEST)

            for category, data in analytics_data.items():
                if not isinstance(data, dict):
                    continue
                # current_new = accumulated NEW arrivals in window (incoming_sum); fallback 0 if missing
                new_arrivals = self._safe_count(data.get("current_new"))
                # current = baseline (first total in scene at window start); fallback 0 if missing
                baseline = self._safe_count(data.get("current"))
                # unique_present = baseline + incoming_sum
                unique_present_in_window = baseline + new_arrivals
                # total = cumulative unique; fallback 0 if missing
                cumulative_total = self._safe_count(data.get("total"))
                
                # current_counts = NEW arrivals (accumulated current_new_counts)
                current_counts.append({
                    "category": category,
                    "count": new_arrivals
                })
                
                # total_current_counts = unique present in window (baseline + incoming_sum)
                total_current_counts.append({
                    "category": category,
                    "count": unique_present_in_window
                })

                # total_counts = cumulative unique since reset
                total_counts.append({
                    "category": category,
                    "count": cumulative_total
                })
            
            # Get timestamps
            current_time = datetime.now(timezone.utc)
            input_timestamp = current_time.strftime("%H:%M:%S.%f")[:-5]  # Format: HH:MM:SS.d
            reset_timestamp = self.reset_timestamps.get(camera_id, "00:00:00")
            
            # Build tracking_stats with correct key names
            # - current_counts: NEW arrivals in this window (accumulated)
            # - total_current_counts: unique present in window (baseline + incoming_sum)
            # - total_counts: Cumulative unique since reset
            tracking_stats = {
                "input_timestamp": input_timestamp,
                "reset_timestamp": reset_timestamp,
                "current_counts": current_counts,
                "total_current_counts": total_current_counts,
                "total_counts": total_counts
            }
            
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
                "tracking_stats": tracking_stats
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
            await self.redis_stream.async_add_message(
                self.ANALYTICS_TOPIC,
                message_json,
                key=camera_id
            )

            # Log at info level so we can see when data is being published
            tracking_stats = message.get("tracking_stats", {})
            current_counts = tracking_stats.get("current_counts", [])
            total_counts = tracking_stats.get("total_counts", [])
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
            await self.kafka_stream.async_add_message(
                self.ANALYTICS_TOPIC,
                message_json,
                key=camera_id
            )
            
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
            "streams": {
                "redis": {
                    "enabled": True,
                    "connected": self.redis_stream is not None,
                    "host": f"{self.redis_host}:{self.redis_port}"
                },
                "kafka": {
                    "enabled": self.enable_kafka,
                    "connected": self.kafka_stream is not None
                }
            },
            "camera_analytics": {}
        }

        # Add per-camera metrics with actual count data
        for camera_id, analytics_data in self.analytics_store.items():
            camera_metrics = {
                "categories_tracked": len(analytics_data),
                "categories": list(analytics_data.keys()),
                "counts": {}
            }
            for category, data in analytics_data.items():
                camera_metrics["counts"][category] = {
                    "current": data.get("current", 0),
                    "total": data.get("total", 0)
                }
            metrics["camera_analytics"][camera_id] = camera_metrics

        return metrics
