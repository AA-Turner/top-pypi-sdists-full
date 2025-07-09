from matrice.deploy.server.inference.model_manager import ModelManager
from matrice.deploy.utils.post_processing import (
    PostProcessor,
    create_config_from_template,
    create_people_counting_config,
    create_customer_service_config,
    create_advanced_customer_service_config,
    create_basic_counting_tracking_config,
)
from matrice.deploy.utils.post_processing.core.config import BaseConfig
from typing import Dict, Any, Optional, Callable, Tuple, List, Union
from matrice.action_tracker import ActionTracker
from datetime import datetime, timezone
import asyncio
import logging
from dataclasses import dataclass, field
import time


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
class InferenceInterface:
    """Interface for proxying requests to model servers with optional post-processing."""

    def __init__(
        self,
        action_tracker: ActionTracker,
        model_manager: ModelManager,
        batch_size: int = 1,
        dynamic_batching: bool = False,
        post_processing_config: Optional[
            Union[Dict[str, Any], BaseConfig, str]
        ] = None,
        custom_post_processing_fn: Optional[Callable] = None,
        max_batch_wait_time: float = 0.05,
    ):
        """
        Initialize the inference interface.

        Args:
            action_tracker: Action tracker for category mapping
            model_manager: Model manager for inference
            batch_size: Batch size for processing
            dynamic_batching: Whether to enable dynamic batching
            post_processing_config: Default post-processing configuration
                Can be a dict, BaseConfig object, or use case name string
            custom_post_processing_fn: Custom post-processing function
            max_batch_wait_time: Maximum wait time for batching
        """
        self.logger = logging.getLogger(__name__)
        self.batch_size = batch_size
        self.dynamic_batching = dynamic_batching
        self.model_manager = model_manager
        self.action_tracker = action_tracker
        self.post_processor = PostProcessor()
        self.latest_inference_time = datetime.now(timezone.utc)
        self.max_batch_wait_time = max_batch_wait_time

        # Dynamic batching components
        self.batch_queue: List[BatchRequest] = []
        self.batch_lock = asyncio.Lock()
        self.processing_batch = False

        # Set up default post-processing configuration
        self.post_processing_config = None
        if post_processing_config:
            self.logger.debug(f"Parsing post-processing config: {post_processing_config}")
            self.post_processing_config = self._parse_post_processing_config(
                post_processing_config
            )
            if self.post_processing_config:
                self.logger.info(f"Successfully parsed post-processing config for usecase: {self.post_processing_config.usecase}")
            else:
                self.logger.warning("Failed to parse post-processing config")
        else:
            self.logger.info("No post-processing config provided")

        self.custom_post_processing_fn = custom_post_processing_fn
        

    def _parse_post_processing_config(
        self, config: Union[Dict[str, Any], BaseConfig, str]
    ) -> Optional[BaseConfig]:
        """Parse post-processing configuration from various formats."""
        try:
            if isinstance(config, BaseConfig):
                return config
            elif isinstance(config, dict):
                usecase = config.get("usecase")
                if not usecase:
                    raise ValueError("Configuration dict must contain 'usecase' key")

                # Create a copy of config without usecase and category to avoid conflicts
                config_params = config.copy()
                config_params.pop("usecase", None)
                config_params.pop("category", None)

                category = config.get("category", "general")

                # Use generic config creation to avoid parameter conflicts
                return self.post_processor.create_config(
                    usecase, category, **config_params
                )

            elif isinstance(config, str):
                # Assume it's a use case name, create with defaults
                return create_config_from_template(config)
            else:
                self.logger.warning(f"Unsupported config type: {type(config)}")
                return None
        except Exception as e:
            self.logger.error(f"Failed to parse post-processing config: {str(e)}")
            return None

    async def inference(
        self,
        input1,
        input2=None,
        extra_params=None,
        apply_post_processing: bool = False,
        post_processing_config: Optional[Union[Dict[str, Any], BaseConfig, str]] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Any, Optional[Dict[str, Any]]]:
        """Perform inference using the appropriate client with optional post-processing.

        Args:
            input1: Primary input data
            input2: Secondary input data (optional)
            extra_params: Additional parameters for inference (optional)
            apply_post_processing: Whether to apply post-processing
            post_processing_config: Post-processing configuration (overrides default)
            stream_key: Stream key for the inference
            stream_info: Stream info for the inference (optional)
        Returns:
            Tuple containing (inference_result, post_processing_result).
            If post-processing is not applied, post_processing_result will be None.
            If post-processing is applied, post_processing_result contains the full post-processing metadata.

        Raises:
            ValueError: If client is not set up
            RuntimeError: If inference fails
        """
        self.latest_inference_time = datetime.now(timezone.utc)

        # If dynamic batching is enabled, use batch processing
        if self.dynamic_batching:
            return await self._dynamic_batch_inference(
                input1,
                input2,
                extra_params,
                apply_post_processing,
                post_processing_config,
                stream_key,
                stream_info,
            )

        # Get raw inference results
        try:
            raw_results, success = self.model_manager.inference(
                input1,
                input2,
                extra_params,
                stream_key,
                stream_info,
            )
            if not success:
                raise RuntimeError("Model inference failed")
        except Exception as e:
            raise RuntimeError(f"Model inference failed: {str(e)}") from e

        if not apply_post_processing:
            return raw_results, None

        # Apply post-processing
        return await self._apply_post_processing(
            raw_results, input1, post_processing_config, stream_key, stream_info
        )

    async def _dynamic_batch_inference(
        self,
        input1,
        input2=None,
        extra_params=None,
        apply_post_processing: bool = False,
        post_processing_config: Optional[Union[Dict[str, Any], BaseConfig, str]] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Any, Optional[Dict[str, Any]]]:
        """Handle inference with dynamic batching"""
        # Create a batch request
        batch_request = BatchRequest(
            input1=input1,
            input2=input2,
            extra_params=extra_params,
            apply_post_processing=apply_post_processing,
            post_processing_config=post_processing_config,
            stream_key=stream_key,
            stream_info=stream_info,
        )

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
            # Validate that all requests in the batch have the same stream_key
            batch_stream_keys = [req.stream_key for req in current_batch]
            if not all(sk == stream_key for sk in batch_stream_keys):
                self.logger.warning(
                    f"Batch contains requests with different stream keys: {set(batch_stream_keys)}. "
                    f"Using first request's stream key: {stream_key} for model inference, "
                    f"but individual stream keys for post-processing."
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
                )

                if not success:
                    raise RuntimeError("Batch inference failed")

                # Process results for each request
                for i, (request, result) in enumerate(
                    zip(current_batch, batch_results)
                ):
                    try:
                        if request.apply_post_processing:
                            processed_result, post_processing_result = (
                                await self._apply_post_processing(
                                    result,
                                    request.input1,
                                    request.post_processing_config,
                                    request.stream_key,
                                    request.stream_info,
                                )
                            )
                            request.future.set_result(
                                (processed_result, post_processing_result)
                            )
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

    async def _apply_post_processing(
        self,
        raw_results,
        input1,
        post_processing_config: Optional[Union[Dict[str, Any], BaseConfig, str]] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Any, Optional[Dict[str, Any]]]:
        """Apply post-processing to inference results"""
        try:
            # Determine which configuration to use
            config_to_use = post_processing_config or self.post_processing_config
            
            # Normalize stream_key for logging and processing
            normalized_stream_key = stream_key or "default_stream"
            
            self.logger.debug(f"Post-processing config to use: {config_to_use} for stream: {normalized_stream_key}")

            if config_to_use is None and self.custom_post_processing_fn is None:
                self.logger.warning(
                    f"No post-processing configuration or custom function provided for stream: {normalized_stream_key}"
                )
                return raw_results, None

            # Use custom function if provided and no specific config
            if self.custom_post_processing_fn and post_processing_config is None:
                post_processing_result = self.custom_post_processing_fn(raw_results)
                # Handle custom function output
                if (
                    isinstance(post_processing_result, tuple)
                    and len(post_processing_result) == 2
                ):
                    processed_result, post_processing_result = post_processing_result
                else:
                    processed_result = post_processing_result
                    post_processing_result = {"processed_data": processed_result}
                return processed_result, post_processing_result

            # Parse configuration if needed
            if not isinstance(config_to_use, BaseConfig):
                config_to_use = self._parse_post_processing_config(config_to_use)

            if config_to_use is None:
                self.logger.error(f"Failed to parse post-processing configuration for stream: {normalized_stream_key}")
                return raw_results, {
                    "error": "Invalid post-processing configuration",
                    "status": "configuration_error",
                    "processed_data": raw_results,
                    "stream_key": normalized_stream_key,
                }

            # Add index to category mapping if available
            if (
                hasattr(config_to_use, "index_to_category")
                and not config_to_use.index_to_category
            ):
                config_to_use.index_to_category = (
                    self.action_tracker.get_index_to_category()
                )

            # Apply post-processing using the unified processor
            result = self.post_processor.process(raw_results, config_to_use, input1, stream_key=stream_key, stream_info=stream_info)

            if result.is_success():
                return raw_results, {
                    "status": "success",
                    "processing_time": result.processing_time,
                    "usecase": result.usecase,
                    "category": result.category,
                    "summary": result.summary,
                    "insights": result.insights,
                    "metrics": result.metrics,
                    "predictions": result.predictions,
                    "processed_data": result.data,
                    "stream_key": normalized_stream_key,
                }
            else:
                self.logger.error(f"Post-processing failed for stream {normalized_stream_key}: {result.error_message}")
                return raw_results, {
                    "error": result.error_message,
                    "error_type": result.error_type,
                    "status": "post_processing_failed",
                    "processing_time": result.processing_time,
                    "processed_data": raw_results,
                    "stream_key": normalized_stream_key,
                }

        except Exception as e:
            # Log the error and return raw results with error info
            normalized_stream_key = stream_key or "default_stream"
            self.logger.error(f"Post-processing failed for stream {normalized_stream_key}: {str(e)}", exc_info=True)
            return raw_results, {
                "error": str(e),
                "status": "post_processing_failed",
                "processed_data": raw_results,
                "stream_key": normalized_stream_key,
            }

    async def batch_inference(
        self,
        batch_input1: List[Any],
        batch_input2: Optional[List[Any]] = None,
        batch_extra_params: Optional[List[Dict[str, Any]]] = None,
        apply_post_processing: bool = False,
        post_processing_configs: Optional[
            List[Union[Dict[str, Any], BaseConfig, str]]
        ] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Tuple[Any, Optional[Dict[str, Any]]]]:
        """Perform batch inference directly without dynamic batching.

        Args:
            batch_input1: List of primary input data
            batch_input2: List of secondary input data (optional)
            batch_extra_params: List of additional parameters for each inference (optional)
            apply_post_processing: Whether to apply post-processing
            post_processing_configs: List of post-processing configurations for each input
            stream_key: Stream key for the inference
            stream_info: Stream info for the inference (optional)
        Returns:
            List of tuples containing (inference_result, post_processing_result) for each input.

        Raises:
            ValueError: If input data is invalid
            RuntimeError: If inference fails
        """
        self.latest_inference_time = datetime.now(timezone.utc)

        if not batch_input1:
            raise ValueError("Batch input cannot be empty")

        # Ensure all batch inputs have the same length
        batch_size = len(batch_input1)
        if batch_input2 and len(batch_input2) != batch_size:
            raise ValueError("batch_input2 must have the same length as batch_input1")
        if batch_extra_params and len(batch_extra_params) != batch_size:
            raise ValueError(
                "batch_extra_params must have the same length as batch_input1"
            )
        if post_processing_configs and len(post_processing_configs) != batch_size:
            raise ValueError(
                "post_processing_configs must have the same length as batch_input1"
            )

        # Prepare merged extra params
        if batch_extra_params and all(
            params == batch_extra_params[0] for params in batch_extra_params
        ):
            merged_extra_params = batch_extra_params[0]
        else:
            # Handle heterogeneous extra_params - use first non-None or empty dict
            merged_extra_params = next(
                (params for params in (batch_extra_params or []) if params), {}
            )

        try:
            # Perform batch inference
            batch_results, success = self.model_manager.batch_inference(
                batch_input1,
                batch_input2,
                merged_extra_params,
                stream_key,
                stream_info,
            )

            if not success:
                raise RuntimeError("Batch inference failed")

            # Process results
            results = []
            for i, result in enumerate(batch_results):
                input1 = batch_input1[i]

                if apply_post_processing:
                    # Get configuration for this specific input
                    config = None
                    if post_processing_configs:
                        config = post_processing_configs[i]

                    processed_result, post_processing_result = (
                        await self._apply_post_processing(result, input1, config, stream_key, stream_info)
                    )
                    results.append((processed_result, post_processing_result))
                else:
                    results.append((result, None))

            return results

        except Exception as e:
            raise RuntimeError(f"Batch inference failed: {str(e)}") from e

    def get_latest_inference_time(self) -> datetime:
        """Get the latest inference time."""
        return self.latest_inference_time

    def get_batch_stats(self) -> Dict[str, Any]:
        """Get statistics about the current batching state."""
        return {
            "dynamic_batching_enabled": self.dynamic_batching,
            "batch_size": self.batch_size,
            "max_batch_wait_time": self.max_batch_wait_time,
            "current_queue_size": len(self.batch_queue),
            "processing_batch": self.processing_batch,
        }

    async def flush_batch_queue(self) -> int:
        """Force process all remaining items in the batch queue.

        Returns:
            Number of items processed
        """
        if not self.dynamic_batching:
            return 0

        async with self.batch_lock:
            remaining_items = len(self.batch_queue)
            if remaining_items > 0 and not self.processing_batch:
                self.processing_batch = True
                asyncio.create_task(self._process_batch())

        return remaining_items

    def get_post_processing_cache_stats(self) -> Dict[str, Any]:
        """Get post-processing cache statistics from the underlying processor.
        
        Returns:
            Dict[str, Any]: Cache statistics including cached instances and keys
        """
        return self.post_processor.get_cache_stats()

    def clear_post_processing_cache(self) -> None:
        """Clear the post-processing cache in the underlying processor."""
        self.post_processor.clear_use_case_cache()
        self.logger.info("Cleared post-processing cache")


# DONE: Improved post-processing integration with new unified system
# DONE: Added support for per-request post-processing configuration
# DONE: Added utility functions for easy setup
# DONE: Added stream_key support to post-processing with caching
# TODO: Add support for multi-model execution
# TODO: Add the Metrics and Logging
# TODO: Add the Auto Scale Up and Scale Down
# TODO: Add Buffer Cache for the inference
# TODO: Add post-processing metrics and performance monitoring
# TODO: Add the support of Triton Model Manager
