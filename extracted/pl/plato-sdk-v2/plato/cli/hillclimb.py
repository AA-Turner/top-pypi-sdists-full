"""plato hillclimb — launch an interactive hillclimb session with Claude Code."""

from __future__ import annotations

import os
import shutil
import subprocess

import typer

from plato.cli.utils import console

hillclimb_app = typer.Typer(help="Launch interactive hillclimb sessions.")

HILLCLIMB_SYSTEM_PROMPT = """\
You are running an interactive hillclimb session — an iterative improvement \
loop for a Plato world. You have MCP tools for experiment management, \
evaluation, and hypothesis tracking.

## Core Workflow

1. **Analyze** — Use `get_experiment_file`, `credit_assignment`, \
`get_annotations` to understand baseline performance and find weak spots.
2. **Hypothesize** — Use `record_hypothesis` to track what you think is \
wrong and how to fix it. Be specific about the causal variable.
3. **Implement** — Edit the world code directly. Run `uv run pytest` and \
`uv run ruff check` for basic validation.
4. **Test** — Run `plato chronos test <config>.json` to validate on a real \
VM. This is critical — unit tests alone miss prompt quality issues.
5. **Report test runs** — After each `plato chronos test`, note the \
CHRONOS_SESSION_ID. Use `plato chronos traces <id>` or \
`plato chronos analysis <id>` to inspect what happened.
6. **Publish & launch** — Use `publish_dev_version`, \
`create_experiment_version`, `launch_experiment` to run a full experiment.
7. **Evaluate** — Use `run_target_reviews`, `compare_scores` to see if \
your changes improved things.

## When to Use Experiments vs Test Runs

- **`run_test` MCP tool** = quick, isolated hypothesis validation. Runs \
`plato chronos test` on a config, automatically registers the test run \
with Chronos linked to the experiment, and returns session_id + results. \
Fast feedback loop (~2-5 min). Always do this first.
- **Full experiments** (`launch_experiment`) = comprehensive evaluation \
against the baseline. Use this after test runs confirm your hypothesis. \
Takes longer but gives authoritative scores.

## Sub-Experiment Test Runs

Use the `run_test` MCP tool instead of running `plato chronos test` \
manually. It handles everything:
1. Runs the test on a real VM
2. Registers the test run with Chronos (linked to the experiment version, \
commit SHA, and git link)
3. Returns session_id, status, exit_code, and phase results

After `run_test` completes:
1. Analyze traces with `plato chronos traces <session_id>` or \
`plato chronos analysis <session_id>`
2. Use `update_test_run_evidence` to record whether the hypothesis was \
validated or rejected, with a summary of what you observed
3. Use `update_hypothesis` to update the hypothesis status

## Key Principles

- **Test before you publish** — always run `plato chronos test` before \
`publish_dev_version`. Catching issues early saves hours.
- **One hypothesis at a time** — don't change multiple things between \
evaluations. You won't know what worked.
- **Read the traces** — `plato chronos traces <id>` shows what agents \
actually did. This is more valuable than test pass/fail.
- **Track everything** — use `record_hypothesis` and `update_hypothesis` \
so you build a knowledge base across iterations.
"""


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

    # Build claude command — interactive with hillclimb system prompt
    cmd = ["claude", "--worktree", session_name]
    cmd.extend(["--append-system-prompt", HILLCLIMB_SYSTEM_PROMPT])
    if skip_permissions:
        cmd.append("--dangerously-skip-permissions")

    print(f"Launching Claude Code on branch {branch}")
    print(f"Experiment: {experiment_file_id}")
    print(f"Target: {target_world}")
    print("Config written to .hillclimb/live-config.json")
    print()
    print("Tip: start with 'explore the experiment' to see baseline state", flush=True)

    os.execvp("claude", cmd)
