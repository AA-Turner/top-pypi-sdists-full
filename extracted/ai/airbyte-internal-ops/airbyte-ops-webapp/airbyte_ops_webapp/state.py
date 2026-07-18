"""Shared runtime configuration for the Airbyte Ops Webapp."""

from __future__ import annotations

import os
from importlib.metadata import PackageNotFoundError, version

from pydantic import BaseModel, ConfigDict

MOCK_ONLY_ENV_VAR = "AIRBYTE_OPS_WEBAPP_MOCKONLY"
PREVIEW_ENV_VAR = "AIRBYTE_OPS_WEBAPP_PREVIEW"
PREVIEW_PR_ENV_VAR = "AIRBYTE_OPS_WEBAPP_PREVIEW_PR"
DEPLOY_SHA_ENV_VAR = "AIRBYTE_OPS_WEBAPP_DEPLOY_SHA"
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
    """Shared Prefab page state for every Airbyte Ops page.

    This is the single source of truth for the environment, deploy, and auth
    state that every page needs. Pages build their initial state by spreading
    `OpsPageState.from_env(...).to_prefab_state()` and adding only their own
    page-specific keys, so the shared block is never re-declared per page.
    """

    model_config = ConfigDict(frozen=True)

    # --- Fixed environment / deploy metadata (read-only at render time) ---
    is_mock_only: bool
    is_preview_deploy: bool = False
    preview_pr_number: str = ""
    preview_pr_url: str = ""
    deploy_sha: str = ""
    deploy_sha_url: str = ""
    ops_package_version: str = ""
    default_connector_from_args: bool = False

    # --- Shared tool-call lifecycle ---
    is_loading: bool = False
    loading_message: str = ""
    tool_error: str = ""

    # --- Auth (Airbyte / Keycloak) ---
    auth_bearer_token: str = ""
    admin_user_email: str = ""
    oauth_config: OAuthConfigState
    oauth_enabled: bool
    oauth_authenticated: bool = False
    oauth_status: str = ""
    oauth_user_email: str = ""

    # --- Auth (Google / BigQuery) ---
    google_authenticated: bool = False
    google_user_email: str = ""
    google_access_token: str = ""
    google_status: str = ""

    @classmethod
    def from_env(
        cls,
        *,
        oauth_config: OAuthConfigState,
        default_connector_from_args: bool = False,
    ) -> OpsPageState:
        """Build shared page state from process env vars and the OAuth config.

        Reads the environment-derived values (`mock_only_enabled`,
        `preview_*`, `deploy_sha*`, `ops_package_version`) so no page has to
        repeat that wiring. `default_connector_from_args` records whether the
        page was opened with an explicit connector argument.
        """
        return cls(
            is_mock_only=mock_only_enabled(),
            is_preview_deploy=preview_deploy_enabled(),
            preview_pr_number=preview_pr_number(),
            preview_pr_url=preview_pr_url(),
            deploy_sha=deploy_sha(),
            deploy_sha_url=deploy_sha_url(),
            ops_package_version=ops_package_version(),
            oauth_config=oauth_config,
            oauth_enabled=oauth_config.enabled,
            default_connector_from_args=default_connector_from_args,
        )

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


def deploy_sha() -> str:
    """Return the short commit SHA for the current deploy, or empty string."""
    return os.getenv(DEPLOY_SHA_ENV_VAR, "").strip()


def deploy_sha_url() -> str:
    """Return the GitHub commit URL for the current deploy SHA."""
    sha = deploy_sha()
    if not sha:
        return ""
    return f"{GITHUB_REPO_URL}/commit/{sha}"


def ops_package_version() -> str:
    """Return the installed version of the `airbyte-internal-ops` package."""
    try:
        return version("airbyte-internal-ops")
    except PackageNotFoundError:
        return ""
