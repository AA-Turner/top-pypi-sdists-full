"""plato hillclimb — launch an interactive hillclimb session with Claude Code."""

from __future__ import annotations

import os
import shutil
import subprocess

import typer

from plato.cli.utils import console

hillclimb_app = typer.Typer(help="Launch interactive hillclimb sessions.")


@hillclimb_app.callback(invoke_without_command=True)
def hillclimb(
    ctx: typer.Context,
    experiment_file_id: str = typer.Argument(..., help="Chronos experiment file public ID"),
    target_world: str = typer.Argument(..., help="Target world path (e.g. 'worlds/webclone')"),
    name: str = typer.Option(
        None,
        "--name",
        "-n",
        help="Session name (defaults to experiment file ID prefix)",
    ),
    base_branch: str = typer.Option(
        "main",
        "--base",
        "-b",
        help="Base branch to create experiment branch from",
    ),
    skip_permissions: bool = typer.Option(
        True,
        "--skip-permissions/--no-skip-permissions",
        help="Launch Claude with --dangerously-skip-permissions",
    ),
) -> None:
    """Launch an interactive hillclimb session.

    Creates an experiment branch, spins up a worktree via Claude Code,
    and configures the hillclimb MCP server with your experiment file.

    Example:

        plato hillclimb abc123-def4-5678 worlds/webclone

        plato hillclimb abc123-def4-5678 worlds/webclone -n webclone-perf
    """
    # Verify we're in a git repo
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        console.print("[red]Not in a git repository[/red]")
        raise typer.Exit(1)
    repo_root = result.stdout.strip()

    # Verify we're not in a worktree
    git_common = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        capture_output=True,
        text=True,
        cwd=repo_root,
    ).stdout.strip()
    if os.path.isabs(git_common):
        main_root = os.path.dirname(git_common)
        if repo_root != main_root:
            console.print(f"[red]Run this from the main repo root ({main_root}), not a worktree[/red]")
            raise typer.Exit(1)

    # Verify claude is installed
    if not shutil.which("claude"):
        console.print("[red]claude CLI not found. Install Claude Code first.[/red]")
        raise typer.Exit(1)

    # Derive session name
    session_name = name or experiment_file_id[:8]
    branch = f"exp/{session_name}"

    # Create branch if needed
    subprocess.run(
        ["git", "fetch", "origin", base_branch, "--quiet"],
        capture_output=True,
    )
    check_branch = subprocess.run(
        ["git", "rev-parse", "--verify", branch],
        capture_output=True,
    )
    if check_branch.returncode != 0:
        console.print(f"Creating branch [bold]{branch}[/bold] off {base_branch}")
        subprocess.run(
            ["git", "branch", branch, f"origin/{base_branch}"],
            check=True,
        )

    # Switch to the experiment branch so --worktree picks it up
    subprocess.run(["git", "checkout", branch], check=True)

    # Pre-write hillclimb config so the MCP server picks it up in the worktree
    import json
    from pathlib import Path

    config_dir = Path(repo_root) / ".hillclimb"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "live-config.json"
    config: dict = {}
    if config_file.exists():
        config = json.loads(config_file.read_text())
    config["experiment_file_id"] = experiment_file_id
    config["target_world_path"] = target_world
    config_file.write_text(json.dumps(config, indent=2) + "\n")

    # Build claude command — interactive, no prompt flag
    cmd = ["claude", "--worktree", session_name]
    if skip_permissions:
        cmd.append("--dangerously-skip-permissions")

    print(f"Launching Claude Code on branch {branch}")
    print(f"Experiment: {experiment_file_id}")
    print(f"Target: {target_world}")
    print("Config written to .hillclimb/live-config.json")
    print()
    print("Tip: start with 'explore the experiment' to see baseline state", flush=True)

    os.execvp("claude", cmd)
