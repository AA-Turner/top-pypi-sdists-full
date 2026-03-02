"""CLI commands for checkpoint management."""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from .manager import CheckpointManager
from .storage import CheckpointStorage


def find_repo_root() -> Path:
    """Find the git repository root from current directory."""
    current = Path.cwd()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return Path.cwd()


def cmd_list(args: argparse.Namespace) -> int:
    """List available checkpoints."""
    repo_root = find_repo_root()
    storage = CheckpointStorage(repo_root)
    checkpoints = storage.get_checkpoints(
        session_id=args.session,
        limit=args.limit,
    )

    if not checkpoints:
        print("No checkpoints found.")
        return 0

    if args.format == "json":
        print(json.dumps([cp.to_dict() for cp in checkpoints], indent=2))
    else:
        # Table format
        print(f"{'ID':<20} {'Session':<10} {'Iter':>4} {'Timestamp':<20} {'Summary':<40} {'Commit':<8}")
        print("-" * 110)
        for cp in checkpoints:
            summary = cp.summary[:37] + "..." if len(cp.summary) > 40 else cp.summary
            commit = cp.commit_sha[:8] if cp.commit_sha else "N/A"
            print(f"{cp.id:<20} {cp.session_id:<10} {cp.iteration:>4} {cp.timestamp[:19]:<20} {summary:<40} {commit:<8}")

    return 0


def cmd_show(args: argparse.Namespace) -> int:
    """Show checkpoint details."""
    repo_root = find_repo_root()
    storage = CheckpointStorage(repo_root)
    metadata = storage.find_checkpoint(args.checkpoint_id)

    if not metadata:
        print(f"Checkpoint not found: {args.checkpoint_id}", file=sys.stderr)
        return 1

    print(f"Checkpoint: {metadata.id}")
    print(f"Session:    {metadata.session_id}")
    print(f"Iteration:  {metadata.iteration}")
    print(f"Timestamp:  {metadata.timestamp}")
    print(f"Commit:     {metadata.commit_sha or 'N/A'}")
    print(f"Summary:    {metadata.summary}")
    print(f"Tools Used: {', '.join(metadata.tools_used) or 'None'}")
    print(f"Files Modified:")
    for f in metadata.files_modified:
        print(f"  - {f}")
    print(f"Token Usage:")
    for key, value in metadata.token_usage.items():
        print(f"  - {key}: {value}")

    return 0


def cmd_restore(args: argparse.Namespace) -> int:
    """Restore to a checkpoint."""
    repo_root = find_repo_root()
    manager = CheckpointManager(repo_root)

    try:
        conv_state = manager.restore_checkpoint(
            args.checkpoint_id,
            restore_conversation=not args.no_conversation,
        )

        print(f"Restored to checkpoint {args.checkpoint_id}")

        if conv_state:
            print(f"Conversation restored with {len(conv_state.messages)} messages")
            print(f"Model: {conv_state.model}")

        return 0

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_diff(args: argparse.Namespace) -> int:
    """Show diff between two checkpoints."""
    repo_root = find_repo_root()
    storage = CheckpointStorage(repo_root)

    cp1 = storage.find_checkpoint(args.checkpoint1)
    cp2 = storage.find_checkpoint(args.checkpoint2)

    if not cp1:
        print(f"Checkpoint not found: {args.checkpoint1}", file=sys.stderr)
        return 1
    if not cp2:
        print(f"Checkpoint not found: {args.checkpoint2}", file=sys.stderr)
        return 1

    if not cp1.commit_sha or not cp2.commit_sha:
        print("Cannot diff: one or both checkpoints have no commit SHA", file=sys.stderr)
        return 1

    # Use git diff
    import subprocess
    result = subprocess.run(
        ["git", "diff", cp1.commit_sha, cp2.commit_sha],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    return result.returncode


def main(argv: Optional[list[str]] = None) -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="emdash-checkpoint",
        description="Manage emdash checkpoints",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list command
    list_parser = subparsers.add_parser("list", help="List available checkpoints")
    list_parser.add_argument("-s", "--session", help="Filter by session ID")
    list_parser.add_argument("-n", "--limit", type=int, default=20, help="Number of checkpoints to show")
    list_parser.add_argument("--format", choices=["table", "json"], default="table", help="Output format")
    list_parser.set_defaults(func=cmd_list)

    # show command
    show_parser = subparsers.add_parser("show", help="Show checkpoint details")
    show_parser.add_argument("checkpoint_id", help="Checkpoint ID to show")
    show_parser.set_defaults(func=cmd_show)

    # restore command
    restore_parser = subparsers.add_parser("restore", help="Restore to a checkpoint")
    restore_parser.add_argument("checkpoint_id", help="Checkpoint ID to restore")
    restore_parser.add_argument("--no-conversation", action="store_true", help="Skip conversation restore")
    restore_parser.set_defaults(func=cmd_restore)

    # diff command
    diff_parser = subparsers.add_parser("diff", help="Show diff between two checkpoints")
    diff_parser.add_argument("checkpoint1", help="First checkpoint ID")
    diff_parser.add_argument("checkpoint2", help="Second checkpoint ID")
    diff_parser.set_defaults(func=cmd_diff)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
