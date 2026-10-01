# Python internals
import os
import platform
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from itertools import chain
from typing import (
    Any,
    Callable,
    Iterator,
    Mapping,
    Optional,
    Sequence,
    Set,
    Union,
    cast,
)
from urllib.parse import parse_qs, urlparse
from uuid import UUID

# Other libraries
import yaml
from dlt._workspace._workspace_context import active
from dlt._workspace.cli import echo as fmt
from dlt._workspace.cli.exceptions import CliCommandInnerException
from dlt._workspace.cli.utils import open_url, track_command as dlt_track_command
from dlt._workspace.deployment import DEFAULT_DEPLOYMENT_MODULE
from dlt._workspace.deployment._run_helpers import (
    promote_deployment_arg,
    resolve_selector,
    select_single_job,
    warn_missing_profiles,
)
from dlt._workspace.deployment._run_views import pick_one_job
from dlt._workspace.deployment._trigger_helpers import humanize_trigger, is_selector
from dlt._workspace.deployment.exceptions import AmbiguousJobSelector
from dlt._workspace.deployment.typing import TTrigger

# Current package
from dlt_runtime import runtime as _runtime_module, urls
from dlt_runtime._loopback_pages import _LOOPBACK_ERROR_HTML, _LOOPBACK_SUCCESS_HTML
from dlt_runtime._runtime_command_helpers import (  # noqa: F401
    _change_workspace_variables,
    _default_dashboard_manifest_bundle,
    _do_deploy_manifest,
    _do_sync_configuration,
    _do_sync_deployment,
    _ensure_profile_warning,
    _fetch_available_regions,
    _fetch_configuration_info,
    _fetch_configurations,
    _fetch_deployment_info,
    _fetch_deployments,
    _fetch_job_info,
    _fetch_job_run_info,
    _fetch_run_detail,
    _fetch_runs,
    _fetch_runtime_info,
    _fetch_workspace_variables,
    _fetch_workspaces,
    _generate_local_manifest,
    _get_latest_run,
    _get_workspace_name,
    _get_workspace_org_name,
    _group_workspaces_by_org,
    _is_recently_finished_terminal,
    _org_id_to_persist,
    _org_label,
    _raise_cross_org,
    _resolve_effective_org_id,
    _resolve_job_ref_from_server,
    _resolve_run_id_by_number,
    _resolve_selectors_to_scripts,
    _resolve_trigger_selectors,
    _resolve_workspace_id,
    _run_id_from_ref,
    _scope_caller_info_to_org,
    _should_hide_log_line,
    _sole_active_org_id,
    _validate_pinned_org_id,
    requires_auth,
    requires_workspace,
)
from dlt_runtime._runtime_command_views import (
    _confirm_variable_delete,
    _format_log_line,
    _open_login_page,
    _print_bulk_cancel_result,
    _print_configuration_info,
    _print_configurations,
    _print_deploy_result,
    _print_deployment_info,
    _print_deployments,
    _print_device_flow_interactive,
    _print_device_flow_start,
    _print_job_info,
    _print_job_paused,
    _print_job_resumed,
    _print_job_run_info,
    _print_jobs,
    _print_login_result,
    _print_loopback_login,
    _print_org_groups_non_interactive,
    _print_run_banner,
    _print_run_final_status,
    _print_runs,
    _print_runtime_info,
    _print_show_url,
    _print_sync_result,
    _print_trigger_skip,
    _print_variable_change,
    _print_variables,
    _print_waiting_for_auth,
    _print_workspace_connected,
    _print_workspaces,
    _prompt_create_missing_workspace_in_org,
    _prompt_new_workspace,
    _prompt_region_selection,
    _prompt_variable_value,
    _prompt_workspace_selection,
    format_job_selector,
    format_run_status,
)
from dlt_runtime.exceptions import (
    NoRunnableRun,
    OrgRegionRequired,
    RuntimeClientException,
    RuntimeNotAuthenticated,
    WorkspaceNotFound,
    handle_client_exceptions,
)
from dlt_runtime.runtime import (
    AuthenticationMethod,
    AuthInfo,
    CliSession,
    PrincipalKind,
    get_auth_transport,
)
from dlt_runtime.strings import (
    JOB_NO_SELECTOR_MATCH,
    JOB_SCHEDULE_TOGGLE_FAILED,
    LOGIN_CANCELLED_RESUME_HINT,
    PERSONAL_API_KEY_CONNECT_REQUIRES_NAME,
    VARIABLE_SECRET_NEEDS_VALUE,
    WORKSPACE_API_KEY_CANNOT_CREATE,
    WORKSPACE_API_KEY_NO_ACCESS,
    WORKSPACE_API_KEY_ORG_MISMATCH,
    WORKSPACE_API_KEY_PIN_MISMATCH,
    WORKSPACE_API_KEY_WRONG_ORG,
    WORKSPACE_API_KEY_WRONG_WORKSPACE,
    WORKSPACE_CONNECT_CREATE_DECLINED,
    WORKSPACE_CREATE_REQUIRES_NAME,
    WORKSPACE_NAME_ALREADY_EXISTS,
    WORKSPACE_NAME_NOT_FOUND,
)
from dlt_runtime.typing import (
    CallerInfo,
    ConnectedWorkspaceInfo,
    CreateInOrgChoice,
    DeviceFlowStartResult,
    LoginResult,
    RuntimeRunBannerInfo,
    SyncLoggingLevel,
    SyncResult,
    TriggerSkipInfo,
    TriggerStatus,
    WorkspaceInfo,
)
from dlthub_sdk import (
    JobRun,
    JobRunStatus,
    LogLine,
    Sync,
    TriggerResult,
    VariableChangeStatus,
    Workspace,
)
from dlthub_sdk._auth import Pending, generate_pkce
from dlthub_sdk.errors import (
    ApiError as SdkApiError,
    NotFound as SdkNotFound,
    TransportError as SdkTransportError,
)


def _open_stored_run_logs(run: JobRun[Sync]) -> Optional[Iterator[LogLine]]:
    """Start reading a finished run's persisted log, or None if there is none yet.

    Pulls the first line so a caller can tell "not consolidated" from "empty"
    before printing a header, without buffering the whole log.
    """
    lines = iter(run.logs())
    try:
        with handle_client_exceptions():
            first = next(lines, None)
    except RuntimeClientException as e:
        if isinstance(e.__cause__, SdkNotFound):
            return None
        raise
    return lines if first is None else chain([first], lines)


def _stream_run_logs(run: JobRun[Sync], *, follow: bool = True) -> None:
    """Display streamed logs from the run stream endpoint using SSE."""
    try:
        with handle_client_exceptions():
            try:
                for line in run.stream_logs(follow=follow):
                    if _should_hide_log_line(line):
                        continue
                    fmt.echo(_format_log_line(line))
            except (SdkApiError, SdkTransportError) as e:
                # Reported, not raised: the caller still prints the run's final status.
                fmt.error(e.message)
    except KeyboardInterrupt:
        fmt.echo("\nLog streaming interrupted.")


def _show_final_run_status(
    run: JobRun[Sync],
    *,
    workspace: Workspace[Sync],
) -> None:
    """Fetch + render the run's current status after the follow loop exits.

    Exits the process with code 1 when the run finished in FAILED or CANCELLED;
    non-terminal statuses (after Ctrl+C / stream errors) are printed as-is and
    do not affect the exit code.
    """
    fresh = _fetch_run_detail(UUID(run.id), workspace=workspace)
    _print_run_final_status(fresh)
    if fresh.failed:
        sys.exit(1)


def track_command(**kwargs: Any) -> Callable[[Any], Any]:
    """Telemetry decorator that keeps the command's own signature visible.

    `with_telemetry` replaces it with `(*f_args, **f_kwargs)` and sets no
    `__wrapped__`, which would hide what a command declares from
    `@requires_workspace`, whose injection reads exactly that.

    Args:
        **kwargs: Forwarded to the dlt decorator.

    Returns:
        The decorator to apply.
    """
    decorate = dlt_track_command("runtime", track_before=False, **kwargs)

    def apply(fn: Any) -> Any:
        tracked = decorate(fn)
        tracked.__wrapped__ = fn
        return tracked

    return apply


def _start_device_flow() -> DeviceFlowStartResult:
    """Start the OAuth device flow without blocking. No browser, no polling."""
    with handle_client_exceptions("Login failed. Error calling the dltHub API"):
        started = get_auth_transport().device_flow_start()
    return DeviceFlowStartResult(
        verification_uri=started.verification_uri,
        verification_uri_complete=started.verification_uri_complete,
        user_code=started.user_code,
        device_code=started.device_code,
        interval=started.interval,
    )


def _cancel_login_with_resume_hint(device_code: str) -> None:
    """Print the `--resume` hint and exit 130; shared by interactive prompt and poll."""
    fmt.echo(LOGIN_CANCELLED_RESUME_HINT.format(device_code=device_code))
    sys.exit(130)


# RFC 8628 §3.5: on `slow_down` the client adds 5 seconds to its polling interval.
_SLOW_DOWN_STEP_SECONDS = 5


def _poll_device_flow_loop(
    device_code: str,
    interval: int,
    *,
    tick: "Callable[[int], None] | None" = None,
    poll_first: bool = False,
) -> tuple[str, str]:
    """Polling loop. `tick(seconds)` runs between requests (defaults to `time.sleep`)."""
    transport = get_auth_transport(include_device_id=True)
    error_message = "Failed to complete authentication"
    tick = tick or time.sleep
    wait = not poll_first
    while True:
        if wait:
            tick(interval)
        wait = True
        with handle_client_exceptions(error_message):
            outcome = transport.device_flow_complete(device_code=device_code)

        if isinstance(outcome, Pending):
            if outcome.slow_down:
                interval += _SLOW_DOWN_STEP_SECONDS
            continue
        return outcome.access_token, outcome.refresh_token


def _poll_device_flow(
    device_code: str,
    interval: int,
    *,
    poll_first: bool = False,
) -> tuple[str, str]:
    """Main-thread poll: catches Ctrl+C and prints the `--resume` hint."""
    try:
        return _poll_device_flow_loop(device_code, interval, poll_first=poll_first)
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
    pkce = generate_pkce()
    return pkce.verifier, pkce.challenge, pkce.state


def _start_auth_code_flow(redirect_uri: str, code_challenge: str, state: str) -> str:
    """Ask the auth service for the WorkOS authorization URL to open in the browser."""
    with handle_client_exceptions("Login failed. Error calling the dltHub API"):
        return get_auth_transport().auth_code_start(
            redirect_uri=redirect_uri, code_challenge=code_challenge, state=state
        )


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
    with handle_client_exceptions("Failed to complete authentication"):
        tokens = get_auth_transport(include_device_id=True).auth_code_exchange(
            code=code, code_verifier=code_verifier
        )
    return tokens.access_token, tokens.refresh_token


def _perform_loopback_login(
    session: CliSession,
    web_ui_url: str,
    server: _LoopbackServer,
    *,
    not_logged_in_hint: bool = False,
) -> Optional[tuple[CliSession, LoginResult]]:
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
    auth_info = session.login(jwt_token, refresh_token=refresh_token)
    return session, _login_complete_result(auth_info, web_ui_url, is_new_login=True)


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
) -> Union[tuple[CliSession, LoginResult], DeviceFlowStartResult]:
    """Authenticate via resume / existing token / loopback / device flow. Returns auth service + result."""
    session = CliSession(run_context=active())
    web_ui_url = urls.web_ui_base()

    if session.authentication_method() is AuthenticationMethod.API_KEY:
        raise CliCommandInnerException(
            cmd="dlthub",
            msg=(
                "Login is disabled while an API key is configured. Remove the "
                "configured API key to login via device flow."
            ),
        )

    # Phase 2: resume an in-flight device flow.
    if resume is not None:
        jwt_token, refresh_token = _poll_device_flow(
            resume, interval=5, poll_first=True
        )
        resumed_auth = session.login(jwt_token, refresh_token=refresh_token)
        return session, _login_complete_result(
            resumed_auth, web_ui_url, is_new_login=True
        )

    # if token expired, auth_info remains None. `RuntimeNotAuthenticated` is
    # ignored here - it will be handled in execute() catch all if re raised later
    auth_info: Optional[AuthInfo] = None
    try:
        auth_info = session.authenticate()
    except RuntimeNotAuthenticated:
        pass

    if auth_info is not None:
        return session, _login_complete_result(
            auth_info, web_ui_url, is_new_login=False
        )

    # Loopback login is the default on a local terminal where a browser can reach
    # the callback port; remote sessions take the device flow.
    if not force_device and _can_use_loopback_browser():
        server = _try_start_loopback_server()
        if server is not None:
            loopback_result = _perform_loopback_login(
                session,
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
    auth_info = session.login(jwt_token, refresh_token=refresh_token)
    return session, _login_complete_result(auth_info, web_ui_url, is_new_login=True)


@track_command(operation="login")
def login(
    minimal_logging: bool = True,
    resume: Optional[str] = None,
    *,
    force_device: bool = False,
    not_logged_in_hint: bool = False,
) -> Optional[CliSession]:
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

    session, login_result = result
    _print_login_result(login_result, minimal_logging)
    return session


@track_command(operation="logout")
def logout() -> None:
    session = CliSession(run_context=active())
    session.logout()
    fmt.echo("Logged out")


@requires_auth
@track_command(operation="workspace", suboperation="list")
def workspace_list(*, session: CliSession) -> None:
    """List all workspaces the caller has access to.

    Requires auth but NOT a connected workspace, since the user may be picking one.
    """
    workspaces, current_ws_id = _fetch_workspaces(session)
    _print_workspaces(workspaces, current_ws_id)


@requires_auth
@track_command(operation="workspace", suboperation="connect")
def workspace_connect(
    workspace: Optional[str] = None,
    org_id: Optional[str] = None,
    create: bool = False,
    *,
    session: CliSession,
) -> None:
    """Connect this project to a remote workspace by name/ID, or `--create` a new one"""
    if session.principal_kind() is PrincipalKind.SERVICE_ACCOUNT:
        if create:
            raise CliCommandInnerException(
                cmd="workspace", msg=WORKSPACE_API_KEY_CANNOT_CREATE
            )
        _connect_bound_workspace(session, workspace, org_id)
        return
    if (
        workspace is None
        and not create
        and session.authentication_method() is AuthenticationMethod.API_KEY
    ):
        raise CliCommandInnerException(
            cmd="workspace", msg=PERSONAL_API_KEY_CONNECT_REQUIRES_NAME
        )
    # Persists workspace_id (always) + organization_id (write-once) to
    # [runtime], plus workspace name to [workspace.settings] in
    # .dlt/config.toml. Org precedence: pinned org in config > --org-id flag >
    # sole active org > none (multi-org picker / non-interactive error).
    caller_info = session.fetch_caller_info()
    pinned_org_id = session.organization_id
    effective_org_id = _resolve_effective_org_id(caller_info, pinned_org_id, org_id)

    # Scope visible workspaces to the effective org (for picker, name lookup,
    # and ambiguity detection).
    scoped_caller_info = (
        _scope_caller_info_to_org(caller_info, effective_org_id)
        if effective_org_id
        else caller_info
    )

    if create:
        # Explicit create: workspace name is required, must not already exist.
        if workspace is None:
            raise CliCommandInnerException(
                cmd="workspace",
                msg=WORKSPACE_CREATE_REQUIRES_NAME,
            )
        if any(ws["name"] == workspace for ws in scoped_caller_info["workspaces"]):
            org_label = (
                _org_label(caller_info, effective_org_id)
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
            caller_info,
            effective_org_id,
            workspace=workspace,
        )
        workspace_id = _create_workspace(
            session,
            caller_info,
            workspace,
            create_org_id,
        )
        created = True
    elif workspace is None:
        # No args. Bootstrap path on zero owned workspaces in scope (the only
        # auto-create CLI path); otherwise fire the picker.
        owned = [
            ws for ws in scoped_caller_info["workspaces"] if ws.get("role") == "owner"
        ]
        if not owned:
            workspace_id = _create_workspace_with_default_name(
                session,
                caller_info,
                effective_org_id,
            )
            created = True
        else:
            workspace_id, created = _select_or_create_workspace(
                session, scoped_caller_info
            )
    else:
        # connect to existing workspace
        created = False
        if effective_org_id:
            # if requested workspace is in other org - notify user
            cross_org_match = next(
                (
                    ws
                    for ws in caller_info["workspaces"]
                    if ws["id"] == workspace
                    and ws.get("organization_id")
                    and ws.get("organization_id") != effective_org_id
                ),
                None,
            )
            if cross_org_match is not None:
                _raise_cross_org(caller_info, cross_org_match, effective_org_id)
        try:
            workspace_id = _resolve_workspace_id(scoped_caller_info, workspace)
        except WorkspaceNotFound as e:
            if e.is_uuid:
                raise CliCommandInnerException(
                    cmd="workspace",
                    msg=(
                        f"Workspace '{workspace}' not found among your "
                        "owned workspaces."
                    ),
                ) from e
            connect_create_org_id = effective_org_id or _sole_active_org_id(caller_info)
            if not fmt.is_interactive() or connect_create_org_id is None:
                raise CliCommandInnerException(
                    cmd="workspace",
                    msg=WORKSPACE_NAME_NOT_FOUND.format(name=workspace),
                ) from e
            if not _prompt_create_missing_workspace_in_org(
                workspace, _org_label(caller_info, connect_create_org_id)
            ):
                raise CliCommandInnerException(
                    cmd="workspace",
                    msg=WORKSPACE_CONNECT_CREATE_DECLINED.format(name=workspace),
                ) from e
            workspace_id = _create_workspace(
                session, caller_info, workspace, connect_create_org_id
            )
            created = True

    # CLI never overwrites a pinned `organization_id`.
    resolved_ws = next(
        (ws for ws in caller_info["workspaces"] if ws["id"] == workspace_id), None
    )
    if (
        effective_org_id
        and resolved_ws is not None
        and resolved_ws.get("organization_id")
        and resolved_ws.get("organization_id") != effective_org_id
    ):
        _raise_cross_org(caller_info, resolved_ws, effective_org_id)

    session.write_connection(
        workspace_id,
        _org_id_to_persist(caller_info, resolved_ws, effective_org_id),
    )

    ws_name = _get_workspace_name(caller_info["workspaces"], workspace_id)
    if ws_name:
        session.write_workspace_name(ws_name)

    info: ConnectedWorkspaceInfo = {"workspace_id": workspace_id}
    if created:
        info["created"] = True
    if ws_name:
        info["workspace_name"] = ws_name
    org_name = _get_workspace_org_name(caller_info["workspaces"], workspace_id)
    if org_name:
        info["organization_name"] = org_name
    _print_workspace_connected(info)


def _connect_bound_workspace(
    session: CliSession, workspace: Optional[str], org_id: Optional[str]
) -> None:
    """Pin the workspace the API key is bound to; an argument or existing pin may only confirm it."""
    workspaces = session.fetch_caller_info()["workspaces"]
    if not workspaces:
        raise CliCommandInnerException(cmd="workspace", msg=WORKSPACE_API_KEY_NO_ACCESS)
    bound = workspaces[0]
    if workspace is not None and workspace not in (bound["id"], bound["name"]):
        raise CliCommandInnerException(
            cmd="workspace",
            msg=WORKSPACE_API_KEY_WRONG_WORKSPACE.format(
                bound_workspace_name=bound["name"],
                bound_workspace_id=bound["id"],
                workspace=workspace,
            ),
        )
    if org_id is not None and org_id != bound["organization_id"]:
        raise CliCommandInnerException(
            cmd="workspace",
            msg=WORKSPACE_API_KEY_WRONG_ORG.format(
                key_org_name=bound["organization_name"],
                key_org_id=bound["organization_id"],
                org_id=org_id,
            ),
        )
    if session.has_workspace() and session.workspace_id != bound["id"]:
        raise CliCommandInnerException(
            cmd="workspace",
            msg=WORKSPACE_API_KEY_PIN_MISMATCH.format(
                workspace_id=session.workspace_id,
                bound_workspace_id=bound["id"],
            ),
        )
    pinned_org_id = session.organization_id
    if pinned_org_id is not None and pinned_org_id != bound["organization_id"]:
        raise CliCommandInnerException(
            cmd="workspace",
            msg=WORKSPACE_API_KEY_ORG_MISMATCH.format(
                organization_id=pinned_org_id,
                key_org_name=bound["organization_name"],
                key_org_id=bound["organization_id"],
            ),
        )
    session.write_connection(bound["id"], bound["organization_id"])
    session.write_workspace_name(bound["name"])
    info: ConnectedWorkspaceInfo = {
        "workspace_id": bound["id"],
        "workspace_name": bound["name"],
    }
    org_name = bound.get("organization_name")
    if org_name:
        info["organization_name"] = org_name
    _print_workspace_connected(info)


def _raise_unscoped_multi_org_error(caller_info: CallerInfo) -> None:
    """Render the picker layout in non-interactive mode and raise."""
    groups = _group_workspaces_by_org(caller_info)
    _print_org_groups_non_interactive(groups)
    raise RuntimeClientException(
        "You belong to multiple organizations and no `organization_id` is "
        "pinned. Re-run `dlthub workspace connect` with `--org-id <UUID>` "
        "(see commands above), or run `dlthub workspace connect` without a "
        "workspace argument to use the interactive picker."
    )


def _resolve_create_org_or_raise(
    caller_info: CallerInfo,
    effective_org_id: Optional[str],
    *,
    workspace: str,
) -> str:
    """Choose the org id new-workspace creation will use, or raise."""
    if effective_org_id:
        return effective_org_id
    sole = _sole_active_org_id(caller_info)
    if sole:
        return sole
    _raise_unscoped_multi_org_error(caller_info)
    raise AssertionError("unreachable")


def _default_workspace_name() -> str:
    """Default workspace name when creating: read from active WorkspaceRunContext."""
    return active().name


def _prompt_and_set_org_region(
    session: CliSession,
    organization_id: str,
) -> None:
    """Recover from the region gate: prompt the owner to pick a region and set it."""
    # Module-attribute lookup keeps `patch.object(runtime, ...)` effective.
    regions = _fetch_available_regions(runtime=_runtime_module.get_sdk_runtime(session))
    dataplane_id = _prompt_region_selection(regions)
    session.set_organization_region(organization_id, dataplane_id)


def _create_workspace(
    session: CliSession,
    caller_info: CallerInfo,
    name: str,
    organization_id: str,
    *,
    description: Optional[str] = None,
    organization_name: Optional[str] = None,
) -> str:
    """Create a workspace via the API and stamp it onto caller_info.

    On a region-less org the create is gated (409); the owner is prompted to set
    the region, then the create is retried once.
    """
    try:
        new_ws_id = session.create_new_workspace(
            name,
            description,
            organization_id=organization_id,
        )
    except OrgRegionRequired:
        _prompt_and_set_org_region(session, organization_id)
        new_ws_id = session.create_new_workspace(
            name,
            description,
            organization_id=organization_id,
        )
    if organization_name is None:
        organization_name = next(
            (
                org["name"]
                for org in caller_info["organizations"]
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
    caller_info["workspaces"].append(new_ws)
    return new_ws_id


def _create_workspace_with_default_name(
    session: CliSession,
    caller_info: CallerInfo,
    effective_org_id: Optional[str],
) -> str:
    """Auto-create a workspace named `ctx.name` in the effective/sole org."""
    # Only used when zero owned workspaces exist in the effective scope — the
    # single auto-create path that doesn't require explicit `--create`.
    ws_name = _default_workspace_name()
    create_org_id = _resolve_create_org_or_raise(
        caller_info,
        effective_org_id,
        workspace=ws_name,
    )
    return _create_workspace(
        session,
        caller_info,
        ws_name,
        create_org_id,
    )


def _connect_workspace_with_picker(session: CliSession) -> None:
    """Use picker to connect to remote workspace; auto-connect when there is no choice."""
    caller_info = session.fetch_caller_info()
    pinned_org_id = session.organization_id
    if pinned_org_id:
        # Stale pin → clear remediation message before scoping yields nothing.
        _validate_pinned_org_id(caller_info, pinned_org_id)
    scoped = (
        _scope_caller_info_to_org(caller_info, pinned_org_id)
        if pinned_org_id
        else caller_info
    )
    owned = [ws for ws in scoped["workspaces"] if ws.get("role") == "owner"]

    if not owned:
        # Bootstrap path: auto-create with ctx.name + bind locally.
        new_ws_id = _create_workspace_with_default_name(
            session, caller_info, pinned_org_id
        )
        selected = next(ws for ws in caller_info["workspaces"] if ws["id"] == new_ws_id)
        session.write_connection(new_ws_id, selected["organization_id"])
        session.write_workspace_name(selected["name"])
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
        session.write_connection(single["id"], single["organization_id"])
        session.write_workspace_name(single["name"])
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
    selected_id, created = _select_or_create_workspace(session, scoped)
    # The picker may have created a new workspace, which stamps it onto
    # `caller_info["workspaces"]` (not `scoped`). Look up there in the created
    # case so the new entry is visible.
    selected = next(
        ws
        for ws in (caller_info["workspaces"] if created else scoped["workspaces"])
        if ws["id"] == selected_id
    )
    session.write_connection(selected["id"], selected["organization_id"])
    session.write_workspace_name(selected["name"])
    picker_info: ConnectedWorkspaceInfo = {"workspace_id": selected["id"]}
    if created:
        picker_info["created"] = True
    if selected.get("name"):
        picker_info["workspace_name"] = selected["name"]
    if selected.get("organization_name"):
        picker_info["organization_name"] = selected["organization_name"]
    _print_workspace_connected(picker_info)


def _create_workspace_from_prompt(
    session: CliSession,
    caller_info: CallerInfo,
    *,
    organization_id: str,
    organization_name: Optional[str] = None,
) -> str:
    """Prompt user for workspace name + description, then create it."""
    default_name = _default_workspace_name()
    name, description = _prompt_new_workspace(default_name=default_name)
    return _create_workspace(
        session,
        caller_info,
        name,
        organization_id,
        description=description,
        organization_name=organization_name,
    )


def _select_or_create_workspace(
    session: CliSession,
    org_scoped_caller_info: CallerInfo,
) -> tuple[str, bool]:
    """Pick or create an owned workspace interactively; returns (id, created)."""
    groups = _group_workspaces_by_org(org_scoped_caller_info)
    viewer_only = [
        ws for ws in org_scoped_caller_info["workspaces"] if ws.get("role") != "owner"
    ]

    if viewer_only:
        fmt.echo("")
        fmt.note(
            "%d workspace(s) where you are a viewer are not shown. "
            "Only workspaces you own can be connected from the CLI." % len(viewer_only)
        )
        fmt.echo("")

    if not groups:
        # No active orgs at all — should be impossible if /user succeeded, but
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
    create_choice: CreateInOrgChoice = selected
    new_ws_id = _create_workspace_from_prompt(
        session,
        org_scoped_caller_info,
        organization_id=create_choice["organization_id"],
        organization_name=create_choice["organization_name"],
    )
    return new_ws_id, True


@requires_auth
@requires_workspace
@track_command(operation="workspace", suboperation="deploy")
def deploy_manifest(
    deployment: Optional[str] = None,
    dry_run: bool = False,
    show_manifest: bool = False,
    *,
    workspace: Workspace[Sync],
) -> None:
    for w in warn_missing_profiles():
        fmt.warning(w)
    if show_manifest:
        manifest, _, _, warnings = _generate_local_manifest(
            deployment or DEFAULT_DEPLOYMENT_MODULE
        )
        fmt.echo(yaml.dump(dict(manifest), default_flow_style=False, sort_keys=False))
        for w in warnings:
            fmt.warning(w)
        return

    _sync_deployment(
        level="minimal",
        dry_run=dry_run,
        workspace=workspace,
    )
    _sync_configuration(
        level="minimal",
        dry_run=dry_run,
        workspace=workspace,
    )

    manifest, manifest_hash, api_jobs, warnings = _generate_local_manifest(
        deployment or DEFAULT_DEPLOYMENT_MODULE
    )

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
        workspace=workspace,
    )

    _print_deploy_result(
        result,
        deployment_module=resolved_module,
        job_count=len(api_jobs),
        description=description,
        dry_run=dry_run,
    )


def _deploy_default_dashboard(*, workspace: Workspace[Sync]) -> None:
    """Deploy only the default workspace dashboard (ad-hoc, no __deployment__.py)."""
    _sync_deployment(workspace=workspace)
    _sync_configuration(workspace=workspace)
    manifest, manifest_hash, api_jobs, _ = _default_dashboard_manifest_bundle()
    _do_deploy_manifest(
        manifest_hash=manifest_hash,
        api_jobs=api_jobs,
        deployment_module=manifest["deployment_module"],
        description=manifest.get("description"),
        dry_run=False,
        workspace=workspace,
    )


@requires_auth
@requires_workspace
@track_command(operation="workspace.deployment", suboperation="sync")
def sync_deployment(
    *,
    level: SyncLoggingLevel = "full",
    dry_run: bool = False,
    verbose: bool = False,
    workspace: Workspace[Sync],
) -> None:
    _sync_deployment(
        level=level,
        dry_run=dry_run,
        verbose=verbose,
        workspace=workspace,
    )


def _sync_deployment(
    *,
    level: SyncLoggingLevel = "silent",
    dry_run: bool = False,
    verbose: bool = False,
    workspace: Workspace[Sync],
) -> SyncResult:
    result = _do_sync_deployment(
        workspace=workspace,
        dry_run=dry_run,
    )
    if level != "silent":
        _print_sync_result("deployment", result, level=level, verbose=verbose)
    return result


@requires_auth
@requires_workspace
@track_command(operation="workspace.configuration", suboperation="sync")
def sync_configuration(
    *,
    level: SyncLoggingLevel = "full",
    dry_run: bool = False,
    verbose: bool = False,
    workspace: Workspace[Sync],
) -> None:
    _sync_configuration(
        level=level,
        dry_run=dry_run,
        verbose=verbose,
        workspace=workspace,
    )


def _sync_configuration(
    *,
    level: SyncLoggingLevel = "silent",
    dry_run: bool = False,
    verbose: bool = False,
    workspace: Workspace[Sync],
) -> SyncResult:
    result = _do_sync_configuration(
        workspace=workspace,
        dry_run=dry_run,
    )
    if level != "silent":
        _print_sync_result("configuration", result, level=level, verbose=verbose)
    return result


@requires_auth
@requires_workspace
@track_command(operation="job.runs", suboperation="info")
def get_job_run_info(
    script_path_or_job_name: Optional[str] = None,
    run_number: Optional[int] = None,
    *,
    workspace: Workspace[Sync],
) -> None:
    if script_path_or_job_name is None:
        raise ValueError("Script path, job name, or run id is required")
    if _run_id_from_ref(script_path_or_job_name, run_number) is None:
        script_path_or_job_name = _resolve_job_ref_from_server(
            script_path_or_job_name, workspace=workspace
        )
    run = _fetch_job_run_info(
        workspace,
        script_path_or_job_name=script_path_or_job_name,
        run_number=run_number,
    )
    _print_job_run_info(run)


@requires_auth
@requires_workspace
@track_command(operation="job", suboperation="logs")
def logs(
    script_path_or_job_name: Optional[str] = None,
    run_number: Optional[int] = None,
    *,
    follow: bool = False,
    workspace: Workspace[Sync],
) -> None:
    _fetch_run_logs(
        script_path_or_job_name,
        run_number,
        follow=follow,
        workspace=workspace,
    )


@requires_auth
@requires_workspace
@track_command(operation="job.runs", suboperation="logs")
def job_run_logs(
    script_path_or_job_name: Optional[str] = None,
    run_number: Optional[int] = None,
    *,
    follow: bool = False,
    workspace: Workspace[Sync],
) -> None:
    _fetch_run_logs(
        script_path_or_job_name,
        run_number,
        follow=follow,
        workspace=workspace,
    )


def _fetch_run_logs(
    script_path_or_job_name: Optional[str] = None,
    run_number: Optional[int] = None,
    *,
    follow: bool = False,
    workspace: Workspace[Sync],
) -> None:
    """Get logs for a run of job (latest if run number not provided)."""
    if script_path_or_job_name is None:
        raise ValueError("Script path, job name, or run id is required")
    if _run_id_from_ref(script_path_or_job_name, run_number) is None:
        script_path_or_job_name = _resolve_job_ref_from_server(
            script_path_or_job_name, workspace=workspace
        )
    run = _fetch_job_run_info(
        workspace,
        script_path_or_job_name=script_path_or_job_name,
        run_number=run_number,
    )

    if run.finished:
        # A terminal run serves complete, persisted logs. NotFound on a
        # just-finished run means they aren't consolidated yet: fall through to
        # streaming, but only while the run is recent enough for that to be why.
        stored = _open_stored_run_logs(run)
        if stored is not None:
            run_info = f"Run # {run.number} of job {run.job_ref}"
            fmt.echo(f"========== Run logs for {run_info} ==========")
            try:
                # The read continues past the first line, so a failure part-way
                # through a long log still has to reach the user as a CLI error.
                with handle_client_exceptions():
                    for line in stored:
                        if _should_hide_log_line(line):
                            continue
                        fmt.echo(_format_log_line(line))
            except KeyboardInterrupt:
                fmt.echo("\nLog fetch interrupted.")
            fmt.echo(f"========== End of run logs for {run_info} ==========")
            return
        if not _is_recently_finished_terminal(run.ended_at):
            fmt.echo("No logs found for this run.")
            return

    header = "Streaming logs" if follow else "Run logs"
    fmt.echo(f"========== {header} for run (status: {run.status}) ==========")
    _stream_run_logs(run, follow=follow)
    footer = "End of log stream" if follow else "End of run logs"
    fmt.echo(f"========== {footer} ==========")
    if follow:
        _show_final_run_status(run, workspace=workspace)


@requires_auth
@requires_workspace
@track_command(operation="job.runs", suboperation="list")
def get_runs(
    script_path_or_job_name: Optional[str] = None,
    *,
    running: bool = False,
    workspace: Workspace[Sync],
) -> None:
    if script_path_or_job_name is not None and is_selector(script_path_or_job_name):
        matched = _resolve_selectors_to_scripts(
            [script_path_or_job_name],
            workspace=workspace,
        )
        matched_refs = {sc.job_ref for sc in matched}
        all_runs = _fetch_runs(workspace, running_only=running)
        runs = [r for r in all_runs if r.job_ref in matched_refs]
    else:
        if script_path_or_job_name is not None:
            script_path_or_job_name = _resolve_job_ref_from_server(
                script_path_or_job_name, workspace=workspace
            )
        runs = _fetch_runs(
            workspace,
            script_path_or_job_name,
            running_only=running,
        )
    _print_runs(runs, running_only=running)


@requires_auth
@requires_workspace
@track_command(operation="workspace.deployment", suboperation="list")
def get_deployments(*, workspace: Workspace[Sync]) -> None:
    deployments = _fetch_deployments(workspace)
    _print_deployments(deployments)


@requires_auth
@requires_workspace
@track_command(operation="workspace.deployment", suboperation="info")
def get_deployment_info(
    deployment_version_no: Optional[int] = None,
    *,
    workspace: Workspace[Sync],
) -> None:
    deployment = _fetch_deployment_info(workspace, deployment_version_no)
    _print_deployment_info(deployment)


@requires_auth
@requires_workspace
@track_command(operation="job", suboperation="cancel")
def cancel(
    selectors_or_refs: list[str],
    *,
    dry_run: bool = False,
    workspace: Workspace[Sync],
) -> None:
    matched = _resolve_selectors_to_scripts(selectors_or_refs, workspace=workspace)
    if not matched:
        raise LookupError(f"No jobs matched: {', '.join(selectors_or_refs)}")
    job_refs = [sc.job_ref for sc in matched]

    with handle_client_exceptions("Failed to cancel runs"):
        report = workspace.job_runs.cancel_all(job_refs=job_refs, dry_run=dry_run)
    _print_bulk_cancel_result(report, dry_run=dry_run)


@requires_auth
@requires_workspace
@track_command(operation="job.runs", suboperation="cancel")
def cancel_job_run(
    script_path_or_job_name: Optional[str] = None,
    run_number: Optional[int] = None,
    *,
    workspace: Workspace[Sync],
) -> None:
    _request_run_cancel(
        script_path_or_job_name,
        run_number,
        workspace=workspace,
    )


def _request_run_cancel(
    script_path_or_job_name: Optional[str] = None,
    run_number: Optional[int] = None,
    *,
    workspace: Workspace[Sync],
) -> None:
    """Request the cancellation of a run, for a script or workspace if script is not provided"""
    if script_path_or_job_name is None:
        raise ValueError("Script path, job name, or run id is required")
    # Only the by-number path lacks the run itself, so the terminal-state guard
    # below covers a run addressed by id exactly as it covers the latest one.
    ref_run_id = _run_id_from_ref(script_path_or_job_name, run_number)
    if ref_run_id is not None:
        run = _fetch_run_detail(ref_run_id, workspace=workspace)
    else:
        script_path_or_job_name = _resolve_job_ref_from_server(
            script_path_or_job_name, workspace=workspace
        )
        if run_number is None:
            run = _get_latest_run(workspace, script_path_or_job_name)
        else:
            run = _fetch_job_run_info(
                workspace,
                script_path_or_job_name=script_path_or_job_name,
                run_number=run_number,
            )
    if run.finished:
        raise NoRunnableRun(
            f"Run # {run.number} is already in a terminal state: {run.status}"
        )

    with handle_client_exceptions("Failed to request cancellation of run"):
        run.cancel()
    fmt.echo(f"Successfully requested cancellation of run # {run.number}")


@requires_auth
@requires_workspace
@track_command(operation="workspace.configuration", suboperation="list")
def get_configurations(*, workspace: Workspace[Sync]) -> None:
    configurations = _fetch_configurations(workspace)
    _print_configurations(configurations)


@requires_auth
@requires_workspace
@track_command(operation="workspace.configuration", suboperation="info")
def get_configuration_info(
    configuration_version_no: Optional[int] = None,
    *,
    workspace: Workspace[Sync],
) -> None:
    configuration = _fetch_configuration_info(workspace, configuration_version_no)
    _print_configuration_info(configuration)


# Convenience commands


def _deploy_and_trigger_job(
    job_ref: str,
    manifest_hash: str,
    api_jobs: Sequence[Mapping[str, Any]],
    deployment_module: str | None,
    description: str | None,
    *,
    workspace: Workspace[Sync],
    refresh: bool = False,
) -> TriggerResult:
    """Deploy manifest then trigger a single job by job_ref."""
    _do_deploy_manifest(
        manifest_hash=manifest_hash,
        api_jobs=api_jobs,
        deployment_module=deployment_module,
        description=description,
        dry_run=False,
        workspace=workspace,
    )

    with handle_client_exceptions("Failed to trigger job"):
        triggered = workspace.jobs.trigger(refs=[job_ref], refresh=refresh)
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


def _swap_browser_url(url: str, session: CliSession) -> str:
    """Web-app `url` with a single-use swap code appended for browser opening.

    Returns the plain URL if minting fails. Only use for the opened URL, never
    an echoed one — the code is single-use.
    """
    code = session.mint_swap_code()
    return urls.with_swap_code(url, code) if code else url


def _browser_url_for(url: str, session: CliSession) -> Optional[str]:
    """Swap-coded browser URL, or None when non-interactive (avoids minting an unused code)."""
    if not fmt.is_interactive():
        return None
    return _swap_browser_url(url, session)


def _open_app_url(url: str, session: CliSession) -> None:
    """Open a web-app URL in the browser, attaching a single-use swap code so
    the page lands logged-in."""
    open_url(_swap_browser_url(url, session))


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
    session: CliSession,
    workspace: Workspace[Sync],
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
    _sync_deployment(workspace=workspace)
    _sync_configuration(workspace=workspace)

    # The local select_single_job pick is the source of truth — send the
    # exact job_ref so the server resolves to the same single script (no
    # fnmatch against other deployed scripts).
    triggered = _deploy_and_trigger_job(
        job_def["job_ref"],
        manifest_hash,
        api_jobs,
        deployment_module,
        manifest.get("description"),
        workspace=workspace,
        refresh=refresh,
    )

    # TriggeredJob does not carry job_definition, and this line is a
    # copy-paste-runnable identifier — keep the raw job_ref.
    if not triggered.run_id:
        # Server matched the job but did not start a run — render a friendly
        # message and remediation hints
        status_value = str(triggered.status or "skipped")
        reasons = list(triggered.reasons) or None
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
                url = _fetch_job_info(workspace, triggered.job_ref).interactive_url
                if url:
                    skip_info["web_url"] = url
            except Exception:
                pass
        _print_trigger_skip(skip_info)
        return

    # Profile comes from the run row the server just created
    run = _fetch_run_detail(UUID(triggered.run_id), workspace=workspace)
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
        "run_url": urls.job_run_url(workspace.id, triggered.run_id),
    }
    banner["workspace_name"] = workspace.name
    _print_run_banner(banner)

    if is_interactive:
        # Wait until RUNNING, then show URL
        _follow_run_status(
            UUID(str(triggered.run_id)),
            False,
            workspace=workspace,
        )
        try:
            url = _fetch_job_info(workspace, triggered.job_ref).interactive_url
            if url:
                fmt.echo(f"Opening {url}")
                _open_app_url(url, session)
        except Exception:
            # Raw job_ref — a trigger result lacks the definition format_job_selector wants.
            fmt.warning(f"Failed to open application URL for {triggered.job_ref}")

    if follow:
        if not is_interactive:
            _follow_run_status(UUID(str(triggered.run_id)), True, workspace=workspace)
        _follow_run_logs(
            UUID(str(triggered.run_id)),
            workspace=workspace,
        )
    else:
        fmt.echo(f"  Job:        {triggered.job_ref}")
        fmt.echo(f"  Run #:      {run.number}")
        fmt.echo(f"  Status:     {format_run_status(run.status)}")
        fmt.echo("")
        fmt.echo(f"To follow logs: dlthub job logs {triggered.job_ref} --follow")


@requires_auth
@requires_workspace
@track_command(operation="job", suboperation="run")
def launch(
    selector_or_job_ref: Optional[str] = None,
    deployment: Optional[str] = None,
    follow: bool = False,
    refresh: bool = False,
    job_ref: Optional[str] = None,
    *,
    session: CliSession,
    workspace: Workspace[Sync],
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
        session=session,
        workspace=workspace,
    )


@requires_auth
@requires_workspace
@track_command(operation="job", suboperation="serve")
def serve(
    selector_or_job_ref: Optional[str] = None,
    deployment: Optional[str] = None,
    follow: bool = False,
    job_ref: Optional[str] = None,
    *,
    session: CliSession,
    workspace: Workspace[Sync],
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
        session=session,
        workspace=workspace,
    )


@requires_auth
@requires_workspace
@track_command(operation="job", suboperation="trigger")
def trigger(
    selectors: list[str],
    dry_run: bool = False,
    profile: Optional[str] = None,
    refresh: bool = False,
    *,
    session: CliSession,
    workspace: Workspace[Sync],
) -> None:
    selectors, job_refs = _resolve_trigger_selectors(selectors, workspace=workspace)

    with handle_client_exceptions("Failed to trigger jobs"):
        results = workspace.jobs.trigger(
            refs=job_refs or None,
            selectors=selectors or None,
            profile=profile,
            refresh=refresh,
            dry_run=dry_run,
        )
    if not results:
        fmt.echo("No jobs matched the selector(s)")
        fmt.note(
            "Remember to deploy your workspace if you added/modified job definitons."
        )
        return

    prefix = "[DRY RUN] " if dry_run else ""
    runs = [t for t in results if t.started]
    skipped = [t for t in results if not t.started]
    # Trigger summary lines use raw job_ref — a trigger result carries no
    # job_definition, and these are copy-paste-runnable identifiers.
    if runs:
        fmt.echo(f"{prefix}Triggered ({len(runs)}):")
        for t in runs:
            # Prefer the human-friendly run number; fall back to the id when the
            # server didn't return a run object (e.g. dry-run).
            if t.run_number is not None:
                run_info = f" (run #{t.run_number})"
            elif t.run_id:
                run_info = f" (run #{t.run_id})"
            else:
                run_info = ""
            fmt.echo(f"  {fmt.bold(t.job_ref)}: {t.trigger}{run_info}")
            if t.run_id:
                fmt.echo(f"    - {urls.job_run_url(workspace.id, t.run_id)}")
    if skipped:
        fmt.echo(f"{prefix}Skipped ({len(skipped)}):")
        for t in skipped:
            skip_info: TriggerSkipInfo = {
                "job_ref": t.job_ref,
                "status": cast(TriggerStatus, str(t.status)),
                "trigger": t.trigger,
            }
            if t.reasons:
                skip_info["reasons"] = list(t.reasons)
            # `concurrency` intentionally omitted — the bulk path has
            # no manifest, so we can't tell concurrency==1 from >1.
            _print_trigger_skip(skip_info, terse=True)
    fmt.echo(f"{prefix}{len(runs)} job(s) triggered, {len(skipped)} skipped")


@requires_auth
@requires_workspace
@track_command(operation="pipeline", suboperation="run")
def run_pipeline(
    pipeline_name: str,
    job_ref: Optional[str] = None,
    follow: bool = False,
    refresh: bool = False,
    *,
    session: CliSession,
    workspace: Workspace[Sync],
) -> None:
    _do_launch(
        [f"pipeline_name:{pipeline_name}"],
        available_selectors=["pipeline_name:*"],
        forbidden_job_type="interactive",
        follow=follow,
        refresh=refresh,
        job_ref=job_ref,
        session=session,
        workspace=workspace,
    )


@requires_auth
@requires_workspace
@track_command(operation="job", suboperation="publish")
def publish(
    script_path: str,
    cancel: bool = False,
    *,
    workspace: Workspace[Sync],
) -> None:
    """Enable or disable a public link for an interactive script."""
    _ensure_profile_warning("access")
    if cancel:
        _disable_public_link_impl(script_path, workspace=workspace)
        return

    script_path = _resolve_job_ref_from_server(script_path, workspace=workspace)
    job = _fetch_job_info(workspace, script_path)
    if job.public_url:
        fmt.echo(
            f"Public link for script {script_path} already enabled: {job.public_url}"
        )
        return
    with handle_client_exceptions("Failed to enable public link"):
        published = job.publish()
    fmt.echo(
        f"Public link for script {script_path} enabled successfully: "
        f"{published.public_url}"
    )


def _disable_public_link_impl(script_path: str, *, workspace: Workspace[Sync]) -> None:
    _ensure_profile_warning("access")
    script_path = _resolve_job_ref_from_server(script_path, workspace=workspace)
    job = _fetch_job_info(workspace, script_path)
    if not job.public_url:
        fmt.echo(f"Public link for script {script_path} already disabled")
        return

    with handle_client_exceptions("Failed to disable public link"):
        job.unpublish()
    fmt.echo(f"Public link for script {script_path} disabled successfully")


def _follow_run_status(
    run_id: UUID,
    is_batch: bool,
    *,
    workspace: Workspace[Sync],
) -> None:
    # Batch accepts STARTING/RUNNING/COMPLETED so log streaming can take over;
    # fast providers (Modal cached image) can skip STARTING straight to
    # RUNNING/COMPLETED, which would otherwise spin the poll loop forever.
    final_states = {JobRunStatus.FAILED, JobRunStatus.CANCELLED}
    if is_batch:
        final_states |= {
            JobRunStatus.STARTING,
            JobRunStatus.RUNNING,
            JobRunStatus.COMPLETED,
        }
    else:
        final_states.add(JobRunStatus.RUNNING)
    return _follow_job_run(run_id, final_states, workspace=workspace)


def _follow_run_logs(
    run_id: UUID,
    *,
    workspace: Workspace[Sync],
) -> None:
    run = _fetch_run_detail(run_id, workspace=workspace)
    fmt.echo("========== Run logs ==========")
    _stream_run_logs(run, follow=True)
    fmt.echo("========== End of run logs ==========")
    _show_final_run_status(run, workspace=workspace)


def _follow_job_run(
    run_id: UUID,
    final_states: Set[JobRunStatus],
    start_status: Optional[JobRunStatus] = None,
    *,
    workspace: Workspace[Sync],
) -> None:
    status = start_status
    try:
        while True:
            new_status = _fetch_run_detail(run_id, workspace=workspace).status
            if new_status != status:
                fmt.echo(f"Run status: {new_status}")
                status = new_status

            if status in final_states:
                break
            time.sleep(2)
    except KeyboardInterrupt:
        fmt.echo("\nInterrupted.")


@requires_auth
@requires_workspace
@track_command(operation="job", suboperation="unpublish")
def unpublish(script_path: str, *, workspace: Workspace[Sync]) -> None:
    _disable_public_link_impl(script_path, workspace=workspace)


@requires_auth
@requires_workspace
@track_command(operation="workspace", suboperation="show")
def open_workspace(*, session: CliSession) -> None:
    """Open the workspace overview in the web GUI."""
    _ensure_profile_warning("access")
    url = urls.workspace_url(session.workspace_id)
    _print_show_url("Workspace", url, _browser_url_for(url, session))


@requires_auth
@requires_workspace
@track_command(operation="workspace", suboperation="dashboard")
def open_dashboard(*, session: CliSession, workspace: Workspace[Sync]) -> None:
    _ensure_profile_warning("access")
    dashboard_ref = "jobs.workspace.dashboard"
    try:
        job = _fetch_job_info(workspace, dashboard_ref)
    except RuntimeClientException as e:
        # Only "no such job" means it was never deployed; anything else (a 5xx,
        # a rejected request) must not be answered by deploying the workspace.
        if not isinstance(e.__cause__, SdkNotFound):
            raise
        # Try a normal deploy first, falling back to an ad-hoc dashboard-only
        # manifest when __deployment__.py is missing.
        fmt.echo("Dashboard not deployed. Deploying workspace...")
        try:
            deploy_manifest(workspace=workspace)
        except FileNotFoundError:
            fmt.echo("No __deployment__.py found. Deploying default dashboard only...")
            _deploy_default_dashboard(workspace=workspace)
        job = _fetch_job_info(workspace, dashboard_ref)

    script_url = job.interactive_url
    if not script_url:
        fmt.error("Failed to get the URL for the dashboard")
        return

    _print_show_url("Dashboard", script_url, _browser_url_for(script_url, session))


@requires_auth
@requires_workspace
@track_command(operation="job", suboperation="show")
def show_job(
    selector_or_job_name: Optional[str] = None,
    *,
    session: CliSession,
    workspace: Workspace[Sync],
) -> None:
    """Show the URL of the job page in the web GUI."""
    if selector_or_job_name is None:
        raise ValueError("Job name, script path, or selector is required")
    job_ref = _resolve_job_ref_from_server(selector_or_job_name, workspace=workspace)
    url = urls.job_url(workspace.id, job_ref)
    _print_show_url("Job", url, _browser_url_for(url, session))


@requires_auth
@requires_workspace
@track_command(operation="job.runs", suboperation="show")
def show_job_run(
    selector_or_job_name: Optional[str] = None,
    run_number: Optional[int] = None,
    *,
    session: CliSession,
    workspace: Workspace[Sync],
) -> None:
    """Show the URL of the job run page in the web GUI."""
    if selector_or_job_name is None:
        raise ValueError("Job name, script path, selector, or run id is required")
    run_id = _run_id_from_ref(selector_or_job_name, run_number)
    if run_id is None:
        job_ref = _resolve_job_ref_from_server(
            selector_or_job_name, workspace=workspace
        )
        if run_number is None:
            run_id = UUID(_get_latest_run(workspace, job_ref).id)
        else:
            run_id = _resolve_run_id_by_number(
                workspace=workspace,
                script_path_or_job_name=job_ref,
                run_number=run_number,
            )
    url = urls.job_run_url(workspace.id, run_id)
    _print_show_url("Job run", url, _browser_url_for(url, session))


@requires_auth
@requires_workspace
@track_command(operation="pipeline", suboperation="show")
def show_pipeline(
    pipeline_name: str,
    *,
    session: CliSession,
) -> None:
    """Show the URL of the pipeline observability view in the web GUI."""
    url = urls.pipeline_url(session.workspace_id, pipeline_name)
    _print_show_url("Pipeline", url, _browser_url_for(url, session))


@requires_auth
@requires_workspace
@track_command(operation="workspace", suboperation="info")
def runtime_info(*, session: CliSession, workspace: Workspace[Sync]) -> None:
    info = _fetch_runtime_info(session=session, workspace=workspace)
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
            workspace=workspace,
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


@requires_auth
@requires_workspace
@track_command(operation="job", suboperation="list")
def jobs_list(
    selectors: list[str] | None = None,
    *,
    archived: bool = False,
    workspace: Workspace[Sync],
) -> None:
    jobs = _resolve_selectors_to_scripts(
        selectors or [],
        workspace=workspace,
        include_archived=archived,
    )
    _print_jobs(jobs)


@requires_auth
@requires_workspace
@track_command(operation="job", suboperation="info")
def job_info(
    script_path_or_job_name: Optional[str] = None,
    *,
    workspace: Workspace[Sync],
) -> None:
    if not script_path_or_job_name:
        raise ValueError("Script path or job name is required")
    script_path_or_job_name = _resolve_job_ref_from_server(
        script_path_or_job_name, workspace=workspace
    )
    job = _fetch_job_info(workspace, script_path_or_job_name)
    _print_job_info(job)


def _toggle_schedule_pause(
    selectors: Optional[list[str]],
    *,
    pause: bool,
    workspace: Workspace[Sync],
) -> None:
    scripts = _resolve_selectors_to_scripts(selectors or [], workspace=workspace)
    if not scripts:
        fmt.echo(JOB_NO_SELECTOR_MATCH)
        return

    action = "pause" if pause else "resume"
    # A per-job failure does not stop the rest, but does make the command exit non-zero.
    failed: list[str] = []
    for script in scripts:
        job_ref = script.job_ref
        # The endpoints are idempotent, so a no-op is reported rather than written again.
        if script.paused is pause:
            if pause:
                _print_job_paused(job_ref, already_paused=True)
            else:
                _print_job_resumed(job_ref, was_paused=False)
            continue

        try:
            with handle_client_exceptions():
                if pause:
                    script.pause()
                else:
                    script.resume()
        except RuntimeClientException as exc:
            failed.append(job_ref)
            fmt.error(f"Cannot {action} {job_ref}: {exc}")
            continue
        if pause:
            _print_job_paused(job_ref)
        else:
            _print_job_resumed(job_ref)

    if failed:
        raise CliCommandInnerException(
            cmd="job",
            msg=JOB_SCHEDULE_TOGGLE_FAILED.format(
                action=action, job_refs=", ".join(failed)
            ),
        )


@requires_auth
@requires_workspace
@track_command(operation="job", suboperation="pause")
def pause_job(
    selectors: Optional[list[str]] = None,
    *,
    workspace: Workspace[Sync],
) -> None:
    _toggle_schedule_pause(selectors, pause=True, workspace=workspace)


@requires_auth
@requires_workspace
@track_command(operation="job", suboperation="resume")
def resume_job(
    selectors: Optional[list[str]] = None,
    *,
    workspace: Workspace[Sync],
) -> None:
    _toggle_schedule_pause(selectors, pause=False, workspace=workspace)


def _variable_scope_label(profile: Optional[str]) -> str:
    return f"profile '{profile}'" if profile else "the workspace scope"


@requires_auth
@requires_workspace
@track_command(operation="workspace.variable", suboperation="list")
def variable_list(
    profile: Optional[str] = None,
    workspace_only: bool = False,
    *,
    workspace: Workspace[Sync],
) -> None:
    scopes = _fetch_workspace_variables(
        workspace,
        profile=profile,
        workspace_only=workspace_only,
    )
    _print_variables(scopes)


@requires_auth
@requires_workspace
@track_command(operation="workspace.variable", suboperation="set")
def variable_set(
    name: str,
    secret: bool,
    value: Optional[str] = None,
    profile: Optional[str] = None,
    *,
    workspace: Workspace[Sync],
) -> None:
    if value is None:
        value = _prompt_variable_value(name)
    if secret and not value:
        raise RuntimeClientException(VARIABLE_SECRET_NEEDS_VALUE)
    pair = {name: value}
    changes = _change_workspace_variables(
        workspace,
        profile=profile,
        plain=None if secret else pair,
        secrets=pair if secret else None,
    )
    _print_variable_change(changes, scope_label=_variable_scope_label(profile))


@requires_auth
@requires_workspace
@track_command(operation="workspace.variable", suboperation="delete")
def variable_delete(
    name: str,
    profile: Optional[str] = None,
    allow_missing: bool = False,
    *,
    workspace: Workspace[Sync],
) -> None:
    scope_label = _variable_scope_label(profile)
    if not _confirm_variable_delete(name, scope_label=scope_label):
        fmt.echo(f"Left {fmt.bold(name)} in {scope_label}.")
        return
    changes = _change_workspace_variables(
        workspace,
        profile=profile,
        deletes=[name],
    )
    _print_variable_change(changes, scope_label=scope_label)
    # The API is idempotent by design; erroring on a missing name is CLI policy.
    if not allow_missing and any(
        change.status is VariableChangeStatus.NOT_FOUND for change in changes
    ):
        raise RuntimeClientException(f"Variable {name} does not exist in {scope_label}")
