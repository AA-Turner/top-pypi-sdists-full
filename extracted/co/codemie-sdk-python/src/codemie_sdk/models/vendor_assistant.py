"""Models for vendor assistant settings."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class VendorType(str, Enum):
    """Supported cloud vendor types."""

    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"


class VendorAssistantStatus(str, Enum):
    """Status of vendor assistant."""

    PREPARED = "PREPARED"
    NOT_PREPARED = "NOT_PREPARED"


class VendorAssistantSetting(BaseModel):
    """Model representing a vendor assistant setting."""

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


class PaginationInfo(BaseModel):
    """Pagination information for list responses."""

    model_config = ConfigDict(extra="ignore")

    total: int = Field(..., description="Total number of items")
    pages: int = Field(..., description="Total number of pages")
    page: int = Field(..., description="Current page number (0-based)")
    per_page: int = Field(..., description="Number of items per page")


class VendorAssistantSettingsResponse(BaseModel):
    """Response model for vendor assistant settings list."""

    model_config = ConfigDict(extra="ignore")

    data: list[VendorAssistantSetting] = Field(
        ..., description="List of vendor assistant settings"
    )
    pagination: PaginationInfo = Field(..., description="Pagination information")


class VendorAssistant(BaseModel):
    """Model representing a vendor assistant."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="Unique identifier for the assistant")
    name: str = Field(..., description="Name of the assistant")
    status: VendorAssistantStatus = Field(..., description="Status of the assistant")
    description: str | None = Field(None, description="Description of the assistant")
    updatedAt: datetime = Field(
        ..., description="Last update timestamp", alias="updatedAt"
    )


class VendorAssistantVersion(BaseModel):
    """Model representing a specific version of a vendor assistant with detailed information."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="Unique identifier for the assistant")
    name: str = Field(..., description="Name of the assistant")
    status: VendorAssistantStatus = Field(..., description="Status of the assistant")
    version: str = Field(..., description="Version of the assistant")
    instruction: str = Field(..., description="Instructions for the assistant")
    foundationModel: str = Field(
        ...,
        description="ARN or identifier of the foundation model",
        alias="foundationModel",
    )
    description: str | None = Field(None, description="Description of the assistant")
    createdAt: datetime = Field(
        ..., description="Creation timestamp", alias="createdAt"
    )
    updatedAt: datetime = Field(
        ..., description="Last update timestamp", alias="updatedAt"
    )


class TokenPagination(BaseModel):
    """Token-based pagination information."""

    model_config = ConfigDict(extra="ignore")

    next_token: str | None = Field(None, description="Token for the next page")


class VendorAssistantsResponse(BaseModel):
    """Response model for vendor assistants list."""

    model_config = ConfigDict(extra="ignore")

    data: list[VendorAssistant] = Field(..., description="List of vendor assistants")
    pagination: TokenPagination = Field(
        ..., description="Token-based pagination information"
    )


class VendorAssistantAlias(BaseModel):
    """Model representing a vendor assistant alias."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="Unique identifier for the alias")
    name: str = Field(..., description="Name of the alias")
    status: VendorAssistantStatus = Field(..., description="Status of the alias")
    description: str | None = Field(None, description="Description of the alias")
    version: str = Field(..., description="Version of the alias")
    createdAt: datetime = Field(
        ..., description="Creation timestamp", alias="createdAt"
    )
    updatedAt: datetime = Field(
        ..., description="Last update timestamp", alias="updatedAt"
    )


class VendorAssistantAliasesResponse(BaseModel):
    """Response model for vendor assistant aliases list."""

    model_config = ConfigDict(extra="ignore")

    data: list[VendorAssistantAlias] = Field(
        ..., description="List of vendor assistant aliases"
    )
    pagination: TokenPagination = Field(
        ..., description="Token-based pagination information"
    )


class VendorAssistantInstallRequest(BaseModel):
    """Model for a single assistant installation request."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="Assistant ID to install")
    agentAliasId: str = Field(..., description="Alias ID to use for the assistant")
    setting_id: str = Field(..., description="Vendor setting ID")


class VendorAssistantInstallSummary(BaseModel):
    """Model for assistant installation summary."""

    model_config = ConfigDict(extra="ignore")

    agentId: str = Field(..., description="Installed assistant ID")
    agentAliasId: str = Field(..., description="Alias ID used for installation")
    aiRunId: str = Field(..., description="AI run ID for the installation")


class VendorAssistantInstallResponse(BaseModel):
    """Response model for assistant installation."""

    model_config = ConfigDict(extra="ignore")

    summary: list[VendorAssistantInstallSummary] = Field(
        ..., description="List of installation summaries"
    )


class VendorAssistantUninstallResponse(BaseModel):
    """Response model for assistant uninstallation."""

    model_config = ConfigDict(extra="ignore")

    success: bool = Field(..., description="Whether the uninstallation was successful")
