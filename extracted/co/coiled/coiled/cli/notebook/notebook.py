from __future__ import annotations

import asyncio
import logging
import signal
import subprocess
from pathlib import Path
from typing import List, Sequence, Union
from webbrowser import open as open_webbrowser

import click
import importlib_metadata
from packaging.version import Version
from rich import print
from rich.control import Control
from rich.prompt import Confirm
from rich.segment import ControlType
from urllib3.util import parse_url

import coiled
from coiled.cli.cluster.ssh import check_ssh_agent
from coiled.compatibility import DISTRIBUTED_VERSION
from coiled.errors import DoesNotExist
from coiled.software_utils import make_coiled_local_name
from coiled.utils import dict_from_key_val_list, error_info_for_tracking

from ...utils import unset_single_thread_defaults
from ...v2.widgets.rich import LightRichClusterWidget
from ..sync import (
    MUTAGEN_NAME_FORMAT,
    can_use_mutagen,
    connect_mutagen_sync,
    get_mutagen_path,
    mutagen_session_exists,
    start_sync,
    stop_sync,
)
from ..utils import CONTEXT_SETTINGS

# Path on VM to sync to.
# We use `/scratch` for now because it's already bind-mounted into docker.
MIN_DISTRIBUTED_VERSION = Version("2022.8.1")


class NotebookError(Exception):
    pass


def check_distributed_version() -> bool:
    if DISTRIBUTED_VERSION < MIN_DISTRIBUTED_VERSION:
        print(
            "[bold red]"
            f"distributed>{MIN_DISTRIBUTED_VERSION} is required to launch notebooks. "
            f"You have {DISTRIBUTED_VERSION}."
            "[/]"
        )
        return False
    return True


def check_jupyter() -> bool:
    try:
        importlib_metadata.distribution("jupyterlab")
    except ModuleNotFoundError:
        print("[bold red]Jupyterlab must be installed locally to launch notebooks.[/]")
        return False

    try:
        importlib_metadata.distribution("jupyter_server_proxy")
    except ModuleNotFoundError:
        print(
            "[bold red]jupyter-server-proxy is not installed, "
            "without this you won't be able to access Dask dashboard for local clusters created on notebook server.[/]"
        )

    return True


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--name",
    default=None,
    help="Cluster name. If not given, defaults to a hash based on current working directory.",
)
@click.option(
    "--account",
    "--workspace",
    default=None,
    help="Coiled workspace (uses default workspace if not specified)."
    " Note: --account is deprecated, please use --workspace instead.",
)
@click.option(
    "--sync",
    default=False,
    is_flag=True,
    help="Sync the working directory with the filesystem on the notebook. Requires mutagen.",
)
@click.option(
    "--allow-sync-from",
    default="me",
    type=str,
    help=(
        "IP address or CIDR from which connections to port 22 (SSH) are open; "
        "can also be specified as 'everyone' (0.0.0.0/0) or 'me' (automatically determines public IP detected "
        "for your local client). Note that `--sync` relies on SSH connection."
    ),
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
@click.option("--cpu", default=None, type=int, help="Number of CPUs requested for this notebook.")
@click.option(
    "--memory",
    default=None,
    help="Amount of memory for this notebook, Coiled will use a +/-10% buffer from the memory you specify.",
)
@click.option(
    "--gpu",
    default=False,
    is_flag=True,
    help="Use GPU notebook server.",
)
@click.option(
    "--disk-size",
    default=None,
    help="Use larger-than-default disk on VM, specified in GiB.",
)
@click.option(
    "--region",
    default=None,
    help="The cloud provider region in which to run the notebook.",
)
@click.option(
    "--open",
    default=True,
    is_flag=True,
    help="Whether to open the notebook in the default browser once it's launched.",
)
@click.option(
    "--block/--no-block",
    default=True,
    is_flag=True,
    help="Whether to block while the notebook is running.",
)
@click.option(
    "--include-vcs",
    default=False,
    is_flag=True,
    help="Include version control files when syncing (e.g., `.git`).",
)
@click.option(
    "--idle-timeout",
    default="4 hours",
    help="Period of idleness after which to automatically shut down the notebook, "
    "e.g. '20 minutes' or '1 hour' or '10 days' (default is '4 hours'). "
    "The notebook is considered active (not idle) if a browser is connected, "
    "even if no code is running.",
)
@click.option(
    "--allow-ingress-from",
    default=None,
    help="Control the CIDR from which cluster firewall allows ingress to scheduler; "
    "by default this is open to any source address (0.0.0.0/0). You can specify "
    "CIDR, or 'me' for just your IP address.",
)
@click.option(
    "--env",
    "-e",
    default=[],
    multiple=True,
    help=(
        "Environment variables securely transmitted to run command environment. "
        "Format is ``KEY=val``, multiple vars can be set with separate ``--env`` for each."
    ),
)
@click.option(
    "--tag",
    "-t",
    default=[],
    multiple=True,
    help="Tags. Format is ``KEY=val``, multiple vars can be set with separate ``--tag`` for each.",
)
@click.option(
    "--sync-ignore",
    default=None,
    multiple=True,
    help="Paths to not sync when using ``--sync``.",
)
@click.option(
    "--mount-bucket",
    default=None,
    multiple=True,
    help="S3 or GCS bucket(s) to mount as volumes.",
)
@click.option(
    "--host-setup-script",
    default=None,
    help="Path to local script which will be run on each VM during setup process.",
)
@click.option(
    "--resumable",
    default=False,
    is_flag=True,
    help=(
        "Allow pausing and resuming your notebook sessions. "
        "There may be cloud costs associated with leaving a session paused."
    ),
    hidden=True,
)
def start_notebook(
    name: str | None,
    account: str | None,
    sync: bool,
    allow_sync_from: str,
    software: str | None,
    container: str | None,
    vm_type: Sequence[str],
    cpu: Union[int, None],
    memory: Union[str, None],
    gpu: bool,
    disk_size: int | None,
    region: str | None,
    open: bool,
    block: bool,
    include_vcs: bool,
    idle_timeout: str,
    allow_ingress_from: str | None,
    env: List[str] | None,
    tag: List[str] | None,
    sync_ignore: List[str] | None,
    mount_bucket: List[str] | None,
    host_setup_script: str | None,
    resumable: bool = False,
):
    """
    Launch or re-open a notebook session, with optional file syncing.

    If a notebook session with the same ``name`` already exists, it's not re-created.
    If file sync was initially not enabled, running ``coiled notebook start --sync``
    will begin file sync without re-launching the notebook.
    """
    _start_notebook(
        name=name,
        workspace=account,
        sync=sync,
        allow_sync_from=allow_sync_from,
        software=software,
        container=container,
        vm_type=vm_type,
        cpu=cpu,
        memory=memory,
        gpu=gpu,
        disk_size=disk_size,
        region=region,
        open=open,
        block=block,
        include_vcs=include_vcs,
        idle_timeout=idle_timeout,
        allow_ingress_from=allow_ingress_from,
        env=env,
        tag=tag,
        sync_ignore=sync_ignore,
        mount_bucket=mount_bucket,
        host_setup_script=host_setup_script,
        resumable=resumable,
    )


def _start_notebook(
    *,
    name: str | None = None,
    workspace: str | None = None,
    sync: bool = False,
    allow_sync_from: str = "me",
    software: str | None = None,
    container: str | None = None,
    vm_type: Sequence[str] = [],
    cpu: Union[int, None] = None,
    memory: Union[str, None] = None,
    gpu: bool = False,
    disk_size: int | None = None,
    region: str | None = None,
    open: bool = False,
    block: bool = True,
    include_vcs: bool = False,
    idle_timeout: str = "4 hours",
    debug: bool = False,
    allow_ingress_from: str | None = None,
    env: List[str] | None = None,
    tag: List[str] | None = None,
    sync_ignore: List[str] | None = None,
    mount_bucket: List[str] | None = None,
    host_setup_script: str | None = None,
    resumable: bool = False,
) -> coiled.Cluster | None:
    """
    Launch or re-open a notebook session, with optional file syncing.

    If a notebook session with the same ``name`` already exists, it's not re-created.
    If file sync was initially not enabled, running ``coiled notebook start --sync``
    will begin file sync without re-launching the notebook.
    """
    info = {"vm_type": vm_type, "sync": sync, "block": block, "include_vcs": include_vcs}
    success = True
    exception = None

    runtime_env_dict = dict_from_key_val_list(env)
    tags = dict_from_key_val_list(tag)

    try:
        # when using package sync, check that local env has jupyter and recent distributed
        if not software and not container:
            if not check_distributed_version():
                raise NotebookError("distributed version check")
            if not check_jupyter():
                raise NotebookError("jupyter missing")

        if sync and not can_use_mutagen():
            return

        if sync and not check_ssh_agent():
            print("Sync may be unable to start but we'll try anyway...")
            info["problem"] = "check_ssh_agent failed"

        initial_env = {}
        if container and "rapidsai" in container:
            initial_env["DISABLE_JUPYTER"] = "true"  # needed for "stable" RAPIDS image

        name = name or f"notebook-{coiled.utils.short_random_string()}"
        with (
            LightRichClusterWidget(
                workspace=workspace,
                title=f"Notebook [bold]{name}[/bold]...",
                extra_link_title="Jupyter",
                extra_link="...",
                width=84,
            ) as widget,
            coiled.Cloud(workspace=workspace) as cloud,
        ):
            workspace = workspace or cloud.default_workspace
            info["workspace"] = workspace
            widget.update(
                server=cloud.server,
                cluster_details=None,
                logs=None,
                workspace=workspace,
                extra_link="...",
            )
            try:
                package_sync_ignore = [make_coiled_local_name(Path.cwd().resolve().name)]
            except FileNotFoundError:
                package_sync_ignore = []

            cluster = coiled.Cluster(
                name=name,
                workspace=workspace,
                cloud=cloud,
                n_workers=0,
                software=software,
                container=container,
                jupyter=True,
                scheduler_options={"idle_timeout": idle_timeout},
                scheduler_vm_types=list(vm_type) if vm_type else None,
                worker_vm_types=list(vm_type) if vm_type else None,
                scheduler_cpu=cpu,
                scheduler_memory=memory,
                scheduler_disk_size=disk_size,
                allow_ssh_from=allow_sync_from,
                environ=initial_env,
                scheduler_gpu=gpu,
                region=region,
                tags={**tags, "coiled-cluster-type": "notebook"},
                custom_widget=widget,
                package_sync_ignore=package_sync_ignore,
                allow_ingress_from=allow_ingress_from,
                mount_bucket=mount_bucket,
                host_setup_script=host_setup_script,
                shutdown_on_close=False,
                unset_single_threading_variables=True,
                pause_on_exit=resumable,
            )
            info["cluster_id"] = cluster.cluster_id

            url = cluster.jupyter_link
            cluster_id = cluster.cluster_id
            assert cluster_id is not None

            # by default, jupyter on the scheduler gives us client to that very scheduler
            # clear ENV var so default `Client()` on notebook gives us a new local cluster
            cluster.unset_env_vars(["DASK_SCHEDULER_ADDRESS"])

            # some env vars are set in dask config early in the dask loading process
            # we set these to `""` since that's what we can do in the relevant dask config
            # but some libraries don't accept empty string, so we'll unset them here.
            # this won't affect things loaded by dask, but should affect user-code.
            cluster.unset_env_vars(unset_single_thread_defaults().keys())

            if runtime_env_dict:
                cluster.send_private_envs(runtime_env_dict)

            if sync:
                url = parse_url(url)._replace(path="/jupyter/lab/tree/synced").url

            widget.update(
                cluster_details=None,
                logs=None,
                extra_link=url,
            )

            if sync:
                connected, error_message = connect_mutagen_sync(
                    cloud,
                    cluster_id,
                    widget.live.console,
                    include_vcs=include_vcs,
                    debug=debug,
                    ignores=sync_ignore,
                )
                if not connected:
                    widget.stop()
                    print(
                        "[red]Unable to start sync, see error shown above for more details.[/red]\n"
                        "If sync is not required, you can start notebook without [green]--sync[/green]."
                    )

                    cluster._queue_cluster_event(
                        "notebook", f"error attempting to connect sync:\n{error_message}", level=logging.ERROR
                    )

                    _stop_notebook(name=name, workspace=workspace, cluster_id=cluster_id)

                    # close the cluster object so we comms close cleanly (and don't print error)
                    cluster.close(reason="The notebook sync failed to start")
                    raise NotebookError(f"unable to start sync: {error_message}")

            if open:
                open_webbrowser(url, new=2)

            if block:
                action = "pause" if resumable else "stop"
                widget.update(
                    cluster_details=None,
                    logs=None,
                    trailer=f"Use Control-C to {action} this notebook server",
                )

                def signal_handler_noop(_, frame):
                    # Ignore the input signal
                    return

                async def update_widget():
                    while True:
                        cluster_details = await cloud._get_cluster_details(cluster_id=cluster_id, workspace=workspace)
                        widget.update(cluster_details, logs=None)
                        # don't make user hit control-c if the cluster been stopped another way
                        if cluster_details["scheduler"]["current_state"]["state"] in ("error", "stopped"):
                            return False
                        await asyncio.sleep(1.0)

                while True:
                    try:
                        if not cluster.sync(update_widget):
                            widget.stop()
                            break
                    except KeyboardInterrupt:
                        widget.stop()
                        try:
                            exit = Confirm.ask(f"Are you sure you want to {action} this notebook server?", default=True)
                        except KeyboardInterrupt:
                            exit = True
                        if exit:
                            # Register noop handler since we're shutting down and
                            # want to make sure the notebook is shutdown even when
                            # hammering ctrl-C
                            signal.signal(signal.SIGINT, signal_handler_noop)
                            break
                        else:
                            # write over the prompt
                            print(Control.move(0, -1), Control((ControlType.ERASE_IN_LINE, 2)))
                            print("[green]Continuing with this notebook server... [/]")

                            # move cursor to bottom of widget so widget won't shift
                            print(Control.move(0, -2))
                            widget.start()

                if resumable:
                    _pause_notebook(name=name, workspace=workspace, cluster_id=cluster_id)
                else:
                    _stop_notebook(name=name, workspace=workspace, cluster_id=cluster_id)

                # close the cluster object so we comms close cleanly (and don't print error)
                cluster.close()
            else:
                valid_actions = ("pause", "stop") if resumable else ("stop",)
                for action in valid_actions:
                    action_command = f"coiled notebook {action}"
                    if workspace:
                        action_command = f"{action_command} --workspace {workspace}"
                    action_command = f"{action_command} {name}"

                    print(f"To {action} this notebook server: [green]{action_command}[/]")
        return cluster
    except NotebookError as e:
        success = False
        exception = e
        # don't raise, we've already printed appropriate message about the issue
    except Exception as e:
        success = False
        exception = e
        raise e
    finally:
        coiled.add_interaction(
            "coiled-notebook",
            success=success,
            **info,
            **error_info_for_tracking(exception),
        )


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("name")
@click.option(
    "--account",
    "--workspace",
    default=None,
    help="Coiled workspace (uses default workspace if not specified)."
    " Note: --account is deprecated, please use --workspace instead.",
)
def stop_notebook(name: str, account: str | None):
    """
    Shut down a notebook session
    """
    _stop_notebook(name=name, workspace=account)


def _stop_notebook(name: str, workspace: str | None, cluster_id: int | None = None):
    with coiled.Cloud(workspace=workspace) as cloud:
        notebook_running = True
        try:
            cluster_id = cloud.get_cluster_by_name(name, include_paused=True)
        except DoesNotExist:
            print(f"[bold red]There is no running notebook named {name!r}[/]")
            notebook_running = False

        stop_sync(cloud, cluster_id, f"Stopping sync with notebook {name!r} ({cluster_id})")

        if cluster_id and notebook_running:
            print(f"Stopping notebook {name!r} ({cluster_id})...")
            cloud.delete_cluster(cluster_id, workspace, reason="User requested notebook stop via CLI")


@click.command(context_settings=CONTEXT_SETTINGS, hidden=True)
@click.argument("name")
@click.option(
    "--account",
    "--workspace",
    default=None,
    help="Coiled workspace (uses default workspace if not specified)."
    " Note: --account is deprecated, please use --workspace instead.",
)
def pause_notebook(name: str, account: str | None):
    """
    Pause a notebook session
    """
    _pause_notebook(name=name, workspace=account)


def _pause_notebook(name: str, workspace: str | None, cluster_id: int | None = None):
    with coiled.Cloud(workspace=workspace) as cloud:
        notebook_running = True
        try:
            cluster_id = cloud.get_cluster_by_name(name, include_paused=True)
        except DoesNotExist:
            print(f"[bold red]There is no running notebook named {name!r}[/]")
            notebook_running = False

        stop_sync(cloud, cluster_id, f"Stopping sync with notebook {name!r} ({cluster_id})")

        if cluster_id and notebook_running:
            print(f"Pausing notebook {name!r} ({cluster_id})...")
            cloud.delete_cluster(cluster_id, workspace, reason="User requested notebook pause via CLI", pause=True)


@click.command(context_settings=CONTEXT_SETTINGS, hidden=True)
@click.argument("name")
@click.option(
    "--include-vcs",
    default=False,
    is_flag=True,
    help="Include version control files when syncing (e.g., `.git`).",
)
@click.option(
    "--debug",
    default=False,
    is_flag=True,
)
def start_standalone_sync(name: str, include_vcs: bool, debug: bool):
    error = None
    with coiled.Cloud() as cloud:
        try:
            cluster_id = cloud.get_cluster_by_name(name, include_paused=True)
            error = start_sync(cloud=cloud, cluster_id=cluster_id, include_vcs=include_vcs, debug=debug)
        except DoesNotExist:
            print(f"[bold red]Cluster {name!r} does not exist[/]")
            return

    coiled.add_interaction(
        "coiled-notebook-standalone-sync",
        success=not error,
        include_vcs=include_vcs,
    )


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("name")
def monitor_sync(name: str):
    """Monitor file sync status for a notebook session."""
    mutagen_path = get_mutagen_path()
    if not mutagen_path:
        return

    with coiled.Cloud() as cloud:
        try:
            cluster_id = cloud.get_cluster_by_name(name, include_paused=True)
        except DoesNotExist:
            print(f"[bold red]Cluster {name!r} does not exist[/]")
            return  # TODO exit 1

    if not mutagen_session_exists(cluster_id):
        print(f"[bold red]No file synchronization session for cluster {name!r} ({cluster_id})[/]")
        return  # TODO exit 1

    subprocess.run([mutagen_path, "sync", "monitor", MUTAGEN_NAME_FORMAT.format(cluster_id=cluster_id)])
