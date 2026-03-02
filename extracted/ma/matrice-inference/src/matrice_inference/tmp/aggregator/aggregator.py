import logging
import threading
import time
import copy
from typing import Dict, Optional, Any, Set, Tuple
from queue import Queue, Empty
from collections import defaultdict, deque
import copy


class ResultsAggregator:
    """
    Optimized aggregation and combination of synchronized results from multiple deployments.
    This component takes synchronized results and combines them into meaningful aggregated outputs
    while maintaining consistent structure with individual deployment results.
    """

    def __init__(
        self,
        synchronized_results_queue: Queue,
        aggregate_by_location: bool = False,
    ):
        """
        Initialize the results aggregator.

        Args:
            synchronized_results_queue: Queue containing synchronized results from synchronizer
            aggregate_by_location: Whether to aggregate by location
        """
        self.synchronized_results_queue = synchronized_results_queue
        self.aggregated_results_queue = Queue()
        self.aggregate_by_location = aggregate_by_location

        # Threading and state management
        self._stop_aggregation = threading.Event()
        self._aggregation_thread: Optional[threading.Thread] = None
        self._is_running = False
        self._stats_lock = threading.Lock()
        
        # Use more efficient data structure for tracking sent keys
        # Use a deque with fixed maxlen for automatic cleanup
        self._sent_keys: deque = deque(maxlen=50000)  # More memory efficient than manual cleanup
        self._sent_keys_set: Set[Tuple[str, str, int]] = set()  # For O(1) lookups

        # Statistics
        self.stats = {
            "start_time": None,
            "results_processed": 0,
            "aggregations_created": 0,
            "errors": 0,
            "last_error": None,
            "last_error_time": None,
            "duplicates_skipped": 0,
        }

    def start_aggregation(self) -> bool:
        """
        Start the results aggregation process.

        Returns:
            bool: True if aggregation started successfully, False otherwise
        """
        if self._is_running:
            logging.warning("Results aggregation is already running")
            return True

        try:
            self._is_running = True
            self.stats["start_time"] = time.time()
            self._stop_aggregation.clear()

            # Start aggregation thread
            self._aggregation_thread = threading.Thread(
                target=self._aggregation_worker,
                name="ResultsAggregator",
                daemon=True,
            )
            self._aggregation_thread.start()

            logging.info("Results aggregation started successfully")
            return True

        except Exception as exc:
            self._record_error(f"Failed to start results aggregation: {str(exc)}")
            self.stop_aggregation()
            return False

    def stop_aggregation(self):
        """Stop the results aggregation process."""
        if not self._is_running:
            logging.info("Results aggregation is not running")
            return

        self._is_running = False
        self._stop_aggregation.set()

        logging.info("Stopping results aggregation...")

        # Wait for aggregation thread to complete
        if self._aggregation_thread and self._aggregation_thread.is_alive():
            try:
                self._aggregation_thread.join(timeout=5.0)
                if self._aggregation_thread.is_alive():
                    logging.warning("Results aggregation thread did not stop gracefully")
            except Exception as exc:
                logging.error(f"Error joining aggregation thread: {exc}")

        self._aggregation_thread = None
        logging.info("Results aggregation stopped")

    def _aggregation_worker(self):
        """Optimized main aggregation worker thread for immediate processing."""
        logging.info("Results aggregation worker started")
        last_log_time = time.time()
        log_interval = 30.0  # Log every 30 seconds

        while not self._stop_aggregation.is_set():
            try:
                # Get synchronized result from queue
                try:
                    synced_result = self.synchronized_results_queue.get(timeout=1.0)
                except Empty:
                    continue

                # Process the single synchronized result immediately
                aggregated_result = self._aggregate_single_result(synced_result)
                
                if aggregated_result:
                    # Add to output queue immediately
                    self.aggregated_results_queue.put(aggregated_result)
                    
                    # Update statistics
                    with self._stats_lock:
                        self.stats["results_processed"] += 1
                        self.stats["aggregations_created"] += 1
                else:
                    # Track duplicates
                    with self._stats_lock:
                        self.stats["duplicates_skipped"] += 1

                # Mark task as done
                self.synchronized_results_queue.task_done()

                # Reduced frequency logging
                current_time = time.time()
                if (current_time - last_log_time) > log_interval:
                    with self._stats_lock:
                        processed = self.stats["results_processed"]
                        duplicates = self.stats["duplicates_skipped"]
                        queue_size = self.aggregated_results_queue.qsize()
                    if processed > 0 or duplicates > 0:
                        logging.debug(f"Aggregator: processed={processed}, duplicates={duplicates}, queue_size={queue_size}")
                    last_log_time = current_time

            except Exception as exc:
                if not self._stop_aggregation.is_set():
                    self._record_error(f"Error in aggregation worker: {str(exc)}")
                    time.sleep(0.1)  # Prevent tight error loops

        logging.info("Results aggregation worker stopped")

    def _aggregate_single_result(self, sync_result: Dict) -> Optional[Dict]:
        """Optimized aggregation of a single synchronized result."""
        try:
            # Extract deployment results
            deployment_results = sync_result.get("deployment_results", {})
            if not deployment_results:
                return None

            # Get stream info from synchronized result
            stream_key = sync_result.get("stream_key")
            input_order = sync_result.get("input_order")
            stream_group_key = sync_result.get("stream_group_key")
            
            if not stream_key or input_order is None:
                return None

            # Efficient duplicate checking using O(1) set lookup
            key = (stream_group_key, stream_key, input_order)
            if key in self._sent_keys_set:
                return None  # Duplicate, skip silently for performance
            
            # Add to both deque (for automatic cleanup) and set (for fast lookup)
            self._sent_keys.append(key)
            self._sent_keys_set.add(key)
            
            # Clean up set when deque automatically removes old items
            if len(self._sent_keys_set) > self._sent_keys.maxlen:
                # Only keep recent items in set - rebuild from deque
                self._sent_keys_set = set(self._sent_keys)

            # Extract input_stream and camera_info efficiently (avoid deep copy)
            first_deployment_result = next(iter(deployment_results.values()))
            first_app_result = first_deployment_result.get("result", {})
            input_streams = first_app_result.get("input_streams", [])
            
            # Get input stream data efficiently
            if input_streams:
                input_data = input_streams[0]
                input_stream = copy.deepcopy(input_data.get("input_stream", input_data))
            else:
                input_stream = {}
            
            # Get camera_info without deep copy
            camera_info = first_app_result.get("camera_info", {})
            
            # Collect all app results efficiently
            agg_apps = []
            current_timestamp = time.time()
            
            for deployment_id, deployment_result in deployment_results.items():
                app_result = deployment_result.get("result", {})
                if not app_result:
                    continue
                    
                # Create optimized app result
                optimized_app_result = {
                    **app_result,  # Shallow copy for performance
                    "deployment_id": deployment_id,
                    "deployment_timestamp": deployment_result.get("timestamp", current_timestamp)
                }
                
                # Remove large content fields to save memory
                if "input_streams" in optimized_app_result:
                    input_streams_clean = []
                    for item in optimized_app_result["input_streams"]:
                        clean_item = {k: v for k, v in item.items() if k != "content"}
                        if "input_stream" in clean_item and isinstance(clean_item["input_stream"], dict):
                            clean_item["input_stream"] = {k: v for k, v in clean_item["input_stream"].items() if k != "content"}
                        input_streams_clean.append(clean_item)
                    optimized_app_result["input_streams"] = input_streams_clean
                
                agg_apps.append(optimized_app_result)

            # Create optimized camera_results structure
            camera_results = {
                "input_stream": input_stream,
                "camera_info": camera_info,
                "agg_apps": agg_apps,
                "aggregation_metadata": {
                    "stream_key": stream_key,
                    "input_order": input_order,
                    "stream_group_key": stream_group_key,
                    "deployment_count": len(deployment_results),
                    "aggregation_timestamp": current_timestamp,
                    "aggregation_type": "camera_results",
                    "synchronization_metadata": sync_result.get("synchronization_metadata", {})
                }
            }

            return camera_results

        except Exception as exc:
            self._record_error(f"Error aggregating single result: {str(exc)}")
            return None

    def _record_error(self, error_message: str):
        """Record an error in statistics."""
        with self._stats_lock:
            self.stats["errors"] += 1
            self.stats["last_error"] = error_message
            self.stats["last_error_time"] = time.time()
        # Reduce logging frequency for performance
        if self.stats["errors"] % 10 == 1:  # Log every 10th error
            logging.error(f"Aggregator error (#{self.stats['errors']}): {error_message}")

    def get_stats(self) -> Dict[str, Any]:
        """Get current aggregation statistics."""
        with self._stats_lock:
            stats = self.stats.copy()

        # Add runtime statistics
        if stats["start_time"]:
            stats["runtime_seconds"] = time.time() - stats["start_time"]

        stats["output_queue_size"] = self.aggregated_results_queue.qsize()
        stats["sent_keys_count"] = len(self._sent_keys)
        stats["sent_keys_set_count"] = len(self._sent_keys_set)

        return stats

    def get_health_status(self) -> Dict[str, Any]:
        """Get health status of the aggregator."""
        health = {
            "status": "healthy",
            "is_running": self._is_running,
            "output_queue_size": self.aggregated_results_queue.qsize(),
            "errors": self.stats["errors"],
        }

        # Check for recent errors (within last 60 seconds)
        if (
            self.stats["last_error_time"]
            and (time.time() - self.stats["last_error_time"]) < 60
        ):
            health["status"] = "degraded"
            health["reason"] = f"Recent error: {self.stats['last_error']}"
            logging.warning(f"Aggregator degraded due to recent error: {self.stats['last_error']}")

        # Check if output queue is getting full
        queue_size = self.aggregated_results_queue.qsize()
        if queue_size > 1000:
            health["status"] = "degraded"
            health["reason"] = f"Output queue too large ({queue_size} items)"
            logging.warning(f"Aggregator degraded: output queue has {queue_size} items (threshold: 100)")

        # Check if not running when it should be
        if not self._is_running:
            health["status"] = "unhealthy"
            health["reason"] = "Aggregator is not running"
            logging.error("Aggregator is not running")

        return health

    def cleanup(self):
        """Clean up resources."""
        self.stop_aggregation()
        
        # Clear queues
        try:
            while not self.aggregated_results_queue.empty():
                self.aggregated_results_queue.get_nowait()
        except Exception:
            pass
        
        # Clear tracking data
        self._sent_keys.clear()
        self._sent_keys_set.clear()

        logging.info("Results aggregator cleanup completed") 