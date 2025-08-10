"""Auto streaming utility class for camera configuration and input conversion."""

import logging
import time
from typing import Dict, List, Optional, Tuple

from matrice.deployment.camera_manager import Camera, CameraGroup, CameraManager
from matrice.deployment.streaming_gateway_manager import StreamingGateway
from matrice.deploy.client.streaming_gateway import ModelInputType, InputConfig, InputType


class AutoStreamingUtils:
    """
    Utility class for auto streaming camera configuration and input conversion.
    
    This class provides methods for converting camera configurations to input configurations,
    managing streaming statistics, and validating gateway configurations.
    """

    def __init__(
        self,
        default_fps: int = 30,
        default_quality: int = 80,
        default_video_chunk_duration: int = 10,
        default_video_format: str = "mp4",
        simulate_video_file_stream: bool = False,
    ):
        """
        Initialize AutoStreamingUtils with default configuration values.

        Args:
            default_fps: Default FPS for camera streams
            default_quality: Default quality for camera streams
            default_video_chunk_duration: Default video chunk duration for video input type
            default_video_format: Default video format for video input type
            simulate_video_file_stream: Whether to simulate video file stream
        """
        self.default_fps = default_fps
        self.default_quality = default_quality
        self.default_video_chunk_duration = default_video_chunk_duration
        self.default_video_format = default_video_format
        self.simulate_video_file_stream = simulate_video_file_stream

    def convert_camera_configs_to_inputs(
        self,
        camera_configs: List[Camera], 
        camera_groups: Dict[str, CameraGroup],
        deployment_id: str,
        model_input_type: ModelInputType = ModelInputType.FRAMES
    ) -> List[InputConfig]:
        """
        Convert camera configurations to input configurations for streaming.

        Args:
            camera_configs: List of Camera instance objects
            camera_groups: Dictionary mapping group IDs to CameraGroupInstance objects
            deployment_id: Deployment ID for logging
            model_input_type: Model input type (FRAMES or VIDEO)

        Returns:
            List of InputConfig objects
        """
        input_configs = []

        for camera_config in camera_configs:
            try:
                # Get camera group for effective settings
                camera_group = camera_groups.get(camera_config.camera_group_id)
                if not camera_group:
                    logging.warning(
                        f"Camera group {camera_config.camera_group_id} not found for camera {camera_config.camera_name}"
                    )
                    continue

                # Get effective stream settings
                effective_settings = camera_config.get_effective_stream_settings(
                    camera_group.default_stream_settings
                )

                # Diagnostics about each camera before building input config
                logging.debug(
                    (
                        "Preparing input for camera name=%s id=%s group_id=%s | "
                        "stream_url_present=%s | effective_settings={fps:%s, quality:%s, width:%s, height:%s}"
                    ),
                    getattr(camera_config, 'camera_name', None),
                    getattr(camera_config, 'id', None),
                    getattr(camera_config, 'camera_group_id', None),
                    bool(getattr(camera_config, 'stream_url', None)),
                    getattr(effective_settings, 'fps', None),
                    getattr(effective_settings, 'video_quality', None),
                    getattr(effective_settings, 'width', None),
                    getattr(effective_settings, 'height', None),
                )

                if not getattr(camera_config, 'stream_url', None):
                    logging.warning(
                        f"Camera {getattr(camera_config, 'camera_name', None)} has no stream_url; skipping"
                    )
                    continue

                input_config = InputConfig(
                    type=InputType.AUTO,
                    source=camera_config.stream_url,
                    fps=effective_settings.fps if effective_settings.fps > 0 else self.default_fps,
                    stream_key=f"{camera_config.camera_name}",
                    stream_group_key=f"{camera_config.camera_group_id}",
                    quality=(
                        effective_settings.video_quality
                        if effective_settings.video_quality > 0
                        else self.default_quality
                    ),
                    width=effective_settings.width if effective_settings.width > 0 else None,
                    height=effective_settings.height if effective_settings.height > 0 else None,
                    model_input_type=model_input_type,
                    video_duration=self.default_video_chunk_duration,
                    video_format=self.default_video_format,
                    simulate_video_file_stream=self.simulate_video_file_stream,
                )

                input_configs.append(input_config)

                logging.info(
                    f"Added camera input for {deployment_id}: {camera_config.camera_name} "
                    f"({camera_config.stream_url}) from group {camera_group.name}"
                )

            except Exception as e:
                logging.error(
                    f"Failed to create input config for camera {camera_config.camera_name} in {deployment_id}: {e}"
                )
                continue

        return input_configs

    def get_camera_configs_as_inputs(
        self,
        camera_manager: CameraManager,
        deployment_id: str,
        model_input_type: ModelInputType = ModelInputType.FRAMES
    ) -> Tuple[Optional[List[InputConfig]], Optional[str], str]:
        """
        Get camera configurations for a deployment and convert them to input configurations.
        
        This method fetches both camera groups and camera configs, then converts them
        to input configs using effective stream settings.

        Args:
            camera_manager: CameraManager instance
            deployment_id: The ID of the deployment to get camera configs for
            model_input_type: Model input type (FRAMES or VIDEO)

        Returns:
            tuple: (input_configs, error, message)
        """
        # Get camera groups
        camera_groups_list, error, message = camera_manager.get_camera_groups(limit=100)
        if error:
            return None, error, message

        # Convert to dictionary for easy lookup
        camera_groups = {group.id: group for group in camera_groups_list}
        
        # Get camera configurations
        camera_configs, error, message = camera_manager.get_cameras(limit=100)
        if error:
            return None, error, message
        
        if not camera_configs:
            return [], None, "No camera configurations found for deployment"
        
        # Convert to input configurations
        try:
            input_configs = self.convert_camera_configs_to_inputs(
                camera_configs=camera_configs,
                camera_groups=camera_groups,
                deployment_id=deployment_id,
                model_input_type=model_input_type
            )
            
            return input_configs, None, f"Successfully converted {len(input_configs)} camera configs to input configs"
            
        except Exception as e:
            error_msg = f"Failed to convert camera configs to input configs: {str(e)}"
            logging.error(error_msg)
            return None, error_msg, "Conversion failed"

    def get_gateway_cameras_as_inputs(
        self,
        camera_manager: CameraManager,
        streaming_gateway_config_instance: StreamingGateway,
        model_input_type: ModelInputType = ModelInputType.FRAMES
    ) -> Tuple[Optional[List[InputConfig]], Optional[str], str]:
        """
        Get camera configurations for a specific streaming gateway and convert to input configs.

        Args:
            camera_manager: CameraManager instance to use for camera operations
            streaming_gateway_config_instance: StreamingGateway instance to use for gateway operations
            model_input_type: Model input type (FRAMES or VIDEO)

        Returns:
            tuple: (input_configs, error, message)
        """
        # Get cameras from all camera groups in this gateway
        camera_configs = []
        group_id_list = list(getattr(streaming_gateway_config_instance, 'camera_group_ids', []) or [])
        logging.debug(
            f"Fetching cameras for gateway={getattr(streaming_gateway_config_instance, 'id', None)} "
            f"service_id={getattr(streaming_gateway_config_instance, 'id_service', None)} "
            f"groups_count={len(group_id_list)} groups={group_id_list}"
        )
        for group_id in group_id_list:
            group_cameras, error, message = camera_manager.get_cameras(group_id=group_id, limit=100)
            if error:
                logging.warning(f"Failed to get cameras for group {group_id}: {error} | message={message}")
                continue
            logging.debug(
                f"Group {group_id}: fetched_cameras={len(group_cameras) if group_cameras else 0}"
            )
            if group_cameras:
                camera_configs.extend(group_cameras)
        
        if not camera_configs:
            return [], None, (
                f"No cameras found for gateway {getattr(streaming_gateway_config_instance, 'id', None)}. "
                f"Checked groups={group_id_list}. Ensure cameras are assigned and visible to the deployment."
            )

        # Get camera groups for the deployment
        camera_groups_list, error, message = camera_manager.get_camera_groups(limit=100)
        if error:
            logging.error(
                f"Failed to get camera groups for service_id={getattr(streaming_gateway_config_instance, 'id_service', None)}: {error} | message={message}"
            )
            return None, error, message

        # Convert to dictionary for easy lookup
        camera_groups = {group.id: group for group in camera_groups_list}
        logging.debug(
            f"Camera groups available: {len(camera_groups)} | ids={list(camera_groups.keys())}"
        )

        # Convert to input configurations
        try:
            input_configs = self.convert_camera_configs_to_inputs(
                camera_configs=camera_configs,
                camera_groups=camera_groups,
                deployment_id=streaming_gateway_config_instance.id_service,
                model_input_type=model_input_type
            )

            return input_configs, None, (
                f"Successfully converted {len(input_configs)} camera configs to input configs for gateway "
                f"{getattr(streaming_gateway_config_instance, 'id', None)}"
            )

        except Exception as e:
            error_msg = (
                f"Failed to convert camera configs to input configs for gateway "
                f"{getattr(streaming_gateway_config_instance, 'id', None)}: {str(e)}"
            )
            logging.error(error_msg)
            return None, error_msg, "Conversion failed"

    @staticmethod
    def create_auto_streaming_stats(streaming_gateway_ids: List[str]) -> Dict:
        """
        Create initial statistics dictionary for auto streaming.

        Args:
            streaming_gateway_ids: List of streaming gateway IDs

        Returns:
            Dictionary with initial statistics
        """
        return {
            "enabled": True,
            "streaming_gateway_ids": streaming_gateway_ids,
            "active_streams": {},
            "failed_streams": {},
            "total_gateways": len(streaming_gateway_ids),
            "camera_configs_loaded": 0,
            "start_time": None,
            "errors": 0,
            "last_error": None,
            "last_error_time": None,
        }

    @staticmethod
    def record_error(stats: Dict, error_message: str):
        """
        Record an error in statistics.

        Args:
            stats: Statistics dictionary
            error_message: Error message to record
        """
        stats["errors"] += 1
        stats["last_error"] = error_message
        stats["last_error_time"] = time.time()

    @staticmethod
    def update_stream_status(stats: Dict, gateway_id: str, status: str, camera_count: int = None):
        """
        Update the status of a streaming gateway in statistics.

        Args:
            stats: Statistics dictionary
            gateway_id: ID of the streaming gateway
            status: New status (starting, running, stopped, failed)
            camera_count: Number of cameras (optional)
        """
        if status in ["starting", "running"]:
            if gateway_id not in stats["active_streams"]:
                stats["active_streams"][gateway_id] = {}
            
            stats["active_streams"][gateway_id]["status"] = status
            if camera_count is not None:
                stats["active_streams"][gateway_id]["cameras"] = camera_count
            if status == "starting":
                stats["active_streams"][gateway_id]["start_time"] = time.time()
        
        elif status in ["stopped", "failed"]:
            if gateway_id in stats["active_streams"]:
                stats["active_streams"][gateway_id]["status"] = status

    @staticmethod
    def calculate_runtime_stats(stats: Dict) -> Dict:
        """
        Calculate runtime statistics.

        Args:
            stats: Statistics dictionary

        Returns:
            Updated statistics dictionary with runtime information
        """
        result_stats = stats.copy()
        
        # Calculate runtime
        if result_stats["start_time"]:
            runtime = time.time() - result_stats["start_time"]
            result_stats["runtime_seconds"] = runtime
        else:
            result_stats["runtime_seconds"] = 0

        return result_stats

    @staticmethod
    def validate_streaming_gateway_config(gateway_config) -> Tuple[bool, str]:
        """
        Validate streaming gateway configuration.

        Args:
            gateway_config:  object

        Returns:
            tuple: (is_valid, error_message)
        """
        if not gateway_config:
            return False, "Gateway configuration is None"

        if not gateway_config.id_service:
            return False, "No deployment ID found in gateway configuration"

        if not gateway_config.camera_group_ids:
            return False, "No camera group IDs found in gateway configuration"

        return True, ""
