"""Module providing stream worker functionality for parallel processing."""

import asyncio
import logging
import time
import uuid
import base64
from typing import Dict, Optional
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
    ):
        """Initialize stream worker.
        
        Args:
            worker_id: Unique identifier for this worker
            session: Session object for authentication and RPC
            deployment_id: ID of the deployment
            deployment_instance_id: ID of the deployment instance
            inference_interface: Inference interface to use for inference
            consumer_group_suffix: Optional suffix for consumer group ID
        """
        self.worker_id = worker_id
        self.session = session
        self.deployment_id = deployment_id
        self.deployment_instance_id = deployment_instance_id
        self.inference_interface = inference_interface
        
        # Kafka setup with unique consumer group for this worker
        consumer_group_id = f"{deployment_id}-worker-{worker_id}"
        if consumer_group_suffix:
            consumer_group_id += f"-{consumer_group_suffix}"
            
        self.kafka_deployment = MatriceKafkaDeployment(
            session,
            deployment_id,
            "server",
            consumer_group_id,
            f"{deployment_instance_id}-{worker_id}",
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
                logging.debug(f"Processing task for worker {self.worker_id} cancelled successfully")
            except asyncio.TimeoutError:
                logging.warning(f"Processing task for worker {self.worker_id} did not cancel within timeout")
            except Exception as exc:
                logging.error(f"Error while cancelling processing task for worker {self.worker_id}: {str(exc)}")
        
        # Close Kafka connections with proper error handling
        if self.kafka_deployment:
            try:
                logging.debug(f"Closing Kafka connections for worker {self.worker_id}")
                # Check if event loop is still running before attempting async close
                try:
                    loop = asyncio.get_running_loop()
                    if loop.is_closed():
                        logging.warning(f"Event loop closed, skipping Kafka close for worker {self.worker_id}")
                    else:
                        await self.kafka_deployment.close()
                        logging.debug(f"Kafka connections closed for worker {self.worker_id}")
                except RuntimeError:
                    logging.warning(f"No running event loop, skipping Kafka close for worker {self.worker_id}")
            except Exception as exc:
                logging.error(f"Error closing Kafka for worker {self.worker_id}: {str(exc)}")
        
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
                logging.error(f"Error in processing loop for worker {self.worker_id}: {str(exc)}")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, max_retry_delay)
        
        logging.debug(f"Processing loop ended for worker {self.worker_id}")
    
    def _extract_stream_key(self, message: Dict) -> str:
        """Extract stream key (camera_id/stream_id) from message for logging."""
        try:
            value = message.get("value", {})
            
            # Try different possible key fields for stream identification
            stream_key = (
                value.get("stream_key") or
                value.get("camera_id") or
                value.get("stream_id") or
                value.get("source_id") or
                value.get("key") or
                message.get("key")
            )
            
            if isinstance(stream_key, bytes):
                stream_key = stream_key.decode('utf-8')
            
            return str(stream_key) if stream_key else "default_stream"
                
        except Exception as exc:
            logging.error(f"Error extracting stream key: {str(exc)}")
            return "default_stream"
    
    async def _process_message(self, message: Dict) -> None:
        """Process a single message."""
        start_time = time.time()
        stream_key = self._extract_stream_key(message)
        
        try:
            # Process the message using the same logic as inference_interface
            processed_result = await self._process_kafka_message(message)
            
            # Produce result back to Kafka with stream key
            await self.kafka_deployment.async_produce_message(
                processed_result,
                key=stream_key
            )
            
            processing_time = time.time() - start_time
            
            logging.debug(f"Worker {self.worker_id} processed message for stream {stream_key} in {processing_time:.3f}s")
            
        except Exception as exc:
            logging.error(f"Worker {self.worker_id} failed to process message for stream {stream_key}: {str(exc)}")
    
    async def _process_kafka_message(self, message: Dict) -> Dict:
        """Process a message from Kafka (same logic as InferenceInterface).

        Args:
            message: Kafka message containing inference request

        Returns:
            Processed result in the new structured format

        Raises:
            ValueError: If message format is invalid
        """
        if not isinstance(message, dict):
            raise ValueError("Invalid message format: expected dictionary")

        # Extract stream key for logging and response
        stream_key = self._extract_stream_key(message)
        

        # Get the value and try to parse it if it's bytes
        value = message.get("value")
        if not value or not isinstance(value, dict):
            raise ValueError("Invalid message format: missing or invalid 'value' field")

        input_order = value.get("input_order")
        metadata = value.get("metadata", {})
        stream_info = metadata.get("stream_info", {})
        input_settings = stream_info.get("input_settings", {})

        input_data = value.get("input")
        if not input_data:
            raise ValueError("Invalid message format: missing 'input' field")

        try:
            input_bytes = base64.b64decode(input_data)
        except Exception as exc:
            raise ValueError(f"Failed to decode base64 input: {str(exc)}")

        # Timing for model processing
        model_start_time = time.time()
        
        # Extract enhanced metadata for better processing
        fps = stream_info.get("fps", 30)
        original_fps = stream_info.get("original_fps", fps)
        frame_sample_rate = stream_info.get("frame_sample_rate", 1.0)
        video_timestamp = stream_info.get("video_timestamp", 0.0)
        is_video_chunk = input_settings.get("is_video_chunk", False)
        chunk_duration = input_settings.get("chunk_duration_seconds", 0.0)
        video_properties = input_settings.get("video_properties", {})
        
        try:
            result, post_processing_result = await self.inference_interface.inference(
                input_bytes, 
                apply_post_processing=True,
                stream_key=stream_key,
                stream_info=stream_info
            )
            
            model_process_time = time.time() - model_start_time
            total_process_time = model_process_time  # For now, same as model time

            # Enhanced structure the response in the new format with improved metadata
            structured_response = {
                "stream_info": {
                    "stream_key": stream_key,
                    "fps": fps,
                    "original_fps": original_fps,  # Added original FPS
                    "frame_sample_rate": frame_sample_rate,  # Added frame sample rate
                    "video_timestamp": video_timestamp,  # Added video timestamp
                    "stream_time": stream_info.get("stream_time", 
                                                 datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")),
                    "is_video_chunk": is_video_chunk,  # Added video chunk flag
                    "chunk_duration_seconds": chunk_duration,  # Added chunk duration
                    "input_settings": [{
                        "video_file": input_settings.get("video_file"),
                        "camera_id": input_settings.get("camera_id"),
                        "location_info": input_settings.get("location_info"),
                        "start_frame": input_settings.get("start_frame", input_order),
                        "end_frame": input_settings.get("end_frame", input_order),
                        "stream_key": stream_key,
                        "video_format": input_settings.get("video_format"),
                        "video_properties": video_properties,  # Added video properties
                        "quality": input_settings.get("quality"),
                        "width": input_settings.get("width"),
                        "height": input_settings.get("height"),
                        "stream_type": input_settings.get("stream_type"),  # Added stream type
                    }]
                },
                "model_configs": [{
                    "deployment_id": self.deployment_id,
                    "model_input": {
                        "start_frame": input_settings.get("start_frame", input_order),
                        "end_frame": input_settings.get("end_frame", input_order),
                        "stream_key": stream_key,
                        "video_timestamp": video_timestamp,  # Added video timestamp
                        "frame_sample_rate": frame_sample_rate,  # Added frame sample rate
                        "is_video_chunk": is_video_chunk,  # Added video chunk flag
                        "chunk_duration_seconds": chunk_duration,  # Added chunk duration
                    },
                    "model_process_time_sec": round(model_process_time, 3),
                    "total_process_time_sec": round(total_process_time, 3),
                    "model_output": {
                        "raw_output": result,
                        "is_video_chunk": is_video_chunk,  # Flag to help with processing
                        "original_fps": original_fps,  # Include original FPS in output
                        "frame_sample_rate": frame_sample_rate,  # Include frame sample rate
                    }
                }],
                "agg_summary": {
                    "events": [],
                    "tracking_stats": []
                }
            }

            # Add post-processing results to agg_summary if available
            if post_processing_result and isinstance(post_processing_result, dict):
                if post_processing_result.get("status") == "success":
                    # Extract events and tracking stats from post-processing result
                    processed_data = post_processing_result.get("processed_data", {})
                    
                    # Add events if available
                    if "events" in processed_data:
                        structured_response["agg_summary"]["events"] = processed_data["events"]
                    
                    # Add tracking stats if available
                    if "tracking_stats" in processed_data:
                        structured_response["agg_summary"]["tracking_stats"] = processed_data["tracking_stats"]
                    
                    # If no specific events/tracking_stats, create from summary/insights
                    if not structured_response["agg_summary"]["events"] and not structured_response["agg_summary"]["tracking_stats"]:
                        summary = post_processing_result.get("summary", "")
                        insights = post_processing_result.get("insights", [])
                        
                        if summary or insights:
                            structured_response["agg_summary"]["tracking_stats"] = [{
                                "tracking_start_time": stream_info.get("stream_time", 
                                                                     datetime.now(timezone.utc).strftime("%Y-%m-%d")),
                                "all_results_for_tracking": post_processing_result,
                                "human_text": f"{summary}\n" + "\n".join(insights) if insights else summary
                            }]

            # Enhanced original metadata for backward compatibility
            structured_response["original_metadata"] = {
                "input_order": input_order,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "worker_id": self.worker_id,
                "post_processing_applied": post_processing_result is not None,
                "stream_key": stream_key,  # Include the stream key in response
                "fps": fps,
                "original_fps": original_fps,  # Added original FPS
                "frame_sample_rate": frame_sample_rate,  # Added frame sample rate
                "video_timestamp": video_timestamp,  # Added video timestamp
                "is_video_chunk": is_video_chunk,  # Added video chunk flag
                "chunk_duration_seconds": chunk_duration,  # Added chunk duration
                "video_properties": video_properties,  # Added video properties
            }
            
            return structured_response
            
        except Exception as exc:
            model_process_time = time.time() - model_start_time
            
            error_response = {
                "stream_info": {
                    "fps": fps,
                    "original_fps": original_fps,  # Added original FPS
                    "frame_sample_rate": frame_sample_rate,  # Added frame sample rate
                    "video_timestamp": video_timestamp,  # Added video timestamp
                    "stream_time": stream_info.get("stream_time", 
                                                 datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")),
                    "is_video_chunk": is_video_chunk,  # Added video chunk flag
                    "chunk_duration_seconds": chunk_duration,  # Added chunk duration
                    "input_settings": [{
                        "video_file": input_settings.get("video_file"),
                        "camera_id": input_settings.get("camera_id"),
                        "location_info": None,
                        "start_frame": input_settings.get("start_frame", input_order),
                        "end_frame": input_settings.get("end_frame", input_order),
                        "stream_key": stream_key,
                        "video_format": input_settings.get("video_format"),
                        "video_properties": video_properties,  # Added video properties
                        "stream_type": input_settings.get("stream_type"),  # Added stream type
                    }]
                },
                "model_configs": [{
                    "deployment_id": self.deployment_id,
                    "model_input": {
                        "start_frame": input_settings.get("start_frame", input_order),
                        "end_frame": input_settings.get("end_frame", input_order),
                        "stream_key": stream_key,
                        "video_timestamp": video_timestamp,  # Added video timestamp
                        "frame_sample_rate": frame_sample_rate,  # Added frame sample rate
                        "is_video_chunk": is_video_chunk,  # Added video chunk flag
                        "chunk_duration_seconds": chunk_duration,  # Added chunk duration
                    },
                    "model_process_time_sec": round(model_process_time, 3),
                    "total_process_time_sec": round(model_process_time, 3),
                    "model_output": {
                        "raw_output": None,
                        "error": str(exc),
                        "is_video_chunk": is_video_chunk,  # Flag to help with error handling
                        "original_fps": original_fps,  # Include original FPS in error response
                        "frame_sample_rate": frame_sample_rate,  # Include frame sample rate
                    }
                }],
                "agg_summary": {
                    "events": [{
                        "type": "error",
                        "stream_time": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC"),
                        "level": "critical",
                        "intensity": 5,
                        "config": {"min_value": 0, "max_value": 10, "level_settings": {"info": 2, "warning": 5, "critical": 7}},
                        "application_name": "Model Processing",
                        "application_version": "1.0",
                        "location_info": None,
                        "human_text": f"Event: Processing Error\nLevel: Critical\nTime: {datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S.%f UTC')}\nError: {str(exc)}"
                    }],
                    "tracking_stats": []
                },
                "original_metadata": {
                    "input_order": input_order,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "worker_id": self.worker_id,
                    "error": str(exc),
                    "stream_key": stream_key,
                    "fps": fps,
                    "original_fps": original_fps,  # Added original FPS
                    "frame_sample_rate": frame_sample_rate,  # Added frame sample rate
                    "video_timestamp": video_timestamp,  # Added video timestamp
                    "is_video_chunk": is_video_chunk,  # Added video chunk flag
                    "chunk_duration_seconds": chunk_duration,  # Added chunk duration
                    "video_properties": video_properties,  # Added video properties
                }
            }

            return error_response
    

class StreamWorkerManager:
    """Manages multiple stream workers for parallel processing."""
    
    def __init__(
        self,
        session,
        deployment_id: str,
        deployment_instance_id: str,
        inference_interface: InferenceInterface,
        num_workers: int = 1,
    ):
        """Initialize stream worker manager.
        
        Args:
            session: Session object for authentication and RPC
            deployment_id: ID of the deployment
            deployment_instance_id: ID of the deployment instance
            inference_interface: Inference interface to use for inference
            num_workers: Number of workers to create
        """
        self.session = session
        self.deployment_id = deployment_id
        self.deployment_instance_id = deployment_instance_id
        self.inference_interface = inference_interface
        self.num_workers = num_workers
        
        # Worker management
        self.workers: Dict[str, StreamWorker] = {}
        self.is_running = False
        
        logging.info(f"Initialized StreamWorkerManager with {num_workers} workers for deployment {deployment_id}")
    
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
                    logging.error(f"Error creating stop task for worker {worker_id}: {str(exc)}")
            
            # Wait for all workers to stop with timeout
            if stop_tasks:
                try:
                    await asyncio.wait_for(
                        asyncio.gather(*stop_tasks, return_exceptions=True), 
                        timeout=30.0
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
            workers_to_remove = list(self.workers.keys())[:current_count - target_count]
            for worker_id in workers_to_remove:
                await self.remove_worker(worker_id)
        
        logging.info(f"Scaled workers from {current_count} to {target_count}")
        return True
