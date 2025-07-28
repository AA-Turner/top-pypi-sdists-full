import logging
import gc
from typing import Tuple
from matrice.deploy.server.inference.cache_manager import CacheManager


class ModelManager:
    """Enhanced ModelManager with multimodal support"""

    def __init__(
        self,
        model_id: str,
        internal_server_type: str,
        internal_port: int,
        internal_host: str,
        load_model=None,
        predict=None,
        batch_predict=None,
        action_tracker=None,
        num_model_instances: int = 1,
    ):
        """Initialize the ModelManager with optional multimodal support

        Args:
            model_id: ID of the model
            internal_server_type: Type of internal server
            internal_port: Internal port number
            internal_host: Internal host address
            load_model: Function to load the model
            predict: Function to run predictions
            batch_predict: Function to run batch predictions
            action_tracker: Tracker for monitoring actions
            num_model_instances: Number of model instances to create
            multimodal_config: Configuration for multimodal manager
        """
        try:
            self.model_id = model_id
            self.internal_server_type = internal_server_type
            self.internal_port = internal_port
            self.internal_host = internal_host

            self.load_model = load_model
            self.predict = self._create_prediction_wrapper(predict)
            self.batch_predict = self._create_prediction_wrapper(batch_predict)
            self.action_tracker = action_tracker
            self.cache_manager = CacheManager()
            self.model_instances = []

            for i in range(num_model_instances):
                self.scale_up()
        except Exception as e:
            logging.error(f"Failed to initialize ModelManager: {str(e)}")
            raise

    def scale_up(self):
        """Load the model into memory (scale up)"""
        try:
            self.model_instances.append(self.load_model(self.action_tracker))
            return True
        except Exception as e:
            logging.error(f"Failed to scale up model {self.model_id}: {str(e)}")
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
            logging.error(f"Failed to scale down model {self.model_id}: {str(e)}")
            return False

    def get_model(self):
        """Get the model instance in round-robin fashion"""
        if not self.model_instances:
            return None

        # Initialize round-robin counter if it doesn't exist
        if not hasattr(self, "_round_robin_counter"):
            self._round_robin_counter = 0

        # Get the current model instance
        model = self.model_instances[
            self._round_robin_counter % len(self.model_instances)
        ]

        # Increment counter for next call
        self._round_robin_counter = (self._round_robin_counter + 1) % len(
            self.model_instances
        )

        return model

    def _create_prediction_wrapper(self, predict_func):
        """Create a wrapper function that handles parameter passing to the prediction function.

        Args:
            predict_func: The prediction function to wrap

        Returns:
            A wrapper function that handles parameter passing safely
        """

        def wrapper(model, input1, input2=None, extra_params=None, stream_key=None, stream_info=None) -> dict:
            """Wrapper that safely calls the prediction function with proper parameter handling."""
            try:
                # Extract extra parameters and filter based on function signature
                extra_params = extra_params or {}
                param_names = predict_func.__code__.co_varnames[
                    : predict_func.__code__.co_argcount
                ]
                filtered_params = {
                    k: v for k, v in extra_params.items() if k in param_names
                }

                # Build arguments list
                args = [model, input1]

                # Add optional second input if present
                if input2 is not None:
                    args.append(input2)

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

    def inference(self, input1, input2=None, extra_params=None, stream_key=None, stream_info=None, input_hash=None) -> Tuple[dict, bool]:
        """Run inference on the provided input data.

        Args:
            input1: Primary input data
            input2: Secondary input data (optional)
            extra_params: Additional parameters for inference (optional)
            stream_key: Stream key for the inference
            stream_info: Stream info for the inference
            input_hash: Input hash for the inference
        Returns:
            Tuple of (results, success_flag)

        Raises:
            ValueError: If input data is invalid
        """
        if input1 is None:
            raise ValueError("Input data cannot be None")
        try:
            if input_hash:
                cached_result = self.cache_manager.get_cached_result(input_hash, stream_key)
                if cached_result:
                    return cached_result, True
            
            # Get the model
            model = self.get_model()

            # Run prediction
            results = self.predict(model, input1, input2, extra_params, stream_key, stream_info)

            # Update results through action tracker if available
            if self.action_tracker:
                results = self.action_tracker.update_prediction_results(results)

            if input_hash:
                self.cache_manager.set_cached_result(input_hash, results, stream_key)

            return results, True

        except Exception as e:
            logging.error(f"Inference failed on model {self.model_id}: {str(e)}")
            return None, False

    def batch_inference(
        self, input1, input2=None, extra_params=None, stream_key=None, stream_info=None, input_hash=None
    ) -> Tuple[dict, bool]:
        """Run batch inference on the provided input data.

        Args:
            input1: Primary input data
            input2: Secondary input data (optional)
            extra_params: Additional parameters for inference (optional)
            stream_key: Stream key for the inference
            stream_info: Stream info for the inference
            input_hash: Input hash for the inference
        Returns:
            Tuple of (results, success_flag)

        Raises:
            ValueError: If input data is invalid
        """
        if input1 is None:
            raise ValueError("Input data cannot be None")
        try:
            if input_hash:
                cached_result = self.cache_manager.get_cached_result(input_hash, stream_key)
                if cached_result:
                    return cached_result, True
            
            # Get the model
            model = self.get_model()

            # Run batch prediction
            if not self.batch_predict:
                logging.error(f"Batch prediction function not found for model {self.model_id}")
                return None, False
            results = self.batch_predict(model, input1, input2, extra_params, stream_key, stream_info)

            # Update results through action tracker if available
            if self.action_tracker:
                for result in results:
                    self.action_tracker.update_prediction_results(result)

            if input_hash:
                self.cache_manager.set_cached_result(input_hash, results, stream_key)

            return results, True

        except Exception as e:
            logging.error(f"Batch inference failed on model {self.model_id}: {str(e)}")
            return None, False
