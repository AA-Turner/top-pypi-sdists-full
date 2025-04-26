import datetime
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional

import click
import dask.config
from rich import print
from rich.prompt import Confirm

import coiled
from coiled.utils import get_temp_dir

from ..utils import CONTEXT_SETTINGS
from .utils import find_cluster

DEFAULT_SSH_AGENT_CONFIG = "Host *.dask.host\n  IdentityAgent SSH_AUTH_SOCK"


def open_ssh(address: str, key: str, jump_to_address: Optional[str] = None, host_command: Optional[str] = None):
    """Open an SSH session, relies on `ssh` and `ssh-add` (agent)."""
    if not add_key_to_agent(address, key, t=5):
        return

    ssh_shell(address, jump_to_address, host_command)


def get_ssh_path() -> Optional[str]:
    ssh_path = shutil.which("ssh")
    if not ssh_path:
        print("Unable to find `ssh`, you may need to install OpenSSH or add it to your paths.")
        return None
    return ssh_path


def get_ssh_add_path() -> Optional[str]:
    ssh_add_path = shutil.which("ssh-add")
    if not ssh_add_path:
        print("Unable to find `ssh-add`, you may need to install OpenSSH or add it to your paths.")
        return None
    return ssh_add_path


def check_ssh_agent():
    user_config_path = Path(os.path.expanduser("~")) / ".ssh" / "config"
    if user_config_path.exists():
        with open(user_config_path) as f:
            user_config = f.read()
            if "dask.host" in user_config:
                return True
            if re.search("IdentityAgent[^\n]+1password", user_config):
                print("Coiled cannot add temporary SSH key to [bold]1Password SSH Agent[/bold].")
                print(
                    "You can explicitly allow Coiled to use the system SSH agent by adding these lines to the "
                    f"beginning of [green]{user_config_path}[/green]:\n\n{DEFAULT_SSH_AGENT_CONFIG}\n\n"
                )
                if Confirm.ask("May Coiled edit your ssh config to add these lines?", default=True):
                    with open(user_config_path, "w") as f:
                        f.write(f"{DEFAULT_SSH_AGENT_CONFIG}\n\n{user_config}")
                    return True
                return False
    return True


def add_key_to_agent(address: str, key: str, t: Optional[int] = None, delete: bool = False) -> bool:
    """Add (or remove) ssh key to ssh agent."""
    ssh_add_path = get_ssh_add_path()
    if not ssh_add_path:
        return False

    with get_temp_dir() as keydir:
        key_path = os.path.join(keydir, f"scheduler-key-{address}.pem")

        with open(key_path, "w") as f:
            f.write(key)

        # ssh needs file permissions to be set
        os.chmod(key_path, mode=0o600)

        cmd = [ssh_add_path]
        if delete:
            cmd.append("-d")
        if t:
            cmd.extend(["-t", f"{t}"])
        cmd.append(key_path)

        # briefly add key to agent, this allows us to jump to worker with agent forwarding
        p = subprocess.run(cmd, capture_output=True, text=True)

        if p.returncode and p.stderr:
            print("An error occurred calling `ssh-add`. You may need to enable the ssh agent.")
            print(p.stderr)
            return False

    return True


def _write_coiled_ssh_key(coiled_ssh_dir, address, key):
    key_path = os.path.join(coiled_ssh_dir, f"scheduler-key-{address}.pem")

    with open(key_path, "w") as f:
        f.write(key)
    # ssh needs file permissions to be set
    os.chmod(key_path, mode=0o600)

    return key_path


def _delete_coiled_ssh_key_file(coiled_ssh_dir, address):
    key_path = os.path.join(coiled_ssh_dir, f"scheduler-key-{address}.pem")

    if os.path.exists(key_path):
        os.remove(key_path)


def _add_host_to_coiled_ssh_config(coiled_config_path, address, key_path):
    identity_config = f"""
Host {address}
    # added {datetime.datetime.now()}
    HostName {address}
    User ubuntu
    IdentityFile {key_path}
    """
    # print(identity_config)
    do_write = False
    if not os.path.exists(coiled_config_path):
        do_write = True
    else:
        with open(coiled_config_path, "r") as f:
            if f"Host {address}" not in f.read():
                do_write = True
            else:
                # print(f"Host {address} is already in {coiled_config_path}")
                ...
    if do_write:
        with open(coiled_config_path, "a") as af:
            af.write(identity_config)


def _remove_host_from_coiled_ssh_config(coiled_config_path, address):
    if os.path.exists(coiled_config_path):
        with open(coiled_config_path, "r") as f:
            contents = f.read()
        if f"Host {address}" in contents:
            updated = re.sub(rf"\nHost {address}(\n +[^\n]+)*\n", "", contents, flags=re.MULTILINE)
            with open(coiled_config_path, "w") as f:
                f.write(updated)
            # print(f"Removed 'Host {address} [...]' from {coiled_config_path}")


def _add_coiled_to_ssh_config(coiled_config_path):
    ssh_dir = Path(os.path.expanduser("~")) / ".ssh"
    ssh_config_path = ssh_dir / "config"
    include_line = f"Include {coiled_config_path}"
    try:
        os.makedirs(ssh_dir, exist_ok=True)
        if ssh_config_path.exists():
            with open(ssh_config_path, "r") as f:
                ssh_config_contents = f.read()
        else:
            ssh_config_contents = ""

        if include_line not in ssh_config_contents:
            with open(ssh_config_path, "w") as wf:
                print(f"Add {include_line!r} to {ssh_config_path}")
                wf.write(f"{include_line}\n\n{ssh_config_contents}")
        else:
            # print(f"{include_line!r} already in {ssh_config_path}")
            ...
    except Exception as e:
        raise coiled.exceptions.CoiledException(
            "Unable to update your SSH config file to include the Coiled-specific SSH config because of this error:\n"
            f"  {e}\n\n"
            "You can run\n"
            "  coiled config set coiled.use_ssh_agent True\n"
            "to use the SSH agent instead of SSH config for Coiled SSH access,\n"
            "or contact support@coiled.io if you'd like help troubleshooting."
        ) from None


def add_ssh_identity_to_config(address: str, key: str):
    # Make directory for Coiled-specific SSH things (keys and config)
    coiled_ssh_dir = Path(os.path.expanduser("~")) / ".coiled" / "ssh"
    os.makedirs(coiled_ssh_dir, exist_ok=True)

    # Key
    key_path = _write_coiled_ssh_key(coiled_ssh_dir, address, key)

    # Add host to the Coiled-specific SSH config file
    coiled_config_path = os.path.join(coiled_ssh_dir, "coiled-identities")
    _add_host_to_coiled_ssh_config(coiled_config_path, address, key_path)

    # Make sure Coiled-specific SSH config file is included in general SSH config file
    _add_coiled_to_ssh_config(coiled_config_path)


def remove_ssh_key_from_config(address: str):
    # Remove the SSH key file
    coiled_ssh_dir = Path(os.path.expanduser("~")) / ".coiled" / "ssh"
    _delete_coiled_ssh_key_file(coiled_ssh_dir, address)

    # Remove identity from Coiled-specific SSH config file
    coiled_config_path = os.path.join(coiled_ssh_dir, "coiled-identities")
    _remove_host_from_coiled_ssh_config(coiled_config_path, address)


def add_ssh_access(address: str, key: str, t=None):
    if dask.config.get("coiled.use_ssh_agent", False):
        add_key_to_agent(address, key, t)
    else:
        add_ssh_identity_to_config(address, key)


def remove_ssh_access(address: str, key: str):
    if dask.config.get("coiled.use_ssh_agent", False):
        add_key_to_agent(address, key, delete=True)
    else:
        remove_ssh_key_from_config(address)


def ssh_shell(address: str, jump_to_address: Optional[str] = None, host_command: Optional[str] = None):
    if jump_to_address:
        ssh_target = ["-J", f"ubuntu@{address}", f"ubuntu@{jump_to_address}"]
        ssh_target_label = f"worker at {jump_to_address}"
    else:
        ssh_target = [f"ubuntu@{address}"]
        ssh_target_label = f"scheduler at {address}"

    ssh_path = get_ssh_path()
    if not ssh_path:
        return
    ssh_command = [ssh_path, "-t", *ssh_target, "-o", "StrictHostKeyChecking=no", "-o", "ForwardAgent=yes"]
    if host_command:
        ssh_command.append(host_command)

    print(f"===Starting SSH session to {ssh_target_label}===")
    if host_command:
        print(f"> {host_command}")
    subprocess.run(ssh_command)
    print("===SSH session closed===")


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("cluster", default="", required=False)
@click.option(
    "--account",
    "--workspace",
    default=None,
    help="Coiled workspace (uses default workspace if not specified)."
    " Note: --account is deprecated, please use --workspace instead.",
)
@click.option(
    "--private",
    default=False,
    is_flag=True,
    help="Use private IP address of scheduler (default is DNS hostname for public IP)",
)
@click.option(
    "--by-ip",
    default=False,
    is_flag=True,
    help="Use public IP address of scheduler directly, not using DNS hostname",
)
@click.option(
    "--worker",
    default=None,
    help="Connect to worker with specified name or private IP address (default is to connect to scheduler)",
)
@click.option(
    "--add-key",
    default=False,
    is_flag=True,
    help="Just add ssh key to local OpenSSH agent, no lifetime/expiration set",
)
@click.option(
    "--delete-key",
    default=False,
    is_flag=True,
    help="Just delete ssh key from local OpenSSH agent",
)
@click.option(
    "--dask", default=False, is_flag=True, help="Attach to shell in Dask container rather than shell on host machine."
)
@click.option(
    "--command",
    default=None,
    hidden=True,
)
def ssh(
    cluster: str,
    account: Optional[str],
    private: bool,
    by_ip: bool,
    worker: Optional[str],
    add_key: bool,
    delete_key: bool,
    dask: bool,
    command: Optional[str],
):
    with coiled.Cloud(account=account) as cloud:
        cluster_info = find_cluster(cloud, cluster)
        cluster_id = cluster_info["id"]
        ssh_info = cloud.get_ssh_key(cluster_id=cluster_id, worker=worker)

    if private:
        scheduler_address = ssh_info["scheduler_private_address"]
    else:
        if by_ip:
            scheduler_address = ssh_info["scheduler_public_address"]
        else:
            scheduler_address = ssh_info["scheduler_hostname"] or ssh_info["scheduler_public_address"]

    if add_key:
        # just add the key, maybe you want to use rsync or something like that
        add_ssh_access(scheduler_address, key=ssh_info["private_key"])

    elif delete_key:
        # just delete the key
        remove_ssh_access(scheduler_address, key=ssh_info["private_key"])

    else:
        if not check_ssh_agent():
            print("You may get an error, but we'll try SSH anyway...")

        # open an ssh shell
        if ssh_info["scheduler_state"] not in ("starting", "started"):
            print(
                f"[red]Scheduler for {cluster_info['name']} ({cluster_id}) is "
                f"[bold]{ssh_info['scheduler_state']}[/bold]. "
                "You can only connect when scheduler is 'starting' or 'started'."
            )
            return

        if not scheduler_address:
            print(
                f"[red]Scheduler for {cluster_info['name']} ({cluster_id}) is "
                f"[bold]{ssh_info['scheduler_state']}[/bold] and does not currently have an IP address.[/]"
            )
            return

        if not ssh_info["private_key"]:
            print("Unable to retrieve SSH key")
            return

        # Default container name is parent dir (tmp) + service name (dask) + instance number (1).
        # If we need to make this more flexible in the future, name could be returned by cloud.get_ssh_key;
        # for now we don't need that flexibility and it's okay if SSH CLI requires client update someday.
        command = f"docker exec -it tmp-dask-1 {command or 'bash'}" if dask else command

        open_ssh(
            address=scheduler_address,
            key=ssh_info["private_key"],
            jump_to_address=ssh_info["worker_address"],
            host_command=command,
        )
