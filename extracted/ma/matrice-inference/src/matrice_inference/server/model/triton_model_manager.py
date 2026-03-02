import logging
import numpy as np
import requests
import time
import asyncio
from typing import Tuple, Any, List, Union, Callable, Dict
from matrice_inference.server.model.triton_server import TritonServer, TritonInference

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
        is_ocr: bool = False,
        use_trt_accelerator: bool = False,
        preprocess_fn: Callable = None, 
        postprocess_fn: Callable = None,
        preprocess_params: Dict[str, Any] = None,
        postprocess_params: Dict[str, Any] = None,
    ):
        try:
            if internal_server_type not in ["rest", "grpc"]:
                logging.warning(f"Invalid internal_server_type '{internal_server_type}', defaulting to 'rest'")

            if preprocess_fn is None or postprocess_fn is None:
                raise ValueError("preprocess_fn and postprocess_fn must be provided")

            self.internal_server_type = internal_server_type
            self.internal_port = internal_port
            self.internal_host = internal_host
            self.use_dynamic_batching = use_dynamic_batching
            self.max_batch_size = max_batch_size
            self.preprocess_params = preprocess_params or {}
            self.postprocess_params = postprocess_params or {}
            self.preprocess_fn = self._create_preprocess_wrapper(preprocess_fn)
            self.postprocess_fn = self._create_postprocess_wrapper(postprocess_fn)

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
                is_ocr=is_ocr,
                use_trt_accelerator=use_trt_accelerator,
            )

            logging.info(f"Starting Triton server on {internal_host}:{internal_port}...")
            self.triton_server_process = self.triton_server.setup(internal_port)

            logging.info("Waiting for Triton server to be ready...")
            self._wait_for_ready()

            self.client = TritonInference(
                server_type=self.triton_server.connection_protocol,
                model_name=model_name,
                internal_port=internal_port,
                internal_host=internal_host,
                runtime_framework=self.triton_server.runtime_framework,
                is_yolo=self.triton_server.is_yolo,
                is_ocr=self.triton_server.is_ocr,
                input_size=input_size,
            )
            
            logging.info(f"Initialized TritonModelManager with {num_model_instances} client instances, protocol: {self.triton_server.connection_protocol}")
            
        except Exception as e:
            logging.error(f"Failed to initialize TritonModelManager: {str(e)}", exc_info=True)
            raise

    def _create_preprocess_wrapper(self, preprocess_fn: Callable) -> Callable:
        """
        Create a wrapper for preprocessing function to standardize input handling.

        Args:
            preprocess_fn: Original preprocessing function (bytes/np.ndarray -> np.ndarray or tuple(np.ndarray, dict)).

        Returns:
            Callable: Wrapped function ensuring consistent input/output and parameter filtering.
        """
        def wrapper(input_data: Union[bytes, np.ndarray], **kwargs) -> np.ndarray:
            try:
                # Filter kwargs to match function signature
                param_names = preprocess_fn.__code__.co_varnames[:preprocess_fn.__code__.co_argcount]
                filtered_kwargs = {k: v for k, v in {**self.preprocess_params, **kwargs}.items() if k in param_names}
                result = preprocess_fn(input_data, **filtered_kwargs)
                
                # Handle YOLO's tuple return (array, padding_info)
                if isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], np.ndarray):
                    arr, metadata = result
                    self.postprocess_params["padding_info"] = metadata
                else:
                    arr = result
                
                if not isinstance(arr, np.ndarray):
                    raise ValueError(f"Preprocess function must return np.ndarray or tuple(np.ndarray, dict), got {type(arr)}")
                if arr.dtype != np.float32:
                    arr = arr.astype(np.float32)
                if not arr.flags.c_contiguous:
                    arr = np.ascontiguousarray(arr)
                if arr.ndim != 4 or arr.shape[0] != 1 or arr.shape[1] not in (1, 3):
                    raise ValueError(f"Expected preprocessed shape [1, C, H, W] with C=1 or 3, got {arr.shape}")
                
                logging.debug(f"Preprocessed input shape: {arr.shape}, dtype: {arr.dtype}")
                return arr
            except Exception as e:
                logging.error(f"Preprocessing failed: {str(e)}")
                raise ValueError(f"Preprocessing failed: {str(e)}") from e
        
        return wrapper

    def _create_postprocess_wrapper(self, postprocess_fn: Callable) -> Callable:
        """
        Create a wrapper for postprocessing function to standardize output handling.

        Args:
            postprocess_fn: Original postprocessing function (np.ndarray -> dict).

        Returns:
            Callable: Wrapped function ensuring consistent output format and parameter filtering.
        """
        def wrapper(output: np.ndarray, **kwargs) -> Dict[str, Any]:
            try:
                # Filter kwargs to match function signature and add model_id
                param_names = postprocess_fn.__code__.co_varnames[:postprocess_fn.__code__.co_argcount]
                filtered_kwargs = {
                    k: v for k, v in {**self.postprocess_params, **kwargs, "model_id": self.model_name}.items()
                    if k in param_names
                }
                result = postprocess_fn(output, **filtered_kwargs)
                
                
                logging.debug(f"Postprocessed result: {result}")
                return result
            except Exception as e:
                logging.error(f"Postprocessing failed: {str(e)}")
                raise ValueError(f"Postprocessing failed: {str(e)}") from e
        
        return wrapper

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

    def inference(
        self,
        input: bytes,
    ) -> Tuple[Any, bool]:
        """Perform synchronous single inference using TritonInference client.

        Args:
            input: Primary input data (e.g., image bytes).
        
        Returns:
            Tuple of (results, success_flag).
        """
        if input is None:
            raise ValueError("Input data cannot be None")
        try:
            client = self.client
            if not client:
                raise RuntimeError("No Triton client available")
            processed_input = self.preprocess_fn(input)
            raw_output = client.inference(processed_input)
            results = self.postprocess_fn(raw_output)
            return results, True
        except Exception as e:
            logging.error(f"Triton sync inference failed for: {str(e)}", exc_info=True)
            return None, False

    async def async_inference(
        self,
        input: Union[bytes, np.ndarray],
    ) -> Tuple[Any, bool]:
        """Perform asynchronous single inference using TritonInference client.
        Args:
            input: Primary input data (Image bytes or numpy array).
        
        Returns:
            Tuple of (results, success_flag).
        """


        if input is None:
            logging.error("Input data cannot be None")
            raise ValueError("Input data cannot be None")
        try:
            client = self.client
            if not client:
                logging.error("No Triton client available")
                raise RuntimeError("No Triton client available")
            processed_input = self.preprocess_fn(input)
            raw_output = await client.async_inference(processed_input)
            results = self.postprocess_fn(raw_output)
            logging.info(f"Async inference result: {results}")
            return results, True
        except Exception as e:
            logging.error(f"Triton async inference failed: {e}")
            return {"error": str(e), "predictions": None}, False


    def batch_inference(
        self,
        input: List[bytes],
    ) -> Tuple[List[Any], bool]:
        """Perform synchronous batch inference using TritonInference client.

        Args:
            input: List of primary input data (e.g., image bytes).
        
        Returns:
            Tuple of (results_list, success_flag).
        """
        if not input:
            raise ValueError("Batch input cannot be None")
        try:
            client = self.client
            if not client:
                raise RuntimeError("No Triton client available")
            results = []

            if self.use_dynamic_batching:
                input_array = self._preprocess_batch_inputs(input, client)
                batch_results = client.inference(input_array)
                split_raw_results = self._split_batch_results(batch_results, len(input))
                results = [self.postprocess_fn(r) for r in split_raw_results]
                logging.info(f"Batch inference results: {results}")
            else:
                for inp in input:
                    preprocessed_inp = self.preprocess_fn(inp)
                    raw_res = client.inference(preprocessed_inp)
                    postprocessed_res = self.postprocess_fn(raw_res)
                    results.append(postprocessed_res)

            return results, True
        except Exception as e:
            logging.error(f"Triton sync batch inference failed for: {str(e)}", exc_info=True)
            return None, False

    async def async_batch_inference(
        self,
        input: List[bytes],
    ) -> Tuple[List[Any], bool]:
        """Perform asynchronous batch inference using TritonInference client.

        Args:
            input: List of primary input data (e.g., image bytes).

        Returns:
            Tuple of (results_list, success_flag).
        """
        if not input:
            raise ValueError("Batch input cannot be None")
        try:
            client = self.client
            if not client:
                raise RuntimeError("No Triton client available")
            results = []

            if self.use_dynamic_batching:
                input_array = self._preprocess_batch_inputs(input, client)
                batch_results = await client.async_inference(input_array)
                split_raw_results = self._split_batch_results(batch_results, len(input))
                results = [self.postprocess_fn(r) for r in split_raw_results]
            else:
                tasks = [client.async_inference(self.preprocess_fn(inp)) for inp in input]
                raw_results = await asyncio.gather(*tasks)
                results = [self.postprocess_fn(res) for res in raw_results]
            logging.info(f"Async batch inference results: {results}")
            return results, True
        except Exception as e:
            logging.error(f"Triton async batch inference failed: {str(e)}", exc_info=True)
            return None, False
        
        
    def _preprocess_batch_inputs(self, input: List[bytes], client: TritonInference) -> np.ndarray:
        """Preprocess batch inputs for Triton dynamic batching.

        Args:
            input: List of input data (e.g., image bytes).
            client: TritonInference client for shape and data type information.

        Returns:
            Preprocessed NumPy array for batch inference.
        """
        try:
            batch_inputs = []
            # TODO (x1): Parallelize this loop -- ensure pre and post process work across dimensions or thread level parallelism
            for inp in input:
                arr = self.preprocess_fn(inp)

                if arr.ndim == 4 and arr.shape[0] == 1:
                    arr = np.squeeze(arr, axis=0)

                if arr.ndim != 3 or arr.shape[0] not in (1, 3):
                    raise ValueError(f"Expected preprocessed shape (C,H,W) with C=1 or 3, got {arr.shape}")

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
            if batch_results.shape[0] != batch_size:
                raise ValueError(f"Batch results shape {batch_results.shape} does not match batch_size {batch_size}")
            return [batch_results[i:i+1] for i in range(batch_size)] # Keep batch dim for each
        except Exception as e:
            logging.error(f"Failed to split batch results: {str(e)}")
            raise

# TODO: Remove deprecated redundant flags like is_yolo, is_ocr after ensuring pipeline updates