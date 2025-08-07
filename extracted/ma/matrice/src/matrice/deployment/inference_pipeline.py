"""Module providing inference pipeline functionality for managing ML model deployment orchestration."""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import time

# Import camera and streaming gateway managers and instances
from .camera_manager import (
    CameraManager,
    Camera,
    CameraGroup,
    CameraGroupConfig,
    CameraConfig,
)
from .streaming_gateway_manager import (
    StreamingGatewayManager,
    StreamingGateway,
    StreamingGatewayConfig,
)
from matrice.utils import handle_response


@dataclass
class ApplicationDeployment:
    """
    Application deployment configuration for inference pipelines.

    Attributes:
        application_id: ID of the application
        application_version: Version of the application
        deployment_id: ID of the deployment (optional)
        status: Status of the application deployment
    """

    application_id: str
    application_version: str
    deployment_id: Optional[str] = None
    status: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert the application deployment to a dictionary for API calls."""
        data = {
            "_idApplication": self.application_id,
            "applicationVersion": self.application_version,
        }
        if self.deployment_id:
            data["_idDeployment"] = self.deployment_id
        if self.status:
            data["status"] = self.status
        return data

    @classmethod
    def from_dict(cls, data: Dict) -> "ApplicationDeployment":
        """Create an ApplicationDeployment instance from API response data."""
        # Handle MongoDB ObjectID conversion to string
        app_id = data.get("_idApplication", "")
        if hasattr(app_id, "__str__"):
            app_id = str(app_id)

        deployment_id = data.get("_idDeployment")
        if deployment_id and hasattr(deployment_id, "__str__"):
            deployment_id = str(deployment_id)

        return cls(
            application_id=app_id,
            application_version=data.get("applicationVersion", ""),
            deployment_id=deployment_id,
            status=data.get("status"),
        )


@dataclass
class Aggregator:
    """
    Aggregator configuration for inference pipelines.

    Attributes:
        id: Unique identifier for the aggregator (MongoDB ObjectID)
        action_id: ID of the associated action (MongoDB ObjectID)
        status: Status of the aggregator
        is_running: Whether the aggregator is currently running
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    action_id: str
    id: Optional[str] = None
    status: Optional[str] = None
    is_running: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert the aggregator to a dictionary for API calls."""
        data = {"_idAction": self.action_id}
        if self.id:
            data["_id"] = self.id
        if self.status:
            data["status"] = self.status
        if self.is_running is not None:
            data["isRunning"] = self.is_running
        if self.created_at:
            data["createdAt"] = self.created_at
        if self.updated_at:
            data["updatedAt"] = self.updated_at
        return data

    @classmethod
    def from_dict(cls, data: Dict) -> "Aggregator":
        """Create an Aggregator instance from API response data."""
        # Handle MongoDB ObjectID conversion to string
        aggregator_id = data.get("_id")
        if aggregator_id and hasattr(aggregator_id, "__str__"):
            aggregator_id = str(aggregator_id)

        action_id = data.get("_idAction", "")
        if hasattr(action_id, "__str__"):
            action_id = str(action_id)

        return cls(
            id=aggregator_id,
            action_id=action_id,
            status=data.get("status"),
            is_running=data.get("isRunning"),
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt"),
        )


@dataclass
class InferencePipelineConfig:
    """
    Inference pipeline configuration data class.

    Attributes:
        name: Name of the inference pipeline
        description: Description of the inference pipeline
        applications: List of application deployments
        aggregators: List of aggregators (optional)
        id: Unique identifier for the pipeline (MongoDB ObjectID)
        project_id: Project ID this pipeline belongs to
        user_id: User ID who created the pipeline
        status: Status of the pipeline
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    name: str
    description: str
    applications: List[ApplicationDeployment]
    aggregators: Optional[List[Aggregator]] = None
    id: Optional[str] = None
    project_id: Optional[str] = None
    user_id: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        if self.applications is None:
            self.applications = []
        if self.aggregators is None:
            self.aggregators = []

    def to_dict(self) -> Dict:
        """Convert the inference pipeline config to a dictionary for API calls."""
        if not self.name or not self.name.strip():
            raise ValueError("Pipeline name is required")
        if not self.applications:
            raise ValueError("At least one application is required")

        data = {
            "name": self.name,
            "description": self.description or "",
            "applications": [app.to_dict() for app in self.applications],
        }

        # Add aggregators if provided
        if self.aggregators:
            data["aggregators"] = [agg.to_dict() for agg in self.aggregators]

        if self.id:
            data["_id"] = self.id
        if self.project_id:
            data["_idProject"] = self.project_id
        if self.status:
            data["status"] = self.status
        if self.created_at:
            data["createdAt"] = self.created_at
        if self.updated_at:
            data["updatedAt"] = self.updated_at
        # Note: UserID is automatically set by the backend from JWT token
        return data

    @classmethod
    def from_dict(cls, data: Dict) -> "InferencePipelineConfig":
        """Create an InferencePipelineConfig instance from API response data."""
        applications = [
            ApplicationDeployment.from_dict(app_data)
            for app_data in data.get("applications", [])
        ]

        aggregators = [
            Aggregator.from_dict(agg_data) for agg_data in data.get("aggregators", [])
        ]

        # Handle MongoDB ObjectID conversion to string
        pipeline_id = data.get("_id") or data.get("id")
        if pipeline_id and hasattr(pipeline_id, "__str__"):
            pipeline_id = str(pipeline_id)

        project_id = data.get("_idProject")
        if project_id and hasattr(project_id, "__str__"):
            project_id = str(project_id)

        user_id = data.get("_idUser")
        if user_id and hasattr(user_id, "__str__"):
            user_id = str(user_id)

        return cls(
            id=pipeline_id,
            project_id=project_id,
            user_id=user_id,
            name=data.get("name", ""),
            description=data.get("description", ""),
            applications=applications,
            aggregators=aggregators,
            status=data.get("status"),
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt"),
        )


class InferencePipeline:
    """
    Inference pipeline instance for managing a specific ML model deployment orchestration.

    This class provides methods to start, stop, monitor, and manage a single inference pipeline
    that orchestrates the deployment and execution of machine learning models for
    real-time data processing and inference.

    Example:
        Working with a specific inference pipeline:
        ```python
        from matrice import Session
        from matrice.deployment.inference_pipeline import InferencePipeline

        session = Session(account_number="...", access_key="...", secret_key="...")

        # Load existing pipeline
        pipeline = InferencePipeline(session, pipeline_id="664ab1df23abcf1c33123456")

        # Start the pipeline
        result, error, message = pipeline.start()
        if not error:
            print("Pipeline started successfully")

        # Check status
        status, error, message = pipeline.get_status()
        if not error:
            print(f"Pipeline status: {status}")

        # Stop the pipeline
        result, error, message = pipeline.stop()
        ```
    """

    def __init__(
        self, session, config: InferencePipelineConfig = None, pipeline_id: str = None
    ):
        """
        Initialize an InferencePipeline instance.

        Args:
            session: Session object containing RPC client for API communication
            config: InferencePipelineConfig object (for new pipelines)
            pipeline_id: The ID of an existing pipeline to load
        """
        self.session = session
        self.rpc = session.rpc
        self._config = config
        self._pipeline_id = pipeline_id

        # Load from ID if provided
        if pipeline_id and not config:
            self._load_from_id(pipeline_id)

        # Initialize camera and streaming gateway managers
        self.camera_manager = CameraManager(session, service_id=self.id)
        self.streaming_gateway_manager = StreamingGatewayManager(
            session, service_id=self.id
        )

    @property
    def id(self) -> Optional[str]:
        """Get the pipeline ID."""
        return self._config.id if self._config else self._pipeline_id

    @property
    def name(self) -> str:
        """Get the pipeline name."""
        return self._config.name if self._config else ""

    @name.setter
    def name(self, value: str):
        """Set the pipeline name."""
        if self._config:
            self._config.name = value

    @property
    def description(self) -> str:
        """Get the pipeline description."""
        return self._config.description if self._config else ""

    @description.setter
    def description(self, value: str):
        """Set the pipeline description."""
        if self._config:
            self._config.description = value

    @property
    def applications(self) -> List[ApplicationDeployment]:
        """Get the pipeline applications."""
        return self._config.applications if self._config else []

    @applications.setter
    def applications(self, value: List[ApplicationDeployment]):
        """Set the pipeline applications."""
        if self._config:
            self._config.applications = value

    @property
    def deployment_ids(self) -> List[str]:
        """Get the deployment IDs."""
        return [app.deployment_id for app in self.applications if app.deployment_id]

    @property
    def aggregators(self) -> List[Aggregator]:
        """Get the pipeline aggregators."""
        return self._config.aggregators if self._config else []

    @aggregators.setter
    def aggregators(self, value: List[Aggregator]):
        """Set the pipeline aggregators."""
        if self._config:
            self._config.aggregators = value

    @property
    def status(self) -> Optional[str]:
        """Get the pipeline status."""
        return self._config.status if self._config else None

    @property
    def config(self) -> Optional[InferencePipelineConfig]:
        """Get the pipeline configuration."""
        return self._config

    @config.setter
    def config(self, value: InferencePipelineConfig):
        """Set the pipeline configuration."""
        self._config = value
        # Update managers with new service ID
        self.camera_manager = CameraManager(self.session, service_id=self.id)
        self.streaming_gateway_manager = StreamingGatewayManager(
            self.session, service_id=self.id
        )

    def _load_from_id(self, pipeline_id: str):
        """Load pipeline configuration from API using pipeline ID."""
        try:
            path = f"/v1/inference/get_inference_pipeline/{pipeline_id}"
            resp = self.rpc.get(path=path)
            result, error, message = handle_response(
                resp,
                "Pipeline details retrieved successfully",
                "Failed to retrieve pipeline details",
            )

            if error:
                raise Exception(f"Failed to load pipeline: {error}")

            if result:
                self._config = InferencePipelineConfig.from_dict(result)
                self._pipeline_id = pipeline_id
                # Update managers with loaded service ID
                self.camera_manager = CameraManager(self.session, service_id=self.id)
                self.streaming_gateway_manager = StreamingGatewayManager(
                    self.session, service_id=self.id
                )
        except Exception as e:
            raise Exception(
                f"Failed to load inference pipeline {pipeline_id}: {str(e)}"
            )

    def save(self, project_id: str = None) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Save this inference pipeline to the backend.

        Args:
            project_id: The ID of the project (optional if set in config)

        Returns:
            tuple: (result, error, message)
        """
        if not self._config:
            return None, "No pipeline configuration to save", "Missing configuration"

        # Validate configuration
        is_valid, error_msg = self._validate_pipeline_config()
        if not is_valid:
            return None, error_msg, "Invalid configuration"

        # Use provided IDs or defaults from config
        target_project_id = (
            project_id
            or self._config.project_id
            or getattr(self.session, "project_id", None)
        )

        if not target_project_id:
            return None, "Project ID is required", "Missing project ID"

        # Set the project ID in config (user_id is set automatically by backend)
        self._config.project_id = target_project_id

        try:
            path = "/v1/inference/inference_pipeline"
            payload = self._config.to_dict()

            resp = self.rpc.post(
                path=path, headers={"Content-Type": "application/json"}, payload=payload
            )
            result, error, message = handle_response(
                resp,
                "Inference pipeline created successfully",
                "Failed to create inference pipeline",
            )

            if error:
                return None, error, message

            # Update config with returned data
            if result and result.get("_id"):
                self._config.id = result["_id"]
                self._pipeline_id = result["_id"]
                # Update managers with new service ID
                self.camera_manager = CameraManager(self.session, service_id=self.id)
                self.streaming_gateway_manager = StreamingGatewayManager(
                    self.session, service_id=self.id
                )

            return result, None, message

        except Exception as e:
            return None, str(e), "Failed to save inference pipeline"

    def start(self) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Start this inference pipeline for real-time processing.

        Returns:
            tuple: (result, error, message)
        """
        if not self.id:
            return None, "Pipeline ID is required", "Invalid pipeline ID"

        path = f"/v1/inference/start_inference_pipeline/{self.id}"
        resp = self.rpc.put(path=path)

        result, error, message = handle_response(
            resp,
            "Inference pipeline started successfully",
            "Failed to start inference pipeline",
        )

        # Update status in config if successful
        if not error and self._config:
            self._config.status = "starting"

        return result, error, message

    def stop(self, force: bool = False) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Stop this inference pipeline and clean up resources.

        Args:
            force: Force stop even if active streams exist

        Returns:
            tuple: (result, error, message)
        """
        if not self.id:
            return None, "Pipeline ID is required", "Invalid pipeline ID"

        path = f"/v1/inference/stop_inference_pipeline/{self.id}"
        params = {}
        if force:
            params["force"] = "true"

        resp = self.rpc.put(path=path, params=params)

        result, error, message = handle_response(
            resp,
            "Inference pipeline stopped successfully",
            "Failed to stop inference pipeline",
        )

        # Update status in config if successful
        if not error and self._config:
            self._config.status = "stopping"

        return result, error, message

    def get_status(self) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Retrieve the current status of this inference pipeline.

        Returns:
            tuple: (result, error, message)
        """
        if not self.id:
            return None, "Pipeline ID is required", "Invalid pipeline ID"

        path = f"/v1/inference/get_inference_pipeline/{self.id}"
        resp = self.rpc.get(path=path)

        result, error, message = handle_response(
            resp,
            "Pipeline status retrieved successfully",
            "Failed to retrieve pipeline status",
        )

        # Update config with latest data if successful
        if not error and result and self._config:
            self._config.status = result.get("status")

        return result, error, message

    def get_details(self) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Retrieve detailed information about this inference pipeline.

        Returns:
            tuple: (pipeline_details, error, message)
        """
        if not self.id:
            return None, "Pipeline ID is required", "Invalid pipeline ID"

        path = f"/v1/inference/get_inference_pipeline/{self.id}"
        resp = self.rpc.get(path=path)

        result, error, message = handle_response(
            resp,
            "Pipeline details retrieved successfully",
            "Failed to retrieve pipeline details",
        )

        if error:
            return None, error, message

        if result:
            try:
                # Update config with latest data
                if self._config:
                    updated_config = InferencePipelineConfig.from_dict(result)
                    self._config = updated_config
                return result, None, message
            except Exception as e:
                return (
                    None,
                    f"Failed to parse pipeline details: {str(e)}",
                    "Parse error",
                )

        return None, "No pipeline data received", message

    def update(self) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update this inference pipeline with the current configuration.

        Returns:
            tuple: (result, error, message)
        """
        if not self.id:
            return None, "Pipeline ID is required", "Invalid pipeline ID"

        if not self._config:
            return None, "No configuration to update", "Missing configuration"

        # Validate configuration
        is_valid, error_msg = self._validate_pipeline_config()
        if not is_valid:
            return None, error_msg, "Invalid configuration"

        # Note: Update functionality may not be implemented in the backend yet
        return (
            None,
            "Pipeline update functionality is not yet implemented in the backend",
            "Not implemented",
        )

    def delete(self, force: bool = False) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Delete this inference pipeline and clean up all associated resources.

        Args:
            force: Force delete even if active

        Returns:
            tuple: (result, error, message)
        """
        if not self.id:
            return None, "Pipeline ID is required", "Invalid pipeline ID"

        # Note: Delete functionality may not be implemented in the backend yet
        return (
            None,
            "Pipeline deletion functionality is not yet implemented in the backend",
            "Not implemented",
        )

    def wait_for_ready(
        self, timeout: int = 300, poll_interval: int = 10
    ) -> Tuple[bool, Optional[str], str]:
        """
        Wait for this pipeline to reach 'ready' status.

        Args:
            timeout: Maximum time to wait in seconds
            poll_interval: Time between status checks in seconds

        Returns:
            tuple: (is_ready, error, message)
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            result, error, message = self.get_status()

            if error:
                return False, error, message

            if result and result.get("status") == "ready":
                return True, None, "Pipeline is ready"
            elif result and result.get("status") == "error":
                return False, "Pipeline entered error state", "Pipeline failed"

            time.sleep(poll_interval)

        return False, "Timeout waiting for pipeline to be ready", "Timeout"

    def wait_for_active(
        self, timeout: int = 300, poll_interval: int = 10
    ) -> Tuple[bool, Optional[str], str]:
        """
        Wait for this pipeline to reach 'active' status.

        Args:
            timeout: Maximum time to wait in seconds
            poll_interval: Time between status checks in seconds

        Returns:
            tuple: (is_active, error, message)
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            result, error, message = self.get_status()

            if error:
                return False, error, message

            if result and result.get("status") == "active":
                return True, None, "Pipeline is active"
            elif result and result.get("status") == "error":
                return False, "Pipeline entered error state", "Pipeline failed"

            time.sleep(poll_interval)

        return False, "Timeout waiting for pipeline to be active", "Timeout"

    def refresh(self):
        """Refresh the pipeline configuration from the backend."""
        if self.id:
            try:
                self._load_from_id(self.id)
            except Exception as e:
                raise Exception(f"Failed to refresh pipeline: {str(e)}")

    def _validate_pipeline_config(self) -> Tuple[bool, str]:
        """
        Validate the pipeline configuration.

        Returns:
            tuple: (is_valid, error_message)
        """
        if not self._config:
            return False, "Pipeline configuration is missing"

        if not self._config.name or not self._config.name.strip():
            return False, "Pipeline name is required"

        if not self._config.applications:
            return False, "At least one application is required"

        # Validate each application
        for app in self._config.applications:
            if not app.application_id or not app.application_id.strip():
                return False, "Application ID is required for all applications"

        return True, "Valid configuration"

    # Camera Management Integration Methods
    def create_camera_group(
        self, group: CameraGroupConfig
    ) -> Tuple[Optional["CameraGroup"], Optional[str], str]:
        """
        Create a camera group for this inference pipeline.

        Args:
            group: CameraGroupConfig object containing the group configuration

        Returns:
            tuple: (camera_group_instance, error, message)
        """
        return self.camera_manager.create_camera_group(group)

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
        return self.camera_manager.get_camera_group_by_id(group_id)

    def get_camera_groups(
        self, page: int = 1, limit: int = 10, search: str = None
    ) -> Tuple[Optional[List["CameraGroup"]], Optional[str], str]:
        """
        Get camera groups for this inference pipeline.

        Args:
            page: Page number for pagination
            limit: Items per page
            search: Optional search term

        Returns:
            tuple: (camera_group_instances, error, message)
        """
        return self.camera_manager.get_camera_groups(page, limit, search)

    def create_camera(
        self, camera_config: CameraConfig
    ) -> Tuple[Optional["Camera"], Optional[str], str]:
        """
        Create a camera for this inference pipeline.

        Args:
            camera_config: CameraConfig object containing the camera configuration

        Returns:
            tuple: (camera_instance, error, message)
        """
        return self.camera_manager.create_camera(camera_config)

    def get_cameras(
        self, page: int = 1, limit: int = 10, search: str = None, group_id: str = None
    ) -> Tuple[Optional[List["Camera"]], Optional[str], str]:
        """
        Get cameras for this inference pipeline.

        Args:
            page: Page number for pagination
            limit: Items per page
            search: Optional search term
            group_id: Optional filter by camera group ID

        Returns:
            tuple: (camera_instances, error, message)
        """
        return self.camera_manager.get_cameras(page, limit, search, group_id)

    def add_cameras_to_group(
        self, group_id: str, camera_configs: List[CameraConfig]
    ) -> Tuple[Optional[List["Camera"]], Optional[str], str]:
        """
        Add multiple cameras to a camera group in this inference pipeline.

        Args:
            group_id: The ID of the camera group
            camera_configs: List of CameraConfig objects

        Returns:
            tuple: (camera_instances, error, message)
        """
        return self.camera_manager.add_cameras_to_group(group_id, camera_configs)

    # Streaming Gateway Management Integration Methods
    def create_streaming_gateway(
        self, gateway_config: StreamingGatewayConfig
    ) -> Tuple[Optional["StreamingGateway"], Optional[str], str]:
        """
        Create a streaming gateway for this inference pipeline.

        Args:
            gateway_config: StreamingGatewayConfig object containing the gateway configuration

        Returns:
            tuple: (streaming_gateway, error, message)
        """
        return self.streaming_gateway_manager.create_streaming_gateway(gateway_config)

    def get_streaming_gateway_by_id(
        self, gateway_id: str
    ) -> Tuple[Optional["StreamingGateway"], Optional[str], str]:
        """
        Get a streaming gateway by its ID.

        Args:
            gateway_id: The ID of the streaming gateway to retrieve

        Returns:
            tuple: (streaming_gateway, error, message)
        """
        return self.streaming_gateway_manager.get_streaming_gateway_by_id(gateway_id)

    def get_streaming_gateways(
        self, page: int = 1, limit: int = 10, search: str = None
    ) -> Tuple[Optional[List["StreamingGateway"]], Optional[str], str]:
        """
        Get streaming gateways for this inference pipeline.

        Args:
            page: Page number for pagination
            limit: Items per page
            search: Optional search term

        Returns:
            tuple: (streaming_gateways, error, message)
        """
        return self.streaming_gateway_manager.get_streaming_gateways(
            page, limit, search
        )

    def update_streaming_gateway(
        self, gateway_id: str, gateway_config: StreamingGatewayConfig
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Update an existing streaming gateway.

        Args:
            gateway_id: The ID of the streaming gateway to update
            gateway_config: StreamingGatewayConfig object with updated configuration

        Returns:
            tuple: (result, error, message)
        """
        try:
            gateway = StreamingGateway(self.session, gateway_id=gateway_id)
            # Update the configuration
            gateway.config = gateway_config
            return gateway.update()
        except Exception as e:
            return None, str(e), "Failed to update streaming gateway"

    def delete_streaming_gateway(
        self, gateway_id: str, force: bool = False
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Delete a streaming gateway by its ID.

        Args:
            gateway_id: The ID of the streaming gateway to delete
            force: Force delete even if active

        Returns:
            tuple: (result, error, message)
        """
        try:
            gateway = StreamingGateway(self.session, gateway_id=gateway_id)
            return gateway.delete(force=force)
        except Exception as e:
            return None, str(e), "Failed to delete streaming gateway"

    def add_camera_groups_to_streaming_gateway(
        self, gateway_id: str, camera_group_ids: List[str]
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Add camera groups to a streaming gateway.

        Args:
            gateway_id: The ID of the streaming gateway
            camera_group_ids: List of camera group IDs to add

        Returns:
            tuple: (result, error, message)
        """
        try:
            gateway = StreamingGateway(self.session, gateway_id=gateway_id)
            return gateway.add_camera_groups(camera_group_ids)
        except Exception as e:
            return None, str(e), "Failed to add camera groups to streaming gateway"

    def remove_camera_groups_from_streaming_gateway(
        self, gateway_id: str, camera_group_ids: List[str]
    ) -> Tuple[Optional[Dict], Optional[str], str]:
        """
        Remove camera groups from a streaming gateway.

        Args:
            gateway_id: The ID of the streaming gateway
            camera_group_ids: List of camera group IDs to remove

        Returns:
            tuple: (result, error, message)
        """
        try:
            gateway = StreamingGateway(self.session, gateway_id=gateway_id)
            return gateway.remove_camera_groups(camera_group_ids)
        except Exception as e:
            return None, str(e), "Failed to remove camera groups from streaming gateway"


class InferencePipelineManager:
    """
    Manager for inference pipeline operations.

    This class provides methods to create, list, and manage multiple inference pipelines
    within a project. It handles the overall management of inference pipelines while
    individual pipelines are managed through the InferencePipeline class.

    Example:
        Managing multiple inference pipelines:
        ```python
        from matrice import Session
        from matrice.deployment.inference_pipeline import InferencePipelineManager, InferencePipelineConfig, ApplicationDeployment

        session = Session(account_number="...", access_key="...", secret_key="...")
        manager = InferencePipelineManager(session)

        # Create a new pipeline
        apps = [
            ApplicationDeployment(
                application_id="664ab1df23abcf1c33123456",
                application_version="v1.0"
            )
        ]

        config = InferencePipelineConfig(
            name="Multi-App Pipeline",
            description="Pipeline for multiple applications",
            applications=apps
        )

        pipeline, error, message = manager.create_inference_pipeline(config)
        if not error:
            print(f"Created pipeline: {pipeline.id}")

        # List all pipelines
        pipelines, error, message = manager.get_inference_pipelines()
        if not error:
            print(f"Found {len(pipelines)} pipelines")
        ```
    """

    def __init__(self, session, project_id: str = None):
        """
        Initialize the InferencePipelineManager.

        Args:
            session: Session object containing RPC client for API communication
            project_id: The ID of the project (optional, can be inferred from session)
        """
        self.session = session
        self.rpc = session.rpc
        self.project_id = project_id or getattr(session, "project_id", None)

    def create_inference_pipeline(
        self, config: InferencePipelineConfig, project_id: str = None
    ) -> Tuple[Optional["InferencePipeline"], Optional[str], str]:
        """
        Create a new inference pipeline.

        Args:
            config: InferencePipelineConfig object containing the pipeline configuration
            project_id: The ID of the project (optional, uses manager's project_id if not provided)

        Returns:
            tuple: (inference_pipeline_instance, error, message)
        """
        # Validate configuration
        is_valid, error_msg = self._validate_pipeline_config(config)
        if not is_valid:
            return None, error_msg, "Invalid configuration"

        # Create pipeline instance
        pipeline = InferencePipeline(self.session, config=config)

        # Save the pipeline
        target_project_id = project_id or self.project_id
        result, error, message = pipeline.save(project_id=target_project_id)

        if error:
            return None, error, message

        return pipeline, None, message

    def get_inference_pipeline_by_id(
        self, pipeline_id: str
    ) -> Tuple[Optional["InferencePipeline"], Optional[str], str]:
        """
        Get an inference pipeline by its ID.

        Args:
            pipeline_id: The ID of the inference pipeline to retrieve

        Returns:
            tuple: (inference_pipeline_instance, error, message)
        """
        if not pipeline_id:
            return None, "Pipeline ID is required", "Invalid pipeline ID"

        try:
            pipeline = InferencePipeline(self.session, pipeline_id=pipeline_id)
            return pipeline, None, "Pipeline loaded successfully"
        except Exception as e:
            return None, str(e), "Failed to load pipeline"

    def get_inference_pipelines(
        self, page: int = 1, limit: int = 10, search: str = None, project_id: str = None
    ) -> Tuple[Optional[List["InferencePipeline"]], Optional[str], str]:
        """
        Get all inference pipelines for a project.

        Args:
            page: Page number for pagination
            limit: Items per page
            search: Optional search term
            project_id: The ID of the project (optional, uses manager's project_id if not provided)

        Returns:
            tuple: (inference_pipeline_instances, error, message)
        """
        target_project_id = project_id or self.project_id
        if not target_project_id:
            return None, "Project ID is required", "Missing project ID"

        try:
            # Build path with pagination parameters
            path = f"/v1/inference/list_inference_pipelines/{target_project_id}"
            params = {"page": page, "limit": limit}
            if search:
                params["search"] = search

            resp = self.rpc.get(path=path, params=params)
            result, error, message = handle_response(
                resp,
                "Inference pipelines retrieved successfully",
                "Failed to retrieve inference pipelines",
            )

            if error:
                return None, error, message

            if not result:
                return [], None, "No pipelines found"

            # Extract pipeline data from paginated response
            pipelines_data = result.get("items", [])
            pipelines = []

            for pipeline_data in pipelines_data:
                try:
                    config = InferencePipelineConfig.from_dict(pipeline_data)
                    pipeline = InferencePipeline(self.session, config=config)
                    pipelines.append(pipeline)
                except Exception as e:
                    print(f"Warning: Failed to parse pipeline data: {e}")
                    continue

            return pipelines, None, message

        except Exception as e:
            return None, str(e), "Failed to retrieve inference pipelines"

    def _validate_pipeline_config(
        self, config: InferencePipelineConfig
    ) -> Tuple[bool, str]:
        """
        Validate an inference pipeline configuration.

        Args:
            config: InferencePipelineConfig object to validate

        Returns:
            tuple: (is_valid, error_message)
        """
        if not config:
            return False, "Pipeline configuration is missing"

        if not config.name or not config.name.strip():
            return False, "Pipeline name is required"

        if not config.applications:
            return False, "At least one application is required"

        # Validate each application
        for app in config.applications:
            if not app.application_id or not app.application_id.strip():
                return False, "Application ID is required for all applications"

        return True, "Valid configuration"
