import os
from typing import Optional, Sequence

import click
import dask.config
from rich import print

import coiled

from .run import start_run
from .utils import CONTEXT_SETTINGS


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--cluster-name",
    default=None,
    help="Name of Coiled cluster",
)
@click.option(
    "--account",
    "--workspace",
    default=None,
    help="Coiled workspace (uses default workspace if not specified)."
    " Note: --account is deprecated, please use --workspace instead.",
)
@click.option(
    "--software",
    default=None,
    help=(
        "Software environment name to use. If neither software nor container is specified, "
        "all the currently-installed Python packages are replicated on the VM using package sync."
    ),
)
@click.option(
    "--container",
    default=None,
    help=(
        "Container image to use. If neither software nor container is specified, "
        "all the currently-installed Python packages are replicated on the VM using package sync."
    ),
)
@click.option(
    "--vm-type",
    default=[],
    multiple=True,
    help="VM type to use. Specify multiple times to provide multiple options.",
)
@click.option(
    "--gpu",
    default=False,
    is_flag=True,
    help="Have a GPU available.",
)
@click.option(
    "--region",
    default=None,
    help="The cloud provider region in which to run the notebook.",
)
@click.option(
    "--disk-size",
    default=None,
    help="Use larger-than-default disk on VM, specified in GiB.",
)
@click.option(
    "--file",
    "-f",
    default=[],
    multiple=True,
    help="Local files required to run command.",
)
@click.option(
    "--env",
    "-e",
    default=[],
    multiple=True,
    help=(
        "Environment variables securely transmitted to prefect flow environment. "
        "Format is `KEY=val`, multiple vars can be set with separate `--env` for each."
    ),
)
@click.option(
    "--tag",
    "-t",
    default=[],
    multiple=True,
    help=("Tags. Format is `KEY=val`, multiple vars can be set with separate `--tag` for each."),
)
@click.argument("command", nargs=-1)
def serve(
    cluster_name: Optional[str],
    account: Optional[str],
    software: Optional[str],
    container: Optional[str],
    vm_type: Sequence[str],
    gpu: bool,
    region: Optional[str],
    disk_size: Optional[int],
    file,
    env,
    tag,
    command,
):
    """Start server for Prefect deployment (using ``my_flow.serve()`` API)"""
    try:
        from prefect.settings import load_current_profile  # type: ignore

        runtime_env_vars = [f"{key.name}={val}" for key, val in load_current_profile().settings.items()]
    except ImportError as e:
        print(f"Error importing prefect: {e}")
        return
    except Exception:
        print(
            "Error loading Prefect authentication from local profile. "
            "You may need to run [green]prefect cloud login[/green]."
        )
        return

    runtime_env_vars.append(f"DASK_COILED__TOKEN={dask.config.get('coiled.token')}")
    if account:
        runtime_env_vars.append(f"DASK_COILED__ACCOUNT={account}")

    # User-provided environment variables
    if env:
        runtime_env_vars.extend(env)
        # Forward environment variables to set in `@coiled.function`-decorated tasks
        runtime_env_vars.append(f"COILED_REUSE_ENVIRON_KEYS={','.join(i.split('=')[0] for i in env)}")

    if command[0] != "python":
        prefect_command = os.path.basename(command[0].replace(".py", ""))
    elif len(command) > 1 and command[1].endswith(".py"):
        prefect_command = os.path.basename(command[1].replace(".py", ""))
    else:
        prefect_command = ""

    cluster_name = cluster_name or f"prefect-{prefect_command}-{coiled.utils.short_random_string()}"
    info = start_run(
        command=command,
        cluster_type_tag="prefect/serve",
        detach=True,
        env=runtime_env_vars,
        tag=tag,
        file=file,
        interactive=False,
        skip_entrypoint=False,
        name=cluster_name,
        workspace=account,
        software=software,
        container=container,
        vm_type=vm_type,
        gpu=gpu,
        region=region,
        disk_size=disk_size,
    )
    print(f"To stop this Coiled VM, run\n  [green]coiled prefect stop {cluster_name}[/green]")
    return info["exit_code"]
