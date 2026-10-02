"""Models for vendor AgentCore runtime settings."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from .vendor_assistant import PaginationInfo, TokenPagination


class VendorRuntimeStatus(str, Enum):
    """Status of a vendor AgentCore runtime. AWS READY maps to PREPARED."""

    PREPARED = "PREPARED"
    NOT_PREPARED = "NOT_PREPARED"


class VendorRuntimeSetting(BaseModel):
    """Model representing a vendor runtime setting."""

    model_config = ConfigDict(extra="ignore")

    setting_id: str = Field(..., description="Unique identifier for the setting")
    setting_name: str = Field(..., description="Name of the setting")
    project: str = Field(..., description="Project associated with the setting")
    entities: list[str] = Field(
        default_factory=list, description="List of entities associated with the setting"
    )
    invalid: bool | None = Field(None, description="Whether the setting is invalid")
    error: str | None = Field(
        None, description="Error message if the setting is invalid"
    )


class VendorRuntimeSettingsResponse(BaseModel):
    """Response model for vendor runtime settings list."""

    model_config = ConfigDict(extra="ignore")

    data: list[VendorRuntimeSetting] = Field(
        ..., description="List of vendor runtime settings"
    )
    pagination: PaginationInfo = Field(..., description="Pagination information")


class VendorRuntime(BaseModel):
    """Model representing a vendor AgentCore runtime."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="Unique identifier for the runtime")
    name: str = Field(..., description="Name of the runtime")
    status: VendorRuntimeStatus = Field(..., description="Status of the runtime")
    description: str | None = Field(None, description="Description of the runtime")
    version: str | None = Field(None, description="Version of the runtime")
    updatedAt: datetime = Field(
        ..., description="Last update timestamp", alias="updatedAt"
    )


class VendorRuntimesResponse(BaseModel):
    """Response model for vendor runtimes list."""

    model_config = ConfigDict(extra="ignore")

    data: list[VendorRuntime] = Field(..., description="List of vendor runtimes")
    pagination: TokenPagination = Field(
        ..., description="Token-based pagination information"
    )


class VendorRuntimeEndpointStatus(str, Enum):
    """Status of a vendor AgentCore runtime endpoint. AWS READY maps to PREPARED."""

    PREPARED = "PREPARED"
    NOT_PREPARED = "NOT_PREPARED"


class VendorRuntimeEndpoint(BaseModel):
    """Model representing a vendor AgentCore runtime endpoint."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="Unique identifier for the endpoint")
    name: str = Field(..., description="Name of the endpoint")
    status: VendorRuntimeEndpointStatus = Field(
        ..., description="Status of the endpoint"
    )
    description: str | None = Field(None, description="Description of the endpoint")
    liveVersion: str | None = Field(None, description="Currently live version")
    targetVersion: str | None = Field(None, description="Target/in-progress version")
    createdAt: datetime = Field(..., description="Creation timestamp")
    updatedAt: datetime = Field(..., description="Last update timestamp")
    aiRunId: str | None = Field(
        None,
        description="CodeMie assistant ID when endpoint is already imported; None otherwise",
    )


class VendorRuntimeEndpointsResponse(BaseModel):
    """Response model for vendor runtime endpoints list."""

    model_config = ConfigDict(extra="ignore")

    data: list[VendorRuntimeEndpoint] = Field(..., description="List of endpoints")
    pagination: TokenPagination = Field(
        ..., description="Token-based pagination information"
    )


class VendorRuntimeInstallRequest(BaseModel):
    """Request model for installing a vendor AgentCore runtime endpoint into CodeMie."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="Runtime ID")
    agentcoreRuntimeEndpointName: str = Field(
        ..., description="Endpoint name to install"
    )
    setting_id: str = Field(..., description="Vendor setting ID")
    configuration_json: str = Field(
        ...,
        description="JSON template string — either legacy __QUERY_PLACEHOLDER__ or new structured config",
    )
    assistant_name: str | None = Field(None, description="Assistant display name")
    assistant_description: str | None = Field(None, description="Assistant description")


class VendorRuntimeInstallSummary(BaseModel):
    """Per-endpoint summary returned from a runtime install operation."""

    model_config = ConfigDict(extra="ignore")

    runtimeId: str = Field(..., description="Runtime ID")
    endpointName: str = Field(..., description="Endpoint name")
    aiRunId: str = Field(
        ..., description="CodeMie assistant ID assigned to the endpoint"
    )


class VendorRuntimeInstallResponse(BaseModel):
    """Response model for vendor runtime endpoint install."""

    model_config = ConfigDict(extra="ignore")

    summary: list[VendorRuntimeInstallSummary] = Field(
        ..., description="Per-endpoint installation results"
    )


class VendorRuntimeUninstallResponse(BaseModel):
    """Response model for vendor runtime endpoint uninstall."""

    model_config = ConfigDict(extra="ignore")

    success: bool = Field(..., description="Whether the uninstall succeeded")


class VendorRuntimeEndpointDetail(VendorRuntimeEndpoint):
    """Detail model for a vendor AgentCore runtime endpoint (GET by name).

    Extends the list view with fields only present in the detail response.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    arn: str | None = Field(
        None, alias="agentRuntimeEndpointArn", description="Endpoint ARN"
    )
    runtimeArn: str | None = Field(
        None, alias="agentRuntimeArn", description="Parent runtime ARN"
    )
    failureReason: str | None = Field(
        None, description="Failure reason when status is NOT_PREPARED"
    )
