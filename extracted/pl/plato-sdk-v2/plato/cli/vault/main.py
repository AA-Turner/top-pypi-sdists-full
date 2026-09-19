"""Plato vault CLI - read the login inventory and bake snapshots via the login console."""

from __future__ import annotations

import json
from contextlib import contextmanager
from typing import Annotated, Any

import typer
from rich.markup import escape
from rich.table import Table

from plato.cli.chronos.settings import get_settings
from plato.cli.utils import console
from plato.cli.vault.client import (
    ENV_VAR,
    MODES,
    NotFound,
    VaultConsoleClient,
    VaultConsoleError,
    quote_segment,
    resolve_base_url,
    translate_mode,
)

vault_app = typer.Typer(help="Login vault: inventory, snapshot health, and bakes over the login console.")

ConsoleUrlArg = Annotated[
    str | None,
    typer.Option("--console-url", help=f"Login console base URL (default: ${ENV_VAR})"),
]
JsonArg = Annotated[bool, typer.Option("--json", "-j", help="Output as JSON")]
AccountArg = Annotated[str, typer.Option("--account", "-a", help="Account under the login_key")]

# Only these fields are ever rendered. The console record also carries
# credential-shaped values (a reveal route feeds the same page), so an allowlist
# means no code path here can print one by accident. Presence flags only.
_DETAIL_FIELDS = (
    "login_key",
    "account",
    "email",
    "method",
    "method_kinds",
    "migrated",
    "archived",
    "live",
    "bakeable",
    "browser_mode",
    "bake_session_id",
    "default_for",
    "login_url",
    "op_item_url",
)
_SNAPSHOT_FIELDS = (
    "status",
    "age_days",
    "created_at",
    "ref",
    "kind",
    "mode",
    "proxy_exit",
    "context_id",
    "via_vm",
)
_PROXY_FIELDS = ("name", "note", "error", "label")
# The vault's own field names (op_client._FIELDS) - what `cred_presence` is keyed
# by. Always these four keys, so a driver can read `creds["password"]` whatever
# the console had in hand; the flat has_* flags are all it sends when 1Password
# is unconfigured or hiccups (build_detail emits `cred_presence` as `{}` there).
_CRED_FIELDS = ("username", "password", "totp", "phone")
_CRED_FLAT = {"username": "has_user", "password": "has_pass", "totp": "has_totp"}
# `bakeable` and `browser_mode` are computed by build_detail only - the list
# route has no equivalent, so reading them here rendered "no" for every
# account. They are a `get` fact. `proxy` is the exit the run resolves.
_ACCOUNT_FIELDS = ("account", "migrated", "archived", "live", "proxy")


def _pick(record: Any, fields: tuple[str, ...]) -> dict:
    """The allowlisted subset of a console record."""
    if not isinstance(record, dict):
        return {}
    return {k: record.get(k) for k in fields}


def _creds(detail: dict) -> dict[str, bool]:
    """Credential PRESENCE only, coerced to booleans so no value can leak."""
    presence = detail.get("cred_presence")
    if isinstance(presence, dict) and presence:
        return {k: bool(presence.get(k)) for k in _CRED_FIELDS}
    return {k: bool(detail.get(_CRED_FLAT[k])) if k in _CRED_FLAT else False for k in _CRED_FIELDS}


def _detail_view(detail: dict) -> dict:
    """The safe projection of ``build_detail`` that every command prints."""
    view = _pick(detail, _DETAIL_FIELDS)
    view["creds"] = _creds(detail)
    view["snapshot"] = _pick(detail.get("snapshot"), _SNAPSHOT_FIELDS)
    view["proxy"] = _pick(detail.get("proxy"), _PROXY_FIELDS)
    lineage = detail.get("lineage")
    view["lineage_count"] = len(lineage) if isinstance(lineage, list) else 0
    return view


def _same_key(group: Any, login_key: str) -> bool:
    """Match a group's login_key. The console lowercases keys, the operator may not."""
    return str((group or {}).get("login_key") or "").lower() == login_key.lower()


def _print_json(payload: Any) -> None:
    """One JSON object on stdout - use print() so Rich adds no ANSI codes."""
    print(json.dumps(payload, indent=2, default=str))


def _field(key: str, value: Any) -> None:
    """One `  key: value` line. The value is console text (a proxy note, an
    exception string), so it is escaped - rich markup would eat `[agent]` and a
    stray closing tag would raise MarkupError mid-render."""
    console.print(f"  [cyan]{key}:[/cyan] {escape(str(value))}")


def _fail(error: VaultConsoleError, json_output: bool) -> None:
    if json_output:
        _print_json({"error": str(error)})
    else:
        console.print(f"[red]{escape(str(error))}[/red]")
    raise typer.Exit(error.exit_code)


@contextmanager
def _console_client(console_url: str | None, json_output: bool):
    """Open the console client, mapping typed errors to driver exit codes."""
    try:
        with VaultConsoleClient(resolve_base_url(console_url)) as client:
            yield client
    except VaultConsoleError as e:
        _fail(e, json_output)


def _session_url(session_id: str) -> str:
    return f"{get_settings().chronos_url}/sessions/{session_id}"


def _print_abort(session_id: str) -> None:
    console.print(
        f"to abort: plato chronos stop {escape(session_id)}  "
        "[dim](loses the snapshot - it commits only at the end of the run)[/dim]"
    )


def _print_watch(live: dict, session_id: str) -> None:
    """Watch links for an in-flight bake: noVNC for a VM bake, the session otherwise."""
    novnc = live.get("novnc") or []
    for entry in novnc:
        if isinstance(entry, dict) and entry.get("url"):
            # markup=False: the aliases are `agent`/`browser`, so rich would read
            # `[agent]` as a style tag and print the links unlabelled.
            console.print(f"  noVNC [{entry.get('alias')}]: {entry['url']}", markup=False)
    if not novnc:
        console.print(f"  session: {_session_url(session_id)}")
        if live.get("trajectory_only"):
            console.print("  [dim]no VM browser for this mode - watch the trajectory[/dim]")


@vault_app.command("list")
def list_logins(
    login_key: Annotated[str | None, typer.Option("--login-key", help="Only this login_key")] = None,
    include_archived: Annotated[bool, typer.Option("--include-archived", help="Include archived accounts")] = False,
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """List the login inventory: which accounts exist and how healthy their snapshots are."""
    with _console_client(console_url, json_output) as client:
        inventory = client.list_logins(include_archived=include_archived)

    groups = [g for g in inventory.get("groups", []) if not login_key or _same_key(g, login_key)]
    rows = [
        {
            "login_key": g.get("login_key"),
            **_pick(account, _ACCOUNT_FIELDS),
            "snapshot": _pick(account.get("snapshot"), _SNAPSHOT_FIELDS),
        }
        for g in groups
        for account in g.get("accounts", [])
    ]

    if json_output:
        _print_json({"logins": rows, "counts": inventory.get("counts", {})})
        return

    table = Table(title="Logins")
    for column in ("login_key", "account", "snapshot", "age (d)", "mode", "exit"):
        table.add_column(column)
    for row in rows:
        snapshot = row["snapshot"]
        # Every cell is console text: escaped, or rich would read a `[...]` in a
        # key, account or exit name as a style tag.
        table.add_row(
            *(
                escape(str(cell))
                for cell in (
                    row["login_key"],
                    row["account"],
                    snapshot.get("status") or "none",
                    snapshot.get("age_days") if snapshot.get("age_days") is not None else "-",
                    snapshot.get("mode") or "-",
                    # The BOUND exit, not `snapshot.proxy_exit` (the exit the last
                    # bake left from). Absent renders "-", never "direct": the list
                    # route cannot tell a direct account from an unreadable vault.
                    row.get("proxy") or "-",
                )
            )
        )
    console.print(table)


@vault_app.command()
def get(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. google")],
    account: Annotated[str | None, typer.Option("--account", "-a", help="Account; omit to list accounts")] = None,
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """Show one login record: snapshot health, bound exit, credential presence. Never values."""
    if account is None:
        with _console_client(console_url, json_output) as client:
            inventory = client.list_logins()
        groups = [g for g in inventory.get("groups", []) if _same_key(g, login_key)]
        if not groups:
            # The `--account` form 404s; an unknown key must not read as "exists,
            # no accounts" just because this form asks the list route instead.
            _fail(NotFound(f"no such login_key: {login_key}"), json_output)
        accounts = [_pick(a, _ACCOUNT_FIELDS) for g in groups for a in g.get("accounts", [])]
        if json_output:
            _print_json({"login_key": login_key, "accounts": accounts})
            return
        console.print(
            f"[bold]{escape(login_key)}[/bold] accounts: "
            + (", ".join(escape(str(a["account"])) for a in accounts) or "-")
        )
        return

    with _console_client(console_url, json_output) as client:
        detail = client.get_login_detail(login_key, account)
    view = _detail_view(detail)

    if json_output:
        _print_json(view)
        return

    console.print(f"[bold]{escape(str(view['login_key']))}/{escape(str(view['account']))}[/bold]")
    for key, value in view.items():
        if key in ("login_key", "account"):
            continue
        _field(key, value)


@vault_app.command()
def bake(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. slack")],
    account: AccountArg,
    mode: Annotated[
        str | None,
        typer.Option("--mode", help=f"One of {', '.join(MODES)}; omit to use the saved mode"),
    ] = None,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Print the request and exit; launches nothing")] = False,
    yes: Annotated[bool, typer.Option("--yes", help="Required to actually launch")] = False,
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """Bake this account's snapshot. Launches a REAL session: it signs into the live
    account and costs money, so --yes is required - that confirmation is the only
    human rail. The console owns the rest (exit bans, the single-bake lock).
    """
    if not dry_run and not yes:
        _fail(
            VaultConsoleError(
                "refusing to launch: `bake` signs into the live account and costs money. "
                "Re-run with --yes, or --dry-run to see the request."
            ),
            json_output,
        )

    with _console_client(console_url, json_output) as client:
        browser_mode = translate_mode(mode)

        if dry_run:
            # The detail read only feeds this display, so a launch never depends
            # on a second route answering.
            detail = client.get_login_detail(login_key, account)
            request = {
                "method": "POST",
                # Quoted exactly as the client will send it, so the displayed
                # path is the one that would actually be hit.
                "path": f"/api/logins/{quote_segment(login_key)}/{quote_segment(account)}/bake",
                "browser_mode": browser_mode,
                "saved_browser_mode": detail.get("browser_mode"),
                "bakeable": detail.get("bakeable"),
                "proxy_exit": (detail.get("proxy") or {}).get("name"),
                "snapshot": _pick(detail.get("snapshot"), _SNAPSHOT_FIELDS),
            }
            if json_output:
                _print_json({"dry_run": True, "request": request})
            else:
                console.print("[yellow]dry run - nothing launched[/yellow]")
                for key, value in request.items():
                    _field(key, value)
                console.print("[dim]the console builds the launch payload; this CLI only asks it to[/dim]")
            return

        result = client.bake_login(login_key, account, browser_mode=browser_mode)
        session_id = str(result.get("session_id") or "")

        # The session is LIVE and billing from here. Print the id and the abort
        # line before anything that can fail: the watch links are decorative, but
        # losing the id leaves a paid session nobody can stop.
        if not json_output:
            console.print(f"[green]bake launched[/green] session {escape(session_id) or 'unknown'}")
            if session_id:
                _print_abort(session_id)

        live: dict = {}
        live_error: str | None = None
        if session_id:
            try:
                live = client.get_bake_live(login_key, account)
            except VaultConsoleError as e:
                live_error = str(e)

    if json_output:
        _print_json(
            {
                "session_id": session_id or None,
                "browser_mode": browser_mode,
                "live": live,
                "live_error": live_error,
            }
        )
        return

    if live_error:
        # A warning, never an exit code: the bake is running either way.
        console.print(f"[yellow]watch links unavailable:[/yellow] {escape(live_error)}")
    elif session_id:
        _print_watch(live, session_id)


@vault_app.command()
def status(
    login_key: Annotated[str, typer.Argument(help="Which auth system, e.g. slack")],
    account: AccountArg,
    console_url: ConsoleUrlArg = None,
    json_output: JsonArg = False,
):
    """Watch links for this account's in-flight bake, from the console's bake-live route."""
    with _console_client(console_url, json_output) as client:
        live = client.get_bake_live(login_key, account)

    if json_output:
        _print_json(live)
        return

    session_id = live.get("session_id")
    if not session_id:
        console.print(f"no bake in flight for {escape(login_key)}/{escape(account)}")
        return
    console.print(f"[bold]{escape(login_key)}/{escape(account)}[/bold] baking in session {escape(str(session_id))}")
    _print_watch(live, str(session_id))
    _print_abort(str(session_id))
