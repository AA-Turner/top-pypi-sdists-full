"""Models for vendor knowledge base settings."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from .vendor_assistant import PaginationInfo, TokenPagination


class VendorKnowledgeBaseSetting(BaseModel):
    """Model representing a vendor knowledge base setting."""

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


class VendorKnowledgeBaseSettingsResponse(BaseModel):
    """Response model for vendor knowledge base settings list."""

    model_config = ConfigDict(extra="ignore")

    data: list[VendorKnowledgeBaseSetting] = Field(
        ..., description="List of vendor knowledge base settings"
    )
    pagination: PaginationInfo = Field(..., description="Pagination information")


class VendorKnowledgeBaseStatus(str, Enum):
    """Status of vendor knowledge base."""

    PREPARED = "PREPARED"
    NOT_PREPARED = "NOT_PREPARED"


class VendorKnowledgeBase(BaseModel):
    """Model representing a vendor knowledge base."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="Unique identifier for the knowledge base")
    name: str = Field(..., description="Name of the knowledge base")
    status: VendorKnowledgeBaseStatus = Field(
        ..., description="Status of the knowledge base"
    )
    description: str | None = Field(
        None, description="Description of the knowledge base"
    )
    updatedAt: datetime = Field(
        ..., description="Last update timestamp", alias="updatedAt"
    )
    aiRunId: str | None = Field(
        None,
        description="AI run ID if the knowledge base is installed",
        alias="aiRunId",
    )


class VendorKnowledgeBasesResponse(BaseModel):
    """Response model for vendor knowledge bases list."""

    model_config = ConfigDict(extra="ignore")

    data: list[VendorKnowledgeBase] = Field(
        ..., description="List of vendor knowledge bases"
    )
    pagination: TokenPagination = Field(
        ..., description="Token-based pagination information"
    )


class VendorKnowledgeBaseDetail(BaseModel):
    """Model representing detailed information about a vendor knowledge base."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="Unique identifier for the knowledge base")
    name: str = Field(..., description="Name of the knowledge base")
    description: str | None = Field(
        None, description="Description of the knowledge base"
    )
    type: str = Field(..., description="Type of knowledge base (e.g., VECTOR)")
    status: VendorKnowledgeBaseStatus = Field(
        ..., description="Status of the knowledge base"
    )
    embeddingModel: str = Field(
        ...,
        description="Embedding model used by the knowledge base",
        alias="embeddingModel",
    )
    kendraIndexArn: str | None = Field(
        None, description="Kendra index ARN if applicable", alias="kendraIndexArn"
    )
    createdAt: datetime = Field(
        ..., description="Creation timestamp", alias="createdAt"
    )
    updatedAt: datetime = Field(
        ..., description="Last update timestamp", alias="updatedAt"
    )
    aiRunId: str | None = Field(
        None,
        description="AI run ID if the knowledge base is installed",
        alias="aiRunId",
    )


class VendorKnowledgeBaseInstallRequest(BaseModel):
    """Model for a single knowledge base installation request."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="Knowledge base ID to install")
    setting_id: str = Field(..., description="Vendor setting ID")


class VendorKnowledgeBaseInstallSummary(BaseModel):
    """Model for knowledge base installation summary."""

    model_config = ConfigDict(extra="ignore")

    knowledgeBaseId: str = Field(..., description="Installed knowledge base ID")
    aiRunId: str = Field(..., description="AI run ID for the installation")


class VendorKnowledgeBaseInstallResponse(BaseModel):
    """Response model for knowledge base installation."""

    model_config = ConfigDict(extra="ignore")

    summary: list[VendorKnowledgeBaseInstallSummary] = Field(
        ..., description="List of installation summaries"
    )


class VendorKnowledgeBaseUninstallResponse(BaseModel):
    """Response model for knowledge base uninstallation."""

    model_config = ConfigDict(extra="ignore")

    success: bool = Field(..., description="Whether the uninstallation was successful")
