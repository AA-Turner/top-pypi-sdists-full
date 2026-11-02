"""CLI entry point for the no-change suppressed-triage follow-up reaper.

Provides the ``agdt-suppressed-triage-reap`` command that instantiates the
GitHub provider and runs the reaper. All business logic lives in
:mod:`agentic_devtools.cli.ci.suppressed_reaper`; the scheduled workflow only
invokes this command.
"""

from __future__ import annotations

import argparse
import json
import logging
import os

from agentic_devtools.cli.github.repo_resolution import resolve_github_repo

logger = logging.getLogger(__name__)


def suppressed_triage_reap_command(argv: list[str] | None = None) -> int:
    """CLI entry point for ``agdt-suppressed-triage-reap``.

    Closes every open Copilot-authored follow-up pull request whose diff is
    empty and whose body satisfies the no-change contract, posting the verdict
    table to the deferral issue and closing that issue as completed.

    Args:
        argv: Command-line arguments (defaults to ``sys.argv[1:]``).

    Returns:
        Exit code: 0 on success, 1 when the run failed.
    """
    parser = argparse.ArgumentParser(
        prog="agdt-suppressed-triage-reap",
        description="Close no-change suppressed-comment triage follow-up pull requests",
    )
    parser.add_argument("--repo", type=str, default=None, help="Repository (owner/repo)")
    parser.add_argument(
        "--max-prs",
        type=int,
        default=None,
        help="Maximum number of pull requests to close in one run (default: no limit)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report the pull requests that would be closed without mutating anything",
    )
    args = parser.parse_args(argv)

    from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
    from agentic_devtools.cli.ci.suppressed_reaper import reap_no_change_prs

    repo = resolve_github_repo(args.repo or os.environ.get("GITHUB_REPOSITORY"))
    provider = GitHubActionsProvider(repo=repo)

    try:
        result = reap_no_change_prs(provider, max_prs=args.max_prs, dry_run=args.dry_run)
    except Exception as exc:
        logger.error("Suppressed-triage reap failed: %s", exc, exc_info=True)
        return 1

    print(json.dumps(result))
    return 0
