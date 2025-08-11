"""Module providing camera manager functionality for deployments."""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict


@dataclass
class StreamSettings:
    """
    Stream settings data class for camera configurations.

    Attributes:
        aspect_ratio: Aspect ratio of the camera (e.g., "16:9", "4:3")
        video_quality: Video quality setting (0-100)
        height: Video height in pixels
        width: Video width in pixels
        fps: Frames per second
    """

    aspect_ratio: str
    video_quality: int
    height: int
    width: int
    fps: int

    def to_dict(self) -> Dict:
        """Convert the stream settings to a dictionary for API calls."""
        return {
            "aspectRatio": self.aspect_ratio,
            "videoQuality": self.video_quality,
            "height": self.height,
            "width": self.width,
            "fps": self.fps,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "StreamSettings":
        """Create a StreamSettings instance from API response data."""
        return cls(
            aspect_ratio=data.get("aspectRatio", ""),
            video_quality=data.get("videoQuality", 0),
            height=data.get("height", 0),
            width=data.get("width", 0),
            fps=data.get("fps", 0),
        )


@dataclass
class CameraGroupConfig:
    """
    Camera group data class for managing collections of cameras with shared settings.

    Attributes:
        id: Unique identifier for the camera group (MongoDB ObjectID)
        id_service: Deployment ID this group belongs to (MongoDB ObjectID)
        name: Name of the camera group
        location: Physical location description of the group
        default_stream_settings: Default stream settings for cameras in this group
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    name: str
    location: str
    default_stream_settings: StreamSettings
    id: Optional[str] = None
    id_service: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert the camera group to a dictionary for API calls."""
        data = {
            "name": self.name,
            "location": self.location,
            "defaultStreamSettings": self.default_stream_settings.to_dict(),
        }
        if self.id:
            data["_id"] = self.id
        if self.id_service:
            data["idService"] = self.id_service
        return data

    @classmethod
    def from_dict(cls, data: Dict) -> "CameraGroupConfig":
        """Create a CameraGroup instance from API response data."""
        default_settings = StreamSettings.from_dict(
            data.get("defaultStreamSettings", {})
        )
        return cls(
            id=data.get("_id") or data.get("id") or data.get("ID"),
            id_service=data.get("idService") or data.get("IDService"),
            name=data.get("name") or data.get("Name"),
            location=data.get("location") or data.get("Location"),
            default_stream_settings=default_settings,
            created_at=data.get("createdAt") or data.get("CreatedAt"),
            updated_at=data.get("updatedAt") or data.get("UpdatedAt"),
        )


@dataclass
class CameraConfig:
    """
    Camera configuration data class.

    Attributes:
        id: Unique identifier for the camera config (MongoDB ObjectID)
        id_service: Deployment ID this camera config belongs to (MongoDB ObjectID)
        camera_group_id: ID of the camera group this camera belongs to
        is_stream_url: Whether the stream URL is a valid URL
        camera_name: Name/identifier for the camera
        stream_url: URL for the camera stream
        custom_stream_settings: Custom stream settings that override group defaults
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    camera_name: str
    stream_url: str
    camera_group_id: str
    is_stream_url: bool
    custom_stream_settings: Optional[Dict] = None
    id: Optional[str] = None
    id_service: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        if self.custom_stream_settings is None:
            self.custom_stream_settings = {}

    def to_dict(self) -> Dict:
        """Convert the camera config to a dictionary for API calls."""
        data = {
            "cameraName": self.camera_name,
            "streamUrl": self.stream_url,
            "cameraGroupId": self.camera_group_id,
            "isStreamURL": self.is_stream_url,
            "customStreamSettings": self.custom_stream_settings,
        }
        if self.id:
            data["_id"] = self.id
        if self.id_service:
            data["idService"] = self.id_service
        return data

    @classmethod
    def from_dict(cls, data: Dict) -> "CameraConfig":
        """Create a CameraConfig instance from API response data."""
        camera_group_id = (
            data.get("CameraGroupID")
            or data.get("cameraGroupId")
            or data.get("groupId")
            or data.get("GroupId")
        )

        instance = cls(
            id=data.get("ID") or data.get("id") or data.get("_id"),
            id_service=data.get("IDService") or data.get("idService"),
            camera_group_id=camera_group_id,
            camera_name=data.get("CameraName") or data.get("cameraName"),
            stream_url=data.get("StreamURL") or data.get("streamUrl"),
            is_stream_url=data.get("IsStreamURL")
            or data.get("isStreamURL")
            or data.get("isStreamUrl"),
            custom_stream_settings=data.get("CustomStreamSettings")
            or data.get("customStreamSettings"),
            created_at=data.get("CreatedAt") or data.get("createdAt"),
            updated_at=data.get("UpdatedAt") or data.get("updatedAt"),
        )

        # Emit a debug diagnostic if camera_group_id could not be parsed
        if instance.camera_group_id in (None, ""):
            try:
                logging.debug(
                    "CameraConfig.from_dict: missing camera_group_id in payload keys=%s",
                    list(data.keys()),
                )
            except Exception:
                pass

        return instance

    def get_effective_stream_settings(
        self, group_defaults: StreamSettings
    ) -> StreamSettings:
        """
        Get the effective stream settings by merging group defaults with custom overrides.

        Args:
            group_defaults: Default stream settings from the camera group

        Returns:
            StreamSettings with effective values
        """
        # Start with group defaults
        effective = asdict(group_defaults)

        # Override with custom settings (convert camelCase to snake_case)
        custom_mapping = {
            "aspectRatio": "aspect_ratio",
            "videoQuality": "video_quality",
            "height": "height",
            "width": "width",
            "fps": "fps",
        }

        for api_key, attr_name in custom_mapping.items():
            if api_key in self.custom_stream_settings and self.custom_stream_settings[api_key]:
                effective[attr_name] = self.custom_stream_settings[api_key]

        return StreamSettings(**effective)


class Camera:
    """
    Camera instance class for managing individual camera configurations.

    This class represents a single camera and provides methods to manage
    its configuration, stream settings, and operational status.

    Example:
        Basic usage:
        ```python
        from matrice import Session
        from matrice.deployment.camera_manager import Camera, CameraConfig

        session = Session(account_number="...", access_key="...", secret_key="...")

        # Create camera config
        config = CameraConfig(
            camera_name="entrance_cam_01",
            stream_url="rtsp://192.168.1.100:554/stream1",
            camera_group_id="group_id_123",
            custom_stream_settings={"videoQuality": 90}
        )

        # Create camera instance
        camera = Camera(session, config)

        # Save to backend
        result, error, message = camera.save(service_id="deployment_id")
        if not error:
            print(f"Camera created with ID: {camera.id}")

        # Update configuration
        camera.stream_url = "rtsp://192.168.1.101:554/stream1"
        result, error, message = camera.update()
        ```
    """

    def __init__(self, session, config: CameraConfig = None, camera_id: str = None):
        """
        Initialize a Camera instance.

        Args:
            session: Session object containing RPC client for API communication
            config: CameraConfig object (for new cameras)
            camera_id: ID of existing camera to load (mutually exclusive with config)
        """
        if not config and not camera_id:
            raise ValueError("Either config or camera_id must be provided")

        self.session = session
        self.rpc = session.rpc

        if camera_id:
            # Load existing camera
            self.config = None
            self._load_from_id(camera_id)
        else:
            # New camera from config
            self.config = config

    @property
    def id(self) -> Optional[str]:
        """Get the camera ID."""
        return self.config.id if self.config else None

    @property
    def camera_name(self) -> str:
        """Get the camera name."""
        return self.config.camera_name if self.config else ""

    @camera_name.setter
    def camera_name(self, value: str):
        """Set the camera name."""
        if self.config:
            self.config.camera_name = value

    @property
    def stream_url(self) -> str:
        """Get the camera stream URL."""
        return self.get_stream_url()

    @stream_url.setter
    def stream_url(self, value: str):
        """Set the camera stream URL."""
        if self.config:
            self.config.stream_url = value

    @property
    def is_stream_url(self) -> bool:
        """Get whether the camera stream URL is a valid URL."""
        return self.config.is_stream_url if self.config else False

    @is_stream_url.setter
    def is_stream_url(self, value: bool):
        """Set whether the camera stream URL is a valid URL."""
        if self.config:
            self.config.is_stream_url = value

    @property
    def camera_group_id(self) -> str:
        """Get the camera group ID."""
        return self.config.camera_group_id if self.config else ""

    @camera_group_id.setter
    def camera_group_id(self, value: str):
        """Set the camera group ID."""
        if self.config:
            self.config.camera_group_id = value

    @property
    def custom_stream_settings(self) -> Dict:
        """Get the custom stream settings."""
        return self.config.custom_stream_settings if self.config else {}

    @custom_stream_settings.setter
    def custom_stream_settings(self, value: Dict):
        """Set the custom stream settings."""
        if self.config:
            self.config.custom_stream_settings = value

    def _load_from_id(self, camera_id: str):
        """Load camera configuration from backend by ID."""
        path = f"/v1/inference/get_camera/{camera_id}"
        resp = self.rpc.get(path=path)

        if resp and resp.get("success"):
            data = resp.get("data")
            if data:
                self.config = CameraConfig.from_dict(data)
            else:
                raise ValueError(f"No data found for camera ID: {camera_id}")
        else:
            error_msg = resp.get("message") if resp else "No response received"
            raise ValueError(f"Failed to load camera: {error_msg}")

    def save(self, service_id: str = None) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Save the camera configuration to the backend (create new).

        Args:
            service_id: The deployment or inference pipeline ID to associate with

        Returns:
            tuple: (result, error, message)
        """
        if not self.config:
            return None, "No configuration to save", "Invalid state"

        if self.id:
            return None, "Camera already exists, use update() instead", "Already exists"

        if service_id:
            self.config.id_service = service_id

        if not self.config.id_service:
            return None, "Service ID is required", "Missing service ID"

        # Validate camera config
        is_valid, validation_error = self._validate_camera_config()
        if not is_valid:
            return None, validation_error, "Validation failed"

        path = f"/v1/inference/add_cameras/{self.config.id_service}"
        payload = [self.config.to_dict()]  # Backend expects array

        resp = self.rpc.post(path=path, payload=payload)

        if resp and resp.get("success"):
            result = resp.get("data")
            # Extract camera ID from response if available
            if result and isinstance(result, list) and len(result) > 0:
                camera_data = result[0]
                if "_id" in camera_data:
                    self.config.id = camera_data["_id"]
            return result, None, "Camera created successfully"
        else:
            error = resp.get("message") if resp else "No response received"
            return None, error, "Failed to create camera"

    def update(self) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update the camera configuration in the backend.

        Returns:
            tuple: (result, error, message)
        """
        if not self.config or not self.config.id:
            return None, "Camera must be saved before updating", "Invalid state"

        path = f"/v1/inference/update_camera/{self.config.id}"
        payload = self.config.to_dict()

        resp = self.rpc.put(path=path, payload=payload)

        if resp and resp.get("success"):
            result = resp.get("data")
            return result, None, "Camera updated successfully"
        else:
            error = resp.get("message") if resp else "No response received"
            return None, error, "Failed to update camera"

    def delete(self) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Delete the camera from the backend.

        Returns:
            tuple: (result, error, message)
        """
        if not self.config or not self.config.id:
            return None, "Camera must be saved before deleting", "Invalid state"

        path = f"/v1/inference/delete_camera/{self.config.id}"

        resp = self.rpc.delete(path=path)

        if resp and resp.get("success"):
            result = resp.get("data")
            return result, None, "Camera deleted successfully"
        else:
            error = resp.get("message") if resp else "No response received"
            return None, error, "Failed to delete camera"

    def get_stream_url(self) -> str:
        """Get the camera stream URL."""
        if not self.config.id:
            return ""
        if self.config.is_stream_url:
            return self.config.stream_url

        resp = self.rpc.get(f"/v1/inference/get_stream_url/{self.config.id}")
        if resp and resp.get("success") and resp.get("data"):
            self.config.stream_url = resp.get("data", {}).get("streamUrl")
            self.config.is_stream_url = True

        return self.config.stream_url

    def get_effective_stream_settings(
        self, group_defaults: StreamSettings
    ) -> StreamSettings:
        """
        Get the effective stream settings by merging group defaults with custom overrides.

        Args:
            group_defaults: Default stream settings from the camera group

        Returns:
            StreamSettings with effective values
        """
        if self.config:
            return self.config.get_effective_stream_settings(group_defaults)
        return group_defaults

    def refresh(self):
        """Refresh the camera configuration from the backend."""
        if self.config and self.config.id:
            self._load_from_id(self.config.id)

    def _validate_camera_config(self) -> Tuple[bool, str]:
        """
        Validate camera configuration data.

        Returns:
            tuple: (is_valid, error_message)
        """
        if not self.config:
            return False, "No configuration to validate"

        if not self.config.camera_name or not self.config.camera_name.strip():
            return False, "Camera name is required"

        if not self.config.stream_url or not self.config.stream_url.strip():
            return False, "Stream URL is required"

        if not self.config.camera_group_id:
            return False, "Camera group ID is required"

        # Validate custom stream settings if provided
        if self.config.custom_stream_settings:
            custom = self.config.custom_stream_settings

            if "aspectRatio" in custom and custom["aspectRatio"] not in [
                "16:9",
                "4:3",
                "1:1",
            ]:
                return False, "Custom aspect ratio must be one of: 16:9, 4:3, 1:1"

            if "videoQuality" in custom and not (0 <= custom["videoQuality"] <= 100):
                return False, "Custom video quality must be between 0 and 100"

            if "height" in custom and custom["height"] <= 0:
                return False, "Custom height must be greater than 0"

            if "width" in custom and custom["width"] <= 0:
                return False, "Custom width must be greater than 0"

            if "fps" in custom and custom["fps"] <= 0:
                return False, "Custom FPS must be greater than 0"

        return True, ""


class CameraGroup:
    """
    Camera group instance class for managing individual camera groups and their cameras.

    This class represents a single camera group and provides methods to manage
    its configuration, cameras, and operational status.

    Example:
        Basic usage:
        ```python
        from matrice import Session
        from matrice.deployment.camera_manager import CameraGroup, CameraGroup, StreamSettings

        session = Session(account_number="...", access_key="...", secret_key="...")

        # Create camera group config
        default_settings = StreamSettings(
            aspect_ratio="16:9",
            video_quality=80,
            height=1080,
            width=1920,
            fps=30
        )

        group_config = CameraGroupConfig(
            name="Indoor Cameras",
            location="Building A - First Floor",
            default_stream_settings=default_settings
        )

        # Create camera group instance
        camera_group = CameraGroup(session, group_config)

        # Save to backend
        result, error, message = camera_group.save(service_id="deployment_id")
        if not error:
            print(f"Camera group created with ID: {camera_group.id}")

        # Add cameras to the group
        camera_config = CameraConfig(
            camera_name="entrance_cam_01",
            stream_url="rtsp://192.168.1.100:554/stream1",
            camera_group_id=camera_group.id
        )
        camera, error, message = camera_group.add_camera(camera_config)
        ```
    """

    def __init__(self, session, config: CameraGroupConfig = None, group_id: str = None):
        """
        Initialize a CameraGroup.

        Args:
            session: Session object containing RPC client for API communication
            config: CameraGroup object (for new groups)
            group_id: ID of existing group to load (mutually exclusive with config)
        """
        if not config and not group_id:
            raise ValueError("Either config or group_id must be provided")

        self.session = session
        self.rpc = session.rpc
        self._cameras = []  # Cache for cameras in this group

        if group_id:
            # Load existing group
            self.config = None
            self._load_from_id(group_id)
        else:
            # New group from config
            self.config = config

    @property
    def id(self) -> Optional[str]:
        """Get the group ID."""
        return self.config.id if self.config else None

    @property
    def name(self) -> str:
        """Get the group name."""
        return self.config.name if self.config else ""

    @name.setter
    def name(self, value: str):
        """Set the group name."""
        if self.config:
            self.config.name = value

    @property
    def location(self) -> str:
        """Get the group location."""
        return self.config.location if self.config else ""

    @location.setter
    def location(self, value: str):
        """Set the group location."""
        if self.config:
            self.config.location = value

    @property
    def default_stream_settings(self) -> Optional[StreamSettings]:
        """Get the default stream settings."""
        return self.config.default_stream_settings if self.config else None

    @default_stream_settings.setter
    def default_stream_settings(self, value: StreamSettings):
        """Set the default stream settings."""
        if self.config:
            self.config.default_stream_settings = value

    @property
    def cameras(self) -> List["Camera"]:
        """Get all cameras in this group."""
        return self._cameras

    def _load_from_id(self, group_id: str):
        """Load camera group configuration from backend by ID."""
        path = f"/v1/inference/camera_group/{group_id}"
        resp = self.rpc.get(path=path)

        if resp and resp.get("success"):
            data = resp.get("data")
            if data:
                self.config = CameraGroupConfig.from_dict(data)
            else:
                raise ValueError(f"No data found for camera group ID: {group_id}")
        else:
            error_msg = resp.get("message") if resp else "No response received"
            raise ValueError(f"Failed to load camera group: {error_msg}")

    def save(self, service_id: str = None) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Save the camera group configuration to the backend (create new).

        Args:
            service_id: The deployment or inference pipeline ID to associate with

        Returns:
            tuple: (result, error, message)
        """
        if not self.config:
            return None, "No configuration to save", "Invalid state"

        if self.id:
            return (
                None,
                "Camera group already exists, use update() instead",
                "Already exists",
            )

        if service_id:
            self.config.id_service = service_id

        if not self.config.id_service:
            return None, "Service ID is required", "Missing service ID"

        # Validate camera group
        is_valid, validation_error = self._validate_camera_group()
        if not is_valid:
            return None, validation_error, "Validation failed"

        path = "/v1/inference/camera_group"
        payload = self.config.to_dict()
        payload["idService"] = self.config.id_service

        resp = self.rpc.post(path=path, payload=payload)

        if resp and resp.get("success"):
            result = resp.get("data")
            if result and "_id" in result:
                self.config.id = result["_id"]
            return result, None, "Camera group created successfully"
        else:
            error = resp.get("message") if resp else "No response received"
            return None, error, "Failed to create camera group"

    def update(self) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update the camera group configuration in the backend.

        Returns:
            tuple: (result, error, message)
        """
        if not self.config or not self.config.id:
            return None, "Camera group must be saved before updating", "Invalid state"

        path = f"/v1/inference/camera_group/{self.config.id}"
        payload = self.config.to_dict()

        resp = self.rpc.put(path=path, payload=payload)

        if resp and resp.get("success"):
            result = resp.get("data")
            return result, None, "Camera group updated successfully"
        else:
            error = resp.get("message") if resp else "No response received"
            return None, error, "Failed to update camera group"

    def delete(self) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Delete the camera group from the backend.

        Returns:
            tuple: (result, error, message)
        """
        if not self.config or not self.config.id:
            return None, "Camera group must be saved before deleting", "Invalid state"

        path = f"/v1/inference/camera_group/{self.config.id}"

        resp = self.rpc.delete(path=path)

        if resp and resp.get("success"):
            result = resp.get("data")
            return result, None, "Camera group deleted successfully"
        else:
            error = resp.get("message") if resp else "No response received"
            return None, error, "Failed to delete camera group"

    def add_camera(
        self, camera_config: CameraConfig
    ) -> Tuple[Optional["Camera"], Optional[str], str]:
        """
        Add a camera to this camera group.

        Args:
            camera_config: CameraConfig object containing the camera configuration

        Returns:
            tuple: (camera_instance, error, message)
        """
        if not self.config or not self.config.id:
            return (
                None,
                "Camera group must be saved before adding cameras",
                "Invalid state",
            )

        if not isinstance(camera_config, CameraConfig):
            return None, "Config must be a CameraConfig instance", "Invalid config type"

        # Set the camera group ID
        camera_config.camera_group_id = self.config.id
        camera_config.id_service = self.config.id_service

        # Create camera instance
        camera_instance = Camera(self.session, camera_config)

        # Save to backend
        result, error, message = camera_instance.save()

        if error:
            return None, error, message

        # Add to local cache
        self._cameras.append(camera_instance)

        return camera_instance, None, message

    def get_cameras(
        self, page: int = 1, limit: int = 10, search: str = None
    ) -> Tuple[Optional[List["Camera"]], Optional[str], str]:
        """
        Get all cameras in this camera group.

        Args:
            page: Page number for pagination
            limit: Items per page
            search: Optional search term

        Returns:
            tuple: (camera_instances, error, message)
        """
        if not self.config or not self.config.id:
            return (
                None,
                "Camera group must be saved before getting cameras",
                "Invalid state",
            )

        if not self.config.id_service:
            return None, "Service ID is required", "Missing service ID"

        path = f"/v1/inference/get_cameras/{self.config.id_service}"
        params = {"page": page, "limit": limit, "groupId": self.config.id}
        if search:
            params["search"] = search

        resp = self.rpc.get(path=path, params=params)

        if resp and resp.get("success"):
            result = resp.get("data")
            if result and "items" in result:
                try:
                    camera_instances = []
                    for config_data in result["items"]:
                        try:
                            camera_config = CameraConfig.from_dict(config_data)
                            if camera_config.camera_group_id != self.config.id:
                                continue
                            camera_instance = Camera(self.session, camera_config)
                            camera_instances.append(camera_instance)
                        except Exception as e:
                            logging.warning(f"Failed to parse camera config data: {e}")
                            continue

                    # Update local cache
                    self._cameras = camera_instances
                    return camera_instances, None, "Cameras retrieved successfully"
                except Exception as e:
                    return (
                        None,
                        f"Failed to parse camera configs: {str(e)}",
                        "Parse error",
                    )

            return [], None, "No cameras found"
        else:
            error = resp.get("message") if resp else "No response received"
            return None, error, "Failed to retrieve cameras"

    def remove_camera(
        self, camera_id: str
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Remove a camera from this camera group.

        Args:
            camera_id: ID of the camera to remove

        Returns:
            tuple: (result, error, message)
        """
        if not camera_id:
            return None, "Camera ID is required", "Invalid camera ID"

        path = f"/v1/inference/delete_camera/{camera_id}"
        resp = self.rpc.delete(path=path)

        if resp and resp.get("success"):
            result = resp.get("data")
            # Remove from local cache
            self._cameras = [cam for cam in self._cameras if cam.id != camera_id]
            return result, None, "Camera removed successfully"
        else:
            error = resp.get("message") if resp else "No response received"
            return None, error, "Failed to remove camera"

    def refresh(self):
        """Refresh the camera group configuration and cameras from the backend."""
        if self.config and self.config.id:
            self._load_from_id(self.config.id)
            # Refresh cameras list
            self.get_cameras()

    def _validate_camera_group(self) -> Tuple[bool, str]:
        """
        Validate camera group data.

        Returns:
            tuple: (is_valid, error_message)
        """
        if not self.config:
            return False, "No configuration to validate"

        if not self.config.name or not self.config.name.strip():
            return False, "Camera group name is required"

        if not self.config.location or not self.config.location.strip():
            return False, "Camera group location is required"

        # Validate stream settings
        settings = self.config.default_stream_settings
        if settings.aspect_ratio not in ["16:9", "4:3", "1:1"]:
            return False, "Aspect ratio must be one of: 16:9, 4:3, 1:1"

        if not (0 <= settings.video_quality <= 100):
            return False, "Video quality must be between 0 and 100"

        if settings.height <= 0:
            return False, "Height must be greater than 0"

        if settings.width <= 0:
            return False, "Width must be greater than 0"

        if settings.fps <= 0:
            return False, "FPS must be greater than 0"

        return True, ""


class CameraManager:
    """
    Camera manager client for handling camera groups and configurations in deployments.

    This class provides methods to create, read, update, and delete camera groups and
    camera configurations associated with deployments. It offers a streamlined flow
    for managing camera infrastructure.

    Example:
        Basic usage:
        ```python
        from matrice import Session
        from matrice.deployment.camera_manager import CameraManager, CameraGroup, CameraConfig, StreamSettings

        session = Session(account_number="...", access_key="...", secret_key="...")
        camera_manager = CameraManager(session, service_id="...")

        # Create a camera group with default settings
        default_settings = StreamSettings(
            aspect_ratio="16:9",
            video_quality=80,
            height=1080,
            width=1920,
            fps=30
        )

        group = CameraGroup(
            name="Indoor Cameras",
            location="Building A - First Floor",
            default_stream_settings=default_settings
        )

        # Create the camera group
        camera_group, error, message = camera_manager.create_camera_group(group)
        if error:
            print(f"Error: {error}")
        else:
            print(f"Camera group created: {camera_group.name}")

            # Add cameras to the group
            camera_config = CameraConfig(
                camera_name="main_entrance_cam",
                stream_url="rtsp://192.168.1.100:554/stream1",
                camera_group_id=camera_group.id,
                custom_stream_settings={"videoQuality": 90}
            )

            camera, error, message = camera_group.add_camera(camera_config)
            if not error:
                print(f"Camera added: {camera.camera_name}")
        ```
    """

    def __init__(self, session, service_id: str = None):
        """
        Initialize the CameraManager client.

        Args:
            session: Session object containing RPC client for API communication
            service_id: The ID of the deployment or the ID of the inference pipeline
        """
        self.session = session
        self.rpc = session.rpc
        self.service_id = service_id

    def handle_response(
        self, response: Dict, success_message: str, failure_message: str
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """Handle API response and return standardized tuple."""
        if response and response.get("success"):
            result = response.get("data")
            error = None
            message = success_message
        else:
            result = None
            error = response.get("message") if response else "No response received"
            message = failure_message
        return result, error, message

    # Camera Group Management Methods

    def create_camera_group(
        self, group: CameraGroupConfig
    ) -> Tuple[Optional["CameraGroup"], Optional[str], str]:
        """
        Create a new camera group for a deployment.

        Args:
            group: CameraGroup object containing the group configuration

        Returns:
            tuple: (camera_group_instance, error, message)
                - camera_group_instance: CameraGroupInstance if successful, None otherwise
                - error: Error message if failed, None otherwise
                - message: Status message
        """
        if not isinstance(group, CameraGroupConfig):
            return None, "Group must be a CameraGroup instance", "Invalid group type"

        # Create camera group instance
        camera_group_instance = CameraGroup(self.session, group)

        # Save to backend
        result, error, message = camera_group_instance.save(service_id=self.service_id)

        if error:
            return None, error, message

        return camera_group_instance, None, message

    def get_camera_group_by_id(
        self, group_id: str
    ) -> Tuple[Optional["CameraGroup"], Optional[str], str]:
        """
        Get a camera group by its ID.

        Args:
            group_id: The ID of the camera group to retrieve

        Returns:
            tuple: (camera_group_instance, error, message)
        """
        if not group_id:
            return None, "Group ID is required", "Invalid group ID"

        try:
            camera_group_instance = CameraGroup(self.session, group_id=group_id)
            return camera_group_instance, None, "Camera group retrieved successfully"
        except Exception as e:
            return None, str(e), "Failed to retrieve camera group"

    def get_camera_groups(
        self, page: int = 1, limit: int = 10, search: str = None
    ) -> Tuple[Optional[List["CameraGroup"]], Optional[str], str]:
        """
        Get all camera groups for a specific deployment.

        Args:
            page: Page number for pagination
            limit: Items per page
            search: Optional search term

        Returns:
            tuple: (camera_group_instances, error, message)
        """
        if not self.service_id:
            return None, "Service ID is required", "Invalid service ID"

        path = f"/v1/inference/camera_groups/{self.service_id}"
        params = {"page": page, "limit": limit}
        if search:
            params["search"] = search

        resp = self.rpc.get(path=path, params=params)

        result, error, message = self.handle_response(
            resp,
            "Camera groups retrieved successfully",
            "Failed to retrieve camera groups",
        )

        if error:
            return None, error, message

        if result and "items" in result:
            try:
                camera_group_instances = []
                for group_data in result["items"]:
                    try:
                        group_config = CameraGroupConfig.from_dict(group_data)
                        camera_group_instance = CameraGroup(self.session, group_config)
                        camera_group_instances.append(camera_group_instance)
                    except Exception as e:
                        logging.warning(f"Failed to parse camera group data: {e}")
                        continue

                logging.debug(
                    "get_camera_groups: service_id=%s page=%s limit=%s -> groups=%s",
                    self.service_id,
                    page,
                    limit,
                    len(camera_group_instances),
                )
                return camera_group_instances, None, message
            except Exception as e:
                return None, f"Failed to parse camera groups: {str(e)}", "Parse error"

        return [], None, message

    def update_camera_group(
        self, group_id: str, group: CameraGroupConfig
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update an existing camera group.

        Args:
            group_id: The ID of the camera group to update
            group: CameraGroup object with updated configuration

        Returns:
            tuple: (result, error, message)
        """
        if not group_id:
            return None, "Group ID is required", "Invalid group ID"

        if not isinstance(group, CameraGroupConfig):
            return None, "Group must be a CameraGroup instance", "Invalid group type"

        path = f"/v1/inference/camera_group/{group_id}"
        payload = group.to_dict()

        resp = self.rpc.put(path=path, payload=payload)
        return self.handle_response(
            resp, "Camera group updated successfully", "Failed to update camera group"
        )

    def delete_camera_group(
        self, group_id: str
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Delete a camera group by its ID.

        Args:
            group_id: The ID of the camera group to delete

        Returns:
            tuple: (result, error, message)
        """
        if not group_id:
            return None, "Group ID is required", "Invalid group ID"

        path = f"/v1/inference/camera_group/{group_id}"
        resp = self.rpc.delete(path=path)

        return self.handle_response(
            resp, "Camera group deleted successfully", "Failed to delete camera group"
        )

    # Camera Management Methods

    def create_camera(
        self, camera_config: CameraConfig
    ) -> Tuple[Optional["Camera"], Optional[str], str]:
        """
        Create a new camera configuration.

        Args:
            camera_config: CameraConfig object containing the camera configuration

        Returns:
            tuple: (camera_instance, error, message)
        """
        if not isinstance(camera_config, CameraConfig):
            return None, "Config must be a CameraConfig instance", "Invalid config type"

        # Create camera instance
        camera_instance = Camera(self.session, camera_config)

        # Save to backend
        result, error, message = camera_instance.save(service_id=self.service_id)

        if error:
            return result, error, message

        return camera_instance, None, message

    def get_camera_by_id(
        self, camera_id: str
    ) -> Tuple[Optional["Camera"], Optional[str], str]:
        """
        Get a camera by its ID.

        Args:
            camera_id: The ID of the camera to retrieve

        Returns:
            tuple: (camera_instance, error, message)
        """
        if not camera_id:
            return None, "Camera ID is required", "Invalid camera ID"

        try:
            camera_instance = Camera(self.session, camera_id=camera_id)
            return camera_instance, None, "Camera retrieved successfully"
        except Exception as e:
            return None, str(e), "Failed to retrieve camera"

    def list_camera_configs(
        self, page: int = 1, limit: int = 10, search: str = None, group_id: str = None
    ) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        List all camera configs for a specific deployment.

        Returns:
            tuple: (camera_configs, error, message)
        """
        if not self.service_id:
            return None, "Service ID is required", "Invalid service ID"

        path = f"/v1/inference/get_cameras/{self.service_id}"
        params = {"page": page, "limit": limit}
        if search:
            params["search"] = search
        if group_id:
            params["groupId"] = group_id

        resp = self.rpc.get(path=path, params=params)

        result, error, message = self.handle_response(
            resp, "Cameras retrieved successfully", "Failed to retrieve cameras"
        )

        if error:
            return None, error, message

        if result and "items" in result:
            cameras_list = result["items"]
            logging.debug(
                "list_camera_configs: service_id=%s page=%s limit=%s group_id=%s -> cameras=%s",
                self.service_id,
                page,
                limit,
                group_id,
                len(cameras_list),
            )
            return cameras_list, None, message

        return [], None, message

    def get_cameras(
        self, page: int = 1, limit: int = 10, search: str = None, group_id: str = None
    ) -> Tuple[Optional[List["Camera"]], Optional[str], str]:
        """
        Get all cameras for a specific deployment.

        Args:
            page: Page number for pagination
            limit: Items per page
            search: Optional search term
            group_id: Optional filter by camera group ID

        Returns:
            tuple: (camera_instances, error, message)
        """
        logging.debug(
            "get_cameras: service_id=%s page=%s limit=%s group_id=%s search=%s",
            self.service_id,
            page,
            limit,
            group_id,
            search,
        )
        cameras, error, message = self.list_camera_configs(
            page=page, limit=limit, search=search, group_id=group_id
        )
        if error:
            return None, error, message

        camera_instances = []
        for config_data in cameras:
            try:
                camera_config = CameraConfig.from_dict(config_data)
                if group_id and camera_config.camera_group_id != group_id:
                    continue
                camera_instance = Camera(self.session, camera_config)
                camera_instances.append(camera_instance)
            except Exception as e:
                logging.warning(f"Failed to parse camera config data: {e}")
                continue

        logging.debug(
            "get_cameras: built_instances=%s (after parsing/filtering)",
            len(camera_instances),
        )
        return camera_instances, None, message

    def get_stream_url(
        self, config_id: str
    ) -> Tuple[Optional[str], Optional[str], str]:
        """
        Get the stream URL for a camera configuration.

        Args:
            config_id: The ID of the camera configuration

        Returns:
            tuple: (stream_url, error, message)
        """
        if not config_id:
            return None, "Config ID is required", "Invalid config ID"

        path = f"/v1/inference/get_stream_url/{config_id}"
        resp = self.rpc.get(path=path)
        result, error, message = self.handle_response(
            resp, "Stream URL retrieved successfully", "Failed to retrieve stream URL"
        )
        return result, error, message

    def update_camera(
        self, camera_id: str, camera_config: CameraConfig
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update an existing camera configuration.

        Args:
            camera_id: The ID of the camera to update
            camera_config: CameraConfig object with updated configuration

        Returns:
            tuple: (result, error, message)
        """
        if not camera_id:
            return None, "Camera ID is required", "Invalid camera ID"

        if not isinstance(camera_config, CameraConfig):
            return None, "Config must be a CameraConfig instance", "Invalid config type"

        path = f"/v1/inference/update_camera/{camera_id}"
        payload = camera_config.to_dict()

        resp = self.rpc.put(path=path, payload=payload)
        return self.handle_response(
            resp, "Camera updated successfully", "Failed to update camera"
        )

    def delete_camera(
        self, camera_id: str
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Delete a camera by its ID.

        Args:
            camera_id: The ID of the camera to delete

        Returns:
            tuple: (result, error, message)
        """
        if not camera_id:
            return None, "Camera ID is required", "Invalid camera ID"

        path = f"/v1/inference/delete_camera/{camera_id}"
        resp = self.rpc.delete(path=path)

        return self.handle_response(
            resp, "Camera deleted successfully", "Failed to delete camera"
        )

    def delete_all_cameras(
        self, confirm: bool = False
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Delete all cameras for a specific deployment.

        Args:
            confirm: Must be True to confirm bulk deletion

        Returns:
            tuple: (result, error, message)
        """
        if not self.service_id:
            return None, "Service ID is required", "Invalid service ID"

        if not confirm:
            return (
                None,
                "Must confirm bulk deletion by setting confirm=True",
                "Confirmation required",
            )

        path = f"/v1/inference/delete_cameras/{self.service_id}"
        params = {"confirm": "true"}
        resp = self.rpc.delete(path=path, params=params)

        return self.handle_response(
            resp, "All cameras deleted successfully", "Failed to delete cameras"
        )

    # Bulk Operations

    def add_cameras_to_group(
        self, group_id: str, camera_configs: List[CameraConfig]
    ) -> Tuple[Optional[List["Camera"]], Optional[str], str]:
        """
        Add multiple cameras to a camera group.

        Args:
            group_id: The ID of the camera group
            camera_configs: List of CameraConfig objects

        Returns:
            tuple: (camera_instances, error, message)
        """
        if not group_id:
            return None, "Group ID is required", "Invalid group ID"

        if not camera_configs:
            return None, "Camera configs are required", "Invalid configs"

        if not all(isinstance(config, CameraConfig) for config in camera_configs):
            return (
                None,
                "All configs must be CameraConfig instances",
                "Invalid config types",
            )

        # Set camera group ID for all configs
        for config in camera_configs:
            config.camera_group_id = group_id
            config.id_service = self.service_id

        # Validate all camera configs
        for i, config in enumerate(camera_configs):
            is_valid, validation_error = self._validate_camera_config(config)
            if not is_valid:
                return None, f"Config {i+1}: {validation_error}", "Validation failed"

        path = f"/v1/inference/add_cameras/{self.service_id}"
        payload = [config.to_dict() for config in camera_configs]

        resp = self.rpc.post(path=path, payload=payload)
        result, error, message = self.handle_response(
            resp,
            "Cameras added to group successfully",
            "Failed to add cameras to group",
        )

        if error:
            return None, error, message

        # Create camera instances
        camera_instances = []
        for config in camera_configs:
            camera_instance = Camera(self.session, config)
            camera_instances.append(camera_instance)

        return camera_instances, None, message

    def _validate_camera_group(self, group: CameraGroupConfig) -> Tuple[bool, str]:
        """
        Validate camera group data before API calls.

        Args:
            group: CameraGroup object to validate

        Returns:
            tuple: (is_valid, error_message)
        """
        if not group.name or not group.name.strip():
            return False, "Camera group name is required"

        if not group.location or not group.location.strip():
            return False, "Camera group location is required"

        # Validate stream settings
        settings = group.default_stream_settings
        if settings.aspect_ratio not in ["16:9", "4:3", "1:1"]:
            return False, "Aspect ratio must be one of: 16:9, 4:3, 1:1"

        if not (0 <= settings.video_quality <= 100):
            return False, "Video quality must be between 0 and 100"

        if settings.height <= 0:
            return False, "Height must be greater than 0"

        if settings.width <= 0:
            return False, "Width must be greater than 0"

        if settings.fps <= 0:
            return False, "FPS must be greater than 0"

        return True, ""

    def _validate_camera_config(self, config: CameraConfig) -> Tuple[bool, str]:
        """
        Validate camera configuration data before API calls.

        Args:
            config: CameraConfig object to validate

        Returns:
            tuple: (is_valid, error_message)
        """
        if not config.camera_name or not config.camera_name.strip():
            return False, "Camera name is required"

        if not config.stream_url or not config.stream_url.strip():
            return False, "Stream URL is required"

        if not config.camera_group_id:
            return False, "Camera group ID is required"

        # Validate custom stream settings if provided
        if config.custom_stream_settings:
            custom = config.custom_stream_settings

            if "aspectRatio" in custom and custom["aspectRatio"] not in [
                "16:9",
                "4:3",
                "1:1",
            ]:
                return False, "Custom aspect ratio must be one of: 16:9, 4:3, 1:1"

            if "videoQuality" in custom and not (0 <= custom["videoQuality"] <= 100):
                return False, "Custom video quality must be between 0 and 100"

            if "height" in custom and custom["height"] <= 0:
                return False, "Custom height must be greater than 0"

            if "width" in custom and custom["width"] <= 0:
                return False, "Custom width must be greater than 0"

            if "fps" in custom and custom["fps"] <= 0:
                return False, "Custom FPS must be greater than 0"

        return True, ""

    # Legacy method aliases for backward compatibility
    def add_camera_config(
        self, config: CameraConfig
    ) -> Tuple[Optional["Camera"], Optional[str], str]:
        """Legacy method - use create_camera instead."""
        return self.create_camera(config)

    def get_camera_config_by_id(
        self, config_id: str
    ) -> Tuple[Optional["Camera"], Optional[str], str]:
        """Legacy method - use get_camera_by_id instead."""
        return self.get_camera_by_id(config_id)

    def get_camera_configs(
        self, page: int = 1, limit: int = 10, search: str = None, group_id: str = None
    ) -> Tuple[Optional[List["Camera"]], Optional[str], str]:
        """Legacy method - use get_cameras instead."""
        return self.get_cameras(page, limit, search, group_id)

    def update_camera_config(
        self, config_id: str, config: CameraConfig
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """Legacy method - use update_camera instead."""
        return self.update_camera(config_id, config)

    def delete_camera_config_by_id(
        self, config_id: str
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """Legacy method - use delete_camera instead."""
        return self.delete_camera(config_id)

    def delete_camera_configs(
        self, confirm: bool = False
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """Legacy method - use delete_all_cameras instead."""
        return self.delete_all_cameras(confirm)

    def add_camera_configs(
        self, configs: List[CameraConfig]
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """Legacy method - use add_cameras_to_group instead."""
        if not configs:
            return None, "Camera configs are required", "Invalid configs"

        # Use the first config's group ID
        group_id = configs[0].camera_group_id if configs else None
        if not group_id:
            return None, "Camera group ID is required", "Invalid group ID"

        cameras, error, message = self.add_cameras_to_group(group_id, configs)
        if error:
            return None, error, message

        return {"cameras": [cam.config.to_dict() for cam in cameras]}, None, message
