"""CLI entry point: pysae-ai-tools tracker <command>.

Subcommands:
    hook      — PostToolUse hook handler (reads JSON from stdin, appends to daily log)
    stop-hook — Stop hook handler (emits session end event)
    manual    — Log a manual time entry
    report    — Generate activity report for a given day
    dashboard — Launch the activity dashboard in the browser
    setup     — Migrate the legacy tracker hooks out of Claude Code settings
"""

import webbrowser
from datetime import date
from typing import Annotated

import typer

from .hook import hook, log_context_manual, log_manual, stop_hook
from .report import report
from .setup import app as setup_app

app = typer.Typer(help="Activity tracker — log Claude Code sessions and generate reports")
app.command()(hook)
app.command(name="stop-hook")(stop_hook)
app.command()(report)
app.add_typer(setup_app, name="setup")


@app.command()
def manual(
    duration: Annotated[float, typer.Argument(help="Durée en secondes")],
    description: Annotated[str, typer.Option("--description", "-d", help="Description du travail")] = "",
    project_path: Annotated[str, typer.Option("--project-path", help="Chemin du projet (ex: pysae/api)")] = "",
    project_id: Annotated[str, typer.Option("--project-id", help="ID du projet GitLab")] = "",
    project_url: Annotated[str, typer.Option("--project-url", help="URL du projet")] = "",
    issue_iid: Annotated[str, typer.Option("--issue-iid", help="IID de l'issue")] = "",
    issue_title: Annotated[str, typer.Option("--issue-title", help="Titre de l'issue")] = "",
    issue_url: Annotated[str, typer.Option("--issue-url", help="URL de l'issue")] = "",
    issue_labels: Annotated[list[str], typer.Option("--issue-label", help="Labels de l'issue")] = [],  # noqa: B006
    epic_iid: Annotated[str, typer.Option("--epic-iid", help="IID de l'epic")] = "",
    epic_title: Annotated[str, typer.Option("--epic-title", help="Titre de l'epic")] = "",
    epic_url: Annotated[str, typer.Option("--epic-url", help="URL de l'epic")] = "",
    target_date: Annotated[str, typer.Option("--date", help="Date cible (YYYY-MM-DD), défaut: aujourd'hui")] = "",
) -> None:
    """Enregistre une entrée de temps manuelle."""
    parsed_date = date.fromisoformat(target_date) if target_date else None
    log_manual(
        duration_seconds=duration,
        description=description,
        project_path=project_path,
        project_id=project_id,
        project_url=project_url,
        issue_iid=issue_iid,
        issue_title=issue_title,
        issue_url=issue_url,
        issue_labels=issue_labels,
        epic_iid=epic_iid,
        epic_title=epic_title,
        epic_url=epic_url,
        target_date=parsed_date,
    )


@app.command()
def context(
    session_id: Annotated[str, typer.Argument(help="ID de la session à contextualiser")],
    project_path: Annotated[str, typer.Option("--project", "-p", help="Chemin du projet (ex: pysae/op)")] = "",
    project_id: Annotated[str, typer.Option("--project-id", help="ID du projet GitLab")] = "",
    project_url: Annotated[str, typer.Option("--project-url", help="URL du projet")] = "",
    issue_iid: Annotated[str, typer.Option("--issue", "-i", help="IID de l'issue")] = "",
    issue_title: Annotated[str, typer.Option("--issue-title", help="Titre de l'issue")] = "",
    issue_url: Annotated[str, typer.Option("--issue-url", help="URL de l'issue")] = "",
    issue_labels: Annotated[list[str], typer.Option("--label", "-l", help="Labels")] = [],  # noqa: B006
    epic_iid: Annotated[str, typer.Option("--epic", "-e", help="IID de l'epic")] = "",
    epic_title: Annotated[str, typer.Option("--epic-title", help="Titre de l'epic")] = "",
    epic_url: Annotated[str, typer.Option("--epic-url", help="URL de l'epic")] = "",
    target_date: Annotated[str, typer.Option("--date", help="Date cible (YYYY-MM-DD)")] = "",
) -> None:
    """Attribue un contexte (issue, epic, labels) à une session existante."""
    parsed_date = date.fromisoformat(target_date) if target_date else None
    result = log_context_manual(
        session_id=session_id,
        project_path=project_path,
        project_id=project_id,
        project_url=project_url,
        issue_iid=issue_iid,
        issue_title=issue_title,
        issue_url=issue_url,
        issue_labels=issue_labels,
        epic_iid=epic_iid,
        epic_title=epic_title,
        epic_url=epic_url,
        target_date=parsed_date,
    )
    print(result)


@app.command()
def dashboard(
    port: Annotated[int, typer.Option("--port", help="Port (0 = auto)")] = 0,
) -> None:
    """Launch the activity dashboard in the browser."""
    from .server import ensure_server  # heavy: imports FastAPI/uvicorn

    actual_port, is_new = ensure_server(port)
    url = f"http://127.0.0.1:{actual_port}"
    print(url)
    if is_new:
        webbrowser.open(url)


if __name__ == "__main__":
    app()
