"""Install Arraylake Agent Skills into agent-specific skill directories.

Skills follow the open Agent Skills spec (https://agentskills.io) and are
hosted as static content on the Earthmover docs site. This command fetches
the manifest, downloads each skill's files, and writes them into the
directories agent skill loaders read from:

- `~/.claude/skills/`  (Claude Code, opencode via compat shim)
- `~/.agents/skills/`  (Codex, Cursor, Gemini CLI, and others)

With `--project`, installs into `.claude/skills/` and `.agents/skills/`
under the current working directory instead.

Skill content ships independently of the `arraylake` client release. Re-run
`arraylake skills install` to pick up new content; no `pip install -U`
required.
"""

from __future__ import annotations

import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

import httpx
import typer
from packaging.version import InvalidVersion, Version

import arraylake
from arraylake.cli.utils import rich_console
from arraylake.config import config

app = typer.Typer(help="Install Arraylake Agent Skills for AI coding agents")

DEFAULT_SKILLS_URI = "https://docs.earthmover.io/skills"


@dataclass(frozen=True)
class SkillEntry:
    name: str
    version: str
    min_client_version: str | None
    description: str
    files: tuple[str, ...]


def _target_dirs(project: bool) -> list[Path]:
    base = Path.cwd() if project else Path.home()
    return [base / ".claude" / "skills", base / ".agents" / "skills"]


def _skills_uri() -> str:
    uri: str = config.get("skills.uri", DEFAULT_SKILLS_URI)
    return uri.rstrip("/")


def _client_version_ok(min_required: str | None) -> bool:
    if not min_required:
        return True
    try:
        return Version(arraylake.__version__) >= Version(min_required)
    except InvalidVersion:
        # Treat unparseable client versions (e.g. local dev builds without
        # a tag) as "good enough" — don't block users on tooling weirdness.
        return True


def _parse_manifest(payload: dict) -> list[SkillEntry]:
    entries: list[SkillEntry] = []
    for raw in payload.get("skills", []):
        entries.append(
            SkillEntry(
                name=raw["name"],
                version=str(raw.get("version", "0.0")),
                min_client_version=raw.get("min_client_version"),
                description=str(raw.get("description", "")),
                files=tuple(raw.get("files", [])),
            )
        )
    return entries


def _fetch_manifest(uri: str) -> list[SkillEntry]:
    url = f"{uri}/manifest.json"
    with httpx.Client(timeout=20.0, follow_redirects=True) as client:
        resp = client.get(url)
        resp.raise_for_status()
        return _parse_manifest(resp.json())


def _empty_temporary_sibling(dest: Path, prefix: str) -> Path:
    path = Path(tempfile.mkdtemp(prefix=prefix, dir=dest))
    path.rmdir()
    return path


def _remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)


def _install_skill(uri: str, entry: SkillEntry, dest: Path) -> str:
    """Download all of `entry.files` into `dest/<name>/...`.

    Returns one-word status: written | conflict.
    """
    skill_root = dest / entry.name
    if skill_root.exists() and not skill_root.is_dir():
        return "conflict"

    tmp_root = Path(tempfile.mkdtemp(prefix=".arraylake-skill-", dir=dest))
    backup_root: Path | None = None

    try:
        with httpx.Client(timeout=30.0, follow_redirects=True) as client:
            for rel in entry.files:
                if ".." in rel.split("/") or rel.startswith("/"):
                    raise RuntimeError(f"Refusing to write file outside skill root: {rel}")
                file_url = f"{uri}/{entry.name}/{rel}"
                resp = client.get(file_url)
                resp.raise_for_status()
                target = tmp_root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(resp.content)

        if skill_root.exists() or skill_root.is_symlink():
            # Pre-existing install, including legacy wheel-bundled symlinks.
            # Move it aside only after every replacement file has downloaded.
            backup_root = _empty_temporary_sibling(dest, ".arraylake-skill-backup-")
            skill_root.replace(backup_root)

        tmp_root.replace(skill_root)
        if backup_root is not None:
            _remove_path(backup_root)
            backup_root = None
        return "written"
    except Exception:
        if backup_root is not None and (backup_root.exists() or backup_root.is_symlink()):
            if skill_root.exists() or skill_root.is_symlink():
                _remove_path(skill_root)
            backup_root.replace(skill_root)
            backup_root = None
        raise
    finally:
        if tmp_root.exists() or tmp_root.is_symlink():
            _remove_path(tmp_root)


@app.command()
def install(
    project: bool = typer.Option(False, "--project", help="Install into the current directory instead of $HOME."),
    url: str | None = typer.Option(
        None,
        "--url",
        help=f"Override the skills server URL. Default: skills.uri config or {DEFAULT_SKILLS_URI}.",
    ),
) -> None:
    """**Install** Arraylake skills into agent skill directories.

    Default: user scope (`~/.claude/skills/` and `~/.agents/skills/`).
    With `--project`: project scope under the current working directory.

    Fetches the latest published skills from the Earthmover docs site
    (configurable via `--url` or the `skills.uri` config key). Re-run this
    to pick up content updates — they ship independently of the `arraylake`
    package release cycle.
    """
    uri = (url or _skills_uri()).rstrip("/")
    rich_console.print(f"Fetching skill manifest from [cyan]{uri}/manifest.json[/cyan]")
    try:
        entries = _fetch_manifest(uri)
    except httpx.HTTPError as err:
        rich_console.print(f"[red]Failed to fetch skills from {uri}: {err}[/red]")
        raise typer.Exit(code=1) from err

    if not entries:
        rich_console.print("[yellow]Manifest contained no skills; nothing to install.[/yellow]")
        return

    ok = True
    for target in _target_dirs(project):
        target.mkdir(parents=True, exist_ok=True)
        for entry in entries:
            if not _client_version_ok(entry.min_client_version):
                rich_console.print(
                    f"[yellow]skip[/yellow]    {target / entry.name} "
                    f"(skill requires arraylake>={entry.min_client_version}, "
                    f"installed {arraylake.__version__})"
                )
                continue
            try:
                status = _install_skill(uri, entry, target)
            except httpx.HTTPError as err:
                rich_console.print(f"[red]error[/red]   {target / entry.name}: {err}")
                ok = False
                continue
            if status == "conflict":
                ok = False
                rich_console.print(f"[yellow]skip[/yellow]    {target / entry.name} (path exists and is not a directory)")
            else:
                rich_console.print(f"[green]{status:8}[/green]{target / entry.name}")

    if not ok:
        rich_console.print("\n[yellow]One or more skills were skipped. Resolve the conflicts above and re-run.[/yellow]")
        raise typer.Exit(code=1)
