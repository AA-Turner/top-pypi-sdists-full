"""probe context list/show/use/delete: named local contexts, credentials redacted."""

from __future__ import annotations
import sys

import typer
from ....sdk.settings.settings import (
    DEFAULT_BASE_URL,
    current_context_name,
    delete_context,
    load_context,
    load_file,
    resolve,
    use_context)
from ....sdk import session_marker


# -- context ----------------------------------------------------------------
context_app = typer.Typer(
    no_args_is_help=True, help="named local contexts: endpoint + credentials + anchors"
)


def _redact(value: str | None) -> str:
    """Enough of a token to recognize, never enough to use.

    Shows the TAIL, not the head: the head is a shared prefix (`probe_pat_`,
    `ros_pat_`) that identifies nothing, so leading characters spend secret entropy
    to say what every token already says. `context list` output ends up in bug
    reports and CI logs, so this matches `_fingerprint`'s last-4 convention rather
    than inventing a second, weaker redaction rule.
    """
    if not value:
        return "-"
    return f"…{value[-4:]}" if len(value) > 8 else "set"


def _context_row(name: str, ctx: dict, *, active: bool) -> dict:
    anchor = ctx.get("workspace") if isinstance(ctx.get("workspace"), dict) else {}
    return {
        "name": name,
        "active": active,
        "base_url": ctx.get("base_url") or DEFAULT_BASE_URL,
        "token": _redact(ctx.get("token")),
        "mcp_token": _redact(ctx.get("mcp_token")),
        "workspace": anchor.get("id"),
        "project": anchor.get("project"),
    }


@context_app.command("list")
def context_list() -> None:
    """List local contexts. Credentials are shown redacted."""
    data = load_file()
    contexts = data.get("contexts") or {}
    if not contexts:
        print(f"no contexts yet — sign in ({session_marker.WIZARD_HINT})")
        return
    active = current_context_name(data)
    _print_json([_context_row(n, c or {}, active=n == active) for n, c in sorted(contexts.items())])


@context_app.command("show")
def context_show(
    name: str = typer.Argument(None, help="defaults to the active context"),
) -> None:
    """Show one context as it will actually resolve, env overrides included."""
    target = name or current_context_name()
    ctx = load_context(target)
    if not ctx and target not in (load_file().get("contexts") or {}):
        print(f"no such context: {target}", file=sys.stderr)
        raise typer.Exit(1)
    row = _context_row(target, ctx, active=target == current_context_name())
    # Show the resolved view too: an env var silently outranking the file is exactly
    # the confusion this command exists to end.
    settings = resolve(context=target)
    row["resolved"] = {
        "base_url": settings.base_url,
        "workspace": settings.workspace,
        "project": settings.project,
        "workspace_limit": None if settings.workspace_limit is None else settings.workspace_limit.as_json(),
    }
    _print_json(row)


@context_app.command("use")
def context_use(name: str = typer.Argument(..., help="context to make active")) -> None:
    """Switch the active context, creating it empty if it is new."""
    path = use_context(name)
    print(f"active context: {name} ({path})")
    _hold_daemon_key()


@context_app.command("delete")
def context_delete(name: str = typer.Argument(..., help="context to remove")) -> None:
    """Delete a context and its stored credentials."""
    if name not in (load_file().get("contexts") or {}):
        print(f"no such context: {name}", file=sys.stderr)
        raise typer.Exit(1)
    active = current_context_name()
    delete_context(name)
    print(f"deleted context {name} (active: {current_context_name()})")
    if current_context_name() != active:
        _hold_daemon_key()  # the active context went: another one's sign-in is in use now
from probe.cli.commands.account.account import _hold_daemon_key  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
