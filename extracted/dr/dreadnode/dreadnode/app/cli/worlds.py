"""Worlds subcommands for the cyclopts CLI."""

import typing as t

import cyclopts

from dreadnode.app.cli.args import PlatformScopeArgs
from dreadnode.app.cli.shared import (
    _FLAG_QUERY,
    _FLAG_STATUS,
    _collect_pages,
    _continuation,
    _fmt_count,
    _fmt_id,
    _label,
    _print_json,
    _render,
    _render_list,
    _status_color,
    _status_dot,
    _wait_for_job,
    console,
)
from dreadnode.app.model_catalog import resolve_model

cli = cyclopts.App(name="worlds", help="Work with simulated network environments.")


# ---------------------------------------------------------------------------
# Local helpers
# ---------------------------------------------------------------------------


def _summarize_job(p: dict[str, t.Any]) -> str:
    job_id = str(p.get("id", "unknown"))
    status = p.get("status", "unknown")
    kind = p.get("kind", "unknown")
    resource_type = p.get("resource_type") or "resource"
    color = _status_color(status)
    return "  ".join(
        [
            _fmt_id(job_id),
            _status_dot(status),
            f"[{color}]{status}[/{color}]",
            f"[cyan]{kind}[/cyan]",
            f"[dim]{resource_type}[/dim]",
        ]
    )


_JOB_LIST_ROW_FIELDS: tuple[str, ...] = (
    "status",
    "kind",
    "resource_type",
    "resource_id",
    "project_id",
    "created_by",
    "created_at",
    "updated_at",
)


def _summarize_manifest(p: dict[str, t.Any]) -> str:
    manifest_id = str(p.get("id", "unknown"))
    preset = p.get("preset") or "custom"
    name = p.get("name") or "unnamed-manifest"
    return "  ".join(
        [
            _fmt_id(manifest_id),
            f"[magenta]{preset}[/magenta]",
            f"[bold]{name}[/bold]",
        ]
    )


_MANIFEST_LIST_ROW_FIELDS: tuple[str, ...] = (
    "preset",
    "project_id",
    "created_by",
    "created_at",
    "updated_at",
)


def _summarize_trajectory(p: dict[str, t.Any]) -> str:
    traj_id = str(p.get("id", "unknown"))
    success = p.get("success")
    success_text = "success" if success else "pending" if success is None else "failed"
    goal = p.get("goal", "unknown")
    color = _status_color(success_text)
    return "  ".join(
        [
            _fmt_id(traj_id),
            _status_dot(success_text),
            f"[{color}]{success_text}[/{color}]",
            f"[cyan]{goal}[/cyan]",
        ]
    )


_TRAJECTORY_LIST_ROW_FIELDS: tuple[str, ...] = (
    "manifest_id",
    "success",
    "goal",
    "strategy",
    "mode",
    "project_id",
    "created_by",
    "created_at",
    "updated_at",
)


_EXPOSURE_COLORS = {
    "internet": "red",
    "external": "red",
    "dmz": "yellow",
    "internal": "default",
    "isolated": "dim",
}


def _exposure_markup(exposure: str | None) -> str:
    if not exposure:
        return "[dim]-[/dim]"
    color = _EXPOSURE_COLORS.get(exposure, "default")
    return f"[{color}]{exposure}[/{color}]"


def _graph_node_data(item: dict[str, t.Any]) -> dict[str, t.Any]:
    """Flatten the Cytoscape ``{data: {...}}`` wrapper for a graph node."""
    inner = item.get("data") if isinstance(item.get("data"), dict) else None
    return inner if inner is not None else item


def _summarize_graph_node(item: dict[str, t.Any]) -> str:
    data = _graph_node_data(item)
    node_id = str(data.get("id", "unknown"))
    node_type = data.get("node_type", "unknown")
    label = data.get("label") or ""
    return "  ".join(
        [
            _fmt_id(node_id),
            f"[magenta]{node_type}[/magenta]",
            f"[bold]{label}[/bold]" if label else "",
        ]
    ).strip()


_GRAPH_NODE_LIST_ROW_FIELDS: tuple[str, ...] = (
    "label",
    "node_type",
    "properties",
)


def _summarize_graph_edge(item: dict[str, t.Any]) -> str:
    data = _graph_node_data(item)
    edge_id = str(data.get("id", "unknown"))
    source = data.get("source", "?")
    target = data.get("target", "?")
    edge_type = data.get("edge_type", "unknown")
    severity = data.get("severity") or "info"
    sev_color = _status_color(severity)
    return "  ".join(
        [
            _fmt_id(edge_id),
            f"[{sev_color}]●[/{sev_color}] [{sev_color}]{severity}[/{sev_color}]",
            f"[cyan]{edge_type}[/cyan]",
            f"[dim]{source} → {target}[/dim]",
        ]
    )


_GRAPH_EDGE_LIST_ROW_FIELDS: tuple[str, ...] = (
    "source",
    "target",
    "edge_type",
    "severity",
)


def _render_subgraph_detail(p: dict[str, t.Any]) -> None:
    """Multi-line detail view for ``worlds subgraph`` (CLI-OUT-001)."""
    center = p.get("center", "unknown")
    depth = p.get("depth", 0)
    nodes = p.get("nodes") or []
    edges = p.get("edges") or []

    console.print(f"[bold]Subgraph[/bold] [dim]centered on[/dim] [cyan]{center}[/cyan]")
    console.print(f"{_label('Depth')}{depth}")
    console.print(f"{_label('Nodes')}{_fmt_count(len(nodes))}")
    console.print(f"{_label('Edges')}{_fmt_count(len(edges))}")

    if nodes:
        console.print()
        console.print(f"{_label('Sample')}[dim]first {min(5, len(nodes))} nodes[/dim]")
        for raw in nodes[:5]:
            console.print(f"{_continuation()}{_summarize_graph_node(raw)}")
        if len(nodes) > 5:
            console.print(f"{_continuation()}[dim](+{len(nodes) - 5} more — use --json)[/dim]")


def _summarize_principal(p: dict[str, t.Any]) -> str:
    principal_id = str(p.get("principal_id", "unknown"))
    principal_type = p.get("principal_type") or "unknown"
    sam = p.get("sam") or ""
    enabled = p.get("enabled", True)
    state_color = "green" if enabled else "dim"
    state_text = "enabled" if enabled else "disabled"
    domain = p.get("domain")
    name = f"[bold]{sam}[/bold]" + (f"[dim]@{domain}[/dim]" if domain else "")
    return "  ".join(
        [
            _fmt_id(principal_id),
            f"{_status_dot(state_text, color=state_color)} [{state_color}]{state_text}[/{state_color}]",
            f"[magenta]{principal_type}[/magenta]",
            name,
        ]
    )


_PRINCIPAL_LIST_ROW_FIELDS: tuple[str, ...] = (
    "principal_id",
    "principal_type",
    "sam",
    "enabled",
    "upn",
    "dn",
    "sid",
    "domain",
    "email",
    "department",
    "title",
)


def _render_principal_detail(p: dict[str, t.Any], *, full: bool = False) -> None:
    """Multi-line detail for ``worlds principal`` / ``worlds principal-details``.

    *full* controls whether expanded details (credentials, edges) are rendered.
    """
    principal_id = str(p.get("principal_id", "unknown"))
    sam = p.get("sam") or "unnamed"
    domain = p.get("domain")
    enabled = p.get("enabled", True)
    state_color = "green" if enabled else "dim"
    state_text = "enabled" if enabled else "disabled"

    header_name = f"[bold]{sam}[/bold]" + (f"[dim]@{domain}[/dim]" if domain else "")
    console.print(
        f"{_status_dot(state_text, color=state_color)} "
        f"[{state_color}]{state_text}[/{state_color}]  {header_name} "
        f"[dim]({p.get('principal_type') or 'principal'})[/dim]"
    )
    console.print(f"{_label('Principal')}{_fmt_id(principal_id)}")
    if p.get("upn"):
        console.print(f"{_label('UPN')}{p['upn']}")
    if p.get("dn"):
        console.print(f"{_label('DN')}[dim]{p['dn']}[/dim]")
    if p.get("sid"):
        console.print(f"{_label('SID')}[dim]{p['sid']}[/dim]")
    if p.get("email"):
        console.print(f"{_label('Email')}{p['email']}")
    if p.get("department"):
        console.print(f"{_label('Department')}{p['department']}")
    if p.get("title"):
        console.print(f"{_label('Title')}{p['title']}")

    if full:
        memberships = p.get("membership_ids") or []
        credentials = p.get("credentials") or []
        inbound = p.get("inbound_edges") or []
        outbound = p.get("outbound_edges") or []
        if memberships or credentials or inbound or outbound:
            console.print()
        if memberships:
            console.print(f"{_label('Memberships')}{_fmt_count(len(memberships))}")
        if credentials:
            console.print(f"{_label('Credentials')}{_fmt_count(len(credentials))}")
            for cred in credentials[:5]:
                console.print(
                    f"{_continuation()}[cyan]{cred.get('kind', '?')}[/cyan]  "
                    f"[dim]{cred.get('cred_id', '?')}[/dim]"
                )
            if len(credentials) > 5:
                console.print(f"{_continuation()}[dim](+{len(credentials) - 5} more)[/dim]")
        if inbound:
            console.print(f"{_label('Inbound')}{_fmt_count(len(inbound))} edges")
        if outbound:
            console.print(f"{_label('Outbound')}{_fmt_count(len(outbound))} edges")


def _summarize_host(p: dict[str, t.Any]) -> str:
    host_id = str(p.get("host_id", "unknown"))
    hostname = p.get("hostname") or "unnamed-host"
    ip = p.get("ip") or ""
    os_family = p.get("os_family") or "unknown"
    exposure = p.get("exposure_profile") or "unknown"
    return "  ".join(
        [
            _fmt_id(host_id),
            f"[bold]{hostname}[/bold]",
            f"[dim]{ip}[/dim]" if ip else "",
            f"[magenta]{os_family}[/magenta]",
            _exposure_markup(exposure),
        ]
    ).strip()


def _render_host_detail(p: dict[str, t.Any], *, full: bool = False) -> None:
    """Multi-line detail for ``worlds host`` / ``worlds host-details``."""
    host_id = str(p.get("host_id", "unknown"))
    hostname = p.get("hostname") or "unnamed-host"
    exposure = p.get("exposure_profile") or "unknown"

    console.print(f"[bold]{hostname}[/bold] [dim]({p.get('os_family') or 'unknown'})[/dim]")
    console.print(f"{_label('Host')}{_fmt_id(host_id)}")
    if p.get("ip"):
        console.print(f"{_label('IP')}{p['ip']}")
    if p.get("fqdn"):
        console.print(f"{_label('FQDN')}{p['fqdn']}")
    if p.get("os_version"):
        console.print(f"{_label('OS')}[dim]{p['os_version']}[/dim]")
    console.print(f"{_label('Exposure')}{_exposure_markup(exposure)}")
    if p.get("domain"):
        console.print(f"{_label('Domain')}{p['domain']}")
    if p.get("subnet"):
        console.print(f"{_label('Subnet')}[dim]{p['subnet']}[/dim]")
    if p.get("role"):
        console.print(f"{_label('Role')}{p['role']}")
    if p.get("site"):
        console.print(f"{_label('Site')}{p['site']}")

    if full:
        services = p.get("services") or []
        artifacts = p.get("artifacts") or []
        inbound = p.get("inbound_edges") or []
        outbound = p.get("outbound_edges") or []
        if services or artifacts or inbound or outbound:
            console.print()
        if services:
            console.print(f"{_label('Services')}{_fmt_count(len(services))}")
            for svc in services[:5]:
                state = svc.get("state") or "?"
                state_color = _status_color(state)
                console.print(
                    f"{_continuation()}[{state_color}]●[/{state_color}] "
                    f"[cyan]{svc.get('name', '?')}[/cyan]:[dim]{svc.get('port', '?')}[/dim]/"
                    f"[dim]{svc.get('proto', '?')}[/dim]"
                )
            if len(services) > 5:
                console.print(f"{_continuation()}[dim](+{len(services) - 5} more)[/dim]")
        if artifacts:
            console.print(f"{_label('Artifacts')}{_fmt_count(len(artifacts))}")
        if inbound:
            console.print(f"{_label('Inbound')}{_fmt_count(len(inbound))} edges")
        if outbound:
            console.print(f"{_label('Outbound')}{_fmt_count(len(outbound))} edges")


def _summarize_command_info(p: dict[str, t.Any]) -> str:
    name = p.get("name") or "unknown"
    pattern = p.get("pattern") or ""
    description = (p.get("description") or "").replace("\n", " ")[:80]
    parts = [f"[cyan]{name}[/cyan]"]
    if pattern:
        parts.append(f"[dim]{pattern}[/dim]")
    if description:
        parts.append(description)
    return "  ".join(parts)


_COMMAND_INFO_LIST_ROW_FIELDS: tuple[str, ...] = (
    "name",
    "pattern",
    "description",
    "usage",
    "examples",
    "events",
)


ManifestPreset = t.Literal["small", "medium", "large", "enterprise"]
TrajectoryStrategy = t.Literal["random", "greedy", "recon-first", "smart-random"]
TrajectoryMode = t.Literal["kali", "c2", "agent"]
JobKind = t.Literal["manifest_generation", "trajectory_generation"]
JobStatus = t.Literal["queued", "running", "completed", "failed", "cancelled"]


# ---------------------------------------------------------------------------
# manifest-create
# ---------------------------------------------------------------------------


@cli.command(name="manifest-create")
def manifest_create(
    *,
    name: t.Annotated[str | None, cyclopts.Parameter(help="Manifest name")] = None,
    project_id: t.Annotated[str | None, cyclopts.Parameter(help="Project ID to associate")] = None,
    preset: ManifestPreset | None = None,
    seed: t.Annotated[
        int | None, cyclopts.Parameter(help="Random seed for reproducibility")
    ] = None,
    num_users: t.Annotated[
        int | None, cyclopts.Parameter(help="Number of users to generate")
    ] = None,
    num_hosts: t.Annotated[
        int | None, cyclopts.Parameter(help="Number of hosts to generate")
    ] = None,
    domain: t.Annotated[
        list[str] | None, cyclopts.Parameter(negative_iterable=(), help="Domain name (repeatable)")
    ] = None,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Create a new world manifest."""
    api, profile = platform.connect()
    payload = api.create_world_manifest(
        profile.org_key,
        profile.workspace_key,
        name=name,
        project_id=project_id,
        preset=preset,
        seed=seed,
        num_users=num_users,
        num_hosts=num_hosts,
        domains=list(domain or []) or None,
    )
    _render(payload, as_json=as_json, summary=_summarize_job)


# ---------------------------------------------------------------------------
# manifest-list
# ---------------------------------------------------------------------------


@cli.command(name="manifest-list")
def manifest_list(
    *,
    project_id: t.Annotated[str | None, cyclopts.Parameter(help="Project ID filter")] = None,
    created_by: t.Annotated[str | None, cyclopts.Parameter(help="Filter by creator")] = None,
    limit: int = 50,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """List world manifests."""
    api, profile = platform.connect()
    items = _collect_pages(
        lambda page, page_size: api.list_world_manifests(
            profile.org_key,
            profile.workspace_key,
            project_id=project_id,
            created_by=created_by,
            page=page,
            page_size=page_size,
        ),
        limit=limit,
        page_size=50,
    )
    _render_list(
        items,
        as_json=as_json,
        summary=_summarize_manifest,
        empty_msg="No manifests found",
        fields=_MANIFEST_LIST_ROW_FIELDS,
    )


# ---------------------------------------------------------------------------
# manifest-get
# ---------------------------------------------------------------------------


@cli.command(name="manifest-get")
def manifest_get(
    manifest_id: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Get a world manifest by ID."""
    api, profile = platform.connect()
    payload = api.get_world_manifest(profile.org_key, profile.workspace_key, manifest_id)
    _render(payload, as_json=as_json, summary=_summarize_manifest)


# ---------------------------------------------------------------------------
# graph-nodes
# ---------------------------------------------------------------------------


@cli.command(name="graph-nodes")
def graph_nodes(
    manifest_id: str,
    *,
    limit: int = 1000,
    offset: int = 0,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Get graph nodes for a world manifest."""
    api, profile = platform.connect()
    payload = api.get_world_manifest_graph_nodes(
        profile.org_key,
        profile.workspace_key,
        manifest_id,
        limit=limit,
        offset=offset,
    )
    nodes = [_graph_node_data(node) for node in (payload.get("nodes") or [])]
    _render_list(
        nodes,
        as_json=as_json,
        summary=_summarize_graph_node,
        empty_msg="No graph nodes found",
        fields=_GRAPH_NODE_LIST_ROW_FIELDS,
    )


# ---------------------------------------------------------------------------
# graph-edges
# ---------------------------------------------------------------------------


@cli.command(name="graph-edges")
def graph_edges(
    manifest_id: str,
    *,
    limit: int = 5000,
    offset: int = 0,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Get graph edges for a world manifest."""
    api, profile = platform.connect()
    payload = api.get_world_manifest_graph_edges(
        profile.org_key,
        profile.workspace_key,
        manifest_id,
        limit=limit,
        offset=offset,
    )
    edges = [_graph_node_data(edge) for edge in (payload.get("edges") or [])]
    _render_list(
        edges,
        as_json=as_json,
        summary=_summarize_graph_edge,
        empty_msg="No graph edges found",
        fields=_GRAPH_EDGE_LIST_ROW_FIELDS,
    )


# ---------------------------------------------------------------------------
# subgraph
# ---------------------------------------------------------------------------


@cli.command()
def subgraph(
    manifest_id: str,
    center: str,
    *,
    depth: int = 2,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Get a subgraph centered on a node."""
    api, profile = platform.connect()
    payload = api.get_world_manifest_subgraph(
        profile.org_key,
        profile.workspace_key,
        manifest_id,
        center=center,
        depth=depth,
    )
    if as_json:
        _print_json(payload)
    else:
        _render_subgraph_detail(payload)


# ---------------------------------------------------------------------------
# principals
# ---------------------------------------------------------------------------


@cli.command()
def principals(
    manifest_id: str,
    *,
    query: t.Annotated[
        str | None,
        cyclopts.Parameter(name=_FLAG_QUERY, help="Search query"),
    ] = None,
    principal_type: t.Annotated[
        str | None, cyclopts.Parameter(help="Filter by principal type")
    ] = None,
    limit: int = 50,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Search principals in a world manifest."""
    api, profile = platform.connect()
    items = _collect_pages(
        lambda page, page_size: api.search_world_manifest_principals(
            profile.org_key,
            profile.workspace_key,
            manifest_id,
            query=query,
            principal_type=principal_type,
            page=page,
            page_size=page_size,
        ),
        limit=limit,
        page_size=50,
    )
    _render_list(
        items,
        as_json=as_json,
        summary=_summarize_principal,
        empty_msg="No principals found",
        fields=_PRINCIPAL_LIST_ROW_FIELDS,
    )


# ---------------------------------------------------------------------------
# principal
# ---------------------------------------------------------------------------


@cli.command()
def principal(
    manifest_id: str,
    principal_id: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Get a principal by ID."""
    api, profile = platform.connect()
    payload = api.get_world_manifest_principal(
        profile.org_key,
        profile.workspace_key,
        manifest_id,
        principal_id,
    )
    if as_json:
        _print_json(payload)
    else:
        _render_principal_detail(payload)


# ---------------------------------------------------------------------------
# principal-details
# ---------------------------------------------------------------------------


@cli.command(name="principal-details")
def principal_details(
    manifest_id: str,
    principal_id: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Get detailed info for a principal."""
    api, profile = platform.connect()
    payload = api.get_world_manifest_principal_details(
        profile.org_key,
        profile.workspace_key,
        manifest_id,
        principal_id,
    )
    if as_json:
        _print_json(payload)
    else:
        _render_principal_detail(payload, full=True)


# ---------------------------------------------------------------------------
# host
# ---------------------------------------------------------------------------


@cli.command()
def host(
    manifest_id: str,
    host_id: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Get a host by ID."""
    api, profile = platform.connect()
    payload = api.get_world_manifest_host(
        profile.org_key,
        profile.workspace_key,
        manifest_id,
        host_id,
    )
    if as_json:
        _print_json(payload)
    else:
        _render_host_detail(payload)


# ---------------------------------------------------------------------------
# host-details
# ---------------------------------------------------------------------------


@cli.command(name="host-details")
def host_details(
    manifest_id: str,
    host_id: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Get detailed info for a host."""
    api, profile = platform.connect()
    payload = api.get_world_manifest_host_details(
        profile.org_key,
        profile.workspace_key,
        manifest_id,
        host_id,
    )
    if as_json:
        _print_json(payload)
    else:
        _render_host_detail(payload, full=True)


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------


@cli.command()
def commands(
    manifest_id: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """List commands for a world manifest."""
    api, profile = platform.connect()
    payload = api.list_world_manifest_commands(profile.org_key, profile.workspace_key, manifest_id)
    _render_list(
        payload,
        as_json=as_json,
        summary=_summarize_command_info,
        empty_msg="No commands found",
        fields=_COMMAND_INFO_LIST_ROW_FIELDS,
    )


# ---------------------------------------------------------------------------
# manifest-trajectories
# ---------------------------------------------------------------------------


@cli.command(name="manifest-trajectories")
def manifest_trajectories(
    manifest_id: str,
    *,
    limit: int = 50,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """List trajectories for a world manifest."""
    api, profile = platform.connect()
    items = _collect_pages(
        lambda page, page_size: api.list_world_manifest_trajectories(
            profile.org_key,
            profile.workspace_key,
            manifest_id,
            page=page,
            page_size=page_size,
        ),
        limit=limit,
        page_size=50,
    )
    _render_list(
        items,
        as_json=as_json,
        summary=_summarize_trajectory,
        empty_msg="No trajectories found",
        fields=_TRAJECTORY_LIST_ROW_FIELDS,
    )


# ---------------------------------------------------------------------------
# trajectory-create
# ---------------------------------------------------------------------------


@cli.command(name="trajectory-create")
def trajectory_create(
    *,
    manifest_id: str,
    name: t.Annotated[str | None, cyclopts.Parameter(help="Trajectory name")] = None,
    project_id: t.Annotated[str | None, cyclopts.Parameter(help="Project ID to associate")] = None,
    goal: t.Annotated[str, cyclopts.Parameter(help="Target goal for trajectory")] = "Domain Admins",
    count: t.Annotated[int, cyclopts.Parameter(help="Number of trajectories to generate")] = 1,
    strategy: TrajectoryStrategy = "random",
    max_steps: t.Annotated[int, cyclopts.Parameter(help="Maximum steps per trajectory")] = 100,
    seed: t.Annotated[int, cyclopts.Parameter(help="Random seed for reproducibility")] = 42,
    threads: t.Annotated[int, cyclopts.Parameter(help="Number of parallel threads")] = 1,
    only_successful: t.Annotated[
        bool,
        cyclopts.Parameter(negative=()),
    ] = False,
    mode: TrajectoryMode = "kali",
    runtime_id: t.Annotated[str | None, cyclopts.Parameter(help="Runtime environment ID")] = None,
    capability_name: t.Annotated[str | None, cyclopts.Parameter(help="Capability to use")] = None,
    agent_name: t.Annotated[
        str | None, cyclopts.Parameter(help="Agent name within capability")
    ] = None,
    agent_model: t.Annotated[str | None, cyclopts.Parameter(help="Model for the agent")] = None,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Create a new world trajectory."""
    api, profile = platform.connect()
    payload = api.create_world_trajectory(
        profile.org_key,
        profile.workspace_key,
        manifest_id=manifest_id,
        name=name,
        project_id=project_id,
        goal=goal,
        count=count,
        strategy=strategy,
        max_steps=max_steps,
        seed=seed,
        threads=threads,
        only_successful=only_successful,
        mode=mode,
        runtime_id=runtime_id,
        capability_name=capability_name,
        agent_name=agent_name,
        agent_model=resolve_model(agent_model) if agent_model else None,
    )
    _render(payload, as_json=as_json, summary=_summarize_job)


# ---------------------------------------------------------------------------
# trajectory-list
# ---------------------------------------------------------------------------


@cli.command(name="trajectory-list")
def trajectory_list(
    *,
    manifest_id: t.Annotated[str | None, cyclopts.Parameter(help="Filter by manifest ID")] = None,
    project_id: t.Annotated[str | None, cyclopts.Parameter(help="Project ID filter")] = None,
    created_by: t.Annotated[str | None, cyclopts.Parameter(help="Filter by creator")] = None,
    limit: int = 50,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """List world trajectories."""
    api, profile = platform.connect()
    items = _collect_pages(
        lambda page, page_size: api.list_world_trajectories(
            profile.org_key,
            profile.workspace_key,
            manifest_id=manifest_id,
            project_id=project_id,
            created_by=created_by,
            page=page,
            page_size=page_size,
        ),
        limit=limit,
        page_size=50,
    )
    _render_list(
        items,
        as_json=as_json,
        summary=_summarize_trajectory,
        empty_msg="No trajectories found",
        fields=_TRAJECTORY_LIST_ROW_FIELDS,
    )


# ---------------------------------------------------------------------------
# trajectory-get
# ---------------------------------------------------------------------------


@cli.command(name="trajectory-get")
def trajectory_get(
    trajectory_id: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Get a world trajectory by ID."""
    api, profile = platform.connect()
    payload = api.get_world_trajectory(profile.org_key, profile.workspace_key, trajectory_id)
    _render(payload, as_json=as_json, summary=_summarize_trajectory)


# ---------------------------------------------------------------------------
# job-list
# ---------------------------------------------------------------------------


@cli.command(name="job-list")
def job_list(
    *,
    project_id: t.Annotated[str | None, cyclopts.Parameter(help="Project ID filter")] = None,
    created_by: t.Annotated[str | None, cyclopts.Parameter(help="Filter by creator")] = None,
    kind: JobKind | None = None,
    status: t.Annotated[
        JobStatus | None,
        cyclopts.Parameter(name=_FLAG_STATUS),
    ] = None,
    limit: int = 50,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """List world jobs."""
    api, profile = platform.connect()
    items = _collect_pages(
        lambda page, page_size: api.list_world_jobs(
            profile.org_key,
            profile.workspace_key,
            project_id=project_id,
            created_by=created_by,
            kind=kind,
            status=status,
            page=page,
            page_size=page_size,
        ),
        limit=limit,
        page_size=50,
    )
    _render_list(
        items,
        as_json=as_json,
        summary=_summarize_job,
        empty_msg="No jobs found",
        fields=_JOB_LIST_ROW_FIELDS,
    )


# ---------------------------------------------------------------------------
# job-get
# ---------------------------------------------------------------------------


@cli.command(name="job-get")
def job_get(
    job_id: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Get a world job by ID."""
    api, profile = platform.connect()
    payload = api.get_world_job(profile.org_key, profile.workspace_key, job_id)
    _render(payload, as_json=as_json, summary=_summarize_job)


# ---------------------------------------------------------------------------
# job-wait
# ---------------------------------------------------------------------------


@cli.command(name="job-wait")
def job_wait(
    job_id: str,
    *,
    poll_interval_sec: t.Annotated[
        float,
        cyclopts.Parameter(
            validator=cyclopts.validators.Number(gt=0), help="Polling interval in seconds"
        ),
    ] = 5.0,
    timeout_sec: t.Annotated[
        float | None, cyclopts.Parameter(help="Timeout in seconds for waiting")
    ] = None,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Wait for a world job to complete."""
    api, profile = platform.connect()
    payload = _wait_for_job(
        lambda: api.get_world_job(profile.org_key, profile.workspace_key, job_id),
        job_id=job_id,
        label="world",
        poll_interval_sec=poll_interval_sec,
        timeout_sec=timeout_sec,
    )
    _render(payload, as_json=as_json, summary=_summarize_job)
    if payload.get("status") != "completed":
        raise RuntimeError(
            payload.get("error") or f"World job {job_id} ended with status {payload.get('status')}"
        )


# ---------------------------------------------------------------------------
# job-cancel
# ---------------------------------------------------------------------------


@cli.command(name="job-cancel")
def job_cancel(
    job_id: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Cancel a world job."""
    api, profile = platform.connect()
    payload = api.cancel_world_job(profile.org_key, profile.workspace_key, job_id)
    _render(payload, as_json=as_json, summary=_summarize_job)
