from matrice.deploy.server.inference.model_manager import ModelManager
from matrice.deploy.server.inference.batch_manager import DynamicBatchManager, BatchRequest
from matrice.deploy.utils.post_processing import (
    PostProcessor,
    create_config_from_template
)
from matrice.deploy.utils.post_processing.core.config import BaseConfig
from matrice.deploy.utils.post_processing.config import (
    get_usecase_from_app_name,
    get_category_from_app_name,
)
from typing import Dict, Any, Optional, Callable, Tuple, List, Union
from matrice.action_tracker import ActionTracker
from datetime import datetime, timezone
import logging


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
        app_name: str = "",
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
            app_name: Application name for automatic config loading
        """
        self.logger = logging.getLogger(__name__)
        self.batch_size = batch_size
        self.dynamic_batching = dynamic_batching
        self.model_manager = model_manager
        self.action_tracker = action_tracker
        self.post_processor = PostProcessor()
        self.latest_inference_time = datetime.now(timezone.utc)
        self.max_batch_wait_time = max_batch_wait_time
        self.app_name = app_name

        # Set up index to category mapping
        self.index_to_category = self.action_tracker.get_index_to_category()
        if self.index_to_category:
            self.target_categories = list(self.index_to_category.values())
        else:
            self.target_categories = []

        # Set up default post-processing configuration
        self.post_processing_config = None
        if post_processing_config or self.app_name:
            self.logger.debug(f"Parsing post-processing config: {post_processing_config}")
            self.post_processing_config = self._parse_post_processing_config(
                post_processing_config,
                self.app_name
            )
            if self.post_processing_config:
                self.logger.info(f"Successfully parsed post-processing config for usecase: {self.post_processing_config.usecase}")
            else:
                self.logger.warning("Failed to parse post-processing config")
        else:
            self.logger.info("No post-processing config provided")

        self.custom_post_processing_fn = custom_post_processing_fn

        # Initialize dynamic batch manager if enabled
        self.batch_manager = None
        if self.dynamic_batching:
            self.batch_manager = DynamicBatchManager(
                batch_size=self.batch_size,
                max_batch_wait_time=self.max_batch_wait_time,
                model_manager=self.model_manager,
                post_processing_fn=self._apply_post_processing,
            )
        

    def _load_config_from_app_name(self, app_name: str) -> Optional[BaseConfig]:
        """Load default post-processing configuration based on app name.
        
        Args:
            app_name: The application name to map to a post-processing use case
            
        Returns:
            BaseConfig: The automatically loaded configuration, or None if no mapping found
        """  
        usecase = get_usecase_from_app_name(app_name)
        category = get_category_from_app_name(app_name)
        if not usecase or not category:
            self.logger.warning(f"No usecase or category found for app: {app_name}")
            return None
        config = self.post_processor.create_config(usecase, category)
        return config

    def _parse_post_processing_config(
        self, config: Union[Dict[str, Any], BaseConfig, str], app_name: Optional[str] = None
    ) -> Optional[BaseConfig]:
        """Parse post-processing configuration from various formats."""
        try:
            if not config and not app_name:
                return None
            if not config and app_name:
                config = self._load_config_from_app_name(app_name)
                if config:
                    return config
                else:
                    self.logger.warning(f"No config found for app: {app_name}")
            if isinstance(config, BaseConfig):
                config = config
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
                config = self.post_processor.create_config(
                    usecase, category, **config_params
                )
            elif isinstance(config, str):
                # Assume it's a use case name, create with defaults
                config = create_config_from_template(config)
            else:
                self.logger.warning(f"Unsupported config type: {type(config)}")
                return None
            if hasattr(config, "index_to_category"):
                if not config.index_to_category:
                    config.index_to_category = self.index_to_category
                else:
                    self.index_to_category = config.index_to_category
            if hasattr(config, "target_categories"):
                if not config.target_categories:
                    config.target_categories = self.target_categories
                else:
                    self.target_categories = config.target_categories
            return config
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
        input_hash: Optional[str] = None,
        camera_info: Optional[Dict[str, Any]] = None,
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
            input_hash: Input hash for the inference
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
        if self.dynamic_batching and self.batch_manager:
            return await self._dynamic_batch_inference(
                input1,
                input2,
                extra_params,
                apply_post_processing,
                post_processing_config,
                stream_key,
                stream_info,
                input_hash,
                camera_info,
            )

        # Get raw inference results
        try:
            raw_results, success = self.model_manager.inference(
                input1=input1,
                input2=input2,
                extra_params=extra_params,
                stream_key=stream_key,
                stream_info=stream_info,
                input_hash=input_hash
            )
            if not success:
                raise RuntimeError("Model inference failed")
        except Exception as e:
            raise RuntimeError(f"Model inference failed: {str(e)}") from e

        if not apply_post_processing:
            return raw_results, None

        # Apply post-processing
        return await self._apply_post_processing(
            raw_results, input1, post_processing_config, stream_key, stream_info, camera_info
        )

    async def _apply_post_processing(
        self,
        raw_results,
        input1,
        post_processing_config: Optional[Union[Dict[str, Any], BaseConfig, str]] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
        camera_info: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Any, Optional[Dict[str, Any]]]:
        """Apply post-processing to inference results"""
        try:
            # Determine which configuration to use
            config_to_use = self._parse_post_processing_config(post_processing_config) or self.post_processing_config
            
            # Normalize stream_key for logging and processing
            normalized_stream_key = stream_key or "default_stream"
            
            self.logger.debug(f"Post-processing config to use: {config_to_use} for stream: {normalized_stream_key}")

            if config_to_use is None and self.custom_post_processing_fn is None:
                self.logger.debug(
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

            if config_to_use is None:
                self.logger.error(f"Failed to parse post-processing configuration for stream: {normalized_stream_key}")
                return raw_results, {
                    "error": "Invalid post-processing configuration",
                    "status": "configuration_error",
                    "processed_data": raw_results,
                    "stream_key": normalized_stream_key,
                }

            # Apply post-processing using the unified processor
            result = self.post_processor.process(raw_results, config_to_use, input1, stream_key=stream_key, stream_info=stream_info)

            if result.is_success():
                # Extract agg_summary directly from result.data
                agg_summary = {}
                if hasattr(result, 'data') and isinstance(result.data, dict):
                    agg_summary = result.data.get("agg_summary", {})

                return raw_results, {
                    "status": "success",
                    "processing_time": result.processing_time,
                    "usecase": result.usecase,
                    "category": result.category,
                    "summary": result.summary,
                    "insights": result.insights,
                    "metrics": result.metrics,
                    "predictions": result.predictions,
                    "agg_summary": agg_summary,
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

    async def _dynamic_batch_inference(
        self,
        input1,
        input2=None,
        extra_params=None,
        apply_post_processing: bool = False,
        post_processing_config: Optional[Union[Dict[str, Any], BaseConfig, str]] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
        input_hash: Optional[str] = None,
        camera_info: Optional[Dict[str, Any]] = None,
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
            input_hash=input_hash,
            camera_info=camera_info,
        )

        # Add request to batch manager
        return await self.batch_manager.add_request(batch_request)

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
        input_hash: Optional[str] = None,
        camera_info: Optional[Dict[str, Any]] = None,
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
                input1=batch_input1,
                input2=batch_input2,
                extra_params=merged_extra_params,
                stream_key=stream_key,
                stream_info=stream_info,
                input_hash=input_hash,
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
                        await self._apply_post_processing(result, input1, config, stream_key, stream_info, camera_info)
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
        base_stats = {
            "dynamic_batching_enabled": self.dynamic_batching,
            "batch_size": self.batch_size,
            "max_batch_wait_time": self.max_batch_wait_time,
        }
        
        if self.batch_manager:
            base_stats.update(self.batch_manager.get_stats())
        else:
            base_stats.update({
                "current_queue_size": 0,
                "processing_batch": False,
            })
        
        return base_stats

    async def flush_batch_queue(self) -> int:
        """Force process all remaining items in the batch queue.

        Returns:
            Number of items processed
        """
        if not self.dynamic_batching or not self.batch_manager:
            return 0

        return await self.batch_manager.flush_queue()

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
    
    def _get_high_precision_timestamp(self) -> str:
        """Get high precision timestamp with microsecond granularity."""
        return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")


# DONE: Improved post-processing integration with new unified system
# DONE: Added support for per-request post-processing configuration
# DONE: Added utility functions for easy setup
# DONE: Added stream_key support to post-processing with caching
# DONE: Separated dynamic batching management into a separate class
# TODO: Add support for multi-model execution
# TODO: Add the Metrics and Logging
# TODO: Add the Auto Scale Up and Scale Down
# TODO: Add Buffer Cache for the inference
# TODO: Add post-processing metrics and performance monitoring
# TODO: Add the support of Triton Model Manager
