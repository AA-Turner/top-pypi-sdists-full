import typing as t
import urllib.parse
from dataclasses import asdict
from io import StringIO
from pathlib import Path

import click
from ruamel.yaml import YAML

import tobikodata.tcloud.constants as c
from tobikodata.tcloud.config import TCloudProject, load_project_configs, save_project_config


@click.group()
def project() -> None:
    """
    Tobiko Cloud Project Configuration
    """
    pass


@project.command(name="list")
def list_cmd() -> None:
    """List all projects"""
    yaml = YAML()
    yaml.indent(mapping=2, sequence=2)
    configs, default_project = load_project_configs()
    if not configs:
        click.secho("No projects found", fg="yellow")
    for project_name, project_config in (configs or {}).items():
        is_default = project_name == default_project
        output_stream = StringIO()
        yaml.dump(
            {
                project_name + (" (default)" if is_default else ""): {
                    k: v for k, v in asdict(project_config).items() if v
                }
            },
            output_stream,
        )
        click.echo(output_stream.getvalue())


@project.command()
@click.option(
    "--account",
    prompt="Account Name",
    help="The name of the account (shared by each of your projects)",
)
@click.option("--project", prompt="Project Name", help="The name of the project")
@click.option("--gateway", prompt="Gateway", help="The gateway to use for this project")
@click.option(
    "--extras",
    prompt="Extras (ex: bigquery,snowflake,redshift)",
    default="",
    required=False,
    show_default=False,
    help="Extra to install with sqlmesh (ex: bigquery,snowflake,redshift)",
)
@click.option(
    "--path",
    type=click.Path(dir_okay=False, writable=True, path_type=Path),
    required=False,
    help="Path to the project configuration file to save to. Defaults to ~/.tcloud/tcloud.yaml",
)
def add(
    account: str, project: str, gateway: str, extras: t.Optional[str], path: t.Optional[Path] = None
) -> None:
    """Add a new project"""

    def confirm() -> bool:
        click.secho("Please confirm the following:", bold=True, fg="cyan")
        click.secho(f"{'Account:':<15}{account}", fg="cyan")
        click.secho(f"{'Project:':<15}{project}", fg="cyan")
        click.secho(f"{'Gateway:':<15}{gateway}", fg="cyan")
        click.secho(f"{'Extras:':<15}" + (extras if extras else "No extras"), fg="cyan")
        if token:
            click.secho(f"{'Token:':<15}{token}" if token else "Using SSO", fg="cyan")
        else:
            click.secho(f"{'Using SSO:':<15}Yes", fg="cyan")
        click.secho(f"{'Is Default:':<15}" + ("Yes" if is_default else "No"), fg="cyan")
        return click.confirm("Is this correct?")

    token = None
    if not click.confirm("Are you using Single Sign-On (SSO)?"):
        token = click.prompt("Token")
    is_default = click.confirm("Should this project be your default project?")
    if not confirm():
        click.secho("Aborted", fg="yellow")
        return
    url = f"https://cloud.tobikodata.com/sqlmesh/{urllib.parse.quote_plus(account)}/{urllib.parse.quote_plus(project)}"
    filepath = path or c.TCLOUD_PATH / "tcloud.yml"
    if not filepath.exists():
        filepath.touch()
    existing_config, existing_default = load_project_configs(paths=[filepath], ignore_env=True)
    existing_config = existing_config or {}
    default_project = project if is_default else existing_default
    if project in existing_config:
        click.secho(f"Project '{project}' already exists", fg="yellow")
        if not click.confirm("Do you want to overwrite it?"):
            click.secho("Aborted", fg="yellow")
            return
    existing_config[project] = TCloudProject(
        url=url, token=token, gateway=gateway, extras=extras.split(",") if extras else None
    )
    save_project_config(filepath, existing_config, default_project)
    click.secho(f"Project '{project}' configured. URL: {url}", fg="green")
