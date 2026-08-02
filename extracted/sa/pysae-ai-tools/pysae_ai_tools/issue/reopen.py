"""``pysae-ai-tools issue reopen`` — reopen one or more closed issues."""

from typing import Annotated

import typer

from .resolve import print_json, resolve_provider


def main(
    iids: Annotated[list[str], typer.Argument(help="Issue numbers to reopen")],
    project: Annotated[
        str,
        typer.Option(
            "--project",
            help="Target another repo relative to the current owner ('op', 'infra/infra-cluster') or a full URL",
        ),
    ] = "",
) -> None:
    """Reopen the given issues and print the updated records as JSON. Idempotent."""
    provider = resolve_provider(project=project or None)
    reopened = [provider.reopen_issue(iid) for iid in iids]
    print_json([{"iid": issue.iid, "web_url": issue.web_url, "state": issue.state} for issue in reopened])
