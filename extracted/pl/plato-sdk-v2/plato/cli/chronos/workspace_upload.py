"""Chronos workspace upload commands."""

from __future__ import annotations

import os
import subprocess
import tarfile
import tempfile
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, BinaryIO

import httpx
import typer

from plato.chronos.api.sessions import get_session_workspace_download_url, get_session_workspace_upload_url
from plato.cli.chronos.settings import get_settings
from plato.cli.utils import console
from plato.git_ops.repo import trust_git_directory

workspace_app = typer.Typer(help="Workspace utilities.")
workspace_upload_app = typer.Typer(help="Upload workspace snapshots.")
workspace_app.add_typer(workspace_upload_app, name="upload")

_CHUNK_SIZE = 256 * 1024
_PLATO_GIT_ENV = {
    "GIT_AUTHOR_NAME": "Plato",
    "GIT_AUTHOR_EMAIL": "plato@plato.dev",
    "GIT_COMMITTER_NAME": "Plato",
    "GIT_COMMITTER_EMAIL": "plato@plato.dev",
}


@dataclass(frozen=True, slots=True)
class GitWorkspaceArchive:
    path: Path
    head_sha: str
    size_bytes: int


class _FileStream:
    """Reusable file stream for httpx request bodies."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def __iter__(self) -> Iterator[bytes]:
        with self.path.open("rb") as handle:
            yield from _read_chunks(handle)


def _read_chunks(handle: BinaryIO) -> Iterator[bytes]:
    while True:
        chunk = handle.read(_CHUNK_SIZE)
        if not chunk:
            break
        yield chunk


def _run_git(args: list[str], *, cwd: Path | None = None) -> str:
    env = {**os.environ, **_PLATO_GIT_ENV}
    result = subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        command = " ".join(["git", *args])
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"{command} failed: {detail}")
    return result.stdout.strip()


def _is_git_workspace_root(path: Path) -> bool:
    return (path / "repo" / ".git").is_dir() and (path / ".git-bare" / "HEAD").exists()


def _require_git_workspace_root(path: Path) -> tuple[Path, Path]:
    root = path.expanduser().resolve()
    if _is_git_workspace_root(root):
        return root / "repo", root / ".git-bare"
    if (root / ".git").is_dir() and root.name == "repo" and (root.parent / ".git-bare" / "HEAD").exists():
        return root, root.parent / ".git-bare"
    raise ValueError(
        "Expected a git workspace root containing repo/ and .git-bare/, or the repo/ directory inside that workspace."
    )


def _ensure_bare_push_settings(bare_dir: Path) -> None:
    _run_git(["--git-dir", str(bare_dir), "config", "receive.unpackLimit", "100000"])
    _run_git(["--git-dir", str(bare_dir), "config", "transfer.unpackLimit", "100000"])


def _set_origin_to_bare(repo_dir: Path, bare_dir: Path) -> None:
    relative_bare = os.path.relpath(bare_dir, start=repo_dir)
    remotes = _run_git(["remote"], cwd=repo_dir).splitlines()
    if "origin" in remotes:
        _run_git(["remote", "set-url", "origin", relative_bare], cwd=repo_dir)
    else:
        _run_git(["remote", "add", "origin", relative_bare], cwd=repo_dir)


def _sync_repo_to_bare(repo_dir: Path, bare_dir: Path, *, commit_message: str) -> str:
    trust_git_directory(repo_dir)
    trust_git_directory(bare_dir)
    _ensure_bare_push_settings(bare_dir)
    _run_git(["config", "user.email", _PLATO_GIT_ENV["GIT_AUTHOR_EMAIL"]], cwd=repo_dir)
    _run_git(["config", "user.name", _PLATO_GIT_ENV["GIT_AUTHOR_NAME"]], cwd=repo_dir)
    _set_origin_to_bare(repo_dir, bare_dir)
    _run_git(["add", "-A"], cwd=repo_dir)
    status = _run_git(["status", "--porcelain"], cwd=repo_dir)
    if status:
        _run_git(["commit", "-m", commit_message], cwd=repo_dir)
    _run_git(["push", "--force", str(bare_dir), "HEAD:refs/heads/main"], cwd=repo_dir)
    _run_git(["--git-dir", str(bare_dir), "symbolic-ref", "HEAD", "refs/heads/main"])
    return _run_git(["--git-dir", str(bare_dir), "rev-parse", "main"])


def create_git_workspace_archive(
    source: Path,
    *,
    commit_message: str = "Upload Chronos git workspace",
    output: Path | None = None,
) -> GitWorkspaceArchive:
    """Push repo/ to .git-bare and tar the git workspace root."""
    repo_dir, bare_dir = _require_git_workspace_root(source)
    workspace_root = bare_dir.parent
    head_sha = _sync_repo_to_bare(repo_dir, bare_dir, commit_message=commit_message)

    if output is None:
        tmp = tempfile.NamedTemporaryFile(prefix="plato-git-workspace-", suffix=".tar", delete=False)
        archive_path = Path(tmp.name)
        tmp.close()
    else:
        archive_path = output.expanduser().resolve()
        archive_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with tarfile.open(archive_path, "w") as tar:
            tar.add(workspace_root / ".git-bare", arcname=".git-bare", recursive=True)
            tar.add(workspace_root / "repo", arcname="repo", recursive=True)
    except Exception:
        if output is None:
            archive_path.unlink(missing_ok=True)
        raise

    return GitWorkspaceArchive(path=archive_path, head_sha=head_sha, size_bytes=archive_path.stat().st_size)


def upload_git_workspace_archive(
    archive: Path,
    *,
    session_id: str,
    name: str,
    chronos_url: str,
    api_key: str,
    timeout: float = 60.0,
) -> None:
    with httpx.Client(base_url=chronos_url.rstrip("/"), timeout=timeout, headers={"X-API-Key": api_key}) as client:
        payload = get_session_workspace_upload_url.sync(client, public_id=session_id, name=name)
        upload_url = payload["url"]
    headers = {
        "Content-Type": "application/x-tar",
        "Content-Length": str(archive.stat().st_size),
    }
    with httpx.Client(timeout=max(timeout, 300.0)) as client:
        response = client.put(upload_url, content=_FileStream(archive), headers=headers)
        response.raise_for_status()


def download_session_workspace_archive(
    destination: Path,
    *,
    session_id: str,
    name: str,
    chronos_url: str,
    api_key: str,
    timeout: float = 60.0,
) -> int:
    with httpx.Client(base_url=chronos_url.rstrip("/"), timeout=timeout, headers={"X-API-Key": api_key}) as client:
        payload = get_session_workspace_download_url.sync(client, public_id=session_id, name=name)
        download_url = payload["url"]
    destination.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    with httpx.Client(timeout=max(timeout, 300.0)) as client:
        with client.stream("GET", download_url) as response:
            response.raise_for_status()
            with destination.open("wb") as handle:
                for chunk in response.iter_bytes(_CHUNK_SIZE):
                    handle.write(chunk)
                    total += len(chunk)
    return total


@workspace_upload_app.command("git")
def upload_git(
    session_id: Annotated[str, typer.Argument(help="Chronos session ID")],
    source: Annotated[
        Path,
        typer.Argument(
            help="Git workspace root containing repo/ and .git-bare/, or the repo/ directory inside it.",
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
        ),
    ] = Path("."),
    name: Annotated[str, typer.Option("--name", help="Session workspace object name")] = "workspace",
    commit_message: Annotated[str, typer.Option("--message", "-m", help="Auto-commit message")] = (
        "Upload Chronos git workspace"
    ),
    output: Annotated[
        Path | None, typer.Option("--output-archive", help="Also write the generated tar to this path")
    ] = (None),
    keep_archive: Annotated[bool, typer.Option("--keep-archive", help="Keep the temporary tar after upload")] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Create the tar and skip Chronos upload")] = False,
    chronos_url: Annotated[
        str | None, typer.Option("--url", "-u", envvar="CHRONOS_URL", help="Chronos API URL")
    ] = None,
    api_key: Annotated[
        str | None,
        typer.Option("--api-key", "-k", envvar="PLATO_API_KEY", help="Plato API key for authentication"),
    ] = None,
) -> None:
    """Upload a git-backed workspace tarball for a Chronos session."""
    resolved_api_key = api_key or os.environ.get("PLATO_API_KEY")
    if not dry_run and not resolved_api_key:
        console.print("[red]No API key provided[/red]")
        console.print("Set PLATO_API_KEY environment variable or use --api-key")
        raise typer.Exit(1)

    archive: GitWorkspaceArchive | None = None
    try:
        archive = create_git_workspace_archive(
            source,
            commit_message=commit_message,
            output=output,
        )
        if dry_run:
            console.print(f"[green]Created git workspace archive[/green] {archive.path}")
        else:
            upload_git_workspace_archive(
                archive.path,
                session_id=session_id,
                name=name,
                chronos_url=chronos_url or get_settings().chronos_url,
                api_key=resolved_api_key or "",
            )
            console.print(f"[green]Uploaded git workspace[/green] {archive.head_sha[:12]}")
        console.print(f"[dim]Archive size: {archive.size_bytes / 1024 / 1024:.1f} MB[/dim]")
    except Exception as exc:
        console.print(f"[red]Failed: {exc}[/red]")
        raise typer.Exit(1) from exc
    finally:
        if archive is not None and output is None and not keep_archive and not dry_run:
            archive.path.unlink(missing_ok=True)
