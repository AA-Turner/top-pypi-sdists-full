from pathlib import Path
from typing import Optional
from urllib import parse

import click

import vessl
from vessl import vessl_api
from vessl.util.echo import print_info, print_success, print_warning


def set_default_ssh_key(key_path: str):
    path = Path(key_path)
    if path.suffix == '.pub':
        path = path.with_suffix('')

    if path.exists():
        vessl_api.config_loader.default_ssh_private_key_path = str(path.absolute())
        print_success(f"Registered {path} as a default keyfile for vessl ssh commands.")


def ssh_command_from_endpoint(endpoint: str, key_path: Optional[str] = None) -> str:
    endpoint = parse.urlparse(endpoint)
    cmd = f"ssh root@{endpoint.hostname} -p {endpoint.port}"
    if key_path:
        cmd += f" -i {key_path}"
    return cmd


def resolve_ssh_private_key_path(key_path: Optional[str]) -> Optional[str]:
    if key_path:
        return key_path

    if default_key_path := vessl_api.config_loader.default_ssh_private_key_path:
        print_success(f"{default_key_path} found. Using this key to connect...")
        return default_key_path

    print_info("Searching for SSH private key...")
    ssh_keys = vessl.list_ssh_keys()
    if len(ssh_keys) == 0:
        raise click.BadParameter(
            "At least one ssh public key should be added.\n" "Please run `vessl ssh-key add`."
        )

    for ssh_key in ssh_keys:
        if ssh_key.filename.endswith(".pub"):
            key_path = Path.home() / ".ssh" / ssh_key.filename[:-4]
            if key_path.exists():
                print_success(f"{key_path} found. Using this key to connect...")
                return str(key_path)

    for key_path in (
        Path.home() / ".ssh" / "id_ed25519",
        Path.home() / ".ssh" / "id_rsa",
    ):
        if key_path.exists():
            print_success(f"{key_path} found. Using this key to connect...")
            return str(key_path)

    print_warning("No SSH private key found. Please provide the path to the SSH private key with --key-path option.")
    return None


def ssh_private_key_path_callback(
    ctx: click.Context, param: click.Parameter, key_path: Optional[str]
) -> Optional[str]:
    return resolve_ssh_private_key_path(key_path)
