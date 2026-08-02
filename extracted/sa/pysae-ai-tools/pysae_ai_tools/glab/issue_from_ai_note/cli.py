"""`pysae-ai-tools glab issue-from-ai-note` Typer command.

Parses an ai-note's ``Open questions`` into a JSON list of follow-up issues to
create. It deliberately **does not create issues** — the
``/glab-issue-from-ai-note`` skill takes this JSON and delegates each follow-up
to ``/issue-create`` so every ticket goes through the standard issue
pipeline (weight, mandatory ``type::``, board column, template). Each follow-up
carries the ``agent-followup`` label.
"""

import json
from pathlib import Path
from typing import Annotated

import typer

from .parser import OpenQuestion, parse_ai_note

app = typer.Typer(
    no_args_is_help=True,
    help="Parse an ai-note's Open questions into follow-up issues (JSON) for /issue-create.",
)

FOLLOWUP_LABEL = "agent-followup"


def _build_issue_body(q: OpenQuestion) -> str:
    return "\n".join(
        [
            f"**Détail** : {q.detail}",
            "",
            f"Issue parente : {q.source_issue_url or '(inconnue)'}",
        ]
    )


def _resolve_project(explicit: str, questions: list[OpenQuestion]) -> str:
    if explicit:
        return explicit
    for q in questions:
        if q.source_issue_url:
            return q.source_issue_url.split("/-/issues/")[0].replace("https://gitlab.com/", "")
    return ""


@app.command()
def main(
    ai_note_path: Annotated[
        Path,
        typer.Argument(exists=True, dir_okay=False, readable=True),
    ],
    project: Annotated[
        str,
        typer.Option(
            "--project",
            help="Target project path (e.g. pysae/api). Default: parent issue project.",
        ),
    ] = "",
    filter_priority: Annotated[
        str,
        typer.Option(
            "--filter",
            help='Comma-separated priorities to include (e.g. "🔴,🟡").',
        ),
    ] = "",
    epic_iid: Annotated[
        int,
        typer.Option("--epic", help="Optional parent epic IID"),
    ] = 0,
) -> None:
    """Emit, as JSON, the follow-up issues to create from an ai-note.

    Does not create anything — the caller (the /glab-issue-from-ai-note skill)
    delegates each follow-up to /issue-create.
    """
    only = [p.strip() for p in filter_priority.split(",") if p.strip()] or None
    questions = parse_ai_note(ai_note_path.read_text(encoding="utf-8"), only=only)
    payload = {
        "project": _resolve_project(project, questions),
        "label": FOLLOWUP_LABEL,
        "epic_iid": epic_iid or None,
        "followups": [
            {
                "title": q.title,
                "description": _build_issue_body(q),
                "priority": q.priority,
            }
            for q in questions
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    app()
