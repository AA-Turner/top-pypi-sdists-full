import os
from dataclasses import dataclass
from typing import Any, Optional, Union, List
from uuid import UUID

import jose.jwt as jose_jwt
from dlt._workspace._workspace_context import WorkspaceRunContext, active
from dlt._workspace.cli.config_toml_writer import WritableConfigValue, write_values
from dlt._workspace.exceptions import WorkspaceRunContextNotAvailable
from dlt.common.configuration.providers.toml import (
    ConfigTomlProvider,
    SecretsTomlProvider,
)
from dlt.common.configuration.specs.pluggable_run_context import RunContextBase
from dlt.common.configuration.specs.runtime_configuration import RuntimeConfiguration
from jose.exceptions import ExpiredSignatureError, JOSEError

from dlt_runtime.version import __version__

from dlt_runtime.exceptions import (
    LocalWorkspaceIdNotSet,
    RuntimeNotAuthenticated,
    RuntimeOperationNotAuthorized,
    WorkspaceIdMismatch,
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
from dlt_runtime.runtime_clients.auth.client import Client as AuthClient


@dataclass
class AuthInfo:
    user_id: str
    email: str
    jwt_token: str


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
    _user_info: Optional[UserInfo] = None

    _run_context: RunContextBase
    _local_workspace_id: Optional[str] = None
    _remote_workspace_ids: Optional[List[str]] = None

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
        if (
            not self._remote_workspace_ids
            or not self._local_workspace_id
            or self._local_workspace_id not in self._remote_workspace_ids
        ):
            raise RuntimeOperationNotAuthorized()
        return self._local_workspace_id

    @property
    def user_info(self) -> UserInfo:
        if self._user_info is None:
            raise RuntimeNotAuthenticated("No user info found")
        return self._user_info

    def authenticate(self) -> AuthInfo:
        return self._read_token()

    def login(self, token: str) -> AuthInfo:
        auth_info = self._save_token(token)
        self._fetch_user_info()
        return auth_info

    def logout(self) -> None:
        self._delete_token()
        self._remote_workspace_ids = None
        self._user_info = None

    def connect(self) -> str:
        # Ensuring workspace id is set and is one of the remote workspace ids
        self._fetch_user_info()

        self._local_workspace_id = (
            self.workspace_run_context.runtime_config.workspace_id
        )

        if not self._local_workspace_id:
            remote_ids = (
                ", ".join(self._remote_workspace_ids)
                if self._remote_workspace_ids
                else "none"
            )
            raise LocalWorkspaceIdNotSet(remote_ids)
        elif (
            self._remote_workspace_ids
            and self._local_workspace_id not in self._remote_workspace_ids
        ):
            remote_ids = ", ".join(self._remote_workspace_ids)
            raise WorkspaceIdMismatch(self._local_workspace_id, remote_ids)

        return self.workspace_id

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

    def _fetch_user_info(self) -> None:
        """Fetch user info including all accessible workspaces from /me endpoint."""
        error_message = "Failed to get your user info from the Runtime API. Try logging out and in again"
        client = get_api_client(self)
        with handle_client_exceptions(error_message, auth_service=self):
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

            self._user_info = UserInfo(
                email=parsed.email,
                user_id=parsed.user_id,
                identity_id=parsed.identity_id,
                default_organization_id=parsed.primary_organization.id,
                default_workspace=self._convert_workspace(parsed.last_workspace),
                workspaces=workspaces_list,
            )
            self._remote_workspace_ids = [
                str(workspace.id) for workspace in self.user_info.workspaces
            ]
        else:
            # Auto-delete invalid token on 401 so user can re-login without explicit logout
            if me_response.status_code == 401:
                try:
                    self.logout()
                except Exception:
                    pass
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

    def _convert_workspace_membership(self, wm: Any) -> WorkspaceInfo:
        """Convert a WorkspaceWithMembershipResponse to WorkspaceInfo."""
        info = self._convert_workspace(wm.workspace)
        info.role = wm.role
        return info

    def create_new_workspace(
        self,
        name: str,
        description: Optional[str],
    ) -> str:
        """Create a new workspace via the API."""
        with handle_client_exceptions("Failed to create workspace"):
            create_result = create_workspace.sync_detailed(
                organization_id=self.user_info.default_organization_id,
                client=get_api_client(self),
                body=WorkspaceCreateRequest(name=name, description=description),
            )
        if isinstance(create_result.parsed, WorkspaceResponse):
            # Updating user info to store a newly created workspace info as well
            self._fetch_user_info()
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

    def _validate_and_decode_jwt(self, token: Union[str, bytes]) -> AuthInfo:
        if isinstance(token, str):
            token = token.encode("utf-8")
        try:
            payload = jose_jwt.decode(
                token, key="", audience="cli", options={"verify_signature": False}
            )
        except ExpiredSignatureError:
            raise RuntimeNotAuthenticated(
                "Your authentication token has expired. Please run 'dlt runtime login' to re-authenticate"
            )
        except JOSEError as e:
            raise RuntimeNotAuthenticated("Failed to decode JWT") from e

        try:
            auth_info = AuthInfo(
                jwt_token=token.decode("utf-8"),
                email=payload["email"],
                user_id=payload["sub"],
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
    if auth_service.auth_info:
        headers["Authorization"] = f"Bearer {auth_service.auth_info.jwt_token}"

    return ApiClient(
        base_url=api_base_url,
        verify_ssl=False,
        headers=headers,
        raise_on_unexpected_status=True,
    )
