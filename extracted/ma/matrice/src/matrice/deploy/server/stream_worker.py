"""Module providing stream worker functionality for parallel processing."""

import asyncio
import logging
import time
import uuid
import base64
from typing import Dict, Optional, List
from datetime import datetime, timezone
from matrice.deploy.utils.kafka_utils import MatriceKafkaDeployment
from matrice.deploy.server.inference.inference_interface import InferenceInterface


class StreamWorker:
    """Individual worker for processing stream messages in parallel."""

    def __init__(
        self,
        worker_id: str,
        session,
        deployment_id: str,
        deployment_instance_id: str,
        inference_interface: InferenceInterface,
        consumer_group_suffix: str = "",
        app_name: str = "",
        app_version: str = "",
        inference_pipeline_id: str = "",
    ):
        """Initialize stream worker.

        Args:
            worker_id: Unique identifier for this worker
            session: Session object for authentication and RPC
            deployment_id: ID of the deployment
            deployment_instance_id: ID of the deployment instance
            inference_interface: Inference interface to use for inference
            consumer_group_suffix: Optional suffix for consumer group ID
            app_name: Application name for result formatting
            app_version: Application version for result formatting
            inference_pipeline_id: Inference pipeline ID
        """
        self.worker_id = worker_id
        self.session = session
        self.deployment_id = deployment_id
        self.deployment_instance_id = deployment_instance_id
        self.inference_interface = inference_interface
        self.app_name = app_name
        self.app_version = app_version
        self.inference_pipeline_id = inference_pipeline_id
        # Kafka setup with unique consumer group for this worker
        consumer_group_id = f"{deployment_id}-worker-{worker_id}"
        if consumer_group_suffix:
            consumer_group_id += f"-{consumer_group_suffix}"

        custom_request_service_id = (
            self.inference_pipeline_id
            if (
                self.inference_pipeline_id
                and self.inference_pipeline_id != "000000000000000000000000"
            )
            else deployment_id
        )

        self.kafka_deployment = MatriceKafkaDeployment(
            session,
            deployment_id,
            "server",
            consumer_group_id,
            f"{deployment_instance_id}-{worker_id}",
            custom_request_service_id=custom_request_service_id
        )

        # Worker state
        self.is_running = False
        self.is_active = True

        # Processing control
        self._stop_event = asyncio.Event()
        self._processing_task: Optional[asyncio.Task] = None

        logging.info(f"Initialized StreamWorker: {worker_id}")

    async def start(self) -> None:
        """Start the worker."""
        if self.is_running:
            logging.warning(f"Worker {self.worker_id} is already running")
            return

        self.is_running = True
        self.is_active = True
        self._stop_event.clear()

        # Start the processing loop
        self._processing_task = asyncio.create_task(self._processing_loop())

        logging.info(f"Started StreamWorker: {self.worker_id}")

    async def stop(self) -> None:
        """Stop the worker."""
        if not self.is_running:
            return

        logging.info(f"Stopping StreamWorker: {self.worker_id}")

        self.is_running = False
        self.is_active = False
        self._stop_event.set()

        # Cancel and wait for processing task with timeout
        if self._processing_task and not self._processing_task.done():
            self._processing_task.cancel()
            try:
                # Wait for task cancellation with timeout
                await asyncio.wait_for(self._processing_task, timeout=5.0)
            except asyncio.CancelledError:
                logging.debug(
                    f"Processing task for worker {self.worker_id} cancelled successfully"
                )
            except asyncio.TimeoutError:
                logging.warning(
                    f"Processing task for worker {self.worker_id} did not cancel within timeout"
                )
            except Exception as exc:
                logging.error(
                    f"Error while cancelling processing task for worker {self.worker_id}: {str(exc)}"
                )

        # Close Kafka connections with proper error handling
        if self.kafka_deployment:
            try:
                logging.debug(f"Closing Kafka connections for worker {self.worker_id}")
                # Check if event loop is still running before attempting async close
                try:
                    loop = asyncio.get_running_loop()
                    if loop.is_closed():
                        logging.warning(
                            f"Event loop closed, skipping Kafka close for worker {self.worker_id}"
                        )
                    else:
                        await self.kafka_deployment.close()
                        logging.debug(
                            f"Kafka connections closed for worker {self.worker_id}"
                        )
                except RuntimeError:
                    logging.warning(
                        f"No running event loop, skipping Kafka close for worker {self.worker_id}"
                    )
            except Exception as exc:
                logging.error(
                    f"Error closing Kafka for worker {self.worker_id}: {str(exc)}"
                )

        logging.info(f"Stopped StreamWorker: {self.worker_id}")

    async def _processing_loop(self) -> None:
        """Main processing loop for consuming and processing messages."""
        retry_delay = 1.0
        max_retry_delay = 30.0

        while self.is_running and not self._stop_event.is_set():
            try:
                # Consume message from Kafka
                message = await self.kafka_deployment.async_consume_message(timeout=1.0)

                if message:
                    await self._process_message(message)
                    retry_delay = 1.0  # Reset retry delay on success
                else:
                    # No message available, brief pause
                    await asyncio.sleep(0.1)

            except asyncio.CancelledError:
                break
            except Exception as exc:
                logging.error(
                    f"Error in processing loop for worker {self.worker_id}: {str(exc)}"
                )
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, max_retry_delay)

        logging.debug(f"Processing loop ended for worker {self.worker_id}")

    async def _process_message(self, message: Dict) -> None:
        """Process a single message."""
        try:
            processed_result = await self._process_kafka_message(message)
            await self.kafka_deployment.async_produce_message(
                processed_result, key=message.get("key")
            )
        except Exception as exc:
            logging.error(
                f"Worker {self.worker_id} failed to process message: {str(exc)}"
            )

    async def _process_kafka_message(self, message: Dict) -> Dict:
        """Process a message from Kafka (same logic as InferenceInterface).

        Args:
            message: Kafka message containing inference request

        Returns:
            Processed result in the new app_result structured format

        Raises:
            ValueError: If message format is invalid
        """
        if not isinstance(message, dict):
            raise ValueError("Invalid message format: expected dictionary")

        # Get the value containing the message data
        input_data = message.get("value")
        if not input_data or not isinstance(input_data, dict):
            raise ValueError("Invalid message format: missing or invalid 'value' field")

        input_stream = input_data.get("input_stream", {})
        input_content = input_stream.get("content")
        input_hash = input_stream.get("input_hash")
        camera_info = input_stream.get("camera_info")

        if not input_content:
            raise ValueError(
                "Invalid message format: missing 'content' field in input_content"
            )

        try:
            input_content = base64.b64decode(input_content)
        except Exception as exc:
            raise ValueError(f"Failed to decode base64 input: {str(exc)}")

        try:
            # Create stream_info with input_settings for frame number extraction
            stream_info = {
                "input_settings": {
                    "start_frame": input_stream.get("start_frame"),
                    "end_frame": input_stream.get("end_frame"),
                    "stream_unit": input_stream.get("stream_unit"),
                    "input_order": input_stream.get("input_order"),
                    "original_fps": input_stream.get("original_fps",31),
                }
            }

            model_result, post_processing_result = await self.inference_interface.inference(
                input_content,
                apply_post_processing=True,
                stream_key=message.get("key"),
                stream_info=stream_info,
                camera_info=camera_info,
                input_hash=input_hash
            )

            # Extract agg_summary from post-processing result
            agg_summary = {}
            if post_processing_result and isinstance(post_processing_result, dict):
                agg_summary = post_processing_result.get("agg_summary", {})

            output_stream = {
                "output_name": "detection_0",
                "output_unit": "detection",
                "output_stream": {
                    "broker": self.kafka_deployment.bootstrap_server,
                    "topic": self.kafka_deployment.producing_topic,
                    "stream_time": self._get_high_precision_timestamp(),
                },
            }

            app_result = {
                "application_name": self.app_name,
                "application_key_name": self.app_name.replace(" ", "_").replace("-", "_"), 
                "application_version": self.app_version,
                "ip_key_name": "TODO",
                "camera_info": camera_info,
                "input_streams": [input_data],
                "output_streams": [output_stream],
                "model_streams": [
                    {
                        "model_name": "detection_0",
                        "mp_order": 0,
                        "model_stream": {
                            "deployment_id": self.deployment_id,
                            "deployment_instance": self.deployment_instance_id,
                            # "input_streams": [input_data],  # TODO: check if should be added when having multiple models
                            # "output_streams": [output_stream],  # TODO: check if should be added when having multiple models
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
            }

            return self._clean_stream_result(app_result)

        except Exception as exc:
            logging.error(f"Error in _process_kafka_message for worker {self.worker_id}: {str(exc)}", exc_info=True)
            return {}

    def _get_high_precision_timestamp(self) -> str:
        """Get high precision timestamp with microsecond granularity."""
        return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

    def _clean_stream_result(self, stream_result: Dict) -> Dict:
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

class StreamWorkerManager:
    """Manages multiple stream workers for parallel processing."""

    def __init__(
        self,
        session,
        deployment_id: str,
        deployment_instance_id: str,
        inference_interface: InferenceInterface,
        num_workers: int = 1,
        app_name: str = "",
        app_version: str = "",
        inference_pipeline_id: str = "",
    ):
        """Initialize stream worker manager.

        Args:
            session: Session object for authentication and RPC
            deployment_id: ID of the deployment
            deployment_instance_id: ID of the deployment instance
            inference_interface: Inference interface to use for inference
            num_workers: Number of workers to create
            app_name: Application name for result formatting
            app_version: Application version for result formatting
            inference_pipeline_id: Inference pipeline ID
        """
        self.session = session
        self.deployment_id = deployment_id
        self.deployment_instance_id = deployment_instance_id
        self.inference_interface = inference_interface
        self.num_workers = num_workers
        self.app_name = app_name
        self.app_version = app_version
        self.inference_pipeline_id = inference_pipeline_id
        # Worker management
        self.workers: Dict[str, StreamWorker] = {}
        self.is_running = False

        logging.info(
            f"Initialized StreamWorkerManager with {num_workers} workers for deployment {deployment_id}"
        )

    async def start(self) -> None:
        """Start all workers."""
        if self.is_running:
            logging.warning("StreamWorkerManager is already running")
            return

        self.is_running = True

        # Create and start workers with staggered delays to avoid race conditions
        for i in range(self.num_workers):
            worker_id = f"worker_{i}_{uuid.uuid4().hex[:8]}"
            worker = StreamWorker(
                worker_id=worker_id,
                session=self.session,
                deployment_id=self.deployment_id,
                deployment_instance_id=self.deployment_instance_id,
                inference_interface=self.inference_interface,
                app_name=self.app_name,
                app_version=self.app_version,
                inference_pipeline_id=self.inference_pipeline_id,
            )

            self.workers[worker_id] = worker

            # Start worker with error handling
            try:
                await worker.start()
                logging.info(f"Started worker {worker_id}")

                # Add staggered delay between worker startups to avoid race conditions
                if i < self.num_workers - 1:  # Don't delay after the last worker
                    await asyncio.sleep(2.0)  # 2 second delay between worker startups

            except Exception as exc:
                logging.error(f"Failed to start worker {worker_id}: {str(exc)}")
                # Remove failed worker from workers dict
                del self.workers[worker_id]

        logging.info(f"Started StreamWorkerManager with {len(self.workers)} workers")

    async def stop(self) -> None:
        """Stop all workers."""
        if not self.is_running:
            return

        logging.info("Stopping StreamWorkerManager...")

        self.is_running = False

        # Stop all workers with timeout and error handling
        if self.workers:
            logging.info(f"Stopping {len(self.workers)} workers...")
            stop_tasks = []

            for worker_id, worker in self.workers.items():
                try:
                    stop_task = asyncio.create_task(worker.stop())
                    stop_tasks.append(stop_task)
                except Exception as exc:
                    logging.error(
                        f"Error creating stop task for worker {worker_id}: {str(exc)}"
                    )

            # Wait for all workers to stop with timeout
            if stop_tasks:
                try:
                    await asyncio.wait_for(
                        asyncio.gather(*stop_tasks, return_exceptions=True),
                        timeout=30.0,
                    )
                    logging.info("All workers stopped successfully")
                except asyncio.TimeoutError:
                    logging.warning("Some workers did not stop within timeout")
                    # Cancel remaining tasks
                    for task in stop_tasks:
                        if not task.done():
                            task.cancel()
                except Exception as exc:
                    logging.error(f"Error stopping workers: {str(exc)}")

        self.workers.clear()

        logging.info("Stopped StreamWorkerManager")

    async def add_worker(self) -> Optional[str]:
        """Add a new worker to the pool.

        Returns:
            Worker ID if successfully added, None otherwise
        """
        if not self.is_running:
            logging.warning("Cannot add worker: manager not running")
            return None

        worker_id = f"worker_{len(self.workers)}_{uuid.uuid4().hex[:8]}"
        worker = StreamWorker(
            worker_id=worker_id,
            session=self.session,
            deployment_id=self.deployment_id,
            deployment_instance_id=self.deployment_instance_id,
            inference_interface=self.inference_interface,
            app_name=self.app_name,
            app_version=self.app_version,
            inference_pipeline_id=self.inference_pipeline_id,
        )

        self.workers[worker_id] = worker
        await worker.start()

        logging.info(f"Added new worker: {worker_id}")
        return worker_id

    async def remove_worker(self, worker_id: str) -> bool:
        """Remove a worker from the pool.

        Args:
            worker_id: ID of the worker to remove

        Returns:
            True if successfully removed
        """
        if worker_id not in self.workers:
            return False

        worker = self.workers[worker_id]
        await worker.stop()
        del self.workers[worker_id]

        logging.info(f"Removed worker: {worker_id}")
        return True

    async def scale_workers(self, target_count: int) -> bool:
        """Scale workers to target count.

        Args:
            target_count: Target number of workers

        Returns:
            True if scaling was successful
        """
        if not self.is_running:
            logging.warning("Cannot scale workers: manager not running")
            return False

        current_count = len(self.workers)

        if target_count > current_count:
            # Scale up
            for _ in range(target_count - current_count):
                worker_id = await self.add_worker()
                if not worker_id:
                    logging.error("Failed to add worker during scale up")
                    return False

        elif target_count < current_count:
            # Scale down
            workers_to_remove = list(self.workers.keys())[
                : current_count - target_count
            ]
            for worker_id in workers_to_remove:
                await self.remove_worker(worker_id)

        logging.info(f"Scaled workers from {current_count} to {target_count}")
        return True
