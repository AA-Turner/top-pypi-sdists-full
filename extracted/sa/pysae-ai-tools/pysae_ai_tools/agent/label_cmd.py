"""``pysae-ai-tools agent label`` — agent:: label lifecycle (claim / block / done).

Thin CLI over :mod:`pysae_ai_tools.agent.labels` so the in-session orchestration
skill drives the ``agent::ready → agent::wip → (cleared | agent::blocked)``
lifecycle without re-implementing the label logic. Operates on ``project_path``
+ ``iid`` (the label helpers only read those and the author for the mention).
"""

from datetime import datetime, timezone
from typing import Annotated

import typer

from .labels import CommentPostError, LabelTransitionError, clear_wip, mark_blocked, mark_wip
from .models import Ticket

app = typer.Typer(no_args_is_help=True, help="agent:: label lifecycle (claim/block/done)")


def _ticket(project_path: str, iid: int, author: str = "") -> Ticket:
    return Ticket(
        iid=iid,
        project_path=project_path,
        title="",
        web_url="",
        updated_at=datetime.now(timezone.utc),
        author_username=author,
    )


def _run(fn: object) -> None:
    try:
        fn()  # type: ignore[operator]
    except (LabelTransitionError, CommentPostError) as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from None


@app.command()
def claim(project_path: str, iid: int) -> None:
    """agent::ready → agent::wip (posts the pickup marker)."""
    _run(lambda: mark_wip(_ticket(project_path, iid)))


@app.command()
def block(
    project_path: str,
    iid: int,
    reason: Annotated[str, typer.Option("--reason", help="Escalation reason (posted as a comment).")],
    author: Annotated[str, typer.Option("--author", help="Ticket author username, for the @mention.")] = "",
    run_id: Annotated[str, typer.Option("--run-id")] = "manual",
) -> None:
    """→ agent::blocked (removes wip/ready, posts the escalation comment)."""
    _run(lambda: mark_blocked(_ticket(project_path, iid, author), reason, run_id))


@app.command()
def done(project_path: str, iid: int) -> None:
    """Clear agent::wip (successful completion)."""
    _run(lambda: clear_wip(_ticket(project_path, iid)))
