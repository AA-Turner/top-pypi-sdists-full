import os
import time
from dataclasses import dataclass
from typing import Generator, Optional, Union
from uuid import UUID

import httpx
import jwt
from dlt._workspace._workspace_context import WorkspaceRunContext, active
from dlt._workspace.cli.config_toml_writer import WritableConfigValue, write_values
from dlt._workspace.exceptions import WorkspaceRunContextNotAvailable
from dlt.common.configuration.providers.toml import (
    ConfigTomlProvider,
    SecretsTomlProvider,
)
from dlt.common.configuration.specs.pluggable_run_context import RunContextBase
from dlt.common.configuration.specs.runtime_configuration import RuntimeConfiguration
from jwt.exceptions import PyJWTError

from dlt_runtime.version import __version__

from dlt_runtime.exceptions import (
    RuntimeNotAuthenticated,
    RuntimeOperationNotAuthorized,
    exception_from_response,
    handle_client_exceptions,
)
from dlt_runtime.runtime_clients.api.api.me import me
from dlt_runtime.runtime_clients.api.api.workspaces import create_workspace
from dlt_runtime.runtime_clients.api.client import Client as ApiClient
from dlt_runtime.runtime_clients.api.models.me_response import MeResponse
from dlt_runtime.runtime_clients.api.models.workspace_create_request import (
    WorkspaceCreateRequest,
)
from dlt_runtime.runtime_clients.api.models.workspace_response import WorkspaceResponse
from dlt_runtime.runtime_clients.api.models.workspace_with_membership_response import (
    WorkspaceWithMembershipResponse,
)
from dlt_runtime.runtime_clients.auth.api.default import refresh as refresh_api
from dlt_runtime.runtime_clients.auth.client import Client as AuthClient
from dlt_runtime.runtime_clients.auth.models.refresh_request import RefreshRequest
from dlt_runtime.runtime_clients.auth.models.refresh_response import RefreshResponse


@dataclass
class AuthInfo:
    user_id: str
    email: str
    jwt_token: str
    token_expiry: Optional[float] = None


@dataclass
class WorkspaceInfo:
    """Information about a workspace from /me endpoint."""

    id: str
    name: str
    description: Optional[str]
    role: Optional[str] = None


@dataclass
class UserInfo:
    """Information about the currently authenticated user from /me endpoint."""

    email: str
    user_id: UUID
    identity_id: UUID
    default_organization_id: UUID
    default_workspace: WorkspaceInfo
    workspaces: list[WorkspaceInfo]


class RuntimeAuthService:
    """
    Implements login, logout and auth check internals

    Authentication is performed based on the JWT token stored in the global secrets. On top of that,
    authorization uses organisation and workspace id stored in the local config. For that, depending on the usage,
    either workspace run context or base run context is required.
    """

    auth_info: Optional[AuthInfo] = None

    _run_context: RunContextBase
    _local_workspace_id: Optional[str] = None

    def __init__(self, run_context: RunContextBase):
        self._run_context = run_context

    @property
    def workspace_run_context(self) -> WorkspaceRunContext:
        if isinstance(self._run_context, WorkspaceRunContext):
            return self._run_context
        else:
            raise WorkspaceRunContextNotAvailable(self._run_context.run_dir)

    @property
    def run_context(self) -> WorkspaceRunContext:
        if not isinstance(self._run_context, WorkspaceRunContext):
            raise RuntimeOperationNotAuthorized(
                "Run context is not a WorkspaceRunContext"
            )
        return self._run_context

    @property
    def workspace_id(self) -> str:
        ws_id = (
            self._local_workspace_id
            or self.workspace_run_context.runtime_config.workspace_id
        )
        if not ws_id:
            raise RuntimeOperationNotAuthorized()
        return ws_id

    def authenticate(self) -> AuthInfo:
        try:
            return self._read_token()
        except RuntimeNotAuthenticated:
            # Token invalid/expired — try refresh before giving up.
            try:
                if self.refresh():
                    assert self.auth_info is not None
                    return self.auth_info
            except Exception:
                pass  # refresh failed — fall through to re-raise original
            raise

    def login(
        self, token: str, refresh_token: Optional[str] = None
    ) -> tuple[AuthInfo, UserInfo]:
        auth_info = self._save_token(token)
        if refresh_token:
            self._save_refresh_token(refresh_token)
        user_info = self.fetch_user_info()
        return auth_info, user_info

    def logout(self) -> None:
        self._delete_token()
        self._delete_refresh_token()
        self.auth_info = None

    def refresh(self) -> bool:
        """Refresh JWT using stored refresh token. Returns True on success."""
        # Bail out early if there's no refresh token stored
        stored_refresh_token = self._read_refresh_token()
        if not stored_refresh_token:
            return False

        # Call the refresh endpoint — 400/401 mean the token is invalid,
        # any other error (5xx, network) should propagate to the caller.
        response = refresh_api.sync_detailed(
            client=get_auth_client(),
            body=RefreshRequest(refresh_token=stored_refresh_token),
        )
        if not isinstance(response.parsed, RefreshResponse):
            return False

        # Persist the new JWT and rotate the refresh token
        self._save_token(response.parsed.jwt)
        self._save_refresh_token(response.parsed.refresh_token)
        return True

    def overwrite_local_workspace_id(self, selected_workspace_id: str) -> None:
        local_toml_config = ConfigTomlProvider(self.workspace_run_context.settings_dir)
        local_toml_config.set_value(
            "workspace_id",
            str(selected_workspace_id),
            None,
            RuntimeConfiguration.__section__,
        )
        local_toml_config.write_toml()
        self._local_workspace_id = selected_workspace_id

    def _read_token(self) -> AuthInfo:
        config = self.workspace_run_context.runtime_config
        if not config.auth_token:
            raise RuntimeNotAuthenticated("No token found")
        self.auth_info = self._validate_and_decode_jwt(config.auth_token)
        return self.auth_info

    def _save_token(self, token: str) -> AuthInfo:
        self.auth_info = self._validate_and_decode_jwt(token)
        value = [
            WritableConfigValue(
                "auth_token", str, token, (RuntimeConfiguration.__section__,)
            )
        ]
        # write global secrets
        global_path = self.run_context.global_dir
        os.makedirs(global_path, exist_ok=True)
        secrets = SecretsTomlProvider(settings_dir=global_path)
        write_values(secrets._config_toml, value, overwrite_existing=True)
        secrets.write_toml()
        return self.auth_info

    def fetch_user_info(self) -> UserInfo:
        """Fetch user info including all accessible workspaces from /me endpoint."""
        error_message = "Failed to get your user info from the Runtime API. Try logging out and in again"
        client = get_api_client(self)
        with handle_client_exceptions(error_message):
            me_response = me.sync_detailed(client=client)

        if isinstance(me_response.parsed, MeResponse):
            parsed = me_response.parsed

            workspaces_list: list[WorkspaceInfo]
            if isinstance(parsed.workspaces, list):
                workspaces_list = [
                    self._convert_workspace_membership(wm) for wm in parsed.workspaces
                ]
            else:
                # Fallback: just the last workspace if workspaces not returned.
                # Assume owner role since this is the user's own default workspace.
                ws_info = self._convert_workspace(parsed.last_workspace)
                ws_info.role = "owner"
                workspaces_list = [ws_info]

            return UserInfo(
                email=parsed.email,
                user_id=parsed.user_id,
                identity_id=parsed.identity_id,
                default_organization_id=parsed.primary_organization.id,
                default_workspace=self._convert_workspace(parsed.last_workspace),
                workspaces=workspaces_list,
            )
        else:
            raise exception_from_response(error_message, me_response)

    def _convert_workspace(self, workspace: WorkspaceResponse) -> WorkspaceInfo:
        from dlt_runtime.runtime_clients.api.types import Unset

        description = workspace.description
        if isinstance(description, Unset):
            description = None

        return WorkspaceInfo(
            id=str(workspace.id),
            name=workspace.name,
            description=description,
        )

    def _convert_workspace_membership(
        self, wm: WorkspaceWithMembershipResponse
    ) -> WorkspaceInfo:
        """Convert a WorkspaceWithMembershipResponse to WorkspaceInfo."""
        info = self._convert_workspace(wm.workspace)
        info.role = wm.role
        return info

    def create_new_workspace(
        self,
        user_info: UserInfo,
        name: str,
        description: Optional[str],
    ) -> str:
        """Create a new workspace via the API."""
        with handle_client_exceptions("Failed to create workspace"):
            create_result = create_workspace.sync_detailed(
                organization_id=user_info.default_organization_id,
                client=get_api_client(self),
                body=WorkspaceCreateRequest(name=name, description=description),
            )
        if isinstance(create_result.parsed, WorkspaceResponse):
            return str(create_result.parsed.id)
        else:
            raise exception_from_response("Failed to create workspace", create_result)

    def _delete_token(self) -> None:
        # delete from global secrets directly, because in other cases config deletion is not supported
        local_toml_config = SecretsTomlProvider(self.workspace_run_context.global_dir)
        local_toml_config.set_value(
            "auth_token",
            "",
            None,
            RuntimeConfiguration.__section__,
        )
        local_toml_config.write_toml()

    def _save_refresh_token(self, refresh_token: str) -> None:
        """Persist the refresh token to the global secrets.toml."""
        value = [
            WritableConfigValue(
                "refresh_token", str, refresh_token, (RuntimeConfiguration.__section__,)
            )
        ]
        global_path = self.run_context.global_dir
        os.makedirs(global_path, exist_ok=True)
        secrets = SecretsTomlProvider(settings_dir=global_path)
        write_values(secrets._config_toml, value, overwrite_existing=True)
        secrets.write_toml()

    def _read_refresh_token(self) -> Optional[str]:
        """Read the refresh token from the global secrets.toml, or None if absent."""
        secrets = SecretsTomlProvider(
            settings_dir=self.workspace_run_context.global_dir
        )
        value, _ = secrets.get_value(
            "refresh_token", str, "", RuntimeConfiguration.__section__
        )
        return value if value else None

    def _delete_refresh_token(self) -> None:
        """Remove the refresh token from the global secrets.toml."""
        secrets = SecretsTomlProvider(self.workspace_run_context.global_dir)
        secrets.set_value(
            "refresh_token",
            "",
            None,
            RuntimeConfiguration.__section__,
        )
        secrets.write_toml()

    def _validate_and_decode_jwt(self, token: Union[str, bytes]) -> AuthInfo:
        if isinstance(token, str):
            token = token.encode("utf-8")
        try:
            payload = jwt.decode(
                token,
                key="",
                algorithms=["EdDSA"],
                options={
                    "verify_signature": False,
                    "verify_exp": False,
                    "verify_aud": False,
                },
            )
        except PyJWTError as e:
            raise RuntimeNotAuthenticated("Failed to decode JWT") from e

        token_expiry = payload.get("exp")
        if token_expiry is not None and token_expiry < time.time():
            raise RuntimeNotAuthenticated(
                "Your authentication token has expired. Please run 'dlt runtime login' to re-authenticate"
            )

        try:
            auth_info = AuthInfo(
                jwt_token=token.decode("utf-8"),
                email=payload["email"],
                user_id=payload["sub"],
                token_expiry=token_expiry,
            )
        except (KeyError, TypeError) as e:
            raise RuntimeNotAuthenticated("Failed to validate JWT payload") from e

        return auth_info


def get_auth_client() -> AuthClient:
    auth_base_url = active().runtime_config.auth_base_url
    if not auth_base_url:
        raise RuntimeError(
            "auth_base_url is not configured in the runtime configuration"
        )
    return AuthClient(
        base_url=auth_base_url, verify_ssl=False, raise_on_unexpected_status=True
    )


# Must match the detail string returned by the API auth middleware for expired tokens.
_EXPIRED_TOKEN_MARKER = "Token expired"


class RuntimeAuth(httpx.Auth):
    """httpx Auth that sets the Bearer token and refreshes on 401."""

    requires_response_body = True

    def __init__(self, auth_service: RuntimeAuthService) -> None:
        self._auth_service = auth_service

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        proactive_refresh_succeeded = False

        # Proactive refresh: if the token expires within 60 s, refresh now
        # to avoid a wasted 401 round-trip.
        if self._auth_service.auth_info and self._is_token_expiring():
            try:
                proactive_refresh_succeeded = self._auth_service.refresh()
            except Exception:
                pass

        # Attach current JWT (possibly freshly refreshed)
        if self._auth_service.auth_info:
            request.headers["Authorization"] = (
                f"Bearer {self._auth_service.auth_info.jwt_token}"
            )

        response = yield request

        if response.status_code != 401:
            return

        # If the proactive refresh succeeded and the server still returned
        # 401-expired, the problem isn't a stale token. Clear everything.
        if proactive_refresh_succeeded and self._is_expired_token_response(response):
            self._auth_service.logout()
            return

        # Try to obtain a new JWT using the stored refresh token.
        # This handles both expired tokens and corrupted/invalid tokens
        # (e.g. wrong signature) — as long as a valid refresh_token exists.
        if not self._auth_service.refresh():
            self._auth_service.logout()
            return

        # Retry with the refreshed token
        assert self._auth_service.auth_info is not None
        request.headers["Authorization"] = (
            f"Bearer {self._auth_service.auth_info.jwt_token}"
        )
        yield request

    def _is_token_expiring(self, offset_seconds: int = 60) -> bool:
        """True if the stored JWT expires within `offset_seconds`."""
        auth = self._auth_service.auth_info
        if auth is None or auth.token_expiry is None:
            return False
        return auth.token_expiry < time.time() + offset_seconds

    @staticmethod
    def _is_expired_token_response(response: httpx.Response) -> bool:
        """True if the 401 response detail indicates an expired token."""
        try:
            detail = response.json().get("detail", "")
        except Exception:
            detail = response.text
        return isinstance(detail, str) and _EXPIRED_TOKEN_MARKER in detail


def get_api_client(auth_service: Optional[RuntimeAuthService] = None) -> ApiClient:
    api_base_url = active().runtime_config.api_base_url
    if not api_base_url:
        raise RuntimeError(
            "api_base_url is not configured in the runtime configuration"
        )

    if auth_service is None:
        auth_service = RuntimeAuthService(run_context=active())
        auth_service.authenticate()

    headers = {"User-Agent": f"dlt-runtime-cli/{__version__}"}

    return ApiClient(
        base_url=api_base_url,
        verify_ssl=False,
        headers=headers,
        raise_on_unexpected_status=True,
        httpx_args={"auth": RuntimeAuth(auth_service)},
    )
