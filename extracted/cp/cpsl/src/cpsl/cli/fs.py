import os

import click
import requests
from rich.console import Console
from rich.table import Table

from .. import terminal
from ..channel import ServiceClient, pass_service_client
from ..clients.capsule import (
    CreateFilesystemRequest,
    DeleteFilesystemRequest,
    ListFilesystemsRequest,
)
from ..config import get_config_context


def _http_base() -> tuple[str, dict[str, str]]:
    """Return (base_url, headers) for the gateway HTTP API."""
    ctx = get_config_context()
    if not ctx or not ctx.is_valid():
        terminal.error("Not logged in. Run 'capsule login' first.")
        raise SystemExit(1)

    port = ctx.gateway_http_port
    if port is None:
        port = ctx.gateway_port if ctx.gateway_port in (443, 80) else ctx.gateway_port + 1
    scheme = "https" if port == 443 else "http"
    host = ctx.gateway_host
    if port not in (443, 80):
        host = f"{host}:{port}"
    base = f"{scheme}://{host}/api/v1/fs"
    headers = {"Authorization": f"Bearer {ctx.token}"}
    return base, headers


@click.group()
def fs():
    """Manage filesystems."""
    pass


@fs.command("create")
@click.argument("name")
@pass_service_client
def create(client: ServiceClient, name: str):
    """Create a new filesystem."""
    res = client.filesystems.create_filesystem(CreateFilesystemRequest(name=name))
    if not res.ok:
        terminal.error(f"Failed: {res.err_msg}")
        raise SystemExit(1)

    terminal.success(f'Filesystem "{name}" created.')
    terminal.detail(f"  id: {res.filesystem.id}")


@fs.command("list")
@pass_service_client
def list_fs(client: ServiceClient):
    """List all filesystems."""
    _list_filesystems(client)


def _list_filesystems(client: ServiceClient):
    res = client.filesystems.list_filesystems(ListFilesystemsRequest())
    if not res.ok:
        terminal.error(f"Failed: {res.err_msg}")
        raise SystemExit(1)

    if not res.filesystems:
        terminal.info("No filesystems. Create one with 'capsule fs create <name>'.")
        return

    table = Table(title="Filesystems")
    table.add_column("Name")
    table.add_column("ID")
    table.add_column("Created")

    for f in res.filesystems:
        table.add_row(f.name, f.id, f.created_at)

    Console().print(table)


@fs.command("delete")
@click.argument("name")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation.")
@pass_service_client
def delete(client: ServiceClient, name: str, yes: bool):
    """Delete a filesystem."""
    if not yes:
        click.confirm(f'Delete filesystem "{name}"? This cannot be undone', abort=True)

    res = client.filesystems.delete_filesystem(DeleteFilesystemRequest(name=name))
    if not res.ok:
        terminal.error(f"Failed: {res.err_msg}")
        raise SystemExit(1)

    terminal.success(f'Filesystem "{name}" deleted.')


@fs.command("ls")
@click.argument("name", required=False)
@click.argument("path", default="/")
@pass_service_client
def ls(client: ServiceClient, name: str | None, path: str):
    """List filesystems, or files in a named filesystem."""
    from ..clients.capsule import GetFilesystemRequest

    if not name:
        _list_filesystems(client)
        return

    res = client.filesystems.get_filesystem(GetFilesystemRequest(name=name))
    if not res.ok:
        terminal.error(f"Filesystem not found: {res.err_msg}")
        raise SystemExit(1)

    base, headers = _http_base()
    r = requests.get(f"{base}/{res.filesystem.id}/list", params={"path": path}, headers=headers)
    if r.status_code != 200:
        terminal.error(f"List failed: {r.text}")
        raise SystemExit(1)

    data = r.json()
    entries = data.get("entries", [])

    if not entries:
        terminal.info(f"Empty: {path}")
        return

    table = Table(title=f"{name}:{path}")
    table.add_column("Name")
    table.add_column("Type", width=4)
    table.add_column("Size", justify="right")

    for f in entries:
        kind = "dir" if f.get("is_folder") else "file"
        size = str(f.get("size", "")) if not f.get("is_folder") else ""
        table.add_row(f.get("name", ""), kind, size)

    Console().print(table)


@fs.command("upload")
@click.argument("name")
@click.argument("local_path", type=click.Path(exists=True))
@click.argument("remote_path", default="")
@pass_service_client
def upload(client: ServiceClient, name: str, local_path: str, remote_path: str):
    """Upload a file to a filesystem.

    capsule fs upload my-data ./report.csv /reports/report.csv
    """
    from ..clients.capsule import GetFilesystemRequest

    if not remote_path:
        remote_path = "/" + os.path.basename(local_path)

    res = client.filesystems.get_filesystem(GetFilesystemRequest(name=name))
    if not res.ok:
        terminal.error(f"Filesystem not found: {res.err_msg}")
        raise SystemExit(1)

    base, headers = _http_base()

    import mimetypes

    content_type = mimetypes.guess_type(local_path)[0] or "application/octet-stream"

    r = requests.post(
        f"{base}/{res.filesystem.id}/upload-url",
        json={"path": remote_path, "content_type": content_type},
        headers=headers,
    )
    if r.status_code != 200:
        terminal.error(f"Get upload URL failed: {r.text}")
        raise SystemExit(1)

    presigned_url = r.json().get("url")
    if not presigned_url:
        terminal.error("No upload URL returned.")
        raise SystemExit(1)

    file_size = os.path.getsize(local_path)
    terminal.header("Uploading", f"{os.path.basename(local_path)} ({file_size} bytes)")

    with open(local_path, "rb") as f:
        put_r = requests.put(presigned_url, data=f, headers={"Content-Type": content_type})
        if put_r.status_code not in (200, 201):
            terminal.error(f"Upload failed: {put_r.status_code}")
            raise SystemExit(1)

    requests.post(
        f"{base}/{res.filesystem.id}/upload-complete",
        json={"path": remote_path},
        headers=headers,
    )

    terminal.success(f"Uploaded {local_path} -> {name}:{remote_path}")


@fs.command("download")
@click.argument("name")
@click.argument("remote_path")
@click.argument("local_path", default="")
@pass_service_client
def download(client: ServiceClient, name: str, remote_path: str, local_path: str):
    """Download a file from a filesystem.

    capsule fs download my-data /reports/report.csv ./report.csv
    """
    from ..clients.capsule import GetFilesystemRequest

    if not local_path:
        local_path = os.path.basename(remote_path)

    res = client.filesystems.get_filesystem(GetFilesystemRequest(name=name))
    if not res.ok:
        terminal.error(f"Filesystem not found: {res.err_msg}")
        raise SystemExit(1)

    base, headers = _http_base()

    r = requests.get(
        f"{base}/{res.filesystem.id}/download-url",
        params={"path": remote_path},
        headers=headers,
    )
    if r.status_code != 200:
        terminal.error(f"Get download URL failed: {r.text}")
        raise SystemExit(1)

    presigned_url = r.json().get("url")
    if not presigned_url:
        terminal.error("No download URL returned.")
        raise SystemExit(1)

    terminal.header("Downloading", f"{remote_path} -> {local_path}")

    dl = requests.get(presigned_url, stream=True)
    if dl.status_code != 200:
        terminal.error(f"Download failed: {dl.status_code}")
        raise SystemExit(1)

    with open(local_path, "wb") as f:
        for chunk in dl.iter_content(chunk_size=8192):
            f.write(chunk)

    terminal.success(f"Downloaded {name}:{remote_path} -> {local_path}")
