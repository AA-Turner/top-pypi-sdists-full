import logging
import gc
from typing import Tuple, Any, Optional, List, Callable, Dict

class ModelManager:
    """Minimal ModelManager that focuses on model lifecycle and prediction calls."""

    def __init__(
        self,
        action_tracker: Any,
        load_model: Optional[Callable] = None,
        predict: Optional[Callable] = None,
        batch_predict: Optional[Callable] = None,
        async_predict: Optional[Callable] = None,
        async_batch_predict: Optional[Callable] = None,
        async_load_model: Optional[Callable] = None,
        num_model_instances: int = 1,
        model_path: Optional[str] = None, # For local model loading testing
    ):
        """Initialize the ModelManager

        Args:
            action_tracker: Tracker for monitoring actions.
            load_model: Function to load the model (synchronous).
            predict: Function to run single predictions (sync).
            batch_predict: Function to run batch predictions (sync).
            async_predict: Function to run single predictions (async).
            async_batch_predict: Function to run batch predictions (async).
            async_load_model: Function to load the model asynchronously (loaded lazily in worker thread's event loop).
            num_model_instances: Number of model instances to create.
            model_path: Path to the model directory.
        """
        try:
            self.load_model = self._create_load_model_wrapper(load_model)
            self.predict = self._create_prediction_wrapper(predict)
            self.batch_predict = self._create_prediction_wrapper(batch_predict)
            self.async_predict = self._create_async_prediction_wrapper(async_predict)
            self.async_batch_predict = self._create_async_batch_prediction_wrapper(async_batch_predict)
            self.async_load_model = self._create_async_load_model_wrapper(async_load_model)
            self.action_tracker = action_tracker

            # Model instances
            self.model_instances = []
            self._round_robin_counter = 0
            self.model_path = model_path

            # Lazy loading: If async_load_model is provided, defer loading to worker threads
            # Otherwise, load synchronously now for backward compatibility
            if self.async_load_model:
                # Create placeholders for lazy loading
                for _ in range(num_model_instances):
                    self.model_instances.append(None)
                logging.info(f"Deferred model loading: {num_model_instances} instances will be lazy-loaded in worker threads")
            else:
                # Load synchronously (existing behavior)
                for _ in range(num_model_instances):
                    self.scale_up()
        except Exception as e:
            logging.error(f"Failed to initialize ModelManager: {str(e)}")
            raise

    def _create_load_model_wrapper(self, load_model_func: Callable):
        """Create a wrapper function that handles parameter passing to the load model function.

        Args:
            load_model_func: The load model function to wrap

        Returns:
            A wrapper function that handles parameter passing safely
        """
        if not load_model_func:
            return load_model_func

        def wrapper():
            """Wrapper that safely calls the load model function with proper parameter handling."""
            try:
                # Get function parameter names
                param_names = load_model_func.__code__.co_varnames[
                    : load_model_func.__code__.co_argcount
                ]
                
                arg_count = load_model_func.__code__.co_argcount
                
                # Handle case where function has exactly 1 argument and it's not named
                if arg_count == 1 and param_names and param_names[0] in ['_', 'arg', 'args']:
                    # Pass action_tracker as positional argument
                    if self.action_tracker is not None:
                        return load_model_func(self.action_tracker)
                    else:
                        # Try calling with no arguments if action_tracker is None
                        return load_model_func()
                
                # Handle case where function has exactly 1 argument with a recognizable name
                if arg_count == 1 and param_names:
                    param_name = param_names[0]
                    # Check if it's likely to want action_tracker
                    if param_name in ["action_tracker", "actionTracker", "tracker"]:
                        return load_model_func(self.action_tracker)
                    elif param_name in ["model_path", "path"] and self.model_path is not None:
                        return load_model_func(self.model_path)
                    else:
                        # Pass action_tracker as fallback for single argument functions
                        return load_model_func(self.action_tracker if self.action_tracker is not None else None)
                
                # Build filtered parameters based on what the function accepts (original logic for multi-param functions)
                filtered_params = {}
                
                # Add action_tracker if the function accepts it
                if self.action_tracker is not None:
                    if "action_tracker" in param_names:
                        filtered_params["action_tracker"] = self.action_tracker
                    elif "actionTracker" in param_names:
                        filtered_params["actionTracker"] = self.action_tracker
                
                # Add model_path if the function accepts it
                if "model_path" in param_names and self.model_path is not None:
                    filtered_params["model_path"] = self.model_path

                return load_model_func(**filtered_params)

            except Exception as e:
                error_msg = f"Load model function execution failed: {str(e)}"
                logging.error(error_msg, exc_info=True)
                raise RuntimeError(error_msg) from e

        return wrapper

    def _create_async_load_model_wrapper(self, async_load_model_func: Callable):
        """Create a wrapper function that handles parameter passing to the async load model function.

        Args:
            async_load_model_func: The async load model function to wrap

        Returns:
            A wrapper function that handles parameter passing safely, or None if no function provided
        """
        if not async_load_model_func:
            return None

        async def wrapper():
            """Wrapper that safely calls the async load model function with proper parameter handling."""
            try:
                # Get function parameter names
                param_names = async_load_model_func.__code__.co_varnames[
                    : async_load_model_func.__code__.co_argcount
                ]

                arg_count = async_load_model_func.__code__.co_argcount

                # Handle case where function has exactly 1 argument and it's not named
                if arg_count == 1 and param_names and param_names[0] in ['_', 'arg', 'args']:
                    # Pass action_tracker as positional argument
                    if self.action_tracker is not None:
                        return await async_load_model_func(self.action_tracker)
                    else:
                        # Try calling with no arguments if action_tracker is None
                        return await async_load_model_func()

                # Handle case where function has exactly 1 argument with a recognizable name
                if arg_count == 1 and param_names:
                    param_name = param_names[0]
                    # Check if it's likely to want action_tracker
                    if param_name in ["action_tracker", "actionTracker", "tracker"]:
                        return await async_load_model_func(self.action_tracker)
                    elif param_name in ["model_path", "path"] and self.model_path is not None:
                        return await async_load_model_func(self.model_path)
                    else:
                        # Pass action_tracker as fallback for single argument functions
                        return await async_load_model_func(self.action_tracker if self.action_tracker is not None else None)

                # Build filtered parameters based on what the function accepts (original logic for multi-param functions)
                filtered_params = {}

                # Add action_tracker if the function accepts it
                if self.action_tracker is not None:
                    if "action_tracker" in param_names:
                        filtered_params["action_tracker"] = self.action_tracker
                    elif "actionTracker" in param_names:
                        filtered_params["actionTracker"] = self.action_tracker

                # Add model_path if the function accepts it
                if "model_path" in param_names and self.model_path is not None:
                    filtered_params["model_path"] = self.model_path

                return await async_load_model_func(**filtered_params)

            except Exception as e:
                error_msg = f"Async load model function execution failed: {str(e)}"
                logging.error(error_msg, exc_info=True)
                raise RuntimeError(error_msg) from e

        return wrapper

    def _create_async_prediction_wrapper(self, async_predict_func: Callable):
        """Create a wrapper function that handles parameter passing to the async prediction function.

        Args:
            async_predict_func: The async prediction function to wrap

        Returns:
            A wrapper function that handles parameter passing safely
        """
        if not async_predict_func:
            return None

        async def wrapper(model, input: bytes, extra_params: Dict[str, Any]=None, stream_key: Optional[str]=None, stream_info: Optional[Dict[str, Any]]=None) -> dict:
            """Wrapper that safely calls the async prediction function with proper parameter handling."""
            try:
                # Ensure extra_params is a dictionary
                if extra_params is None:
                    extra_params = {}
                elif isinstance(extra_params, list):
                    logging.warning(f"extra_params received as list instead of dict, converting: {extra_params}")
                    # Convert list to dict if possible, otherwise use empty dict
                    if len(extra_params) == 0:
                        extra_params = {}
                    elif all(isinstance(item, dict) for item in extra_params):
                        # Merge all dictionaries in the list
                        merged_params = {}
                        for item in extra_params:
                            merged_params.update(item)
                        extra_params = merged_params
                    else:
                        logging.error(f"Cannot convert extra_params list to dict: {extra_params}")
                        extra_params = {}
                elif not isinstance(extra_params, dict):
                    logging.warning(f"extra_params is not a dict, using empty dict instead. Received: {type(extra_params)}")
                    extra_params = {}
                
                param_names = async_predict_func.__code__.co_varnames[
                    : async_predict_func.__code__.co_argcount
                ]
                filtered_params = {
                    k: v for k, v in extra_params.items() if k in param_names
                }

                # Build arguments list
                args = [model, input]

                # Add stream_key if the function accepts it (regardless of its value)
                if "stream_key" in param_names:
                    filtered_params["stream_key"] = stream_key

                if "stream_info" in param_names:
                    filtered_params["stream_info"] = stream_info

                return await async_predict_func(*args, **filtered_params)

            except Exception as e:
                error_msg = f"Async prediction function execution failed: {str(e)}"
                logging.error(error_msg, exc_info=True)
                raise RuntimeError(error_msg) from e

        return wrapper

    def _create_async_batch_prediction_wrapper(self, async_batch_predict_func: Callable):
        """Create a wrapper function that handles parameter passing to the async batch prediction function.

        Args:
            async_batch_predict_func: The async batch prediction function to wrap

        Returns:
            A wrapper function that handles parameter passing safely, or None if no function provided
        """
        if not async_batch_predict_func:
            return None

        async def wrapper(model, inputs: List[bytes], extra_params: Dict[str, Any]=None, stream_key: Optional[str]=None, stream_info: Optional[Dict[str, Any]]=None) -> List[dict]:
            """Wrapper that safely calls the async batch prediction function with proper parameter handling."""
            try:
                # Ensure extra_params is a dictionary
                if extra_params is None:
                    extra_params = {}
                elif isinstance(extra_params, list):
                    logging.warning(f"extra_params received as list instead of dict, converting: {extra_params}")
                    if len(extra_params) == 0:
                        extra_params = {}
                    elif all(isinstance(item, dict) for item in extra_params):
                        merged_params = {}
                        for item in extra_params:
                            merged_params.update(item)
                        extra_params = merged_params
                    else:
                        logging.error(f"Cannot convert extra_params list to dict: {extra_params}")
                        extra_params = {}
                elif not isinstance(extra_params, dict):
                    logging.warning(f"extra_params is not a dict, using empty dict instead. Received: {type(extra_params)}")
                    extra_params = {}

                param_names = async_batch_predict_func.__code__.co_varnames[
                    : async_batch_predict_func.__code__.co_argcount
                ]
                filtered_params = {
                    k: v for k, v in extra_params.items() if k in param_names
                }

                # Build arguments list
                args = [model, inputs]

                # Add stream_key if the function accepts it
                if "stream_key" in param_names:
                    filtered_params["stream_key"] = stream_key

                if "stream_info" in param_names:
                    filtered_params["stream_info"] = stream_info

                return await async_batch_predict_func(*args, **filtered_params)

            except Exception as e:
                error_msg = f"Async batch prediction function execution failed: {str(e)}"
                logging.error(error_msg, exc_info=True)
                raise RuntimeError(error_msg) from e

        return wrapper

    def scale_up(self):
        """Load the model into memory (scale up)"""
        try:
            self.model_instances.append(self.load_model())
            return True
        except Exception as e:
            logging.error(f"Failed to scale up model: {str(e)}")
            return False

    def scale_down(self):
        """Unload the model from memory (scale down)"""
        if not self.model_instances:
            return True
        try:
            del self.model_instances[-1]
            gc.collect()
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            return True
        except Exception as e:
            logging.error(f"Failed to scale down model: {str(e)}")
            return False

    async def ensure_models_loaded(self):
        """Ensure all model instances are loaded in the current event loop.

        This method MUST be called in the StreamingPipeline's event loop
        before inference begins. It loads models asynchronously if async_load_model
        is provided, otherwise loads synchronously.

        This ensures all models are loaded in the same event loop used for inference.

        Returns:
            bool: True if all models loaded successfully, False otherwise
        """
        try:
            num_to_load = len(self.model_instances)
            logging.info(f"Ensuring {num_to_load} model instances are loaded...")

            for i in range(num_to_load):
                if self.model_instances[i] is not None:
                    logging.debug(f"Model instance {i} already loaded, skipping")
                    continue

                logging.info(f"Loading model instance {i}...")

                if self.async_load_model:
                    # Async loading in current event loop (StreamingPipeline's loop)
                    try:
                        model = await self.async_load_model()
                        self.model_instances[i] = model
                        logging.info(f"✓ Model instance {i} loaded asynchronously in StreamingPipeline event loop")
                    except Exception as e:
                        logging.error(f"✗ Async model loading failed for instance {i}: {e}", exc_info=True)
                        # Try fallback to sync loading
                        if self.load_model:
                            logging.warning(f"Attempting fallback to synchronous model loading for instance {i}")
                            try:
                                model = self.load_model()
                                self.model_instances[i] = model
                                logging.info(f"✓ Model instance {i} loaded synchronously (fallback)")
                            except Exception as sync_error:
                                logging.error(f"✗ Synchronous fallback also failed for instance {i}: {sync_error}", exc_info=True)
                                return False
                        else:
                            logging.error(f"✗ No fallback load_model available for instance {i}")
                            return False
                else:
                    # Synchronous loading
                    if not self.load_model:
                        logging.error("No load_model function provided")
                        return False
                    try:
                        model = self.load_model()
                        self.model_instances[i] = model
                        logging.info(f"✓ Model instance {i} loaded synchronously")
                    except Exception as e:
                        logging.error(f"✗ Model loading failed for instance {i}: {e}", exc_info=True)
                        return False

            logging.info(f"✓ All {num_to_load} model instances loaded successfully")
            return True

        except Exception as e:
            logging.error(f"✗ Critical error in ensure_models_loaded: {e}", exc_info=True)
            return False

    def get_model(self):
        """Get the model instance in round-robin fashion.

        Models MUST be loaded before calling this method by calling ensure_models_loaded()
        in the StreamingPipeline's event loop. This ensures all async operations use
        the same event loop.

        Returns:
            model: The loaded model instance

        Raises:
            RuntimeError: If model is not loaded
        """
        if not self.model_instances:
            error_msg = "No model instances available"
            logging.error(error_msg)
            raise RuntimeError(error_msg)

        order = self._round_robin_counter % len(self.model_instances)
        model = self.model_instances[order]

        if not model:
            # Model not loaded - this is an error
            error_msg = (
                f"Model instance {order} not loaded. "
                f"Call ensure_models_loaded() in StreamingPipeline's event loop "
                f"before starting inference."
            )
            logging.error(error_msg)
            raise RuntimeError(error_msg)

        # Increment counter for next call
        self._round_robin_counter = (self._round_robin_counter + 1) % len(
            self.model_instances
        )

        return model

    def _create_prediction_wrapper(self, predict_func: Callable):
        """Create a wrapper function that handles parameter passing to the prediction function.

        Args:
            predict_func: The prediction function to wrap

        Returns:
            A wrapper function that handles parameter passing safely, or None if predict_func is None
        """
        if not predict_func:
            # Log the issue but don't crash
            logging.warning(f"predict_func is {type(predict_func)} - returning None wrapper")
            return None

        # Validate that it's actually callable
        if not callable(predict_func):
            logging.error(f"predict_func is not callable: {type(predict_func)}")
            return None

        logging.info(f"✓ Creating prediction wrapper for {type(predict_func).__name__}")

        def wrapper(model, input: bytes, extra_params: Dict[str, Any]=None, stream_key: Optional[str]=None, stream_info: Optional[Dict[str, Any]]=None) -> dict:
            """Wrapper that safely calls the prediction function with proper parameter handling."""
            try:
                # Ensure extra_params is a dictionary
                if extra_params is None:
                    extra_params = {}
                elif isinstance(extra_params, list):
                    logging.warning(f"extra_params received as list instead of dict, converting: {extra_params}")
                    # Convert list to dict if possible, otherwise use empty dict
                    if len(extra_params) == 0:
                        extra_params = {}
                    elif all(isinstance(item, dict) for item in extra_params):
                        # Merge all dictionaries in the list
                        merged_params = {}
                        for item in extra_params:
                            merged_params.update(item)
                        extra_params = merged_params
                    else:
                        logging.error(f"Cannot convert extra_params list to dict: {extra_params}")
                        extra_params = {}
                elif not isinstance(extra_params, dict):
                    logging.warning(f"extra_params is not a dict, using empty dict instead. Received: {type(extra_params)}")
                    extra_params = {}
                
                param_names = predict_func.__code__.co_varnames[
                    : predict_func.__code__.co_argcount
                ]
                filtered_params = {
                    k: v for k, v in extra_params.items() if k in param_names
                }

                # Build arguments list
                args = [model, input]

                # Add stream_key if the function accepts it (regardless of its value)
                if "stream_key" in param_names:
                    filtered_params["stream_key"] = stream_key

                if "stream_info" in param_names:
                    filtered_params["stream_info"] = stream_info

                return predict_func(*args, **filtered_params)

            except Exception as e:
                error_msg = f"Prediction function execution failed: {str(e)}"
                logging.error(error_msg, exc_info=True)
                raise RuntimeError(error_msg) from e

        return wrapper

    def inference(self, input: bytes, extra_params: Dict[str, Any]=None, stream_key: Optional[str]=None, stream_info: Optional[Dict[str, Any]]=None) -> Tuple[dict, bool]:
        """Run inference on the provided input data.

        Args:
            input: Primary input data (can be image bytes or numpy array)
            extra_params: Additional parameters for inference (optional)
            stream_key: Stream key for the inference
            stream_info: Stream info for the inference
        Returns:
            Tuple of (results, success_flag)

        Raises:
            ValueError: If input data is invalid
        """
        if input is None:
            raise ValueError("Input data cannot be None")
        
        try:
            model = self.get_model()
            results = self.predict(model, input, extra_params, stream_key, stream_info)
            if self.action_tracker:
                results = self.action_tracker.update_prediction_results(results)
            return results, True
        except Exception as e:
            logging.error(f"Inference failed: {str(e)}")
            return None, False

    async def async_inference(self, input: bytes, extra_params: Dict[str, Any]=None, stream_key: Optional[str]=None, stream_info: Optional[Dict[str, Any]]=None) -> Tuple[dict, bool]:
        """Run asynchronous inference on the provided input data.

        Args:
            input: Primary input data (can be image bytes or numpy array)
            extra_params: Additional parameters for inference (optional)
            stream_key: Stream key for the inference
            stream_info: Stream info for the inference
        Returns:
            Tuple of (results, success_flag)

        Raises:
            ValueError: If input data is invalid
        """
        if input is None:
            raise ValueError("Input data cannot be None")
        
        if not self.async_predict:
            # Fallback to synchronous predict if async_predict is not available
            logging.debug("async_predict not available, falling back to synchronous predict")
            return self.inference(input, extra_params, stream_key, stream_info)
        
        try:
            model = self.get_model()
            results = await self.async_predict(model, input, extra_params, stream_key, stream_info)
            if self.action_tracker:
                results = self.action_tracker.update_prediction_results(results)
            return results, True
        except Exception as e:
            logging.error(f"Async inference failed: {str(e)}")
            return None, False

    def batch_inference(
        self, input: List[bytes], extra_params: Dict[str, Any]=None, stream_key: Optional[str]=None, stream_info: Optional[Dict[str, Any]]=None
    ) -> Tuple[List[dict], bool]:
        """Run synchronous batch inference on the provided input data.

        If batch_predict is not available, falls back to calling predict
        on each input individually (similar to async_inference fallback).

        Args:
            input: List of input data (e.g., image bytes)
            extra_params: Additional parameters for inference (optional)
            stream_key: Stream key for the inference
            stream_info: Stream info for the inference
        Returns:
            Tuple of (results_list, success_flag)

        Raises:
            ValueError: If input data is invalid
        """
        if input is None:
            raise ValueError("Input data cannot be None")
        try:
            model = self.get_model()

            # If batch_predict is not available, fall back to single-frame processing
            if not self.batch_predict:
                logging.debug(
                    f"batch_predict not available, falling back to single-frame processing "
                    f"for {len(input)} inputs"
                )
                results = []
                for single_input in input:
                    result, success = self.inference(single_input, extra_params, stream_key, stream_info)
                    if not success:
                        logging.error("Single-frame inference failed in batch fallback")
                        return None, False
                    results.append(result)
                return results, True

            # Normal batch processing
            results = self.batch_predict(model, input, extra_params, stream_key, stream_info)
            if self.action_tracker:
                for result in results:
                    self.action_tracker.update_prediction_results(result)
            return results, True
        except Exception as e:
            logging.error(f"Batch inference failed: {str(e)}")
            return None, False

    async def async_batch_inference(
        self, input: List[bytes], extra_params: Dict[str, Any]=None, stream_key: Optional[str]=None, stream_info: Optional[Dict[str, Any]]=None
    ) -> Tuple[List[dict], bool]:
        """Run asynchronous batch inference on the provided input data.

        Args:
            input: List of input data (e.g., image bytes)
            extra_params: Additional parameters for inference (optional)
            stream_key: Stream key for the inference
            stream_info: Stream info for the inference
        Returns:
            Tuple of (results_list, success_flag)

        Raises:
            ValueError: If input data is invalid
        """
        if input is None:
            raise ValueError("Input data cannot be None")

        # If async_batch_predict is not available, fallback to sync batch_inference
        if not self.async_batch_predict:
            logging.debug("async_batch_predict not available, falling back to synchronous batch_inference")
            return self.batch_inference(input, extra_params, stream_key, stream_info)

        try:
            model = self.get_model()
            results = await self.async_batch_predict(model, input, extra_params, stream_key, stream_info)
            if self.action_tracker:
                for result in results:
                    self.action_tracker.update_prediction_results(result)
            return results, True
        except Exception as e:
            logging.error(f"Async batch inference failed: {str(e)}")
            return None, False

# TODO: Add multi model execution with torch.cuda.stream()