import os
import time
from dataclasses import dataclass, field
from typing import Generator, Optional, Union
from uuid import UUID

import httpx
import jwt
from dlt._workspace._workspace_context import WorkspaceRunContext, active
from dlt._workspace.cli import echo as fmt
from dlt._workspace.cli.config_toml_writer import WritableConfigValue, write_values
from dlt._workspace.exceptions import WorkspaceRunContextNotAvailable
from dlt.common.configuration.providers.toml import (
    ConfigTomlProvider,
    SecretsTomlProvider,
)
from dlt.common.configuration.specs.pluggable_run_context import RunContextBase
from dlt.common.configuration.specs.runtime_configuration import RuntimeConfiguration
from jwt.exceptions import PyJWTError

from dlt_runtime._telemetry import DEVICE_ID_HEADER, get_telemetry_device_id
from dlt_runtime.urls import normalize_api_base_url
from dlt_runtime.version import __version__

from dlt_runtime.exceptions import (
    ApiKeyInvalid,
    OrgRegionRequired,
    RuntimeNotAuthenticated,
    RuntimeOperationNotAuthorized,
    exception_from_response,
    handle_client_exceptions,
)
from dlt_runtime.runtime_clients.api.api.me import me
from dlt_runtime.runtime_clients.api.api.organizations import set_organization_region
from dlt_runtime.runtime_clients.api.api.workspaces import create_workspace
from dlt_runtime.runtime_clients.api.client import Client as ApiClient
from dlt_runtime.runtime_clients.api.models.create_workspace_response_409 import (
    CreateWorkspaceResponse409,
)
from dlt_runtime.runtime_clients.api.models.me_response import MeResponse
from dlt_runtime.runtime_clients.api.models.organization_membership_response import (
    OrganizationMembershipResponse,
)
from dlt_runtime.runtime_clients.api.models.organization_response import (
    OrganizationResponse,
)
from dlt_runtime.runtime_clients.api.models.set_organization_region_request import (
    SetOrganizationRegionRequest,
)
from dlt_runtime.runtime_clients.api.models.workspace_create_request import (
    WorkspaceCreateRequest,
)
from dlt_runtime.runtime_clients.api.models.workspace_response import WorkspaceResponse
from dlt_runtime.runtime_clients.api.models.workspace_with_membership_response import (
    WorkspaceWithMembershipResponse,
)
from dlt_runtime.runtime_clients.auth.api.default import (
    create_session_swap_code as swap_code_api,
)
from dlt_runtime.runtime_clients.auth.api.default import refresh as refresh_api
from dlt_runtime.runtime_clients.auth.client import Client as AuthClient
from dlt_runtime.runtime_clients.auth.models.refresh_request import RefreshRequest
from dlt_runtime.runtime_clients.auth.models.refresh_response import RefreshResponse
from dlt_runtime.runtime_clients.auth.models.swap_code_request import SwapCodeRequest
from dlt_runtime.runtime_clients.auth.models.swap_code_response import SwapCodeResponse
from dlt_runtime.typing import OrganizationInfo, UserInfo, WorkspaceInfo


def _tls_verify() -> bool:
    """TLS verification toggle for httpx clients targeting the data plane."""

    return os.environ.get("DLT_RUNTIME_INSECURE", "").strip().lower() not in {
        "1",
        "true",
        "yes",
    }


@dataclass
class AuthInfo:
    user_id: str
    email: str
    jwt_token: str
    token_expiry: Optional[float] = None
    feature_flags: list[str] = field(default_factory=list)


class RuntimeAuthService:
    """
    Implements login, logout and auth check internals

    Authentication is performed based on the JWT token stored in the global secrets. On top of that,
    authorization uses organization and workspace id stored in the local config. For that, depending on the usage,
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

    def has_workspace(self) -> bool:
        """True iff a workspace is currently connected (probes `workspace_id`)."""
        try:
            _ = self.workspace_id
            return True
        except RuntimeOperationNotAuthorized:
            return False

    def has_api_key(self) -> bool:
        """True iff an API key is configured."""
        return bool(self.workspace_run_context.runtime_config.api_key)

    @property
    def organization_id(self) -> Optional[str]:
        """Return the organization_id pinned in `.dlt/config.toml`, or None."""
        # Org pinning is write-once: `workspace connect` filters
        # listings and creates new workspaces in this org, but the CLI never
        # mutates this value — user removes it manually to switch orgs.
        return self.workspace_run_context.runtime_config.organization_id

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
        auth_info = self._save_token_and_refresh_token(token, refresh_token)
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

        # Persist the new JWT and refresh token in a single file write so
        # a crash or concurrent process can never observe a state where the
        # JWT was updated but the refresh token still holds the old (now
        # server-side revoked) value — that stale token would trigger theft
        # detection on the next refresh attempt.
        self._save_token_and_refresh_token(
            response.parsed.jwt, response.parsed.refresh_token
        )
        return True

    def mint_swap_code(self) -> Optional[str]:
        """Mint a single-use code that logs the web app into this CLI session.

        Returns None when no refresh token is stored or the auth service
        rejects it — callers fall back to opening the plain URL.
        """
        stored_refresh_token = self._read_refresh_token()
        if not stored_refresh_token:
            return None
        try:
            response = swap_code_api.sync_detailed(
                client=get_auth_client(),
                body=SwapCodeRequest(refresh_token=stored_refresh_token),
            )
        except Exception:
            return None
        if isinstance(response.parsed, SwapCodeResponse):
            return response.parsed.swap_code
        return None

    def _write_runtime_config(self, **values: Optional[str]) -> None:
        """Persist `[runtime]` keys to .dlt/config.toml and mirror onto the
        cached `runtime_config` so reads later in this process see the change.

        Pass None as a value to delete the key (relies on dlt-core
        `set_value(key, None, ...)` semantics — TOML can't represent None).
        """
        provider = ConfigTomlProvider(self.workspace_run_context.settings_dir)
        cfg = self.workspace_run_context.runtime_config
        for key, val in values.items():
            provider.set_value(key, val, None, RuntimeConfiguration.__section__)
            setattr(cfg, key, val)
        provider.write_toml()
        if "workspace_id" in values:
            self._local_workspace_id = values["workspace_id"]

    def write_connection(self, workspace_id: str, organization_id: str) -> None:
        """Persist workspace_id (always) and organization_id (write-once) to [runtime]."""
        kw: dict[str, Optional[str]] = {"workspace_id": str(workspace_id)}
        # Skip org_id if a value is already present — switching orgs requires
        # the user to remove the line manually.
        existing_org_id = self.workspace_run_context.runtime_config.organization_id
        if existing_org_id is None:
            kw["organization_id"] = str(organization_id)
        else:
            # invariant: organization associated with workspace cannot differ from
            # the one pinned in config.toml.
            assert organization_id == existing_org_id, (
                f"organization_id mismatch: caller passed {organization_id!r}, "
                f"pinned is {existing_org_id!r}"
            )

        self._write_runtime_config(**kw)

    def write_workspace_name(self, name: str) -> None:
        """Persist the workspace name to `.dlt/config.toml` `[workspace.settings]`."""
        local_toml_config = ConfigTomlProvider(self.workspace_run_context.settings_dir)
        local_toml_config.set_value("name", name, None, "workspace", "settings")
        local_toml_config.write_toml()

    def _read_token(self) -> AuthInfo:
        config = self.workspace_run_context.runtime_config
        if not config.auth_token:
            raise RuntimeNotAuthenticated("No token found")
        self.auth_info = self._validate_and_decode_user_jwt(config.auth_token)
        return self.auth_info

    def _save_token_and_refresh_token(
        self, token: str, refresh_token: Optional[str] = None
    ) -> AuthInfo:
        """Persist the JWT (and optionally the refresh token) in a single
        atomic file write.

        Writing both values in one shot prevents a crash or concurrent
        process from observing a state where the JWT was updated but the
        refresh token still holds the old (server-side revoked) value.
        That stale refresh token would trigger theft detection on the next
        refresh attempt, revoking *all* user tokens.
        """
        self.auth_info = self._validate_and_decode_user_jwt(token)
        values = [
            WritableConfigValue(
                "auth_token", str, token, (RuntimeConfiguration.__section__,)
            )
        ]
        if refresh_token is not None:
            values.append(
                WritableConfigValue(
                    "refresh_token",
                    str,
                    refresh_token,
                    (RuntimeConfiguration.__section__,),
                )
            )
        # write global secrets — single read-modify-write cycle
        global_path = self.run_context.global_dir
        os.makedirs(global_path, exist_ok=True)
        secrets = SecretsTomlProvider(settings_dir=global_path)
        write_values(secrets._config_toml, values, overwrite_existing=True)
        secrets.write_toml()
        return self.auth_info

    def fetch_user_info(self) -> UserInfo:
        """Fetch user info from /me, which self-bootstraps the caller's org on first call."""
        error_message = "Failed to get your user info from the dltHub API. Run 'dlthub login' or update your API key"
        client = get_api_client(self)
        with handle_client_exceptions(error_message):
            me_response = me.sync_detailed(client=client)

        if isinstance(me_response.parsed, MeResponse):
            return self._me_response_to_user_info(me_response.parsed)

        raise exception_from_response(error_message, me_response)

    def _me_response_to_user_info(self, parsed: MeResponse) -> UserInfo:
        last_workspace = (
            parsed.last_workspace
            if isinstance(parsed.last_workspace, WorkspaceResponse)
            else None
        )

        workspaces_list: list[WorkspaceInfo]
        if isinstance(parsed.workspaces, list):
            workspaces_list = [
                self._convert_workspace_membership(wm) for wm in parsed.workspaces
            ]
        elif last_workspace is not None:
            # Fallback: just the last workspace if workspaces not returned.
            # Assume owner role since this is the user's own default workspace.
            ws_info = self._convert_workspace(last_workspace)
            ws_info["role"] = "owner"
            workspaces_list = [ws_info]
        else:
            workspaces_list = []

        assert isinstance(parsed.organizations, list), (
            "MeResponse.organizations missing — server contract requires it"
        )
        organizations_list = [
            self._convert_organization_membership(om) for om in parsed.organizations
        ]

        user_info: UserInfo = {
            "email": parsed.email,
            "user_id": str(parsed.user_id),
            "identity_id": str(parsed.identity_id),
            "default_organization_id": str(parsed.primary_organization.id),
            "workspaces": workspaces_list,
            "organizations": organizations_list,
        }
        if last_workspace is not None:
            user_info["default_workspace"] = self._convert_workspace(last_workspace)
        self._validate_local_workspace(user_info)
        return user_info

    def _validate_local_workspace(self, user_info: UserInfo) -> None:
        """Wipe stale workspace_id from .dlt/config.toml."""
        # Runs after every successful login / token refresh that hits `/me`.
        # `organization_id` is write-once and the user removes it manually to
        # switch orgs — the CLI never overwrites it (matches `write_connection`).
        cfg = self.workspace_run_context.runtime_config
        accessible_ws = {ws["id"] for ws in user_info["workspaces"]}
        if not cfg.workspace_id or cfg.workspace_id in accessible_ws:
            return
        self._write_runtime_config(workspace_id=None)
        fmt.warning(
            "Local workspace in `.dlt/config.toml` is no longer accessible —"
            " cleared. Reconnect with `dlthub workspace connect`."
        )

    def _convert_workspace(self, workspace: WorkspaceResponse) -> WorkspaceInfo:
        from dlt_runtime.runtime_clients.api.types import Unset

        info: WorkspaceInfo = {
            "id": str(workspace.id),
            "name": workspace.name,
        }
        if not isinstance(workspace.description, Unset) and workspace.description:
            info["description"] = workspace.description
        if not isinstance(workspace.predefined_profiles, Unset):
            info["predefined_profiles"] = dict(
                workspace.predefined_profiles.additional_properties
            )
        return info

    def _convert_workspace_membership(
        self, wm: WorkspaceWithMembershipResponse
    ) -> WorkspaceInfo:
        """Convert a WorkspaceWithMembershipResponse to WorkspaceInfo."""
        info = self._convert_workspace(wm.workspace)
        info["role"] = wm.role
        info["organization_id"] = str(wm.organization.id)
        info["organization_name"] = wm.organization.name
        return info

    def _convert_organization_membership(
        self, om: OrganizationMembershipResponse
    ) -> OrganizationInfo:
        return {
            "id": str(om.organization.id),
            "name": om.organization.name,
            "role": om.role,
            "active": om.active,
        }

    def create_new_workspace(
        self,
        user_info: UserInfo,
        name: str,
        description: Optional[str],
        *,
        organization_id: Optional[str] = None,
    ) -> str:
        """Create a new workspace via the API."""
        # `organization_id` overrides the user's default org so a pinned-org
        # `workspace connect` keeps creates within that org.
        org_id = organization_id or user_info["default_organization_id"]
        with handle_client_exceptions("Failed to create workspace"):
            create_result = create_workspace.sync_detailed(
                organization_id=UUID(org_id),
                client=get_api_client(self),
                body=WorkspaceCreateRequest(name=name, description=description),
            )
        if isinstance(create_result.parsed, WorkspaceResponse):
            return str(create_result.parsed.id)
        if isinstance(create_result.parsed, CreateWorkspaceResponse409):
            raise OrgRegionRequired()
        raise exception_from_response("Failed to create workspace", create_result)

    def set_organization_region(self, organization_id: str, dataplane_id: str) -> None:
        """Set the org's region (set-once). Raises on failure (e.g. already set)."""
        with handle_client_exceptions("Failed to set organization region"):
            result = set_organization_region.sync_detailed(
                organization_id=UUID(organization_id),
                client=get_api_client(self),
                body=SetOrganizationRegionRequest(dataplane_id=dataplane_id),
            )
        if not isinstance(result.parsed, OrganizationResponse):
            raise exception_from_response("Failed to set organization region", result)

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

    def _validate_and_decode_user_jwt(self, token: Union[str, bytes]) -> AuthInfo:
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
                "Your authentication token has expired. Please run 'dlthub login' to re-authenticate"
            )

        raw_flags = payload.get("feature_flags") or []
        feature_flags = [flag for flag in raw_flags if isinstance(flag, str)]

        try:
            auth_info = AuthInfo(
                jwt_token=token.decode("utf-8"),
                email=payload["email"],
                user_id=payload["sub"],
                token_expiry=token_expiry,
                feature_flags=feature_flags,
            )
        except (KeyError, TypeError) as e:
            raise RuntimeNotAuthenticated("Failed to validate JWT payload") from e

        return auth_info


def get_auth_client(*, include_device_id: bool = False) -> AuthClient:
    api_base_url = active().runtime_config.api_base_url
    if not api_base_url:
        raise RuntimeError(
            "api_base_url is not configured in the runtime configuration"
        )
    api_base_url = normalize_api_base_url(api_base_url)
    headers = {"User-Agent": f"dlt-runtime-cli/{__version__}"}
    if include_device_id:
        device_id = get_telemetry_device_id()
        if device_id:
            headers[DEVICE_ID_HEADER] = device_id
    return AuthClient(
        base_url=api_base_url,
        verify_ssl=_tls_verify(),
        headers=headers,
        raise_on_unexpected_status=True,
    )


# Must match the detail string returned by the API auth middleware for expired tokens.
_EXPIRED_TOKEN_MARKER = "Token expired"


class JwtAuth(httpx.Auth):
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


class ApiKeyAuth(httpx.Auth):
    """httpx Auth that sets an API key as the Bearer token and surfaces
    an ApiKeyInvalid error on 401 without a refresh path.
    """

    requires_response_body = True

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        request.headers["Authorization"] = f"Bearer {self._api_key}"
        response = yield request
        if response.status_code == 401:
            try:
                detail = response.json().get("detail", "")
            except Exception:
                detail = response.text
            raise ApiKeyInvalid(
                detail=detail if isinstance(detail, str) and detail else None
            )


def get_api_client(auth_service: Optional[RuntimeAuthService] = None) -> ApiClient:
    config = active().runtime_config
    if not config.api_base_url:
        raise RuntimeError(
            "api_base_url is not configured in the runtime configuration"
        )
    api_base_url = normalize_api_base_url(config.api_base_url)

    headers = {"User-Agent": f"dlt-runtime-cli/{__version__}"}

    if config.api_key:
        return ApiClient(
            base_url=api_base_url,
            verify_ssl=_tls_verify(),
            headers=headers,
            raise_on_unexpected_status=True,
            httpx_args={"auth": ApiKeyAuth(config.api_key)},
        )

    if auth_service is None:
        auth_service = RuntimeAuthService(run_context=active())
        auth_service.authenticate()

    return ApiClient(
        base_url=api_base_url,
        verify_ssl=_tls_verify(),
        headers=headers,
        raise_on_unexpected_status=True,
        httpx_args={"auth": JwtAuth(auth_service)},
    )
