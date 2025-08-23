"""Kafka consumer worker for hybrid stream processing architecture."""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone

from matrice.deploy.stream.kafka_stream import MatriceKafkaDeployment
from matrice.deploy.optimize.transmission import ServerTransmissionHandler


class KafkaConsumerWorker:
    """Kafka consumer worker that polls from topics and adds to input queue."""
    
    def __init__(
        self,
        worker_id: str,
        session,
        deployment_id: str,
        deployment_instance_id: str,
        input_queue: asyncio.PriorityQueue,  # Simple queue wrapper
        consumer_group_suffix: str = "",
        poll_timeout: float = 1.0,
        max_messages_per_poll: int = 1,
        inference_pipeline_id: str = "",
        app_name: str = ""
    ):
        """Initialize Kafka consumer worker.
        
        Args:
            worker_id: Unique identifier for this worker
            session: Session object for authentication and RPC
            deployment_id: ID of the deployment
            deployment_instance_id: ID of the deployment instance
            input_queue: Queue to put consumed messages into
            consumer_group_suffix: Optional suffix for consumer group ID
            poll_timeout: Timeout for Kafka polling
            max_messages_per_poll: Maximum messages to consume in one poll
        """
        self.worker_id = worker_id
        self.session = session
        self.deployment_id = deployment_id
        self.deployment_instance_id = deployment_instance_id
        self.input_queue = input_queue
        self.poll_timeout = poll_timeout
        self.max_messages_per_poll = max_messages_per_poll
        self.inference_pipeline_id = inference_pipeline_id
        self.app_name = app_name.lower().replace(" ", "_")
        # Kafka setup with unique consumer group for this worker
        custom_request_service_id = (
            self.inference_pipeline_id
            if (
                self.inference_pipeline_id
                and self.inference_pipeline_id != "000000000000000000000000"
            )
            else deployment_id
        )
        consumer_group_id = f"{custom_request_service_id}-consumer-{app_name}"
        if consumer_group_suffix:
            consumer_group_id += f"-{consumer_group_suffix}"
        self.kafka_deployment = MatriceKafkaDeployment(
            session,
            deployment_id,
            "server",
            consumer_group_id,
            f"{consumer_group_id}-{worker_id}",
            custom_request_service_id=custom_request_service_id
        )
        # Note: async consumer setup moved to start() method
        
        # Worker state
        self.is_running = False
        self.is_active = True
        self.global_counter = 0
        self._stop_event = asyncio.Event()
        self._processing_task: Optional[asyncio.Task] = None
        
        # Metrics
        self.messages_consumed = 0
        self.messages_queued = 0
        self.messages_dropped = 0
        self.last_message_time = None
        
        self.logger = logging.getLogger(f"{__name__}.{worker_id}")
        self.logger.info(f"Initialized KafkaConsumerWorker: {worker_id}")
        # Transmission normalizer
        self.txh = ServerTransmissionHandler()
    
    async def start(self) -> None:
        """Start the consumer worker."""
        if self.is_running:
            self.logger.warning(f"Consumer worker {self.worker_id} is already running")
            return
        
        # Check if event loop is available before starting
        try:
            loop = asyncio.get_running_loop()
            if loop.is_closed():
                raise RuntimeError("Event loop is closed, cannot start consumer worker")
        except RuntimeError as exc:
            if "no running event loop" in str(exc).lower():
                raise RuntimeError("No event loop available for consumer worker startup")
            raise
        
        self.is_running = True
        self.is_active = True
        self._stop_event.clear()
        
        # Set up async consumer now that we have a valid event loop
        try:
            consumer_setup_success = await self.kafka_deployment._ensure_async_consumer()
            if not consumer_setup_success:
                raise RuntimeError("Failed to set up async Kafka consumer")
            self.logger.debug(f"Async consumer set up successfully for worker {self.worker_id}")
        except Exception as exc:
            self.is_running = False
            self.is_active = False
            self.logger.error(f"Failed to set up async consumer for worker {self.worker_id}: {str(exc)}")
            raise RuntimeError(f"Failed to set up async consumer: {str(exc)}")
        
        # Start the processing loop
        self._processing_task = asyncio.create_task(self._processing_loop())
        
        self.logger.info(f"Started KafkaConsumerWorker: {self.worker_id}")
    
    async def stop(self) -> None:
        """Stop the consumer worker."""
        if not self.is_running:
            return
        
        self.logger.info(f"Stopping KafkaConsumerWorker: {self.worker_id}")
        
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
                self.logger.error(f"Error stopping consumer worker {self.worker_id}: {str(exc)}")
        
        # Close Kafka connections
        if self.kafka_deployment:
            try:
                await self.kafka_deployment.close()
            except Exception as exc:
                self.logger.error(f"Error closing Kafka for consumer worker {self.worker_id}: {str(exc)}")
        
        self.logger.info(f"Stopped KafkaConsumerWorker: {self.worker_id}")
    
    async def _processing_loop(self) -> None:
        """Main processing loop for consuming messages from Kafka."""
        retry_delay = 1.0
        max_retry_delay = 30.0
        consecutive_errors = 0
        
        while self.is_running and not self._stop_event.is_set():
            try:
                # Single-message consume
                try:
                    message = await self.kafka_deployment.async_consume_message(timeout=60)
                except Exception as exc:
                    self.logger.error(f"Error consuming message: {str(exc)}")
                    message = None

                if not message:
                    await asyncio.sleep(0.1)
                    continue

                try:
                    processed_message = self._process_kafka_message(message)
                    try:
                        key_dbg = processed_message.get("message_key")
                        strat_dbg = processed_message.get("transmission_strategy")
                        hash_dbg = processed_message.get("input_hash")
                        size_dbg = len(processed_message.get("input_content") or b"")
                        self.logger.debug(
                            f"Consumed key={key_dbg} strat={strat_dbg} hash={'set' if hash_dbg else 'none'} bytes={size_dbg} in_q={self.input_queue.qsize()}"
                        )
                    except Exception:
                        pass
                    try:
                        processed_message["global_counter"] = self.global_counter
                        self.global_counter += 1
                        await self.input_queue.put((self.global_counter, processed_message))
                        self.messages_consumed += 1
                        self.messages_queued += 1
                        self.last_message_time = datetime.now(timezone.utc)
                        retry_delay = 1.0
                        consecutive_errors = 0
                    except asyncio.QueueFull:
                        self.messages_dropped += 1
                        self.logger.warning(
                            f"Dropped message in consumer {self.worker_id} - input queue full (size: {self.input_queue.qsize()})"
                        )
                    except Exception as put_exc:
                        self.messages_dropped += 1
                        self.logger.error(
                            f"Failed to put message in queue for consumer {self.worker_id}: {str(put_exc)}"
                        )
                except Exception as exc:
                    self.logger.error(
                        f"Error processing message in consumer {self.worker_id}: {str(exc)}"
                    )
                    self.messages_dropped += 1
                
            except asyncio.CancelledError:
                break
            except Exception as exc:
                consecutive_errors += 1
                self.logger.error(
                    f"Error in consumer loop for worker {self.worker_id} (error #{consecutive_errors}): {str(exc)}"
                )
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 1.5, max_retry_delay)
                
                # If too many consecutive errors, pause longer
                if consecutive_errors >= 10:
                    self.logger.error(f"Too many consecutive errors in consumer {self.worker_id}, pausing...")
                    await asyncio.sleep(max_retry_delay)
                    consecutive_errors = 0
        
        self.logger.debug(f"Processing loop ended for consumer worker {self.worker_id}")
    
    def _process_kafka_message(self, message: Dict) -> Dict[str, Any]:
        """Normalize and process a Kafka message via ServerTransmissionHandler."""
        if not isinstance(message, dict):
            raise ValueError("Invalid message format: expected dictionary")
        input_data = message.get("value")
        if not input_data or not isinstance(input_data, dict):
            raise ValueError("Invalid message format: missing or invalid 'value' field")
        return self.txh.process_input_message(
            raw_message_value=input_data,
            message_key=message.get("key"),
            consumer_worker_id=self.worker_id,
        )
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get worker metrics."""
        return {
            "worker_id": self.worker_id,
            "is_running": self.is_running,
            "is_active": self.is_active,
            "messages_consumed": self.messages_consumed,
            "messages_queued": self.messages_queued,
            "messages_dropped": self.messages_dropped,
            "last_message_time": self.last_message_time.isoformat() if self.last_message_time else None,
            "queue_size": self.input_queue.qsize(),
            "queue_under_backpressure": self.input_queue.full(),
        }
    
    def reset_metrics(self) -> None:
        """Reset worker metrics."""
        self.messages_consumed = 0
        self.messages_queued = 0
        self.messages_dropped = 0
        self.last_message_time = None