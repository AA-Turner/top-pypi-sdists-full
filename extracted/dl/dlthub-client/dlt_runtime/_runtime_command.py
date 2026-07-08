# Python internals
import base64
import hashlib
import os
import platform
import secrets
import sys
import time
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

import yaml
from typing import TYPE_CHECKING, Any, Callable, Optional, Set, Union, cast
from uuid import UUID

# Other libraries
from dlt._workspace._workspace_context import active
from dlt._workspace.cli import echo as fmt
from dlt._workspace.cli.exceptions import CliCommandInnerException
from dlt._workspace.cli.utils import open_url, track_command as dlt_track_command
from dlt._workspace.deployment import DEFAULT_DEPLOYMENT_MODULE
from dlt._workspace.deployment._trigger_helpers import is_selector


from dlt_runtime.exceptions import (
    NoRunnableRun,
    OrgRegionRequired,
    RuntimeClientException,
    RuntimeNotAuthenticated,
    WorkspaceNotFound,
    exception_from_response,
    handle_client_exceptions,
)
from dlt_runtime.runtime import (
    AuthInfo,
    RuntimeAuthService,
    get_api_client,
    get_auth_client,
)
from dlt_runtime.runtime_clients.api.api.runs import (
    bulk_cancel_runs,
    cancel_run,
    get_run,
)
from dlt_runtime.runtime_clients.api.models.bulk_cancel_request import (
    BulkCancelRequest,
)
from dlt_runtime.runtime_clients.api.api.scripts import (
    disable_public_url,
    enable_public_url,
    get_script,
    trigger_jobs,
)
from dlt_runtime.runtime_clients.api.models.trigger_jobs_request import (
    TriggerJobsRequest,
)
from dlt_runtime.runtime_clients.api.client import Client as ApiClient
from dlt_runtime.runtime_clients.api.models.run_status import RunStatus
from dlt_runtime.runtime_clients.api.types import UNSET, Unset
from dlt_runtime.runtime_clients.auth.api.workos import (
    workos_auth_code_exchange,
    workos_auth_code_start,
    workos_device_flow_complete,
    workos_device_flow_start,
)
from dlt_runtime.runtime_clients.auth.errors import (
    UnexpectedStatus as AuthUnexpectedStatus,
)

if TYPE_CHECKING:
    from dlt_runtime.runtime_clients.api.models.triggered_job import TriggeredJob

from dlt_runtime._loopback_pages import (
    _LOOPBACK_ERROR_HTML,
    _LOOPBACK_SUCCESS_HTML,
)
from dlt_runtime._runtime_command_helpers import (  # noqa: F401
    _active_org_count,
    _check_org_arg_matches_pin,
    _fetch_available_regions,
    _default_dashboard_manifest_bundle,
    _do_deploy_manifest,
    _do_sync_configuration,
    _do_sync_deployment,
    _ensure_profile_warning,
    _fetch_configuration_info,
    _fetch_configurations,
    _fetch_deployment_info,
    _fetch_deployments,
    _fetch_job_info,
    _fetch_job_run_info,
    _fetch_jobs,
    _fetch_run_detail,
    _fetch_runs,
    _fetch_runtime_info,
    _fetch_workspaces,
    _flatten_owned,
    _generate_local_manifest,
    _get_latest_run,
    _get_workspace_name,
    _get_workspace_org_name,
    _group_workspaces_by_org,
    _iter_run_log_stream,
    _iter_run_logs_historical,
    _org_id_to_persist,
    _org_label,
    _preprocess_run_output,
    _raise_cross_org,
    _resolve_dataplane_logs_endpoint,
    _resolve_effective_org_id,
    _resolve_job_ref_from_server,
    _resolve_run_id_by_number,
    _resolve_selectors_to_scripts,
    _resolve_trigger_selectors,
    _resolve_workspace_id,
    _resolve_workspace_name,
    _scope_user_info_to_org,
    _sole_active_org_id,
    _tls_verify,
    _to_uuid,
    _validate_org_id,
    _validate_pinned_org_id,
    requires_login,
    requires_workspace,
)
from dlt._workspace.deployment._run_helpers import (
    promote_deployment_arg,
    resolve_selector,
    select_single_job,
    warn_missing_profiles,
)
from dlt._workspace.deployment._run_views import pick_one_job
from dlt._workspace.deployment._trigger_helpers import humanize_trigger
from dlt._workspace.deployment.exceptions import AmbiguousJobSelector
from dlt._workspace.deployment.typing import TTrigger
from dlt_runtime.typing import (
    ConnectedWorkspaceInfo,
    CreateInOrgChoice,
    DeviceFlowStartResult,
    LoginResult,
    RuntimeRunBannerInfo,
    SyncLoggingLevel,
    SyncResult,
    TriggerSkipInfo,
    TriggerStatus,
    UserInfo,
    WorkspaceInfo,
)
from dlt_runtime import urls
from dlt_runtime.strings import (
    LOGIN_CANCELLED_RESUME_HINT,
    WORKSPACE_CONNECT_CREATE_DECLINED,
    WORKSPACE_CONNECT_REQUIRES_NAME_FOR_API_KEY,
    WORKSPACE_CREATE_REQUIRES_NAME,
    WORKSPACE_NAME_ALREADY_EXISTS,
    WORKSPACE_NAME_NOT_FOUND,
)
from dlt_runtime._runtime_command_views import (
    _open_login_page,
    format_job_selector,
    format_run_status,
    _print_device_flow_interactive,
    _print_device_flow_start,
    _print_loopback_login,
    _print_waiting_for_auth,
    _print_login_result,
    _print_org_groups_non_interactive,
    _print_runtime_info,
    _print_run_banner,
    _print_show_url,
    _print_sync_result,
    _print_workspace_connected,
    _prompt_workspace_selection,
    _prompt_new_workspace,
    _prompt_region_selection,
    _prompt_create_missing_workspace_in_org,
    _print_workspaces,
    _print_job_run_info,
    _print_runs,
    _print_deployments,
    _print_deployment_info,
    _print_configurations,
    _print_configuration_info,
    _print_jobs,
    _print_job_info,
    _print_deploy_result,
    _print_bulk_cancel_result,
    _print_trigger_skip,
    _print_run_final_status,
    FAILED_RUN_STATUSES,
)


def _stream_run_logs(
    run_id: UUID,
    *,
    follow: bool = True,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    """Display streamed logs from the run stream endpoint using SSE."""
    try:
        for level, message in _iter_run_log_stream(
            run_id, follow=follow, auth_service=auth_service, api_client=api_client
        ):
            if level == "log":
                fmt.echo(message)
            elif level == "warning":
                fmt.warning(message)
            elif level == "error":
                fmt.error(message)
    except KeyboardInterrupt:
        fmt.echo("\nLog streaming interrupted.")


def _show_final_run_status(
    run_id: UUID,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    """Fetch + render the run's current status after the follow loop exits.

    Exits the process with code 1 when the run finished in FAILED or CANCELLED;
    non-terminal statuses (after Ctrl+C / stream errors) are printed as-is and
    do not affect the exit code.
    """
    run = _fetch_run_detail(run_id, auth_service=auth_service, api_client=api_client)
    _print_run_final_status(run)
    if run.status in FAILED_RUN_STATUSES:
        sys.exit(1)


track_command = partial(dlt_track_command, "runtime", track_before=False)


def _start_device_flow() -> DeviceFlowStartResult:
    """Start the OAuth device flow without blocking. No browser, no polling."""
    client = get_auth_client()
    with handle_client_exceptions("Login failed. Error calling the dltHub API"):
        login_request = workos_device_flow_start.sync_detailed(client=client)
    if not isinstance(
        login_request.parsed, workos_device_flow_start.WorkosDeviceFlowStartResponse
    ):
        raise exception_from_response("Failed to start login", login_request)
    return DeviceFlowStartResult(
        verification_uri=login_request.parsed.verification_uri,
        verification_uri_complete=login_request.parsed.verification_uri_complete,
        user_code=login_request.parsed.user_code,
        device_code=login_request.parsed.device_code,
        interval=login_request.parsed.interval,
    )


def _cancel_login_with_resume_hint(device_code: str) -> None:
    """Print the `--resume` hint and exit 130; shared by interactive prompt and poll."""
    fmt.echo(LOGIN_CANCELLED_RESUME_HINT.format(device_code=device_code))
    sys.exit(130)


def _poll_device_flow_loop(
    device_code: str,
    interval: int,
    *,
    tick: "Callable[[int], None] | None" = None,
) -> tuple[str, str]:
    """Polling loop. `tick(seconds)` runs between requests (defaults to `time.sleep`)."""
    client = get_auth_client(include_device_id=True)
    error_message = "Failed to complete authentication"
    tick = tick or time.sleep
    while True:
        tick(interval)
        try:
            token_response = workos_device_flow_complete.sync_detailed(
                client=client,
                body=workos_device_flow_complete.WorkosDeviceFlowLoginRequest(
                    device_code=device_code,
                ),
            )
        except AuthUnexpectedStatus as e:
            if e.status_code == 403:
                continue
            raise exception_from_response(error_message, e) from e
        except Exception as e:
            error_message += f". Underlying error: {e}"
            raise RuntimeError(error_message) from e

        if isinstance(token_response.parsed, workos_device_flow_complete.LoginResponse):
            return (
                token_response.parsed.jwt,
                token_response.parsed.refresh_token,
            )
        elif isinstance(
            token_response.parsed, workos_device_flow_complete.ErrorResponse400
        ):
            raise exception_from_response(error_message, token_response)


def _poll_device_flow(
    device_code: str,
    interval: int,
) -> tuple[str, str]:
    """Main-thread poll: catches Ctrl+C and prints the `--resume` hint."""
    try:
        return _poll_device_flow_loop(device_code, interval)
    except KeyboardInterrupt:
        _cancel_login_with_resume_hint(device_code)
        raise  # Unreachable: _cancel_login_with_resume_hint calls sys.exit.


_LOOPBACK_HOST = "127.0.0.1"
_LOOPBACK_SCHEME = "http"
_LOOPBACK_CALLBACK_PATH = "/callback"
_LOOPBACK_TIMEOUT_SECONDS = 300


class _LoopbackServer(HTTPServer):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.expected_state: Optional[str] = None
        self.auth_code: Optional[str] = None
        self.auth_state: Optional[str] = None
        self.auth_error: Optional[str] = None


class _LoopbackHandler(BaseHTTPRequestHandler):
    # Prevent a silent peer from blocking handle_request() past the deadline.
    timeout = 10

    def do_GET(self) -> None:
        server = cast(_LoopbackServer, self.server)
        parsed = urlparse(self.path)
        if parsed.path != _LOOPBACK_CALLBACK_PATH:
            self.send_response(404)
            self.end_headers()
            return
        params = parse_qs(parsed.query)
        server.auth_code = params.get("code", [None])[0]
        server.auth_state = params.get("state", [None])[0]
        server.auth_error = params.get("error", [None])[0]
        ok = server.auth_error is None and server.auth_state == server.expected_state
        body = _LOOPBACK_SUCCESS_HTML if ok else _LOOPBACK_ERROR_HTML
        self.send_response(200 if ok else 400)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args: Any) -> None:
        pass


def _can_use_loopback_browser() -> bool:
    """Whether a browser can reach a 127.0.0.1 callback bound on this host."""
    if os.environ.get("CI"):
        return False
    if os.environ.get("CODESPACES") == "true":
        return False
    if os.environ.get("SSH_CONNECTION") or os.environ.get("SSH_TTY"):
        return False
    # Linux needs a graphical session, this matches Python's webbrowser's GUI check:
    if platform.system().lower() == "linux":
        return bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
    return True


def _try_start_loopback_server() -> Optional[_LoopbackServer]:
    """Bind a loopback callback server on a random free port; None if binding fails."""
    try:
        return _LoopbackServer((_LOOPBACK_HOST, 0), _LoopbackHandler)
    except OSError:
        return None


def _generate_pkce() -> tuple[str, str, str]:
    """Return (code_verifier, code_challenge, state) for a loopback PKCE login."""
    code_verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    code_challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return code_verifier, code_challenge, secrets.token_urlsafe(32)


def _start_auth_code_flow(redirect_uri: str, code_challenge: str, state: str) -> str:
    """Ask the auth service for the WorkOS authorization URL to open in the browser."""
    client = get_auth_client()
    with handle_client_exceptions("Login failed. Error calling the dltHub API"):
        response = workos_auth_code_start.sync_detailed(
            client=client,
            body=workos_auth_code_start.WorkosAuthCodeStartRequest(
                redirect_uri=redirect_uri,
                code_challenge=code_challenge,
                state=state,
            ),
        )
    if not isinstance(
        response.parsed, workos_auth_code_start.WorkosAuthCodeStartResponse
    ):
        raise exception_from_response("Failed to start login", response)
    return response.parsed.authorization_url


def _await_loopback_callback(server: _LoopbackServer, expected_state: str) -> str:
    """Block until the browser hits the loopback callback (or timeout); validate state."""
    server.expected_state = expected_state
    server.timeout = 1
    deadline = time.monotonic() + _LOOPBACK_TIMEOUT_SECONDS
    try:
        while server.auth_code is None and server.auth_error is None:
            if time.monotonic() > deadline:
                raise CliCommandInnerException(
                    cmd="dlthub",
                    msg=(
                        "Login timed out before the browser completed. "
                        "Re-run, or use `dlthub login --device`."
                    ),
                )
            server.handle_request()
    except KeyboardInterrupt:
        raise CliCommandInnerException(
            cmd="dlthub",
            msg="Login cancelled. To log in without a browser, run `dlthub login --device`.",
        )
    if server.auth_error:
        raise CliCommandInnerException(
            cmd="dlthub", msg=f"Login failed: {server.auth_error}"
        )
    # state binds the redirect to this CLI process; a mismatch means a forged callback.
    if server.auth_state != expected_state:
        raise CliCommandInnerException(
            cmd="dlthub", msg="Login failed: state mismatch."
        )
    assert server.auth_code is not None
    return server.auth_code


def _exchange_auth_code(code: str, code_verifier: str) -> tuple[str, str]:
    """Exchange the authorization code (+ PKCE verifier) for a JWT and refresh token."""
    client = get_auth_client(include_device_id=True)
    error_message = "Failed to complete authentication"
    with handle_client_exceptions(error_message):
        response = workos_auth_code_exchange.sync_detailed(
            client=client,
            body=workos_auth_code_exchange.WorkosAuthCodeExchangeRequest(
                code=code, code_verifier=code_verifier
            ),
        )
    if isinstance(response.parsed, workos_auth_code_exchange.LoginResponse):
        return response.parsed.jwt, response.parsed.refresh_token
    raise exception_from_response(error_message, response)


def _perform_loopback_login(
    auth_service: RuntimeAuthService,
    web_ui_url: str,
    server: _LoopbackServer,
    *,
    not_logged_in_hint: bool = False,
) -> Optional[tuple[RuntimeAuthService, LoginResult]]:
    """Codeless browser login.

    Returns None only when the pre-browser start call fails, so the caller can fall back
    to the device flow. Once the browser is opened, any failure raises instead of falling back.
    """
    code_verifier, code_challenge, state = _generate_pkce()
    port = server.server_address[1]
    redirect_uri = (
        f"{_LOOPBACK_SCHEME}://{_LOOPBACK_HOST}:{port}{_LOOPBACK_CALLBACK_PATH}"
    )
    try:
        authorization_url = _start_auth_code_flow(redirect_uri, code_challenge, state)
    except Exception:
        # Pre-browser start failure nothing opened yet, so fall back to the device flow.
        server.server_close()
        return None
    try:
        _print_loopback_login(authorization_url, not_logged_in_hint=not_logged_in_hint)
        _open_login_page(authorization_url)
        _print_waiting_for_auth(loopback=True)
        code = _await_loopback_callback(server, state)
        jwt_token, refresh_token = _exchange_auth_code(code, code_verifier)
    finally:
        server.server_close()
    auth_info, _ = auth_service.login(jwt_token, refresh_token=refresh_token)
    return auth_service, _login_complete_result(
        auth_info, web_ui_url, is_new_login=True
    )


def _login_complete_result(
    auth_info: Any,
    web_ui_url: str,
    is_new_login: bool,
) -> LoginResult:
    """Build LoginResult after device flow completes (or token already valid)."""
    return LoginResult(
        email=auth_info.email,
        web_ui_url=web_ui_url,
        is_new_login=is_new_login,
    )


def _perform_login(
    resume: Optional[str] = None,
    *,
    force_device: bool = False,
    not_logged_in_hint: bool = False,
) -> Union[tuple[RuntimeAuthService, LoginResult], DeviceFlowStartResult]:
    """Authenticate via resume / existing token / loopback / device flow. Returns auth service + result."""
    auth_service = RuntimeAuthService(run_context=active())
    web_ui_url = urls.web_ui_base()

    if auth_service.has_api_key():
        raise CliCommandInnerException(
            cmd="dlthub",
            msg=(
                "Login is disabled while an API key is configured. Remove the "
                "configured API key to login via device flow."
            ),
        )

    # Phase 2: resume an in-flight device flow.
    if resume is not None:
        jwt_token, refresh_token = _poll_device_flow(resume, interval=5)
        resumed_auth, _ = auth_service.login(jwt_token, refresh_token=refresh_token)
        return auth_service, _login_complete_result(
            resumed_auth, web_ui_url, is_new_login=True
        )

    # if token expired, auth_info remains None. `RuntimeNotAuthenticated` is
    # ignored here - it will be handled in execute() catch all if re raised later
    auth_info: Optional[AuthInfo] = None
    try:
        auth_info = auth_service.authenticate()
    except RuntimeNotAuthenticated:
        pass

    if auth_info is not None:
        return auth_service, _login_complete_result(
            auth_info, web_ui_url, is_new_login=False
        )

    # Loopback login is the default on a local terminal where a browser can reach
    # the callback port; remote sessions take the device flow.
    if not force_device and _can_use_loopback_browser():
        server = _try_start_loopback_server()
        if server is not None:
            loopback_result = _perform_loopback_login(
                auth_service,
                web_ui_url,
                server,
                not_logged_in_hint=not_logged_in_hint,
            )
            if loopback_result is not None:
                return loopback_result

    # Phase 1: non-interactive — start device flow and let the caller print info.
    if not fmt.is_interactive():
        return _start_device_flow()

    # Interactive: open the browser to the code-complete URL and poll.
    flow = _start_device_flow()
    _print_device_flow_interactive(
        flow["verification_uri_complete"],
        flow["user_code"],
        not_logged_in_hint=not_logged_in_hint,
    )
    _open_login_page(flow["verification_uri_complete"])
    _print_waiting_for_auth()
    jwt_token, refresh_token = _poll_device_flow(
        flow["device_code"],
        flow["interval"],
    )
    auth_info, _ = auth_service.login(jwt_token, refresh_token=refresh_token)
    return auth_service, _login_complete_result(
        auth_info, web_ui_url, is_new_login=True
    )


@track_command(operation="login")
def login(
    minimal_logging: bool = True,
    resume: Optional[str] = None,
    *,
    force_device: bool = False,
    not_logged_in_hint: bool = False,
) -> Optional[RuntimeAuthService]:
    result = _perform_login(
        resume=resume,
        force_device=force_device,
        not_logged_in_hint=not_logged_in_hint,
    )

    # Phase 1 result: device flow started, agent must invoke `--resume` next.
    if isinstance(result, dict):
        _print_device_flow_start(
            result["verification_uri_complete"],
            result["user_code"],
            result["device_code"],
            not_logged_in_hint=not_logged_in_hint,
        )
        return None

    auth_service, login_result = result
    _print_login_result(login_result, minimal_logging)
    return auth_service


@track_command(operation="logout")
def logout() -> None:
    auth_service = RuntimeAuthService(run_context=active())
    auth_service.logout()
    fmt.echo("Logged out")


@requires_login
@track_command(operation="workspace", suboperation="list")
def workspace_list(*, auth_service: RuntimeAuthService) -> None:
    """List all workspaces the authenticated user has access to.

    Requires login but NOT a connected workspace — the user may be picking one.
    """
    user_info = auth_service.fetch_user_info()
    workspaces, current_ws_id = _fetch_workspaces(auth_service, user_info)
    _print_workspaces(workspaces, current_ws_id)


@requires_login
@track_command(operation="workspace", suboperation="connect")
def workspace_connect(
    workspace: Optional[str] = None,
    org_id: Optional[str] = None,
    create: bool = False,
    *,
    auth_service: RuntimeAuthService,
) -> None:
    """Connect this project to a remote workspace by name/ID, or `--create` a new one"""
    if workspace is None and not create and auth_service.has_api_key():
        raise CliCommandInnerException(
            cmd="workspace",
            msg=WORKSPACE_CONNECT_REQUIRES_NAME_FOR_API_KEY,
        )
    # Persists workspace_id (always) + organization_id (write-once) to
    # [runtime], plus workspace name to [workspace.settings] in
    # .dlt/config.toml. Org precedence: pinned org in config > --org-id flag >
    # sole active org > none (multi-org picker / non-interactive error).
    user_info = auth_service.fetch_user_info()
    pinned_org_id = auth_service.organization_id
    effective_org_id = _resolve_effective_org_id(user_info, pinned_org_id, org_id)

    # Scope visible workspaces to the effective org (for picker, name lookup,
    # and ambiguity detection).
    scoped_user_info = (
        _scope_user_info_to_org(user_info, effective_org_id)
        if effective_org_id
        else user_info
    )

    if create:
        # Explicit create: workspace name is required, must not already exist.
        if workspace is None:
            raise CliCommandInnerException(
                cmd="workspace",
                msg=WORKSPACE_CREATE_REQUIRES_NAME,
            )
        if any(ws["name"] == workspace for ws in scoped_user_info["workspaces"]):
            org_label = (
                _org_label(user_info, effective_org_id)
                if effective_org_id
                else "your organization"
            )
            raise CliCommandInnerException(
                cmd="workspace",
                msg=WORKSPACE_NAME_ALREADY_EXISTS.format(
                    name=workspace, org_label=org_label
                ),
            )
        create_org_id = _resolve_create_org_or_raise(
            user_info,
            effective_org_id,
            workspace=workspace,
        )
        workspace_id = _create_workspace(
            auth_service,
            user_info,
            workspace,
            create_org_id,
        )
        created = True
    elif workspace is None:
        # No args. Bootstrap path on zero owned workspaces in scope (the only
        # auto-create CLI path); otherwise fire the picker.
        owned = [
            ws for ws in scoped_user_info["workspaces"] if ws.get("role") == "owner"
        ]
        if not owned:
            workspace_id = _create_workspace_with_default_name(
                auth_service,
                user_info,
                effective_org_id,
            )
            created = True
        else:
            workspace_id, created = _select_or_create_workspace(
                auth_service, scoped_user_info
            )
    else:
        # connect to existing workspace
        created = False
        if effective_org_id:
            # if requested workspace is in other org - notify user
            cross_org_match = next(
                (
                    ws
                    for ws in user_info["workspaces"]
                    if ws["id"] == workspace
                    and ws.get("organization_id")
                    and ws.get("organization_id") != effective_org_id
                ),
                None,
            )
            if cross_org_match is not None:
                _raise_cross_org(user_info, cross_org_match, effective_org_id)
        try:
            workspace_id = _resolve_workspace_id(scoped_user_info, workspace)
        except WorkspaceNotFound as e:
            if e.is_uuid:
                raise CliCommandInnerException(
                    cmd="workspace",
                    msg=(
                        f"Workspace '{workspace}' not found among your "
                        "owned workspaces."
                    ),
                ) from e
            connect_create_org_id = effective_org_id or _sole_active_org_id(user_info)
            if not fmt.is_interactive() or connect_create_org_id is None:
                raise CliCommandInnerException(
                    cmd="workspace",
                    msg=WORKSPACE_NAME_NOT_FOUND.format(name=workspace),
                ) from e
            if not _prompt_create_missing_workspace_in_org(
                workspace, _org_label(user_info, connect_create_org_id)
            ):
                raise CliCommandInnerException(
                    cmd="workspace",
                    msg=WORKSPACE_CONNECT_CREATE_DECLINED.format(name=workspace),
                ) from e
            workspace_id = _create_workspace(
                auth_service, user_info, workspace, connect_create_org_id
            )
            created = True

    # CLI never overwrites a pinned `organization_id`.
    resolved_ws = next(
        (ws for ws in user_info["workspaces"] if ws["id"] == workspace_id), None
    )
    if (
        effective_org_id
        and resolved_ws is not None
        and resolved_ws.get("organization_id")
        and resolved_ws.get("organization_id") != effective_org_id
    ):
        _raise_cross_org(user_info, resolved_ws, effective_org_id)

    auth_service.write_connection(
        workspace_id,
        _org_id_to_persist(user_info, resolved_ws, effective_org_id),
    )

    ws_name = _get_workspace_name(user_info, workspace_id)
    if ws_name:
        auth_service.write_workspace_name(ws_name)

    info: ConnectedWorkspaceInfo = {"workspace_id": workspace_id}
    if created:
        info["created"] = True
    if ws_name:
        info["workspace_name"] = ws_name
    org_name = _get_workspace_org_name(user_info, workspace_id)
    if org_name:
        info["organization_name"] = org_name
    _print_workspace_connected(info)


def _raise_unscoped_multi_org_error(user_info: UserInfo) -> None:
    """Render the picker layout in non-interactive mode and raise."""
    groups = _group_workspaces_by_org(user_info)
    _print_org_groups_non_interactive(groups)
    raise RuntimeClientException(
        "You belong to multiple organizations and no `organization_id` is "
        "pinned. Re-run `dlthub workspace connect` with `--org-id <UUID>` "
        "(see commands above), or run `dlthub workspace connect` without a "
        "workspace argument to use the interactive picker."
    )


def _resolve_create_org_or_raise(
    user_info: UserInfo,
    effective_org_id: Optional[str],
    *,
    workspace: str,
) -> str:
    """Choose the org id new-workspace creation will use, or raise."""
    if effective_org_id:
        return effective_org_id
    sole = _sole_active_org_id(user_info)
    if sole:
        return sole
    _raise_unscoped_multi_org_error(user_info)
    raise AssertionError("unreachable")


def _default_workspace_name() -> str:
    """Default workspace name when creating: read from active WorkspaceRunContext."""
    return active().name


def _prompt_and_set_org_region(
    auth_service: RuntimeAuthService,
    organization_id: str,
) -> None:
    """Recover from the region gate: prompt the owner to pick a region and set it."""
    regions = _fetch_available_regions(api_client=get_api_client(auth_service))
    dataplane_id = _prompt_region_selection(regions)
    auth_service.set_organization_region(organization_id, dataplane_id)


def _create_workspace(
    auth_service: RuntimeAuthService,
    user_info: UserInfo,
    name: str,
    organization_id: str,
    *,
    description: Optional[str] = None,
    organization_name: Optional[str] = None,
) -> str:
    """Create a workspace via the API and stamp it onto user_info.

    On a region-less org the create is gated (409); the owner is prompted to set
    the region, then the create is retried once.
    """
    try:
        new_ws_id = auth_service.create_new_workspace(
            user_info,
            name,
            description,
            organization_id=organization_id,
        )
    except OrgRegionRequired:
        _prompt_and_set_org_region(auth_service, organization_id)
        new_ws_id = auth_service.create_new_workspace(
            user_info,
            name,
            description,
            organization_id=organization_id,
        )
    if organization_name is None:
        organization_name = next(
            (
                org["name"]
                for org in user_info["organizations"]
                if org["id"] == organization_id
            ),
            None,
        )
    # add workspace info to user data
    new_ws: WorkspaceInfo = {
        "id": new_ws_id,
        "name": name,
        "role": "owner",
        "organization_id": organization_id,
    }
    if organization_name:
        new_ws["organization_name"] = organization_name
    if description:
        new_ws["description"] = description
    user_info["workspaces"].append(new_ws)
    return new_ws_id


def _create_workspace_with_default_name(
    auth_service: RuntimeAuthService,
    user_info: UserInfo,
    effective_org_id: Optional[str],
) -> str:
    """Auto-create a workspace named `ctx.name` in the effective/sole org."""
    # Only used when zero owned workspaces exist in the effective scope — the
    # single auto-create path that doesn't require explicit `--create`.
    ws_name = _default_workspace_name()
    create_org_id = _resolve_create_org_or_raise(
        user_info,
        effective_org_id,
        workspace=ws_name,
    )
    return _create_workspace(
        auth_service,
        user_info,
        ws_name,
        create_org_id,
    )


def _connect_workspace_with_picker(auth_service: RuntimeAuthService) -> None:
    """Use picker to connect to remote workspace; auto-connect when there is no choice."""
    user_info = auth_service.fetch_user_info()
    pinned_org_id = auth_service.organization_id
    if pinned_org_id:
        # Stale pin → clear remediation message before scoping yields nothing.
        _validate_pinned_org_id(user_info, pinned_org_id)
    scoped = (
        _scope_user_info_to_org(user_info, pinned_org_id)
        if pinned_org_id
        else user_info
    )
    owned = [ws for ws in scoped["workspaces"] if ws.get("role") == "owner"]

    if not owned:
        # Bootstrap path: auto-create with ctx.name + bind locally.
        new_ws_id = _create_workspace_with_default_name(
            auth_service, user_info, pinned_org_id
        )
        selected = next(ws for ws in user_info["workspaces"] if ws["id"] == new_ws_id)
        auth_service.write_connection(new_ws_id, selected["organization_id"])
        auth_service.write_workspace_name(selected["name"])
        info: ConnectedWorkspaceInfo = {
            "workspace_id": new_ws_id,
            "auto": True,
            "created": True,
        }
        if selected.get("name"):
            info["workspace_name"] = selected["name"]
        if selected.get("organization_name"):
            info["organization_name"] = selected["organization_name"]
        _print_workspace_connected(info)
        return

    if len(owned) == 1:
        # Single owned workspace in scope — typically the auto-created
        # playground in a fresh org. Connect without prompting.
        single = owned[0]
        auth_service.write_connection(
            single["id"],
            single.get("organization_id") or user_info["default_organization_id"],
        )
        auth_service.write_workspace_name(single["name"])
        auto_info: ConnectedWorkspaceInfo = {
            "workspace_id": single["id"],
            "auto": True,
        }
        if single.get("name"):
            auto_info["workspace_name"] = single["name"]
        if single.get("organization_name"):
            auto_info["organization_name"] = single["organization_name"]
        _print_workspace_connected(auto_info)
        return

    # 1+ workspaces in scope: picker (interactive) or non-interactive error.
    selected_id, created = _select_or_create_workspace(auth_service, scoped)
    # The picker may have created a new workspace, which stamps it onto
    # `user_info["workspaces"]` (not `scoped`). Look up there in the created
    # case so the new entry is visible.
    selected = next(
        ws
        for ws in (user_info["workspaces"] if created else scoped["workspaces"])
        if ws["id"] == selected_id
    )
    org_id_to_write = (
        selected.get("organization_id") or user_info["default_organization_id"]
    )
    auth_service.write_connection(selected["id"], org_id_to_write)
    auth_service.write_workspace_name(selected["name"])
    picker_info: ConnectedWorkspaceInfo = {"workspace_id": selected["id"]}
    if created:
        picker_info["created"] = True
    if selected.get("name"):
        picker_info["workspace_name"] = selected["name"]
    if selected.get("organization_name"):
        picker_info["organization_name"] = selected["organization_name"]
    _print_workspace_connected(picker_info)


def _create_workspace_from_prompt(
    auth_service: RuntimeAuthService,
    user_info: UserInfo,
    *,
    organization_id: str,
    organization_name: Optional[str] = None,
) -> str:
    """Prompt user for workspace name + description, then create it."""
    default_name = _default_workspace_name()
    name, description = _prompt_new_workspace(default_name=default_name)
    return _create_workspace(
        auth_service,
        user_info,
        name,
        organization_id,
        description=description,
        organization_name=organization_name,
    )


def _select_or_create_workspace(
    auth_service: RuntimeAuthService,
    org_scoped_user_info: UserInfo,
) -> tuple[str, bool]:
    """Pick or create an owned workspace interactively; returns (id, created)."""
    groups = _group_workspaces_by_org(org_scoped_user_info)
    viewer_only = [
        ws for ws in org_scoped_user_info["workspaces"] if ws.get("role") != "owner"
    ]

    if viewer_only:
        fmt.echo("")
        fmt.note(
            "%d workspace(s) where you are a viewer are not shown. "
            "Only workspaces you own can be connected from the CLI." % len(viewer_only)
        )
        fmt.echo("")

    if not groups:
        # No active orgs at all — should be impossible if /me succeeded, but
        # don't silently auto-create in the user's default org. Raise a
        # diagnostic the user can act on.

        raise CliCommandInnerException(
            cmd="workspace",
            msg=(
                "No active organizations available for your account. Contact "
                "support or check `dlthub workspace list` for membership."
            ),
        )

    fmt.echo("Please select a workspace from the list below or create a new one:")
    fmt.echo("")
    selected = _prompt_workspace_selection(groups)

    # `selected` is either an existing WorkspaceInfo (has `id`) or a
    # CreateInOrgChoice (has only org keys). TypedDict union narrowing isn't
    # supported by mypy, so we cast manually after probing the `id` key.
    if "id" in selected:
        existing: WorkspaceInfo = selected  # type: ignore[assignment]
        return existing["id"], False
    create_choice: CreateInOrgChoice = selected  # type: ignore[assignment]
    new_ws_id = _create_workspace_from_prompt(
        auth_service,
        org_scoped_user_info,
        organization_id=create_choice["organization_id"],
        organization_name=create_choice["organization_name"],
    )
    return new_ws_id, True


@requires_login
@requires_workspace
@track_command(operation="workspace", suboperation="deploy")
def deploy_manifest(
    deployment: Optional[str] = None,
    dry_run: bool = False,
    show_manifest: bool = False,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    for w in warn_missing_profiles():
        fmt.warning(w)

    _sync_deployment(
        level="minimal",
        dry_run=dry_run,
        auth_service=auth_service,
        api_client=api_client,
    )
    _sync_configuration(
        level="minimal",
        dry_run=dry_run,
        auth_service=auth_service,
        api_client=api_client,
    )

    manifest, manifest_hash, api_jobs, warnings = _generate_local_manifest(
        deployment or DEFAULT_DEPLOYMENT_MODULE
    )

    if show_manifest:
        fmt.echo(yaml.dump(dict(manifest), default_flow_style=False, sort_keys=False))
        return

    for w in warnings:
        fmt.warning(w)

    resolved_module = manifest["deployment_module"]
    description = manifest.get("description")
    result = _do_deploy_manifest(
        manifest_hash=manifest_hash,
        api_jobs=api_jobs,
        deployment_module=resolved_module,
        description=description,
        dry_run=dry_run,
        auth_service=auth_service,
        api_client=api_client,
    )

    _print_deploy_result(
        result,
        deployment_module=resolved_module,
        job_count=len(api_jobs),
        description=description,
        dry_run=dry_run,
    )


def _deploy_default_dashboard(
    *, auth_service: RuntimeAuthService, api_client: ApiClient
) -> None:
    """Deploy only the default workspace dashboard (ad-hoc, no __deployment__.py)."""
    _sync_deployment(auth_service=auth_service, api_client=api_client)
    _sync_configuration(auth_service=auth_service, api_client=api_client)
    manifest, manifest_hash, api_jobs, _ = _default_dashboard_manifest_bundle()
    _do_deploy_manifest(
        manifest_hash=manifest_hash,
        api_jobs=api_jobs,
        deployment_module=manifest["deployment_module"],
        description=manifest.get("description"),
        dry_run=False,
        auth_service=auth_service,
        api_client=api_client,
    )


@requires_login
@requires_workspace
@track_command(operation="workspace.deployment", suboperation="sync")
def sync_deployment(
    *,
    level: SyncLoggingLevel = "full",
    dry_run: bool = False,
    verbose: bool = False,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    _sync_deployment(
        level=level,
        dry_run=dry_run,
        verbose=verbose,
        auth_service=auth_service,
        api_client=api_client,
    )


def _sync_deployment(
    *,
    level: SyncLoggingLevel = "silent",
    dry_run: bool = False,
    verbose: bool = False,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> SyncResult:
    result = _do_sync_deployment(
        auth_service=auth_service,
        api_client=api_client,
        dry_run=dry_run,
        compute_diff=level != "silent",
    )
    if level != "silent":
        _print_sync_result("deployment", result, level=level, verbose=verbose)
    return result


@requires_login
@requires_workspace
@track_command(operation="workspace.configuration", suboperation="sync")
def sync_configuration(
    *,
    level: SyncLoggingLevel = "full",
    dry_run: bool = False,
    verbose: bool = False,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    _sync_configuration(
        level=level,
        dry_run=dry_run,
        verbose=verbose,
        auth_service=auth_service,
        api_client=api_client,
    )


def _sync_configuration(
    *,
    level: SyncLoggingLevel = "silent",
    dry_run: bool = False,
    verbose: bool = False,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> SyncResult:
    result = _do_sync_configuration(
        auth_service=auth_service,
        api_client=api_client,
        dry_run=dry_run,
        compute_diff=level != "silent",
    )
    if level != "silent":
        _print_sync_result("configuration", result, level=level, verbose=verbose)
    return result


@requires_login
@requires_workspace
@track_command(operation="job.runs", suboperation="info")
def get_job_run_info(
    script_path_or_job_name: Optional[str] = None,
    run_number: Optional[int] = None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    if script_path_or_job_name is None:
        raise ValueError("Script path or job name is required")
    script_path_or_job_name = _resolve_job_ref_from_server(
        script_path_or_job_name, auth_service=auth_service, api_client=api_client
    )
    run = _fetch_job_run_info(
        api_client,
        auth_service,
        script_path_or_job_name=script_path_or_job_name,
        run_number=run_number,
    )
    _print_job_run_info(run)


@requires_login
@requires_workspace
@track_command(operation="job", suboperation="logs")
def logs(
    script_path_or_job_name: Optional[str] = None,
    run_number: Optional[int] = None,
    *,
    follow: bool = False,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    _fetch_run_logs(
        script_path_or_job_name,
        run_number,
        follow=follow,
        auth_service=auth_service,
        api_client=api_client,
    )


@requires_login
@requires_workspace
@track_command(operation="job.runs", suboperation="logs")
def job_run_logs(
    script_path_or_job_name: Optional[str] = None,
    run_number: Optional[int] = None,
    *,
    follow: bool = False,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    _fetch_run_logs(
        script_path_or_job_name,
        run_number,
        follow=follow,
        auth_service=auth_service,
        api_client=api_client,
    )


def _fetch_run_logs(
    script_path_or_job_name: Optional[str] = None,
    run_number: Optional[int] = None,
    *,
    follow: bool = False,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    """Get logs for a run of job (latest if run number not provided)."""
    if script_path_or_job_name is None:
        raise ValueError("Script path or job name is required")
    script_path_or_job_name = _resolve_job_ref_from_server(
        script_path_or_job_name, auth_service=auth_service, api_client=api_client
    )
    if run_number is None:
        run = _get_latest_run(api_client, auth_service, script_path_or_job_name)
    else:
        run_id = _resolve_run_id_by_number(
            api_client=api_client,
            auth_service=auth_service,
            script_path_or_job_name=script_path_or_job_name,
            run_number=run_number,
        )
        with handle_client_exceptions():
            get_run_result = get_run.sync_detailed(
                client=api_client,
                workspace_id=_to_uuid(auth_service.workspace_id),
                run_id=run_id,
            )
        if not isinstance(get_run_result.parsed, get_run.DetailedRunResponse):
            raise exception_from_response("Failed to get run status", get_run_result)
        run = get_run_result.parsed

    run_id = run.id
    run_status = run.status

    # Terminal states - fetch static logs
    terminal_states = {
        RunStatus.FAILED,
        RunStatus.CANCELLED,
        RunStatus.COMPLETED,
        RunStatus.SKIPPED,
    }

    if run_status in terminal_states:
        run_info = f"Run # {run.number} of job {run.script.name}"
        fmt.echo(f"========== Run logs for {run_info} ==========")
        try:
            for level, message in _iter_run_logs_historical(
                run_id, auth_service=auth_service, api_client=api_client
            ):
                if level == "log":
                    fmt.echo(message)
                elif level == "warning":
                    fmt.warning(message)
                elif level == "error":
                    fmt.error(message)
        except KeyboardInterrupt:
            fmt.echo("\nLog fetch interrupted.")
        fmt.echo(f"========== End of run logs for {run_info} ==========")
    else:
        # Stream logs for non-terminal runs
        header = "Streaming logs" if follow else "Run logs"
        fmt.echo(f"========== {header} for run (status: {run_status}) ==========")
        _stream_run_logs(
            run_id,
            follow=follow,
            auth_service=auth_service,
            api_client=api_client,
        )
        footer = "End of log stream" if follow else "End of run logs"
        fmt.echo(f"========== {footer} ==========")
        if follow:
            _show_final_run_status(
                run_id, auth_service=auth_service, api_client=api_client
            )


@requires_login
@requires_workspace
@track_command(operation="job.runs", suboperation="list")
def get_runs(
    script_path_or_job_name: Optional[str] = None,
    *,
    running: bool = False,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    if script_path_or_job_name is not None and is_selector(script_path_or_job_name):
        matched = _resolve_selectors_to_scripts(
            [script_path_or_job_name],
            api_client=api_client,
            auth_service=auth_service,
        )
        matched_refs = {sc.job_ref for sc in matched}
        all_runs = _fetch_runs(api_client, auth_service, running_only=running)
        runs = [r for r in all_runs if r.script.job_ref in matched_refs]
    else:
        if script_path_or_job_name is not None:
            script_path_or_job_name = _resolve_job_ref_from_server(
                script_path_or_job_name,
                auth_service=auth_service,
                api_client=api_client,
            )
        runs = _fetch_runs(
            api_client,
            auth_service,
            script_path_or_job_name,
            running_only=running,
        )
    _print_runs(runs, running_only=running)


@requires_login
@requires_workspace
@track_command(operation="workspace.deployment", suboperation="list")
def get_deployments(*, auth_service: RuntimeAuthService, api_client: ApiClient) -> None:
    deployments = _fetch_deployments(api_client, auth_service)
    _print_deployments(deployments)


@requires_login
@requires_workspace
@track_command(operation="workspace.deployment", suboperation="info")
def get_deployment_info(
    deployment_version_no: Optional[int] = None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    deployment = _fetch_deployment_info(api_client, auth_service, deployment_version_no)
    _print_deployment_info(deployment)


@requires_login
@requires_workspace
@track_command(operation="job", suboperation="cancel")
def cancel(
    selectors_or_refs: list[str],
    *,
    dry_run: bool = False,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    matched = _resolve_selectors_to_scripts(
        selectors_or_refs, api_client=api_client, auth_service=auth_service
    )
    if not matched:
        raise LookupError(f"No jobs matched: {', '.join(selectors_or_refs)}")
    job_refs = [sc.job_ref for sc in matched]

    with handle_client_exceptions():
        result = bulk_cancel_runs.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            body=BulkCancelRequest(job_refs=job_refs, dry_run=dry_run),
        )
    if isinstance(result.parsed, bulk_cancel_runs.BulkCancelResponse):
        _print_bulk_cancel_result(result.parsed, dry_run=dry_run)
    else:
        raise exception_from_response("Failed to cancel runs", result)


@requires_login
@requires_workspace
@track_command(operation="job.runs", suboperation="cancel")
def cancel_job_run(
    script_path_or_job_name: Optional[str] = None,
    run_number: Optional[int] = None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    _request_run_cancel(
        script_path_or_job_name,
        run_number,
        auth_service=auth_service,
        api_client=api_client,
    )


def _request_run_cancel(
    script_path_or_job_name: Optional[str] = None,
    run_number: Optional[int] = None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    """Request the cancellation of a run, for a script or workspace if script is not provided"""
    if script_path_or_job_name is None:
        raise ValueError("Script path or job name is required")
    script_path_or_job_name = _resolve_job_ref_from_server(
        script_path_or_job_name, auth_service=auth_service, api_client=api_client
    )
    terminal_states = {
        RunStatus.FAILED,
        RunStatus.CANCELLED,
        RunStatus.COMPLETED,
        RunStatus.SKIPPED,
    }
    if run_number is None:
        run = _get_latest_run(api_client, auth_service, script_path_or_job_name)
        if run.status in terminal_states:
            raise NoRunnableRun(
                f"Run # {run.number} is already in a terminal state: {run.status}"
            )
        run_id = run.id
        run_no = run.number
    else:
        run_id = _resolve_run_id_by_number(
            api_client=api_client,
            auth_service=auth_service,
            script_path_or_job_name=script_path_or_job_name,
            run_number=run_number,
        )
        run_no = run_number

    with handle_client_exceptions():
        cancel_run_result = cancel_run.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            run_id=_to_uuid(run_id),
        )
    if isinstance(cancel_run_result.parsed, cancel_run.DetailedRunResponse):
        fmt.echo(f"Successfully requested cancellation of run # {run_no}")
    else:
        raise exception_from_response(
            "Failed to request cancellation of run", cancel_run_result
        )


@requires_login
@requires_workspace
@track_command(operation="workspace.configuration", suboperation="list")
def get_configurations(
    *, auth_service: RuntimeAuthService, api_client: ApiClient
) -> None:
    configurations = _fetch_configurations(api_client, auth_service)
    _print_configurations(configurations)


@requires_login
@requires_workspace
@track_command(operation="workspace.configuration", suboperation="info")
def get_configuration_info(
    configuration_version_no: Optional[int] = None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    configuration = _fetch_configuration_info(
        api_client, auth_service, configuration_version_no
    )
    _print_configuration_info(configuration)


# Convenience commands


def _deploy_and_trigger_job(
    job_ref: str,
    manifest_hash: str,
    api_jobs: list[Any],
    deployment_module: str | None,
    description: str | None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
    refresh: bool = False,
) -> "TriggeredJob":
    """Deploy manifest then trigger a single job by job_ref. Returns the TriggeredJob."""
    _do_deploy_manifest(
        manifest_hash=manifest_hash,
        api_jobs=api_jobs,
        deployment_module=deployment_module,
        description=description,
        dry_run=False,
        auth_service=auth_service,
        api_client=api_client,
    )

    with handle_client_exceptions():
        result = trigger_jobs.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            body=TriggerJobsRequest(job_refs=[job_ref], refresh=refresh),
        )
    if isinstance(result.parsed, trigger_jobs.TriggerJobsResponse):
        triggered = result.parsed.triggered
        if not triggered:
            raise RuntimeClientException(f"Job '{job_ref}' was not triggered.")
        # Using job_refs guarantees server-side resolves to exactly one script.
        if len(triggered) != 1:
            refs = ", ".join(t.job_ref for t in triggered)
            raise RuntimeClientException(
                f"Server triggered {len(triggered)} jobs ({refs}) for job_ref"
                f" '{job_ref}'. This indicates a server-side bug."
            )
        return triggered[0]
    raise exception_from_response("Failed to trigger job", result)


def _swap_browser_url(url: str, auth_service: RuntimeAuthService) -> str:
    """Web-app `url` with a single-use swap code appended for browser opening.

    Returns the plain URL if minting fails. Only use for the opened URL, never
    an echoed one — the code is single-use.
    """
    code = auth_service.mint_swap_code()
    return urls.with_swap_code(url, code) if code else url


def _browser_url_for(url: str, auth_service: RuntimeAuthService) -> Optional[str]:
    """Swap-coded browser URL, or None when non-interactive (avoids minting an unused code)."""
    if not fmt.is_interactive():
        return None
    return _swap_browser_url(url, auth_service)


def _open_app_url(url: str, auth_service: RuntimeAuthService) -> None:
    """Open a web-app URL in the browser, attaching a single-use swap code so
    the page lands logged-in."""
    open_url(_swap_browser_url(url, auth_service))


def _do_launch(
    selectors: list[str],
    *,
    available_selectors: list[str],
    deployment: Optional[str] = None,
    selector_or_job_ref: Optional[str] = None,
    default_selector: str = "batch",
    forbidden_job_type: Optional[str] = None,
    follow: bool = True,
    refresh: bool = False,
    job_ref: Optional[str] = None,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    """Shared implementation for launch, serve, and run-pipeline.

    Generates manifest, selects a single job, syncs, deploys, triggers, follows logs.
    For interactive jobs: shows URL and opens browser.

    Either pass pre-built `selectors` directly (e.g. run-pipeline)
    or pass `selector_or_job_ref` + `default_selector` to resolve them from the manifest.
    When `selector_or_job_ref` is provided it overrides `selectors`.
    """
    # Generate manifest
    if deployment:
        manifest, manifest_hash, api_jobs, warnings = _generate_local_manifest(
            deployment, use_all=False
        )
        deployment_module = None  # ad-hoc deploy
    else:
        manifest, manifest_hash, api_jobs, warnings = _generate_local_manifest(
            DEFAULT_DEPLOYMENT_MODULE
        )
        deployment_module = DEFAULT_DEPLOYMENT_MODULE

    for w in warnings:
        fmt.warning(w)

    # Resolve selectors from job_ref if needed
    if selector_or_job_ref is not None or not selectors:
        selectors = resolve_selector(
            selector_or_job_ref, manifest, default_selector=default_selector
        )

    # Select job locally; route ambiguity through the shared interactive picker.
    # `available_selectors` scopes the no-match listing to jobs the current
    # command can launch (batch / interactive / pipeline_name:*).
    try:
        job_def, _ = select_single_job(
            manifest,
            selectors,
            forbidden_job_type=forbidden_job_type,
            job_ref=job_ref,
            available_selectors=available_selectors,
        )
    except AmbiguousJobSelector as exc:
        # `pick_one_job` prompts in tty / re-raises in non-tty.
        job_def, _ = pick_one_job(exc.matches)

    is_interactive = job_def["entry_point"]["job_type"] == "interactive"

    for w in warn_missing_profiles():
        fmt.warning(w)

    # Sync, deploy, and trigger
    _sync_deployment(auth_service=auth_service, api_client=api_client)
    _sync_configuration(auth_service=auth_service, api_client=api_client)

    # The local select_single_job pick is the source of truth — send the
    # exact job_ref so the server resolves to the same single script (no
    # fnmatch against other deployed scripts).
    triggered = _deploy_and_trigger_job(
        job_def["job_ref"],
        manifest_hash,
        api_jobs,
        deployment_module,
        manifest.get("description"),
        auth_service=auth_service,
        api_client=api_client,
        refresh=refresh,
    )

    # TriggeredJob does not carry job_definition, and this line is a
    # copy-paste-runnable identifier — keep the raw job_ref.
    if not triggered.run_id:
        # Server matched the job but did not start a run — render a friendly
        # message and remediation hints
        status_value = str(getattr(triggered, "status", "")) or "skipped"
        reasons = getattr(triggered, "reasons", None)
        if isinstance(reasons, Unset):
            reasons = None
        skip_info: TriggerSkipInfo = {
            "job_ref": triggered.job_ref,
            "status": cast(TriggerStatus, status_value),
            "trigger": str(triggered.trigger),
            # Default = 1 matches dlt's @job decorator default (decorators.py:276).
            "concurrency": int(job_def.get("execute", {}).get("concurrency", 1) or 1),
        }
        if reasons:
            skip_info["reasons"] = list(reasons)
        # For interactive jobs blocked by the concurrency limit, surface the
        # already-running instance's web UI link — that's where the user wants
        # to land. Best-effort: a network failure here must not turn into a
        # second error on top of the skip message.
        if is_interactive and status_value == "skipped_concurrency_limit":
            try:
                with handle_client_exceptions():
                    res = get_script.sync_detailed(
                        client=api_client,
                        workspace_id=_to_uuid(auth_service.workspace_id),
                        script_id_or_ref=triggered.job_ref,
                    )
                if isinstance(res.parsed, get_script.DetailedScriptResponse):
                    url = res.parsed.script_url
                    if url:
                        skip_info["web_url"] = url
            except Exception:
                pass
        _print_trigger_skip(skip_info)
        return

    # Profile comes from the run row the server just created
    run = triggered.run if not isinstance(triggered.run, Unset) else None
    run_profile: Optional[str] = None
    if run is not None and not isinstance(run.profile, Unset):
        run_profile = run.profile

    manifest_refs = [j["job_ref"] for j in manifest.get("jobs", [])]
    banner: RuntimeRunBannerInfo = {
        "display_label": format_job_selector(job_def["job_ref"], manifest_refs),
        "job_ref": triggered.job_ref,
        "trigger": str(triggered.trigger),
        "trigger_humanized": humanize_trigger(TTrigger(str(triggered.trigger))),
        "profile": run_profile or "unk",
        "location": "remote",
        "run_id": str(triggered.run_id),
        "run_url": urls.job_run_url(auth_service.workspace_id, triggered.run_id),
    }
    if ws_name := _resolve_workspace_name(auth_service):
        banner["workspace_name"] = ws_name
    _print_run_banner(banner)

    if is_interactive:
        # Wait until RUNNING, then show URL
        _follow_run_status(
            triggered.run_id, False, auth_service=auth_service, api_client=api_client
        )
        try:
            with handle_client_exceptions():
                res = get_script.sync_detailed(
                    client=api_client,
                    workspace_id=_to_uuid(auth_service.workspace_id),
                    script_id_or_ref=triggered.job_ref,
                )
            if isinstance(res.parsed, get_script.DetailedScriptResponse):
                url = res.parsed.script_url
                if url:
                    fmt.echo(f"Opening {url}")
                    _open_app_url(url, auth_service)
        except Exception:
            # Raw job_ref — TriggeredJob lacks job_definition for format_job_selector.
            fmt.warning(f"Failed to open application URL for {triggered.job_ref}")

    if follow:
        if not is_interactive:
            _follow_run_status(
                triggered.run_id, True, auth_service=auth_service, api_client=api_client
            )
        _follow_run_logs(
            triggered.run_id,
            auth_service=auth_service,
            api_client=api_client,
        )
    else:
        if not isinstance(triggered.run, Unset) and triggered.run is not None:
            fmt.echo(f"  Job:        {triggered.job_ref}")
            fmt.echo(f"  Run #:      {triggered.run.number}")
            fmt.echo(f"  Status:     {format_run_status(triggered.run.status)}")
            fmt.echo("")
        fmt.echo(f"To follow logs: dlthub job logs {triggered.job_ref} --follow")


@requires_login
@requires_workspace
@track_command(operation="job", suboperation="run")
def launch(
    selector_or_job_ref: Optional[str] = None,
    deployment: Optional[str] = None,
    follow: bool = False,
    refresh: bool = False,
    job_ref: Optional[str] = None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    selector_or_job_ref, deployment = promote_deployment_arg(
        selector_or_job_ref, deployment
    )
    _do_launch(
        [],
        available_selectors=["batch"],
        deployment=deployment,
        selector_or_job_ref=selector_or_job_ref,
        default_selector="manual:",
        forbidden_job_type="interactive",
        follow=follow,
        refresh=refresh,
        job_ref=job_ref,
        auth_service=auth_service,
        api_client=api_client,
    )


@requires_login
@requires_workspace
@track_command(operation="job", suboperation="serve")
def serve(
    selector_or_job_ref: Optional[str] = None,
    deployment: Optional[str] = None,
    follow: bool = False,
    job_ref: Optional[str] = None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    selector_or_job_ref, deployment = promote_deployment_arg(
        selector_or_job_ref, deployment
    )
    _do_launch(
        [],
        available_selectors=["interactive"],
        deployment=deployment,
        selector_or_job_ref=selector_or_job_ref,
        default_selector="manual:",
        forbidden_job_type="batch",
        follow=follow,
        job_ref=job_ref,
        auth_service=auth_service,
        api_client=api_client,
    )


@requires_login
@requires_workspace
@track_command(operation="job", suboperation="trigger")
def trigger(
    selectors: list[str],
    dry_run: bool = False,
    profile: Optional[str] = None,
    refresh: bool = False,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    selectors, job_refs = _resolve_trigger_selectors(
        selectors, auth_service=auth_service, api_client=api_client
    )

    with handle_client_exceptions():
        result = trigger_jobs.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            body=TriggerJobsRequest(
                selectors=selectors or UNSET,
                job_refs=job_refs or UNSET,
                dry_run=dry_run,
                profile=profile,
                refresh=refresh,
            ),
        )
    if isinstance(result.parsed, trigger_jobs.TriggerJobsResponse):
        all_jobs = result.parsed.triggered or []
        if not all_jobs:
            fmt.echo("No jobs matched the selector(s)")
            fmt.note(
                "Remember to deploy your workspace if you added/modified job definitons."
            )
        else:
            prefix = "[DRY RUN] " if dry_run else ""
            runs = [
                t for t in all_jobs if getattr(t, "status", "triggered") == "triggered"
            ]
            skipped = [
                t for t in all_jobs if getattr(t, "status", "triggered") != "triggered"
            ]
            # Trigger summary lines use raw job_ref — TriggeredJob carries no
            # job_definition, and these are copy-paste-runnable identifiers.
            if runs:
                fmt.echo(f"{prefix}Triggered ({len(runs)}):")
                for t in runs:
                    run_id = getattr(t, "run_id", None)
                    # Prefer the human-friendly run number; fall back to the id
                    # when the server didn't return a run object (e.g. dry-run).
                    run = t.run if not isinstance(t.run, Unset) else None
                    if run is not None and not isinstance(run.number, Unset):
                        run_info = f" (run #{run.number})"
                    elif run_id:
                        run_info = f" (run #{run_id})"
                    else:
                        run_info = ""
                    fmt.echo(f"  {fmt.bold(t.job_ref)}: {t.trigger}{run_info}")
                    if run_id:
                        fmt.echo(
                            f"    - {urls.job_run_url(auth_service.workspace_id, run_id)}"
                        )
            if skipped:
                fmt.echo(f"{prefix}Skipped ({len(skipped)}):")
                for t in skipped:
                    status_value = str(getattr(t, "status", "")) or "skipped"
                    reasons = getattr(t, "reasons", None)
                    if isinstance(reasons, Unset):
                        reasons = None
                    skip_info: TriggerSkipInfo = {
                        "job_ref": t.job_ref,
                        "status": cast(TriggerStatus, status_value),
                        "trigger": str(t.trigger),
                    }
                    if reasons:
                        skip_info["reasons"] = list(reasons)
                    # `concurrency` intentionally omitted — the bulk path has
                    # no manifest, so we can't tell concurrency==1 from >1.
                    _print_trigger_skip(skip_info, terse=True)
            fmt.echo(f"{prefix}{len(runs)} job(s) triggered, {len(skipped)} skipped")
    else:
        raise exception_from_response("Failed to trigger jobs", result)


@requires_login
@requires_workspace
@track_command(operation="pipeline", suboperation="run")
def run_pipeline(
    pipeline_name: str,
    job_ref: Optional[str] = None,
    follow: bool = False,
    refresh: bool = False,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    _do_launch(
        [f"pipeline_name:{pipeline_name}"],
        available_selectors=["pipeline_name:*"],
        forbidden_job_type="interactive",
        follow=follow,
        refresh=refresh,
        job_ref=job_ref,
        auth_service=auth_service,
        api_client=api_client,
    )


@requires_login
@requires_workspace
@track_command(operation="job", suboperation="publish")
def publish(
    script_path: str,
    cancel: bool = False,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    """Enable or disable a public link for an interactive script."""
    _ensure_profile_warning("access")
    script_path = _resolve_job_ref_from_server(
        script_path, auth_service=auth_service, api_client=api_client
    )

    with handle_client_exceptions():
        script = get_script.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            script_id_or_ref=script_path,
        )
    if not isinstance(script.parsed, get_script.DetailedScriptResponse):
        raise exception_from_response(
            f"Failed to get script with name or id {script_path}", script
        )

    if cancel:
        # disabling public link
        if not script.parsed.public_url:
            fmt.echo(f"Public link for script {script_path} already disabled")
            return
        with handle_client_exceptions():
            disable_public_url_result = disable_public_url.sync_detailed(
                client=api_client,
                workspace_id=_to_uuid(auth_service.workspace_id),
                script_id_or_ref=script_path,
            )
        if isinstance(
            disable_public_url_result.parsed, disable_public_url.ScriptResponse
        ):
            fmt.echo(f"Public link for script {script_path} disabled successfully")
        else:
            raise exception_from_response(
                "Failed to disable public link", disable_public_url_result
            )
        return

    # enabling public link
    if script.parsed.public_url:
        fmt.echo(
            f"Public link for script {script_path} already enabled: {script.parsed.public_url}"
        )
        return
    with handle_client_exceptions():
        enable_public_url_result = enable_public_url.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            script_id_or_ref=script_path,
        )
    if isinstance(enable_public_url_result.parsed, enable_public_url.ScriptResponse):
        fmt.echo(
            f"Public link for script {script_path} enabled successfully: {enable_public_url_result.parsed.public_url}"
        )
    else:
        raise exception_from_response(
            "Failed to enable public link", enable_public_url_result
        )


def _disable_public_link_impl(
    script_path: str, *, auth_service: RuntimeAuthService, api_client: ApiClient
) -> None:
    _ensure_profile_warning("access")
    script_path = _resolve_job_ref_from_server(
        script_path, auth_service=auth_service, api_client=api_client
    )

    with handle_client_exceptions():
        script = get_script.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            script_id_or_ref=script_path,
        )
    if not isinstance(script.parsed, get_script.DetailedScriptResponse):
        raise exception_from_response(
            f"Failed to get script with name or id {script_path}", script
        )
    if not script.parsed.public_url:
        fmt.echo(f"Public link for script {script_path} already disabled")
        return

    with handle_client_exceptions():
        disable_public_url_result = disable_public_url.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            script_id_or_ref=script_path,
        )
    if isinstance(disable_public_url_result.parsed, disable_public_url.ScriptResponse):
        fmt.echo(f"Public link for script {script_path} disabled successfully")
    else:
        raise exception_from_response(
            "Failed to disable public link", disable_public_url_result
        )


def _follow_run_status(
    run_id: UUID,
    is_batch: bool,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    # Batch accepts STARTING/RUNNING/COMPLETED so log streaming can take over;
    # fast providers (Modal cached image) can skip STARTING straight to
    # RUNNING/COMPLETED, which would otherwise spin the poll loop forever.
    final_states = {RunStatus.FAILED, RunStatus.CANCELLED}
    if is_batch:
        final_states |= {RunStatus.STARTING, RunStatus.RUNNING, RunStatus.COMPLETED}
    else:
        final_states.add(RunStatus.RUNNING)
    return _follow_job_run(
        run_id, final_states, auth_service=auth_service, api_client=api_client
    )


def _follow_run_logs(
    run_id: UUID,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    final_states = {RunStatus.FAILED, RunStatus.CANCELLED, RunStatus.COMPLETED}
    return _follow_job_run(
        run_id,
        final_states,
        RunStatus.STARTING,
        True,
        auth_service=auth_service,
        api_client=api_client,
    )


def _follow_job_run(
    run_id: UUID,
    final_states: Set[RunStatus],
    start_status: Optional[RunStatus] = None,
    follow_logs: bool = False,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    if follow_logs:
        # Stream logs in real-time instead of polling
        fmt.echo("========== Run logs ==========")
        _stream_run_logs(
            run_id,
            follow=True,
            auth_service=auth_service,
            api_client=api_client,
        )
        fmt.echo("========== End of run logs ==========")
        _show_final_run_status(run_id, auth_service=auth_service, api_client=api_client)
        return

    # Follow status changes without logs
    status = start_status
    try:
        while True:
            with handle_client_exceptions():
                get_run_result = get_run.sync_detailed(
                    client=api_client,
                    workspace_id=_to_uuid(auth_service.workspace_id),
                    run_id=run_id,
                )
            if not isinstance(get_run_result.parsed, get_run.DetailedRunResponse):
                raise exception_from_response("Failed to get run info", get_run_result)
            new_status = get_run_result.parsed.status
            if new_status != status:
                fmt.echo(f"Run status: {new_status}")
                status = new_status

            if status in final_states:
                break
            time.sleep(2)
    except KeyboardInterrupt:
        fmt.echo("\nInterrupted.")


@requires_login
@requires_workspace
@track_command(operation="job", suboperation="unpublish")
def unpublish(
    script_path: str, *, auth_service: RuntimeAuthService, api_client: ApiClient
) -> None:
    _disable_public_link_impl(
        script_path, auth_service=auth_service, api_client=api_client
    )


@requires_login
@requires_workspace
@track_command(operation="workspace", suboperation="show")
def open_workspace(*, auth_service: RuntimeAuthService, api_client: ApiClient) -> None:
    """Open the workspace overview in the web GUI."""
    _ensure_profile_warning("access")
    url = urls.workspace_url(auth_service.workspace_id)
    _print_show_url("Workspace", url, _browser_url_for(url, auth_service))


@requires_login
@requires_workspace
@track_command(operation="workspace", suboperation="dashboard")
def open_dashboard(*, auth_service: RuntimeAuthService, api_client: ApiClient) -> None:
    _ensure_profile_warning("access")

    # Try to find the dashboard job by job_ref
    dashboard_ref = "jobs.workspace.dashboard"
    with handle_client_exceptions():
        resp = get_script.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            script_id_or_ref=dashboard_ref,
        )

    if isinstance(resp.parsed, get_script.ErrorResponse404):
        # Dashboard not deployed yet. Try normal deploy first, falling back to
        # an ad-hoc dashboard-only manifest when __deployment__.py is missing.
        fmt.echo("Dashboard not deployed. Deploying workspace...")
        try:
            deploy_manifest(auth_service=auth_service, api_client=api_client)
        except FileNotFoundError:
            fmt.echo("No __deployment__.py found. Deploying default dashboard only...")
            _deploy_default_dashboard(auth_service=auth_service, api_client=api_client)
        # Re-fetch
        with handle_client_exceptions():
            resp = get_script.sync_detailed(
                client=api_client,
                workspace_id=_to_uuid(auth_service.workspace_id),
                script_id_or_ref=dashboard_ref,
            )

    if isinstance(resp.parsed, get_script.DetailedScriptResponse):
        script_url = resp.parsed.script_url
    else:
        raise exception_from_response("Failed to get dashboard job", resp)

    if not script_url:
        fmt.error("Failed to get the URL for the dashboard")
        return

    _print_show_url("Dashboard", script_url, _browser_url_for(script_url, auth_service))


@requires_login
@requires_workspace
@track_command(operation="job", suboperation="show")
def show_job(
    selector_or_job_name: Optional[str] = None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    """Show the URL of the job page in the web GUI."""
    if selector_or_job_name is None:
        raise ValueError("Job name, script path, or selector is required")
    job_ref = _resolve_job_ref_from_server(
        selector_or_job_name, auth_service=auth_service, api_client=api_client
    )
    url = urls.job_url(auth_service.workspace_id, job_ref)
    _print_show_url("Job", url, _browser_url_for(url, auth_service))


@requires_login
@requires_workspace
@track_command(operation="job.runs", suboperation="show")
def show_job_run(
    selector_or_job_name: Optional[str] = None,
    run_number: Optional[int] = None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    """Show the URL of the job run page in the web GUI."""
    if selector_or_job_name is None:
        raise ValueError("Job name, script path, or selector is required")
    job_ref = _resolve_job_ref_from_server(
        selector_or_job_name, auth_service=auth_service, api_client=api_client
    )
    if run_number is None:
        run_id = _get_latest_run(api_client, auth_service, job_ref).id
    else:
        run_id = _resolve_run_id_by_number(
            api_client=api_client,
            auth_service=auth_service,
            script_path_or_job_name=job_ref,
            run_number=run_number,
        )
    url = urls.job_run_url(auth_service.workspace_id, run_id)
    _print_show_url("Job run", url, _browser_url_for(url, auth_service))


@requires_login
@requires_workspace
@track_command(operation="pipeline", suboperation="show")
def show_pipeline(
    pipeline_name: str,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    """Show the URL of the pipeline observability view in the web GUI."""
    url = urls.pipeline_url(auth_service.workspace_id, pipeline_name)
    _print_show_url("Pipeline", url, _browser_url_for(url, auth_service))


@requires_login
@requires_workspace
@track_command(operation="workspace", suboperation="info")
def runtime_info(*, auth_service: RuntimeAuthService, api_client: ApiClient) -> None:
    info = _fetch_runtime_info(auth_service=auth_service, api_client=api_client)
    _print_runtime_info(info)

    # Show the deploy reconciliation plan (same as `dlthub workspace deploy --dry-run`).
    # Surface manifest-load errors as warnings and continue — `info` should
    # never fail because the local deployment module is broken.
    try:
        manifest, manifest_hash, api_jobs, warnings = _generate_local_manifest(
            DEFAULT_DEPLOYMENT_MODULE
        )
    except (ImportError, FileNotFoundError) as e:
        # Graceful degradation: never fail `runtime info` because the local
        # deployment module is broken or missing — just warn.
        fmt.echo("")
        fmt.warning(str(e))
        return

    for w in warnings:
        fmt.warning(w)

    resolved_module = manifest["deployment_module"]
    description = manifest.get("description")
    try:
        plan = _do_deploy_manifest(
            manifest_hash=manifest_hash,
            api_jobs=api_jobs,
            deployment_module=resolved_module,
            description=description,
            dry_run=True,
            auth_service=auth_service,
            api_client=api_client,
        )
    except Exception as e:
        fmt.warning(f"Could not fetch deploy plan: {e}")
        return

    fmt.echo("")
    _print_deploy_result(
        plan,
        deployment_module=resolved_module,
        job_count=len(api_jobs),
        description=description,
        dry_run=True,
    )


# Power user: jobs and job-runs


@requires_login
@requires_workspace
@track_command(operation="job", suboperation="list")
def jobs_list(
    selectors: list[str] | None = None,
    *,
    archived: bool = False,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    jobs = _resolve_selectors_to_scripts(
        selectors or [],
        api_client=api_client,
        auth_service=auth_service,
        include_archived=archived,
    )
    _print_jobs(jobs)


@requires_login
@requires_workspace
@track_command(operation="job", suboperation="info")
def job_info(
    script_path_or_job_name: Optional[str] = None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    if not script_path_or_job_name:
        raise ValueError("Script path or job name is required")
    script_path_or_job_name = _resolve_job_ref_from_server(
        script_path_or_job_name, auth_service=auth_service, api_client=api_client
    )
    job = _fetch_job_info(api_client, auth_service, script_path_or_job_name)
    _print_job_info(job)
