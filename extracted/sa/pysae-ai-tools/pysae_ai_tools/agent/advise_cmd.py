"""``pysae-ai-tools agent advise`` — post a non-blocking advisory note.

Wraps :func:`pysae_ai_tools.agent.labels.post_advisory_note` (leaves labels
untouched). Used by the in-session skill to surface structural gaps (missing
template sections) and Sonnet completeness gaps (missing edge cases) without
re-implementing the comment formatting.
"""

from datetime import datetime, timezone
from typing import Annotated

import typer

from .labels import CommentPostError, post_advisory_note
from .models import Ticket


def main(
    project_path: str,
    iid: int,
    kind: Annotated[str, typer.Option("--kind", help="Advisory kind, e.g. 'ready-check' or 'completeness'.")],
    body: Annotated[str, typer.Option("--body", help="Advisory body (markdown).")],
    author: Annotated[str, typer.Option("--author", help="Ticket author username, for the @mention.")] = "",
    run_id: Annotated[str, typer.Option("--run-id")] = "manual",
) -> None:
    """Post a non-blocking advisory comment on a ticket (labels untouched)."""
    ticket = Ticket(
        iid=iid,
        project_path=project_path,
        title="",
        web_url="",
        updated_at=datetime.now(timezone.utc),
        author_username=author,
    )
    try:
        post_advisory_note(ticket, kind, body, run_id)
    except CommentPostError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from None
