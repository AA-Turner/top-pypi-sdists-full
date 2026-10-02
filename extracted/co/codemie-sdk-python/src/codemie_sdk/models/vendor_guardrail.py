"""Models for vendor guardrail settings."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from .vendor_assistant import PaginationInfo, TokenPagination


class VendorGuardrailSetting(BaseModel):
    """Model representing a vendor guardrail setting."""

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


class VendorGuardrailSettingsResponse(BaseModel):
    """Response model for vendor guardrail settings list."""

    model_config = ConfigDict(extra="ignore")

    data: list[VendorGuardrailSetting] = Field(
        ..., description="List of vendor guardrail settings"
    )
    pagination: PaginationInfo = Field(..., description="Pagination information")


class VendorGuardrailStatus(str, Enum):
    """Status of vendor guardrail."""

    PREPARED = "PREPARED"
    NOT_PREPARED = "NOT_PREPARED"


class VendorGuardrail(BaseModel):
    """Model representing a vendor guardrail."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="Unique identifier for the guardrail")
    name: str = Field(..., description="Name of the guardrail")
    status: VendorGuardrailStatus = Field(..., description="Status of the guardrail")
    description: str | None = Field(None, description="Description of the guardrail")
    version: str = Field(..., description="Version of the guardrail")
    createdAt: datetime = Field(
        ..., description="Creation timestamp", alias="createdAt"
    )
    updatedAt: datetime = Field(
        ..., description="Last update timestamp", alias="updatedAt"
    )


class VendorGuardrailsResponse(BaseModel):
    """Response model for vendor guardrails list."""

    model_config = ConfigDict(extra="ignore")

    data: list[VendorGuardrail] = Field(..., description="List of vendor guardrails")
    pagination: TokenPagination = Field(
        ..., description="Token-based pagination information"
    )


class VendorGuardrailVersion(BaseModel):
    """Model representing a vendor guardrail version."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="Unique identifier for the guardrail")
    version: str = Field(..., description="Version of the guardrail")
    name: str = Field(..., description="Name of the guardrail")
    status: VendorGuardrailStatus = Field(..., description="Status of the version")
    description: str | None = Field(None, description="Description of the version")
    blockedInputMessaging: str | None = Field(
        None,
        description="Message to display when input is blocked by guardrail",
        alias="blockedInputMessaging",
    )
    blockedOutputsMessaging: str | None = Field(
        None,
        description="Message to display when output is blocked by guardrail",
        alias="blockedOutputsMessaging",
    )
    createdAt: datetime = Field(
        ..., description="Creation timestamp", alias="createdAt"
    )
    updatedAt: datetime = Field(
        ..., description="Last update timestamp", alias="updatedAt"
    )


class VendorGuardrailVersionsResponse(BaseModel):
    """Response model for vendor guardrail versions list."""

    model_config = ConfigDict(extra="ignore")

    data: list[VendorGuardrailVersion] = Field(
        ..., description="List of vendor guardrail versions"
    )
    pagination: TokenPagination = Field(
        ..., description="Token-based pagination information"
    )


class VendorGuardrailInstallRequest(BaseModel):
    """Model for a single guardrail installation request."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="Guardrail ID to install")
    version: str = Field(..., description="Version to use for the guardrail")
    setting_id: str = Field(..., description="Vendor setting ID")


class VendorGuardrailInstallSummary(BaseModel):
    """Model for guardrail installation summary."""

    model_config = ConfigDict(extra="ignore")

    guardrailId: str = Field(..., description="Installed guardrail ID")
    version: str = Field(..., description="Version used for installation")
    aiRunId: str = Field(..., description="AI run ID for the installation")


class VendorGuardrailInstallResponse(BaseModel):
    """Response model for guardrail installation."""

    model_config = ConfigDict(extra="ignore")

    summary: list[VendorGuardrailInstallSummary] = Field(
        ..., description="List of installation summaries"
    )


class VendorGuardrailUninstallResponse(BaseModel):
    """Response model for guardrail uninstallation."""

    model_config = ConfigDict(extra="ignore")

    success: bool = Field(..., description="Whether the uninstallation was successful")
