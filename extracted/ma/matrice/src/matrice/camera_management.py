"""Module to handle camera management operations including locations, groups, streams, and topics."""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests
from matrice_common.utils import handle_response


class CameraManagement:
    """
    A class for handling camera management operations using the backend API.

    This includes camera locations, camera groups, camera streams, and camera topics.

    Attributes
    ----------
    session : Session
        The session object used for API interactions.
    account_number : str
        The account number associated with the session.
    rpc : RPC
        The RPC object for making API calls.

    Examples
    --------
    >>> from matrice_common.session import Session
    >>> session = Session(account_number="ACC123", access_key="key", secret_key="secret")
    >>> camera_mgmt = CameraManagement(session)
    >>>
    >>> # Create a location
    >>> location, error, message = camera_mgmt.create_location(
    ...     location_name="Building A",
    ...     street_address="123 Main St",
    ...     city="San Francisco",
    ...     state="CA",
    ...     country="USA"
    ... )
    """

    def __init__(self, session):
        """
        Initialize the CameraManagement class.

        Parameters
        ----------
        session : Session
            The session object with authentication credentials
        """
        self.session = session
        self.account_number = session.account_number
        self.rpc = session.rpc

    # ==================== Camera Group Management ====================

    def create_camera_group(
        self,
        camera_group_name: str,
        lan_id: str = "",
        streaming_gateway_id: str = "",
        default_stream_settings: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Create a new camera group.

        Parameters
        ----------
        camera_group_name : str
            Name of the camera group
        lan_id : str, optional
            ID of the LAN
        streaming_gateway_id : str, optional
            ID of the streaming gateway
        default_stream_settings : dict, optional
            Default stream settings including make, model, aspectRatio, height, width,
            videoQuality, streamingFPS

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Camera group details
            - str or None: Error message if failed
            - str: Status message

        Examples
        --------
        >>> settings = {
        ...     "make": "Hikvision",
        ...     "model": "DS-2CD2143G0-I",
        ...     "aspectRatio": "16:9",
        ...     "height": 1080,
        ...     "width": 1920,
        ...     "videoQuality": 85,
        ...     "streamingFPS": 30
        ... }
        >>> group, error, message = camera_mgmt.create_camera_group(
        ...     camera_group_name="Parking Cameras",
        ...     lan_id="507f1f77bcf86cd799439011",
        ...     streaming_gateway_id="507f1f77bcf86cd799439012",
        ...     default_stream_settings=settings
        ... )
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

        path = "/v1/inference/create_camera_group"
        payload = {
            "accountNumber": self.account_number,
            "cameraGroupName": camera_group_name,
            "lanId": lan_id,
            "streamingGatewayId": streaming_gateway_id,
            "defaultStreamSettings": default_stream_settings,
        }

        resp = self.rpc.post(path=path, payload=payload)
        return handle_response(
            resp,
            "Camera group created successfully",
            "Failed to create camera group",
        )

    def create_camera_group_vms(
        self, camera_ids: List[str], group_name: str
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Create a VMS camera group.

                Parameters
                ----------
                camera_ids : list of str
                    List of camera IDs to include in the VMS group
                group_name : str
                    Name of the VMS group

                Returns
                -------
                tuple
                    A tuple containing:
                    - dict: VMS group details
                    - str or None: Error message if failed
                    - str: Status message
        """
        path = "/v1/inference/create_camera_group_vms"
        payload = {
            "cameraIds": camera_ids,
            "accountNumber": self.account_number,
            "groupName": group_name,
        }

        resp = self.rpc.post(path=path, payload=payload)
        return handle_response(
            resp,
            "VMS camera group created successfully",
            "Failed to create VMS camera group",
        )

    def get_camera_groups_by_account(self) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all camera groups for the account.

                Returns
                -------
                tuple
                    A tuple containing:
                    - list: List of camera group dictionaries
                    - str or None: Error message if failed
                    - str: Status message
        """
        path = f"/v1/inference/camera_groups_by_acc_number/{self.account_number}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Camera groups retrieved successfully",
            "Failed to retrieve camera groups",
        )

    def get_camera_group_dashboard(self, page: int = 1, limit: int = 10) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get camera group dashboard with pagination.

                Parameters
                ----------
                page : int, optional
                    Page number (default: 1)
                limit : int, optional
                    Items per page (default: 10)

                Returns
                -------
                tuple
                    A tuple containing:
                    - dict: Dashboard data with groups and statistics
                    - str or None: Error message if failed
                    - str: Status message
        """
        path = (
            f"/v1/inference/get_camera_group_dashboard?page={page}&limit={limit}&account_number={self.account_number}"
        )
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Camera group dashboard retrieved successfully",
            "Failed to retrieve camera group dashboard",
        )

    def get_camera_group_by_id(self, group_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get a specific camera group by ID.

                Parameters
                ----------
                group_id : str
                    The camera group ID

                Returns
                -------
                tuple
                    A tuple containing:
                    - dict: Camera group details
                    - str or None: Error message if failed
                    - str: Status message
        """
        path = f"/v1/inference/get_camera_group/{group_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Camera group retrieved successfully",
            "Failed to retrieve camera group",
        )

    def list_camera_groups(self, page: int = 1, limit: int = 10) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        List all camera groups with pagination.

                Parameters
                ----------
                page : int, optional
                    Page number (default: 1)
                limit : int, optional
                    Items per page (default: 10)

                Returns
                -------
                tuple
                    A tuple containing:
                    - dict: Paginated camera groups data
                    - str or None: Error message if failed
                    - str: Status message
        """
        path = f"/v1/inference/all_camera_groups_pag/{self.account_number}?page={page}&limit={limit}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Camera groups list retrieved successfully",
            "Failed to retrieve camera groups list",
        )

    def get_camera_groups_by_gateway_id(self, gateway_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all camera groups for a specific gateway.

                Parameters
                ----------
                gateway_id : str
                    The streaming gateway ID

                Returns
                -------
                tuple
                    A tuple containing:
                    - list: List of camera groups
                    - str or None: Error message if failed
                    - str: Status message
        """
        path = f"/v1/inference/all_camera_groups_by_gateway_id/{gateway_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Camera groups retrieved successfully",
            "Failed to retrieve camera groups for gateway",
        )

    def get_camera_group_vms_by_account(self) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all VMS camera groups for the account.

                Returns
                -------
                tuple
                    A tuple containing:
                    - list: List of VMS camera groups
                    - str or None: Error message if failed
                    - str: Status message
        """
        path = f"/v1/inference/camera_group_vms_by_acc_number?account_number={self.account_number}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "VMS camera groups retrieved successfully",
            "Failed to retrieve VMS camera groups",
        )

    def get_camera_groups_by_group_id_vms(self, group_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get camera groups by VMS group ID.

                Parameters
                ----------
                group_id : str
                    The VMS group ID

                Returns
                -------
                tuple
                    A tuple containing:
                    - list: List of camera groups
                    - str or None: Error message if failed
                    - str: Status message
        """
        path = f"/v1/inference/camera_groups_by_groupId_vms/{group_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Camera groups retrieved successfully",
            "Failed to retrieve camera groups by VMS group ID",
        )

    def update_camera_group(
        self,
        group_id: str,
        camera_group_name: Optional[str] = None,
        lan_id: Optional[str] = None,
        streaming_gateway_id: Optional[str] = None,
        default_stream_settings: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update a camera group.

        Parameters
        ----------
        group_id : str
            The camera group ID to update
        camera_group_name : str, optional
            New camera group name
        lan_id : str, optional
            New LAN ID
        streaming_gateway_id : str, optional
            New streaming gateway ID
        default_stream_settings : dict, optional
            New default stream settings

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Updated camera group details
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/update_camera_group/{group_id}"
        payload: Dict[str, Any] = {}

        if camera_group_name is not None:
            payload["cameraGroupName"] = camera_group_name
        if lan_id is not None:
            payload["lanId"] = lan_id
        if streaming_gateway_id is not None:
            payload["streamingGatewayId"] = streaming_gateway_id
        if default_stream_settings is not None:
            payload["defaultStreamSettings"] = default_stream_settings

        resp = self.rpc.put(path=path, payload=payload)
        return handle_response(
            resp,
            "Camera group updated successfully",
            "Failed to update camera group",
        )

    def delete_camera_group(self, group_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Delete a camera group.

                Parameters
                ----------
                group_id : str
                    The camera group ID to delete

                Returns
                -------
                tuple
                    A tuple containing:
                    - dict: Deletion confirmation
                    - str or None: Error message if failed
                    - str: Status message
        """
        path = f"/v1/inference/delete_camera_group/{group_id}"
        resp = self.rpc.delete(path=path)
        return handle_response(
            resp,
            "Camera group deleted successfully",
            "Failed to delete camera group",
        )

    # ==================== Camera Stream Management ====================

    def create_camera_stream(
        self,
        camera_name: str,
        lan_id: str = "",
        streaming_gateway_id: str = "",
        cluster_name: str = "",
        protocol_type: str = "RTSP",
        camera_feed_path: str = "",
        simulation_video_path: str = "",
        custom_stream_settings: Optional[Dict[str, Any]] = None,
        applications: Optional[List[Dict[str, Any]]] = None,
        memory_usage_mb: float = 0.0,
        is_active: bool = True,
        custom_schedule: bool = False,
        location_id: str = "",
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Create a new camera stream.

        When ``cluster_name`` is provided the backend automatically resolves the
        streaming gateway and media storage for the given account + cluster, so
        ``streaming_gateway_id`` can be omitted.

        Parameters
        ----------
        camera_name : str
            Name of the camera
        lan_id : str, optional
            ID of the LAN (Local Area Network) the camera belongs to
        streaming_gateway_id : str, optional
            ID of the streaming gateway (not required when cluster_name is set)
        cluster_name : str, optional
            Cluster name – backend auto-assigns gateway and media storage
        protocol_type : str, optional
            Protocol type - "RTSP", "IP", or "FILE" (default: "RTSP")
        camera_feed_path : str, optional
            RTSP URL for live camera feed
        simulation_video_path : str, optional
            S3 path for simulation video (for FILE protocol)
        custom_stream_settings : dict, optional
            Custom stream settings
        applications : list of dict, optional
            List of applications to attach to the camera
        memory_usage_mb : float, optional
            Estimated memory usage in MB
        is_active : bool, optional
            Whether the camera is active (default: True)
        custom_schedule : bool, optional
            Whether the camera uses a custom schedule (default: False)
        location_id : str, optional
            DEPRECATED – use ``lan_id`` instead

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Camera stream details
            - str or None: Error message if failed
            - str: Status message

        Examples
        --------
        >>> camera, error, message = camera_mgmt.create_camera_stream(
        ...     camera_name="Entrance Camera 1",
        ...     lan_id="507f1f77bcf86cd799439011",
        ...     cluster_name="thor2",
        ...     protocol_type="RTSP",
        ...     camera_feed_path="rtsp://admin:pass@192.168.1.100:554/stream1"  # pragma: allowlist secret
        ... )

        Security note: ``camera_feed_path`` embeds camera credentials in the URL
        (``user:pass@``). Treat this value as a secret -- it is transmitted and
        stored by the backend, so it must never be written to logs or exports.
        Redact it (strip userinfo and query string) before printing.
        """
        # Backwards-compatible alias
        if location_id and not lan_id:
            import warnings

            warnings.warn("location_id is deprecated, use lan_id instead", DeprecationWarning, stacklevel=2)
            lan_id = location_id

        path = "/v1/inference/create_camera_stream"
        payload: Dict[str, Any] = {
            "accountNumber": self.account_number,
            "cameraName": camera_name,
            "protocolType": protocol_type,
            "cameraFeedPath": camera_feed_path,
            "simulationVideoPath": simulation_video_path,
            "isActive": is_active,
            "customSchedule": custom_schedule,
        }

        if lan_id:
            payload["lanId"] = lan_id
        if streaming_gateway_id:
            payload["streamingGatewayId"] = streaming_gateway_id
        if cluster_name:
            payload["clusterName"] = cluster_name
        if memory_usage_mb:
            payload["memoryUsageMB"] = memory_usage_mb
        if custom_stream_settings is not None:
            payload["customStreamSettings"] = custom_stream_settings
        if applications is not None:
            payload["applications"] = applications

        resp = self.rpc.post(path=path, payload=[payload], timeout=600)
        return handle_response(
            resp,
            "Camera stream created successfully",
            "Failed to create camera stream",
        )

    def attach_gateway_to_cameras(
        self, camera_ids: List[str], streaming_gateway_id: str
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Attach a streaming gateway to multiple cameras.

        Parameters
        ----------
        camera_ids : list of str
            List of camera IDs
        streaming_gateway_id : str
            ID of the streaming gateway

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Operation result
            - str or None: Error message if failed
            - str: Status message
        """
        path = "/v1/inference/attach_gateway_to_cameras"
        payload = {
            "cameraIds": camera_ids,
            "streamingGatewayId": streaming_gateway_id,
        }

        resp = self.rpc.post(path=path, payload=payload)
        return handle_response(
            resp,
            "Gateway attached to cameras successfully",
            "Failed to attach gateway to cameras",
        )

    def get_camera_stream_dashboard(self, page: int = 1, limit: int = 10) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get camera stream dashboard with pagination.

        Parameters
        ----------
        page : int, optional
            Page number (default: 1)
        limit : int, optional
            Items per page (default: 10)

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Dashboard data with cameras and statistics
            - str or None: Error message if failed
            - str: Status message
        """
        path = (
            f"/v1/inference/get_camera_stream_dashboard?page={page}&limit={limit}&account_number={self.account_number}"
        )
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Camera stream dashboard retrieved successfully",
            "Failed to retrieve camera stream dashboard",
        )

    def get_camera_streams_by_account(self) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all camera streams for the account.

        Returns
        -------
        tuple
            A tuple containing:
            - list: List of camera streams
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/get_camerastream_by_acc_number/{self.account_number}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Camera streams retrieved successfully",
            "Failed to retrieve camera streams",
        )

    def get_camera_stream_by_id(self, camera_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get a specific camera stream by ID.

        Parameters
        ----------
        camera_id : str
            The camera ID

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Camera stream details
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/get_camera_stream/{camera_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Camera stream retrieved successfully",
            "Failed to retrieve camera stream",
        )

    def get_simulated_stream_url(self, camera_id: str) -> Tuple[Optional[str], Optional[str], str]:
        """
        Get the simulated stream URL for a camera.

        Parameters
        ----------
        camera_id : str
            The camera ID

        Returns
        -------
        tuple
            A tuple containing:
            - str: Simulated stream URL
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/get_simulated_stream_url/{camera_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Simulated stream URL retrieved successfully",
            "Failed to retrieve simulated stream URL",
        )

    def list_camera_streams(self, page: int = 1, limit: int = 10) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        List all camera streams with pagination.

        Parameters
        ----------
        page : int, optional
            Page number (default: 1)
        limit : int, optional
            Items per page (default: 10)

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Paginated camera streams data
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/all_camera_streams_pag/{self.account_number}?page={page}&limit={limit}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Camera streams list retrieved successfully",
            "Failed to retrieve camera streams list",
        )

    def get_cameras_by_group_id(self, group_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all cameras in a specific group.

        Parameters
        ----------
        group_id : str
            The camera group ID

        Returns
        -------
        tuple
            A tuple containing:
            - list: List of cameras
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/all_camera_by_group_id/{group_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Cameras retrieved successfully",
            "Failed to retrieve cameras by group ID",
        )

    def get_cameras_by_streaming_gateway_id(self, gateway_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all cameras for a specific streaming gateway.

        Parameters
        ----------
        gateway_id : str
            The streaming gateway ID

        Returns
        -------
        tuple
            A tuple containing:
            - list: List of cameras
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/all_camera_by_streaming_gateway_id/{gateway_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Cameras retrieved successfully",
            "Failed to retrieve cameras by gateway ID",
        )

    def check_camera_application_usage(
        self, camera_id: str, application_id: str
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Check if a camera-application combination is in use.

        Parameters
        ----------
        camera_id : str
            The camera ID
        application_id : str
            The application ID

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Usage information with 'inUse', 'pipelineIds', 'isActive', 'deploymentId'
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/check_camera_application_usage/{camera_id}/{application_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Camera application usage checked successfully",
            "Failed to check camera application usage",
        )

    def get_cameras_by_app_deployment(self, app_deployment_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get cameras using a specific application deployment.

        Parameters
        ----------
        app_deployment_id : str
            The application deployment ID

        Returns
        -------
        tuple
            A tuple containing:
            - list: List of cameras
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/cameras_by_app_deployment/{app_deployment_id}?account_number={self.account_number}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Cameras retrieved successfully",
            "Failed to retrieve cameras by app deployment",
        )

    def update_camera_stream(
        self,
        camera_id: str,
        camera_name: Optional[str] = None,
        lan_id: Optional[str] = None,
        streaming_gateway_id: Optional[str] = None,
        cluster_name: Optional[str] = None,
        protocol_type: Optional[str] = None,
        camera_feed_path: Optional[str] = None,
        simulation_video_path: Optional[str] = None,
        custom_stream_settings: Optional[Dict[str, Any]] = None,
        applications: Optional[List[Dict[str, Any]]] = None,
        is_active: Optional[bool] = None,
        custom_schedule: Optional[bool] = None,
        media_storage_id: Optional[str] = None,
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update a camera stream.

        Parameters
        ----------
        camera_id : str
            The camera ID to update
        camera_name : str, optional
            New camera name
        lan_id : str, optional
            New LAN ID
        streaming_gateway_id : str, optional
            New streaming gateway ID
        cluster_name : str, optional
            New cluster name
        protocol_type : str, optional
            New protocol type
        camera_feed_path : str, optional
            New camera feed path
        simulation_video_path : str, optional
            New simulation video path
        custom_stream_settings : dict, optional
            New custom stream settings
        applications : list of dict, optional
            New applications list
        is_active : bool, optional
            Whether the camera is active
        custom_schedule : bool, optional
            Whether the camera uses a custom schedule
        media_storage_id : str, optional
            New media storage ID

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Updated camera details
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/update_camera_stream/{camera_id}"
        payload: Dict[str, Any] = {}

        if camera_name is not None:
            payload["cameraName"] = camera_name
        if lan_id is not None:
            payload["lanId"] = lan_id
        if streaming_gateway_id is not None:
            payload["streamingGatewayId"] = streaming_gateway_id
        if cluster_name is not None:
            payload["clusterName"] = cluster_name
        if protocol_type is not None:
            payload["protocolType"] = protocol_type
        if camera_feed_path is not None:
            payload["cameraFeedPath"] = camera_feed_path
        if simulation_video_path is not None:
            payload["simulationVideoPath"] = simulation_video_path
        if custom_stream_settings is not None:
            payload["customStreamSettings"] = custom_stream_settings
        if applications is not None:
            payload["applications"] = applications
        if is_active is not None:
            payload["isActive"] = is_active
        if custom_schedule is not None:
            payload["customSchedule"] = custom_schedule
        if media_storage_id is not None:
            payload["mediaStorageId"] = media_storage_id

        resp = self.rpc.put(path=path, payload=payload)
        return handle_response(
            resp,
            "Camera stream updated successfully",
            "Failed to update camera stream",
        )

    def delete_camera_stream(self, camera_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Delete a camera stream.

        Parameters
        ----------
        camera_id : str
            The camera ID to delete

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Deletion confirmation
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/delete_camera_stream/{camera_id}"
        resp = self.rpc.delete(path=path)
        return handle_response(
            resp,
            "Camera stream deleted successfully",
            "Failed to delete camera stream",
        )

    def remove_camera_application_from_pipeline(
        self, camera_id: str, application_id: str
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Remove a camera application from its pipeline.

        Parameters
        ----------
        camera_id : str
            The camera ID
        application_id : str
            The application ID

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Operation result
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/remove_camera_application_from_pipeline/{camera_id}/{application_id}"
        resp = self.rpc.delete(path=path)
        return handle_response(
            resp,
            "Camera application removed from pipeline successfully",
            "Failed to remove camera application from pipeline",
        )

    # ==================== Video Upload Methods ====================

    def get_presigned_url_for_video(self, file_name: str) -> Tuple[Optional[str], Optional[str], str]:
        """
        Get a presigned URL for video upload to S3.

        Parameters
        ----------
        file_name : str
            Name of the file to upload

        Returns
        -------
        tuple
            A tuple containing:
            - str: Presigned URL for upload
            - str or None: Error message if failed
            - str: Status message

        Examples
        --------
        >>> url, error, message = camera_mgmt.get_presigned_url_for_video("my_video.mp4")
        >>> if not error:
        ...     # Use the presigned URL to upload the video
        ...     pass
        """
        path = f"/v1/inference/get_presigned_url_stream?fileName={file_name}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Presigned URL retrieved successfully",
            "Failed to get presigned URL",
        )

    def upload_video_file(
        self, video_path: str, file_name: Optional[str] = None
    ) -> Tuple[Optional[str], Optional[str], str]:
        """
        Upload a video file to S3 using a presigned URL.

        Parameters
        ----------
        video_path : str
            Path to the local video file
        file_name : str, optional
            Name for the uploaded file (defaults to original filename)

        Returns
        -------
        tuple
            A tuple containing:
            - str: S3 URL of the uploaded video
            - str or None: Error message if failed
            - str: Status message

        Examples
        --------
        >>> s3_url, error, message = camera_mgmt.upload_video_file("/path/to/video.mp4")
        >>> if not error:
        ...     print(f"Video uploaded to: {s3_url}")
        """
        video_file = Path(video_path)
        if not video_file.exists():
            return None, f"Video file not found: {video_path}", "Failed to upload video"

        if file_name is None:
            file_name = video_file.name

        # Get presigned URL
        presigned_url, error, message = self.get_presigned_url_for_video(file_name)
        if error:
            return None, error, message
        if presigned_url is None:
            return None, "Presigned URL is missing", "Failed to upload video"

        # Upload file to presigned URL
        try:
            with open(video_file, "rb") as f:
                resp = requests.put(presigned_url, data=f, timeout=300)
                resp.raise_for_status()

            # Extract S3 URL (remove query parameters)
            s3_url = presigned_url.split("?")[0]
            return s3_url, None, "Video uploaded successfully"
        except Exception as e:
            return None, str(e), "Failed to upload video to S3"

    # ==================== Batch Camera Operations ====================

    def create_camera_streams_batch(
        self, cameras: List[Dict[str, Any]]
    ) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Create multiple camera streams in batch.
        Checks for existing cameras before creating to avoid duplicate errors.
        Camera group removed from flow.

        Parameters
        ----------
        cameras : list of dict
            List of camera configurations. Each dict should contain:
            - accountNumber: str
            - lanId: str (optional – LAN ID)
            - clusterName: str (optional – backend auto-assigns gateway)
            - streamingGatewayId: str (optional if clusterName provided)
            - cameraName: str (optional, auto-generated if not provided)
            - protocolType: str ("RTSP", "IP", or "FILE")
            - cameraFeedPath: str (for RTSP/IP)
            - simulationVideoPath: str (for FILE)
            - customStreamSettings: dict (optional)

        Returns
        -------
        tuple
            A tuple containing:
            - list: List of created/existing camera streams
            - str or None: Error message if failed
            - str: Status message

        Examples
        --------
        >>> cameras = [
        ...     {
        ...         "accountNumber": "ACC123",
        ...         "clusterName": "thor2",
        ...         "lanId": "507f1f77bcf86cd799439011",  # pragma: allowlist secret
        ...         "cameraName": "Camera 1",
        ...         "protocolType": "RTSP",
        ...         "cameraFeedPath": "rtsp://192.168.1.100:554/stream1"
        ...     },
        ...     {
        ...         "accountNumber": "ACC123",
        ...         "clusterName": "thor2",
        ...         "lanId": "507f1f77bcf86cd799439011",  # pragma: allowlist secret
        ...         "cameraName": "Camera 2",
        ...         "protocolType": "FILE",
        ...         "simulationVideoPath": "https://s3.amazonaws.com/bucket/video.mp4"
        ...     }
        ... ]
        >>> created_cameras, error, message = camera_mgmt.create_camera_streams_batch(cameras)
        """
        if not cameras:
            return [], None, "No cameras to create"

        # Generate random camera names for cameras that don't have them
        for cam in cameras:
            if not cam.get("cameraName"):
                cam_unique_id = str(uuid.uuid4())[:8]
                cam["cameraName"] = f"camera-{cam_unique_id}"

        # Get camera names to check for existing cameras
        camera_names = [cam.get("cameraName") for cam in cameras if cam.get("cameraName")]
        if not camera_names:
            return None, "No camera names found in camera configurations", "Failed to create cameras"

        # Check for existing cameras by name
        all_cameras_data, error, message = self.get_camera_streams_by_account()
        if error:
            return None, f"Failed to check existing cameras: {error}", "Failed to create cameras"

        # Find existing cameras by name
        existing_cameras = {}
        all_cameras = all_cameras_data if isinstance(all_cameras_data, list) else []
        for cam in all_cameras:
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
            return list(existing_cameras.values()), None, "All cameras already exist"

        # Create cameras using batch endpoint
        path = "/v1/inference/create_camera_stream"
        resp = self.rpc.post(path=path, payload=cameras_to_create, timeout=600)

        if resp.get("success"):
            # Get all cameras again to find the newly created ones
            all_cameras_data, error, message = self.get_camera_streams_by_account()
            if error:
                return None, f"Cameras created but failed to retrieve: {error}", "Failed to retrieve created cameras"

            # Find all cameras (both existing and newly created)
            result_cameras = []
            all_cameras = all_cameras_data if isinstance(all_cameras_data, list) else []
            for cam in all_cameras:
                cam_name = cam.get("cameraName")
                if cam_name in camera_names:
                    result_cameras.append(cam)

            return result_cameras, None, "Cameras created successfully"
        else:
            # Check if error is "already exists" - if so, return existing cameras
            error_message = resp.get("message", "Unknown error")
            if "already exists" in error_message.lower() or "Camera stream already exists" in error_message:
                # Return existing cameras we found earlier
                result_cameras = list(existing_cameras.values())
                # Try to get any newly created cameras
                # get_camera_streams_by_account returns (data, error, message)
                # Unpack all three to avoid mypy/mypyc tuple size mismatch
                all_cameras_data, _, _ = self.get_camera_streams_by_account()
                if all_cameras_data and isinstance(all_cameras_data, list):
                    for cam in all_cameras_data:
                        cam_name = cam.get("cameraName")
                        if cam_name in camera_names and cam_name not in existing_cameras:
                            result_cameras.append(cam)
                return result_cameras, None, "Some cameras already exist"
            else:
                return None, error_message, "Failed to create cameras"

    def get_camera_streams_with_filters(
        self,
        camera_group_id: Optional[str] = None,  # Deprecated - camera group removed from flow
        page: int = 1,
        limit: int = 10,
        # ── Filter 1: Camera Name (UI column: "Camera Name", operator: contains) ──
        search: Optional[str] = None,
        # ── Filter 2: Protocol Type (UI column: "Protocol Type", operator: equals) ─
        protocol_type: Optional[str] = None,
        # ── Filter 3: Feed Path (UI column: "Feed Path", operator: contains) ───────
        feed_path_contains: Optional[str] = None,
        # ── Filter 4: Aspect Ratio (UI column: "Aspect Ratio", operator: equals) ───
        aspect_ratio: Optional[str] = None,
        # ── Filter 5: Dimensions (UI column: "Dimensions", operator: equals) ───────
        width: Optional[int] = None,
        height: Optional[int] = None,
        # ── Filter 6: Streaming FPS (UI column: "Streaming FPS", operator: equals) ─
        streaming_fps: Optional[int] = None,
        # ── Filter 7: Memory Usage (UI column: "Memory Usage", operator: range) ────
        memory_min_mb: Optional[float] = None,
        memory_max_mb: Optional[float] = None,
    ) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get camera streams with filtering and pagination support.

        All filters are applied client-side after fetching the full camera list
        from the API. They match exactly the column filters exposed in the
        Matrice UI camera table.

        Parameters
        ----------
        camera_group_id : str, optional
            DEPRECATED - no longer used.
        page : int, optional
            Page number for pagination (default: 1).
        limit : int, optional
            Number of cameras per page returned by the API (default: 10).
            Increase this when using local filters so enough results are fetched
            before filtering (e.g. ``limit=1000``).
        search : str, optional
            **UI: Camera Name contains** — case-insensitive substring match
            on ``cameraName``, applied client-side.
        protocol_type : str, optional
            **UI: Protocol Type equals** — ``"RTSP"``, ``"FILE"``, or ``"IP"``.
        feed_path_contains : str, optional
            **UI: Feed Path contains** — substring match on ``cameraFeedPath``
            (RTSP/IP) or ``simulationVideoPath`` (FILE), case-insensitive.
        aspect_ratio : str, optional
            **UI: Aspect Ratio equals** — e.g. ``"16:9"``, ``"4:3"``.
            Reads ``customStreamSettings.aspectRatio``.
        width : int, optional
            **UI: Dimensions width equals** — reads ``customStreamSettings.width``.
        height : int, optional
            **UI: Dimensions height equals** — reads ``customStreamSettings.height``.
        streaming_fps : int, optional
            **UI: Streaming FPS equals** — reads ``customStreamSettings.streamingFPS``.
        memory_min_mb : float, optional
            **UI: Memory Usage >=** — lower bound on ``memoryUsageMB``.
        memory_max_mb : float, optional
            **UI: Memory Usage <=** — upper bound on ``memoryUsageMB``.

        Returns
        -------
        tuple
            A tuple containing:
            - list: Camera streams matching all supplied filters.
            - str or None: Error message if the API call failed.
            - str: Status message.

        Examples
        --------
        >>> # Filter by name (server-side)
        >>> cameras, error, msg = camera_mgmt.get_camera_streams_with_filters(
        ...     search="entrance", limit=50
        ... )

        >>> # Filter by protocol type (local)
        >>> cameras, error, msg = camera_mgmt.get_camera_streams_with_filters(
        ...     protocol_type="FILE", limit=200
        ... )

        >>> # Filter by dimensions + FPS (local)
        >>> cameras, error, msg = camera_mgmt.get_camera_streams_with_filters(
        ...     width=1920, height=1080, streaming_fps=30, limit=200
        ... )

        >>> # Filter by feed path substring (local)
        >>> cameras, error, msg = camera_mgmt.get_camera_streams_with_filters(
        ...     feed_path_contains="s3.us-west", limit=200
        ... )

        >>> # Filter by memory usage range (local)
        >>> cameras, error, msg = camera_mgmt.get_camera_streams_with_filters(
        ...     memory_min_mb=100, memory_max_mb=500, limit=200
        ... )
        """
        # ── 1. Build and execute the API request ─────────────────────────────
        path = f"/v1/inference/get_camerastream_by_acc_number/{self.account_number}"
        params: Dict[str, str] = {"page": str(page), "limit": str(limit)}

        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        resp = self.rpc.get(path=f"{path}?{query_string}")

        if not resp.get("success"):
            return None, resp.get("message", "Unknown error"), "Failed to retrieve camera streams"

        cameras = resp.get("data", [])
        if isinstance(cameras, dict) and "items" in cameras:
            cameras = cameras["items"]
        if not isinstance(cameras, list):
            cameras = []

        # ── 2. Apply local filters (Filters 1-7) ─────────────────────────────
        # Filter 1 — Camera Name contains (client-side, case-insensitive)
        # The backend endpoint does not honour the ?search= param, so we filter here.
        if search:
            needle = search.lower()
            cameras = [c for c in cameras if needle in (c.get("cameraName") or "").lower()]

        # Filter 2 — Protocol Type
        if protocol_type is not None:
            cameras = [c for c in cameras if c.get("protocolType", "").upper() == protocol_type.upper()]

        # Filter 3 — Feed Path contains
        if feed_path_contains is not None:
            needle = feed_path_contains.lower()
            cameras = [
                c for c in cameras if needle in (c.get("cameraFeedPath") or c.get("simulationVideoPath") or "").lower()
            ]

        # Filters 4, 5, 6 all read from customStreamSettings
        needs_stream_settings = (
            aspect_ratio is not None or width is not None or height is not None or streaming_fps is not None
        )
        if needs_stream_settings:

            def _ss(cam: Dict) -> Dict:
                return cam.get("customStreamSettings") or {}

            # Filter 4 — Aspect Ratio
            if aspect_ratio is not None:
                cameras = [c for c in cameras if _ss(c).get("aspectRatio") == aspect_ratio]

            # Filter 5 — Dimensions (width and/or height)
            if width is not None:
                cameras = [c for c in cameras if _ss(c).get("width") == width]
            if height is not None:
                cameras = [c for c in cameras if _ss(c).get("height") == height]

            # Filter 6 — Streaming FPS
            if streaming_fps is not None:
                cameras = [c for c in cameras if _ss(c).get("streamingFPS") == streaming_fps]

        # Filter 7 — Memory Usage
        if memory_min_mb is not None:
            cameras = [c for c in cameras if (c.get("memoryUsageMB") or 0) >= memory_min_mb]
        if memory_max_mb is not None:
            cameras = [c for c in cameras if (c.get("memoryUsageMB") or 0) <= memory_max_mb]

        return cameras, None, "Camera streams retrieved successfully"

    # ==================== Camera Stream Topics Management ====================

    def create_camera_stream_topic(
        self,
        camera_id: str,
        streaming_gateway_id: str,
        server_id: str,
        server_type: str,
        topic_name: str,
        topic_type: str,
        ip_address: str,
        port: int,
        status: str = "active",
        is_active: bool = True,
        consuming_apps_deployment_ids: Optional[List[str]] = None,
        app_deployment_id: Optional[str] = None,
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Create a camera stream topic (Kafka/Redis).

        Parameters
        ----------
        camera_id : str
            The camera ID
        streaming_gateway_id : str
            The streaming gateway ID
        server_id : str
            The server ID
        server_type : str
            Server type - "kafka" or "redis"
        topic_name : str
            Name of the topic
        topic_type : str
            Topic type - "input" or "output"
        ip_address : str
            IP address of the server
        port : int
            Port number
        status : str, optional
            Status of the topic (default: "active")
        is_active : bool, optional
            Whether the topic is active (default: True)
        consuming_apps_deployment_ids : list of str, optional
            List of consuming application deployment IDs
        app_deployment_id : str, optional
            Application deployment ID

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Topic details
            - str or None: Error message if failed
            - str: Status message
        """
        path = "/v1/inference/create_camera_stream_topic"
        payload = {
            "accountNumber": self.account_number,
            "cameraId": camera_id,
            "streamingGatewayId": streaming_gateway_id,
            "serverId": server_id,
            "serverType": server_type,
            "topicName": topic_name,
            "topicType": topic_type,
            "ipAddress": ip_address,
            "port": port,
            "status": status,
            "isActive": is_active,
        }

        if consuming_apps_deployment_ids is not None:
            payload["consumingAppsDeploymentIds"] = consuming_apps_deployment_ids
        if app_deployment_id is not None:
            payload["appDeploymentId"] = app_deployment_id

        resp = self.rpc.post(path=path, payload=payload, timeout=600)
        return handle_response(
            resp,
            "Camera stream topic created successfully",
            "Failed to create camera stream topic",
        )

    def append_consuming_app_deployment_id(
        self,
        camera_id: str,
        streaming_id: str,
        topic_type: str,
        app_deployment_id: str,
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Append a consuming app deployment ID to a topic.

        Parameters
        ----------
        camera_id : str
            The camera ID
        streaming_id : str
            The streaming gateway ID
        topic_type : str
            Topic type - "input" or "output"
        app_deployment_id : str
            Application deployment ID to append

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Updated topic details
            - str or None: Error message if failed
            - str: Status message
        """
        path = "/v1/inference/append_consuming_app_deployment_id"
        payload = {
            "cameraId": camera_id,
            "streamingId": streaming_id,
            "topicType": topic_type,
            "appDeploymentId": app_deployment_id,
        }

        resp = self.rpc.put(path=path, payload=payload)
        return handle_response(
            resp,
            "App deployment ID appended successfully",
            "Failed to append app deployment ID",
        )

    def update_topic_ip_and_port(
        self,
        camera_id: str,
        streaming_id: str,
        topic_type: str,
        ip_address: str,
        port: int,
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update IP address and port of a topic.

        Parameters
        ----------
        camera_id : str
            The camera ID
        streaming_id : str
            The streaming gateway ID
        topic_type : str
            Topic type - "input" or "output"
        ip_address : str
            New IP address
        port : int
            New port number

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Updated topic details
            - str or None: Error message if failed
            - str: Status message
        """
        path = "/v1/inference/update_ip_and_port"
        payload = {
            "cameraId": camera_id,
            "streamingId": streaming_id,
            "topicType": topic_type,
            "ipAddress": ip_address,
            "port": port,
        }

        resp = self.rpc.put(path=path, payload=payload)
        return handle_response(
            resp,
            "Topic IP and port updated successfully",
            "Failed to update topic IP and port",
        )

    def get_camera_output_topics_by_camera_id(self, camera_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all output topics for a camera.

        Parameters
        ----------
        camera_id : str
            The camera ID

        Returns
        -------
        tuple
            A tuple containing:
            - list: List of output topics
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/get_camera_output_topics_by_camera_id/{camera_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Camera output topics retrieved successfully",
            "Failed to retrieve camera output topics",
        )

    def get_camera_input_topic_by_camera_id(self, camera_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get the input topic for a camera.

        Parameters
        ----------
        camera_id : str
            The camera ID

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Input topic details
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/get_camera_input_topic_by_camera_id/{camera_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Camera input topic retrieved successfully",
            "Failed to retrieve camera input topic",
        )

    def get_camera_output_topic_by_cam_id_and_app_deployment_id(
        self, camera_id: str, app_deployment_id: str
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get camera output topic by camera ID and app deployment ID.

        Parameters
        ----------
        camera_id : str
            The camera ID
        app_deployment_id : str
            The application deployment ID

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Output topic details
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/get_camera_output_topic_by_cam_id_and_app_deployment_id/{camera_id}/{app_deployment_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Camera output topic retrieved successfully",
            "Failed to retrieve camera output topic",
        )

    def get_topics_by_streaming_id_and_server_id(
        self, streaming_id: str, server_id: str
    ) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get topics by streaming gateway ID and server ID.

        Parameters
        ----------
        streaming_id : str
            The streaming gateway ID
        server_id : str
            The server ID

        Returns
        -------
        tuple
            A tuple containing:
            - list: List of topics
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/get_topics_by_streaming_id_and_server_id/{streaming_id}/{server_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Topics retrieved successfully",
            "Failed to retrieve topics",
        )

    def get_topics_by_server_id(self, server_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all topics for a server.

        Parameters
        ----------
        server_id : str
            The server ID

        Returns
        -------
        tuple
            A tuple containing:
            - list: List of topics
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/get_topics_by_server_id/{server_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Topics retrieved successfully",
            "Failed to retrieve topics by server ID",
        )

    def get_input_topics_by_app_deployment_id(
        self, app_deployment_id: str
    ) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get input topics for an application deployment.

        Parameters
        ----------
        app_deployment_id : str
            The application deployment ID

        Returns
        -------
        tuple
            A tuple containing:
            - list: List of input topics
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/get_input_topics_by_app_deployment_id/{app_deployment_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Input topics retrieved successfully",
            "Failed to retrieve input topics",
        )

    def get_output_topics_by_app_deployment_id(
        self, app_deployment_id: str
    ) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get output topics for an application deployment.

        Parameters
        ----------
        app_deployment_id : str
            The application deployment ID

        Returns
        -------
        tuple
            A tuple containing:
            - list: List of output topics
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/get_output_topics_by_app_deployment_id/{app_deployment_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Output topics retrieved successfully",
            "Failed to retrieve output topics",
        )

    # ==================== Pipeline Camera Queries ====================

    def get_cameras_by_inference_pipeline(self, pipeline_id: str) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all cameras associated with an inference pipeline.

        Parameters
        ----------
        pipeline_id : str
            The inference pipeline ID

        Returns
        -------
        tuple
            A tuple containing:
            - list: List of camera dictionaries
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/cameras_by_inference_pipeline/{pipeline_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Cameras retrieved successfully",
            "Failed to retrieve cameras for pipeline",
        )

    def get_cameras_by_inference_pipeline_filtered(
        self, pipeline_id: str, **filters
    ) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get cameras for an inference pipeline with filters.

        Parameters
        ----------
        pipeline_id : str
            The inference pipeline ID
        **filters
            Query parameters to filter cameras (e.g., status="active")

        Returns
        -------
        tuple
            A tuple containing:
            - list: List of filtered camera dictionaries
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/cameras_by_inference_pipeline_filtered/{pipeline_id}"
        if filters:
            query_params = "&".join(f"{k}={v}" for k, v in filters.items())
            path += f"?{query_params}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Filtered cameras retrieved successfully",
            "Failed to retrieve filtered cameras for pipeline",
        )

    def get_cameras_batch_info(self, camera_ids: List[str]) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get batch information for multiple cameras.

        Parameters
        ----------
        camera_ids : list of str
            List of camera IDs to get info for

        Returns
        -------
        tuple
            A tuple containing:
            - list: List of camera info dictionaries
            - str or None: Error message if failed
            - str: Status message
        """
        path = "/v1/inference/cameras/batch_info"
        payload = {"cameraIds": camera_ids}
        resp = self.rpc.post(path=path, payload=payload)
        return handle_response(
            resp,
            "Camera batch info retrieved successfully",
            "Failed to retrieve camera batch info",
        )

    # ==================== Recording Management ====================

    def start_recording(self, camera_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Start recording for a camera.

        Parameters
        ----------
        camera_id : str
            The camera ID to start recording

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Recording start confirmation
            - str or None: Error message if failed
            - str: Status message
        """
        path = "/v1/inference/recording/start"
        payload = {"cameraId": camera_id}
        resp = self.rpc.post(path=path, payload=payload)
        return handle_response(
            resp,
            "Recording started successfully",
            "Failed to start recording",
        )

    def stop_recording(self, camera_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Stop recording for a camera.

        Parameters
        ----------
        camera_id : str
            The camera ID to stop recording

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Recording stop confirmation
            - str or None: Error message if failed
            - str: Status message
        """
        path = "/v1/inference/recording/stop"
        payload = {"cameraId": camera_id}
        resp = self.rpc.post(path=path, payload=payload)
        return handle_response(
            resp,
            "Recording stopped successfully",
            "Failed to stop recording",
        )

    def get_camera_group_id_by_camera(self, camera_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get the camera group ID for a specific camera.

        Parameters
        ----------
        camera_id : str
            The camera ID

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Camera group info
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/get_camera_group_id_by_camera/{camera_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Camera group ID retrieved successfully",
            "Failed to retrieve camera group ID",
        )
