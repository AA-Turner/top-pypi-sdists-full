"""``plato workflow`` — submit and monitor Chronos workflows.

Talks to the workflow submission service running on a workflow world VM. Endpoint
and token resolve from ``--url``/``--token`` flags, then ``$WORKFLOW_SERVICE_URL``
/ ``$WORKFLOW_SERVICE_TOKEN``, then the ``.workflow-endpoint.json`` file on the
results mount. Designed to run on orchestrator agent VMs where the ``plato``
console script is already on PATH.
"""

import json
import sys
import time
from pathlib import Path
from typing import Any

import typer

from plato.cli.utils import console
from plato.utils.workflow_client import WorkflowServiceClient, WorkflowServiceError, resolve_endpoint

workflow_app = typer.Typer(help="Submit and monitor Chronos workflows")

_TERMINAL = frozenset({"complete", "error", "cancelled"})


def _client(url: str | None, token: str | None) -> WorkflowServiceClient:
    try:
        base_url, resolved_token = resolve_endpoint(url, token)
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc
    return WorkflowServiceClient(base_url, resolved_token)


def _load_args(args: str | None, args_file: str | None) -> Any:
    """Parse workflow args from an inline JSON string or a JSON file."""
    if args is not None and args_file is not None:
        console.print("[red]Pass only one of --args / --args-file[/red]")
        raise typer.Exit(1)
    raw: str | None = None
    if args_file is not None:
        raw = Path(args_file).read_text()
    elif args is not None:
        raw = args
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        console.print(f"[red]--args is not valid JSON: {exc}[/red]")
        raise typer.Exit(1) from exc


def _read_script(script_arg: str) -> str:
    """Read the workflow script from a file path, or from stdin when '-'."""
    if script_arg == "-":
        return sys.stdin.read()
    path = Path(script_arg)
    if not path.exists():
        console.print(f"[red]Script file not found: {script_arg}[/red]")
        raise typer.Exit(1)
    return path.read_text()


def _render_event(record: dict[str, Any]) -> str:
    """Render one journal record as a concise narrator line."""
    rec_type = record.get("type")
    seq = record.get("seq")
    if rec_type == "workflow_started":
        return f"[{seq}] workflow started"
    if rec_type == "phase":
        return f"[{seq}] phase: {record.get('phase')}"
    if rec_type == "call_started":
        return f"[{seq}] -> call {record.get('call_id')} started"
    if rec_type == "call_result":
        status = record.get("status")
        cost = record.get("cost_usd")
        cost_str = f" (${cost:.4f})" if isinstance(cost, (int, float)) else ""
        cached = " [cached]" if record.get("cached_from") else ""
        merged_sha = record.get("merged_sha")
        merged_str = f" [merged to main: {merged_sha}]" if merged_sha else ""
        salvage = record.get("salvage_ref")
        salvage_str = f" [salvaged: {salvage}]" if salvage else ""
        published_str = ""
        error_str = ""
        if status != "ok":
            # A failed call's published ref means its git work survived even
            # though the call soft-failed to None — surface it, or it is only
            # discoverable by ls-remote.
            published = record.get("published_ref")
            published_str = f" [published: {published}]" if published else ""
            error = record.get("error")
            error_str = f" — {error}" if error else ""
        return (
            f"[{seq}] call {record.get('call_id')} {status}{cost_str}{cached}"
            f"{merged_str}{published_str}{salvage_str}{error_str}"
        )
    if rec_type == "workflow_result":
        return f"[{seq}] workflow finished"
    return f"[{seq}] {rec_type}"


def _watch(client: WorkflowServiceClient, workflow_id: str, poll_interval: float) -> str:
    """Poll events + status until terminal, printing narrator lines. Returns final status."""
    after_seq = -1
    while True:
        try:
            events_resp = client.events(workflow_id, after_seq)
            for record in events_resp.get("events", []):
                console.print(f"[dim]{_render_event(record)}[/dim]")
            after_seq = events_resp.get("next_seq", after_seq)
            status_resp = client.status(workflow_id)
        except WorkflowServiceError as exc:
            console.print(f"[red]{exc}[/red]")
            raise typer.Exit(1) from exc
        status = status_resp.get("status", "unknown")
        if status in _TERMINAL:
            return status
        time.sleep(poll_interval)


@workflow_app.command()
def submit(
    script: str = typer.Argument(..., help="Path to the workflow script (.py), or '-' for stdin."),
    args: str = typer.Option(None, "--args", help="Workflow args as an inline JSON value."),
    args_file: str = typer.Option(None, "--args-file", help="Path to a JSON file with the workflow args."),
    name: str = typer.Option(None, "--name", help="Optional human-readable workflow name."),
    budget_usd: float = typer.Option(None, "--budget", help="USD budget ceiling for the workflow."),
    workflow_id: str = typer.Option(None, "--workflow-id", help="Explicit workflow id (default: content hash)."),
    url: str = typer.Option(None, "--url", help="Workflow service base URL."),
    token: str = typer.Option(None, "--token", help="Workflow service bearer token."),
    watch: bool = typer.Option(False, "--watch", help="Stream narrator lines until the workflow finishes."),
    poll_interval: float = typer.Option(2.0, "--poll-interval", help="Seconds between polls when watching."),
) -> None:
    """Submit a workflow script for execution."""
    script_source = _read_script(script)
    parsed_args = _load_args(args, args_file)
    client = _client(url, token)
    try:
        resp = client.submit(
            script_source,
            args=parsed_args,
            name=name,
            budget_usd=budget_usd,
            workflow_id=workflow_id,
        )
    except WorkflowServiceError as exc:
        if exc.status_code == 422 and isinstance(exc.payload, dict):
            console.print("[red]Workflow script failed to compile:[/red]")
            console.print(f"  [red]{exc.payload.get('error')}[/red]")
            if exc.payload.get("lineno") is not None:
                console.print(f"  [yellow]line {exc.payload['lineno']}[/yellow]")
            if exc.payload.get("excerpt"):
                console.print(f"  [dim]{exc.payload['excerpt']}[/dim]")
        else:
            console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc

    wf_id = resp.get("workflow_id")
    console.print(f"[green]submitted[/green] workflow_id=[bold]{wf_id}[/bold] status={resp.get('status')}")
    for warning in resp.get("lint_warnings", []) or []:
        console.print(f"[yellow]lint: {warning}[/yellow]")

    if watch and wf_id:
        final_status = _watch(client, wf_id, poll_interval)
        _print_final(client, wf_id, final_status)
        if final_status != "complete":
            raise typer.Exit(1)


@workflow_app.command()
def status(
    workflow_id: str = typer.Argument(..., help="Workflow id."),
    url: str = typer.Option(None, "--url", help="Workflow service base URL."),
    token: str = typer.Option(None, "--token", help="Workflow service bearer token."),
) -> None:
    """Show a workflow's status, phase, stats, and spend."""
    client = _client(url, token)
    try:
        resp = client.status(workflow_id)
    except WorkflowServiceError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc
    console.print_json(data=resp)


@workflow_app.command()
def result(
    workflow_id: str = typer.Argument(..., help="Workflow id."),
    url: str = typer.Option(None, "--url", help="Workflow service base URL."),
    token: str = typer.Option(None, "--token", help="Workflow service bearer token."),
    watch: bool = typer.Option(False, "--watch", help="Wait for completion, streaming narrator lines."),
    poll_interval: float = typer.Option(2.0, "--poll-interval", help="Seconds between polls when watching."),
) -> None:
    """Fetch a workflow's result (202 while still running unless --watch)."""
    client = _client(url, token)
    if watch:
        final_status = _watch(client, workflow_id, poll_interval)
        _print_final(client, workflow_id, final_status)
        if final_status != "complete":
            raise typer.Exit(1)
        return
    try:
        resp = client.result(workflow_id)
    except WorkflowServiceError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc
    if resp.get("status") in ("queued", "running"):
        console.print(f"[yellow]workflow still {resp.get('status')}[/yellow]")
        raise typer.Exit(2)
    console.print_json(data=resp)


@workflow_app.command()
def logs(
    workflow_id: str = typer.Argument(..., help="Workflow id."),
    after_seq: int = typer.Option(-1, "--after-seq", help="Only show events after this seq (-1 = from start)."),
    follow: bool = typer.Option(False, "--follow", "-f", help="Keep polling for new events until terminal."),
    url: str = typer.Option(None, "--url", help="Workflow service base URL."),
    token: str = typer.Option(None, "--token", help="Workflow service bearer token."),
    poll_interval: float = typer.Option(2.0, "--poll-interval", help="Seconds between polls when following."),
) -> None:
    """Print a workflow's journal event stream as narrator lines."""
    client = _client(url, token)
    try:
        if not follow:
            resp = client.events(workflow_id, after_seq)
            for record in resp.get("events", []):
                console.print(_render_event(record))
            return
        seq = after_seq
        while True:
            resp = client.events(workflow_id, seq)
            for record in resp.get("events", []):
                console.print(_render_event(record))
            seq = resp.get("next_seq", seq)
            if client.status(workflow_id).get("status") in _TERMINAL:
                break
            time.sleep(poll_interval)
    except WorkflowServiceError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc


@workflow_app.command()
def cancel(
    workflow_id: str = typer.Argument(..., help="Workflow id."),
    url: str = typer.Option(None, "--url", help="Workflow service base URL."),
    token: str = typer.Option(None, "--token", help="Workflow service bearer token."),
) -> None:
    """Request cancellation of a workflow."""
    client = _client(url, token)
    try:
        resp = client.cancel(workflow_id)
    except WorkflowServiceError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc
    console.print(f"[yellow]cancel requested[/yellow] status={resp.get('status')}")


def _print_final(client: WorkflowServiceClient, workflow_id: str, final_status: str) -> None:
    """Print the terminal outcome and (on success) the result payload."""
    color = "green" if final_status == "complete" else "red"
    console.print(f"[{color}]workflow {final_status}[/{color}]")
    try:
        resp = client.result(workflow_id)
    except WorkflowServiceError as exc:
        console.print(f"[red]{exc}[/red]")
        return
    console.print_json(data=resp)
