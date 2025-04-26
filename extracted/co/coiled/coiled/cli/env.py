from typing import Optional

import click
from dask import config
from rich.console import Console
from rich.table import Table

from coiled.exceptions import BuildError
from coiled.types import ArchitectureTypesEnum
from coiled.v2.core import setup_logging

from ..core import Cloud, create_software_environment, delete_software_environment
from ..utils import COILED_SERVER
from .utils import CONTEXT_SETTINGS

console = Console()


@click.group(context_settings=CONTEXT_SETTINGS)
def env():
    """Commands for managing Coiled software environments"""
    setup_logging()


@env.command(context_settings=CONTEXT_SETTINGS)
@click.option("-n", "--name", help="Name of software environment, it must be lowercase.")
@click.option("--container", default=None, help="Base docker image to use.")
@click.option(
    "--ignore-container-entrypoint",
    default=False,
    help="Ignore the ENTRYPOINT when using specified container.",
    is_flag=True,
)
@click.option(
    "--conda",
    default=None,
    help="Conda environment file.",
    type=click.Path(exists=True),
)
@click.option("--pip", default=None, help="Pip requirements file.", type=click.Path(exists=True))
@click.option(
    "--force-rebuild",
    default=False,
    help="Skip checks for an existing software environment build.",
    is_flag=True,
)
@click.option(
    "--account",
    "--workspace",
    default=None,
    type=str,
    help="Workspace to use for creating this software environment."
    " Note: --account is deprecated, please use --workspace instead.",
)
@click.option(
    "--gpu-enabled",
    is_flag=True,
    show_default=True,
    default=False,
    help="Set CUDA virtual package for Conda",
)
@click.option(
    "--arm",
    is_flag=True,
    default=False,
    show_default=True,
    help="Use ARM CPU architecture; takes precedence over ``--architecture`` option.",
)
@click.option(
    "--architecture",
    type=click.Choice([e.value for e in ArchitectureTypesEnum]),
    default=ArchitectureTypesEnum.X86_64.value,
    show_default=True,
    help="CPU architecture to use for the software environment",
)
@click.option(
    "--region-name",
    default=None,
    type=str,
    help="AWS or GCP region to use for storing this software environment.",
)
@click.option(
    "--include-local-code",
    default=False,
    is_flag=True,
    help="Include local code in the software environment build. "
    "This includes editable installs and importable python files.",
)
@click.option(
    "-i",
    "--ignore-local-package",
    multiple=True,
    help="Ignore a local package in the software environment build."
    " Only applies to packages included by the include-local-code option."
    " Specify multiple times for multiple packages."
    " Example: -i coiled -i pytorch",
)
@click.option(
    "--disable-uv-installer",
    default=False,
    is_flag=True,
    help="Do not use uv to install PyPI packages when building this environment.",
)
def create(
    name,
    container,
    ignore_container_entrypoint,
    conda,
    pip,
    force_rebuild,
    account,
    gpu_enabled,
    arm,
    architecture,
    region_name,
    include_local_code,
    disable_uv_installer,
    ignore_local_package,
):
    """Create a Coiled software environment"""
    try:
        create_software_environment(
            name=name,
            container=container,
            conda=conda,
            pip=pip,
            force_rebuild=force_rebuild,
            account=account,
            arm=arm,
            gpu_enabled=gpu_enabled,
            architecture=architecture,
            region_name=region_name,
            include_local_code=include_local_code,
            ignore_local_packages=ignore_local_package,
            use_uv_installer=not disable_uv_installer,
            use_entrypoint=not ignore_container_entrypoint,
        )
    except BuildError as e:
        raise click.ClickException(f"{e}") from e


@env.command(context_settings=CONTEXT_SETTINGS)
@click.argument("name")
@click.option(
    "--workspace", default=None, required=False, help="Coiled workspace (uses default workspace if not specified)."
)
def delete(name: str, workspace: Optional[str]):
    """Delete a Coiled software environment"""
    delete_software_environment(name, workspace=workspace)


@env.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--workspace", default=None, required=False, help="Coiled workspace (uses default workspace if not specified)."
)
def list(workspace: str):
    """List the Coiled software environments in a workspace"""
    with Cloud(workspace=workspace) as cloud:
        environments = cloud.list_software_environments(
            workspace,
        )
        table = Table(title="Software Environments")
        table.add_column("Name", style="cyan")
        table.add_column("Updated", style="magenta")
        table.add_column("Link", style="magenta")
        table.add_column("Status", style="green")
        server = config.get("coiled.server", COILED_SERVER).replace("8000", "5173")
        account = workspace or config.get("coiled.workspace", config.get("coiled.account"))
        for env_name, env_details in environments.items():
            latest_build = env_details["latest_spec"].get("latest_build")
            if latest_build:
                build_status = latest_build["state"] if latest_build["state"] != "error" else "[red]error[/red]"
                env_url = f"{server}/software/alias/{env_details['id']}/build/{latest_build['id']}?account={account}"
            else:
                build_status = "n/a"
                env_url = f"{server}/software/alias/{env_details['id']}?account={account}"
            table.add_row(
                env_name,
                env_details["updated"],
                env_url,
                build_status,
            )
        console.print(table)


@env.command(
    context_settings=CONTEXT_SETTINGS,
    help="View the details of a Coiled software environment",
)
@click.argument("name")
def inspect(name: str):
    """View the details of a Coiled software environment

    Parameters
    ----------
    name
        Identifier of the software environment to use, in the format (<account>/)<name>. If the software environment
        is owned by the same account as that passed into "account", the (<account>/) prefix is optional.

        For example, suppose your account is "wondercorp", but your friends at "friendlycorp" have an environment
        named "xgboost" that you want to use; you can specify this with "friendlycorp/xgboost". If you simply
        entered "xgboost", this is shorthand for "wondercorp/xgboost".

        The "name" portion of (<account>/)<name> can only contain ASCII letters, hyphens and underscores.

    Examples
    --------
    >>> import coiled
    >>> coiled.inspect("coiled/default")

    """
    with Cloud() as cloud:
        results = cloud.get_software_info(name)
        console.print(results)
