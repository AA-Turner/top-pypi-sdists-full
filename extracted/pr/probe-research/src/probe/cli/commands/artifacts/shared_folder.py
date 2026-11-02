"""probe shared list/add/share/unshare/download/delete: the team's Shared folder."""

from __future__ import annotations
import os

import typer
from ....sdk.artifact.anchors import Anchor
from ....sdk.artifact.filetype import name_with_extension


# -- shared folder ----------------------------------------------------------
shared_app = typer.Typer(no_args_is_help=True, help="the team's Shared folder")


@shared_app.command("list")
def shared_list() -> None:
    """List the team's Shared files."""
    with _client() as c:
        _print_json(c.list_anchored(Anchor.SHARED))


@shared_app.command("add")
def shared_add(
    path: str = typer.Argument(..., help="local file to upload"),
    name: str = typer.Option(None, "--name", help="defaults to the file's basename"),
    content_type: str = typer.Option(None, "--content-type"),
) -> None:
    """Upload a file straight into the team's Shared folder."""
    resolved = name_with_extension(name or os.path.basename(path), path)
    with _client() as c:
        _print_json(c.upload_file(Anchor.SHARED, None, resolved, path, content_type=content_type))


@shared_app.command("share")
def shared_share(
    artifact_id: str = typer.Argument(..., help="a workspace file id"),
    replace: bool = typer.Option(
        False, "--replace", help="supersede a same-named file already in Shared"
    ),
) -> None:
    """Move one of your workspace files into the team's Shared folder.

    A MOVE, not a copy: the file leaves your workspace listing. Ownership transfers
    and the search index is re-keyed in the same transaction.

    A name already taken in Shared is a 409 — the server never silently supersedes
    someone else's file. Pass --replace to do it deliberately.
    """
    with _client() as c:
        _print_json(c.share_workspace_file(artifact_id, replace=replace))


@shared_app.command("unshare")
def shared_unshare(
    artifact_id: str = typer.Argument(..., help="a shared file id"),
    replace: bool = typer.Option(
        False, "--replace", help="supersede a same-named file in the default workspace"
    ),
) -> None:
    """Move a Shared file into the server default workspace."""
    with _client() as c:
        _print_json(c.unshare_file(artifact_id, replace=replace))


@shared_app.command("download")
def shared_download(
    artifact_id: str = typer.Argument(..., help="a shared file id"),
) -> None:
    """Print a presigned download URL for a Shared file."""
    with _client() as c:
        _print_json(c.download_shared_file(artifact_id))


@shared_app.command("delete")
def shared_delete(
    artifact_id: str = typer.Argument(..., help="a shared file id"),
) -> None:
    """Remove a file from the Shared folder (soft delete; recoverable)."""
    with _client() as c:
        c.delete_shared_file(artifact_id)
    print(f"shared file {artifact_id} deleted")
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
