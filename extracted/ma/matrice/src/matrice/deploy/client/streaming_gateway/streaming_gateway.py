import json
import logging
import time
import threading
from typing import Dict, List, Optional, Callable
from matrice.deploy.client.client import MatriceDeployClient
from matrice.deploy.client.streaming_gateway.streaming_gateway_utils import (
    InputConfig,
    OutputConfig,
    InputType,
    ModelInputType,
)
from matrice.deploy.client.streaming_gateway.streaming_results_handler import (
    StreamingResultsHandler,
)


class StreamingGateway:
    """Simplified streaming gateway that leverages MatriceDeployClient's capabilities.

    Supports both frame-based streaming (sending individual images) and video-based
    streaming (sending video chunks) based on the model_input_type configuration.

    Now includes optional post-processing capabilities for model results.

    Prevents multiple deployments or background streams from being started simultaneously
    using simple class-level tracking.

    Example usage:
        # Traditional usage with manual input config
        frame_input = create_camera_frame_input(camera_index=0, fps=30)
        video_input = create_camera_video_input(
            camera_index=0,
            fps=30,
            video_duration=5.0,  # 5-second chunks
            video_format="mp4"
        )

        gateway = StreamingGateway(
            session=session,
            deployment_id="your_deployment_id",
            inputs_config=[video_input],
            output_config=output_config
        )

        gateway.start_streaming()

        # To stop all streams from any instance:
        StreamingGateway.stop_all_active_streams()
    """

    # Class-level tracking of active instances
    _active_instances: Dict[str, "StreamingGateway"] = {}  # deployment_id -> instance
    _class_lock = threading.RLock()

    def __init__(
        self,
        session,
        deployment_id: str = None,
        inputs_config: List[InputConfig] = None,
        output_config: OutputConfig = None,
        create_deployment_config: Dict = None,
        auth_key: str = None,
        consumer_group_id: str = None,
        result_callback: Optional[Callable] = None,
        strip_input_from_result: bool = True,
        force_restart: bool = False,
    ):
        """Initialize StreamingGateway.

        Args:
            session: Session object for authentication
            deployment_id: ID of existing deployment (optional if create_deployment_config provided)
            inputs_config: Multiple input configurations (alternative to input_config)
            output_config: Output configuration
            create_deployment_config: Configuration for creating new deployment
            auth_key: Authentication key for deployment
            consumer_group_id: Kafka consumer group ID
            result_callback: Optional callback function for processing results
            strip_input_from_result: Whether to remove 'input' field from results to save space
            force_restart: Whether to force stop existing streams and restart (use with caution)
        """
        if not session:
            raise ValueError("Session is required")

        self.session = session
        self.rpc = self.session.rpc
        self.auth_key = auth_key
        self.deployment_id = deployment_id
        self.create_deployment_config = create_deployment_config
        self.strip_input_from_result = strip_input_from_result
        self.force_restart = force_restart

        # Validate inputs
        if not (self.deployment_id or self.create_deployment_config):
            raise ValueError(
                "Either deployment_id or create_deployment_config must be provided"
            )

        if not inputs_config:
            raise ValueError("At least one input configuration is required")

        self.inputs_config = (
            inputs_config if isinstance(inputs_config, list) else [inputs_config]
        )

        # Validate each input config
        for i, config in enumerate(self.inputs_config):
            if not isinstance(config, InputConfig):
                raise ValueError(f"Input config {i} must be an InputConfig instance")

        self.output_config = output_config
        self.consumer_group_id = consumer_group_id
        self.result_callback = result_callback
        self.kafka_producer = None

        # Initialize client
        self.client = MatriceDeployClient(
            session=self.session,
            deployment_id=self.deployment_id,
            auth_key=self.auth_key,
            consumer_group_id=self.consumer_group_id,
            create_deployment_config=self.create_deployment_config,
        )
        if not self.deployment_id:
            self.deployment_id = self.client.create_deployment(
                self.create_deployment_config
            )
        self.client.create_auth_key_if_not_exists()

        # State management with proper synchronization
        self.is_streaming = False
        self.result_thread: Optional[threading.Thread] = None
        self._stop_streaming = threading.Event()
        self._file_counter = 0
        self._state_lock = threading.RLock()
        self._my_stream_keys = set()

        # Initialize results handler if needed
        self.results_handler = None
        if self.output_config or self.result_callback:
            self.results_handler = StreamingResultsHandler(
                client=self.client,
                output_config=self.output_config,
                deployment_id=self.deployment_id,
                strip_input_from_result=self.strip_input_from_result,
                result_callback=self.result_callback,
            )

        # Initialize post-processing
        self.post_processor = None
        if self.output_config and self.output_config.apply_post_processing:
            self._setup_post_processing()

        # Statistics
        self.stats = {
            "start_time": None,
            "results_received": 0,
            "results_post_processed": 0,
            "post_processing_errors": 0,
            "errors": 0,
            "last_error": None,
            "last_error_time": None,
        }

        # Setup output
        self._setup_output()

        logging.info(
            f"StreamingGateway initialized for deployment {self.deployment_id}"
        )

    def _register_as_active(self):
        """Register this instance as active."""
        with self.__class__._class_lock:
            self.__class__._active_instances[self.deployment_id] = self
        logging.info(
            f"Registered as active instance for deployment {self.deployment_id}"
        )

    def _unregister_as_active(self):
        """Unregister this instance from active tracking."""
        with self.__class__._class_lock:
            if self.deployment_id in self.__class__._active_instances:
                if self.__class__._active_instances[self.deployment_id] is self:
                    del self.__class__._active_instances[self.deployment_id]

        logging.info(
            f"Unregistered active instance for deployment {self.deployment_id}"
        )

    def stop_all_active_streams(self):
        """Stop all active streams across all deployments."""

        if not self.force_restart:
            return

        logging.warning(
            f"Force stopping existing streams for deployment {self.deployment_id}"
        )

        with self.__class__._class_lock:
            if self.deployment_id in self.__class__._active_instances:
                existing_instance = self.__class__._active_instances[self.deployment_id]

                try:
                    # Stop the existing instance
                    existing_instance.stop_streaming()
                    logging.info(
                        f"Force stopped existing streams for deployment {self.deployment_id}"
                    )
                except Exception as e:
                    logging.warning(f"Error during force stop: {e}")

                # Wait a moment for cleanup
                time.sleep(1.0)

        logging.info("Stopping all active streams...")

    def start_streaming(self) -> bool:
        """Start streaming using MatriceDeployClient's built-in capabilities.

        Returns:
            bool: True if streaming started successfully, False otherwise
        """
        with self._state_lock:
            if self.is_streaming:
                logging.warning("Streaming is already active on this instance")
                return False

            if not self.client:
                logging.error("No client available for streaming")
                return False

        # Validate that we have inputs to stream
        if not self.inputs_config:
            logging.error("No input configurations available for streaming")
            return False

        # Register as active instance
        self._register_as_active()

        # Start streaming for each input
        started_streams = []
        try:
            for i, input_config in enumerate(self.inputs_config):
                # Convert input source based on type
                if input_config.type == InputType.CAMERA:
                    input_source = int(input_config.source)
                else:
                    input_source = str(input_config.source)

                stream_key = input_config.stream_key or f"stream_{i}"

                # Choose streaming method based on model input type
                if input_config.model_input_type == ModelInputType.VIDEO:
                    # Start video streaming
                    success = self.client.start_background_video_stream(
                        input=input_source,
                        fps=input_config.fps,
                        stream_key=stream_key,
                        quality=input_config.quality,
                        width=input_config.width,
                        height=input_config.height,
                        video_duration=input_config.video_duration,
                        max_frames=input_config.max_frames,
                        video_format=input_config.video_format,
                    )
                    logging.info(
                        f"Started video streaming for input {input_config.source} "
                        f"(duration: {input_config.video_duration}s, "
                        f"max_frames: {input_config.max_frames}, "
                        f"format: {input_config.video_format})"
                    )
                else:
                    # Start frame streaming (default)
                    success = self.client.start_background_stream(
                        input=input_source,
                        fps=input_config.fps,
                        stream_key=stream_key,
                        quality=input_config.quality,
                        width=input_config.width,
                        height=input_config.height,
                    )
                    logging.info(
                        f"Started frame streaming for input {input_config.source}"
                    )

                if not success:
                    logging.error(
                        f"Failed to start streaming for input {input_config.source}"
                    )
                    # Stop already started streams
                    if started_streams:
                        logging.info("Stopping already started streams due to failure")
                        self.stop_streaming()

                    return False

                started_streams.append(stream_key)
                self._my_stream_keys.add(stream_key)

            with self._state_lock:
                self._stop_streaming.clear()
                self.is_streaming = True
                self.stats["start_time"] = time.time()

            # Start result consumption thread if we have output config or callback
            if self.output_config or self.result_callback:
                self.result_thread = threading.Thread(
                    target=self._consume_results, daemon=True, name="ResultConsumer"
                )
                self.result_thread.start()

            logging.info(
                f"Started streaming successfully with {len(self.inputs_config)} inputs"
            )
            return True

        except Exception as exc:
            logging.error(f"Error starting streaming: {exc}")
            # Clean up on error
            try:
                self.stop_streaming()
            except Exception as cleanup_exc:
                logging.error(f"Error during cleanup: {cleanup_exc}")
            return False

    def stop_streaming(self):
        """Stop all streaming operations."""
        with self._state_lock:
            if not self.is_streaming:
                logging.warning("Streaming is not active")
                return

            logging.info("Stopping streaming...")
            self._stop_streaming.set()
            self.is_streaming = False

        # Stop client streaming
        if self.client:
            try:
                self.client.stop_streaming()
            except Exception as exc:
                logging.error(f"Error stopping client streaming: {exc}")

        # Wait for result thread to finish
        if self.result_thread and self.result_thread.is_alive():
            self.result_thread.join(timeout=10.0)
            if self.result_thread.is_alive():
                logging.warning("Result thread did not stop gracefully")

        self.result_thread = None

        # Flush Kafka producer with extended timeout if needed
        if self.kafka_producer:
            try:
                logging.debug("Flushing Kafka producer...")
                # First attempt with standard timeout
                remaining = self.kafka_producer.flush(timeout=5.0)

                if remaining > 0:
                    logging.warning(
                        f"{remaining} messages still in queue, extending flush timeout"
                    )
                    # Extended flush for remaining messages
                    remaining = self.kafka_producer.flush(timeout=30.0)

                    if remaining > 0:
                        logging.error(
                            f"{remaining} messages could not be delivered within extended timeout"
                        )
                    else:
                        logging.info("All remaining messages delivered successfully")
                else:
                    logging.debug("Kafka producer flushed successfully")

            except Exception as exc:
                logging.error(f"Error flushing Kafka producer: {exc}")

        # Unregister from active tracking
        self._unregister_as_active()

        logging.info("Streaming stopped")

    def get_statistics(self) -> Dict:
        """Get streaming statistics.

        Returns:
            Dict with streaming statistics
        """
        with self._state_lock:
            stats = self.stats.copy()

        if stats["start_time"]:
            runtime = time.time() - stats["start_time"]
            stats["runtime_seconds"] = runtime
            if runtime > 0:
                stats["results_per_second"] = stats["results_received"] / runtime
            else:
                stats["results_per_second"] = 0
        else:
            stats["runtime_seconds"] = 0
            stats["results_per_second"] = 0

        # Add streaming status
        stats["is_streaming"] = self.is_streaming
        stats["my_stream_keys"] = list(self._my_stream_keys)

        return stats

    def get_config(self) -> Dict:
        """Get current configuration.

        Returns:
            Dict with current configuration
        """
        return {
            "deployment_id": self.deployment_id,
            "inputs_config": [config.to_dict() for config in self.inputs_config],
            "output_config": (
                self.output_config.to_dict() if self.output_config else None
            ),
            "consumer_group_id": self.consumer_group_id,
            "strip_input_from_result": self.strip_input_from_result,
            "force_restart": self.force_restart,
        }

    def save_config(self, filepath: str):
        """Save current configuration to file.

        Args:
            filepath: Path to save configuration
        """
        config = self.get_config()
        with open(filepath, "w") as f:
            json.dump(config, f, indent=2)

    @classmethod
    def load_config(
        cls, filepath: str, session=None, auth_key: str = None
    ) -> "StreamingGateway":
        """Load configuration from file and create StreamingGateway.

        Args:
            filepath: Path to configuration file
            session: Session object (required)
            auth_key: Authentication key

        Returns:
            StreamingGateway instance
        """
        if not session:
            raise ValueError("Session is required")

        with open(filepath, "r") as f:
            config = json.load(f)

        inputs_config = (
            [InputConfig.from_dict(input_cfg) for input_cfg in config["inputs_config"]]
            if config["inputs_config"]
            else None
        )

        output_config = (
            OutputConfig.from_dict(config["output_config"])
            if config["output_config"]
            else None
        )

        return cls(
            session=session,
            deployment_id=config["deployment_id"],
            inputs_config=inputs_config,
            output_config=output_config,
            auth_key=auth_key,
            consumer_group_id=config.get("consumer_group_id"),
            strip_input_from_result=config.get("strip_input_from_result", True),
            force_restart=config.get("force_restart", False),
        )

    def _consume_results(self):
        """Consume and process results from the deployment."""
        if self.results_handler:
            self.results_handler._consume_results()
        else:
            logging.warning("No results handler available for result consumption")

    def _setup_output(self):
        """Setup output configurations."""
        if self.results_handler:
            self.results_handler._setup_output()

    def _setup_post_processing(self):
        """Setup post-processing capabilities."""
        if self.results_handler:
            self.results_handler._setup_post_processing()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop_streaming()
