# Python internals
import time
import webbrowser
from functools import partial
from pathlib import Path

import yaml
from typing import TYPE_CHECKING, Any, Optional, Set
from uuid import UUID

# Other libraries
from dlt._workspace._workspace_context import active
from dlt._workspace.cli import echo as fmt
from dlt._workspace.cli.exceptions import CliCommandInnerException
from dlt._workspace.cli.utils import track_command as dlt_track_command
from dlt._workspace.deployment import DEFAULT_DEPLOYMENT_MODULE
from dlt._workspace.deployment._trigger_helpers import is_selector


from dlt_runtime.exceptions import (
    NoRunnableRun,
    RuntimeNotAuthenticated,
    exception_from_response,
    handle_client_exceptions,
)
from dlt_runtime.runtime import (
    RuntimeAuthService,
    UserInfo,
    WorkspaceInfo,
    get_auth_client,
)
from dlt_runtime.runtime_clients.api.api.runs import (
    bulk_cancel_runs,
    cancel_run,
    get_run,
    get_run_logs,
)
from dlt_runtime.runtime_clients.api.models.bulk_cancel_request import (
    BulkCancelRequest,
)
from dlt_runtime.runtime_clients.api.api.scripts import (
    disable_public_url,
    enable_public_url,
    get_script,
)
from dlt_runtime.runtime_clients.api.client import Client as ApiClient
from dlt_runtime.runtime_clients.api.models.log_line import LogLine
from dlt_runtime.runtime_clients.api.models.run_status import RunStatus
from dlt_runtime.runtime_clients.api.types import Unset
from dlt_runtime.runtime_clients.auth.api.workos import (
    workos_device_flow_complete,
    workos_device_flow_start,
)
from dlt_runtime.runtime_clients.auth.errors import (
    UnexpectedStatus as AuthUnexpectedStatus,
)

if TYPE_CHECKING:
    from dlt_runtime.runtime_clients.api.models.triggered_job import TriggeredJob

from dlt_runtime._runtime_command_helpers import (  # noqa: F401
    _to_uuid,
    _get_web_ui_url,
    _resolve_workspace,
    _resolve_or_create_workspace,
    _get_workspace_name,
    _preprocess_run_output,
    _ensure_profile_warning,
    _warn_missing_profiles,
    _generate_local_manifest,
    _do_deploy_manifest,
    _select_single_job,
    _resolve_selector,
    _resolve_job_ref_from_server,
    _resolve_trigger_selectors,
    _require_auth,
    _get_latest_run,
    _resolve_run_id_by_number,
    _resolve_connection,
    _do_sync_deployment,
    _do_sync_configuration,
    _fetch_runtime_info,
    _fetch_workspaces,
    _fetch_job_run_info,
    _fetch_runs,
    _fetch_deployments,
    _fetch_deployment_info,
    _fetch_configurations,
    _fetch_configuration_info,
    _fetch_jobs,
    _fetch_job_info,
    _resolve_selectors_to_scripts,
    _default_dashboard_manifest_bundle,
    _iter_run_log_stream,
)
from dlt_runtime.typing import (
    ConnectInfo,
    LoginResult,
    SwitchedWorkspaceInfo,
    SyncResult,
)
from dlt_runtime._runtime_command_views import (
    _format_log_line,
    _print_connect_info,
    _print_login_result,
    _print_sync_result,
    _print_workspace_switched,
    _prompt_workspace_selection,
    _prompt_new_workspace,
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


track_command = partial(dlt_track_command, "runtime", track_before=False)


def _perform_login(
    workspace: Optional[str] = None,
) -> tuple[RuntimeAuthService, LoginResult]:
    """Login logic — returns auth service and result info, no display."""
    auth_service = RuntimeAuthService(run_context=active())
    web_ui_url = _get_web_ui_url()

    try:
        auth_info = auth_service.authenticate()
        user_info = auth_service.fetch_user_info()
        workspace_id = (
            _resolve_or_create_workspace(
                user_info, workspace, auth_service=auth_service
            )
            if workspace
            else None
        )
        return auth_service, LoginResult(
            email=auth_info.email,
            web_ui_url=web_ui_url,
            is_new_login=False,
            connect_info=_resolve_connection(auth_service, user_info, workspace_id),
        )
    except RuntimeNotAuthenticated:
        pass

    # Device flow needed — this part is inherently interactive (browser + polling)
    client = get_auth_client()
    login_request = workos_device_flow_start.sync_detailed(client=client)
    if not isinstance(
        login_request.parsed, workos_device_flow_start.WorkosDeviceFlowStartResponse
    ):
        raise exception_from_response("Failed to start login", login_request)

    fmt.echo(
        "Please go to %s and enter the code %s"
        % (
            fmt.bold(login_request.parsed.verification_uri),
            fmt.bold(login_request.parsed.user_code),
        )
    )
    webbrowser.open(login_request.parsed.verification_uri)
    fmt.echo("Waiting for authentication...\n")

    error_message = "Failed to complete authentication"
    while True:
        time.sleep(login_request.parsed.interval)
        try:
            token_response = workos_device_flow_complete.sync_detailed(
                client=client,
                body=workos_device_flow_complete.WorkosDeviceFlowLoginRequest(
                    device_code=login_request.parsed.device_code
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
            auth_info, user_info = auth_service.login(
                token_response.parsed.jwt,
                refresh_token=token_response.parsed.refresh_token,
            )
            workspace_id = (
                _resolve_or_create_workspace(
                    user_info, workspace, auth_service=auth_service
                )
                if workspace
                else None
            )
            return auth_service, LoginResult(
                email=auth_info.email,
                web_ui_url=web_ui_url,
                is_new_login=True,
                connect_info=_resolve_connection(auth_service, user_info, workspace_id),
            )
        elif isinstance(
            token_response.parsed, workos_device_flow_complete.ErrorResponse400
        ):
            raise exception_from_response(error_message, token_response)


@track_command(operation="login")
def login(
    minimal_logging: bool = True, workspace: Optional[str] = None
) -> RuntimeAuthService:
    auth_service, result = _perform_login(workspace=workspace)
    _print_login_result(result, minimal_logging)

    # Handle workspace connection (may need interactive selection)
    info = result.get("connect_info")
    if info and info.get("needs_selection"):
        user_info = auth_service.fetch_user_info()
        info = _connect(auth_service, user_info)
    elif info and info["workspace_id"]:
        auth_service.overwrite_local_workspace_id(info["workspace_id"])

    if not minimal_logging and info:
        _print_connect_info(info)

    return auth_service


@track_command(operation="logout")
def logout() -> None:
    auth_service = RuntimeAuthService(run_context=active())
    auth_service.logout()
    fmt.echo("Logged out")


@track_command(operation="workspace", suboperation="list")
def workspace_list() -> None:
    """List all workspaces the authenticated user has access to.

    Uses only authenticate() — does NOT require a workspace to be connected.
    This allows the command to work before workspace selection.
    """
    auth_service, user_info = _require_auth()
    workspaces, current_ws_id = _fetch_workspaces(auth_service, user_info)
    _print_workspaces(workspaces, current_ws_id)


@track_command(operation="workspace", suboperation="switch")
def workspace_switch(workspace: Optional[str] = None) -> None:
    """Switch the locally connected workspace by name/ID, or interactively if omitted."""
    auth_service, user_info = _require_auth()
    if workspace is None:
        workspace_id = _select_or_create_workspace(
            auth_service, user_info, auto_select_single=False
        )
    else:
        workspace_id = _resolve_or_create_workspace(
            user_info, workspace, auth_service=auth_service
        )
    auth_service.overwrite_local_workspace_id(workspace_id)
    info: SwitchedWorkspaceInfo = {"workspace_id": workspace_id}
    ws_name = _get_workspace_name(user_info, workspace_id)
    if ws_name:
        info["workspace_name"] = ws_name
    _print_workspace_switched(info)


def _connect(
    auth_service: RuntimeAuthService,
    user_info: UserInfo,
    workspace_id: Optional[str] = None,
) -> ConnectInfo:
    """Resolve workspace connection, handle interactive selection, return ConnectInfo.

    Persists the selected workspace ID. Interactive prompts are displayed
    when selection is needed, but the final ConnectInfo is returned for
    callers to display as they choose.
    """
    info = _resolve_connection(auth_service, user_info, workspace_id)

    needs = info.get("needs_selection")
    if needs == "no_local":
        fmt.echo(
            "\nIt seems your local workspace is not connected to any remote one on dltHub Runtime."
        )
        selected_id = _select_or_create_workspace(auth_service, user_info)
        auth_service.overwrite_local_workspace_id(selected_id)
        info = _resolve_connection(auth_service, user_info, selected_id)
    elif needs == "mismatch":
        fmt.warning(
            "\nWorkspace id in local config (%s) does not match any remote workspace id on dltHub Runtime."
            % info["workspace_id"],
        )
        selected_id = _select_or_create_workspace(auth_service, user_info)
        auth_service.overwrite_local_workspace_id(selected_id)
        info = _resolve_connection(auth_service, user_info, selected_id)
    elif workspace_id is not None:
        auth_service.overwrite_local_workspace_id(workspace_id)

    return info


def _prompt_and_create_new_workspace(
    auth_service: RuntimeAuthService, user_info: UserInfo
) -> str:
    """Prompt user for workspace name, create it, return new workspace ID."""
    name, description = _prompt_new_workspace()
    new_ws_id = auth_service.create_new_workspace(user_info, name, description)
    fmt.echo(f"Created workspace with id: {fmt.bold(new_ws_id)}")
    # Add to user_info so _get_workspace_name can find it later
    user_info.workspaces.append(
        WorkspaceInfo(id=new_ws_id, name=name, description=description, role="owner")
    )
    return new_ws_id


def _select_or_create_workspace(
    auth_service: RuntimeAuthService,
    user_info: UserInfo,
    *,
    auto_select_single: bool = True,
) -> str:
    """Pick or create an owned workspace interactively; returns its ID.

    `auto_select_single=False` forces the picker even with one owned workspace
    so the user can still choose to create a new one (used by `workspace switch`).
    """
    owned = [ws for ws in user_info.workspaces if ws.role == "owner"]
    viewer_only = [ws for ws in user_info.workspaces if ws.role != "owner"]

    if not owned:
        if viewer_only:
            fmt.note(
                "You have access to %d workspace(s) but only as a viewer. "
                "You need the 'owner' role to connect a workspace from the CLI."
                % len(viewer_only)
            )
        fmt.echo("No owned workspaces found. Let's create one.")
        return _prompt_and_create_new_workspace(auth_service, user_info)

    if len(owned) == 1 and auto_select_single:
        ws = owned[0]
        fmt.echo("Auto-selected workspace: %s (only one available)" % fmt.bold(ws.name))
        return str(ws.id)

    if viewer_only:
        fmt.echo("")
        fmt.note(
            "%d workspace(s) where you are a viewer are not shown. "
            "Only workspaces you own can be connected from the CLI." % len(viewer_only)
        )
        fmt.echo("")

    # Show selection menu
    fmt.echo("Please select a workspace from the list below or create a new one:")
    fmt.echo("")
    selected = _prompt_workspace_selection(owned)

    if selected is None:
        # User chose to create a new workspace
        return _prompt_and_create_new_workspace(auth_service, user_info)
    else:
        return str(selected.id)


@track_command(operation="sync")
def sync_workspace(*, auth_service: RuntimeAuthService, api_client: ApiClient) -> None:
    fmt.echo("Syncing deployment...")
    _sync_deployment(
        minimal_logging=False, auth_service=auth_service, api_client=api_client
    )
    fmt.echo("Syncing configuration...")
    _sync_configuration(
        minimal_logging=False, auth_service=auth_service, api_client=api_client
    )
    fmt.echo("Workspace synchronized successfully")


@track_command(operation="deploy")
def deploy_manifest(
    file: Optional[str] = None,
    dry_run: bool = False,
    show_manifest: bool = False,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    _warn_missing_profiles()

    if not dry_run:
        _sync_deployment(auth_service=auth_service, api_client=api_client)
        _sync_configuration(auth_service=auth_service, api_client=api_client)

    manifest, manifest_hash, api_jobs, warnings = _generate_local_manifest(
        file or DEFAULT_DEPLOYMENT_MODULE
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


@track_command(operation="deployment", suboperation="sync")
def sync_deployment(
    minimal_logging: bool = True,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    _sync_deployment(
        minimal_logging=minimal_logging,
        auth_service=auth_service,
        api_client=api_client,
    )


def _sync_deployment(
    minimal_logging: bool = True,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> SyncResult:
    result = _do_sync_deployment(auth_service=auth_service, api_client=api_client)
    if not minimal_logging:
        _print_sync_result("deployment", result)
    return result


@track_command(operation="configuration", suboperation="sync")
def sync_configuration(
    minimal_logging: bool = True,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    _sync_configuration(
        minimal_logging=minimal_logging,
        auth_service=auth_service,
        api_client=api_client,
    )


def _sync_configuration(
    minimal_logging: bool = True,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> SyncResult:
    result = _do_sync_configuration(auth_service=auth_service, api_client=api_client)
    if not minimal_logging:
        _print_sync_result("configuration", result)
    return result


@track_command(operation="job-runs", suboperation="info")
def get_job_run_info(
    script_path_or_job_name: Optional[str] = None,
    run_number: Optional[int] = None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    if script_path_or_job_name is None:
        raise CliCommandInnerException(
            cmd="runtime",
            msg="Script path or job name is required",
        )
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


@track_command(operation="logs")
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


@track_command(operation="job-runs", suboperation="logs")
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
        raise CliCommandInnerException(
            cmd="runtime",
            msg="Script path or job name is required",
        )
    script_path_or_job_name = _resolve_job_ref_from_server(
        script_path_or_job_name, auth_service=auth_service, api_client=api_client
    )
    if run_number is None:
        run = _get_latest_run(api_client, auth_service, script_path_or_job_name)
        run_id = run.id
        run_status = run.status
    else:
        run_id = _resolve_run_id_by_number(
            api_client=api_client,
            auth_service=auth_service,
            script_path_or_job_name=script_path_or_job_name,
            run_number=run_number,
        )
        # Get run status
        with handle_client_exceptions():
            get_run_result = get_run.sync_detailed(
                client=api_client,
                workspace_id=_to_uuid(auth_service.workspace_id),
                run_id=run_id,
            )
        if isinstance(get_run_result.parsed, get_run.DetailedRunResponse):
            run_status = get_run_result.parsed.status
        else:
            raise exception_from_response("Failed to get run status", get_run_result)

    # Terminal states - fetch static logs
    terminal_states = {
        RunStatus.FAILED,
        RunStatus.CANCELLED,
        RunStatus.COMPLETED,
        RunStatus.SKIPPED,
    }

    if run_status in terminal_states:
        # Fetch static logs for terminal runs
        with handle_client_exceptions():
            get_run_logs_result = get_run_logs.sync_detailed(
                client=api_client,
                workspace_id=_to_uuid(auth_service.workspace_id),
                run_id=run_id,
            )
        if isinstance(get_run_logs_result.parsed, get_run_logs.LogsResponse):
            run = get_run_logs_result.parsed.run
            run_info = f"Run # {run.number} of job {run.script.name}"
            fmt.echo(f"========== Run logs for {run_info} ==========")
            # Format logs if they are LogLine objects
            if isinstance(get_run_logs_result.parsed.logs, list):
                for log in get_run_logs_result.parsed.logs:
                    if isinstance(log, LogLine):
                        fmt.echo(_format_log_line(log))
                    else:
                        fmt.echo(str(log))
            else:
                fmt.echo(get_run_logs_result.parsed.logs)
            fmt.echo(f"========== End of run logs for {run_info} ==========")
        else:
            raise exception_from_response(
                "Failed to get run logs.", get_run_logs_result
            )
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


@track_command(operation="job-runs", suboperation="list")
def get_runs(
    script_path_or_job_name: Optional[str] = None,
    *,
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
        all_runs = _fetch_runs(api_client, auth_service)
        runs = [r for r in all_runs if r.script.job_ref in matched_refs]
    else:
        if script_path_or_job_name is not None:
            script_path_or_job_name = _resolve_job_ref_from_server(
                script_path_or_job_name,
                auth_service=auth_service,
                api_client=api_client,
            )
        runs = _fetch_runs(api_client, auth_service, script_path_or_job_name)
    _print_runs(runs)


@track_command(operation="deployment", suboperation="list")
def get_deployments(*, auth_service: RuntimeAuthService, api_client: ApiClient) -> None:
    deployments = _fetch_deployments(api_client, auth_service)
    _print_deployments(deployments)


@track_command(operation="deployment", suboperation="info")
def get_deployment_info(
    deployment_version_no: Optional[int] = None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    deployment = _fetch_deployment_info(api_client, auth_service, deployment_version_no)
    _print_deployment_info(deployment)


@track_command(operation="cancel")
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
        raise CliCommandInnerException(
            cmd="runtime",
            msg=f"No jobs matched: {', '.join(selectors_or_refs)}",
        )
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


@track_command(operation="job-runs", suboperation="cancel")
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
        raise CliCommandInnerException(
            cmd="runtime",
            msg="Script path or job name is required",
        )
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


@track_command(operation="configuration", suboperation="list")
def get_configurations(
    *, auth_service: RuntimeAuthService, api_client: ApiClient
) -> None:
    configurations = _fetch_configurations(api_client, auth_service)
    _print_configurations(configurations)


@track_command(operation="configuration", suboperation="info")
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
    from dlt_runtime.runtime_clients.api.api.scripts import (
        trigger_jobs as trigger_jobs_api,
    )
    from dlt_runtime.runtime_clients.api.models.trigger_jobs_request import (
        TriggerJobsRequest,
    )

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
        result = trigger_jobs_api.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            body=TriggerJobsRequest(job_refs=[job_ref], refresh=refresh),
        )
    if isinstance(result.parsed, trigger_jobs_api.TriggerJobsResponse):
        triggered = result.parsed.triggered
        if not triggered:
            raise CliCommandInnerException(
                cmd="runtime",
                msg=f"Job '{job_ref}' was not triggered.",
            )
        # Using job_refs guarantees server-side resolves to exactly one script.
        if len(triggered) != 1:
            refs = ", ".join(t.job_ref for t in triggered)
            raise CliCommandInnerException(
                cmd="runtime",
                msg=(
                    f"Server triggered {len(triggered)} jobs ({refs}) for job_ref"
                    f" '{job_ref}'. This indicates a server-side bug."
                ),
            )
        return triggered[0]
    raise exception_from_response("Failed to trigger job", result)


def _promote_file_arg(
    selector_or_job_ref: Optional[str],
    file: Optional[str],
) -> tuple[Optional[str], Optional[str]]:
    """Promote a positional ``.py`` argument to the ``--file`` slot.

    Used by `launch` and `serve` to support `dlt runtime launch script.py`
    as shorthand for `dlt runtime launch --file script.py`. Returns the
    (possibly rewritten) `(selector_or_job_ref, file)` pair.

    Rules:
    - If the positional doesn't end in ``.py`` (case-insensitive), pass through.
    - If both a positional ``.py`` and an explicit ``--file`` are given, error
      (ambiguous).
    - If the positional ``.py`` doesn't exist on disk, error.
    - Otherwise: clear the positional and put the path in ``file``.

    Job refs can never end in ``.py`` because the upstream `dlt` decorators
    enforce that job names and sections are valid Python identifiers (and
    section/name parts can't carry the trailing ``.py`` suffix), so the
    detection is unambiguous.
    """
    if selector_or_job_ref is None or not selector_or_job_ref.lower().endswith(".py"):
        return selector_or_job_ref, file
    if file is not None:
        raise CliCommandInnerException(
            cmd="runtime",
            msg=(
                f"Cannot pass both a positional file '{selector_or_job_ref}' "
                f"and --file '{file}'. Use one or the other."
            ),
        )
    if not Path(selector_or_job_ref).is_file():
        raise CliCommandInnerException(
            cmd="runtime",
            msg=(
                f"File not found: '{selector_or_job_ref}'. Pass an existing "
                ".py file or a job ref/selector."
            ),
        )
    return None, selector_or_job_ref


def _do_launch(
    selectors: list[str],
    *,
    file: Optional[str] = None,
    selector_or_job_ref: Optional[str] = None,
    default_selector: str = "batch",
    forbidden_job_type: Optional[str] = None,
    follow: bool = True,
    refresh: bool = False,
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
    if file:
        manifest, manifest_hash, api_jobs, warnings = _generate_local_manifest(
            file, use_all=False
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
        selectors = _resolve_selector(
            selector_or_job_ref, manifest, default_selector=default_selector
        )

    # Select job locally
    job_def, trigger = _select_single_job(
        manifest, selectors, forbidden_job_type=forbidden_job_type
    )

    is_interactive = job_def["entry_point"]["job_type"] == "interactive"

    _warn_missing_profiles()

    # Sync, deploy, and trigger
    _sync_deployment(auth_service=auth_service, api_client=api_client)
    _sync_configuration(auth_service=auth_service, api_client=api_client)

    # The local _select_single_job pick is the source of truth — send the
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
        # Server matched the job but did not start a run (freshness gating,
        # pending upstream, etc.) — surface the reason instead of silently
        # exiting after the generic "triggered" line.
        status = getattr(triggered, "status", None)
        reason = str(status) if status else "skipped"
        fmt.echo(
            f"Job {fmt.bold(triggered.job_ref)} was not started "
            f"(trigger: {triggered.trigger}, reason: {reason})"
        )
        return

    fmt.echo(
        f"Job {fmt.bold(triggered.job_ref)} triggered (trigger: {triggered.trigger})"
    )

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
                    webbrowser.open(url, new=2, autoraise=True)
        except Exception:
            # Raw job_ref — TriggeredJob lacks job_definition for format_job_label.
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
            fmt.echo(f"  Status:     {triggered.run.status.value}")
            fmt.echo("")
        fmt.echo(f"To follow logs: dlt runtime logs {triggered.job_ref} --follow")


@track_command(operation="launch")
def launch(
    selector_or_job_ref: Optional[str] = None,
    file: Optional[str] = None,
    follow: bool = False,
    refresh: bool = False,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    selector_or_job_ref, file = _promote_file_arg(selector_or_job_ref, file)
    _do_launch(
        [],
        file=file,
        selector_or_job_ref=selector_or_job_ref,
        default_selector="manual:",
        forbidden_job_type="interactive",
        follow=follow,
        refresh=refresh,
        auth_service=auth_service,
        api_client=api_client,
    )


@track_command(operation="serve")
def serve(
    selector_or_job_ref: Optional[str] = None,
    file: Optional[str] = None,
    follow: bool = False,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    selector_or_job_ref, file = _promote_file_arg(selector_or_job_ref, file)
    _do_launch(
        [],
        file=file,
        selector_or_job_ref=selector_or_job_ref,
        default_selector="manual:",
        forbidden_job_type="batch",
        follow=follow,
        auth_service=auth_service,
        api_client=api_client,
    )


@track_command(operation="trigger")
def trigger(
    selectors: list[str],
    dry_run: bool = False,
    profile: Optional[str] = None,
    refresh: bool = False,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    from dlt_runtime.runtime_clients.api.api.scripts import trigger_jobs
    from dlt_runtime.runtime_clients.api.models.trigger_jobs_request import (
        TriggerJobsRequest,
    )
    from dlt_runtime.runtime_clients.api.types import UNSET

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
                    run_info = (
                        f" (run #{t.run_id})" if getattr(t, "run_id", None) else ""
                    )
                    fmt.echo(f"  {t.job_ref}: {t.trigger}{run_info}")
            if skipped:
                fmt.echo(f"{prefix}Skipped ({len(skipped)}):")
                for t in skipped:
                    reason = getattr(t, "status", "skipped")
                    fmt.echo(f"  {t.job_ref}: {reason}")
            fmt.echo(f"{prefix}{len(runs)} job(s) triggered, {len(skipped)} skipped")
    else:
        raise exception_from_response("Failed to trigger jobs", result)


@track_command(operation="run-pipeline")
def run_pipeline(
    pipeline_name: str,
    job_ref: Optional[str] = None,
    follow: bool = False,
    refresh: bool = False,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    if job_ref:
        # --job-ref narrows to a specific job via manual: selector
        _do_launch(
            [],
            selector_or_job_ref=job_ref,
            default_selector=f"pipeline_name:{pipeline_name}",
            forbidden_job_type="interactive",
            follow=follow,
            refresh=refresh,
            auth_service=auth_service,
            api_client=api_client,
        )
    else:
        _do_launch(
            [f"pipeline_name:{pipeline_name}"],
            forbidden_job_type="interactive",
            follow=follow,
            refresh=refresh,
            auth_service=auth_service,
            api_client=api_client,
        )


@track_command(operation="publish")
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


@track_command(operation="serve", suboperation="publish")
def enable_public_link(
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


@track_command(operation="serve", suboperation="unpublish")
def disable_public_link(
    script_path: str, *, auth_service: RuntimeAuthService, api_client: ApiClient
) -> None:
    _disable_public_link_impl(
        script_path, auth_service=auth_service, api_client=api_client
    )


def _follow_run_status(
    run_id: UUID,
    is_batch: bool,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    final_states = {RunStatus.FAILED, RunStatus.CANCELLED}
    if is_batch:
        final_states.add(RunStatus.STARTING)
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


@track_command(operation="unpublish")
def unpublish(
    script_path: str, *, auth_service: RuntimeAuthService, api_client: ApiClient
) -> None:
    _disable_public_link_impl(
        script_path, auth_service=auth_service, api_client=api_client
    )


@track_command(operation="dashboard")
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
        except CliCommandInnerException as e:
            if f"No '{DEFAULT_DEPLOYMENT_MODULE}.py' file found" not in str(e):
                raise
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

    fmt.echo(f"Dashboard is available at {script_url}")
    webbrowser.open(script_url)


@track_command(operation="info")
def runtime_info(*, auth_service: RuntimeAuthService, api_client: ApiClient) -> None:
    from dlt_runtime._runtime_command_views import (
        _print_deploy_result,
        _print_runtime_info,
    )

    info = _fetch_runtime_info(auth_service=auth_service, api_client=api_client)
    _print_runtime_info(info)

    # Show the deploy reconciliation plan (same as `dlt runtime deploy --dry-run`).
    # Surface manifest-load errors as warnings and continue — `info` should
    # never fail because the local deployment module is broken.
    try:
        manifest, manifest_hash, api_jobs, warnings = _generate_local_manifest(
            DEFAULT_DEPLOYMENT_MODULE
        )
    except CliCommandInnerException as e:
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


@track_command(operation="jobs", suboperation="list")
def jobs_list(
    selectors: list[str] | None = None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    jobs = _resolve_selectors_to_scripts(
        selectors or [], api_client=api_client, auth_service=auth_service
    )
    _print_jobs(jobs)


@track_command(operation="jobs", suboperation="info")
def job_info(
    script_path_or_job_name: Optional[str] = None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    if not script_path_or_job_name:
        raise CliCommandInnerException(
            cmd="runtime",
            msg="Script path or job name is required",
        )
    script_path_or_job_name = _resolve_job_ref_from_server(
        script_path_or_job_name, auth_service=auth_service, api_client=api_client
    )
    job = _fetch_job_info(api_client, auth_service, script_path_or_job_name)
    _print_job_info(job)
