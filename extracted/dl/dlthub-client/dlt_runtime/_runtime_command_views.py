from datetime import datetime
from typing import Any, Optional, Sequence, Union

import humanize
from dlt._workspace.cli import echo as fmt
from dlt._workspace.cli.utils import open_url
from dlt._workspace.deployment._job_ref import parse_job_ref, resolve_job_ref
from dlt._workspace.deployment._run_views import print_run_banner
from dlt._workspace.deployment.exceptions import (
    AmbiguousJobRef,
    InvalidJobRef,
    JobRefNotFound,
)
from dlt._workspace.deployment.typing import TJobRef
from dlt.common.time import ensure_datetime

from dlt_runtime.exceptions import RuntimeClientException
from tabulate import tabulate

from dlt_runtime.runtime_clients.api.models.dataplane_info import DataplaneInfo
from dlt_runtime.runtime_clients.api.models.run_status import RunStatus
from dlt_runtime.runtime_clients.api.types import Unset
from dlt_runtime.strings import (
    NON_INTERACTIVE_PICKER_CREATE_LINE,
    NON_INTERACTIVE_PICKER_HEADER,
    NON_INTERACTIVE_PICKER_SELECT_LINE,
    TRIGGER_CONCURRENCY_ONE_MESSAGE,
    TRIGGER_CONCURRENCY_OPEN_LINE,
    TRIGGER_CONCURRENCY_SUGGESTIONS,
    TRIGGER_STATUS_MESSAGES,
)
from dlt_runtime.typing import (
    ConnectedWorkspaceInfo,
    CreateInOrgChoice,
    FileDelta,
    LoginResult,
    OrganizationGroup,
    RuntimeInfo,
    RuntimeRunBannerInfo,
    SyncLoggingLevel,
    SyncResult,
    TriggerSkipInfo,
    WorkspaceInfo,
)


# dltHub brand lavender (#AAA8D4, web --dlt-lightest-purple) as a chip bg with
# dark-navy ink (#191937, --dlt-dark-purple) — mirrors the web dark-mode chip.
# The chip carries its own bg+fg, so it reads on both light and dark terminals.
_DLT_CHIP_BG = (170, 168, 212)
_DLT_CHIP_FG = (25, 25, 55)


# Toggled by `--timestamps` on the runtime parser; flips date/duration views
# from humanized ("2 minutes ago") to exact ISO / `1.291 s`.
_show_exact_timestamps: bool = False


def set_show_exact_timestamps(enabled: bool) -> None:
    global _show_exact_timestamps
    _show_exact_timestamps = enabled


def _format_datetime(value: datetime) -> str:
    """Format a datetime as short relative time ('5m ago'), or ISO when --timestamps is set."""
    if _show_exact_timestamps:
        return value.isoformat()
    when = datetime.now(value.tzinfo) if value.tzinfo is not None else datetime.now()
    secs = int((when - value).total_seconds())
    # Future timestamps are rare in practice; let humanize handle them verbosely.
    if secs < 0:
        return humanize.naturaltime(value, when=when)
    if secs < 60:
        return f"{secs}s ago"
    if secs < 3600:
        return f"{secs // 60}m ago"
    if secs < 86400:
        return f"{secs // 3600}h ago"
    return f"{secs // 86400}d ago"


def _format_duration_short(seconds: float, *, sub_second: bool = False) -> str:
    """Short h/m/s duration: '15s', '14m 44s', '1h 2m 3s'."""
    if seconds < 0:
        return "-" + _format_duration_short(-seconds, sub_second=sub_second)
    whole = int(seconds)
    hours, rem = divmod(whole, 3600)
    minutes, secs = divmod(rem, 60)
    parts: list[str] = []
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if sub_second:
        # Push fractional milliseconds onto the seconds field; always show it.
        parts.append(f"{secs + (seconds - whole):.3f}s")
    elif secs or not parts:
        parts.append(f"{secs}s")
    return " ".join(parts)


def _format_duration_seconds(seconds: float) -> str:
    """Short h/m/s duration; --timestamps adds .mmm precision on the seconds field."""
    return _format_duration_short(seconds, sub_second=_show_exact_timestamps)


def _format_active_run_duration(elapsed: float, max_run_time_seconds: float) -> str:
    """`<elapsed> of <max>` label used while a run is still in flight."""
    return f"{_format_duration_short(elapsed)} of {_format_duration_short(max_run_time_seconds)}"


# Row keys (from API model `to_dict()`) that `_humanize_row` reformats.
_DATETIME_ROW_KEYS = frozenset(
    {"date_added", "date_updated", "time_started", "time_ended"}
)
_DURATION_ROW_KEYS = frozenset({"duration"})

# Run statuses that mean the run has reached an end state (no further log output).
TERMINAL_RUN_STATUSES = frozenset(
    {RunStatus.COMPLETED, RunStatus.FAILED, RunStatus.CANCELLED, RunStatus.SKIPPED}
)
# Subset that indicates the run did not succeed; callers may exit non-zero.
FAILED_RUN_STATUSES = frozenset({RunStatus.FAILED, RunStatus.CANCELLED})


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
    # Live duration: in-progress run (started, no end) → now - started.
    if "duration" in out and not out.get("duration") and out.get("time_started"):
        try:
            started = ensure_datetime(out["time_started"])
            ended = out.get("time_ended")
            ended_dt = ensure_datetime(ended) if ended else None
            if ended_dt is None:
                now = datetime.now(started.tzinfo) if started.tzinfo else datetime.now()
                out["duration"] = (now - started).total_seconds()
        except (TypeError, ValueError):
            pass
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
}
# Single-record detail view; rendered vertically as key:value rows.
JOB_INFO_HEADERS = {
    "job_ref": fmt.bold("Job ref"),
    "name": fmt.bold("Selector"),
    "display_name": fmt.bold("Display name"),
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
    "duration": fmt.bold("Duration"),
}
# Single-record detail; rendered vertically. Adds interval window + run id.
JOB_RUN_INFO_HEADERS = {
    "id": fmt.bold("Run ID"),
    "number": fmt.bold("Run #"),
    "job_name": fmt.bold("Job"),
    "status": fmt.bold("Status"),
    "trigger": fmt.bold("Trigger"),
    "profile": fmt.bold("Profile"),
    "time_started": fmt.bold("Started at"),
    "time_ended": fmt.bold("Ended at"),
    "duration": fmt.bold("Duration"),
    "time_to_timeout": fmt.bold("Time to timeout"),
    "interval_start": fmt.bold("Interval start"),
    "interval_end": fmt.bold("Interval end"),
}
WORKSPACE_HEADERS = {
    "name": fmt.bold("Name"),
    "organization": fmt.bold("Organization"),
    "id": fmt.bold("ID"),
    "role": fmt.bold("Role"),
    "description": fmt.bold("Description"),
}


def _extract_keys(data: dict[str, Any], keys_dict: dict[str, str]) -> dict[str, Any]:
    return {key: data.get(key, "") for key in keys_dict}


def format_job_selector(
    job_ref: str, all_job_refs: Optional[Sequence[str]] = None
) -> str:
    """Shortest form of `job_ref` that round-trips through OSS `resolve_job_ref`."""
    section, name = parse_job_ref(TJobRef(job_ref))
    # Module-level (`jobs.name`) has no section to elide.
    if not section:
        return name
    # Try the bare name against the caller's scope; it round-trips iff unique.
    if all_job_refs is not None:
        try:
            resolve_job_ref(name, [TJobRef(r) for r in all_job_refs])
            return name
        except (InvalidJobRef, JobRefNotFound, AmbiguousJobRef):
            pass
    return f"{section}.{name}"


def _preprocess_run_output(
    run: dict[str, Any],
    headers: dict[str, str],
    all_job_refs: Optional[Sequence[str]] = None,
) -> dict[str, Any]:
    result = _humanize_row(_extract_keys(run, headers))
    jd = run["script"]["job_definition"]
    result["job_name"] = format_job_selector(jd["job_ref"], all_job_refs)
    if "status" in result and result["status"]:
        result["status"] = format_run_status(RunStatus(result["status"]))
    # Active run: server leaves `duration` null; show "<elapsed> of <max>" instead of blank.
    if "duration" in headers and not run.get("time_ended"):
        elapsed = _compute_active_elapsed(run.get("time_started"))
        max_rts = run["script_version"]["max_run_time_seconds"]
        if elapsed is not None and max_rts:
            result["duration"] = _format_active_run_duration(elapsed, float(max_rts))
    return {key: result[key] for key in headers.keys() if key in result}


def _compute_active_elapsed(time_started: Any) -> Optional[float]:
    """Seconds elapsed since `time_started` (ISO str or datetime); None if unparseable."""
    if not time_started:
        return None
    if isinstance(time_started, str):
        try:
            started = datetime.fromisoformat(time_started)
        except ValueError:
            return None
    elif isinstance(time_started, datetime):
        started = time_started
    else:
        return None
    now = datetime.now(started.tzinfo) if started.tzinfo else datetime.now()
    return (now - started).total_seconds()


def _format_log_line(log: Any) -> str:
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
        fmt.echo("  dltHub dashboard: %s" % fmt.bold(result["web_ui_url"]))


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


def _format_workspace_label(
    workspace_id: str,
    workspace_name: Optional[str] = None,
    organization_name: Optional[str] = None,
) -> str:
    """Canonical workspace label used by every workspace-rendering view."""

    if workspace_name and organization_name:
        return "%s (%s) %s" % (
            fmt.bold(workspace_name),
            fmt.bold(organization_name),
            workspace_id,
        )
    if workspace_name:
        return "%s %s" % (fmt.bold(workspace_name), workspace_id)
    return workspace_id


def _print_org_groups_interactive(groups: list[OrganizationGroup]) -> None:
    """Echo the picker layout with `[N]` selectors."""
    for group in groups:
        # Plain UUID alongside the bold name so users can copy it for
        # `--org-id <UUID>` without re-running another command.
        fmt.echo(
            "Organization %s  %s:"
            % (fmt.bold(group["organization_name"]), group["organization_id"])
        )
        create_label = fmt.bold(f"[{group['create_id']}]")
        fmt.echo(f"  {create_label} Create new workspace")
        for choice in group["workspaces"]:
            ws = choice["workspace"]
            row_label = fmt.bold(f"[{choice['id']}]")
            fmt.echo(f"  {row_label} {fmt.bold(ws['name'])}  {ws['id']}")
            if ws.get("description"):
                fmt.echo(f"       {ws['description']}")
        fmt.echo("")


def _print_org_groups_non_interactive(groups: list[OrganizationGroup]) -> None:
    """Non-interactive picker layout — header + grouped list + per-org command lines."""
    fmt.echo(NON_INTERACTIVE_PICKER_HEADER)
    fmt.echo("")
    for group in groups:
        org_id = group["organization_id"]
        fmt.echo(
            "Organization %s  %s:" % (fmt.bold(group["organization_name"]), org_id)
        )
        for choice in group["workspaces"]:
            ws = choice["workspace"]
            fmt.echo(f"  {fmt.bold(ws['name'])}  {ws['id']}")
            if ws.get("description"):
                fmt.echo(f"     {ws['description']}")
        fmt.echo("  " + NON_INTERACTIVE_PICKER_SELECT_LINE.format(org_id=org_id))
        fmt.echo("  " + NON_INTERACTIVE_PICKER_CREATE_LINE.format(org_id=org_id))
        fmt.echo("")


def _resolve_picker_choice(
    groups: list[OrganizationGroup], chosen_id: int
) -> Union[WorkspaceInfo, CreateInOrgChoice]:
    """Map the user's `[N]` input back to a workspace or create-in-org entry.

    Pure data lookup over the ids stamped by `_group_workspaces_by_org` —
    kept here so the prompt function stays a thin wrapper.
    """
    for group in groups:
        if group["create_id"] == chosen_id:
            return CreateInOrgChoice(
                organization_id=group["organization_id"],
                organization_name=group["organization_name"],
            )
        for choice in group["workspaces"]:
            if choice["id"] == chosen_id:
                return choice["workspace"]
    raise RuntimeClientException(
        f"Picker choice {chosen_id} is out of range — no matching row."
    )


def _picker_choice_count(groups: list[OrganizationGroup]) -> int:
    """Total number of selectable rows across all groups (one create + workspaces per group)."""
    return sum(1 + len(g["workspaces"]) for g in groups)


def _prompt_workspace_selection(
    groups: list[OrganizationGroup],
) -> Union[WorkspaceInfo, CreateInOrgChoice]:
    """Interactive menu for workspace selection.

    Returns the chosen `WorkspaceInfo` for an existing workspace, or a
    `CreateInOrgChoice` carrying the org the user picked `Create new` under.
    """
    _print_org_groups_interactive(groups)

    if not fmt.is_interactive() and fmt.ALWAYS_CHOOSE_VALUE is None:
        raise RuntimeClientException(
            "Non-interactive mode: cannot prompt for workspace selection. "
            "Run `dlthub workspace connect <workspace_uuid> --org-id <UUID>` "
            "to connect to an existing workspace, or `dlthub workspace "
            "connect <new-name> --org-id <UUID>` to create one."
        )

    total = _picker_choice_count(groups)
    choices = [str(i) for i in range(total)]
    try:
        choice = fmt.prompt("Select a workspace", choices=choices)
    except KeyboardInterrupt as e:
        # Translate ^C to EOFError so the boundary handler treats it as
        # "user-cancelled input" rather than re-raising the interrupt.
        raise EOFError("Workspace selection cancelled") from e
    return _resolve_picker_choice(groups, int(choice))


def _prompt_region_selection(regions: list[DataplaneInfo]) -> str:
    """Interactive menu for organization region selection.

    Returns the chosen plane's ``id``; the choice is permanent.
    """
    fmt.echo(
        "\nChoose your organization's region. "
        "This is permanent and cannot be changed later."
    )
    for i, dp in enumerate(regions):
        fmt.echo(f"  [{i}] {dp.name} ({dp.region})")
    if not fmt.is_interactive() and fmt.ALWAYS_CHOOSE_VALUE is None:
        raise RuntimeClientException(
            "Non-interactive mode: cannot prompt for an organization region. "
            "Re-run in an interactive terminal without `--non-interactive` to "
            "pick a region, or set it in the web app and then retry."
        )
    choices = [str(i) for i in range(len(regions))]
    try:
        choice = fmt.prompt("Select a region", choices=choices)
        chosen = regions[int(choice)]
        if not fmt.confirm(
            f"Set region to '{chosen.name}'? This cannot be changed.",
            default=False,
        ):
            raise EOFError("Organization region selection cancelled")
    except KeyboardInterrupt as e:
        raise EOFError("Organization region selection cancelled") from e
    return chosen.id


def _prompt_new_workspace(default_name: str = "default") -> tuple[str, str]:
    """Prompt for workspace name and description. Returns (name, description)."""
    # `default_name` is offered as the input default in interactive mode and
    # used verbatim in non-interactive mode.
    fmt.echo("\nCreating a new workspace...")
    if not fmt.is_interactive():
        fmt.echo(
            "Using default workspace name `%s` (non-interactive mode)" % default_name
        )
        return default_name, ""
    name = (
        fmt.text_input(
            "Workspace name (leave empty for `%s`)" % default_name, default=""
        )
        or default_name
    )
    description = fmt.text_input("Workspace description (optional)", default="")
    return name, description


def _prompt_create_missing_workspace_in_org(name: str, org_label: str) -> bool:
    """Confirm creating workspace `name` in the org identified by `org_label`."""
    question = "Workspace '%s' not found. Create it in '%s'?" % (name, org_label)
    try:
        return fmt.confirm(question, default=False)
    except KeyboardInterrupt as e:
        raise EOFError("Workspace creation cancelled") from e


def _print_device_flow_start(
    verification_uri_complete: str,
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
        "Please open %s and confirm the page shows the code %s"
        % (
            fmt.style(verification_uri_complete, underline=True, bold=True),
            fmt.style(user_code, fg=_DLT_CHIP_FG, bg=_DLT_CHIP_BG, bold=True),
        )
    )
    fmt.echo("")
    fmt.echo("After completing authentication in the browser, run:")
    fmt.echo("  dlthub login --resume %s" % device_code)


def _print_device_flow_interactive(
    verification_uri_complete: str,
    user_code: str,
    *,
    not_logged_in_hint: bool = False,
) -> None:
    """Print code + fallback URL; caller opens the browser."""
    if not_logged_in_hint:
        fmt.echo("Not logged in.")
    fmt.echo("")
    fmt.echo(
        "Login code:%s"
        % fmt.style(" %s " % user_code, fg=_DLT_CHIP_FG, bg=_DLT_CHIP_BG, bold=True)
    )
    fmt.echo("Confirm in the browser that the page shows this code.")
    fmt.echo("")
    fmt.echo("If your browser did not open automatically, open this URL:")
    fmt.echo("  %s" % fmt.style(verification_uri_complete, underline=True, bold=True))
    fmt.echo("")


def _print_loopback_login(
    authorization_url: str,
    *,
    not_logged_in_hint: bool = False,
) -> None:
    """Loopback (codeless) login: print the URL as a fallback."""
    if not_logged_in_hint:
        fmt.echo("Not logged in.")
    fmt.echo("")
    fmt.echo("Opening your browser to log in...")
    fmt.echo("")
    fmt.echo("If your browser did not open automatically, open this URL:")
    fmt.echo("  %s" % fmt.style(authorization_url, underline=True, bold=True))
    fmt.echo("")


def _print_waiting_for_auth(*, loopback: bool = False) -> None:
    fmt.echo("Waiting for authentication in your browser...")
    if loopback:
        fmt.echo(
            "If the browser can't reach this machine (remote/SSH session), "
            "press Ctrl+C and run `dlthub login --device`."
        )


def _open_login_page(url: str) -> None:
    """Open `url` via the OSS dlt URL opener; no-op for mock/dev placeholder URIs."""
    if not url.startswith(("http://", "https://")):
        return
    open_url(url)


def _print_show_url(
    label: str,
    url: str,
    browser_url: Optional[str] = None,
) -> None:
    """Echo the swap-free `url`; open `browser_url` when set. The single-use
    swap code rides only in `browser_url` and must never reach stdout."""
    fmt.echo(f"{label} is available at {url}")
    if browser_url:
        open_url(browser_url)


def _print_run_banner(info: RuntimeRunBannerInfo) -> None:
    """Render the OSS run banner, then append `run_url:` when present."""
    # OSS print_run_banner ignores keys it doesn't know, so passing the extended dict is safe.
    print_run_banner(info)
    url = info.get("run_url")
    if url:
        fmt.echo(f"  run_url:    {url}")


def _print_workspace_connected(info: ConnectedWorkspaceInfo) -> None:
    """Render the result of a successful `workspace connect`.

    Prints up to two lines based on `info`:
      `Created workspace with id: <id>`   (when `info["created"]`)
      `Auto-connected to workspace: ...`  (when `info["auto"]`)
      `Connected to workspace: ...`       (otherwise — second line)
    """
    if info.get("created"):
        fmt.echo(f"Created workspace with id: {fmt.bold(info['workspace_id'])}")
    prefix = "Auto-connected" if info.get("auto") else "Connected"
    fmt.echo(
        "%s to workspace: %s"
        % (
            prefix,
            _format_workspace_label(
                info["workspace_id"],
                info.get("workspace_name"),
                info.get("organization_name"),
            ),
        )
    )


def _print_runtime_info(info: RuntimeInfo) -> None:
    """Display workspace overview."""
    if "email" in info:
        fmt.echo(f"User: {fmt.bold(info['email'])}")
    fmt.echo(
        "Workspace: %s"
        % _format_workspace_label(
            info["workspace_id"],
            info["workspace_name"],
        )
    )
    org_name = info.get("organization_name")
    if org_name:
        fmt.echo(f"Organization: {fmt.bold(org_name)}")
    fmt.echo(f"Local directory: {fmt.bold(info['local_dir'])}")
    fmt.echo(f"Workspace URL: {fmt.bold(info['workspace_url'])}")
    fmt.echo("")

    fmt.echo(
        f"# registered jobs: {info['job_count']}. Run `dlthub job list` to see all"
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
        msg += ". Run `dlthub workspace deployment info` to see detailed deployment information"
        fmt.echo(msg)
    else:
        fmt.echo("No deployment has been uploaded to this workspace")

    if "configuration_version" in info:
        msg = f"Current configuration version: {info['configuration_version']}"
        if "configuration_date" in info:
            msg += f", last updated {_format_datetime(info['configuration_date'])}"
        msg += (
            ". Run `dlthub workspace configuration info` to see detailed configuration"
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
        name = ws["name"]
        if ws["id"] == current_ws_id:
            name = f"* {name}"
        rows.append(
            {
                "name": name,
                "organization": ws.get("organization_name") or "",
                "id": ws["id"],
                "role": ws.get("role") or "",
                "description": ws.get("description") or "",
            }
        )
    fmt.echo(tabulate(rows, headers=WORKSPACE_HEADERS))


def _print_job_run_info(run: Any) -> None:
    """Display a single run's info as vertical key:value rows."""

    # Read straight off the typed model — API responses are strongly typed,
    # so datetimes arrive as datetimes (no ISO-string round-trip needed).
    def _opt(attr: str) -> Any:
        v = getattr(run, attr, None)
        return None if isinstance(v, Unset) else v

    started = _opt("time_started")
    ended = _opt("time_ended")
    duration = _opt("duration")
    max_rts = run.script_version.max_run_time_seconds
    # Live duration for in-progress runs.
    if duration is None and started is not None and ended is None:
        now = datetime.now(started.tzinfo) if started.tzinfo else datetime.now()
        duration = (now - started).total_seconds()

    # Active run: show "<elapsed> of <max>" so the budget is visible inline.
    if duration is not None and ended is None and max_rts:
        duration_str = _format_active_run_duration(duration, float(max_rts))
    elif duration is not None:
        duration_str = _format_duration_seconds(duration)
    else:
        duration_str = ""

    # Time to timeout = budget − elapsed. Only meaningful while the run is active.
    time_to_timeout: str = ""
    if max_rts is not None and duration is not None and ended is None:
        remaining = max_rts - duration
        time_to_timeout = _format_duration_seconds(abs(remaining))
        if remaining <= 0:
            time_to_timeout = fmt.style(f"-{time_to_timeout} (overdue)", fg="red")
        elif remaining < max_rts * 0.25:
            time_to_timeout = fmt.style(time_to_timeout, fg="yellow")

    interval_start = _opt("interval_start")
    interval_end = _opt("interval_end")
    values: dict[str, str] = {
        "id": str(run.id),
        "number": str(run.number),
        "job_name": format_job_selector(run.script.job_definition.job_ref),
        "status": format_run_status(run.status),
        "trigger": str(run.trigger),
        "profile": _opt("profile") or "",
        "time_started": _format_datetime(started) if started else "",
        "time_ended": _format_datetime(ended) if ended else "",
        "duration": duration_str,
        "time_to_timeout": time_to_timeout,
        # Intervals stay ISO — they're machine-readable window bounds, not "X ago".
        "interval_start": interval_start.isoformat() if interval_start else "",
        "interval_end": interval_end.isoformat() if interval_end else "",
    }
    rows = [
        (label, values.get(key, ""))
        for key, label in JOB_RUN_INFO_HEADERS.items()
        # Hide intervals and time-to-timeout rows that aren't meaningful here.
        if (
            (not key.startswith("interval_") and key != "time_to_timeout")
            or values.get(key)
        )
    ]
    fmt.echo(tabulate(rows, tablefmt="plain"))


def _print_runs(runs: list[Any], *, running_only: bool = False) -> None:
    """Display a list of runs."""
    # Loader (`_fetch_runs`) sorts desc by run number; view renders as-is.
    if not runs:
        kind = "running jobs" if running_only else "runs"
        fmt.echo(f"No {kind} found in this workspace")
        return
    fmt.echo(
        tabulate(
            [_preprocess_run_output(run.to_dict(), JOB_RUN_HEADERS) for run in runs],
            headers=JOB_RUN_HEADERS,
        )
    )


_STATUS_STYLE: dict[RunStatus, dict[str, Any]] = {
    RunStatus.COMPLETED: {"fg": "green"},
    RunStatus.FAILED: {"fg": "red"},
    RunStatus.CANCELLED: {"fg": "yellow"},
    RunStatus.SKIPPED: {"fg": "yellow"},
    RunStatus.RUNNING: {"fg": "white", "bold": True},
}


def format_run_status(status: Any) -> str:
    """Stringify and color a RunStatus using the shared status palette."""
    text = status.value if hasattr(status, "value") else str(status)
    style = _STATUS_STYLE.get(status)
    return fmt.style(text, **style) if style else text


def _print_run_final_status(run: Any) -> None:
    """One-liner shown after the follow-logs loop exits."""

    status = run.status
    verb = (
        "finished with status" if status in TERMINAL_RUN_STATUSES else "current status"
    )
    status_text = status.value if hasattr(status, "value") else str(status)
    extras: list[str] = []
    duration = getattr(run, "duration", None)
    if duration is not None and not isinstance(duration, Unset):
        extras.append(f"duration: {_format_duration_value(duration)}")
    suffix = f" ({', '.join(extras)})" if extras else ""
    script_name = getattr(getattr(run, "script", None), "name", None) or "?"
    label = f"Run # {run.number} of job {script_name}"
    line = f"{label} {verb}: {fmt.bold(status_text)}{suffix}"
    style = _STATUS_STYLE.get(status)
    if style:
        fmt.secho(line, **style)
    else:
        fmt.echo(line)


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
    job: dict[str, Any],
    headers: dict[str, str],
    all_job_refs: Optional[Sequence[str]] = None,
) -> dict[str, Any]:
    """Extract job fields for display, including entry_point from job_definition."""
    result = _humanize_row(_extract_keys(job, headers))
    jd = job["job_definition"]
    name = format_job_selector(jd["job_ref"], all_job_refs)
    # Tag archived rows inline so the listing flags them when --archived is on.
    if job.get("archived"):
        name = f"{name} (archived)"
    result["name"] = name
    # Detail-view-only columns: canonical job_ref and humanised display_name.
    if "job_ref" in headers:
        result["job_ref"] = jd["job_ref"]
    if "display_name" in headers:
        expose = jd.get("expose") or {}
        result["display_name"] = expose.get("display_name") or ""
    ep = jd["entry_point"]
    result["entry_point"] = (
        f"{ep['module']}::{ep['function']}" if ep["function"] else ep["module"]
    )
    return result


def _print_jobs(jobs: list[Any]) -> None:
    """Display a list of jobs."""
    if not jobs:
        fmt.echo("No jobs found in this workspace")
        return
    # No manifest in scope for `dlthub job list` — render the qualified `section.name`.
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
    """Display a single job's info as vertical key:value rows."""
    row = _preprocess_job_output(job.to_dict(), JOB_INFO_HEADERS)
    # 2-column tabulate; key column right-aligned for a clean " key : value" look.
    fmt.echo(
        tabulate(
            [(label, row.get(key, "")) for key, label in JOB_INFO_HEADERS.items()],
            tablefmt="plain",
        )
    )
    archived = getattr(job, "archived", False)
    if not isinstance(archived, Unset) and archived:
        fmt.secho("This job is archived", fg="red")


def _script_label_with_trigger(
    script: Any, all_job_refs: Optional[Sequence[str]] = None
) -> str:
    """Job selector plus '(trigger: ...)' suffix when default_trigger is set."""
    label = format_job_selector(script.job_definition.job_ref, all_job_refs)
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

    # All scripts in this reconciliation form the selector scope for shortening.
    all_scripts = [
        *result.added,
        *(u.script for u in result.updated),
        *result.archived,
        *result.unchanged,
    ]
    all_refs = [s.job_definition.job_ref for s in all_scripts]

    if result.added:
        fmt.echo("")
        fmt.echo("New jobs:")
        for s in result.added:
            fmt.secho(f"  + {_script_label_with_trigger(s, all_refs)}", fg="green")

    if result.updated:
        fmt.echo("")
        fmt.echo("Updated jobs:")
        for u in result.updated:
            fmt.secho(
                f"  ~ {_script_label_with_trigger(u.script, all_refs)}", fg="blue"
            )

    if result.archived:
        fmt.echo("")
        fmt.echo("Archived jobs:")
        for s in result.archived:
            fmt.secho(
                f"  - {format_job_selector(s.job_definition.job_ref, all_refs)}",
                fg="red",
            )

    if result.unchanged:
        fmt.echo("")
        fmt.echo("Unchanged jobs:")
        for s in result.unchanged:
            fmt.echo(
                fmt.style(
                    f"    {format_job_selector(s.job_definition.job_ref, all_refs)}",
                    dim=True,
                )
            )

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

    for reason in info.get("reasons") or []:
        fmt.echo(f"    - {reason}")

    if terse:
        return

    # Status-specific suggestion lines.
    if status == "skipped_concurrency_limit":
        for line in TRIGGER_CONCURRENCY_SUGGESTIONS:
            fmt.echo(line.format(job_ref=job_ref))
        web_url = info.get("web_url")
        if web_url:
            fmt.echo(TRIGGER_CONCURRENCY_OPEN_LINE.format(url=web_url))
