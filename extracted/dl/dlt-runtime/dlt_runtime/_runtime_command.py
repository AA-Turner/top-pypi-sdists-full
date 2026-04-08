# Python internals
import argparse
import json
import time
import webbrowser
from datetime import datetime
from functools import partial
from io import BytesIO
from pathlib import Path
from typing import Any, Optional, Set, Union
from uuid import UUID

# Other libraries
import httpx
from urllib.parse import urlparse
from cron_descriptor import FormatException, get_description
from dlt._workspace._workspace_context import active
from dlt._workspace.cli import echo as fmt
from dlt._workspace.cli.exceptions import CliCommandInnerException
from dlt._workspace.cli.utils import track_command as dlt_track_command
from dlt._workspace.deployment.file_selector import (
    ConfigurationFileSelector,
    WorkspaceFileSelector,
)
from dlt._workspace.deployment.package_builder import PackageBuilder
from tabulate import tabulate

from dlt_runtime.version import __version__

from dlt._workspace.exceptions import WorkspaceRunContextNotAvailable

from dlt_runtime.exceptions import (
    NoRunnableRun,
    NoRunsFound,
    RuntimeNotAuthenticated,
    RuntimeOperationNotAuthorized,
    exception_from_response,
    handle_client_exceptions,
)
from dlt_runtime.runtime import (
    RuntimeAuthService,
    UserInfo,
    WorkspaceInfo,
    get_auth_client,
)
from dlt_runtime.runtime_clients.api.api.configurations import (
    create_configuration,
    get_configuration,
    get_latest_configuration,
    list_configurations,
)
from dlt_runtime.runtime_clients.api.api.deployments import (
    create_deployment,
    get_deployment,
    get_latest_deployment,
    list_deployments,
)
from dlt_runtime.runtime_clients.api.api.runs import (
    cancel_run,
    create_run,
    get_run,
    get_run_logs,
    list_runs,
)
from dlt_runtime.runtime_clients.api.api.scripts import (
    create_or_update_script,
    disable_public_url,
    enable_public_url,
    get_script,
    list_scripts,
)
from dlt_runtime.runtime_clients.api.client import Client as ApiClient
from dlt_runtime.runtime_clients.api.models.create_deployment_body import (
    CreateDeploymentBody,
)
from dlt_runtime.runtime_clients.api.models.detailed_run_response import (
    DetailedRunResponse,
)
from dlt_runtime.runtime_clients.api.models.interactive_script_type import (
    InteractiveScriptType,
)
from dlt_runtime.runtime_clients.api.models.log_line import LogLine
from dlt_runtime.runtime_clients.api.models.run_status import RunStatus
from dlt_runtime.runtime_clients.api.models.script_type import ScriptType
from dlt_runtime.runtime_clients.api.types import File
from dlt_runtime.runtime_clients.auth.api.workos import (
    workos_device_flow_complete,
    workos_device_flow_start,
)
from dlt_runtime.runtime_clients.api.errors import (
    UnexpectedStatus as ApiUnexpectedStatus,
)
from dlt_runtime.runtime_clients.auth.errors import (
    UnexpectedStatus as AuthUnexpectedStatus,
)


def _format_log_line(log: LogLine) -> str:
    """
    Format a log line for CLI output.

    Format: [line_num] HH:MM:SS.mmm [phase] message
    Example: [   1] 14:30:45.123 [setup] Installing dependencies...
    """
    # Parse ISO timestamp and convert to local time
    try:
        if isinstance(log.reported_at, str):
            timestamp = datetime.fromisoformat(log.reported_at.replace("Z", "+00:00"))
        else:
            timestamp = log.reported_at

        # Format as HH:MM:SS.mmm in local time
        time_str = timestamp.astimezone().strftime("%H:%M:%S.%f")[:-3]
    except (ValueError, AttributeError):
        time_str = str(log.reported_at)

    # Format line number (right-aligned, 4 chars wide, 1-indexed)
    line_num = f"{log.line_num + 1:4d}"

    # Phase badge
    phase = f"[{log.phase}]"

    # Combine all parts
    return f"[{line_num}] {time_str} {phase:8s} {log.content}"


def _stream_run_logs(
    run_id: UUID,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    """
    Stream logs from the run stream endpoint using SSE.

    Displays logs in real-time as they are received from the server.
    """
    workspace_id = _to_uuid(auth_service.workspace_id)

    # Get the base URL and auth headers from the API client
    base_url = api_client._base_url.rstrip("/")
    stream_url = f"{base_url}/v1/workspaces/{workspace_id}/runs/{run_id}/logs/stream"

    headers = {
        "Accept": "text/event-stream",
        "User-Agent": f"dlt-runtime-cli/{__version__}",
    }

    if auth_service.auth_info:
        headers["Authorization"] = f"Bearer {auth_service.auth_info.jwt_token}"

    try:
        with httpx.stream(
            "GET", stream_url, headers=headers, timeout=None, verify=False
        ) as response:
            if response.status_code != 200:
                fmt.error(f"Failed to connect to log stream: {response.status_code}")
                return

            buffer = ""
            for chunk in response.iter_text():
                buffer += chunk
                lines = buffer.split("\n")
                buffer = lines.pop()  # Keep incomplete line in buffer

                for line in lines:
                    if line.startswith("data: "):
                        data = line[6:]  # Remove "data: " prefix
                        try:
                            log_data = json.loads(data)
                            # Create LogLine from the streamed data
                            log = LogLine(
                                phase=log_data["channel"],
                                line_num=log_data["line_num"],
                                reported_at=log_data["reported_at"],
                                content=log_data["content"],
                            )
                            fmt.echo(_format_log_line(log))
                        except (json.JSONDecodeError, KeyError) as e:
                            fmt.warning(f"Failed to parse log line: {e}")
                    elif line.startswith("event: error"):
                        fmt.error("Stream error event received")
                        return
    except httpx.HTTPError as e:
        fmt.error(f"HTTP error while streaming logs: {e}")
    except Exception as e:
        fmt.error(f"Error streaming logs: {e}")


DEPLOYMENT_HEADERS = {
    "version": fmt.bold("Version #"),
    "date_added": fmt.bold("Created at"),
    "file_count": fmt.bold("File count"),
    "content_hash": fmt.bold("Content hash"),
}
CONFIGURATION_HEADERS = {
    "version": fmt.bold("Version #"),
    "date_added": fmt.bold("Created at"),
    "file_count": fmt.bold("File count"),
    "content_hash": fmt.bold("Content hash"),
    "profiles": fmt.bold("Profiles"),
}
JOB_HEADERS = {
    "name": fmt.bold("Job name"),
    "version": fmt.bold("Version #"),
    "entry_point": fmt.bold("Script path"),
    "script_type": fmt.bold("Type"),
    "date_added": fmt.bold("Created at"),
    "schedule": fmt.bold("Schedule"),
    "script_url": fmt.bold("Script URL"),
}
JOB_RUN_HEADERS = {
    "job_name": fmt.bold("Job name"),
    "number": fmt.bold("Run #"),
    "status": fmt.bold("Status"),
    "trigger": fmt.bold("Trigger"),
    "profile": fmt.bold("Profile"),
    "time_started": fmt.bold("Started at"),
    "time_ended": fmt.bold("Ended at"),
    "duration": fmt.bold("Duration (s)"),
}
WORKSPACE_HEADERS = {
    "name": fmt.bold("Name"),
    "id": fmt.bold("ID"),
    "role": fmt.bold("Role"),
    "description": fmt.bold("Description"),
}


INTERACTIVE_APP_DETECTION_RULES: dict[InteractiveScriptType, list[str]] = {
    InteractiveScriptType.MARIMO: [
        "import marimo",
        "from marimo import",
        "marimo.App(",
    ],
    InteractiveScriptType.STREAMLIT: [
        "import streamlit",
        "import streamlit as st",
        "st.set_page_config",
        "st.title(",
    ],
    InteractiveScriptType.MCP: [
        "import fastmcp",
        "from fastmcp",
        "FastMCP(",
    ],
}


def _validate_interactive_script_type(
    script_path: Path,
    expected: InteractiveScriptType,
) -> bool:
    """
    Returns:
      True  -> content matches expected type
      False -> content contradicts expected type

    Raises:
      CliCommandInnerException if file cannot be read
    """
    try:
        content = script_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        raise CliCommandInnerException(
            cmd="runtime",
            msg="Failed to read script file for app type validation",
            inner_exc=e,
        )

    content_lower = content.lower()
    markers = INTERACTIVE_APP_DETECTION_RULES[expected]

    return any(marker.lower() in content_lower for marker in markers)


track_command = partial(dlt_track_command, "runtime", track_before=False)


def _to_uuid(value: Union[str, UUID]) -> UUID:
    if isinstance(value, UUID):
        return value
    try:
        return UUID(value)
    except ValueError:
        raise RuntimeError(f"Invalid UUID: {value}")


def _check_cron_expression(cron_expression: Optional[str]) -> None:
    if cron_expression:
        try:
            get_description(cron_expression)
        except FormatException as exc:
            raise CliCommandInnerException(
                cmd="runtime",
                msg=f"Invalid cron expression: {cron_expression} ({exc})",
                inner_exc=exc,
            )


def _get_web_ui_url() -> Optional[str]:
    """Derive the web UI URL from the configured api_base_url."""
    api_base_url = active().runtime_config.api_base_url
    if not api_base_url:
        return None
    parsed = urlparse(api_base_url)
    return f"{parsed.scheme}://{parsed.hostname}/"


def _extract_keys(data: dict[str, Any], keys_dict: dict[str, str]) -> dict[str, Any]:
    return {key: data[key] for key in keys_dict.keys() if key in data}


@track_command(operation="login")
def login(
    minimal_logging: bool = True, workspace: Optional[str] = None
) -> RuntimeAuthService:
    auth_service = RuntimeAuthService(run_context=active())
    try:
        auth_info = auth_service.authenticate()
        if not minimal_logging:
            fmt.secho("Already logged in as %s" % fmt.bold(auth_info.email), fg="green")
            web_ui_url = _get_web_ui_url()
            if web_ui_url:
                fmt.echo("  dltHub Runtime Web UI: %s" % fmt.bold(web_ui_url))
        user_info = auth_service.fetch_user_info()
        workspace_id = _resolve_workspace(user_info, workspace) if workspace else None
        _connect(
            auth_service=auth_service,
            user_info=user_info,
            minimal_logging=minimal_logging,
            workspace_id=workspace_id,
        )
        return auth_service
    except RuntimeNotAuthenticated:
        client = get_auth_client()
        # start device flow
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
                    # Not currently specified in Runtime Auth API spec, but it's returned
                    # while user hasn't yet finalized the login in the browser using the
                    # device_code provided. As with empty response, we're just retrying
                    # the request
                    continue
                raise exception_from_response(error_message, e) from e
            except Exception as e:
                error_message += f". Underlying error: {e}"
                raise RuntimeError(error_message) from e

            if isinstance(
                token_response.parsed, workos_device_flow_complete.LoginResponse
            ):
                auth_info, user_info = auth_service.login(
                    token_response.parsed.jwt,
                    refresh_token=token_response.parsed.refresh_token,
                )
                fmt.secho("Logged in as %s" % fmt.bold(auth_info.email), fg="green")
                web_ui_url = _get_web_ui_url()
                if web_ui_url:
                    fmt.echo("  dltHub Runtime Web UI: %s" % fmt.bold(web_ui_url))
                workspace_id = (
                    _resolve_workspace(user_info, workspace) if workspace else None
                )
                _connect(
                    auth_service=auth_service,
                    user_info=user_info,
                    workspace_id=workspace_id,
                )
                return auth_service
            elif isinstance(
                token_response.parsed, workos_device_flow_complete.ErrorResponse400
            ):
                raise exception_from_response(error_message, token_response)


@track_command(operation="logout")
def logout() -> None:
    auth_service = RuntimeAuthService(run_context=active())
    auth_service.logout()
    fmt.echo("Logged out")


def _require_auth() -> tuple[RuntimeAuthService, UserInfo]:
    """Authenticate and return (auth_service, user_info), or raise a CLI error."""
    auth_service = RuntimeAuthService(run_context=active())
    try:
        auth_service.authenticate()
    except RuntimeNotAuthenticated:
        raise CliCommandInnerException(
            cmd="runtime",
            msg="Not logged in. Run 'dlt runtime login' first.",
        )
    return auth_service, auth_service.fetch_user_info()


@track_command(operation="workspace", suboperation="list")
def workspace_list() -> None:
    """List all workspaces the authenticated user has access to.

    Uses only authenticate() — does NOT require a workspace to be connected.
    This allows the command to work before workspace selection.
    """
    auth_service, user_info = _require_auth()
    if not user_info.workspaces:
        fmt.echo("No workspaces found")
        return

    # Determine the currently connected workspace ID (if any)
    try:
        current_ws_id = auth_service.workspace_id
    except (RuntimeOperationNotAuthorized, WorkspaceRunContextNotAvailable):
        current_ws_id = None

    rows = []
    for ws in user_info.workspaces:
        name = ws.name
        if ws.id == current_ws_id:
            name = f"* {name}"
        rows.append(
            {
                "name": name,
                "id": ws.id,
                "role": ws.role or "",
                "description": ws.description or "",
            }
        )

    fmt.echo(tabulate(rows, headers=WORKSPACE_HEADERS))


@track_command(operation="workspace", suboperation="switch")
def workspace_switch(workspace: str) -> None:
    """Switch the locally connected workspace by name or ID.

    Uses only authenticate() — does NOT trigger the full login/OAuth flow.
    """
    auth_service, user_info = _require_auth()
    workspace_id = _resolve_workspace(user_info, workspace)
    auth_service.overwrite_local_workspace_id(workspace_id)
    ws_name = _get_workspace_name(user_info, workspace_id)
    ws_id_dim = fmt.style(workspace_id, dim=True)
    if ws_name:
        ws_label = "%s %s" % (fmt.bold(ws_name), ws_id_dim)
    else:
        ws_label = ws_id_dim
    fmt.echo("Switched to workspace: %s" % ws_label)


def _get_workspace_name(user_info: UserInfo, workspace_id: str) -> Optional[str]:
    """Look up the workspace name for the currently connected workspace."""
    for ws in user_info.workspaces:
        if ws.id == workspace_id:
            return ws.name
    return None


def _connect(
    auth_service: RuntimeAuthService,
    user_info: UserInfo,
    minimal_logging: bool = False,
    workspace_id: Optional[str] = None,
) -> None:
    if workspace_id is not None:
        auth_service.overwrite_local_workspace_id(workspace_id)
    else:
        remote_ids = [ws.id for ws in user_info.workspaces]
        local_ws_id = auth_service.workspace_run_context.runtime_config.workspace_id

        selected_id: Optional[str] = None
        if not local_ws_id:
            fmt.echo(
                "\nIt seems your local workspace is not connected to any remote one on dltHub Runtime."
            )
            selected_id = _select_or_create_workspace(auth_service, user_info)
        elif remote_ids and local_ws_id not in remote_ids:
            fmt.warning(
                "\nWorkspace id in local config (%s) does not match any remote workspace id on dltHub Runtime."
                % local_ws_id,
            )
            selected_id = _select_or_create_workspace(auth_service, user_info)

        if selected_id is not None:
            auth_service.overwrite_local_workspace_id(selected_id)

    if not minimal_logging:
        ws_id = auth_service.workspace_id
        ws_name = _get_workspace_name(user_info, ws_id)
        ws_id_dim = fmt.style(ws_id, dim=True)
        if ws_name:
            ws_label = "%s %s" % (fmt.bold(ws_name), ws_id_dim)
        else:
            ws_label = ws_id_dim
        fmt.echo("  Connected workspace:   %s" % ws_label)
        fmt.echo("  Local directory:       %s" % fmt.bold(active().run_dir))


def _prompt_workspace_selection(
    workspaces: list[WorkspaceInfo],
) -> Optional[WorkspaceInfo]:
    """
    Display an interactive menu for workspace selection.
    Returns the selected WorkspaceResponse, or None if user chooses to create a new workspace.

    fmt/click requires the user to type full choice string which is very inconvenient here, so
    using our own choice processing here
    """
    fmt.echo(f"  {fmt.bold('[0]')} Create new workspace")
    for idx, ws in enumerate(workspaces, start=1):
        ws_id_dim = fmt.style(ws.id, dim=True)
        fmt.echo(f"  {fmt.bold(f'[{idx}]')} {fmt.bold(ws.name)} {ws_id_dim}")
        if ws.description:
            fmt.echo(f"       {ws.description}")
    fmt.echo("")

    while True:
        try:
            choice = input("Select a workspace (enter number): ")
            choice_num = int(choice)
            if choice_num == 0:
                return None  # User wants to create new workspace
            elif 1 <= choice_num <= len(workspaces):
                return workspaces[choice_num - 1]
            else:
                fmt.warning(f"Please enter a number between 0 and {len(workspaces)}")
        except ValueError:
            fmt.warning("Please enter a valid number")
        except (EOFError, KeyboardInterrupt):
            raise RuntimeError("Workspace selection cancelled")


def _prompt_and_create_new_workspace(
    auth_service: RuntimeAuthService, user_info: UserInfo
) -> str:
    """Prompt user for workspace name and optional description."""
    fmt.echo("\nCreating a new workspace...")
    name = input("Workspace name (leave empty for `default`): ")
    if not name:
        name = "default"
    description = input("Workspace description (optional): ")

    new_ws_id = auth_service.create_new_workspace(user_info, name, description)
    fmt.echo(f"Created workspace with id: {fmt.bold(new_ws_id)}")
    # Add to user_info so _get_workspace_name can find it later
    user_info.workspaces.append(
        WorkspaceInfo(id=new_ws_id, name=name, description=description, role="owner")
    )
    return new_ws_id


def _resolve_workspace(user_info: UserInfo, workspace: str) -> str:
    """Resolve a workspace name or ID to a verified workspace ID.

    Only considers owned workspaces. When matching by name, fails if multiple
    workspaces share the same name to keep behaviour deterministic.
    """
    workspace = workspace.strip()

    # Exact ID match is always unambiguous — return immediately.
    for ws in user_info.workspaces:
        if ws.role == "owner" and workspace == ws.id:
            return ws.id

    # Name match — collect all owned workspaces with this name.
    matches = [
        ws for ws in user_info.workspaces if ws.role == "owner" and ws.name == workspace
    ]

    if len(matches) == 1:
        return matches[0].id

    if len(matches) > 1:
        ids = ", ".join(ws.id for ws in matches)
        raise CliCommandInnerException(
            cmd="runtime",
            msg=(
                f"Multiple owned workspaces are named '{workspace}' ({ids}). "
                "Pass the workspace ID instead to avoid ambiguity."
            ),
        )

    raise CliCommandInnerException(
        cmd="runtime",
        msg=f"Workspace '{workspace}' not found among your owned workspaces.",
    )


def _select_or_create_workspace(
    auth_service: RuntimeAuthService, user_info: UserInfo
) -> str:
    """
    Interactive workspace selection flow.
    Returns the selected or newly created workspace ID as string.
    Only workspaces where the user has the 'owner' role are shown.
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

    if len(owned) == 1:
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


@track_command(operation="deploy")
def deploy(*, auth_service: RuntimeAuthService, api_client: ApiClient) -> None:
    _sync_deployment(
        minimal_logging=False, auth_service=auth_service, api_client=api_client
    )
    _sync_configuration(
        minimal_logging=False, auth_service=auth_service, api_client=api_client
    )
    fmt.echo("Deployment and Configuration synchronized successfully")


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
) -> None:
    content_stream = BytesIO()
    package_builder = PackageBuilder(context=active())
    package_hash = package_builder.write_package_to_stream(
        file_selector=WorkspaceFileSelector(active()), output_stream=content_stream
    )
    with handle_client_exceptions():
        latest_deployment = get_latest_deployment.sync_detailed(
            workspace_id=_to_uuid(auth_service.workspace_id),
            client=api_client,
        )
    if isinstance(latest_deployment.parsed, get_latest_deployment.DeploymentResponse):
        if latest_deployment.parsed.content_hash == package_hash:
            if not minimal_logging:
                fmt.echo("No changes detected in the deployment, skipping file upload")
            content_stream.close()
            return
    elif isinstance(latest_deployment.parsed, get_latest_deployment.ErrorResponse404):
        if not minimal_logging:
            fmt.echo("No deployment found in this workspace, creating new deployment")
    else:
        content_stream.close()
        raise exception_from_response(
            "Failed to get latest deployment", latest_deployment
        )

    with handle_client_exceptions():
        create_deployment_result = create_deployment.sync_detailed(
            workspace_id=_to_uuid(auth_service.workspace_id),
            client=api_client,
            body=CreateDeploymentBody(
                file=File(
                    payload=content_stream,
                    file_name="workspace.tar.gz",
                    mime_type="application/x-tar",
                )
            ),
        )
    if isinstance(
        create_deployment_result.parsed, create_deployment.DeploymentResponse
    ):
        if not minimal_logging:
            fmt.echo(
                tabulate(
                    [
                        _extract_keys(
                            create_deployment_result.parsed.to_dict(),
                            DEPLOYMENT_HEADERS,
                        )
                    ],
                    headers=DEPLOYMENT_HEADERS,
                )
            )
    else:
        raise exception_from_response(
            "Failed to create deployment", create_deployment_result
        )


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
) -> None:
    content_stream = BytesIO()
    package_builder = PackageBuilder(context=active())
    package_hash = package_builder.write_package_to_stream(
        file_selector=ConfigurationFileSelector(active()), output_stream=content_stream
    )

    with handle_client_exceptions():
        latest_configuration = get_latest_configuration.sync_detailed(
            workspace_id=_to_uuid(auth_service.workspace_id),
            client=api_client,
        )
    if isinstance(
        latest_configuration.parsed, get_latest_configuration.ConfigurationResponse
    ):
        if latest_configuration.parsed.content_hash == package_hash:
            if not minimal_logging:
                fmt.echo(
                    "No changes detected in the configuration, skipping file upload"
                )
            content_stream.close()
            return
    elif isinstance(
        latest_configuration.parsed,
        get_latest_configuration.ErrorResponse404,
    ):
        if not minimal_logging:
            fmt.echo(
                "No configuration found in this workspace, creating new configuration"
            )
    else:
        content_stream.close()
        raise exception_from_response(
            "Failed to get latest configuration", latest_configuration
        )

    with handle_client_exceptions():
        create_configuration_result = create_configuration.sync_detailed(
            workspace_id=_to_uuid(auth_service.workspace_id),
            client=api_client,
            body=create_configuration.CreateConfigurationBody(
                file=File(
                    payload=content_stream,
                    file_name="configurations.tar.gz",
                    mime_type="application/x-tar",
                )
            ),
        )
    if isinstance(
        create_configuration_result.parsed, create_configuration.ConfigurationResponse
    ):
        if not minimal_logging:
            fmt.echo(
                tabulate(
                    [
                        _extract_keys(
                            create_configuration_result.parsed.to_dict(),
                            CONFIGURATION_HEADERS,
                        )
                    ],
                    headers=CONFIGURATION_HEADERS,
                )
            )
    else:
        raise exception_from_response(
            "Failed to create configuration", create_configuration_result
        )


def _preprocess_run_output(
    run: dict[str, Any], headers: dict[str, str]
) -> dict[str, Any]:
    result = _extract_keys(run, headers)
    result["job_name"] = run["script"]["name"]
    return {key: result[key] for key in headers.keys() if key in result}


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
    if run_number is None:
        run = _get_latest_run(api_client, auth_service, script_path_or_job_name)
        run_id = run.id
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
            run_id=_to_uuid(run_id),
        )
    if isinstance(get_run_result.parsed, get_run.DetailedRunResponse):
        fmt.echo(
            tabulate(
                [_extract_keys(get_run_result.parsed.to_dict(), JOB_RUN_HEADERS)],
                headers=JOB_RUN_HEADERS,
            )
        )

    else:
        raise exception_from_response("Failed to get run status", get_run_result)


@track_command(operation="logs")
def logs(
    script_path_or_job_name: Optional[str] = None,
    run_number: Optional[int] = None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    # Note: follow parameter is deprecated, streaming is automatic for non-terminal runs
    _fetch_run_logs(
        script_path_or_job_name,
        run_number,
        auth_service=auth_service,
        api_client=api_client,
    )


@track_command(operation="job-runs", suboperation="logs")
def job_run_logs(
    script_path_or_job_name: Optional[str] = None,
    run_number: Optional[int] = None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    # Note: follow parameter is deprecated, streaming is automatic for non-terminal runs
    _fetch_run_logs(
        script_path_or_job_name,
        run_number,
        auth_service=auth_service,
        api_client=api_client,
    )


def _fetch_run_logs(
    script_path_or_job_name: Optional[str] = None,
    run_number: Optional[int] = None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    """Get logs for a run of job (latest if run number not provided)."""
    if script_path_or_job_name is None:
        raise CliCommandInnerException(
            cmd="runtime",
            msg="Script path or job name is required",
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

    # If finalizing, wait until the run reaches a true terminal state (logs aren't ready yet during FINALIZING)
    if run_status == RunStatus.FINALIZING:
        _follow_job_run(
            run_id,
            terminal_states,
            run_status,
            follow_logs=False,
            auth_service=auth_service,
            api_client=api_client,
        )
        # Re-fetch the status after waiting
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
        fmt.echo(f"========== Streaming logs for run (status: {run_status}) ==========")
        _stream_run_logs(
            run_id,
            auth_service=auth_service,
            api_client=api_client,
        )
        fmt.echo("========== End of log stream ==========")


@track_command(operation="job-runs", suboperation="list")
def get_runs(
    script_path_or_job_name: Optional[str] = None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    script_id: Optional[UUID] = None
    if script_path_or_job_name:
        with handle_client_exceptions():
            script = get_script.sync_detailed(
                client=api_client,
                workspace_id=_to_uuid(auth_service.workspace_id),
                script_id_or_name=script_path_or_job_name,
            )
        if isinstance(script.parsed, get_script.DetailedScriptResponse):
            script_id = script.parsed.id
        else:
            raise exception_from_response(
                f"Failed to get script with name {script_path_or_job_name} from runtime. Did you"
                " create one?",
                script,
            )

    with handle_client_exceptions():
        list_runs_result = list_runs.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            script_id=script_id,
        )
    if isinstance(list_runs_result.parsed, list_runs.ListRunsResponse200):
        if not list_runs_result.parsed.items:
            fmt.echo("No runs found in this workspace")
            return
        fmt.echo(
            tabulate(
                [
                    _preprocess_run_output(run.to_dict(), JOB_RUN_HEADERS)
                    for run in reversed(list_runs_result.parsed.items)
                ],
                headers=JOB_RUN_HEADERS,
            )
        )
    else:
        raise exception_from_response("Failed to list workspace runs", list_runs_result)


@track_command(operation="deployment", suboperation="list")
def get_deployments(*, auth_service: RuntimeAuthService, api_client: ApiClient) -> None:
    with handle_client_exceptions():
        list_deployments_result = list_deployments.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
        )
    if isinstance(
        list_deployments_result.parsed, list_deployments.ListDeploymentsResponse200
    ):
        if not list_deployments_result.parsed.items:
            fmt.echo("No deployments found in this workspace")
            return
        fmt.echo(
            tabulate(
                [
                    _extract_keys(deployment.to_dict(), DEPLOYMENT_HEADERS)
                    for deployment in reversed(list_deployments_result.parsed.items)
                ],
                headers=DEPLOYMENT_HEADERS,
            )
        )
    else:
        raise exception_from_response(
            "Failed to list deployments", list_deployments_result
        )


@track_command(operation="deployment", suboperation="info")
def get_deployment_info(
    deployment_version_no: Optional[int] = None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    get_deployment_result: Any
    if deployment_version_no is None:
        with handle_client_exceptions():
            get_deployment_result = get_latest_deployment.sync_detailed(
                client=api_client,
                workspace_id=_to_uuid(auth_service.workspace_id),
            )
    else:
        with handle_client_exceptions():
            get_deployment_result = get_deployment.sync_detailed(
                client=api_client,
                workspace_id=_to_uuid(auth_service.workspace_id),
                deployment_id_or_version=deployment_version_no,
            )
    if isinstance(get_deployment_result.parsed, get_deployment.DeploymentResponse):
        fmt.echo(
            tabulate(
                [
                    _extract_keys(
                        get_deployment_result.parsed.to_dict(), DEPLOYMENT_HEADERS
                    )
                ],
                headers=DEPLOYMENT_HEADERS,
            )
        )
    else:
        raise exception_from_response(
            "Failed to get deployment info", get_deployment_result
        )


@track_command(operation="cancel")
def cancel(
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
    terminal_states = {
        RunStatus.FAILED,
        RunStatus.CANCELLED,
        RunStatus.COMPLETED,
        RunStatus.FINALIZING,
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


def _get_latest_run(
    api_client: ApiClient,
    auth_service: RuntimeAuthService,
    script_id_or_name: Optional[str] = None,
) -> DetailedRunResponse:
    """Get the latest run for a script or workspace if script is not provided"""
    if script_id_or_name:
        with handle_client_exceptions():
            script = get_script.sync_detailed(
                client=api_client,
                workspace_id=_to_uuid(auth_service.workspace_id),
                script_id_or_name=script_id_or_name,
            )
        if isinstance(script.parsed, get_script.DetailedScriptResponse):
            fmt.echo(f"Job {script.parsed.name} found on runtime.")
            with handle_client_exceptions():
                runs = list_runs.sync_detailed(
                    client=api_client,
                    workspace_id=_to_uuid(auth_service.workspace_id),
                    script_id=script.parsed.id,
                    limit=1,
                )
            if isinstance(runs.parsed, list_runs.ListRunsResponse200):
                if not runs.parsed.items:
                    raise NoRunsFound("No runs executed for this job")
                else:
                    return runs.parsed.items[0]
            raise exception_from_response(
                f"Failed to get runs for script with name or id {script_id_or_name}",
                runs,
            )
        else:
            raise exception_from_response(
                f"Failed to get script with name or id {script_id_or_name}", script
            )

    else:
        with handle_client_exceptions():
            runs = list_runs.sync_detailed(
                client=api_client,
                workspace_id=_to_uuid(auth_service.workspace_id),
                limit=1,
            )
        if isinstance(runs.parsed, list_runs.ListRunsResponse200):
            if not runs.parsed.items:
                raise NoRunsFound("No runs executed in this workspace")
            else:
                return runs.parsed.items[0]
        raise exception_from_response("Failed to get runs for workspace", runs)


def _cancel_active_run_if_exists(
    script_name: str,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    """If the script has an active run, cancel it and wait for termination."""
    active_states = {RunStatus.PENDING, RunStatus.STARTING, RunStatus.RUNNING}
    transitional_states = {RunStatus.CANCELLING, RunStatus.FINALIZING}
    terminal_states = {
        RunStatus.FAILED,
        RunStatus.CANCELLED,
        RunStatus.COMPLETED,
        RunStatus.SKIPPED,
    }

    try:
        latest_run = _get_latest_run(api_client, auth_service, script_name)
    except (NoRunsFound, CliCommandInnerException):
        return  # script not found or no runs — nothing to cancel

    assert latest_run.script.script_type == ScriptType.INTERACTIVE, (
        f"Auto-cancel is only safe for interactive scripts, got {latest_run.script.script_type}"
    )

    if latest_run.status in terminal_states:
        return  # already done

    needs_cancel = latest_run.status in active_states

    if needs_cancel:
        fmt.echo(
            f"Found existing run # {latest_run.number} ({latest_run.status}), cancelling..."
        )
        try:
            with handle_client_exceptions():
                cancel_result = cancel_run.sync_detailed(
                    client=api_client,
                    workspace_id=_to_uuid(auth_service.workspace_id),
                    run_id=latest_run.id,
                )
            if not isinstance(cancel_result.parsed, cancel_run.DetailedRunResponse):
                raise exception_from_response(
                    "Failed to cancel existing run", cancel_result
                )
        except (CliCommandInnerException, ApiUnexpectedStatus):
            # Run may have reached a terminal state between the check and the
            # cancel request (race condition).  Fall through to polling which
            # will confirm the terminal state.
            pass
    elif latest_run.status in transitional_states:
        fmt.echo(
            f"Existing run # {latest_run.number} is {latest_run.status}, waiting for it to finish..."
        )

    # Wait for terminal state
    _follow_job_run(
        latest_run.id,
        terminal_states,
        auth_service=auth_service,
        api_client=api_client,
    )


@track_command(operation="configuration", suboperation="list")
def get_configurations(
    *, auth_service: RuntimeAuthService, api_client: ApiClient
) -> None:
    with handle_client_exceptions():
        list_configurations_result = list_configurations.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
        )
    if isinstance(
        list_configurations_result.parsed,
        list_configurations.ListConfigurationsResponse200,
    ) and isinstance(list_configurations_result.parsed.items, list):
        if not list_configurations_result.parsed.items:
            fmt.echo("No configurations found in this workspace")
            return
        fmt.echo(
            tabulate(
                [
                    _extract_keys(configuration.to_dict(), CONFIGURATION_HEADERS)
                    for configuration in reversed(
                        list_configurations_result.parsed.items
                    )
                ],
                headers=CONFIGURATION_HEADERS,
            )
        )
    else:
        raise exception_from_response(
            "Failed to list configurations", list_configurations_result
        )


@track_command(operation="configuration", suboperation="info")
def get_configuration_info(
    configuration_version_no: Optional[int] = None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    get_configuration_result: Any
    if configuration_version_no is None:
        with handle_client_exceptions():
            get_configuration_result = get_latest_configuration.sync_detailed(
                client=api_client,
                workspace_id=_to_uuid(auth_service.workspace_id),
            )
    else:
        with handle_client_exceptions():
            get_configuration_result = get_configuration.sync_detailed(
                client=api_client,
                workspace_id=_to_uuid(auth_service.workspace_id),
                configuration_id_or_version=configuration_version_no,
            )
    if isinstance(
        get_configuration_result.parsed, get_configuration.ConfigurationResponse
    ):
        fmt.echo(
            tabulate(
                [
                    _extract_keys(
                        get_configuration_result.parsed.to_dict(), CONFIGURATION_HEADERS
                    )
                ],
                headers=CONFIGURATION_HEADERS,
            )
        )
    else:
        raise exception_from_response(
            "Failed to get configuration info", get_configuration_result
        )


def _ensure_profile_warning(required_profile: str) -> bool:
    """Warn if recommended profile is not set up."""
    try:
        ctx = active()
        available = set(ctx.available_profiles())
        if required_profile not in available:
            if required_profile == "access":
                fmt.warning(
                    "No 'access' profile detected. Only default config/secrets will be used. "
                    "Dashboard/notebook sharing may be limited."
                )
            elif required_profile == "prod":
                fmt.warning(
                    "No 'prod' profile detected. Only default config/secrets will be used."
                )
            return False
        return True
    except Exception:
        # Fallback silent; lack of profiles is non-fatal
        return False


def _resolve_run_id_by_number(
    *,
    api_client: ApiClient,
    auth_service: RuntimeAuthService,
    script_path_or_job_name: str,
    run_number: int,
) -> UUID:
    with handle_client_exceptions():
        script = get_script.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            script_id_or_name=script_path_or_job_name,
        )
    if not isinstance(script.parsed, get_script.DetailedScriptResponse):
        raise exception_from_response(
            f"Failed to get script with name or id {script_path_or_job_name}", script
        )
    with handle_client_exceptions():
        runs = list_runs.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            script_id=script.parsed.id,
        )
    if (
        not isinstance(runs.parsed, list_runs.ListRunsResponse200)
        or not runs.parsed.items
    ):
        raise exception_from_response("Failed to get runs for script", runs)
    for r in runs.parsed.items:
        if r.number == run_number:
            return r.id
    raise CliCommandInnerException(
        cmd="runtime",
        msg=f"Run number {run_number} not found for script/job {script_path_or_job_name}",
    )


# Convenience commands


@track_command(operation="launch")
def launch(
    script_path: str,
    follow: bool = False,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    _ensure_profile_warning("prod")
    script_path_obj = Path(active().run_dir) / script_path
    if not script_path_obj.exists() or not script_path_obj.is_file():
        raise CliCommandInnerException(
            cmd="runtime",
            msg="Provided script path does not exist locally",
        )
    # Sync and run
    _sync_deployment(auth_service=auth_service, api_client=api_client)
    _sync_configuration(auth_service=auth_service, api_client=api_client)
    run_response = _run_script(
        script_path_obj,
        ScriptType.BATCH,
        auth_service=auth_service,
        api_client=api_client,
    )
    if follow:
        # Show status and then logs for latest run
        _follow_run_status(
            run_response.id, True, auth_service=auth_service, api_client=api_client
        )
        _follow_run_logs(
            run_response.id,
            auth_service=auth_service,
            api_client=api_client,
        )
    else:
        fmt.echo(f"  Job:        {run_response.script.name}")
        fmt.echo(f"  Run #:      {run_response.number}")
        fmt.echo(f"  Status:     {run_response.status.value}")
        fmt.echo("")
        fmt.echo(f"To follow logs: dlt runtime logs {script_path}")
        fmt.echo(
            f"To see logs about this specific run: dlt runtime logs {script_path}"
            f" {run_response.number}"
        )


@track_command(operation="serve")
def serve(
    script_path: str,
    interactive_script_type: InteractiveScriptType | None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    _ensure_profile_warning("access")
    script_path_obj = Path(active().run_dir) / script_path
    if not script_path_obj.exists() or not script_path_obj.is_file():
        raise CliCommandInnerException(
            cmd="runtime",
            msg="Provided script path does not exist locally",
        )
    user_provided_type = interactive_script_type
    # If no interactive script type provided, we fall back to marimo
    if interactive_script_type is None:
        interactive_script_type = InteractiveScriptType.MARIMO
    elif isinstance(interactive_script_type, str):
        interactive_script_type = InteractiveScriptType(interactive_script_type)

    valid = _validate_interactive_script_type(script_path_obj, interactive_script_type)

    if not valid:
        if user_provided_type:
            fmt.warning(
                f"Could not detect a {interactive_script_type} in the provided script. "
                f"Proceeding to serve as an interactive app as python {script_path}"
            )
        else:
            raise CliCommandInnerException(
                cmd="runtime",
                msg=f"We could not validate that {script_path} is a {interactive_script_type} app.",
            )

    # Sync and run interactive
    _sync_deployment(auth_service=auth_service, api_client=api_client)
    _sync_configuration(auth_service=auth_service, api_client=api_client)
    _cancel_active_run_if_exists(
        script_path_obj.name,
        auth_service=auth_service,
        api_client=api_client,
    )
    run_response = _run_script(
        script_path_obj,
        ScriptType.INTERACTIVE,
        interactive_script_type=interactive_script_type,
        auth_service=auth_service,
        api_client=api_client,
    )
    # Follow until ready: show status
    is_batch = False
    _follow_run_status(
        run_response.id, is_batch, auth_service=auth_service, api_client=api_client
    )

    # Open the application URL
    try:
        with handle_client_exceptions():
            res = get_script.sync_detailed(
                client=api_client,
                workspace_id=_to_uuid(auth_service.workspace_id),
                script_id_or_name=script_path,
            )
        if isinstance(res.parsed, get_script.DetailedScriptResponse):
            url = res.parsed.script_url
            assert isinstance(url, str)
            fmt.echo(f"Opening {url}")
            webbrowser.open(url, new=2, autoraise=True)
    except Exception:
        # Non-fatal if we cannot resolve or open URL
        fmt.warning(f"Failed to open application URL for script {script_path}")


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

    with handle_client_exceptions():
        script = get_script.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            script_id_or_name=script_path,
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
                script_id_or_name=script_path,
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
            script_id_or_name=script_path,
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

    with handle_client_exceptions():
        script = get_script.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            script_id_or_name=script_path,
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
            script_id_or_name=script_path,
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

    with handle_client_exceptions():
        script = get_script.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            script_id_or_name=script_path,
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
            script_id_or_name=script_path,
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


def _run_script(
    script_path: Path,
    script_type: ScriptType,
    interactive_script_type: Optional[InteractiveScriptType] = None,
    profile: Optional[str] = None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> "create_run.DetailedRunResponse":
    if interactive_script_type and script_type != ScriptType.INTERACTIVE:
        raise CliCommandInnerException(
            cmd="runtime",
            msg=(
                "--app-type can only be used with interactive jobs. "
                "Either add --interactive or remove --app-type."
            ),
        )

    script_file_name = script_path.name
    with handle_client_exceptions():
        create_script_result = create_or_update_script.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            body=create_or_update_script.CreateScriptRequest(
                name=script_file_name,
                description=f"The {script_file_name} script",
                entry_point=script_file_name,
                script_type=script_type,
                interactive_script_type=interactive_script_type,
                profile=profile,
            ),
        )
    if not isinstance(
        create_script_result.parsed, create_or_update_script.ScriptResponse
    ):
        raise exception_from_response("Failed to create script", create_script_result)
    else:
        fmt.echo(
            f"Job {script_file_name} created or updated successfully, version #:"
            f" {create_script_result.parsed.version}"
        )

    with handle_client_exceptions():
        create_run_result = create_run.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            body=create_run.CreateRunRequest(
                script_id_or_name_or_secret=script_file_name,
                profile=None,
            ),
        )
    if isinstance(create_run_result.parsed, create_run.DetailedRunResponse):
        fmt.echo("Job %s run successfully" % (fmt.bold(str(script_file_name))))
        if script_type == ScriptType.INTERACTIVE:
            url = create_script_result.parsed.script_url
            fmt.echo(f"Job is accessible at {url}")
        return create_run_result.parsed
    else:
        raise exception_from_response("Failed to run script", create_run_result)


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
            auth_service=auth_service,
            api_client=api_client,
        )
        fmt.echo("========== End of run logs ==========")
        return

    # Follow status changes without logs
    status = start_status
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


@track_command(operation="schedule")
def schedule(
    script_path: str,
    cron: Optional[str],
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    if not cron:
        raise CliCommandInnerException(
            cmd="runtime",
            msg=(
                "Cron schedule must be provided: dlt runtime schedule <SCRIPT_PATH> <SCHEDULE_CRON>"
            ),
        )
    _check_cron_expression(cron)
    _ensure_profile_warning("prod")

    # Ensure deployment/configuration in place
    _sync_deployment(auth_service=auth_service, api_client=api_client)
    _sync_configuration(auth_service=auth_service, api_client=api_client)

    # Upsert script with schedule
    with handle_client_exceptions():
        upsert = create_or_update_script.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            body=create_or_update_script.CreateScriptRequest(
                name=script_path,
                description=f"The {script_path} scheduled job",
                entry_point=script_path,
                script_type=ScriptType.BATCH,
                schedule=cron,
            ),
        )
    if isinstance(upsert.parsed, create_or_update_script.ScriptResponse):
        fmt.echo(
            f"Scheduled {fmt.bold(script_path)} with cron {fmt.bold(cron)}. Job version #:"
            f" {upsert.parsed.version}"
        )
    else:
        raise exception_from_response("Failed to schedule script", upsert)


def _schedule_cancel_impl(
    script_path: str,
    cancel_current: bool = False,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    with handle_client_exceptions():
        existing_script = get_script.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            script_id_or_name=script_path,
        )
    if isinstance(existing_script.parsed, get_script.DetailedScriptResponse):
        if not isinstance(existing_script.parsed.schedule, str):
            raise CliCommandInnerException(
                cmd="runtime", msg=f"{script_path} is not a scheduled job"
            )
    else:
        raise exception_from_response("Failed to get job", existing_script)

    # Unset schedule
    with handle_client_exceptions():
        upsert = create_or_update_script.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            body=create_or_update_script.CreateScriptRequest(
                name=script_path,
                description=f"The {script_path} job",
                entry_point=script_path,
                script_type=ScriptType.BATCH,
                schedule=None,
            ),
        )
    if isinstance(upsert.parsed, create_or_update_script.ScriptResponse):
        fmt.echo(f"Cancelled schedule for {fmt.bold(script_path)}")
    else:
        raise exception_from_response("Failed to cancel schedule", upsert)
    if cancel_current:
        try:
            _request_run_cancel(
                script_path, auth_service=auth_service, api_client=api_client
            )
        except (NoRunnableRun, NoRunsFound):
            pass


@track_command(operation="schedule", suboperation="cancel")
def schedule_cancel(
    script_path: str,
    cancel_current: bool = False,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    _schedule_cancel_impl(
        script_path,
        cancel_current,
        auth_service=auth_service,
        api_client=api_client,
    )


@track_command(operation="unschedule")
def unschedule(
    script_path: str,
    cancel_current: bool = False,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    _schedule_cancel_impl(
        script_path,
        cancel_current,
        auth_service=auth_service,
        api_client=api_client,
    )


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
    # Check deployment exists
    with handle_client_exceptions():
        latest_deployment = get_latest_deployment.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
        )
    if isinstance(latest_deployment.parsed, get_latest_deployment.DeploymentResponse):
        pass
    elif isinstance(latest_deployment.parsed, get_latest_deployment.ErrorResponse404):
        raise exception_from_response(
            "No deployment found for this workspace. Dashboard is not available until you create a deployment",
            latest_deployment,
        )
    else:
        raise exception_from_response(
            "Failed to get latest deployment", latest_deployment
        )

    with handle_client_exceptions():
        resp = get_script.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            script_id_or_name="dashboard",
        )

    if isinstance(resp.parsed, get_script.DetailedScriptResponse):
        script_url = resp.parsed.script_url

    elif isinstance(resp.parsed, get_script.ErrorResponse404):
        with handle_client_exceptions():
            create_resp = create_or_update_script.sync_detailed(
                client=api_client,
                workspace_id=_to_uuid(auth_service.workspace_id),
                body=create_or_update_script.CreateScriptRequest(
                    name="dashboard",
                    description="dlt dashboard",
                    entry_point="dashboard",
                    script_type=ScriptType.INTERACTIVE,
                    interactive_script_type=InteractiveScriptType.MARIMO,
                    schedule=None,
                ),
            )

        if isinstance(create_resp.parsed, create_or_update_script.ScriptResponse):
            script_url = create_resp.parsed.script_url
        else:
            raise exception_from_response(
                "Failed to create dashboard script", create_resp
            )

    else:
        raise exception_from_response("Failed to get dashboard job", resp)

    if not script_url:
        fmt.error("Failed to get the URL for the dashboard")
        return

    fmt.echo(f"Dashboard is available at {script_url}")
    webbrowser.open(script_url)


@track_command(operation="info")
def runtime_info(*, auth_service: RuntimeAuthService, api_client: ApiClient) -> None:
    # workspace info
    user_info = auth_service.fetch_user_info()
    ws_id = auth_service.workspace_id
    ws_name = _get_workspace_name(user_info, ws_id)
    if ws_name:
        fmt.echo(f"Workspace: {fmt.bold(ws_name)} ({ws_id})")
    else:
        fmt.echo(f"Workspace: {ws_id}")
    fmt.echo(f"Local directory: {fmt.bold(str(active().run_dir))}")
    fmt.echo("")

    # jobs
    with handle_client_exceptions():
        scr = list_scripts.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
        )
    job_count = (
        len(scr.parsed.items)
        if isinstance(scr.parsed, list_scripts.ListScriptsResponse200)
        and scr.parsed.items
        else 0
    )
    fmt.echo(f"# registered jobs: {job_count}. Run `dlt runtime job list` to see all")

    # last job run

    try:
        latest_run = _get_latest_run(api_client, auth_service)
    except NoRunsFound:
        latest_run = None
    if isinstance(latest_run, DetailedRunResponse):
        fmt.echo(
            f"Latest job run: {latest_run.script.name} ({latest_run.status}), started at"
            f" {latest_run.time_started}, ended at {latest_run.time_ended}"
        )
    elif latest_run is None:
        fmt.echo("No jobs have been run in this workspace yet")
    else:
        raise exception_from_response("Failed to get latest run", latest_run)

    # deployments
    with handle_client_exceptions():
        latest_deployment = get_latest_deployment.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
        )
    if isinstance(latest_deployment.parsed, get_latest_deployment.DeploymentResponse):
        fmt.echo(
            f"Current deployment version: {latest_deployment.parsed.version}, last updated at"
            f" {latest_deployment.parsed.date_added}. Run `dlt runtime deployment info` to see"
            " detailed deployment information"
        )
    elif isinstance(latest_deployment.parsed, get_latest_deployment.ErrorResponse404):
        fmt.echo("No deployment has been uploaded to this workspace")
    else:
        raise exception_from_response(
            "Failed to get latest deployment", latest_deployment
        )

    # configurations
    with handle_client_exceptions():
        latest_configuration = get_latest_configuration.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
        )
    if isinstance(
        latest_configuration.parsed, get_latest_configuration.ConfigurationResponse
    ):
        fmt.echo(
            f"Current configuration version: {latest_configuration.parsed.version}, last updated at"
            f" {latest_configuration.parsed.date_added}. Run `dlt runtime configuration info` to"
            " see detailed configuration information"
        )
    elif isinstance(
        latest_configuration.parsed,
        get_latest_configuration.ErrorResponse404,
    ):
        fmt.echo("No configuration has been uploaded to this workspace")
    else:
        raise exception_from_response(
            "Failed to get latest configuration", latest_configuration
        )


# Power user: jobs and job-runs


@track_command(operation="jobs", suboperation="list")
def jobs_list(*, auth_service: RuntimeAuthService, api_client: ApiClient) -> None:
    with handle_client_exceptions():
        res = list_scripts.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
        )
    if isinstance(res.parsed, list_scripts.ListScriptsResponse200) and isinstance(
        res.parsed.items, list
    ):
        if not res.parsed.items:
            fmt.echo("No jobs found in this workspace")
            return
        fmt.echo(
            tabulate(
                [
                    _extract_keys(script.to_dict(), JOB_HEADERS)
                    for script in reversed(res.parsed.items)
                ],
                headers=JOB_HEADERS,
            )
        )
    else:
        raise exception_from_response("Failed to list jobs", res)


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
    with handle_client_exceptions():
        res = get_script.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            script_id_or_name=script_path_or_job_name,
        )
    if isinstance(res.parsed, get_script.DetailedScriptResponse):
        fmt.echo(
            tabulate(
                [_extract_keys(res.parsed.to_dict(), JOB_HEADERS)], headers=JOB_HEADERS
            )
        )
    else:
        raise exception_from_response("Failed to get job info", res)


@track_command(operation="jobs", suboperation="create")
def job_create(
    script_path: Optional[str],
    args: argparse.Namespace,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    if not script_path:
        raise CliCommandInnerException(
            cmd="runtime",
            msg="Script path is required as the first argument",
        )
    script_path_obj = Path(active().run_dir) / script_path
    if not script_path_obj.exists():
        raise CliCommandInnerException(
            cmd="runtime",
            msg="Script path is required as the first argument. Provided path does not exist",
        )
    if args.schedule:
        _check_cron_expression(args.schedule)
    job_name = args.name or script_path
    job_type = ScriptType.INTERACTIVE if args.interactive else ScriptType.BATCH
    interactive_script_type = None
    if args.interactive:
        interactive_script_type = (
            InteractiveScriptType(args.app_type)
            if args.app_type
            else InteractiveScriptType.MARIMO
        )
    job_description = args.description or f"The {job_name} job"

    # warn if the job exists already with different parameters
    with handle_client_exceptions():
        res = get_script.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            script_id_or_name=job_name,
        )
    if isinstance(res.parsed, get_script.DetailedScriptResponse):
        if args.name and res.parsed.entry_point != script_path:
            fmt.warning(
                f"Warning: Job {job_name} already exists for a different script path"
                f" ({res.parsed.entry_point} -> {script_path}). Overwriting..."
            )
        if res.parsed.schedule != args.schedule:
            fmt.warning(
                f"Warning: Job {job_name} already exists with a different schedule"
                f" ({res.parsed.schedule} -> {args.schedule}). Overwriting..."
            )
        if res.parsed.script_type != job_type:
            fmt.warning(
                f"Warning: Job {job_name} already exists with a different interactive mode"
                f" ({res.parsed.script_type} -> {job_type}). Overwriting..."
            )

    with handle_client_exceptions():
        upsert = create_or_update_script.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            body=create_or_update_script.CreateScriptRequest(
                name=job_name,
                description=job_description,
                entry_point=script_path,
                script_type=job_type,
                interactive_script_type=interactive_script_type,
                profile=None,
                schedule=args.schedule,
            ),
        )
    if isinstance(upsert.parsed, create_or_update_script.ScriptResponse):
        fmt.echo(
            tabulate(
                [_extract_keys(upsert.parsed.to_dict(), JOB_HEADERS)],
                headers=JOB_HEADERS,
            )
        )
    else:
        raise exception_from_response("Failed to create job", upsert)


@track_command(operation="job-runs", suboperation="create")
def create_job_run(
    script_path_or_job_name: Optional[str] = None,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> None:
    if script_path_or_job_name is None:
        raise CliCommandInnerException(
            cmd="runtime",
            msg="Script path or job name is required",
        )
    with handle_client_exceptions():
        res = create_run.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            body=create_run.CreateRunRequest(
                script_id_or_name_or_secret=script_path_or_job_name,
                profile=None,
            ),
        )
    if isinstance(res.parsed, create_run.DetailedRunResponse):
        fmt.echo(
            tabulate(
                [_extract_keys(res.parsed.to_dict(), JOB_RUN_HEADERS)],
                headers=JOB_RUN_HEADERS,
            )
        )
    else:
        raise exception_from_response("Failed to start run", res)
