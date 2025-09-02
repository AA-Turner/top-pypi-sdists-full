import asyncio
import base64
import os
import tempfile
import uuid
from urllib.parse import urlparse


def _add_ssh_scheme_to_url(url: str) -> str:
    scheme: str = "ssh://"
    if url.startswith(scheme):
        return url
    url_with_scheme = scheme + url
    return url_with_scheme


def _url_has_port(url: str) -> bool:
    parsed_url = urlparse(url)
    try:
        if parsed_url.port:
            return True
    except ValueError:
        # Port could not be cast to integer value, or
        # Port out of range 0-65535
        return False
    else:
        return False


def _set_default_ssh_port(url_with_scheme: str) -> str:
    """Add a default port placeholder to a URL that lacks an explicit port.

    This function modifies URLs that use the SSH protocol format for Git
    repositories. It adds a placeholder for the default port
    (represented by ':/')  after the hostname.

    Args:
        url_with_scheme (str): The input URL, expected to be in the format
        "ssh://git@hostname:path/to/repo.git"

    Returns:
        str: The modified URL with the default port placeholder added,
        in the format "ssh://git@hostname:/path/to/repo.git"

    Examples:
        "ssh://git@gitlab.com:fluidattacks/demo.git" becomes
        "ssh://git@gitlab.com:/fluidattacks/demo.git"

    Note:
        This function modifies the URL only if all the following
        conditions are met:
        1. The URL starts with 'ssh://'.
        2. The URL does not already contain a port.
        3. The URL contains exactly two colons after the 'ssh://' scheme.
        URLs not meeting these criteria are returned unchanged.

    """
    has_ssh_scheme = url_with_scheme.startswith("ssh://")

    # formatting is skipped if no ssh scheme or URL contains a port
    if not has_ssh_scheme or _url_has_port(url_with_scheme):
        return url_with_scheme

    url_parts = url_with_scheme.split(":", 2)
    if len(url_parts) < 3:
        return url_with_scheme

    url_with_default_port = f"{url_parts[0]}:{url_parts[1]}:/{url_parts[2]}"
    return url_with_default_port


def parse_ssh_url(url: str) -> str:
    if "source.developers.google" in url or url.startswith("ssh://FLUID"):
        return url

    url_with_scheme = _add_ssh_scheme_to_url(url)

    # url misses an explicit ssh port
    url_with_default_ssh_port = _set_default_ssh_port(url_with_scheme)
    return url_with_default_ssh_port


def _create_ssh_file(temp_dir: str, credential_key: str) -> str:
    ssh_file_name: str = os.path.join(temp_dir, str(uuid.uuid4()))
    with open(
        os.open(ssh_file_name, os.O_CREAT | os.O_WRONLY, 0o400),
        "w",
        encoding="utf-8",
    ) as ssh_file:
        ssh_file.write(base64.b64decode(credential_key).decode())
    return ssh_file_name


async def _execute_git_command(
    ssh_file_name: str,
    raw_root_url: str,
    branch: str,
) -> tuple[bytes, bytes, int | None]:
    proc = await asyncio.create_subprocess_exec(
        "git",
        "ls-remote",
        "--",
        raw_root_url,
        branch,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        env={
            **os.environ.copy(),
            "GIT_SSH_COMMAND": (
                f"ssh -i {ssh_file_name}"
                " -o UserKnownHostsFile=/dev/null"
                " -o StrictHostKeyChecking=no"
                " -o IdentitiesOnly=yes"
                " -o HostkeyAlgorithms=+ssh-rsa"
                " -o PubkeyAcceptedAlgorithms=+ssh-rsa"
            ),
        },
    )
    stdout, stderr = await asyncio.wait_for(proc.communicate(), 20)

    return stdout, stderr, proc.returncode


async def ssh_ls_remote(
    repo_url: str,
    credential_key: str,
    branch: str,
) -> tuple[str | None, str | None]:
    raw_root_url = parse_ssh_url(repo_url)
    with tempfile.TemporaryDirectory() as temp_dir:
        ssh_file_name = _create_ssh_file(temp_dir, credential_key)
        try:
            stdout, stderr, return_code = await _execute_git_command(
                ssh_file_name,
                raw_root_url,
                branch,
            )
        except asyncio.exceptions.TimeoutError:
            return None, "git ls-remote time out"

        finally:
            os.remove(ssh_file_name)

        if return_code == 0:
            return stdout.decode().split("\t")[0], None

        return None, stderr.decode("utf-8")


async def call_ssh_ls_remote(
    repo_url: str,
    credential_key: str,
    branch: str,
) -> tuple[str | None, str | None]:
    return await ssh_ls_remote(
        repo_url=repo_url,
        credential_key=credential_key,
        branch=branch,
    )
