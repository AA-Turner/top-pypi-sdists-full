"""``pysae-ai-tools agent rank`` — final ranking from externally-scored candidates.

Reads (stdin, JSON) the ``agent candidates`` pool where each entry has been
augmented with the in-session subagent's assessment (``success_probability``,
``sensitive_domain_match``). Applies the same weighting as ``score.py``, filters
sensitive tickets and those below the success-probability floor, sorts and caps.
Emits ``{"process": [...], "escalate": [...]}`` — no LLM call.
"""

import json
import sys
from typing import Annotated, Any

import typer

from .autopilot_config import load_autopilot
from .guards import OVERRIDE_LABEL
from .score import weighted_final_score


def main(
    max_tickets: Annotated[int | None, typer.Option("--max-tickets")] = None,
    min_success_probability: Annotated[int | None, typer.Option("--min-success-probability")] = None,
    project: Annotated[
        str | None, typer.Option("--project", help="Resolve max_tickets default from this repo.")
    ] = None,
) -> None:
    """Rank scored candidates from stdin; emit process/escalate lists as JSON.

    ``--max-tickets`` / ``--min-success-probability`` override the per-repo
    ``autopilot`` config; unset, the floor is each candidate's own repo config and
    the cap is ``--project``'s config (or the schema default when neither is given).
    """
    try:
        candidates: list[dict[str, Any]] = json.loads(sys.stdin.read() or "[]")
    except json.JSONDecodeError as exc:
        typer.echo(f"invalid JSON on stdin: {exc}", err=True)
        raise typer.Exit(code=1) from None

    cap = max_tickets if max_tickets is not None else load_autopilot(project).max_tickets

    process: list[dict[str, Any]] = []
    escalate: list[dict[str, Any]] = []
    for c in candidates:
        has_override = OVERRIDE_LABEL in c.get("labels", [])
        success = int(c.get("success_probability", 0))
        floor = (
            min_success_probability
            if min_success_probability is not None
            else load_autopilot(c.get("project_path")).min_success_probability
        )
        # Only the LLM sensitive-domain verdict blocks. The regex `sensitive_path`
        # is advisory (broad, matches incidental mentions) — the skill posts a
        # sensitive-paths note but the ticket still ranks; the LLM verdict is the
        # authoritative sensitive gate.
        if c.get("sensitive_domain_match") and not has_override:
            escalate.append(
                {
                    **c,
                    "escalation_reason": "garde-fou LLM domaine sensible. "
                    "Override possible en ajoutant le label agent-override-sensitive "
                    "(il coexiste avec agent::ready) puis en remettant agent::ready.",
                }
            )
        elif success < floor:
            rationale = (c.get("rationale") or "").strip() or "rationale non fourni"
            escalate.append(
                {
                    **c,
                    "escalation_reason": f"success_probability={success} < seuil {floor}. "
                    f"Haiku rationale: {rationale[:200]}",
                }
            )
        else:
            process.append({**c, "final_score": weighted_final_score(float(c.get("business_score", 0)), success)})

    process.sort(key=lambda c: c["final_score"], reverse=True)
    # Pre-pickup escalations count against the cap, exactly like the pipeline
    # where NOT_READY outcomes fill result.outcomes before budget_exhausted breaks
    # the processing loop (guards.budget_exhausted). So #processed = cap − #escalated.
    process_cap = max(0, cap - len(escalate))
    typer.echo(json.dumps({"process": process[:process_cap], "escalate": escalate}, ensure_ascii=False))
