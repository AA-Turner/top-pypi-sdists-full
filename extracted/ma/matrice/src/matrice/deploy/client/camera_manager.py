"""Module providing camera manager functionality for deployments."""

from typing import Dict, List, Optional , Tuple
from dataclasses import dataclass, asdict


@dataclass
class CameraConfig:
    """
    Camera configuration data class.
    
    Attributes:
        id: Unique identifier for the camera config (MongoDB ObjectID)
        id_service: Deployment ID this camera config belongs to (MongoDB ObjectID)
        camera_location: Physical location description of the camera
        stream_url: URL for the camera stream
        stream_key: Authentication key for the stream
        aspect_ratio: Aspect ratio of the camera (e.g., "16:9", "4:3")
        video_quality: Video quality setting (0-100)
        height: Video height in pixels
        width: Video width in pixels  
        fps: Frames per second
    """
    camera_location: str
    stream_url: str
    stream_key: str
    aspect_ratio: str
    video_quality: int
    height: int
    width: int
    fps: int
    id: Optional[str] = None
    id_service: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert the camera config to a dictionary for API calls."""
        data = asdict(self)
        # Convert snake_case to camelCase for API compatibility
        api_data = {
            "cameraLocation": data["camera_location"],
            "streamUrl": data["stream_url"],
            "streamKey": data["stream_key"],
            "aspectRatio": data["aspect_ratio"],
            "videoQuality": data["video_quality"],
            "height": data["height"],
            "width": data["width"],
            "fps": data["fps"]
        }
        if data["id"]:
            api_data["id"] = data["id"]
        if data["id_service"]:
            api_data["idService"] = data["id_service"]
        return api_data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'CameraConfig':
        """Create a CameraConfig instance from API response data."""
        return cls(
            id=data.get("id"),
            id_service=data.get("idService"),
            camera_location=data.get("cameraLocation", ""),
            stream_url=data.get("streamUrl", ""),
            stream_key=data.get("streamKey", ""),
            aspect_ratio=data.get("aspectRatio", ""),
            video_quality=data.get("videoQuality", 0),
            height=data.get("height", 0),
            width=data.get("width", 0),
            fps=data.get("fps", 0)
        )


class CameraManager:
    """
    Camera manager client for handling camera configurations in deployments.
    
    This class provides methods to create, read, update, and delete camera configurations
    associated with deployments.
    
    Example:
        Basic usage:
        ```python
        from matrice import Session
        from matrice.deploy.client.camera_manager import CameraManager, CameraConfig
        
        session = Session(account_number="...", access_key="...", secret_key="...")
        camera_manager = CameraManager(session)
        
        # Create a camera config
        config = CameraConfig(
            camera_location="Front Door",
            stream_url="rtsp://camera1.example.com:554/stream",
            stream_key="auth_key_123",
            aspect_ratio="16:9",
            video_quality=80,
            height=1080,
            width=1920,
            fps=30
        )
        
        result, error, message = camera_manager.add_camera_config("deployment_id", config)
        if error:
            print(f"Error: {error}")
        else:
            print(f"Camera config added: {result}")
        
        # Get camera configs for a deployment
        configs, error, message = camera_manager.get_camera_configs_by_deployment_id("deployment_id")
        if not error:
            for config in configs:
                print(f"Camera: {config.camera_location}")
        ```
    """
    
    def __init__(self, session):
        """
        Initialize the CameraManager client.
        
        Args:
            session: Session object containing RPC client for API communication
        """
        self.session = session
        self.rpc = session.rpc
    
    def handle_response(self, response: Dict, success_message: str, failure_message: str) -> Tuple[Optional[Dict], Optional[str], str]:
        if response and response.get("success"):
            result = response.get("data")
            error = None
            message = success_message
        else:
            result = None
            error = response.get("message") if response else "No response received"
            message = failure_message
        return result, error, message
    
    def add_camera_config(self, deployment_id: str, config: CameraConfig) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Add a new camera configuration to a deployment.
        
        Args:
            deployment_id: The ID of the deployment to add the camera config to
            config: CameraConfig object containing the camera configuration
            
        Returns:
            tuple: (result, error, message)
                - result: API response data if successful, None otherwise
                - error: Error message if failed, None otherwise  
                - message: Status message
                
        Example:
            >>> config = CameraConfig(
            ...     camera_location="Main Entrance",
            ...     stream_url="rtsp://192.168.1.100:554/stream1",
            ...     stream_key="abc123",
            ...     aspect_ratio="16:9",
            ...     video_quality=85,
            ...     height=1080,
            ...     width=1920,
            ...     fps=25
            ... )
            >>> result, error, message = camera_mgmt.add_camera_config("deploy123", config)
        """
        if not deployment_id:
            return None, "Deployment ID is required", "Invalid deployment ID"
        
        if not isinstance(config, CameraConfig):
            return None, "Config must be a CameraConfig instance", "Invalid config type"
        
        path = f"/v1/deployment/add_camera/{deployment_id}"
        payload = config.to_dict()
        headers = {"Content-Type": "application/json"}
        
        resp = self.rpc.post(path=path, headers=headers, payload=payload)
        return self.handle_response(
            resp,
            "Camera config added successfully",
            "Failed to add camera config"
        )
    
    def get_camera_config_by_id(self, config_id: str) -> Tuple[Optional[CameraConfig], Optional[str], str]:
        """
        Get a camera configuration by its ID.
        
        Args:
            config_id: The ID of the camera configuration to retrieve
            
        Returns:
            tuple: (camera_config, error, message)
                - camera_config: CameraConfig object if successful, None otherwise
                - error: Error message if failed, None otherwise
                - message: Status message
                
        Example:
            >>> config, error, message = camera_mgmt.get_camera_config_by_id("config123")
            >>> if not error:
            ...     print(f"Camera location: {config.camera_location}")
        """
        if not config_id:
            return None, "Config ID is required", "Invalid config ID"
        
        path = f"/v1/deployment/get_camera/{config_id}"
        resp = self.rpc.get(path=path)
        
        result, error, message = self.handle_response(
            resp,
            "Camera config retrieved successfully",
            "Failed to retrieve camera config"
        )
        
        if error:
            return None, error, message
        
        if result:
            try:
                camera_config = CameraConfig.from_dict(result)
                return camera_config, None, message
            except Exception as e:
                return None, f"Failed to parse camera config: {str(e)}", "Parse error"
        
        return None, "No camera config data received", message
    
    def get_camera_configs_by_deployment_id(self, deployment_id: str) -> Tuple[Optional[List[CameraConfig]], Optional[str], str]:
        """
        Get all camera configurations for a specific deployment.
        
        Args:
            deployment_id: The ID of the deployment to get camera configs for
            
        Returns:
            tuple: (camera_configs, error, message)
                - camera_configs: List of CameraConfig objects if successful, None otherwise
                - error: Error message if failed, None otherwise
                - message: Status message
                
        Example:
            >>> configs, error, message = camera_mgmt.get_camera_configs_by_deployment_id("deploy123")
            >>> if not error:
            ...     for config in configs:
            ...         print(f"Camera: {config.camera_location} - {config.stream_url}")
        """
        if not deployment_id:
            return None, "Deployment ID is required", "Invalid deployment ID"
        
        path = f"/v1/deployment/get_cameras/{deployment_id}"
        resp = self.rpc.get(path=path)
        
        result, error, message = self.handle_response(
            resp,
            "Camera configs retrieved successfully",
            "Failed to retrieve camera configs"
        )
        
        if error:
            return None, error, message
        
        if result:
            try:
                if isinstance(result, list):
                    camera_configs = [CameraConfig.from_dict(config_data) for config_data in result]
                    return camera_configs, None, message
                else:
                    return None, "Expected list of camera configs", "Invalid response format"
            except Exception as e:
                return None, f"Failed to parse camera configs: {str(e)}", "Parse error"
        
        return [], None, message  # Return empty list if no configs found
    
    def update_camera_config(self, config_id: str, config: CameraConfig) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update an existing camera configuration.
        
        Args:
            config_id: The ID of the camera configuration to update
            config: CameraConfig object with updated configuration
            
        Returns:
            tuple: (result, error, message)
                - result: API response data if successful, None otherwise
                - error: Error message if failed, None otherwise
                - message: Status message
                
        Example:
            >>> config.video_quality = 90  # Update quality
            >>> result, error, message = camera_mgmt.update_camera_config("config123", config)
        """
        if not config_id:
            return None, "Config ID is required", "Invalid config ID"
        
        if not isinstance(config, CameraConfig):
            return None, "Config must be a CameraConfig instance", "Invalid config type"
        
        path = f"/v1/deployment/update_camera/{config_id}"
        payload = config.to_dict()
        headers = {"Content-Type": "application/json"}
        
        resp = self.rpc.put(path=path, headers=headers, payload=payload)
        return self.handle_response(
            resp,
            "Camera config updated successfully",
            "Failed to update camera config"
        )
    
    def delete_camera_config_by_id(self, config_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Delete a camera configuration by its ID.
        
        Args:
            config_id: The ID of the camera configuration to delete
            
        Returns:
            tuple: (result, error, message)
                - result: API response data if successful, None otherwise
                - error: Error message if failed, None otherwise
                - message: Status message
                
        Example:
            >>> result, error, message = camera_mgmt.delete_camera_config_by_id("config123")
            >>> if not error:
            ...     print("Camera config deleted successfully")
        """
        if not config_id:
            return None, "Config ID is required", "Invalid config ID"
        
        path = f"/v1/deployment/delete_camera/{config_id}"
        resp = self.rpc.delete(path=path)
        
        return self.handle_response(
            resp,
            "Camera config deleted successfully",
            "Failed to delete camera config"
        )
    
    def delete_camera_configs_by_deployment_id(self, deployment_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Delete all camera configurations for a specific deployment.
        
        Args:
            deployment_id: The ID of the deployment to delete all camera configs for
            
        Returns:
            tuple: (result, error, message)
                - result: API response data if successful, None otherwise
                - error: Error message if failed, None otherwise
                - message: Status message
                
        Example:
            >>> result, error, message = camera_mgmt.delete_camera_configs_by_deployment_id("deploy123")
            >>> if not error:
            ...     print("All camera configs deleted successfully")
        """
        if not deployment_id:
            return None, "Deployment ID is required", "Invalid deployment ID"
        
        path = f"/v1/deployment/delete_cameras/{deployment_id}"
        resp = self.rpc.delete(path=path)
        
        return self.handle_response(
            resp,
            "Camera configs deleted successfully",
            "Failed to delete camera configs"
        )
    
    def list_camera_configs(self, deployment_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        List all camera configurations for a deployment in a simple dictionary format.
        
        This is a convenience method that returns raw dictionary data instead of CameraConfig objects.
        
        Args:
            deployment_id: The ID of the deployment to list camera configs for
            
        Returns:
            tuple: (configs_list, error, message)
                - configs_list: List of camera config dictionaries if successful, None otherwise
                - error: Error message if failed, None otherwise
                - message: Status message
                
        Example:
            >>> configs, error, message = camera_mgmt.list_camera_configs("deploy123")
            >>> if not error:
            ...     for config in configs:
            ...         print(f"ID: {config['id']}, Location: {config['cameraLocation']}")
        """
        camera_configs, error, message = self.get_camera_configs_by_deployment_id(deployment_id)
        
        if error:
            return None, error, message
        
        if camera_configs:
            config_dicts = [config.to_dict() for config in camera_configs]
            return config_dicts, None, message
        
        return [], None, message

