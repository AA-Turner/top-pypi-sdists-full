"""Module providing streaming gateway manager functionality for deployments."""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict


@dataclass
class StreamingGatewayConfig:
    """
    Streaming gateway configuration data class.
    
    Attributes:
        id: Unique identifier for the streaming gateway (MongoDB ObjectID)
        id_service: Deployment ID this gateway belongs to (MongoDB ObjectID)
        name: Name of the streaming gateway
        description: Description of the streaming gateway
        camera_group_ids: List of camera group IDs associated with this gateway
        status: Status of the streaming gateway (e.g., "active", "inactive")
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    name: str
    description: Optional[str] = None
    camera_group_ids: Optional[List[str]] = None
    id: Optional[str] = None
    id_service: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def __post_init__(self):
        if self.camera_group_ids is None:
            self.camera_group_ids = []
    
    def to_dict(self) -> Dict:
        """Convert the streaming gateway config to a dictionary for API calls."""
        if not self.name or not self.name.strip():
            raise ValueError("Gateway name is required")
            
        data = {
            "name": self.name,
            "cameraGroupIds": self.camera_group_ids or []
        }
        if self.description:
            data["description"] = self.description
        if self.id:
            data["_id"] = self.id
        if self.id_service:
            data["idService"] = self.id_service
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'StreamingGatewayConfig':
        """Create a StreamingGatewayConfig instance from API response data."""
        return cls(
            id=data.get("_id") or data.get("id") or data.get("ID"),
            id_service=data.get("idService") or data.get("IDService"),
            name=data.get("name") or data.get("Name"),
            description=data.get("description") or data.get("Description"),
            camera_group_ids=data.get("cameraGroupIds") or data.get("CameraGroupIds"),
            status=data.get("status") or data.get("Status"),
            created_at=data.get("createdAt") or data.get("CreatedAt"),
            updated_at=data.get("updatedAt") or data.get("UpdatedAt")
        )


class StreamingGateway:
    """
    Streaming gateway instance class for managing individual streaming gateways.
    
    This class represents a single streaming gateway and provides methods to manage
    its configuration, camera groups, and operational status.
    
    Example:
        Basic usage:
        ```python
        from matrice import Session
        from matrice.deployment.streaming_gateway_manager import StreamingGateway, StreamingGatewayConfig
        
        session = Session(account_number="...", access_key="...", secret_key="...")
        
        # Create gateway config
        config = StreamingGatewayConfig(
            name="Main Gateway",
            description="Primary streaming gateway",
            camera_group_ids=["group1", "group2"]
        )
        
        # Create gateway instance
        gateway = StreamingGateway(session, config)
        
        # Save to backend
        result, error, message = gateway.save()
        if not error:
            print(f"Gateway created with ID: {gateway.id}")
            
        # Update configuration
        gateway.description = "Updated description"
        result, error, message = gateway.update()
        ```
    """
    
    def __init__(self, session, config: StreamingGatewayConfig = None, gateway_id: str = None):
        """
        Initialize a StreamingGateway instance.
        
        Args:
            session: Session object containing RPC client for API communication
            config: StreamingGatewayConfig object (for new gateways)
            gateway_id: ID of existing gateway to load (mutually exclusive with config)
        """
        if not config and not gateway_id:
            raise ValueError("Either config or gateway_id must be provided")
        
        self.session = session
        self.rpc = session.rpc
        
        if gateway_id:
            # Load existing gateway
            self.config = None
            self._load_from_id(gateway_id)
        else:
            # New gateway from config
            self.config = config
    
    @property
    def id(self) -> Optional[str]:
        """Get the gateway ID."""
        return self.config.id if self.config else None
    
    @property
    def name(self) -> str:
        """Get the gateway name."""
        return self.config.name if self.config else ""
    
    @name.setter
    def name(self, value: str):
        """Set the gateway name."""
        if self.config:
            self.config.name = value
    
    @property
    def description(self) -> Optional[str]:
        """Get the gateway description."""
        return self.config.description if self.config else None
    
    @description.setter
    def description(self, value: str):
        """Set the gateway description."""
        if self.config:
            self.config.description = value
    
    @property
    def camera_group_ids(self) -> List[str]:
        """Get the camera group IDs."""
        return self.config.camera_group_ids if self.config else []
    
    @camera_group_ids.setter
    def camera_group_ids(self, value: List[str]):
        """Set the camera group IDs."""
        if self.config:
            self.config.camera_group_ids = value
    
    @property
    def status(self) -> Optional[str]:
        """Get the gateway status."""
        return self.config.status if self.config else None
    
    @property
    def id_service(self) -> Optional[str]:
        """Get the service ID (deployment or inference pipeline ID)."""
        return self.config.id_service if self.config else None
    
    @id_service.setter
    def id_service(self, value: str):
        """Set the service ID (deployment or inference pipeline ID)."""
        if self.config:
            self.config.id_service = value
    
    def _load_from_id(self, gateway_id: str):
        """Load gateway configuration from backend by ID."""
        path = f"/v1/inference/streaming_gateway/{gateway_id}"
        resp = self.rpc.get(path=path)
        
        if resp and resp.get("success"):
            data = resp.get("data")
            if data:
                self.config = StreamingGatewayConfig.from_dict(data)
            else:
                raise ValueError(f"No data found for gateway ID: {gateway_id}")
        else:
            error_msg = resp.get("message") if resp else "No response received"
            raise ValueError(f"Failed to load gateway: {error_msg}")
    
    def save(self, service_id: str = None) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Save the gateway configuration to the backend (create new).
        
        Args:
            service_id: The deployment or inference pipeline ID to associate with
        
        Returns:
            tuple: (result, error, message)
        """
        if not self.config:
            return None, "No configuration to save", "Invalid state"
        
        if self.id:
            return None, "Gateway already exists, use update() instead", "Already exists"
        
        if service_id:
            self.config.id_service = service_id
        
        if not self.config.id_service:
            return None, "Service ID is required", "Missing service ID"
        
        path = "/v1/inference/streaming_gateway"
        payload = self.config.to_dict()
        # Ensure the service ID is included in the payload for the backend
        payload["idService"] = self.config.id_service
        
        resp = self.rpc.post(path=path, payload=payload)
        
        if resp and resp.get("success"):
            result = resp.get("data")
            if result and "id" in result:
                self.config.id = result["id"]
            return result, None, "Streaming gateway created successfully"
        else:
            error = resp.get("message") if resp else "No response received"
            return None, error, "Failed to create streaming gateway"
    
    def update(self) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update the gateway configuration in the backend.
        
        Returns:
            tuple: (result, error, message)
        """
        if not self.config or not self.config.id:
            return None, "Gateway must be saved before updating", "Invalid state"
        
        path = f"/v1/inference/streaming_gateway/{self.config.id}"
        payload = {
            "name": self.config.name,
            "description": self.config.description,
            "cameraGroupIds": self.config.camera_group_ids
        }
        
        resp = self.rpc.put(path=path, payload=payload)
        
        if resp and resp.get("success"):
            result = resp.get("data")
            return result, None, "Streaming gateway updated successfully"
        else:
            error = resp.get("message") if resp else "No response received"
            return None, error, "Failed to update streaming gateway"
    
    def delete(self, force: bool = False) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Delete the gateway from the backend.
        
        Args:
            force: Force delete even if active
        
        Returns:
            tuple: (result, error, message)
        """
        if not self.config or not self.config.id:
            return None, "Gateway must be saved before deleting", "Invalid state"
        
        path = f"/v1/inference/streaming_gateway/{self.config.id}"
        params = {}
        if force:
            params["force"] = "true"
        
        resp = self.rpc.delete(path=path, params=params)
        
        if resp and resp.get("success"):
            result = resp.get("data")
            return result, None, "Streaming gateway deleted successfully"
        else:
            error = resp.get("message") if resp else "No response received"
            return None, error, "Failed to delete streaming gateway"
    
    def add_camera_groups(self, camera_group_ids: List[str]) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Add camera groups to this gateway.
        
        Args:
            camera_group_ids: List of camera group IDs to add
        
        Returns:
            tuple: (result, error, message)
        """
        if not self.config or not self.config.id:
            return None, "Gateway must be saved before adding camera groups", "Invalid state"
        
        if not camera_group_ids:
            return None, "Camera group IDs are required", "Invalid camera group IDs"
        
        path = f"/v1/inference/streaming_gateway/{self.config.id}/add_camera_groups"
        payload = {"cameraGroupIds": camera_group_ids}
        
        resp = self.rpc.post(path=path, payload=payload)
        
        if resp and resp.get("success"):
            # Update local configuration
            for group_id in camera_group_ids:
                if group_id not in self.config.camera_group_ids:
                    self.config.camera_group_ids.append(group_id)
            
            result = resp.get("data")
            return result, None, "Camera groups added successfully"
        else:
            error = resp.get("message") if resp else "No response received"
            return None, error, "Failed to add camera groups"
    
    def remove_camera_groups(self, camera_group_ids: List[str]) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Remove camera groups from this gateway.
        
        Args:
            camera_group_ids: List of camera group IDs to remove
        
        Returns:
            tuple: (result, error, message)
        """
        if not self.config or not self.config.id:
            return None, "Gateway must be saved before removing camera groups", "Invalid state"
        
        if not camera_group_ids:
            return None, "Camera group IDs are required", "Invalid camera group IDs"
        
        path = f"/v1/inference/streaming_gateway/{self.config.id}/remove_camera_groups"
        payload = {"cameraGroupIds": camera_group_ids}
        
        resp = self.rpc.post(path=path, payload=payload)
        
        if resp and resp.get("success"):
            # Update local configuration
            for group_id in camera_group_ids:
                if group_id in self.config.camera_group_ids:
                    self.config.camera_group_ids.remove(group_id)
            
            result = resp.get("data")
            return result, None, "Camera groups removed successfully"
        else:
            error = resp.get("message") if resp else "No response received"
            return None, error, "Failed to remove camera groups"
    
    def refresh(self):
        """Refresh the gateway configuration from the backend."""
        if self.config and self.config.id:
            self._load_from_id(self.config.id)


class StreamingGatewayManager:
    """
    Streaming gateway manager client for handling streaming gateway configurations in deployments.
    
    This class provides methods to create, read, update, and delete streaming gateway configurations
    that manage collections of camera groups for efficient video processing and distribution.
    
    Example:
        Basic usage:
        ```python
        from matrice import Session
        from matrice.deployment.streaming_gateway_manager import StreamingGatewayManager, StreamingGatewayConfig
        
        session = Session(account_number="...", access_key="...", secret_key="...")
        gateway_manager = StreamingGatewayManager(session, service_id="deployment_id")
        
        # Create a streaming gateway config
        config = StreamingGatewayConfig(
            name="Main Streaming Gateway",
            description="Primary gateway for building A camera groups",
            camera_group_ids=["group1_id", "group2_id"]
        )
        
        # Create gateway through manager
        gateway, error, message = gateway_manager.create_streaming_gateway(config)
        if error:
            print(f"Error: {error}")
        else:
            print(f"Streaming gateway created: {gateway.name}")
            
        # Get all gateways for a deployment
        gateways, error, message = gateway_manager.get_streaming_gateways()
        if not error:
            for gateway in gateways:
                print(f"Gateway: {gateway.name} - {len(gateway.camera_group_ids)} camera groups")
        ```
    """
    
    def __init__(self, session, service_id: str = None):
        """
        Initialize the StreamingGatewayManager client.
        
        Args:
            session: Session object containing RPC client for API communication
            service_id: The ID of the deployment or the ID of the inference pipeline
        """
        self.session = session
        self.rpc = session.rpc
        self.service_id = service_id

    def handle_response(self, response: Dict, success_message: str, failure_message: str) -> Tuple[Optional[Dict], Optional[str], str]:
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

    def create_streaming_gateway(self, config: StreamingGatewayConfig) -> Tuple[Optional['StreamingGateway'], Optional[str], str]:
        """
        Create a new streaming gateway from configuration.
        
        Args:
            config: StreamingGatewayConfig object containing the gateway configuration
            
        Returns:
            tuple: (streaming_gateway, error, message)
                - streaming_gateway: StreamingGateway instance if successful, None otherwise
                - error: Error message if failed, None otherwise  
                - message: Status message
        """
        if not isinstance(config, StreamingGatewayConfig):
            return None, "Config must be a StreamingGatewayConfig instance", "Invalid config type"
        
        # Validate gateway config
        is_valid, validation_error = self._validate_streaming_gateway_config(config)
        if not is_valid:
            return None, validation_error, "Validation failed"
        
        # Create gateway instance
        gateway = StreamingGateway(self.session, config)
        
        # Save to backend
        result, error, message = gateway.save(service_id=self.service_id)
        
        if error:
            return None, error, message
        
        return gateway, None, message
    
    def get_streaming_gateway_by_id(self, gateway_id: str) -> Tuple[StreamingGateway, Optional[str], str]:
        """
        Get a streaming gateway by its ID.
        
        Args:
            gateway_id: The ID of the streaming gateway to retrieve
            
        Returns:
            tuple: (streaming_gateway, error, message)
        """
        if not gateway_id:
            return None, "Gateway ID is required", "Invalid gateway ID"
        
        try:
            gateway = StreamingGateway(self.session, gateway_id=gateway_id)
            return gateway, None, "Streaming gateway retrieved successfully"
        except Exception as e:
            return None, str(e), "Failed to retrieve streaming gateway"
    
    def get_streaming_gateways(self, page: int = 1, limit: int = 10, search: str = None) -> Tuple[Optional[List['StreamingGateway']], Optional[str], str]:
        """
        Get all streaming gateways for a specific deployment.
        
        Args:
            page: Page number for pagination
            limit: Items per page
            search: Optional search term
            
        Returns:
            tuple: (streaming_gateways, error, message)
        """
        if not self.service_id:
            return None, "Service ID is required", "Invalid service ID"
        
        path = f"/v1/inference/streaming_gateways/{self.service_id}"
        params = {"page": page, "limit": limit}
        if search:
            params["search"] = search
            
        resp = self.rpc.get(path=path, params=params)
        
        result, error, message = self.handle_response(
            resp,
            "Streaming gateways retrieved successfully",
            "Failed to retrieve streaming gateways"
        )
        
        if error:
            return None, error, message
        
        # Backend returns paginated response structure
        if result:
            try:
                # The result contains data in nested structure: data.items
                if "data" in result:
                    result = result["data"]
                if "items" in result:
                    gateway_data_list = result["items"]
                elif isinstance(result, list):
                    gateway_data_list = result
                else:
                    gateway_data_list = []
                if not gateway_data_list:
                    logging.debug(
                        "get_streaming_gateways: service_id=%s page=%s limit=%s -> 0 gateways",
                        self.service_id,
                        page,
                        limit,
                    )
                    return [], None, "No streaming gateways found"
                
                # Convert to StreamingGateway instances
                streaming_gateways = []
                for gateway_data in gateway_data_list:
                    try:
                        config = StreamingGatewayConfig.from_dict(gateway_data)
                        gateway = StreamingGateway(self.session, config)
                        streaming_gateways.append(gateway)
                    except Exception as e:
                        logging.warning(f"Failed to parse gateway data: {e}")
                        continue
                
                logging.debug(
                    "get_streaming_gateways: service_id=%s -> gateways=%s",
                    self.service_id,
                    len(streaming_gateways),
                )
                return streaming_gateways, None, message
            except Exception as e:
                return None, f"Failed to parse streaming gateways: {str(e)}", "Parse error"
        
        return [], None, message

    def _validate_streaming_gateway_config(self, config: StreamingGatewayConfig) -> Tuple[bool, str]:
        """
        Validate streaming gateway config data before API calls.
        
        Args:
            config: StreamingGatewayConfig object to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not config.name or not config.name.strip():
            return False, "Streaming gateway name is required"
        
        return True, "" 