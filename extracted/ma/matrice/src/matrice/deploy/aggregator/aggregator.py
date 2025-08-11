import logging
import threading
import time
import copy
from typing import Dict, Optional, Any
from queue import Queue, Empty
from collections import defaultdict


class ResultsAggregator:
    """
    Handles complex aggregation and combination of synchronized results from multiple deployments.
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
            aggregation_strategies: List of aggregation strategies to apply
        """
        self.synchronized_results_queue = synchronized_results_queue
        self.aggregated_results_queue = Queue()
        self.aggregate_by_location = aggregate_by_location

        # Threading and state management
        self._stop_aggregation = threading.Event()
        self._aggregation_thread: Optional[threading.Thread] = None
        self._is_running = False
        self._lock = threading.RLock()
        self._sent_keys = set()

        # Statistics
        self.stats = {
            "start_time": None,
            "results_processed": 0,
            "aggregations_created": 0,
            "errors": 0,
            "last_error": None,
            "last_error_time": None,
            "strategy_stats": defaultdict(int),
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
        """Main aggregation worker thread."""
        logging.info("Results aggregation worker started")

        while not self._stop_aggregation.is_set():
            try:
                # Get synchronized result from queue
                try:
                    synced_result = self.synchronized_results_queue.get(timeout=1.0)
                except Empty:
                    continue

                # Process the single synchronized result
                aggregated_result = self._aggregate_single_result(synced_result)
                
                if aggregated_result:
                    # Add to output queue
                    self.aggregated_results_queue.put(aggregated_result)
                    
                    # Update statistics
                    with self._lock:
                        self.stats["results_processed"] += 1
                        self.stats["aggregations_created"] += 1

                # Mark task as done
                self.synchronized_results_queue.task_done()

            except Exception as exc:
                if not self._stop_aggregation.is_set():
                    self._record_error(f"Error in aggregation worker: {str(exc)}")
                    time.sleep(0.1)  # Prevent tight error loops

        logging.info("Results aggregation worker stopped")

    def _aggregate_single_result(self, sync_result: Dict) -> Optional[Dict]:
        """Aggregate a single synchronized result using configured strategies."""
        try:
            # Extract deployment results
            deployment_results = sync_result.get("deployment_results", {})
            if not deployment_results:
                logging.warning("No deployment results found in synchronized result")
                return None

            # Get stream info from synchronized result
            stream_key = sync_result.get("stream_key")
            input_order = sync_result.get("input_order")
            stream_group_key = sync_result.get("stream_group_key")
            
            key = (stream_group_key, stream_key, input_order)
            if key in self._sent_keys:
                logging.debug(f"Skipping duplicate result: {key}")
                return None
            self._sent_keys.add(key)
            
            # Basic memory management - prevent unbounded growth
            if len(self._sent_keys) > 10000:
                # Remove oldest entries (this is a simple approach)
                keys_to_remove = list(self._sent_keys)[:2000]
                for old_key in keys_to_remove:
                    self._sent_keys.discard(old_key)
                logging.debug(f"Cleaned up {len(keys_to_remove)} old keys from _sent_keys")

            if not stream_key or input_order is None:
                logging.warning("Missing stream_key or input_order in synchronized result")
                return None

            # Extract input_stream and camera_info from the first available deployment result
            # These should be consistent across all deployments for the same stream
            first_deployment_result = next(iter(deployment_results.values()))
            first_app_result = first_deployment_result.get("result", {})
            input_streams = first_app_result.get("input_streams", [])
            input_stream = copy.deepcopy(input_streams[0]["input_stream"]) if input_streams else {}
            camera_info = copy.deepcopy(first_app_result.get("camera_info", {}))
            
            # Collect all app results for agg_apps
            agg_apps = []
            
            for deployment_id, deployment_result in deployment_results.items():
                # Extract the actual app result from deployment result
                app_result = deployment_result.get("result", {})
                if app_result:
                    app_result["deployment_id"] = deployment_id
                    app_result["deployment_timestamp"] = deployment_result.get("timestamp", time.time())
                    # Remove content from inner input_streams to save space
                    if "input_streams" in app_result:
                        for input_stream_item in app_result["input_streams"]:
                            if "input_stream" in input_stream_item and "content" in input_stream_item["input_stream"]:
                                del input_stream_item["input_stream"]["content"]
                    agg_apps.append(app_result)

            # Create camera_results structure as expected by the notebook
            camera_results = {
                "input_stream": input_stream,
                "camera_info": camera_info,
                "agg_apps": agg_apps,
                # Add aggregation metadata for tracking
                "aggregation_metadata": {
                    "stream_key": stream_key,
                    "input_order": input_order,
                    "stream_group_key": stream_group_key,
                    "deployment_count": len(deployment_results),
                    "aggregation_timestamp": time.time(),
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
        with self._lock:
            self.stats["errors"] += 1
            self.stats["last_error"] = error_message
            self.stats["last_error_time"] = time.time()
        logging.error(f"Aggregator error: {error_message}")

    def get_stats(self) -> Dict[str, Any]:
        """Get current aggregation statistics."""
        with self._lock:
            stats = self.stats.copy()

        # Add runtime statistics
        if stats["start_time"]:
            stats["runtime_seconds"] = time.time() - stats["start_time"]

        stats["output_queue_size"] = self.aggregated_results_queue.qsize()

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

        logging.info("Results aggregator cleanup completed") 