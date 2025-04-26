import rich.markup
import rich_click as click
from rich.console import Console

from union._config import _DEFAULT_DOMAIN, _DEFAULT_PROJECT_BYOC


@click.group()
def start():
    """Start a resource."""


@start.command()
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
    console.print(f"Starting workspace '{name}'")
    with console.status("Provisioning workspace", spinner="dots"):
        try:
            response = run_sync(ws_remote.start_workspace_instance, workspace_definition_name=name)
        except Exception as exc:
            error_msg = exc.details() if hasattr(exc, "details") else str(exc)
            console.print(f"Error provisioning workspace: {rich.markup.escape(error_msg)}", style="red")
            raise exc

    url = f"https://{remote.config.platform.endpoint}/{response.workspace_instance.spec.uri}"
    loading_url = f"https://{remote.config.platform.endpoint}/loading?type=workspace&url={url}"
    console.print(f"\n🚀 Workspace started: [link={loading_url}]Open VSCode in Browser[/link]")
