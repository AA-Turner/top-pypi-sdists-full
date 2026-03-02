"""Stub file for server.stream directory."""
from typing import Any, Dict, List, Optional, Set, Tuple

from abc import ABC, abstractmethod
from collections import defaultdict
from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ThreadPoolExecutor, as_completed
from confluent_kafka import Producer
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import dataclass, field
from datetime import datetime
from datetime import datetime, timezone
from functools import lru_cache
from kafka import KafkaProducer
from matrice.action_tracker import ActionTracker
from matrice_analytics.post_processing.post_processor import PostProcessor
from matrice_common.optimize import InferenceResultCache
from matrice_common.rpc import RPC
from matrice_common.session import Session
from matrice_common.stream import EventListener
from matrice_common.stream.matrice_stream import MatriceStream
from matrice_common.stream.matrice_stream import MatriceStream, StreamType
from matrice_common.stream.matrice_stream import StreamType
from matrice_common.stream.shm_ring_buffer import ShmRingBuffer
from matrice_inference.server.inference_interface import InferenceInterface
from matrice_inference.server.model.model_manager_wrapper import ModelManagerWrapper
from matrice_inference.server.stream.analytics_publisher import AnalyticsPublisher
from matrice_inference.server.stream.app_deployment import AppDeployment
from matrice_inference.server.stream.app_event_listener import AppEventListener
from matrice_inference.server.stream.async_producer_pool import AsyncProducerPool
from matrice_inference.server.stream.consumer_manager import AsyncConsumerManager
from matrice_inference.server.stream.deployment_refresh_listener import DeploymentRefreshListener
from matrice_inference.server.stream.frame_cache import RedisFrameCache
from matrice_inference.server.stream.inference_metric_logger import InferenceMetricLogger
from matrice_inference.server.stream.inference_metric_logger import InferenceMetricLogger, KafkaMetricPublisher
from matrice_inference.server.stream.inference_worker import MultiprocessInferencePool
from matrice_inference.server.stream.metric_publisher import MetricPublisher, KafkaMetricPublisher, NoOpMetricPublisher
from matrice_inference.server.stream.post_processing_manager import MultiprocessPostProcessingPool
from matrice_inference.server.stream.stream_pipeline import StreamingPipeline
from matrice_inference.server.stream.utils import CameraConfig
from matrice_inference.server.stream.utils import CameraConfig, StreamMessage
from matrice_inference.server.stream.worker_metrics import MultiprocessWorkerMetrics
from matrice_inference.server.stream.worker_metrics import WorkerMetrics
from matrice_inference.server.stream.worker_metrics import WorkerMetrics, MetricSnapshot, MultiprocessMetricsCollector
from redis.asyncio import Redis
import asyncio
import base64
import hashlib
import json
import logging
import multiprocessing as mp
import os
import queue
import redis.asyncio as aioredis
import subprocess
import sys
import threading
import time
import uuid

# Constants
KEY_CAMERA_ID: Any = ...  # From async_producer_pool
KEY_DATA: Any = ...  # From async_producer_pool
KEY_FRAME_ID: Any = ...  # From async_producer_pool
KEY_INPUT_STREAM: Any = ...  # From async_producer_pool
KEY_MESSAGE_KEY: Any = ...  # From async_producer_pool
MAX_PENDING_TASKS: Any = ...  # From async_producer_pool
NUM_CONCURRENT_BATCHES: Any = ...  # From async_producer_pool
PIPELINE_BATCH_SIZE: Any = ...  # From async_producer_pool
REDIS_MAX_CONNECTIONS: Any = ...  # From async_producer_pool
SAVE_OVERLAYS_WITH_SHM: Any = ...  # From async_producer_pool
STREAM_MAXLEN: Any = ...  # From async_producer_pool
USE_SHM: Any = ...  # From async_producer_pool
KEY_CAMERA_ID: Any = ...  # From consumer_manager
KEY_CAM_ID: Any = ...  # From consumer_manager
KEY_CONTENT: Any = ...  # From consumer_manager
KEY_FORMAT: Any = ...  # From consumer_manager
KEY_FRAME_ID: Any = ...  # From consumer_manager
KEY_FRAME_IDX: Any = ...  # From consumer_manager
KEY_HEIGHT: Any = ...  # From consumer_manager
KEY_INPUT_STREAM_CONTENT: Any = ...  # From consumer_manager
KEY_IS_SIMILAR: Any = ...  # From consumer_manager
KEY_REFERENCE_FRAME_IDX: Any = ...  # From consumer_manager
KEY_SHM_MODE: Any = ...  # From consumer_manager
KEY_SHM_NAME: Any = ...  # From consumer_manager
KEY_TS_NS: Any = ...  # From consumer_manager
KEY_WIDTH: Any = ...  # From consumer_manager
USE_SHM: Any = ...  # From consumer_manager
logger: Any = ...  # From inference_metric_logger
ADAPTIVE_THRESHOLD_HIGH: Any = ...  # From inference_worker
ADAPTIVE_THRESHOLD_LOW: Any = ...  # From inference_worker
ASYNC_BUFFER_SIZE: Any = ...  # From inference_worker
BATCH_SIZE: Any = ...  # From inference_worker
BATCH_TIMEOUT_MS: Any = ...  # From inference_worker
ENABLE_ADAPTIVE_BATCH: Any = ...  # From inference_worker
ENABLE_DROP_ON_BACKPRESSURE: Any = ...  # From inference_worker
FEEDER_POLL_TIMEOUT: Any = ...  # From inference_worker
FRAME_STALENESS_MS: Any = ...  # From inference_worker
INFERENCE_TIMEOUT_SECONDS: Any = ...  # From inference_worker
MAX_ADAPTIVE_BATCH: Any = ...  # From inference_worker
MAX_CONCURRENT_SYNC_BATCHES: Any = ...  # From inference_worker
MAX_INFLIGHT_BATCHES: Any = ...  # From inference_worker
MIN_ADAPTIVE_BATCH: Any = ...  # From inference_worker
MIN_BATCH_SIZE: Any = ...  # From inference_worker
SYNC_MODE_THREAD_POOL_SIZE: Any = ...  # From inference_worker
logger: Any = ...  # From metric_publisher
ASYNC_BUFFER_SIZE: Any = ...  # From post_processing_manager
FEEDER_POLL_TIMEOUT: Any = ...  # From post_processing_manager
MAX_CONCURRENT_TASKS: Any = ...  # From post_processing_manager
KEY_CAMERA_ID: Any = ...  # From producer_worker
KEY_DATA: Any = ...  # From producer_worker
KEY_FRAME_ID: Any = ...  # From producer_worker
KEY_INPUT_STREAM: Any = ...  # From producer_worker
KEY_MESSAGE_KEY: Any = ...  # From producer_worker
MAX_CONCURRENT_SENDS: Any = ...  # From producer_worker
PIPELINE_BATCH_SIZE: Any = ...  # From producer_worker
SAVE_OVERLAYS_WITH_SHM: Any = ...  # From producer_worker
STREAM_MAXLEN: Any = ...  # From producer_worker
USE_SHM: Any = ...  # From producer_worker

# Functions
# From inference_metric_logger
def get_gpu_name() -> Optional[str]: ...
    """
    Get GPU name dynamically using nvidia-smi.
    
    This function is cached using lru_cache - the GPU detection only runs once
    and subsequent calls return the cached result. This is appropriate because
    GPU hardware doesn't change during runtime.
    
    Handles multiple edge cases:
    - Multiple GPUs: Returns the first GPU name
    - All GPUs same type: Returns just the name (no index)
    - Jetson devices: Attempts tegrastats fallback if nvidia-smi unavailable
    - No GPU / nvidia-smi not available: Returns None
    
    Returns:
        GPU name string or None if unable to detect
    
    Examples:
        "NVIDIA GeForce RTX 4090"
        "NVIDIA A100-SXM4-80GB"
        "NVIDIA Tegra X1" (Jetson)
        None (no GPU or error)
    
    Cache:
        Use get_gpu_name.cache_clear() to reset cache if needed (e.g., testing)
    """

# From inference_worker
def inference_worker_process(worker_id: int, num_workers: int, input_queue, output_queues: List[mp.Queue], model_config: Dict[str, Any], use_async_inference: bool = True, metrics_queue: Optional[mp.Queue] = None) -> Any: ...
    """
    Worker process for GPU inference with optimized queue handling.
    
    IMPORTANT: Each worker reads from its OWN dedicated queue (input_queue).
    Consumer routes frames based on hash(camera_id) % num_workers.
    This ensures strict ordering per camera.
    
    Processing modes:
    - ASYNC mode (use_async_inference=True):
      - Feeder thread drains mp.Queue → asyncio.Queue (no executor hops)
      - Batch inference without per-batch semaphore (true concurrency)
    - SYNC mode (use_async_inference=False):
      - Simple blocking loop with TRUE BATCH INFERENCE
      - NO asyncio overhead for CPU-bound models
    
    Each process:
    1. Recreates InferenceInterface with ModelManagerWrapper + ModelManager
    2. Starts feeder thread (ASYNC mode) or blocking loop (SYNC mode)
    3. Processes tasks from its dedicated queue (no re-queuing needed)
    4. Routes results to correct post-processing worker queue
    
    Args:
        worker_id: Worker process ID
        num_workers: Total number of worker processes
        input_queue: This worker's dedicated queue (routed by consumer)
        output_queues: List of post-processing worker queues (for routing by camera hash)
        model_config: Model configuration (action_id, predict functions, model_path, etc.)
        use_async_inference: True for async batching, False for blocking thread pool
        metrics_queue: Queue for sending metrics back to main process
    """

# From post_processing_manager
def postprocessing_worker_process(worker_id: int, num_workers: int, input_queue, output_queue, post_processor_config: Dict[str, Any], metrics_queue: Optional[mp.Queue] = None) -> Any: ...
    """
    Worker process for post-processing with async concurrent processing.
    
    ASYNC CONCURRENT ARCHITECTURE (v4):
    - Feeder thread drains mp.Queue → asyncio.Queue (no blocking in event loop)
    - Semaphore-bounded concurrent tasks (up to MAX_CONCURRENT_TASKS)
    - I/O overlap when PostProcessor.process() has external calls
    - Per-camera ordering preserved (same camera → same worker)
    
    IMPORTANT: Each worker reads from its OWN dedicated queue (input_queue).
    Inference workers route frames based on hash(camera_id) % num_workers.
    This ensures strict ordering per camera and isolated tracker states.
    
    Each process:
    1. Initializes PostProcessor with config
    2. Starts feeder thread (mp.Queue → asyncio.Queue)
    3. Runs async event loop with concurrent task processing
    4. Maintains isolated tracker states for assigned cameras
    5. Outputs results to dedicated output queue
    
    Args:
        worker_id: Worker process ID
        num_workers: Total number of worker processes
        input_queue: This worker's dedicated queue (routed by inference workers)
        output_queue: This worker's dedicated output queue
        post_processor_config: Configuration for PostProcessor initialization
        metrics_queue: Queue for sending metrics back to main process
    """

# Classes
# From analytics_publisher
class AnalyticsPublisher:
    """
    Publishes aggregated analytics to Redis (localhost) and Kafka internal streams.
    
    Monitors output queue and aggregates tracking statistics over 5-minute windows.
    Publishes to 'results-agg' topic on both Redis and Kafka.
    
    Output structure:
        tracking_stats: {
            "current_counts": [{"category": "person", "count": 2}],         # NEW people in this publish window (delta)
            "total_current_counts": [{"category": "person", "count": 7}],   # ALL people in frame right now
            "total_counts": [{"category": "person", "count": 15}]           # Cumulative unique since reset
        }
    """

    def __init__(self, camera_configs: Dict[str, Any], aggregation_interval: int = DEFAULT_AGGREGATION_INTERVAL, publish_interval: int = DEFAULT_PUBLISH_INTERVAL, app_deployment_id: Optional[str] = None, inference_pipeline_id: Optional[str] = None, deployment_instance_id: Optional[str] = None, app_id: Optional[str] = None, app_name: Optional[str] = None, app_version: Optional[str] = None, redis_host: str = 'localhost', redis_port: int = 6379, redis_password: Optional[str] = None, redis_username: Optional[str] = None, redis_db: int = 0, kafka_bootstrap_servers: Optional[str] = None, enable_kafka: bool = False) -> None: ...

    ANALYTICS_TOPIC: Any
    DEFAULT_AGGREGATION_INTERVAL: Any
    DEFAULT_PUBLISH_INTERVAL: Any

    def enqueue_analytics_data(self, task_data: Dict[str, Any]) -> None: ...
        """
        Enqueue analytics data from producer for processing.
        Called by ProducerWorker after sending messages.
        
        Args:
            task_data: Task data from output queue containing analytics info
        """

    def get_metrics(self) -> Dict[str, Any]: ...
        """
        Get analytics publisher metrics.
        """

    def start(self) -> Any: ...
        """
        Start the analytics publisher in a separate thread.
        """

    def stop(self) -> Any: ...
        """
        Stop the analytics publisher.
        """


# From app_deployment
class AppDeployment:
    """
    Handles app deployment configuration and camera setup for streaming pipeline.
    """

    def __init__(self, session: Session, app_deployment_id: str, deployment_instance_id: Optional[str] = None, connection_timeout: int = 1200, action_id: Optional[str] = None) -> None: ...

    def close_heartbeat_producer(self) -> Any: ...
        """
        Close Kafka heartbeat producer.
        """

    def get_and_wait_for_connection_info(self, server_type: str, server_id: str) -> Optional[Dict]: ...
        """
        Get the connection information for the streaming gateway.
        """

    def get_camera_configs(self) -> Dict[str, CameraConfig]: ...
        """
        Get camera configurations for the streaming pipeline.
        
        Returns:
            Dict[str, CameraConfig]: Dictionary mapping camera_id to CameraConfig
        """

    def get_input_topics(self) -> List[Dict]: ...
        """
        Get input topics for the app deployment.
        """

    def get_output_topics(self) -> List[Dict]: ...
        """
        Get output topics for the app deployment.
        """

    def get_single_camera_config(self, camera_id: str) -> Optional[CameraConfig]: ...
        """
        Get configuration for a single camera by ID.
        
        This is more efficient than fetching all cameras when we only need one.
        
        Args:
            camera_id: ID of camera to fetch
        
        Returns:
            CameraConfig if found and valid, None otherwise
        """

    def initialize_event_listener(self, streaming_pipeline = None, event_loop = None) -> bool: ...
        """
        Initialize and start the app event listener.
        
                Args:
                    streaming_pipeline: Reference to the StreamingPipeline instance for dynamic updates
                    event_loop: Event loop for scheduling async tasks (optional, will try to get running loop)
        
                Returns:
                    bool: True if successfully initialized and started
        """

    def initialize_refresh_listener(self, streaming_pipeline = None, event_loop = None, camera_config_monitor = None) -> bool: ...
        """
        Initialize and start the deployment refresh listener.
        
                Args:
                    streaming_pipeline: Reference to the StreamingPipeline instance
                    event_loop: Event loop for scheduling async tasks
                    camera_config_monitor: Reference to CameraConfigMonitor for notifications
        
                Returns:
                    bool: True if successfully initialized and started
        """

    async def load_cameras_incrementally(self, streaming_pipeline = None, event_loop = None, max_parallel_workers: int = 10) -> Dict[str, Any]: ...
        """
        Load cameras incrementally and in parallel, adding each to the pipeline as soon as it's ready.
        
        This method:
        1. Fetches input/output topics
        2. Processes cameras in parallel (up to max_parallel_workers at a time)
        3. Adds each camera to the pipeline as soon as its config is ready
        4. Doesn't wait for all cameras - returns immediately after starting the process
        
        Args:
            streaming_pipeline: Reference to StreamingPipeline to add cameras to
            event_loop: Event loop for async operations
            max_parallel_workers: Maximum number of cameras to process in parallel
        
        Returns:
            Dict with summary: {"total_cameras": int, "started_loading": int}
        """

    def send_heartbeat(self, camera_configs: Dict[str, CameraConfig]) -> bool: ...
        """
        Send heartbeat to Kafka topic with current camera configurations.
        
        Args:
            camera_configs: Dictionary of camera_id -> CameraConfig
        
        Returns:
            True if successful, False otherwise
        """

    def stop_event_listener(self) -> Any: ...
        """
        Stop the app event listener and close heartbeat producer.
        """

    def stop_refresh_listener(self) -> Any: ...
        """
        Stop the deployment refresh listener.
        """


# From app_event_listener
class AppEventListener:
    """
    Listener for app deployment add/delete events from Kafka.
    
        This class wraps the generic EventListener from matrice_common
        and provides app-specific event handling logic for input/output topics.
    
        Events handled:
        - add: New input/output topic created for a camera
        - delete: Input/output topic removed for a camera
    """

    def __init__(self, session: Session, app_deployment_id: str, on_topic_added, on_topic_deleted) -> None: ...
        """
        Initialize app event listener.
        
                Args:
                    session: Session object for authentication
                    app_deployment_id: ID of app deployment to filter events
                    on_topic_added: Callback when a topic is added
                    on_topic_deleted: Callback when a topic is deleted
        """

    def get_statistics(self) -> dict: ...
        """
        Get statistics.
        """

    def handle_event(self, event: Dict[str, Any]) -> Any: ...
        """
        Handle app deployment event.
        
                Args:
                    event: App event dict with structure:
                        {
                            "eventType": "add" | "delete",
                            "appDeploymentId": "...",
                            "topicType": "input" | "output",
                            "timestamp": "...",
                            "data": {
                                "id": "...",
                                "cameraId": "...",
                                "topicName": "...",
                                "topicType": "input" | "output",
                                "serverId": "...",
                                "serverType": "redis" | "kafka",
                                ...
                            }
                        }
        """

    def is_listening(self) -> bool: ...
        """
        Check if listener is active.
        """

    def start(self) -> bool: ...
        """
        Start listening to app events.
        
                Returns:
                    bool: True if started successfully
        """

    def stop(self) -> Any: ...
        """
        Stop listening.
        """


# From async_producer_pool
class AsyncProducerPool:
    """
    Shared async producer pool for high-throughput Redis publishing.
    
    Replaces the thread-per-producer model with a single shared async pool.
    Uses one event loop and a shared Redis connection pool for all output queues.
    
    Architecture:
    - Single dedicated thread running asyncio event loop
    - Shared aioredis connection pool (configurable max connections)
    - Concurrent polling of all output queues using asyncio.gather
    - Batched Redis pipelining (64 messages per round-trip)
    - Bounded concurrency for batch processing (prevents unbounded task explosion)
    
    Thread Safety:
    - All state is accessed only from the event loop thread
    - Queue polling uses run_in_executor for blocking mp.Queue operations
    - Stop signal via threading.Event for clean shutdown
    """

    def __init__(self, output_queues: List[mp.Queue], camera_configs: Dict[str, CameraConfig], stream_config: Dict[str, Any], analytics_publisher: Optional[Any] = None, frame_cache: Optional[Any] = None, app_deployment_id: Optional[str] = None, num_concurrent_batches: int = NUM_CONCURRENT_BATCHES, batch_size: int = PIPELINE_BATCH_SIZE, use_shared_metrics: bool = True) -> None: ...
        """
        Initialize async producer pool.
        
        Args:
            output_queues: List of mp.Queues from post-processing workers
            camera_configs: Camera configurations for stream routing
            stream_config: Redis/stream configuration
            analytics_publisher: Optional analytics publisher
            frame_cache: Optional frame cache for Redis storage
            app_deployment_id: App deployment ID for overlay keys
            num_concurrent_batches: Max concurrent batch operations
            batch_size: Target batch size for Redis pipelining
            use_shared_metrics: Whether to use shared metrics instance
        """

    DEFAULT_DB: Any

    def get_metrics(self) -> Dict[str, Any]: ...
        """
        Get producer pool metrics.
        
                Returns:
                    Dict with metrics summary
        """

    def replace_queue(self, queue_idx: int, new_queue) -> bool: ...
        """
        Replace a stuck queue with a new one.
        
                Called by post-processing pool when it restarts a worker.
                This allows recovery from multiprocessing.Queue pipe deadlock states.
        
                Args:
                    queue_idx: Index of the queue to replace
                    new_queue: New queue instance to use
        
                Returns:
                    True if replacement successful, False otherwise
        """

    def set_queue_stuck_callback(self, callback) -> None: ...
        """
        Set callback to be invoked when a queue is detected as stuck.
        
                The callback receives the queue index as its argument.
                This can be used to trigger worker restart when queue pipe deadlock is detected.
        
                Args:
                    callback: Function that takes queue_idx (int) as argument
        """

    def start(self) -> Any: ...
        """
        Start the async producer pool in a dedicated thread.
        
                Returns:
                    Thread running the event loop
        """

    def stop(self) -> None: ...
        """
        Stop the async producer pool gracefully.
        """

    def update_analytics_publisher(self, analytics_publisher) -> None: ...
        """
        Update analytics publisher reference (for lazy initialization).
        
                Args:
                    analytics_publisher: New analytics publisher instance
        """

    def update_camera_configs(self, camera_configs: Dict[str, CameraConfig]) -> None: ...
        """
        Update camera configurations.
        
                Args:
                    camera_configs: New camera configurations
        """

    def update_frame_cache(self, frame_cache) -> None: ...
        """
        Update frame cache reference (for lazy initialization).
        
                Args:
                    frame_cache: New frame cache instance
        """

    def update_stream_config(self, stream_config: Dict[str, Any]) -> bool: ...
        """
        Update stream configuration and reinitialize Redis connection.
        
                This method is thread-safe and can be called from any thread.
                It schedules the Redis reinitialization on the event loop.
        
                Used for lazy initialization when cameras are added after startup
                and provide proper Redis auth credentials.
        
                Args:
                    stream_config: New stream configuration with Redis connection details
        
                Returns:
                    True if update was scheduled successfully, False otherwise
        """


# From camera_config_monitor
class CameraConfigMonitor:
    """
    Monitors and syncs camera configurations from app deployment API.
    """

    def __init__(self, app_deployment, streaming_pipeline, check_interval: int = DEFAULT_CHECK_INTERVAL, heartbeat_interval: int = DEFAULT_HEARTBEAT_INTERVAL) -> None: ...
        """
        Initialize the camera config monitor.
        
                Args:
                    app_deployment: AppDeployment instance to fetch configs
                    streaming_pipeline: StreamingPipeline instance to update
                    check_interval: Seconds between config checks
                    heartbeat_interval: Seconds between heartbeat sends
        """

    DEFAULT_CHECK_INTERVAL: Any
    DEFAULT_HEARTBEAT_INTERVAL: Any
    MAX_RETRY_ATTEMPTS: Any

    def notify_refresh_completed(self, new_camera_configs: Dict[str, CameraConfig], old_camera_configs: Dict[str, CameraConfig]) -> None: ...
        """
        Notify monitor that a refresh event has completed successfully.
        
                Updates the internal hash cache and resets retry counts to prevent
                immediate re-syncing after refresh event handling. Makes refresh the
                PRIMARY source of truth.
        
                ALL cameras affected by the refresh event are marked as refresh-managed:
                - Cameras in the refresh event (added/updated)
                - Cameras that were in the OLD pipeline but NOT in refresh event (removed)
        
                Once a camera is managed by ANY refresh event, it can ONLY be modified by
                subsequent refresh events (never by app events or monitor polling).
        
                Args:
                    new_camera_configs: Dictionary of camera_id -> CameraConfig from refresh event (NEW state)
                    old_camera_configs: Dictionary of camera_id -> CameraConfig from pipeline before reconciliation (OLD state)
        """

    def start(self) -> None: ...
        """
        Start the background monitoring thread.
        """

    def stop(self) -> None: ...
        """
        Stop the background monitoring thread.
        """


# From consumer_manager
class AsyncConsumerManager:
    """
    Manages 1000 camera streams with single async event loop.
    
    HIGH-PERFORMANCE ARCHITECTURE (optimized.py pattern):
    - Direct redis.asyncio client (no MatriceStream abstraction)
    - Single XREAD call for ALL streams (not per-stream XREADGROUP)
    - Pre-encoded byte keys for field access
    - At-most-once delivery (drop under backpressure, no ACK)
    - asyncio.Queue with put_nowait() (no feeder threads)
    - Lightweight FrameTask tuples instead of Dict[str, Any]
    
    Key Features:
    - Single event loop for all cameras (not 1000 threads)
    - Non-blocking async stream reads
    - Backpressure handling (drop frames if queue full)
    - Dynamic camera add/remove support
    """

    def __init__(self, camera_configs: Dict[str, CameraConfig], stream_config: Dict[str, Any], app_deployment_id: str, pipeline, message_timeout: float = 0.5, use_shm: bool = USE_SHM, enable_flow_control: bool = False, max_in_flight_frames: int = 8000, enable_drop_on_backpressure: bool = True) -> None: ...

    BACKPRESSURE_THRESHOLD: Any
    BATCH_SIZE: Any
    BLOCK_MS: Any
    CIRCUIT_BREAKER_FAILURE_THRESHOLD: Any
    CIRCUIT_BREAKER_MAX_BACKOFF: Any
    CIRCUIT_BREAKER_MIN_BACKOFF: Any
    CIRCUIT_BREAKER_RESET_TIMEOUT: Any
    FRAME_STALENESS_NS: Any
    METRICS_AGGREGATION_COUNT: Any
    QUEUE_MAX: Any

    async def add_camera(self, camera_id: str, config) -> Any: ...
        """
        Add a new camera dynamically.
        
        The camera's stream will be added to the single XREAD on the next iteration.
        
        Args:
            camera_id: Unique camera identifier
            config: Camera configuration
        """

    def get_task_queue(self) -> Optional[asyncio.Queue]: ...
        """
        Get the task queue for inference workers to consume from.
        
                Returns:
                    asyncio.Queue containing FrameTask tuples
        """

    async def remove_camera(self, camera_id: str) -> Any: ...
        """
        Remove a camera dynamically.
        
        The camera's stream will be removed from the XREAD on the next iteration.
        
        Args:
            camera_id: Unique camera identifier
        """

    async def start(self) -> Any: ...
        """
        Start optimized consumer using single XREAD for all streams.
        
                HIGH-PERFORMANCE ARCHITECTURE:
                - Single redis.asyncio connection for ALL streams
                - Single XREAD call reads from ALL streams at once
                - asyncio.Queue for direct message passing (no feeder threads)
                - At-most-once delivery (drop under backpressure, no ACK)
        """

    async def stop(self) -> Any: ...
        """
        Stop consumer and clean up resources.
        """


# From consumer_manager
class FrameTask(NamedTuple):
    """
    Lightweight frame task for minimal overhead message passing.
    
        Using NamedTuple instead of Dict[str, Any] reduces:
        - Memory allocation (no dict overhead)
        - Attribute access time (direct vs hash lookup)
        - Serialization cost (fixed structure)
    
        Supports both SHM mode (shm_name/frame_idx) and legacy mode (frame_bytes).
    """

    pass

# From deployment_refresh_listener
class DeploymentRefreshListener:
    """
    Listener for deployment instance refresh events from Kafka.
    
        This class wraps the generic EventListener from matrice_common
        and provides deployment-specific event handling logic for full
        configuration refreshes.
    
        Events handled:
        - refresh: Complete snapshot of all streaming topics for this deployment
    
        The refresh event is the PRIMARY source of truth and triggers full
        reconciliation of camera configurations.
    """

    def __init__(self, session: Session, deployment_instance_id: str, on_refresh) -> None: ...
        """
        Initialize deployment refresh listener.
        
                Args:
                    session: Session object for authentication
                    deployment_instance_id: ID of deployment instance
                    on_refresh: Callback when a refresh event is received
        """

    def get_statistics(self) -> dict: ...
        """
        Get refresh listener statistics.
        
                Returns:
                    dict: Statistics including refresh counts and listener stats
        """

    def handle_event(self, event: Dict[str, Any]) -> Any: ...
        """
        Handle deployment refresh event.
        
                Args:
                    event: Refresh event dict with structure:
                        {
                            "eventType": "refresh",
                            "streamingGatewayId": "...",  # NOTE: Key name is wrong, this is actually deployInstanceId
                            "timestamp": "2025-01-14T10:30:00Z",
                            "data": [
                                {
                                    "id": "...",
                                    "accountNumber": "...",
                                    "cameraId": "...",
                                    "streamingGatewayId": "...",
                                    "serverId": "...",
                                    "serverType": "redis" | "kafka",
                                    "appDeploymentId": "...",
                                    "topicName": "...",
                                    "topicType": "input" | "output",
                                    "ipAddress": "...",
                                    "port": 123,
                                    "consumingAppsDeploymentIds": [...],
                                    "cameraFPS": 30,
                                    "deployInstanceId": "..."
                                },
                                ...
                            ]
                        }
        
                        NOTE: Backend sends "streamingGatewayId" but the value is actually
                        the deployment instance ID. The key name is incorrect in the backend.
        """

    def is_listening(self) -> bool: ...
        """
        Check if listener is active.
        """

    def start(self) -> bool: ...
        """
        Start listening to refresh events.
        
                Returns:
                    bool: True if started successfully
        """

    def stop(self) -> Any: ...
        """
        Stop listening.
        """


# From frame_cache
class RedisFrameCache:
    """
    Async Redis cache for frames with high-throughput design.
    
        Uses redis.asyncio for non-blocking Redis operations, eliminating the need
        for worker threads. All operations are async and return immediately.
    
        Stores base64 string content under key 'stream:frames:{frame_id}' with field 'frame'.
        Each insert sets or refreshes the TTL.
    
        IMPORTANT: This class supports multiple event loops by maintaining per-loop
        Redis clients and semaphores. This is critical because:
        - Producer worker runs in its own event loop (in a separate thread)
        - Analytics publisher runs in its own event loop (in a separate thread)
        - Main pipeline may have its own event loop
        Each event loop needs its own Redis client because redis.asyncio clients
        use internal asyncio locks that are bound to the event loop where they were created.
    """

    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0, password: Optional[str] = None, username: Optional[str] = None, ttl_seconds: int = DEFAULT_TTL_SECONDS, prefix: str = DEFAULT_PREFIX, max_queue: int = 10000, worker_threads: int = 16, connect_timeout: float = DEFAULT_CONNECT_TIMEOUT, socket_timeout: float = DEFAULT_SOCKET_TIMEOUT, max_connections: int = DEFAULT_MAX_CONNECTIONS, shm_mode: bool = False) -> None: ...

    DEFAULT_CONNECT_TIMEOUT: Any
    DEFAULT_MAX_CONNECTIONS: Any
    DEFAULT_PREFIX: Any
    DEFAULT_SOCKET_TIMEOUT: Any
    DEFAULT_TTL_SECONDS: Any

    def close_all_clients(self) -> None: ...
        """
        Close all Redis clients synchronously (for shutdown).
        
                This is a best-effort cleanup when we can't use async.
                The connections will eventually be garbage collected anyway.
        """

    async def close_async(self) -> None: ...
        """
        Close async Redis client for the CURRENT event loop.
        
                This should be called from each event loop that used the cache
                before the loop is closed.
        """

    def get_metrics(self) -> Dict[str, Any]: ...
        """
        Get cache performance metrics for monitoring.
        """

    def put(self, frame_id: str, binary_content) -> None: ...
        """
        Queue a frame for async caching (fire-and-forget).
        
                This method is synchronous but creates an async task for the actual
                Redis operation. The task runs in the background without blocking.
        
                Args:
                    frame_id: unique identifier for the frame
                    binary_content: raw image bytes (JPEG/PNG/etc)
        """

    def put_overlay(self, frame_id: str, camera_id: str, app_deployment_id: str, overlay_data, ttl_seconds: Optional[int] = None) -> bool: ...
        """
        Queue overlay data for async storage (fire-and-forget).
        
                Key format: overlay:{frame_id}_{camera_id}_{app_deployment_id}
        
                Args:
                    frame_id: Unique frame identifier
                    camera_id: Camera identifier
                    app_deployment_id: App deployment identifier
                    overlay_data: Serialized overlay/results data (JSON bytes)
                    ttl_seconds: Optional TTL override
        
                Returns:
                    bool: True if task was scheduled, False otherwise
        """

    def start(self) -> None: ...
        """
        Start the frame cache (marks as running, lazy client init).
        """

    def stop(self) -> None: ...
        """
        Stop the frame cache and cleanup resources.
        """


# From inference_metric_logger
class InferenceMetricLogger:
    """
    Background aggregator for worker metrics with periodic publishing.
    
    This class:
    - Runs on a dedicated background thread using threading.Timer
    - Periodically collects metrics from all workers via StreamingPipeline
    - Aggregates by worker_type (merges multiple instances)
    - Produces InferenceMetricLog matching the required schema
    - Publishes via configurable MetricPublisher
    - Handles graceful shutdown with timeout
    
    Thread Safety:
        - Timer-based execution ensures single aggregator thread
        - Worker metrics use internal locks for snapshot operations
        - No shared mutable state between collection cycles
    
    Lifecycle:
        logger = InferenceMetricLogger(pipeline, ...)
        logger.start()
        # ... runs in background ...
        logger.stop(timeout=10)
    """

    def __init__(self, streaming_pipeline, interval_seconds: float = 60.0, publisher: Optional[MetricPublisher] = None, deployment_id: Optional[str] = None, deployment_instance_id: Optional[str] = None, app_deploy_id: Optional[str] = None, action_id: Optional[str] = None, app_id: Optional[str] = None, log_metrics_every_n: int = 5, multiprocess_metrics_queue: Optional[mp.Queue] = None) -> None: ...
        """
        Initialize metric logger.
        
        Args:
            streaming_pipeline: Reference to StreamingPipeline instance
            interval_seconds: Reporting interval (INFERENCE_METRIC_LOGGING_INTERVAL)
            publisher: MetricPublisher implementation (defaults to Kafka)
            deployment_id: Deployment identifier for metric log
            deployment_instance_id: Deployment instance identifier for metric log
            app_deploy_id: App deployment identifier
            action_id: Action identifier
            app_id: Application identifier
            log_metrics_every_n: Log detailed metrics every N collections (0 = never)
            multiprocess_metrics_queue: Shared queue for receiving metrics from worker processes
        """

    def get_stats(self) -> Dict[str, Any]: ...
        """
        Get logger statistics.
        
        Returns:
            Dictionary with collection statistics
        """

    def start(self) -> None: ...
        """
        Start the background metric collection loop.
        
        Spawns a timer-based thread that wakes every interval_seconds
        to collect and publish metrics.
        
        Thread Safety:
            Uses lock to prevent multiple start calls from creating
            duplicate timer threads.
        """

    def stop(self, timeout: float = 10.0) -> None: ...
        """
        Stop the background metric collection loop.
        
        Args:
            timeout: Maximum time to wait for final collection (seconds)
        
        Note:
            Performs one final collection before stopping to avoid
            losing metrics from the last interval.
        """

    def wait(self, timeout: Optional[float] = None) -> None: ...
        """
        Wait for the metric logger to stop.
        
        Args:
            timeout: Maximum time to wait (None = wait indefinitely)
        
        Note:
            This is a passive wait - use stop() to actually stop the logger.
        """


# From inference_worker
class MultiprocessInferencePool:
    """
    Pool of multiprocessing inference workers with per-worker queues.
    
    Architecture:
    - Creates multiple worker processes (one per GPU/core)
    - Each worker has its OWN dedicated input queue (routed by consumer)
    - Each process recreates InferenceInterface → ModelManagerWrapper → ModelManager
    - Uses normal ModelManager with async_predict from predict.py (NOT Triton)
    - Each process runs its own async event loop
    - Routes results to correct post-processing worker queue
    - 100% order preservation per camera (no re-queuing)
    - Metrics sent back to main process via metrics_queue for aggregation
    
    Processing Modes:
    - ASYNC (use_async_inference=True): Up to 16 concurrent requests per worker
    - SYNC (use_async_inference=False): TRUE BATCH INFERENCE via sync_batch_inference
    """

    def __init__(self, num_workers: int, model_config: Dict[str, Any], input_queues: List[mp.Queue], output_queues: List[mp.Queue], use_async_inference: bool = True, metrics_queue: Optional[mp.Queue] = None) -> None: ...

    def get_result(self, timeout: float = 0.001) -> Optional[Dict[str, Any]]: ...
        """
        Get inference result from worker pool.
        
        Args:
            timeout: Max time to wait for result
        
        Returns:
            Result dict or None if no result available
        """

    def start(self) -> Any: ...
        """
        Start all worker processes with dedicated queues.
        """

    def stop(self) -> Any: ...
        """
        Stop all worker processes.
        """

    def submit_task(self, task_data: Dict[str, Any], timeout: float = 0.1) -> bool: ...
        """
        Submit inference task to worker pool.
        
        Args:
            task_data: Task data with camera_id, frame, etc.
            timeout: Max time to wait if queue is full
        
        Returns:
            True if task was submitted, False if queue full (backpressure)
        """


# From metric_publisher
class KafkaMetricPublisher(MetricPublisher):
    """
    Kafka-based metric publisher using confluent-kafka.
    
    Follows the same pattern as error logging producer for consistency.
    Lazy-loads Kafka dependencies and fetches config via RPC.
    
    Thread Safety:
        Producer.produce() is thread-safe per confluent-kafka documentation.
    """

    def __init__(self, rpc_client: Optional[Any] = None, access_key: Optional[str] = None, secret_key: Optional[str] = None) -> None: ...
        """
        Initialize Kafka publisher.
        
        Args:
            rpc_client: Optional RPC client for fetching Kafka config
            access_key: Matrice access key (falls back to env var)
            secret_key: Matrice secret key (falls back to env var)
        
        Raises:
            ImportError: If confluent-kafka not available
            ValueError: If credentials missing or Kafka config fetch fails
        """

    TOPIC_NAME: Any

    def close(self) -> None: ...
        """
        Flush and close Kafka producer.
        """

    def publish(self, metric_log: Dict[str, Any]) -> bool: ...
        """
        Publish metric log to Kafka.
        
        Args:
            metric_log: InferenceMetricLog dictionary
        
        Returns:
            True if publish succeeded, False otherwise
        """


# From metric_publisher
class MetricPublisher(ABC):
    """
    Abstract interface for metric publishing.
    
    Implementations must be thread-safe as they may be called from
    the background aggregator thread.
    """

    def close(self) -> None: ...
        """
        Clean up publisher resources.
        
        Called during InferenceMetricLogger shutdown.
        """

    def publish(self, metric_log: Dict[str, Any]) -> bool: ...
        """
        Publish a metric log.
        
        Args:
            metric_log: InferenceMetricLog dictionary matching schema
        
        Returns:
            True if publish succeeded, False otherwise
        
        Note:
            Implementations should catch and log exceptions internally
            to avoid breaking the aggregator loop.
        """


# From metric_publisher
class NoOpMetricPublisher(MetricPublisher):
    """
    No-op publisher for testing or when Kafka is unavailable.
    
    Logs metrics to DEBUG level instead of publishing.
    """

    def close(self) -> None: ...
        """
        Nothing to clean up.
        """

    def publish(self, metric_log: Dict[str, Any]) -> bool: ...
        """
        Log metric instead of publishing.
        """


# From post_processing_manager
class MultiprocessPostProcessingPool:
    """
    Pool of multiprocessing post-processing workers with per-worker queues.
    
    Architecture:
    - Creates multiple worker processes (4 workers for CPU-bound tasks)
    - Each worker has its OWN dedicated input queue (routed by inference workers)
    - Each worker writes to its OWN dedicated output queue (eliminates lock contention)
    - Each process maintains isolated tracker states for assigned cameras
    - 100% order preservation per camera (no re-queuing)
    - Processes communicate via multiprocessing queues
    - True parallelism (bypasses Python GIL)
    - Metrics sent back to main process via metrics_queue for aggregation
    """

    def __init__(self, pipeline, post_processor_config: Dict[str, Any], input_queues: List[mp.Queue], output_queues: List[mp.Queue], num_processes: int = 4, metrics_queue: Optional[mp.Queue] = None) -> None: ...
        """
        Initialize post-processing pool with per-worker queues.
        
        Args:
            pipeline: Reference to StreamingPipeline (not used in workers, for compatibility)
            post_processor_config: Configuration for PostProcessor initialization
            input_queues: List of mp.Queues (one per worker, routed by inference workers)
            output_queues: List of mp.Queues (one per worker, eliminates lock contention)
            num_processes: Number of worker processes
            metrics_queue: Queue for sending metrics back to main process
        """

    def get_result(self, timeout: float = 0.001) -> Optional[Dict[str, Any]]: ...
        """
        Get result from any worker output queue (round-robin polling).
        
        Args:
            timeout: Max time to wait for result
        
        Returns:
            Result dict or None if no result available
        """

    def start(self) -> Any: ...
        """
        Start all worker processes with dedicated input and output queues.
        """

    def stop(self) -> Any: ...
        """
        Stop all worker processes.
        """

    def submit_task(self, task_data: Dict[str, Any], timeout: float = 0.1) -> bool: ...
        """
        Submit task to worker queue based on camera_id hash routing.
        
        Camera-based routing ensures:
        - Same camera always goes to same worker process
        - Tracker state remains isolated within that process
        - Per-camera ordering is preserved
        
        Args:
            task_data: Task data with camera_id, model_result, etc.
            timeout: Max time to wait if queue is full
        
        Returns:
            True if task was submitted, False if queue full (backpressure)
        """


# From producer_worker
class ProducerWorker:
    """
    Handles message production to streams with per-camera queue handling.
    
        Supports sharded output queues (one per post-processing worker) to eliminate
        lock contention. Uses round-robin polling to read from all queues efficiently.
    """

    def __init__(self, worker_id: int, output_queues: List[Any], pipeline, camera_configs: Dict[str, CameraConfig], message_timeout: float, analytics_publisher: Optional[Any] = None, frame_cache: Optional[Any] = None, use_shared_metrics: Optional[bool] = True, app_deployment_id: Optional[str] = None) -> None: ...

    DEFAULT_DB: Any

    def remove_camera_stream(self, camera_id: str) -> bool: ...
        """
        Remove producer stream for a specific camera (thread-safe).
        
                This method can be called from any thread. It schedules the stream
                cleanup on the ProducerWorker's event loop using run_coroutine_threadsafe.
        
                Args:
                    camera_id: ID of camera whose stream should be removed
        
                Returns:
                    bool: True if successfully removed, False otherwise
        """

    def start(self) -> Any: ...
        """
        Start the producer worker in a separate thread.
        """

    def stop(self) -> Any: ...
        """
        Stop the producer worker.
        """


# From stream_pipeline
class StreamingPipeline:
    """
    Optimized streaming pipeline with dynamic camera configuration and clean resource management.
    """

    def __init__(self, inference_interface: Optional[InferenceInterface] = None, inference_queue_maxsize: int = DEFAULT_QUEUE_SIZE, postproc_queue_maxsize: int = DEFAULT_QUEUE_SIZE, output_queue_maxsize: int = DEFAULT_QUEUE_SIZE, message_timeout: float = DEFAULT_MESSAGE_TIMEOUT, inference_timeout: float = DEFAULT_INFERENCE_TIMEOUT, shutdown_timeout: float = DEFAULT_SHUTDOWN_TIMEOUT, camera_configs: Optional[Dict[str, CameraConfig]] = None, app_deployment_id: Optional[str] = None, inference_pipeline_id: Optional[str] = None, enable_analytics_publisher: bool = True, deployment_id: Optional[str] = None, deployment_instance_id: Optional[str] = None, action_id: Optional[str] = None, app_id: Optional[str] = None, app_name: Optional[str] = None, app_version: Optional[str] = None, use_shared_metrics: Optional[bool] = True, enable_metric_logging: bool = True, metric_logging_interval: float = DEFAULT_METRIC_INTERVAL, frame_cache_worker_threads: int = 20, frame_cache_max_queue: int = 50000, frame_cache_max_connections: int = 200, load_model: Optional[Any] = None, predict: Optional[Any] = None, async_predict: Optional[Any] = None, async_batch_predict: Optional[Any] = None, async_load_model: Optional[Any] = None, batch_predict: Optional[Any] = None, post_processing_config: Optional[Dict[str, Any]] = None, index_to_category: Optional[Any] = None, target_categories: Optional[Any] = None, enable_flow_control: bool = True, max_in_flight_frames: int = 256, enable_drop_on_backpressure: bool = True, drop_stale_frames: bool = True, frame_staleness_ms: float = 500.0, consumer_queue_max: int = 2000, consumer_batch_size: int = 500, result_cache_enabled: bool = True, result_cache_max_size: int = 50000, result_cache_ttl_seconds: int = 300, is_inference_API: bool = False) -> None: ...

    DEFAULT_INFERENCE_TIMEOUT: Any
    DEFAULT_MESSAGE_TIMEOUT: Any
    DEFAULT_METRIC_INTERVAL: Any
    DEFAULT_QUEUE_SIZE: Any
    DEFAULT_SHUTDOWN_TIMEOUT: Any

    async def add_camera_config(self, camera_config) -> bool: ...
        """
        Add a camera configuration dynamically while pipeline is running.
        
        Args:
            camera_config: Camera configuration to add
        
        Returns:
            bool: True if successfully added, False otherwise
        """

    def disable_camera(self, camera_id: str) -> bool: ...
        """
        Disable a camera configuration.
        """

    def enable_camera(self, camera_id: str) -> bool: ...
        """
        Enable a camera configuration.
        """

    def get_metrics(self) -> Dict[str, Any]: ...
        """
        Get pipeline metrics including frame cache statistics.
        """

    async def reconcile_camera_configs(self, new_camera_configs: Dict[str, CameraConfig]) -> Dict[str, Any]: ...
        """
        Perform full reconciliation of camera configurations.
        
        This method replaces the current camera configurations with the provided
        snapshot, performing adds, updates, and removals as needed.
        
        Args:
            new_camera_configs: Complete snapshot of camera configurations
        
        Returns:
            Dict with reconciliation results:
                {
                    "success": bool,
                    "added": int,
                    "updated": int,
                    "removed": int,
                    "total_cameras": int,
                    "errors": List[str]
                }
        """

    async def remove_camera_config(self, camera_id: str) -> bool: ...
        """
        Remove a camera configuration dynamically.
        
        Args:
            camera_id: ID of camera to remove
        
        Returns:
            bool: True if successfully removed, False otherwise
        """

    def start(self) -> None: ...
        """
        Start the pipeline with proper error handling.
        """

    def stop(self) -> None: ...
        """
        Stop the pipeline gracefully with proper cleanup.
        """

    async def update_camera_config(self, camera_config) -> bool: ...
        """
        Update an existing camera configuration.
        
        Args:
            camera_config: Updated camera configuration
        
        Returns:
            bool: True if successfully updated, False otherwise
        """


# From utils
class CameraConfig:
    """
    Configuration for a camera stream.
    """

    pass

# From utils
class StreamMessage:
    """
    Raw message from stream.
    """

    pass

# From worker_metrics
class MetricSnapshot:
    """
    Immutable snapshot of metrics for a time interval.
    """

    pass

# From worker_metrics
class MetricUpdate:
    """
    Lightweight metric update sent from worker process to main process.
    
    Used by multiprocessing workers to report their metrics without
    requiring shared memory. The main process aggregates these updates.
    """

    pass

# From worker_metrics
class MultiprocessMetricsCollector:
    """
    Collector for metrics from multiprocessing workers.
    
    This class runs in the MAIN PROCESS and aggregates MetricUpdate messages
    sent from worker processes via a shared multiprocessing.Queue.
    
    Architecture:
        - Worker processes call record_latency/record_throughput on their local
          MultiprocessWorkerMetrics instance
        - MultiprocessWorkerMetrics periodically flushes updates to the shared queue
        - This collector drains the queue and aggregates metrics by worker_type
        - InferenceMetricLogger calls snapshot_and_reset() to get aggregated metrics
    
    Thread Safety:
        - Uses internal lock for thread-safe aggregation
        - Queue operations are process-safe (multiprocessing.Queue)
    """

    def __init__(self, metrics_queue) -> None: ...
        """
        Initialize collector with shared metrics queue.
        
        Args:
            metrics_queue: Shared multiprocessing.Queue for receiving MetricUpdate
        """

    def drain_queue(self) -> int: ...
        """
        Drain all pending MetricUpdate messages from the queue.
        
        This should be called periodically (e.g., before snapshot_and_reset).
        
        Returns:
            Number of updates processed
        """

    def snapshot_and_reset(self, worker_type: str, interval_start_ts: float, interval_end_ts: float) -> Any: ...
        """
        Get snapshot for a worker type and reset its metrics.
        
        This first drains the queue to ensure all pending updates are included.
        
        Args:
            worker_type: Type of worker (inference, post_processing)
            interval_start_ts: Start of interval (Unix epoch)
            interval_end_ts: End of interval (Unix epoch)
        
        Returns:
            MetricSnapshot with aggregated metrics for this worker type
        """


# From worker_metrics
class MultiprocessWorkerMetrics:
    """
    Metrics collector for workers running in separate processes.
    
    This class is used INSIDE WORKER PROCESSES. It collects metrics locally
    and periodically flushes them to a shared multiprocessing.Queue.
    
    The main process uses MultiprocessMetricsCollector to aggregate these updates.
    
    Usage in worker process:
        metrics = MultiprocessWorkerMetrics(
            worker_id="inference_0",
            worker_type="inference",
            metrics_queue=shared_queue
        )
    
        # Record metrics (batched locally)
        metrics.record_latency(latency_ms)
        metrics.record_throughput(count=1)
    
        # Periodically flush to main process (e.g., every N items or M seconds)
        metrics.flush()
    
    Thread Safety:
        - Uses internal lock for thread-safe local operations
        - Queue.put() is process-safe
    """

    def __init__(self, worker_id: str, worker_type: str, metrics_queue) -> None: ...
        """
        Initialize worker metrics.
        
        Args:
            worker_id: Unique identifier for this worker
            worker_type: Type of worker (inference, post_processing)
            metrics_queue: Shared queue for sending updates to main process
        """

    FLUSH_INTERVAL_SECONDS: Any
    FLUSH_ITEM_THRESHOLD: Any

    def flush(self) -> None: ...
        """
        Manually flush metrics to the main process.
        """

    def mark_active(self) -> None: ...
        """
        Mark this worker as active.
        """

    def mark_inactive(self) -> None: ...
        """
        Mark this worker as inactive and flush remaining metrics.
        """

    def record_drop(self, count: int = 1, reason: str = 'backpressure') -> None: ...
        """
        Record dropped frames due to backpressure or other reasons.
        
        Args:
            count: Number of frames dropped (default: 1)
            reason: Reason for dropping (default: "backpressure")
                    Common reasons: "backpressure", "stale", "queue_full", "error"
        """

    def record_latency(self, value_ms: float, timestamp: Optional[float] = None) -> None: ...
        """
        Record a latency measurement.
        
        Args:
            value_ms: Latency value in milliseconds
            timestamp: Optional timestamp (unused, for API compatibility)
        """

    def record_throughput(self, count: int = 1, timestamp: Optional[float] = None) -> None: ...
        """
        Record throughput event(s).
        
        Args:
            count: Number of items processed
            timestamp: Optional timestamp (unused, for API compatibility)
        """


# From worker_metrics
class WorkerMetrics:
    """
    Thread-safe metrics storage for worker instances.
    
    Supports two modes:
    1. INSTANCE MODE: Each worker creates its own WorkerMetrics (legacy)
    2. SHARED MODE: All workers of same type share one WorkerMetrics (new)
    
    SHARED MODE DESIGN:
        - One WorkerMetrics per worker_type stored in class-level registry
        - Workers access via WorkerMetrics.get_shared(worker_type)
        - All operations are thread-safe with internal locking
        - Transparent to worker code - still use self.metrics.record_*()
    
    Thread Safety:
        All public methods acquire internal lock before state modification.
        Lock is reentrant (RLock) to support nested calls if needed.
        Snapshot operation is atomic - no data corruption during collection.
    
    Memory Management:
        Shared mode significantly reduces memory overhead:
        - Instance mode: 4 workers * 1000 samples = 4000 floats
        - Shared mode: 1 shared * 1000 samples = 1000 floats (75% reduction)
    
    Backward Compatibility:
        Existing code using WorkerMetrics(worker_id, worker_type) continues
        to work unchanged. To use shared mode, workers call get_shared().
    """

    def __init__(self, worker_id: str, worker_type: str, latency_unit: str = 'ms', throughput_unit: str = 'msg/sec', max_samples: Optional[int] = None, _is_shared: bool = False) -> None: ...
        """
        Initialize worker metrics storage.
        
        Args:
            worker_id: Unique identifier for this worker instance (or "shared" for shared mode)
            worker_type: Type of worker (consumer, inference, post_processing, producer)
            latency_unit: Unit string for latency measurements
            throughput_unit: Unit string for throughput rate
            max_samples: Maximum samples to retain (None = unlimited)
            _is_shared: Internal flag indicating this is a shared instance
        """

    def clear_shared_metrics(cls) -> None: ...
        """
        Clear all shared metrics instances.
        
        Used for testing and cleanup. Should not be called during normal operation.
        """

    def compute_interval_summary(snapshot) -> Dict[str, Any]: ...
        """
        Compute aggregated statistics from a snapshot for reporting.
        
        Args:
            snapshot: MetricSnapshot from snapshot_and_reset()
        
        Returns:
            Dictionary with latency and throughput statistics for the interval
            Omits latency if no samples available
        """

    def get_shared(cls, worker_type: str) -> Any: ...
        """
        Get or create shared WorkerMetrics instance for a worker type.
        
        This is the primary method for workers to access class-level metrics.
        Thread-safe - multiple workers can call concurrently.
        
        Args:
            worker_type: Type of worker (consumer, inference, post_processing, producer)
        
        Returns:
            Shared WorkerMetrics instance for this worker type
        
        Example:
            # In worker __init__:
            self.metrics = WorkerMetrics.get_shared("inference")
        
            # In worker _run:
            self.metrics.record_latency(latency_ms)  # Thread-safe, shared storage
        """

    def mark_active(self) -> None: ...
        """
        Mark this worker as active for the current interval.
        
        For shared metrics, increments active worker count.
        Thread-safe.
        """

    def mark_inactive(self) -> None: ...
        """
        Mark this worker as inactive for the current interval.
        
        For shared metrics, decrements active worker count.
        Thread-safe.
        """

    def merge(cls, metrics_list: List['WorkerMetrics']) -> Any: ...
        """
        Merge multiple WorkerMetrics instances into one aggregate.
        
        NOTE: This method is deprecated for shared metrics mode.
        When using shared metrics, no merging is needed - all workers
        already write to the same instance.
        
        Kept for backward compatibility with instance-mode usage.
        
        Args:
            metrics_list: List of WorkerMetrics to merge
        
        Returns:
            New WorkerMetrics instance with combined data
        """

    def record_drop(self, count: int = 1, reason: str = 'backpressure') -> None: ...
        """
        Record dropped frames due to backpressure or other reasons.
        
        Thread-safe for concurrent calls from multiple workers.
        
        Args:
            count: Number of frames dropped (default: 1)
            reason: Reason for dropping (default: "backpressure")
                    Common reasons: "backpressure", "stale", "queue_full", "error"
        """

    def record_latency(self, value_ms: float, timestamp: Optional[float] = None) -> None: ...
        """
        Record a latency measurement.
        
        Thread-safe for concurrent calls from multiple workers.
        
        Args:
            value_ms: Latency value in milliseconds
            timestamp: Optional timestamp (unused, for future extensions)
        """

    def record_throughput(self, count: int = 1, timestamp: Optional[float] = None) -> None: ...
        """
        Record throughput event(s).
        
        Thread-safe for concurrent calls from multiple workers.
        
        Args:
            count: Number of items processed (default: 1)
            timestamp: Optional timestamp (unused, for future extensions)
        """

    def set_running(self, running: bool) -> None: ...
        """
        Set worker running state.
        """

    def snapshot_and_reset(self, interval_start_ts: float, interval_end_ts: float) -> Any: ...
        """
        Capture current metrics and reset for next interval.
        
        This method atomically:
        1. Creates a snapshot of current metrics
        2. Clears internal storage for next interval
        3. Preserves active state
        
        Thread Safety:
            Atomic operation - entire snapshot under lock.
            Safe for concurrent access from multiple workers.
        
        Args:
            interval_start_ts: Start timestamp of the interval (Unix epoch)
            interval_end_ts: End timestamp of the interval (Unix epoch)
        
        Returns:
            MetricSnapshot containing interval data
        """

    def to_summary_dict(self) -> Dict[str, Any]: ...
        """
        Generate summary statistics from current state without reset.
        
        Thread-safe.
        
        Returns:
            Dictionary with latency and throughput statistics
        
        Note:
            Omits latency metrics when no data available (inactive worker).
        """


from . import analytics_publisher, app_deployment, app_event_listener, async_producer_pool, camera_config_monitor, consumer_manager, deployment_refresh_listener, frame_cache, inference_metric_logger, inference_worker, metric_publisher, post_processing_manager, producer_worker, stream_pipeline, utils, worker_metrics