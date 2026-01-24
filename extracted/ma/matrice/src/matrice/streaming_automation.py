"""
Automated script for creating and managing streaming gateways, cameras, and inference pipelines.
Uses Session and RPC classes for authentication and API communication.
"""

import os
import json
import time
import uuid
import random
import string
import mimetypes
from typing import Optional, Dict, List, Any, Tuple, Union
from pathlib import Path
from urllib.parse import urlparse
import requests

# Import Session and RPC classes
try:
    from matrice_common.session import Session
    from matrice_common.rpc import RPC
except ImportError:
    # Fallback if running from different directory structure
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), 'py_common', 'src'))
    from matrice_common.session import Session
    from matrice_common.rpc import RPC


class StreamingAutomation:
    """
    Class to automate the creation and management of streaming gateways,
    cameras, locations, camera groups, and inference pipelines.
    """

    def __init__(
        self,
        account_number: str,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        project_id: Optional[str] = None,
        project_name: Optional[str] = None,
    ):
        """
        Initialize the automation class with session credentials.

        Parameters
        ----------
        account_number : str
            The account number for the Matrice account
        access_key : str, optional
            Access key for authentication (or set MATRICE_ACCESS_KEY_ID env var)
        secret_key : str, optional
            Secret key for authentication (or set MATRICE_SECRET_ACCESS_KEY env var)
        project_id : str, optional
            Project ID to use
        project_name : str, optional
            Project name to use (will fetch project_id if provided)
        """
        self.account_number = account_number
        self.session = Session(
            account_number=account_number,
            access_key=access_key,
            secret_key=secret_key,
            project_id=project_id,
            project_name=project_name,
        )
        self.rpc = self.session.rpc

    @staticmethod
    def _generate_tag(prefix: str = "auto") -> str:
        """
        Generate a random tag with prefix and UUID.

        Parameters
        ----------
        prefix : str
            Prefix for the tag (default: "auto")

        Returns
        -------
        str : Generated tag
        """
        # Use UUID to avoid any naming conflicts
        unique_id = str(uuid.uuid4())[:8]
        return f"{prefix}-{unique_id}"

    @staticmethod
    def _generate_id() -> str:
        """
        Generate a random ID.

        Returns
        -------
        str : Generated ID
        """
        return str(uuid.uuid4())

    @staticmethod
    def _is_valid_id(value: str) -> bool:
        """
        Check if a string looks like a valid MongoDB ObjectId.
        MongoDB IDs are 24 character hexadecimal strings.

        Parameters
        ----------
        value : str
            String to check

        Returns
        -------
        bool : True if it looks like a valid ID, False otherwise
        """
        if not value or not isinstance(value, str):
            return False
        # Check if it's 24 characters long and contains only hex characters
        return len(value) == 24 and all(c in '0123456789abcdefABCDEF' for c in value)

    @staticmethod
    def _parse_cameras(cameras_input: Union[str, Dict, List[Dict]]) -> List[Dict[str, Any]]:
        """
        Parse cameras input from various formats (JSON string, dict, list of dicts).

        Parameters
        ----------
        cameras_input : str, dict, or list of dicts
            Cameras data in various formats

        Returns
        -------
        list : List of camera dictionaries
        """
        if isinstance(cameras_input, str):
            # Try to parse as JSON
            try:
                parsed = json.loads(cameras_input)
                if isinstance(parsed, list):
                    return parsed
                elif isinstance(parsed, dict):
                    # If single dict, check if it's a list wrapper
                    if "cameras" in parsed:
                        return parsed["cameras"]
                    elif "items" in parsed:
                        return parsed["items"]
                    else:
                        return [parsed]
                else:
                    return []
            except json.JSONDecodeError:
                # Try reading as file path
                try:
                    with open(cameras_input, 'r') as f:
                        content = f.read()
                        parsed = json.loads(content)
                        if isinstance(parsed, list):
                            return parsed
                        elif isinstance(parsed, dict):
                            if "cameras" in parsed:
                                return parsed["cameras"]
                            elif "items" in parsed:
                                return parsed["items"]
                            else:
                                return [parsed]
                        return []
                except Exception:
                    raise ValueError(f"Could not parse cameras input: {cameras_input}")
        elif isinstance(cameras_input, dict):
            # Single camera dict
            return [cameras_input]
        elif isinstance(cameras_input, list):
            # List of cameras
            return cameras_input
        else:
            raise ValueError(f"Unsupported cameras input type: {type(cameras_input)}")

    @staticmethod
    def _extract_camera_info(cameras: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract location and camera group information from camera data.

        Parameters
        ----------
        cameras : list of dicts
            List of camera dictionaries

        Returns
        -------
        dict : Extracted information with location, camera_group defaults
        """
        info = {
            "location_name": None,
            "location_info": {
                "streetAddress": "",
                "city": "",
                "state": "",
                "country": "",
            },
            "camera_group_name": None,
        }

        # Try to extract from first camera
        if cameras:
            first_camera = cameras[0]

            # Extract location info
            if "location" in first_camera:
                loc = first_camera["location"]
                if isinstance(loc, dict):
                    info["location_name"] = loc.get("name") or loc.get("locationName")
                    if "locationInfo" in loc:
                        info["location_info"].update(loc["locationInfo"])
                    elif "info" in loc:
                        info["location_info"].update(loc["info"])

            if "locationName" in first_camera:
                info["location_name"] = first_camera["locationName"]
            if "locationInfo" in first_camera:
                info["location_info"].update(first_camera["locationInfo"])

            # Extract camera group info
            if "cameraGroup" in first_camera:
                cg = first_camera["cameraGroup"]
                if isinstance(cg, dict):
                    info["camera_group_name"] = cg.get("name") or cg.get("cameraGroupName")
            if "cameraGroupName" in first_camera:
                info["camera_group_name"] = first_camera["cameraGroupName"]

        # Generate defaults if not found
        if not info["location_name"]:
            info["location_name"] = StreamingAutomation._generate_tag("loc")
        if not info["camera_group_name"]:
            info["camera_group_name"] = StreamingAutomation._generate_tag("cg")

        return info

    @staticmethod
    def _is_local_file(path: str) -> bool:
        """
        Check if a path is a local file.

        Parameters
        ----------
        path : str
            Path to check

        Returns
        -------
        bool : True if local file, False otherwise
        """
        if not path:
            return False

        # Check if it's a URL
        try:
            parsed = urlparse(path)
            if parsed.scheme in ['http', 'https', 's3', 'gs', 'ftp', 'ftps']:
                return False
        except Exception:
            pass

        # Check if file exists locally
        return Path(path).exists() and Path(path).is_file()

    @staticmethod
    def _is_video_file(path: str) -> bool:
        """
        Check if a path is a video file.

        Parameters
        ----------
        path : str
            Path to check

        Returns
        -------
        bool : True if video file, False otherwise
        """
        if not path:
            return False

        video_extensions = [
            '.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm',
            '.m4v', '.mpg', '.mpeg', '.3gp', '.f4v', '.ts'
        ]

        path_lower = path.lower()
        for ext in video_extensions:
            if path_lower.endswith(ext):
                return True

        # Also check MIME type if available
        mime_type, _ = mimetypes.guess_type(path)
        if mime_type and mime_type.startswith('video/'):
            return True

        return False

    @staticmethod
    def _is_rtsp_url(path: str) -> bool:
        """
        Check if a path is an RTSP URL.

        Parameters
        ----------
        path : str
            Path to check

        Returns
        -------
        bool : True if RTSP URL, False otherwise
        """
        if not path:
            return False
        return path.lower().startswith('rtsp://')

    @staticmethod
    def _detect_protocol_type(path: str) -> str:
        """
        Automatically detect protocol type from path.

        Parameters
        ----------
        path : str
            Path to analyze

        Returns
        -------
        str : "RTSP" or "FILE"
        """
        if not path:
            return "RTSP"  # Default

        # Check for RTSP URL
        if StreamingAutomation._is_rtsp_url(path):
            return "RTSP"

        # Check for video file (local or remote)
        if StreamingAutomation._is_video_file(path):
            return "FILE"

        # Check for other protocols
        path_lower = path.lower()
        if any(path_lower.startswith(proto) for proto in ['http://', 'https://', 's3://']):
            return "FILE"

        # Default to RTSP
        return "RTSP"

    # ==================== Streaming Gateway Methods ====================

    def create_streaming_gateway(
        self,
        gateway_name: str,
        description: str = "",
        compute_alias: str = "",
        account_type: str = "enterprise",
        server_type: str = "redis",
        video: str = "h264",
        network_settings: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Create a streaming gateway.

        Parameters
        ----------
        gateway_name : str
            Name of the gateway
        description : str
            Description of the gateway
        compute_alias : str
            Compute alias for the gateway
        account_type : str
            Account type (default: "enterprise")
        server_type : str
            Server type - "redis" or "kafka" (default: "redis")
        video : str
            Video codec (default: "h264")
        network_settings : dict, optional
            Network settings dict with IPAddress, accessScale, port, region, etc.

        Returns
        -------
        tuple : (gateway_id, error_message)
            Returns gateway_id if successful, None and error message if failed
        """
        if network_settings is None:
            network_settings = {
                "IPAddress": "",
                "accessScale": "local",
                "port": 0,
                "region": "",
                "maxBandwidthMbps": 0,
                "currentBandwidthMbps": 0,
            }

        payload = {
            "gatewayName": gateway_name,
            "description": description,
            "accountNumber": self.account_number,
            "computeAlias": compute_alias,
            "accountType": account_type,
            "serverType": server_type,
            "video": video,
            "networkSettings": network_settings,
        }

        try:
            resp = self.rpc.post(
                path="/v1/inference/create_streaming_gateway",
                payload=payload,
            )
            if resp.get("success"):
                # API returns ID in data.id (see auto_start_new.py line 26)
                data = resp.get("data", {})
                if isinstance(data, dict):
                    gateway_id = data.get("id")
                    if gateway_id and self._is_valid_id(gateway_id):
                        return gateway_id, None
                
                # Fallback: List gateways and find the one we just created
                gateways, error = self.list_streaming_gateways(page_size=100)
                if error:
                    return None, f"Gateway created but failed to retrieve ID: {error}"
                
                # Find the gateway with matching name
                for gw in gateways or []:
                    if gw.get("gatewayName") == gateway_name:
                        return gw.get("id"), None
                
                return None, f"Gateway created but could not find it in list (searched for name: {gateway_name})"
            else:
                return None, resp.get("message", "Unknown error")
        except Exception as e:
            return None, str(e)

    def list_streaming_gateways(
        self, page_size: int = 20, page: int = 0
    ) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        List all streaming gateways for the account.

        Returns
        -------
        tuple : (list of gateways, error_message)
        """
        try:
            path = f"/v1/inference/all_streaming_gateways_pag/{self.account_number}?pageSize={page_size}&page={page}"
            resp = self.rpc.get(path=path)
            if resp.get("success"):
                data = resp.get("data", {})
                # Ensure data is a dict before calling .get()
                if isinstance(data, dict):
                    items = data.get("items", [])
                    return items, None
                else:
                    return None, f"Unexpected response format: data is {type(data).__name__}, not dict"
            else:
                return None, resp.get("message", "Unknown error")
        except Exception as e:
            return None, str(e)

    def start_streaming_gateway(self, gateway_id: str) -> Tuple[bool, Optional[str]]:
        """
        Start a streaming gateway.

        Parameters
        ----------
        gateway_id : str
            ID of the gateway to start

        Returns
        -------
        tuple : (success, error_message)
        """
        try:
            resp = self.rpc.put(
                path=f"/v1/inference/start_streaming_gateway/{gateway_id}",
                payload={},
            )
            if resp.get("success"):
                return True, None
            else:
                return False, resp.get("message", "Unknown error")
        except Exception as e:
            return False, str(e)

    # ==================== Location Methods ====================

    def create_location(
        self,
        location_name: str,
        street_address: str = "",
        city: str = "",
        state: str = "",
        country: str = "",
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Create a location.

        Parameters
        ----------
        location_name : str
            Name of the location
        street_address : str
            Street address
        city : str
            City name
        state : str
            State/province
        country : str
            Country name

        Returns
        -------
        tuple : (location_id, error_message)
        """
        payload = {
            "accountNumber": self.account_number,
            "locationName": location_name,
            "locationInfo": {
                "streetAddress": street_address,
                "city": city,
                "state": state,
                "country": country,
            },
        }

        try:
            resp = self.rpc.post(
                path="/v1/inference/create_location",
                payload=payload,
            )
            if resp.get("success"):
                # API doesn't return ID in response, must list to find it
                # See auto_start_new.py line 69 - immediately calls list_locations
                locations, error = self.list_locations(page_size=100)
                if error:
                    return None, f"Location created but failed to retrieve ID: {error}"
                
                # Find the location with matching name (most recent one)
                for loc in locations or []:
                    if loc.get("locationName") == location_name:
                        return loc.get("id"), None
                
                return None, f"Location created but could not find it in list (searched for name: {location_name})"
            else:
                return None, resp.get("message", "Unknown error")
        except Exception as e:
            return None, str(e)

    def list_locations(
        self, page_size: int = 20, page: int = 0
    ) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        List all locations for the account.

        Returns
        -------
        tuple : (list of locations, error_message)
        """
        try:
            path = f"/v1/inference/all_locations_pag/{self.account_number}?pageSize={page_size}&page={page}"
            resp = self.rpc.get(path=path)
            if resp.get("success"):
                data = resp.get("data", {})
                # Ensure data is a dict before calling .get()
                if isinstance(data, dict):
                    items = data.get("items", [])
                    return items, None
                else:
                    return None, f"Unexpected response format: data is {type(data).__name__}, not dict"
            else:
                return None, resp.get("message", "Unknown error")
        except Exception as e:
            return None, str(e)

    # ==================== Camera Group Methods ====================

    def create_camera_group(
        self,
        camera_group_name: str,
        location_id: str,
        streaming_gateway_id: str,
        default_stream_settings: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Create a camera group.

        Parameters
        ----------
        camera_group_name : str
            Name of the camera group
        location_id : str
            ID of the location
        streaming_gateway_id : str
            ID of the streaming gateway
        default_stream_settings : dict, optional
            Default stream settings with aspectRatio, height, width, videoQuality, streamingFPS

        Returns
        -------
        tuple : (camera_group_id, error_message)
        """
        if default_stream_settings is None:
            default_stream_settings = {
                "make": "",
                "model": "",
                "aspectRatio": "16:9",
                "height": 480,
                "width": 640,
                "videoQuality": 80,
                "streamingFPS": 10,
            }

        payload = {
            "accountNumber": self.account_number,
            "cameraGroupName": camera_group_name,
            "locationId": location_id,
            "streamingGatewayId": streaming_gateway_id,
            "defaultStreamSettings": default_stream_settings,
        }

        try:
            resp = self.rpc.post(
                path="/v1/inference/create_camera_group",
                payload=payload,
            )
            if resp.get("success"):
                # API returns ID in data.id (see auto_start_new.py line 178)
                data = resp.get("data", {})
                if isinstance(data, dict):
                    camera_group_id = data.get("id")
                    if camera_group_id and self._is_valid_id(camera_group_id):
                        return camera_group_id, None
                
                # Fallback: List camera groups and find the one we just created
                camera_groups, error = self.list_camera_groups(page_size=100)
                if error:
                    return None, f"Camera group created but failed to retrieve ID: {error}"
                
                # Find the camera group with matching name and location
                for cg in camera_groups or []:
                    if (cg.get("cameraGroupName") == camera_group_name and 
                        cg.get("locationId") == location_id):
                        return cg.get("id"), None
                
                return None, f"Camera group created but could not find it in list (searched for name: {camera_group_name})"
            else:
                return None, resp.get("message", "Unknown error")
        except Exception as e:
            return None, str(e)

    def list_camera_groups(
        self, page_size: int = 20, page: int = 0
    ) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        List all camera groups for the account.

        Returns
        -------
        tuple : (list of camera groups, error_message)
        """
        try:
            path = f"/v1/inference/all_camera_groups_pag/{self.account_number}?pageSize={page_size}&page={page}"
            resp = self.rpc.get(path=path)
            if resp.get("success"):
                data = resp.get("data", {})
                # Ensure data is a dict before calling .get()
                if isinstance(data, dict):
                    items = data.get("items", [])
                    return items, None
                else:
                    return None, f"Unexpected response format: data is {type(data).__name__}, not dict"
            else:
                return None, resp.get("message", "Unknown error")
        except Exception as e:
            return None, str(e)

    # ==================== Video Upload Methods ====================

    def get_presigned_url(self, file_name: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Get a presigned URL for video upload.

        Parameters
        ----------
        file_name : str
            Name of the file to upload

        Returns
        -------
        tuple : (presigned_url, error_message)
        """
        try:
            path = f"/v1/inference/get_presigned_url_stream?fileName={file_name}"
            resp = self.rpc.get(path=path)
            if resp.get("success"):
                presigned_url = resp.get("data")
                return presigned_url, None
            else:
                return None, resp.get("message", "Unknown error")
        except Exception as e:
            return None, str(e)

    def upload_video(
        self, video_path: str, file_name: Optional[str] = None
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Upload a video file to S3 using presigned URL.

        Parameters
        ----------
        video_path : str
            Path to the video file
        file_name : str, optional
            Name for the uploaded file (defaults to original filename)

        Returns
        -------
        tuple : (s3_url, error_message)
        """
        video_file = Path(video_path)
        if not video_file.exists():
            return None, f"Video file not found: {video_path}"

        if file_name is None:
            file_name = video_file.name

        # Get presigned URL
        presigned_url, error = self.get_presigned_url(file_name)
        if error:
            return None, error

        # Upload file to presigned URL
        try:
            with open(video_file, "rb") as f:
                resp = requests.put(presigned_url, data=f)
                resp.raise_for_status()

            # Extract S3 URL (remove query parameters)
            s3_url = presigned_url.split("?")[0]
            return s3_url, None
        except Exception as e:
            return None, str(e)

    # ==================== Camera Methods ====================

    def create_cameras(
        self, cameras: List[Dict[str, Any]]
    ) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        Create cameras (supports both RTSP and FILE protocol types).
        Checks for existing cameras before creating to avoid duplicate errors.

        Parameters
        ----------
        cameras : list of dict
            List of camera configurations. Each dict should contain:
            - accountNumber: str
            - cameraGroupId: str
            - streamingGatewayId: str
            - locationId: str
            - cameraName: str
            - protocolType: str ("RTSP" or "FILE")
            - cameraFeedPath: str (for RTSP)
            - simulationVideoPath: str (for FILE)
            - defaultStreamSettings: dict (optional)

        Returns
        -------
        tuple : (list of created/existing cameras, error_message)
        """
        if not cameras:
            return [], None
        
        # Get camera names to check for existing cameras
        camera_names = [cam.get("cameraName") for cam in cameras if cam.get("cameraName")]
        if not camera_names:
            return None, "No camera names found in camera configurations"
        
        # Check for existing cameras by name
        all_cameras, error = self.get_cameras(limit=1000)  # Get more cameras to check
        if error:
            return None, f"Failed to check existing cameras: {error}"
        
        # Find existing cameras by name
        existing_cameras = {}
        for cam in all_cameras or []:
            cam_name = cam.get("cameraName")
            if cam_name in camera_names:
                existing_cameras[cam_name] = cam
        
        # Filter out cameras that already exist
        cameras_to_create = []
        for cam in cameras:
            cam_name = cam.get("cameraName")
            if cam_name not in existing_cameras:
                cameras_to_create.append(cam)
        
        # If all cameras already exist, return them
        if not cameras_to_create:
            return list(existing_cameras.values()), None
        
        # Create only new cameras
        try:
            resp = self.rpc.post(
                path="/v1/inference/create_camera_stream",
                payload=cameras_to_create,
            )
            if resp.get("success"):
                # Get all cameras again to find the newly created ones
                all_cameras, error = self.get_cameras(limit=1000)
                if error:
                    return None, f"Cameras created but failed to retrieve: {error}"
                
                # Find all cameras (both existing and newly created)
                result_cameras = []
                for cam in all_cameras or []:
                    cam_name = cam.get("cameraName")
                    if cam_name in camera_names:
                        result_cameras.append(cam)
                
                return result_cameras, None
            else:
                # Check if error is "already exists" - if so, return existing cameras
                error_message = resp.get("message", "")
                if "already exists" in error_message.lower() or "Camera stream already exists" in error_message:
                    # Return existing cameras we found earlier
                    result_cameras = list(existing_cameras.values())
                    # Try to get any newly created cameras
                    all_cameras, _ = self.get_cameras(limit=1000)
                    if all_cameras:
                        for cam in all_cameras:
                            cam_name = cam.get("cameraName")
                            if cam_name in camera_names and cam_name not in existing_cameras:
                                result_cameras.append(cam)
                    return result_cameras, None
                else:
                    return None, error_message
        except Exception as e:
            error_str = str(e)
            # Check if error contains "already exists"
            if "already exists" in error_str.lower() or "Camera stream already exists" in error_str:
                # Return existing cameras
                return list(existing_cameras.values()), None
            return None, error_str

    def get_cameras(
        self,
        camera_group_id: Optional[str] = None,
        page: int = 1,
        limit: int = 10,
        search: Optional[str] = None,
    ) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        Get cameras. If camera_group_id is provided, filters by group.

        Parameters
        ----------
        camera_group_id : str, optional
            Filter cameras by camera group ID
        page : int
            Page number for pagination (default: 1)
        limit : int
            Items per page (default: 10)
        search : str, optional
            Search term to filter cameras

        Returns
        -------
        tuple : (list of cameras, error_message)
        """
        try:
            # API endpoint (see auto_start_new.py line 242)
            path = f"/v1/inference/get_camerastream_by_acc_number/{self.account_number}"
            params = {"page": page, "limit": limit}
            if camera_group_id:
                params["groupId"] = camera_group_id
            if search:
                params["search"] = search

            # Build query string
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            path = f"{path}?{query_string}"

            resp = self.rpc.get(path=path)
            if resp.get("success"):
                # API returns data as array directly (see auto_start_new.py line 262)
                cameras = resp.get("data", [])
                if isinstance(cameras, dict) and "items" in cameras:
                    cameras = cameras["items"]
                return cameras, None
            else:
                return None, resp.get("message", "Unknown error")
        except Exception as e:
            return None, str(e)

    def get_camera_json(self, camera_id: str) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Get camera details as JSON.
        
        Note: This method is deprecated as the API endpoint doesn't exist.
        Use get_cameras() instead to retrieve camera information.

        Parameters
        ----------
        camera_id : str
            ID of the camera

        Returns
        -------
        tuple : (camera_dict, error_message)
        """
        # This API endpoint doesn't exist in the actual API
        # Return None to indicate it's not available
        return None, "API endpoint /v1/inference/camera/{id} does not exist"

    def export_cameras_to_jsonl(
        self,
        output_file: str,
        camera_group_id: Optional[str] = None,
        include_details: bool = True,
    ) -> Tuple[bool, Optional[str]]:
        """
        Export cameras to JSONL (JSON Lines) format.

        Parameters
        ----------
        output_file : str
            Path to output JSONL file
        camera_group_id : str, optional
            Filter cameras by camera group ID
        include_details : bool
            Deprecated parameter (kept for backward compatibility)

        Returns
        -------
        tuple : (success, error_message)
        """
        try:
            cameras, error = self.get_cameras(camera_group_id=camera_group_id)
            if error:
                return False, error

            with open(output_file, "w") as f:
                for camera in cameras or []:
                    # Write camera data directly (no need to fetch details as API doesn't exist)
                    f.write(json.dumps(camera) + "\n")

            return True, None
        except Exception as e:
            return False, str(e)

    def export_cameras_to_json(
        self,
        output_file: str,
        camera_group_id: Optional[str] = None,
        include_details: bool = True,
    ) -> Tuple[bool, Optional[str]]:
        """
        Export cameras to JSON format (single JSON array).

        Parameters
        ----------
        output_file : str
            Path to output JSON file
        camera_group_id : str, optional
            Filter cameras by camera group ID
        include_details : bool
            Deprecated parameter (kept for backward compatibility)

        Returns
        -------
        tuple : (success, error_message)
        """
        try:
            cameras, error = self.get_cameras(camera_group_id=camera_group_id)
            if error:
                return False, error

            # Write camera data directly (no need to fetch details as API doesn't exist)
            cameras_list = cameras or []

            with open(output_file, "w") as f:
                json.dump(cameras_list, f, indent=2)

            return True, None
        except Exception as e:
            return False, str(e)

    # ==================== Application Methods ====================

    def get_applications(
        self,
        page_size: int = 200,
        page_number: int = 0,
        sort_by: str = "",
        sort_order: str = "asc",
    ) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        Get available applications.

        Returns
        -------
        tuple : (list of applications, error_message)
        """
        try:
            params = {
                "pageSize": page_size,
                "pageNumber": page_number,
                "sortBy": sort_by,
                "sortOrder": sort_order,
            }
            # Remove empty params
            params = {k: v for k, v in params.items() if v}

            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            path = f"/v1/public/applications/?{query_string}"

            resp = self.rpc.get(path=path)
            if resp.get("success"):
                data = resp.get("data", {})
                # Ensure data is a dict before calling .get()
                if isinstance(data, dict):
                    items = data.get("items", [])
                    return items, None
                else:
                    return None, f"Unexpected response format: data is {type(data).__name__}, not dict"
            else:
                return None, resp.get("message", "Unknown error")
        except Exception as e:
            return None, str(e)

    def find_application_by_name(
        self, application_name: str
    ) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Find an application by name.

        Parameters
        ----------
        application_name : str
            Name of the application to find

        Returns
        -------
        tuple : (application_dict, error_message)
        """
        applications, error = self.get_applications()
        if error:
            return None, error

        for app in applications or []:
            if app.get("name") == application_name:
                return app, None

        return None, f"Application '{application_name}' not found"

    # ==================== Server Methods ====================

    def get_facial_recognition_servers(
        self,
        project_id: str,
        page: int = 1,
        page_size: int = 10,
    ) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        Get facial recognition servers for a project.

        Parameters
        ----------
        project_id : str
            Project ID
        page : int
            Page number (default: 1)
        page_size : int
            Page size (default: 10)

        Returns
        -------
        tuple : (list of FR servers, error_message)
        """
        try:
            path = f"/v1/actions/get_facial_recognition_servers?projectId={project_id}&page={page}&pageSize={page_size}"
            resp = self.rpc.get(path=path)
            if resp.get("success"):
                data = resp.get("data", {})
                # Ensure data is a dict before calling .get()
                if isinstance(data, dict):
                    items = data.get("items", [])
                    return items, None
                else:
                    return None, f"Unexpected response format: data is {type(data).__name__}, not dict"
            else:
                return None, resp.get("message", "Unknown error")
        except Exception as e:
            return None, str(e)

    def get_lpr_servers(
        self,
        project_id: str,
        page: int = 1,
        page_size: int = 10,
    ) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        Get LPR (License Plate Recognition) servers for a project.

        Parameters
        ----------
        project_id : str
            Project ID
        page : int
            Page number (default: 1)
        page_size : int
            Page size (default: 10)

        Returns
        -------
        tuple : (list of LPR servers, error_message)
        """
        try:
            path = f"/v1/actions/lpr_servers?project_id={project_id}&account_number={self.account_number}&page={page}&pageSize={page_size}"
            resp = self.rpc.get(path=path)
            if resp.get("success"):
                # LPR servers endpoint returns data as array directly
                servers = resp.get("data", [])
                if isinstance(servers, list):
                    return servers, None
                else:
                    return None, "Unexpected response format"
            else:
                return None, resp.get("message", "Unknown error")
        except Exception as e:
            return None, str(e)

    # ==================== Inference Pipeline Methods ====================

    def create_inference_pipeline(
        self,
        name: str,
        project_id: str,
        cameras: List[Dict[str, Any]],
        description: str = "",
        access_scale: str = "local",
        deploy_type: str = "account",
        server_type: str = "fastapi",
        facial_recognition_server_id: Optional[str] = None,
        lpr_server_id: Optional[str] = None,
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Create an inference pipeline using the new format with cameras array.

        Parameters
        ----------
        name : str
            Name of the pipeline
        project_id : str
            Project ID
        cameras : list of dict
            List of camera configurations. Each dict should contain:
            - cameraId: str (ID of the camera)
            - applications: list of dict with "_idApplication" key
        description : str
            Description of the pipeline
        access_scale : str
            Access scale (default: "local")
        deploy_type : str
            Deploy type (default: "account")
        server_type : str
            Server type (default: "fastapi", can be empty string "")
        facial_recognition_server_id : str, optional
            Facial recognition server ID (required for FR applications)
        lpr_server_id : str, optional
            LPR server ID (required for LPR applications)

        Returns
        -------
        tuple : (pipeline_id, error_message)
        """
        payload = {
            "name": name,
            "_idProject": project_id,
            "status": "created",
            "cameras": cameras,
            "description": description,
            "accessScale": access_scale,
            "deployType": deploy_type,
            "serverType": server_type,
        }

        if facial_recognition_server_id:
            payload["_idServerFacialRecognition"] = facial_recognition_server_id

        if lpr_server_id:
            payload["_idLPRServer"] = lpr_server_id

        try:
            resp = self.rpc.post(
                path="/v1/inference/inference_pipeline",
                payload=payload,
            )
            if resp.get("success"):
                # API doesn't return ID in response, must list to find it
                # See auto_start_new.py line 912 - no response shown
                pipelines, error = self.list_inference_pipelines(project_id=project_id, page_size=100)
                if error:
                    return None, f"Pipeline created but failed to retrieve ID: {error}"
                
                # Find the pipeline with matching name (most recent one)
                for pipeline in pipelines or []:
                    if pipeline.get("name") == name:
                        return pipeline.get("_id"), None
                
                return None, f"Pipeline created but could not find it in list (searched for name: {name})"
            else:
                return None, resp.get("message", "Unknown error")
        except Exception as e:
            return None, str(e)

    def list_inference_pipelines(
        self,
        project_id: str,
        page_size: int = 10,
        page_number: int = 0,
        sort_by: str = "",
        sort_order: str = "asc",
    ) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        List inference pipelines for a project.

        Returns
        -------
        tuple : (list of pipelines, error_message)
        """
        try:
            params = {
                "pageSize": page_size,
                "pageNumber": page_number,
                "sortBy": sort_by,
                "sortOrder": sort_order,
                "projectId": project_id,
            }
            # Remove empty params
            params = {k: v for k, v in params.items() if v}

            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            path = f"/v1/inference/list_inference_pipelines/{project_id}?{query_string}"

            resp = self.rpc.get(path=path)
            if resp.get("success"):
                data = resp.get("data", {})
                # Ensure data is a dict before calling .get()
                if isinstance(data, dict):
                    items = data.get("items", [])
                    return items, None
                else:
                    return None, f"Unexpected response format: data is {type(data).__name__}, not dict"
            else:
                return None, resp.get("message", "Unknown error")
        except Exception as e:
            return None, str(e)

    def start_inference_pipeline(
        self, pipeline_id: str, compute_alias: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Start an inference pipeline with compute alias.

        Parameters
        ----------
        pipeline_id : str
            ID of the pipeline to start
        compute_alias : str
            Compute alias to use for the pipeline

        Returns
        -------
        tuple : (success, error_message)
        """
        try:
            resp = self.rpc.put(
                path=f"/v1/inference/start_inference_pipeline/{pipeline_id}",
                payload={"computeAlias": compute_alias},
            )
            if resp.get("success"):
                return True, None
            else:
                return False, resp.get("message", "Unknown error")
        except Exception as e:
            return False, str(e)

    # ==================== Complete Workflow Methods ====================

    def create_complete_setup(
        self,
        gateway_name: str,
        location_name: str,
        camera_group_name: str,
        cameras: List[Dict[str, Any]],
        project_id: str,
        application_names: List[str],
        compute_alias: str = "",
        location_info: Optional[Dict[str, str]] = None,
        start_gateway: bool = True,
        start_pipeline: bool = True,
        facial_recognition_server_id: Optional[str] = None,
        lpr_server_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Complete workflow to create and start everything.

        Parameters
        ----------
        gateway_name : str
            Name for the streaming gateway
        location_name : str
            Name for the location
        camera_group_name : str
            Name for the camera group
        cameras : list of dict
            List of camera configurations
        project_id : str
            Project ID
        application_names : list of str
            List of application names to use
        compute_alias : str
            Compute alias for gateway
        location_info : dict, optional
            Location info with streetAddress, city, state, country
        start_gateway : bool
            Whether to start the gateway (default: True)
        start_pipeline : bool
            Whether to start the pipeline (default: True)

        Returns
        -------
        dict : Results dictionary with all created IDs and any errors
        """
        results = {
            "gateway_id": None,
            "location_id": None,
            "camera_group_id": None,
            "camera_ids": [],
            "pipeline_id": None,
            "errors": [],
        }

        # 1. Create streaming gateway
        gateway_id, error = self.create_streaming_gateway(
            gateway_name=gateway_name,
            description=f"Gateway for {gateway_name}",
            compute_alias=compute_alias,
        )
        if error:
            results["errors"].append(f"Failed to create gateway: {error}")
            return results
        results["gateway_id"] = gateway_id
        print(f"✓ Created streaming gateway: {gateway_id}")

        # 2. Create location
        if location_info is None:
            location_info = {
                "streetAddress": "",
                "city": "",
                "state": "",
                "country": "",
            }
        location_id, error = self.create_location(
            location_name=location_name,
            street_address=location_info.get("streetAddress", ""),
            city=location_info.get("city", ""),
            state=location_info.get("state", ""),
            country=location_info.get("country", ""),
        )
        if error:
            results["errors"].append(f"Failed to create location: {error}")
            return results
        results["location_id"] = location_id
        print(f"✓ Created location: {location_id}")

        # 3. Create camera group
        camera_group_id, error = self.create_camera_group(
            camera_group_name=camera_group_name,
            location_id=location_id,
            streaming_gateway_id=gateway_id,
        )
        if error:
            results["errors"].append(f"Failed to create camera group: {error}")
            return results
        results["camera_group_id"] = camera_group_id
        print(f"✓ Created camera group: {camera_group_id}")

        # 4. Add accountNumber, cameraGroupId, streamingGatewayId, and locationId to cameras
        for camera in cameras:
            camera["accountNumber"] = self.account_number
            camera["cameraGroupId"] = camera_group_id
            camera["streamingGatewayId"] = gateway_id
            camera["locationId"] = location_id

        # 5. Create cameras
        created_cameras, error = self.create_cameras(cameras)
        if error:
            results["errors"].append(f"Failed to create cameras: {error}")
            return results
        results["camera_ids"] = [
            cam.get("_id") or cam.get("id") 
            for cam in (created_cameras or []) 
            if isinstance(cam, dict)
        ]
        print(f"✓ Created {len(results['camera_ids'])} cameras")

        # 6. Start gateway if requested
        if start_gateway:
            success, error = self.start_streaming_gateway(gateway_id)
            if error:
                results["errors"].append(f"Failed to start gateway: {error}")
            else:
                print(f"✓ Started streaming gateway: {gateway_id}")

        # 7. Get applications and build cameras array for pipeline
        application_ids = []
        for app_name in application_names:
            app, error = self.find_application_by_name(app_name)
            if error:
                results["errors"].append(f"Failed to find application '{app_name}': {error}")
                continue
            application_ids.append({"_idApplication": app["_id"]})
        print(f"✓ Found {len(application_ids)} applications")

        # Build cameras array for pipeline (new format)
        pipeline_cameras = []
        for camera_id in results["camera_ids"]:
            pipeline_cameras.append({
                "cameraId": camera_id,
                "applications": application_ids
            })

        # 8. Create inference pipeline (using new format)
        pipeline_id, error = self.create_inference_pipeline(
            name=f"Pipeline for {gateway_name}",
            project_id=project_id,
            cameras=pipeline_cameras,
            facial_recognition_server_id=facial_recognition_server_id,
            lpr_server_id=lpr_server_id,
        )
        if error:
            results["errors"].append(f"Failed to create pipeline: {error}")
            return results
        results["pipeline_id"] = pipeline_id
        print(f"✓ Created inference pipeline: {pipeline_id}")

        # 9. Start pipeline if requested
        if start_pipeline:
            success, error = self.start_inference_pipeline(pipeline_id, compute_alias)
            if error:
                results["errors"].append(f"Failed to start pipeline: {error}")
            else:
                print(f"✓ Started inference pipeline: {pipeline_id}")

        return results

    def auto_setup_from_cameras(
        self,
        cameras: Union[str, Dict, List[Dict]],
        compute_alias: str,
        project_id: Optional[str] = None,
        application_names: Optional[List[str]] = None,
        auto_start: bool = False,
        facial_recognition_server_id: Optional[str] = None,
        lpr_server_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Fully automated setup from camera data. Only requires minimal inputs.

        This method automatically:
        - Parses cameras from various formats (JSON string, dict, list of dicts, file path)
        - Extracts location and camera group info from cameras (or generates defaults)
        - Creates streaming gateway with auto-generated name and tag
        - Creates location (from camera data or auto-generated)
        - Creates camera group (from camera data or auto-generated)
        - Creates cameras
        - Starts streaming gateway
        - Creates inference pipeline (if applications provided)
        - Starts inference pipeline

        Parameters
        ----------
        cameras : str, dict, or list of dicts
            Camera data in any format:
            - JSON string: '{"cameraName": "cam1", "protocolType": "RTSP", ...}'
            - File path: Path to JSON file containing cameras
            - Single dict: {"cameraName": "cam1", ...}
            - List of dicts: [{"cameraName": "cam1", ...}, ...]
        compute_alias : str
            Compute alias for the streaming gateway
        project_id : str, optional
            Project ID (uses session project_id if not provided)
        application_names : list of str, optional
            List of application names to add to pipeline (e.g., ["People Counting", "Color Detection"])
            If not provided, pipeline will be created without applications
        auto_start : bool
            Whether to automatically start gateway and pipeline (default: True)
        facial_recognition_server_id : str, optional
            Facial recognition server ID (required for FR applications like "Face Recognition")
        lpr_server_id : str, optional
            LPR server ID (required for LPR applications like "License Plate Recognition")

        Returns
        -------
        dict : Results dictionary with all created IDs, tags, and any errors
            {
                "gateway_id": "...",
                "gateway_name": "...",
                "location_id": "...",
                "location_name": "...",
                "camera_group_id": "...",
                "camera_group_name": "...",
                "camera_ids": [...],
                "pipeline_id": "...",
                "pipeline_name": "...",
                "tag": "...",  # Auto-generated tag for this setup
                "errors": []
            }
        """
        results = {
            "gateway_id": None,
            "gateway_name": None,
            "location_id": None,
            "location_name": None,
            "camera_group_id": None,
            "camera_group_name": None,
            "camera_ids": [],
            "pipeline_id": None,
            "pipeline_name": None,
            "tag": self._generate_tag("setup"),
            "errors": [],
        }

        # Use project_id from session if not provided
        if not project_id:
            project_id = self.session.project_id
            if not project_id:
                results["errors"].append("Project ID is required")
                return results

        # Parse cameras
        try:
            parsed_cameras = self._parse_cameras(cameras)
            if not parsed_cameras:
                results["errors"].append("No cameras found in input")
                return results
        except Exception as e:
            results["errors"].append(f"Failed to parse cameras: {str(e)}")
            return results

        # Extract info from cameras - but use UUID-based names to avoid conflicts
        camera_info = self._extract_camera_info(parsed_cameras)
        
        # Always use UUID-based names to avoid any naming conflicts
        unique_id = str(uuid.uuid4())[:8]
        location_name = f"location-{unique_id}"
        camera_group_name = f"camera-group-{unique_id}"
        gateway_name = f"gateway-{unique_id}"
        
        # Set location_info with default UUID-based values
        location_info = {
            "streetAddress": location_name,
            "city": location_name,
            "state": location_name,
            "country": location_name,
        }
        
        gateway_description = f"Auto-generated gateway {unique_id}"

        # 1. Create streaming gateway
        gateway_id, error = self.create_streaming_gateway(
            gateway_name=gateway_name,
            description=gateway_description,
            compute_alias=compute_alias,
        )
        if error:
            results["errors"].append(f"Failed to create gateway: {error}")
            return results
        results["gateway_id"] = gateway_id
        results["gateway_name"] = gateway_name
        print(f"✓ Created streaming gateway: {gateway_name} ({gateway_id})")

        # 2. Create location with auto-filled data
        location_id, error = self.create_location(
            location_name=location_name,
            street_address=location_info.get("streetAddress", location_name),
            city=location_info.get("city", location_name),
            state=location_info.get("state", location_name),
            country=location_info.get("country", location_name),
        )
        if error:
            results["errors"].append(f"Failed to create location: {error}")
            return results
        results["location_id"] = location_id
        results["location_name"] = location_name
        print(f"✓ Created location: {location_name} ({location_id})")

        # 3. Create camera group
        camera_group_id, error = self.create_camera_group(
            camera_group_name=camera_group_name,
            location_id=location_id,
            streaming_gateway_id=gateway_id,
        )
        if error:
            results["errors"].append(f"Failed to create camera group: {error}")
            return results
        results["camera_group_id"] = camera_group_id
        results["camera_group_name"] = camera_group_name
        print(f"✓ Created camera group: {camera_group_name} ({camera_group_id})")

        # 4. Normalize cameras - ensure they have required fields and auto-upload videos
        normalized_cameras = []
        for idx, camera in enumerate(parsed_cameras):
            # Generate default camera name using UUID if not provided
            cam_unique_id = str(uuid.uuid4())[:8]
            default_camera_name = f"camera-{cam_unique_id}"
            
            normalized = {
                "accountNumber": self.account_number,
                "cameraGroupId": camera_group_id,
                "streamingGatewayId": gateway_id,
                "locationId": location_id,
            }

            # Copy existing fields - try multiple field name variations
            camera_name = None
            for key in ["cameraName", "camera_name", "name"]:
                if key in camera and camera[key]:
                    camera_name = camera[key]
                    break
            
            # Use provided name or auto-generate
            normalized["cameraName"] = camera_name or default_camera_name

            # Get the path/URL from various possible fields
            path = (
                camera.get("cameraFeedPath") or
                camera.get("camera_feed_path") or
                camera.get("simulationVideoPath") or
                camera.get("simulation_video_path") or
                camera.get("video_path") or
                camera.get("video_url") or
                camera.get("rtsp_url") or
                camera.get("url") or
                camera.get("path") or
                camera.get("feed_path") or
                camera.get("stream_url") or
                ""
            )

            # Auto-detect protocol type if not provided
            protocol_type = camera.get("protocolType") or camera.get("protocol_type") or camera.get("protocol")
            if not protocol_type and path:
                protocol_type = self._detect_protocol_type(path)
            elif not protocol_type:
                protocol_type = "RTSP"  # Default

            # Handle local video file upload
            if protocol_type == "FILE" and path:
                if self._is_local_file(path):
                    print(f"  Uploading local video file: {path}")
                    # Generate unique filename using UUID to avoid conflicts
                    file_unique_id = str(uuid.uuid4())[:8]
                    original_name = Path(path).name
                    file_name = f"video-{file_unique_id}-{original_name}"

                    # Upload the video
                    s3_url, error = self.upload_video(path, file_name)
                    if error:
                        results["errors"].append(f"Failed to upload video '{path}': {error}")
                        print(f"  ✗ Failed to upload video: {error}")
                        # Skip this camera
                        continue
                    else:
                        path = s3_url
                        print(f"  ✓ Uploaded to: {s3_url}")

            normalized["protocolType"] = protocol_type

            # Add protocol-specific fields
            if protocol_type == "RTSP":
                normalized["cameraFeedPath"] = path
            elif protocol_type == "FILE":
                normalized["simulationVideoPath"] = path

            # Add default stream settings - use provided or sensible defaults
            if "defaultStreamSettings" in camera and camera["defaultStreamSettings"]:
                normalized["defaultStreamSettings"] = camera["defaultStreamSettings"]
            elif "stream_settings" in camera and camera["stream_settings"]:
                normalized["defaultStreamSettings"] = camera["stream_settings"]
            else:
                # Auto-generate sensible default stream settings
                normalized["defaultStreamSettings"] = {
                    "width": 640,
                    "height": 480,
                    "fps": 10,
                    "aspectRatio": "16:9",
                    "videoQuality": 80
                }

            normalized_cameras.append(normalized)

        # 5. Create cameras
        created_cameras, error = self.create_cameras(normalized_cameras)
        if error:
            results["errors"].append(f"Failed to create cameras: {error}")
            return results
        results["camera_ids"] = [
            cam.get("_id") or cam.get("id") 
            for cam in (created_cameras or []) 
            if isinstance(cam, dict)
        ]
        print(f"✓ Created {len(results['camera_ids'])} cameras")

        # 6. Start gateway if requested
        if auto_start:
            success, error = self.start_streaming_gateway(gateway_id)
            if error:
                results["errors"].append(f"Failed to start gateway: {error}")
            else:
                print(f"✓ Started streaming gateway: {gateway_name}")

        # 7. Create inference pipeline if applications provided
        # Support per-camera apps or default apps
        has_any_apps = False
        
        # Check if any camera has apps or if default apps are provided
        for camera in parsed_cameras:
            if camera.get("apps") or camera.get("applications"):
                has_any_apps = True
                break
        
        if has_any_apps or application_names:
            # Build default application IDs
            default_application_ids = []
            if application_names:
                for app_name in application_names:
                    app, error = self.find_application_by_name(app_name)
                    if error:
                        results["errors"].append(f"Failed to find application '{app_name}': {error}")
                        continue
                    default_application_ids.append({"_idApplication": app["_id"]})

            # Build cameras array for pipeline with per-camera or default apps
            pipeline_cameras = []
            for idx, camera_id in enumerate(results["camera_ids"]):
                # Check if this camera has specific apps
                camera_apps = None
                if idx < len(parsed_cameras):
                    original_camera = parsed_cameras[idx]
                    camera_specific_apps = original_camera.get("apps") or original_camera.get("applications")
                    
                    if camera_specific_apps:
                        # Parse camera-specific apps
                        if isinstance(camera_specific_apps, str):
                            # Comma-separated or single app name
                            if "," in camera_specific_apps:
                                camera_specific_apps = [app.strip() for app in camera_specific_apps.split(",")]
                            else:
                                camera_specific_apps = [camera_specific_apps]
                        
                        # Convert app names to IDs
                        camera_app_ids = []
                        for app_name in camera_specific_apps:
                            if isinstance(app_name, dict) and "_idApplication" in app_name:
                                # Already in correct format
                                camera_app_ids.append(app_name)
                            elif isinstance(app_name, str):
                                # App name - need to find ID
                                app, error = self.find_application_by_name(app_name)
                                if error:
                                    results["errors"].append(f"Failed to find application '{app_name}' for camera {idx+1}: {error}")
                                    continue
                                camera_app_ids.append({"_idApplication": app["_id"]})
                        
                        if camera_app_ids:
                            camera_apps = camera_app_ids

                # Use camera-specific apps or default apps
                apps_to_use = camera_apps if camera_apps else default_application_ids
                
                if apps_to_use:
                    pipeline_cameras.append({
                        "cameraId": camera_id,
                        "applications": apps_to_use
                    })

            if pipeline_cameras:
                # Auto-generate pipeline name using UUID
                pipeline_unique_id = str(uuid.uuid4())[:8]
                pipeline_name = f"pipeline-{pipeline_unique_id}"
                pipeline_description = f"Auto-generated pipeline for {len(pipeline_cameras)} camera(s)"
                
                pipeline_id, error = self.create_inference_pipeline(
                    name=pipeline_name,
                    project_id=project_id,
                    cameras=pipeline_cameras,
                    description=pipeline_description,
                    facial_recognition_server_id=facial_recognition_server_id,
                    lpr_server_id=lpr_server_id,
                )
                if error:
                    results["errors"].append(f"Failed to create pipeline: {error}")
                else:
                    results["pipeline_id"] = pipeline_id
                    results["pipeline_name"] = pipeline_name
                    print(f"✓ Created inference pipeline: {pipeline_name} ({pipeline_id})")

                    # 8. Start pipeline if requested
                    if auto_start:
                        success, error = self.start_inference_pipeline(pipeline_id, compute_alias)
                        if error:
                            results["errors"].append(f"Failed to start pipeline: {error}")
                        else:
                            print(f"✓ Started inference pipeline: {pipeline_name}")

        return results

    def quick_setup(
        self,
        cameras: Union[str, Dict, List[Dict]],
        compute_alias: Optional[str] = None,
        apps: Optional[Union[str, List[str]]] = None,
        project_id: Optional[str] = None,
        auto_start: bool = False,
        fr_server_id: Optional[str] = None,
        lpr_server_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Simplest way to set up everything with minimal input.
        Accepts various flexible input formats.

        Parameters
        ----------
        cameras : str, dict, or list of dicts
            Camera data in flexible formats:
            - Single camera as dict: {"name": "cam1", "path": "rtsp://..."}
            - List of cameras: [{"name": "cam1", "path": "rtsp://..."}, ...]
            - JSON string with cameras
            - File path to JSON file

            Each camera can have:
            - name/cameraName/camera_name: Camera name (auto-generated if not provided)
            - path/url/feed_path/rtsp_url/video_path: Path or URL (REQUIRED)
            - type/protocolType/protocol: "RTSP" or "FILE" (auto-detected if not provided)
            - apps/applications: Per-camera app list (uses default apps if not provided)
            - Any other optional fields

            Examples:
            ```python
            # Simple RTSP camera
            {"name": "entrance", "path": "rtsp://192.168.1.100:554/stream1"}

            # Video file (local - will be auto-uploaded)
            {"name": "parking", "path": "/path/to/video.mp4"}

            # Video file (remote URL)
            {"name": "parking", "path": "https://example.com/video.mp4"}

            # With explicit type
            {"name": "cam1", "path": "rtsp://...", "type": "RTSP"}

            # With camera-specific apps (overrides default apps)
            {"name": "cam1", "path": "rtsp://...", "apps": ["People Counting"]}

            # Multiple cameras with different apps each
            [
                {"name": "cam1", "path": "rtsp://...", "apps": ["People Counting", "Color Detection"]},
                {"name": "cam2", "path": "rtsp://...", "apps": ["Fire and Smoke Detection"]},
                {"name": "cam3", "path": "rtsp://..."}  # Uses default apps
            ]

            # Camera-specific apps as comma-separated string
            {"name": "cam1", "path": "rtsp://...", "apps": "People Counting, Color Detection"}
            ```

        compute_alias : str, optional
            Compute alias for the streaming gateway (auto-generated if not provided)

        apps : str or list of str, optional
            Application names to add to pipeline. Examples:
            - Single app: "People Counting"
            - Multiple apps: ["People Counting", "Color Detection"]
            - Comma-separated string: "People Counting, Color Detection"

        project_id : str, optional
            Project ID (uses session project_id if not provided)

        auto_start : bool
            Whether to auto-start gateway and pipeline (default: True)

        fr_server_id : str, optional
            Facial recognition server ID (required for FR apps like "Face Recognition")

        lpr_server_id : str, optional
            LPR server ID (required for LPR apps like "License Plate Recognition")

        Returns
        -------
        dict : Results with all created IDs and any errors

        Examples
        --------
        ```python
        # ABSOLUTE MINIMUM - Just camera paths (everything auto-generated)
        results = automation.quick_setup(
            cameras=[
                {"path": "rtsp://192.168.1.100:554/stream1"},
                {"path": "/path/to/video.mp4"}
            ]
        )

        # With optional compute alias and apps
        results = automation.quick_setup(
            cameras=[
                {"name": "entrance", "path": "rtsp://192.168.1.100:554/stream1"},
                {"name": "parking", "path": "/path/to/video.mp4"}
            ],
            compute_alias="my-device",  # Optional - auto-generated if not provided
            apps=["People Counting", "Color Detection"]
        )

        # From JSON file
        results = automation.quick_setup(
            cameras="cameras.json",
            apps="People Counting"
        )
        
        
        # Single camera
        results = automation.quick_setup(
            cameras={"path": "rtsp://..."}
        )
        ```
        """
        # Generate compute_alias if not provided (using UUID to avoid conflicts)
        if not compute_alias:
            compute_alias = ""
        
        # Parse application names
        application_names = None
        if apps:
            if isinstance(apps, str):
                # Split by comma if comma-separated string
                if "," in apps:
                    application_names = [app.strip() for app in apps.split(",")]
                else:
                    application_names = [apps]
            elif isinstance(apps, list):
                application_names = apps

        # Call the auto_setup_from_cameras method
        resp =  self.auto_setup_from_cameras(
            cameras=cameras,
            compute_alias=compute_alias,
            project_id=project_id,
            application_names=application_names,
            auto_start=auto_start,
            facial_recognition_server_id=fr_server_id,
            lpr_server_id=lpr_server_id,
        )
        
        return resp

    def setup_from_paths(
        self,
        paths: Union[str, List[str]],
        compute_alias: Optional[str] = None,
        apps: Optional[Union[str, List[str]]] = None,
        project_id: Optional[str] = None,
        auto_start: bool = False,
    ) -> Dict[str, Any]:
        """
        Ultra-simple setup - just provide camera paths as strings.
        Everything else is auto-generated with UUID-based names.

        Parameters
        ----------
        paths : str or list of str
            Camera paths/URLs:
            - Single path: "rtsp://192.168.1.100:554/stream1"
            - Multiple paths: ["rtsp://...", "/path/to/video.mp4", "https://..."]
        compute_alias : str, optional
            Compute alias (auto-generated if not provided)
        apps : str or list of str, optional
            Application names (optional)
        project_id : str, optional
            Project ID (uses session project_id if not provided)
        auto_start : bool
            Whether to auto-start gateway and pipeline (default: True)

        Returns
        -------
        dict : Results with all created IDs and any errors

        Examples
        --------
        ```python
        # Single path
        results = automation.setup_from_paths("rtsp://192.168.1.100:554/stream1")

        # Multiple paths
        results = automation.setup_from_paths([
            "rtsp://192.168.1.100:554/stream1",
            "rtsp://192.168.1.101:554/stream1",
            "/path/to/video.mp4"
        ])

        # With apps
        results = automation.setup_from_paths(
            ["rtsp://...", "/path/to/video.mp4"],
            apps="People Counting"
        )
        ```
        """
        # Convert paths to camera dictionaries
        if isinstance(paths, str):
            paths = [paths]
        
        cameras = [{"path": path} for path in paths]
        
        # Call quick_setup
        return self.quick_setup(
            cameras=cameras,
            compute_alias=compute_alias,
            apps=apps,
            project_id=project_id,
            auto_start=auto_start,
        )
