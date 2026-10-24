# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Plan and execute the Project Lighthouse daily outreach job."""

from __future__ import annotations

import json
import logging
import os
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal
from importlib.resources import files
from pathlib import Path
from typing import Any

import google.auth.exceptions
from google.cloud import bigquery

from airbyte_ops_mcp import slack_posting
from airbyte_ops_mcp.gcp_auth import (
    get_gcp_credentials_for_bigquery,
    get_gcp_credentials_for_prod_db_replica,
)
from airbyte_ops_mcp.prod_db_access.queries import (
    query_org_admin_contacts,
    query_org_user_last_connection_events,
)
from airbyte_ops_mcp.zendesk_api import (
    ZendeskAPIError,
    add_internal_note,
    add_ticket_tags,
    create_ticket,
    find_organizations_by_airbyte_org_id,
    find_ticket_form_id,
    get_current_user,
    get_ticket_comments,
    list_tickets_by_external_id,
    resolve_zendesk_credentials,
    search,
)

logger = logging.getLogger(__name__)

BIGGEST_OFF = "biggest_off"
TOP3_FAILING = "top3_failing"
HALF_FAILING = "half_failing"
TRIGGER_ORDER = {BIGGEST_OFF: 0, TOP3_FAILING: 1, HALF_FAILING: 2}
OPEN_STATUSES = frozenset({"new", "open", "pending", "hold"})
PERSONAL_ACCOUNT_ID = "0015e000017PIPhAAO"
PERSONAL_ACCOUNT_PURCHASES_ID = PERSONAL_ACCOUNT_ID
LIGHTHOUSE_SLACK_CHANNEL = "C02U1H7M71A"
PROJECT_ID = "airbyte-data-prod"
_NO_MOONBOT = object()


@dataclass(frozen=True)
class LighthouseRunResult:
    """The complete plan and status for one Lighthouse run."""

    actions: list[dict[str, Any]]
    markdown: str
    errors: list[str]
    plan_path: Path

    @property
    def failed(self) -> bool:
        """Return whether any part of the run failed."""
        return bool(self.errors)


def load_trigger_sql() -> str:
    """Load the packaged BigQuery trigger query."""
    return files(__package__).joinpath("triggers.sql").read_text(encoding="utf-8")


def query_fires(run_date: date) -> list[dict[str, Any]]:
    """Run the Lighthouse BigQuery script for `run_date`."""
    client = bigquery.Client(
        project=PROJECT_ID,
        credentials=get_gcp_credentials_for_bigquery(),
    )
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("run_date", "DATE", run_date),
        ],
    )
    return [
        _as_mapping(row)
        for row in client.query(load_trigger_sql(), job_config=job_config).result()
    ]


def _as_mapping(value: Any) -> dict[str, Any]:
    """Convert a BigQuery row or mapping to a regular dictionary."""
    if isinstance(value, Mapping):
        return dict(value)
    if hasattr(value, "items"):
        return dict(value.items())
    return {}


def _as_date(value: Any) -> date:
    """Return a date value from BigQuery or Zendesk-compatible input."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value)[:10])


def _as_datetime(value: Any) -> datetime | None:
    """Parse a timestamp while preserving UTC ordering for naive values."""
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, date):
        parsed = datetime.combine(value, time.min)
    elif isinstance(value, str) and value:
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    else:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _json_safe(value: Any) -> Any:
    """Convert query and action data to JSON-serializable values."""
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if hasattr(value, "items"):
        return {str(key): _json_safe(item) for key, item in value.items()}
    return str(value)


def _connections(fire: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Return the connections for a trigger as ordinary mappings."""
    value = fire.get("connections") or []
    return [_as_mapping(connection) for connection in value]


def _first_connection(fire: Mapping[str, Any]) -> dict[str, Any]:
    """Return the first connection, or an empty mapping for malformed input."""
    connections = _connections(fire)
    return connections[0] if connections else {}


def _connector_pair(connection: Mapping[str, Any]) -> tuple[str, str]:
    """Return source and destination names with readable fallbacks."""
    return (
        str(connection.get("source_connector_name") or "unknown source"),
        str(connection.get("destination_connector_name") or "unknown destination"),
    )


def _days_of_syncs(value: Any) -> str:
    """Render the SQL lower bound for days of syncs."""
    days = int(value or 0)
    return "3+ months" if days >= 90 else f"{days} days"


def render_reason(fire: Mapping[str, Any]) -> str:
    """Render the customer-facing reason for one trigger."""
    connection = _first_connection(fire)
    source, destination = _connector_pair(connection)
    trigger_type = fire.get("trigger_type")
    if trigger_type == BIGGEST_OFF:
        return (
            f"biggest connection ({source} → {destination}) turned off after "
            f"{_days_of_syncs(connection.get('days_of_syncs'))} of syncs"
        )
    if trigger_type == TOP3_FAILING:
        return (
            f"#{connection.get('conn_rank')} connection ({source} → {destination}) "
            "failing 3 days in a row"
        )
    if trigger_type == HALF_FAILING:
        return (
            f"{fire.get('n_connections_failing')} of "
            f"{fire.get('n_connections_with_jobs')} connections failing for 3 days"
        )
    raise ValueError(f"Unknown Lighthouse trigger type: {trigger_type!r}")


def render_subject(fire: Mapping[str, Any]) -> str:
    """Render the Zendesk subject for one trigger."""
    connection = _first_connection(fire)
    source, destination = _connector_pair(connection)
    trigger_type = fire.get("trigger_type")
    if trigger_type == BIGGEST_OFF:
        return f"Airbyte // Checking in on your {source} → {destination} connection"
    if trigger_type == TOP3_FAILING:
        return f"Airbyte // Your {source} → {destination} connection is failing"
    if trigger_type == HALF_FAILING:
        return "Airbyte // Several of your connections are failing"
    raise ValueError(f"Unknown Lighthouse trigger type: {trigger_type!r}")


def render_draft(fire: Mapping[str, Any], *, requester_name: str | None = None) -> str:
    """Render the suggested first reply for one trigger."""
    connection = _first_connection(fire)
    source, destination = _connector_pair(connection)
    requester_name_parts = (requester_name or "").split()
    first_name = requester_name_parts[0] if requester_name_parts else "there"
    trigger_type = fire.get("trigger_type")
    if trigger_type == BIGGEST_OFF:
        off_date = _as_date(fire["fire_date"]) - timedelta(days=3)
        return (
            f"Hi {first_name},\n\nI'm reaching out from Airbyte Support because we "
            f"noticed your {source} → {destination} connection was turned off on "
            f"{off_date.isoformat()}. If that was planned, there's nothing you need "
            "to do.\n\nIf it was turned off because of a problem, or you'd like a "
            "hand with anything, just reply here and we'll help you get it running "
            "again."
        )
    if trigger_type == TOP3_FAILING:
        streak_start = _as_date(fire["fire_date"]) - timedelta(days=2)
        draft = (
            f"Hi {first_name},\n\nI'm reaching out from Airbyte Support because your "
            f"{source} → {destination} connection has failed every sync since "
            f"{streak_start.isoformat()}."
        )
        last_error = connection.get("last_error")
        if last_error:
            draft += f" The latest error was:\n\n{last_error}"
        return (
            f"{draft}\n\nWe'd like to help get it syncing again. Reply here and we "
            "can take a look together."
        )
    if trigger_type == HALF_FAILING:
        failing_lines = [
            f"- {conn_source} → {conn_destination} "
            f"({connection_item.get('connection_name') or 'unnamed connection'})"
            for connection_item in _connections(fire)
            for conn_source, conn_destination in [_connector_pair(connection_item)]
        ]
        lines = "\n".join(failing_lines)
        return (
            f"Hi {first_name},\n\nI'm reaching out from Airbyte Support because "
            f"{fire.get('n_connections_failing')} of your "
            f"{fire.get('n_connections_with_jobs')} connections have failed every "
            f"sync for the last 3 days:\n{lines}\n\nWe'd like to help get them "
            "syncing again. Reply here and we can take a look together."
        )
    raise ValueError(f"Unknown Lighthouse trigger type: {trigger_type!r}")


def _escape_html(value: Any) -> str:
    """Escape text values before embedding them in an internal HTML note."""
    text = str(value)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )


def _lighthouse_key(fire: Mapping[str, Any]) -> str:
    """Build the stable idempotency key for one trigger fire."""
    return (
        f"lighthouse:{fire['organization_id']}:{fire['trigger_type']}:"
        f"{_as_date(fire['fire_date']).isoformat()}"
    )


def render_internal_note(
    fire: Mapping[str, Any],
    *,
    display_name: str,
    requester_name: str | None,
    other_admin_emails: Sequence[str],
    no_contact: bool,
) -> str:
    """Render the private HTML note attached to a Lighthouse ticket."""
    key = _lighthouse_key(fire)
    reason = render_reason(fire)
    arr = Decimal(str(fire.get("self_serve_arr") or 0))
    profile_month_end = _as_date(fire["profile_month_end"]).isoformat()
    connection_items: list[str] = []
    for connection in _connections(fire):
        source, destination = _connector_pair(connection)
        name = _escape_html(connection.get("connection_name") or "unnamed connection")
        cloud_url = connection.get("cloud_url")
        label = f"{name}: {_escape_html(source)} → {_escape_html(destination)}"
        if cloud_url:
            label = f'<a href="{_escape_html(cloud_url)}">{label}</a>'
        extra: list[str] = []
        spend = connection.get("usd_ok_30d")
        if spend is not None:
            extra.append(f"30-day spend: ${Decimal(str(spend)):,.2f}")
        last_error = connection.get("last_error")
        if last_error:
            extra.append(f"Last error: {_escape_html(last_error)}")
        if extra:
            label += f" ({'; '.join(extra)})"
        connection_items.append(f"<li>{label}</li>")
    admins = ", ".join(_escape_html(email) for email in other_admin_emails) or "none"
    parts = [
        "<p>Automated note from Project Lighthouse (airbyte-ops-mcp lighthouse job).</p>",
        f"<p>Trigger: {_escape_html(reason)}.</p>",
        (
            f"<p>Account: {_escape_html(display_name)}, org "
            f"{_escape_html(fire['organization_id'])}, ARR at trigger "
            f"${arr:,.0f} (profile month-end {profile_month_end}).</p>"
        ),
    ]
    if connection_items:
        parts.append(f"<ul>{''.join(connection_items)}</ul>")
    if no_contact:
        parts.append(
            "<p>No admin contact found — set the requester before replying.</p>"
        )
    parts.extend(
        [
            f"<p>Other admins (add as CC when replying): {admins}</p>",
            f"<p>Lighthouse key: {_escape_html(key)}</p>",
            "<p>Draft first reply (edit before sending):</p>",
            f"<p>{_escape_html(render_draft(fire, requester_name=requester_name)).replace(chr(10), '<br>')}</p>",
        ]
    )
    return "".join(parts)


def _ticket_org_and_trigger(ticket: Mapping[str, Any]) -> tuple[str, str] | None:
    """Parse the organization and trigger type from a Lighthouse ticket key."""
    external_id = ticket.get("external_id")
    if not isinstance(external_id, str):
        return None
    pieces = external_id.split(":")
    if len(pieces) != 4 or pieces[0] != "lighthouse":
        return None
    return pieces[1], pieces[2]


def _is_open(ticket: Mapping[str, Any]) -> bool:
    """Return whether a Zendesk ticket is currently open."""
    return str(ticket.get("status") or "").lower() in OPEN_STATUSES


def _within_cooldown(
    ticket: Mapping[str, Any], *, run_date: date, trigger_type: str
) -> bool:
    """Return whether a closed ticket for this trigger is in its cooldown."""
    parsed = _ticket_org_and_trigger(ticket)
    if parsed is None or parsed[1] != trigger_type:
        return False
    if str(ticket.get("status") or "").lower() not in {"solved", "closed"}:
        return False
    updated_at = _as_datetime(ticket.get("updated_at"))
    if updated_at is None:
        return False
    updated_date = updated_at.date()
    return run_date - timedelta(days=30) <= updated_date <= run_date


def choose_action(
    fire: Mapping[str, Any],
    *,
    existing_for_key: Sequence[Mapping[str, Any]],
    indexed_tickets: Sequence[Mapping[str, Any]],
    run_date: date,
) -> tuple[str, Mapping[str, Any] | None]:
    """Choose the idempotent Zendesk action for one trigger fire."""
    if existing_for_key:
        return "skip_exists", existing_for_key[0]
    org_id = str(fire["organization_id"])
    open_tickets = [
        ticket
        for ticket in indexed_tickets
        if _ticket_org_and_trigger(ticket)
        and _ticket_org_and_trigger(ticket)[0] == org_id
        and _is_open(ticket)
    ]
    if open_tickets:
        selected = sorted(
            open_tickets,
            key=lambda ticket: (
                _as_datetime(ticket.get("updated_at"))
                or datetime.min.replace(tzinfo=timezone.utc),
                int(ticket.get("id") or 0),
            ),
            reverse=True,
        )[0]
        return "note", selected
    if any(
        _within_cooldown(
            ticket, run_date=run_date, trigger_type=str(fire["trigger_type"])
        )
        for ticket in indexed_tickets
        if _ticket_org_and_trigger(ticket)
        and _ticket_org_and_trigger(ticket)[0] == org_id
    ):
        return "skip_cooldown", None
    return "create", None


def has_lighthouse_key(comments: Sequence[Mapping[str, Any]], key: str) -> bool:
    """Return whether ticket comments already contain the trigger key."""
    line = f"Lighthouse key: {key}"
    return any(line in str(comment.get("body") or "") for comment in comments)


def select_requesters(
    contact_rows: Sequence[Mapping[str, Any]],
    activity_rows: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, Any] | None, list[str]]:
    """Filter and order contacts, returning the primary and other admin emails."""
    activity_by_user: dict[str, datetime | None] = {}
    for row in activity_rows:
        activity_by_user[str(row.get("user_id"))] = _as_datetime(
            row.get("last_connection_event_at")
        )

    users: dict[str, dict[str, Any]] = {}
    for row in contact_rows:
        email = str(row.get("user_email") or "").strip()
        if not email or email.casefold().endswith("@airbyte.io"):
            continue
        if str(row.get("user_status") or "").strip().casefold() == "disabled":
            continue
        user_id = str(row.get("user_id") or email.casefold())
        user = users.get(user_id)
        if user is None:
            user = {
                "name": str(row.get("user_name") or "").strip(),
                "email": email,
                "is_org_admin": False,
                "user_updated_at": _as_datetime(row.get("user_updated_at")),
            }
            users[user_id] = user
        user["is_org_admin"] = user["is_org_admin"] or (
            row.get("admin_role") == "organization_admin"
        )
        updated_at = _as_datetime(row.get("user_updated_at"))
        if updated_at and (
            user["user_updated_at"] is None or updated_at > user["user_updated_at"]
        ):
            user["user_updated_at"] = updated_at
    contacts = [
        {
            **user,
            "last_connection_event_at": activity_by_user.get(user_id),
        }
        for user_id, user in users.items()
    ]
    contacts.sort(
        key=lambda user: (
            not user["is_org_admin"],
            user["last_connection_event_at"] is None,
            -(
                user["last_connection_event_at"].timestamp()
                if user["last_connection_event_at"]
                else 0
            ),
            user["user_updated_at"] is None,
            -(user["user_updated_at"].timestamp() if user["user_updated_at"] else 0),
            user["email"].casefold(),
        )
    )
    if not contacts:
        return None, []
    primary = contacts[0]
    return primary, [user["email"] for user in contacts[1:]]


def _markdown_escape(value: Any) -> str:
    """Escape a value for inclusion in a Markdown table cell."""
    return str(value or "").replace("|", "\\|").replace("\n", " ")


def _email_domain(value: Any) -> str | None:
    """Return only the domain portion of an email address."""
    email = str(value or "").strip()
    local_part, separator, domain = email.rpartition("@")
    return domain.casefold() if local_part and separator and domain else None


def render_markdown(actions: Sequence[Mapping[str, Any]]) -> str:
    """Render the per-trigger action summary table."""
    lines = [
        "# Project Lighthouse",
        "",
        "| Org | Display name | ARR | Trigger | Reason | Action | Requester email | Connection URL |",
        "| --- | --- | ---: | --- | --- | --- | --- | --- |",
    ]
    for action in actions:
        arr = action.get("self_serve_arr")
        arr_text = f"${Decimal(str(arr)):,.0f}" if arr is not None else ""
        connection_url = action.get("connection_url")
        link = ""
        if connection_url:
            url = str(connection_url)
            if url.startswith(
                ("https://cloud.airbyte.com/", "https://cloud.airbyte.io/")
            ):
                safe_url = _markdown_escape(url).replace("(", "%28").replace(")", "%29")
                link = f"[connection]({safe_url})"
            else:
                safe_url = _markdown_escape(url).replace("`", "&#96;")
                link = f"`{safe_url}`"
        lines.append(
            "| "
            + " | ".join(
                (
                    _markdown_escape(action.get("organization_id")),
                    _markdown_escape(action.get("display_name")),
                    arr_text,
                    _markdown_escape(action.get("trigger_type")),
                    _markdown_escape(action.get("reason")),
                    _markdown_escape(action.get("action")),
                    _markdown_escape(_email_domain(action.get("requester_email"))),
                    link,
                )
            )
            + " |"
        )
    if not actions:
        lines.append("| — | — | — | — | No fires | — | — | — |")
    return "\n".join(lines)


def _redact_plan_action(action: Mapping[str, Any]) -> dict[str, Any]:
    """Redact requester PII from the serialized plan without mutating live data."""
    redacted = dict(action)
    for key in ("requester_name", "internal_note_html", "draft"):
        redacted.pop(key, None)

    if "requester_email" in redacted:
        redacted["requester_email"] = _email_domain(redacted["requester_email"])
    if "other_admin_emails" in redacted:
        redacted["other_admin_emails"] = [
            domain
            for email in redacted["other_admin_emails"]
            if (domain := _email_domain(email)) is not None
        ]

    ticket_payload = redacted.get("ticket_payload")
    if isinstance(ticket_payload, Mapping):
        safe_payload = dict(ticket_payload)
        safe_payload.pop("requester", None)
        comment = safe_payload.get("comment")
        if isinstance(comment, Mapping):
            safe_comment = dict(comment)
            for key in ("html_body", "body"):
                if key in safe_comment:
                    safe_comment[key] = "[redacted]"
            safe_payload["comment"] = safe_comment
        redacted["ticket_payload"] = safe_payload
    return redacted


def _write_plan(
    path: Path, actions: Sequence[Mapping[str, Any]], errors: Sequence[str]
) -> None:
    """Write the complete plan artifact without exposing credential values."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "actions": _json_safe(
                    [_redact_plan_action(action) for action in actions]
                ),
                "errors": list(errors),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def _zendesk_org(
    organization_id: str,
    *,
    credentials: Any,
    cache: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    """Look up and cache Zendesk organizations for one Airbyte org."""
    if organization_id not in cache:
        cache[organization_id] = find_organizations_by_airbyte_org_id(
            organization_id, credentials=credentials
        )
    return cache[organization_id]


def _merge_indexed_tickets(
    indexed_tickets: Sequence[Mapping[str, Any]],
    additional_tickets: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Merge ticket search results, keeping one record per Zendesk ticket ID."""
    merged: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for ticket in (*indexed_tickets, *additional_tickets):
        ticket_data = dict(ticket)
        ticket_id = ticket_data.get("id")
        if ticket_id is not None:
            ticket_id_key = str(ticket_id)
            if ticket_id_key in seen_ids:
                continue
            seen_ids.add(ticket_id_key)
        merged.append(ticket_data)
    return merged


def _display_name(
    fire: Mapping[str, Any], organizations: Sequence[Mapping[str, Any]]
) -> str:
    """Choose the account or Zendesk organization display name."""
    account_name = fire.get("account_name")
    personal = str(
        fire.get("account_id") or ""
    ) == PERSONAL_ACCOUNT_PURCHASES_ID or bool(fire.get("is_personal_email"))
    if account_name and not personal:
        return str(account_name)
    for organization in organizations:
        if organization.get("name"):
            return str(organization["name"])
    return f"org {str(fire['organization_id'])[:8]}"


def _requester_for_fire(
    fire: Mapping[str, Any], run_date: date
) -> tuple[dict[str, Any] | None, list[str]]:
    """Query admin contacts and activity for this fire's workspaces."""
    workspace_ids = sorted(
        {
            str(connection["workspace_id"])
            for connection in _connections(fire)
            if connection.get("workspace_id")
        }
    )
    contact_rows = query_org_admin_contacts(str(fire["organization_id"]), workspace_ids)
    user_ids = sorted(
        {str(row["user_id"]) for row in contact_rows if row.get("user_id")}
    )
    activity_rows: list[dict[str, Any]] = []
    if user_ids:
        cutoff = datetime.combine(run_date, time.min, tzinfo=timezone.utc) - timedelta(
            days=90
        )
        activity_rows = query_org_user_last_connection_events(
            str(fire["organization_id"]), user_ids, cutoff
        )
    return select_requesters(contact_rows, activity_rows)


def _ticket_tags(fire: Mapping[str, Any], *, no_contact: bool) -> list[str]:
    """Build Lighthouse ticket tags in stable order."""
    tags = ["outreach", "lighthouse", f"lighthouse_{fire['trigger_type']}"]
    if str(fire.get("account_id") or "") == PERSONAL_ACCOUNT_ID or bool(
        fire.get("is_personal_email")
    ):
        tags.append("lighthouse_personal")
    if no_contact:
        tags.append("lighthouse_no_contact")
    return tags


def _prod_db_credentials_available() -> bool:
    """Return whether GCP credentials for the prod DB replica resolve (key or ADC)."""
    try:
        get_gcp_credentials_for_prod_db_replica()
    except google.auth.exceptions.DefaultCredentialsError:
        return False
    return True


def run_lighthouse(
    run_date: date,
    *,
    live: bool = False,
    plan_path: str | Path = "lighthouse_plan.json",
) -> LighthouseRunResult:
    """Plan or execute Lighthouse actions for `run_date`.

    Zendesk and Slack writes are impossible unless `live` is `True`.
    """
    destination = Path(plan_path)
    errors: list[str] = []
    try:
        fires = [_as_mapping(fire) for fire in query_fires(run_date)]
    except Exception as exc:
        message = (
            f"BigQuery trigger query failed ({type(exc).__name__}: {str(exc)[:500]})."
        )
        logger.error(message)
        errors.append(message)
        markdown = render_markdown([])
        _write_plan(destination, [], errors)
        _write_step_summary(markdown, errors)
        return LighthouseRunResult([], markdown, errors, destination)

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for fire in fires:
        grouped[str(fire["organization_id"])].append(fire)
    for org_fires in grouped.values():
        org_fires.sort(
            key=lambda fire: (
                TRIGGER_ORDER.get(str(fire.get("trigger_type")), 99),
                str(fire.get("trigger_type") or ""),
            )
        )

    slack_token: str | None = None
    if live:
        try:
            slack_token = slack_posting.resolve_slack_bot_token()
        except Exception as exc:
            logger.error("Slack bot token resolution failed (%s)", type(exc).__name__)

    zendesk_credentials = None
    zendesk_available = True
    try:
        zendesk_credentials = resolve_zendesk_credentials()
    except ZendeskAPIError as exc:
        zendesk_available = False
        message = f"Zendesk credentials unavailable ({type(exc).__name__})."
        logger.error(message)
        errors.append(message)

    indexed_tickets: list[dict[str, Any]] = []
    search_error = False
    if zendesk_available:
        cutoff = run_date - timedelta(days=120)
        for query in (
            f"type:ticket tags:lighthouse created>{cutoff.isoformat()}",
            "type:ticket tags:lighthouse status<solved",
        ):
            try:
                results = search(
                    query,
                    max_results=1000,
                    credentials=zendesk_credentials,
                )
                indexed_tickets = _merge_indexed_tickets(indexed_tickets, results)
            except Exception as exc:
                search_error = True
                message = (
                    f"Zendesk Lighthouse ticket search failed ({type(exc).__name__})."
                )
                logger.error(message)
                errors.append(message)

    organization_cache: dict[str, list[dict[str, Any]]] = {}
    moonbot: dict[str, Any] | object = _NO_MOONBOT
    actions: list[dict[str, Any]] = []
    db_credentials_present = _prod_db_credentials_available()
    for organization_id in sorted(grouped):
        for fire in grouped[organization_id]:
            key = _lighthouse_key(fire)
            action_data: dict[str, Any] = {
                "organization_id": organization_id,
                "fire_date": _as_date(fire["fire_date"]),
                "profile_month_end": _as_date(fire["profile_month_end"]),
                "trigger_type": fire["trigger_type"],
                "self_serve_arr": fire.get("self_serve_arr"),
                "reason": render_reason(fire),
                "subject": render_subject(fire),
                "key": key,
                "connections": _connections(fire),
                "connection_url": _first_connection(fire).get("cloud_url"),
                "status": "planned",
                "live": live,
            }
            try:
                organizations: list[dict[str, Any]] = []
                if zendesk_available:
                    organizations = _zendesk_org(
                        organization_id,
                        credentials=zendesk_credentials,
                        cache=organization_cache,
                    )
                display_name = _display_name(fire, organizations)
                action_data["display_name"] = display_name
                zendesk_org_id = (
                    organizations[0].get("id") if len(organizations) == 1 else None
                )
                zendesk_org_name = (
                    organizations[0].get("name") if len(organizations) == 1 else None
                )
                action_data["zendesk_organization_id"] = zendesk_org_id
                action_data["zendesk_organization_name"] = zendesk_org_name

                requester_contact: dict[str, Any] | None = None
                other_admin_emails: list[str] = []
                if db_credentials_present:
                    requester_contact, other_admin_emails = _requester_for_fire(
                        fire, run_date
                    )
                no_contact = requester_contact is None
                if no_contact:
                    action_data["requester_name"] = "MoonBot"
                    action_data["requester_email"] = None
                    action_data["other_admin_emails"] = []
                else:
                    action_data["requester_name"] = requester_contact["name"] or None
                    action_data["requester_email"] = requester_contact["email"]
                    action_data["other_admin_emails"] = other_admin_emails

                if zendesk_available:
                    existing_for_key = list_tickets_by_external_id(
                        key, credentials=zendesk_credentials
                    )
                    selected_action, ticket = choose_action(
                        fire,
                        existing_for_key=existing_for_key,
                        indexed_tickets=indexed_tickets,
                        run_date=run_date,
                    )
                    if selected_action == "skip_exists" and ticket and _is_open(ticket):
                        indexed_tickets.append(dict(ticket))
                    if selected_action == "create" and search_error:
                        selected_action = "error"
                        action_data["error"] = (
                            "Zendesk ticket search failed; refusing to create without "
                            "checking for an open or cooldown ticket."
                        )
                    if (
                        live
                        and selected_action in {"create", "note"}
                        and slack_token is None
                    ):
                        selected_action = "error"
                        action_data["error"] = (
                            "Slack bot token is unavailable; no ticket changes were made."
                        )
                    if selected_action == "note" and ticket is not None:
                        comments = get_ticket_comments(
                            ticket["id"], credentials=zendesk_credentials
                        )
                        action_data["note_already_present"] = has_lighthouse_key(
                            comments, key
                        )
                    action_data["ticket_id"] = ticket.get("id") if ticket else None
                    action_data["action"] = selected_action
                else:
                    action_data["action"] = (
                        "create (unchecked)" if not live else "error"
                    )
                    if live:
                        action_data["error"] = "Zendesk credentials are unavailable."

                if action_data["action"] in {"create", "create (unchecked)", "note"}:
                    if zendesk_available and moonbot is _NO_MOONBOT:
                        moonbot = get_current_user(credentials=zendesk_credentials)
                    moonbot_user = (
                        moonbot if isinstance(moonbot, dict) else {"name": "MoonBot"}
                    )
                    requester_name = (
                        requester_contact.get("name")
                        if requester_contact is not None
                        else None
                    )
                    action_data["no_contact"] = no_contact
                    action_data["draft"] = render_draft(
                        fire, requester_name=requester_name
                    )
                    action_data["internal_note_html"] = render_internal_note(
                        fire,
                        display_name=display_name,
                        requester_name=requester_name,
                        other_admin_emails=other_admin_emails,
                        no_contact=no_contact,
                    )
                    action_data["tags"] = _ticket_tags(fire, no_contact=no_contact)
                    if action_data["action"] in {"create", "create (unchecked)"}:
                        ticket_form_id = (
                            find_ticket_form_id(
                                "Support Outreach", credentials=zendesk_credentials
                            )
                            if zendesk_available
                            else None
                        )
                        current_user_id = moonbot_user.get("id")
                        payload: dict[str, Any] = {
                            "subject": action_data["subject"],
                            "comment": {
                                "html_body": action_data["internal_note_html"],
                                "public": False,
                            },
                            "status": "new",
                            "priority": "normal",
                            "tags": action_data["tags"],
                            "external_id": key,
                            "ticket_form_id": ticket_form_id,
                            "submitter_id": current_user_id,
                        }
                        if zendesk_org_id is not None:
                            payload["organization_id"] = zendesk_org_id
                        if requester_contact is not None:
                            payload["requester"] = {
                                "name": requester_contact["name"] or "",
                                "email": requester_contact["email"],
                            }
                        else:
                            payload["requester_id"] = current_user_id
                        action_data["ticket_payload"] = payload

                if action_data["action"] == "error":
                    errors.append(
                        f"{organization_id} {fire['trigger_type']}: "
                        f"{action_data.get('error', 'unable to determine action')}"
                    )
                    action_data["status"] = "error"
                    actions.append(action_data)
                    continue

                if live and zendesk_available:
                    selected_action = action_data["action"]
                    ticket_id = action_data.get("ticket_id")
                    note_added = False
                    if selected_action == "create":
                        created_ticket = create_ticket(
                            action_data["ticket_payload"],
                            credentials=zendesk_credentials,
                        )
                        ticket_id = created_ticket.get("id")
                        if ticket_id is None:
                            raise ZendeskAPIError(
                                "Zendesk create response did not include a ticket ID."
                            )
                        action_data["ticket_id"] = ticket_id
                        action_data["status"] = "created"
                        try:
                            duplicate_check = list_tickets_by_external_id(
                                key, credentials=zendesk_credentials
                            )
                            if len(duplicate_check) > 1:
                                message = f"Multiple Zendesk tickets share Lighthouse key {key}."
                                logger.error(message)
                                errors.append(message)
                                action_data["error"] = message
                            elif duplicate_check:
                                created_ticket = duplicate_check[0]
                                ticket_id = created_ticket.get("id", ticket_id)
                                action_data["ticket_id"] = ticket_id
                        except Exception as exc:
                            message = (
                                f"Created ticket {ticket_id} but duplicate re-check failed: "
                                f"{type(exc).__name__}."
                            )
                            logger.error(message)
                            errors.append(message)
                            action_data["error"] = message
                        indexed_tickets.append(
                            {
                                **created_ticket,
                                "id": ticket_id,
                                "external_id": key,
                                "status": created_ticket.get("status", "new"),
                            }
                        )
                        note_added = True
                    elif selected_action == "note":
                        if not action_data.get("note_already_present"):
                            add_internal_note(
                                ticket_id,
                                action_data["internal_note_html"],
                                credentials=zendesk_credentials,
                            )
                            note_added = True
                        add_ticket_tags(
                            ticket_id,
                            [f"lighthouse_{fire['trigger_type']}"],
                            credentials=zendesk_credentials,
                        )
                        action_data["status"] = (
                            "note_already_present" if not note_added else "noted"
                        )
                    if ticket_id is not None and (
                        selected_action == "create" or note_added
                    ):
                        slack_text = (
                            f"<https://{zendesk_credentials.subdomain}.zendesk.com/"
                            f"agent/tickets/{ticket_id}|#{ticket_id}> · {display_name} "
                            f"· {action_data['reason']}"
                        )
                        if selected_action == "note":
                            slack_text += " (added to open ticket)"
                        try:
                            slack_posting.post_channel_message(
                                LIGHTHOUSE_SLACK_CHANNEL,
                                slack_text,
                                token=slack_token,
                            )
                            action_data["slack_posted"] = True
                        except Exception as exc:
                            message = (
                                f"Slack notice failed for ticket {ticket_id} "
                                f"({type(exc).__name__})."
                            )
                            logger.error(message)
                            errors.append(message)
                            action_data["error"] = message
                            action_data["status"] = "error"
                    if selected_action in {"skip_exists", "skip_cooldown"}:
                        action_data["status"] = selected_action
                elif not live:
                    action_data["status"] = "dry_run"
                elif not zendesk_available:
                    action_data["status"] = "error"
                actions.append(action_data)
            except Exception as exc:
                message = (
                    f"Lighthouse processing failed for {organization_id} "
                    f"{fire.get('trigger_type')} ({type(exc).__name__})."
                )
                logger.error(message)
                errors.append(message)
                action_data["action"] = "error"
                action_data["error"] = message
                action_data["status"] = "error"
                actions.append(action_data)

    markdown = render_markdown(actions)
    _write_plan(destination, actions, errors)
    _write_step_summary(markdown, errors)
    return LighthouseRunResult(actions, markdown, errors, destination)


def _write_step_summary(markdown: str, errors: Sequence[str]) -> None:
    """Append the run report to GitHub Actions when a summary path is configured."""
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    with Path(summary_path).open("a", encoding="utf-8") as summary_file:
        summary_file.write(markdown + "\n")
        if errors:
            summary_file.write("\n## Errors\n\n")
            summary_file.writelines(f"- {error}\n" for error in errors)
