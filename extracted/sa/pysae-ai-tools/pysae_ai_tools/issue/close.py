"""``pysae-ai-tools issue close`` — close one or more issues (state only)."""

from typing import Annotated

import typer

from .resolve import print_json, resolve_provider


def main(
    iids: Annotated[list[str], typer.Argument(help="Issue numbers to close")],
    project: Annotated[
        str,
        typer.Option(
            "--project",
            help="Target another repo relative to the current owner ('op', 'infra/infra-cluster') or a full URL",
        ),
    ] = "",
) -> None:
    """Close the given issues and print the updated records as JSON.

    A pure state transition: labels (including ``workflow::*`` columns) are left
    untouched — board logic lives elsewhere. Idempotent: closing an already-closed
    issue is not an error.
    """
    provider = resolve_provider(project=project or None)
    closed = [provider.close_issue(iid) for iid in iids]
    print_json([{"iid": issue.iid, "web_url": issue.web_url, "state": issue.state} for issue in closed])
