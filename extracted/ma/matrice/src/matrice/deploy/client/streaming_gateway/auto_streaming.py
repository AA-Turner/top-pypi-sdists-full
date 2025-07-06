"""Auto streaming functionality for deployment streaming."""

import logging
import threading
import time
from typing import Dict, List, Optional, Callable

from matrice.deploy.client.camera_manager import CameraManager, CameraConfig
from matrice.deploy.client.streaming_gateway.streaming_gateway_utils import (
    InputConfig,
    OutputConfig,
    InputType,
    ModelInputType,
)
from matrice.deploy.client.streaming_gateway.streaming_gateway import StreamingGateway


class AutoStreaming:
    """
    Handles automatic streaming setup and management using camera configurations.

    This class encapsulates all auto streaming logic, making it reusable across
    different components and easier to maintain.

    Example usage:
        auto_streaming = AutoStreaming(
            session=session,
            deployment_ids=["deploy1", "deploy2"],
            model_input_type=ModelInputType.FRAMES,
            output_configs={"deploy1": output_config}
        )

        # Start auto streaming
        success = auto_streaming.start()

        # Stop auto streaming
        auto_streaming.stop()

        # Get statistics
        stats = auto_streaming.get_statistics()
    """

    def __init__(
        self,
        session,
        deployment_ids: List[str] = [],
        model_input_type: ModelInputType = ModelInputType.FRAMES,
        output_configs: Optional[Dict[str, OutputConfig]] = None,
        result_callback: Optional[Callable] = None,
        strip_input_from_result: bool = True,
    ):
        """
        Initialize AutoStreaming.

        Args:
            session: Session object for authentication
            deployment_ids: List of deployment IDs to enable auto streaming for
            model_input_type: Model input type (FRAMES or VIDEO)
            output_configs: Optional output configurations per deployment
            result_callback: Optional callback for processing results
            strip_input_from_result: Whether to strip input from results
        """
        self.session = session
        self.deployment_ids = deployment_ids or []
        self.model_input_type = model_input_type
        self.output_configs = output_configs or {}
        self.result_callback = result_callback
        self.strip_input_from_result = strip_input_from_result

        # Streaming configuration
        self.default_video_chunk_duration = 10
        self.default_video_format = "mp4"

        # Initialize camera manager
        self.camera_manager = CameraManager(self.session)

        # State management
        self.streaming_gateways: Dict[str, StreamingGateway] = {}
        self.streaming_threads: Dict[str, threading.Thread] = {}
        self.is_running = False
        self._stop_event = threading.Event()
        self._state_lock = threading.RLock()

        # Statistics
        self.stats = {
            "enabled": True,
            "deployment_ids": self.deployment_ids,
            "active_streams": {},
            "failed_streams": {},
            "total_deployments": len(self.deployment_ids),
            "camera_configs_loaded": 0,
            "start_time": None,
            "errors": 0,
            "last_error": None,
            "last_error_time": None,
        }

        logging.info(
            f"AutoStreaming initialized for {len(self.deployment_ids)} deployments"
        )

    def setup_streaming_gateways(self) -> bool:
        """
        Setup StreamingGateway instances for each deployment.

        Returns:
            bool: True if all gateways were setup successfully, False otherwise
        """
        success_count = 0
        for deployment_id in self.deployment_ids:
            try:
                gateway = StreamingGateway(
                    session=self.session,
                    deployment_id=deployment_id,
                    output_config=self.output_configs.get(deployment_id, None),
                    model_input_type=self.model_input_type,
                    auto_streaming=True,
                    result_callback=self.result_callback,
                    strip_input_from_result=self.strip_input_from_result,
                )

                self.streaming_gateways[deployment_id] = gateway
                success_count += 1

                logging.info(f"Setup streaming gateway for deployment: {deployment_id}")

            except Exception as e:
                error_msg = (
                    f"Failed to setup streaming gateway for {deployment_id}: {e}"
                )
                logging.error(error_msg)
                self._record_error(error_msg)
                self.stats["failed_streams"][deployment_id] = str(e)

        if success_count == 0:
            logging.error("Failed to setup any streaming gateways")
            return False

        logging.info(
            f"Successfully setup {success_count}/{len(self.deployment_ids)} streaming gateways"
        )
        return True

    def setup_camera_configurations(self) -> bool:
        """
        Setup camera configurations for all deployments.

        Returns:
            bool: True if at least one deployment has camera configs, False otherwise
        """
        total_cameras = 0

        for deployment_id in self.deployment_ids:
            if deployment_id not in self.streaming_gateways:
                continue

            try:
                # Get camera configurations for this deployment
                camera_configs, error, message = (
                    self.camera_manager.get_camera_configs_by_deployment_id(
                        deployment_id
                    )
                )

                if error:
                    error_msg = (
                        f"Failed to get camera configs for {deployment_id}: {error}"
                    )
                    logging.error(error_msg)
                    self._record_error(error_msg)
                    self.stats["failed_streams"][deployment_id] = error
                    continue

                if not camera_configs:
                    logging.warning(
                        f"No camera configurations found for deployment {deployment_id}"
                    )
                    continue

                # Convert camera configs to input configs
                input_configs = self._convert_camera_configs_to_inputs(
                    camera_configs, deployment_id
                )

                if input_configs:
                    # Set input configs on the gateway
                    gateway = self.streaming_gateways[deployment_id]
                    gateway.inputs_config = input_configs
                    total_cameras += len(input_configs)

                    logging.info(
                        f"Configured {len(input_configs)} cameras for deployment {deployment_id}"
                    )
                else:
                    logging.warning(
                        f"No valid input configurations created for deployment {deployment_id}"
                    )

            except Exception as e:
                error_msg = f"Error setting up camera configs for {deployment_id}: {e}"
                logging.error(error_msg)
                self._record_error(error_msg)
                self.stats["failed_streams"][deployment_id] = str(e)

        self.stats["camera_configs_loaded"] = total_cameras

        if total_cameras == 0:
            logging.error("No camera configurations could be loaded for any deployment")
            return False

        logging.info(
            f"Successfully configured {total_cameras} cameras across all deployments"
        )
        return True

    def _convert_camera_configs_to_inputs(
        self, camera_configs: List[CameraConfig], deployment_id: str
    ) -> List[InputConfig]:
        """
        Convert camera configurations to input configurations.

        Args:
            camera_configs: List of CameraConfig objects
            deployment_id: Deployment ID for logging

        Returns:
            List of InputConfig objects
        """
        input_configs = []

        for i, camera_config in enumerate(camera_configs):
            try:
                # Determine input type based on stream URL
                input_type = (
                    InputType.RTSP_STREAM
                    if not camera_config.stream_url.isdigit()
                    else InputType.CAMERA
                )

                input_config = InputConfig(
                    type=input_type,
                    source=camera_config.stream_url,
                    fps=camera_config.fps if camera_config.fps > 0 else self.fps,
                    stream_key=f"camera_{camera_config.id or i}",
                    quality=(
                        camera_config.video_quality
                        if camera_config.video_quality > 0
                        else self.quality
                    ),
                    width=camera_config.width if camera_config.width > 0 else None,
                    height=camera_config.height if camera_config.height > 0 else None,
                    model_input_type=self.model_input_type,
                    video_duration=self.default_video_chunk_duration,
                    video_format=self.default_video_format,
                )

                input_configs.append(input_config)

                logging.info(
                    f"Added camera input for {deployment_id}: {camera_config.camera_location} "
                    f"({camera_config.stream_url})"
                )

            except Exception as e:
                logging.error(
                    f"Failed to create input config for camera {i} in {deployment_id}: {e}"
                )
                continue

        return input_configs

    def start(self) -> bool:
        """
        Start auto streaming for all configured deployments.

        Returns:
            bool: True if streaming started successfully, False otherwise
        """
        with self._state_lock:
            if self.is_running:
                logging.warning("Auto streaming is already running")
                return False

            logging.info("Starting auto streaming...")
            self.stats["start_time"] = time.time()
            self._stop_event.clear()

            # Setup streaming gateways
            if not self.setup_streaming_gateways():
                return False

            # Setup camera configurations
            if not self.setup_camera_configurations():
                return False

            # Start streaming for each deployment
            started_count = 0
            for deployment_id, gateway in self.streaming_gateways.items():
                if not gateway.inputs_config:
                    logging.warning(
                        f"No input configs for deployment {deployment_id}, skipping"
                    )
                    continue

                try:
                    # Create and start streaming thread
                    thread = threading.Thread(
                        target=self._streaming_worker,
                        args=(deployment_id, gateway),
                        name=f"AutoStream-{deployment_id}",
                        daemon=True,
                    )

                    self.streaming_threads[deployment_id] = thread
                    thread.start()
                    started_count += 1

                    self.stats["active_streams"][deployment_id] = {
                        "status": "starting",
                        "cameras": len(gateway.inputs_config),
                        "start_time": time.time(),
                    }

                    logging.info(
                        f"Started streaming thread for deployment: {deployment_id}"
                    )

                except Exception as e:
                    error_msg = f"Failed to start streaming for {deployment_id}: {e}"
                    logging.error(error_msg)
                    self._record_error(error_msg)
                    self.stats["failed_streams"][deployment_id] = str(e)

            if started_count == 0:
                logging.error("Failed to start streaming for any deployment")
                return False

            self.is_running = True
            logging.info(
                f"Auto streaming started successfully for {started_count} deployments"
            )
            return True

    def _streaming_worker(self, deployment_id: str, gateway: StreamingGateway):
        """
        Worker thread for streaming a specific deployment.

        Args:
            deployment_id: Deployment ID
            gateway: StreamingGateway instance
        """
        try:
            # Start streaming
            success = gateway.start_streaming()

            if success:
                self.stats["active_streams"][deployment_id]["status"] = "running"
                logging.info(
                    f"Streaming started successfully for deployment: {deployment_id}"
                )

                # Keep the thread alive while streaming
                while not self._stop_event.is_set() and gateway.is_streaming:
                    time.sleep(1.0)

            else:
                error_msg = f"Failed to start streaming for deployment: {deployment_id}"
                logging.error(error_msg)
                self._record_error(error_msg)
                self.stats["failed_streams"][
                    deployment_id
                ] = "Failed to start streaming"

        except Exception as e:
            error_msg = f"Error in streaming worker for {deployment_id}: {e}"
            logging.error(error_msg)
            self._record_error(error_msg)
            self.stats["failed_streams"][deployment_id] = str(e)

        finally:
            # Update status
            if deployment_id in self.stats["active_streams"]:
                self.stats["active_streams"][deployment_id]["status"] = "stopped"

            logging.info(f"Streaming worker stopped for deployment: {deployment_id}")

    def stop(self):
        """Stop auto streaming for all deployments."""
        with self._state_lock:
            if not self.is_running:
                logging.warning("Auto streaming is not running")
                return

            logging.info("Stopping auto streaming...")
            self._stop_event.set()
            self.is_running = False

            # Stop all streaming gateways
            for deployment_id, gateway in self.streaming_gateways.items():
                try:
                    gateway.stop_streaming()
                    logging.info(f"Stopped streaming for deployment: {deployment_id}")
                except Exception as e:
                    logging.error(f"Error stopping streaming for {deployment_id}: {e}")

            # Wait for all threads to finish
            for deployment_id, thread in self.streaming_threads.items():
                try:
                    if thread.is_alive():
                        thread.join(timeout=10.0)
                        if thread.is_alive():
                            logging.warning(
                                f"Thread for {deployment_id} did not stop gracefully"
                            )
                except Exception as e:
                    logging.error(f"Error joining thread for {deployment_id}: {e}")

            # Clear state
            self.streaming_threads.clear()
            self.streaming_gateways.clear()

            # Update stats
            for deployment_id in self.stats["active_streams"]:
                self.stats["active_streams"][deployment_id]["status"] = "stopped"

            logging.info("Auto streaming stopped successfully")

    def refresh_camera_configs(self) -> bool:
        """
        Refresh camera configurations for all deployments.

        Returns:
            bool: True if configurations were refreshed successfully
        """
        if self.is_running:
            logging.warning(
                "Cannot refresh camera configs while auto streaming is running"
            )
            return False

        logging.info("Refreshing camera configurations...")
        return self.setup_camera_configurations()

    def get_statistics(self) -> Dict:
        """
        Get auto streaming statistics.

        Returns:
            Dict with comprehensive statistics
        """
        with self._state_lock:
            stats = self.stats.copy()

            # Calculate runtime
            if stats["start_time"]:
                runtime = time.time() - stats["start_time"]
                stats["runtime_seconds"] = runtime
            else:
                stats["runtime_seconds"] = 0

            # Add current status
            stats["is_running"] = self.is_running
            stats["active_deployments"] = len(self.streaming_gateways)
            stats["running_threads"] = sum(
                1 for t in self.streaming_threads.values() if t.is_alive()
            )

            return stats

    def get_deployment_status(self, deployment_id: str) -> Optional[Dict]:
        """
        Get status for a specific deployment.

        Args:
            deployment_id: Deployment ID

        Returns:
            Dict with deployment status or None if not found
        """
        if deployment_id not in self.streaming_gateways:
            return None

        gateway = self.streaming_gateways[deployment_id]
        thread = self.streaming_threads.get(deployment_id)

        return {
            "deployment_id": deployment_id,
            "is_streaming": (
                gateway.is_streaming if hasattr(gateway, "is_streaming") else False
            ),
            "thread_alive": thread.is_alive() if thread else False,
            "input_count": len(gateway.inputs_config) if gateway.inputs_config else 0,
            "active_stream_info": self.stats["active_streams"].get(deployment_id, {}),
            "failed_stream_info": self.stats["failed_streams"].get(deployment_id, None),
        }

    def _record_error(self, error_message: str):
        """Record an error in statistics."""
        self.stats["errors"] += 1
        self.stats["last_error"] = error_message
        self.stats["last_error_time"] = time.time()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
