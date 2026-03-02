import logging
import time
import threading
from typing import Dict, Optional, List, Tuple
from queue import Empty, PriorityQueue, Full
from matrice_common.session import Session
from matrice_common.stream.kafka_stream import MatriceKafkaDeployment
import itertools



class ResultsIngestor:
    """
    Streams and manages results from multiple deployments.
    Handles result collection, queuing, and distribution with enhanced structure consistency.
    """

    def __init__(
        self, deployment_ids: List[str], session: Session, consumer_timeout: float = 300, action_id: str = ""
    ):
        """
        Initialize the results streamer.

        Args:
            deployment_ids: List of deployment IDs
            session: Session object for authentication
            consumer_timeout: Timeout for consuming results from deployments
        """
        self.deployment_ids = deployment_ids
        self.session = session
        self.deployments_stream_utils: Dict[str, MatriceKafkaDeployment] = {}
        for deployment_id in self.deployment_ids:
            self.deployments_stream_utils[deployment_id] = MatriceKafkaDeployment(
                self.session,
                deployment_id,
                type="client",
                consumer_group_id=f"aggregator-{deployment_id}",
                consumer_group_instance_id=f"aggregator-{deployment_id}-{action_id}",
            )

        self.consumer_timeout = consumer_timeout

        # Result queues for each deployment (now using PriorityQueue)
        self.results_queues: Dict[str, PriorityQueue] = {}

        # Streaming threads
        self.results_streaming_threads: Dict[str, threading.Thread] = {}

        # Control flags
        self._stop_streaming = threading.Event()
        self._is_streaming = False
        self._lock = threading.Lock()  # Main state lock
        self._stats_lock = threading.Lock()  # Separate lock for better performance

        # Counter for ordering within (deployment_id, stream_key, stream_group_key)
        self._counters: Dict[Tuple[str, str, str], itertools.count] = {}
        # Global per-deployment sequence for PriorityQueue tie-breaking across streams
        self._queue_seq_counters: Dict[str, itertools.count] = {}

        # Track last seen input_order for reset detection
        self._last_input_order: Dict[Tuple[str, str], int] = {}

        # Track session/epoch for each (deployment_id, stream_key) to handle resets
        self._session_counters: Dict[Tuple[str, str], int] = {}

        # Statistics
        self.stats = {
            "results_consumed": 0,
            "results_processed": 0,
            "errors": 0,
            "last_error": None,
            "last_error_time": None,
            "queue_sizes": {},
            "start_time": None,
            "consumer_timeout": consumer_timeout,
        }

        # Initialize queues
        self._initialize_queues()

    def _initialize_queues(self):
        """Initialize result priority queues for each deployment."""
        for deployment_id in self.deployment_ids:
            self.results_queues[deployment_id] = PriorityQueue()
            self.stats["queue_sizes"][deployment_id] = 0
            # Initialize per-deployment sequence counter
            self._queue_seq_counters[deployment_id] = itertools.count()

    def start_streaming(self) -> bool:
        """
        Start streaming results from all deployments.

        Returns:
            bool: True if streaming started successfully, False otherwise
        """
        with self._lock:
            if self._is_streaming:
                logging.warning("Results streaming is already running")
                return True

            self._stop_streaming.clear()
            self._is_streaming = True
            self.stats["start_time"] = time.time()

        try:
            # Start result streaming threads for each deployment
            for deployment_id in self.deployment_ids:
                thread = threading.Thread(
                    target=self._stream_results_to_queue,
                    args=(deployment_id, self.results_queues[deployment_id]),
                    name=f"ResultStreamer-{deployment_id}",
                    daemon=True,
                )
                thread.start()
                self.results_streaming_threads[deployment_id] = thread
                logging.info(
                    f"Started result streaming for deployment: {deployment_id}"
                )

            logging.info(
                f"Started results streaming for {len(self.deployment_ids)} deployments"
            )
            return True

        except Exception as exc:
            logging.error(f"Failed to start results streaming: {exc}")
            self.stop_streaming()
            return False

    def stop_streaming(self):
        """Stop all streaming operations."""
        with self._lock:
            if not self._is_streaming:
                logging.info("Results streaming is not running")
                return

            self._is_streaming = False
            self._stop_streaming.set()

        logging.info("Stopping results streaming...")

        # Stop deployment streaming
        for deployment_id in self.deployment_ids:
            try:
                for stream_utils in self.deployments_stream_utils.values():
                    stream_utils.sync_kafka.close()
            except Exception as exc:
                logging.error(
                    f"Error stopping streaming for deployment {deployment_id}: {exc}"
                )

        # Wait for streaming threads to complete
        for deployment_id, thread in self.results_streaming_threads.items():
            try:
                if thread.is_alive():
                    thread.join(timeout=5.0)
                    if thread.is_alive():
                        logging.warning(
                            f"Result streaming thread for {deployment_id} did not stop gracefully"
                        )
            except Exception as exc:
                logging.error(
                    f"Error joining thread for deployment {deployment_id}: {exc}"
                )

        # Clear threads
        self.results_streaming_threads.clear()

        logging.info("Results streaming stopped")

    def _get_priority_counter(self, deployment_id: str, stream_key: str, stream_group_key: str) -> int:
        """
        Get a monotonically increasing counter per (deployment_id, stream_key, stream_group_key) for ordering.
        
        Returns:
            int: Priority counter for ordering within the same stream
        """
        key = (deployment_id, stream_key, stream_group_key)

        # Initialize counters if needed
        if key not in self._counters:
            self._counters[key] = itertools.count()

        return next(self._counters[key])

    def _get_queue_sequence(self, deployment_id: str) -> int:
        """
        Get a global per-deployment sequence number for tie-breaking across different streams
        placed in the same PriorityQueue. This prevents Python from trying to compare dicts
        when primary priorities are equal.
        """
        if deployment_id not in self._queue_seq_counters:
            self._queue_seq_counters[deployment_id] = itertools.count()
        return next(self._queue_seq_counters[deployment_id])

    def _stream_results_to_queue(
        self, deployment_id: str, results_queue: PriorityQueue
    ):
        """
        Stream results from a deployment to its result queue.

        Args:
            deployment_id: ID of the deployment
            results_queue: Priority queue to store results ordered by input_order
        """
        logging.info(f"Starting result streaming for deployment: {deployment_id}")

        while not self._stop_streaming.is_set():
            try:
                # Consume result with timeout
                result = self.deployments_stream_utils[deployment_id].consume_message(
                    self.consumer_timeout
                )

                if result is not None:
                    # Handle the structured response format from stream_worker.py
                    result_value = result.get("value", {})
                    input_streams = result_value.get("input_streams", [])
                    # Handle both input_stream if key in dict and input_data if key is not in dict
                    input_data = input_streams[0] if input_streams else {}
                    input_stream = input_data.get("input_stream", input_data)
                    # input_order = input_stream.get("input_order")
                    camera_info = input_stream.get("camera_info") or {}
                    stream_key = camera_info.get("camera_name")
                    stream_group_key = camera_info.get("camera_group") or "default_group"

                    if not stream_key:
                        logging.warning(
                            f"Missing stream_key for deployment {deployment_id}, skipping result. "
                            f"Stream key: {stream_key}, Stream group: {stream_group_key}"
                        )
                        continue

                    order = self._get_priority_counter(deployment_id, stream_key, stream_group_key)
                    seq = self._get_queue_sequence(deployment_id)
                    # Create enhanced result object with the structured response
                    enhanced_result = {
                        "deployment_id": deployment_id,
                        "stream_key": stream_key,
                        "stream_group_key": stream_group_key,
                        "input_order": order,
                        "timestamp": time.time(),
                        "result": result_value, # TODO: check if should send this or just agg_summary
                    }

                    try:
                        # Include a sequence tie-breaker to avoid comparing dicts when priorities are equal
                        results_queue.put((order, seq, enhanced_result), block=False)

                        with self._stats_lock:
                            self.stats["results_consumed"] += 1
                            self.stats["queue_sizes"][deployment_id] = results_queue.qsize()

                    except Full:
                        # Queue is full - reduce logging frequency for performance
                        with self._stats_lock:
                            self.stats["errors"] += 1
                            self.stats["last_error"] = "Queue full"
                            self.stats["last_error_time"] = time.time()
                            # Only log every 10th queue full error
                            if self.stats["errors"] % 10 == 1:
                                logging.warning(f"Result queue full for deployment {deployment_id}, dropping result (#{self.stats['errors']})")
                    except Exception as exc:
                        # Other enqueue errors
                        with self._stats_lock:
                            self.stats["errors"] += 1
                            self.stats["last_error"] = str(exc)
                            self.stats["last_error_time"] = time.time()
                            # Only log every 10th enqueue error
                            if self.stats["errors"] % 10 == 1:
                                logging.error(f"Failed to enqueue result for deployment {deployment_id}: {exc} (#{self.stats['errors']})")

            except Exception as exc:
                if not self._stop_streaming.is_set():
                    with self._stats_lock:
                        self.stats["errors"] += 1
                        self.stats["last_error"] = str(exc)
                        self.stats["last_error_time"] = time.time()
                        # Reduce logging frequency for performance
                        if self.stats["errors"] % 10 == 1:
                            logging.error(f"Error streaming results for deployment {deployment_id}: {exc} (#{self.stats['errors']})", exc_info=True)

                    # Add small delay to prevent tight error loops
                    time.sleep(0.1)

        logging.info(f"Stopped result streaming for deployment: {deployment_id}")

    def get_results(self, deployment_id: str, timeout: float = 1.0) -> Optional[Dict]:
        """
        Get a result from a specific deployment's priority queue.

        Args:
            deployment_id: ID of the deployment
            timeout: Timeout for getting the result

        Returns:
            Dict: Result dictionary or None if timeout/no result
        """
        if deployment_id not in self.results_queues:
            logging.error(f"No queue found for deployment: {deployment_id}")
            return None

        try:
            priority_result = self.results_queues[deployment_id].get(timeout=timeout)
            self.results_queues[deployment_id].task_done()

            with self._stats_lock:
                self.stats["queue_sizes"][deployment_id] = self.results_queues[deployment_id].qsize()

            # Handle both 2-tuple (legacy) and 3-tuple (with seq) queue items
            if isinstance(priority_result, tuple):
                if len(priority_result) >= 3:
                    return priority_result[2]
                elif len(priority_result) == 2:
                    return priority_result[1]
            return priority_result
        except Empty:
            return None
        except Exception as exc:
            logging.error(
                f"Error getting result from deployment {deployment_id}: {exc}"
            )
            return None

    def get_all_results(self, timeout: float = 1.0) -> List[Dict]:
        """
        Get results from all deployment queues.

        Args:
            timeout: Timeout for getting results

        Returns:
            List[Dict]: List of result dictionaries
        """
        results = []

        for deployment_id in self.results_queues.keys():
            result = self.get_results(deployment_id, timeout=timeout)
            if result:
                results.append(result)

        return results

    def get_stats(self) -> Dict:
        """Get current statistics."""
        with self._stats_lock:
            stats = self.stats.copy()

        # Add runtime statistics
        if stats["start_time"]:
            stats["runtime_seconds"] = time.time() - stats["start_time"]

        # Add queue statistics
        total_queue_size = sum(stats["queue_sizes"].values())
        stats["total_queue_size"] = total_queue_size

        return stats

    def get_health_status(self) -> Dict:
        """Get health status of the results streamer."""
        health = {
            "status": "healthy",
            "is_streaming": self._is_streaming,
            "deployments": len(self.deployment_ids),
            "active_threads": len(
                [t for t in self.results_streaming_threads.values() if t.is_alive()]
            ),
            "queue_sizes": {},
            "errors": self.stats["errors"],
        }

        # Check queue sizes
        total_queue_size = 0
        for deployment_id, queue in self.results_queues.items():
            queue_size = queue.qsize()
            health["queue_sizes"][deployment_id] = queue_size
            total_queue_size += queue_size

            # Mark as degraded if queue is getting full
            if queue_size > 1000:
                health["status"] = "degraded"
                health["reason"] = f"Queue for {deployment_id} nearly full ({queue_size})"
                logging.warning(f"Ingestor degraded: {deployment_id} queue has {queue_size} items")

        # Check for recent errors (within last 60 seconds)
        if (
            self.stats["last_error_time"]
            and (time.time() - self.stats["last_error_time"]) < 60
        ):
            health["status"] = "degraded"
            health["reason"] = f"Recent error: {self.stats['last_error']}"
            logging.warning(f"Ingestor degraded due to recent error: {self.stats['last_error']}")

        # Check if threads are running when they should be
        if self._is_streaming:
            dead_threads = []
            for deployment_id, thread in self.results_streaming_threads.items():
                if not thread.is_alive():
                    dead_threads.append(deployment_id)

            if dead_threads:
                health["status"] = "degraded" 
                health["reason"] = f"Dead threads for deployments: {', '.join(dead_threads)}"
                logging.warning(f"Ingestor degraded: dead threads for {len(dead_threads)} deployments: {', '.join(dead_threads)}")

        # Check if not streaming when it should be
        if not self._is_streaming:
            health["status"] = "unhealthy"
            health["reason"] = "Ingestor is not streaming"
            logging.error("Ingestor is not streaming")

        return health

    def cleanup(self):
        """Clean up all resources."""
        logging.info("Cleaning up results streamer...")

        # Stop streaming if running
        if self._is_streaming:
            self.stop_streaming()

        # Clear all queues
        for deployment_id, queue in self.results_queues.items():
            try:
                while not queue.empty():
                    queue.get_nowait()
                    queue.task_done()
            except Exception:
                pass

        self.results_queues.clear()

        # Clear tracking data
        self._counters.clear()
        self._last_input_order.clear()
        self._session_counters.clear()

        logging.info("Results streamer cleanup completed")
