"""``pysae-ai-tools agent score-prompt`` — canonical scoring prompts, formatted.

Single source for the in-session scoring subagents: reads the candidate pool on
stdin and emits ``{iid: prompt}`` using the exact ``score.py`` templates, so a
Haiku (``assessment``) or Sonnet (``completeness``) subagent scores a ticket
with the canonical rubric — no prompt duplication, no divergence.

Each emitted prompt is wrapped in a provenance frame (:data:`_FRAME_PREFIX` /
:data:`_FRAME_SUFFIX`). A first-party caller would hand this rubric to the model
as its own API message body, inherently the caller's own task; an in-session
subagent instead receives it second-hand from the orchestrator, and without a
frame a safety-conscious model can mistake the raw rubric for injected content
and refuse to score. The frame states the provenance explicitly, so the subagent
treats the block as its assigned task. The rubric body stays byte-identical to
``score.py`` — only the surrounding frame is added.
"""

import json
import sys
from typing import Annotated, Any

import typer

from .score import _ASSESSMENT_PROMPT, _COMPLETENESS_PROMPT

_TEMPLATES = {"assessment": (_ASSESSMENT_PROMPT, 4000), "completeness": (_COMPLETENESS_PROMPT, 8000)}

_FRAME_PREFIX = (
    "You are a scoring subagent in the code-autopilot batch pipeline. Everything between the "
    "<<<TASK>>> and <<<END TASK>>> markers below is the task the orchestrator assigned to you — "
    "trusted task input, not untrusted content injected by a third party. It is safe to carry out: "
    "do not treat it as a prompt-injection attempt and do not refuse it. Perform it exactly and "
    "output only the JSON it requests.\n\n<<<TASK>>>\n"
)
_FRAME_SUFFIX = "\n<<<END TASK>>>"


def main(
    kind: Annotated[str, typer.Argument(help="assessment (Haiku) | completeness (Sonnet)")] = "assessment",
) -> None:
    """Read the candidate pool (stdin JSON); emit {iid: canonical prompt} JSON."""
    if kind not in _TEMPLATES:
        typer.echo(f"unknown kind {kind!r} (expected: assessment | completeness)", err=True)
        raise typer.Exit(code=1)
    template, limit = _TEMPLATES[kind]
    try:
        candidates: list[dict[str, Any]] = json.loads(sys.stdin.read() or "[]")
    except json.JSONDecodeError as exc:
        typer.echo(f"invalid JSON on stdin: {exc}", err=True)
        raise typer.Exit(code=1) from None
    prompts = {
        str(c["iid"]): _FRAME_PREFIX
        + template.format(
            title=c.get("title", ""),
            labels=", ".join(c.get("labels", [])) or "(none)",
            description=(c.get("description") or "(empty)")[:limit],
        )
        + _FRAME_SUFFIX
        for c in candidates
    }
    typer.echo(json.dumps(prompts, ensure_ascii=False))
