"""Models for vendor workflow settings."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from .vendor_assistant import PaginationInfo, TokenPagination


class VendorWorkflowSetting(BaseModel):
    """Model representing a vendor workflow setting."""

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


class VendorWorkflowSettingsResponse(BaseModel):
    """Response model for vendor workflow settings list."""

    model_config = ConfigDict(extra="ignore")

    data: list[VendorWorkflowSetting] = Field(
        ..., description="List of vendor workflow settings"
    )
    pagination: PaginationInfo = Field(..., description="Pagination information")


class VendorWorkflowStatus(str, Enum):
    """Status of vendor workflow."""

    PREPARED = "PREPARED"
    NOT_PREPARED = "NOT_PREPARED"


class VendorWorkflow(BaseModel):
    """Model representing a vendor workflow."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="Unique identifier for the workflow")
    name: str = Field(..., description="Name of the workflow")
    status: VendorWorkflowStatus = Field(..., description="Status of the workflow")
    description: str | None = Field(None, description="Description of the workflow")
    version: str = Field(..., description="Version of the workflow")
    createdAt: datetime = Field(
        ..., description="Creation timestamp", alias="createdAt"
    )
    updatedAt: datetime = Field(
        ..., description="Last update timestamp", alias="updatedAt"
    )


class VendorWorkflowsResponse(BaseModel):
    """Response model for vendor workflows list."""

    model_config = ConfigDict(extra="ignore")

    data: list[VendorWorkflow] = Field(..., description="List of vendor workflows")
    pagination: TokenPagination = Field(
        ..., description="Token-based pagination information"
    )


class VendorWorkflowAlias(BaseModel):
    """Model representing a vendor workflow alias."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="Unique identifier for the alias")
    name: str = Field(..., description="Name of the alias")
    status: VendorWorkflowStatus = Field(..., description="Status of the alias")
    description: str | None = Field(None, description="Description of the alias")
    version: str = Field(..., description="Version of the alias")
    createdAt: datetime = Field(
        ..., description="Creation timestamp", alias="createdAt"
    )
    updatedAt: datetime = Field(
        ..., description="Last update timestamp", alias="updatedAt"
    )
    aiRunId: str | None = Field(
        None, description="AI run ID if the alias is installed", alias="aiRunId"
    )


class VendorWorkflowAliasesResponse(BaseModel):
    """Response model for vendor workflow aliases list."""

    model_config = ConfigDict(extra="ignore")

    data: list[VendorWorkflowAlias] = Field(
        ..., description="List of vendor workflow aliases"
    )
    pagination: TokenPagination = Field(
        ..., description="Token-based pagination information"
    )


class VendorWorkflowInstallRequest(BaseModel):
    """Model for a single workflow installation request."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="Workflow ID to install")
    flowAliasId: str = Field(..., description="Flow alias ID to use for the workflow")
    setting_id: str = Field(..., description="Vendor setting ID")


class VendorWorkflowInstallSummary(BaseModel):
    """Model for workflow installation summary."""

    model_config = ConfigDict(extra="ignore")

    flowId: str = Field(..., description="Installed workflow ID")
    flowAliasId: str = Field(..., description="Flow alias ID used for installation")
    aiRunId: str = Field(..., description="AI run ID for the installation")


class VendorWorkflowInstallResponse(BaseModel):
    """Response model for workflow installation."""

    model_config = ConfigDict(extra="ignore")

    summary: list[VendorWorkflowInstallSummary] = Field(
        ..., description="List of installation summaries"
    )


class VendorWorkflowUninstallResponse(BaseModel):
    """Response model for workflow uninstallation."""

    model_config = ConfigDict(extra="ignore")

    success: bool = Field(..., description="Whether the uninstallation was successful")
