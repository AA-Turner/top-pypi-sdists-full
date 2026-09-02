"""CLI entry point for ``agdt-delete-pr-review-comments``.

Bulk-deletes agentic-devtools review-scaffolding (and/or a given author's)
comment threads on an Azure DevOps pull request, routed through the
``CIPlatformProvider`` abstraction. Azure DevOps is the implemented backend;
GitHub raises ``NotImplementedError`` because this is an Azure DevOps-only
review-tooling operation.

Selection (handled by the provider): a non-deleted ``text`` comment carrying an
``agdt-review`` marker (the safe default) or, optionally, whose author matches
``--author``. Defaults to a dry run — pass ``--execute`` to actually delete.
"""

from __future__ import annotations

import argparse
import os
import sys

from agentic_devtools.cli.ci.models import ReviewCommentDeletionResult
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.subprocess_utils import run_safe


def _build_arg_parser() -> argparse.ArgumentParser:
    """Build the argument parser for ``agdt-delete-pr-review-comments``."""
    parser = argparse.ArgumentParser(
        prog="agdt-delete-pr-review-comments",
        description=(
            "Bulk-delete agentic-devtools review-scaffolding (and/or a given "
            "author's) comment threads on an Azure DevOps pull request. "
            "Defaults to a dry run; pass --execute to delete."
        ),
    )
    parser.add_argument(
        "--pr",
        "-p",
        dest="pr",
        type=int,
        required=True,
        help="Pull request ID.",
    )
    parser.add_argument(
        "--org",
        dest="org",
        default=None,
        help="Azure DevOps organization URL (e.g. https://dev.azure.com/myorg).",
    )
    parser.add_argument(
        "--project",
        dest="project",
        default=None,
        help="Azure DevOps project name.",
    )
    parser.add_argument(
        "--repo",
        dest="repo",
        default=None,
        help="Azure DevOps repository name.",
    )
    parser.add_argument(
        "--author",
        dest="author",
        default=None,
        help=(
            "Case-insensitive author substring; selects that author's comments "
            "in addition to the marker-tagged review-scaffolding comments."
        ),
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually delete the selected comments (default: dry-run).",
    )
    return parser


def _load_code_hosting(repo_path: str) -> str:
    """Return the configured ``code_hosting`` platform for *repo_path*."""
    from agentic_devtools.config import load_platform_config

    return load_platform_config(repo_path)["code_hosting"]


def _resolve_ado_coordinates(args: argparse.Namespace, repo_path: str) -> tuple[str, str, str]:
    """Resolve the Azure DevOps ``(organization, project, repository)`` triple.

    Resolution order per field: explicit CLI argument, then
    ``platform.azure_devops`` in ``.github/agdt-config.json``, then
    :meth:`AzureDevOpsConfig.from_state` (state values / git remote detection).

    Raises:
        ValueError: When any coordinate cannot be resolved to a real value
            (i.e. it is empty or still the placeholder default).
    """
    from agentic_devtools.cli.azure_devops.config import (
        DEFAULT_ORGANIZATION,
        DEFAULT_PROJECT,
        DEFAULT_REPOSITORY,
        AzureDevOpsConfig,
    )
    from agentic_devtools.config import load_platform_config

    ado_config = load_platform_config(repo_path).get("azure_devops", {})
    state_config = AzureDevOpsConfig.from_state()

    organization = args.org or ado_config.get("organization") or state_config.organization
    project = args.project or ado_config.get("project") or state_config.project
    repository = args.repo or ado_config.get("repository") or state_config.repository

    missing: list[str] = []
    if not organization or organization == DEFAULT_ORGANIZATION:
        missing.append("organization (--org)")
    if not project or project == DEFAULT_PROJECT:
        missing.append("project (--project)")
    if not repository or repository == DEFAULT_REPOSITORY:
        missing.append("repository (--repo)")
    if missing:
        raise ValueError(
            "Could not resolve Azure DevOps " + ", ".join(missing) + ". "
            "Pass the missing argument(s), set them via agdt-set, or configure "
            "platform.azure_devops in .github/agdt-config.json."
        )

    return organization, project, repository


def _build_provider(args: argparse.Namespace, repo_path: str) -> CIPlatformProvider:
    """Construct the CI provider for the deletion request.

    Routes to :class:`GitHubActionsProvider` (a stub that raises
    ``NotImplementedError``) only when the repository's ``code_hosting`` is
    GitHub *and* no explicit Azure DevOps ``--org`` was supplied. Every other
    case targets Azure DevOps, so an explicit ``--org`` always selects the
    Azure DevOps backend.
    """
    if not args.org and _load_code_hosting(repo_path) == "github":
        from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider

        return GitHubActionsProvider()

    from agentic_devtools.cli.ci.ado_provider import AzureDevOpsProvider

    organization, project, repository = _resolve_ado_coordinates(args, repo_path)
    return AzureDevOpsProvider(organization=organization, project=project, repository=repository)


def _resolve_repo_path() -> str:
    """Resolve the repository root path, falling back to the current directory."""
    try:
        result = run_safe(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            shell=False,
        )
    except OSError:
        return os.getcwd()

    if result.returncode == 0:
        repo_root = (result.stdout or "").strip()
        if repo_root:
            return repo_root
    return os.getcwd()


def _print_result(result: ReviewCommentDeletionResult, pr_id: int) -> None:
    """Print a human-readable summary of the deletion result."""
    mode = "EXECUTE" if result.executed else "DRY-RUN"
    print(f"[{mode}] PR #{pr_id}: {result.selected_count} comment(s) selected for deletion.")
    for target in result.targets:
        kind = f"marker:{target.marker_type}" if target.marker_type else "author"
        outcome = ""
        if result.executed:
            outcome = " -> deleted" if target.deleted else f" -> FAILED ({target.error})"
        print(f"  thread {target.thread_id} comment {target.comment_id} [{kind}]: {target.snippet}{outcome}")

    if result.selected_count == 0:
        print("Nothing to delete.")
        return
    if result.executed:
        print(f"Done: {result.deleted_count} deleted, {result.failed_count} failed.")
    else:
        print(f"Dry-run only. Re-run with --execute to delete these {result.selected_count} comment(s).")


def delete_review_comments_command(argv: list[str] | None = None) -> int:
    """CLI entry point for ``agdt-delete-pr-review-comments``.

    Args:
        argv: Command-line arguments (defaults to ``sys.argv[1:]``).

    Returns:
        ``0`` on success (a dry run, or an execute with no failures), ``1`` when
        a deletion fails or the provider does not support the operation (e.g. a
        GitHub-hosted repository), and ``2`` for configuration/resolution
        errors (such as an unresolvable organization/project/repository).
    """
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    repo_path = _resolve_repo_path()

    try:
        provider = _build_provider(args, repo_path)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    try:
        result = provider.delete_review_comments(
            args.pr,
            execute=args.execute,
            author_substring=args.author,
        )
    except NotImplementedError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except (OSError, RuntimeError) as exc:
        print(f"Error: failed to delete review comments on PR #{args.pr}: {exc}", file=sys.stderr)
        return 1

    _print_result(result, args.pr)
    if result.executed and result.failed_count:
        return 1
    return 0
