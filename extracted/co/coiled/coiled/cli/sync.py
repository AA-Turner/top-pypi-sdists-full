from __future__ import annotations

import os
import shlex
import shutil
import subprocess
from typing import List, Tuple

from rich import print
from rich.console import Console

from .cluster.ssh import add_ssh_access, get_ssh_add_path, get_ssh_path, remove_ssh_access

# Path on VM to sync to.
# We use `/scratch` for now because it's already bind-mounted into docker.
SYNC_TARGET = "/scratch/synced"
MUTAGEN_NAME_FORMAT = "coiled-{cluster_id}"


def can_use_mutagen():
    return get_mutagen_path() and get_ssh_path() and get_ssh_keygen_path()


def start_sync(cloud, cluster_id, console=None, include_vcs=False, debug=False, ignores=None):
    mutagen_path = get_mutagen_path()
    if not mutagen_path:
        return

    console = console or Console()

    _, error = connect_mutagen_sync(
        cloud=cloud, cluster_id=cluster_id, console=console, include_vcs=include_vcs, debug=debug, ignores=ignores
    )
    if error:
        print(error)
    return error


def stop_sync(cloud, cluster_id, message=None, wait=False):
    mutagen_path = get_mutagen_path()
    if cluster_id and mutagen_path and mutagen_session_exists(cluster_id):
        # NOTE: we can't tell if the user asked for `--sync` or not at creation.
        # Best we can do is check if mutagen is installed and the session exists.
        ssh_keygen_path = get_ssh_keygen_path()
        if not ssh_keygen_path:
            return

        # Stop mutagen
        if message:
            print(message)

        if wait:
            subprocess.run([mutagen_path, "sync", "flush", MUTAGEN_NAME_FORMAT.format(cluster_id=cluster_id)])

        subprocess.run([mutagen_path, "sync", "terminate", MUTAGEN_NAME_FORMAT.format(cluster_id=cluster_id)])

        ssh_info = cloud.get_ssh_key(cluster_id)
        scheduler_address = ssh_info["scheduler_hostname"] or ssh_info["scheduler_address_to_use"]

        remove_ssh_access(scheduler_address, key=ssh_info["private_key"])

        # Remove `known_hosts` entries.
        # TODO don't like touching the user's `known_hosts` file like this.
        subprocess.run(
            [
                ssh_keygen_path,
                "-f",
                os.path.expanduser("~/.ssh/known_hosts"),
                "-R",
                scheduler_address,
            ],
            capture_output=True,
        )


def get_mutagen_path() -> str | None:
    mutagen_path = shutil.which("mutagen")
    if not mutagen_path:
        print(
            "[bold red]"
            "mutagen must be installed to synchronize files with notebooks.[/]\n"
            "Install via homebrew (on macOS, Linux, or Windows) with:\n\n"
            "brew install mutagen-io/mutagen/mutagen@0.16\n\n"
            "Or, visit https://github.com/mutagen-io/mutagen/releases/latest to download "
            "a static, pre-compiled binary for your system, and place it anywhere on your $PATH."
        )
        return None
    return mutagen_path


def get_ssh_keygen_path() -> str | None:
    ssh_keygen_path = shutil.which("ssh-keygen")
    if not ssh_keygen_path:
        print("[bold red]Unable to find `ssh-keygen`, you may need to install OpenSSH or add it to your paths.[/]")
        return None
    return ssh_keygen_path


def mutagen_session_exists(cluster_id: int) -> bool:
    mutagen_path = get_mutagen_path()
    if not mutagen_path:
        return False
    sessions = (
        subprocess.run(
            [
                mutagen_path,
                "sync",
                "list",
                "--label-selector",
                f"managed-by=coiled,cluster-id={cluster_id}",
                "--template",
                "{{range .}}{{.Name}}{{end}}",
            ],
            text=True,
            capture_output=True,
        )
        .stdout.strip()
        .splitlines()
    )

    if not sessions:
        return False
    if sessions == [MUTAGEN_NAME_FORMAT.format(cluster_id=cluster_id)]:
        return True

    if len(sessions) == 1:
        raise RuntimeError(
            f"Unexpected mutagen session name {sessions[0]!r}. "
            f"Expected {MUTAGEN_NAME_FORMAT.format(cluster_id=cluster_id)!r}."
        )

    raise RuntimeError(f"Multiple mutagen sessions found for cluster {cluster_id}: {sessions}")


def add_host_to_known_hosts(console, target: str) -> Tuple[bool, str]:
    # Since we may not know the location of known_hosts, use `ssh` to add the key to the agent
    ssh_path = get_ssh_path()
    if not ssh_path:
        raise RuntimeError("ssh not installed")
    result = subprocess.run(
        [
            ssh_path,
            "-o",
            "BatchMode=yes",
            "-o",
            "ConnectTimeout=5",
            "-o",
            "StrictHostKeyChecking=no",
            target,
            "echo",
            "ok",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        console.print(f"[red]Error attempting to ssh...[/red]\n\n{result.stderr}")
        return False, result.stderr
    return True, ""


def connect_mutagen_sync(
    cloud, cluster_id, console, include_vcs: bool = False, debug=False, ignores: List[str] | None = None
) -> Tuple[bool, str]:
    ignores = ignores or []
    ignores = [*ignores, ".venv"]

    if mutagen_session_exists(cluster_id):
        console.print("[bold]File sync session already active; reusing it.[/]")
    else:
        console.print("[bold]Launching file synchronization...[/]")
        ssh_info = cloud.get_ssh_key(cluster_id)

        scheduler_address = ssh_info["scheduler_hostname"] or ssh_info["scheduler_public_address"]
        target = f"ubuntu@{scheduler_address}"

        add_ssh_access(scheduler_address, key=ssh_info["private_key"])

        added, ssh_error = add_host_to_known_hosts(console, target)
        if not added:
            return False, ssh_error

        if debug:
            ssh_keygen = shutil.which("ssh-keygen")
            if ssh_keygen:
                proc = subprocess.run(
                    [ssh_keygen, "-H", "-F", scheduler_address],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                console.print(f"Existing known_hosts entries for {scheduler_address}:\n[green]{proc.stdout}[/green]\n")
            ssh_add_path = get_ssh_add_path()
            if ssh_add_path:
                proc = subprocess.run(
                    [ssh_add_path, "-l"],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                console.print(f"Existing ssh keys:\n[green]{proc.stdout}[/green]\n")

        # Start mutagen
        sync_command = [
            "mutagen",
            "sync",
            "create",
            "--name",
            MUTAGEN_NAME_FORMAT.format(cluster_id=cluster_id),
            "--label",
            "managed-by=coiled",
            "--label",
            f"cluster-id={cluster_id}",
            "--no-ignore-vcs" if include_vcs else "--ignore-vcs",
            f"--ignore={','.join(ignores)}" if ignores else "",
            "--max-staging-file-size=1 GiB",
            # make files on the remote public (to avoid problems if uid on host != uid in container)
            "--default-file-mode-beta=666",
            "--default-directory-mode-beta=0777",
            ".",
            f"{target}:{SYNC_TARGET}",
        ]
        if debug:
            console.print(f"Sync command:\n[green]{shlex.join(sync_command)}[/green]\n")

        result = subprocess.run(
            sync_command,
            check=False,
            text=True,
            capture_output=True,
        )

        # TODO show output live by wrapping console.print as file object that we pass to subprocess.run (?)
        if result.stderr:
            console.print("[red]Error attempting to connect sync...[/red]\n\n")
            console.out(result.stderr)
        elif result.stdout:
            console.out(result.stdout)

        if result.returncode != 0:
            # there was a problem starting mutagen sync, so no reason to link the sync directory
            # (and most likely ssh is the problem so this too would fail)
            return False, result.stderr

        # From host (outside container), make the directory and set permissions.
        # If container user doesn't match host user, then we can't do this *inside* container.
        outside_dir_setup = f"mkdir -p {SYNC_TARGET} && chmod a+rwx {SYNC_TARGET}"

        # Within the docker container, symlink the sync directory (`/scratch/sync`)
        # into the working directory for Jupyter, so you can actually see the synced
        # files in the Jupyter browser. We use a symlink since the container doesn't
        # have capabilities to make a bind mount.
        # TODO if we don't like the symlink, Coiled could see what the workdir is for
        #  the image before running, and bind-mount `/sync` on the host to `$workdir/sync`
        #  in the container? Custom docker images make this tricky; we can't assume anything
        #  about the directory layout or what the working directory will be.
        inside_dir_setup = f"docker exec tmp-dask-1 bash -c 'ln -s {SYNC_TARGET} .'"

        symlink_command = [
            "ssh",
            target,
            f"{outside_dir_setup} && {inside_dir_setup}",
        ]
        if debug:
            console.print(
                "Symlink command so /sync in container maps to synced directory:\n"
                f"[green]{shlex.join(symlink_command)}[/green]\n"
            )
        subprocess.run(
            symlink_command,
            check=True,
            capture_output=True,
        )
    return True, ""
