"""Namespace administration and table discovery for Arraylake's Iceberg catalog."""

import json
import re
from enum import StrEnum
from typing import Any

import typer
from rich.table import Table

from arraylake import Client
from arraylake.cli.utils import rich_console
from arraylake.types import RepoVisibility

app = typer.Typer(help="Manage Iceberg namespaces and discover tables", no_args_is_help=True)
namespace_app = typer.Typer(help="Manage Iceberg namespaces", no_args_is_help=True)
table_app = typer.Typer(help="Discover and describe Iceberg tables", no_args_is_help=True)
app.add_typer(namespace_app, name="namespace")
app.add_typer(table_app, name="table")


class Output(StrEnum):
    rich = "rich"
    json = "json"


class NamespaceSort(StrEnum):
    relevance = "relevance"
    updated = "updated"
    created = "created"
    name = "name"
    tables = "tables"


class TableSort(StrEnum):
    relevance = "relevance"
    updated = "updated"
    created = "created"
    name = "name"


class Direction(StrEnum):
    asc = "asc"
    desc = "desc"


def _table_identifier(namespace: str, table: str) -> str:
    """Format exact names; quoted components escape double quotes by doubling them."""

    def quote(name: str) -> str:
        return name if re.fullmatch(r"[A-Za-z0-9_-]+", name) else '"' + name.replace('"', '""') + '"'

    return f"{quote(namespace)}.{quote(table)}"


def _parse_table_identifier(identifier: str) -> tuple[str, str]:
    # Keep this grammar in sync with the app's iceberg-identifier.ts formatter.
    component = r'(?:[A-Za-z0-9_-]+|"(?:[^"]|"")+")'
    match = re.fullmatch(rf"({component})\.({component})", identifier)
    if match is None:
        raise typer.BadParameter(
            "Expected NAMESPACE.TABLE. Double-quote names containing dots or special characters, "
            "and wrap the identifier in single quotes in your shell, e.g. '\"namespace.v2\".table'.",
            param_hint="IDENTIFIER",
        )
    namespace, table = (part[1:-1].replace('""', '"') if part.startswith('"') else part for part in match.groups())
    return namespace, table


def _json_object(value: str | None, option: str) -> dict[str, Any] | None:
    if value is None:
        return None
    try:
        result = json.loads(value)
    except ValueError as exc:
        raise typer.BadParameter("Expected a JSON object", param_hint=option) from exc
    if not isinstance(result, dict):
        raise typer.BadParameter("Expected a JSON object", param_hint=option)
    return result


def _show(value: Any, output: Output) -> None:
    if output == Output.json:
        typer.echo(json.dumps(value))
    else:
        rich_console.print(value)


def _show_list(rows: list[dict[str, Any]], output: Output, *, namespaces: bool) -> None:
    if not namespaces:
        rows = [{**row, "identifier": _table_identifier(row["namespace"], row["name"])} for row in rows]
    if output == Output.json:
        _show(rows, output)
        return
    table = Table("Name" if namespaces else "Identifier", "Updated", "Tables" if namespaces else "Storage override")
    for row in rows:
        table.add_row(
            row["name"] if namespaces else row["identifier"],
            row["updated"],
            str(row["table_count"] if namespaces else row["has_storage_override"]),
        )
    rich_console.print(table)


@namespace_app.command("list")
def list_namespaces(
    org: str,
    search: str | None = None,
    filter_metadata: str | None = typer.Option(None, help="JSON metadata filter"),
    sort: NamespaceSort | None = None,
    direction: Direction = Direction.desc,
    include_ghosts: bool = False,
    page_size: int = typer.Option(50, min=1, max=100),
    output: Output = Output.rich,
):
    """List namespaces, with optional search, metadata filters, and sorting."""
    rows = Client().list_iceberg_namespaces_paginated(
        org,
        search=search,
        filter_metadata=_json_object(filter_metadata, "--filter-metadata"),
        sort=sort.value if sort else None,
        direction=direction.value,
        include_ghosts=include_ghosts,
        page_size=page_size,
    )
    _show_list([row.model_dump(mode="json") for row in rows], output, namespaces=True)


@namespace_app.command("get")
def get_namespace(org: str, name: str, output: Output = Output.rich):
    """Show namespace storage, description, metadata, and visibility."""
    _show(Client().get_iceberg_namespace(org, name).model_dump(mode="json"), output)


@namespace_app.command("create")
def create_namespace(
    org: str,
    name: str,
    bucket_config_nickname: str | None = None,
    description: str | None = None,
    metadata: str | None = typer.Option(None, help="JSON discovery metadata"),
    visibility: RepoVisibility = RepoVisibility.PRIVATE,
    properties: str | None = typer.Option(None, help="JSON Iceberg properties (string values)"),
    output: Output = Output.rich,
):
    """Create a namespace on the chosen or default bucket."""
    props = _json_object(properties, "--properties")
    if props is not None and any(not isinstance(v, str) for v in props.values()):
        raise typer.BadParameter("Property values must be strings", param_hint="--properties")
    result = Client().create_iceberg_namespace(
        org,
        name,
        bucket_config_nickname=bucket_config_nickname,
        description=description,
        metadata=_json_object(metadata, "--metadata"),
        visibility=visibility,
        properties=props,
    )
    _show(result.model_dump(mode="json"), output)


@namespace_app.command("update")
def update_namespace(
    org: str,
    name: str,
    description: str | None = None,
    add_metadata: str | None = typer.Option(None, help="JSON metadata to add"),
    remove_metadata: list[str] | None = typer.Option(None, help="Metadata key to remove; repeat for multiple keys"),
    update_metadata: str | None = typer.Option(None, help="JSON metadata to update"),
    visibility: RepoVisibility | None = None,
    output: Output = Output.rich,
):
    """Update description, discovery metadata, or visibility. Use --description '' to clear."""
    result = Client().modify_iceberg_namespace(
        org,
        name,
        description=description,
        add_metadata=_json_object(add_metadata, "--add-metadata"),
        remove_metadata=remove_metadata,
        update_metadata=_json_object(update_metadata, "--update-metadata"),
        visibility=visibility,
    )
    _show(result.model_dump(mode="json"), output)


@namespace_app.command("delete")
def delete_namespace(
    org: str,
    name: str,
    confirm: bool = typer.Option(False, "--confirm", help="Skip the confirmation prompt"),
    immediate: bool = typer.Option(
        False, "--immediate", help="Skip the recovery period: the namespace cannot be restored and its name is reusable at once"
    ),
    retain_data: bool = typer.Option(False, "--retain-data", help="Leave the bytes under the namespace's storage prefix in the bucket"),
):
    """Delete an empty namespace. A soft-delete by default: restore it during its recovery period."""
    if not confirm:
        verb = "Permanently delete" if immediate else "Delete"
        typer.confirm(f"{verb} namespace {org}/{name}?", abort=True)
    Client().delete_iceberg_namespace(org, name, imsure=True, immediate=immediate, retain_data=retain_data)
    typer.echo(f"Deleted {org}/{name}")


@namespace_app.command("restore")
def restore_namespace(org: str, name: str):
    """Restore a soft-deleted namespace."""
    Client().restore_iceberg_namespace(org, name)
    typer.echo(f"Restored {org}/{name}")


@table_app.command("list")
def list_tables(
    org: str,
    namespace: str,
    search: str | None = None,
    sort: TableSort | None = None,
    direction: Direction = Direction.desc,
    page_size: int = typer.Option(50, min=1, max=100),
    output: Output = Output.rich,
):
    """List table summaries without fetching table metadata or recording accesses."""
    rows = Client().list_iceberg_tables_paginated(
        org,
        namespace,
        search=search,
        sort=sort.value if sort else None,
        direction=direction.value,
        page_size=page_size,
    )
    _show_list([row.model_dump(mode="json") for row in rows], output, namespaces=False)


@table_app.command("describe")
def describe_table(
    org: str,
    identifier: str = typer.Argument(..., help="NAMESPACE.TABLE; double-quote components containing dots or special characters."),
    output: Output = Output.rich,
):
    """Load a table's schema, snapshots, partitioning, and properties. Requires arraylake[iceberg]."""
    namespace, table = _parse_table_identifier(identifier)
    catalog = Client().get_iceberg(org)
    try:
        loaded = catalog.load_table((namespace, table))
        _show(
            {
                "name": table,
                "namespace": namespace,
                "identifier": _table_identifier(namespace, table),
                "metadata_location": loaded.metadata_location,
                "metadata": loaded.metadata.model_dump(mode="json", by_alias=True),
            },
            output,
        )
    finally:
        catalog.close()
