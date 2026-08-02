"""``pysae-ai-tools mr create`` — open a merge request via the resolved provider."""

from pathlib import Path
from typing import Annotated

import typer

from ..common.conventional import COMMIT_TYPES, is_valid_commit_header
from ..common.project_config import flag_enabled
from .resolve import resolve_provider

_PROJECT_HELP = "Target another repo relative to the current owner ('op', 'infra/infra-cluster') or a full URL"


def _invalid_title_message(title: str) -> str:
    return (
        f'ERROR: MR title is not a valid Conventional Commits header: "{title}"\n'
        "The MR title becomes the squash-merge commit message and is validated by "
        "commitlint on the target branch — a non-conforming title blocks the merge.\n"
        "Expected: <type>[(<scope>)][!]: <subject>\n"
        f"Allowed types: {', '.join(COMMIT_TYPES)}\n"
        "Example: feat(ndp): add trip export endpoint"
    )


def main(
    title: Annotated[str, typer.Option("--title", help="Merge request title (Conventional Commits header)")],
    source_branch: Annotated[str, typer.Option("--source-branch", help="Source branch")],
    target_branch: Annotated[str, typer.Option("--target-branch", help="Target branch")],
    description: Annotated[str, typer.Option("--description", help="Description body")] = "",
    description_file: Annotated[str, typer.Option("--description-file", help="Read the body from this file")] = "",
    label: Annotated[list[str] | None, typer.Option("--label", help="Label (repeatable)")] = None,
    assignee: Annotated[list[str] | None, typer.Option("--assignee", help="Assignee username (repeatable)")] = None,
    draft: Annotated[bool, typer.Option("--draft", help="Open as draft")] = False,
    remove_source_branch: Annotated[
        bool, typer.Option("--remove-source-branch", help="Delete the source branch on merge")
    ] = False,
    project: Annotated[str, typer.Option("--project", help=_PROJECT_HELP)] = "",
) -> None:
    """Open a merge request and print its URL."""
    # Honour the per-repo creation flag centrally, so every caller is covered.
    if not project and not flag_enabled(Path.cwd(), "merge_requests", "enabled"):
        typer.echo("skipped: merge_requests.enabled is false for this repo — no MR created")
        return
    # The title becomes the squash-merge commit message (commitlint-checked on merge):
    # fail fast here rather than opening an unmergeable MR.
    if not is_valid_commit_header(title):
        typer.echo(_invalid_title_message(title), err=True)
        raise typer.Exit(code=1)
    body = Path(description_file).read_text(encoding="utf-8", errors="replace") if description_file else description
    provider = resolve_provider(project=project or None)
    mr = provider.create_mr(
        title=title,
        description=body,
        source_branch=source_branch,
        target_branch=target_branch,
        labels=label or [],
        assignees=assignee or [],
        draft=draft,
        remove_source_branch=remove_source_branch,
    )
    typer.echo(mr.web_url or mr.iid)
