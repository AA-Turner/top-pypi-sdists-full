from typing import List, Dict, Tuple, Set
from queue import Queue, Empty, PriorityQueue
import threading
import time
import logging
from collections import defaultdict, deque
import heapq


class ResultsSynchronizer:
    """
    Optimized synchronization of results from multiple deployments by stream_key and input_order.
    Ensures consistent structure and proper error handling for the aggregation pipeline.
    """

    def __init__(
        self,
        results_queues: Dict[str, PriorityQueue],
        sync_timeout: float = 300,
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
        self.deployment_ids = tuple(results_queues.keys())  # Use tuple for faster iteration
        self.deployment_count = len(self.deployment_ids)

        # State management
        self._is_running = False
        self._stop_synchronization = threading.Event()
        # Use separate locks to reduce contention
        self._pending_lock = threading.Lock()
        self._stats_lock = threading.Lock()
        self._synchronization_thread = None

        # Optimized synchronization state using more efficient data structures
        # Structure: {(stream_group_key, stream_key, input_order): {deployment_id: result, ...}}
        self._pending_results: Dict[Tuple[str, str, int], Dict[str, Dict]] = {}
        # Track when each key combination was first seen - use list for faster cleanup
        self._result_timestamps: Dict[Tuple[str, str, int], float] = {}
        # Timeout queue for efficient cleanup - (timestamp, key)
        self._timeout_queue: List[Tuple[float, Tuple[str, str, int]]] = []
        # Track keys that have been timed out to prevent duplicate processing
        self._timed_out_keys: Set[Tuple[str, str, int]] = set()
        # Track latest result per deployment for timeout scenarios
        self._latest_deployment_results: Dict[Tuple[str, str, int], Dict[str, Dict]] = {}

        # Statistics - use separate dict to reduce lock contention
        self._stats = {
            "results_consumed": 0,
            "results_synchronized": 0,
            "partial_syncs": 0,
            "complete_syncs": 0,
            "timeouts": 0,
            "errors": 0,
            "pending_keys": 0,
            "timed_out_keys": 0,
            "duplicates_prevented": 0,
        }
        self._timing_stats = {
            "start_time": None,
            "last_error": None,
            "last_error_time": None,
            "avg_sync_time": 0.0,
            "max_sync_time": 0.0,
            "total_sync_time": 0.0,
        }

    def _record_error(self, error_message: str):
        """Record an error in statistics."""
        with self._stats_lock:
            self._stats["errors"] += 1
            self._timing_stats["last_error"] = error_message
            self._timing_stats["last_error_time"] = time.time()
        # Reduce logging frequency for performance
        if self._stats["errors"] % 10 == 1:  # Log every 10th error
            logging.error(f"Synchronizer error (#{self._stats['errors']}): {error_message}")

    def _collect_results_from_queues(self) -> int:
        """Collect results from all deployment queues for immediate processing."""
        results_collected = 0
        current_time = time.time()
        
        # Collect from all queues non-blocking
        for deployment_id in self.deployment_ids:
            queue = self.results_queues[deployment_id]

            try:
                # Get all available results from this queue
                while True:
                    try:
                        priority_result = queue.get(block=False)
                        # Extract result from priority queue tuple
                        if isinstance(priority_result, tuple):
                            result = priority_result[-1]  # Last element is always the result
                        else:
                            result = priority_result

                        # Process immediately
                        stream_key = result.get("stream_key")
                        stream_group_key = result.get("stream_group_key")
                        input_order = result.get("input_order")

                        if not all([stream_key, stream_group_key, input_order is not None]):
                            continue  # Skip invalid results

                        key = (stream_group_key, stream_key, input_order)
                        
                        with self._pending_lock:
                            # Skip if this key has already been timed out to prevent duplicates
                            if key in self._timed_out_keys:
                                with self._stats_lock:
                                    self._stats["duplicates_prevented"] += 1
                                logging.debug(f"Prevented duplicate processing for timed-out key: {key}")
                                continue
                                
                            # Initialize if first result for this key
                            if key not in self._pending_results:
                                self._pending_results[key] = {}
                                self._result_timestamps[key] = current_time
                                self._latest_deployment_results[key] = {}
                                # Add to timeout queue for efficient cleanup
                                heapq.heappush(self._timeout_queue, (current_time + self.sync_timeout, key))
                            
                            # Add result to pending collection and track as latest
                            self._pending_results[key][deployment_id] = result
                            self._latest_deployment_results[key][deployment_id] = result
                            results_collected += 1

                    except Empty:
                        break  # No more results in this queue

            except Exception as exc:
                if not self._stop_synchronization.is_set():
                    self._record_error(f"Error collecting from {deployment_id}: {str(exc)}")

        # Update stats
        if results_collected > 0:
            with self._stats_lock:
                self._stats["results_consumed"] += results_collected
                self._stats["pending_keys"] = len(self._pending_results)

        return results_collected

    def _create_synchronized_result(
        self,
        key: Tuple[str, str, int],
        deployment_results: Dict[str, Dict],
        is_complete: bool,
        is_timeout: bool,
        sync_start_time: float,
    ) -> Dict:
        """Create a synchronized result dictionary with enhanced metadata."""
        stream_group_key, stream_key, input_order = key
        current_time = time.time()
        sync_duration = current_time - sync_start_time

        # Update sync time statistics (batch update for performance)
        with self._stats_lock:
            self._timing_stats["max_sync_time"] = max(self._timing_stats["max_sync_time"], sync_duration)
            self._timing_stats["total_sync_time"] += sync_duration
            # Calculate running average more efficiently
            sync_count = self._stats["results_synchronized"] + 1
            self._timing_stats["avg_sync_time"] = self._timing_stats["total_sync_time"] / sync_count

        # Pre-calculate metadata to avoid repeated calculations
        deployments_count = len(deployment_results)
        sync_completeness_ratio = deployments_count / self.deployment_count
        
        # Create synchronized result with minimal object creation
        synchronized_result = {
            "stream_key": stream_key,
            "input_order": input_order,
            "stream_group_key": stream_group_key,
            "deployment_results": deployment_results,  # Don't copy, transfer ownership
            "synchronization_metadata": {
                "deployments_count": deployments_count,
                "expected_deployments": self.deployment_count,
                "complete": is_complete,
                "timeout": is_timeout,
                "sync_duration_seconds": sync_duration,
                "sync_start_timestamp": sync_start_time,
                "sync_end_timestamp": current_time,
                "sync_completeness_ratio": sync_completeness_ratio,
                "synchronizer_version": "2.1",  # Updated optimized version
            },
        }

        # Add missing deployments only if needed (avoid list comprehension when complete)
        if not is_complete:
            missing = []
            for dep_id in self.deployment_ids:
                if dep_id not in deployment_results:
                    missing.append(dep_id)
            synchronized_result["synchronization_metadata"]["missing_deployments"] = missing
        else:
            synchronized_result["synchronization_metadata"]["missing_deployments"] = []

        # Add timeout reason if applicable
        if is_timeout:
            synchronized_result["synchronization_metadata"]["timeout_reason"] = (
                f"Sync timeout after {self.sync_timeout} seconds"
            )

        return synchronized_result

    def _process_synchronized_results(self) -> List[Dict]:
        """Process pending results using efficient timeout queue and batch processing."""
        synchronized_results = []
        current_time = time.time()
        keys_to_remove = []
        complete_count = 0
        partial_count = 0

        with self._pending_lock:
            # Process timeouts efficiently using heap
            while self._timeout_queue and self._timeout_queue[0][0] <= current_time:
                timeout_time, key = heapq.heappop(self._timeout_queue)
                if key in self._pending_results and key not in self._timed_out_keys:
                    # Use latest deployment results for timeout (ensures we get most recent data)
                    deployment_results = self._latest_deployment_results.get(key, self._pending_results[key])
                    is_complete = len(deployment_results) == self.deployment_count
                    sync_start_time = self._result_timestamps[key]
                    
                    # Mark this key as timed out to prevent future processing
                    self._timed_out_keys.add(key)
                    
                    synchronized_result = self._create_synchronized_result(
                        key, deployment_results, is_complete, True, sync_start_time
                    )
                    synchronized_results.append(synchronized_result)
                    keys_to_remove.append(key)

                    if is_complete:
                        complete_count += 1
                    else:
                        partial_count += 1
                        
                    logging.debug(f"Processed timeout for key {key} with {len(deployment_results)} deployments (complete: {is_complete})")

            # Check for complete results (not timed out yet)
            for key, deployment_results in list(self._pending_results.items()):
                if key not in keys_to_remove and key not in self._timed_out_keys and len(deployment_results) == self.deployment_count:
                    sync_start_time = self._result_timestamps[key]
                    synchronized_result = self._create_synchronized_result(
                        key, deployment_results, True, False, sync_start_time
                    )
                    synchronized_results.append(synchronized_result)
                    keys_to_remove.append(key)
                    complete_count += 1

            # Batch remove processed keys and cleanup all related data structures
            for key in keys_to_remove:
                self._pending_results.pop(key, None)
                self._result_timestamps.pop(key, None)
                self._latest_deployment_results.pop(key, None)
                # Don't remove from _timed_out_keys yet - keep for duplicate prevention

        # Batch update statistics
        if synchronized_results:
            with self._stats_lock:
                self._stats["complete_syncs"] += complete_count
                self._stats["partial_syncs"] += partial_count
                self._stats["results_synchronized"] += len(synchronized_results)
                self._stats["pending_keys"] = len(self._pending_results)
                if partial_count > 0:
                    self._stats["timeouts"] += partial_count

            # Reduce debug logging frequency for performance
            if complete_count > 0 and self._stats["complete_syncs"] % 100 == 0:
                logging.debug(f"Processed {complete_count} complete syncs, {partial_count} partial syncs")
            elif partial_count > 0 and self._stats["partial_syncs"] % 10 == 0:
                logging.warning(f"Processed {partial_count} partial syncs (timeouts), {complete_count} complete syncs")

        return synchronized_results

    def _cleanup_old_timed_out_keys(self, current_time: float):
        """Clean up old timed-out keys to prevent memory leaks."""
        # Clean up timed-out keys older than 2x the sync timeout
        cleanup_age = self.sync_timeout * 2
        keys_to_cleanup = []
        
        for key in self._timed_out_keys:
            # Check if we have timestamp info for this key
            if key in self._result_timestamps:
                key_age = current_time - self._result_timestamps[key]
                if key_age > cleanup_age:
                    keys_to_cleanup.append(key)
            else:
                # If no timestamp, it's safe to cleanup (shouldn't happen but defensive)
                keys_to_cleanup.append(key)
        
        # Remove old keys
        for key in keys_to_cleanup:
            self._timed_out_keys.discard(key)
            
        if keys_to_cleanup:
            logging.debug(f"Cleaned up {len(keys_to_cleanup)} old timed-out keys")

    def _send_synchronized_result(self, synchronized_result: Dict):
        """Send a single synchronized result to the output queue."""
        try:
            self.synchronized_results_queue.put(synchronized_result)

            logging.debug(
                f"Sent synchronized result for group {synchronized_result.get('stream_group_key')}, "
                f"stream {synchronized_result['stream_key']}, "
                f"order {synchronized_result['input_order']}"
            )

        except Exception as exc:
            self._record_error(f"Error sending synchronized result: {str(exc)}")

    def _synchronization_worker(self):
        """Optimized main synchronization worker thread for immediate processing."""
        logging.info("Results synchronization worker started")
        last_log_time = time.time()
        last_cleanup_time = time.time()
        log_interval = 30.0  # Log every 30 seconds instead of every cycle
        cleanup_interval = 120.0  # Clean up old timed-out keys every 2 minutes

        while not self._stop_synchronization.is_set():
            try:
                # Collect new results for immediate processing
                results_collected = self._collect_results_from_queues()

                # Process synchronized results (complete or timed out)
                synchronized_results = self._process_synchronized_results()

                # Send results immediately
                for synchronized_result in synchronized_results:
                    self._send_synchronized_result(synchronized_result)

                # Reduced frequency logging for performance
                current_time = time.time()
                if (results_collected > 0 or synchronized_results) and (current_time - last_log_time) > log_interval:
                    with self._stats_lock:
                        total_syncs = self._stats['complete_syncs'] + self._stats['partial_syncs']
                        completion_rate = self._stats['complete_syncs'] / max(total_syncs, 1)
                        logging.debug(
                            f"Synchronizer: collected={results_collected}, "
                            f"synchronized={len(synchronized_results)}, "
                            f"pending_keys={self._stats['pending_keys']}, "
                            f"timed_out_keys={len(self._timed_out_keys)}, "
                            f"duplicates_prevented={self._stats['duplicates_prevented']}, "
                            f"completion_rate={completion_rate:.3f}, "
                            f"avg_sync_time={self._timing_stats['avg_sync_time']:.3f}s"
                        )
                    last_log_time = current_time

                # Periodic cleanup of old timed-out keys
                if (current_time - last_cleanup_time) > cleanup_interval:
                    with self._pending_lock:
                        self._cleanup_old_timed_out_keys(current_time)
                        with self._stats_lock:
                            self._stats["timed_out_keys"] = len(self._timed_out_keys)
                    last_cleanup_time = current_time

                # Minimal delay for immediate processing
                if results_collected > 0 or synchronized_results:
                    time.sleep(0.001)  # Activity detected, minimal delay
                else:
                    time.sleep(0.01)  # No activity, short delay

            except Exception as exc:
                if not self._stop_synchronization.is_set():
                    self._record_error(f"Error in synchronization worker: {str(exc)}")
                    time.sleep(0.1)  # Prevent tight error loops

        # Process any remaining results before stopping
        try:
            final_results = self._process_synchronized_results()
            if final_results:
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
        self._timing_stats["start_time"] = time.time()
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
        with self._stats_lock:
            stats = self._stats.copy()
            timing_stats = self._timing_stats.copy()

        # Merge statistics
        stats.update(timing_stats)

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
        
        # Add performance metrics
        stats["deployment_count"] = self.deployment_count

        return stats

    def get_health_status(self) -> Dict:
        """Get health status of the synchronizer."""
        health = {
            "status": "healthy",
            "is_running": self._is_running,
            "deployments": len(self.results_queues),
            "queue_sizes": {},
            "pending_sync_keys": 0,
            "errors": 0,
            "completion_rate": 0.0,
            "avg_sync_time": 0.0,
        }

        # Check queue sizes
        for deployment_id, queue in self.results_queues.items():
            queue_size = queue.qsize()
            health["queue_sizes"][deployment_id] = queue_size

        # Calculate completion rate
        with self._stats_lock:
            total_syncs = self._stats["complete_syncs"] + self._stats["partial_syncs"]
            if total_syncs > 0:
                health["completion_rate"] = self._stats["complete_syncs"] / total_syncs
            
            health["errors"] = self._stats["errors"]
            health["pending_sync_keys"] = self._stats["pending_keys"]
            health["avg_sync_time"] = self._timing_stats["avg_sync_time"]

        # Check for recent errors (within last 60 seconds)
        if (
            self._timing_stats["last_error_time"]
            and (time.time() - self._timing_stats["last_error_time"]) < 60
        ):
            health["status"] = "degraded"
            health["recent_error"] = self._timing_stats["last_error"]
            health["issue"] = f"Recent error: {self._timing_stats['last_error']}"
            logging.warning(f"Synchronizer degraded due to recent error: {self._timing_stats['last_error']}")

        # Check for excessive pending keys (potential memory issue)
        if self._stats["pending_keys"] > 1000:
            health["status"] = "degraded"
            health["issue"] = f"Too many pending sync keys ({self._stats['pending_keys']})"
            logging.warning(f"Synchronizer degraded: too many pending sync keys ({self._stats['pending_keys']}, threshold: 1000)")

        # Check completion rate
        if total_syncs > 10 and health["completion_rate"] < 0.8:  # Less than 80% completion
            health["status"] = "degraded"
            health["issue"] = f"Low completion rate: {health['completion_rate']:.2%} ({self._stats['complete_syncs']}/{total_syncs})"
            logging.warning(f"Synchronizer degraded: low completion rate {health['completion_rate']:.2%} ({self._stats['complete_syncs']}/{total_syncs} complete)")

        # Check sync time
        if self._timing_stats["avg_sync_time"] > self.sync_timeout * 0.8:  # Average sync time near timeout
            health["status"] = "degraded"
            health["issue"] = f"High average sync time: {self._timing_stats['avg_sync_time']:.2f}s (timeout: {self.sync_timeout}s)"
            logging.warning(f"Synchronizer degraded: high average sync time {self._timing_stats['avg_sync_time']:.2f}s (timeout threshold: {self.sync_timeout * 0.8:.1f}s)")

        # Check if not running when it should be
        if not self._is_running:
            health["status"] = "unhealthy"
            health["issue"] = "Synchronizer is not running"
            logging.error("Synchronizer is not running")

        return health

    def force_sync_pending(self) -> int:
        """Force synchronization of all pending results regardless of completeness."""
        with self._pending_lock:
            pending_count = len(self._pending_results)
            if pending_count == 0:
                return 0

            # Get all pending results
            synchronized_results = []
            for key, deployment_results in self._pending_results.items():
                sync_start_time = self._result_timestamps.get(key, time.time())
                synchronized_result = self._create_synchronized_result(
                    key, deployment_results, False, True, sync_start_time
                )
                synchronized_results.append(synchronized_result)

            # Clear pending state
            self._pending_results.clear()
            self._result_timestamps.clear()
            self._timeout_queue.clear()
            self._latest_deployment_results.clear()
            # Don't clear _timed_out_keys to maintain duplicate prevention
            
            with self._stats_lock:
                self._stats["pending_keys"] = 0

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
        with self._pending_lock:
            self._pending_results.clear()
            self._result_timestamps.clear()
            self._timeout_queue.clear()
            self._timed_out_keys.clear()
            self._latest_deployment_results.clear()

        logging.info("Results synchronizer cleanup completed")