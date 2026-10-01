# Python internals
import os
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union

# Other libraries
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

# Current package
from dlt_runtime._telemetry import DEVICE_ID_HEADER, get_telemetry_device_id
from dlt_runtime.exceptions import (
    ApiKeyInvalid,
    OrgRegionRequired,
    RuntimeClientException,
    RuntimeNotAuthenticated,
    RuntimeOperationNotAuthorized,
    handle_client_exceptions,
)
from dlt_runtime.strings import API_KEY_UNRECOGNIZED
from dlt_runtime.typing import CallerInfo, WorkspaceInfo
from dlt_runtime.urls import normalize_api_base_url
from dlt_runtime.version import USER_AGENT
from dlthub_sdk import (
    Organization,
    OrganizationCaller,
    Runtime,
    Sync,
    Workspace,
    connect,
)
from dlthub_sdk._auth import AuthTransport, decode_token
from dlthub_sdk.errors import (
    Conflict as SdkConflict,
    NotAuthenticated as SdkNotAuthenticated,
)

PERSONAL_API_KEY_PREFIX = "dlt_u_"
WORKSPACE_API_KEY_PREFIX = "dlt_sa_"


class AuthenticationMethod(str, Enum):
    """How the CLI authenticates. API keys are static: no JWT, no refresh token."""

    JWT = "jwt"
    API_KEY = "api_key"


class PrincipalKind(str, Enum):
    """Who the stored credential acts as.

    Derived from the credential the CLI holds, never read off a response, so it
    is the CLI's own vocabulary rather than the platform's.
    """

    HUMAN = "human"
    SERVICE_ACCOUNT = "service_account"


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


class CliSession:
    """Who the caller is, what proves it, and which workspace they are on.

    One per command. Owns the credential on disk — the JWT and refresh token in
    the global secrets, the workspace and organization pinned in the local
    config — so the SDK never touches the filesystem. Most reads need a
    `WorkspaceRunContext`; `has_workspace` probes for one.
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

    def authentication_method(self) -> AuthenticationMethod:
        if self.workspace_run_context.runtime_config.api_key:
            return AuthenticationMethod.API_KEY
        return AuthenticationMethod.JWT

    def principal_kind(self) -> PrincipalKind:
        """Who the credential acts as. Raises on an API key with an unknown prefix."""
        api_key = self.workspace_run_context.runtime_config.api_key
        if api_key is None or api_key.startswith(PERSONAL_API_KEY_PREFIX):
            return PrincipalKind.HUMAN
        if api_key.startswith(WORKSPACE_API_KEY_PREFIX):
            return PrincipalKind.SERVICE_ACCOUNT
        raise ApiKeyInvalid(API_KEY_UNRECOGNIZED)

    @property
    def organization_id(self) -> Optional[str]:
        """Return the pinned organization_id from the dlt config, or None."""
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

    def login(self, token: str, refresh_token: Optional[str] = None) -> AuthInfo:
        auth_info = self._save_token_and_refresh_token(token, refresh_token)
        self._bootstrap_caller()
        return auth_info

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

        # A rejected token is an answer, not a failure; anything else (5xx,
        # network) propagates to the caller.
        tokens = get_auth_transport().refresh(refresh_token=stored_refresh_token)
        if tokens is None:
            return False

        # Persist the new JWT and refresh token in a single file write so
        # a crash or concurrent process can never observe a state where the
        # JWT was updated but the refresh token still holds the old (now
        # server-side revoked) value — that stale token would trigger theft
        # detection on the next refresh attempt.
        self._save_token_and_refresh_token(tokens.access_token, tokens.refresh_token)
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
            return get_auth_transport().create_session_swap_code(
                refresh_token=stored_refresh_token
            )
        except Exception:
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

    def _bootstrap_caller(self) -> None:
        """Call /user at login to self-bootstrap the caller's org, then validate local state."""
        error_message = "Failed to get your user info from the dltHub API. Run 'dlthub login' or update your API key"
        # Only a user token reaches `/user`; login always holds one by here.
        with handle_client_exceptions(error_message):
            get_sdk_runtime(self).me()

        self.fetch_caller_info()

    def fetch_caller_info(self) -> CallerInfo:
        """Workspaces and organizations of the caller, via org endpoints available to all principals."""
        error_message = "Failed to get workspace info from the dltHub API. Run 'dlthub login' or update your API key"
        with handle_client_exceptions(error_message):
            runtime = get_sdk_runtime(self)
            # One `me` per organization; the SDK keeps the fan-out visible.
            callers = [(org, org.me()) for org in runtime.organizations.list()]

        caller_info: CallerInfo = {
            "workspaces": [
                ws
                for org, caller in callers
                for ws in self._caller_to_workspace_infos(org, caller)
            ],
            # list_organizations only returns active memberships.
            "organizations": [
                {
                    "id": org.id,
                    "name": org.name,
                    "role": caller.role,
                    "active": True,
                }
                for org, caller in callers
            ],
        }
        if callers:
            first = callers[0][1]
            caller_info["identity"] = {
                "email": first.email,
                "user_id": first.user_id,
                "identity_id": first.identity_id,
            }
        if self.principal_kind() is PrincipalKind.HUMAN:
            self._validate_local_workspace(caller_info)
        return caller_info

    def _caller_to_workspace_infos(
        self, org: "Organization[Sync]", caller: "OrganizationCaller[Sync]"
    ) -> list[WorkspaceInfo]:
        """The caller's workspaces in one organization, each stamped with it."""
        workspaces = []
        for membership in caller.memberships:
            info = self._convert_workspace(membership.workspace)
            info["role"] = membership.role
            info["organization_id"] = org.id
            info["organization_name"] = org.name
            workspaces.append(info)
        return workspaces

    def _validate_local_workspace(self, caller_info: CallerInfo) -> None:
        """Wipe stale workspace_id from .dlt/config.toml."""
        # Runs on every human caller-info fetch; workspace-key pins are instead
        # validated explicitly by `workspace connect` (pin-mismatch errors).
        # `organization_id` is write-once and the user removes it manually to
        # switch orgs — the CLI never overwrites it (matches `write_connection`).
        cfg = self.workspace_run_context.runtime_config
        accessible_ws = {ws["id"] for ws in caller_info["workspaces"]}
        if not cfg.workspace_id or cfg.workspace_id in accessible_ws:
            return
        self._write_runtime_config(workspace_id=None)
        fmt.warning(
            "Local workspace in `.dlt/config.toml` is no longer accessible —"
            " cleared. Reconnect with `dlthub workspace connect`."
        )

    def _convert_workspace(self, workspace: "Workspace[Sync]") -> WorkspaceInfo:
        info: WorkspaceInfo = {
            "id": workspace.id,
            "name": workspace.name,
        }
        if workspace.description:
            info["description"] = workspace.description
        if workspace.predefined_profiles:
            info["predefined_profiles"] = dict(workspace.predefined_profiles)
        return info

    def create_new_workspace(
        self,
        name: str,
        description: Optional[str],
        *,
        organization_id: str,
    ) -> str:
        """Create a new workspace via the API."""
        try:
            with handle_client_exceptions("Failed to create workspace"):
                created = get_sdk_runtime(self).workspaces.create(
                    name=name,
                    description=description,
                    organization_id=organization_id,
                )
        except RuntimeClientException as e:
            # 409 means the organization has no region pinned yet.
            if isinstance(e.__cause__, SdkConflict):
                raise OrgRegionRequired() from e
            raise
        return created.id

    def set_organization_region(self, organization_id: str, dataplane_id: str) -> None:
        """Set the org's region (set-once). Raises on failure (e.g. already set)."""
        with handle_client_exceptions("Failed to set organization region"):
            runtime = get_sdk_runtime(self)
            runtime.organizations.get(id=organization_id).set_dataplane(
                dataplane_id=dataplane_id
            )

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
        return str(value) if value else None

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
        # The SDK reads the claims; the CLI owns the type callers recover on and
        # the wording of the remedy, which names a CLI command.
        try:
            claims = decode_token(token)
        except SdkNotAuthenticated as e:
            raise RuntimeNotAuthenticated(f"Failed to decode JWT: {e}") from e
        if claims.expires_at is not None and claims.expires_at < time.time():
            raise RuntimeNotAuthenticated(
                "Your authentication token has expired. Please run 'dlthub login' to re-authenticate"
            )
        raw = token.decode("utf-8") if isinstance(token, bytes) else token
        return AuthInfo(
            jwt_token=raw,
            email=claims.email,
            user_id=claims.user_id,
            token_expiry=claims.expires_at,
            feature_flags=list(claims.feature_flags),
        )


def get_auth_transport(*, include_device_id: bool = False) -> AuthTransport:
    """Build a transport for the configured auth service.

    Args:
        include_device_id: Send the telemetry device id, which the login flows
            do so a device can be recognised across attempts.

    Returns:
        A transport bound to the configured auth service.

    Raises:
        RuntimeError: No api_base_url is configured.
    """
    api_base_url = active().runtime_config.api_base_url
    if not api_base_url:
        raise RuntimeError(
            "api_base_url is not configured in the runtime configuration"
        )
    headers = {"User-Agent": USER_AGENT}
    if include_device_id:
        device_id = get_telemetry_device_id()
        if device_id:
            headers[DEVICE_ID_HEADER] = device_id
    return AuthTransport(
        normalize_api_base_url(api_base_url),
        headers=headers,
        verify_ssl=_tls_verify(),
    )


class _JwtCredentials:
    """The SDK's read of the stored user JWT, renewed against the stored grant.

    Args:
        session: Owner of the stored token and the refresh grant.
    """

    def __init__(self, session: "CliSession") -> None:
        self._session = session

    def token(self) -> str:
        """Return the JWT to send, renewing first if it is close to expiry.

        Returns:
            The bearer token, or an empty string when nothing is stored — the
            platform's 401 is a better error than one invented here.
        """
        auth = self._session.auth_info
        if auth is not None and self._is_expiring():
            try:
                self._session.refresh()
            except Exception:
                pass
        auth = self._session.auth_info
        return auth.jwt_token if auth is not None else ""

    def refreshed(self) -> Optional[str]:
        """Renew after the platform rejected the token, or give up and log out.

        Returns:
            A token to retry with, or ``None`` once there is nothing left to try.
        """
        # Renewed even right after a renewal: a 401 need not mean expiry, and
        # the SDK asks at most once per request, so this cannot loop.
        if not self._session.refresh():
            self._session.logout()
            return None
        auth = self._session.auth_info
        return auth.jwt_token if auth is not None else None

    def _is_expiring(self, offset_seconds: int = 60) -> bool:
        auth = self._session.auth_info
        if auth is None or auth.token_expiry is None:
            return False
        return auth.token_expiry < time.time() + offset_seconds


class _ApiKeyCredentials:
    """An API key, which never rotates.

    Args:
        api_key: The configured key.
    """

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def token(self) -> str:
        """Return the key.

        Returns:
            The bearer token.
        """
        return self._api_key

    def refreshed(self) -> Optional[str]:
        """Give up: there is no grant to renew an API key with.

        Returns:
            Always ``None``, which the SDK turns into ``NotAuthenticated``.
        """
        return None


def get_sdk_runtime(session: Optional[CliSession] = None) -> Runtime[Sync]:
    """Build the SDK client the CLI reads the platform through.

    The only client the CLI reads the platform through.

    Args:
        session: Owner of the stored token. Built and authenticated here
            when the caller has none.

    Returns:
        A blocking SDK runtime, scoped to the pinned organization when there is one.

    Raises:
        RuntimeError: No `api_base_url` in the runtime configuration.
    """
    config = active().runtime_config
    if not config.api_base_url:
        raise RuntimeError(
            "api_base_url is not configured in the runtime configuration"
        )
    credentials: Union[_JwtCredentials, _ApiKeyCredentials]
    if config.api_key:
        credentials = _ApiKeyCredentials(config.api_key)
    else:
        if session is None:
            session = CliSession(run_context=active())
            session.authenticate()
        credentials = _JwtCredentials(session)
    return connect(
        credentials=credentials,
        base_url=normalize_api_base_url(config.api_base_url),
        # Read off the config, not the auth service: the pin is the same either
        # way, and an api key reaches here without one.
        organization_id=config.organization_id,
        verify_ssl=_tls_verify(),
        headers={"User-Agent": USER_AGENT},
    )
