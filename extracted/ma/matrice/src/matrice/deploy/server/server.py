"""Module providing server functionality."""

import os
import threading
import time
import urllib.request
import logging
import asyncio
from datetime import datetime, timezone
from typing import Optional, Callable

from matrice.deploy.server.proxy.proxy_interface import (
    MatriceProxyInterface,
)
from matrice.action_tracker import ActionTracker
from matrice.deploy.server.inference.model_manager import ModelManager
from matrice.deploy.server.inference.inference_interface import InferenceInterface
from matrice.deploy.server.stream_worker import StreamWorkerManager

# Module constants
DEFAULT_EXTERNAL_PORT = 80
DEFAULT_SHUTDOWN_THRESHOLD_MINUTES = 15
MIN_SHUTDOWN_THRESHOLD_MINUTES = 1
MAX_NUM_WORKERS = 20
MIN_NUM_WORKERS = 1
HEARTBEAT_INTERVAL_SECONDS = 30
SHUTDOWN_CHECK_INTERVAL_SECONDS = 30
CLEANUP_DELAY_SECONDS = 5
FINAL_CLEANUP_DELAY_SECONDS = 10
MAX_IP_FETCH_ATTEMPTS = 3
IP_FETCH_TIMEOUT_SECONDS = 10

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True,
)


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
    ):
        """Initialize MatriceDeploy.

        Args:
            load_model (callable, optional): Function to load model. Defaults to None.
            predict (callable, optional): Function to make predictions. Defaults to None.
            batch_predict (callable, optional): Function to make batch predictions. Defaults to None.
            custom_post_processing_fn (callable, optional): Function to get custom post processing config. Defaults to None.
            action_id (str, optional): ID for action tracking. Defaults to "".
            external_port (int, optional): External port number. Defaults to 80.

        Raises:
            ValueError: If required parameters are invalid
            Exception: If initialization fails
        """
        try:
            # Validate inputs
            self._validate_init_parameters(
                load_model, predict, action_id, external_port
            )

            self.external_port = int(external_port)

            # Initialize action tracker
            self.action_tracker = ActionTracker(action_id)

            # Get session and RPC from action tracker
            self.session = self.action_tracker.session
            self.rpc = self.session.rpc
            self.action_details = self.action_tracker.action_details
            self.job_params = self.action_tracker.get_job_params()
            self.server_type = self.action_tracker.server_type

            logging.info("Action details: %s", self.action_details)

            # Extract deployment information
            self.deployment_instance_id = self.action_details.get(
                "_idModelDeployInstance"
            )
            self.deployment_id = self.action_details.get("_idDeployment")
            self.model_id = self.action_details.get("_idModelDeploy")

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
            self.custom_post_processing_fn = custom_post_processing_fn

            # Initialize component references
            self.proxy_interface = None
            self.model_manager = None
            self.inference_interface = None
            self.stream_worker_manager = None

            # Initialize utilities
            self.utils = None

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

    def _validate_init_parameters(self, load_model, predict, action_id, external_port):
        """Validate initialization parameters.

        Args:
            load_model: Model loading function
            predict: Prediction function
            action_id: Action ID string
            external_port: External port number

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
            raise ValueError(
                f"Invalid external port: {external_port}. Must be between 1 and 65535"
            )

    def start(self):
        """Start the proxy interface and all server components."""
        try:
            self._validate_configuration()
            self._initialize_model_manager()
            self._initialize_inference_interface()
            self._start_stream_worker_if_enabled()
            self._start_proxy_interface()
            logging.info("All server components started successfully")

            # Update deployment status and address
            self.action_tracker.update_status(
                "MDL_DPY_MDL",
                "OK",
                "Model deployment model loaded",
            )
            self.utils = MatriceDeployServerUtils(
                self.action_tracker, self.inference_interface, self.external_port
            )
            self.utils.update_deployment_address()
            self.utils.run_background_checkers()
            self.action_tracker.update_status(
                "MDL_DPY_STR",
                "SUCCESS",
                "Model deployment started",
            )
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
        logging.info("Initializing model manager for model ID: %s", self.model_id)

        self.model_manager = ModelManager(
            model_id=self.model_id,
            internal_server_type=self.server_type,
            internal_port=os.environ["INTERNAL_PORT"],
            internal_host="localhost",
            load_model=self.load_model,
            predict=self.predict,
            batch_predict=self.batch_predict,
            action_tracker=self.action_tracker,
            num_model_instances=self.action_details.get("numModelInstances", 1),
        )

        logging.info("Model manager initialized successfully")

    def _initialize_inference_interface(self):
        """Initialize the inference interface component."""
        batch_size = self.action_details.get("batchSize", 1)
        dynamic_batching = self.action_details.get("dynamicBatching", False)

        # Validate batch size
        if not isinstance(batch_size, int) or batch_size < 1:
            logging.warning("Invalid batch size %s, using default: 1", batch_size)
            batch_size = 1

        logging.info(
            "Initializing inference interface with batch_size: %d, dynamic_batching: %s",
            batch_size,
            dynamic_batching,
        )

        self.inference_interface = InferenceInterface(
            action_tracker=self.action_tracker,
            model_manager=self.model_manager,
            batch_size=batch_size,
            dynamic_batching=dynamic_batching,
            post_processing_config=self.job_params.get("postProcessingConfig", None),
            custom_post_processing_fn=self.custom_post_processing_fn,
        )

        logging.info("Inference interface initialized successfully")

    def _start_stream_worker_if_enabled(self):
        """Start stream worker manager if Kafka is enabled."""
        is_kafka_enabled = self.action_details.get("isKafkaEnabled", False)

        if not is_kafka_enabled:
            logging.info("Kafka streaming is disabled")
            return

        enable_multi_worker = self.action_details.get("enableMultiWorker", False)
        num_workers = min(
            max(
                int(self.action_details.get("numWorkers", MIN_NUM_WORKERS)),
                MIN_NUM_WORKERS,
            ),
            MAX_NUM_WORKERS,
        )

        logging.info(
            "Starting stream worker manager with multi-worker: %s, num_workers: %d",
            enable_multi_worker,
            num_workers,
        )

        self.stream_worker_manager = StreamWorkerManager(
            session=self.session,
            deployment_id=self.deployment_id,
            deployment_instance_id=self.deployment_instance_id,
            inference_interface=self.inference_interface,
            num_workers=num_workers,
        )

        # Start stream worker manager in background thread since it's async
        def start_stream_worker():
            """Start the async stream worker manager in a new event loop."""

            async def start_and_run_forever():
                await self.stream_worker_manager.start()
                logging.info("Stream worker manager started successfully")
                # Keep the event loop running
                await asyncio.Event().wait()

            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(start_and_run_forever())
            except Exception as exc:
                logging.error("Failed to start stream worker manager: %s", str(exc))
                raise

        try:
            worker_thread = threading.Thread(
                target=start_stream_worker, daemon=False, name="StreamWorkerManager"
            )
            worker_thread.start()
            logging.info("Stream worker manager thread started successfully")
        except Exception as exc:
            logging.error("Failed to start stream worker thread: %s", str(exc))
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

    def start_server(self):
        """Start the server and related components.

        Raises:
            Exception: If unable to initialize server
        """
        self.start()

    def stop_server(self):
        """Stop the server and related components."""
        # TODO: Implement server stop with keyboard interrupt
        ...


class MatriceDeployServerUtils:
    """Utility class for managing deployment server operations."""

    def __init__(self, action_tracker: ActionTracker, inference_interface: InferenceInterface, external_port: int):
        """Initialize utils with reference to the main server.

        Args:
            action_tracker: ActionTracker instance
            inference_interface: InferenceInterface instance
            external_port: External port number
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
        self._ip = None
        self._ip_fetch_attempts = 0
        self._max_ip_fetch_attempts = MAX_IP_FETCH_ATTEMPTS

    @property
    def ip(self):
        """Get the external IP address with caching and retry logic."""
        if self._ip is None and self._ip_fetch_attempts < self._max_ip_fetch_attempts:
            self._ip_fetch_attempts += 1
            try:
                with urllib.request.urlopen(
                    "https://ident.me", timeout=IP_FETCH_TIMEOUT_SECONDS
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
                f"/v1/deployment/get_deployment_without_auth_key/{self.deployment_id}",
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
                logging.debug("No running instances found")
                return False

            for instance in running_instances:
                if instance.get("modelDeployInstanceId") == self.deployment_instance_id:
                    is_deployed = instance.get("deployed", False)
                    logging.debug(
                        "Instance %s deployment status: %s",
                        self.deployment_instance_id,
                        "deployed" if is_deployed else "not deployed",
                    )
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

        # Try to get latest prediction time from API
        # try:
        #     latest_prediction_time = self.rpc.get(
        #         f"/v1/model_prediction/get_latest_prediction_time/{self.deployment_instance_id}",
        #         raise_exception=False,
        #     )

        #     if (
        #         latest_prediction_time
        #         and latest_prediction_time.get("success")
        #         and latest_prediction_time.get("data")
        #     ):
        #         try:
        #             last_time = datetime.strptime(
        #                 latest_prediction_time["data"],
        #                 "%Y-%m-%dT%H:%M:%S.%fZ",
        #             ).replace(tzinfo=timezone.utc)
        #             elapsed_time = (now - last_time).total_seconds()
        #             logging.debug(
        #                 "Successfully retrieved latest prediction time, elapsed: %.1fs",
        #                 elapsed_time,
        #             )
        #             return elapsed_time
        #         except (ValueError, TypeError) as date_exc:
        #             logging.warning(
        #                 "Failed to parse prediction time '%s': %s",
        #                 latest_prediction_time.get("data"),
        #                 str(date_exc),
        #             )
        #     else:
        #         # API call failed or returned no data
        #         error_msg = (
        #             latest_prediction_time.get(
        #                 "message", "No response or invalid response"
        #             )
        #             if isinstance(latest_prediction_time, dict)
        #             else "No response"
        #         )
        #         logging.debug(
        #             "No recent prediction time available (%s), falling back to deployment start time",
        #             error_msg,
        #         )

        # except Exception as exc:
        #     # Any exception during API call
        #     logging.debug(
        #         "Exception getting latest prediction time (%s), falling back to deployment start time",
        #         str(exc),
        #     )

        if self.inference_interface.get_latest_inference_time():
            elapsed_time = (now - self.inference_interface.get_latest_inference_time()).total_seconds()
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
            # Check if instance is still running according to backend
            if not self.is_instance_running():
                logging.info(
                    "Instance is no longer running according to backend, initiating shutdown"
                )
                self.shutdown()
                return

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
                logging.debug(
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
            logging.info("Initiating shutdown sequence...")

            # Notify backend of shutdown
            try:
                resp = self.rpc.delete(
                    f"/v1/deployment/delete_deploy_instance/{self.deployment_instance_id}",
                    raise_exception=False,
                )
                if resp and resp.get("success"):
                    logging.info(
                        "Successfully notified backend of deployment instance shutdown"
                    )
                else:
                    error_msg = (
                        resp.get("message", "Unknown error") if resp else "No response"
                    )
                    logging.warning(
                        "Failed to notify backend of shutdown: %s", error_msg
                    )
            except Exception as exc:
                logging.error(
                    "Exception while notifying backend of shutdown: %s", str(exc)
                )

            # Allow time for cleanup
            time.sleep(CLEANUP_DELAY_SECONDS)

            # Update status
            try:
                self.action_tracker.update_status(
                    "MDL_DPL_STP",
                    "SUCCESS",
                    "Model deployment stopped",
                )
                logging.info("Updated deployment status to stopped")
            except Exception as exc:
                logging.error("Failed to update deployment status: %s", str(exc))

            logging.info("Waiting for final cleanup...")
            time.sleep(FINAL_CLEANUP_DELAY_SECONDS)
            logging.info("Shutdown complete, exiting process")
            os._exit(0)

        except Exception as exc:
            logging.error("Error during shutdown: %s", str(exc))
            os._exit(1)

    def shutdown_checker(self):
        """Background thread to periodically check for idle shutdown condition."""
        logging.info("Shutdown checker started")

        while True:
            try:
                self.trigger_shutdown_if_needed()
            except Exception as exc:
                logging.error("Error in shutdown checker: %s", str(exc))
            finally:
                time.sleep(SHUTDOWN_CHECK_INTERVAL_SECONDS)

    def heartbeat_checker(self):
        """Background thread to periodically send heartbeat."""
        consecutive_failures = 0
        max_consecutive_failures = 3

        logging.info("Heartbeat checker started")
        while True:
            try:
                resp = self.rpc.post(
                    f"/v1/deployment/add_instance_heartbeat/{self.deployment_instance_id}",
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
                    logging.warning(
                        "Heartbeat failed (%d/%d): %s",
                        consecutive_failures,
                        max_consecutive_failures,
                        error_msg,
                    )

                    if consecutive_failures >= max_consecutive_failures:
                        logging.error(
                            "Heartbeat failed %d consecutive times, this may indicate connectivity issues",
                            consecutive_failures,
                        )

            except Exception as exc:
                consecutive_failures += 1
                logging.warning(
                    "Heartbeat exception (%d/%d): %s",
                    consecutive_failures,
                    max_consecutive_failures,
                    str(exc),
                )

            time.sleep(HEARTBEAT_INTERVAL_SECONDS)

    def run_background_checkers(self):
        """Start the shutdown checker and heartbeat checker threads as daemons."""
        shutdown_thread = threading.Thread(
            target=self.shutdown_checker,
            name="ShutdownChecker",
        )
        heartbeat_thread = threading.Thread(
            target=self.heartbeat_checker,
            name="HeartbeatChecker",
        )

        shutdown_thread.daemon = True
        heartbeat_thread.daemon = True

        shutdown_thread.start()
        heartbeat_thread.start()

        logging.info("Background checker threads started successfully")

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
                path="/v1/deployment/update_deploy_instance_address",
                payload=payload,
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
