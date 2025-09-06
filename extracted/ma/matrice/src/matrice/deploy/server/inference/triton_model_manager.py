import logging
import numpy as np
import requests
import time
from typing import Tuple, Dict, Any, Optional, List, Union
from simplified_triton_utils import TritonServer, TritonInference
import logging
import time
import requests
from typing import Union, List

class TritonModelManager:
    """Model manager for Triton Inference Server, aligned with pipeline and inference interface."""

    def __init__(
        self,
        model_name: str,
        model_path: str,
        runtime_framework: str,
        internal_server_type: str,
        internal_port: int,
        internal_host: str,
        input_size: Union[int, List[int]] = 640, # Priority Obj det
        num_classes: int = 10,
        num_model_instances: int = 1,
        use_dynamic_batching: bool = False,
        max_batch_size: int = 8,

        is_yolo: bool = False,
        use_trt_accelerator: bool = False,
    ):
        try:
            if internal_server_type not in ["rest", "grpc"]:
                logging.warning(f"Invalid internal_server_type '{internal_server_type}', defaulting to 'rest'")

            self.internal_server_type = internal_server_type
            self.internal_port = internal_port
            self.internal_host = internal_host
            self.use_dynamic_batching = use_dynamic_batching
            self.max_batch_size = max_batch_size
            self.model_instances = []
            self._round_robin_counter = 0

            self.triton_server = TritonServer(
                model_name=model_name,
                model_path=model_path,
                runtime_framework=runtime_framework,
                input_size=input_size,
                num_classes=num_classes,
                dynamic_batching=use_dynamic_batching,
                num_model_instances=num_model_instances,
                max_batch_size=max_batch_size,
                connection_protocol=internal_server_type,
                is_yolo=is_yolo,
                use_trt_accelerator=use_trt_accelerator,
            )
            
            logging.info(f"Starting Triton server on {internal_host}:{internal_port}...")
            self.triton_server_process = self.triton_server.setup(internal_port)

            logging.info("Waiting for Triton server to be ready...")
            self._wait_for_ready()

            for _ in range(num_model_instances):
                client = TritonInference(
                    server_type=self.triton_server.connection_protocol,
                    model_name=model_name,
                    internal_port=internal_port,
                    internal_host=internal_host,
                    runtime_framework=self.triton_server.runtime_framework,
                    is_yolo = self.triton_server.is_yolo,
                    input_size=input_size,
                    # action_tracker=self.triton_server.action_tracker,
                )
                self.model_instances.append(client)
            
            logging.info(f"Initialized TritonModelManager with {num_model_instances} client instances, protocol: {self.triton_server.connection_protocol}")
            
        except Exception as e:
            logging.error(f"Failed to initialize TritonModelManager: {str(e)}", exc_info=True)
            raise

    def _wait_for_ready(self):
        """Wait for Triton server to be ready with fixed retries and 5s sleep."""
        max_attempts = 30  # 150 seconds wait time
        for attempt in range(max_attempts):
            try:
                if self.internal_server_type == "rest":
                    response = requests.get(
                        f"http://{self.internal_host}:{self.internal_port}/v2/health/ready",
                        timeout=5
                    )
                    if response.status_code == 200:
                        logging.info("=========  Triton server is ready (REST) =========")
                        break
                    else:
                        logging.info(f"Attempt {attempt + 1}/{max_attempts} - server not ready, retrying in 5 seconds...")
                        time.sleep(5)

                else:  # gRPC
                    try:
                        import tritonclient.grpc as grpcclient
                    except ImportError:
                        grpcclient = None

                    if grpcclient is None:
                        raise ImportError("tritonclient.grpc required for gRPC")

                    with grpcclient.InferenceServerClient(f"{self.internal_host}:{self.internal_port}") as client:
                        if client.is_server_ready():
                            logging.info("=========  Triton server is ready (gRPC) =========")
                            break
                        else:
                            logging.info(f"Attempt {attempt + 1}/{max_attempts} - server not ready, retrying in 5 seconds...")
                            time.sleep(5)

            except Exception as e:
                if attempt < max_attempts - 1:
                    logging.info(f"Attempt {attempt + 1}/{max_attempts} failed, retrying in 5 seconds... (Error: {str(e)})")
                    time.sleep(5)
                else:
                    logging.error("Triton server failed to become ready after maximum attempts")
                    raise

            
    def get_model(self) -> Any:
        """Get a TritonInference client instance in round-robin fashion."""
        if not self.model_instances:
            logging.warning(f"No Triton clients available for model")
            return None
        model = self.model_instances[self._round_robin_counter % len(self.model_instances)]
        self._round_robin_counter = (self._round_robin_counter + 1) % len(self.model_instances)
        return model

    def inference(
        self,
        input1: Any,
        input2: Optional[Any] = None,
        extra_params: Optional[Dict[str, Any]] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
        input_hash: Optional[str] = None,
    ) -> Tuple[Any, bool]:
        """Perform synchronous single inference using TritonInference client.

        Args:
            input1: Primary input data (e.g., image bytes).
            input2: Secondary input data (optional, ignored for Triton).
            extra_params: Additional parameters for inference.
            stream_key: Stream key for caching.
            stream_info: Stream info for post-processing.
            input_hash: Input hash for caching.

        Returns:
            Tuple of (results, success_flag).
        """
        if input1 is None:
            raise ValueError("Input data cannot be None")
        try:
            client = self.get_model()
            if not client:
                raise RuntimeError("No Triton client available")
            results = client.inference(input1)
            results = client.format_response(results)
            return results, True
        except Exception as e:
            logging.error(f"Triton sync inference failed for: {str(e)}", exc_info=True)
            return None, False

    async def async_inference(
        self,
        input1: Union[bytes, np.ndarray],
        input2: Optional[Any] = None,
        extra_params: Optional[Dict[str, Any]] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
        input_hash: Optional[str] = None,
    ) -> Tuple[Any, bool]:
        """Perform asynchronous single inference using TritonInference client.
        Args:
            input1: Primary input data (Image bytes or numpy array).
            input2: Secondary input data (optional, ignored for Triton).
            extra_params: Additional parameters for inference.
            stream_key: Stream key for caching.
            stream_info: Stream info for post-processing.
            input_hash: Input hash for caching.
        Returns:
            Tuple of (results, success_flag).
        """
        

        if input1 is None:
            logging.error("Input data cannot be None")
            raise ValueError("Input data cannot be None")
        try:
            client = self.get_model()
            if not client:
                logging.error("No Triton client available")
                raise RuntimeError("No Triton client available")
            results = await client.async_inference(input1)
            results = client.format_response(results)
            logging.info(f"Async inference result: {results}")
            return results, True
        except Exception as e:
            logging.error(f"Triton async inference failed: {e}")
            return {"error": str(e), "predictions": None}, False

    def batch_inference(
        self,
        input1: List[Any],
        input2: Optional[List[Any]] = None,
        extra_params: Optional[Dict[str, Any]] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
        input_hash: Optional[str] = None,
    ) -> Tuple[List[Any], bool]:
        """Perform synchronous batch inference using TritonInference client.

        Args:
            input1: List of primary input data (e.g., image bytes).
            input2: List of secondary input data (optional, ignored for Triton).
            extra_params: Additional parameters for inference.
            stream_key: Stream key for caching.
            stream_info: Stream info for post-processing.
            input_hash: Input hash for caching.

        Returns:
            Tuple of (results_list, success_flag).
        """
        if not input1:
            raise ValueError("Batch input cannot be None")
        try:
            client = self.get_model()
            if not client:
                raise RuntimeError("No Triton client available")
            results = []

            if self.use_dynamic_batching:
                input_array = self._preprocess_batch_inputs(input1, client)
                batch_results = client.inference(input_array)
                results = self._split_batch_results(batch_results, len(input1))
            else:
                for inp in input1:
                    result = client.inference(inp)
                    results.append(result)

            results = [client.format_response(result) for result in results]
            return results, True
        except Exception as e:
            logging.error(f"Triton sync batch inference failed for: {str(e)}", exc_info=True)
            return None, False

    async def async_batch_inference(
        self,
        input1: List[Any],
        input2: Optional[List[Any]] = None,
        extra_params: Optional[Dict[str, Any]] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
        input_hash: Optional[str] = None,
    ) -> Tuple[List[Any], bool]:
        """Perform asynchronous batch inference using TritonInference client.

        Args:
            input1: List of primary input data (e.g., image bytes).
            input2: List of secondary input data (optional, ignored for Triton).
            extra_params: Additional parameters for inference.
            stream_key: Stream key for caching.
            stream_info: Stream info for post-processing.
            input_hash: Input hash for caching.

        Returns:
            Tuple of (results_list, success_flag).
        """
        if not input1:
            raise ValueError("Batch input cannot be None")
        try:
            client = self.get_model()
            if not client:
                raise RuntimeError("No Triton client available")
            results = []

            if self.use_dynamic_batching:
                input_array = self._preprocess_batch_inputs(input1, client)
                batch_results = await client.async_inference(input_array)
                split_results = self._split_batch_results(batch_results, len(input1))
                results = [client.format_response(r) for r in split_results]
            else:
                for inp in input1:
                    res = await client.async_inference(inp)
                    results.append(client.format_response(res))

            return results, True
        except Exception as e:
            logging.error(f"Triton async batch inference failed for: {str(e)}", exc_info=True)
            return None, False

    def _preprocess_batch_inputs(self, input1: List[Any], client: TritonInference) -> np.ndarray:
        """Preprocess batch inputs for Triton dynamic batching.

        Args:
            input1: List of input data (e.g., image bytes).
            client: TritonInference client for shape and data type information.

        Returns:
            Preprocessed NumPy array for batch inference.
        """
        try:
            batch_inputs = []
            for inp in input1:
                arr = client._preprocess_input(inp)

                if arr.ndim == 4 and arr.shape[0] == 1:
                    arr = np.squeeze(arr, axis=0)

                if arr.ndim != 3:
                    logging.warning(f"Unexpected input shape {arr.shape}, expected (C,H,W) after preprocessing")

                batch_inputs.append(arr)

            # Stack into final batch (B, C, H, W)
            stacked = np.stack(batch_inputs, axis=0)
            # Ensure C-contiguous (important for Triton)
            return np.ascontiguousarray(stacked)

        except Exception as e:
            logging.error(f"Failed to preprocess batch inputs: {str(e)}", exc_info=True)
            raise


    def _split_batch_results(self, batch_results: np.ndarray, batch_size: int) -> List[Any]:
        """Split batch results into individual results.

        Args:
            batch_results: NumPy array of batch inference results.
            batch_size: Number of inputs in the batch.

        Returns:
            List of individual results.
        """
        try:
            if batch_results.ndim == 1:
                return [batch_results] * batch_size
            return [batch_results[i] for i in range(batch_size)]
        except Exception as e:
            logging.error(f"Failed to split batch results: {str(e)}", exc_info=True)
            raise