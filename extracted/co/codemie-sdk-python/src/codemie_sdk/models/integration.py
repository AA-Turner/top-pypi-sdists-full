"""Models for assistant-related data structures."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, ConfigDict, field_serializer


class CredentialTypes(str, Enum):
    """Enum for credential types."""

    JIRA = "Jira"
    CONFLUENCE = "Confluence"
    GIT = "Git"
    KUBERNETES = "Kubernetes"
    AWS = "AWS"
    GCP = "GCP"
    KEYCLOAK = "Keycloak"
    AZURE = "Azure"
    ELASTIC = "Elastic"
    OPENAPI = "OpenAPI"
    PLUGIN = "Plugin"
    FILESYSTEM = "FileSystem"
    SCHEDULER = "Scheduler"
    WEBHOOK = "Webhook"
    EMAIL = "Email"
    AZURE_DEVOPS = "AzureDevOps"
    SONAR = "Sonar"
    SQL = "SQL"
    TELEGRAM = "Telegram"
    ZEPHYR_SCALE = "ZephyrScale"
    SERVICE_NOW = "ServiceNow"
    DIAL = "DIAL"
    A2A = "A2A"
    MCP = "MCP"
    LITE_LLM = "LiteLLM"
    REPORT_PORTAL = "ReportPortal"
    XRAY = "Xray"
    SHAREPOINT = "SharePoint"
    GOOGLE_OAUTH = "GoogleOAuth"
    XWIKI = "XWiki"
    MS_TEAMS = "MSTeams"


class IntegrationType(str, Enum):
    """Enum for setting types."""

    USER = "user"
    PROJECT = "project"


class CredentialValues(BaseModel):
    """Model for credential values."""

    model_config = ConfigDict(extra="ignore")

    key: str
    value: Any


class Integration(BaseModel):
    """Model for settings configuration."""

    def __getitem__(self, key):
        return getattr(self, key)

    model_config = ConfigDict(extra="ignore")

    id: str | None = None
    date: datetime | None = None
    update_date: datetime | None = None
    user_id: str | None = None
    project_name: str
    alias: str | None = None
    default: bool = False
    is_global: bool | None = False
    credential_type: CredentialTypes
    credential_values: list[CredentialValues]
    setting_type: IntegrationType = Field(default=IntegrationType.USER)

    @field_serializer("date", "update_date")
    def serialize_dt(self, dt: datetime, _info):
        return dt.isoformat()


class IntegrationTestRequest(BaseModel):
    """Model for integration test request."""

    credential_type: str
    credential_values: list[CredentialValues] | None = None
    setting_id: str | None = None


class IntegrationTestResponse(BaseModel):
    """Model for integration test response."""

    def __getitem__(self, key):
        return getattr(self, key)

    message: str
    success: bool


class TransferMode(str, Enum):
    """Enum for the POST /v1/settings/transfer mode."""

    MOVE = "move"
    COPY = "copy"


class TransferItem(BaseModel):
    """Model for a single integration transferred or skipped by a settings-transfer request."""

    id: str
    alias: str
    credential_type: str


class TransferSettingsResponse(BaseModel):
    """Model for the response of POST /v1/settings/transfer.

    Mirrors ``codemie.rest_api.models.settings_transfer.TransferSettingsResponse``
    on the backend.
    """

    message: str
    source_project_name: str
    target_project_name: str
    mode: TransferMode
    transferred_count: int
    transferred: list[TransferItem] = Field(default_factory=list)
    skipped_count: int = 0
    skipped: list[TransferItem] = Field(default_factory=list)
