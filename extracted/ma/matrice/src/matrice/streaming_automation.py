"""
Automated script for creating and managing streaming gateways, cameras, and inference pipelines.
Uses Session and management classes for authentication and API communication.
"""

from __future__ import annotations

import json
import mimetypes
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, TypedDict, Union, cast
from urllib.parse import urlparse

# Import Session and management classes
from matrice_common.rpc import RPC
from matrice_common.session import Session

from matrice.camera_management import CameraManagement
from matrice.inference_pipeline_management import InferencePipelineManagement
from matrice.streaming_gateway_management import StreamingGatewayManagement

UNEXPECTED_RESPONSE_FORMAT = "Unexpected response format"
UNKNOWN_ERROR = "Unknown error"


class CameraInfo(TypedDict):
    location_name: Optional[str]
    location_info: Dict[str, str]
    camera_group_name: Optional[str]


# NOTE: mypyc does not support nested class definitions. These TypedDicts
# are defined at module scope and referenced inside methods for type checking
# only; this does not change any runtime logic or behavior.
class _CompleteSetupResults(TypedDict):
    camera_ids: List[str]
    pipeline_id: Optional[str]
    errors: List[str]


class _AutoSetupResults(TypedDict):
    camera_ids: List[str]
    pipeline_id: Optional[str]
    pipeline_name: Optional[str]
    tag: str
    errors: List[str]


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
        # Session.rpc is typed Optional[RPC] (it is cleared on close); here the
        # session is freshly built and always has a live RPC, so narrow it and
        # fail loudly if that invariant is ever violated.
        if self.session.rpc is None:  # type: ignore[attr-defined]
            raise RuntimeError("Session has no active RPC connection")
        self.rpc: RPC = self.session.rpc  # type: ignore[attr-defined]

        # Initialize management classes
        self.gateway_mgmt = StreamingGatewayManagement(self.session)
        self.camera_mgmt = CameraManagement(self.session)
        self.pipeline_mgmt = InferencePipelineManagement(self.session)

        # Cache for video uploads: file_path -> s3_url
        self._video_upload_cache: Dict[str, str] = {}

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
        return len(value) == 24 and all(c in "0123456789abcdefABCDEF" for c in value)

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
                    with open(cameras_input, "r") as f:
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
    def _extract_camera_info(cameras: List[Dict[str, Any]]) -> CameraInfo:
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
        info: CameraInfo = {
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
                    if "locationInfo" in loc and isinstance(loc["locationInfo"], dict):
                        info["location_info"].update(loc["locationInfo"])
                    elif "info" in loc and isinstance(loc["info"], dict):
                        info["location_info"].update(loc["info"])

            if "locationName" in first_camera:
                info["location_name"] = first_camera["locationName"]
            if "locationInfo" in first_camera and isinstance(first_camera["locationInfo"], dict):
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
        parsed = urlparse(path)
        if parsed.scheme in ["http", "https", "s3", "gs", "ftp", "ftps"]:
            return False

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
            ".mp4",
            ".avi",
            ".mov",
            ".mkv",
            ".flv",
            ".wmv",
            ".webm",
            ".m4v",
            ".mpg",
            ".mpeg",
            ".3gp",
            ".f4v",
            ".ts",
        ]

        path_lower = path.lower()
        for ext in video_extensions:
            if path_lower.endswith(ext):
                return True

        # Also check MIME type if available
        mime_type, _ = mimetypes.guess_type(path)
        if mime_type and mime_type.startswith("video/"):
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
        return path.lower().startswith("rtsp://")

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
        if path_lower.split("://", 1)[0] in ("http", "https", "s3"):
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
        video: str = "H.264",
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
            Server type - "redis", "cloud", etc. (default: "redis")
        video : str
            Video codec (default: "H.264")
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
                "maxBandwidthMbps": 0.0,
                "currentBandwidthMbps": 0.0,
            }

        try:
            data, error, _ = self.gateway_mgmt.create_streaming_gateway(
                gateway_name=gateway_name,
                description=description,
                compute_alias=compute_alias,
                account_type=account_type,
                server_type=server_type,
                video=video,
                network_settings=network_settings,
            )

            if error:
                return None, error

            # Extract gateway ID from response
            if data and isinstance(data, dict):
                gateway_id = data.get("id") or data.get("_id")
                if gateway_id and self._is_valid_id(gateway_id):
                    return gateway_id, None

                # Fallback: List gateways and find the one we just created
                gateways, error = self.list_streaming_gateways(page_size=100)
                if error:
                    return None, f"Gateway created but failed to retrieve ID: {error}"

                # Find the gateway with matching name
                for gw in gateways or []:
                    if gw.get("gatewayName") == gateway_name:
                        return gw.get("id") or gw.get("_id"), None

                return None, f"Gateway created but could not find it in list (searched for name: {gateway_name})"
            else:
                return None, "Gateway created but response data is invalid"
        except Exception as e:
            return None, str(e)

    def list_streaming_gateways(self, page_size: int = 20, page: int = 0) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        List all streaming gateways for the account.

        Returns
        -------
        tuple : (list of gateways, error_message)
        """
        try:
            # Note: page parameter is 0-indexed here but 1-indexed in management class
            data, error, _ = self.gateway_mgmt.list_streaming_gateways(
                page=page + 1,
                limit=page_size,  # Convert to 1-indexed
            )

            if error:
                return None, error

            # Extract items from paginated response
            if data and isinstance(data, dict):
                items = data.get("items", [])
                return items, None
            else:
                return None, UNEXPECTED_RESPONSE_FORMAT
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
            _, error, _ = self.gateway_mgmt.start_streaming_gateway(gateway_id)

            if error:
                return False, error

            return True, None
        except Exception as e:
            return False, str(e)

    # ==================== Camera Group Methods ====================
    # CAMERA GROUP METHODS REMOVED FROM FLOW - Commented out

    # def create_camera_group(
    #     self,
    #     camera_group_name: str,
    #     location_id: str,
    #     streaming_gateway_id: str,
    #     default_stream_settings: Optional[Dict[str, Any]] = None,
    # ) -> Tuple[Optional[str], Optional[str]]:
    #     """
    #     Create a camera group.

    #     Parameters
    #     ----------
    #     camera_group_name : str
    #         Name of the camera group
    #     location_id : str
    #         ID of the location
    #     streaming_gateway_id : str
    #         ID of the streaming gateway
    #     default_stream_settings : dict, optional
    #         Default stream settings with aspectRatio, height, width, videoQuality, streamingFPS

    #     Returns
    #     -------
    #     tuple : (camera_group_id, error_message)
    #     """
    #     if default_stream_settings is None:
    #         default_stream_settings = {
    #             "make": "",
    #             "model": "",
    #             "aspectRatio": "16:9",
    #             "height": 480,
    #             "width": 640,
    #             "videoQuality": 80,
    #             "streamingFPS": 10,
    #         }

    #     try:
    #         data, error, message = self.camera_mgmt.create_camera_group(
    #             camera_group_name=camera_group_name,
    #             location_id=location_id,
    #             streaming_gateway_id=streaming_gateway_id,
    #             default_stream_settings=default_stream_settings,
    #         )

    #         if error:
    #             return None, error

    #         # Extract camera group ID from response
    #         if data and isinstance(data, dict):
    #             camera_group_id = data.get("id") or data.get("_id")
    #             if camera_group_id and self._is_valid_id(camera_group_id):
    #                 return camera_group_id, None

    #         # Fallback: List camera groups and find the one we just created
    #         camera_groups, error = self.list_camera_groups(page_size=100)
    #         if error:
    #             return None, f"Camera group created but failed to retrieve ID: {error}"

    #         # Find the camera group with matching name and location
    #         for cg in camera_groups or []:
    #             if (cg.get("cameraGroupName") == camera_group_name and
    #                 cg.get("locationId") == location_id):
    #                 return cg.get("id") or cg.get("_id"), None

    #         return None, f"Camera group created but could not find it in list (searched for name: {camera_group_name})"
    #     except Exception as e:
    #         return None, str(e)

    # def list_camera_groups(
    #     self, page_size: int = 20, page: int = 0
    # ) -> Tuple[Optional[List[Dict]], Optional[str]]:
    #     """
    #     List all camera groups for the account.

    #     Returns
    #     -------
    #     tuple : (list of camera groups, error_message)
    #     """
    #     try:
    #         # Note: page parameter is 0-indexed here but 1-indexed in management class
    #         data, error, message = self.camera_mgmt.list_camera_groups(
    #             page=page + 1,  # Convert to 1-indexed
    #             limit=page_size
    #         )

    #         if error:
    #             return None, error

    #         # Extract items from paginated response
    #         if data and isinstance(data, dict):
    #             items = data.get("items", [])
    #             return items, None
    #         else:
    #             return None, "Unexpected response format"
    #     except Exception as e:
    #         return None, str(e)

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
            presigned_url, error, _ = self.camera_mgmt.get_presigned_url_for_video(file_name)

            if error:
                return None, error

            return presigned_url, None
        except Exception as e:
            return None, str(e)

    def upload_video(self, video_path: str, file_name: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
        """
        Upload a video file to S3 using presigned URL.
        Caches the S3 URL for the same file path to avoid re-uploading.

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
        # Use absolute path as cache key to ensure same file is matched
        abs_path = str(Path(video_path).resolve())

        # Check cache first
        if abs_path in self._video_upload_cache:
            cached_url = self._video_upload_cache[abs_path]
            return cached_url, None

        try:
            s3_url, error, _ = self.camera_mgmt.upload_video_file(video_path, file_name)

            if error or not s3_url:
                return None, error or "Upload returned empty URL"

            # Cache the result for future use
            self._video_upload_cache[abs_path] = s3_url
            return s3_url, None
        except Exception as e:
            return None, str(e)

    # ==================== Camera Methods ====================

    def create_cameras(self, cameras: List[Dict[str, Any]]) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        Create cameras (supports both RTSP and FILE protocol types).
        Checks for existing cameras before creating to avoid duplicate errors.

        Parameters
        ----------
        cameras : list of dict
            List of camera configurations. Each dict should contain:
            - accountNumber: str
            # - cameraGroupId: str  # Camera group removed from flow
            - streamingGatewayId: str
            - locationId: str
            - cameraName: str (optional, auto-generated if not provided)
            - protocolType: str ("RTSP" or "FILE")
            - cameraFeedPath: str (for RTSP)
            - simulationVideoPath: str (for FILE)
            - defaultStreamSettings: dict (optional)

        Returns
        -------
        tuple : (list of created/existing cameras, error_message)
        """
        try:
            result_cameras, error, _ = self.camera_mgmt.create_camera_streams_batch(cameras)

            if error:
                return None, error

            return result_cameras, None
        except Exception as e:
            return None, str(e)

    def get_cameras(
        self,
        camera_group_id: Optional[str] = None,  # Deprecated - camera group removed from flow
        page: int = 1,
        limit: int = 10,
        search: Optional[str] = None,
    ) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        Get cameras. Camera group filtering removed from flow.

        Parameters
        ----------
        camera_group_id : str, optional
            DEPRECATED - Filter cameras by camera group ID (no longer used)
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
            cameras, error, _ = self.camera_mgmt.get_camera_streams_with_filters(
                camera_group_id=None,  # Camera group removed - always pass None
                page=page,
                limit=limit,
                search=search,
            )

            if error:
                return None, error

            return cameras, None
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
        # Note: Uses public API endpoint - no equivalent in management classes
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

            # Cast RPC response to Dict for type-checking; runtime returns dict-like
            resp = cast(Dict[str, Any], self.rpc.get(path=path, timeout=300))
            if resp.get("success"):
                data = resp.get("data", {})
                # Ensure data is a dict before calling .get()
                if isinstance(data, dict):
                    items = data.get("items", [])
                    return items, None
                else:
                    return None, f"Unexpected response format: data is {type(data).__name__}, not dict"
            else:
                return None, resp.get("message", UNKNOWN_ERROR)
        except Exception as e:
            return None, str(e)

    def find_application_by_name(self, application_name: str) -> Tuple[Optional[Dict], Optional[str]]:
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
        # Note: Uses actions API endpoint - no equivalent in management classes
        try:
            path = f"/v1/actions/get_facial_recognition_servers?projectId={project_id}&page={page}&pageSize={page_size}"
            # Cast RPC response to Dict for type-checking; runtime returns dict-like
            resp = cast(Dict[str, Any], self.rpc.get(path=path, timeout=300))
            if resp.get("success"):
                data = resp.get("data", {})
                # Ensure data is a dict before calling .get()
                if isinstance(data, dict):
                    items = data.get("items", [])
                    return items, None
                else:
                    return None, f"Unexpected response format: data is {type(data).__name__}, not dict"
            else:
                return None, resp.get("message", UNKNOWN_ERROR)
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
        # Note: Uses actions API endpoint - no equivalent in management classes
        try:
            path = f"/v1/actions/lpr_servers?project_id={project_id}&account_number={self.account_number}&page={page}&pageSize={page_size}"
            # Cast RPC response to Dict for type-checking; runtime returns dict-like
            resp = cast(Dict[str, Any], self.rpc.get(path=path, timeout=300))
            if resp.get("success"):
                # LPR servers endpoint returns data as array directly
                servers = resp.get("data", [])
                if isinstance(servers, list):
                    return servers, None
                else:
                    return None, UNEXPECTED_RESPONSE_FORMAT
            else:
                return None, resp.get("message", UNKNOWN_ERROR)
        except Exception as e:
            return None, str(e)

    # ==================== Inference Pipeline Methods ====================

    def create_inference_pipeline(
        self,
        name: str,
        project_id: str,
        cameras: List[Dict[str, Any]],
        user_id: str = "",
        description: str = "",
        access_scale: str = "local",
        deploy_type: str = "account",
        server_type: str = "fastapi",
        facial_recognition_server_id: Optional[str] = None,
        lpr_server_id: Optional[str] = None,
        cluster_name: str = "",
        runtime_framework: str = "Triton",
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
        user_id : str
            User ID (required by backend)
        description : str
            Description of the pipeline
        access_scale : str
            Access scale (default: "local")
        deploy_type : str
            Deploy type (default: "real_time")
        server_type : str
            Server type (default: "fastapi", can be empty string "")
        facial_recognition_server_id : str, optional
            Facial recognition server ID (required for FR applications)
        lpr_server_id : str, optional
            LPR server ID (required for LPR applications)
        cluster_name : str, optional
            Cluster name for deployment (e.g., "thor2")
        runtime_framework : str, optional
            Runtime framework (default: "Triton")

        Returns
        -------
        tuple : (pipeline_id, error_message)
        """
        try:
            # Use session user_id if not provided
            if not user_id:
                user_id = getattr(self.session, "user_id", "") or ""
            data, error, _ = self.pipeline_mgmt.create_inference_pipeline(
                name=name,
                project_id=project_id,
                cameras=cameras,
                user_id=user_id,
                description=description,
                access_scale=access_scale,
                deploy_type=deploy_type,
                server_type=server_type,
                facial_recognition_server_id=facial_recognition_server_id,
                lpr_server_id=lpr_server_id,
                cluster_name=cluster_name,
                runtime_framework=runtime_framework,
            )

            if error:
                return None, error

            # Extract pipeline ID from response
            if data and isinstance(data, dict):
                pipeline_id = data.get("id") or data.get("_id")
                if pipeline_id and self._is_valid_id(pipeline_id):
                    return pipeline_id, None

            # API doesn't return ID in response, must list to find it
            pipelines, error = self.list_inference_pipelines(project_id=project_id, page_size=100)
            if error:
                return None, f"Pipeline created but failed to retrieve ID: {error}"

            # Find the pipeline with matching name (most recent one)
            for pipeline in pipelines or []:
                if pipeline.get("name") == name:
                    return pipeline.get("_id") or pipeline.get("id"), None

            return None, f"Pipeline created but could not find it in list (searched for name: {name})"
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
            # Note: page_number is 0-indexed here but 1-indexed in management class
            data, error, _ = self.pipeline_mgmt.list_inference_pipelines(
                project_id=project_id,
                page=page_number + 1,  # Convert to 1-indexed
                limit=page_size,
                sort_by=sort_by,
                sort_order=sort_order,
            )

            if error:
                return None, error

            # Extract items from paginated response
            if data and isinstance(data, dict):
                items = data.get("items", [])
                return items, None
            else:
                return None, UNEXPECTED_RESPONSE_FORMAT
        except Exception as e:
            return None, str(e)

    def start_inference_pipeline(
        self, pipeline_id: str, compute_alias: str, cluster_name: str = ""
    ) -> Tuple[bool, Optional[str]]:
        """
        Start an inference pipeline with compute alias.

        Parameters
        ----------
        pipeline_id : str
            ID of the pipeline to start
        compute_alias : str
            Compute alias to use for the pipeline
        cluster_name : str, optional
            Cluster name for deployment

        Returns
        -------
        tuple : (success, error_message)
        """
        try:
            _, error, _ = self.pipeline_mgmt.start_inference_pipeline(
                pipeline_id=pipeline_id,
                compute_alias=compute_alias,
                cluster_name=cluster_name,
            )

            if error:
                return False, error

            return True, None
        except Exception as e:
            return False, str(e)

    # ==================== Complete Workflow Methods ====================

    def create_complete_setup(
        self,
        cameras: List[Dict[str, Any]],
        project_id: str,
        application_names: List[str],
        cluster_name: str,
        compute_alias: str = "",
        lan_id: str = "",
        start_pipeline: bool = True,
        facial_recognition_server_id: Optional[str] = None,
        lpr_server_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Complete workflow to create cameras and pipeline.
        When cameras are assigned a clusterName, the backend automatically
        resolves the streaming gateway. Locations are replaced by LANs (lanId).

        Parameters
        ----------
        cameras : list of dict
            List of camera configurations. Each camera dict should contain:
            - cameraName: str (optional, auto-generated if not provided)
            - protocolType: str ("RTSP" or "FILE")
            - cameraFeedPath: str (for RTSP) or simulationVideoPath: str (for FILE)
            - Other required fields will be added automatically
        project_id : str
            Project ID
        application_names : list of str
            List of application names to use
        cluster_name : str
            Cluster name for backend gateway resolution
        compute_alias : str
            Compute alias for pipeline
        lan_id : str
            LAN ID (replaces location)
        start_pipeline : bool
            Whether to start the pipeline (default: True)
        facial_recognition_server_id : str, optional
            Facial recognition server ID (required for FR applications)
        lpr_server_id : str, optional
            LPR server ID (required for LPR applications)

        Returns
        -------
        dict : Results dictionary with all created IDs and any errors
        """
        # Using module-level _CompleteSetupResults TypedDict due to mypyc
        # limitation on nested class definitions.

        results: _CompleteSetupResults = {
            "camera_ids": [],
            "pipeline_id": None,
            "errors": [],
        }

        # 1. Add accountNumber, lanId, and clusterName to cameras
        for camera in cameras:
            camera["accountNumber"] = self.account_number
            camera["lanId"] = lan_id
            camera["clusterName"] = cluster_name

        # 2. Create cameras
        created_cameras, error = self.create_cameras(cameras)
        if error:
            results["errors"].append(f"Failed to create cameras: {error}")
            # Cast to Dict to match function annotation without changing logic
            return cast(Dict[str, Any], results)
        results["camera_ids"] = [
            cam_id
            for cam_id in [
                (cam.get("_id") if isinstance(cam, dict) else None)
                or (cam.get("id") if isinstance(cam, dict) else None)
                for cam in (created_cameras or [])
            ]
            if isinstance(cam_id, str)
        ]
        print(f"Created {len(results['camera_ids'])} cameras")

        # 3. Get applications and build cameras array for pipeline
        application_ids: List[Dict[str, str]] = []
        for app_name in application_names:
            app, error = self.find_application_by_name(app_name)
            if error or not app:
                results["errors"].append(f"Failed to find application '{app_name}': {error or 'not found'}")
                continue
            app_id = app.get("_id") or app.get("id")
            if isinstance(app_id, str):
                application_ids.append({"_idApplication": app_id})
            else:
                results["errors"].append(f"Application '{app_name}' missing ID")
        print(f"Found {len(application_ids)} applications")

        # Build cameras array for pipeline (new format)
        pipeline_cameras: List[Dict[str, Any]] = []
        for camera_id in results["camera_ids"]:
            pipeline_cameras.append(
                {
                    "cameraId": camera_id,
                    "applications": application_ids,
                }
            )

        # 4. Create inference pipeline (using new format)
        pipeline_unique_id = str(uuid.uuid4())[:8]
        pipeline_name = f"pipeline-{pipeline_unique_id}"
        pipeline_id, error = self.create_inference_pipeline(
            name=pipeline_name,
            project_id=project_id,
            cameras=pipeline_cameras,
            facial_recognition_server_id=facial_recognition_server_id,
            lpr_server_id=lpr_server_id,
            cluster_name=cluster_name,
        )
        if error or not pipeline_id:
            results["errors"].append(f"Failed to create pipeline: {error or 'unknown error'}")
            # Cast to Dict to match function annotation without changing logic
            return cast(Dict[str, Any], results)
        results["pipeline_id"] = pipeline_id
        print(f"Created inference pipeline: {pipeline_id}")

        # 5. Start pipeline if requested
        if start_pipeline and results["pipeline_id"]:
            _, error = self.start_inference_pipeline(results["pipeline_id"], compute_alias)
            if error:
                results["errors"].append(f"Failed to start pipeline: {error}")
            else:
                print(f"Started inference pipeline: {pipeline_id}")

        # Cast to Dict to match function annotation without changing logic
        return cast(Dict[str, Any], results)

    def _normalize_camera_for_setup(
        self,
        camera: Dict[str, Any],
        lan_id: str,
        cluster_name: str,
        results: "_AutoSetupResults",
    ) -> Optional[Dict[str, Any]]:
        """Normalize a single camera dict for auto setup.

        Returns the normalized camera dict, or None if the camera should be
        skipped (e.g. local video upload failed).
        """
        # Generate default camera name using UUID if not provided
        cam_unique_id = str(uuid.uuid4())[:8]
        default_camera_name = f"camera-{cam_unique_id}"

        normalized: Dict[str, Any] = {
            "accountNumber": self.account_number,
            "lanId": lan_id,
            "clusterName": cluster_name,
        }

        # Copy existing fields - try multiple field name variations
        camera_name = None
        for key in ["cameraName", "camera_name", "name"]:
            if key in camera and camera[key]:
                camera_name = str(camera[key])
                break

        # Use provided name or auto-generate
        normalized["cameraName"] = camera_name or default_camera_name

        # Get the path/URL from various possible fields
        path = (
            camera.get("cameraFeedPath")
            or camera.get("camera_feed_path")
            or camera.get("simulationVideoPath")
            or camera.get("simulation_video_path")
            or camera.get("video_path")
            or camera.get("video_url")
            or camera.get("rtsp_url")
            or camera.get("url")
            or camera.get("path")
            or camera.get("feed_path")
            or camera.get("stream_url")
            or ""
        )

        # Auto-detect protocol type if not provided
        protocol_type = camera.get("protocolType") or camera.get("protocol_type") or camera.get("protocol")
        if not protocol_type and path:
            protocol_type = self._detect_protocol_type(str(path))
        elif not protocol_type:
            protocol_type = "RTSP"  # Default

        # Handle local video file upload
        if protocol_type == "FILE" and path:
            if self._is_local_file(str(path)):
                # Check cache first
                abs_path = str(Path(str(path)).resolve())
                if abs_path in self._video_upload_cache:
                    # Use cached S3 URL
                    path = self._video_upload_cache[abs_path]
                    print(f"  Using cached S3 URL: {path}")
                else:
                    # Upload the video (upload_video will cache it)
                    print(f"  Uploading local video file: {path}")
                    # Generate unique filename using UUID to avoid conflicts
                    file_unique_id = str(uuid.uuid4())[:8]
                    original_name = Path(str(path)).name
                    file_name = f"video-{file_unique_id}-{original_name}"

                    s3_url, error = self.upload_video(str(path), file_name)
                    if error or not s3_url:
                        results["errors"].append(f"Failed to upload video '{path}': {error or 'unknown error'}")
                        print(f"  Failed to upload video: {error}")
                        # Skip this camera
                        return None
                    else:
                        path = s3_url
                        print(f"  Uploaded to: {s3_url}")

        normalized["protocolType"] = str(protocol_type)

        # Add protocol-specific fields
        if protocol_type == "RTSP":
            normalized["cameraFeedPath"] = str(path)
        elif protocol_type == "FILE":
            normalized["simulationVideoPath"] = str(path)

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
                "streamingFPS": 10,
                "aspectRatio": "16:9",
                "videoQuality": 80,
            }

        return normalized

    def _resolve_default_application_ids(
        self,
        application_names: Optional[List[str]],
        results: "_AutoSetupResults",
    ) -> List[Dict[str, str]]:
        """Resolve a list of application names into ``_idApplication`` dicts."""
        default_application_ids: List[Dict[str, str]] = []
        if application_names:
            for app_name in application_names:
                app, error = self.find_application_by_name(app_name)
                if error or not app:
                    results["errors"].append(f"Failed to find application '{app_name}': {error or 'not found'}")
                    continue
                app_id = app.get("_id") or app.get("id")
                if isinstance(app_id, str):
                    default_application_ids.append({"_idApplication": app_id})
                else:
                    results["errors"].append(f"Application '{app_name}' missing ID")
        return default_application_ids

    def _build_pipeline_cameras(
        self,
        parsed_cameras: List[Dict[str, Any]],
        default_application_ids: List[Dict[str, str]],
        results: "_AutoSetupResults",
    ) -> List[Dict[str, Any]]:
        """Build the cameras array for a pipeline using per-camera or default apps."""
        pipeline_cameras: List[Dict[str, Any]] = []
        for idx, camera_id in enumerate(results["camera_ids"]):
            # Check if this camera has specific apps
            camera_apps: Optional[List[Dict[str, str]]] = None
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
                    camera_app_ids: List[Dict[str, str]] = []
                    for app_name in camera_specific_apps:
                        if (
                            isinstance(app_name, dict)
                            and "_idApplication" in app_name
                            and isinstance(app_name["_idApplication"], str)
                        ):
                            camera_app_ids.append({"_idApplication": app_name["_idApplication"]})
                        elif isinstance(app_name, str):
                            app, error = self.find_application_by_name(app_name)
                            if error or not app:
                                results["errors"].append(
                                    f"Failed to find application '{app_name}' for camera {idx + 1}: {error or 'not found'}"
                                )
                                continue
                            app_id = app.get("_id") or app.get("id")
                            if isinstance(app_id, str):
                                camera_app_ids.append({"_idApplication": app_id})
                            else:
                                results["errors"].append(f"Application '{app_name}' missing ID")

                    if camera_app_ids:
                        camera_apps = camera_app_ids

            # Use camera-specific apps or default apps
            apps_to_use = camera_apps if camera_apps else default_application_ids

            if apps_to_use:
                pipeline_cameras.append({"cameraId": camera_id, "applications": apps_to_use})
        return pipeline_cameras

    def auto_setup_from_cameras(
        self,
        cameras: Union[str, Dict, List[Dict]],
        compute_alias: str,
        cluster_name: str,
        lan_id: str = "",
        project_id: Optional[str] = None,
        application_names: Optional[List[str]] = None,
        auto_start: bool = False,
        facial_recognition_server_id: Optional[str] = None,
        lpr_server_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Fully automated setup from camera data. Only requires minimal inputs.

        When cameras are assigned a clusterName, the backend automatically
        resolves the streaming gateway. Locations are replaced by LANs (lanId).

        This method automatically:
        - Parses cameras from various formats (JSON string, dict, list of dicts, file path)
        - Creates cameras with lanId and clusterName
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
            Compute alias for the inference pipeline
        cluster_name : str
            Cluster name for backend gateway resolution
        lan_id : str
            LAN ID (replaces location)
        project_id : str, optional
            Project ID (uses session project_id if not provided)
        application_names : list of str, optional
            List of application names to add to pipeline (e.g., ["People Counting", "Color Detection"])
            If not provided, pipeline will be created without applications
        auto_start : bool
            Whether to automatically start pipeline (default: False)
        facial_recognition_server_id : str, optional
            Facial recognition server ID (required for FR applications like "Face Recognition")
        lpr_server_id : str, optional
            LPR server ID (required for LPR applications like "License Plate Recognition")

        Returns
        -------
        dict : Results dictionary with all created IDs, tags, and any errors
            {
                "camera_ids": [...],
                "pipeline_id": "...",
                "pipeline_name": "...",
                "tag": "...",  # Auto-generated tag for this setup
                "errors": []
            }
        """
        # Using module-level _AutoSetupResults TypedDict due to mypyc
        # limitation on nested class definitions.

        results: _AutoSetupResults = {
            "camera_ids": [],
            "pipeline_id": None,
            "pipeline_name": None,
            "tag": self._generate_tag("setup"),
            "errors": [],
        }

        # Use project_id from session if not provided
        if not project_id:
            project_id = getattr(self.session, "project_id", None)
            if not project_id:
                results["errors"].append("Project ID is required")
                # Cast to Dict to match function annotation without changing logic
                return cast(Dict[str, Any], results)

        # Parse cameras
        try:
            parsed_cameras = self._parse_cameras(cameras)
            if not parsed_cameras:
                results["errors"].append("No cameras found in input")
                # Cast to Dict to match function annotation without changing logic
                return cast(Dict[str, Any], results)
        except Exception as e:
            results["errors"].append(f"Failed to parse cameras: {str(e)}")
            # Cast to Dict to match function annotation without changing logic
            return cast(Dict[str, Any], results)

        # 1. Normalize cameras - ensure they have required fields and auto-upload videos
        normalized_cameras: List[Dict[str, Any]] = []
        for camera in parsed_cameras:
            normalized = self._normalize_camera_for_setup(camera, lan_id, cluster_name, results)
            if normalized is not None:
                normalized_cameras.append(normalized)

        # 2. Create cameras
        created_cameras, error = self.create_cameras(normalized_cameras)
        if error:
            results["errors"].append(f"Failed to create cameras: {error}")
            # Cast to Dict to match function annotation without changing logic
            return cast(Dict[str, Any], results)
        results["camera_ids"] = [
            cam_id
            for cam_id in [
                (cam.get("_id") if isinstance(cam, dict) else None)
                or (cam.get("id") if isinstance(cam, dict) else None)
                for cam in (created_cameras or [])
            ]
            if isinstance(cam_id, str)
        ]
        print(f"Created {len(results['camera_ids'])} cameras")

        # 3. Create inference pipeline if applications provided
        # Support per-camera apps or default apps
        has_any_apps = False

        # Check if any camera has apps or if default apps are provided
        for camera in parsed_cameras:
            if camera.get("apps") or camera.get("applications"):
                has_any_apps = True
                break

        if has_any_apps or application_names:
            # Build default application IDs
            default_application_ids = self._resolve_default_application_ids(application_names, results)

            # Build cameras array for pipeline with per-camera or default apps
            pipeline_cameras = self._build_pipeline_cameras(parsed_cameras, default_application_ids, results)

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
                    cluster_name=cluster_name,
                )
                if error or not pipeline_id:
                    results["errors"].append(f"Failed to create pipeline: {error or 'unknown error'}")
                else:
                    results["pipeline_id"] = pipeline_id
                    results["pipeline_name"] = pipeline_name
                    print(f"Created inference pipeline: {pipeline_name} ({pipeline_id})")

                    # 4. Start pipeline if requested
                    if auto_start and results["pipeline_id"]:
                        _, error = self.start_inference_pipeline(results["pipeline_id"], compute_alias)
                        if error:
                            results["errors"].append(f"Failed to start pipeline: {error}")
                        else:
                            print(f"Started inference pipeline: {pipeline_name}")

        # Cast to Dict to match function annotation without changing logic
        return cast(Dict[str, Any], results)

    def quick_setup(
        self,
        cameras: Union[str, List[Dict[str, Any]]],
        cluster_name: str,
        compute_alias: Optional[str] = None,
        lan_id: str = "",
        apps: Optional[Union[str, List[str]]] = None,
        project_id: Optional[str] = None,
        auto_start: bool = False,
        facial_recognition_server_id: Optional[str] = None,
        lpr_server_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Quick setup wrapper around auto_setup_from_cameras.
        Parses application names and delegates to auto_setup_from_cameras.
        """
        # Generate compute_alias if not provided (using UUID to avoid conflicts)
        if not compute_alias:
            compute_alias = ""

        # Parse application names
        application_names: Optional[List[str]] = None
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
        resp = self.auto_setup_from_cameras(
            cameras=cameras,
            compute_alias=compute_alias,
            cluster_name=cluster_name,
            lan_id=lan_id,
            project_id=project_id,
            application_names=application_names,
            auto_start=auto_start,
            facial_recognition_server_id=facial_recognition_server_id,
            lpr_server_id=lpr_server_id,
        )

        return resp

    def setup_from_paths(
        self,
        paths: Union[str, List[str]],
        cluster_name: str,
        compute_alias: Optional[str] = None,
        lan_id: str = "",
        apps: Optional[Union[str, List[str]]] = None,
        project_id: Optional[str] = None,
        auto_start: bool = False,
    ) -> Dict[str, Any]:
        """
        Ultra-simple setup - just provide camera paths as strings.
        Everything else is auto-generated with UUID-based names.

        When cameras are assigned a clusterName, the backend automatically
        resolves the streaming gateway. Locations are replaced by LANs (lanId).

        Parameters
        ----------
        paths : str or list of str
            Camera paths/URLs:
            - Single path: "rtsp://192.168.1.100:554/stream1"
            - Multiple paths: ["rtsp://...", "/path/to/video.mp4", "https://..."]
        cluster_name : str
            Cluster name for backend gateway resolution
        compute_alias : str, optional
            Compute alias (auto-generated if not provided)
        lan_id : str
            LAN ID (replaces location)
        apps : str or list of str, optional
            Application names (optional)
        project_id : str, optional
            Project ID (uses session project_id if not provided)
        auto_start : bool
            Whether to auto-start pipeline (default: False)

        Returns
        -------
        dict : Results with all created IDs and any errors

        Examples
        --------
        ```python
        # Single path
        results = automation.setup_from_paths(
            "rtsp://192.168.1.100:554/stream1",
            cluster_name="thor2",
        )

        # Multiple paths
        results = automation.setup_from_paths(
            [
                "rtsp://192.168.1.100:554/stream1",
                "rtsp://192.168.1.101:554/stream1",
                "/path/to/video.mp4"
            ],
            cluster_name="thor2",
        )

        # With apps
        results = automation.setup_from_paths(
            ["rtsp://...", "/path/to/video.mp4"],
            cluster_name="thor2",
            apps="People Counting",
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
            cluster_name=cluster_name,
            compute_alias=compute_alias,
            lan_id=lan_id,
            apps=apps,
            project_id=project_id,
            auto_start=auto_start,
        )

    def add_cameras_and_applications_to_pipeline(
        self,
        pipeline_id: str,
        cameras: List[Dict[str, Any]],
        compute_alias: str = "",
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Add cameras and applications to an existing pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID
        cameras : list of dict
            List of camera configurations with cameraId and applications
        compute_alias : str, optional
            Compute resource alias

        Returns
        -------
        tuple
            (result_dict, error) - Result dict if successful, error message if failed

        Examples
        --------
        >>> cameras = [
        ...     {
        ...         "cameraId": "507f1f77bcf86cd799439017",  # pragma: allowlist secret
        ...         "applications": [{"_idApplication": "507f1f77bcf86cd799439023"}]  # pragma: allowlist secret
        ...     }
        ... ]
        >>> result, error = automation.add_cameras_and_applications_to_pipeline(
        ...     pipeline_id="507f1f77bcf86cd799439022",
        ...     cameras=cameras,
        ...     compute_alias="inference-compute-01"
        ... )
        """
        result, error, _ = self.pipeline_mgmt.add_cameras_and_applications_to_pipeline(
            pipeline_id=pipeline_id,
            cameras=cameras,
            compute_alias=compute_alias,
        )
        return result, error
