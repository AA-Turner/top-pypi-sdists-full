"""Workflow subcommands for the cyclopts CLI.

`dn workflow` operates on *authored* workflows — compiled graphs of typed events
and steps, pushed as part of a capability. Not to be confused with the ad-hoc
session grouping that `RuntimeClient.session_group()` creates.
"""

import json
import typing as t
import uuid

import cyclopts
from rich.table import Table

from dreadnode.app.cli.args import PlatformScopeArgs
from dreadnode.app.cli.shared import (
    _print_json,
    _short_id,
    confirm_destructive,
    console,
)

cli = cyclopts.App(
    name="workflow",
    help="Authored multi-step agent pipelines: definitions, runs, and approvals.",
)

_NODE_STATUS_STYLE = {
    "completed": "green",
    "running": "cyan",
    "ready": "cyan",
    "pending": "dim",
    "failed": "red",
    "cancelled": "red",
    "skipped": "yellow",
    "awaiting_approval": "magenta",
}
_RUN_STATUS_STYLE = {
    "completed": "green",
    "running": "cyan",
    "suspended": "magenta",
    "failed": "red",
    "cancelled": "red",
    "lost": "red",
    "pending": "dim",
}


def _styled(value: str, styles: dict[str, str]) -> str:
    return f"[{styles.get(value, 'white')}]{value}[/]"


def parse_inputs(pairs: list[str] | None) -> dict[str, t.Any]:
    """Parse ``--input k=v`` pairs, decoding JSON values where possible.

    ``max_steps=200`` becomes an int and ``tags=["a"]`` becomes a list, so typed
    workflow inputs do not all arrive as strings. A bare value that is not valid
    JSON stays a string, which is what makes ``github_url=https://...`` work.
    """
    parsed: dict[str, t.Any] = {}
    for pair in pairs or []:
        key, sep, raw = pair.partition("=")
        if not sep:
            raise ValueError(f"--input expects key=value, got {pair!r}")
        try:
            parsed[key] = json.loads(raw)
        except json.JSONDecodeError:
            parsed[key] = raw
    return parsed


# ---------------------------------------------------------------------------
# definitions
# ---------------------------------------------------------------------------


@cli.command(name="definitions", alias="defs")
def definitions(
    *,
    capability: str | None = None,
    name: str | None = None,
    agent: str | None = None,
    limit: int = 50,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """List compiled workflow definitions in your organization.

    Args:
        capability: Only workflows from this capability.
        name: Only workflows with this name.
        agent: Only workflows whose steps call this agent.
        limit: Maximum results to show.
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    rows = api.list_workflow_definitions(
        profile.org_key,
        profile.workspace_key,
        capability=capability,
        name=name,
        agent=agent,
        limit=limit,
    )
    if as_json:
        _print_json(rows)
        return
    if not rows:
        console.print("[dim]No workflow definitions found[/]")
        return

    table = Table(box=None, pad_edge=False)
    for column in ("ID", "CAPABILITY", "NAME", "NODES", "AGENTS", "GATE"):
        table.add_column(column)
    for row in rows:
        table.add_row(
            _short_id(str(row["id"])),
            f"{row['capability_name']}@{row['capability_version']}",
            row["name"],
            str(row["node_count"]),
            ", ".join(row.get("agent_names") or []) or "[dim]-[/]",
            "[magenta]yes[/]" if row.get("has_approval_gate") else "[dim]no[/]",
        )
    console.print(table)


@cli.command(name="get")
def get(
    definition_id: str,
    *,
    topology: t.Annotated[bool, cyclopts.Parameter(name="--topology", negative=())] = False,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Show a workflow definition.

    Args:
        definition_id: The definition to show.
        topology: Print the full compiled topology document.
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    definition = api.get_workflow_definition(profile.org_key, profile.workspace_key, definition_id)

    if as_json:
        _print_json(definition)
        return
    if topology:
        _print_json(definition.get("topology_json") or {})
        return

    graph = definition.get("topology_json") or {}
    console.print(f"[bold]{definition['name']}[/]  [dim]{definition['id']}[/]")
    console.print(
        f"  capability   {definition['capability_name']}@{definition['capability_version']}"
    )
    console.print(f"  content      [dim]{definition['topology_sha256'][:12]}[/]")
    console.print(f"  entry        {graph.get('entry', '?')}")
    console.print(f"  terminals    {', '.join(graph.get('terminals') or []) or '?'}")

    nodes = graph.get("nodes") or []
    if nodes:
        console.print()
        table = Table(box=None, pad_edge=False)
        for column in ("STEP", "KIND", "CONSUMES", "EMITS", "AGENTS"):
            table.add_column(column)
        for node in nodes:
            consumes = ", ".join((node.get("consumes") or {}).get("events") or [])
            if (node.get("consumes") or {}).get("collect"):
                consumes = f"Collect[{consumes}]"
            emits = ", ".join(
                f"{e['event']}{'[]' if e.get('cardinality') == 'many' else ''}"
                for e in node.get("emits") or []
            )
            agents = ", ".join(node.get("agents") or [])
            if node.get("agents_dynamic"):
                agents = f"{agents}, [dim]dynamic[/]" if agents else "[dim]dynamic[/]"
            table.add_row(node["key"], node["kind"], consumes, emits, agents or "[dim]-[/]")
        console.print(table)


# ---------------------------------------------------------------------------
# runs
# ---------------------------------------------------------------------------


@cli.command(name="run")
def run(
    definition_id: str,
    *,
    project_id: str,
    input: t.Annotated[list[str] | None, cyclopts.Parameter(name="--input", negative=())] = None,
    local: t.Annotated[bool, cyclopts.Parameter(name="--local", negative=())] = False,
    runtime_id: str | None = None,
    runtime_url: str | None = None,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Start a workflow run.

    Args:
        definition_id: The compiled definition to run.
        project_id: Project the run belongs to.
        input: Workflow input as key=value; repeatable. Values are JSON-decoded
            when possible, so `max_steps=200` is an int.
        local: Execute here, in this process, shipping facts to the platform as
            it goes. Without it the selected runtime executes the workflow.
        runtime_id: Runtime that owns remote execution. Required unless `--local`.
        runtime_url: Runtime to run agents against when using `--local`.
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    try:
        input_data = parse_inputs(input)
    except ValueError as exc:
        console.print(f"[red]{exc}[/]")
        raise SystemExit(2) from exc
    if local and runtime_id is not None:
        console.print("[red]--runtime-id cannot be combined with --local[/]")
        raise SystemExit(2)
    if not local and runtime_id is None:
        console.print("[red]--runtime-id is required unless --local is set[/]")
        raise SystemExit(2)

    definition = api.get_workflow_definition(profile.org_key, profile.workspace_key, definition_id)
    created = api.create_workflow_run(
        profile.org_key,
        profile.workspace_key,
        definition_id=definition_id,
        project_id=project_id,
        input_data=input_data,
        host_kind="local" if local else "runtime",
        runtime_id=runtime_id,
    )
    run_id = str(created["id"])

    if not local:
        if runtime_id is None:
            raise RuntimeError("runtime-hosted workflow is missing its runtime id")
        if as_json:
            _print_json(created)
            return
        console.print(
            f"Started run [cyan]{_short_id(run_id)}[/] on runtime "
            f"[cyan]{_short_id(runtime_id)}[/] [dim]({created['status']})[/]"
        )
        return

    execution_id = str(uuid.uuid4())
    api.claim_workflow_run(
        profile.org_key,
        profile.workspace_key,
        run_id,
        execution_id=execution_id,
    )
    result = _execute_locally(
        api=api,
        org=profile.org_key,
        workspace=profile.workspace_key,
        run_id=run_id,
        definition=definition,
        input_data=input_data,
        runtime_url=runtime_url,
        session_group_id=created.get("session_group_id"),
        execution_id=execution_id,
    )
    if as_json:
        _print_json({"run_id": run_id, "status": result.status, "result": result.result})
        return

    console.print()
    console.print(f"Run [cyan]{_short_id(run_id)}[/] {_styled(result.status, _RUN_STATUS_STYLE)}")
    if result.result is not None:
        console.print(f"[dim]result:[/] {result.result}")


def _execute_locally(
    *,
    api: t.Any,
    org: str,
    workspace: str,
    run_id: str,
    definition: dict[str, t.Any],
    input_data: dict[str, t.Any],
    runtime_url: str | None,
    execution_id: str,
    session_group_id: str | None = None,
) -> t.Any:
    """Run the workflow in this process, streaming progress and shipping facts.

    This is the Release 1 execution mode: the runtime host, in-process. A run
    started this way does not survive the process, which is why the CLI says so
    rather than implying otherwise.
    """
    import asyncio

    from dreadnode.app.client.runtime_client import RuntimeClient
    from dreadnode.workflows import PlatformFactSink, WorkflowHost
    from dreadnode.workflows.loader import load_workflow_for_definition

    workflow, topology = load_workflow_for_definition(definition)
    sink = PlatformFactSink(api, org, workspace, run_id, execution_id)
    client = RuntimeClient(runtime_url) if runtime_url else RuntimeClient()

    host = WorkflowHost(
        workflow,
        topology,
        client=client,
        sink=sink,
        capability=definition.get("capability_name"),
        run_id=str(run_id),
        session_group_id=str(session_group_id) if session_group_id else None,
    )

    console.print(
        f"[dim]Executing locally against {client.server_url} "
        f"\u2014 this run ends if you stop the process.[/]"
    )

    async def _drive() -> t.Any:
        progress = asyncio.create_task(_progress_loop(host))
        try:
            return await host.run(input_data)
        finally:
            progress.cancel()
            with __import__("contextlib").suppress(asyncio.CancelledError):
                await progress

    return asyncio.run(_drive())


async def _progress_loop(host: t.Any) -> None:
    """Print node transitions as they happen."""
    import asyncio

    from dreadnode.workflows import fold

    seen: dict[str, str] = {}
    while True:
        await asyncio.sleep(0.2)
        state = fold(host.facts)
        for unit, node in state.nodes.items():
            key = str(unit)
            if seen.get(key) != node.status:
                seen[key] = node.status
                console.print(
                    f"  {_styled(node.status.ljust(9), _NODE_STATUS_STYLE)} "
                    f"{unit.node_key}"
                    + (f"[{unit.ordinal}]" if unit.ordinal else "")
                    + (f" [dim]{node.error}[/]" if node.error else "")
                )


@cli.command(name="list", alias="ls")
def list_(
    *,
    project_id: str,
    definition_id: str | None = None,
    status: str | None = None,
    limit: int = 50,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Show workflow runs in a project.

    Args:
        project_id: Project to list runs for.
        definition_id: Only runs of this definition.
        status: Filter by run status.
        limit: Maximum results to show.
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    rows = api.list_workflow_runs(
        profile.org_key,
        profile.workspace_key,
        project_id=project_id,
        definition_id=definition_id,
        status=status,
        limit=limit,
    )
    if as_json:
        _print_json(rows)
        return
    if not rows:
        console.print("[dim]No workflow runs found[/]")
        return

    table = Table(box=None, pad_edge=False)
    for column in ("ID", "STATUS", "HOST", "FACTS", "STARTED"):
        table.add_column(column)
    for row in rows:
        table.add_row(
            _short_id(str(row["id"])),
            _styled(row["status"], _RUN_STATUS_STYLE),
            row.get("host_kind", "-"),
            str(row.get("last_fact_seq", 0)),
            str(row.get("started_at") or "[dim]-[/]"),
        )
    console.print(table)


@cli.command(name="status")
def status_(
    run_id: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Show a run with its node statuses.

    Args:
        run_id: The run to show.
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    detail = api.get_workflow_run(profile.org_key, profile.workspace_key, run_id)
    if as_json:
        _print_json(detail)
        return

    console.print(
        f"[bold]run {_short_id(str(detail['id']))}[/]  "
        f"{_styled(detail['status'], _RUN_STATUS_STYLE)}"
    )
    if detail["status"] == "lost":
        # Release 1 runs do not survive their runtime, and the UI must not
        # imply otherwise.
        console.print("[yellow]The runtime executing this run stopped. It will not resume.[/]")
    if detail.get("error"):
        console.print(f"[red]{detail['error']}[/]")

    nodes = detail.get("nodes") or []
    if not nodes:
        console.print("[dim]No nodes have been recorded yet[/]")
        return

    console.print()
    table = Table(box=None, pad_edge=False)
    for column in ("STEP", "STATUS", "SESSION", "DETAIL"):
        table.add_column(column)
    for node in nodes:
        label = node["node_key"]
        if node.get("ordinal"):
            label = f"{label}[{node['ordinal']}]"
        detail_text = (
            node.get("error")
            or node.get("skipped_reason")
            or (f"failure: {node['failure_class']}" if node.get("failure_class") else "")
        )
        table.add_row(
            label,
            _styled(node["status"], _NODE_STATUS_STYLE),
            _short_id(str(node["session_id"])) if node.get("session_id") else "[dim]-[/]",
            detail_text or "",
        )
    console.print(table)


@cli.command(name="cancel")
def cancel(
    run_id: str,
    *,
    project_id: str,
    force: t.Annotated[bool, cyclopts.Parameter(name="--force", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Cancel a workflow before a runtime claims it.

    Args:
        run_id: The run to cancel.
        project_id: Project containing the run.
        force: Skip the confirmation prompt.
    """
    api, profile = platform.connect()
    if not confirm_destructive(
        f"Cancel workflow run {_short_id(run_id)}?",
        yes=force,
    ):
        return
    cancelled = api.cancel_workflow_run(
        profile.org_key,
        profile.workspace_key,
        run_id,
        project_id=project_id,
    )
    console.print(
        f"Run [cyan]{_short_id(str(cancelled['id']))}[/] "
        f"is now {_styled(cancelled['status'], _RUN_STATUS_STYLE)}"
    )


# ---------------------------------------------------------------------------
# approvals
# ---------------------------------------------------------------------------


@cli.command(name="approvals")
def approvals(
    *,
    project_id: str,
    limit: int = 50,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """List approvals waiting on a decision.

    V1 uses this queue for in-agent tool calls. Authored workflow gates are
    rejected when the run is created.

    Args:
        project_id: Project to list approvals for.
        limit: Maximum results to show.
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    rows = api.list_workflow_approvals(
        profile.org_key,
        profile.workspace_key,
        project_id=project_id,
        limit=limit,
    )
    if as_json:
        _print_json(rows)
        return
    if not rows:
        console.print("[dim]Nothing is waiting on a decision[/]")
        return

    table = Table(box=None, pad_edge=False)
    for column in ("ID", "SUBJECT", "SUMMARY", "REQUESTED"):
        table.add_column(column)
    for row in rows:
        table.add_row(
            _short_id(str(row["id"])),
            row["subject_kind"],
            row["summary"],
            str(row.get("requested_at") or "-"),
        )
    console.print(table)


@cli.command(name="approve")
def approve(
    approval_id: str,
    *,
    session: t.Annotated[bool, cyclopts.Parameter(name="--session", negative=())] = False,
    note: str | None = None,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Allow a pending approval.

    Args:
        approval_id: The approval to allow.
        session: Allow for the rest of the session rather than once.
        note: Optional note recorded with the decision.
    """
    api, profile = platform.connect()
    decided = api.decide_workflow_approval(
        profile.org_key,
        profile.workspace_key,
        approval_id,
        outcome="allow_session" if session else "allow_once",
        note=note,
    )
    console.print(
        f"Approval [cyan]{_short_id(str(decided['id']))}[/] "
        f"[green]{decided['status']}[/] [dim](scope: {decided.get('scope')})[/]"
    )


@cli.command(name="deny")
def deny(
    approval_id: str,
    *,
    note: str | None = None,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Deny a pending approval.

    Args:
        approval_id: The approval to deny.
        note: Optional note recorded with the decision.
    """
    api, profile = platform.connect()
    decided = api.decide_workflow_approval(
        profile.org_key,
        profile.workspace_key,
        approval_id,
        outcome="deny",
        note=note,
    )
    console.print(f"Approval [cyan]{_short_id(str(decided['id']))}[/] [red]{decided['status']}[/]")
