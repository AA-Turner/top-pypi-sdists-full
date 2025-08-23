"""Kafka producer worker for hybrid stream processing architecture."""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone

from matrice.deploy.stream.kafka_stream import MatriceKafkaDeployment


class KafkaProducerWorker:
    """Kafka producer worker that consumes from output queue and produces to topics."""
    
    def __init__(
        self,
        worker_id: str,
        session,
        deployment_id: str,
        deployment_instance_id: str,
        output_queue,  # Simple queue wrapper
        app_name: str = "",
        app_version: str = "",
        produce_timeout: float = 60.0,
        inference_pipeline_id: str = ""
    ):
        """Initialize Kafka producer worker.
        
        Args:
            worker_id: Unique identifier for this worker
            session: Session object for authentication and RPC
            deployment_id: ID of the deployment
            deployment_instance_id: ID of the deployment instance
            output_queue: Queue to get result messages from
            app_name: Application name for result formatting
            app_version: Application version for result formatting
            produce_timeout: Timeout for producing to Kafka
            inference_pipeline_id: ID of the inference pipeline
        """
        self.worker_id = worker_id
        self.session = session
        self.deployment_id = deployment_id
        self.deployment_instance_id = deployment_instance_id
        self.output_queue = output_queue
        self.app_name = app_name
        self.app_version = app_version
        self.produce_timeout = produce_timeout
        self.inference_pipeline_id = inference_pipeline_id
        # Kafka setup for producer (no consumer group needed)
        self.kafka_deployment = MatriceKafkaDeployment(
            session,
            deployment_id,
            "server",
            f"{deployment_id}-producer-{worker_id}",  # Not used for producer
            f"{deployment_instance_id}-producer-{worker_id}",
        )
        # Note: async producer setup moved to start() method

        # Worker state
        self.is_running = False
        self.is_active = True
        self._stop_event = asyncio.Event()
        self._processing_task: Optional[asyncio.Task] = None
        
        # Metrics
        self.messages_consumed = 0
        self.messages_produced = 0
        self.messages_failed = 0
        self.last_produce_time = None
        
        self.logger = logging.getLogger(f"{__name__}.{worker_id}")
        self.logger.info(f"Initialized KafkaProducerWorker: {worker_id}")
    
    async def start(self) -> None:
        """Start the producer worker."""
        if self.is_running:
            self.logger.warning(f"Producer worker {self.worker_id} is already running")
            return
        
        # Check if event loop is available before starting
        try:
            loop = asyncio.get_running_loop()
            if loop.is_closed():
                raise RuntimeError("Event loop is closed, cannot start producer worker")
        except RuntimeError as exc:
            if "no running event loop" in str(exc).lower():
                raise RuntimeError("No event loop available for producer worker startup")
            raise
        
        self.is_running = True
        self.is_active = True
        self._stop_event.clear()
        
        # Set up async producer now that we have a valid event loop
        try:
            producer_setup_success = await self.kafka_deployment._ensure_async_producer()
            if not producer_setup_success:
                raise RuntimeError("Failed to set up async Kafka producer")
            self.logger.debug(f"Async producer set up successfully for worker {self.worker_id}")
        except Exception as exc:
            self.is_running = False
            self.is_active = False
            self.logger.error(f"Failed to set up async producer for worker {self.worker_id}: {str(exc)}")
            raise RuntimeError(f"Failed to set up async producer: {str(exc)}")
        
        # Start the processing loop
        self._processing_task = asyncio.create_task(self._processing_loop())
        
        self.logger.info(f"Started KafkaProducerWorker: {self.worker_id}")
    
    async def stop(self) -> None:
        """Stop the producer worker."""
        if not self.is_running:
            return
        
        self.logger.info(f"Stopping KafkaProducerWorker: {self.worker_id}")
        
        self.is_running = False
        self.is_active = False
        self._stop_event.set()
        
        # Cancel and wait for processing task
        if self._processing_task and not self._processing_task.done():
            self._processing_task.cancel()
            try:
                await asyncio.wait_for(self._processing_task, timeout=5.0)
            except (asyncio.CancelledError, asyncio.TimeoutError):
                pass
            except Exception as exc:
                self.logger.error(f"Error stopping producer worker {self.worker_id}: {str(exc)}")
        
        # Close Kafka connections gracefully
        if self.kafka_deployment:
            try:
                # Check if event loop is still running before attempting async cleanup
                try:
                    loop = asyncio.get_running_loop()
                    if loop.is_closed():
                        self.logger.warning(f"Event loop is closed, skipping async Kafka cleanup for worker {self.worker_id}")
                        return
                except RuntimeError:
                    self.logger.warning(f"No running event loop, skipping async Kafka cleanup for worker {self.worker_id}")
                    return
                
                await self.kafka_deployment.close()
                self.logger.debug(f"Kafka connections closed for worker {self.worker_id}")
            except Exception as exc:
                # Log but don't raise - we want to complete the shutdown
                self.logger.error(f"Error closing Kafka for producer worker {self.worker_id}: {str(exc)}")
        
        self.logger.info(f"Stopped KafkaProducerWorker: {self.worker_id}")
    
    async def _processing_loop(self) -> None:
        """Main processing loop for producing messages to Kafka."""
        retry_delay = 1.0
        max_retry_delay = 30.0
        consecutive_errors = 0
        loop_count = 0
        
        while self.is_running and not self._stop_event.is_set():
            try:
                loop_count += 1
                # Log every 100 loops to show producer is active
                if loop_count % 100 == 1:
                    self.logger.debug(
                        f"Producer {self.worker_id} active (loop #{loop_count}) - queue size: {self.output_queue.qsize()}"
                    )
                
                # Single-message produce
                try:
                    priority, message = await self.output_queue.get()
                except asyncio.TimeoutError:
                    # Log periodically when queue is empty
                    if loop_count % 50 == 1:
                        self.logger.debug(
                            f"Producer {self.worker_id} waiting - no messages in output queue (size: {self.output_queue.qsize()})"
                        )
                    await asyncio.sleep(0.1)
                    continue
                try:
                    # Debug before construct
                    try:
                        key_dbg = message.get("message_key")
                        has_pp = bool(message.get("post_processing_result"))
                        self.logger.debug(
                            f"Producing key={key_dbg} pp={'yes' if has_pp else 'no'} out_q={self.output_queue.qsize()}"
                        )
                    except Exception:
                        pass
                    
                    output_message = self._construct_output_stream(message)
                    
                    # Attempt to produce message with error handling for event loop issues
                    try:
                        await asyncio.wait_for(
                            self.kafka_deployment.async_produce_message(
                                output_message,
                                key=message.get("message_key")
                            ),
                            timeout=self.produce_timeout
                        )
                        self.messages_consumed += 1
                        self.messages_produced += 1
                        self.last_produce_time = datetime.now(timezone.utc)
                        try:
                            self.logger.debug(
                                f"Produced key={message.get('message_key')} topic={self.kafka_deployment.producing_topic}"
                            )
                        except Exception:
                            pass
                        retry_delay = 1.0
                        consecutive_errors = 0
                    except RuntimeError as exc:
                        error_msg = str(exc)
                        if any(phrase in error_msg for phrase in [
                            "event loop is closed", "no event loop available", 
                            "event loop is shutting down", "cannot schedule new futures after shutdown"
                        ]):
                            self.logger.error(
                                f"Producer worker {self.worker_id} cannot produce due to event loop state: {error_msg}. "
                                "This may indicate shutdown is in progress."
                            )
                            # Don't count this as a failed message since it's likely due to shutdown
                            # Break instead of continue to stop processing gracefully
                            break
                        else:
                            self.logger.error(f"Runtime error producing message in producer worker {self.worker_id}: {error_msg}")
                            self.messages_failed += 1
                            
                except asyncio.TimeoutError:
                    self.logger.error(f"Timeout producing message in producer worker {self.worker_id}")
                    self.messages_failed += 1
                except Exception as exc:
                    self.logger.error(f"Error producing message in producer worker {self.worker_id}: {str(exc)}")
                    self.messages_failed += 1
             
            except asyncio.CancelledError:
                break
            except Exception as exc:
                consecutive_errors += 1
                self.logger.error(
                    f"Error in producer loop for worker {self.worker_id} (error #{consecutive_errors}): {str(exc)}"
                )
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 1.5, max_retry_delay)
                
                # If too many consecutive errors, pause longer
                if consecutive_errors >= 5:
                    self.logger.error(f"Too many consecutive errors in producer worker {self.worker_id}, pausing...")
                    await asyncio.sleep(max_retry_delay)
                    consecutive_errors = 0
        
        self.logger.debug(f"Processing loop ended for producer worker {self.worker_id}")
    
    def _construct_output_stream(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Construct output stream message from inference result.
        
        Args:
            message: Result message from inference worker
            
        Returns:
            Formatted output message for Kafka
        """
        model_result = message.get("model_result", {})
        post_processing_result = message.get("post_processing_result", {})
        camera_info = message.get("camera_info", {})
        input_stream = message.get("input_stream", {})
        
        # Extract aggregation summary from post-processing result
        agg_summary = {}
        if post_processing_result and isinstance(post_processing_result, dict):
            agg_summary = post_processing_result.get("agg_summary", {})
        
        # Create output stream metadata
        output_stream = {
            "output_name": "detection_0",
            "output_unit": "detection",
            "output_stream": {
                "broker": self.kafka_deployment.bootstrap_server,
                "topic": self.kafka_deployment.producing_topic,
                "stream_time": self._get_high_precision_timestamp(),
            },
        }
        
        # Construct the application result structure
        app_result = {
            "application_name": self.app_name,
            "application_key_name": self.app_name.replace(" ", "_").replace("-", "_"),
            "application_version": self.app_version,
            "ip_key_name": "TODO",
            "camera_info": camera_info,
            "input_streams": [{"input_stream": input_stream}], # TODO: Update in the aggregator and FE to use input_streams directly
            "output_streams": [output_stream],
            "input_hash": message.get("input_hash"),
            "model_streams": [
                {
                    "model_name": "detection_0",
                    "mp_order": 0,
                    "model_stream": {
                        "deployment_id": self.deployment_id,
                        "deployment_instance": self.deployment_instance_id,
                        "model_outputs": [
                            {
                                "output_name": "detection_0",
                                "detections": model_result,
                            }
                        ],
                        "latency_stats": {
                            "model_latency_sec": "TODO",
                            "last_read_time_sec": "TODO",
                            "last_write_time_sec": "TODO",
                            "last_process_time_sec": "TODO",
                        },
                    },
                }
            ],
            "agg_summary": agg_summary or {},
            "latency_stats": {
                "app_e2e_sec": "TODO",
                "last_input_feed_sec": "TODO",
                "last_output_sec": "TODO",
            },
            # Add processing metadata
            "processing_metadata": {
                "consumer_worker_id": message.get("consumer_worker_id"),
                "inference_worker_id": message.get("inference_worker_id"),
                "producer_worker_id": self.worker_id,
                "original_timestamp": message.get("original_timestamp"),
                "inference_timestamp": message.get("inference_timestamp"),
                "produce_timestamp": datetime.now(timezone.utc),
            }
        }
        
        return self._clean_stream_result(self._make_json_safe(app_result))
    
    def _make_json_safe(self, value: Any) -> Any:
        """Convert value to a JSON-safe type."""
        if isinstance(value, dict):
            return {str(k): self._make_json_safe(v) for k, v in value.items()}
        elif isinstance(value, (list, tuple, set)):
            return [self._make_json_safe(v) for v in value]
        elif isinstance(value, (str, int, float, bool)) or value is None:
            return value
        elif isinstance(value, datetime):
            return value.isoformat()
        else:
            return str(value)
    
    def _get_high_precision_timestamp(self) -> str:
        """Get high precision timestamp with microsecond granularity."""
        return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
    
    def _clean_stream_result(self, stream_result: Dict[str, Any]) -> Dict[str, Any]:
        """Clean stream result to remove unnecessary fields."""
        
        def remove_latency_stats(data):
            if isinstance(data, dict):
                new_data = {}
                for key, value in data.items():
                    if key != "latency_stats":
                        new_data[key] = remove_latency_stats(value)
                return new_data
            elif isinstance(data, list):
                return [remove_latency_stats(item) for item in data]
            else:
                return data
        
        return remove_latency_stats(stream_result)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get worker metrics."""
        return {
            "worker_id": self.worker_id,
            "is_running": self.is_running,
            "is_active": self.is_active,
            "messages_consumed": self.messages_consumed,
            "messages_produced": self.messages_produced,
            "messages_failed": self.messages_failed,
            "last_produce_time": self.last_produce_time.isoformat() if self.last_produce_time else None,
            "output_queue_size": self.output_queue.qsize(),
        }
    
    def reset_metrics(self) -> None:
        """Reset worker metrics."""
        self.messages_consumed = 0
        self.messages_produced = 0
        self.messages_failed = 0
        self.last_produce_time = None