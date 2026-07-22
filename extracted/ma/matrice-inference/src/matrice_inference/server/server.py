"""Module providing server functionality."""

import asyncio
import atexit
import logging
import os
import signal
import threading
import time
import urllib.request
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Optional

from matrice.action_tracker import ActionTracker
from matrice_analytics.post_processing.post_processor import PostProcessor

from matrice_inference.server.inference_interface import InferenceInterface
from matrice_inference.server.model.model_manager_wrapper import ModelManagerWrapper
from matrice_inference.server.proxy_interface import MatriceProxyInterface
from matrice_inference.server.stream.camera_config_manager import CameraConfigManager
from matrice_inference.server.stream.stream_pipeline import StreamingPipeline
from matrice_inference.server.stream.utils import redact_sensitive

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
        preprocess_params: Optional[Dict[str, Any]] = None,
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
                load_model,
                predict,
                action_id,
                external_port,
                preprocess_fn,
                postprocess_fn,
                async_predict,
                async_batch_predict,
                async_load_model,
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
            self.server_type = self.action_details.get("server_type", "fastapi")
            self.app_id = self.job_params.get("application_id", "")
            self.app_name = self.job_params.get("application_name", "")
            self.app_version = self.job_params.get("application_version", "")

            # Redact secrets and presigned-URL query tokens before logging:
            # action_details may carry checkpoint_value presigned URLs and other
            # sensitive deployment config (see redact_sensitive in stream.utils).
            logging.info("Action details: %s", redact_sensitive(self.action_details))

            # Extract deployment information
            self.deployment_instance_id = self.action_details.get("_idModelDeployInstance")
            self.deployment_id = self.action_details.get("_idDeployment")
            self.model_id = self.action_details.get("_idModelDeploy")
            self.inference_pipeline_id = self.action_details.get("inference_pipeline_id")
            # _idComputeInstance lives on the outer action record, not inside actionDetails
            action_doc = self.action_tracker.action_doc
            self.instance_id = action_doc.get("_idComputeInstance")
            self.instance_string_id = (
                action_doc.get("instanceID") or self.action_details.get("instanceID") or self.instance_id
            )
            logging.info(
                "Instance IDs: _idComputeInstance=%s, instanceID=%s, instance_string_id=%s",
                self.instance_id,
                action_doc.get("instanceID"),
                self.instance_string_id,
            )
            if not self.instance_id:
                logging.error(
                    "CRITICAL: _idComputeInstance is None on the outer action record. "
                    "Camera loading via get_consuming_topics_by_instance will fail. "
                    "Ensure backend sends _idComputeInstance in action details. "
                    "action_doc top-level keys: %s",
                    list(action_doc.keys()) if action_doc else "action_doc is None/empty",
                )
                # Log all ID-like fields from action_doc for debugging
                id_fields = {
                    k: v for k, v in (action_doc or {}).items() if "id" in k.lower() or "instance" in k.lower()
                }
                logging.error("action_doc ID-related fields: %s", id_fields)

            # Validate deployment information
            if not all([self.deployment_instance_id, self.deployment_id, self.model_id]):
                raise ValueError("Missing required deployment identifiers in action details")

            # Set shutdown configuration
            shutdown_threshold_minutes = int(
                self.action_details.get("shutdownThreshold", DEFAULT_SHUTDOWN_THRESHOLD_MINUTES)
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
                    pickle.dumps(self.load_model)  # nosemgrep: python.lang.security.deserialization.pickle.avoid-pickle
                    logging.info("✓ load_model is picklable")
                except Exception as e:
                    logging.exception(f"✗ load_model is NOT picklable: {e}")

                try:
                    pickle.dumps(self.predict)  # nosemgrep: python.lang.security.deserialization.pickle.avoid-pickle
                    logging.info("✓ predict is picklable")
                except Exception as e:
                    logging.exception(f"✗ predict is NOT picklable: {e}")

            # TMM required args
            self.model_path = model_path
            self.runtime_framework = runtime_framework
            self.use_dynamic_batching = use_dynamic_batching

            logging.info(
                "Model path: %s, Runtime framework: %s passed to MDS",
                model_path,
                runtime_framework,
            )

            # TMM non-mandatory args
            self.num_classes = num_classes
            self.max_batch_size = max_batch_size
            self.use_trt_accelerator = use_trt_accelerator
            self.input_size = input_size

            logging.info(
                "Num classes: %s, Input size: %s, Max batch size: %s, Use TRT accelerator: %s passed to MDS",
                num_classes,
                input_size,
                max_batch_size,
                use_trt_accelerator,
            )

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
            self.camera_config_manager = None
            self.stream_manager = None

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
            logging.exception("Failed to initialize MatriceDeployServer: %s", str(exc))
            raise

    def _register_shutdown_handlers(self):
        """Register signal handlers and atexit callback for graceful shutdown."""

        def signal_handler(signum, frame):
            logging.info("Received signal %d, triggering shutdown through utils...", signum)
            try:
                # Use utils shutdown to trigger coordinated shutdown
                if hasattr(self, "utils") and self.utils:
                    self.utils._shutdown_initiated.set()
                else:
                    # Fallback to direct shutdown if utils not available
                    self.stop_server()
                    os._exit(0)
            except Exception as exc:
                logging.exception("Error during signal-triggered shutdown: %s", str(exc))
                os._exit(1)

        def atexit_handler():
            logging.info("Process exiting, ensuring graceful shutdown...")
            try:
                if not self._shutdown_event.is_set():
                    if hasattr(self, "utils") and self.utils and not self.utils._shutdown_initiated.is_set():
                        self.utils._shutdown_initiated.set()
                    else:
                        self.stop_server()
            except Exception as exc:
                logging.exception("Error during atexit shutdown: %s", str(exc))

        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        # Register atexit handler as a final safety net
        atexit.register(atexit_handler)

        logging.info("Shutdown handlers registered successfully")

    def _validate_init_parameters(
        self,
        load_model,
        predict,
        action_id,
        external_port,
        preprocess_fn,
        postprocess_fn,
        async_predict,
        async_batch_predict,
        async_load_model,
    ):
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

        # Validate action_id
        if not isinstance(action_id, str):
            raise ValueError("action_id must be a string")

        external_port = int(external_port)
        # Validate external_port
        if not isinstance(external_port, int):
            raise ValueError("external_port must be an integer")
        if not (1 <= external_port <= 65535):
            raise ValueError(f"Invalid external port: {external_port}. Must be between 1 and 65535")
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

                # Allow some time for model manager to be fully ready [TritonMM to reach ]
                # NOTE : Might need to update based on model load and latency milestone constraint (in future)
                time.sleep(15)

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
            logging.exception("Failed to start server components: %s", str(exc))
            self.action_tracker.update_status(
                "ERROR",
                "ERROR",
                f"Model deployment error: {exc!s}",
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
        missing_details = [key for key in required_details if not self.action_details.get(key)]
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

        server_type_list = self.server_type.lower().split("_")
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
            post_processing_config["facial_recognition_server_id"] = self.job_params.get(
                "facial_recognition_server_id", None
            )
            post_processing_config["lpr_server_id"] = self.job_params.get("lpr_server_id", None)
            post_processing_config["session"] = self.session  # Pass the session to post-processing
            # Pass deployment_id for facial recognition deployment update
            post_processing_config["deployment_id"] = self.deployment_id

        # Get index_to_category from action_tracker if available
        index_to_category = None
        target_categories = None
        try:
            if hasattr(self.action_tracker, "get_index_to_category"):
                index_to_category = self.action_tracker.get_index_to_category(
                    getattr(self.action_tracker, "is_exported", True)
                )
        except Exception as e:
            logging.warning(f"Failed to get index_to_category from action_tracker: {e!s}")

        # Store post-processing config for passing to CUDA SHM engine
        self._post_processing_config = post_processing_config
        self._index_to_category = index_to_category
        self._target_categories = target_categories

        # Pass config to CUDA SHM engine if available
        if self.cuda_shm_engine:
            # Pass the action tracker's downloaded checkpoint path and presigned URL
            # so the engine's fallback chain can use the custom model instead of
            # falling back to the default COCO pretrained engine.
            checkpoint_path = getattr(self.action_tracker, "checkpoint_path", None)
            checkpoint_url = self.action_details.get("checkpoint_value", "")
            checkpoint_presigned_url = (
                checkpoint_url
                if checkpoint_url and isinstance(checkpoint_url, str) and "http" in checkpoint_url
                else None
            )
            self.cuda_shm_engine.set_post_processing_config(
                post_processing_config=post_processing_config,
                app_name=self.app_name,
                index_to_category=index_to_category,
                target_categories=target_categories,
                checkpoint_path=checkpoint_path,
                checkpoint_presigned_url=checkpoint_presigned_url,
            )
            logging.info(
                f"Post-processing config passed to CUDA SHM engine: app_name={self.app_name}, "
                f"checkpoint_path={checkpoint_path}, has_presigned_url={checkpoint_presigned_url is not None}"
            )

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
            post_processing_config["facial_recognition_server_id"] = self.job_params.get(
                "facial_recognition_server_id", None
            )
            post_processing_config["lpr_server_id"] = self.job_params.get("lpr_server_id", None)
            post_processing_config["session"] = self.session  # Pass the session to post-processing
            # Pass deployment_id for facial recognition deployment update
            post_processing_config["deployment_id"] = self.deployment_id

        # Get index_to_category from action_tracker if available
        index_to_category = None
        target_categories = None
        try:
            if hasattr(self.action_tracker, "get_index_to_category"):
                index_to_category = self.action_tracker.get_index_to_category(
                    getattr(self.action_tracker, "is_exported", True)
                )
        except Exception as e:
            logging.warning(f"Failed to get index_to_category from action_tracker: {e!s}")

        # Store post-processing config for passing to StreamingPipeline (as dict, not extracted from post_processor)
        self._post_processing_config = post_processing_config
        self._index_to_category = index_to_category
        self._target_categories = target_categories

        # Create PostProcessor
        self.post_processor = PostProcessor(
            post_processing_config=post_processing_config,
            app_name=self.app_name,
            index_to_category=index_to_category,
            target_categories=target_categories,
        )

        # Create InferenceInterface with simplified parameters
        self.inference_interface = InferenceInterface(
            model_manager_wrapper=self.model_manager, post_processor=self.post_processor
        )

        logging.info("Inference interface and post-processor initialized successfully")

    def _initialize_cuda_shm_engine(self):
        """Initialize CUDA SHM engine with camera configs (no streaming pipeline needed)."""
        try:
            logging.info("Initializing CUDA SHM engine...")

            app_deployment_id = self.action_details.get(
                "app_deployment_id", self.job_params.get("app_deployment_id", None)
            )
            if not app_deployment_id:
                logging.warning("No app_deployment_id found, CUDA SHM engine will start with no cameras")
                self.cuda_shm_engine.start()
                return

            if not self.instance_id:
                logging.error(
                    "CUDA SHM: instance_id is None — "
                    "get_consuming_topics_by_instance will return empty, "
                    "no cameras will be loaded. "
                    "Verify _idComputeInstance is present in action record."
                )

            # Create CameraConfigManager (owns API, refresh listener, heartbeat)
            self.camera_config_manager = CameraConfigManager(
                session=self.session,
                app_deployment_id=app_deployment_id,
                instance_id=self.instance_id,
                deployment_instance_id=self.deployment_instance_id,
                instance_string_id=self.instance_string_id,
                action_id=self.action_id,
                connection_timeout=self.job_params.get("stream_connection_timeout", 1200),
                heartbeat_interval=self.job_params.get("app_deployment_heartbeat_interval", 30),
                auto_refresh_interval=self.job_params.get("auto_refresh_interval", 300.0),
                on_config_changed=lambda new_configs: self._on_cuda_shm_config_changed(new_configs, app_deployment_id),
            )

            # Initial camera load
            logging.info("CUDA SHM mode: Loading all cameras synchronously from API...")
            camera_configs = self.camera_config_manager.get_camera_configs()
            self.camera_config_manager.camera_configs = camera_configs or {}

            converted_configs = {}
            if camera_configs:
                logging.info(f"CUDA SHM mode: Loaded {len(camera_configs)} cameras")
                converted_configs = CameraConfigManager.convert_configs_for_engine(
                    camera_configs, app_deployment_id, self.app_id
                )
                self.cuda_shm_engine.set_camera_configs(converted_configs)
            else:
                logging.warning(
                    "CUDA SHM mode: No cameras found from API. "
                    "Check that instance_id=%s is valid and has consuming topics assigned.",
                    self.instance_id,
                )

            # Initialize AnalyticsPublisher for results-agg publishing
            # Pass raw CameraConfig objects (not engine-converted dicts) so
            # _build_analytics_message can access .stream_config attribute
            self._initialize_cuda_shm_analytics_publisher(
                camera_configs=camera_configs or {},
                app_deployment_id=app_deployment_id,
            )

            # Start engine
            logging.info("CUDA SHM mode: Starting engine...")
            self.cuda_shm_engine.start()
            logging.info("CUDA SHM mode: Engine started successfully")

            # Start refresh + heartbeat (Kafka events + periodic)
            self.camera_config_manager.start()

        except Exception as e:
            logging.exception(f"Failed to initialize CUDA SHM engine: {e}")
            raise

    def _on_cuda_shm_config_changed(self, new_configs, app_deployment_id):
        """Handle camera config changes for CUDA SHM mode.

        Prefer an incremental reconcile (add/remove only the changed cameras on
        live workers — no inference gap for the rest). Fall back to a full engine
        stop+restart only if the engine isn't running yet or the reconcile fails.
        """
        try:
            converted = CameraConfigManager.convert_configs_for_engine(new_configs, app_deployment_id, self.app_id)

            reconciled = False
            engine = self.cuda_shm_engine
            if getattr(engine, "running", False) and hasattr(engine, "reconcile_camera_configs"):
                result = engine.reconcile_camera_configs(converted)
                if result.get("success"):
                    reconciled = True
                    logging.info(
                        "CUDA SHM config change: reconciled incrementally (+%d, -%d, total=%d)",
                        result.get("added", 0),
                        result.get("removed", 0),
                        result.get("total_cameras", len(converted)),
                    )
                else:
                    logging.warning(
                        "CUDA SHM config change: incremental reconcile failed (%s); "
                        "falling back to full engine restart",
                        result.get("reason", "unknown"),
                    )

            if not reconciled:
                logging.info(
                    "CUDA SHM config change: restarting engine with %d cameras",
                    len(converted),
                )
                engine.stop()
                engine.set_camera_configs(converted)
                engine._init_started = False
                engine.start()
                logging.info("CUDA SHM config change: engine restarted successfully")

            # Update analytics publisher with fresh CameraConfig objects
            if hasattr(self, "_cuda_shm_analytics_publisher") and self._cuda_shm_analytics_publisher:
                self._cuda_shm_analytics_publisher.update_camera_configs(new_configs)
                logging.info(
                    "CUDA SHM config change: updated analytics publisher with %d cameras",
                    len(new_configs),
                )
        except Exception as e:
            logging.exception(f"Failed to apply config change to CUDA SHM engine: {e}")

    def _initialize_cuda_shm_analytics_publisher(self, camera_configs, app_deployment_id):
        """Deprecated no-op: analytics/results-agg publishing for CUDA-SHM is now
        owned end-to-end by the ml-codebases deployment script (``deploy.py``),
        which builds a single ``matrice_analytics`` ``AnalyticsPublisher`` fed by
        the engine's per-worker queues. The SDK must NOT build a second, competing
        results-agg writer here (it caused the two-publisher race). Kept as a no-op
        so the cuda-shm init path and any callers stay intact.

        Note: the per-worker feed (``set_analytics_queue`` on this engine) is a
        no-op anyway, so this SDK publisher was starved; removing it loses nothing.
        """
        logging.info("Skipping SDK cuda-shm AnalyticsPublisher: ml-codebases deploy.py owns results-agg publishing now")

    def _initialize_cuda_shm_analytics_publisher_legacy(self, camera_configs, app_deployment_id):
        """Retained for reference only; no longer called. See the no-op above."""
        import multiprocessing as mp

        try:
            from matrice_inference.server.stream.analytics_publisher import (
                AnalyticsPublisher,
            )
        except ImportError:
            logging.warning("AnalyticsPublisher not available, results-agg will not be published")
            return

        try:
            # Get Redis config from instance API (authoritative source with Sentinel)
            redis_host = "localhost"
            redis_port = 6379
            redis_password = None
            redis_username = None
            sentinel_hosts = None
            master_name = None

            if hasattr(self, "camera_config_manager") and self.camera_config_manager:
                try:
                    conn = self.camera_config_manager.get_redis_connection_by_instance()
                    if conn:
                        redis_host = conn.get("host", "localhost")
                        redis_port = int(conn.get("port", 6379))
                        redis_password = conn.get("password")
                        redis_username = conn.get("username")
                        sentinel_hosts = conn.get("sentinel_hosts")
                        master_name = conn.get("master_name")
                        logging.info(
                            "AnalyticsPublisher Redis config from API: host=%s, port=%d, sentinel=%s, master=%s",
                            redis_host,
                            redis_port,
                            f"yes ({len(sentinel_hosts)} nodes)" if sentinel_hosts else "no",
                            master_name or "N/A",
                        )
                    else:
                        logging.error(
                            "AnalyticsPublisher: get_redis_connection_by_instance() returned None — "
                            "analytics will be unavailable until Redis config is available"
                        )
                except Exception as e:
                    logging.exception("AnalyticsPublisher: Failed to get Redis config from API: %s", e)
            else:
                logging.error("AnalyticsPublisher: No camera_config_manager available — analytics will be unavailable")

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
                sentinel_hosts=sentinel_hosts,
                master_name=master_name,
            )
            self._cuda_shm_analytics_publisher = analytics_publisher
            self._cuda_shm_analytics_mp_queue = analytics_mp_queue

            # Provide API-based config refresh for retry scenarios
            if hasattr(self, "camera_config_manager") and self.camera_config_manager:
                analytics_publisher.set_redis_config_provider(
                    self.camera_config_manager.get_redis_connection_by_instance
                )

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

            sentinel_info = f", sentinel=yes, master={master_name}" if sentinel_hosts else ", sentinel=no"
            logging.info(
                f"CUDA SHM mode: AnalyticsPublisher started "
                f"(redis={redis_host}:{redis_port}{sentinel_info}, app_name={self.app_name})"
            )
        except Exception as e:
            logging.warning(f"Failed to start AnalyticsPublisher for CUDA SHM mode (non-fatal): {e}")

    def _initialize_streaming_pipeline(self):
        """Initialize the streaming pipeline component."""
        try:
            logging.info("Initializing streaming pipeline...")

            app_deployment_id = self.action_details.get(
                "app_deployment_id", self.job_params.get("app_deployment_id", None)
            )

            # Normal mode: start with no cameras, rely on refresh events
            camera_configs = {}
            if app_deployment_id:
                # Create CameraConfigManager (owns API, refresh listener, heartbeat)
                self.camera_config_manager = CameraConfigManager(
                    session=self.session,
                    app_deployment_id=app_deployment_id,
                    instance_id=self.instance_id,
                    deployment_instance_id=self.deployment_instance_id,
                    instance_string_id=self.instance_string_id,
                    action_id=self.action_id,
                    connection_timeout=self.job_params.get("stream_connection_timeout", 1200),
                    heartbeat_interval=self.job_params.get("app_deployment_heartbeat_interval", 30),
                    auto_refresh_interval=self.job_params.get("auto_refresh_interval", 300.0),
                    on_config_changed=self._on_pipeline_config_changed,
                )
                logging.info(
                    "Skipping initial camera fetch - system will wait for refresh events to provide camera configurations. "
                    "This avoids Redis authentication issues and improves startup performance."
                )
            else:
                logging.warning("No app_deployment_id found in job_params, starting pipeline without cameras")

            # Create streaming pipeline with configured parameters
            self.streaming_pipeline = StreamingPipeline(
                inference_interface=self.inference_interface,
                inference_queue_maxsize=self.job_params.get("inference_queue_maxsize", 5000),
                postproc_queue_maxsize=self.job_params.get("postproc_queue_maxsize", 5000),
                output_queue_maxsize=self.job_params.get("output_queue_maxsize", 5000),
                message_timeout=self.job_params.get("message_timeout", 2.0),
                inference_timeout=self.job_params.get("inference_timeout", 60.0),
                shutdown_timeout=self.job_params.get("shutdown_timeout", 60.0),
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
                use_shared_metrics=self.job_params.get("use_shared_metrics", True),
                load_model=self.load_model,
                predict=self.predict,
                async_predict=self.async_predict,
                async_batch_predict=self.async_batch_predict,
                async_load_model=self.async_load_model,
                batch_predict=self.batch_predict,
                post_processing_config=getattr(self, "_post_processing_config", {}),
                index_to_category=getattr(self, "_index_to_category", None),
                target_categories=getattr(self, "_target_categories", None),
                is_inference_API=self.is_inference_API,
            )

            # Start the pipeline (manages its own event loop thread)
            self.streaming_pipeline.start()

            # Start refresh + heartbeat via CameraConfigManager
            if self.camera_config_manager:
                self.camera_config_manager.start()

            logging.info("Streaming pipeline initialized successfully")

        except Exception as e:
            logging.exception(f"Failed to initialize streaming pipeline: {e!s}")
            raise

    def _on_pipeline_config_changed(self, new_configs):
        """Handle camera config changes for streaming pipeline mode.

        Schedules reconciliation on the pipeline's event loop (same as the
        old _trigger_api_refresh + _reconcile_cameras chain).
        """
        if not self.streaming_pipeline:
            logging.error("No streaming pipeline available for config change reconciliation")
            return

        event_loop = getattr(self.streaming_pipeline, "_event_loop", None)
        if not event_loop or event_loop.is_closed() or not event_loop.is_running():
            logging.error("Event loop not available for pipeline reconciliation")
            raise RuntimeError("Event loop not available")

        async def _reconcile():
            try:
                result = await self.streaming_pipeline.reconcile_camera_configs(new_configs)
                if result.get("success"):
                    logging.info(
                        "Pipeline reconciliation completed: %d cameras active (+%d, ~%d, -%d)",
                        result["total_cameras"],
                        result["added"],
                        result["updated"],
                        result["removed"],
                    )
                else:
                    logging.error(
                        "Pipeline reconciliation failed: %s",
                        result.get("errors", []),
                    )
            except Exception as e:
                logging.exception(f"Exception during pipeline reconciliation: {e}")

        try:
            future = asyncio.run_coroutine_threadsafe(_reconcile(), event_loop)
            future.add_done_callback(
                lambda fut: (
                    logging.error(f"Reconciliation future error: {fut.exception()}") if fut.exception() else None
                )
            )
        except RuntimeError as e:
            logging.exception(f"Failed to schedule reconciliation: {e}")
            raise

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

            # Stop camera config manager (refresh listener + heartbeat + producer)
            if self.camera_config_manager:
                try:
                    self.camera_config_manager.stop()
                    logging.info("Camera config manager stopped")
                except Exception as exc:
                    logging.exception("Error stopping camera config manager: %s", str(exc))

            # Stop CUDA SHM analytics publisher if running
            if hasattr(self, "_cuda_shm_analytics_publisher") and self._cuda_shm_analytics_publisher:
                try:
                    self._cuda_shm_analytics_publisher.stop()
                    logging.info("CUDA SHM analytics publisher stopped")
                except Exception as exc:
                    logging.exception("Error stopping CUDA SHM analytics publisher: %s", str(exc))

            # Stop CUDA SHM engine if running (operates independently)
            if self.cuda_shm_engine:
                try:
                    self.cuda_shm_engine.stop()
                    logging.info("CUDA SHM inference engine stopped")
                except Exception as exc:
                    logging.exception("Error stopping CUDA SHM engine: %s", str(exc))

            # Stop streaming pipeline
            if self.streaming_pipeline:
                try:
                    # Stop the pipeline (now manages its own event loop thread)
                    self.streaming_pipeline.stop()
                    logging.info("Streaming pipeline stopped")
                except Exception as exc:
                    logging.exception("Error stopping streaming pipeline: %s", str(exc))

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
                    logging.exception("Error waiting for stream manager thread: %s", str(exc))

            # Stop proxy interface
            if self.proxy_interface:
                try:
                    self.proxy_interface.stop()
                    logging.info("Proxy interface stopped")
                except Exception as exc:
                    logging.exception("Error stopping proxy interface: %s", str(exc))

            logging.info("Server shutdown completed")

        except Exception as exc:
            logging.exception("Error during server shutdown: %s", str(exc))
            raise


class MatriceDeployServerUtils:
    """Utility class for managing deployment server operations."""

    def __init__(
        self,
        action_tracker: ActionTracker,
        inference_interface: InferenceInterface,
        external_port: int,
        main_server: "MatriceDeployServer" = None,
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
        self.shutdown_threshold = int(self.action_details.get("shutdownThreshold", 15)) * 60
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
                with urllib.request.urlopen("https://v4.ident.me", timeout=IP_FETCH_TIMEOUT_SECONDS) as response:  # nosec B310  # nosemgrep: python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected
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
                logging.warning("Failed to get deployment instance status: %s", error_msg)
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
            elapsed_time = (now - self.inference_interface.get_latest_inference_time()).total_seconds()
            logging.debug(
                "Using latest inference time for elapsed calculation: %.1fs",
                elapsed_time,
            )
            return elapsed_time

        # Final fallback: return a safe default
        logging.warning("No latest inference time available, using safe default of 0 seconds")
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
            logging.exception(
                "Error checking shutdown condition: %s",
                str(exc),
            )

    def shutdown(self):
        """Gracefully shutdown the deployment instance."""
        try:
            logging.warning("Initiating shutdown sequence...")

            # Notify backend of shutdown
            try:
                logging.warning("Shutdown is triggered, but notifying backend is disabled")
            except Exception as exc:
                logging.exception("Exception while notifying backend of shutdown: %s", str(exc))

            # Update status
            try:
                self.action_tracker.update_status(
                    "MDL_DPL_STP",
                    "SUCCESS",
                    "Model deployment stopped",
                )
                logging.warning("Updated deployment status to stopped")
            except Exception as exc:
                logging.exception("Failed to update deployment status: %s", str(exc))

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
            logging.exception("Error during shutdown: %s", str(exc))
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
                    failure_duration_minutes = (consecutive_deployment_failures * SHUTDOWN_CHECK_INTERVAL_SECONDS) / 60

                    logging.warning(
                        "Deployment status check failed (%d/%d) - %.1f minutes of failures",
                        consecutive_deployment_failures,
                        MAX_DEPLOYMENT_CHECK_FAILURES_BEFORE_SHUTDOWN,
                        failure_duration_minutes,
                    )

                    if consecutive_deployment_failures >= MAX_DEPLOYMENT_CHECK_FAILURES_BEFORE_SHUTDOWN:
                        logging.error(
                            "Deployment status check failed %d consecutive times (%.1f minutes), initiating shutdown",
                            consecutive_deployment_failures,
                            failure_duration_minutes,
                        )
                        self.shutdown()
                        return

            except Exception as exc:
                consecutive_deployment_failures += 1
                failure_duration_minutes = (consecutive_deployment_failures * SHUTDOWN_CHECK_INTERVAL_SECONDS) / 60

                logging.exception(
                    "Error in shutdown checker (%d/%d) - %.1f minutes of failures: %s",
                    consecutive_deployment_failures,
                    MAX_DEPLOYMENT_CHECK_FAILURES_BEFORE_SHUTDOWN,
                    failure_duration_minutes,
                    str(exc),
                )

                if consecutive_deployment_failures >= MAX_DEPLOYMENT_CHECK_FAILURES_BEFORE_SHUTDOWN:
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
                        logging.debug("Heartbeat successful: %s", resp.get("message", "Success"))
                    consecutive_failures = 0
                else:
                    consecutive_failures += 1
                    error_msg = resp.get("message", "Unknown error") if resp else "No response"
                    failure_duration_minutes = (consecutive_failures * HEARTBEAT_INTERVAL_SECONDS) / 60

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
                failure_duration_minutes = (consecutive_failures * HEARTBEAT_INTERVAL_SECONDS) / 60

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

            # Removed commented-out code related to coordinated shutdown for code quality improvements. Refer to Git history for details.

        except KeyboardInterrupt:
            logging.warning("Received KeyboardInterrupt, initiating shutdown...")
            self._shutdown_initiated.set()
            if self.main_server:
                try:
                    self.main_server.stop_server()
                except Exception as exc:
                    logging.exception("Error during keyboard interrupt shutdown: %s", str(exc))
            self._shutdown_complete.set()
        except Exception as exc:
            logging.exception("Error in wait_for_shutdown: %s", str(exc))
            self._shutdown_initiated.set()
            if self.main_server:
                try:
                    self.main_server.stop_server()
                except Exception as exc:
                    logging.exception("Error during exception shutdown: %s", str(exc))
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

            resp = self.rpc.put(path="/v1/inference/update_deploy_instance_address", payload=payload)
            logging.info(
                "Successfully updated deployment address to %s:%s, response: %s",
                ip_address,
                self.external_port,
                resp,
            )
        except Exception as exc:
            logging.exception(
                "Failed to update deployment address: %s",
                str(exc),
            )
            raise
