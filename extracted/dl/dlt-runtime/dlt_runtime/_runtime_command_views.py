from datetime import datetime, timedelta
from typing import Any, Optional

import humanize
from dlt._workspace.cli import echo as fmt
from dlt._workspace.deployment._job_ref import format_job_label

from dlt_runtime.exceptions import RuntimeClientException
from tabulate import tabulate

from dlt_runtime.runtime import WorkspaceInfo
from dlt_runtime.runtime_clients.api.models.log_line import LogLine
from dlt_runtime.runtime_clients.api.types import Unset
from dlt_runtime.strings import (
    TRIGGER_CONCURRENCY_ONE_MESSAGE,
    TRIGGER_CONCURRENCY_OPEN_LINE,
    TRIGGER_CONCURRENCY_SUGGESTIONS,
    TRIGGER_REFRESH_HINT,
    TRIGGER_STATUS_MESSAGES,
)
from dlt_runtime.typing import (
    ConnectInfo,
    FileDelta,
    LoginResult,
    RuntimeInfo,
    SwitchedWorkspaceInfo,
    SyncLoggingLevel,
    SyncResult,
    TriggerSkipInfo,
)


# Toggled by `--timestamps` on the runtime parser; flips date/duration views
# from humanized ("2 minutes ago") to exact ISO / `1.291 s`.
_show_exact_timestamps: bool = False


def set_show_exact_timestamps(enabled: bool) -> None:
    global _show_exact_timestamps
    _show_exact_timestamps = enabled


def _format_datetime(value: datetime) -> str:
    """Format a datetime as humanized relative time, or ISO when --timestamps is set."""
    if _show_exact_timestamps:
        return value.isoformat()
    # naturaltime needs `now` with matching tz-awareness when value is tz-aware.
    when = datetime.now(value.tzinfo) if value.tzinfo is not None else None
    return humanize.naturaltime(value, when=when)


def _format_duration_seconds(seconds: float) -> str:
    """Format a duration in seconds as humanized text, or `1.291 s` when --timestamps is set."""
    if _show_exact_timestamps:
        return f"{seconds:.3f} s"
    return humanize.precisedelta(timedelta(seconds=seconds))


# Row keys (from API model `to_dict()`) that `_humanize_row` reformats.
_DATETIME_ROW_KEYS = frozenset(
    {"date_added", "date_updated", "time_started", "time_ended"}
)
_DURATION_ROW_KEYS = frozenset({"duration"})


def _format_iso_or_value(value: Any) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, datetime):
        return _format_datetime(value)
    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value)
        except ValueError:
            return value
        return _format_datetime(parsed)
    return str(value)


def _format_duration_value(value: Any) -> str:
    if value is None or value == "":
        return ""
    try:
        seconds = float(value)
    except (TypeError, ValueError):
        return str(value)
    return _format_duration_seconds(seconds)


def _humanize_row(row: dict[str, Any]) -> dict[str, Any]:
    """Reformat known datetime/duration keys in a `model.to_dict()` row for tabulate."""
    out = dict(row)
    for key in _DATETIME_ROW_KEYS:
        if key in out:
            out[key] = _format_iso_or_value(out[key])
    for key in _DURATION_ROW_KEYS:
        if key in out:
            out[key] = _format_duration_value(out[key])
    return out


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
    "entry_point": fmt.bold("Entry point"),
    "script_type": fmt.bold("Type"),
    "date_added": fmt.bold("Created at"),
    "default_trigger": fmt.bold("Default trigger"),
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


def _extract_keys(data: dict[str, Any], keys_dict: dict[str, str]) -> dict[str, Any]:
    return {key: data.get(key, "") for key in keys_dict}


def _preprocess_run_output(
    run: dict[str, Any], headers: dict[str, str]
) -> dict[str, Any]:
    result = _humanize_row(_extract_keys(run, headers))
    jd = run["script"]["job_definition"]
    result["job_name"] = format_job_label(
        jd["job_ref"], jd.get("expose"), jd.get("deliver")
    )
    return {key: result[key] for key in headers.keys() if key in result}


def _format_log_line(log: LogLine) -> str:
    """Format a log line as `[line] HH:MM:SS.mmm [phase] msg`, or full ISO with --timestamps."""
    # Parse ISO timestamp and convert to local time
    try:
        if isinstance(log.reported_at, str):
            timestamp = datetime.fromisoformat(log.reported_at.replace("Z", "+00:00"))
        else:
            timestamp = log.reported_at

        if _show_exact_timestamps:
            time_str = timestamp.isoformat()
        else:
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


def _print_login_result(result: LoginResult, minimal_logging: bool) -> None:
    """Display login result."""
    if not minimal_logging:
        label = "Logged in as" if result["is_new_login"] else "Already logged in as"
        fmt.secho("%s %s" % (label, fmt.bold(result["email"])), fg="green")
        fmt.echo("  dltHub Runtime Web UI: %s" % fmt.bold(result["web_ui_url"]))


def _format_file_delta_counts(delta: FileDelta) -> str:
    """Render '(N added, M updated, K deleted)' for the MINIMAL line."""
    return (
        f"({len(delta['added'])} added, {len(delta['updated'])} updated, "
        f"{len(delta['deleted'])} deleted)"
    )


def _print_files_manifest_diff(delta: FileDelta) -> None:
    """Render the FULL-mode file delta tree (mirrors _print_deploy_result)."""
    fmt.echo("")
    fmt.echo("Files:")
    for p in delta["added"]:
        fmt.secho(f"  + {p}", fg="green")
    for p in delta["updated"]:
        fmt.secho(f"  ~ {p}", fg="blue")
    for p in delta["deleted"]:
        fmt.secho(f"  - {p}", fg="red")
    if delta["unchanged_count"]:
        fmt.echo(fmt.style(f"  ({delta['unchanged_count']} unchanged)", dim=True))


def _print_sync_result(
    label: str,
    result: SyncResult,
    *,
    level: SyncLoggingLevel = "full",
    verbose: bool = False,
) -> None:
    """Display sync result for deployment or configuration."""
    if level == "silent":
        return

    # The "subject" the user reads: "workspace files" for deployment, "workspace
    # configuration" for configuration. Used by minimal/dry-run lines.
    subject = "workspace files" if label == "deployment" else "workspace configuration"
    status = result["status"]
    data = result.get("data") or {}
    file_delta: FileDelta | None = data.get("file_delta")

    if level == "minimal":
        # Append "(N added, M updated, K deleted)" when the diff is available
        # so users see what changed even on the deploy happy path.
        suffix = f" {_format_file_delta_counts(file_delta)}" if file_delta else ""
        if status == "created":
            fmt.echo(f"Synced changed {subject}{suffix}")
        elif status == "would_create":
            fmt.echo(
                f"{subject.capitalize()} changed{suffix}, skipping sync due to dry run"
            )
        # no_changes → quiet on minimal so `deploy` happy path stays clean
        return

    # level == "full": resource-level `deployment sync` / `configuration sync`.
    # The full per-file tree only renders when --verbose is set; default FULL
    # output is the tabulate row + counts, no tree.
    if status == "no_changes":
        fmt.echo(f"No changes detected in the {label}, skipping file upload")
    elif status == "created":
        headers = DEPLOYMENT_HEADERS if label == "deployment" else CONFIGURATION_HEADERS
        # Tabulate skips the file_delta key (not a header column)
        row = {k: v for k, v in data.items() if k != "file_delta"}
        fmt.echo(tabulate([_humanize_row(row)], headers=headers))
        if file_delta is not None:
            fmt.echo(f"Files: {_format_file_delta_counts(file_delta)}")
            if verbose:
                _print_files_manifest_diff(file_delta)
    elif status == "would_create":
        fmt.echo(f"{subject.capitalize()} would be uploaded (dry run, skipping)")
        if file_delta is not None:
            fmt.echo(f"Files: {_format_file_delta_counts(file_delta)}")
            if verbose:
                _print_files_manifest_diff(file_delta)


def _print_connect_info(info: ConnectInfo) -> None:
    """Display workspace connection info."""
    ws_id_dim = fmt.style(info["workspace_id"], dim=True)
    if info["workspace_name"]:
        ws_label = "%s (%s)" % (fmt.bold(info["workspace_name"]), ws_id_dim)
    else:
        ws_label = ws_id_dim
    fmt.echo("  Connected workspace:   %s" % ws_label)
    fmt.echo("  Local directory:       %s" % fmt.bold(info["local_dir"]))


def _prompt_workspace_selection(
    workspaces: list[WorkspaceInfo],
) -> Optional[WorkspaceInfo]:
    """Interactive menu for workspace selection; None means "create new"."""
    # In non-interactive mode (ALWAYS_CHOOSE_DEFAULT set by maybe_no_stdin)
    # there's no default to pick — raise with re-run instructions.
    fmt.echo(f"  {fmt.bold('[0]')} Create new workspace")
    for idx, ws in enumerate(workspaces, start=1):
        ws_id_dim = fmt.style(ws.id, dim=True)
        fmt.echo(f"  {fmt.bold(f'[{idx}]')} {fmt.bold(ws.name)} {ws_id_dim}")
        if ws.description:
            fmt.echo(f"       {ws.description}")
    fmt.echo("")

    if fmt.ALWAYS_CHOOSE_DEFAULT and fmt.ALWAYS_CHOOSE_VALUE is None:
        raise RuntimeClientException(
            "Non-interactive mode: cannot prompt for workspace selection. "
            "Run `dlt runtime login --workspace <name-or-id>` to select a "
            "workspace, or `dlt runtime login --workspace <new-name>` to "
            "create a new one."
        )

    choices = [str(i) for i in range(len(workspaces) + 1)]
    try:
        choice = fmt.prompt("Select a workspace", choices=choices)
    except KeyboardInterrupt as e:
        # Translate ^C to EOFError so the boundary handler treats it as
        # "user-cancelled input" rather than re-raising the interrupt.
        raise EOFError("Workspace selection cancelled") from e
    choice_num = int(choice)
    if choice_num == 0:
        return None
    return workspaces[choice_num - 1]


def _prompt_new_workspace() -> tuple[str, str]:
    """Prompt user for workspace name and description. Returns (name, description).

    In non-interactive mode, fall back to defaults (`default`, ``).
    """
    fmt.echo("\nCreating a new workspace...")
    if fmt.ALWAYS_CHOOSE_DEFAULT:
        fmt.echo("Using default workspace name `default` (non-interactive mode)")
        return "default", ""
    name = (
        fmt.text_input("Workspace name (leave empty for `default`)", default="")
        or "default"
    )
    description = fmt.text_input("Workspace description (optional)", default="")
    return name, description


def _print_device_flow_start(
    verification_uri: str,
    user_code: str,
    device_code: str,
    *,
    not_logged_in_hint: bool = False,
) -> None:
    """Phase 1 view: device flow started, print instructions for non-interactive resume."""
    if not_logged_in_hint:
        fmt.echo("Not logged in.")
        fmt.echo("")
    fmt.echo(
        "Please go to %s and enter the code %s"
        % (fmt.bold(verification_uri), fmt.bold(user_code))
    )
    fmt.echo("")
    fmt.echo("After completing authentication in the browser, run:")
    fmt.echo("  dlt runtime login --resume %s" % device_code)


def _print_device_flow_interactive(
    verification_uri: str,
    user_code: str,
    *,
    not_logged_in_hint: bool = False,
) -> None:
    """Interactive device-flow prompt: same hint as Phase 1, but waits in-process."""
    if not_logged_in_hint:
        fmt.echo("Not logged in.")
        fmt.echo("")
    fmt.echo(
        "Please go to %s and enter the code %s"
        % (fmt.bold(verification_uri), fmt.bold(user_code))
    )
    fmt.echo("Waiting for authentication...\n")


def _print_workspace_switched(info: SwitchedWorkspaceInfo) -> None:
    """Render the result of a successful `workspace switch`."""
    ws_id_dim = fmt.style(info["workspace_id"], dim=True)
    ws_name = info.get("workspace_name")
    if ws_name:
        ws_label = "%s (%s)" % (fmt.bold(ws_name), ws_id_dim)
    else:
        ws_label = ws_id_dim
    fmt.echo("Switched to workspace: %s" % ws_label)


def _print_runtime_info(info: RuntimeInfo) -> None:
    """Display workspace overview."""
    if "email" in info:
        fmt.echo(f"User: {fmt.bold(info['email'])}")
    ws_name = info["workspace_name"]
    ws_id = info["workspace_id"]
    if ws_name:
        fmt.echo(f"Workspace: {fmt.bold(ws_name)} ({ws_id})")
    else:
        fmt.echo(f"Workspace: {ws_id}")
    fmt.echo(f"Local directory: {fmt.bold(info['local_dir'])}")
    fmt.echo(f"Workspace URL: {fmt.bold(info['workspace_url'])}")
    fmt.echo("")

    fmt.echo(
        f"# registered jobs: {info['job_count']}. Run `dlt runtime job list` to see all"
    )

    if "latest_run_name" in info:
        msg = f"Latest job run: {info['latest_run_name']} ({info['latest_run_status']})"
        if "latest_run_started" in info:
            msg += f", started {_format_datetime(info['latest_run_started'])}"
        if "latest_run_ended" in info:
            msg += f", ended {_format_datetime(info['latest_run_ended'])}"
        fmt.echo(msg)
    else:
        fmt.echo("No jobs have been run in this workspace yet")

    if "deployment_version" in info:
        msg = f"Current deployment version: {info['deployment_version']}"
        if "deployment_date" in info:
            msg += f", last updated {_format_datetime(info['deployment_date'])}"
        msg += (
            ". Run `dlt runtime deployment info` to see detailed deployment information"
        )
        fmt.echo(msg)
    else:
        fmt.echo("No deployment has been uploaded to this workspace")

    if "configuration_version" in info:
        msg = f"Current configuration version: {info['configuration_version']}"
        if "configuration_date" in info:
            msg += f", last updated {_format_datetime(info['configuration_date'])}"
        msg += (
            ". Run `dlt runtime configuration info` to see detailed configuration"
            " information"
        )
        fmt.echo(msg)
    else:
        fmt.echo("No configuration has been uploaded to this workspace")

    # Predefined profiles (server-side, mapped by access level)
    if "predefined_profiles" in info and info["predefined_profiles"]:
        fmt.echo("")
        fmt.echo("Predefined profiles:")
        for access_level, profile_name in info["predefined_profiles"].items():
            fmt.echo(f"  {access_level}: {profile_name}")


# ---------------------------------------------------------------------------
# Entity views (accept API models, display formatted output)
# ---------------------------------------------------------------------------


def _print_workspaces(workspaces: list[Any], current_ws_id: Optional[str]) -> None:
    """Display workspace list with current workspace marked."""
    if not workspaces:
        fmt.echo("No workspaces found")
        return

    rows = []
    for ws in workspaces:
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


def _print_job_run_info(run: Any) -> None:
    """Display a single run's info."""
    fmt.echo(
        tabulate(
            [_humanize_row(_extract_keys(run.to_dict(), JOB_RUN_HEADERS))],
            headers=JOB_RUN_HEADERS,
        )
    )


def _print_runs(runs: list[Any]) -> None:
    """Display a list of runs."""
    if not runs:
        fmt.echo("No runs found in this workspace")
        return
    fmt.echo(
        tabulate(
            [
                _preprocess_run_output(run.to_dict(), JOB_RUN_HEADERS)
                for run in reversed(runs)
            ],
            headers=JOB_RUN_HEADERS,
        )
    )


def _print_deployments(deployments: list[Any]) -> None:
    """Display a list of deployments."""
    if not deployments:
        fmt.echo("No deployments found in this workspace")
        return
    fmt.echo(
        tabulate(
            [
                _humanize_row(_extract_keys(deployment.to_dict(), DEPLOYMENT_HEADERS))
                for deployment in reversed(deployments)
            ],
            headers=DEPLOYMENT_HEADERS,
        )
    )


def _print_deployment_info(deployment: Any) -> None:
    """Display a single deployment's info."""
    fmt.echo(
        tabulate(
            [_humanize_row(_extract_keys(deployment.to_dict(), DEPLOYMENT_HEADERS))],
            headers=DEPLOYMENT_HEADERS,
        )
    )


def _print_configurations(configurations: list[Any]) -> None:
    """Display a list of configurations."""
    if not configurations:
        fmt.echo("No configurations found in this workspace")
        return
    fmt.echo(
        tabulate(
            [
                _humanize_row(
                    _extract_keys(configuration.to_dict(), CONFIGURATION_HEADERS)
                )
                for configuration in reversed(configurations)
            ],
            headers=CONFIGURATION_HEADERS,
        )
    )


def _print_configuration_info(configuration: Any) -> None:
    """Display a single configuration's info."""
    fmt.echo(
        tabulate(
            [
                _humanize_row(
                    _extract_keys(configuration.to_dict(), CONFIGURATION_HEADERS)
                )
            ],
            headers=CONFIGURATION_HEADERS,
        )
    )


def _preprocess_job_output(
    job: dict[str, Any], headers: dict[str, str]
) -> dict[str, Any]:
    """Extract job fields for display, including entry_point from job_definition."""
    result = _humanize_row(_extract_keys(job, headers))
    jd = job["job_definition"]
    # "Job name" column is the formatted label derived from the job definition
    result["name"] = format_job_label(
        jd["job_ref"], jd.get("expose"), jd.get("deliver")
    )
    # Build entry_point string from nested job_definition
    ep = jd["entry_point"]
    module = ep["module"]
    function = ep["function"]
    result["entry_point"] = f"{module}::{function}" if function else module
    return result


def _print_jobs(jobs: list[Any]) -> None:
    """Display a list of jobs."""
    if not jobs:
        fmt.echo("No jobs found in this workspace")
        return
    fmt.echo(
        tabulate(
            [
                _preprocess_job_output(script.to_dict(), JOB_HEADERS)
                for script in reversed(jobs)
            ],
            headers=JOB_HEADERS,
        )
    )


def _print_job_info(job: Any) -> None:
    """Display a single job's info."""
    fmt.echo(
        tabulate(
            [_preprocess_job_output(job.to_dict(), JOB_HEADERS)],
            headers=JOB_HEADERS,
        )
    )


def _script_job_label(script: Any) -> str:
    """Format a ScriptResponse's job_ref using its job_definition."""
    jd = script.job_definition.to_dict()
    return format_job_label(jd["job_ref"], jd.get("expose"), jd.get("deliver"))


def _script_label_with_trigger(script: Any) -> str:
    """Job label plus '(trigger: ...)' suffix when default_trigger is set."""
    label = _script_job_label(script)
    trigger = getattr(script, "default_trigger", None)
    if isinstance(trigger, Unset) or not trigger:
        return label
    return f"{label} (trigger: {trigger})"


def _print_deploy_result(
    result: Any,
    *,
    deployment_module: str,
    job_count: int,
    description: Optional[str] = None,
    dry_run: bool = False,
) -> None:
    """Display deploy manifest result as a reconciliation plan."""
    fmt.echo(f"{job_count} job(s) found in {deployment_module}")
    if description:
        fmt.echo(description)

    if result.added:
        fmt.echo("")
        fmt.echo("New jobs:")
        for s in result.added:
            fmt.secho(f"  + {_script_label_with_trigger(s)}", fg="green")

    if result.updated:
        fmt.echo("")
        fmt.echo("Updated jobs:")
        for u in result.updated:
            fmt.secho(f"  ~ {_script_label_with_trigger(u.script)}", fg="blue")

    if result.archived:
        fmt.echo("")
        fmt.echo("Archived jobs:")
        for s in result.archived:
            fmt.secho(f"  - {_script_job_label(s)}", fg="red")

    if result.unchanged:
        fmt.echo("")
        fmt.echo("Unchanged jobs:")
        for s in result.unchanged:
            fmt.echo(fmt.style(f"    {_script_job_label(s)}", dim=True))

    if result.warnings:
        for w in result.warnings:
            fmt.warning(w)

    fmt.echo("")
    if dry_run:
        fmt.echo("Dry run, skipping...")
    else:
        fmt.echo(
            f"{len(result.added)} added, "
            f"{len(result.updated)} updated, "
            f"{len(result.archived)} archived"
        )


def _print_bulk_cancel_result(result: Any, *, dry_run: bool = False) -> None:
    """Display bulk cancel result."""
    prefix = "Would cancel" if dry_run else "Cancelled"
    if result.cancelled:
        for c in result.cancelled:
            fmt.echo(
                f"  {prefix} run # {c.run_number} of {fmt.bold(c.job_ref)}"
                f" (was {c.previous_status.value})"
            )
    if result.not_running:
        for ref in result.not_running:
            fmt.echo(f"  {ref}: no active run")
    if not result.cancelled and not result.not_running:
        fmt.echo("No matching jobs found")
    elif result.cancelled:
        fmt.echo(
            f"\n{len(result.cancelled)} run(s) {'would be cancelled' if dry_run else 'cancelled'}"
        )


def _print_trigger_skip(info: TriggerSkipInfo, *, terse: bool = False) -> None:
    """Render a friendly message + remediation hints for a skipped TriggerJob.
    `terse=True` prints only the lead line
    """
    job_ref = info["job_ref"]
    status = info["status"]

    # Lead line: "  <job_ref>: <message>"
    if status == "skipped_concurrency_limit" and info.get("concurrency") == 1:
        message = TRIGGER_CONCURRENCY_ONE_MESSAGE
    else:
        # Fall back to the raw status if the table is missing an entry —
        # better than silence, and surfaces unmapped codes in tests.
        message = TRIGGER_STATUS_MESSAGES.get(status, status)
    fmt.echo(f"  {fmt.bold(job_ref)}: {message}")

    if terse:
        return

    # Status-specific suggestion lines.
    if status == "skipped_concurrency_limit":
        for line in TRIGGER_CONCURRENCY_SUGGESTIONS:
            fmt.echo(line.format(job_ref=job_ref))
        web_url = info.get("web_url")
        if web_url:
            fmt.echo(TRIGGER_CONCURRENCY_OPEN_LINE.format(url=web_url))
    elif status == "skipped_fresh":
        fmt.echo(TRIGGER_REFRESH_HINT)
