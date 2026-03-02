"""
InferenceInterface: Thread-safe inference with worker queue routing.

THREAD SAFETY & CONCURRENT REQUEST HANDLING:
============================================

This module solves the greenlet thread context switching problem that occurs when:
1. Streaming frames are being processed continuously through the StreamingPipeline
2. Direct API calls (e.g., identity images for face recognition) arrive simultaneously

The Problem:
-----------
- Streaming frames are processed by inference worker processes with their own models
- Direct API calls attempt to use models in the main process from different thread contexts
- Models using gevent/greenlet internally cannot switch between different greenlet contexts
- This causes: "Cannot switch to a different thread" errors

The Solution (Worker Queue Routing):
-----------------------------------
1. StreamingPipeline creates inference worker processes that load their own models
2. When pipeline is active, ALL inference requests (streaming + direct API) are routed
   through the same worker queue (inference_queue)
3. Direct API calls (identity images) submit tasks to the worker queue and wait for
   responses via a dedicated response queue (direct_api_response_queue)
4. This ensures all inference uses the same greenlet context (worker process)
5. High-priority requests bypass the streaming queue backpressure with priority handling

Benefits:
--------
- No greenlet thread context errors (all inference in worker process context)
- Identity images work during streaming
- Natural frame skipping: Workers process identity images, streaming frames queue up
  and may be dropped if queue fills (acceptable for continuous video streams)
- Simple, robust architecture using multiprocessing queues

Usage:
-----
1. StreamingPipeline calls: inference_interface.set_worker_queues(input_queue, response_queue)
2. Direct API calls automatically route through worker queue when pipeline is active
3. High-priority requests (identity images) get dedicated handling
"""

from matrice_inference.server.model.model_manager_wrapper import ModelManagerWrapper
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime, timezone
import logging
import time
import asyncio
import multiprocessing as mp
import uuid
import queue
from matrice_analytics.post_processing.post_processor import PostProcessor

class InferenceInterface:
    """Interface for proxying requests to model servers with optional post-processing."""

    def __init__(
        self,
        model_manager_wrapper: Optional[ModelManagerWrapper] = None,
        post_processor: Optional[PostProcessor] = None,
    ):
        """
        Initialize the inference interface.

        Args:
            model_manager_wrapper: Model manager for model inference. Can be None if not configured.
            post_processor: Post processor for post-processing
        """
        self.logger = logging.getLogger(__name__)
        self.model_manager_wrapper = model_manager_wrapper
        self.post_processor = post_processor
        self.latest_inference_time = datetime.now(timezone.utc)
        self.pipeline_event_loop: Optional[asyncio.AbstractEventLoop] = None

        # Worker queue routing for direct API calls
        # When set, ALL inference requests are routed through worker processes
        # to avoid greenlet context switching issues
        self._worker_input_queues: Optional[List[mp.Queue]] = None
        self._worker_response_queue: Optional[mp.Queue] = None
        self._use_worker_queue_routing = False
        self._direct_api_worker_counter = 0  # Round-robin counter for load balancing

        # Track concurrent inference requests for monitoring
        self._active_inference_count = 0
        self._inference_count_lock = asyncio.Lock() if asyncio else None

    def get_latest_inference_time(self) -> datetime:
        """Get the latest inference time."""
        return self.latest_inference_time

    def set_pipeline_event_loop(self, event_loop: asyncio.AbstractEventLoop) -> None:
        """Set the pipeline event loop for thread-safe async operations.

        Args:
            event_loop: Event loop from StreamingPipeline
        """
        self.pipeline_event_loop = event_loop
        self.logger.info("Pipeline event loop registered for thread-safe inference")

    def set_worker_queues(
        self,
        input_queues: List[mp.Queue],
        response_queue: mp.Queue,
    ) -> None:
        """Set worker queues for routing direct API calls through inference workers.

        When set, direct API calls (e.g., identity images for face recognition) are
        routed through the same inference worker processes that handle streaming frames.
        This avoids greenlet context switching issues by ensuring all model inference
        happens in the worker process context.

        Args:
            input_queues: List of multiprocessing queues (one per worker) for submitting tasks
            response_queue: Multiprocessing queue for receiving inference results
        """
        self._worker_input_queues = input_queues
        self._worker_response_queue = response_queue
        self._use_worker_queue_routing = True
        self._direct_api_worker_counter = 0  # Round-robin counter for load balancing
        self.logger.info(
            f"Worker queue routing enabled - direct API calls will use {len(input_queues)} inference workers"
        )

    def disable_worker_queue_routing(self) -> None:
        """Disable worker queue routing (used when pipeline stops)."""
        self._use_worker_queue_routing = False
        self._worker_input_queues = None
        self._worker_response_queue = None
        self._direct_api_worker_counter = 0
        self.logger.info("Worker queue routing disabled")

    def has_async_predict(self) -> bool:
        """Check if async_predict is available in the underlying model manager.

        Returns:
            bool: True if async_predict is available, False otherwise
        """
        try:
            # No model manager, no async_predict
            if self.model_manager_wrapper is None:
                return False

            # Check if model_manager_wrapper has model_manager attribute
            if not hasattr(self.model_manager_wrapper, 'model_manager'):
                return False

            model_manager = self.model_manager_wrapper.model_manager

            # Check if model_manager has async_predict and it's not None
            if hasattr(model_manager, 'async_predict') and model_manager.async_predict is not None:
                return True

            return False
        except Exception as e:
            self.logger.warning(f"Error checking async_predict availability: {e}")
            return False

    def _route_through_worker_queue(
        self,
        input: Any,
        extra_params: Optional[Dict[str, Any]] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
        timeout: float = 30.0,
    ) -> Tuple[Any, bool]:
        """Route inference through worker queue to avoid greenlet context issues.

        This method submits the inference task to the same queue used by streaming
        frames, ensuring the model is accessed in the worker process context where
        it was loaded. This avoids greenlet "Cannot switch to a different thread" errors.

        Args:
            input: Input data (image bytes)
            extra_params: Additional parameters for inference
            stream_key: Stream key identifier
            stream_info: Stream metadata
            timeout: Maximum time to wait for response (seconds)

        Returns:
            Tuple of (results, success_flag)

        Raises:
            RuntimeError: If worker queue routing fails
        """
        if not self._worker_input_queues:
            raise RuntimeError("Worker queues not configured for routing")

        # Generate unique request ID for correlation
        request_id = str(uuid.uuid4())

        # Create a dedicated response queue for this request to avoid cross-talk
        response_queue = mp.Queue(maxsize=1)

        # Create task for worker queue
        # Uses special "direct_api" type so workers know to send response back
        task = {
            "type": "direct_api",
            "request_id": request_id,
            "input_bytes": input if isinstance(input, bytes) else bytes(input),
            "extra_params": extra_params or {},
            "stream_key": stream_key or f"direct_api_{request_id}",
            "stream_info": stream_info,
            "response_queue": response_queue,
            # Required fields for worker validation (using placeholder values)
            "camera_id": f"direct_api_{request_id[:8]}",
            "frame_id": request_id,
            "message": {"type": "direct_api"},
            "camera_config": {"type": "direct_api"},
        }

        # Round-robin select a worker queue for load balancing
        num_workers = len(self._worker_input_queues)
        worker_id = self._direct_api_worker_counter % num_workers
        self._direct_api_worker_counter += 1
        target_queue = self._worker_input_queues[worker_id]

        self.logger.debug(f"Submitting direct API task {request_id} to worker {worker_id}")

        try:
            # Submit task to worker queue with reasonable timeout
            # Identity images may need more time if queue has backlog
            target_queue.put(task, timeout=10.0)
        except Exception as e:
            self.logger.error(f"Failed to submit task to worker queue {worker_id}: {e}")
            raise RuntimeError(f"Worker queue submission failed: {e}") from e

        # Wait for response on the dedicated response queue
        try:
            result = response_queue.get(timeout=timeout)
        except Exception:
            raise RuntimeError(
                f"Timeout waiting for worker response (request_id={request_id}, timeout={timeout}s)"
            )

        # Extract result
        if result.get("success"):
            self.logger.debug(f"Direct API task {request_id} completed successfully")
            return result.get("model_result"), True
        else:
            error_msg = result.get("error", "Unknown worker error")
            self.logger.error(f"Direct API task {request_id} failed: {error_msg}")
            return None, False

    def _are_main_process_models_loaded(self) -> bool:
        """Check if main process models are loaded and ready for inference.

        This checks if the ModelManagerWrapper's ModelManager has loaded model instances.
        When async_load_model is used, models are lazy-loaded in worker processes only,
        so main process models will be None placeholders.

        Returns:
            bool: True if models are loaded and ready, False otherwise
        """
        try:
            # No model manager
            if self.model_manager_wrapper is None:
                return False

            if not hasattr(self.model_manager_wrapper, 'model_manager'):
                return False

            model_manager = self.model_manager_wrapper.model_manager
            if not hasattr(model_manager, 'model_instances'):
                return False

            # Check if we have any loaded (non-None) model instances
            model_instances = model_manager.model_instances
            if not model_instances:
                return False

            # Check if at least one model is actually loaded (not None placeholder)
            return any(model is not None for model in model_instances)

        except Exception:
            return False

    async def _inference_via_main_process(
        self,
        input: Any,
        extra_params: Optional[Dict[str, Any]] = None,
        apply_post_processing: bool = False,
        post_processing_config: Optional[Union[Dict[str, Any], str]] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
        pipeline_event_loop: Optional[asyncio.AbstractEventLoop] = None,
    ) -> Tuple[Any, Optional[Dict[str, Any]]]:
        """Perform inference using the main process's ModelManagerWrapper directly.

        This method attempts to use the ModelManagerWrapper instance that was passed
        to InferenceInterface from server.py. This is the model loaded in the main
        process and is faster than worker queue routing (no IPC overhead).

        However, this may fail with greenlet errors if the model uses gevent/greenlet
        internally (e.g., Triton gRPC clients). In that case, the caller should
        fall back to worker queue routing.

        Note: When async_load_model is used, models are only loaded in worker processes,
        not in the main process. This method will raise an error in that case, and the
        caller should fall back to worker queue routing.

        Args:
            input: Input data (image bytes)
            extra_params: Additional parameters for inference
            apply_post_processing: Whether to apply post-processing
            post_processing_config: Configuration for post-processing
            stream_key: Stream key identifier
            stream_info: Stream metadata
            pipeline_event_loop: Event loop from StreamingPipeline (if available)

        Returns:
            Tuple of (results, metadata)

        Raises:
            RuntimeError: If inference fails (including greenlet errors or models not loaded)
        """
        # Quick check: Are models actually loaded in main process?
        # When async_load_model is used, models are only loaded in worker processes
        if not self._are_main_process_models_loaded():
            raise RuntimeError(
                "Main process models not loaded (async_load_model defers loading to workers). "
                "Will fall back to worker queue routing."
            )

        model_start_time = time.time()

        # Update latest inference time
        self.latest_inference_time = datetime.now(timezone.utc)

        try:
            # Use provided event loop or fall back to stored pipeline event loop
            event_loop_to_use = pipeline_event_loop or self.pipeline_event_loop

            # If event loop is available and has async_predict, use thread-safe async inference
            if event_loop_to_use and self.has_async_predict():
                # Run async inference in pipeline's event loop from any thread
                self.logger.debug(
                    f"Main process: Using thread-safe async inference via pipeline event loop "
                    f"(stream_key={stream_key})"
                )
                future = asyncio.run_coroutine_threadsafe(
                    self.model_manager_wrapper.async_inference(
                        input=input,
                        extra_params=extra_params,
                        stream_key=stream_key,
                        stream_info=stream_info
                    ),
                    event_loop_to_use
                )
                # Use longer timeout for high-priority requests
                raw_results, success = future.result(timeout=30.0)
            else:
                # Fall back to sync inference (no async support or no event loop)
                self.logger.debug("Main process: Using synchronous inference")
                raw_results, success = self.model_manager_wrapper.inference(
                    input=input,
                    extra_params=extra_params,
                    stream_key=stream_key,
                    stream_info=stream_info
                )

            model_inference_time = time.time() - model_start_time

            if not success:
                raise RuntimeError("Model inference failed in main process")

            self.logger.debug(
                f"Main process inference executed stream_key={stream_key} "
                f"time={model_inference_time:.4f}s"
            )

        except Exception as exc:
            error_msg = str(exc)
            # Re-raise to let caller handle fallback
            self.logger.debug(f"Main process inference failed: {error_msg}")
            raise RuntimeError(f"Main process inference failed: {error_msg}") from exc

        # If no post-processing requested, return raw results
        if not apply_post_processing or not self.post_processor:
            return raw_results, {
                "timing_metadata": {
                    "model_inference_time_sec": model_inference_time,
                    "post_processing_time_sec": 0.0,
                    "total_time_sec": model_inference_time,
                },
                "routing": "main_process",
            }

        # Apply post-processing using PostProcessor
        try:
            post_processing_start_time = time.time()

            result = await self.post_processor.process(
                data=raw_results,
                config=post_processing_config,
                input_bytes=input if isinstance(input, bytes) else None,
                stream_key=stream_key,
                stream_info=stream_info
            )

            post_processing_time = time.time() - post_processing_start_time

            if result.is_success():
                processed_raw_results = [] if (
                    hasattr(result, 'usecase') and result.usecase == 'face_recognition'
                ) else raw_results

                agg_summary = {}
                if hasattr(result, 'data') and isinstance(result.data, dict):
                    agg_summary = result.data.get("agg_summary", {})

                post_processing_result = {
                    "status": "success",
                    "processing_time": result.processing_time,
                    "usecase": getattr(result, 'usecase', ''),
                    "category": getattr(result, 'category', ''),
                    "summary": getattr(result, 'summary', ''),
                    "insights": getattr(result, 'insights', []),
                    "metrics": getattr(result, 'metrics', {}),
                    "predictions": getattr(result, 'predictions', []),
                    "agg_summary": agg_summary,
                    "stream_key": stream_key or "default_stream",
                    "timing_metadata": {
                        "model_inference_time_sec": model_inference_time,
                        "post_processing_time_sec": post_processing_time,
                        "total_time_sec": model_inference_time + post_processing_time,
                    },
                    "routing": "main_process",
                }

                return processed_raw_results, post_processing_result
            else:
                self.logger.error(f"Post-processing failed: {result.error_message}")
                return raw_results, {
                    "status": "post_processing_failed",
                    "error": result.error_message,
                    "error_type": getattr(result, 'error_type', 'ProcessingError'),
                    "processing_time": result.processing_time,
                    "processed_data": raw_results,
                    "stream_key": stream_key or "default_stream",
                    "timing_metadata": {
                        "model_inference_time_sec": model_inference_time,
                        "post_processing_time_sec": post_processing_time,
                        "total_time_sec": model_inference_time + post_processing_time,
                    },
                    "routing": "main_process",
                }

        except Exception as e:
            post_processing_time = time.time() - post_processing_start_time
            self.logger.error(f"Post-processing exception: {str(e)}", exc_info=True)

            return raw_results, {
                "status": "post_processing_failed",
                "error": str(e),
                "error_type": type(e).__name__,
                "processed_data": raw_results,
                "stream_key": stream_key or "default_stream",
                "timing_metadata": {
                    "model_inference_time_sec": model_inference_time,
                    "post_processing_time_sec": post_processing_time,
                    "total_time_sec": model_inference_time + post_processing_time,
                },
                "routing": "main_process",
            }

    async def _inference_via_worker_queue(
        self,
        input: Any,
        extra_params: Optional[Dict[str, Any]] = None,
        apply_post_processing: bool = False,
        post_processing_config: Optional[Union[Dict[str, Any], str]] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Any, Optional[Dict[str, Any]]]:
        """Async wrapper for worker queue inference with optional post-processing.

        Routes inference through worker queue and handles post-processing if requested.
        This method is used as a fallback for high-priority requests when main process
        inference fails (e.g., due to greenlet context switching issues).

        Args:
            input: Input data (image bytes)
            extra_params: Additional parameters for inference
            apply_post_processing: Whether to apply post-processing
            post_processing_config: Configuration for post-processing
            stream_key: Stream key identifier
            stream_info: Stream metadata

        Returns:
            Tuple of (results, metadata)
        """
        model_start_time = time.time()

        # Update latest inference time
        self.latest_inference_time = datetime.now(timezone.utc)

        try:
            # Route through worker queue (synchronous call)
            # Run in thread pool to avoid blocking async event loop
            loop = asyncio.get_event_loop()
            raw_results, success = await loop.run_in_executor(
                None,  # Use default executor
                self._route_through_worker_queue,
                input,
                extra_params,
                stream_key,
                stream_info,
                30.0,  # timeout - increased for identity image processing
            )

            model_inference_time = time.time() - model_start_time

            if not success:
                raise RuntimeError("Model inference via worker queue failed")

            self.logger.debug(
                f"Worker queue inference executed stream_key={stream_key} "
                f"time={model_inference_time:.4f}s"
            )

        except Exception as exc:
            error_msg = str(exc)
            if "greenlet" in error_msg.lower() or "cannot switch" in error_msg.lower():
                self.logger.error(
                    f"Greenlet error in worker queue routing. This is unexpected - "
                    f"worker queue routing should avoid greenlet issues. Error: {error_msg}",
                    exc_info=True
                )
            else:
                self.logger.error(f"Worker queue inference failed: {error_msg}", exc_info=True)
            raise RuntimeError(f"Worker queue inference failed: {error_msg}") from exc

        # If no post-processing requested, return raw results
        if not apply_post_processing or not self.post_processor:
            return raw_results, {
                "timing_metadata": {
                    "model_inference_time_sec": model_inference_time,
                    "post_processing_time_sec": 0.0,
                    "total_time_sec": model_inference_time,
                },
                "routing": "worker_queue",
            }

        # Apply post-processing using PostProcessor
        try:
            post_processing_start_time = time.time()

            result = await self.post_processor.process(
                data=raw_results,
                config=post_processing_config,
                input_bytes=input if isinstance(input, bytes) else None,
                stream_key=stream_key,
                stream_info=stream_info
            )

            post_processing_time = time.time() - post_processing_start_time

            if result.is_success():
                processed_raw_results = [] if (
                    hasattr(result, 'usecase') and result.usecase == 'face_recognition'
                ) else raw_results

                agg_summary = {}
                if hasattr(result, 'data') and isinstance(result.data, dict):
                    agg_summary = result.data.get("agg_summary", {})

                post_processing_result = {
                    "status": "success",
                    "processing_time": result.processing_time,
                    "usecase": getattr(result, 'usecase', ''),
                    "category": getattr(result, 'category', ''),
                    "summary": getattr(result, 'summary', ''),
                    "insights": getattr(result, 'insights', []),
                    "metrics": getattr(result, 'metrics', {}),
                    "predictions": getattr(result, 'predictions', []),
                    "agg_summary": agg_summary,
                    "stream_key": stream_key or "default_stream",
                    "timing_metadata": {
                        "model_inference_time_sec": model_inference_time,
                        "post_processing_time_sec": post_processing_time,
                        "total_time_sec": model_inference_time + post_processing_time,
                    },
                    "routing": "worker_queue",
                }

                return processed_raw_results, post_processing_result
            else:
                self.logger.error(f"Post-processing failed: {result.error_message}")
                return raw_results, {
                    "status": "post_processing_failed",
                    "error": result.error_message,
                    "error_type": getattr(result, 'error_type', 'ProcessingError'),
                    "processing_time": result.processing_time,
                    "processed_data": raw_results,
                    "stream_key": stream_key or "default_stream",
                    "timing_metadata": {
                        "model_inference_time_sec": model_inference_time,
                        "post_processing_time_sec": post_processing_time,
                        "total_time_sec": model_inference_time + post_processing_time,
                    },
                    "routing": "worker_queue",
                }

        except Exception as e:
            post_processing_time = time.time() - post_processing_start_time
            self.logger.error(f"Post-processing exception: {str(e)}", exc_info=True)

            return raw_results, {
                "status": "post_processing_failed",
                "error": str(e),
                "error_type": type(e).__name__,
                "processed_data": raw_results,
                "stream_key": stream_key or "default_stream",
                "timing_metadata": {
                    "model_inference_time_sec": model_inference_time,
                    "post_processing_time_sec": post_processing_time,
                    "total_time_sec": model_inference_time + post_processing_time,
                },
                "routing": "worker_queue",
            }
    
    async def inference(
        self,
        input: Any,
        extra_params: Optional[Dict[str, Any]] = None,
        apply_post_processing: bool = False,
        post_processing_config: Optional[Union[Dict[str, Any], str]] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
        camera_info: Optional[Dict[str, Any]] = None,
        pipeline_event_loop: Optional[asyncio.AbstractEventLoop] = None,
        is_high_priority: bool = False,
    ) -> Tuple[Any, Optional[Dict[str, Any]]]:
        """Perform inference using the appropriate client with optional post-processing.

        Args:
            input: Primary input data (e.g., image bytes, numpy array)
            extra_params: Additional parameters for inference (optional)
            apply_post_processing: Whether to apply post-processing
            post_processing_config: Configuration for post-processing
            stream_key: Unique identifier for the input stream
            stream_info: Additional metadata about the stream (optional)
            camera_info: Additional metadata about the camera/source (optional)
            pipeline_event_loop: Event loop from StreamingPipeline (if available)
            is_high_priority: If True, this is a high-priority request (e.g., identity image)

        Returns:
            A tuple containing:
                - The inference results (raw or post-processed)
                - Metadata about the inference and post-processing (if applicable)

        Note:
            High-priority requests (like identity images for face recognition) are routed
            through the worker queue when streaming is active. This avoids greenlet context
            switching issues by ensuring all model inference happens in the worker process.
            During their execution, streaming frames may be naturally skipped if the
            inference queue fills up, which is acceptable for continuous streaming scenarios.
        """
        if input is None:
            raise ValueError("Input cannot be None")

        # Log high-priority requests for monitoring
        if is_high_priority:
            self.logger.info(f"Processing high-priority inference request (stream_key={stream_key})")

        # HIGH-PRIORITY REQUEST HANDLING STRATEGY:
        # =========================================
        # For high-priority requests (e.g., identity images for face recognition) when
        # streaming is active, we use a two-tier fallback strategy:
        #
        # 1. FIRST TRY: Use the main process's ModelManagerWrapper directly
        #    - This is the ModelManagerWrapper instance passed to InferenceInterface from server.py
        #    - It's already initialized with loaded models in the main process
        #    - Faster than worker queue routing (no IPC overhead)
        #    - May fail with greenlet errors if model uses gevent/greenlet internally
        #
        # 2. FALLBACK: Route through worker queue if main process inference fails
        #    - Worker processes have their own models loaded in their own greenlet context
        #    - Avoids greenlet "Cannot switch to a different thread" errors
        #    - Slightly slower due to IPC (queue put/get)
        #
        # 3. RAISE ERROR: If both fail, raise an error with clear message
        #
        # This strategy prioritizes using the already-loaded main process model for
        # speed, but falls back to worker processes for greenlet compatibility.

        if (
            is_high_priority
            and self._use_worker_queue_routing
            and self._worker_input_queues is not None
        ):
            # FIRST TRY: Use main process's ModelManagerWrapper directly
            self.logger.info(
                f"High-priority request: trying main process ModelManagerWrapper first "
                f"(stream_key={stream_key})"
            )

            main_process_error = None
            try:
                # Try direct inference using the main process's model
                # This uses self.model_manager_wrapper which was passed from server.py
                return await self._inference_via_main_process(
                    input=input,
                    extra_params=extra_params,
                    apply_post_processing=apply_post_processing,
                    post_processing_config=post_processing_config,
                    stream_key=stream_key,
                    stream_info=stream_info,
                    pipeline_event_loop=pipeline_event_loop,
                )
            except Exception as main_exc:
                main_process_error = main_exc
                error_msg = str(main_exc)

                # Check if this is a greenlet error - these MUST be routed through workers
                is_greenlet_error = (
                    "greenlet" in error_msg.lower() or
                    "cannot switch" in error_msg.lower()
                )

                if is_greenlet_error:
                    self.logger.warning(
                        f"Main process inference failed with greenlet error, "
                        f"falling back to worker queue routing (stream_key={stream_key}): {error_msg}"
                    )
                else:
                    self.logger.warning(
                        f"Main process inference failed, "
                        f"falling back to worker queue routing (stream_key={stream_key}): {error_msg}"
                    )

            # FALLBACK: Route through worker queue
            self.logger.info(
                f"Routing high-priority request through worker queue "
                f"(stream_key={stream_key})"
            )
            try:
                return await self._inference_via_worker_queue(
                    input=input,
                    extra_params=extra_params,
                    apply_post_processing=apply_post_processing,
                    post_processing_config=post_processing_config,
                    stream_key=stream_key,
                    stream_info=stream_info,
                )
            except Exception as worker_exc:
                # BOTH main process and worker queue failed - raise comprehensive error
                error_msg = (
                    f"High-priority inference failed with both strategies. "
                    f"Main process error: {main_process_error}. "
                    f"Worker queue error: {worker_exc}. "
                    f"Ensure models are loaded and worker processes are running."
                )
                self.logger.error(error_msg)
                raise RuntimeError(error_msg) from worker_exc

        # Measure model inference time
        model_start_time = time.time()

        # Update latest inference time
        self.latest_inference_time = datetime.now(timezone.utc)

        # Run model inference with proper thread-safety
        try:
            # Use provided event loop or fall back to stored pipeline event loop
            event_loop_to_use = pipeline_event_loop or self.pipeline_event_loop

            # If event loop is available and has async_predict, use thread-safe async inference
            if event_loop_to_use and self.has_async_predict():
                # Run async inference in pipeline's event loop from any thread
                # This ensures identity images and streaming frames use the same event loop
                # This prevents greenlet/gevent thread context switching errors
                self.logger.debug(
                    f"Using thread-safe async inference via pipeline event loop "
                    f"(priority={'high' if is_high_priority else 'normal'})"
                )
                future = asyncio.run_coroutine_threadsafe(
                    self.model_manager_wrapper.async_inference(
                        input=input,
                        extra_params=extra_params,
                        stream_key=stream_key,
                        stream_info=stream_info
                    ),
                    event_loop_to_use
                )
                # High-priority requests get longer timeout
                timeout = 10.0 if is_high_priority else 6.0
                raw_results, success = future.result(timeout=timeout)
            else:
                # Fall back to sync inference (no async support or no event loop)
                self.logger.debug("Using synchronous inference (no async support or event loop)")
                raw_results, success = self.model_manager_wrapper.inference(
                    input=input,
                    extra_params=extra_params,
                    stream_key=stream_key,
                    stream_info=stream_info
                )

            model_inference_time = time.time() - model_start_time

            if not success:
                raise RuntimeError("Model inference failed")

            self.logger.debug(
                f"Model inference executed stream_key={stream_key} "
                f"time={model_inference_time:.4f}s priority={'high' if is_high_priority else 'normal'}"
            )

        except Exception as exc:
            # Add context about greenlet errors
            error_msg = str(exc)
            if "greenlet" in error_msg.lower() or "cannot switch" in error_msg.lower():
                self.logger.error(
                    f"Greenlet thread context error detected. This typically means the model "
                    f"is being accessed from multiple threads without proper event loop coordination. "
                    f"Error: {error_msg}",
                    exc_info=True
                )
            else:
                self.logger.error(f"Model inference failed: {error_msg}", exc_info=True)
            raise RuntimeError(f"Model inference failed: {error_msg}") from exc
        
        # If no post-processing requested, return raw results
        if not apply_post_processing or not self.post_processor:
            return raw_results, {
                "timing_metadata": {
                    "model_inference_time_sec": model_inference_time,
                    "post_processing_time_sec": 0.0,
                    "total_time_sec": model_inference_time,
                }
            }

        # Apply post-processing using PostProcessor
        try:
            post_processing_start_time = time.time()
            
            # Use PostProcessor.process() method directly
            result = await self.post_processor.process(
                data=raw_results,
                config=post_processing_config,  # Use stream_key as fallback if no config
                input_bytes=input if isinstance(input, bytes) else None,
                stream_key=stream_key,
                stream_info=stream_info
            )
            
            post_processing_time = time.time() - post_processing_start_time
            
            # Format the response based on PostProcessor result
            if result.is_success():
                # For face recognition use case, return empty raw results
                processed_raw_results = [] if (
                    hasattr(result, 'usecase') and result.usecase == 'face_recognition'
                ) else raw_results
                
                # Extract agg_summary from result data if available
                agg_summary = {}
                if hasattr(result, 'data') and isinstance(result.data, dict):
                    agg_summary = result.data.get("agg_summary", {})
                
                post_processing_result = {
                    "status": "success",
                    "processing_time": result.processing_time,
                    "usecase": getattr(result, 'usecase', ''),
                    "category": getattr(result, 'category', ''),
                    "summary": getattr(result, 'summary', ''),
                    "insights": getattr(result, 'insights', []),
                    "metrics": getattr(result, 'metrics', {}),
                    "predictions": getattr(result, 'predictions', []),
                    "agg_summary": agg_summary,
                    "stream_key": stream_key or "default_stream",
                    "timing_metadata": {
                        "model_inference_time_sec": model_inference_time,
                        "post_processing_time_sec": post_processing_time,
                        "total_time_sec": model_inference_time + post_processing_time,
                    }
                }
                
                return processed_raw_results, post_processing_result
            else:
                # Post-processing failed
                self.logger.error(f"Post-processing failed: {result.error_message}")
                return raw_results, {
                    "status": "post_processing_failed",
                    "error": result.error_message,
                    "error_type": getattr(result, 'error_type', 'ProcessingError'),
                    "processing_time": result.processing_time,
                    "processed_data": raw_results,
                    "stream_key": stream_key or "default_stream",
                    "timing_metadata": {
                        "model_inference_time_sec": model_inference_time,
                        "post_processing_time_sec": post_processing_time,
                        "total_time_sec": model_inference_time + post_processing_time,
                    }
                }
                
        except Exception as e:
            post_processing_time = time.time() - post_processing_start_time
            self.logger.error(f"Post-processing exception: {str(e)}", exc_info=True)

            return raw_results, {
                "status": "post_processing_failed",
                "error": str(e),
                "error_type": type(e).__name__,
                "processed_data": raw_results,
                "stream_key": stream_key or "default_stream",
                "timing_metadata": {
                    "model_inference_time_sec": model_inference_time,
                    "post_processing_time_sec": post_processing_time,
                    "total_time_sec": model_inference_time + post_processing_time,
                }
            }

    def sync_inference(
        self,
        input: Any,
        extra_params: Optional[Dict[str, Any]] = None,
        apply_post_processing: bool = False,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Any, Optional[Dict[str, Any]]]:
        """Perform SYNCHRONOUS inference - pure Python, no asyncio.

        This method is designed for SYNC mode workers where asyncio overhead
        is undesirable. It calls ModelManagerWrapper.inference() directly
        without any async wrappers.

        IMPORTANT: This method does NOT support post-processing (which is async).
        Post-processing should be handled separately in the pipeline if needed.

        Args:
            input: Primary input data (e.g., image bytes, numpy array)
            extra_params: Additional parameters for inference (optional)
            apply_post_processing: Ignored (kept for API compatibility)
            stream_key: Unique identifier for the input stream
            stream_info: Additional metadata about the stream (optional)

        Returns:
            A tuple containing:
                - The inference results (raw model output)
                - Metadata dict with timing information
        """
        if input is None:
            raise ValueError("Input cannot be None")

        # Update latest inference time
        self.latest_inference_time = datetime.now(timezone.utc)

        model_start_time = time.time()

        try:
            # Direct synchronous call - no asyncio overhead
            raw_results, success = self.model_manager_wrapper.inference(
                input=input,
                extra_params=extra_params,
                stream_key=stream_key,
                stream_info=stream_info,
            )

            model_inference_time = time.time() - model_start_time

            if not success:
                raise RuntimeError("Synchronous model inference failed")

            return raw_results, {
                "timing_metadata": {
                    "model_inference_time_sec": model_inference_time,
                    "post_processing_time_sec": 0.0,
                    "total_time_sec": model_inference_time,
                },
                "mode": "sync",
            }

        except Exception as exc:
            model_inference_time = time.time() - model_start_time
            self.logger.error(f"Sync inference failed: {str(exc)}", exc_info=True)
            raise RuntimeError(f"Sync inference failed: {str(exc)}") from exc

    def sync_batch_inference(
        self,
        input_list: List[Any],
        extra_params: Optional[Dict[str, Any]] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> Tuple[List[Any], bool]:
        """Perform SYNCHRONOUS batch inference - pure Python, no asyncio.

        This method is designed for SYNC mode workers where asyncio overhead
        is undesirable. It calls ModelManagerWrapper.batch_inference() directly
        without any async wrappers.

        Args:
            input_list: List of input data (e.g., image bytes for each frame)
            extra_params: Optional parameters for inference
            stream_key: Stream identifier (for logging)
            stream_info: Stream metadata

        Returns:
            Tuple of (results_list, success_bool):
                - results_list: List of inference results (same order as inputs)
                - success_bool: True if inference succeeded, False otherwise
        """
        if not input_list:
            return [], True

        # Update latest inference time
        self.latest_inference_time = datetime.now(timezone.utc)

        start_time = time.time()

        try:
            # Direct synchronous call - no asyncio overhead
            results, success = self.model_manager_wrapper.batch_inference(
                input=input_list,
                extra_params=extra_params,
                stream_key=stream_key,
                stream_info=stream_info,
            )

            inference_time = time.time() - start_time

            if not success:
                self.logger.warning(
                    f"Sync batch inference returned success=False for {len(input_list)} inputs"
                )
                return results or [], False

            return results, True

        except Exception as exc:
            inference_time = time.time() - start_time
            self.logger.error(
                f"Sync batch inference failed after {inference_time:.3f}s: {exc}",
                exc_info=True
            )
            return [], False

    async def async_inference(
        self,
        input: Any,
        extra_params: Optional[Dict[str, Any]] = None,
        apply_post_processing: bool = False,
        post_processing_config: Optional[Union[Dict[str, Any], str]] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
        camera_info: Optional[Dict[str, Any]] = None,
        pipeline_event_loop: Optional[asyncio.AbstractEventLoop] = None,
    ) -> Tuple[Any, Optional[Dict[str, Any]]]:
        """Perform ASYNCHRONOUS inference using async_predict when available.

        This method MUST be called within an async context (event loop).
        For pure synchronous calls from thread pools, use sync_inference() instead.

        Args:
            input: Primary input data (e.g., image bytes, numpy array)
            extra_params: Additional parameters for inference (optional)
            apply_post_processing: Whether to apply post-processing
            post_processing_config: Configuration for post-processing
            stream_key: Unique identifier for the input stream
            stream_info: Additional metadata about the stream (optional)
            camera_info: Additional metadata about the camera/source (optional)
            pipeline_event_loop: Event loop from StreamingPipeline (optional, for validation)

        Returns:
            A tuple containing:
                - The inference results (raw or post-processed)
                - Metadata about the inference and post-processing (if applicable)
        """
        if input is None:
            raise ValueError("Input cannot be None")

        # Measure model inference time
        model_start_time = time.time()

        # Update latest inference time
        self.latest_inference_time = datetime.now(timezone.utc)

        # Run asynchronous model inference
        try:
            raw_results, success = await self.model_manager_wrapper.async_inference(
                input=input,
                extra_params=extra_params,
                stream_key=stream_key,
                stream_info=stream_info
            )
            model_inference_time = time.time() - model_start_time

            if not success:
                raise RuntimeError("Model inference failed")

            self.logger.debug(
                f"Async model inference executed stream_key={stream_key} time={model_inference_time:.4f}s"
            )

        except Exception as exc:
            self.logger.error(f"Async model inference failed: {str(exc)}", exc_info=True)
            raise RuntimeError(f"Async model inference failed: {str(exc)}") from exc
        
        # If no post-processing requested, return raw results
        if not apply_post_processing or not self.post_processor:
            return raw_results, {
                "timing_metadata": {
                    "model_inference_time_sec": model_inference_time,
                    "post_processing_time_sec": 0.0,
                    "total_time_sec": model_inference_time,
                }
            }

        # Apply post-processing using PostProcessor
        try:
            post_processing_start_time = time.time()
            
            # Use PostProcessor.process() method directly (async)
            result = await self.post_processor.process(
                data=raw_results,
                config=post_processing_config,
                input_bytes=input if isinstance(input, bytes) else None,
                stream_key=stream_key,
                stream_info=stream_info
            )
            
            post_processing_time = time.time() - post_processing_start_time
            
            # Format the response based on PostProcessor result
            if result.is_success():
                # For face recognition use case, return empty raw results
                processed_raw_results = [] if (
                    hasattr(result, 'usecase') and result.usecase == 'face_recognition'
                ) else raw_results
                
                # Extract agg_summary from result data if available
                agg_summary = {}
                if hasattr(result, 'data') and isinstance(result.data, dict):
                    agg_summary = result.data.get("agg_summary", {})
                
                post_processing_result = {
                    "status": "success",
                    "processing_time": result.processing_time,
                    "usecase": getattr(result, 'usecase', ''),
                    "category": getattr(result, 'category', ''),
                    "summary": getattr(result, 'summary', ''),
                    "insights": getattr(result, 'insights', []),
                    "metrics": getattr(result, 'metrics', {}),
                    "predictions": getattr(result, 'predictions', []),
                    "agg_summary": agg_summary,
                    "stream_key": stream_key or "default_stream",
                    "timing_metadata": {
                        "model_inference_time_sec": model_inference_time,
                        "post_processing_time_sec": post_processing_time,
                        "total_time_sec": model_inference_time + post_processing_time,
                    }
                }
                
                return processed_raw_results, post_processing_result
            else:
                # Post-processing failed
                self.logger.error(f"Post-processing failed: {result.error_message}")
                return raw_results, {
                    "status": "post_processing_failed",
                    "error": result.error_message,
                    "error_type": getattr(result, 'error_type', 'ProcessingError'),
                    "processing_time": result.processing_time,
                    "processed_data": raw_results,
                    "stream_key": stream_key or "default_stream",
                    "timing_metadata": {
                        "model_inference_time_sec": model_inference_time,
                        "post_processing_time_sec": post_processing_time,
                        "total_time_sec": model_inference_time + post_processing_time,
                    }
                }
                
        except Exception as e:
            post_processing_time = time.time() - post_processing_start_time
            self.logger.error(f"Post-processing exception: {str(e)}", exc_info=True)

            return raw_results, {
                "status": "post_processing_failed",
                "error": str(e),
                "error_type": type(e).__name__,
                "processed_data": raw_results,
                "stream_key": stream_key or "default_stream",
                "timing_metadata": {
                    "model_inference_time_sec": model_inference_time,
                    "post_processing_time_sec": post_processing_time,
                    "total_time_sec": model_inference_time + post_processing_time,
                }
            }

    async def async_batch_inference(
        self,
        input_list: List[Any],
        extra_params: Optional[Dict[str, Any]] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> Tuple[List[Any], bool]:
        """
        Run batch inference on multiple inputs.

        This method is optimized for processing multiple frames together,
        allowing for better GPU utilization through batching. It calls the
        underlying ModelManagerWrapper's async_batch_inference method.

        Args:
            input_list: List of input data (e.g., image bytes for each frame)
            extra_params: Optional parameters for inference
            stream_key: Stream identifier (for logging)
            stream_info: Stream metadata

        Returns:
            Tuple of (results_list, success_bool):
                - results_list: List of inference results (same order as inputs)
                - success_bool: True if inference succeeded, False otherwise

        Raises:
            RuntimeError: If batch inference fails critically
        """
        if not input_list:
            return [], True

        # Update latest inference time
        self.latest_inference_time = datetime.now(timezone.utc)

        batch_size = len(input_list)

        start_time = time.time()

        try:
            # Route through model manager wrapper's batch inference
            results, success = await self.model_manager_wrapper.async_batch_inference(
                input=input_list,  # ModelManagerWrapper expects 'input' parameter
                extra_params=extra_params,
                stream_key=stream_key,
                stream_info=stream_info,
            )

            inference_time = time.time() - start_time

            if not success:
                self.logger.warning(
                    f"Batch inference returned success=False for {batch_size} inputs"
                )
                return results or [], False

            return results, True

        except Exception as exc:
            inference_time = time.time() - start_time
            self.logger.error(
                f"Batch inference failed after {inference_time:.3f}s: {exc}",
                exc_info=True
            )
            return [], False