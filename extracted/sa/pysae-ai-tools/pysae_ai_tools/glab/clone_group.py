#!/usr/bin/env python3
"""Clone all repositories from a GitLab group and its subgroups.

For each project found:
- If the directory does not exist: clone it.
- If it exists and is a git repo: verify the remote URL matches, fix it if needed, then pull.
- If it exists but is not a git repo: skip with a warning.

Usage:
    pysae-ai-tools clone_group.clone [OPTIONS]

Examples:
    pysae-ai-tools clone_group.clone
    pysae-ai-tools clone_group.clone --base-dir ~/projects
    pysae-ai-tools clone_group.clone --protocol https --dry-run
"""

import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Any

import typer

from ..common.git import (
    current_branch,
    default_branch,
    get_remote_url,
    has_local_changes,
    normalize_url,
    remote_branch_exists,
    set_remote_url,
    tracking_branch,
)
from ..common.glab.fetch_issues import glab_api_paginated
from ..common.group import resolve_group, resolve_group_id


@dataclass
class Project:
    """A GitLab project with its full path."""

    id: int
    path_with_namespace: str
    ssh_url: str
    http_url: str
    archived: bool

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Project":
        return cls(
            id=data["id"],
            path_with_namespace=data["path_with_namespace"],
            ssh_url=data.get("ssh_url_to_repo", ""),
            http_url=data.get("http_url_to_repo", ""),
            archived=data.get("archived", False),
        )

    def url(self, protocol: str) -> str:
        return self.ssh_url if protocol == "ssh" else self.http_url


def fetch_all_projects(
    group_id: int,
    include_archived: bool = False,
    include_read_only: bool = False,
) -> list[Project]:
    """Fetch all projects in a group and its subgroups via glab API.

    By default, skips archived projects and projects the current user cannot
    push to (access level below Developer = 30).
    """
    endpoint = f"groups/{group_id}/projects?include_subgroups=true&per_page=100"
    if not include_archived:
        endpoint += "&archived=false"
    if not include_read_only:
        endpoint += "&min_access_level=30"
    raw = glab_api_paginated(endpoint)
    return [Project.from_api(p) for p in raw]


def _checkout_default_branch_if_needed(repo_dir: Path) -> str | None:
    """If the current branch tracks a deleted remote branch, checkout the default branch.

    Returns the name of the branch switched to, or None if no switch was needed.
    """
    current = current_branch(repo_dir)
    if current is None:
        return None  # detached HEAD, skip

    default = default_branch(repo_dir)
    if default is None:
        return None

    if current == default:
        return None  # already on default branch

    # Check if the current branch's upstream still exists on the remote
    tracking = tracking_branch(repo_dir)
    if tracking is not None and remote_branch_exists(repo_dir, tracking.removeprefix("origin/")):
        return None  # upstream exists, no need to switch

    # Upstream is gone or not set — switch to default branch
    result = subprocess.run(
        ["git", "-C", str(repo_dir), "checkout", default],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    if result.returncode == 0:
        return default
    return None


def _do_pull(repo_dir: Path) -> str:
    """Pull with rebase, stashing local changes if needed.

    If rebase conflicts, aborts the rebase to leave the repo clean.
    Returns 'pulled', 'pulled (stashed)', or 'pull-error: ...'.
    """
    stashed = False
    try:
        # Stash local changes if any
        if has_local_changes(repo_dir):
            stash_result = subprocess.run(
                ["git", "-C", str(repo_dir), "stash", "--include-untracked"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
            )
            if stash_result.returncode != 0:
                return f"pull-error: stash failed -- {stash_result.stderr.strip()[:60]}"
            stashed = True

        # Pull with rebase
        result = subprocess.run(
            ["git", "-C", str(repo_dir), "pull", "--rebase", "--quiet"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )

        if result.returncode != 0:
            # Abort rebase to leave repo clean
            subprocess.run(
                ["git", "-C", str(repo_dir), "rebase", "--abort"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=10,
            )
            # Restore stashed changes
            if stashed:
                subprocess.run(
                    ["git", "-C", str(repo_dir), "stash", "pop"],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=10,
                )
            return f"pull-conflict: rebase aborted -- {result.stderr.strip()[:60]}"

        # Restore stashed changes
        if stashed:
            pop_result = subprocess.run(
                ["git", "-C", str(repo_dir), "stash", "pop"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=10,
            )
            if pop_result.returncode != 0:
                return f"pulled but stash-pop-conflict: {pop_result.stderr.strip()[:60]}"
            return "pulled (stashed)"

        return "pulled"
    except subprocess.TimeoutExpired:
        if stashed:
            subprocess.run(
                ["git", "-C", str(repo_dir), "rebase", "--abort"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=10,
            )
            subprocess.run(
                ["git", "-C", str(repo_dir), "stash", "pop"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=10,
            )
        return "pull-error: timeout"


def process_project(project: Project, base_dir: Path, protocol: str, dry_run: bool) -> str:
    """Process a single project: clone if missing, or verify remote and pull if existing.

    Returns a status string.
    """
    repo_dir = base_dir / project.path_with_namespace
    expected_url = project.url(protocol)

    if not expected_url:
        return "error: no URL"

    # Case 1: directory does not exist -> clone
    if not repo_dir.exists():
        if dry_run:
            return "would clone"
        repo_dir.parent.mkdir(parents=True, exist_ok=True)
        try:
            result = subprocess.run(
                ["git", "clone", "--quiet", expected_url, str(repo_dir)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=300,
            )
            if result.returncode == 0:
                return "cloned"
            return f"clone-error: {result.stderr.strip()[:100]}"
        except subprocess.TimeoutExpired:
            return "clone-error: timeout"

    # Case 2: directory exists but is not a git repo
    if not (repo_dir / ".git").is_dir():
        return "skipped: not a git repo"

    # Case 3: directory exists and is a git repo -> check remote
    current_url = get_remote_url(repo_dir)
    remote_status = ""

    if current_url is None:
        if dry_run:
            return "would add remote"
        subprocess.run(
            ["git", "-C", str(repo_dir), "remote", "add", "origin", expected_url],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
        remote_status = "remote-added"
    elif normalize_url(current_url) != normalize_url(expected_url):
        if dry_run:
            return f"would fix remote: {current_url} -> {expected_url}"
        set_remote_url(repo_dir, expected_url)
        remote_status = f"remote-fixed: {current_url} -> {expected_url}"
    else:
        remote_status = "remote-ok"

    # Fetch to update remote refs before checking branch state
    subprocess.run(
        ["git", "-C", str(repo_dir), "fetch", "--prune", "--quiet"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )

    # Switch to default branch if current branch tracks a deleted remote branch
    switched_to = _checkout_default_branch_if_needed(repo_dir)
    branch_note = f", switched to {switched_to}" if switched_to else ""

    # Pull
    if dry_run:
        return f"would pull ({remote_status}{branch_note})"
    pull_status = _do_pull(repo_dir)
    return f"{pull_status} ({remote_status}{branch_note})"


STATUS_SYMBOLS: dict[str, str] = {
    "cloned": "+",
    "pulled": "=",
    "would clone": "?",
    "would pull": "~",
}


def _find_orphan_repos(base_dir: Path, group: str, known_paths: set[str]) -> list[Path]:
    """Walk base_dir/<group>/ to find top-level git repos that aren't in known_paths.

    Descends into directories, stopping at the first ``.git`` found on each path
    (so nested repos like ``.terraform/modules/*`` are not reported). A repo is
    identified by its path relative to base_dir (e.g. 'pysae/tools/ai-tools').
    """
    group_root = base_dir / group
    if not group_root.is_dir():
        return []

    orphans: list[Path] = []
    stack: list[Path] = [group_root]
    while stack:
        current = stack.pop()
        if (current / ".git").is_dir():
            rel = current.relative_to(base_dir).as_posix()
            if rel not in known_paths:
                orphans.append(current)
            continue  # don't descend into a git repo
        try:
            for entry in current.iterdir():
                if entry.is_dir() and not entry.is_symlink():
                    stack.append(entry)
        except PermissionError:
            continue
    return sorted(orphans)


def _prompt_confirm(prompt: str) -> bool:
    """Prompt the user for y/N confirmation on stdin. Returns True if confirmed."""
    try:
        answer = input(prompt).strip().lower()
    except EOFError:
        return False
    return answer in {"y", "yes", "o", "oui"}


def _delete_repo(repo_dir: Path) -> bool:
    """Delete a repo directory recursively. Returns True on success."""
    try:
        shutil.rmtree(repo_dir)
        return True
    except OSError as exc:
        print(f"  error: {exc}", file=sys.stderr)
        return False


cli = typer.Typer()


@cli.command()
def main(
    base_dir: Annotated[
        str,
        typer.Option("--base-dir", help="Base directory for cloning (default: ~/projects)"),
    ] = str(Path.home() / "projects"),
    group: Annotated[
        str | None,
        typer.Option("--group", help="GitLab group path (default: resolved from origin / env / 'pysae')."),
    ] = None,
    group_id: Annotated[
        int | None,
        typer.Option("--group-id", help="GitLab group ID (default: resolved live from the group path)."),
    ] = None,
    protocol: Annotated[
        str,
        typer.Option("--protocol", help="Git protocol for cloning: ssh or https (default: https)"),
    ] = "https",
    include_archived: Annotated[
        bool,
        typer.Option("--include-archived", help="Include archived repositories"),
    ] = False,
    include_read_only: Annotated[
        bool,
        typer.Option(
            "--include-read-only",
            help="Include projects where the user has no push rights (default: skip)",
        ),
    ] = False,
    prune: Annotated[
        bool,
        typer.Option(
            "--prune",
            help="After syncing, delete local repos that no longer exist or are no longer accessible remotely",
        ),
    ] = False,
    yes: Annotated[
        bool,
        typer.Option("--yes", "-y", help="Auto-confirm prune deletions (no prompt)"),
    ] = False,
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Show what would be done without actually cloning/pulling"),
    ] = False,
) -> None:
    """Clone all GitLab repos from a group, preserving subgroup structure."""
    base_path = Path(base_dir)
    group = group or resolve_group()
    try:
        group_id = group_id if group_id is not None else resolve_group_id(group)
    except RuntimeError as exc:
        print(f"✗ {exc}", file=sys.stderr)
        raise typer.Exit(code=1) from None
    print(f"Fetching projects from group {group} (ID: {group_id})...", file=sys.stderr)

    projects = fetch_all_projects(
        group_id,
        include_archived=include_archived,
        include_read_only=include_read_only,
    )
    projects.sort(key=lambda p: p.path_with_namespace)

    print(f"Found {len(projects)} projects.", file=sys.stderr)

    results: dict[str, list[str]] = {}
    for i, project in enumerate(projects, 1):
        status = process_project(project, base_path, protocol, dry_run)
        # Group by simplified status (strip details after colon for summary)
        key = status.split("(")[0].strip() if "(" in status else status
        results.setdefault(key, []).append(project.path_with_namespace)
        # Pick symbol
        symbol = "!"
        for prefix, sym in STATUS_SYMBOLS.items():
            if status.startswith(prefix):
                symbol = sym
                break
        print(f"  [{i}/{len(projects)}] {symbol} {project.path_with_namespace} -- {status}", file=sys.stderr)

    # Prune: find local repos that no longer match any accessible remote project
    pruned: list[str] = []
    prune_skipped: list[str] = []
    if prune:
        known_paths = {p.path_with_namespace for p in projects}
        orphans = _find_orphan_repos(base_path, group, known_paths)
        if orphans:
            print(f"\nFound {len(orphans)} orphan local repo(s) (no longer accessible):", file=sys.stderr)
            for orphan in orphans:
                rel = orphan.relative_to(base_path).as_posix()
                print(f"  - {rel}", file=sys.stderr)

            if dry_run:
                prune_skipped = [p.relative_to(base_path).as_posix() for p in orphans]
                print("  (dry-run: nothing deleted)", file=sys.stderr)
            else:
                for orphan in orphans:
                    rel = orphan.relative_to(base_path).as_posix()
                    if yes or _prompt_confirm(f"Delete {rel}? [y/N] "):
                        if _delete_repo(orphan):
                            pruned.append(rel)
                            print(f"  deleted: {rel}", file=sys.stderr)
                    else:
                        prune_skipped.append(rel)
        else:
            print("\nNo orphan local repos to prune.", file=sys.stderr)

    # Summary as JSON to stdout
    summary: dict[str, Any] = {
        "base_dir": str(base_path),
        "group": group,
        "total": len(projects),
        "results": {k: len(v) for k, v in sorted(results.items())},
        "projects": {k: sorted(v) for k, v in sorted(results.items())},
    }
    if prune:
        summary["pruned"] = sorted(pruned)
        summary["prune_skipped"] = sorted(prune_skipped)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    cli()
