from typing import Optional

import rich_click as click
from click import secho, style
from flytekit.clis.sdk_in_container.constants import CTX_VERBOSE
from flytekit.models.task import Resources
from rich.console import Console
from rich.table import Table

from union._config import _DEFAULT_DOMAIN, _DEFAULT_PROJECT_BYOC
from union.internal.common.list_pb2 import ListRequest
from union.internal.identity.app_payload_pb2 import ListAppsRequest
from union.internal.secret.definition_pb2 import SecretType
from union.internal.secret.payload_pb2 import ListSecretsRequest
from union.remote import UnionRemote


@click.group()
def get():
    """Get a resource."""


@get.command()
@click.option("--project", help="Project name")
@click.option("--domain", help="Domain name")
def secret(
    project: Optional[str],
    domain: Optional[str],
):
    """Get secrets."""
    remote = UnionRemote(default_project=project, default_domain=domain)
    stub = remote.secret_client
    secrets = []

    per_cluster_tokens, has_next = None, True

    try:
        while has_next:
            request = ListSecretsRequest(domain=domain, project=project, limit=20)
            if per_cluster_tokens:
                request.per_cluster_tokens.update(per_cluster_tokens)
            response = stub.ListSecrets(request)
            per_cluster_tokens = response.per_cluster_tokens
            has_next = any(v for _, v in per_cluster_tokens.items() if v)

            secrets.extend(response.secrets)
    except Exception as e:
        raise click.ClickException(f"Unable to get secrets.\n{e}") from e

    if secrets:
        table = Table()
        for name in ["name", "project", "domain", "type"]:
            table.add_column(name, justify="right")

        for secret in secrets:
            project = secret.id.project or "-"
            domain = secret.id.domain or "-"
            table.add_row(
                secret.id.name,
                project,
                domain,
                SecretType.Name(secret.secret_metadata.type).replace("SECRET_TYPE_", ""),
            )

        console = Console()
        console.print(table)
    else:
        click.echo("No secrets found")


@get.group("api-key")
def api_key():
    """Manage API keys."""


@api_key.command("admin")
def admin():
    """Show existing API keys for admin."""
    remote = UnionRemote()
    stub = remote.apps_service_client

    apps = []
    next_token, has_next = "", True
    try:
        while has_next:
            request = ListAppsRequest(request=ListRequest(limit=20, token=next_token))
            response = stub.List(request)
            next_token = response.token
            has_next = next_token != ""

            apps.extend(response.apps)
    except Exception as e:
        raise click.ClickException(f"Unable to get apps.\n{e}") from e

    if apps:
        table = Table()
        table.add_column("name", overflow="fold")

        for app in apps:
            table.add_row(app.client_id)

        console = Console()
        console.print(table)
    else:
        click.echo("No apps found.")


@get.command()
@click.pass_context
@click.option("--name", default=None)
@click.option("--project", default=_DEFAULT_PROJECT_BYOC, help="Project name")
@click.option("--domain", default=_DEFAULT_DOMAIN, help="Domain name")
def apps(ctx: click.Context, name: Optional[str], project: str, domain: str):
    """Get apps."""
    verbose_on = ctx.obj[CTX_VERBOSE] > 0

    remote = UnionRemote(default_project=project, default_domain=domain)
    app_remote = remote._app_remote

    if name is None:
        # TODO: Add filter
        app_list = app_remote.list()
        if verbose_on:
            secho(app_list)
            return

        if not app_list:
            secho("No applications running")
            return

        table = Table()
        table.add_column("Name", overflow="fold")
        table.add_column("Link", overflow="fold")
        table.add_column("Status", overflow="fold")
        table.add_column("Desired State", overflow="fold")
        table.add_column("Message", overflow="fold")
        table.add_column("CPU", overflow="fold")
        table.add_column("Memory", overflow="fold")

        table_items = []

        for app in app_list:
            url = f"[link={app.status.ingress.public_url}]Click Here[/link]"
            limits = app_remote.get_limits(app)

            status = app_remote.deployment_status(app)
            desired_state = app_remote.desired_state(app)
            message = app_remote.get_message(app)

            table_items.append(
                {
                    "name": app.metadata.id.name,
                    "url": url,
                    "status": status,
                    "desired_state": desired_state,
                    "message": message,
                    "cpu": limits.get("cpu", "-"),
                    "memory": limits.get("memory", "-"),
                }
            )

        sorted_table_items = sorted(table_items, key=lambda item: item["status"])

        for item in sorted_table_items:
            table.add_row(
                item["name"],
                item["url"],
                item["status"],
                item["desired_state"],
                item["message"],
                item["cpu"],
                item["memory"],
            )

        console = Console()
        console.print(table)
    else:
        app_idl = app_remote.get(name=name)
        if verbose_on:
            secho(app_idl)
        else:
            limits = app_remote.get_limits(app_idl)
            details = {
                "name": app_idl.metadata.id.name,
                "status": app_remote.deployment_status(app_idl),
                "link": app_idl.status.ingress.public_url,
                "desired_state": app_remote.desired_state(app_idl),
                "message": app_remote.get_message(app_idl),
                "cpu": limits.get("cpu", "-"),
                "memory": limits.get("memory", "-"),
            }
            items = ["name", "link", "status", "message", "cpu", "memory", "desired_state"]
            max_item_len = max(len(i) for i in items)

            for item in items:
                styled_name = style(f"{item:<{max_item_len}}", bold=True)
                value = details[item]
                secho(f"{styled_name} : {value}")


@get.command()
@click.pass_context
@click.option("--name", default=None)
@click.option("--project", default=_DEFAULT_PROJECT_BYOC, help="Project name")
@click.option("--domain", default=_DEFAULT_DOMAIN, help="Domain name")
@click.option("--show-details", default=False, is_flag=True, help="Show additional details")
def workspace(ctx: click.Context, name: Optional[str], project: str, domain: str, show_details: bool):
    """Get workspaces."""

    from union._async import run_sync
    from union.internal.workspace.workspace_definition_payload_pb2 import ListWorkspaceDefinitionsResponse
    from union.workspace._vscode_remote import WorkspaceRemote

    remote = UnionRemote(default_domain=domain, default_project=project)
    ws_remote = WorkspaceRemote(default_domain=domain, default_project=project, union_remote=remote)

    ws_defs: ListWorkspaceDefinitionsResponse = run_sync(
        ws_remote.list_workspace_definitions,
        name,
        sort_by="created_at",
        direction="desc",
    )
    if len(ws_defs.workspace_definitions) == 0:
        click.echo("No workspaces found.")
        return

    table = Table(header_style="yellow", border_style="yellow")
    table.add_column("Workspace name", overflow="fold")
    table.add_column("CPU", overflow="fold")
    table.add_column("Memory", overflow="fold")
    table.add_column("GPU", overflow="fold")
    table.add_column("Accelerator", overflow="fold")
    table.add_column("TTL Seconds", overflow="fold")
    table.add_column("Active URL", overflow="fold", style="green")

    workspace_names = set()
    for ws_def in ws_defs.workspace_definitions:
        if ws_def.id.name in workspace_names:
            continue

        workspace_names.add(ws_def.id.name)
        try:
            uri = run_sync(ws_remote.get_latest_workspace_instance_uri, ws_def.id.name, ws_def.id.version)
            if uri is None:
                loading_url = None
            else:
                url = f"https://{remote.config.platform.endpoint}/{uri}"
                loading_url = f"https://{remote.config.platform.endpoint}/loading?type=workspace&url={url}"
        except RuntimeError:
            loading_url = None

        cpu, memory, gpu = None, None, None
        resources = Resources.from_flyte_idl(ws_def.spec.resources)
        for i in range(len(resources.requests)):
            name = resources.requests[i].name
            value = resources.requests[i].value

            if name == Resources.ResourceName.CPU:
                cpu = value
            elif name == Resources.ResourceName.MEMORY:
                memory = value
            elif name == Resources.ResourceName.GPU:
                gpu = value

        table.add_row(
            ws_def.id.name,
            cpu or "-",
            memory or "-",
            gpu or "-",
            str(ws_def.spec.extended_resources.gpu_accelerator) or "-",
            str(ws_def.spec.ttl_seconds),
            f"[link={loading_url}]Open in Browser[/link]" if loading_url else "-",
        )

    console = Console()
    console.print(table)


@get.command()
@click.argument("uri", metavar="URI of the type flyte://av0/...")
@click.pass_context
def artifact(ctx: click.Context, uri: str):
    """Get artifacts."""
    remote = UnionRemote()
    art = remote.get_artifact(uri=uri)
    url = remote.generate_console_url(art)
    Console().print(
        f"[green]Artifact: [bold][link={url}]{art.name}[/link][/bold]"
        f" and Artifact ID: [bold]{art.metadata().uri}[/bold][/green]"
    )
