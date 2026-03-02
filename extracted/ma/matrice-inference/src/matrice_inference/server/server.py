"""Module providing server functionality."""

import os
import threading
import time
import urllib.request
import logging
import asyncio
import signal
import atexit
import time
from datetime import datetime, timezone
from typing import Optional, Callable, Dict, Any

from matrice.action_tracker import ActionTracker
from matrice_analytics.post_processing.post_processor import PostProcessor
from matrice_inference.server.proxy_interface import MatriceProxyInterface
from matrice_inference.server.model.model_manager_wrapper import ModelManagerWrapper
from matrice_inference.server.inference_interface import InferenceInterface
from matrice_inference.server.stream.stream_pipeline import StreamingPipeline
from matrice_inference.server.stream.app_deployment import AppDeployment


# Module constants
DEFAULT_EXTERNAL_PORT = 80
DEFAULT_SHUTDOWN_THRESHOLD_MINUTES = 15
MIN_SHUTDOWN_THRESHOLD_MINUTES = 1
HEARTBEAT_INTERVAL_SECONDS = 30
SHUTDOWN_CHECK_INTERVAL_SECONDS = 30
CLEANUP_DELAY_SECONDS = 5
FINAL_CLEANUP_DELAY_SECONDS = 10
MAX_IP_FETCH_ATTEMPTS = 5  # Increased from 3 to 5
IP_FETCH_TIMEOUT_SECONDS = 30  # Increased from 10 to 30
# Shutdown after 10 minutes of consecutive failures (increased from 5 minutes)
MAX_HEARTBEAT_FAILURES_BEFORE_SHUTDOWN = 20  # 10 minutes at 30 second intervals
MAX_DEPLOYMENT_CHECK_FAILURES_BEFORE_SHUTDOWN = 20  # 10 minutes at 30 second intervals


class MatriceDeployServer:
    """Class for managing model deployment and server functionality."""

    def __init__(
        self,
        load_model: Optional[Callable] = None,
        predict: Optional[Callable] = None,
        action_id: str = "",
        external_port: int = DEFAULT_EXTERNAL_PORT,
        batch_predict: Optional[Callable] = None,
        custom_post_processing_fn: Optional[Callable] = None,
        preprocess_fn: Optional[Callable] = None,
        postprocess_fn: Optional[Callable] = None,
        preprocess_params: Optional[Dict[str, Any] ]= None,
        postprocess_params: Optional[Dict[str, Any]] = None,

        model_path: Optional[str] = None,
        runtime_framework: Optional[str] = None,
        use_dynamic_batching: bool = False,

        num_classes: Optional[int] = None,
        input_size: Optional[Any] = None,
        max_batch_size: Optional[int] = None,
        use_trt_accelerator: Optional[bool] = None,
        async_predict: Optional[Callable] = None,
        async_batch_predict: Optional[Callable] = None,
        async_load_model: Optional[Callable] = None,
        is_inference_API: bool = False,
        # CUDA SHM inference engine instance (replaces consumer + inference workers)
        # Pass an instance of CudaShmInferenceEngine from your deploy code
        cuda_shm_engine: Optional[Any] = None,
    ):
        """Initialize MatriceDeploy.

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
        try:
            # Validate inputs
            self._validate_init_parameters(
                load_model, predict, action_id, external_port, preprocess_fn, postprocess_fn, 
                async_predict, async_batch_predict, async_load_model
            )

            self.external_port = int(external_port)

            # Initialize action tracker
            self.action_id = action_id
            self.action_tracker = ActionTracker(action_id)

            # Get session and RPC from action tracker
            self.session = self.action_tracker.session
            self.rpc = self.session.rpc
            self.action_details = self.action_tracker.action_details
            self.job_params = self.action_tracker.get_job_params()
            self.server_type = self.action_details.get('server_type', 'fastapi')
            self.app_id = self.job_params.get("application_id", "")
            self.app_name = self.job_params.get("application_name", "")
            self.app_version = self.job_params.get("application_version", "")

            logging.info("Action details: %s", self.action_details)

            # Extract deployment information
            self.deployment_instance_id = self.action_details.get(
                "_idModelDeployInstance"
            )
            self.deployment_id = self.action_details.get("_idDeployment")
            self.model_id = self.action_details.get("_idModelDeploy")
            self.inference_pipeline_id = self.action_details.get("inference_pipeline_id")

            # Validate deployment information
            if not all(
                [self.deployment_instance_id, self.deployment_id, self.model_id]
            ):
                raise ValueError(
                    "Missing required deployment identifiers in action details"
                )

            # Set shutdown configuration
            shutdown_threshold_minutes = int(
                self.action_details.get(
                    "shutdownThreshold", DEFAULT_SHUTDOWN_THRESHOLD_MINUTES
                )
            )
            if shutdown_threshold_minutes < MIN_SHUTDOWN_THRESHOLD_MINUTES:
                logging.warning(
                    "Invalid shutdown threshold %d, using default: %d",
                    shutdown_threshold_minutes,
                    DEFAULT_SHUTDOWN_THRESHOLD_MINUTES,
                )
                shutdown_threshold_minutes = DEFAULT_SHUTDOWN_THRESHOLD_MINUTES
            self.shutdown_threshold = shutdown_threshold_minutes * 60

            self.auto_shutdown = bool(self.action_details.get("autoShutdown", True))

            # Store user functions
            self.load_model = load_model
            self.predict = predict
            self.batch_predict = batch_predict
            self.async_predict = async_predict
            self.async_batch_predict = async_batch_predict
            self.async_load_model = async_load_model
            self.custom_post_processing_fn = custom_post_processing_fn

            # Store inference API flag
            self.is_inference_API = is_inference_API

            # CUDA SHM engine instance (replaces consumer + inference workers)
            self.cuda_shm_engine = cuda_shm_engine

            # Validate functions only if NOT using CUDA SHM engine
            if self.cuda_shm_engine:
                logging.info(
                    "CUDA SHM engine provided - skipping load_model/predict validation. "
                    "Engine handles inference directly."
                )
            else:
                # Validate that required functions are provided and not None
                if self.load_model is None:
                    logging.warning("load_model function is None - model loading will fail!")
                else:
                    logging.info(f"✓ load_model function provided: {type(self.load_model).__name__}")

                if self.predict is None:
                    logging.warning("predict function is None - inference will fail!")
                else:
                    logging.info(f"✓ predict function provided: {type(self.predict).__name__}")

                # Test if functions are picklable (for multiprocessing)
                import pickle
                try:
                    pickle.dumps(self.load_model)
                    logging.info("✓ load_model is picklable")
                except Exception as e:
                    logging.error(f"✗ load_model is NOT picklable: {e}")

                try:
                    pickle.dumps(self.predict)
                    logging.info("✓ predict is picklable")
                except Exception as e:
                    logging.error(f"✗ predict is NOT picklable: {e}")

            # TMM required args
            self.model_path = model_path
            self.runtime_framework = runtime_framework
            self.use_dynamic_batching = use_dynamic_batching

            logging.info("Model path: %s, Runtime framework: %s passed to MDS", model_path, runtime_framework)

            # TMM non-mandatory args
            self.num_classes = num_classes 
            self.max_batch_size = max_batch_size
            self.use_trt_accelerator = use_trt_accelerator
            self.input_size = input_size

            logging.info("Num classes: %s, Input size: %s, Max batch size: %s, Use TRT accelerator: %s passed to MDS",
                         num_classes, input_size, max_batch_size, use_trt_accelerator)

            # BYOM defined codebase for model specific processing on triton 
            self.preprocess_fn = preprocess_fn
            self.postprocess_fn = postprocess_fn
            self.preprocess_params = preprocess_params
            self.postprocess_params = postprocess_params

            # Initialize component references
            self.proxy_interface = None
            self.model_manager = None
            self.inference_interface = None
            self.post_processor = None
            self.streaming_pipeline = None
            self.app_deployment = None
            self.stream_manager = None
            self.camera_config_monitor = None

            # Initialize utilities
            self.utils = None

            # Shutdown coordination
            self._shutdown_event = threading.Event()
            self._stream_manager_thread = None

            # Register shutdown handlers to ensure clean shutdown
            self._register_shutdown_handlers()

            # Update initial status
            self.action_tracker.update_status(
                "MDL_DPY_ACK",
                "OK",
                "Model deployment acknowledged",
            )

            logging.info("MatriceDeployServer initialized successfully")

        except Exception as exc:
            logging.error("Failed to initialize MatriceDeployServer: %s", str(exc))
            raise

    def _register_shutdown_handlers(self):
        """Register signal handlers and atexit callback for graceful shutdown."""
        def signal_handler(signum, frame):
            logging.info("Received signal %d, triggering shutdown through utils...", signum)
            try:
                # Use utils shutdown to trigger coordinated shutdown
                if hasattr(self, 'utils') and self.utils:
                    self.utils._shutdown_initiated.set()
                else:
                    # Fallback to direct shutdown if utils not available
                    self.stop_server()
                    os._exit(0)
            except Exception as exc:
                logging.error("Error during signal-triggered shutdown: %s", str(exc))
                os._exit(1)

        def atexit_handler():
            logging.info("Process exiting, ensuring graceful shutdown...")
            try:
                if not self._shutdown_event.is_set():
                    if hasattr(self, 'utils') and self.utils and not self.utils._shutdown_initiated.is_set():
                        self.utils._shutdown_initiated.set()
                    else:
                        self.stop_server()
            except Exception as exc:
                logging.error("Error during atexit shutdown: %s", str(exc))

        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        # Register atexit handler as a final safety net
        atexit.register(atexit_handler)

        logging.info("Shutdown handlers registered successfully")

    def _validate_init_parameters(self, load_model, predict, action_id, external_port, preprocess_fn, postprocess_fn, async_predict, async_batch_predict, async_load_model):
        """Validate initialization parameters.

        Args:
            load_model: Model loading function
            predict: Prediction function
            action_id: Action ID string
            external_port: External port number
            preprocess_fn: Preprocessing function
            postprocess_fn: Postprocessing function
            async_predict: Asynchronous single prediction function
            async_batch_predict: Asynchronous batch prediction function
            async_load_model: Asynchronous model loading function

        Raises:
            ValueError: If parameters are invalid
        """
        # Validate callable functions
        if load_model is not None and not callable(load_model):
            raise ValueError("load_model must be callable or None")

        if predict is not None and not callable(predict):
            raise ValueError("predict must be callable or None")

        # if async_predict is not None and not callable(async_predict):
        #     raise ValueError("async_predict must be callable or None")

        # if async_load_model is not None and not callable(async_load_model):
        #     raise ValueError("async_load_model must be callable or None")

        # Validate action_id
        if not isinstance(action_id, str):
            raise ValueError("action_id must be a string")

        external_port = int(external_port)
        # Validate external_port
        if not isinstance(external_port, int):
            raise ValueError("external_port must be an integer")
        if not (1 <= external_port <= 65535):
            raise ValueError(
                f"Invalid external port: {external_port}. Must be between 1 and 65535"
            )
        if preprocess_fn is not None and not callable(preprocess_fn):
            raise ValueError("preprocess_fn must be callable or None")
        
        if postprocess_fn is not None and not callable(postprocess_fn):
            raise ValueError("postprocess_fn must be callable or None")

    def start(self, block=True):
        """Start the proxy interface and all server components."""
        try:
            self._validate_configuration()

            # CUDA SHM mode: Skip model manager, inference interface, AND streaming pipeline entirely
            # Engine operates independently - just load camera configs and start it
            if self.cuda_shm_engine:
                logging.info(
                    "CUDA SHM engine mode - skipping model manager, inference interface, and streaming pipeline. "
                    "Engine handles inference directly via CUDA IPC ring buffers."
                )
                # Still need to extract post-processing config for the CUDA SHM engine
                self._initialize_post_processing_config()
                # Initialize CUDA SHM engine with cameras (skip streaming pipeline)
                self._initialize_cuda_shm_engine()
            else:
                # Normal mode: Initialize model manager and full inference interface
                self._initialize_model_manager()
                self._initialize_inference_interface()
                self._initialize_streaming_pipeline()

            self._start_proxy_interface()
            
            logging.info("All server components started successfully")

            # Update deployment status and address
            self.action_tracker.update_status(
                "MDL_DPY_MDL",
                "OK",
                "Model deployment model loaded",
            )
            self.utils = MatriceDeployServerUtils(
                self.action_tracker, self.inference_interface, self.external_port, self
            )
            # update_deployment_address is non-critical - don't kill the pipeline if it fails
            # The streaming pipeline is already running at this point
            try:
                self.utils.update_deployment_address()
            except Exception as addr_err:
                logging.warning(
                    f"Failed to update deployment address (non-fatal): {addr_err}. "
                    "Streaming pipeline will continue running."
                )
            self.utils.run_background_checkers()
            self.action_tracker.update_status(
                "MDL_DPY_STR",
                "SUCCESS",
                "Model deployment started",
            )
            if block:
                self.utils.wait_for_shutdown()
        except Exception as exc:
            logging.error("Failed to start server components: %s", str(exc))
            self.action_tracker.update_status(
                "ERROR",
                "ERROR",
                f"Model deployment error: {str(exc)}",
            )
            raise

    def _validate_configuration(self):
        """Validate server configuration before starting components."""
        required_env_vars = ["INTERNAL_PORT"]
        missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {missing_vars}")

        # Validate action details
        required_details = ["_idModelDeployInstance", "_idDeployment", "_idModelDeploy"]
        missing_details = [
            key for key in required_details if not self.action_details.get(key)
        ]
        if missing_details:
            raise ValueError(f"Missing required action details: {missing_details}")

        # Validate port
        internal_port = int(os.environ["INTERNAL_PORT"])
        if not (1 <= internal_port <= 65535):
            raise ValueError(f"Invalid internal port: {internal_port}")

        logging.info("Configuration validation passed")

    def _initialize_model_manager(self):
        """Initialize the model manager component."""
        logging.info("Initializing model manager wrapper for model ID: %s", self.model_id)

        # Determine model type based on server configuration
        model_type = "default"
        internal_server_type = None

        server_type_list = self.server_type.lower().split('_')
        if "triton" in server_type_list:
            model_type = "triton"
            internal_server_type = "grpc" if "grpc" in server_type_list else "rest"
        elif "fastapi" in server_type_list:
            model_type = "default"
            internal_server_type = None

        # Validate functions before passing to ModelManagerWrapper
        logging.info(f"load_model type before ModelManagerWrapper: {type(self.load_model)}")
        logging.info(f"predict type before ModelManagerWrapper: {type(self.predict)}")

        if self.load_model is None:
            logging.error("load_model is None before creating ModelManagerWrapper!")
        if self.predict is None:
            logging.error("predict is None before creating ModelManagerWrapper!")

        self.model_manager = ModelManagerWrapper(
            action_tracker=self.action_tracker,
            test_env=False,  # Use production mode with action_tracker
            model_type=model_type,
            num_model_instances=self.action_details.get("numModelInstances", 1),
            load_model=self.load_model,
            predict=self.predict,
            batch_predict=self.batch_predict,

            model_name=self.action_details.get("modelKey", None),
            model_path=self.model_path,
            runtime_framework=self.runtime_framework,
            internal_server_type=internal_server_type,
            internal_port=int(os.environ["INTERNAL_PORT"]),
            internal_host="localhost",
            input_size=self.input_size,
            num_classes=self.num_classes,
            use_dynamic_batching=self.use_dynamic_batching,
            max_batch_size=self.max_batch_size,
            use_trt_accelerator=self.use_trt_accelerator,

            preprocess_fn=self.preprocess_fn,
            postprocess_fn=self.postprocess_fn,
            preprocess_params=self.preprocess_params,
            postprocess_params=self.postprocess_params,
            async_predict=self.async_predict,
            async_batch_predict=self.async_batch_predict,
            async_load_model=self.async_load_model,
        )

        logging.info("Model manager wrapper initialized successfully")

    def _initialize_post_processing_config(self):
        """Initialize post-processing configuration only (for CUDA SHM mode).

        This extracts the post-processing config without creating the full
        InferenceInterface. Used when CUDA SHM engine handles inference directly.
        """
        logging.info("Initializing post-processing configuration for CUDA SHM engine")

        # Initialize PostProcessor configuration from job params
        post_processing_config = self.job_params.get(
            "post_processing_config", self.job_params.get("postProcessingConfig", None)
        )

        # Add session and facial recognition server ID to config if available
        if post_processing_config is None:
            post_processing_config = {}
        if isinstance(post_processing_config, dict):
            post_processing_config["facial_recognition_server_id"] = self.job_params.get("facial_recognition_server_id", None)
            post_processing_config["lpr_server_id"] = self.job_params.get("lpr_server_id", None)
            post_processing_config["session"] = self.session  # Pass the session to post-processing
            # Pass deployment_id for facial recognition deployment update
            post_processing_config["deployment_id"] = self.deployment_id

        # Get index_to_category from action_tracker if available
        index_to_category = None
        target_categories = None
        try:
            if hasattr(self.action_tracker, 'get_index_to_category'):
                index_to_category = self.action_tracker.get_index_to_category(
                    getattr(self.action_tracker, 'is_exported', True)
                )
        except Exception as e:
            logging.warning(f"Failed to get index_to_category from action_tracker: {str(e)}")

        # Store post-processing config for passing to CUDA SHM engine
        self._post_processing_config = post_processing_config
        self._index_to_category = index_to_category
        self._target_categories = target_categories

        # Pass config to CUDA SHM engine if available
        if self.cuda_shm_engine:
            self.cuda_shm_engine.set_post_processing_config(
                post_processing_config=post_processing_config,
                app_name=self.app_name,
                index_to_category=index_to_category,
                target_categories=target_categories,
            )
            logging.info(f"Post-processing config passed to CUDA SHM engine: app_name={self.app_name}")

        logging.info("Post-processing configuration initialized successfully")

    def _initialize_inference_interface(self):
        """Initialize the inference interface component."""
        logging.info("Initializing inference interface and post-processor")

        # Initialize PostProcessor with configuration from job params
        post_processing_config = self.job_params.get(
            "post_processing_config", self.job_params.get("postProcessingConfig", None)
        )
        
        # Add session and facial recognition server ID to config if available
        if post_processing_config is None:
            post_processing_config = {}
        if isinstance(post_processing_config, dict):
            post_processing_config["facial_recognition_server_id"] = self.job_params.get("facial_recognition_server_id", None)
            post_processing_config["lpr_server_id"] = self.job_params.get("lpr_server_id", None)
            post_processing_config["session"] = self.session  # Pass the session to post-processing
            # Pass deployment_id for facial recognition deployment update
            post_processing_config["deployment_id"] = self.deployment_id 
        
        # Get index_to_category from action_tracker if available
        index_to_category = None
        target_categories = None
        try:
            if hasattr(self.action_tracker, 'get_index_to_category'):
                index_to_category = self.action_tracker.get_index_to_category(
                    getattr(self.action_tracker, 'is_exported', True)
                )
        except Exception as e:
            logging.warning(f"Failed to get index_to_category from action_tracker: {str(e)}")
        
        # Store post-processing config for passing to StreamingPipeline (as dict, not extracted from post_processor)
        self._post_processing_config = post_processing_config
        self._index_to_category = index_to_category
        self._target_categories = target_categories
        
        # Create PostProcessor
        self.post_processor = PostProcessor(
            post_processing_config=post_processing_config,
            app_name=self.app_name,
            index_to_category=index_to_category,
            target_categories=target_categories
        )
        
        # Create InferenceInterface with simplified parameters
        self.inference_interface = InferenceInterface(
            model_manager_wrapper=self.model_manager,
            post_processor=self.post_processor
        )

        logging.info("Inference interface and post-processor initialized successfully")

    def _initialize_cuda_shm_engine(self):
        """Initialize CUDA SHM engine with camera configs (no streaming pipeline needed)."""
        try:
            logging.info("Initializing CUDA SHM engine...")

            # Get camera configs from app deployment
            app_deployment_id = self.action_details.get("app_deployment_id", self.job_params.get("app_deployment_id", None))
            if not app_deployment_id:
                logging.warning("No app_deployment_id found, CUDA SHM engine will start with no cameras")
                camera_configs = {}
            else:
                self.app_deployment = AppDeployment(
                    session=self.session,
                    app_deployment_id=app_deployment_id,
                    deployment_instance_id=self.deployment_instance_id,
                    connection_timeout=self.job_params.get("stream_connection_timeout", 1200),
                    action_id=self.action_id
                )

                logging.info("CUDA SHM mode: Loading all cameras synchronously from API...")
                camera_configs = self.app_deployment.get_camera_configs()
                if not camera_configs:
                    logging.warning("CUDA SHM mode: No cameras found from API")
                else:
                    logging.info(f"CUDA SHM mode: Loaded {len(camera_configs)} cameras")

            # Pass camera configs to engine and start it
            # Convert CameraConfig objects to dicts for e2e_benchmark engine compatibility
            if camera_configs:
                converted_configs = {}
                for cam_id, cfg in camera_configs.items():
                    logging.info(f"Processing camera {cam_id}: type={type(cfg).__name__}, hasattr_stream_config={hasattr(cfg, 'stream_config')}")
                    if hasattr(cfg, 'stream_config'):
                        # CameraConfig has stream_config dict with Redis settings
                        sc = cfg.stream_config if isinstance(cfg.stream_config, dict) else {}

                        # Auto-detect stream_type from video source URL
                        # Check input_topic, video_path attributes and stream_config
                        video_path = (
                            getattr(cfg, 'video_path', None) or
                            getattr(cfg, 'input_topic', None) or
                            sc.get('video_path', '') or
                            sc.get('input_topic', '')
                        )
                        # ALWAYS auto-detect from URL, ignore upstream stream_type value
                        # rtsp:// or rtsps:// = "rtsp", everything else = "file"
                        if video_path and isinstance(video_path, str):
                            if video_path.startswith(('rtsp://', 'rtsps://')):
                                stream_type = 'rtsp'
                            else:
                                stream_type = 'file'
                        else:
                            stream_type = 'file'  # Default to 'file' if no video_path

                        cfg_dict = {
                            "camera_id": getattr(cfg, 'camera_id', cam_id),
                            "input_topic": getattr(cfg, 'input_topic', None),
                            "output_topic": getattr(cfg, 'output_topic', None),
                            "stream_type": stream_type,
                            "camera_name": sc.get('camera_name', cam_id),
                            "camera_group": sc.get('camera_group', 'default'),
                            "location": sc.get('location', 'unknown'),
                            "stream_config": {
                                "host": sc.get('host', 'localhost'),
                                "port": sc.get('port', 6379),
                                "password": sc.get('password'),
                                "username": sc.get('username'),
                                "db": sc.get('db', 0),
                                # Keep original stream_type in stream_config for Redis connection detection
                                # The top-level stream_type indicates video source type (file/rtsp)
                                "stream_type": sc.get('stream_type', 'redis'),
                                "camera_name": sc.get('camera_name', cam_id),
                                "camera_group": sc.get('camera_group', 'default'),
                                "location": sc.get('location', 'unknown'),
                            },
                        }
                        cfg_dict["app_deployment_id"] = app_deployment_id or ""
                        cfg_dict["application_id"] = self.app_id or ""
                        converted_configs[cam_id] = cfg_dict
                    elif isinstance(cfg, dict):
                        # Fix stream_type for dict configs (upstream may send 'redis' which is invalid)
                        fixed_cfg = cfg.copy()
                        video_path = cfg.get('video_path', '') or cfg.get('input_topic', '')
                        original_stream_type = cfg.get('stream_type', 'unset')
                        if video_path and isinstance(video_path, str):
                            if video_path.startswith(('rtsp://', 'rtsps://')):
                                fixed_cfg['stream_type'] = 'rtsp'
                            else:
                                fixed_cfg['stream_type'] = 'file'
                        elif fixed_cfg.get('stream_type') == 'redis':
                            # 'redis' is not a valid video source type, default to 'file'
                            fixed_cfg['stream_type'] = 'file'
                        logging.info(f"Camera {cam_id}: stream_type fixed from '{original_stream_type}' to '{fixed_cfg.get('stream_type')}'")
                        fixed_cfg["app_deployment_id"] = fixed_cfg.get("app_deployment_id", "") or app_deployment_id or ""
                        fixed_cfg["application_id"] = fixed_cfg.get("application_id", "") or self.app_id or ""
                        converted_configs[cam_id] = fixed_cfg
                    else:
                        # Fallback for other object types
                        # Auto-detect stream_type from video source URL
                        video_path = getattr(cfg, 'video_path', None) or getattr(cfg, 'input_topic', None) or ''
                        if video_path and isinstance(video_path, str) and video_path.startswith(('rtsp://', 'rtsps://')):
                            stream_type = 'rtsp'
                        else:
                            stream_type = 'file'

                        cfg_dict = {
                            "camera_id": getattr(cfg, 'camera_id', cam_id),
                            "input_topic": getattr(cfg, 'input_topic', None),
                            "output_topic": getattr(cfg, 'output_topic', None),
                            "stream_type": stream_type,
                            "stream_config": {},
                        }
                        cfg_dict["app_deployment_id"] = app_deployment_id or ""
                        cfg_dict["application_id"] = self.app_id or ""
                        converted_configs[cam_id] = cfg_dict
                logging.info(f"Converted {len(converted_configs)} camera configs to dict format")
                self.cuda_shm_engine.set_camera_configs(converted_configs)

            # Initialize AnalyticsPublisher for results-agg publishing
            self._initialize_cuda_shm_analytics_publisher(
                camera_configs=converted_configs if camera_configs else {},
                app_deployment_id=app_deployment_id,
            )

            logging.info("CUDA SHM mode: Starting engine...")
            self.cuda_shm_engine.start()
            logging.info("CUDA SHM mode: Engine started successfully")

        except Exception as e:
            logging.error(f"Failed to initialize CUDA SHM engine: {e}")
            raise

    def _initialize_cuda_shm_analytics_publisher(self, camera_configs, app_deployment_id):
        """Initialize AnalyticsPublisher for CUDA SHM mode.

        Creates a multiprocessing Queue, sets it on the engine, and starts an
        AnalyticsPublisher thread with a bridge that drains the mp.Queue.
        """
        import multiprocessing as mp

        try:
            from matrice_inference.server.stream.analytics_publisher import AnalyticsPublisher
        except ImportError:
            logging.warning("AnalyticsPublisher not available, results-agg will not be published")
            return

        try:
            # Extract Redis connection from camera configs (env vars as fallback)
            redis_host = os.environ.get("REDIS_HOST", "localhost")
            redis_port = int(os.environ.get("REDIS_PORT", "6379"))
            redis_password = os.environ.get("REDIS_PASSWORD")
            redis_username = None
            for cfg in camera_configs.values():
                sc = cfg.get("stream_config", {}) if isinstance(cfg, dict) else {}
                if sc.get("host"):
                    redis_host = sc["host"]
                    redis_port = int(sc.get("port", 6379))
                    redis_password = sc.get("password")
                    redis_username = sc.get("username")
                    break

            analytics_mp_queue = mp.Queue(maxsize=5000)
            self.cuda_shm_engine.set_analytics_queue(analytics_mp_queue)

            analytics_publisher = AnalyticsPublisher(
                camera_configs=camera_configs,
                app_deployment_id=app_deployment_id,
                inference_pipeline_id=self.inference_pipeline_id,
                deployment_instance_id=self.deployment_instance_id,
                app_id=self.app_id,
                app_name=self.app_name,
                app_version=self.app_version,
                redis_host=redis_host,
                redis_port=redis_port,
                redis_password=redis_password,
                redis_username=redis_username,
            )
            self._cuda_shm_analytics_publisher = analytics_publisher
            self._cuda_shm_analytics_mp_queue = analytics_mp_queue

            # Start analytics publisher thread
            analytics_publisher.start()

            # Bridge thread: drains mp.Queue and feeds AnalyticsPublisher's internal queue
            import threading

            def _analytics_bridge():
                while True:
                    try:
                        task_data = analytics_mp_queue.get(timeout=1.0)
                        analytics_publisher.enqueue_analytics_data(task_data)
                    except Exception:
                        # queue.Empty on timeout or process shutdown
                        if not analytics_publisher.running:
                            break

            bridge_thread = threading.Thread(
                target=_analytics_bridge,
                name="AnalyticsBridge",
                daemon=True,
            )
            bridge_thread.start()

            logging.info(
                f"CUDA SHM mode: AnalyticsPublisher started "
                f"(redis={redis_host}:{redis_port}, app_name={self.app_name})"
            )
        except Exception as e:
            logging.warning(f"Failed to start AnalyticsPublisher for CUDA SHM mode (non-fatal): {e}")

    def _initialize_streaming_pipeline(self):
        """Initialize the streaming pipeline component."""
        try:
            logging.info("Initializing streaming pipeline...")
            
            # Initialize app deployment to get camera configurations
            app_deployment_id = self.action_details.get("app_deployment_id", self.job_params.get("app_deployment_id", None))
            if not app_deployment_id:
                logging.warning("No app_deployment_id found in job_params, starting pipeline without cameras")
                camera_configs = {}
            else:
                self.app_deployment = AppDeployment(
                    session=self.session,
                    app_deployment_id=app_deployment_id,
                    deployment_instance_id=self.deployment_instance_id,
                    connection_timeout=self.job_params.get("stream_connection_timeout", 1200),  # Increased timeout
                    action_id=self.action_id
                )

                # CUDA SHM mode: Load ALL cameras from API at startup (REQUIRED)
                # Engine operates independently - set camera configs and start it directly
                if self.cuda_shm_engine:
                    logging.info("CUDA SHM mode: Loading all cameras synchronously from API...")
                    try:
                        camera_configs = self.app_deployment.get_camera_configs()
                        if not camera_configs:
                            logging.warning("CUDA SHM mode: No cameras found from API - engine may not start")
                        else:
                            logging.info(f"CUDA SHM mode: Loaded {len(camera_configs)} cameras for engine initialization")
                            # Fix stream_type in camera configs (upstream may send 'redis' which is invalid)
                            for cam_id, cfg in camera_configs.items():
                                if isinstance(cfg, dict):
                                    video_path = cfg.get('video_path', '') or cfg.get('input_topic', '')
                                    if video_path and isinstance(video_path, str):
                                        if video_path.startswith(('rtsp://', 'rtsps://')):
                                            cfg['stream_type'] = 'rtsp'
                                        else:
                                            cfg['stream_type'] = 'file'
                                    elif cfg.get('stream_type') == 'redis':
                                        cfg['stream_type'] = 'file'
                                    logging.info(f"Camera {cam_id}: stream_type set to '{cfg.get('stream_type')}'")
                            # Pass camera configs to engine and start it independently
                            self.cuda_shm_engine.set_camera_configs(camera_configs)
                            logging.info("CUDA SHM mode: Starting engine independently...")
                            self.cuda_shm_engine.start()
                            logging.info("CUDA SHM mode: Engine started successfully")
                    except Exception as e:
                        logging.error(f"CUDA SHM mode: Failed to load cameras or start engine: {e}")
                        camera_configs = {}
                else:
                    # Normal mode: Skip initial camera fetch to avoid Redis auth issues and performance problems
                    # with large camera deployments (1000+ cameras). The system will start with no cameras
                    # and rely entirely on refresh events to provide camera configurations dynamically.
                    camera_configs = {}
                    logging.info(
                        "Skipping initial camera fetch - system will wait for refresh events to provide camera configurations. "
                        "This avoids Redis authentication issues and improves startup performance."
                    )
            
            # Create streaming pipeline with configured parameters
            self.streaming_pipeline = StreamingPipeline(
                inference_interface=self.inference_interface,
                inference_queue_maxsize=self.job_params.get("inference_queue_maxsize", 5000),
                postproc_queue_maxsize=self.job_params.get("postproc_queue_maxsize", 5000),
                output_queue_maxsize=self.job_params.get("output_queue_maxsize", 5000),
                message_timeout=self.job_params.get("message_timeout", 2.0),  # Increased from 1.0
                inference_timeout=self.job_params.get("inference_timeout", 60.0),  # Increased from 30.0
                shutdown_timeout=self.job_params.get("shutdown_timeout", 60.0),  # Increased from 30.0
                camera_configs=camera_configs,
                app_deployment_id=app_deployment_id,
                inference_pipeline_id=self.inference_pipeline_id,
                enable_analytics_publisher=self.job_params.get("enable_analytics_publisher", True),

                deployment_id=self.deployment_id,
                deployment_instance_id=self.deployment_instance_id,
                action_id=self.action_id,
                app_id=self.app_id,
                app_name=self.app_name,
                app_version=self.app_version,
                use_shared_metrics=self.job_params.get("use_shared_metrics", True), # YET to be implemented
                # TODO : Add option for toggling metric logging and interval in job params
                # Pass predict functions from MatriceDeployServer to inference workers
                load_model=self.load_model,
                predict=self.predict,
                async_predict=self.async_predict,
                async_batch_predict=self.async_batch_predict,
                async_load_model=self.async_load_model,
                batch_predict=self.batch_predict,
                # Pass post-processing configuration as dict (not extracted from post_processor)
                post_processing_config=getattr(self, '_post_processing_config', {}),
                index_to_category=getattr(self, '_index_to_category', None),
                target_categories=getattr(self, '_target_categories', None),
                # Pass inference API flag to control worker count
                is_inference_API=self.is_inference_API,
            )
            
            # Start the pipeline (now manages its own event loop thread)
            self.streaming_pipeline.start()

            # Start camera config monitor if app deployment is available
            self._start_camera_config_monitor()

            logging.info("Streaming pipeline initialized successfully")
            
        except Exception as e:
            logging.error(f"Failed to initialize streaming pipeline: {str(e)}")
            raise

    def _start_camera_config_monitor(self):
        """Start the camera config monitor and app event listener if app deployment is available."""
        try:
            if not self.app_deployment:
                logging.info("No app deployment configured, skipping camera config monitor")
                return

            if not self.streaming_pipeline:
                logging.warning("Streaming pipeline not initialized, skipping camera config monitor")
                return

            # CUDA SHM mode: Skip event listeners (cameras loaded at startup)
            # Set cuda_shm_enable_dynamic_updates=True in job_params to re-enable
            cuda_shm_enable_dynamic_updates = self.job_params.get("cuda_shm_enable_dynamic_updates", False)
            if self.cuda_shm_engine and not cuda_shm_enable_dynamic_updates:
                logging.info(
                    "CUDA SHM mode: Event listeners DISABLED (cameras loaded at startup). "
                    "Set cuda_shm_enable_dynamic_updates=True in job_params to re-enable."
                )
                return

            # Get check interval and heartbeat interval from job params
            check_interval = self.job_params.get("camera_config_check_interval", 60)
            heartbeat_interval = self.job_params.get("app_deployment_heartbeat_interval", 30)

            # Import and create the monitor
            from matrice_inference.server.stream.camera_config_monitor import CameraConfigMonitor

            self.camera_config_monitor = CameraConfigMonitor(
                app_deployment=self.app_deployment,
                streaming_pipeline=self.streaming_pipeline,
                check_interval=check_interval,
                heartbeat_interval=heartbeat_interval
            )

            # Start monitoring
            self.camera_config_monitor.start()
            logging.info(f"Camera config monitor started (check interval: {check_interval}s, heartbeat interval: {heartbeat_interval}s)")

            # Initialize and start app event listener for real-time topic updates
            try:
                # Get the event loop from the streaming pipeline
                event_loop = None
                if self.streaming_pipeline and hasattr(self.streaming_pipeline, '_event_loop'):
                    event_loop = self.streaming_pipeline._event_loop
                    if event_loop:
                        logging.info(f"Using streaming pipeline's event loop for event listener")
                    else:
                        logging.warning("Streaming pipeline has no event loop, event listener may not work properly")
                else:
                    logging.error("Could not get event loop from streaming pipeline, event listener may not work properly")

                success = self.app_deployment.initialize_event_listener(
                    streaming_pipeline=self.streaming_pipeline,
                    event_loop=event_loop
                )

                if success:
                    logging.info("App event listener started for real-time topic updates")
                else:
                    logging.warning("Failed to start app event listener, will rely on polling")
            except Exception as e:
                logging.error(f"Error starting app event listener: {str(e)}")
                # Don't raise - event listener is complementary to polling

            # Initialize and start deployment refresh listener (PRIMARY source of truth)
            try:
                success = self.app_deployment.initialize_refresh_listener(
                    streaming_pipeline=self.streaming_pipeline,
                    event_loop=event_loop,
                    camera_config_monitor=self.camera_config_monitor
                )

                if success:
                    logging.info("Deployment refresh listener started as PRIMARY source of truth for configuration updates")
                else:
                    logging.warning("Failed to start deployment refresh listener, relying on event listener and polling")
            except Exception as e:
                logging.error(f"Error starting deployment refresh listener: {str(e)}")
                # Don't raise - refresh listener is complementary to other mechanisms

        except Exception as e:
            logging.error(f"Failed to start camera config monitor: {str(e)}")
            # Don't raise - monitor is optional

    def _start_proxy_interface(self):
        """Start the proxy interface component."""
        logging.info(
            "Starting proxy interface on external port: %d",
            self.external_port,
        )

        self.proxy_interface = MatriceProxyInterface(
            session=self.session,
            deployment_id=self.deployment_id,
            deployment_instance_id=self.deployment_instance_id,
            external_port=self.external_port,
            inference_interface=self.inference_interface,
        )

        self.proxy_interface.start()
        logging.info("Proxy interface started successfully")

    def start_server(self, block=True):
        """Start the server and related components.

        Args:
            block: If True, wait for shutdown signal. If False, return immediately after starting.

        Raises:
            Exception: If unable to initialize server
        """
        self.start(block=block)

    def stop_server(self):
        """Stop the server and related components."""
        try:
            logging.info("Initiating server shutdown...")

            # Signal shutdown to all components
            self._shutdown_event.set()

            # Stop refresh listener
            if self.app_deployment:
                try:
                    self.app_deployment.stop_refresh_listener()
                    logging.info("Deployment refresh listener stopped")
                except Exception as exc:
                    logging.error("Error stopping refresh listener: %s", str(exc))

            # Stop app event listener
            if self.app_deployment:
                try:
                    self.app_deployment.stop_event_listener()
                    logging.info("App event listener stopped")
                except Exception as exc:
                    logging.error("Error stopping app event listener: %s", str(exc))

            # Stop camera config monitor
            if self.camera_config_monitor:
                try:
                    self.camera_config_monitor.stop()
                    logging.info("Camera config monitor stopped")
                except Exception as exc:
                    logging.error("Error stopping camera config monitor: %s", str(exc))

            # Stop CUDA SHM analytics publisher if running
            if hasattr(self, '_cuda_shm_analytics_publisher') and self._cuda_shm_analytics_publisher:
                try:
                    self._cuda_shm_analytics_publisher.stop()
                    logging.info("CUDA SHM analytics publisher stopped")
                except Exception as exc:
                    logging.error("Error stopping CUDA SHM analytics publisher: %s", str(exc))

            # Stop CUDA SHM engine if running (operates independently)
            if self.cuda_shm_engine:
                try:
                    self.cuda_shm_engine.stop()
                    logging.info("CUDA SHM inference engine stopped")
                except Exception as exc:
                    logging.error("Error stopping CUDA SHM engine: %s", str(exc))

            # Stop streaming pipeline
            if self.streaming_pipeline:
                try:
                    # Stop the pipeline (now manages its own event loop thread)
                    self.streaming_pipeline.stop()
                    logging.info("Streaming pipeline stopped")
                except Exception as exc:
                    logging.error("Error stopping streaming pipeline: %s", str(exc))
            
            # Wait for stream manager thread to finish
            if self._stream_manager_thread and self._stream_manager_thread.is_alive():
                logging.info("Waiting for stream manager thread to stop...")
                try:
                    self._stream_manager_thread.join(timeout=10.0)
                    if self._stream_manager_thread.is_alive():
                        logging.warning("Stream manager thread did not stop within timeout")
                    else:
                        logging.info("Stream manager thread stopped successfully")
                except Exception as exc:
                    logging.error("Error waiting for stream manager thread: %s", str(exc))

            # Stop proxy interface
            if self.proxy_interface:
                try:
                    self.proxy_interface.stop()
                    logging.info("Proxy interface stopped")
                except Exception as exc:
                    logging.error("Error stopping proxy interface: %s", str(exc))

            logging.info("Server shutdown completed")

        except Exception as exc:
            logging.error("Error during server shutdown: %s", str(exc))
            raise


class MatriceDeployServerUtils:
    """Utility class for managing deployment server operations."""

    def __init__(
        self,
        action_tracker: ActionTracker,
        inference_interface: InferenceInterface,
        external_port: int,
        main_server: 'MatriceDeployServer' = None,
    ):
        """Initialize utils with reference to the main server.

        Args:
            action_tracker: ActionTracker instance
            inference_interface: InferenceInterface instance
            external_port: External port number
            main_server: Reference to the main MatriceDeployServer instance
        """
        self.action_tracker = action_tracker
        self.session = self.action_tracker.session
        self.rpc = self.session.rpc
        self.action_details = self.action_tracker.action_details
        self.deployment_instance_id = self.action_details["_idModelDeployInstance"]
        self.deployment_id = self.action_details["_idDeployment"]
        self.model_id = self.action_details["_idModelDeploy"]
        self.shutdown_threshold = (
            int(self.action_details.get("shutdownThreshold", 15)) * 60
        )
        self.auto_shutdown = self.action_details.get("autoShutdown", True)
        self.inference_interface = inference_interface
        self.external_port = external_port
        self.main_server = main_server
        self._ip = None
        self._ip_fetch_attempts = 0
        self._max_ip_fetch_attempts = MAX_IP_FETCH_ATTEMPTS
        
        # Shutdown coordination
        self._shutdown_initiated = threading.Event()
        self._shutdown_complete = threading.Event()

    @property
    def ip(self):
        """Get the external IP address with caching and retry logic."""
        if self._ip is None and self._ip_fetch_attempts < self._max_ip_fetch_attempts:
            self._ip_fetch_attempts += 1
            try:
                with urllib.request.urlopen(
                    "https://v4.ident.me", timeout=IP_FETCH_TIMEOUT_SECONDS
                ) as response:
                    self._ip = response.read().decode("utf8").strip()
                    logging.info("Successfully fetched external IP: %s", self._ip)
            except Exception as exc:
                logging.warning(
                    "Failed to fetch external IP (attempt %d/%d): %s",
                    self._ip_fetch_attempts,
                    self._max_ip_fetch_attempts,
                    str(exc),
                )
                if self._ip_fetch_attempts >= self._max_ip_fetch_attempts:
                    # Fallback to localhost for local development
                    self._ip = "localhost"
                    logging.warning("Using localhost as fallback IP address")

        return self._ip or "localhost"

    def is_instance_running(self):
        """Check if deployment instance is running.

        Returns:
            bool: True if instance is running, False otherwise
        """
        try:
            resp = self.rpc.get(
                f"/v1/inference/get_deployment_without_auth_key/{self.deployment_id}",
                raise_exception=False,
            )
            if not resp:
                logging.warning("No response received when checking instance status")
                return False

            if not resp.get("success"):
                error_msg = resp.get("message", "Unknown error")
                logging.warning(
                    "Failed to get deployment instance status: %s", error_msg
                )
                return False

            running_instances = resp.get("data", {}).get("runningInstances", [])
            if not running_instances:
                logging.warning("No running instances found")
                return False

            for instance in running_instances:
                if instance.get("modelDeployInstanceId") == self.deployment_instance_id:
                    is_deployed = instance.get("deployed", False)
                    logging.debug(
                        "Instance %s deployment status: %s",
                        self.deployment_instance_id,
                        "deployed" if is_deployed else "not deployed",
                    )
                    if not is_deployed:
                        logging.warning("Instance %s is not deployed", self.deployment_instance_id)
                    return is_deployed

            logging.warning(
                "Instance %s not found in running instances list",
                self.deployment_instance_id,
            )
            return False

        except Exception as exc:
            logging.warning(
                "Exception checking deployment instance status: %s",
                str(exc),
            )
            return False

    def get_elapsed_time_since_latest_inference(self):
        """Get time elapsed since latest inference.

        Returns:
            float: Elapsed time in seconds

        Raises:
            Exception: If unable to get elapsed time and no fallback available
        """
        now = datetime.now(timezone.utc)

        # Handle CUDA SHM mode where inference_interface may be None
        if self.inference_interface is None:
            # In CUDA SHM mode, inference is handled by the engine directly
            # Return 0 to prevent auto-shutdown (engine is always "active")
            logging.debug("CUDA SHM mode: inference_interface is None, returning 0 elapsed time")
            return 0.0

        if self.inference_interface.get_latest_inference_time():
            elapsed_time = (
                now - self.inference_interface.get_latest_inference_time()
            ).total_seconds()
            logging.debug(
                "Using latest inference time for elapsed calculation: %.1fs",
                elapsed_time,
            )
            return elapsed_time

        # Final fallback: return a safe default
        logging.warning(
            "No latest inference time available, using safe default of 0 seconds"
        )
        return 0.0

    def trigger_shutdown_if_needed(self):
        """Check idle time and trigger shutdown if threshold exceeded."""
        try:
            # Check if auto shutdown is enabled
            if not self.auto_shutdown:
                logging.debug("Auto shutdown is disabled")
                return

            # Check elapsed time
            elapsed_time = self.get_elapsed_time_since_latest_inference()

            if elapsed_time > self.shutdown_threshold:
                logging.info(
                    "Idle time (%.1fs) exceeded threshold (%.1fs), initiating shutdown",
                    elapsed_time,
                    self.shutdown_threshold,
                )
                self.shutdown()
            else:
                time_until_shutdown = max(0, self.shutdown_threshold - elapsed_time)
                # Only log every 10 minutes to reduce noise
                if int(elapsed_time) % 600 == 0 or elapsed_time < 60:
                    logging.info(
                        "Time since last inference: %.1fs, time until shutdown: %.1fs",
                        elapsed_time,
                        time_until_shutdown,
                    )

        except Exception as exc:
            logging.error(
                "Error checking shutdown condition: %s",
                str(exc),
            )

    def shutdown(self):
        """Gracefully shutdown the deployment instance."""
        try:
            logging.warning("Initiating shutdown sequence...")

            # Notify backend of shutdown
            try:
                # resp = self.rpc.delete( # TODO: Enable after fixing shutdown and remove return None
                #     f"/v1/inference/delete_deploy_instance/{self.deployment_instance_id}",
                #     raise_exception=False,
                # )
                # if resp and resp.get("success"):
                #     logging.warning(
                #         "Successfully notified backend of deployment instance shutdown"
                #     )
                # else:
                #     error_msg = (
                #         resp.get("message", "Unknown error") if resp else "No response"
                #     )
                #     logging.warning(
                #         "Failed to notify backend of shutdown: %s", error_msg
                #     )
                logging.warning("Shutdown is triggered, but notifying backend is disabled")
                return None
            except Exception as exc:
                logging.error(
                    "Exception while notifying backend of shutdown: %s", str(exc)
                )

            # Update status
            try:
                self.action_tracker.update_status(
                    "MDL_DPL_STP",
                    "SUCCESS",
                    "Model deployment stopped",
                )
                logging.warning("Updated deployment status to stopped")
            except Exception as exc:
                logging.error("Failed to update deployment status: %s", str(exc))

            # Signal shutdown initiation instead of direct exit
            logging.warning("Signaling shutdown to main thread...")
            self._shutdown_initiated.set()
            
            # Wait for coordinated shutdown to complete or timeout
            if self._shutdown_complete.wait(timeout=30.0):
                logging.warning("Coordinated shutdown completed, exiting process")
            else:
                logging.warning("Coordinated shutdown timed out, forcing exit")
            
            # Final exit
            os._exit(0)

        except Exception as exc:
            logging.error("Error during shutdown: %s", str(exc))
            # Signal shutdown even on error
            self._shutdown_initiated.set()
            os._exit(1)

    def shutdown_checker(self):
        """Background thread to periodically check for idle shutdown condition and deployment status."""
        consecutive_deployment_failures = 0
        logging.warning("Shutdown checker started")

        while True:
            try:
                # Check if deployment instance is still running
                is_running = self.is_instance_running()

                if is_running:
                    # Reset failure counter if deployment check succeeds
                    if consecutive_deployment_failures > 0:
                        logging.info(
                            "Deployment status check recovered after %d failures",
                            consecutive_deployment_failures,
                        )
                        consecutive_deployment_failures = 0

                    # Check for idle shutdown condition
                    self.trigger_shutdown_if_needed()
                else:
                    consecutive_deployment_failures += 1
                    failure_duration_minutes = (
                        consecutive_deployment_failures
                        * SHUTDOWN_CHECK_INTERVAL_SECONDS
                    ) / 60

                    logging.warning(
                        "Deployment status check failed (%d/%d) - %.1f minutes of failures",
                        consecutive_deployment_failures,
                        MAX_DEPLOYMENT_CHECK_FAILURES_BEFORE_SHUTDOWN,
                        failure_duration_minutes,
                    )

                    if (
                        consecutive_deployment_failures
                        >= MAX_DEPLOYMENT_CHECK_FAILURES_BEFORE_SHUTDOWN
                    ):
                        logging.error(
                            "Deployment status check failed %d consecutive times (%.1f minutes), initiating shutdown",
                            consecutive_deployment_failures,
                            failure_duration_minutes,
                        )
                        self.shutdown()
                        return

            except Exception as exc:
                consecutive_deployment_failures += 1
                failure_duration_minutes = (
                    consecutive_deployment_failures * SHUTDOWN_CHECK_INTERVAL_SECONDS
                ) / 60

                logging.error(
                    "Error in shutdown checker (%d/%d) - %.1f minutes of failures: %s",
                    consecutive_deployment_failures,
                    MAX_DEPLOYMENT_CHECK_FAILURES_BEFORE_SHUTDOWN,
                    failure_duration_minutes,
                    str(exc),
                )

                if (
                    consecutive_deployment_failures
                    >= MAX_DEPLOYMENT_CHECK_FAILURES_BEFORE_SHUTDOWN
                ):
                    logging.error(
                        "Shutdown checker failed %d consecutive times (%.1f minutes), initiating shutdown",
                        consecutive_deployment_failures,
                        failure_duration_minutes,
                    )
                    self.shutdown()
                    return
            finally:
                time.sleep(SHUTDOWN_CHECK_INTERVAL_SECONDS)

    def heartbeat_checker(self):
        """Background thread to periodically send heartbeat."""
        consecutive_failures = 0

        logging.info("Heartbeat checker started")
        while True:
            try:
                resp = self.rpc.post(
                    f"/v1/inference/add_instance_heartbeat/{self.deployment_instance_id}",
                    raise_exception=False,
                )

                if resp and resp.get("success"):
                    if consecutive_failures > 0:
                        logging.info(
                            "Heartbeat recovered after %d failures: %s",
                            consecutive_failures,
                            resp.get("message", "Success"),
                        )
                    else:
                        logging.debug(
                            "Heartbeat successful: %s", resp.get("message", "Success")
                        )
                    consecutive_failures = 0
                else:
                    consecutive_failures += 1
                    error_msg = (
                        resp.get("message", "Unknown error") if resp else "No response"
                    )
                    failure_duration_minutes = (
                        consecutive_failures * HEARTBEAT_INTERVAL_SECONDS
                    ) / 60

                    logging.warning(
                        "Heartbeat failed (%d/%d) - %.1f minutes of failures: %s",
                        consecutive_failures,
                        MAX_HEARTBEAT_FAILURES_BEFORE_SHUTDOWN,
                        failure_duration_minutes,
                        error_msg,
                    )

                    if consecutive_failures >= MAX_HEARTBEAT_FAILURES_BEFORE_SHUTDOWN:
                        logging.error(
                            "Heartbeat failed %d consecutive times (%.1f minutes), initiating shutdown",
                            consecutive_failures,
                            failure_duration_minutes,
                        )
                        self.shutdown()
                        return

            except Exception as exc:
                consecutive_failures += 1
                failure_duration_minutes = (
                    consecutive_failures * HEARTBEAT_INTERVAL_SECONDS
                ) / 60

                logging.warning(
                    "Heartbeat exception (%d/%d) - %.1f minutes of failures: %s",
                    consecutive_failures,
                    MAX_HEARTBEAT_FAILURES_BEFORE_SHUTDOWN,
                    failure_duration_minutes,
                    str(exc),
                )

                if consecutive_failures >= MAX_HEARTBEAT_FAILURES_BEFORE_SHUTDOWN:
                    logging.error(
                        "Heartbeat failed %d consecutive times (%.1f minutes), initiating shutdown",
                        consecutive_failures,
                        failure_duration_minutes,
                    )
                    self.shutdown()
                    return

            time.sleep(HEARTBEAT_INTERVAL_SECONDS)

    def run_background_checkers(self):
        """Start the shutdown checker and heartbeat checker threads as daemons."""
        shutdown_thread = threading.Thread(
            target=self.shutdown_checker,
            name="ShutdownChecker",
            daemon=False,
        )
        heartbeat_thread = threading.Thread(
            target=self.heartbeat_checker,
            name="HeartbeatChecker",
            daemon=False,
        )

        shutdown_thread.start()
        heartbeat_thread.start()

        logging.info("Background checker threads started successfully")

    def wait_for_shutdown(self):
        """Wait for shutdown to be initiated by background checkers or external signals.
        
        This method blocks the main thread until shutdown is triggered.
        """
        try:
            logging.warning("Main thread waiting for shutdown signal...")
            
            # Wait for shutdown to be initiated
            while not self._shutdown_initiated.is_set():
                time.sleep(10)
            
            logging.warning("Shutdown signal received, initiating server shutdown...")
            
            # Trigger coordinated shutdown # TODO: Enable after fixing shutdown
            # if self.main_server:
            #     try:
            #         self.main_server.stop_server()
            #         logging.warning("Server shutdown completed")
            #     except Exception as exc:
            #         logging.error("Error during server shutdown: %s", str(exc))
            
            # # Signal that shutdown is complete
            # self._shutdown_complete.set()
            
        except KeyboardInterrupt:
            logging.warning("Received KeyboardInterrupt, initiating shutdown...")
            self._shutdown_initiated.set()
            if self.main_server:
                try:
                    self.main_server.stop_server()
                except Exception as exc:
                    logging.error("Error during keyboard interrupt shutdown: %s", str(exc))
            self._shutdown_complete.set()
        except Exception as exc:
            logging.error("Error in wait_for_shutdown: %s", str(exc))
            self._shutdown_initiated.set()
            if self.main_server:
                try:
                    self.main_server.stop_server()
                except Exception as exc:
                    logging.error("Error during exception shutdown: %s", str(exc))
            self._shutdown_complete.set()

    def update_deployment_address(self):
        """Update the deployment address in the backend.

        Raises:
            Exception: If unable to update deployment address
        """
        try:
            # Get IP address (with fallback to localhost)
            ip_address = self.ip
            logging.info(f"Using IP address: {ip_address}")

            # Validate external port
            if not (1 <= self.external_port <= 65535):
                raise ValueError(f"Invalid external port: {self.external_port}")

            instance_id = self.action_details.get("instanceID")
            if not instance_id:
                raise ValueError("Missing instanceID in action details")

            payload = {
                "port": int(self.external_port),
                "ipAddress": ip_address,
                "_idDeploymentInstance": self.deployment_instance_id,
                "_idModelDeploy": self.deployment_id,
                "_idInstance": instance_id,
            }

            logging.info(f"Updating deployment address with payload: {payload}")

            resp = self.rpc.put(
                path="/v1/inference/update_deploy_instance_address",
                payload=payload
            )
            logging.info(
                "Successfully updated deployment address to %s:%s, response: %s",
                ip_address,
                self.external_port,
                resp,
            )
        except Exception as exc:
            logging.error(
                "Failed to update deployment address: %s",
                str(exc),
            )
            raise
