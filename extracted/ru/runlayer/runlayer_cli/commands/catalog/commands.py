"""Typer wiring for `runlayer catalog`.

Every command is a thin wrapper: it gathers options and hands a `work(api)`
closure to `run_catalog_command`, which owns logging, client setup, and the
shared error/exit handling so that boilerplate lives in exactly one place.
"""

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable

import structlog
import typer

from runlayer_cli.api import RunlayerClient
from runlayer_cli.commands.catalog import display
from runlayer_cli.commands.catalog.kinds import (
    ALL_KINDS,
    CONNECTOR_KIND,
    KIND_BY_INFO_TYPE,
    PLUGIN_KIND,
    SKILL_KIND,
    CatalogInfoType,
    CatalogKind,
)
from runlayer_cli.config import resolve_credentials, set_credentials_in_context
from runlayer_cli.console import print_error
from runlayer_cli.logging import setup_logging

logger = structlog.get_logger(__name__)
app = typer.Typer(help="Browse available Runlayer catalog resources")

_SecretOption = typer.Option(None, "--secret", "-s", envvar="RUNLAYER_API_KEY")
_HostOption = typer.Option(None, "--host", "-H", envvar="RUNLAYER_HOST")
_QueryOption = typer.Option(None, "--query", "-q", help="Search text")
_NamespaceOption = typer.Option(None, "--namespace", "-N", help="Filter by namespace")
_JsonOption = typer.Option(False, "--json", help="Print JSON")
_IncludeBetaOption = typer.Option(
    False,
    "--include-beta",
    help="Include beta connectors (no effect on skills/plugins)",
)


@app.callback(invoke_without_command=True)
def catalog_callback(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


def _api(ctx: typer.Context, secret: str | None, host: str | None) -> RunlayerClient:
    set_credentials_in_context(ctx, secret, host)
    credentials = resolve_credentials(ctx, require_auth=True)
    return RunlayerClient(hostname=credentials["host"], secret=credentials["secret"])


def run_catalog_command(
    ctx: typer.Context,
    *,
    command: str,
    secret: str | None,
    host: str | None,
    work: Callable[[RunlayerClient], None],
) -> None:
    """Shared shell: logging + client + uniform error handling for every command."""
    log_file_path = setup_logging(command=command, quiet_console=False)
    try:
        work(_api(ctx, secret, host))
    except typer.Exit:
        raise
    except Exception as exc:
        logger.error(
            "catalog_command_failed",
            command=command,
            error=str(exc),
            exc_info=True,
        )
        print_error(str(exc), str(log_file_path))
        raise typer.Exit(1)


def _render_list(
    kind: CatalogKind[Any], items: list[Any], *, json_output: bool
) -> None:
    items = sorted(items, key=kind.sort_key)
    if json_output:
        display.dump_json([kind.to_summary(item) for item in items])
        return
    if not items:
        typer.echo(f"No {kind.noun}s found.")
        return
    for item in items:
        typer.echo(kind.render_row(item))
    typer.echo(f"\n{len(items)} {kind.noun}(s) available")


def _render_search_json(
    results: dict[str, list[Any]],
    errors: list[str],
    kinds: list[CatalogKind[Any]],
) -> None:
    payload: dict[str, Any] = {
        f"{kind.noun}s": [kind.to_summary(i) for i in results[kind.noun]]
        for kind in kinds
    }
    payload["errors"] = errors
    display.dump_json(payload)
    if errors and not any(results[kind.noun] for kind in kinds):
        raise typer.Exit(1)


def _render_search_text(
    results: dict[str, list[Any]],
    errors: list[str],
    kinds: list[CatalogKind[Any]],
) -> None:
    for error in errors:
        typer.echo(f"Warning: failed to search {error}", err=True)

    if not any(results[kind.noun] for kind in kinds):
        typer.echo("No catalog results found.")
        if errors:
            raise typer.Exit(1)
        return

    sections: list[str] = []
    for kind in kinds:
        items = results[kind.noun]
        if not items:
            continue
        rows = [f"{kind.noun.capitalize()}s:"]
        rows.extend(kind.render_row(item) for item in items)
        sections.append("\n".join(rows))
    typer.echo("\n\n".join(sections))


@app.command(name="skills", help="List available skills")
def skills(
    ctx: typer.Context,
    query: str | None = _QueryOption,
    namespace: str | None = _NamespaceOption,
    json_output: bool = _JsonOption,
    secret: str | None = _SecretOption,
    host: str | None = _HostOption,
) -> None:
    def work(api: RunlayerClient) -> None:
        items = SKILL_KIND.list_items(api, query=query, namespace=namespace)
        _render_list(SKILL_KIND, items, json_output=json_output)

    run_catalog_command(
        ctx, command="catalog-skills", secret=secret, host=host, work=work
    )


@app.command(name="plugins", help="List available plugins")
def plugins(
    ctx: typer.Context,
    query: str | None = _QueryOption,
    namespace: str | None = _NamespaceOption,
    json_output: bool = _JsonOption,
    secret: str | None = _SecretOption,
    host: str | None = _HostOption,
) -> None:
    def work(api: RunlayerClient) -> None:
        items = PLUGIN_KIND.list_items(api, query=query, namespace=namespace)
        _render_list(PLUGIN_KIND, items, json_output=json_output)

    run_catalog_command(
        ctx, command="catalog-plugins", secret=secret, host=host, work=work
    )


@app.command(name="connectors", help="List available MCP connectors")
def connectors(
    ctx: typer.Context,
    query: str | None = _QueryOption,
    include_beta: bool = _IncludeBetaOption,
    json_output: bool = _JsonOption,
    secret: str | None = _SecretOption,
    host: str | None = _HostOption,
) -> None:
    def work(api: RunlayerClient) -> None:
        items = CONNECTOR_KIND.list_items(
            api, query=query, namespace=None, include_beta=include_beta
        )
        _render_list(CONNECTOR_KIND, items, json_output=json_output)

    run_catalog_command(
        ctx, command="catalog-connectors", secret=secret, host=host, work=work
    )


@app.command(name="search", help="Search all catalog resources")
def search(
    ctx: typer.Context,
    query: str = typer.Argument(..., help="Search text"),
    include_beta: bool = _IncludeBetaOption,
    json_output: bool = _JsonOption,
    secret: str | None = _SecretOption,
    host: str | None = _HostOption,
) -> None:
    def work(api: RunlayerClient) -> None:
        results: dict[str, list[Any]] = {}
        errors: list[str] = []

        def list_kwargs(kind: CatalogKind[Any]) -> dict[str, Any]:
            # Only forward --include-beta to kinds that understand it; skills
            # and plugins have no beta concept, so passing it would error.
            kwargs: dict[str, Any] = {"query": query, "namespace": None}
            if kind.supports_beta:
                kwargs["include_beta"] = include_beta
            return kwargs

        # The three listings are independent network I/O; fetch concurrently
        # but keep per-kind partial-failure semantics and ALL_KINDS ordering.
        with ThreadPoolExecutor(max_workers=len(ALL_KINDS)) as pool:
            futures = {
                kind.noun: pool.submit(kind.list_items, api, **list_kwargs(kind))
                for kind in ALL_KINDS
            }
        for kind in ALL_KINDS:
            try:
                items = futures[kind.noun].result()
                results[kind.noun] = sorted(items, key=kind.sort_key)
            except Exception as exc:
                errors.append(f"{kind.noun}s: {exc}")
                results[kind.noun] = []

        if json_output:
            _render_search_json(results, errors, ALL_KINDS)
        else:
            _render_search_text(results, errors, ALL_KINDS)

    run_catalog_command(
        ctx, command="catalog-search", secret=secret, host=host, work=work
    )


@app.command(name="info", help="Show catalog item details")
def info(
    ctx: typer.Context,
    resource_type: CatalogInfoType = typer.Argument(..., help="Item type"),
    name_or_id: str = typer.Argument(..., help="Exact name or id"),
    json_output: bool = _JsonOption,
    secret: str | None = _SecretOption,
    host: str | None = _HostOption,
) -> None:
    def work(api: RunlayerClient) -> None:
        kind = KIND_BY_INFO_TYPE[resource_type]
        item = kind.resolve_ref(api, name_or_id)
        display.render_detail(kind.to_detail(item), json_output=json_output)

    run_catalog_command(
        ctx, command="catalog-info", secret=secret, host=host, work=work
    )
