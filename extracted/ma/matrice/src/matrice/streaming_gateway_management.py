"""Module to handle streaming gateway management operations."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple, cast

from matrice_common.utils import handle_response


class StreamingGatewayManagement:
    """
    A class for handling streaming gateway management operations using the backend API.

    This includes gateway creation, control, monitoring, and heartbeat management.

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
    >>> gateway_mgmt = StreamingGatewayManagement(session)
    >>>
    >>> # Create a streaming gateway
    >>> gateway, error, message = gateway_mgmt.create_streaming_gateway(
    ...     gateway_name="Main Gateway",
    ...     description="Primary streaming gateway",
    ...     compute_alias="redis-compute-01"
    ... )
    """

    def __init__(self, session):
        """
        Initialize the StreamingGatewayManagement class.

        Parameters
        ----------
        session : Session
            The session object with authentication credentials
        """
        self.session = session
        self.account_number = session.account_number
        self.rpc = session.rpc

    # ==================== Gateway Management ====================

    def create_streaming_gateway(
        self,
        gateway_name: str,
        description: str = "",
        account_type: str = "enterprise",
        status: str = "created",
        server_type: str = "redis",
        network_settings: Optional[Dict[str, Any]] = None,
        compute_alias: str = "",
        cluster_name: str = "",
        video: str = "H.264",
        user_id: str = "",
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Create a new streaming gateway.

        Parameters
        ----------
        gateway_name : str
            Name of the gateway
        description : str, optional
            Description of the gateway
        account_type : str, optional
            Account type - "enterprise" or other (default: "enterprise")
        status : str, optional
            Initial status (default: "created")
        server_type : str, optional
            Server type - "redis", "cloud", etc. (default: "redis")
        network_settings : dict, optional
            Network configuration with IPAddress, port, accessScale, region,
            maxBandwidthMbps, currentBandwidthMbps
        compute_alias : str, optional
            Compute resource alias
        cluster_name : str, optional
            Name of the cluster
        video : str, optional
            Video codec - "H.264", "H.265", "Frame" (default: "H.264")
        user_id : str, optional
            User ID creating the gateway

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Gateway details including ID, status, network settings
            - str or None: Error message if failed
            - str: Status message

        Examples
        --------
        >>> network_settings = {
        ...     "IPAddress": "10.0.1.100",
        ...     "port": 8080,
        ...     "accessScale": "regional",
        ...     "region": "us-west-2",
        ...     "maxBandwidthMbps": 1000.0,
        ...     "currentBandwidthMbps": 0.0
        ... }
        >>> gateway, error, message = gateway_mgmt.create_streaming_gateway(
        ...     gateway_name="Campus Gateway",
        ...     description="Main campus streaming gateway",
        ...     network_settings=network_settings,
        ...     compute_alias="redis-compute-01"
        ... )
        """
        if network_settings is None:
            network_settings = {
                "IPAddress": "",
                "port": 0,
                "accessScale": "local",
                "region": "",
                "maxBandwidthMbps": 0.0,
                "currentBandwidthMbps": 0.0,
            }

        path = "/v1/inference/create_streaming_gateway"
        payload = {
            "accountNumber": self.account_number,
            "accountType": account_type,
            "gatewayName": gateway_name,
            "description": description,
            "status": status,
            "serverType": server_type,
            "networkSettings": network_settings,
            "computeAlias": compute_alias,
            "clusterName": cluster_name,
            "video": video,
        }

        if user_id:
            payload["userID"] = user_id

        resp = self.rpc.post(path=path, payload=payload)
        return handle_response(
            resp,
            "Streaming gateway created successfully",
            "Failed to create streaming gateway",
        )

    def start_streaming_gateway(self, gateway_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Start a streaming gateway.

        Parameters
        ----------
        gateway_id : str
            The gateway ID to start

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Updated gateway with status "starting" or "running"
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/start_streaming_gateway/{gateway_id}"
        resp = self.rpc.post(path=path, payload={})
        return handle_response(
            resp,
            "Streaming gateway started successfully",
            "Failed to start streaming gateway",
        )

    def stop_streaming_gateway(self, gateway_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Stop a streaming gateway.

        Parameters
        ----------
        gateway_id : str
            The gateway ID to stop

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Updated gateway with status "stopped"
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/stop_streaming_gateway/{gateway_id}"
        resp = self.rpc.post(path=path, payload={})
        return handle_response(
            resp,
            "Streaming gateway stopped successfully",
            "Failed to stop streaming gateway",
        )

    def get_streaming_gateway_dashboard(
        self, page: int = 1, limit: int = 10
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get streaming gateway dashboard with pagination.

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
            - dict: Dashboard data with gateways and statistics
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/get_streaming_gateway_dashboard?page={page}&limit={limit}&account_number={self.account_number}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Streaming gateway dashboard retrieved successfully",
            "Failed to retrieve streaming gateway dashboard",
        )

    def get_streaming_gateways_by_account(
        self,
    ) -> Tuple[Optional[List[Dict]], Optional[str], str]:
        """
        Get all streaming gateways for the account.

        Returns
        -------
        tuple
            A tuple containing:
            - list: List of streaming gateways
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/streaming_gateways_by_acc_number/{self.account_number}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Streaming gateways retrieved successfully",
            "Failed to retrieve streaming gateways",
        )

    def get_streaming_gateway_by_id(self, gateway_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Get a specific streaming gateway by ID.

        Parameters
        ----------
        gateway_id : str
            The gateway ID

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Gateway details
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/get_streaming_gateways/{gateway_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Streaming gateway retrieved successfully",
            "Failed to retrieve streaming gateway",
        )

    def list_streaming_gateways(self, page: int = 1, limit: int = 10) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        List all streaming gateways with pagination.

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
            - dict: Paginated gateways data with 'items', 'total', 'page', 'limit'
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/all_streaming_gateways_pag/{self.account_number}?page={page}&limit={limit}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Streaming gateways list retrieved successfully",
            "Failed to retrieve streaming gateways list",
        )

    def update_streaming_gateway(
        self,
        gateway_id: str,
        gateway_name: str = None,
        description: str = None,
        account_type: str = None,
        server_type: str = None,
        network_settings: Optional[Dict[str, Any]] = None,
        compute_alias: str = None,
        cluster_name: str = None,
        video: str = None,
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update a streaming gateway.

        Parameters
        ----------
        gateway_id : str
            The gateway ID to update
        gateway_name : str, optional
            New gateway name
        description : str, optional
            New description
        account_type : str, optional
            New account type
        server_type : str, optional
            New server type
        network_settings : dict, optional
            New network settings
        compute_alias : str, optional
            New compute alias
        cluster_name : str, optional
            New cluster name
        video : str, optional
            New video codec

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Updated gateway details
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/update_streaming_gateway/{gateway_id}"
        payload: Dict[str, Any] = {}

        if gateway_name is not None:
            payload["gatewayName"] = gateway_name
        if description is not None:
            payload["description"] = description
        if account_type is not None:
            payload["accountType"] = account_type
        if server_type is not None:
            payload["serverType"] = server_type
        if network_settings is not None:
            payload["networkSettings"] = network_settings
        if compute_alias is not None:
            payload["computeAlias"] = compute_alias
        if cluster_name is not None:
            payload["clusterName"] = cluster_name
        if video is not None:
            payload["video"] = video

        resp = self.rpc.put(path=path, payload=payload)
        return handle_response(
            resp,
            "Streaming gateway updated successfully",
            "Failed to update streaming gateway",
        )

    def update_streaming_gateway_status(
        self, gateway_id: str, status: str
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update the status of a streaming gateway.

        Parameters
        ----------
        gateway_id : str
            The gateway ID
        status : str
            New status - "starting", "running", "stopped", "failed", "created"

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Updated gateway details
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/update_streaming_gateway_status/{gateway_id}?status={status}"
        resp = self.rpc.put(path=path, payload={})
        return handle_response(
            resp,
            f"Streaming gateway status updated to '{status}' successfully",
            "Failed to update streaming gateway status",
        )

    def delete_streaming_gateway(self, gateway_id: str) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Delete a streaming gateway.

        Parameters
        ----------
        gateway_id : str
            The gateway ID to delete

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Deletion confirmation
            - str or None: Error message if failed
            - str: Status message
        """
        path = f"/v1/inference/delete_streaming_gateway/{gateway_id}"
        resp = self.rpc.delete(path=path)
        return handle_response(
            resp,
            "Streaming gateway deleted successfully",
            "Failed to delete streaming gateway",
        )

    # ==================== Gateway Heartbeat Management ====================

    def add_streaming_gateway_heartbeat(
        self,
        gateway_id: str,
        timestamp: str,
        status: str,
        metrics: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Add a heartbeat record for a streaming gateway.

        Parameters
        ----------
        gateway_id : str
            The gateway ID
        timestamp : str
            Timestamp in ISO format (e.g., "2025-11-12T10:30:00Z")
        status : str
            Current status of the gateway
        metrics : dict, optional
            Metrics data including cpuUsage, memoryUsage, bandwidthUsage, etc.

        Returns
        -------
        tuple
            A tuple containing:
            - dict: Heartbeat record details
            - str or None: Error message if failed
            - str: Status message

        Examples
        --------
        >>> metrics = {
        ...     "cpuUsage": 45.2,
        ...     "memoryUsage": 60.5,
        ...     "bandwidthUsage": 250.0
        ... }
        >>> heartbeat, error, message = gateway_mgmt.add_streaming_gateway_heartbeat(
        ...     gateway_id="507f1f77bcf86cd799439012",
        ...     timestamp="2025-11-12T10:30:00Z",
        ...     status="running",
        ...     metrics=metrics
        ... )
        """
        path = f"/v1/inference/add_streaming_gateway_heartbeat/{gateway_id}"
        payload: Dict[str, Any] = {
            "timestamp": timestamp,
            "status": status,
        }

        if metrics is not None:
            payload["metrics"] = cast(Any, metrics)

        resp = self.rpc.post(path=path, payload=payload)
        return handle_response(
            resp,
            "Gateway heartbeat added successfully",
            "Failed to add gateway heartbeat",
        )
