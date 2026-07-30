"""Configuration for the SaaS github-documents-cloud ingestion source."""

from __future__ import annotations

from typing import Optional

from pydantic import Field, SecretStr, field_validator, model_validator

from acryl_datahub_cloud.github_documents_cloud.sync_back.config import SyncBackConfig
from datahub.ingestion.source.github_documents.github_documents_config import (
    GitHubDocumentsSourceConfig,
)

GITHUB_CONNECTION_URN = "urn:li:dataHubConnection:__system_github-0"


class GitHubDocumentsCloudSourceConfig(GitHubDocumentsSourceConfig):
    """Extends the OSS github-documents config with GitHub App connection auth.

    Authentication resolves in priority order:

    1. ``connection`` — set to the tenant-wide GitHub App connection URN
       (``__system_github-0``). Short-lived installation tokens are minted by the
       DataHub backend (GMS proxies to the integrations service / cloud-router),
       so the executor never handles the App signing key. This is the preferred
       SaaS path.
    2. ``github_token`` — a personal access token fallback for users who opt out
       of the GitHub App.

    Exactly one of the two must be provided.
    """

    # Override the OSS field to make PAT optional (App auth is preferred).
    # validate_auth_method enforces that some credential resolves.
    github_token: Optional[SecretStr] = Field(  # type: ignore[assignment]
        default=None,
        description=(
            "GitHub personal access token. Optional fallback used only when no "
            "GitHub App connection is configured."
        ),
    )

    connection: Optional[str] = Field(
        default=None,
        description=(
            "URN of the GitHub App connection to authenticate with "
            f"(typically {GITHUB_CONNECTION_URN}). When set, short-lived "
            "installation tokens are minted by the DataHub backend; no GitHub "
            "credentials are stored in the recipe."
        ),
    )

    sync_back: SyncBackConfig = Field(
        default_factory=SyncBackConfig,
        description=(
            "Cloud-only: write DataHub document edits back to GitHub after the "
            "import phase. Disabled by default."
        ),
    )

    @field_validator("github_token")
    @classmethod
    def validate_github_token(  # type: ignore[override]
        cls, value: Optional[SecretStr]
    ) -> Optional[SecretStr]:
        # Relax the OSS validator: github_token is optional here. The XOR check in
        # validate_auth_method enforces that some credential is present.
        if value is not None and not value.get_secret_value().strip():
            return None
        return value

    @property
    def has_app_auth(self) -> bool:
        return bool(self.connection)

    @property
    def has_pat_auth(self) -> bool:
        return self.github_token is not None

    @model_validator(mode="after")
    def validate_auth_method(self) -> "GitHubDocumentsCloudSourceConfig":
        if self.has_app_auth and self.has_pat_auth:
            raise ValueError(
                "Provide either a GitHub App 'connection' or a 'github_token', "
                "not both."
            )
        if not self.has_app_auth and not self.has_pat_auth:
            raise ValueError(
                "GitHub authentication is required: set 'connection' to a GitHub "
                "App connection URN or provide a 'github_token'."
            )
        return self
