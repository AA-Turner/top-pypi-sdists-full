"""Sandbox inspection subcommands for the cyclopts CLI."""

import typing as t

import cyclopts

from dreadnode.app.cli.args import PlatformScopeArgs
from dreadnode.app.cli.shared import (
    _FLAG_STATE,
    _SANDBOX_LIST_ROW_FIELDS,
    _render,
    _render_list,
    _summarize_sandbox,
    confirm_destructive,
    console,
    print_success,
)

cli = cyclopts.App(name="sandbox", help="Inspect platform sandboxes.")


def _summarize_usage(payload: dict[str, t.Any]) -> str:
    total_runtime_seconds = payload.get("total_runtime_seconds", 0)
    sessions_count = payload.get("sessions_count", 0)
    current_month_seconds = payload.get("current_month_seconds", 0)
    return (
        f"[cyan]{sessions_count}[/cyan] sessions "
        f"[dim]total={total_runtime_seconds}s month={current_month_seconds}s[/dim]"
    )


@cli.command(name="list")
def list_(
    *,
    state: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(
            name=_FLAG_STATE,
            help="Filter by sandbox state (repeatable: running, paused, killed)",
            negative_iterable=(),
        ),
    ] = None,
    limit: t.Annotated[int, cyclopts.Parameter(help="Maximum sandboxes to return")] = 50,
    cursor: t.Annotated[
        str | None, cyclopts.Parameter(help="Pagination cursor from a previous list response")
    ] = None,
    project_id: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Optional explicit project UUID to filter sandboxes"),
    ] = None,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """List sandboxes for the active organization."""
    api, profile = platform.connect()
    payload = api.list_sandboxes(
        profile.org_key,
        state=state,
        project_id=project_id,
        limit=limit,
        cursor=cursor,
    )
    _render_list(
        payload,
        as_json=as_json,
        summary=_summarize_sandbox,
        empty_msg="No sandboxes found",
        fields=_SANDBOX_LIST_ROW_FIELDS,
    )


@cli.command()
def get(
    sandbox_id: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Get sandbox details by provider sandbox ID."""
    api, profile = platform.connect()
    payload = api.get_sandbox(profile.org_key, sandbox_id)
    _render(payload, as_json=as_json, summary=_summarize_sandbox)


@cli.command()
def logs(
    sandbox_id: str,
    *,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Get sandbox server logs by provider sandbox ID."""
    api, profile = platform.connect()
    logs_payload = api.get_sandbox_logs(profile.org_key, sandbox_id)
    if logs_payload:
        console.print(logs_payload, end="")
        if not logs_payload.endswith("\n"):
            console.print()
        return
    console.print("[dim]No sandbox logs found[/dim]")


@cli.command()
def usage(
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Get aggregate sandbox usage for the active organization."""
    api, profile = platform.connect()
    payload = api.get_sandbox_usage(profile.org_key)
    _render(payload, as_json=as_json, summary=_summarize_usage)


@cli.command(alias="rm")
def delete(
    sandbox_id: str,
    *,
    yes: t.Annotated[bool, cyclopts.Parameter(name="--yes", alias="-y", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Delete (kill) a sandbox by provider sandbox ID."""
    api, profile = platform.connect()
    api.get_sandbox(profile.org_key, sandbox_id)

    if not confirm_destructive(f"Delete sandbox [dim]{sandbox_id}[/dim]?", yes=yes):
        console.print("[dim]Cancelled[/dim]")
        return

    api.delete_sandbox(profile.org_key, sandbox_id)
    print_success(f"Deleted sandbox [dim]{sandbox_id}[/dim]")
