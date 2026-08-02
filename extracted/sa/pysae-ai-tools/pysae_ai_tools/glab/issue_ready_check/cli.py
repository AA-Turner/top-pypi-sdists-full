"""`pysae-ai-tools glab issue-ready-check` Typer command."""

import json as jsonlib
import subprocess
from importlib.metadata import PackageNotFoundError, version
from typing import Annotated

import typer

from ...common.glab.fetch_issues import run_glab
from ...common.glab.templates import find_section
from .actions import apply_failure_actions, apply_suggestion_comment
from .llm_review import review_ac_quality
from .models import ReadyCheckResult
from .rules import evaluate_ticket

app = typer.Typer(
    no_args_is_help=True,
    help="Check if a ticket is ready for autopilot.",
)


def _tool_version() -> str:
    try:
        return version("pysae-ai-tools")
    except PackageNotFoundError:
        return "dev"


def evaluate_for_batch(description: str, labels: list[str]) -> ReadyCheckResult:
    """Pure structural evaluation, no side-effects, no LLM. Safe for batch pre-filter."""
    return evaluate_ticket(description=description, labels=labels)


@app.command()
def main(
    issue_ref: Annotated[
        str,
        typer.Argument(
            help="Issue IID, URL, or <project>#<iid> (resolved via detect-context).",
        ),
    ],
    apply: Annotated[
        bool,
        typer.Option(
            "--apply",
            help="Apply GitLab actions on failure (labels + comment).",
        ),
    ] = False,
    no_llm_review: Annotated[
        bool,
        typer.Option(
            "--no-llm-review",
            help="Disable the Sonnet AC quality suggestion.",
        ),
    ] = False,
    json: Annotated[
        bool,
        typer.Option("--json", help="Emit the result as JSON on stdout."),
    ] = False,
) -> None:
    try:
        proc = subprocess.run(
            ["pysae-ai-tools", "internal", "detect-context", issue_ref],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
        typer.echo(f"ready-check: detect-context failed ({exc})", err=True)
        raise typer.Exit(code=2) from exc
    if proc.returncode != 0:
        typer.echo(f"ready-check: detect-context failed: {(proc.stderr or '').strip()}", err=True)
        raise typer.Exit(code=2)
    ctx = jsonlib.loads(proc.stdout)
    project_path = ctx.get("project_path") or ""
    issue_iid = int(ctx.get("issue_iid") or 0)
    if not project_path or not issue_iid:
        typer.echo("ready-check: unable to resolve project + issue from arg", err=True)
        raise typer.Exit(code=2)

    raw = run_glab(
        "issue",
        "view",
        str(issue_iid),
        "-R",
        project_path,
        "--output",
        "json",
    )
    issue = jsonlib.loads(raw)
    description = issue.get("description") or ""
    labels = [label["name"] if isinstance(label, dict) else label for label in issue.get("labels") or []]
    author_username = (issue.get("author") or {}).get("username")

    structural = evaluate_ticket(description=description, labels=labels)
    result = ReadyCheckResult(
        ready=structural.ready,
        type=structural.type,
        violations=structural.violations,
    )

    if not structural.ready:
        if apply:
            actions = apply_failure_actions(
                project_path=project_path,
                issue_iid=issue_iid,
                result=structural,
                author_username=author_username,
                tool_version=_tool_version(),
            )
            result = result.model_copy(update={"actions_applied": actions})
    else:
        if not no_llm_review:
            ac_section = find_section(description, "Critères d'acceptation")
            ac_body = ac_section.body if ac_section else ""
            review = review_ac_quality(description=description, ac_section_body=ac_body)
            if review is not None and review.quality_score < 4 and apply:
                actions = apply_suggestion_comment(
                    project_path=project_path,
                    issue_iid=issue_iid,
                    review=review,
                )
                result = result.model_copy(update={"llm_review": review, "actions_applied": actions})
            elif review is not None:
                result = result.model_copy(update={"llm_review": review})

    if json:
        typer.echo(result.model_dump_json())
        return

    if result.ready:
        typer.echo(f"ready-check OK ({result.type.value})")
        if result.llm_review:
            typer.echo(f"AC quality: {result.llm_review.quality_score}/5")
    else:
        typer.echo(f"ready-check FAIL ({result.type.value})", err=True)
        for v in result.violations:
            typer.echo(f"  - {v}", err=True)
        raise typer.Exit(code=1)
