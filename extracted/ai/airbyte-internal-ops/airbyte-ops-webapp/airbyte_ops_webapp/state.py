"""Shared runtime configuration for the Airbyte Ops Webapp."""

from __future__ import annotations

import os

from pydantic import BaseModel, ConfigDict

MOCK_ONLY_ENV_VAR = "AIRBYTE_OPS_WEBAPP_MOCKONLY"
PREVIEW_ENV_VAR = "AIRBYTE_OPS_WEBAPP_PREVIEW"
PREVIEW_PR_ENV_VAR = "AIRBYTE_OPS_WEBAPP_PREVIEW_PR"
GITHUB_REPO_URL = "https://github.com/airbytehq/airbyte-ops-mcp"
AIRBYTE_BEARER_TOKEN_ENV_VAR = "AIRBYTE_CLOUD_BEARER_TOKEN"
AIRBYTE_CLIENT_ID_ENV_VAR = "AIRBYTE_CLOUD_CLIENT_ID"
AIRBYTE_CLIENT_SECRET_ENV_VAR = "AIRBYTE_CLOUD_CLIENT_SECRET"
AIRBYTE_CONFIG_API_ROOT_ENV_VAR = "AIRBYTE_CLOUD_CONFIG_API_URL"
OAUTH_CLIENT_ID_ENV_VAR = "AIRBYTE_OPS_WEBAPP_OAUTH_CLIENT_ID"
OAUTH_CLIENT_SECRET_ENV_VAR = "AIRBYTE_OPS_WEBAPP_OAUTH_CLIENT_SECRET"
OAUTH_ENABLED_ENV_VAR = "AIRBYTE_OPS_WEBAPP_OAUTH_ENABLED"
OAUTH_ISSUER_ENV_VAR = "AIRBYTE_OPS_WEBAPP_OAUTH_ISSUER"
OAUTH_PUBLIC_URL_ENV_VAR = "AIRBYTE_OPS_WEBAPP_PUBLIC_URL"
OAUTH_REDIRECT_URI_ENV_VAR = "AIRBYTE_OPS_WEBAPP_OAUTH_REDIRECT_URI"


class OAuthConfigState(BaseModel):
    """OAuth configuration exposed to Prefab page state."""

    model_config = ConfigDict(frozen=True)

    enabled: bool
    issuer: str
    client_id: str
    redirect_uri: str
    authorization_endpoint: str
    token_endpoint: str
    session_endpoint: str
    token_exchange_endpoint: str


class OpsPageState(BaseModel):
    """Shared Prefab page state for Airbyte Ops pages."""

    model_config = ConfigDict(frozen=True)

    auth_bearer_token: str = ""
    admin_user_email: str = ""
    default_connector_from_args: bool = False
    is_mock_only: bool
    is_preview_deploy: bool = False
    preview_pr_number: str = ""
    preview_pr_url: str = ""
    oauth_config: OAuthConfigState
    oauth_enabled: bool
    oauth_authenticated: bool = False
    oauth_status: str = ""
    oauth_user_email: str = ""

    def to_prefab_state(self) -> dict[str, object]:
        """Return this model as `PrefabApp.state` data."""
        return self.model_dump(mode="json")


def mock_only_enabled() -> bool:
    """Return `True` when the app is explicitly running with mock data."""
    return os.getenv(MOCK_ONLY_ENV_VAR, "").strip().lower() in {"1", "true"}


def preview_deploy_enabled() -> bool:
    """Return `True` when the app is running as a preview deploy."""
    return os.getenv(PREVIEW_ENV_VAR, "").strip().lower() in {"1", "true"}


def preview_pr_number() -> str:
    """Return the PR number for the current preview deploy, or empty string."""
    return os.getenv(PREVIEW_PR_ENV_VAR, "").strip()


def preview_pr_url() -> str:
    """Return the full GitHub PR URL for the current preview deploy."""
    pr = preview_pr_number()
    if not pr:
        return ""
    return f"{GITHUB_REPO_URL}/pull/{pr}"
