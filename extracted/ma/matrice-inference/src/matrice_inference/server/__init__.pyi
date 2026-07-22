"""Stub file for server directory."""
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from datetime import datetime
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from matrice.action_tracker import ActionTracker
from matrice_analytics.post_processing.post_processor import PostProcessor
from matrice_inference.server.inference_interface import InferenceInterface
from matrice_inference.server.model.model_manager_wrapper import ModelManagerWrapper
from matrice_inference.server.proxy_interface import MatriceProxyInterface
from matrice_inference.server.stream.analytics_publisher import AnalyticsPublisher
from matrice_inference.server.stream.camera_config_manager import CameraConfigManager
from matrice_inference.server.stream.stream_pipeline import StreamingPipeline
from matrice_inference.server.stream.utils import redact_sensitive
from urllib.parse import urlparse
import asyncio
import atexit
import httpx
import ipaddress
import logging
import multiprocessing as mp
import os
import pickle
import signal
import socket
import threading
import time
import urllib.request
import uuid
import uvicorn

# Constants
logger: Any = ...  # From proxy_interface
CLEANUP_DELAY_SECONDS: Any = ...  # From server
DEFAULT_EXTERNAL_PORT: Any = ...  # From server
DEFAULT_SHUTDOWN_THRESHOLD_MINUTES: Any = ...  # From server
FINAL_CLEANUP_DELAY_SECONDS: Any = ...  # From server
HEARTBEAT_INTERVAL_SECONDS: Any = ...  # From server
IP_FETCH_TIMEOUT_SECONDS: Any = ...  # From server
MAX_DEPLOYMENT_CHECK_FAILURES_BEFORE_SHUTDOWN: Any = ...  # From server
MAX_HEARTBEAT_FAILURES_BEFORE_SHUTDOWN: Any = ...  # From server
MAX_IP_FETCH_ATTEMPTS: Any = ...  # From server
MIN_SHUTDOWN_THRESHOLD_MINUTES: Any = ...  # From server
SHUTDOWN_CHECK_INTERVAL_SECONDS: Any = ...  # From server

# Classes
# From inference_interface
class InferenceInterface:
    # Interface for proxying requests to model servers with optional post-processing.

    def __init__(self, model_manager_wrapper: Optional[ModelManagerWrapper] = None, post_processor: Optional[PostProcessor] = None) -> None:
        """
        Initialize the inference interface.
        
        Args:
            model_manager_wrapper: Model manager for model inference. Can be None if not configured.
            post_processor: Post processor for post-processing
        """
        ...

    async def async_batch_inference(self, input_list: List[Any], extra_params: Optional[Dict[str, Any]] = None, stream_key: Optional[str] = None, stream_info: Optional[Dict[str, Any]] = None) -> Tuple[List[Any], bool]:
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
        ...

    async def async_inference(self, input, extra_params: Optional[Dict[str, Any]] = None, apply_post_processing: bool = False, post_processing_config: Optional[Union[Dict[str, Any], str]] = None, stream_key: Optional[str] = None, stream_info: Optional[Dict[str, Any]] = None, camera_info: Optional[Dict[str, Any]] = None, pipeline_event_loop: Optional[asyncio.AbstractEventLoop] = None) -> Tuple[Any, Optional[Dict[str, Any]]]:
        """
        Perform ASYNCHRONOUS inference using async_predict when available.
        
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
        ...

    def disable_worker_queue_routing(self) -> None:
        """
        Disable worker queue routing (used when pipeline stops).
        """
        ...

    def get_latest_inference_time(self) -> Any:
        """
        Get the latest inference time.
        """
        ...

    def has_async_predict(self) -> bool:
        """
        Check if async_predict is available in the underlying model manager.
        
                Returns:
                    bool: True if async_predict is available, False otherwise
        """
        ...

    async def inference(self, input, extra_params: Optional[Dict[str, Any]] = None, apply_post_processing: bool = False, post_processing_config: Optional[Union[Dict[str, Any], str]] = None, stream_key: Optional[str] = None, stream_info: Optional[Dict[str, Any]] = None, camera_info: Optional[Dict[str, Any]] = None, pipeline_event_loop: Optional[asyncio.AbstractEventLoop] = None, is_high_priority: bool = False) -> Tuple[Any, Optional[Dict[str, Any]]]:
        """
        Perform inference using the appropriate client with optional post-processing.
        
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
        ...

    def set_pipeline_event_loop(self, event_loop) -> None:
        """
        Set the pipeline event loop for thread-safe async operations.
        
                Args:
                    event_loop: Event loop from StreamingPipeline
        """
        ...

    def set_worker_queues(self, input_queues: List[mp.Queue], response_queue) -> None:
        """
        Set worker queues for routing direct API calls through inference workers.
        
                When set, direct API calls (e.g., identity images for face recognition) are
                routed through the same inference worker processes that handle streaming frames.
                This avoids greenlet context switching issues by ensuring all model inference
                happens in the worker process context.
        
                Args:
                    input_queues: List of multiprocessing queues (one per worker) for submitting tasks
                    response_queue: Multiprocessing queue for receiving inference results
        """
        ...

    def sync_batch_inference(self, input_list: List[Any], extra_params: Optional[Dict[str, Any]] = None, stream_key: Optional[str] = None, stream_info: Optional[Dict[str, Any]] = None) -> Tuple[List[Any], bool]:
        """
        Perform SYNCHRONOUS batch inference - pure Python, no asyncio.
        
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
        ...

    def sync_inference(self, input, extra_params: Optional[Dict[str, Any]] = None, apply_post_processing: bool = False, stream_key: Optional[str] = None, stream_info: Optional[Dict[str, Any]] = None) -> Tuple[Any, Optional[Dict[str, Any]]]:
        """
        Perform SYNCHRONOUS inference - pure Python, no asyncio.
        
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
        ...


# From proxy_interface
class MatriceProxyInterface:
    # Interface for proxying requests to model servers.

    def __init__(self, session, deployment_id: str, deployment_instance_id: str, external_port: int, inference_interface: Optional[InferenceInterface] = None, auth_refresh_interval_minutes: int = 1) -> None:
        """
        Initialize proxy server.
        
                Args:
                    session: Session object for authentication and RPC
                    deployment_id: ID of the deployment
                    deployment_instance_id: ID of the deployment instance
                    external_port: Port to expose externally
                    inference_interface: Interface for model inference. Can be None if not configured.
                    auth_refresh_interval_minutes: Minimum minutes between auth key refreshes
        """
        ...

    def start(self) -> Any:
        """
        Start the proxy server in a background thread.
        """
        ...

    def stop(self) -> Any:
        """
        Stop the proxy server gracefully.
        """
        ...

    def update_auth_keys(self) -> None:
        """
        Fetch and validate auth keys for the deployment.
        """
        ...

    def validate_auth_key(self, auth_key) -> Any:
        """
        Validate auth key.
        
                Args:
                    auth_key: Authentication key to validate
        
                Returns:
                    bool: True if valid, False otherwise
        """
        ...


# From server
class MatriceDeployServer:
    # Class for managing model deployment and server functionality.

    def __init__(self, load_model: Optional[Callable] = None, predict: Optional[Callable] = None, action_id: str = '', external_port: int = DEFAULT_EXTERNAL_PORT, batch_predict: Optional[Callable] = None, custom_post_processing_fn: Optional[Callable] = None, preprocess_fn: Optional[Callable] = None, postprocess_fn: Optional[Callable] = None, preprocess_params: Optional[Dict[str, Any]] = None, postprocess_params: Optional[Dict[str, Any]] = None, model_path: Optional[str] = None, runtime_framework: Optional[str] = None, use_dynamic_batching: bool = False, num_classes: Optional[int] = None, input_size: Optional[Any] = None, max_batch_size: Optional[int] = None, use_trt_accelerator: Optional[bool] = None, async_predict: Optional[Callable] = None, async_batch_predict: Optional[Callable] = None, async_load_model: Optional[Callable] = None, is_inference_API: bool = False, cuda_shm_engine: Optional[Any] = None) -> None:
        """
        Initialize MatriceDeploy.
        
                Args:
                    load_model (callable, optional): Function to load model. Defaults to None.
                    predict (callable, optional): Function to make predictions. Defaults to None.
                    batch_predict (callable, optional): Function to make batch predictions. Defaults to None.
                    custom_post_processing_fn (callable, optional): Function to get custom post processing config. Defaults to None.
                    action_id (str, optional): ID for action tracking. Defaults to "".
                    external_port (int, optional): External port number. Defaults to 80.
                    preprocess_fn: User-provided preprocessing function (optional).
                    postprocess_fn: User-provided postprocessing function (optional).
                    preprocess_params: Parameters for the preprocessing function.
                    postprocess_params: Parameters for the postprocessing function.
                    async_predict: Function for single async predictions. Defaults to None.
                    async_batch_predict: Function for batch async predictions. Defaults to None.
                    async_load_model: Function to load model asynchronously (loaded lazily in worker thread's event loop). Defaults to None.
                    is_inference_API (bool, optional): Whether this is an inference API server. If False, uses only 1 inference worker to avoid loading model multiple times. Defaults to False.
                Raises:
                    ValueError: If required parameters are invalid
                    Exception: If initialization fails
        """
        ...

    def start(self, block = True) -> Any:
        """
        Start the proxy interface and all server components.
        """
        ...

    def start_server(self, block = True) -> Any:
        """
        Start the server and related components.
        
                Args:
                    block: If True, wait for shutdown signal. If False, return immediately after starting.
        
                Raises:
                    Exception: If unable to initialize server
        """
        ...

    def stop_server(self) -> Any:
        """
        Stop the server and related components.
        """
        ...


# From server
class MatriceDeployServerUtils:
    # Utility class for managing deployment server operations.

    def __init__(self, action_tracker, inference_interface, external_port: int, main_server = None) -> None:
        """
        Initialize utils with reference to the main server.
        
                Args:
                    action_tracker: ActionTracker instance
                    inference_interface: InferenceInterface instance
                    external_port: External port number
                    main_server: Reference to the main MatriceDeployServer instance
        """
        ...

    def get_elapsed_time_since_latest_inference(self) -> Any:
        """
        Get time elapsed since latest inference.
        
                Returns:
                    float: Elapsed time in seconds
        
                Raises:
                    Exception: If unable to get elapsed time and no fallback available
        """
        ...

    def heartbeat_checker(self) -> Any:
        """
        Background thread to periodically send heartbeat.
        """
        ...

    def ip(self) -> Any:
        """
        Get the external IP address with caching and retry logic.
        """
        ...

    def is_instance_running(self) -> Any:
        """
        Check if deployment instance is running.
        
                Returns:
                    bool: True if instance is running, False otherwise
        """
        ...

    def run_background_checkers(self) -> Any:
        """
        Start the shutdown checker and heartbeat checker threads as daemons.
        """
        ...

    def shutdown(self) -> Any:
        """
        Gracefully shutdown the deployment instance.
        """
        ...

    def shutdown_checker(self) -> Any:
        """
        Background thread to periodically check for idle shutdown condition and deployment status.
        """
        ...

    def trigger_shutdown_if_needed(self) -> Any:
        """
        Check idle time and trigger shutdown if threshold exceeded.
        """
        ...

    def update_deployment_address(self) -> Any:
        """
        Update the deployment address in the backend.
        
                Raises:
                    Exception: If unable to update deployment address
        """
        ...

    def wait_for_shutdown(self) -> Any:
        """
        Wait for shutdown to be initiated by background checkers or external signals.
        
                This method blocks the main thread until shutdown is triggered.
        """
        ...


from . import inference_interface, proxy_interface, server