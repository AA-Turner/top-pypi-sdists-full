"""
Dynamic batching manager for inference requests.

This module contains the batching logic separated from the main inference interface
to improve modularity and maintainability.
"""

import asyncio
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from matrice_analytics.post_processing.core.config import BaseConfig

@dataclass
class BatchRequest:
    """Represents a single inference request in a batch"""

    input1: Any
    input2: Optional[Any] = None
    extra_params: Optional[Dict[str, Any]] = None
    apply_post_processing: bool = False
    post_processing_config: Optional[Union[Dict[str, Any], BaseConfig]] = None
    future: asyncio.Future = field(default_factory=asyncio.Future)
    timestamp: float = field(default_factory=time.time)
    stream_key: Optional[str] = None
    stream_info: Optional[Dict[str, Any]] = None
    input_hash: Optional[str] = None
    camera_info: Optional[Dict[str, Any]] = None


class DynamicBatchManager:
    """Manages dynamic batching for inference requests"""

    def __init__(
        self,
        batch_size: int,
        max_batch_wait_time: float,
        model_manager,
        post_processing_fn: Callable,
    ):
        """
        Initialize the dynamic batch manager.

        Args:
            batch_size: Maximum batch size for processing
            max_batch_wait_time: Maximum wait time for batching
            model_manager: Model manager for inference
            post_processing_fn: Function to apply post-processing
        """
        self.logger = logging.getLogger(__name__)
        self.batch_size = batch_size
        self.max_batch_wait_time = max_batch_wait_time
        self.model_manager = model_manager
        self.post_processing_fn = post_processing_fn
        
        # Dynamic batching components
        self.batch_queue: List[BatchRequest] = []
        self.batch_lock = asyncio.Lock()
        self.processing_batch = False

    async def add_request(self, batch_request: BatchRequest) -> Tuple[Any, Optional[Dict[str, Any]]]:
        """Add a request to the batch queue and process if needed"""
        # Add to batch queue
        async with self.batch_lock:
            self.batch_queue.append(batch_request)

            # Check if we should process the batch
            should_process = (
                len(self.batch_queue) >= self.batch_size or not self.processing_batch
            )

            if should_process and not self.processing_batch:
                self.processing_batch = True
                # Start batch processing in background
                asyncio.create_task(self._process_batch())

        # Wait for the result
        try:
            return await batch_request.future
        except Exception as e:
            raise RuntimeError(f"Dynamic batch inference failed: {str(e)}") from e

    async def _process_batch(self):
        """Process batched inference requests"""
        try:
            # Wait for batch to fill up or timeout
            await asyncio.sleep(self.max_batch_wait_time)

            async with self.batch_lock:
                if not self.batch_queue:
                    self.processing_batch = False
                    return

                # Extract current batch
                current_batch = self.batch_queue[: self.batch_size]
                self.batch_queue = self.batch_queue[self.batch_size :]

                # Reset processing flag if no more items
                if not self.batch_queue:
                    self.processing_batch = False
                else:
                    # Continue processing remaining items
                    asyncio.create_task(self._process_batch())

            if not current_batch:
                return

            # Prepare batch inputs
            batch_input1 = [req.input1 for req in current_batch]
            batch_input2 = (
                [req.input2 for req in current_batch]
                if any(req.input2 is not None for req in current_batch)
                else None
            )
            batch_extra_params = [req.extra_params for req in current_batch]
            stream_key = current_batch[0].stream_key
            stream_info = current_batch[0].stream_info
            input_hash = current_batch[0].input_hash
            
            # Validate that all requests in the batch have the same stream_key
            batch_stream_keys = [req.stream_key for req in current_batch]
            if not all(sk == stream_key for sk in batch_stream_keys):
                self.logger.warning(
                    f"Batch contains requests with different stream keys: {set(batch_stream_keys)}. "
                    f"Using first request's stream key: {stream_key} for model inference, "
                    f"but individual stream keys for post-processing."
                )
            else:
                self.logger.debug(
                    f"Processing batch size={len(current_batch)} stream_key={stream_key}"
                )
            
            # Check if all requests have the same extra_params structure
            if batch_extra_params and all(
                params == batch_extra_params[0] for params in batch_extra_params
            ):
                merged_extra_params = batch_extra_params[0]
            else:
                # Handle heterogeneous extra_params - use first non-None or empty dict
                merged_extra_params = next(
                    (params for params in batch_extra_params if params), {}
                )

            try:
                # Perform batch inference
                batch_results, success = self.model_manager.batch_inference(
                    batch_input1,
                    batch_input2,
                    merged_extra_params,
                    stream_key,
                    stream_info,
                    input_hash
                )

                if not success:
                    raise RuntimeError("Batch inference failed")
                self.logger.debug(
                    f"Batch inference executed items={len(current_batch)} stream_key={stream_key}"
                )

                # Process results for each request
                for i, (request, result) in enumerate(
                    zip(current_batch, batch_results)
                ):
                    try:
                        if request.apply_post_processing:
                            processed_result, post_processing_result = (
                                await self.post_processing_fn(
                                    result,
                                    request.input1,
                                    request.post_processing_config,
                                    request.stream_key,
                                    request.stream_info,
                                    request.camera_info,
                                )
                            )
                            request.future.set_result(
                                (processed_result, post_processing_result)
                            )
                        else:
                            # Check if this is face recognition use case and return empty predictions for raw results
                            if self._is_face_recognition_request(request):
                                request.future.set_result(([], None))
                            else:
                                request.future.set_result((result, None))
                    except Exception as e:
                        request.future.set_exception(e)

            except Exception as e:
                # Set exception for all requests in the batch
                for request in current_batch:
                    if not request.future.done():
                        request.future.set_exception(e)

        except Exception as e:
            # Handle unexpected errors
            self.logger.error(f"Batch processing failed: {str(e)}")
            async with self.batch_lock:
                self.processing_batch = False

    def _is_face_recognition_request(self, request: BatchRequest) -> bool:
        """Check if a request is for face recognition use case."""
        try:
            # Parse the post-processing config to check if it's face recognition
            config = request.post_processing_config
            if isinstance(config, BaseConfig):
                return hasattr(config, 'usecase') and config.usecase == 'face_recognition'
            elif isinstance(config, dict):
                return config.get('usecase') == 'face_recognition'
            elif isinstance(config, str):
                return config == 'face_recognition'
            return False
        except Exception:
            return False

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the current batching state."""
        return {
            "batch_size": self.batch_size,
            "max_batch_wait_time": self.max_batch_wait_time,
            "current_queue_size": len(self.batch_queue),
            "processing_batch": self.processing_batch,
        }

    async def flush_queue(self) -> int:
        """Force process all remaining items in the batch queue.

        Returns:
            Number of items processed
        """
        async with self.batch_lock:
            remaining_items = len(self.batch_queue)
            if remaining_items > 0 and not self.processing_batch:
                self.processing_batch = True
                asyncio.create_task(self._process_batch())

        return remaining_items 