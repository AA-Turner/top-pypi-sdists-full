from pathlib import Path
from typing import Any, NoReturn

import anyio
import httpx
import structlog
import typer
from fastmcp.client.transports import StreamableHttpTransport
from fastmcp.server.proxy import FastMCPProxy, ProxyClient
from rich.console import Console

from runlayer_cli.api import API_KEY_HEADER_NAME, USER_AGENT, RunlayerClient
from runlayer_cli.commands.interactive_find import (
    confirm_install,
    format_choice,
    prompt_clients,
    prompt_items,
    prompt_scope,
)
from runlayer_cli.console import print_error
from runlayer_cli.config import (
    Config,
    load_config,
    normalize_url,
    resolve_credentials,
    set_credentials_in_context,
)
from runlayer_cli.logging import setup_logging
from runlayer_cli.plugins.discovery import discover_plugins
from runlayer_cli.plugins.installer import (
    NATIVE_PLUGIN_CLIENTS,
    PluginInstallResult,
    PluginLockEntry,
    PluginUpdateResult,
    install_plugins,
    read_plugin_lockfile,
    resolve_plugin_dirs,
    uninstall_plugin,
    update_plugins,
)
from runlayer_cli.plugins.sync_engine import (
    PluginSyncResult,
    sync_discovered_plugins,
)
from runlayer_cli.tls import async_http_client
from runlayer_cli.uuid_utils import is_uuid

logger = structlog.get_logger(__name__)
console = Console()

app = typer.Typer(help="Manage plugins")


@app.callback(invoke_without_command=True)
def plugins_callback(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


# All clients supported for plugin install (native + MCP fallback)
_SUPPORTED_CLIENTS = NATIVE_PLUGIN_CLIENTS | {
    "windsurf",
    "goose",
    "zed",
    "opencode",
}


def _resolve_client(client_name: str | None) -> str:
    if client_name:
        if client_name not in _SUPPORTED_CLIENTS:
            typer.secho(
                f"Unsupported client: {client_name}. "
                f"Supported: {', '.join(sorted(_SUPPORTED_CLIENTS))}",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(1)
        return client_name
    return "claude_code"


def _scope_name(global_install: bool) -> str:
    return "global" if global_install else "project"


def _plugin_mcp_proxy_url(host: str, plugin_id: str) -> str:
    return f"{host.rstrip('/')}/api/v1/proxy/plugins/{plugin_id}/mcp"


def _context_value(ctx: typer.Context, key: str) -> str | None:
    current: Any = ctx
    while current:
        value = current.obj.get(key) if current.obj else None
        if isinstance(value, str) and value:
            return value
        current = current.parent
    return None


def _print_plugin_setup_message(host: str | None = None) -> None:
    login_host = host or "https://YOUR-TENANT.runlayer.com"
    typer.echo("Runlayer is not configured.", err=True)
    typer.echo("", err=True)
    typer.echo("Run:", err=True)
    typer.echo(f"  uvx runlayer login --host {login_host}", err=True)


def _exit_plugin_setup_required(host: str | None = None) -> NoReturn:
    _print_plugin_setup_message(host)
    raise typer.Exit(1)


def _exit_plugin_auth_failed(host: str) -> NoReturn:
    typer.echo(f"Runlayer authentication failed for {host}. Run:", err=True)
    typer.echo(f"  uvx runlayer login --host {host}", err=True)
    raise typer.Exit(1)


def _exit_plugin_not_accessible(plugin_id: str) -> NoReturn:
    typer.echo(f"Plugin MCP not found or not accessible: {plugin_id}", err=True)
    raise typer.Exit(1)


def _resolve_plugin_run_credentials(
    ctx: typer.Context,
    secret: str | None,
    host: str | None,
) -> tuple[str, str]:
    set_credentials_in_context(ctx, secret, host)
    config: Config = load_config()
    effective_host = _context_value(ctx, "host") or config.default_host
    if not effective_host:
        _exit_plugin_setup_required()

    effective_host = normalize_url(effective_host)
    effective_secret = _context_value(ctx, "secret") or config.get_secret_for_host(
        effective_host
    )
    if not effective_secret:
        _exit_plugin_setup_required(effective_host)

    return effective_host, effective_secret


def _verify_plugin_mcp_access(
    client: RunlayerClient,
    host: str,
    plugin_id: str,
) -> None:
    try:
        client.get_plugin(plugin_id)
    except httpx.HTTPStatusError as exc:
        status_code = exc.response.status_code
        if status_code == 401:
            _exit_plugin_auth_failed(host)
        if status_code in {403, 404, 422}:
            _exit_plugin_not_accessible(plugin_id)
        raise


def _group_plugins(entries: list[PluginLockEntry]) -> list[tuple[str, str, list[str]]]:
    grouped: dict[str, tuple[str, str, list[str]]] = {}

    for entry in entries:
        row = grouped.get(entry.id)
        if row is None:
            grouped[entry.id] = (entry.name, entry.namespace or "", [entry.client])
            continue

        name, namespace, clients = row
        if entry.client not in clients:
            clients.append(entry.client)
        if not namespace and entry.namespace:
            grouped[entry.id] = (name, entry.namespace, clients)

    rows = [
        (name, namespace, sorted(dict.fromkeys(clients)))
        for name, namespace, clients in grouped.values()
    ]
    rows.sort(key=lambda row: (row[0], row[1], ",".join(row[2])))
    return rows


@app.command(name="run", help="Run a plugin MCP proxy via stdio")
def run_plugin(
    ctx: typer.Context,
    plugin_id: str = typer.Argument(..., help="Plugin UUID to run"),
    secret: str | None = typer.Option(
        None,
        "--secret",
        "-s",
        envvar="RUNLAYER_API_KEY",
        help="API secret for authentication (optional if logged in)",
    ),
    host: str | None = typer.Option(
        None,
        "--host",
        "-H",
        envvar="RUNLAYER_HOST",
        help="Runlayer host URL (required if not in config)",
    ),
) -> None:
    log_file_path = setup_logging(command="plugins-run", quiet_console=True)

    try:
        if not is_uuid(plugin_id):
            _exit_plugin_not_accessible(plugin_id)

        effective_host, effective_secret = _resolve_plugin_run_credentials(
            ctx, secret, host
        )
        client = RunlayerClient(hostname=effective_host, secret=effective_secret)
        _verify_plugin_mcp_access(client, effective_host, plugin_id)

        mcp_url = _plugin_mcp_proxy_url(effective_host, plugin_id)
        transport = StreamableHttpTransport(
            url=mcp_url,
            headers={
                "User-Agent": USER_AGENT,
                API_KEY_HEADER_NAME: effective_secret,
            },
            httpx_client_factory=async_http_client,
        )
        proxy_client = ProxyClient(transport)

        def reuse_client_factory() -> ProxyClient:
            return proxy_client

        proxy = FastMCPProxy(
            client_factory=reuse_client_factory,
            name=f"runlayer-plugin-{plugin_id[:8]}",
        )

        async def tasks() -> None:
            await proxy.run_stdio_async(show_banner=False)

        logger.info("Starting Runlayer plugin MCP proxy", plugin_id=plugin_id)
        anyio.run(tasks)
    except typer.Exit:
        raise
    except KeyboardInterrupt:
        logger.info("Plugin MCP proxy shutdown requested by user")
    except Exception as e:
        logger.error(
            "plugins_run_failed",
            error=str(e),
            error_type=type(e).__name__,
            exc_info=True,
        )
        print_error(str(e), str(log_file_path))
        raise typer.Exit(1)


@app.command()
def push(
    ctx: typer.Context,
    path: str = typer.Argument(".", help="Root directory"),
    namespace: str = typer.Option(
        ..., "--namespace", "-N", help="Namespace for matching plugins on the server"
    ),
    public: bool = typer.Option(False, "--public"),
    dynamic_tools: bool = typer.Option(False, "--dynamic-tools"),
    secret: str | None = typer.Option(
        None, "--secret", "-s", envvar="RUNLAYER_API_KEY"
    ),
    host: str | None = typer.Option(None, "--host", "-H", envvar="RUNLAYER_HOST"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
    prune: bool = typer.Option(False, "--prune"),
) -> None:
    """Push plugins to Runlayer API."""
    root = Path(path).resolve()
    log_file_path = setup_logging(command="plugins-push", quiet_console=False)

    set_credentials_in_context(ctx, secret, host)
    credentials = resolve_credentials(ctx, require_auth=True)

    try:
        client = RunlayerClient(
            hostname=credentials["host"], secret=credentials["secret"]
        )

        discovered = discover_plugins(root)
        n_plugins = len(discovered)
        n_skills = sum(len(p.skills) for p in discovered)
        typer.echo(f"Found {n_plugins} plugins, {n_skills} skills")

        pushing_printed = False

        def _ensure_pushing_header() -> None:
            nonlocal pushing_printed
            if not pushing_printed:
                typer.echo("\nPushing...")
                pushing_printed = True

        def on_skill_progress(skill_path: str, status: str) -> None:
            if status not in ("unchanged",):
                _ensure_pushing_header()
                typer.echo(f"  {skill_path}: {status}")

        def on_plugin_progress(plugin_path: str, status: str) -> None:
            if status not in ("unchanged",):
                _ensure_pushing_header()
                typer.echo(f"  {plugin_path}: {status}")

        async def _run() -> PluginSyncResult:
            return await sync_discovered_plugins(
                discovered,
                client,
                namespace=namespace,
                is_public=public,
                use_dynamic_tools=dynamic_tools,
                dry_run=dry_run,
                prune=prune,
                on_skill_progress=on_skill_progress,
                on_plugin_progress=on_plugin_progress,
            )

        result = anyio.run(_run)
        sr = result.skill_result

        if dry_run:
            typer.secho("[dry run] ", fg=typer.colors.YELLOW, nl=False)

        # Build summary parts: skills first, then plugins (only if any changed)
        parts: list[str] = []
        if sr.created:
            parts.append(f"{sr.created} skills created")
        if sr.updated:
            parts.append(f"{sr.updated} skills updated")
        if sr.deleted:
            parts.append(f"{sr.deleted} skills deleted")

        if result.created:
            parts.append(f"{result.created} plugins created")
        if result.updated:
            parts.append(f"{result.updated} plugins updated")
        if result.deleted:
            parts.append(f"{result.deleted} plugins deleted")

        if parts:
            unchanged = sr.unchanged + result.unchanged
            summary = ", ".join(parts)
            if unchanged:
                typer.echo(f"Done, {summary} ({unchanged} unchanged)")
            else:
                typer.echo(f"Done, {summary}")
        else:
            typer.echo("Done, everything up to date")

        for warning in result.warnings:
            typer.secho(f"  Warning: {warning}", fg=typer.colors.YELLOW, err=True)
        if result.errors:
            for err in result.errors:
                typer.secho(f"  Error: {err}", fg=typer.colors.RED, err=True)
            raise typer.Exit(1)
    except typer.Exit:
        raise
    except Exception as e:
        logger.error("plugins_push_failed", error=str(e), exc_info=True)
        print_error(str(e), str(log_file_path))
        raise typer.Exit(1)


@app.command()
def find(
    ctx: typer.Context,
    secret: str | None = typer.Option(
        None, "--secret", "-s", envvar="RUNLAYER_API_KEY"
    ),
    host: str | None = typer.Option(None, "--host", "-H", envvar="RUNLAYER_HOST"),
) -> None:
    """Find and install one plugin from Runlayer API."""
    log_file_path = setup_logging(command="plugins-find", quiet_console=False)

    set_credentials_in_context(ctx, secret, host)
    credentials = resolve_credentials(ctx, require_auth=True)

    try:
        api = RunlayerClient(hostname=credentials["host"], secret=credentials["secret"])
        with console.status("Loading plugins..."):
            plugins = sorted(
                api.list_all_plugins(mine_only=False),
                key=lambda plugin: (
                    plugin.name.lower(),
                    (plugin.namespace or "").lower(),
                ),
            )
        selected_plugins = prompt_items(
            plugins,
            noun="plugins",
            format_item=lambda plugin: format_choice(plugin),
        )
        resolved_clients = prompt_clients(list(_SUPPORTED_CLIENTS))
        install_scope = prompt_scope()
        global_install = install_scope == "global"
        confirm_install(
            item_count=len(selected_plugins),
            client_count=len(resolved_clients),
            item_label="plugin(s)",
        )

        async def _run() -> PluginInstallResult:
            combined = PluginInstallResult()
            for resolved_client in resolved_clients:
                canonical, editor, lockfile = resolve_plugin_dirs(
                    resolved_client, global_install, Path.cwd()
                )

                def on_progress(name: str, status: str) -> None:
                    typer.echo(f"  {resolved_client} / {name}: {status}")

                for selected_plugin in selected_plugins:
                    result = await install_plugins(
                        client=api,
                        source=selected_plugin.id,
                        install_all=False,
                        plugin_name=None,
                        canonical_dir=canonical,
                        editor_dir=editor,
                        lockfile_path=lockfile,
                        client_name=resolved_client,
                        host=credentials["host"],
                        install_scope=install_scope,
                        dry_run=False,
                        on_progress=on_progress,
                        secret=credentials["secret"],
                    )
                    combined.installed.extend(result.installed)
                    combined.skipped.extend(result.skipped)
                    combined.errors.extend(result.errors)
            return combined

        result = anyio.run(_run)
        parts = []
        if result.installed:
            parts.append(f"{len(result.installed)} installed")
        if result.skipped:
            parts.append(f"{len(result.skipped)} skipped")
        typer.echo(f"Done: {', '.join(parts) if parts else 'nothing to do'}")

        if result.errors:
            for err in result.errors:
                typer.secho(f"  Error: {err}", fg=typer.colors.RED, err=True)
            raise typer.Exit(1)
    except typer.Exit:
        raise
    except Exception as e:
        logger.error("find_failed", error=str(e), exc_info=True)
        print_error(str(e), str(log_file_path))
        raise typer.Exit(1)


@app.command(
    name="list",
    help=(
        "List installed plugins in the selected scope.\n\n"
        "By default, lists project plugins for all clients.\n"
        "Use --global to list global plugins instead.\n"
        "Use --client to filter to one client."
    ),
)
def list_plugins(
    client_name: str | None = typer.Option(
        None, "--client", "-c", help="Filter to one client"
    ),
    global_install: bool = typer.Option(
        False, "--global", "-g", help="List global plugins instead of project plugins"
    ),
) -> None:
    """List installed plugins in the selected scope."""
    log_file_path = setup_logging(command="plugins-list", quiet_console=False)
    resolved_client = _resolve_client(client_name) if client_name else "claude_code"
    _, _, lockfile = resolve_plugin_dirs(resolved_client, global_install, Path.cwd())
    try:
        entries = read_plugin_lockfile(lockfile)
        if client_name:
            entries = [e for e in entries if e.client == resolved_client]
        grouped_entries = _group_plugins(entries)

        if not grouped_entries:
            typer.echo(f"No plugins installed in {_scope_name(global_install)} scope.")
            raise typer.Exit(0)

        for name, namespace, clients in grouped_entries:
            line = f"  {name}"
            if namespace:
                line += f"  ({namespace})"
            line += f"  [{', '.join(clients)}]"
            typer.echo(line)

        typer.echo(f"\n{len(grouped_entries)} plugin(s) installed")
    except typer.Exit:
        raise
    except Exception as e:
        logger.error("list_failed", error=str(e), exc_info=True)
        print_error(str(e), str(log_file_path))
        raise typer.Exit(1)


@app.command()
def add(
    ctx: typer.Context,
    source: str | None = typer.Argument(
        None, help="Plugin UUID or namespace (e.g. Org/Repo)"
    ),
    install_all: bool = typer.Option(
        False, "--all", help="Install all accessible plugins across namespaces"
    ),
    plugin: str | None = typer.Option(
        None, "--plugin", help="Filter by plugin name within namespace"
    ),
    client_name: str | None = typer.Option(
        None, "--client", "-c", help="Target editor client"
    ),
    global_install: bool = typer.Option(
        False, "--global", "-g", help="Install globally"
    ),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
    secret: str | None = typer.Option(
        None, "--secret", "-s", envvar="RUNLAYER_API_KEY"
    ),
    host: str | None = typer.Option(None, "--host", "-H", envvar="RUNLAYER_HOST"),
) -> None:
    """Add plugins from Runlayer API."""
    if install_all and source is not None:
        typer.secho(
            "Pass either SOURCE or --all, not both.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)
    if not install_all and source is None:
        typer.secho(
            "Missing argument 'SOURCE'. Use SOURCE or --all.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)

    log_file_path = setup_logging(command="plugins-add", quiet_console=False)

    set_credentials_in_context(ctx, secret, host)
    credentials = resolve_credentials(ctx, require_auth=not dry_run)

    resolved_client = _resolve_client(client_name)
    canonical, editor, lockfile = resolve_plugin_dirs(
        resolved_client, global_install, Path.cwd()
    )

    try:
        api = RunlayerClient(hostname=credentials["host"], secret=credentials["secret"])

        def on_progress(name: str, status: str) -> None:
            typer.echo(f"  {name}: {status}")

        async def _run() -> PluginInstallResult:
            return await install_plugins(
                client=api,
                source=source,
                install_all=install_all,
                plugin_name=plugin,
                canonical_dir=canonical,
                editor_dir=editor,
                lockfile_path=lockfile,
                client_name=resolved_client,
                host=credentials["host"],
                install_scope="global" if global_install else "project",
                dry_run=dry_run,
                on_progress=on_progress,
                secret=credentials["secret"],
            )

        result = anyio.run(_run)

        if dry_run:
            typer.secho("[dry run] ", fg=typer.colors.YELLOW, nl=False)

        scope = _scope_name(global_install)
        parts = []
        if result.installed:
            parts.append(f"{len(result.installed)} installed")
        if result.skipped:
            parts.append(f"{len(result.skipped)} skipped")
        typer.echo(
            f"Done: {', '.join(parts) if parts else 'nothing to do'} "
            f"for {resolved_client} in {scope} scope"
        )

        if result.errors:
            for err in result.errors:
                typer.secho(f"  Error: {err}", fg=typer.colors.RED, err=True)
            raise typer.Exit(1)

    except typer.Exit:
        raise
    except Exception as e:
        logger.error("add_failed", error=str(e), exc_info=True)
        print_error(str(e), str(log_file_path))
        raise typer.Exit(1)


@app.command()
def remove(
    plugin_ref: str | None = typer.Argument(None, help="Plugin name or UUID to remove"),
    remove_all: bool = typer.Option(
        False, "--all", help="Remove all installed plugins"
    ),
    yes: bool = typer.Option(False, "--yes", help="Skip confirmation prompt"),
    client_name: str | None = typer.Option(
        None, "--client", "-c", help="Target editor client"
    ),
    global_install: bool = typer.Option(
        False, "--global", "-g", help="Uninstall from global plugins"
    ),
) -> None:
    """Remove an installed plugin."""
    log_file_path = setup_logging(command="plugins-remove", quiet_console=False)
    if remove_all and plugin_ref is not None:
        typer.secho(
            "Pass either PLUGIN_REF or --all, not both.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)
    if not remove_all and plugin_ref is None:
        typer.secho(
            "Missing argument 'PLUGIN_REF'. Use PLUGIN_REF or --all.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)

    try:
        resolved_client = _resolve_client(client_name)
        canonical, editor, lockfile = resolve_plugin_dirs(
            resolved_client, global_install, Path.cwd()
        )

        if remove_all:
            entries = [
                e for e in read_plugin_lockfile(lockfile) if e.client == resolved_client
            ]
            if not entries:
                typer.echo("No plugins installed.")
                raise typer.Exit(0)

            names = list(dict.fromkeys(e.name for e in entries))
            if not yes:
                scope = "global" if global_install else "project"
                confirmed = typer.confirm(
                    f"Remove {len(names)} plugin(s) from {scope} install?",
                    default=False,
                )
                if not confirmed:
                    typer.echo("Aborted.")
                    raise typer.Exit(0)

            async def _run_all() -> list[str]:
                errors: list[str] = []
                for target_name in names:
                    try:
                        await uninstall_plugin(
                            target_name,
                            canonical,
                            editor,
                            lockfile,
                            resolved_client,
                        )
                    except Exception as e:
                        errors.append(f"{target_name}: {e}")
                return errors

            errors = anyio.run(_run_all)
            removed_count = len(names) - len(errors)
            typer.echo(f"Done: {removed_count} removed")
            if errors:
                for err in errors:
                    typer.secho(f"  Error: {err}", fg=typer.colors.RED, err=True)
                raise typer.Exit(1)
            return

        if plugin_ref is None:
            typer.secho(
                "Missing argument 'PLUGIN_REF'. Use PLUGIN_REF or --all.",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(1)

        async def _run() -> str:
            return await uninstall_plugin(
                plugin_ref, canonical, editor, lockfile, resolved_client
            )

        removed_name = anyio.run(_run)
        typer.echo(f"Removed: {removed_name}")

    except typer.Exit:
        raise
    except ValueError as e:
        if remove_all:
            logger.error("remove_failed", error=str(e), exc_info=True)
            print_error(str(e), str(log_file_path))
            raise typer.Exit(1)
        typer.secho(str(e), fg=typer.colors.RED, err=True)
        raise typer.Exit(1)
    except Exception as e:
        logger.error("remove_failed", error=str(e), exc_info=True)
        print_error(str(e), str(log_file_path))
        raise typer.Exit(1)


@app.command()
def update(
    ctx: typer.Context,
    plugin: str | None = typer.Option(
        None, "--plugin", help="Update specific plugin only"
    ),
    client_name: str | None = typer.Option(
        None, "--client", "-c", help="Target editor client"
    ),
    global_install: bool = typer.Option(
        False, "--global", "-g", help="Update global plugins"
    ),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
    secret: str | None = typer.Option(
        None, "--secret", "-s", envvar="RUNLAYER_API_KEY"
    ),
    host: str | None = typer.Option(None, "--host", "-H", envvar="RUNLAYER_HOST"),
) -> None:
    """Update installed plugins from Runlayer API."""
    log_file_path = setup_logging(command="plugins-update", quiet_console=False)

    set_credentials_in_context(ctx, secret, host)
    credentials = resolve_credentials(ctx, require_auth=not dry_run)

    resolved_client = _resolve_client(client_name)
    canonical, editor, lockfile = resolve_plugin_dirs(
        resolved_client, global_install, Path.cwd()
    )

    try:
        api = RunlayerClient(hostname=credentials["host"], secret=credentials["secret"])

        def on_progress(name: str, status: str) -> None:
            typer.echo(f"  {name}: {status}")

        async def _run() -> PluginUpdateResult:
            return await update_plugins(
                client=api,
                plugin_name=plugin,
                canonical_dir=canonical,
                editor_dir=editor,
                lockfile_path=lockfile,
                client_name=resolved_client,
                host=credentials["host"],
                install_scope="global" if global_install else "project",
                dry_run=dry_run,
                on_progress=on_progress,
                secret=credentials["secret"],
            )

        result = anyio.run(_run)

        if dry_run:
            typer.secho("[dry run] ", fg=typer.colors.YELLOW, nl=False)

        parts = []
        if result.updated:
            parts.append(f"{len(result.updated)} updated")
        if result.up_to_date:
            parts.append(f"{len(result.up_to_date)} up to date")
        if result.removed:
            parts.append(f"{len(result.removed)} removed")
        typer.echo(f"Done: {', '.join(parts) if parts else 'nothing to do'}")

        if result.errors:
            for err in result.errors:
                typer.secho(f"  Error: {err}", fg=typer.colors.RED, err=True)
            raise typer.Exit(1)

    except typer.Exit:
        raise
    except Exception as e:
        logger.error("update_failed", error=str(e), exc_info=True)
        print_error(str(e), str(log_file_path))
        raise typer.Exit(1)
