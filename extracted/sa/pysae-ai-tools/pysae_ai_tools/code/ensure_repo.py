"""Ensure a GitLab project is cloned locally and up to date.

Clones the project under ``<base-dir>/<project_path>`` if missing, otherwise
switches to the default branch (``origin/HEAD``, usually ``main``) and runs
``git pull --ff-only``. Uncommitted changes are stashed and restored by
default; pass ``--no-stash`` to discard them instead. Outputs JSON with the
absolute local path and a status code so skills can chain on it.

Usage:
    pysae-ai-tools code ensure-repo pysae/api
    pysae-ai-tools code ensure-repo pysae/api --base-dir /tmp/work
    pysae-ai-tools code ensure-repo pysae/api --no-pull --protocol ssh
    pysae-ai-tools code ensure-repo pysae/api --keep-branch
    pysae-ai-tools code ensure-repo pysae/api --no-stash

By default the command switches to the default branch — support skills want
``main`` so they read the source of truth, not whatever feature branch the
user happened to leave checked out. Use ``--keep-branch`` to preserve the
current branch (debug, advanced workflows).

``--no-stash`` is destructive: any uncommitted change in the working tree
is discarded (``git reset --hard`` + ``git clean -fd``) before the update.
Reserved for explicit user invocation — the support skills never pass it,
to avoid losing work even in clones that "should not" have manual edits.

The default base directory is resolved in this priority order:
1. ``PYSAE_AI_TOOLS_GIT_CLONE_DIR`` environment variable (when set)
2. ``git_clone_dir`` key in ``~/.config/pysae-ai-tools/config.toml``
   (auto-appended to the file on first read)
3. **Interactive prompt** (if stdin is a TTY): asks where to clone
   projects, persists the answer to the config file
4. OS-standard data directory (``~/.local/share/pysae-ai-tools/projects``
   on Linux, ``~/Library/Application Support/pysae-ai-tools/projects`` on
   macOS, ``~/AppData/Local/pysae-ai-tools/projects`` on Windows) — used
   as silent fallback in non-interactive contexts (CI, pipes)

The base dir is created if it doesn't exist.
"""

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer

from ..common.git import (
    current_branch,
    default_branch,
    has_local_changes,
    run_git,
)

DEFAULT_BASE_DIR_ENV = "PYSAE_AI_TOOLS_GIT_CLONE_DIR"


@dataclass
class EnsureResult:
    project_path: str
    local_path: str
    # "cloned" | "pulled" | "already-up-to-date" | "not-git" | "clone-error"
    # | "fetch-error" | "stash-error" | "discard-error" | "checkout-error"
    # | "pull-conflict" | "pulled-stash-conflict"
    status: str
    branch: str | None
    detail: str = ""


def _default_base_dir() -> Path:
    raw = os.environ.get(DEFAULT_BASE_DIR_ENV)
    if raw:
        return Path(raw).expanduser()

    from ..config import load_config, os_default_clone_dir, set_git_clone_dir

    cfg_value = load_config().git_clone_dir
    if cfg_value:
        return Path(cfg_value).expanduser()

    os_default = os_default_clone_dir()

    # Interactive prompt only if stdin is a real TTY (skip in CI, pipes, etc.)
    if sys.stdin.isatty():
        try:
            print(
                "📂 Premier usage : où veux-tu cloner les projets Pysae ?",
                file=sys.stderr,
            )
            print(f"   Défaut OS : {os_default}", file=sys.stderr)
            answer = input("   Chemin (Entrée = défaut OS) : ").strip()
        except (EOFError, KeyboardInterrupt):
            answer = ""
        chosen = Path(answer).expanduser() if answer else os_default
        set_git_clone_dir(str(chosen))
        print(f"✅ Sauvegardé dans la config : {chosen}", file=sys.stderr)
        from .claude_perms import interactive_offer as _claude_perms_offer

        _claude_perms_offer(chosen)
        return chosen

    return os_default


def _build_clone_url(project_path: str, protocol: str) -> str:
    if protocol == "ssh":
        return f"git@gitlab.com:{project_path}.git"
    return f"https://gitlab.com/{project_path}.git"


def _update(repo_dir: Path, keep_branch: bool, no_stash: bool) -> tuple[str, str]:
    """Fetch + (optionally checkout default branch) + pull --ff-only + restore stash.

    A dirty working tree must never block the update — the support skills
    rely on a current copy. By default we stash (including untracked),
    optionally switch to the default branch (``origin/HEAD``), fast-forward
    pull, then pop. The pop happens on the destination branch so the user
    keeps their changes available, even when we switched branches.

    With ``no_stash=True`` the dirty changes are discarded before the update
    (``git reset --hard`` + ``git clean -fd``) — destructive, exposed for
    explicit user use only. Skills never pass this to avoid losing work.

    On any failure we restore the stash (when possible) so no work is lost.
    Conflicts during pop leave the stash in the stack, surfaced via the
    ``pulled-stash-conflict`` status.
    """
    fetch = run_git(repo_dir, "fetch", "--prune", "--quiet", timeout=60)
    if fetch.returncode != 0:
        return "fetch-error", fetch.stderr.strip()[:200]

    target_branch: str | None = None
    if not keep_branch:
        default = default_branch(repo_dir)
        current = current_branch(repo_dir)
        if default and current and current != default:
            target_branch = default

    stashed = False
    discarded = False
    if has_local_changes(repo_dir):
        if no_stash:
            reset = run_git(repo_dir, "reset", "--hard", "HEAD", "--quiet", timeout=30)
            if reset.returncode != 0:
                return "discard-error", reset.stderr.strip()[:200]
            clean = run_git(repo_dir, "clean", "-fd", "--quiet", timeout=30)
            if clean.returncode != 0:
                return "discard-error", clean.stderr.strip()[:200]
            discarded = True
        else:
            stash_message = "pysae-ai-tools ensure-repo: auto-stash before update"
            stash = run_git(
                repo_dir,
                "stash",
                "push",
                "--include-untracked",
                "--quiet",
                "--message",
                stash_message,
                timeout=30,
            )
            if stash.returncode != 0:
                return "stash-error", stash.stderr.strip()[:200]
            stashed = True

    branch_switched = False
    if target_branch is not None:
        co = run_git(repo_dir, "checkout", target_branch, "--quiet", timeout=30)
        if co.returncode != 0:
            if stashed:
                run_git(repo_dir, "stash", "pop", "--quiet", timeout=30)
            return "checkout-error", co.stderr.strip()[:200]
        branch_switched = True

    before = run_git(repo_dir, "rev-parse", "HEAD", timeout=10).stdout.strip()
    pull = run_git(repo_dir, "pull", "--ff-only", "--quiet", timeout=60)
    if pull.returncode != 0:
        if stashed:
            run_git(repo_dir, "stash", "pop", "--quiet", timeout=30)
        return "pull-conflict", pull.stderr.strip()[:200]
    after = run_git(repo_dir, "rev-parse", "HEAD", timeout=10).stdout.strip()
    pulled = before != after

    if stashed:
        pop = run_git(repo_dir, "stash", "pop", "--quiet", timeout=30)
        if pop.returncode != 0:
            return (
                "pulled-stash-conflict",
                f"pulled {before[:7]}..{after[:7]} but `git stash pop` conflicted: " f"{pop.stderr.strip()[:150]}",
            )

    parts: list[str] = []
    if branch_switched:
        parts.append(f"switched to {target_branch}")
    if pulled:
        parts.append(f"{before[:7]}..{after[:7]}")
    if discarded:
        parts.append("discarded uncommitted changes")
    elif stashed:
        parts.append("stashed and restored")

    if not branch_switched and not pulled:
        return "already-up-to-date", ", ".join(parts)
    return "pulled", ", ".join(parts)


def ensure_repo(
    project_path: str,
    base_dir: Path,
    protocol: str = "https",
    pull: bool = True,
    keep_branch: bool = False,
    no_stash: bool = False,
) -> EnsureResult:
    """Clone the project if missing, or update it if already present.

    ``project_path`` is the GitLab path-with-namespace (e.g. ``pysae/api`` or
    ``pysae/shift/app``). The result's ``local_path`` is always the absolute
    path, even if nothing was changed.

    By default, an existing repo is switched to its default branch
    (``origin/HEAD``) before the pull. Pass ``keep_branch=True`` to preserve
    the currently checked-out branch.

    By default, uncommitted changes are stashed and restored after the pull.
    Pass ``no_stash=True`` to discard them instead — destructive, exposed
    for explicit user invocation only.
    """
    base_dir = base_dir.expanduser().resolve()
    base_dir.mkdir(parents=True, exist_ok=True)

    repo_dir = base_dir / project_path

    if not repo_dir.exists():
        url = _build_clone_url(project_path, protocol)
        repo_dir.parent.mkdir(parents=True, exist_ok=True)
        clone = subprocess.run(
            ["git", "clone", "--quiet", url, str(repo_dir)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=600,
        )
        if clone.returncode != 0:
            return EnsureResult(
                project_path=project_path,
                local_path=str(repo_dir),
                status="clone-error",
                branch=None,
                detail=clone.stderr.strip()[:200],
            )
        return EnsureResult(
            project_path=project_path,
            local_path=str(repo_dir),
            status="cloned",
            branch=current_branch(repo_dir),
        )

    if not (repo_dir / ".git").is_dir():
        return EnsureResult(
            project_path=project_path,
            local_path=str(repo_dir),
            status="not-git",
            branch=None,
            detail="directory exists but is not a git repository",
        )

    if not pull:
        return EnsureResult(
            project_path=project_path,
            local_path=str(repo_dir),
            status="already-up-to-date",
            branch=current_branch(repo_dir),
            detail="--no-pull: pull skipped",
        )

    status, detail = _update(repo_dir, keep_branch=keep_branch, no_stash=no_stash)
    return EnsureResult(
        project_path=project_path,
        local_path=str(repo_dir),
        status=status,
        branch=current_branch(repo_dir),
        detail=detail,
    )


app = typer.Typer()


@app.command()
def main(
    project_path: Annotated[
        str,
        typer.Argument(help="GitLab project path with namespace (e.g. pysae/api, pysae/shift/app)"),
    ],
    base_dir: Annotated[
        Path | None,
        typer.Option(
            "--base-dir",
            help=f"Base directory for clones (default: ${DEFAULT_BASE_DIR_ENV} or ~/projects)",
        ),
    ] = None,
    protocol: Annotated[
        str,
        typer.Option("--protocol", help="Git protocol: ssh or https"),
    ] = "https",
    no_pull: Annotated[
        bool,
        typer.Option("--no-pull", help="Skip git pull if the repo already exists"),
    ] = False,
    keep_branch: Annotated[
        bool,
        typer.Option(
            "--keep-branch",
            help="Do not switch to the default branch — pull on the currently checked-out branch",
        ),
    ] = False,
    no_stash: Annotated[
        bool,
        typer.Option(
            "--no-stash",
            help="Discard uncommitted changes instead of stashing them (destructive)",
        ),
    ] = False,
) -> None:
    """Clone the project if missing, otherwise switch to default branch and fast-forward pull."""
    base = base_dir if base_dir is not None else _default_base_dir()
    result = ensure_repo(
        project_path,
        base_dir=base,
        protocol=protocol,
        pull=not no_pull,
        keep_branch=keep_branch,
        no_stash=no_stash,
    )
    print(
        json.dumps(
            {
                "project_path": result.project_path,
                "local_path": result.local_path,
                "status": result.status,
                "branch": result.branch,
                "detail": result.detail,
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    fatal = {
        "clone-error",
        "fetch-error",
        "stash-error",
        "discard-error",
        "checkout-error",
        "pull-conflict",
        "pulled-stash-conflict",
        "not-git",
    }
    if result.status in fatal:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
