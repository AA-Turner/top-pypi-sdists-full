"""Deterministic rubber-duck resolution for the orchestrator (v2 PR review).

Subagents cannot spawn subagents (plan §13.1), so the **orchestrator** runs all
rubber ducks (§15.1). This command resolves the validated duck models for a
given *layer* (``mainAgent`` or ``subagent``) and *author model* via P0's
:func:`resolve_rubber_duck_models`, then writes a critique prompt the
orchestrator hands to each duck it spawns with ``runSubagent``. Accept/reject
rationale is recorded by the orchestrator into the answer's
``reviewer.rubberDucks`` — this command never writes answers or shared state.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from agentic_devtools.cli.azure_devops.review_reviewer_models import (
    AgentPicks,
    resolve_rubber_duck_models,
)
from agentic_devtools.cli.config.project_config import get_available_models
from agentic_devtools.cli.config.pull_request_review_config import (
    load_pull_request_review_config,
)

_VALID_LAYERS = ("mainAgent", "subagent")


def build_critique_prompt(
    *,
    layer: str,
    author_model: str | None,
    file_key: str | None,
    draft_path: str | None,
) -> str:
    """Render the duck-facing critique prompt the orchestrator hands to each duck.

    The prompt is addressed to the rubber-duck subagent only; orchestrator-facing
    details (which models to spawn, or whether the orchestrator must pick its own)
    are reported separately on stdout/JSON by :func:`resolve_ducks_command`, never
    embedded here, so the duck never receives instructions meant for the orchestrator.

    Args:
        layer: ``mainAgent`` (orchestrator's own work) or ``subagent`` (a file
            reviewer's draft).
        author_model: The model that produced the work under critique (may be None).
        file_key: The fileKey under review (None for orchestrator-level work).
        draft_path: Path to the draft answer/work the duck critiques (optional).

    Returns:
        Markdown the orchestrator passes to each ``pr-review/rubber-duck@…`` subagent.
    """
    scope = f"file `{file_key}`" if file_key else "the orchestrator's own work"
    author = author_model or "an unspecified model"

    draft_line = (
        f"- The draft under critique is at `{draft_path}`."
        if draft_path
        else "- The draft under critique is included inline by the orchestrator."
    )

    context_line = (
        "- You also receive the file prompt and the trimmed cluster context."
        if file_key
        else "- You also receive the trimmed cluster context."
    )

    return (
        f"# Rubber-duck critique — layer `{layer}`\n\n"
        f"You are a rubber-duck critic (`pr-review/rubber-duck@<author>#<n>`) — one of the critics "
        f"the orchestrator selected to second-opinion {scope}, originally authored by `{author}`.\n\n"
        "## Inputs\n\n"
        f"{draft_line}\n"
        f"{context_line}\n\n"
        "## Your task\n\n"
        "1. Critically review the draft for correctness, security, missed edge cases, and "
        "false positives.\n"
        "2. Return exactly one verdict — `accept`, `reject`, or `partial` — with concise notes.\n"
        "3. Do **not** write any files, answers, or shared state, and do **not** spawn "
        "subagents; return your critique as your final message only.\n\n"
        "The orchestrator records your verdict into the answer's `reviewer.rubberDucks` "
        "(you do not).\n"
    )


def resolve_ducks_command() -> None:
    """CLI entry point for ``agdt-pr-review-resolve-ducks``."""
    parser = argparse.ArgumentParser(
        description="Resolve validated rubber-duck models and write the orchestrator's critique prompt (v2).",
    )
    parser.add_argument("--layer", required=True, choices=list(_VALID_LAYERS), help="Rubber-duck layer.")
    parser.add_argument("--author-model", default=None, help="Model that authored the work under critique.")
    parser.add_argument("--file-key", default=None, help="fileKey under review (omit for orchestrator work).")
    parser.add_argument("--draft-answer", default=None, help="Path to the draft answer/work the ducks critique.")
    parser.add_argument("--output", default=None, help="Where to write the critique prompt (else stdout).")
    parser.add_argument("--json", action="store_true", help="Emit a JSON result summary to stdout.")
    args = parser.parse_args()

    config = load_pull_request_review_config()
    available = get_available_models()
    resolved = resolve_rubber_duck_models(args.layer, args.author_model, available, config)

    if isinstance(resolved, AgentPicks):
        agent_picks = True
        models: list[str] = []
    else:
        agent_picks = False
        models = list(resolved)

    prompt = build_critique_prompt(
        layer=args.layer,
        author_model=args.author_model,
        file_key=args.file_key,
        draft_path=args.draft_answer,
    )

    if args.output:
        out_path = Path(args.output)
        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(prompt, encoding="utf-8")
        except OSError as exc:
            print(f"Error: could not write critique prompt to {out_path}: {exc}", file=sys.stderr)
            sys.exit(2)

    if args.json:
        print(
            json.dumps(
                {
                    "layer": args.layer,
                    "agentPicks": agent_picks,
                    "models": models,
                    "promptFile": args.output,
                },
                indent=2,
            )
        )
        return

    if agent_picks:
        print(f"Rubber-duck models for layer '{args.layer}': agent picks (no validated models configured).")
    else:
        print(f"Rubber-duck models for layer '{args.layer}': {', '.join(models)}")
    if args.output:
        print(f"Critique prompt written: {args.output}")
    else:
        print()
        print(prompt)
