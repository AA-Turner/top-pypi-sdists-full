"""Post-processing worker for hybrid stream processing architecture with concurrent processing."""

import asyncio
import logging
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone

from matrice.deploy.server.inference.inference_interface import InferenceInterface


class PostProcessingWorker:
    """Post-processing worker that processes inference results concurrently from input queue and adds final results to output queue."""
    
    def __init__(
        self,
        worker_id: str,
        inference_interface: InferenceInterface,
        input_queue,  # Queue containing inference results
        output_queue,  # Queue for final results
        process_timeout: float = 180.0,
        max_concurrent_tasks: int = 20
    ):
        """Initialize post-processing worker.
        
        Args:
            worker_id: Unique identifier for this worker
            inference_interface: Inference interface for post-processing
            input_queue: Queue to get inference results from
            output_queue: Queue to put final results into
            process_timeout: Timeout for post-processing
            max_concurrent_tasks: Maximum number of concurrent processing tasks
        """
        self.worker_id = worker_id
        self.inference_interface = inference_interface
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.process_timeout = process_timeout
        self.max_concurrent_tasks = max_concurrent_tasks
        
        # Worker state
        self.is_running = False
        self.is_active = True
        self.global_counter = 0
        self._stop_event = asyncio.Event()
        self._processing_task: Optional[asyncio.Task] = None
        
        # Metrics
        self.messages_processed = 0
        self.messages_failed = 0
        self.messages_output = 0
        self.messages_dropped_output = 0
        self.total_processing_time = 0.0
        self.last_processing_time = None
        self.concurrent_tasks_count = 0
        self.max_concurrent_reached = 0
        
        self.logger = logging.getLogger(f"{__name__}.{worker_id}")
        self.logger.info(f"Initialized PostProcessingWorker: {worker_id} (dynamic batch processing up to {max_concurrent_tasks} with gather and order preservation)")
    
    async def start(self) -> None:
        """Start the post-processing worker."""
        if self.is_running:
            self.logger.warning(f"Post-processing worker {self.worker_id} is already running")
            return
        
        self.is_running = True
        self.is_active = True
        self._stop_event.clear()
        
        # Start concurrent processing task
        self._processing_task = asyncio.create_task(self._processing_loop())
        
        self.logger.info(f"Started PostProcessingWorker: {self.worker_id} with concurrent processing")
    
    async def stop(self) -> None:
        """Stop the post-processing worker."""
        if not self.is_running:
            return
        
        self.logger.info(f"Stopping PostProcessingWorker: {self.worker_id}")
        
        self.is_running = False
        self.is_active = False
        self._stop_event.set()
        
        # Cancel and wait for main processing task
        if self._processing_task and not self._processing_task.done():
            self._processing_task.cancel()
            
            try:
                await asyncio.wait_for(self._processing_task, timeout=5.0)
            except asyncio.CancelledError:
                pass
            except asyncio.TimeoutError:
                self.logger.warning(f"Main processing task did not stop within timeout for worker {self.worker_id}")
            except Exception as exc:
                self.logger.error(f"Error stopping main processing task for worker {self.worker_id}: {str(exc)}")
        
        self.logger.info(f"Stopped PostProcessingWorker: {self.worker_id}")
    
    async def _processing_loop(self) -> None:
        """Dynamic batch processing - collect up to max_concurrent_tasks, process with gather, emit in order."""
        
        while self.is_running and not self._stop_event.is_set():
            try:
                # Collect messages up to max_concurrent_tasks
                batch = []
                for _ in range(self.max_concurrent_tasks):
                    try:
                        priority, message = await asyncio.wait_for(self.input_queue.get(), timeout=0.1)
                        batch.append((priority, message))
                    except asyncio.TimeoutError:
                        break  # No more messages, process what we have
                
                if not batch:
                    await asyncio.sleep(0.01)  # No messages, wait a bit
                    continue
                
                self.logger.debug(f"Processing batch of {len(batch)} messages (max_concurrent={self.max_concurrent_tasks})")
                
                # Process all messages in batch concurrently
                tasks = []
                results = [None] * len(batch)
                
                for i, (priority, message) in enumerate(batch):
                    task = asyncio.create_task(self._process_message_for_batch(i, message, priority, results))
                    tasks.append(task)
                
                # Update max concurrent reached metric
                if len(tasks) > self.max_concurrent_reached:
                    self.max_concurrent_reached = len(tasks)
                
                # Wait for all to complete using gather
                await asyncio.gather(*tasks, return_exceptions=True)
                
                # Add all results to output queue in order
                for result in results:
                    if result is not None:
                        try:
                            priority, final_message = result
                            await self.output_queue.put((priority, final_message))
                            self.messages_output += 1
                        except Exception as exc:
                            self.messages_dropped_output += 1
                            self.logger.error(f"Failed to add result to queue: {str(exc)}")
                
                self.logger.debug(f"Added batch of {len([r for r in results if r is not None])} results to queue in order")
                
            except asyncio.CancelledError:
                break
            except Exception as exc:
                self.logger.error(f"Error in processing loop: {str(exc)}")
                await asyncio.sleep(1.0)
        
        self.logger.debug(f"Processing loop ended for post-processing worker {self.worker_id}")
    

    
    async def _process_message_for_batch(self, index: int, message: Dict[str, Any], priority: int, results: list) -> None:
        """Process a single message and store result in the correct position."""
        try:
            start_time = asyncio.get_event_loop().time()
            
            # Extract necessary data from the inference result message
            model_result = message.get("model_result")
            input_content = message.get("input_content")
            stream_key = message.get("message_key")
            stream_info = message.get("stream_info")
            camera_info = message.get("camera_info")
            
            if model_result is None:
                self.logger.warning(f"No model result found for key={stream_key}")
                self.messages_failed += 1
                results[index] = None
                return
            
            # Apply post-processing
            processed_result, post_processing_result = await asyncio.wait_for(
                self.inference_interface._apply_post_processing(
                    model_result,
                    input_content,
                    None,  # post_processing_config - use default
                    stream_key,
                    stream_info,
                    camera_info,
                ),
                timeout=self.process_timeout
            )
            
            # Calculate processing timing
            processing_time = asyncio.get_event_loop().time() - start_time
            
            # Create final result message with timing data
            final_message = self._create_final_result_message(
                message, processed_result, post_processing_result, processing_time
            )
            
            # Store result in correct position
            results[index] = (priority, final_message)
            
            # Update metrics
            self.total_processing_time += processing_time
            self.messages_processed += 1
            self.last_processing_time = datetime.now(timezone.utc)
            
        except asyncio.TimeoutError:
            self.logger.error(f"Post-processing timeout for key={message.get('message_key')}")
            self.messages_failed += 1
            results[index] = None
        except Exception as exc:
            self.logger.error(f"Post-processing error for key={message.get('message_key')}: {str(exc)}")
            self.messages_failed += 1
            results[index] = None
    
    def _create_final_result_message(
        self,
        inference_message: Dict[str, Any],
        processed_result: Any,
        post_processing_result: Optional[Dict[str, Any]],
        processing_time: float = 0.0
    ) -> Dict[str, Any]:
        """Create a final result message from post-processing results."""
        # Extract inference timing from the original inference message
        inference_timing = {}
        if "inference_timing" in inference_message:
            inference_timing = inference_message["inference_timing"]
        elif "server_timing" in inference_message:
            # Legacy compatibility
            server_timing = inference_message["server_timing"]
            inference_timing = {
                "model_inference_time_sec": server_timing.get("model_inference_time_sec", 0.0),
                "inference_total_time_sec": server_timing.get("inference_total_time_sec", 0.0),
                "total_worker_time_sec": server_timing.get("total_worker_time_sec", 0.0),
            }
        
        # Create post-processing timing data
        post_processing_timing = {
            "post_processing_time_sec": processing_time,
            "total_worker_time_sec": processing_time,
            "post_processing_timestamp": datetime.now(timezone.utc),
        }
        
        # Extract additional timing from post_processing_result if available
        if post_processing_result and isinstance(post_processing_result, dict):
            timing_metadata = post_processing_result.get("timing_metadata", {})
            if timing_metadata:
                post_processing_timing.update({
                    "post_processing_time_sec": timing_metadata.get("post_processing_time_sec", processing_time),
                    "output_construct_time_sec": timing_metadata.get("output_construct_time_sec", 0.0),
                })
        
        return {
            "message_key": inference_message.get("message_key"),
            "input_stream": inference_message.get("input_stream"),
            "input_hash": inference_message.get("input_hash"),
            "camera_info": inference_message.get("camera_info"),
            "stream_info": inference_message.get("stream_info"),
            "model_result": processed_result,
            "post_processing_result": post_processing_result,
            "inference_timestamp": inference_message.get("inference_timestamp"),
            "post_processing_timestamp": datetime.now(timezone.utc),
            "inference_worker_id": inference_message.get("inference_worker_id"),
            "post_processing_worker_id": self.worker_id,
            "original_timestamp": inference_message.get("original_timestamp"),
            "consumer_worker_id": inference_message.get("consumer_worker_id"),
            "video_chunk_info": inference_message.get("video_chunk_info"),
            "global_counter": self.global_counter,
            # Add timing data for latency tracking
            "inference_timing": inference_timing,
            "post_processing_timing": post_processing_timing,
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get worker metrics."""
        avg_processing_time = 0.0
        if self.messages_processed > 0:
            avg_processing_time = self.total_processing_time / self.messages_processed
        
        return {
            "worker_id": self.worker_id,
            "is_running": self.is_running,
            "is_active": self.is_active,
            "messages_processed": self.messages_processed,
            "messages_failed": self.messages_failed,
            "messages_output": self.messages_output,
            "messages_dropped_output": self.messages_dropped_output,
            "avg_processing_time": avg_processing_time,
            "total_processing_time": self.total_processing_time,
            "last_processing_time": self.last_processing_time.isoformat() if self.last_processing_time else None,
            "input_queue_size": self.input_queue.qsize(),
            "output_queue_size": self.output_queue.qsize(),
            "max_concurrent_tasks": self.max_concurrent_tasks,
            "max_concurrent_reached": self.max_concurrent_reached,
            "concurrent_tasks_count": self.concurrent_tasks_count,
            "processing_mode": "dynamic_batch_gather",
        }
    
    def reset_metrics(self) -> None:
        """Reset worker metrics."""
        self.messages_processed = 0
        self.messages_failed = 0
        self.messages_output = 0
        self.messages_dropped_output = 0
        self.total_processing_time = 0.0
        self.last_processing_time = None
        self.concurrent_tasks_count = 0
        self.max_concurrent_reached = 0
