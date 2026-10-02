# Copyright 2024 Agnostiq Inc.

import json
import warnings
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type, Union
from uuid import UUID

from covalent import TransportableObject
from pydantic import BaseModel, ConfigDict, Field, field_validator
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from covalent_cloud.cloud_executor.cloud_executor import CloudExecutor
from covalent_cloud.cloud_executor.oci_cloud_executor import OCICloudExecutor
from covalent_cloud.function_serve.client import FunctionServeClient
from covalent_cloud.function_serve.common import ServeAssetType, ServiceStatus, SupportedMethods
from covalent_cloud.service_account_interface.client import get_deployment_client
from covalent_cloud.shared.schemas.volume import Volume

__all__ = [
    "Endpoint",
    "FunctionServiceModel",
    "Deployment",
    "FunctionEndpoint",
    "FunctionDeployment",
    "FunctionDeploymentMetadata",
    "FunctionDeploymentList",
    "InferenceAPIKey",
    "InferenceKeyMetadata",
]

COVALENT_CUSTOM_ENCODERS = {
    UUID: str,
    datetime: lambda dt: dt.isoformat(),
    timedelta: lambda td: td.total_seconds(),
}


# Type alias to represent a serialized object type
SerializedObjectType = bytes


class CustomBaseModel(BaseModel):
    """
    Custom Pydantic base model that converts certain data types to strings for json serialization.

    This is useful for when we want to serialize a Pydantic model to json, but the model contains data types that are not json serializable.

    Example:
        class MyModel(CustomBaseModel):
            id: uuid.UUID
            now: datetime.datetime

        model = MyModel(id=uuid.uuid4(), now=datetime.utcnow())
        json_str = model.json()  # was json serializable where before is raised a TypeError
        dict = model.model_dump() # dict is json serializable
    """

    @classmethod
    def encode_value(cls, value: Any, encoders: Dict[Type[Any], Callable[[Any], Any]]) -> Any:
        if isinstance(value, BaseModel):
            return value.model_dump(using_encoder=True, encoders=encoders)
        elif isinstance(value, list):
            return [cls.encode_value(item, encoders) for item in value]
        elif isinstance(value, dict):
            return {k: cls.encode_value(v, encoders) for k, v in value.items()}
        else:
            for encoder_type, encoder_func in encoders.items():
                if isinstance(value, encoder_type):
                    return encoder_func(value)
            return value

    def model_dump(
        self,
        *,
        using_encoder: bool = False,
        encoders: Dict[Type[Any], Callable[[Any], Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        if not using_encoder:
            encoders = COVALENT_CUSTOM_ENCODERS
        encoded_dict = super().model_dump(**kwargs)
        return {key: self.encode_value(value, encoders) for key, value in encoded_dict.items()}

    def json(self, **kwargs) -> str:
        return json.dumps(self.model_dump(**kwargs))

    def dict(self, **kwargs) -> Dict[str, Any]:
        return self.model_dump(**kwargs)

    class Config:
        json_encoders = COVALENT_CUSTOM_ENCODERS


class ServeAsset(BaseModel):
    type: Union[str, ServeAssetType] = ServeAssetType.ASSET
    id: Optional[str] = None
    url: Optional[str] = None
    serialized_object: SerializedObjectType

    def upload(self):
        from covalent_cloud.function_serve.assets import AssetsMediator

        return AssetsMediator.upload_asset(self)

    @field_validator("type")
    @classmethod
    def type_as_str(cls, type_: Union[str, ServeAssetType]):
        if isinstance(type_, Enum):
            return type_.value
        return type_


class Endpoint(BaseModel):  # TODO after v0: include executor and resources
    """
    Information about an individual endpoint for a function service.
    """

    method: str = SupportedMethods.POST
    """HTTP method for the endpoint; 'GET', 'POST', 'PUT', etc."""

    route: str
    """Route for the endpoint; e.g. '/predict'."""

    name: str
    """Name of the endpoint"""

    endpoint_fn: ServeAsset
    """Serialized function that implements the endpoint."""

    endpoint_fn_source: str
    """Source code of the function that implements the endpoint."""

    streaming: bool
    """"Indicates if the endpoint can stream its response."""

    description: str
    """Description of the endpoint."""

    test_endpoint_enabled: bool
    """Flag that indicates one-click testing is possible for the endpoint."""

    def __call__(self, *args, **kwargs):
        return TransportableObject.deserialize(
            self.endpoint_fn.serialized_object
        ).get_deserialized()(*args, **kwargs)


class FunctionServiceModel(CustomBaseModel):
    """
    Encapsulates all information relevant to a function service.
    """

    model_config = ConfigDict(extra="forbid")
    """Pydantic configuration for the model."""

    title: Optional[str] = ""
    """Title of the function service."""

    auth: Optional[bool] = None
    """Flag that indicates if the function service endpoints require authorization."""

    description: Optional[str] = ""
    """User specified description of the function service."""

    executor: Union[CloudExecutor, OCICloudExecutor]
    """Executor that defines the total resources (NOTE: revise after v0!)"""

    compute_share: Optional[float] = 1.0
    """Share of the total compute resources to be allocated to the function service. (NOTE: revise after v0!)"""

    tags: Optional[Union[str, List[str]]] = ""
    """List of optional tags for the function service."""

    init_fn: ServeAsset
    """Serialized service initializer function."""

    init_fn_args: ServeAsset
    """Serialized arguments to the service initializer function."""

    init_fn_args_json: ServeAsset
    """JSON array containing the initializer function arguments."""

    init_fn_kwargs: ServeAsset
    """Serialized keyword arguments to the service initializer function."""

    init_fn_kwargs_json: ServeAsset
    """JSON object containing the initializer function keyword arguments."""

    init_fn_source: str
    """Source code of the service initializer function."""

    endpoints: List[Endpoint]
    """List of endpoints for the function service."""

    volume: Optional[Volume] = None
    """Volume to be mounted to the function service."""

    root_dispatch_id: Optional[str] = None
    """Root dispatch ID of the function service, only valid for workflow-based deployments."""

    @field_validator("compute_share")
    @classmethod
    def compute_share(cls, compute_share: float):
        """Validate the compute shares for the function service."""
        if compute_share <= 0 or compute_share > 1:
            raise ValueError("compute_shares must be a float of value > 0 and <= 1.0.")
        return compute_share


class RouteInfo(BaseModel):
    """
    Contains information about a specific service route.
    This model is a partial `Endpoint` model.
    """

    route: str
    """Route for the endpoint; e.g. '/predict'."""

    method: SupportedMethods
    """HTTP method for the endpoint; 'GET', 'POST', 'PUT', etc."""

    streaming: bool
    """"Indicates if the endpoint can stream its response."""

    description: Optional[str] = ""
    """Description of the endpoint."""


class FunctionEndpoint(BaseModel):
    """Function endpoint information for listing deployments."""

    name: str
    """Name of the endpoint."""

    method: SupportedMethods
    """HTTP method for the endpoint; 'GET', 'POST', 'PUT', etc."""

    route: str
    """Route for the endpoint; e.g. '/predict'."""

    description: Optional[str] = None
    """Description of the endpoint."""

    def __str__(self) -> str:
        return f"{self.method.value} {self.route} ({self.name})"


class FunctionDeployment(BaseModel):
    """Function deployment information for listing."""

    id: str
    """Unique identifier for the deployment."""

    title: str
    """Title of the function deployment."""

    description: str
    """Description of the deployment."""

    status: str
    """Current status of the deployment."""

    created_at: datetime
    """When the deployment was created."""

    updated_at: datetime
    """When the deployment was last updated."""

    endpoints: List[FunctionEndpoint]
    """List of endpoints in the deployment."""

    tags: List[str]
    """Tags associated with the deployment."""

    auth: bool
    """Whether authentication is enabled for the deployment."""

    def __str__(self) -> str:
        # Format timestamps
        created_str = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        updated_str = self.updated_at.strftime("%Y-%m-%d %H:%M:%S")

        # Format tags
        tags_str = ", ".join(self.tags) if self.tags else "None"

        # Format endpoints
        endpoints_section = ""
        if self.endpoints:
            endpoints_section = "\nEndpoints:\n"
            for ep in self.endpoints:
                endpoints_section += f"  - {ep.method.value} {ep.route} ({ep.name})"
                if ep.description:
                    endpoints_section += f": {ep.description}"
                endpoints_section += "\n"

        return f"""Function Deployment
==================
ID: {self.id}
Title: {self.title}
Description: {self.description}
Status: {self.status}
Auth Enabled: {'Yes' if self.auth else 'No'}
Tags: {tags_str}
Created: {created_str}
Updated: {updated_str}{endpoints_section}"""


class FunctionDeploymentMetadata(BaseModel):
    """Metadata for paginated function deployment list."""

    total_count: int
    """Total number of deployments."""

    page: int
    """Current page number (0-indexed)."""

    count: int
    """Number of items in current page."""

    def __str__(self) -> str:
        return f"FunctionDeploymentMetadata(page={self.page}, count={self.count}, total={self.total_count})"


class FunctionDeploymentList(BaseModel):
    """Paginated list of function deployments."""

    records: List[FunctionDeployment]
    """List of function deployments."""

    metadata: FunctionDeploymentMetadata
    """Pagination metadata."""

    def __str__(self) -> str:
        return f"FunctionDeploymentList({len(self.records)} deployments, {self.metadata})"


class InferenceAPIKey(BaseModel):
    """Inference API key with full key value (shown only once)."""

    key_id: str
    """Unique identifier for the API key."""

    key: str
    """The actual API key - shown only once after creation."""

    created_at: Optional[datetime] = None
    """When the API key was created."""

    def __str__(self) -> str:
        # Don't show the actual key in string representation for security
        key_preview = f"{self.key[:8]}..." if len(self.key) > 8 else self.key
        return f"InferenceAPIKey(key_id={self.key_id}, key={key_preview})"


class InferenceKeyMetadata(BaseModel):
    """Inference API key metadata without the actual key value."""

    key_id: str
    """Unique identifier for the API key."""

    created_at: Optional[datetime] = None
    """When the API key was created."""

    last_used: Optional[datetime] = None
    """When the API key was last used."""

    def __str__(self) -> str:
        last_used_str = (
            f", last_used={self.last_used.strftime('%Y-%m-%d')}" if self.last_used else ""
        )
        return f"InferenceKeyMetadata(key_id={self.key_id}{last_used_str})"


class Deployment(BaseModel):
    """
    Returned by `cc.deploy` function and when `@service` decorated function is
    called within a workflow.
    """

    function_id: str
    """Unique identifier for the deployment."""

    address: Optional[str] = None
    """Address of the deployment usable by the user."""

    name: str
    """Name of the deployment."""

    description: str
    """Description of the deployment."""

    routes: List[RouteInfo]
    """All the registered routes for the deployment."""

    status: ServiceStatus
    """Status of the deployment."""

    tags: List[str] = Field(default_factory=list)
    """List of optional tags associated with the deployment."""

    token: Optional[str] = None
    """Authorization token for requests to the endpoints."""

    auth: Optional[bool] = None
    """Flag that indicates if the deployment endpoints require authorization."""

    error: Optional[str] = None
    """Error message associated with creating the deployment."""

    stderr: Optional[str] = None
    """Error message associated with initializing the deployment."""

    # Making this a static method since we don't need to access the class.
    @staticmethod
    def from_function_record(data: Dict[str, Any]) -> "Deployment":
        """
        Create a Deployment object from a function's database record.
        """

        return Deployment(
            function_id=data["id"],
            description=data.get("description"),
            address=str(data["invoke_url"]),
            name=str(data["title"]),
            routes=[RouteInfo(**ep) for ep in data["endpoints"]],
            status=data["status"],
            tags=data["tags"] or [],
            token=(
                data.get("inference_keys", [])[0].get("key")
                if data.get("inference_keys")
                else None
            ),
            auth=data["auth"],
            error=data.get("error"),
            stderr=data.get("stderr"),
        )

    # Not making this a model validator since in that case
    # it will try to attach the method to this model
    # and then Pydantic will raise an error since it cannot
    # serialize a 'method' type object.
    def attach_route_methods(self, overwrite: bool = False) -> "Deployment":
        """
        Attach methods to the Deployment object for each route.
        """

        fs_client = FunctionServeClient(
            function_id=self.function_id,
            host=self.address,
            token_getter=lambda: self.token,
        )

        # Built-in methods.
        setattr(self, "info", fs_client.info)
        setattr(self, "teardown", fs_client.teardown)

        # User-defined methods.
        for route_info in self.routes:

            # Check for name collisions.
            _name = route_info.route.lstrip("/").replace("-", "_")
            if hasattr(self, _name) and not overwrite:
                warnings.warn(
                    f"Object already has an attribute '{_name}'. Skipping method attachment. "
                    f"Please make requests to '{self.address}{route_info.route}' manually.",
                    category=UserWarning,
                )
                continue

            # Sync version.
            _new_sync_method = fs_client.make_request_method(
                route=route_info.route,
                method=route_info.method,
                streaming=route_info.streaming,
                is_async=False,
            )
            _new_sync_method.__name__ = _name
            _new_sync_method.__doc__ = route_info.description
            setattr(self, _name, _new_sync_method)

            # Async version. Append prefix to name and description.
            _async_name = f"async_{_name}"
            _new_async_method = fs_client.make_request_method(
                route=route_info.route,
                method=route_info.method,
                streaming=route_info.streaming,
                is_async=True,
            )
            _new_async_method.__name__ = _async_name
            _new_async_method.__doc__ = "(async) " + route_info.description
            setattr(self, _async_name, _new_async_method)

        return self

    def reload(self) -> None:
        """
        Reload the deployment info with updated information
        such as most recent status or address of the deployment.
        """

        if not self.function_id:
            raise ValueError("Function ID is not set.")

        deployment_client = get_deployment_client()

        # Reload the deployment info.
        response = deployment_client.get(f"/functions/{self.function_id}")

        new_deployment = Deployment.from_function_record(response.json())
        self.__dict__.update(new_deployment.__dict__)

        # Attach route methods for ease of use
        self.attach_route_methods(overwrite=True)

    def _stringify_routes(self) -> Table:
        """Get rich Table representation of route info."""

        routes_table = Table(box=None, show_header=False, padding=(0, 1))
        for i, route in enumerate(self.routes):
            routes_table.add_row("Route", f"{route.method.value} {route.route}")
            routes_table.add_row("Streaming", "Yes" if route.streaming else "No")
            routes_table.add_row("Description", route.description)
            if i < len(self.routes) - 1:
                routes_table.add_row("", "")  # empty row for spacing

        return routes_table

    def __str__(self) -> str:
        console = Console()
        info_table = Table(box=None, show_header=False)
        info_table.add_row("Name", self.name)
        info_table.add_row("Description", self.description)
        info_table.add_row("Function ID", self.function_id)
        info_table.add_row("Address", self.address)
        info_table.add_row("Status", self.status.value)

        if len(self.tags) > 0:
            info_table.add_row("Tags", ", ".join(self.tags))

        info_table.add_row("Auth Enabled", "Yes" if self.auth else "No")

        _panel_width = 90

        # Create a Panel for the main info
        info_panel = Panel(info_table, title="Deployment Information", width=_panel_width)

        # Create panel for error messages
        # Give `stderr` priority over `error`
        error_string = (self.stderr or self.error or "").strip()
        error_panel = Panel(error_string, title="Exception", width=_panel_width)

        # Prepare route info as Tables inside Panels
        routes_panel = Panel(self._stringify_routes(), title="Endpoints", width=_panel_width)

        # Convert everything to string using Rich Console's capture feature
        with console.capture() as capture:

            console.print(info_panel)

            if error_string:
                console.print(error_panel, style="red")

            console.print(routes_panel)

            if self.token:
                console.print(f"Authorization token:\n{self.token}")

        return capture.get()

    class Config:
        """Model configuration."""

        # Need to allow extra for dynamic method assignment.
        extra = "allow"
