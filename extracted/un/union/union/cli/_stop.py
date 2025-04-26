import rich.markup
import rich_click as click
from rich.console import Console

from union._config import _DEFAULT_DOMAIN, _DEFAULT_PROJECT_BYOC
from union.remote import UnionRemote


@click.group()
def stop():
    """Stop a resource."""


@stop.command()
@click.option("--name", type=str, required=True)
@click.option("--project", default=_DEFAULT_PROJECT_BYOC, help="Project name")
@click.option("--domain", default=_DEFAULT_DOMAIN, help="Domain name")
def apps(name: str, project: str, domain: str):
    app_remote = UnionRemote(default_domain=domain, default_project=project)
    app_remote.stop_app(name=name)


@stop.command()
@click.option("--name", type=str, required=True)
@click.option("--project", default=_DEFAULT_PROJECT_BYOC, help="Project name")
@click.option("--domain", default=_DEFAULT_DOMAIN, help="Domain name")
def workspace(name: str, project: str, domain: str):
    from union._async import run_sync
    from union.configuration import UnionAIPlugin
    from union.workspace._vscode_remote import WorkspaceRemote

    remote = UnionAIPlugin.get_remote(config=None, project=project, domain=domain)
    ws_remote = WorkspaceRemote(default_project=project, default_domain=domain, union_remote=remote)
    console = Console()
    try:
        response = run_sync(ws_remote.stop_workspace_instance, workspace_definition_name=name)
    except Exception as exc:
        error_msg = exc.details() if hasattr(exc, "details") else str(exc)
        console.print(rich.markup.escape(f"Error stopping workspace instance '{name}': {error_msg}"), style="red")
        raise exc
    else:
        console.print(f"Workspace instance stopped: {response}")
