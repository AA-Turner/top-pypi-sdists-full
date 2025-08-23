"""Post-processing worker for hybrid stream processing architecture with concurrent processing."""

import asyncio
import logging
import uuid
from typing import Dict, Any, Optional, List, Set
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
        self._active_tasks: Set[asyncio.Task] = set()
        
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
        self.logger.info(f"Initialized PostProcessingWorker: {worker_id} (concurrent processing, max_tasks={max_concurrent_tasks})")
    
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
        
        # Cancel all active tasks
        if self._active_tasks:
            self.logger.info(f"Cancelling {len(self._active_tasks)} active processing tasks...")
            for task in self._active_tasks:
                task.cancel()
            
            # Wait for active tasks to complete
            try:
                await asyncio.wait_for(
                    asyncio.gather(*self._active_tasks, return_exceptions=True),
                    timeout=5.0
                )
            except asyncio.TimeoutError:
                self.logger.warning(f"Some processing tasks did not stop within timeout for worker {self.worker_id}")
            except Exception as exc:
                self.logger.error(f"Error stopping active tasks for worker {self.worker_id}: {str(exc)}")
        
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
        """Main processing loop for concurrent post-processing."""
        retry_delay = 1.0
        max_retry_delay = 10.0
        consecutive_errors = 0
        loop_count = 0
        
        while self.is_running and not self._stop_event.is_set():
            try:
                loop_count += 1
                # Log worker state periodically
                if loop_count % 100 == 1:
                    self.logger.debug(
                        f"Post-processing worker {self.worker_id} active (loop #{loop_count}) - "
                        f"in_q: {self.input_queue.qsize()}, out_q: {self.output_queue.qsize()}, "
                        f"processed: {self.messages_processed}, active_tasks: {len(self._active_tasks)}"
                    )
                
                try:
                    # Clean up completed tasks
                    await self._cleanup_completed_tasks()
                    
                    # Check if we can accept more tasks
                    if len(self._active_tasks) < self.max_concurrent_tasks:
                        # Get a message and start processing concurrently
                        try:
                            priority, message = await asyncio.wait_for(self.input_queue.get(), timeout=1.0)
                            # Start concurrent processing task
                            task = asyncio.create_task(self._process_single_message(message, priority))
                            self._active_tasks.add(task)
                            self.concurrent_tasks_count += 1
                            
                            # Update max concurrent reached metric
                            if len(self._active_tasks) > self.max_concurrent_reached:
                                self.max_concurrent_reached = len(self._active_tasks)
                            
                            retry_delay = 1.0
                            consecutive_errors = 0
                            
                        except asyncio.TimeoutError:
                            # No message available, continue loop
                            pass
                    else:
                        # Wait a bit when at max capacity
                        await asyncio.sleep(0.1)
                    
                except Exception as exc:
                    self.logger.error(
                        f"Error in post-processing worker {self.worker_id}: {str(exc)}"
                    )
                    consecutive_errors += 1
            
            except asyncio.CancelledError:
                break
            except Exception as exc:
                consecutive_errors += 1
                self.logger.error(
                    f"Error in post-processing loop for worker {self.worker_id} (error #{consecutive_errors}): {str(exc)}"
                )
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 1.5, max_retry_delay)
                
                # If too many consecutive errors, pause longer
                if consecutive_errors >= 5:
                    self.logger.error(f"Too many consecutive errors in post-processing worker {self.worker_id}, pausing...")
                    await asyncio.sleep(max_retry_delay)
                    consecutive_errors = 0
        
        self.logger.debug(f"Processing loop ended for post-processing worker {self.worker_id}")
    
    async def _cleanup_completed_tasks(self) -> None:
        """Clean up completed processing tasks."""
        if not self._active_tasks:
            return
        
        # Get completed tasks
        completed_tasks = [task for task in self._active_tasks if task.done()]
        
        # Remove completed tasks
        for task in completed_tasks:
            self._active_tasks.discard(task)
            
            # Check for exceptions in completed tasks
            if not task.cancelled():
                try:
                    task.result()  # This will raise any exception that occurred
                except Exception as exc:
                    self.logger.error(f"Exception in completed post-processing task: {str(exc)}")
    
    async def _process_single_message(self, message: Dict[str, Any], priority: int) -> None:
        """Process a single inference result message."""
        try:
            task_id = f"task_{uuid.uuid4().hex[:8]}"
            self.logger.debug(
                f"Processing single message key={message.get('message_key')} in task {task_id}"
            )
            
            start_time = asyncio.get_event_loop().time()
            
            # Extract necessary data from the inference result message
            model_result = message.get("model_result")
            input_content = message.get("input_content")
            stream_key = message.get("message_key")
            stream_info = message.get("stream_info")
            camera_info = message.get("camera_info")
            
            if model_result is None:
                self.logger.warning(f"No model result found in message for key={stream_key}")
                self.messages_failed += 1
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
            
            # Create final result message
            final_message = self._create_final_result_message(
                message, processed_result, post_processing_result
            )
            
            # Add to output queue
            try:
                await self.output_queue.put((priority, final_message))
                self.messages_output += 1
                self.logger.debug(
                    f"Emitted post-processed result for key={stream_key} task={task_id} out_q={self.output_queue.qsize()}"
                )
            except asyncio.QueueFull:
                self.messages_dropped_output += 1
                self.logger.warning(f"Dropped post-processed result from worker {self.worker_id} - output queue full")
            except Exception as put_exc:
                self.messages_dropped_output += 1
                self.logger.error(f"Failed to put post-processed result to output queue in worker {self.worker_id}: {str(put_exc)}")
            
            # Update metrics
            processing_time = asyncio.get_event_loop().time() - start_time
            self.total_processing_time += processing_time
            self.messages_processed += 1
            self.last_processing_time = datetime.now(timezone.utc)
            
            self.logger.debug(
                f"Post-processing done key={stream_key} task={task_id} time_ms={int(processing_time*1000)}"
            )
            
        except asyncio.TimeoutError:
            self.logger.error(f"Post-processing timeout in task {task_id}")
            self.messages_failed += 1
        except Exception as exc:
            self.logger.error(f"Post-processing error in task {task_id}: {str(exc)}")
            self.messages_failed += 1
    
    def _create_final_result_message(
        self,
        inference_message: Dict[str, Any],
        processed_result: Any,
        post_processing_result: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create a final result message from post-processing results."""
        return {
            "message_key": inference_message.get("message_key"),
            "input_stream": inference_message.get("input_stream"),
            "input_hash": inference_message.get("input_hash"),
            "camera_info": inference_message.get("camera_info"),
            "model_result": processed_result,
            "post_processing_result": post_processing_result,
            "inference_timestamp": inference_message.get("inference_timestamp"),
            "post_processing_timestamp": datetime.now(timezone.utc),
            "inference_worker_id": inference_message.get("inference_worker_id"),
            "post_processing_worker_id": self.worker_id,
            "original_timestamp": inference_message.get("original_timestamp"),
            "consumer_worker_id": inference_message.get("consumer_worker_id"),
            "video_chunk_info": inference_message.get("video_chunk_info"),
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
            "active_tasks": len(self._active_tasks),
            "max_concurrent_tasks": self.max_concurrent_tasks,
            "max_concurrent_reached": self.max_concurrent_reached,
            "concurrent_tasks_count": self.concurrent_tasks_count,
            "processing_mode": "concurrent",
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
