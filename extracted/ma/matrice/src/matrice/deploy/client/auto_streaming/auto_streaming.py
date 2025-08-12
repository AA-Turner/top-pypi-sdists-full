"""Auto streaming functionality for streaming gateway management."""

import logging
import threading
import time
from typing import Dict, List, Optional, Callable

from matrice.deployment.camera_manager import CameraManager
from matrice.deployment.streaming_gateway_manager import StreamingGateway as StreamingGatewayConfig
from matrice.deployment.streaming_gateway_manager import StreamingGatewayManager
from matrice.deploy.client.streaming_gateway import StreamingGateway, ModelInputType, OutputConfig, InputConfig

from .auto_streaming_utils import AutoStreamingUtils


class AutoStreaming:
    """
    Handles automatic streaming setup and management using streaming gateway configurations.

    This class manages multiple streaming gateways, automatically configures cameras
    based on the gateway's camera group assignments, and handles the streaming lifecycle.

    Example usage:
        # Method 1: From service IDs (auto-discovers all gateways)
        auto_streaming = AutoStreaming(
            session=session,
            service_ids=["service_id_123", "service_id_456"],
            model_input_type=ModelInputType.FRAMES
        )

        # Method 2: From specific gateway IDs
        auto_streaming = AutoStreaming(
            session=session,
            streaming_gateway_ids=["gateway1", "gateway2"],
            model_input_type=ModelInputType.FRAMES
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
        service_ids: List[str] = None,
        streaming_gateway_ids: List[str] = None,
        model_input_type: ModelInputType = ModelInputType.FRAMES,
        output_configs: Optional[Dict[str, OutputConfig]] = None,
        result_callback: Optional[Callable] = None,
        strip_input_from_result: bool = True,
        default_fps: int = 30,
        default_quality: int = 80,
        default_video_chunk_duration: int = 10,
        default_video_format: str = "mp4",
        simulate_video_file_stream: bool = False,
    ):
        """
        Initialize AutoStreaming with service IDs or streaming gateway IDs.

        Args:
            session: Session object for authentication
            service_ids: List of Service IDs (deployment or inference pipeline ID) - will auto-discover gateways
            streaming_gateway_ids: List of specific streaming gateway IDs to use
            model_input_type: Model input type (FRAMES or VIDEO)
            output_configs: Optional output configurations per streaming gateway
            result_callback: Optional callback for processing results
            strip_input_from_result: Whether to strip input from results
            default_fps: Default FPS for camera streams
            default_quality: Default quality for camera streams
            default_video_chunk_duration: Default video chunk duration for video input type
            default_video_format: Default video format for video input type
            simulate_video_file_stream: Whether to restream videos
        Note:
            Either service_ids OR streaming_gateway_ids must be provided, not both.
            If service_ids is provided, all gateways for those services will be auto-discovered.
        """
        if not service_ids and not streaming_gateway_ids:
            raise ValueError(
                "Either service_ids or streaming_gateway_ids must be provided"
            )

        if service_ids and streaming_gateway_ids:
            raise ValueError(
                "Cannot provide both service_ids and streaming_gateway_ids"
            )

        self.session = session
        self.service_ids = service_ids or []
        self.streaming_gateway_ids = streaming_gateway_ids or []
        self.model_input_type = model_input_type
        self.output_configs = output_configs or {}
        self.result_callback = result_callback
        self.strip_input_from_result = strip_input_from_result

        if not isinstance(self.service_ids, list):
            self.service_ids = [self.service_ids]
        if not isinstance(self.streaming_gateway_ids, list):
            self.streaming_gateway_ids = [self.streaming_gateway_ids]

        # Auto-discover gateways if service_ids provided
        if self.service_ids:
            self.streaming_gateway_ids.extend(self._discover_gateways_from_services())

        # Initialize utils
        self.utils = AutoStreamingUtils(
            default_fps=default_fps,
            default_quality=default_quality,
            default_video_chunk_duration=default_video_chunk_duration,
            default_video_format=default_video_format,
            simulate_video_file_stream=simulate_video_file_stream,
        )

        # State management
        self.streaming_gateways: Dict[str, StreamingGateway] = {}
        self.gateway_input_configs: Dict[str, List[InputConfig]] = {}
        self.streaming_threads: Dict[str, threading.Thread] = {}
        self.gateway_configs: Dict[str, StreamingGatewayConfig] = {}
        self.is_running = False
        self._stop_event = threading.Event()
        self._state_lock = threading.RLock()

        # Statistics
        self.stats = AutoStreamingUtils.create_auto_streaming_stats(
            self.streaming_gateway_ids
        )

        logging.info(
            f"AutoStreaming initialized for {len(self.streaming_gateway_ids)} streaming gateways"
        )

    def _discover_gateways_from_services(self):
        """Discover all streaming gateways from the provided service IDs."""
        discovered_gateway_ids = []

        for service_id in self.service_ids:
            try:
                gateway_manager = StreamingGatewayManager(
                    self.session, service_id=service_id
                )
                gateways, error, message = gateway_manager.get_streaming_gateways(
                    limit=100
                )

                if error:
                    logging.warning(
                        f"Failed to get gateways for service {service_id}: {error}"
                    )
                    continue

                if gateways:
                    gateway_ids = [g.id for g in gateways if g.id]
                    discovered_gateway_ids.extend(gateway_ids)
                    logging.info(
                        f"Discovered {len(gateway_ids)} gateways for service {service_id}"
                    )
                else:
                    logging.info(f"No gateways found for service {service_id}")

            except Exception as e:
                logging.error(
                    f"Error discovering gateways for service {service_id}: {e}"
                )

        logging.info(f"Total discovered gateways: {len(discovered_gateway_ids)}")
        return discovered_gateway_ids

    def setup_streaming_gateways_input_configs(self) -> Optional[Dict[str, List[InputConfig]]]:
        """
        Setup input configurations for each streaming gateway ID.

        Returns:
            bool: True if all gateway input configs were setup successfully, False otherwise
        """
        success_count = 0

        for gateway_id in self.streaming_gateway_ids:
            try:
                # Get gateway config to determine which service it belongs to
                gateway_manager = StreamingGatewayManager(self.session)
                gateway_config, error, message = (
                    gateway_manager.get_streaming_gateway_by_id(gateway_id)
                )
                if error:
                    error_msg = (
                        f"Failed to get gateway config for {gateway_id}: {error}"
                    )
                    logging.error(error_msg)
                    AutoStreamingUtils.record_error(self.stats, error_msg)
                    self.stats["failed_streams"][gateway_id] = error
                    continue

                # Validate gateway configuration
                is_valid, validation_error = (
                    AutoStreamingUtils.validate_streaming_gateway_config(gateway_config)
                )
                if not is_valid:
                    error_msg = (
                        f"Invalid gateway config for {gateway_id}: {validation_error}"
                    )
                    logging.error(error_msg)
                    AutoStreamingUtils.record_error(self.stats, error_msg)
                    self.stats["failed_streams"][gateway_id] = validation_error
                    continue

                self.gateway_configs[gateway_id] = gateway_config
                service_id = gateway_config.id_service

                # Extra diagnostics about the gateway configuration
                try:
                    logging.debug(
                        f"Gateway {gateway_id} config loaded | service_id={service_id} | "
                        f"camera_groups_count={len(getattr(gateway_config, 'camera_group_ids', []) )} | "
                        f"camera_groups={getattr(gateway_config, 'camera_group_ids', [])}"
                    )
                except Exception:
                    # Do not fail on logging issues
                    pass

                # Create camera manager with correct service_id for this gateway
                camera_manager = CameraManager(self.session, service_id=service_id)

                # Get camera input configurations for this gateway
                input_configs, error, message = (
                    self.utils.get_gateway_cameras_as_inputs(
                        camera_manager=camera_manager,
                        streaming_gateway_config_instance=gateway_config,
                        model_input_type=self.model_input_type,
                    )
                )

                if error:
                    error_msg = (
                        f"Failed to get camera inputs for gateway {gateway_id}: {error}"
                    )
                    logging.error(error_msg)
                    if message:
                        logging.debug(
                            f"Gateway {gateway_id} camera input fetch message: {message}"
                        )
                    AutoStreamingUtils.record_error(self.stats, error_msg)
                    self.stats["failed_streams"][gateway_id] = error
                    continue

                if not input_configs:
                    detailed_msg = (
                        message
                        if message
                        else f"No camera configurations found for gateway {gateway_id}"
                    )
                    logging.warning(
                        f"No camera configurations found for gateway {gateway_id} | "
                        f"service_id={service_id} | camera_groups={getattr(gateway_config, 'camera_group_ids', [])} | "
                        f"details={detailed_msg}"
                    )
                    self.stats["failed_streams"][gateway_id] = detailed_msg
                    continue

                # Store input configs for later use
                self.gateway_input_configs[gateway_id] = input_configs
                success_count += 1

                # Update statistics
                self.stats["camera_configs_loaded"] += len(input_configs)

                logging.info(
                    f"Setup input configs for gateway {gateway_id} with {len(input_configs)} cameras (deployment: {service_id})"
                )

            except Exception as e:
                error_msg = f"Failed to setup input configs for gateway {gateway_id}: {e}"
                logging.error(error_msg)
                AutoStreamingUtils.record_error(self.stats, error_msg)
                self.stats["failed_streams"][gateway_id] = str(e)

        if success_count == 0:
            logging.error("Failed to setup input configs for any streaming gateways")
            return None

        logging.info(
            f"Successfully setup input configs for {success_count}/{len(self.streaming_gateway_ids)} streaming gateways"
        )
        return self.gateway_input_configs
        
    def setup_streaming_gateways(self, gateway_input_configs: Dict[str, List[InputConfig]]=None) -> Dict[str, StreamingGateway]:
        """
        Setup StreamingGateway instances for each streaming gateway ID.

        Returns:
            bool: True if all gateways were setup successfully, False otherwise
        """
        if not gateway_input_configs:
            gateway_input_configs = self.setup_streaming_gateways_input_configs()
            if not gateway_input_configs:
                logging.error("Failed to setup streaming gateways input configs")
                return False

        success_count = 0

        for gateway_id in self.streaming_gateway_ids:
            try:
                # Check if we have gateway config and input configs
                if gateway_id not in self.gateway_configs:
                    error_msg = f"No gateway config found for {gateway_id}"
                    logging.error(error_msg)
                    AutoStreamingUtils.record_error(self.stats, error_msg)
                    self.stats["failed_streams"][gateway_id] = error_msg
                    continue

                if gateway_id not in self.gateway_input_configs:
                    error_msg = f"No input configs found for {gateway_id}"
                    logging.error(error_msg)
                    AutoStreamingUtils.record_error(self.stats, error_msg)
                    self.stats["failed_streams"][gateway_id] = error_msg
                    continue

                gateway_config = self.gateway_configs[gateway_id]
                input_configs = self.gateway_input_configs[gateway_id]
                service_id = gateway_config.id_service

                # Create StreamingGateway instance
                gateway = StreamingGateway(
                    session=self.session,
                    service_id=service_id,
                    output_config=self.output_configs,
                    inputs_config=input_configs,
                    result_callback=self.result_callback,
                    strip_input_from_result=self.strip_input_from_result,
                )

                self.streaming_gateways[gateway_id] = gateway
                success_count += 1

                # Update statistics
                AutoStreamingUtils.update_stream_status(
                    self.stats, gateway_id, "configured", len(input_configs)
                )

                logging.info(
                    f"Setup streaming gateway for {gateway_id} with {len(input_configs)} cameras (deployment: {service_id})"
                )

            except Exception as e:
                error_msg = f"Failed to setup streaming gateway for {gateway_id}: {e}"
                logging.error(error_msg)
                AutoStreamingUtils.record_error(self.stats, error_msg)
                self.stats["failed_streams"][gateway_id] = str(e)

        if success_count == 0:
            logging.error("Failed to setup any streaming gateways")

        logging.info(
            f"Successfully setup {success_count}/{len(self.streaming_gateway_ids)} streaming gateways"
        )

        return self.streaming_gateways

    def start(self, send_to_api: bool = False) -> bool:
        """
        Start auto streaming for all configured streaming gateways.

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
                logging.error("Failed to setup streaming gateways")
                return False

            # Start streaming for each gateway
            started_count = 0
            for gateway_id, gateway in self.streaming_gateways.items():
                try:
                    # Create and start streaming thread
                    thread = threading.Thread(
                        target=self._streaming_worker,
                        args=(gateway_id, gateway, send_to_api),
                        name=f"AutoStream-{gateway_id}",
                        daemon=True,
                    )

                    self.streaming_threads[gateway_id] = thread
                    thread.start()
                    started_count += 1

                    AutoStreamingUtils.update_stream_status(
                        self.stats, gateway_id, "starting", len(gateway.inputs_config)
                    )

                    logging.info(f"Started streaming thread for gateway: {gateway_id}")

                except Exception as e:
                    error_msg = (
                        f"Failed to start streaming for gateway {gateway_id}: {e}"
                    )
                    logging.error(error_msg)
                    AutoStreamingUtils.record_error(self.stats, error_msg)
                    self.stats["failed_streams"][gateway_id] = str(e)

            if started_count == 0:
                logging.error("Failed to start streaming for any gateway")
                return False

            self.is_running = True
            logging.info(
                f"Auto streaming started successfully for {started_count} streaming gateways"
            )
            return True

    def _streaming_worker(self, gateway_id: str, gateway: StreamingGateway, send_to_api: bool = False):
        """
        Worker thread for streaming a specific gateway.

        Args:
            gateway_id: Streaming gateway ID
            gateway: StreamingGateway instance
        """
        try:
            # Start streaming
            success = gateway.start_streaming(send_to_api=send_to_api)

            if success:
                AutoStreamingUtils.update_stream_status(
                    self.stats, gateway_id, "running"
                )
                logging.info(
                    f"Streaming started successfully for gateway: {gateway_id}"
                )

                # Keep the thread alive while streaming
                while not self._stop_event.is_set() and gateway.is_streaming:
                    time.sleep(1.0)

            else:
                error_msg = f"Failed to start streaming for gateway: {gateway_id}"
                logging.error(error_msg)
                AutoStreamingUtils.record_error(self.stats, error_msg)
                self.stats["failed_streams"][gateway_id] = "Failed to start streaming"

        except Exception as e:
            error_msg = f"Error in streaming worker for {gateway_id}: {e}"
            logging.error(error_msg)
            AutoStreamingUtils.record_error(self.stats, error_msg)
            self.stats["failed_streams"][gateway_id] = str(e)

        finally:
            # Update status
            AutoStreamingUtils.update_stream_status(self.stats, gateway_id, "stopped")
            logging.info(f"Streaming worker stopped for gateway: {gateway_id}")

    def stop(self):
        """Stop auto streaming for all gateways."""
        with self._state_lock:
            if not self.is_running:
                logging.warning("Auto streaming is not running")
                return

            logging.info("Stopping auto streaming...")
            self._stop_event.set()
            self.is_running = False

            # Stop all streaming gateways
            for gateway_id, gateway in self.streaming_gateways.items():
                try:
                    gateway.stop_streaming()
                    logging.info(f"Stopped streaming for gateway: {gateway_id}")
                except Exception as e:
                    logging.error(f"Error stopping streaming for {gateway_id}: {e}")

            # Wait for all threads to finish
            for gateway_id, thread in self.streaming_threads.items():
                try:
                    if thread.is_alive():
                        thread.join(timeout=10.0)
                        if thread.is_alive():
                            logging.warning(
                                f"Thread for {gateway_id} did not stop gracefully"
                            )
                except Exception as e:
                    logging.error(f"Error joining thread for {gateway_id}: {e}")

            # Clear state
            self.streaming_threads.clear()
            self.streaming_gateways.clear()
            self.gateway_configs.clear()

            # Update stats
            for gateway_id in self.stats["active_streams"]:
                AutoStreamingUtils.update_stream_status(
                    self.stats, gateway_id, "stopped"
                )

            logging.info("Auto streaming stopped successfully")

    def refresh_camera_configs(self) -> bool:
        """
        Refresh camera configurations for all streaming gateways.

        Returns:
            bool: True if configurations were refreshed successfully
        """
        if self.is_running:
            logging.warning(
                "Cannot refresh camera configs while auto streaming is running"
            )
            return False

        logging.info("Refreshing camera configurations...")
        return self.setup_streaming_gateways()

    def get_statistics(self) -> Dict:
        """
        Get auto streaming statistics.

        Returns:
            Dict with comprehensive statistics
        """
        with self._state_lock:
            stats = AutoStreamingUtils.calculate_runtime_stats(self.stats)

            # Add current status
            stats["is_running"] = self.is_running
            stats["active_gateways"] = len(self.streaming_gateways)
            stats["running_threads"] = sum(
                1 for t in self.streaming_threads.values() if t.is_alive()
            )

            return stats

    def get_gateway_status(self, gateway_id: str) -> Optional[Dict]:
        """
        Get status for a specific streaming gateway.

        Args:
            gateway_id: Streaming gateway ID

        Returns:
            Dict with gateway status or None if not found
        """
        if gateway_id not in self.streaming_gateways:
            return None

        gateway = self.streaming_gateways[gateway_id]
        thread = self.streaming_threads.get(gateway_id)
        gateway_config = self.gateway_configs.get(gateway_id)

        return {
            "gateway_id": gateway_id,
            "service_id": gateway_config.id_service if gateway_config else None,
            "gateway_name": gateway_config.name if gateway_config else None,
            "is_streaming": getattr(gateway, "is_streaming", False),
            "thread_alive": thread.is_alive() if thread else False,
            "input_count": len(gateway.inputs_config) if gateway.inputs_config else 0,
            "camera_groups": gateway_config.camera_group_ids if gateway_config else [],
            "active_stream_info": self.stats["active_streams"].get(gateway_id, {}),
            "failed_stream_info": self.stats["failed_streams"].get(gateway_id, None),
        }

    def add_streaming_gateway(self, gateway_id: str) -> bool:
        """
        Add a new streaming gateway to auto streaming.

        Args:
            gateway_id: ID of the streaming gateway to add

        Returns:
            bool: True if gateway was added successfully
        """
        if self.is_running:
            logging.warning("Cannot add gateway while auto streaming is running")
            return False

        if gateway_id in self.streaming_gateway_ids:
            logging.warning(f"Gateway {gateway_id} is already in the list")
            return False

        self.streaming_gateway_ids.append(gateway_id)
        self.stats["streaming_gateway_ids"] = self.streaming_gateway_ids
        self.stats["total_gateways"] = len(self.streaming_gateway_ids)

        logging.info(f"Added streaming gateway {gateway_id} to auto streaming")
        return True

    def remove_streaming_gateway(self, gateway_id: str) -> bool:
        """
        Remove a streaming gateway from auto streaming.

        Args:
            gateway_id: ID of the streaming gateway to remove

        Returns:
            bool: True if gateway was removed successfully
        """
        if self.is_running:
            logging.warning("Cannot remove gateway while auto streaming is running")
            return False

        if gateway_id not in self.streaming_gateway_ids:
            logging.warning(f"Gateway {gateway_id} is not in the list")
            return False

        self.streaming_gateway_ids.remove(gateway_id)
        self.stats["streaming_gateway_ids"] = self.streaming_gateway_ids
        self.stats["total_gateways"] = len(self.streaming_gateway_ids)

        # Clean up any stored configs
        if gateway_id in self.gateway_configs:
            del self.gateway_configs[gateway_id]

        logging.info(f"Removed streaming gateway {gateway_id} from auto streaming")
        return True

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
