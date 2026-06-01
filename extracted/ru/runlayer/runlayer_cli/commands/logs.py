import json
from datetime import datetime, timedelta, timezone
from typing import Any

import structlog
import typer

from runlayer_cli.api import RunlayerClient
from runlayer_cli.config import resolve_credentials, set_credentials_in_context
from runlayer_cli.console import print_error
from runlayer_cli.logging import setup_logging
from runlayer_cli.symbols import FAIL, OK, WARN

logger = structlog.get_logger(__name__)

TYPE_SHORTCUTS: dict[str, str] = {
    "auth": (
        "auth_success,auth_failed,"
        "proxy_oauth_token_issued,proxy_oauth_authorization_failed,"
        "client_token_refresh_failure,"
        "upstream_token_refresh_success,upstream_token_refresh_failure,"
        "oauth_connected,oauth_revoked"
    ),
    "tools": "tool_call_success,tool_call_failure",
    "security": "security_violation,access_denied,security_decision",
    "servers": (
        "server_created,server_updated,server_deleted,"
        "server_approved,server_rejected,server_disabled,server_enabled"
    ),
    "agents": (
        "agent_created,agent_updated,agent_deleted,"
        "agent_account_created,agent_account_enabled,"
        "agent_account_disabled,agent_account_deleted,"
        "agent_account_token_exchange_success,"
        "agent_account_token_exchange_denied"
    ),
}

_FAILURE_TYPES = {
    "auth_failed",
    "tool_call_failure",
    "proxy_oauth_authorization_failed",
    "client_token_refresh_failure",
    "upstream_token_refresh_failure",
    "access_denied",
    "server_rejected",
    "server_request_rejected",
    "access_request_rejected",
    "agent_account_token_exchange_denied",
    "enrollment_failed",
    "server_create_error",
    "server_update_error",
    "slack_app_create_failed",
}

_WARNING_TYPES = {
    "security_violation",
    "security_decision",
    "shadow_mcp_detected",
    "shadow_skill_detected",
    "shadow_skill_medium_risk",
    "shadow_skill_high_risk",
    "skill_import_medium_risk",
    "skill_import_high_risk",
}


def _status_style(action_type: str) -> tuple[str, str]:
    if action_type in _FAILURE_TYPES:
        return FAIL, "red"
    if action_type in _WARNING_TYPES:
        return WARN, "yellow"
    return OK, "green"


def _format_details(action_type: str, details: dict[str, Any]) -> str:
    if not details:
        return ""

    if action_type == "auth_success":
        parts = []
        if details.get("auth_method"):
            parts.append(details["auth_method"])
        if details.get("client_name"):
            parts.append(details["client_name"])
        return ", ".join(parts)

    if action_type == "auth_failed":
        return details.get("reason", "")

    if action_type == "proxy_oauth_token_issued":
        parts = []
        if details.get("grant_type"):
            parts.append(f"{details['grant_type']} grant")
        if details.get("client_name"):
            parts.append(f"client: {details['client_name']}")
        return ", ".join(parts)

    if action_type in (
        "proxy_oauth_authorization_failed",
        "client_token_refresh_failure",
    ):
        return details.get("error_reason", "")

    if action_type == "security_violation":
        return details.get("violation_reason", "")

    if action_type == "access_denied":
        return details.get("reason", "")

    if action_type in ("tool_call_success", "tool_call_failure"):
        return details.get("resource_name", "")

    if action_type == "upstream_token_refresh_success":
        return details.get("oauth_vendor") or ""

    if action_type == "upstream_token_refresh_failure":
        return details.get("error", "")

    # Default: show a few key fields
    skip = {
        "event_type",
        "subject_id",
        "subject_type",
        "correlation_id",
        "resource_type",
        "resource_id",
        "resource_name",
    }
    parts = []
    for k, v in details.items():
        if k in skip or v is None or isinstance(v, (dict, list)):
            continue
        parts.append(f"{k}={v}")
        if len(parts) >= 3:
            break
    return ", ".join(parts)


def _format_resource(log: dict[str, Any]) -> str:
    # Prefer human-readable server_name from details over resource_info
    # (resource_info.name is often a UUID for token/session resources)
    details = log.get("details")
    if isinstance(details, dict):
        for key in ("server_name", "resource_name"):
            if details.get(key):
                return details[key]

    resource_info = log.get("resource_info")
    if resource_info and resource_info.get("name"):
        return resource_info["name"]

    return "\u2014"


def _describe_range(start: str | None, end: str | None) -> str:
    if start and end:
        return f"{start} to {end}"
    if start:
        return f"since {start}"
    return "last 7 days"


def _expand_type(value: str) -> str:
    return ",".join(TYPE_SHORTCUTS.get(s.strip(), s.strip()) for s in value.split(","))


def logs(
    ctx: typer.Context,
    event_type: str | None = typer.Option(
        None,
        "--type",
        "-t",
        help=(
            "Filter by action type(s). Comma-separated or use shortcuts: "
            + ", ".join(TYPE_SHORTCUTS)
        ),
    ),
    server_id: str | None = typer.Option(
        None, "--server-id", help="Filter by MCP server UUID"
    ),
    agent_id: str | None = typer.Option(
        None, "--agent-id", help="Filter by agent account UUID"
    ),
    client_name: str | None = typer.Option(
        None, "--client-name", help="Filter by client name in event details"
    ),
    user_id: str | None = typer.Option(
        None, "--user-id", help="Filter by user ID (admin only, defaults to self)"
    ),
    all_users: bool = typer.Option(
        False, "--all", help="Show all users' logs (admin only, default: own logs)"
    ),
    start: str | None = typer.Option(
        None, "--start", help="Start time (ISO 8601). Default: 7 days ago"
    ),
    end: str | None = typer.Option(
        None, "--end", help="End time (ISO 8601). Default: now"
    ),
    limit: int = typer.Option(
        50, "--limit", "-n", help="Max events to return (max 2000)"
    ),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON"),
    secret: str | None = typer.Option(
        None, "--secret", "-s", help="API secret for authentication"
    ),
    host: str | None = typer.Option(None, "--host", "-H", help="Runlayer host URL"),
) -> None:
    """Query audit logs from Runlayer."""
    log_file_path = setup_logging(command="logs")
    set_credentials_in_context(ctx, secret, host)
    credentials = resolve_credentials(ctx, require_auth=True)

    api_client = RunlayerClient(
        hostname=credentials["host"], secret=credentials["secret"]
    )

    action_type = _expand_type(event_type) if event_type else None

    start_date = start or (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
    end_date = end

    # Default to own logs; --all or --user-id overrides
    actor_id: str | None = None
    if not all_users and not user_id:
        try:
            me = api_client.get_current_user()
            actor_id = me.get("id")
        except Exception as exc:
            logger.warning(
                "Failed to resolve current user", error=str(exc), exc_info=True
            )

    try:
        result = api_client.get_audit_logs(
            action_type=action_type,
            server_id=server_id,
            agent_id=agent_id,
            actor_id=actor_id,
            client_name=client_name,
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            limit=min(limit, 2000),
        )
    except Exception as e:
        logger.error(
            "Failed to fetch audit logs",
            error=str(e),
            error_type=type(e).__name__,
            exc_info=True,
        )
        print_error(str(e), str(log_file_path))
        raise typer.Exit(1)

    events = result.get("data", [])
    count = result.get("count", len(events))

    if json_output:
        typer.echo(json.dumps(events, indent=2, default=str))
        return

    # Table output
    typer.secho(
        f"\nAudit Logs ({_describe_range(start, end)}, {count} total, showing {len(events)})",
        bold=True,
        err=True,
    )
    typer.echo("=" * 70, err=True)

    if not events:
        typer.echo("No events found.", err=True)
        return

    for log in events:
        ts_raw = log.get("timestamp", "")
        try:
            ts = datetime.fromisoformat(ts_raw).astimezone()
            ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            ts_str = str(ts_raw)[:19]

        action = log.get("action_type", "unknown")
        symbol, color = _status_style(action)
        resource = _format_resource(log)
        details = log.get("details", {})
        if not isinstance(details, dict):
            details = {}
        detail_str = _format_details(action, details)

        actor_info = log.get("actor_info")
        actor_str = ""
        if actor_info:
            actor_str = actor_info.get("email") or actor_info.get("name") or ""

        action_display = action[:35]
        resource_display = resource[:25]
        detail_display = detail_str

        if actor_str and user_id:
            line = f"  {ts_str}  {symbol} {actor_str:<20} {action_display:<30} {resource_display:<20} {detail_display}"
        else:
            line = f"  {ts_str}  {symbol} {action_display:<35} {resource_display:<25} {detail_display}"
        typer.secho(line, fg=color, err=True)

    if count > len(events):
        last_ts_raw = events[-1].get("timestamp", "")
        try:
            last_dt = datetime.fromisoformat(last_ts_raw)
            next_end = (last_dt - timedelta(microseconds=1)).isoformat()
        except (ValueError, TypeError):
            next_end = last_ts_raw
        next_parts = ["runlayer logs", f"--end {next_end}"]
        if start:
            next_parts.append(f"--start {start}")
        if event_type:
            next_parts.append(f"-t {event_type}")
        if server_id:
            next_parts.append(f"--server-id {server_id}")
        if agent_id:
            next_parts.append(f"--agent-id {agent_id}")
        if client_name:
            next_parts.append(f"--client-name {client_name}")
        if user_id:
            next_parts.append(f"--user-id {user_id}")
        if all_users:
            next_parts.append("--all")
        next_parts.append(f"-n {limit}")
        typer.echo(
            f"\n  ... {count - len(events)} more events. Next page:",
            err=True,
        )
        typer.secho(f"  {' '.join(next_parts)}", fg=typer.colors.CYAN, err=True)
    typer.echo("", err=True)
