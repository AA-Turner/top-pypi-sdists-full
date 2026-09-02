"""Local CLI and hook health for the native desktop tray applications."""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Literal, TypedDict
from urllib.parse import urlparse

import httpx
import typer

from runlayer_cli import __version__
from runlayer_cli.api import API_KEY_HEADER_NAME, USER_AGENT
from runlayer_cli.config import load_config
from runlayer_cli.enrollment import enrollment_marker_path
from runlayer_cli.hook_install.check import check_all
from runlayer_cli.hook_install.paths import (
    InstallScope,
    resolve_runlayer_hook_command,
)
from runlayer_cli.tls import http_client


CredentialStatus = Literal["ok", "missing"]

# Tray polls often; keep network enrichment snappy and never block status.
_ENRICH_TIMEOUT_SECONDS = 2.0
# Same FGA capability that gates the admin access-request surfaces.
_CAP_MANAGE_USER_MCP_ACCESS = "manage_user_mcp_access"
_ADMIN_SESSION_LIMIT = 3
_ADMIN_REQUEST_LIMIT = 5


class HostStatus(TypedDict):
    url: str
    credential: CredentialStatus
    enrolled: bool


class HookStatus(TypedDict):
    client: str
    status: str


class IdentityStatus(TypedDict):
    display_name: str
    email: str
    role: str | None
    space: str | None
    # Plumbing for upcoming admin tray surfaces, so they need no second call.
    can_manage_user_mcp_access: bool


class AttentionAccount(TypedDict):
    """One connector session the tray can reconnect via oauth/initiate."""

    account_id: str
    server_id: str
    label: str


class AttentionApprovalRequest(TypedDict):
    """One pending self-approval surfaced to the native tray."""

    id: str
    # "Approval needed: Server -> tool". A notification carrying an Approve
    # button has to name the action; the backend withholds the argument
    # preview from api-key callers, so this title is all the exact-action
    # context the tray gets. Empty against a backend that predates it.
    title: str
    can_decide_inline: bool


class AttentionStatus(TypedDict):
    """User-scoped work blockers for the tray menu and notifications."""

    accounts_needing_reconnect: int
    accounts: list[AttentionAccount]
    approval_requests_pending: int
    approval_requests: list[AttentionApprovalRequest]


class AdminSession(TypedDict):
    id: str
    title: str
    client: str
    started_at: str


class AdminAccessRequest(TypedDict):
    """One pending access request the tray can approve or reject."""

    id: str
    requester: str
    resource: str
    summary: str


class AdminStatus(TypedDict):
    """Admin tray glance when caller has manage_user_mcp_access."""

    sessions: list[AdminSession]
    access_requests: list[AdminAccessRequest]


class StatusSnapshot(TypedDict):
    version: str
    default_host: str | None
    dashboard_url: str | None
    hosts: list[HostStatus]
    hooks: list[HookStatus]
    identity: IdentityStatus | None
    attention: AttentionStatus | None
    admin: AdminStatus | None


def _space_label(*, email: str, host: str) -> str:
    """Best-effort org/space label without an org-name API round-trip."""
    if "@" in email:
        domain = email.rsplit("@", 1)[-1].strip().lower()
        head = domain.split(".", 1)[0]
        if head:
            return head.capitalize()
    hostname = urlparse(host).hostname
    return hostname or host


def _primary_role_label(roles: list[Any]) -> str | None:
    for role in roles:
        if not isinstance(role, dict):
            continue
        name = role.get("name")
        if isinstance(name, str) and name.strip():
            return name.strip()
        role_type = role.get("role_type")
        if isinstance(role_type, str) and role_type.strip():
            return role_type.strip().replace("_", " ").title()
    return None


def _capabilities_from_user_payload(me: dict[str, Any]) -> set[str]:
    raw = me.get("capabilities")
    if not isinstance(raw, list):
        return set()
    return {cap for cap in raw if isinstance(cap, str) and cap.strip()}


def _user_id_from_payload(me: dict[str, Any]) -> str | None:
    user_id = me.get("id")
    if isinstance(user_id, str) and user_id.strip():
        return user_id.strip()
    return None


def _identity_from_user_payload(
    me: dict[str, Any], *, host: str
) -> IdentityStatus | None:
    email = me.get("email")
    if not isinstance(email, str) or not email.strip():
        return None
    email = email.strip()
    full_name = me.get("full_name")
    display_name = (
        full_name.strip() if isinstance(full_name, str) and full_name.strip() else email
    )
    roles_raw = me.get("roles")
    roles: list[Any] = roles_raw if isinstance(roles_raw, list) else []
    capabilities = _capabilities_from_user_payload(me)
    return {
        "display_name": display_name,
        "email": email,
        "role": _primary_role_label(roles),
        "space": _space_label(email=email, host=host),
        "can_manage_user_mcp_access": _CAP_MANAGE_USER_MCP_ACCESS in capabilities,
    }


def _auth_headers(secret: str) -> dict[str, str]:
    return {
        "User-Agent": USER_AGENT,
        API_KEY_HEADER_NAME: secret,
    }


def _fetch_me(host: str, secret: str) -> dict[str, Any] | None:
    """Best-effort /users/me. Failures stay local-only status."""
    try:
        with http_client(
            headers=_auth_headers(secret),
            timeout=_ENRICH_TIMEOUT_SECONDS,
        ) as client:
            response = client.get(f"{host}/api/v1/users/me")
            response.raise_for_status()
            payload = response.json()
    except (httpx.HTTPError, ValueError, TypeError):
        return None
    if not isinstance(payload, dict):
        return None
    return payload


def _get_json(
    host: str,
    secret: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
) -> Any | None:
    """One-shot GET. Soft-fail for tray enrich."""
    try:
        with http_client(
            headers=_auth_headers(secret),
            timeout=_ENRICH_TIMEOUT_SECONDS,
        ) as client:
            response = client.get(f"{host}{path}", params=params)
            response.raise_for_status()
            return response.json()
    except (httpx.HTTPError, ValueError, TypeError, OSError):
        return None


def _account_needs_reconnect(account: dict[str, Any]) -> bool:
    """Mirror webapp ``needsReconnect``: only explicit unhealthy sessions."""
    healthy = account.get("session_healthy")
    if healthy is None:
        return False
    return healthy is False


def _attention_account_from_row(account: dict[str, Any]) -> AttentionAccount | None:
    account_id = account.get("id")
    server_id = account.get("server_id")
    if not isinstance(account_id, str) or not account_id.strip():
        return None
    if not isinstance(server_id, str) or not server_id.strip():
        return None
    label_raw = account.get("label")
    server_name = account.get("server_name")
    if isinstance(label_raw, str) and label_raw.strip():
        label = label_raw.strip()
    elif isinstance(server_name, str) and server_name.strip():
        label = server_name.strip()
    else:
        label = "Connection"
    return {
        "account_id": account_id.strip(),
        "server_id": server_id.strip(),
        "label": label,
    }


def _accounts_needing_reconnect(payload: Any) -> list[AttentionAccount]:
    """``GET /api/v1/accounts`` returns a bare list of AccountPublic."""
    if not isinstance(payload, list):
        return []
    accounts: list[AttentionAccount] = []
    for row in payload:
        if not isinstance(row, dict) or not _account_needs_reconnect(row):
            continue
        parsed = _attention_account_from_row(row)
        if parsed is not None:
            accounts.append(parsed)
    return accounts


def _approval_request_from_row(row: dict[str, Any]) -> AttentionApprovalRequest | None:
    request_id = row.get("id")
    if not isinstance(request_id, str) or not request_id.strip():
        return None
    if row.get("status") != "pending":
        return None
    can_decide_inline = row.get("can_decide_inline")
    return {
        "id": request_id.strip(),
        "title": _approval_title(
            row.get("initial_content"),
            tool_call=row.get("tool_call"),
        ),
        "can_decide_inline": (
            can_decide_inline if isinstance(can_decide_inline, bool) else False
        ),
    }


def _approval_title(initial_content: Any, *, tool_call: Any = None) -> str:
    title = ""
    if isinstance(initial_content, dict):
        stored_title = initial_content.get("title")
        if isinstance(stored_title, str):
            title = stored_title.strip()

    if isinstance(tool_call, dict):
        server_name = tool_call.get("server_name")
        tool_name = tool_call.get("tool_name")
        if isinstance(server_name, str) and isinstance(tool_name, str):
            server_label = " ".join(server_name.split())
            tool_label = " ".join(tool_name.split())
            if server_label and tool_label:
                title = f"Approval needed: {server_label} -> {tool_label}"

    return title


def _approval_requests_pending(payload: Any) -> list[AttentionApprovalRequest]:
    """``GET /api/v1/approvals`` returns ``{data, count}`` for own pending rows."""
    if not isinstance(payload, dict):
        return []
    data = payload.get("data")
    if not isinstance(data, list):
        return []
    approvals: list[AttentionApprovalRequest] = []
    for row in data:
        if not isinstance(row, dict):
            continue
        parsed = _approval_request_from_row(row)
        if parsed is not None:
            approvals.append(parsed)
    return approvals


def _attention_status(
    *,
    accounts: list[AttentionAccount],
    approval_requests: list[AttentionApprovalRequest],
) -> AttentionStatus | None:
    if not accounts and not approval_requests:
        return None
    return {
        "accounts_needing_reconnect": len(accounts),
        "accounts": accounts,
        "approval_requests_pending": len(approval_requests),
        "approval_requests": approval_requests,
    }


def _fetch_attention(host: str, secret: str) -> AttentionStatus | None:
    """Best-effort work blockers. Soft-fail each source independently."""
    accounts_payload = _get_json(host, secret, "/api/v1/accounts")
    approvals_payload = _get_json(host, secret, "/api/v1/approvals")
    return _attention_status(
        accounts=_accounts_needing_reconnect(accounts_payload),
        approval_requests=_approval_requests_pending(approvals_payload),
    )


def _admin_session_from_row(row: dict[str, Any]) -> AdminSession | None:
    # SessionSummary uses session_id (not id).
    session_id = row.get("session_id")
    if not isinstance(session_id, str) or not session_id.strip():
        return None
    title_raw = row.get("title")
    if isinstance(title_raw, str) and title_raw.strip():
        title = title_raw.strip()
    else:
        title = "Untitled session"
    client_raw = row.get("client")
    client = (
        client_raw.strip()
        if isinstance(client_raw, str) and client_raw.strip()
        else "unknown"
    )
    started = row.get("started_at")
    started_at = started.strip() if isinstance(started, str) and started.strip() else ""
    return {
        "id": session_id.strip(),
        "title": title,
        "client": client,
        "started_at": started_at,
    }


def _parse_admin_sessions(payload: Any) -> list[AdminSession]:
    # SessionListResponse uses ``data`` (list[SessionSummary]).
    rows: Any
    if isinstance(payload, dict):
        rows = payload.get("data")
    elif isinstance(payload, list):
        rows = payload
    else:
        return []
    if not isinstance(rows, list):
        return []
    sessions: list[AdminSession] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        parsed = _admin_session_from_row(row)
        if parsed is not None:
            sessions.append(parsed)
        if len(sessions) >= _ADMIN_SESSION_LIMIT:
            break
    return sessions


def _admin_access_request_from_item(item: dict[str, Any]) -> AdminAccessRequest | None:
    # /admin/requests is a mixed queue; only access rows belong in the tray.
    if item.get("type") != "access":
        return None
    data = item.get("data")
    if not isinstance(data, dict):
        return None
    request_id = data.get("id")
    if not isinstance(request_id, str) or not request_id.strip():
        return None
    name = data.get("requested_by_name")
    email = data.get("requested_by_email")
    if isinstance(name, str) and name.strip():
        requester = name.strip()
    elif isinstance(email, str) and email.strip():
        requester = email.strip()
    else:
        requester = "Someone"
    server = item.get("server")
    resource = "connector"
    if isinstance(server, dict):
        server_name = server.get("name")
        if isinstance(server_name, str) and server_name.strip():
            resource = server_name.strip()
    return {
        "id": request_id.strip(),
        "requester": requester,
        "resource": resource,
        "summary": f"{requester} requested {resource}",
    }


def _parse_admin_access_requests(payload: Any) -> list[AdminAccessRequest]:
    if not isinstance(payload, dict):
        return []
    rows = payload.get("data")
    if not isinstance(rows, list):
        return []
    requests: list[AdminAccessRequest] = []
    for item in rows:
        if not isinstance(item, dict):
            continue
        parsed = _admin_access_request_from_item(item)
        if parsed is not None:
            requests.append(parsed)
        if len(requests) >= _ADMIN_REQUEST_LIMIT:
            break
    return requests


def _fetch_admin(host: str, secret: str, *, actor_id: str | None) -> AdminStatus | None:
    """Sessions + pending access requests. Soft-fail → omit the admin block.

    ``actor_id`` scopes sessions to the signed-in user: callers holding
    ``view_org_audit_logs`` get the whole org's sessions from an unscoped list,
    which the tray's "Recent sessions" must never show. Without a resolved
    actor the sessions call is skipped rather than sent unscoped; the requests
    surface stands on its own.
    """
    with ThreadPoolExecutor(max_workers=2) as pool:
        sessions_future = (
            pool.submit(
                _get_json,
                host,
                secret,
                "/api/v1/sessions/",
                params={"limit": _ADMIN_SESSION_LIMIT, "actor_id": actor_id},
            )
            if actor_id
            else None
        )
        requests_future = pool.submit(
            _get_json,
            host,
            secret,
            "/api/v1/admin/requests",
            params={
                "status": "pending",
                "request_type": "access",
                "limit": _ADMIN_REQUEST_LIMIT,
            },
        )
        sessions_payload = (
            sessions_future.result() if sessions_future is not None else None
        )
        requests_payload = requests_future.result()

    # Only drop the whole block when neither endpoint answered (usually 403
    # without the capability); one soft-fail still leaves the other surface.
    if sessions_payload is None and requests_payload is None:
        return None
    return {
        "sessions": _parse_admin_sessions(sessions_payload),
        "access_requests": _parse_admin_access_requests(requests_payload),
    }


def _resolve_network_enrichment(
    *,
    default_host: str | None,
    hosts: list[HostStatus],
    secret_for_host: str | None,
) -> tuple[IdentityStatus | None, AttentionStatus | None, AdminStatus | None]:
    if not default_host or secret_for_host is None:
        return None, None, None
    default_ok = any(
        host["url"] == default_host and host["credential"] == "ok" for host in hosts
    )
    if not default_ok:
        return None, None, None

    # Independent GETs — overlap to keep tray poll latency near one timeout.
    with ThreadPoolExecutor(max_workers=2) as pool:
        me_future = pool.submit(_fetch_me, default_host, secret_for_host)
        attention_future = pool.submit(_fetch_attention, default_host, secret_for_host)
        me = me_future.result()
        attention = attention_future.result()

    identity = (
        _identity_from_user_payload(me, host=default_host) if me is not None else None
    )
    # The admin block is admin-only; skipping it keeps member polls at one round.
    admin: AdminStatus | None = None
    if identity is not None and identity["can_manage_user_mcp_access"]:
        admin = _fetch_admin(
            default_host,
            secret_for_host,
            actor_id=_user_id_from_payload(me) if me is not None else None,
        )
    return identity, attention, admin


def collect_status() -> StatusSnapshot:
    """Collect tray status; identity/attention/admin are best-effort enrich."""
    config = load_config()
    hosts: list[HostStatus] = []
    configured_urls = sorted(
        host_config["url"]
        for host_config in config.hosts.values()
        if host_config.get("url")
    )
    for url in configured_urls:
        hosts.append(
            {
                "url": url,
                "credential": (
                    "ok" if config.get_secret_for_host(url) is not None else "missing"
                ),
                "enrolled": enrollment_marker_path(url).exists(),
            }
        )

    expected_hook_command = resolve_runlayer_hook_command()
    hook_results = check_all(
        scope=InstallScope.USER,
        expected_hook_command=expected_hook_command,
        include_pipeline=False,
    )
    hooks: list[HookStatus] = [
        {
            "client": result.client.value,
            "status": result.status.value,
        }
        for result in hook_results
    ]

    default_host = config.default_host
    secret = (
        config.get_secret_for_host(default_host) if default_host is not None else None
    )
    identity, attention, admin = _resolve_network_enrichment(
        default_host=default_host,
        hosts=hosts,
        secret_for_host=secret,
    )

    return {
        "version": __version__,
        "default_host": default_host,
        "dashboard_url": default_host,
        "hosts": hosts,
        "hooks": hooks,
        "identity": identity,
        "attention": attention,
        "admin": admin,
    }


def _print_human(snapshot: StatusSnapshot) -> None:
    typer.echo(f"Runlayer CLI {snapshot['version']}")
    dashboard_url = snapshot["dashboard_url"]
    typer.echo(f"Dashboard: {dashboard_url or 'Not configured'}")

    identity = snapshot["identity"]
    if identity is not None:
        typer.echo("\nSigned in as:")
        typer.echo(f"  {identity['display_name']} <{identity['email']}>")
        details = " · ".join(
            part for part in (identity.get("role"), identity.get("space")) if part
        )
        if details:
            typer.echo(f"  {details}")

    attention = snapshot.get("attention")
    if attention is not None:
        accounts = attention.get("accounts") or []
        approvals_pending = attention.get("approval_requests_pending") or 0
        request_word = "request" if approvals_pending == 1 else "requests"
        approvals_line = f"{approvals_pending} approval {request_word}"
        if accounts:
            typer.echo("\nNeeds attention:")
            for account in accounts:
                typer.echo(f"  Reconnect {account['label']}")
            if approvals_pending:
                typer.echo(f"  Review {approvals_line}")
        elif approvals_pending:
            typer.echo(f"\nNeeds attention: {approvals_line}")
        else:
            needing = attention.get("accounts_needing_reconnect") or 0
            if needing:
                typer.echo(f"\nNeeds attention: {needing} connection(s) need reconnect")

    admin = snapshot.get("admin")
    if admin is not None:
        requests = admin.get("access_requests") or []
        if requests:
            typer.echo("\nRequests:")
            for request in requests:
                typer.echo(f"  {request['summary']}")
        sessions = admin.get("sessions") or []
        if sessions:
            typer.echo("\nRecent sessions:")
            for session in sessions:
                typer.echo(f"  {session['title']}")

    typer.echo("\nHosts:")
    if not snapshot["hosts"]:
        typer.echo("  No configured hosts")
    for host in snapshot["hosts"]:
        auth = "Authenticated" if host["credential"] == "ok" else "Not authenticated"
        enrollment = ", enrolled" if host["enrolled"] else ""
        typer.echo(f"  {host['url']}: {auth}{enrollment}")

    typer.echo("\nHooks:")
    if not snapshot["hooks"]:
        typer.echo("  No supported clients detected")
    for hook in snapshot["hooks"]:
        client = hook["client"].replace("_", " ").replace("-", " ").title()
        typer.echo(f"  {client}: {hook['status']}")


def status(
    json_output: bool = typer.Option(False, "--json", help="Output status as JSON"),
) -> None:
    """Show local authentication, hook, and packaged CLI status."""
    snapshot = collect_status()
    if json_output:
        typer.echo(json.dumps(snapshot, indent=2))
    else:
        _print_human(snapshot)
