import logging
import threading
import time
from queue import Queue, Empty
from typing import Dict, Optional, Any
from matrice_common.session import Session
from matrice_common.stream.kafka_stream import MatriceKafkaDeployment
from matrice_inference.tmp.aggregator.analytics import AnalyticsSummarizer
from matrice_inference.tmp.aggregator.latency import LatencyTracker


class ResultsPublisher:
    """
    Optimized streaming of final aggregated results from inference pipeline to Kafka.
    Processes results immediately for low latency.
    """

    def __init__(
        self, 
        inference_pipeline_id: str, 
        session: Session, 
        final_results_queue: Queue, 
        analytics_summarizer: Optional[AnalyticsSummarizer] = None,
        latency_tracker: Optional[LatencyTracker] = None
    ):
        """
        Initialize the final results streamer.

        Args:
            inference_pipeline_id: ID of the inference pipeline
            session: Session object for authentication
            final_results_queue: Queue containing final aggregated results
            analytics_summarizer: Optional analytics summarizer for forwarding results
            latency_tracker: Optional latency tracker for performance monitoring
        """
        self.inference_pipeline_id = inference_pipeline_id
        self.session = session
        self.final_results_queue = final_results_queue
        
        self.kafka_handler = MatriceKafkaDeployment(
            session, inference_pipeline_id, type="server"
        )
        # Optional analytics summarizer hook
        self.analytics_summarizer = analytics_summarizer
        # Optional latency tracker hook
        self.latency_tracker = latency_tracker
        
        # Threading and state management
        self._stop_streaming = threading.Event()
        self._streaming_thread: Optional[threading.Thread] = None
        self._is_running = False
        self._stats_lock = threading.Lock()
        
        # Statistics
        self.stats = {
            "start_time": None,
            "messages_produced": 0,
            "validation_errors": 0,
            "kafka_errors": 0,
            "errors": 0,
            "last_error": None,
            "last_error_time": None,
        }

    def start_streaming(self) -> bool:
        """
        Start streaming final results to Kafka.
        
        Returns:
            bool: True if streaming started successfully, False otherwise
        """
        if self._is_running:
            logging.warning("Final results streaming is already running")
            return True
            
        try:  
            # Reset stop event and start streaming thread
            self._stop_streaming.clear()
            self._streaming_thread = threading.Thread(
                target=self._stream_results_to_kafka,
                name=f"FinalResultsStreamer-{self.inference_pipeline_id}",
                daemon=True
            )
            self._streaming_thread.start()
            
            self._is_running = True
            self.stats["start_time"] = time.time()
            
            logging.info(f"Final results streaming started for pipeline: {self.inference_pipeline_id}")
            return True
            
        except Exception as exc:
            logging.error(f"Failed to start final results streaming: {exc}")
            self._record_error(f"Start streaming failed: {str(exc)}")
            return False

    def _stream_results_to_kafka(self):
        """Stream final results from queue to Kafka immediately."""
        logging.info("Starting final results streaming thread")
        last_log_time = time.time()
        log_interval = 30.0  # Log every 30 seconds
        
        while not self._stop_streaming.is_set():
            try:
                # Get result from queue with timeout
                try:
                    aggregated_result = self.final_results_queue.get(timeout=1.0)
                except Empty:
                    continue
                
                # Process single result immediately
                try:
                    # Extract stream key efficiently
                    stream_key = None
                    aggregation_metadata = aggregated_result.get("aggregation_metadata", {})
                    if aggregation_metadata:
                        stream_key = aggregation_metadata.get("stream_key")
                    if not stream_key:
                        # Fallback to camera_info
                        camera_info = aggregated_result.get('camera_info', {})
                        stream_key = camera_info.get('camera_name')
                    
                    # Produce message to Kafka immediately
                    self.kafka_handler.produce_message(
                        message=aggregated_result, 
                        key=stream_key
                    )
                    
                    with self._stats_lock:
                        self.stats["messages_produced"] += 1
                    
                    # Forward to analytics summarizer after successful publish
                    if self.analytics_summarizer is not None and hasattr(self.analytics_summarizer, 'ingest_result'):
                        try:
                            self.analytics_summarizer.ingest_result(aggregated_result)
                        except Exception as exc_inner:
                            if self.stats["messages_produced"] % 100 == 1:  # Log occasionally
                                logging.warning(f"Failed to forward to analytics summarizer: {exc_inner}")
                    
                    # Forward to latency tracker for performance monitoring
                    if self.latency_tracker is not None and hasattr(self.latency_tracker, 'ingest_result'):
                        try:
                            # Extract deployment ID from aggregation metadata
                            deployment_id = None
                            aggregation_metadata = aggregated_result.get("aggregation_metadata", {})
                            if aggregation_metadata:
                                # Use stream key as deployment identifier for tracking
                                deployment_id = aggregation_metadata.get("stream_key")
                            
                            # Forward each deployment result to latency tracker
                            deployment_results = aggregated_result.get("deployment_results", {})
                            for dep_id, deployment_result in deployment_results.items():
                                result_data = deployment_result.get("result", {})
                                if result_data:
                                    self.latency_tracker.ingest_result(dep_id, result_data)
                        except Exception as exc_inner:
                            if self.stats["messages_produced"] % 100 == 1:  # Log occasionally
                                logging.warning(f"Failed to forward to latency tracker: {exc_inner}")
                    
                except Exception as exc:
                    with self._stats_lock:
                        self.stats["kafka_errors"] += 1
                    if self.stats["kafka_errors"] % 10 == 1:  # Log every 10th error
                        self._record_error(f"Failed to produce aggregated result to Kafka: {str(exc)}")
                
                # Mark task as done
                self.final_results_queue.task_done()
                
                # Reduced frequency logging
                current_time = time.time()
                if (current_time - last_log_time) > log_interval:
                    with self._stats_lock:
                        messages_produced = self.stats["messages_produced"]
                        kafka_errors = self.stats["kafka_errors"]
                    if messages_produced > 0 or kafka_errors > 0:
                        logging.debug(f"Publisher: produced={messages_produced} messages, kafka_errors={kafka_errors}")
                    last_log_time = current_time
                
            except Exception as exc:
                if not self._stop_streaming.is_set():
                    logging.error(f"Error streaming final result: {exc}")
                    self._record_error(f"Streaming error: {str(exc)}")
                    time.sleep(0.1)  # Prevent tight error loops
        
        logging.info("Final results streaming thread stopped")

    # def _validate_aggregated_result(self, result: Any) -> bool:
    #     """
    #     Validate the result format for aggregated results based on stream_worker structure.
        
    #     Args:
    #         result: Result to validate
            
    #     Returns:
    #         bool: True if result is valid, False otherwise
    #     """
    #     if not isinstance(result, dict):
    #         logging.warning("Result is not a dictionary")
    #         return False
            
    #     # Check for required top-level fields
    #     required_fields = ["stream_info", "model_configs", "agg_summary"]
    #     for field in required_fields:
    #         if field not in result:
    #             logging.warning(f"Missing required field: {field}")
    #             return False
        
    #     # Validate stream_info structure
    #     stream_info = result.get("stream_info", {})
    #     if not isinstance(stream_info, dict):
    #         logging.warning("stream_info must be a dictionary")
    #         return False
            
    #     # Check for essential stream_info fields
    #     stream_info_required = ["stream_key", "input_order"]
    #     for field in stream_info_required:
    #         if field not in stream_info:
    #             logging.warning(f"Missing required stream_info field: {field}")
    #             return False
        
    #     # Validate stream_key and input_order types
    #     if not isinstance(stream_info.get("stream_key"), str):
    #         logging.warning("stream_key must be a string")
    #         return False
            
    #     if not isinstance(stream_info.get("input_order"), int):
    #         logging.warning("input_order must be an integer")
    #         return False
        
    #     # Validate model_configs
    #     model_configs = result.get("model_configs", [])
    #     if not isinstance(model_configs, list):
    #         logging.warning("model_configs must be a list")
    #         return False
            
    #     # Check each model config
    #     for i, config in enumerate(model_configs):
    #         if not isinstance(config, dict):
    #             logging.warning(f"Model config {i} must be a dictionary")
    #             return False
                
    #         # Check for essential model config fields
    #         config_required = ["deployment_id", "model_output"]
    #         for field in config_required:
    #             if field not in config:
    #                 logging.warning(f"Missing required model config field: {field}")
    #                 return False
        
    #     # Validate agg_summary
    #     agg_summary = result.get("agg_summary", {})
    #     if not isinstance(agg_summary, dict):
    #         logging.warning("agg_summary must be a dictionary")
    #         return False
            
    #     # Check that events and tracking_stats are lists if present
    #     if "events" in agg_summary and not isinstance(agg_summary["events"], list):
    #         logging.warning("agg_summary.events must be a list")
    #         return False
            
    #     if "tracking_stats" in agg_summary and not isinstance(agg_summary["tracking_stats"], list):
    #         logging.warning("agg_summary.tracking_stats must be a list")
    #         return False
        
    #     return True

    # def _enhance_result_for_publishing(self, result: Dict) -> Dict:
    #     """
    #     Enhance the aggregated result with additional metadata for publishing.
        
    #     Args:
    #         result: Aggregated result to enhance
            
    #     Returns:
    #         Enhanced result ready for publishing
    #     """
    #     enhanced_result = result.copy()
        
    #     # Add publishing metadata
    #     enhanced_result["publishing_metadata"] = {
    #         "pipeline_id": self.inference_pipeline_id,
    #         "published_timestamp": time.time(),
    #         "publisher_version": "2.0",
    #         "is_aggregated": True,
    #         "deployment_count": result.get("deployment_count", 0),
    #         "aggregation_type": result.get("aggregation_type", "multi_deployment"),
    #     }
        
    #     # Add strategy summary if available
    #     strategy_results = result.get("strategy_results", {})
    #     if strategy_results:
    #         strategy_summary = {}
    #         for strategy, strategy_data in strategy_results.items():
    #             if isinstance(strategy_data, dict):
    #                 performance_metrics = strategy_data.get("performance_metrics", {})
    #                 strategy_summary[strategy] = {
    #                     "total_outputs": performance_metrics.get("total_outputs", 0),
    #                     "avg_processing_time": performance_metrics.get("avg_processing_time", 0.0),
    #                     "aggregation_type": strategy_data.get("aggregation_type", strategy)
    #                 }
    #         enhanced_result["publishing_metadata"]["strategy_summary"] = strategy_summary
        
    #     # Enhance stream_info with publishing timestamp
    #     if "stream_info" in enhanced_result:
    #         enhanced_result["stream_info"]["published_timestamp"] = time.time()
    #         enhanced_result["stream_info"]["pipeline_id"] = self.inference_pipeline_id
        
    #     # Add final stats to agg_summary
    #     if "agg_summary" in enhanced_result:
    #         enhanced_result["agg_summary"]["publishing_stats"] = {
    #             "total_events": len(enhanced_result["agg_summary"].get("events", [])),
    #             "total_tracking_stats": len(enhanced_result["agg_summary"].get("tracking_stats", [])),
    #             "total_model_configs": len(enhanced_result.get("model_configs", [])),
    #             "aggregation_strategies_count": len(strategy_results),
    #         }
        
    #     return enhanced_result

    def _record_error(self, error_message: str):
        """Record error in statistics."""
        with self._stats_lock:
            self.stats["errors"] += 1
            self.stats["last_error"] = error_message
            self.stats["last_error_time"] = time.time()
        # Reduce logging frequency for performance
        if self.stats["errors"] % 10 == 1:  # Log every 10th error
            logging.error(f"Publisher error (#{self.stats['errors']}): {error_message}")

    def stop_streaming(self):
        """Stop streaming final results."""
        if not self._is_running:
            logging.warning("Final results streaming is not running")
            return
            
        logging.info("Stopping final results streaming...")
        
        # Signal stop and wait for thread
        self._stop_streaming.set()
        
        if self._streaming_thread and self._streaming_thread.is_alive():
            try:
                self._streaming_thread.join(timeout=5.0)
                if self._streaming_thread.is_alive():
                    logging.warning("Final results streaming thread did not stop gracefully")
            except Exception as exc:
                logging.error(f"Error joining streaming thread: {exc}")
        
        # Stop Kafka deployment
        try:
            self.kafka_handler.close()
        except Exception as exc:
            logging.error(f"Error stopping Kafka deployment: {exc}")
        
        self._is_running = False
        self._streaming_thread = None
        
        logging.info("Final results streaming stopped")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get streaming statistics.
        
        Returns:
            Dict containing statistics
        """
        with self._stats_lock:
            stats = self.stats.copy()
            
        stats["is_running"] = self._is_running
        stats["queue_size"] = self.final_results_queue.qsize()
        
        # Calculate success rate
        total_attempts = stats["messages_produced"] + stats["validation_errors"] + stats["kafka_errors"]
        stats["success_rate"] = stats["messages_produced"] / max(total_attempts, 1)
        
        if stats["start_time"]:
            stats["uptime"] = time.time() - stats["start_time"]
            if stats["uptime"] > 0:
                stats["messages_per_second"] = stats["messages_produced"] / stats["uptime"]
        
        return stats

    def get_health_status(self) -> Dict[str, Any]:
        """Get health status of the publisher."""
        health = {
            "status": "healthy",
            "is_running": self._is_running,
            "queue_size": self.final_results_queue.qsize(),
            "errors": self.stats["errors"],
            "validation_errors": self.stats["validation_errors"],
            "kafka_errors": self.stats["kafka_errors"],
            "messages_produced": self.stats["messages_produced"],
        }

        # Check for recent errors (within last 60 seconds)
        if (
            self.stats["last_error_time"]
            and (time.time() - self.stats["last_error_time"]) < 60
        ):
            health["status"] = "degraded"
            health["last_error"] = self.stats["last_error"]
            health["reason"] = f"Recent error: {self.stats['last_error']}"
            logging.warning(f"Publisher degraded due to recent error: {self.stats['last_error']}")

        # Check queue size
        queue_size = self.final_results_queue.qsize()
        if queue_size > 1000:
            health["status"] = "degraded"
            health["reason"] = f"Queue size too large ({queue_size} items)"
            logging.warning(f"Publisher degraded: queue has {queue_size} items (threshold: 100)")

        # Check error rates
        total_attempts = self.stats["messages_produced"] + self.stats["validation_errors"] + self.stats["kafka_errors"]
        if total_attempts > 10:  # Only check after some attempts
            error_rate = (self.stats["validation_errors"] + self.stats["kafka_errors"]) / total_attempts
            if error_rate > 0.1:  # More than 10% error rate
                health["status"] = "degraded"
                health["reason"] = f"High error rate: {error_rate:.2%} ({self.stats['kafka_errors']} kafka, {self.stats['validation_errors']} validation)"
                logging.warning(f"Publisher degraded: high error rate {error_rate:.2%} with {self.stats['kafka_errors']} kafka errors and {self.stats['validation_errors']} validation errors")

        # Check if not running when it should be
        if not self._is_running:
            health["status"] = "unhealthy"
            health["reason"] = "Publisher is not running"
            logging.error("Publisher is not running")

        return health

    @property
    def is_running(self) -> bool:
        """Check if the streamer is currently running."""
        return self._is_running
