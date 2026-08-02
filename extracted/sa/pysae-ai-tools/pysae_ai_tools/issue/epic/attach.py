"""``pysae-ai-tools issue epic attach`` — attach one or more issues to an epic."""

from typing import Annotated

import typer

from ...common.issue_tracking.provider import UnsupportedCapability
from ..resolve import resolve_provider


def _parse_ref(ref: str) -> tuple[str | None, str]:
    """Split ``project#iid`` into ``(project, iid)``; a bare ``iid`` → ``(None, iid)``."""
    if "#" in ref:
        project, iid = ref.rsplit("#", 1)
        return (project or None, iid)
    return (None, ref)


def main(
    epic: Annotated[str, typer.Option("--epic", help="Epic number")],
    issue: Annotated[list[str], typer.Option("--issue", help="Issue ref: 'iid' or 'project#iid' (repeatable)")],
    project: Annotated[
        str,
        typer.Option(
            "--project",
            help="Target another repo relative to the current owner ('op', 'infra/infra-cluster') or a full URL",
        ),
    ] = "",
) -> None:
    """Attach each issue to the epic (supports cross-project refs)."""
    provider = resolve_provider(project=project or None)
    try:
        for ref in issue:
            ref_project, iid = _parse_ref(ref)
            provider.attach_to_epic(iid, epic, project=ref_project)
    except UnsupportedCapability as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc
