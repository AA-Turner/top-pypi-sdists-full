from __future__ import annotations

import datetime
import io
import json
import os
import pathlib
import shlex
import sys
from typing import Dict, List, Sequence, Union

import click
import dask.config
import fabric
import invoke
from dask.utils import parse_timedelta
from paramiko.ed25519key import Ed25519Key
from rich import print
from rich.console import Console
from urllib3.util import parse_url

import coiled
from coiled.credentials.google import send_application_default_credentials
from coiled.spans import span
from coiled.utils import (
    dict_from_key_val_list,
    error_info_for_tracking,
    short_random_string,
    unset_single_thread_defaults,
)
from coiled.v2.cluster import ClusterKwargs
from coiled.v2.widgets.rich import LightRichClusterWidget

from .sync import SYNC_TARGET, start_sync, stop_sync
from .utils import CONTEXT_SETTINGS

# This directory is used by shell scripts that wrap the user's command
# Note that this directory is also referenced in code that runs in our
# cloud_env image, so if it's changed here, that code should also be updated.
COMMAND_DIR = "/scratch/run"
FILE_TEMP_DIR = "/scratch/run-temp-files"

DEFAULT_DASK_CONTAINER = "tmp-dask-1"


class KeepaliveSession:
    def __init__(self, cluster, prefix="", monitor_proc_activity=False):
        self.cluster = cluster
        self.monitor_proc_activity = monitor_proc_activity
        rand_uuid = short_random_string()
        self.session_id = f"{prefix}-{rand_uuid}" if prefix else rand_uuid

    def __enter__(self):
        # keepalive session lets us use keepalive without dask client
        self.cluster._call_scheduler_comm(
            "coiled_add_keepalive_session", name=self.session_id, monitor_proc_activity=self.monitor_proc_activity
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cluster._call_scheduler_comm("coiled_end_keepalive_session", name=self.session_id)


def get_ssh_connection(cloud, cluster_id) -> fabric.connection.Connection:
    ssh_info = cloud.get_ssh_key(cluster_id=cluster_id)

    with io.StringIO(ssh_info["private_key"]) as f:
        pkey = Ed25519Key(file_obj=f)

    ssh_address = ssh_info["scheduler_address_to_use"]
    if not ssh_address:
        raise coiled.exceptions.CoiledException(
            f"Unable to connect to cluster (id={cluster_id}) because we don't have IP address for it."
        )

    connection = fabric.connection.Connection(ssh_address, user="ubuntu", connect_kwargs={"pkey": pkey})

    return connection


def write_via_ssh(connection, content, path, mode=None):
    with io.StringIO(content) as f:
        connection.put(f, path)
    if mode:
        connection.sftp().chmod(path, mode)


def write_files_into_container(connection, files: Dict[str, str]):
    make_remote_dir(connection, FILE_TEMP_DIR)
    temp_paths = {path: f"{FILE_TEMP_DIR}/{short_random_string()}-{path.split('/')[-1]}" for path in files.keys()}
    # write files to temporary (staging) directory inside /scratch, so they're accessible inside container
    for path, content in files.items():
        write_via_ssh(connection, content=content, path=temp_paths[path], mode=0o755)

    # run commands inside container to move files to desired path
    move_commands = []
    for path, temp_path in temp_paths.items():
        # direct path manipulation because this is linux path, not local os path
        path_dir = "/".join(path.split("/")[:-1])
        move_commands.append(f"mkdir -p {path_dir} && mv {temp_path} {path}")
    for command in move_commands:
        # use `bash -c ...` so that `~` in path expands to user home inside container
        connection.run(command_with_docker_exec(f"bash -c '{command}'"), hide=True, in_stream=False)


def upload_file(connection, f, specified_root=None) -> str:
    cwd = os.path.abspath(os.path.curdir)
    base = os.path.basename(f)
    is_under_cwd = os.path.commonpath((os.path.abspath(f), cwd)) == cwd

    if is_under_cwd:
        relative_to = os.path.curdir
    elif specified_root:
        relative_to = specified_root
    else:
        relative_to = None

    if relative_to:
        # For file that's inside cwd, keep the relative path.
        # Note that this could be different from how you specified the path, for example
        #   cwd=/foo/bar
        #   coiled run --file /foo/bar/nested/path.txt
        # file will be copied to /scratch/nested/path.txt
        # which is a little confusing, but means it's equivalent to
        #   coiled run --file ~/nested/path.txt
        # which does feel natural.

        # For file that's not inside cwd, keep path relative if the user specified a directory for upload.
        # For example, if user specified `--file /absolute/subdir/`, then preserve path structure relative
        # to `/absolute/subdir/`, so `/absolute/subdir/foo/bar.txt` would go to `/scratch/subdir/foo/bar.txt`.
        specified_path_dir = os.path.dirname(os.path.relpath(f, relative_to))
        remote_dir = f"/scratch/{specified_path_dir}/"
        make_remote_dir(connection, remote_dir)
    else:
        remote_dir = "/scratch/"

    connection.put(f, remote_dir)

    # we want path on Linux VM, which might not match os.path.join run client-side, so join path manually
    # remote_dir should already end in "/"
    return f"{remote_dir}{base}"


def run_via_ssh(
    cloud,
    cluster,
    info: dict,
    command: List[str],
    file: List[str],
    env: dict,
    skip_entrypoint: bool,
    interactive: bool,
    detach: bool,
    env_unset: Sequence[str] | None = None,
    workdir: str = "/scratch",
    as_root: bool = False,
    in_container_files: Dict[str, str] | None = None,
    console=None,
):
    console = console or Console()

    connection = get_ssh_connection(cloud, cluster.cluster_id)
    results = None

    original_command = shlex.join(command)
    callstack = [{"code": original_command, "relative_line": 0}]
    # Extract and upload files from `command`
    command = shlex.split(original_command)
    info["files-implicit"] = []  # implicit files are part of the command, e.g., `foo.py` in `coiled run python foo.py`
    for idx, implicit_file in enumerate(command):
        if os.path.exists(implicit_file) and os.path.isfile(implicit_file):
            info["files-implicit"].append(implicit_file)

            # this will preserve path structure relative to cwd
            # so `coiled run python ./subdir/foo.py` will go to `/scratch/subdir/foo.py`
            remote_path = upload_file(connection, implicit_file)

            # adjust command to reference path on VM
            command[idx] = remote_path

            # include code files in the "callstack"
            if implicit_file.endswith((".py", ".sh")):
                try:
                    with open(implicit_file) as f:
                        contents = f.read()
                    callstack.append({"code": contents, "filename": implicit_file})
                except Exception:
                    pass

    # Upload user-specified files too
    info["files-explicit"] = file

    files_to_upload = []
    for f in file:
        path = pathlib.Path(f)
        if not path.exists():
            raise FileNotFoundError(f"Cannot find specified file {f}")

        if path.is_file():
            files_to_upload.append({"f": path})
        elif path.is_dir():
            # for paths outside cwd, parent_dir is used as the root so that path structure from there is preserved
            parent_dir = pathlib.Path(path).parent
            for subfile in path.rglob("*"):
                if subfile.is_file():
                    files_to_upload.append({"f": subfile, "specified_root": parent_dir})

    if files_to_upload:
        console.print(
            f"Uploading {len(files_to_upload)} file{'s' if len(files_to_upload) > 1 else ''} "
            "from local machine to cloud VM..."
        )
    for i, file_to_upload in enumerate(files_to_upload):
        try:
            mb_size = file_to_upload["f"].stat().st_size / 1_000_000
            if mb_size > 1:
                console.print(f"  {file_to_upload['f']} is {mb_size:.2f}MiB, this may be slow to upload")
        except Exception:
            pass
        upload_file(connection, **file_to_upload)
        if i and (i % 20 == 0 or i + 1 == len(files_to_upload)):
            console.print(f"  {i + 1}/{len(files_to_upload)} files uploaded")

    if skip_entrypoint:
        entrypoint = ""
    else:
        entrypoint = get_entrypoint(connection, container_name=DEFAULT_DASK_CONTAINER)
        if "cloud-env" in entrypoint:
            # hack for cloud-env containers (e.g., package sync) currently required to avoid re-downloading senv
            # once container is suitably changed, we should just be able to use entrypoint like any other container
            entrypoint = "micromamba run -p /opt/coiled/env"

    command_string = shlex.join(command)
    if not interactive:
        command_string = wrap_command_for_logs_and_stdout(connection, command_string, original_command)

    container_command = command_with_docker_exec(
        command=command_string,
        interactive=interactive,
        detach=detach,
        env=env,
        env_unset=env_unset,
        as_root=as_root,
        workdir=workdir,
        entrypoint=entrypoint,
    )

    if in_container_files:
        write_files_into_container(connection, files=in_container_files)

    try:
        with (
            KeepaliveSession(cluster=cluster, prefix="ssh", monitor_proc_activity=detach),
            span(cluster, callstack=callstack),
        ):
            optional_kwargs = {"in_stream": False} if not interactive else {}
            results = connection.run(container_command, hide=not interactive, pty=interactive, **optional_kwargs)
    except invoke.exceptions.UnexpectedExit as e:
        results = str(e)
    except Exception as e:
        raise e

    return connection, container_command, results


def wrap_command_for_logs_and_stdout(
    connection: fabric.connection.Connection, command_string: str, original_command: str
):
    command_id = f"{datetime.datetime.now(tz=datetime.timezone.utc).isoformat()}_{coiled.utils.short_random_string()}"

    inner_command_path = f"{COMMAND_DIR}/{command_id}.sh"
    tee_command = f"{COMMAND_DIR}/{command_id}-tee.sh"

    make_remote_dir(connection, COMMAND_DIR)

    # write the user's command as a shell file
    write_via_ssh(connection, command_string, inner_command_path, mode=0o755)
    # wrapper file that calls user command, sending output to pseudo-tty and stdout (which goes into logs)
    escaped_original_command = original_command.replace('"', '"')
    tee_script = f"""
    echo "{escaped_original_command}\t{command_id}" >> {COMMAND_DIR}/list
    {inner_command_path} 2>&1 | tee -a /proc/1/fd/1
    """
    write_via_ssh(connection, tee_script, tee_command, mode=0o755)
    command_string = f"bash {tee_command}"

    return command_string


def command_with_docker_exec(
    command: str,
    *,
    container_name: str = DEFAULT_DASK_CONTAINER,
    interactive: bool = False,
    detach: bool = False,
    env: dict | None = None,
    env_unset: Sequence[str] | None = None,
    as_root: bool = False,
    workdir: str = "/scratch",
    entrypoint: str = "",
):
    env = env or {}

    container_user = "-u root" if as_root else ""
    docker_opts = "-it" if interactive else ""
    docker_opts = f"{docker_opts} --detach" if detach else docker_opts

    env_opts = " ".join(f"--env {key}={val}" for key, val in env.items()) if env else ""
    env_unset_opts = " ".join(f"--env {key}" for key in env_unset) if env_unset else ""

    return (
        f"docker exec {container_user} --workdir {workdir} {env_opts} {env_unset_opts} "
        f"{docker_opts} {container_name} {entrypoint} {command}"
    )


def check_explicit_files(files):
    for f in files:
        path = pathlib.Path(f)
        if not path.exists():
            raise FileNotFoundError(f"Cannot find specified file {f}")


def make_remote_dir(connection, dir):
    connection.run(f"mkdir -p {dir} && sudo chmod a+wrx {dir}", in_stream=False)


def get_entrypoint(connection, container_name) -> str:
    entrypoint = ""
    x = connection.run(
        f"docker inspect -f '{{{{json .Config.Entrypoint}}}}' {container_name}", hide=True, in_stream=False
    )
    if x.stdout:
        entrypoint = json.loads(x.stdout)

        if entrypoint:
            # hack so we don't use `tini` for each run, remove everything between `tini` and `--`
            # e.g., "tini -g -- /usr/bin/prepare.sh" -> "/usr/bin/prepare.sh"
            if "tini" in entrypoint[0]:
                if "--" in entrypoint:
                    after_tini = entrypoint.index("--")
                    entrypoint = entrypoint[after_tini + 1 :]

            entrypoint = " ".join(entrypoint) if entrypoint else ""
    return entrypoint or ""


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--name",
    default=None,
    help="Run name. This identifier controls whether `coiled run` "
    "invocations are dispatched to the same cloud VM or not. "
    "Use the same name to run multiple commands on the same VM. "
    "Defaults to a unique name with no VM reuse.",
)
@click.option(
    "--account",
    "--workspace",
    default=None,
    help="Coiled workspace (uses default workspace if not specified)."
    " Note: ``--account`` is deprecated, please use ``--workspace`` instead.",
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
    "--keepalive",
    default=None,
    help=(
        "Keep your VM running for the specified time, even after your command completes. "
        "In seconds (``--keepalive 60``) unless you specify units (``--keepalive 3m`` for 3 minutes)."
        "Default to shutdown immediately after the command finishes."
    ),
)
@click.option(
    "--file",
    "-f",
    default=[],
    multiple=True,
    help=(
        "Local files required to run command. Can be either individual file or entire directory. "
        "Multiple values can be specified, such as ``--file foo.txt --file my-subdir/``."
    ),
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
@click.option("--subdomain", default=None, help="Custom subdomain for the VM hostname.")
@click.option(
    "--allow-ssh-from",
    default="me",
    type=str,
    help=(
        "IP address or CIDR from which connections to port 22 (SSH) are open; "
        "can also be specified as 'everyone' (0.0.0.0/0) or 'me' (automatically determines public IP detected "
        "for your local client). Note that ``coiled run`` relies on SSH connection for executing commands on VM."
    ),
)
@click.option(
    "--port",
    default=[],
    type=int,
    multiple=True,
    help=(
        "Open extra ports in network firewall for inbound connections "
        "(multiple ports can be set with separate ``--port`` for each)."
    ),
)
@click.option(
    "--interactive",
    "-it",
    default=False,
    is_flag=True,
    help="Open an interactive session, e.g., ``coiled run --interactive bash`` or ``coiled run --interactive python``.",
)
@click.option(
    "--detach", default=False, is_flag=True, help="Start the run in the background, don't wait for the results."
)
@click.option(
    "--sync", default=False, is_flag=True, help="Sync files between local working directory and ``/scratch/synced``."
)
@click.option("--root", default=False, is_flag=True, help="Act as root in Docker container.")
@click.option(
    "--skip-entrypoint",
    default=False,
    is_flag=True,
    hidden=True,
)
@click.option(
    "--no-credential-forwarding",
    default=False,
    is_flag=True,
    help=(
        "Disable automatic forwarding of local cloud credentials; "
        "use if you want your code to use credentials attached to the VM (e.g., AWS Instance Profile)."
    ),
)
@click.option(
    "--forward-gcp-adc",
    default=False,
    is_flag=True,
    help="Forward long-lived Google Cloud Application Default Credentials to VM for data access.",
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
    "--package-sync-strict",
    default=False,
    is_flag=True,
    help="Require exact package version matches when using package sync.",
)
@click.option(
    "--package-sync-conda-extras",
    default=None,
    multiple=True,
    help=(
        "A list of conda package names (available on conda-forge) to include in the "
        "environment that are not in your local environment."
    ),
)
@click.option(
    "--docker-shm-size",
    default=None,
    help="Non-default value for shm_size (for example, '3 GiB').",
)
@click.argument("command", nargs=-1)
def run(
    name: str | None,
    account: str | None,
    software: str | None,
    container: str | None,
    vm_type: Sequence[str],
    gpu: bool,
    region: str | None,
    disk_size: int | None,
    keepalive,
    file,
    env,
    interactive: bool,
    subdomain: str | None,
    allow_ssh_from: str,
    port: List[int],
    detach: bool,
    sync: bool,
    root: bool,
    skip_entrypoint: bool,
    no_credential_forwarding: bool,
    forward_gcp_adc: bool,
    tag,
    sync_ignore,
    mount_bucket,
    host_setup_script: str | None,
    package_sync_strict,
    package_sync_conda_extras,
    docker_shm_size,
    command,
):
    """
    Run a command on the cloud.
    """
    info = start_run(
        name=name,
        workspace=account,
        software=software,
        container=container,
        vm_type=vm_type,
        gpu=gpu,
        region=region,
        disk_size=disk_size,
        keepalive=keepalive,
        file=file,
        env=env,
        tag=tag,
        interactive=interactive,
        detach=detach,
        skip_entrypoint=skip_entrypoint,
        command=command,
        subdomain=subdomain,
        open_extra_ports=port,
        allow_ssh_from=allow_ssh_from,
        sync=sync,
        root=root,
        no_credential_forwarding=no_credential_forwarding,
        forward_gcp_adc=forward_gcp_adc,
        sync_ignore=sync_ignore,
        mount_bucket=mount_bucket,
        host_setup_script=host_setup_script,
        package_sync_strict=package_sync_strict,
        package_sync_conda_extras=package_sync_conda_extras,
        docker_shm_size=docker_shm_size,
    )
    sys.exit(info["exit_code"])


def start_run(
    command: List[str],
    *,
    name: str | None = None,
    file: List[str] | None = None,
    env: List[str] | None = None,
    tag: List[str] | None = None,
    interactive: bool = False,
    detach: bool = False,
    skip_entrypoint: bool = False,
    workspace: str | None = None,
    software: str | None = None,
    container: str | None = None,
    vm_type: Sequence[str] | None = None,
    gpu: bool = False,
    region: str | None = None,
    disk_size: int | None = None,
    keepalive: Union[float, str] | None = None,
    account: str | None = None,
    cluster_type_tag: str = "run/cli",
    subdomain: str | None = None,
    open_extra_ports: List[int] | None = None,
    allow_ssh_from: str = "me",
    sync: bool = False,
    root: bool = False,
    no_credential_forwarding: bool = False,
    forward_gcp_adc: bool = False,
    sync_ignore: List[str] | None = None,
    mount_bucket: List[str] | None = None,
    host_setup_script: str | None = None,
    package_sync_strict: bool = False,
    package_sync_conda_extras: List[str] | None = None,
    docker_shm_size: str | None = None,
):
    runtime_env_dict = dict_from_key_val_list(env)
    tags = dict_from_key_val_list(tag)
    file = file or []

    dask_env = {}
    if container and "rapidsai" in container:
        dask_env = {"DISABLE_JUPYTER": "true", **dask_env}  # needed for "stable" RAPIDS image

    if not command:
        raise ValueError("command must be specified")

    if sync and file:
        raise ValueError("--sync and --file cannot be used together")
    if sync and detach:
        raise ValueError("--sync and --detach cannot be used together")

    if detach and keepalive is None:
        # For --detach, we don't want to shut down cluster on close.
        # We'll use keepalive plugin to monitor the "detached" processes
        # and keep cluster alive while these are running.
        keepalive = "10ms"
    keepalive = parse_timedelta(keepalive)
    shutdown_on_close = keepalive is None

    info = {"command": command, "keepalive": keepalive, "subdomain": subdomain, "exit_code": 0}

    success = True
    exception = None

    # Handle command as string case (e.g. `coiled run "python myscript.py"`)
    if len(command) == 1:
        command = shlex.split(command[0])
    # if user tries `coiled run foo.py` they probably want to run `python foo.py` rather than `foo.py`
    if len(command) == 1 and command[0].endswith(".py"):
        command = ["python", command[0]]

    results = None

    # fail early if user specified `--file` that doesn't exist
    check_explicit_files(file)

    try:
        with coiled.Cloud(workspace=workspace or account) as cloud:
            workspace = workspace or cloud.default_workspace
            with LightRichClusterWidget(
                workspace=workspace,
                title=f"Running [bold]{shlex.join(command)}[/bold]",
                include_total_cost=False,
                extra_link="..." if open_extra_ports else None,
                extra_link_title="Server",
            ) as widget:
                widget.update(
                    server=cloud.server,
                    cluster_details=None,
                    logs=None,
                    workspace=workspace,
                )
                info["workspace"] = workspace
                cluster_kwargs: ClusterKwargs = {
                    "workspace": workspace,
                    "n_workers": 0,
                    "software": software,
                    "container": container,
                    "scheduler_options": {"idle_timeout": "520 weeks"},  # rely on shutdown_on_close and/or keepalive
                    "scheduler_vm_types": list(vm_type) if vm_type else None,
                    "worker_vm_types": list(vm_type) if vm_type else None,
                    "allow_ssh_from": allow_ssh_from,
                    "open_extra_ports": open_extra_ports,
                    "extra_worker_on_scheduler": True,
                    "environ": dask_env,
                    "scheduler_gpu": gpu,
                    "region": region,
                    "shutdown_on_close": shutdown_on_close,
                    "tags": {**tags, **{"coiled-cluster-type": cluster_type_tag}},
                    "scheduler_disk_size": disk_size,
                    "worker_disk_size": disk_size,
                    "dashboard_custom_subdomain": subdomain,
                    "mount_bucket": mount_bucket,
                    "host_setup_script": host_setup_script,
                    "package_sync_strict": package_sync_strict,
                    "package_sync_conda_extras": package_sync_conda_extras,
                    "backend_options": {"docker_shm_size": docker_shm_size} if docker_shm_size else None,
                    "unset_single_threading_variables": True,
                }
                cluster_kwargs["name"] = name or f"run-{short_random_string()}"
                cluster_kwargs["cloud"] = cloud
                cluster_kwargs["custom_widget"] = widget  # `Cluster` will update widget until it's "ready"

                if no_credential_forwarding:
                    cluster_kwargs["credentials"] = None
                    dask.config.set({"coiled.use_aws_creds_endpoint": False})
                else:
                    dask.config.set({"coiled.use_aws_creds_endpoint": True})

                with coiled.Cluster(**cluster_kwargs) as cluster:
                    info["cluster_id"] = cluster.cluster_id

                    # set dask config so that cluster started from this cluster will re-use software env
                    runtime_env_dict["DASK_COILED__SOFTWARE"] = cluster._software_environment_name
                    runtime_env_dict["DASK_COILED__SOFTWARE_REQUIRES_VM_ARCH"] = cluster.arch.vm_arch
                    runtime_env_dict["DASK_COILED__SOFTWARE_IS_GPU_CLUSTER"] = cluster._is_gpu_cluster

                    # by default "shutdown on close" is also what enables "keepalive" timeout on clusters,
                    # but we want to use "keepalive" timeout (together with "keepalive sessions") to shut
                    # down cluster after the run (submitted via SSH) is done
                    if not shutdown_on_close:
                        cluster.set_keepalive(keepalive=keepalive)

                    if open_extra_ports:
                        url = (
                            parse_url(cluster._dashboard_address)
                            ._replace(scheme="http", port=open_extra_ports[0], path=None, query=None)
                            .url
                        )
                        widget.update(
                            cluster_details=None,
                            logs=None,
                            extra_link=url,
                        )

                    if interactive:
                        widget.stop()

                    if sync:
                        start_sync(cloud, cluster.cluster_id, console=widget.live.console, ignores=sync_ignore)

                    if forward_gcp_adc:
                        gcp_creds_to_forward = send_application_default_credentials(cluster, return_creds=True)
                        if gcp_creds_to_forward:
                            runtime_env_dict = {**gcp_creds_to_forward.get("env", {}), **runtime_env_dict}

                    _connection, _container_command, results = run_via_ssh(
                        cloud=cloud,
                        cluster=cluster,
                        info=info,
                        command=command,
                        file=file,
                        interactive=interactive,
                        detach=detach,
                        skip_entrypoint=skip_entrypoint,
                        env=runtime_env_dict,
                        env_unset=list(unset_single_thread_defaults().keys()),
                        workdir=SYNC_TARGET if sync else "/scratch",
                        as_root=root,
                        console=widget.live.console,
                    )

            if sync:
                # this will wait on session flush, so remote files will finish being synced to local system
                stop_sync(cloud, cluster.cluster_id, wait=True)

        if cluster.cluster_id and not interactive:
            if detach:
                print(f"Running [green]{shlex.join(command)}[/green] in background.")
            else:
                print()

                print("Output")
                print("-" * len("Output"))
                print()

            if results:
                if isinstance(results, str):
                    print(results)
                else:
                    print(results.stdout)
                    if results.stderr:
                        print(f"[red]{results.stderr}")

            print()
        return info
    except Exception as e:
        success = False
        info["exit_code"] = 1
        exception = e
        print("[red]There was an error:[/red]")
        print(exception)
        return info
    finally:
        coiled.add_interaction(
            "coiled-run-cli",
            success=success,
            **info,
            **error_info_for_tracking(exception),
        )
