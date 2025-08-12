from typing import List, Dict, Tuple
from queue import Queue, Empty, PriorityQueue
import threading
import time
import logging
from collections import defaultdict


class ResultsSynchronizer:
    """
    Handles synchronization of results from multiple deployments by stream_key and input_order.
    Ensures consistent structure and proper error handling for the aggregation pipeline.
    """

    def __init__(
        self,
        results_queues: Dict[str, PriorityQueue],
        sync_timeout: float = 60.0,
    ):
        """
        Initialize the results synchronizer.

        Args:
            results_queues: Dictionary of priority queues containing results from deployments
            sync_timeout: Maximum time to wait for input_order synchronization (in seconds)
        """
        self.results_queues = results_queues
        self.synchronized_results_queue = Queue()
        self.sync_timeout = sync_timeout
        self.deployment_ids = list(results_queues.keys())

        # State management
        self._is_running = False
        self._stop_synchronization = threading.Event()
        self._lock = threading.RLock()
        self._synchronization_thread = None

        # Synchronization state
        # Structure: {(stream_group_key, stream_key, input_order): {deployment_id: result, ...}}
        self._pending_results: Dict[Tuple[str, str, int], Dict[str, Dict]] = defaultdict(
            dict
        )
        # Track when each key combination was first seen
        self._result_timestamps: Dict[Tuple[str, str, int], float] = {}

        # Statistics
        self.stats = {
            "results_consumed": 0,
            "results_synchronized": 0,
            "partial_syncs": 0,
            "complete_syncs": 0,
            "timeouts": 0,
            "start_time": None,
            "errors": 0,
            "last_error": None,
            "last_error_time": None,
            "pending_keys": 0,
            "avg_sync_time": 0.0,
            "max_sync_time": 0.0,
        }

    def _record_error(self, error_message: str):
        """Record an error in statistics."""
        with self._lock:
            self.stats["errors"] += 1
            self.stats["last_error"] = error_message
            self.stats["last_error_time"] = time.time()
        logging.error(f"Synchronizer error: {error_message}")

    def _collect_results_from_queues(self):
        """Collect results from all deployment queues and organize by stream_key and input_order."""
        results_collected = 0

        for deployment_id, queue in self.results_queues.items():
            try:
                while True:  # Collect all available results from this queue
                    try:
                        priority_result = queue.get(block=False)
                        # PriorityQueue items come in as (order, seq, result) or (order, result)
                        if isinstance(priority_result, tuple):
                            if len(priority_result) >= 3:
                                result = priority_result[2]
                            elif len(priority_result) == 2:
                                result = priority_result[1]
                            else:
                                result = priority_result
                        else:
                            result = priority_result

                        stream_key = result.get("stream_key")
                        stream_group_key = result.get("stream_group_key")
                        input_order = result.get("input_order")

                        key = (stream_group_key, stream_key, input_order)
                        current_time = time.time()

                        with self._lock:
                            # Add result to pending collection
                            self._pending_results[key][deployment_id] = result

                            # Track first occurrence timestamp
                            if key not in self._result_timestamps:
                                self._result_timestamps[key] = current_time

                            self.stats["results_consumed"] += 1
                            results_collected += 1

                        logging.debug(
                            f"Collected result from {deployment_id} for stream {stream_key}, stream group {stream_group_key}"
                        )

                    except Empty:
                        break  # No more results in this queue

            except Exception as exc:
                if not self._stop_synchronization.is_set():
                    self._record_error(
                        f"Error collecting results from {deployment_id}: {str(exc)}"
                    )

        return results_collected

    def _create_synchronized_result(
        self,
        key: Tuple[str, str, int],
        deployment_results: Dict[str, Dict],
        is_complete: bool,
        is_timeout: bool,
    ) -> Dict:
        """Create a synchronized result dictionary with enhanced metadata."""
        stream_group_key, stream_key, input_order = key
        current_time = time.time()
        sync_start_time = self._result_timestamps.get(key, current_time)
        sync_duration = current_time - sync_start_time

        # Update sync time statistics
        with self._lock:
            self.stats["max_sync_time"] = max(self.stats["max_sync_time"], sync_duration)
            # Simple running average calculation
            if self.stats["results_synchronized"] > 0:
                self.stats["avg_sync_time"] = (
                    (self.stats["avg_sync_time"] * self.stats["results_synchronized"] + sync_duration) /
                    (self.stats["results_synchronized"] + 1)
                )
            else:
                self.stats["avg_sync_time"] = sync_duration

        # Get stream_group_key from first available result for enhanced metadata
        stream_group_key = None
        for result in deployment_results.values():
            stream_group_key = result.get("stream_group_key")
            if stream_group_key:
                break

        # Create enhanced synchronized result with consistent structure
        synchronized_result = {
            "stream_key": stream_key,
            "input_order": input_order,
            "stream_group_key": stream_group_key,
            "deployment_results": deployment_results.copy(),
            "synchronization_metadata": {
                "deployments_count": len(deployment_results),
                "expected_deployments": len(self.deployment_ids),
                "complete": is_complete,
                "timeout": is_timeout,
                "sync_duration_seconds": sync_duration,
                "sync_start_timestamp": sync_start_time,
                "sync_end_timestamp": current_time,
                "missing_deployments": (
                    [
                        dep_id
                        for dep_id in self.deployment_ids
                        if dep_id not in deployment_results
                    ]
                    if not is_complete
                    else []
                ),
                "sync_completeness_ratio": len(deployment_results) / len(self.deployment_ids),
                "synchronizer_version": "2.0",  # Updated version for session support
            },
        }

        # Add timeout reason if applicable
        if is_timeout:
            synchronized_result["synchronization_metadata"]["timeout_reason"] = (
                f"Sync timeout after {self.sync_timeout} seconds"
            )
            with self._lock:
                self.stats["timeouts"] += 1

        return synchronized_result

    def _process_synchronized_results(self) -> List[Dict]:
        """Process pending results and return synchronized results ready for output."""
        synchronized_results = []
        current_time = time.time()
        keys_to_remove = []

        with self._lock:
            for key, deployment_results in self._pending_results.items():
                result_age = current_time - self._result_timestamps[key]
                is_complete = len(deployment_results) == len(self.deployment_ids)
                is_timeout = result_age >= self.sync_timeout

                # Release result if complete or timed out
                if is_complete or is_timeout:
                    synchronized_result = self._create_synchronized_result(
                        key, deployment_results, is_complete, is_timeout
                    )
                    synchronized_results.append(synchronized_result)
                    keys_to_remove.append(key)

                    # Update statistics
                    if is_complete:
                        self.stats["complete_syncs"] += 1
                        stream_group_key, stream_key, input_order = key
                        logging.debug(
                            f"Complete sync for group {stream_group_key}, stream {stream_key}, "
                            f"order {input_order} with {len(deployment_results)} deployments"
                        )
                    else:
                        self.stats["partial_syncs"] += 1
                        stream_group_key, stream_key, input_order = key
                        logging.warning(
                            f"Partial sync for group {stream_group_key}, stream {stream_key}, "
                            f"order {input_order}: {len(deployment_results)}/{len(self.deployment_ids)} deployments "
                            f"(timeout after {result_age:.2f}s)"
                        )

            # Remove processed keys
            for key in keys_to_remove:
                del self._pending_results[key]
                del self._result_timestamps[key]

            self.stats["pending_keys"] = len(self._pending_results)

        return synchronized_results

    def _send_synchronized_result(self, synchronized_result: Dict):
        """Send a single synchronized result to the output queue."""
        try:
            self.synchronized_results_queue.put(synchronized_result)

            with self._lock:
                self.stats["results_synchronized"] += 1

            logging.debug(
                f"Sent synchronized result for group {synchronized_result.get('stream_group_key')}, "
                f"stream {synchronized_result['stream_key']}, "
                f"order {synchronized_result['input_order']}"
            )

        except Exception as exc:
            self._record_error(f"Error sending synchronized result: {str(exc)}")

    def _synchronization_worker(self):
        """Main synchronization worker thread."""
        logging.info("Results synchronization worker started")

        while not self._stop_synchronization.is_set():
            try:
                # Collect new results from all deployment queues
                results_collected = self._collect_results_from_queues()

                # Process synchronized results (complete or timed out)
                synchronized_results = self._process_synchronized_results()

                # Send each result individually (no batching)
                for synchronized_result in synchronized_results:
                    self._send_synchronized_result(synchronized_result)

                # Log periodic statistics
                if results_collected > 0 or synchronized_results:
                    with self._lock:
                        logging.debug(
                            f"Synchronizer: collected={results_collected}, "
                            f"synchronized={len(synchronized_results)}, "
                            f"pending_keys={self.stats['pending_keys']}, "
                            f"complete_ratio={self.stats['complete_syncs']}/{self.stats['complete_syncs'] + self.stats['partial_syncs']} "
                            f"avg_sync_time={self.stats['avg_sync_time']:.3f}s"
                        )

                # Adaptive delay based on activity
                if results_collected > 0 or synchronized_results:
                    time.sleep(0.01)  # High activity, short delay
                else:
                    time.sleep(0.05)  # Low activity, slightly longer delay

            except Exception as exc:
                if not self._stop_synchronization.is_set():
                    self._record_error(f"Error in synchronization worker: {str(exc)}")
                    time.sleep(0.1)  # Prevent tight error loops

        # Process any remaining results before stopping
        try:
            final_results = self._process_synchronized_results()
            for synchronized_result in final_results:
                self._send_synchronized_result(synchronized_result)
            logging.info(f"Processed {len(final_results)} final results during shutdown")
        except Exception as exc:
            logging.error(f"Error processing final results: {exc}")

        logging.info("Results synchronization worker stopped")

    def start_synchronization(self) -> bool:
        """
        Start the results synchronization process.

        Returns:
            bool: True if synchronization started successfully, False otherwise
        """

        if self._is_running:
            logging.warning("Results synchronization is already running")
            return True

        self._is_running = True
        self.stats["start_time"] = time.time()
        self._stop_synchronization.clear()

        try:
            # Start synchronization thread
            self._synchronization_thread = threading.Thread(
                target=self._synchronization_worker,
                name="ResultsSynchronizer",
                daemon=True,
            )
            self._synchronization_thread.start()

            logging.info(
                f"Started results synchronization for {len(self.results_queues)} deployment queues "
                f"with timeout {self.sync_timeout}s"
            )
            return True

        except Exception as exc:
            self._record_error(f"Failed to start results synchronization: {str(exc)}")
            self.stop_synchronization()
            return False

    def stop_synchronization(self):
        """Stop the results synchronization process."""
        if not self._is_running:
            logging.info("Results synchronization is not running")
            return

        self._is_running = False
        self._stop_synchronization.set()

        logging.info("Stopping results synchronization...")

        # Wait for synchronization thread to complete
        if self._synchronization_thread and self._synchronization_thread.is_alive():
            try:
                self._synchronization_thread.join(timeout=5.0)
                if self._synchronization_thread.is_alive():
                    logging.warning(
                        "Results synchronization thread did not stop gracefully"
                    )
            except Exception as exc:
                logging.error(f"Error joining synchronization thread: {exc}")

        self._synchronization_thread = None
        logging.info("Results synchronization stopped")

    def get_stats(self) -> Dict:
        """Get current synchronization statistics."""
        with self._lock:
            stats = self.stats.copy()

        # Add runtime statistics
        if stats["start_time"]:
            stats["runtime_seconds"] = time.time() - stats["start_time"]

        # Add calculated metrics
        total_syncs = stats["complete_syncs"] + stats["partial_syncs"]
        if total_syncs > 0:
            stats["completion_rate"] = stats["complete_syncs"] / total_syncs
            stats["timeout_rate"] = stats["timeouts"] / total_syncs
        else:
            stats["completion_rate"] = 0.0
            stats["timeout_rate"] = 0.0

        stats["output_queue_size"] = self.synchronized_results_queue.qsize()

        return stats

    def get_health_status(self) -> Dict:
        """Get health status of the synchronizer."""
        health = {
            "status": "healthy",
            "is_running": self._is_running,
            "deployments": len(self.results_queues),
            "queue_sizes": {},
            "pending_sync_keys": self.stats["pending_keys"],
            "errors": self.stats["errors"],
            "completion_rate": 0.0,
            "avg_sync_time": self.stats["avg_sync_time"],
        }

        # Check queue sizes
        with self._lock:
            for deployment_id, queue in self.results_queues.items():
                queue_size = queue.qsize()
                health["queue_sizes"][deployment_id] = queue_size

        # Calculate completion rate
        total_syncs = self.stats["complete_syncs"] + self.stats["partial_syncs"]
        if total_syncs > 0:
            health["completion_rate"] = self.stats["complete_syncs"] / total_syncs

        # Check for recent errors (within last 60 seconds)
        if (
            self.stats["last_error_time"]
            and (time.time() - self.stats["last_error_time"]) < 60
        ):
            health["status"] = "degraded"
            health["recent_error"] = self.stats["last_error"]
            health["issue"] = f"Recent error: {self.stats['last_error']}"
            logging.warning(f"Synchronizer degraded due to recent error: {self.stats['last_error']}")

        # Check for excessive pending keys (potential memory issue)
        if self.stats["pending_keys"] > 1000:
            health["status"] = "degraded"
            health["issue"] = f"Too many pending sync keys ({self.stats['pending_keys']})"
            logging.warning(f"Synchronizer degraded: too many pending sync keys ({self.stats['pending_keys']}, threshold: 1000)")

        # Check completion rate
        if total_syncs > 10 and health["completion_rate"] < 0.8:  # Less than 80% completion
            health["status"] = "degraded"
            health["issue"] = f"Low completion rate: {health['completion_rate']:.2%} ({self.stats['complete_syncs']}/{total_syncs})"
            logging.warning(f"Synchronizer degraded: low completion rate {health['completion_rate']:.2%} ({self.stats['complete_syncs']}/{total_syncs} complete)")

        # Check sync time
        if self.stats["avg_sync_time"] > self.sync_timeout * 0.8:  # Average sync time near timeout
            health["status"] = "degraded"
            health["issue"] = f"High average sync time: {self.stats['avg_sync_time']:.2f}s (timeout: {self.sync_timeout}s)"
            logging.warning(f"Synchronizer degraded: high average sync time {self.stats['avg_sync_time']:.2f}s (timeout threshold: {self.sync_timeout * 0.8:.1f}s)")

        # Check if not running when it should be
        if not self._is_running:
            health["status"] = "unhealthy"
            health["issue"] = "Synchronizer is not running"
            logging.error("Synchronizer is not running")

        return health

    def force_sync_pending(self) -> int:
        """Force synchronization of all pending results regardless of completeness."""
        with self._lock:
            pending_count = len(self._pending_results)
            if pending_count == 0:
                return 0

            # Get all pending results
            synchronized_results = []
            for key, deployment_results in self._pending_results.items():
                synchronized_result = self._create_synchronized_result(
                    key, deployment_results, False, True
                )
                synchronized_results.append(synchronized_result)

            # Clear pending state
            self._pending_results.clear()
            self._result_timestamps.clear()
            self.stats["pending_keys"] = 0

        # Send each result individually
        for synchronized_result in synchronized_results:
            self._send_synchronized_result(synchronized_result)

        logging.info(f"Force synchronized {pending_count} pending result keys")
        return pending_count

    def cleanup(self):
        """Clean up resources."""
        self.stop_synchronization()
        
        # Clear queues safely
        try:
            while not self.synchronized_results_queue.empty():
                self.synchronized_results_queue.get_nowait()
        except Exception:
            pass

        # Clear internal state
        with self._lock:
            self._pending_results.clear()
            self._result_timestamps.clear()

        logging.info("Results synchronizer cleanup completed")
